from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

# GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_MODEL = "gemini-3-flash-preview"

def call_model(model, messages, temperature):
    if model == "gemini":
        return call_gemini(messages, temperature, model_version=GEMINI_MODEL)

    raise ValueError("Unsupported model")

def call_gemini(messages, temperature, model_version="gemini-1.5-flash"):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = convert_messages_to_prompt(messages)

    try:
        response = client.models.generate_content(
            model=model_version,
            contents=prompt,
            config={
                "temperature": temperature
            }
        )
    except Exception:
        raise Exception("Response generation failed")

    return {
        "text": response.text,
        "input_token": 0,
        "output_token": 0
    }

def convert_messages_to_prompt(messages):
    prompt = ""

    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        if role == "system":
            prompt += f"System: {content}\n"
        elif role == "user":
            prompt += f"User: {content}\n"
        elif role == "assistant":
            prompt += f"Assistant: {content}\n"

    prompt += "Assistant:"

    return prompt
