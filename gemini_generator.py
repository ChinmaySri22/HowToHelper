import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import GenerationConfig

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(app: str, question: str, screenshot_desc: str = "") -> str:
    """
    Sends a prompt to Gemini and returns step-by-step instructions.
    """
    # 1) Build the prompt
    prompt_text = (
        f"You are an expert in {app or 'general computer usage'}. "
        f"A user is working in {app}, screenshot summary: {screenshot_desc}\n\n"
        f"User question: {question}\n"
        "Please reply with clear, numbered, step-by-step instructions."
    )

    # 2) Configure generation parameters
    gen_config = GenerationConfig(
        temperature=0.2,
        max_output_tokens=512
    )

    model = genai.GenerativeModel("models/gemini-2.0-flash")

    # 3) Pass prompt as the first positional argument, not as `prompt=`
    response = model.generate_content(
        prompt_text,
        generation_config=gen_config
    )

    return response.text.strip()
