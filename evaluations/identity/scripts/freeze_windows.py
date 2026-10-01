"""Freeze the Development-identity replay windows (step 1 of the identity-gold protocol, before any labelling
or identity code change).

Windows:
- three development windows and one holdout, reusing the frozen clustering-benchmark item files (by path and
  SHA-256, not copied);
- one new multilingual / institutional window exported from a read-only copy of the 2026-09-30
  source-expansion snapshot (``--snapshot PATH``): every item published 2026-09-28 12:00 - 2026-09-30 12:00 UTC.

Each 48 h window is replayed as 4 ticks of 12 h by publication time (items with no publication time go by
fetch time). Writes evaluations/identity/manifest.yaml and windows/*.items.jsonl.

Usage: python evaluations/identity/scripts/freeze_windows.py --snapshot <copy of source-expansion-2026-09-30.db>
"""
import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
CLUSTERING = REPO / "evaluations" / "clustering"
TICK_HOURS = 12

CLUSTERING_WINDOWS = [          # (clustering window id, identity split, why)
    ("2026-08-21", "development", "wayback, 4 outlets incl. Breaking Defense; not used in the Phase 1 replay"),
    ("2026-09-25", "development", "live pipeline data, 6 outlets (Defense News, War on the Rocks)"),
    ("2026-08-31", "holdout", "wayback, 4 outlets; no time overlap with any development window"),
]
ML_WINDOW = ("2026-09-30-multilingual", "development",
             "source-expansion snapshot: en/it/es, institutional sources, roundups, records",
             datetime(2026, 9, 28, 12), datetime(2026, 9, 30, 12))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export_snapshot(db: Path, out: Path, start: datetime, end: datetime) -> int:
    from osint_monitor.processors.language import item_language
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    rows = c.execute(
        "SELECT r.id, r.title, r.content, r.url, r.published_at, r.fetched_at, s.name, s.type "
        "FROM raw_items r JOIN sources s ON s.id = r.source_id ORDER BY r.id").fetchall()
    c.close()
    items = []
    for rid, title, content, url, pub, fetched, source, stype in rows:
        when = pub or fetched
        if not when or not (start.isoformat(" ") <= when[:19] < end.isoformat(" ")):
            continue
        items.append({"id": f"sx-{rid}", "published_at": pub, "fetched_at": fetched, "source": source,
                      "source_type": stype, "title": title, "excerpt": (content or "")[:600], "url": url or "",
                      "lang": item_language(source, title or "")})
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")
    return len(items)


def ticks(start: datetime, end: datetime) -> list[dict]:
    out, t, n = [], start, 1
    while t < end:
        out.append({"tick": n, "from": t.isoformat(), "to": min(t + timedelta(hours=TICK_HOURS), end).isoformat()})
        t, n = t + timedelta(hours=TICK_HOURS), n + 1
    return out


def main() -> int:
    snapshot = Path(sys.argv[sys.argv.index("--snapshot") + 1])
    cm = yaml.safe_load((CLUSTERING / "manifest.yaml").read_text(encoding="utf-8"))
    by_id = {w["id"]: w for w in cm["windows"]}
    windows = []
    for wid, split, why in CLUSTERING_WINDOWS:
        w = by_id[wid]
        items_path = CLUSTERING / w["items_file"]
        assert sha256(items_path) == w["items_sha256"], f"clustering window {wid} changed since it was frozen"
        start, end = datetime.fromisoformat(w["start"]), datetime.fromisoformat(w["end"])
        windows.append({"id": wid, "split": split, "why": why, "start": w["start"], "end": w["end"],
                        "items_file": f"../clustering/{w['items_file']}", "items_sha256": w["items_sha256"],
                        "items": w["stats"]["items"], "source": "clustering benchmark window (frozen)",
                        "ticks": ticks(start, end)})
    wid, split, why, start, end = ML_WINDOW
    out = ROOT / "windows" / f"{wid}.items.jsonl"
    n = export_snapshot(snapshot, out, start, end)
    windows.append({"id": wid, "split": split, "why": why, "start": start.isoformat(), "end": end.isoformat(),
                    "items_file": f"windows/{out.name}", "items_sha256": sha256(out), "items": n,
                    "source": "read-only copy of data/eval/source-expansion-2026-09-30.db (raw_items, sources)",
                    "ticks": ticks(start, end)})
    manifest = {
        "version": 1,
        "frozen_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "note": ("Replay windows frozen before any identity labelling or identity code change. Labels (gold) are "
                 "drafted blind, reviewed by the owner, and only then frozen in gold/ with their own hashes."),
        "tick_hours": TICK_HOURS,
        "windows": windows,
    }
    (ROOT / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, width=110, allow_unicode=True),
                                        encoding="utf-8", newline="\n")
    for w in windows:
        print(w["id"], w["split"], w["items"], "items,", len(w["ticks"]), "ticks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
