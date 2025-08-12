import json, os, tempfile, datetime, platform
from typing import List, Dict

_MAX = 10
_FILE = "mru.json"


def _base_dir() -> str:
    sys = platform.system()
    if sys == "Windows":
        root = os.environ.get("APPDATA", os.path.expanduser("~"))
        return os.path.join(root, "Magnus")
    elif sys == "Darwin":
        return os.path.join(os.path.expanduser("~/Library/Application Support"), "Magnus")
    else:
        return os.path.join(os.path.expanduser("~/.local/share"), "Magnus")

def _path() -> str:
    d = _base_dir()
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, _FILE)

def _now_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def get_mru() -> List[Dict]:
    p = _path()
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []

def _write_atomic(path: str, data: List[Dict]) -> None:
    fd, tmp = tempfile.mkstemp(prefix=".tmp", dir=os.path.dirname(path))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        os.replace(tmp, path)
    finally:
        try:
            os.remove(tmp)
        except Exception:
            pass

def touch_mru(path: str) -> None:
    items = [i for i in get_mru() if i.get("path") != path]
    items.insert(0, {"path": path, "last_opened": _now_str()})
    _write_atomic(_path(), items[:_MAX])

def remove_from_mru(path: str) -> None:
    items = [i for i in get_mru() if i.get("path") != path]
    _write_atomic(_path(), items)
