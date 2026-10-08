"""Seal a multilingual identity holdout window (cross-language stage), before any tuning is judged on it.

    python evaluations/identity/scripts/seal_xlang_holdout.py --live-db PATH --snapshot-dir DIR

1. Takes a SQLite backup-API copy of the live DB (source opened mode=ro) into --snapshot-dir.
2. Exports the news (rss) items fetched 2026-10-06 00:00 - 2026-10-08 00:00 UTC, after every development window, into
   evaluations/identity/holdout-xlang/2026-10-07-live.items.jsonl.
3. Writes holdout-xlang/SEALED.yaml: the window, the counts per language, the SHA-256 of the items and of the
   snapshot, and the rule.

Prints counts only, never item content. Labelling happens only after the cross-language stage is frozen: a blind
annotator draft, owner verdicts, freeze, then one score.
"""
import hashlib
import json
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
START, END = "2026-10-06 00:00:00", "2026-10-08 00:00:00"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main() -> int:
    live = Path(sys.argv[sys.argv.index("--live-db") + 1])
    snapdir = Path(sys.argv[sys.argv.index("--snapshot-dir") + 1])
    out_dir = ROOT / "holdout-xlang"
    if (out_dir / "SEALED.yaml").exists():
        print("refusing: already sealed")
        return 1
    snapdir.mkdir(parents=True, exist_ok=True)
    snap = snapdir / f"live-{datetime.now(timezone.utc):%Y%m%d-%H%M%S}.db"
    src = sqlite3.connect(f"file:{live.as_posix()}?mode=ro", uri=True)
    dst = sqlite3.connect(snap)
    src.backup(dst)
    dst.execute("PRAGMA journal_mode=DELETE")
    dst.close()
    src.close()
    from osint_monitor.processors.language import item_language
    c = sqlite3.connect(f"file:{snap.as_posix()}?mode=ro", uri=True)
    rows = c.execute("SELECT r.id, r.title, r.content, r.url, r.published_at, r.fetched_at, s.name, s.type FROM raw_items r "
                     "JOIN sources s ON s.id = r.source_id WHERE s.type = 'rss' AND r.fetched_at >= ? AND r.fetched_at < ? "
                     "ORDER BY r.id", (START, END)).fetchall()
    c.close()
    out_dir.mkdir(exist_ok=True)
    items = out_dir / "2026-10-07-live.items.jsonl"
    langs = Counter()
    with open(items, "w", encoding="utf-8", newline="\n") as f:
        for rid, title, content, url, pub, fetched, src_name, stype in rows:
            lang = item_language(src_name, title or "")
            langs[lang or "?"] += 1
            f.write(json.dumps({"excerpt": (content or "")[:600], "fetched_at": fetched, "id": f"s-{rid}", "lang": lang,
                                "published_at": pub, "source": src_name, "source_type": stype, "title": title,
                                "url": url or ""}, ensure_ascii=False, sort_keys=True) + "\n")
    sealed = {"sealed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "window": {"id": "2026-10-07-live", "split": "holdout", "fetched_from": START, "fetched_to": END},
              "items": len(rows), "languages": dict(langs),
              "sha256": {"2026-10-07-live.items.jsonl": sha256(items), "snapshot": sha256(snap)},
              "snapshot": str(snap),
              "rule": "Do not open, print, replay or label anything here until the cross-language stage is frozen. "
                      "Then: candidate pairs from this window, blind annotator draft, owner verdicts, freeze, one score."}
    (out_dir / "SEALED.yaml").write_text(yaml.safe_dump(sealed, sort_keys=False, allow_unicode=True), encoding="utf-8",
                                         newline="\n")
    print(f"sealed: {len(rows)} items, languages {dict(langs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
