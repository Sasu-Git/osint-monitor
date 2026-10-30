"""Where tier runs spend their time (read-only): per tier, the phases of each run -- collection, wait for the write
lock (another tier's write phase), DB write, post-processing -- and, for runs that post-processed, each stage.

    python scripts/run_timing.py --db PATH [--since 2026-10-27T00:00] [--tier warm]

Reads the ``_seconds`` key that ``pipeline.run_tier`` stores with each run (runs from before it existed are skipped).
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import statistics
import sys
from collections import defaultdict
from pathlib import Path

PHASES = ("collection", "lock_wait", "db_write", "post_processing")


def _q(values: list[float]) -> str:
    v = sorted(values)
    return f"{statistics.median(v):7.0f} {v[int(0.9 * (len(v) - 1))]:7.0f} {v[-1]:7.0f}"


def report(conn: sqlite3.Connection, since: str, tier: str | None = None) -> str:
    sql = ("SELECT tier, (julianday(finished_at) - julianday(started_at)) * 86400, stages FROM pipeline_runs "
           "WHERE kind = 'tier' AND finished_at IS NOT NULL AND started_at >= ?" + (" AND tier = ?" if tier else ""))
    rows = conn.execute(sql, (since, tier) if tier else (since,)).fetchall()
    by_tier: dict[str, list[tuple[float, dict]]] = defaultdict(list)
    for t, total, stages in rows:
        seconds = (json.loads(stages) if isinstance(stages, str) else (stages or {})).get("_seconds")
        if seconds:
            by_tier[t].append((total, seconds))
    out = []
    for t in ("hot", "warm", "cold"):
        if t not in by_tier:
            continue
        runs = by_tier[t]
        out.append(f"\n{t}: {len(runs)} timed runs since {since}   (seconds: median / p90 / max)")
        out.append(f"  {'total':16s} {_q([r[0] for r in runs])}")
        for p in PHASES:
            vals = [s[p] for _, s in runs if p in s]
            if vals:
                out.append(f"  {p:16s} {_q(vals)}   ({len(vals)} runs)")
        stage_vals: dict[str, list[float]] = defaultdict(list)
        for _, s in runs:
            for k, v in s.items():
                if k not in PHASES:
                    stage_vals[k].append(v)
        if stage_vals:
            out.append("  post-processing stages (slowest median first):")
            for k, vals in sorted(stage_vals.items(), key=lambda kv: -statistics.median(kv[1])):
                out.append(f"    {k:14s} {_q(vals)}")
    return "\n".join(out) if out else f"no timed runs since {since}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", required=True, type=Path)
    ap.add_argument("--since", default="2000-01-01")
    ap.add_argument("--tier", choices=("hot", "warm", "cold"))
    a = ap.parse_args(argv)
    conn = sqlite3.connect(f"file:{a.db.as_posix()}?mode=ro", uri=True)
    print(report(conn, a.since.replace("T", " "), a.tier))
    return 0


if __name__ == "__main__":
    sys.exit(main())
