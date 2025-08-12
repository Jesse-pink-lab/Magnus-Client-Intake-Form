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
    state = dict(state)

    if "investment_objective" not in state:
        ranks = state.get("investment_objectives") or {}
        key_map = {
            "speculation": "Speculation",
            "capital_appreciation": "Capital Appreciation",
            "income": "Income",
            "growth_and_income": "Growth and Income",
        }
        best = None
        best_rank = None
        if isinstance(ranks, dict):
            for k, v in ranks.items():
                label = key_map.get(k)
                if label is None:
                    continue
                try:
                    r = int(v)
                except Exception:
                    continue
                if best_rank is None or r < best_rank:
                    best_rank, best = r, label
        if best:
            state["investment_objective"] = best
        state.pop("investment_objectives", None)
        state.pop("investment_purpose", None)

    if "assets_held_away_total" not in state and "assets_held_away" in state:
        state["assets_held_away_total"] = state.pop("assets_held_away")

    aliases = {
        "trusted_full_name": "tc_full_name",
        "trusted_relationship": "tc_relationship",
        "trusted_phone": "tc_phone",
        "trusted_email": "tc_email",
        "tcp_full_name": "tc_full_name",
        "tcp_relationship": "tc_relationship",
        "tcp_phone": "tc_phone",
        "tcp_email": "tc_email",
    }
    for old, new in aliases.items():
        if old in state and new not in state:
            state[new] = state[old]

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
    """Atomically persist *state* to *path*.

    Writes to a temporary file and replaces the target on success. Any
    exceptions are swallowed to avoid crashing the UI."""
    if not path:
        return
    try:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        tmp = f"{path}.tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=2)
        os.replace(tmp, path)
    except Exception:
        pass
