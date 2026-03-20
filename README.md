# Multi-Persona CLI Chatbot

A CLI chatbot that supports multiple personas, prompt strategies, and model benchmarking — with streaming output, side-by-side strategy comparison, and concurrent multi-model benchmarking.

## Features

- **Multi-persona support** — switch between personas defined in YAML (tech support, creative writer, socratic tutor, code reviewer)
- **Prompt strategy comparison** — run zero-shot, few-shot, and chain-of-thought side by side for the same prompt
- **Multi-model benchmarking** — run the same prompt across all models concurrently and compare quality, speed, and cost
- **Streaming output** — tokens stream to the terminal in real time in chat mode
- **Token usage tracking** — input, output, and thought tokens shown after each response
- **Cost estimation** — estimated USD cost per response based on real model pricing
- **Conversation logging** — each turn appended as JSONL to `logs/conversations.jsonl`

## Setup

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
DEEPSEEK_API_KEY=your_deepseek_key
OLLAMA_API_KEY=your_ollama_key   # optional — omit to use local Ollama at localhost:11434
```

## CLI Usage

### Chat Mode

Interactive chat with a selected persona and model. Streams response tokens to the terminal in real time.

```bash
# Default: tech_support persona, ollama model
python main.py

# Choose a persona
python main.py --persona creative_writer

# Choose a model
python main.py --persona code_reviewer --model gemini

# Available personas: tech_support, creative_writer, socratic_tutor, code_reviewer
# Available models:   gemini, openai, deepseek, ollama
```

**In-chat commands:**
- `/clear` — clear conversation history
- `/exit` — quit

**Example output:**
```
Chatbot ready. Type '/exit' to quit.
You > How do I reverse a list in Python?
Bot > Generating response... Persona: Tech Support  Model: gemini-2.5-flash
There are several ways to reverse a list in Python...

Input tokens: 42 | Output tokens: 138 | Latency: 1.23s
```

---

### Compare Mode

Runs a single prompt through all three prompt strategies — zero-shot, few-shot, and chain-of-thought — and displays results in a terminal-wide side-by-side table.

```bash
python main.py --compare

# With a specific persona and model
python main.py --compare --persona socratic_tutor --model gemini
```

**Example output:**
```
You > What is recursion?

┌─────────────────────┬─────────────────────┬─────────────────────┐
│ Zero Shot           │ Few Shot            │ Chain of Thought    │
├─────────────────────┼─────────────────────┼─────────────────────┤
│ Recursion is when   │ Great question!     │ Let's think step    │
│ a function calls    │ Recursion means...  │ by step. First...   │
├─────────────────────┼─────────────────────┼─────────────────────┤
│ in: 94              │ in: 115             │ in: 99              │
│ out: 210            │ out: 280            │ out: 340            │
│ 2.1s                │ 2.8s                │ 3.5s                │
└─────────────────────┴─────────────────────┴─────────────────────┘
```

---

### Benchmark Mode

Runs the same prompt across all active models **concurrently** and compares response quality, latency, and estimated cost side by side.

```bash
python main.py --benchmark

# With a specific persona
python main.py --benchmark --persona code_reviewer
```

**Example output:**
```
You > Explain async/await in Python

Benchmarking across all models — Persona: Code Reviewer...
⠋ Running all models concurrently...

┌──────────────────────┬──────────────────────┐
│ gemini-2.5-flash     │ gpt-oss:120b          │
├──────────────────────┼──────────────────────┤
│ Async/await in       │ The async/await       │
│ Python allows...     │ syntax enables...     │
├──────────────────────┼──────────────────────┤
│ in: 88               │ in: 91               │
│ out: 312             │ out: 287             │
│ 3.2s                 │ 5.1s                 │
│ ~$0.00082            │ ~$0.00058            │
└──────────────────────┴──────────────────────┘
```

---

## Personas

Defined in `config/prompts.yaml`. Each persona has a system prompt, temperature, and optional few-shot examples.

| Persona | Key | Behaviour |
|---|---|---|
| Tech Support | `tech_support` | Debugging steps, technical explanations |
| Creative Writer | `creative_writer` | Imaginative, expressive writing |
| Socratic Tutor | `socratic_tutor` | Guides with questions rather than answers |
| Code Reviewer | `code_reviewer` | Reviews code for quality and correctness |

To add a new persona, add an entry to `config/prompts.yaml` and a corresponding entry to `PERSONA_NAME` in `constants.py`.

## Models

| Key | Model | Provider |
|---|---|---|
| `gemini` | gemini-2.5-flash | Google |
| `openai` | gpt-5-mini-2025-08-07 | OpenAI |
| `deepseek` | DeepSeek-V3.2 | DeepSeek |
| `ollama` | gpt-oss:120b | Ollama (remote) |

## Pricing Reference

Approximate cost per 1M tokens used for cost estimation:

| Model | Input | Output |
|---|---|---|
| gemini-2.5-flash | $0.30 | $2.50 |
| gpt-5-mini | $0.25 | $2.00 |
| DeepSeek-V3.2 | $0.28 | $0.42 |
| gpt-oss:120b | $0.039 | $0.19 |
