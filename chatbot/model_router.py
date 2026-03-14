from dotenv import load_dotenv
from google import genai
import os
from rich.console import Console
from openai import OpenAI

from constants import GEMINI_MODEL, OPENAI_MODEL

load_dotenv()

console = Console()

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

def call_model(model, messages, temperature):
    if model == "gemini":
        return call_gemini(messages, temperature, model_version=GEMINI_MODEL)
    elif model == "openai":
        return call_openai(messages, temperature, model_version=OPENAI_MODEL)

    raise ValueError("Unsupported model")

def call_gemini(messages, temperature, model_version="gemini-1.5-flash"):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = convert_messages_to_prompt(messages)

    full_text = ""
    input_tokens = 0
    thought_tokens = 0
    output_tokens = 0

    try:
        stream = client.models.generate_content_stream(
            model=model_version,
            contents=prompt,
            config={
                "temperature": temperature
            }
        )
        for chunk in stream:
            if chunk.text:
                console.print(chunk.text, end="")
                full_text += chunk.text
            
            if chunk.usage_metadata:
                input_tokens = chunk.usage_metadata.prompt_token_count
                thought_tokens = chunk.usage_metadata.thoughts_token_count
                output_tokens = chunk.usage_metadata.candidates_token_count

    except Exception:
        raise Exception("Response generation failed")

    return {
        "text": full_text,
        "input_tokens": input_tokens,
        "thought_tokens": thought_tokens,
        "output_tokens": output_tokens
    }

def call_openai(messages, temperature, model_version="gpt-5-mini-2025-08-07"):
    client = OpenAI()

    full_text = ""
    input_tokens = 0
    output_tokens = 0
    thought_tokens = 0

    try:
        stream = client.responses.create(
            model=model_version,
            input=messages,
            reasoning={ "effort": "medium" },
            stream=True
        )
        for event in stream:
            if event.type == "response.output_text.delta":
                console.print(event.text, end="")
                full_text += event.delta
            elif event.type == "response.completed":
                input_tokens = event.response.usage.input_tokens
                output_tokens = event.response.usage.output_tokens
        
    except Exception:
        raise Exception("Response generation failed")
    
    return {
        "text": full_text,
        "input_tokens": input_tokens,
        "thought_tokens": thought_tokens,
        "output_tokens": output_tokens
    }
