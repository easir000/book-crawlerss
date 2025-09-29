# crawler/state.py
import json
from pathlib import Path

_STATE_FILE = Path("crawler/.last_category")

def load_last_category() -> str:
    if _STATE_FILE.exists():
        return _STATE_FILE.read_text().strip()
    return ""

def save_last_category(url: str):
    _STATE_FILE.parent.mkdir(exist_ok=True)
    _STATE_FILE.write_text(url)