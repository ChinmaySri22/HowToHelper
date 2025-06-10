# finetune.py
#!/usr/bin/env python3
import os
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from datasets import load_dataset
from peft import get_peft_model, LoraConfig, TaskType

def main():
    # ─────────── Config from env (with defaults) ───────────
    model_name  = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.1")
    train_file  = os.getenv("TRAIN_FILE", "data/processed/wikihow_train.jsonl")
    val_file    = os.getenv("VAL_FILE",   "data/processed/wikihow_val.jsonl")
    output_dir  = os.getenv("OUTPUT_DIR", "lora-finetuned")
    epochs      = int(os.getenv("EPOCHS",      3))
    batch_size  = int(os.getenv("BATCH_SIZE",  2))
    grad_steps  = int(os.getenv("GRAD_ACC_STEPS", 8))
    lr          = float(os.getenv("LEARNING_RATE", 1e-4))

    # ─────────── Load model & tokenizer ───────────
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # ─────────── Apply LoRA adapters ───────────
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05
    )
    model = get_peft_model(model, peft_config)

    # ─────────── Load & preprocess dataset ───────────
    ds = load_dataset("json", data_files={"train": train_file, "validation": val_file})
    def preprocess(ex):
        prompt = f"### Instruction:\n{ex['instruction']}\n\n### Response:\n{ex['output']}"
        toks = tokenizer(prompt, truncation=True, max_length=512, padding="max_length")
        toks["labels"] = toks["input_ids"].copy()
        return toks
    tokenized = ds.map(preprocess, batched=False, remove_columns=ds["train"].column_names)

    # ─────────── Data collator & Trainer ───────────
    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)
    args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=grad_steps,
        num_train_epochs=epochs,
        learning_rate=lr,
        fp16=True,
        logging_steps=50,
        save_steps=200,
        evaluation_strategy="steps",
        eval_steps=200,
        save_total_limit=3,
        remove_unused_columns=False,
    )
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["validation"],
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    # ─────────── Train & save adapters ───────────
    trainer.train()
    model.save_pretrained(output_dir)
    print(f"✅ Fine‑tuned model saved to {output_dir}")

if __name__ == "__main__":
    main()
