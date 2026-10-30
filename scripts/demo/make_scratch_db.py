"""Copy the live intelligence database to a scratch file for the local demo (read-only on the source).

    python scripts/demo/make_scratch_db.py --src LIVE.db --dst data/demo/intel-scratch.db

The source is opened with mode=ro and copied with the SQLite backup API (consistent even while the daemon
writes). The copy is switched to journal_mode=DELETE so it is one self-contained file that can be marked
read-only. Refuses a destination that is the source or any data/osint.db.
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    a = ap.parse_args(argv)
    src, dst = Path(a.src).resolve(), Path(a.dst).resolve()
    if dst == src or dst.name == "osint.db" or "osint-monitor-daemon" in dst.parts:
        print(f"REFUSED: destination {dst} is a live or production path", file=sys.stderr)
        return 2
    if "demo" not in dst.parts:
        print(f"REFUSED: destination {dst} is not under a demo folder", file=sys.stderr)
        return 2
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_suffix(".tmp")
    tmp.unlink(missing_ok=True)

    source = sqlite3.connect(f"file:{src.as_posix()}?mode=ro", uri=True)
    target = sqlite3.connect(tmp)
    source.backup(target)
    source.close()
    target.execute("PRAGMA journal_mode=DELETE")
    check = target.execute("PRAGMA quick_check").fetchone()[0]
    one = lambda q: target.execute(q).fetchone()[0]
    stats = {"schema_version": one("SELECT value FROM schema_meta WHERE key = 'schema_version'"), "events": one("SELECT count(*) FROM events"),
             "max_event_id": one("SELECT max(id) FROM events"), "raw_items": one("SELECT count(*) FROM raw_items"),
             "situations": one("SELECT count(*) FROM situations")}
    target.close()
    if check != "ok":
        tmp.unlink(missing_ok=True)
        print(f"FAILED: quick_check {check}", file=sys.stderr)
        return 1
    tmp.replace(dst)
    print(f"scratch {dst}  " + "  ".join(f"{k}={v}" for k, v in stats.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
