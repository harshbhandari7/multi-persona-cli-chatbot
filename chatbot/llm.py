import time

from chatbot.prompt_engine import build_prompt
from chatbot.model_router import call_model

def generate_response(
    user,
    persona,
    history,
    strategy="zero_shot",
    model="gemini"
):
    temperature = persona.get("temperature", 0.5)

    messages = build_prompt(
        persona=persona,
        user_prompt=user,
        strategy=strategy,
        history=history,
    )

    start = time.monotonic()
    result = call_model(
        model=model,
        messages=messages,
        temperature=temperature
    )
    latency = time.monotonic() - start

    return {
        "text": result["text"],
        "input_tokens": result["input_tokens"],
        "thought_tokens": result["thought_tokens"],
        "output_tokens": result["output_tokens"],
        "latency": latency
    }
