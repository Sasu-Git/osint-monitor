"""Owner verdicts for the identity review: stored apart from the draft labels, written deterministically.

``review/owner-verdicts.yaml`` maps every case id (sorted) to
  verdict:          SAME_DEVELOPMENT | DIFFERENT_DEVELOPMENT | AMBIGUOUS | ACCEPT | null (unreviewed)
  confidence:       high | medium | low | null
  boundary_reason:  same_occurrence | follow_up_update | distinct_action | commentary_or_analysis | roundup |
                    unclear | null
  note:             free text | null
  reviewed_at:      UTC ISO time of the last change | null
``ACCEPT`` (allowed when editing the file by hand) means the draft label. The draft labels
(``review/draft-labels.json``) are never written here or anywhere else by the review tools.
"""
from __future__ import annotations

import os
import threading
from datetime import datetime
from pathlib import Path

import yaml

REVIEW = Path(__file__).resolve().parents[1] / "review"
VERDICTS_FILE = REVIEW / "owner-verdicts.yaml"
VERDICTS = ("SAME_DEVELOPMENT", "DIFFERENT_DEVELOPMENT", "AMBIGUOUS")
CONFIDENCE = ("high", "medium", "low")
BOUNDARY = ("same_occurrence", "follow_up_update", "distinct_action", "commentary_or_analysis", "roundup", "unclear")
FIELDS = ("verdict", "confidence", "boundary_reason", "note", "reviewed_at")
HEADER = ("# Owner verdicts for the Development-identity review (see scripts/verdicts.py for the fields).\n"
          "# Draft labels live in draft-labels.json and are never changed. Nothing is frozen until review ends.\n")

_lock = threading.Lock()


def blank() -> dict:
    return {f: None for f in FIELDS}


def load(case_ids: list[str], path: Path = VERDICTS_FILE) -> dict[str, dict]:
    """Verdicts for every case id; unknown or missing entries are blank. Older files that also carried a
    ``proposed`` copy of the draft label are read without it."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        raw = {}
    out = {}
    for cid in case_ids:
        entry = raw.get(cid) or {}
        out[cid] = {f: entry.get(f) for f in FIELDS}
    return out


def dump(verdicts: dict[str, dict]) -> str:
    ordered = {cid: {f: verdicts[cid].get(f) for f in FIELDS} for cid in sorted(verdicts)}
    return HEADER + yaml.safe_dump(ordered, sort_keys=False, allow_unicode=True, width=120)


def save(verdicts: dict[str, dict], path: Path = VERDICTS_FILE) -> None:
    """Atomic, deterministic write (sorted case ids, fixed field order)."""
    with _lock:
        tmp = path.with_suffix(".yaml.tmp")
        tmp.write_text(dump(verdicts), encoding="utf-8", newline="\n")
        os.replace(tmp, path)


def validate(entry: dict) -> dict:
    """A verdict update from the review page, checked against the allowed values."""
    clean = blank()
    v = entry.get("verdict")
    if v is not None and v not in VERDICTS:
        raise ValueError(f"verdict must be one of {VERDICTS} or null")
    c = entry.get("confidence") or None
    if c is not None and c not in CONFIDENCE:
        raise ValueError(f"confidence must be one of {CONFIDENCE}")
    b = entry.get("boundary_reason") or None
    if b is not None and b not in BOUNDARY:
        raise ValueError(f"boundary_reason must be one of {BOUNDARY}")
    note = (entry.get("note") or "").strip() or None
    clean.update(verdict=v, confidence=c, boundary_reason=b, note=note[:2000] if note else None,
                 reviewed_at=datetime.utcnow().isoformat(timespec="seconds") + "Z" if v else None)
    return clean
