import json
import os

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")


def save_config(config: dict, path: str = DEFAULT_PATH) -> None:
    with open(path, "w") as f:
        json.dump(config, f, indent=2)


def load_config(path: str = DEFAULT_PATH) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r") as f:
        return json.load(f)