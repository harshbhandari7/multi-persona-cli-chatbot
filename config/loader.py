from pathlib import Path
import yaml
from typing import List

from exceptions import FileNotFoundError
from config.models import PersonaConfig

DEFAULT_PATH = Path(__file__).parent / "prompts.yaml"

def load_personas(path: str=DEFAULT_PATH) -> List[PersonaConfig]:
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
        return data["personas"]
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found at {path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in config: {e}")