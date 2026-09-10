import json
import os
from typing import Any, Dict

DEFAULT_STATE_FILENAME = ".gitresume_state.json"


def state_path_for(config_path: str) -> str:
    """State file lives next to the resolved gitresume.yaml, not in cwd,
    so it stays correct regardless of where the CLI is invoked from."""
    return os.path.join(os.path.dirname(os.path.abspath(config_path)), DEFAULT_STATE_FILENAME)


def load_state(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(path: str, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
