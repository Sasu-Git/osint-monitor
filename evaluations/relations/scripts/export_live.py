"""Export the news items of a read-only DB snapshot copy for one window (relations/windows/<id>.items.jsonl).

    python evaluations/relations/scripts/export_live.py SNAPSHOT_DB WINDOW_ID START END

Only RSS (news) sources are exported: structured records (seismic, ADS-B, CVE...) are not Developments that
typed relations connect. The snapshot is opened with mode=ro; no database is written.
"""
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(db: str, window_id: str, start: str, end: str) -> None:
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    rows = c.execute(
        "SELECT r.id, r.title, r.content, r.url, r.published_at, r.fetched_at, s.name, s.type "
        "FROM raw_items r JOIN sources s ON s.id = r.source_id "
        "WHERE s.type = 'rss' AND r.fetched_at >= ? AND r.fetched_at < ? ORDER BY r.id",
        (start.replace("T", " "), end.replace("T", " "))).fetchall()
    c.close()
    path = ROOT / "windows" / f"{window_id}.items.jsonl"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for rid, title, content, url, pub, fetched, src, stype in rows:
            f.write(json.dumps({"id": f"s-{rid}", "published_at": pub, "fetched_at": fetched, "source": src,
                                "source_type": stype, "title": title, "excerpt": (content or "")[:600],
                                "url": url or ""}, ensure_ascii=False, sort_keys=True) + "\n")
    print(len(rows), "items ->", path, hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == "__main__":
    main(*sys.argv[1:5])
