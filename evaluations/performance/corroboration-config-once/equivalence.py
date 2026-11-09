"""Equivalence and timing of the config-once / batched corroboration (this branch) against frozen bc0d5c0 outputs.

    PYTHONPATH=<this branch> python equivalence.py --db <snapshot> --frozen <impl-full_outputs.json> --out result.json

Frozen reference: the per-Development provenance assessment and corroboration score of bc0d5c0 on the 2026-11-02
snapshot (evaluations/performance/pair-matcher harness, `impl --full`, sha 9424ffce...). Serialised the same way as
that harness. Gate: 0 differences for every Development, on four paths:
  1. score_events (the new stage path: batched, one resolver, categories once)       vs frozen corroboration
  2. compute_corroboration_score(session, id) (default arguments, one event)        vs frozen corroboration
  3. assess_event(session, id) (default arguments)                                   vs frozen provenance
  4. assess_event(session, id, shared resolver, categories read once)                vs frozen provenance
Timing: the new stage path vs the old per-event loop (default arguments), same process, same snapshot.
"""
import argparse, json, sqlite3, time
from collections import Counter

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True)
ap.add_argument("--frozen", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()

import osint_monitor.processors.provenance.context as ctx
import osint_monitor.processors.provenance.resolve as res
from osint_monitor.processors.corroboration import compute_corroboration_score, score_events
from osint_monitor.processors.provenance import ProvenanceResolver, assess_event

calls = Counter()
for owner, name, key in ((ctx, "_feed_categories", "feed_categories"), (res.ProvenanceResolver, "__init__", "resolver")):
    orig = getattr(owner, name)
    def w(*args, _orig=orig, _key=key, **kw):
        calls[_key] += 1
        return _orig(*args, **kw)
    setattr(owner, name, w)

engine = create_engine(f"sqlite:///file:{a.db}?mode=ro&uri=true")
sql = Counter()
@event.listens_for(engine, "after_cursor_execute")
def _count(*_):
    sql["n"] += 1
make = sessionmaker(bind=engine)
frozen = json.load(open(a.frozen))
ids = [r[0] for r in sqlite3.connect(f"file:{a.db}?mode=ro", uri=True).execute("select id from events order by id")]
ser_score = lambda s: json.dumps(s, sort_keys=True, default=str)
ser_prov = lambda p: json.dumps(p.model_dump(mode="json"), sort_keys=True)
out = {"developments": len(ids)}

def timed(label, fn):
    calls.clear(); sql.clear()
    s = make()
    t = time.perf_counter()
    r = fn(s)
    out[label] = {"seconds": round(time.perf_counter() - t, 2), "feed_categories_reads": calls["feed_categories"],
                  "resolver_constructions": calls["resolver"], "sql_statements": sql["n"]}
    s.close()
    return r

old = timed("old_loop", lambda s: {e: compute_corroboration_score(s, e) for e in ids})
new = timed("new_stage_path", lambda s: score_events(s, ids))
mism = {"score_events_vs_frozen": [e for e in ids if isinstance(new[e], Exception)
                                   or ser_score(new[e]) != frozen["corroboration"][str(e)]],
        "compute_default_vs_frozen": [e for e in ids if ser_score(old[e]) != frozen["corroboration"][str(e)]]}
s = make()
mism["assess_event_default_vs_frozen"] = [e for e in ids if ser_prov(assess_event(s, e)) != frozen["provenance"][str(e)]]
resolver, cats = ProvenanceResolver(), ctx._feed_categories()
mism["assess_event_shared_vs_frozen"] = [e for e in ids if ser_prov(assess_event(s, e, resolver, cats))
                                         != frozen["provenance"][str(e)]]
out["mismatches"] = {k: len(v) for k, v in mism.items()}
out["mismatched_ids"] = {k: v[:20] for k, v in mism.items() if v}
out["exceptions_in_new_path"] = [e for e in ids if isinstance(new[e], Exception)]
out["gate"] = "PASS" if not any(mism.values()) else "FAIL"
json.dump(out, open(a.out, "w"), indent=1)
print(json.dumps(out, indent=1))
