"""Where the corroboration stage's time goes after the pair-matcher pre-check (code bc0d5c0), read-only on a snapshot.

    PYTHONPATH=<bc0d5c0 checkout> python measure_residual.py --db <snapshot> --out residual.json

Replays exactly what the pipeline stage does (processors/pipeline.py, _corroboration): compute_corroboration_score for
every Development, on a mode=ro session. Each part of the call is timed by wrapping the functions it calls (no code
change), and every SQL statement is counted and timed. Also derives, from the run ledger, how many Developments each
past post-processing run actually changed (new memberships stamped with that run), to size the avoidable rescan.
"""
import argparse, json, sqlite3, statistics as st, sys, time
from collections import Counter, defaultdict

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()

import osint_monitor.core.config as config_mod
import osint_monitor.processors.corroboration as corr
import osint_monitor.processors.provenance as prov_pkg
import osint_monitor.processors.provenance.confidence as conf_mod
import osint_monitor.processors.provenance.context as ctx_mod
import osint_monitor.processors.provenance.resolve as res_mod

clock, calls = Counter(), Counter()
stack: list[str] = []


def wrap(owner, name, key):
    orig = getattr(owner, name)

    def w(*args, **kw):
        stack.append(key)
        calls[key] += 1
        t = time.perf_counter()
        try:
            return orig(*args, **kw)
        finally:
            clock[key] += time.perf_counter() - t
            stack.pop()
    setattr(owner, name, w)


# order matters: inner functions first; a function imported by name elsewhere is patched where it is looked up
wrap(ctx_mod, "_feed_categories", "evidence: sources.yaml categories")
wrap(ctx_mod, "build_evidence", "evidence: build_evidence (items, claims)")
wrap(prov_pkg, "build_evidence", "evidence: build_evidence (items, claims)")
wrap(res_mod.ProvenanceResolver, "__init__", "provenance: resolver construction (config load, regex compile)")
wrap(res_mod.ProvenanceResolver, "_mark_syndicated_copies", "provenance: syndicated-copy matcher")
wrap(res_mod.ProvenanceResolver, "resolve", "provenance: resolve (roles, attribution, matcher)")
wrap(conf_mod, "assess_confidence", "provenance: assess_confidence (total)")
wrap(prov_pkg, "assess_event", "corroboration: assess_event (total)")

engine = create_engine(f"sqlite:///file:{a.db}?mode=ro&uri=true")
sql_n, sql_t, sql_owner = Counter(), Counter(), Counter()


@event.listens_for(engine, "before_cursor_execute")
def _b(conn, cursor, stmt, params, context, many):
    context._t = time.perf_counter()


@event.listens_for(engine, "after_cursor_execute")
def _a(conn, cursor, stmt, params, context, many):
    owner = stack[-1] if stack else "corroboration: own queries (items, sources, claims)"
    sql_n[owner] += 1
    sql_t[owner] += time.perf_counter() - context._t


session = sessionmaker(bind=engine)()
raw = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True)
ids = [r[0] for r in raw.execute("select id from events order by id")]
per = []
t0 = time.perf_counter()
for eid in ids:
    before = dict(clock)
    t = time.perf_counter()
    corr.compute_corroboration_score(session, eid)
    per.append((eid, time.perf_counter() - t))
total = time.perf_counter() - t0

# ledger: post-processing runs and the Developments they changed (new memberships stamped with the run)
runs = raw.execute("select id, tier, started_at, items_new, stages from pipeline_runs "
                   "where started_at >= '2026-10-27 09:58' and status = 'ok' and stages like '%corroboration%' "
                   "order by started_at").fetchall()
changed = defaultdict(set)
for run_id, eid in raw.execute("select added_run_id, event_id from event_items where added_run_id is not null"):
    changed[run_id].add(eid)
devs_at = lambda ts: raw.execute("select count(*) from events where first_reported_at <= ?", (ts,)).fetchone()[0]
ledger = []
for run_id, tier, started, new, stages in runs:
    sec = (json.loads(stages or "{}").get("_seconds") or {})
    ledger.append({"tier": tier, "started": started, "items_new": new, "developments": devs_at(started),
                   "developments_changed": len(changed.get(run_id, ())), "corroboration_s": sec.get("corroboration")})

out = {
    "developments": len(ids), "total_s": round(total, 2),
    "parts_s": {k: round(v, 2) for k, v in clock.most_common()},
    "calls": dict(calls),
    "sql": {k: {"statements": sql_n[k], "seconds": round(sql_t[k], 2)} for k in sql_n},
    "per_development_ms": {"median": round(st.median(x for _, x in per) * 1e3, 2),
                           "p90": round(sorted(x for _, x in per)[int(0.9 * len(per))] * 1e3, 2),
                           "max": round(max(x for _, x in per) * 1e3, 1)},
    "slowest": [(e, round(x, 3)) for e, x in sorted(per, key=lambda p: -p[1])[:10]],
    "ledger": ledger,
}
ch = [r["developments_changed"] / r["developments"] for r in ledger if r["developments"]]
out["ledger_summary"] = {"runs": len(ledger),
                         "changed_share_median": round(st.median(ch), 4) if ch else None,
                         "changed_share_p90": round(sorted(ch)[int(0.9 * len(ch))], 4) if ch else None,
                         "changed_developments_median": st.median(r["developments_changed"] for r in ledger) if ledger else None}
json.dump(out, open(a.out, "w"), indent=1, default=str)
print(json.dumps({k: out[k] for k in ("developments", "total_s", "parts_s", "sql", "per_development_ms", "ledger_summary")}, indent=1))
