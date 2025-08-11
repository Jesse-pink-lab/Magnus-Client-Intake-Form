import json
import os
from typing import Any, Dict

from magnus_app.pages import PAGES

STATE_FILE = "state.json"

def build_default_state() -> Dict[str, Any]:
    state: Dict[str, Any] = {}

    def walk(fields):
        for fld in fields:
            ftype = fld.get("type")
            if ftype == "group":
                walk(fld.get("fields", []))
                continue
            if ftype == "repeating_group":
                state[fld.get("name")] = []
                continue
            if ftype == "label":
                continue
            name = fld.get("name")
            if ftype == "radio":
                state[name] = "No"
            elif ftype == "checkbox":
                state[name] = False
            else:
                state[name] = ""

    for page in PAGES:
        for section in page.get("sections", []):
            walk(section.get("fields", []))
    return state

def migrate_state(state: Dict[str, Any]) -> Dict[str, Any]:
    default = build_default_state()
    for k, v in default.items():
        state.setdefault(k, v)
    return state

def load_state(path: str) -> Dict[str, Any]:
    state = build_default_state()
    if not os.path.exists(path):
        return state
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        for k, v in data.items():
            if k in state:
                if isinstance(state[k], bool):
                    if isinstance(v, str):
                        state[k] = v.lower() == "yes"
                    else:
                        state[k] = bool(v)
                else:
                    state[k] = v
    except Exception:
        pass
    return migrate_state(state)

def save_state(path: str, state: Dict[str, Any]) -> None:
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=2)
    except Exception:
        pass
