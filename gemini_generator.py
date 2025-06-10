# gemini_generator.py
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# ─────────── Config ───────────
BASE_MODEL     = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.1")
ADAPTER_PATH   = os.getenv("LOCAL_MODEL_PATH", "lora-finetuned")
TEMPERATURE    = float(os.getenv("GEN_TEMP",      0.2))
MAX_NEW_TOKENS = int(os.getenv("GEN_MAX_TOKENS", 512))
DEVICE         = "cuda" if torch.cuda.is_available() else "cpu"

# ─────────── Load tokenizer ───────────
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)

# ─────────── Load model (with or without LoRA) ───────────
if os.path.isdir(ADAPTER_PATH):
    # 1) Load base
    base = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    # 2) Wrap with LoRA adapters
    model = PeftModel.from_pretrained(base, ADAPTER_PATH, torch_dtype=torch.float16)
    print(f"🔥 Loaded LoRA‑fine‑tuned model from `{ADAPTER_PATH}`")
else:
    # Fallback: use base model only
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    print(f"⚠️  Adapter folder `{ADAPTER_PATH}` not found; using base `{BASE_MODEL}`")

model.eval()

def ask_gemini(app: str, question: str, screenshot_desc: str = "") -> str:
    """
    Generate step‑by‑step instructions with your local (fine‑tuned) model.
    """
    prompt = (
        f"You are an expert in {app or 'general computer usage'}.\n"
        f"Screenshot summary: {screenshot_desc}\n\n"
        f"User question: {question}\n"
        "Please reply with clear, numbered, step-by-step instructions."
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            do_sample=False,
            temperature=TEMPERATURE,
            max_new_tokens=MAX_NEW_TOKENS,
            pad_token_id=tokenizer.eos_token_id,
        )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text[len(prompt):].strip() if text.startswith(prompt) else text.strip()
