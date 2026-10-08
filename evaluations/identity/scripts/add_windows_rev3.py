"""Identity gold revision 3: add two development windows to evaluations/identity/manifest.yaml.

    python evaluations/identity/scripts/add_windows_rev3.py --snapshot <read-only copy of the live DB, 2026-10-06>

Revision 3 adds owner-verdicted cases from the live windows (Phase 3 relation review identity suspects and the
cross-language regression cases), so the replay needs their items:

- 2026-10-03-live: the relation-review export (eval/relations-review-ui:evaluations/relations/windows/), copied
  byte for byte, so its SHA-256 is unchanged (news items fetched 2026-09-29 12:00 - 10-03 12:00 UTC);
- 2026-10-05-live: new. News (rss) items fetched 2026-10-04 12:00 - 10-06 00:00 UTC from a read-only copy of the
  live DB taken with the SQLite backup API. It holds the RAF Fairford and Siberian plague en/es pairs.

Windows are replayed in 12 h ticks. Existing windows and the holdout are not changed. Read-only on the snapshot.
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


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ticks(start: datetime, end: datetime) -> list[dict]:
    out, t, n = [], start, 1
    while t < end:
        out.append({"tick": n, "from": t.isoformat(), "to": min(t + timedelta(hours=12), end).isoformat()})
        t, n = t + timedelta(hours=12), n + 1
    return out


def export(snapshot: str, path: Path, start: datetime, end: datetime) -> int:
    from osint_monitor.processors.language import item_language
    c = sqlite3.connect(f"file:{snapshot}?mode=ro", uri=True)
    rows = c.execute("SELECT r.id, r.title, r.content, r.url, r.published_at, r.fetched_at, s.name, s.type FROM raw_items r "
                     "JOIN sources s ON s.id = r.source_id WHERE s.type = 'rss' AND r.fetched_at >= ? AND r.fetched_at < ? "
                     "ORDER BY r.id", (start.isoformat(sep=" "), end.isoformat(sep=" "))).fetchall()
    c.close()
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for rid, title, content, url, pub, fetched, src, stype in rows:
            f.write(json.dumps({"excerpt": (content or "")[:600], "fetched_at": fetched, "id": f"s-{rid}",
                                "lang": item_language(src, title or ""), "published_at": pub, "source": src,
                                "source_type": stype, "title": title, "url": url or ""},
                               ensure_ascii=False, sort_keys=True) + "\n")
    return len(rows)


def main() -> int:
    snapshot = sys.argv[sys.argv.index("--snapshot") + 1]
    source_0303 = Path(sys.argv[sys.argv.index("--items-0303") + 1])
    manifest_path = ROOT / "manifest.yaml"
    m = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    have = {w["id"] for w in m["windows"]}
    if {"2026-10-03-live", "2026-10-05-live"} & have:
        print("refusing: revision 3 windows already present")
        return 1
    rel = ROOT / "windows" / "2026-10-03-live.items.jsonl"
    rel.write_bytes(source_0303.read_bytes())
    s1, e1 = datetime(2026, 9, 29, 12), datetime(2026, 10, 3, 12)
    m["windows"].append({
        "id": "2026-10-03-live", "split": "development",
        "why": "revision 3: Phase 3 relation-review identity suspects (T008, T025, T034, T041)",
        "start": s1.isoformat(), "end": e1.isoformat(), "items_file": "windows/2026-10-03-live.items.jsonl",
        "items_sha256": sha256(rel), "items": sum(1 for _ in rel.open(encoding="utf-8")),
        "source": "relation-review export (rss) of the 2026-10-05 backup-API snapshot", "ticks": ticks(s1, e1)})
    new = ROOT / "windows" / "2026-10-05-live.items.jsonl"
    s2, e2 = datetime(2026, 10, 4, 12), datetime(2026, 10, 6, 0)
    n = export(snapshot, new, s2, e2)
    m["windows"].append({
        "id": "2026-10-05-live", "split": "development",
        "why": "revision 3: cross-language regression cases (RAF Fairford, Siberian plague)",
        "start": s2.isoformat(), "end": e2.isoformat(), "items_file": "windows/2026-10-05-live.items.jsonl",
        "items_sha256": sha256(new), "items": n,
        "source": "read-only backup-API copy of the live DB taken 2026-10-06 (rss items)", "ticks": ticks(s2, e2)})
    manifest_path.write_text(yaml.safe_dump(m, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8",
                             newline="\n")
    print(f"added 2026-10-03-live ({m['windows'][-2]['items']} items) and 2026-10-05-live ({n} items)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
