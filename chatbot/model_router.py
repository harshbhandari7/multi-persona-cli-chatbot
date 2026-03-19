from dotenv import load_dotenv
from google import genai
import os
from rich.console import Console
from openai import OpenAI
from ollama import Client

from constants import GEMINI_MODEL, OPENAI_MODEL, DEEPSEEK_MODEL, OLLAMA_MODEL

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

def call_model(model, messages, temperature, silent=False):
    if model == "gemini":
        return call_gemini(messages, temperature, model_version=GEMINI_MODEL, silent=silent)
    elif model == "openai":
        return call_openai(messages, temperature, model_version=OPENAI_MODEL, silent=silent)
    elif model == "deepseek":
        return call_deepseek(messages, temperature, model_version=DEEPSEEK_MODEL, silent=silent)
    elif model == "ollama":
        return call_ollama(messages, temperature, model_version=OLLAMA_MODEL, silent=silent)

    raise ValueError("Unsupported model")

def call_gemini(messages, temperature, model_version="gemini-1.5-flash", silent=False):
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
                if not silent:
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

def call_openai(messages, temperature, model_version="gpt-5-mini-2025-08-07", silent=False):
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
                if not silent:
                    console.print(event.delta, end="")
                full_text += event.delta
            elif event.type == "response.completed":
                input_tokens = event.response.usage.input_tokens
                output_tokens = event.response.usage.output_tokens
    except Exception as e:
        raise Exception("Response generation failed", e)
    
    return {
        "text": full_text,
        "input_tokens": input_tokens,
        "thought_tokens": thought_tokens,
        "output_tokens": output_tokens
    }

def call_deepseek(messages, temperature, model_version="DeepSeek-V3.2", silent=False):
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )
    full_text = ""
    input_tokens = 0
    output_tokens = 0
    thought_tokens = 0

    try:
        stream = client.chat.completions.create(
            model=model_version,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if not silent:
                console.print(delta, end="")
            full_text += delta

        input_tokens = stream.response.usage.prompt_tokens
        output_tokens = stream.response.usage.completion_tokens 
    except Exception:
        raise Exception("Response generation failed")
    
    return {
        "text": full_text,
        "input_tokens": input_tokens,
        "thought_tokens": thought_tokens,
        "output_tokens": output_tokens
    }

def call_ollama(messages, temperature, model_version="gpt-oss:120b", silent=False):
    client = Client(
        host="https://ollama.com",
        headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
    )
    full_text = ""
    input_tokens = 0
    thought_tokens = 0
    output_tokens = 0

    try:
        stream = client.chat(
            model_version,
            messages=messages,
            stream=True,
            options={ "temperature": temperature }
        )
        for chunk in stream:
            if "message" in chunk and "content" in chunk["message"]:
                content = chunk['message']['content']
                full_text += content
                if not silent:
                    console.print(content, end="")
            if chunk.get("done"):
                input_tokens = chunk.get("prompt_eval_count", 0)
                output_tokens = chunk.get("eval_count", 0)
    except Exception:
        raise Exception("Response generation failed")
    
    return {
        "text": full_text,
        "input_tokens": input_tokens,
        "thought_tokens": thought_tokens,
        "output_tokens": output_tokens
    }
