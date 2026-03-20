def build_one_shot(system_prompt, user_prompt, history=None):
    messages = [
        { "role": "system", "content": system_prompt }
    ]

    if history:
        messages.extend(history)

    messages.append({ "role": "user", "content": user_prompt })

    return messages

def build_few_shot(system_prompt, user_prompt, persona, history=None):
    messages = [
        { "role": "system", "content": system_prompt }
    ]

    examples = persona.get("few_shot_examples", [])

    messages.extend(examples)

    if history:
        messages.extend(history)
    
    messages.append({ "role": "user", "content": user_prompt })
    return messages

def build_chain_of_thought(system_prompt, user_prompt, history=None):
    messages = [
        { "role": "system", "content": system_prompt }
    ]

    if history:
        messages.extend(history)

    messages.append(
        { "role": "user", "content": user_prompt + "\n Think step by step."}
    )

    return messages


def build_prompt(persona, user_prompt, strategy="zero_shot", history=None):
    system_prompt = persona["system_prompt"]
    if strategy == "zero_shot":
        return build_one_shot(system_prompt, user_prompt, history)
    elif strategy == "few_shot":
        return build_few_shot(system_prompt, user_prompt, persona, history)
    elif strategy == "cot":
        return build_chain_of_thought(system_prompt, user_prompt, history)

    raise ValueError("Invalid prompt strategy")