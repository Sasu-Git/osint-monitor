from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent          # chrono-replay-v1/


def sha256_file(path: Path | str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def dumps(obj) -> str:
    """Canonical JSON (sorted keys, no NaN, UTF-8 characters kept): the only serialisation used for trace rows."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"), default=_default)


def _default(o):
    if isinstance(o, (set, frozenset)):
        return sorted(o)
    if hasattr(o, "isoformat"):
        return o.isoformat()
    raise TypeError(f"not serialisable: {type(o)}")


def write_lines(path: Path, rows: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(r + "\n")


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=1, default=_default) + "\n")


def load_pins() -> dict:
    return json.loads((HERE / "PINS.json").read_text(encoding="utf-8"))


def verify(path: Path, expected: str, what: str) -> None:
    got = sha256_file(path)
    if got != expected:
        raise SystemExit(f"STOP: sha256 mismatch for {what} ({path}): expected {expected}, got {got}")
