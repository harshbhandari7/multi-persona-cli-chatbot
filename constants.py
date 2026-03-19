from enum import Enum

# GEMINI_MODEL = "gemini-1.5-flash"
# GEMINI_MODEL = "gemini-3-flash-preview"
GEMINI_MODEL = "gemini-2.5-flash"
OPENAI_MODEL = "gpt-5-mini-2025-08-07"
DEEPSEEK_MODEL = "DeepSeek-V3.2"
OLLAMA_MODEL = "gpt-oss:120b"

PROMPT_STRATEGIES = ["zero_shot", "few_shot", "cot"]

class PERSONA_NAME(Enum):
    tech_support="Tech Support"
    creative_writer="Creative Writer"
    socratic_tutor="Socratic Tutor"
    code_reviewer="Code Reviewer"

class MODEL_VERSION(Enum):
    gemini=GEMINI_MODEL
    openai=OPENAI_MODEL
    deepseek=DEEPSEEK_MODEL
    ollama=OLLAMA_MODEL
