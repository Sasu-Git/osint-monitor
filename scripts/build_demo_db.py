"""Build a separate demo database from real collected items (optional; for the localhost demo).

    python scripts/build_demo_db.py --snapshot data/eval/snapshot-2026-09-29.db \
        --start 2026-09-25T00:00 --end 2026-09-29T12:00

Replays items that were really collected (by their original fetched_at) through the production
pipeline stages in simulated ticks, so every development, classification, ranking and situation
in the demo DB is exactly what the pipeline would have produced at that time. Nothing is
invented; the source snapshot is opened read-only and never modified; the real data/osint.db is
never touched. Network stages (full-text fetch, geocoding) are skipped.

The only non-production detail: event detection times (persist_clusters stamps utcnow) are pinned
to the simulated tick, so first_reported_at is the tick at which the event would have formed.

Then serve it:  OSINT_DB_URL=sqlite:///data/demo/osint-demo.db python main.py serve
"""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


class _Clock:
    """Stand-in for datetime in the clustering module: utcnow() returns the simulated tick."""
    now: datetime | None = None

    def __init__(self, real):
        self._real = real

    def utcnow(self):
        return self.now

    def __getattr__(self, name):
        return getattr(self._real, name)

    def __call__(self, *a, **k):
        return self._real(*a, **k)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", required=True, help="read-only source DB (a snapshot copy of collected data)")
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True, help="items fetched at or after this time are excluded")
    ap.add_argument("--out", default=str(ROOT / "data" / "demo" / "osint-demo.db"))
    ap.add_argument("--tick-hours", type=float, default=2.0)
    ap.add_argument("--force", action="store_true", help="replace an existing demo DB")
    args = ap.parse_args(argv)

    out = Path(args.out).resolve()
    if out == (ROOT / "data" / "osint.db").resolve():
        sys.exit("refusing to write the real database")
    if out.exists():
        if not args.force:
            sys.exit(f"{out} exists; pass --force to rebuild it")
        out.unlink()
    out.parent.mkdir(parents=True, exist_ok=True)
    url = f"sqlite:///{out.as_posix()}"
    os.environ["OSINT_DB_URL"] = url

    from osint_monitor.core.database import Event, get_session, init_db
    from osint_monitor.core.models import RawItemModel
    from osint_monitor.processors import clustering
    from osint_monitor.processors.clustering import cluster_recent_items, persist_clusters
    from osint_monitor.processors.corroboration import compute_corroboration_score
    from osint_monitor.processors.development import classify_events, rank_events
    from osint_monitor.processors.pipeline import process_new_items
    from osint_monitor.processors.principals import mark_principal_actors
    from osint_monitor.processors.situations import assign_situations, get_grouper
    from osint_monitor.processors.summaries import summarize_events

    init_db(url)
    session = get_session(url)
    start, end = datetime.fromisoformat(args.start), datetime.fromisoformat(args.end)
    src = sqlite3.connect(f"file:{Path(args.snapshot).resolve().as_posix()}?mode=ro", uri=True)
    rows = src.execute(
        "select r.title, r.content, r.url, r.published_at, r.fetched_at, r.external_id, s.name, s.type "
        "from raw_items r join sources s on s.id = r.source_id where r.fetched_at >= ? and r.fetched_at < ? "
        "order by r.fetched_at", (start.isoformat(sep=" "), end.isoformat(sep=" "))).fetchall()
    src.close()
    parse = lambda v: datetime.fromisoformat(str(v)) if v else None      # noqa: E731
    items = [RawItemModel(title=t or "", content=c or "", url=u or "", published_at=parse(p), fetched_at=parse(f),
                          external_id=e, source_name=n, source_type=ty) for t, c, u, p, f, e, n, ty in rows]
    print(f"{len(items)} collected items fetched in [{start}, {end})")

    clock = _Clock(clustering.datetime)
    clustering.datetime = clock
    grouper = get_grouper()
    tick, step, i = start, timedelta(hours=args.tick_hours), 0
    try:
        while tick < end:
            tick = min(tick + step, end)
            batch = []
            while i < len(items) and items[i].fetched_at < tick:
                batch.append(items[i])
                i += 1
            if not batch:
                continue
            clock.now = tick
            new = process_new_items(session, batch)["new_items"]
            if not new:
                continue
            persist_clusters(session, cluster_recent_items(session, now=tick))
            mark_principal_actors(session, now=tick)
            classify_events(session, now=tick)
            for ev in session.query(Event).all():
                sc = compute_corroboration_score(session, ev.id)
                ev.source_count = sc.get("independent_sources", 0)
                ev.admiralty_rating = sc.get("admiralty_rating")
                ev.corroboration_level = sc.get("corroboration_level", "UNVERIFIED")
                ev.has_contradictions = sc.get("has_contradictions", False)
                ev.confidence_class = sc.get("confidence_class")
            session.commit()
            summarize_events(session, now=tick)
            rank_events(session, now=tick)
            assign_situations(session, grouper, now=tick)
            print(f"  {tick:%m-%d %H:%M}  +{new} items, {session.query(Event).count()} events")
    finally:
        clustering.datetime = clock._real
        session.close()
    print(f"demo database: {out}\nserve it:  OSINT_DB_URL={url} python main.py serve")


if __name__ == "__main__":
    main()
