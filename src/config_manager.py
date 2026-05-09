import json
import os
from src.paths import get_root

DEFAULT_PATH = os.path.join(get_root(), "config.json")


def save_config(config: dict, path: str = DEFAULT_PATH) -> None:
    with open(path, "w") as f:
        json.dump(config, f, indent=2)


def load_config(path: str = DEFAULT_PATH) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r") as f:
        return json.load(f)