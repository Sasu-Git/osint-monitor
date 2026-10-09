"""Replay relation windows through the current pipeline (temporary databases only) and keep what the relation
gold needs: system Developments, their production Situation, and per-item places and actors.

    python evaluations/relations/scripts/replay_windows.py development
    python evaluations/relations/scripts/replay_windows.py holdout      # sealed: prints counts only

Uses the identity benchmark's tick replay (evaluations/identity/scripts/replay_current.py) unchanged, in 12 h
ticks. Situation grouping is whatever the checked-out code does (production: create_by actor_set).
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "identity" / "scripts"))

import yaml  # noqa: E402


def windows(split: str) -> list[dict]:
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    out = []
    for w in manifest["windows"]:
        if w["split"] != split:
            continue
        path = (ROOT / w["items_file"]).resolve()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == w["items_sha256"], f"{w['id']}: items changed"
        start, end = datetime.fromisoformat(w["start"]), datetime.fromisoformat(w["end"])
        ticks, t, n = [], start, 1
        while t < end:
            ticks.append({"tick": n, "from": t.isoformat(), "to": min(t + timedelta(hours=manifest["tick_hours"]),
                                                                     end).isoformat()})
            t, n = t + timedelta(hours=manifest["tick_hours"]), n + 1
        out.append({**w, "items_file": str(path), "ticks": ticks})
    return out


def main(split: str) -> None:
    import replay_current
    out_dir = ROOT / ("runs" if split == "development" else "holdout" / Path("runs"))
    out_dir.mkdir(parents=True, exist_ok=True)
    for w in windows(split):
        trace = replay_current.replay(w)
        keep = {"window": w["id"], "split": split, "shift_hours": trace["shift_hours"],
                "developments": {k: {f: v.get(f) for f in ("summary", "members", "principals", "sources",
                                                          "corroboration", "situation")}
                                 for k, v in trace["developments"].items()},
                "situations": trace["situations"],
                "items": {i: {f: r[f] for f in ("source", "lang", "title", "excerpt", "published_at", "stored",
                                                "developments", "places", "entities", "roundup")}
                          for i, r in trace["items"].items()}}
        path = out_dir / f"{w['id']}.json"
        path.write_text(json.dumps(keep, indent=1, ensure_ascii=False, sort_keys=True, default=str) + "\n",
                        encoding="utf-8", newline="\n")
        print(w["id"], len(keep["developments"]), "Developments,", len(keep["items"]), "items",
              hashlib.sha256(path.read_bytes()).hexdigest()[:12], flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
