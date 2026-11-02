"""Per-Development cost of the pipeline's corroboration stage, measured read-only on a snapshot.

    PYTHONPATH=<main checkout> python measure.py --db <snapshot.db> --out per_event.csv

Calls compute_corroboration_score(session, id) for every Development, exactly as the stage does
(processors/pipeline.py, _corroboration), on a session opened mode=ro; nothing is written. Records wall time, the
time inside provenance assess_event and inside its syndicated-copy matching, the SQL statement count, the item count
and body characters.
"""
import argparse, csv, sqlite3, time
from collections import Counter

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

import osint_monitor.processors.provenance as provenance
from osint_monitor.processors.corroboration import compute_corroboration_score
from osint_monitor.processors.provenance import resolve as resolve_mod

ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()

engine = create_engine(f"sqlite:///file:{a.db}?mode=ro&uri=true")
sql = Counter()
@event.listens_for(engine, "after_cursor_execute")
def _count(*_):
    sql["n"] += 1
session = sessionmaker(bind=engine)()

clock = Counter()
def timed(owner, name, key):
    orig = getattr(owner, name)
    def w(*args, **kw):
        t = time.perf_counter()
        try:
            return orig(*args, **kw)
        finally:
            clock[key] += time.perf_counter() - t
    setattr(owner, name, w)
timed(resolve_mod.ProvenanceResolver, "_mark_syndicated_copies", "syndication")
orig_assess = provenance.assess_event
def assess(*args, **kw):
    t = time.perf_counter()
    try:
        return orig_assess(*args, **kw)
    finally:
        clock["assess"] += time.perf_counter() - t
provenance.assess_event = assess

raw = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True)
sizes = {eid: (n, ch) for eid, n, ch in raw.execute(
    "select e.id, count(ei.item_id), coalesce(sum(length(coalesce(r.title,'')) + length(coalesce(r.content,''))), 0) "
    "from events e left join event_items ei on ei.event_id = e.id left join raw_items r on r.id = ei.item_id group by e.id")}
with open(a.out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["event_id", "items", "chars", "total_s", "assess_s", "syndication_s", "sql"])
    t_all = time.perf_counter()
    for eid in sorted(sizes):
        clock.clear(); sql.clear()
        t = time.perf_counter()
        compute_corroboration_score(session, eid)
        w.writerow([eid, *sizes[eid], round(time.perf_counter() - t, 4), round(clock["assess"], 4),
                    round(clock["syndication"], 4), sql["n"]])
        f.flush()
    print(f"all {len(sizes)} Developments: {time.perf_counter() - t_all:.1f} s")
