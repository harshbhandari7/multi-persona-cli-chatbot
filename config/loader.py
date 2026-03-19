from pathlib import Path
import yaml
from typing import List

from exceptions import ConfigNotFoundError
from config.models import PersonaConfig

DEFAULT_PATH = Path(__file__).parent / "prompts.yaml"

def load_personas(path: str=DEFAULT_PATH) -> PersonaConfig:
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
        return data["personas"]
    except ConfigNotFoundError:
        raise ConfigNotFoundError(f"Config not found at {path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in config: {e}")