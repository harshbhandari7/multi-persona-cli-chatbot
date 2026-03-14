from pydantic import BaseModel
from typing import Optional

class FewShotExample(BaseModel):
    user: str
    assistant: str

class PersonaConfig(BaseModel):
    system_prompt: str
    temperature: float
    few_shot_examples: list[FewShotExample] = []
    cot_prefix: Optional[str] = None
