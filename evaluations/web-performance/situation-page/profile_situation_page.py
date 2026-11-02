"""Profile GET /situations/<slug> in-process against a read-only snapshot (no server, no live DB).

    PYTHONPATH=<deploy-web-20261102 checkout> python profile_situation_page.py --db <snapshot.db> slug [slug ...]

Opens the snapshot with OSINT_DB_READONLY=1 (mode=ro). For each Situation: 3 timed requests through the real app
(TestClient), then one instrumented request that splits time into stages and counts SQL statements.
"""
import argparse, os, re, sys, time, cProfile, pstats, io
from collections import Counter, defaultdict
from contextlib import contextmanager

ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True)
ap.add_argument("slugs", nargs="+")
a = ap.parse_args()
os.environ["OSINT_DB_URL"] = "sqlite:///" + a.db.replace("\\", "/")
os.environ["OSINT_DB_READONLY"] = "1"
os.environ["OSINT_USER_STATE_DB"] = os.path.join(os.path.dirname(a.db), "profile-user-state.db")
os.environ["HF_HUB_OFFLINE"] = "1"

from fastapi.testclient import TestClient
from sqlalchemy import event
import osint_monitor.api.situation_views as sv
import osint_monitor.processors.provenance as prov_mod
from osint_monitor.api.app import app
from osint_monitor.core.database import get_engine

sql_count, sql_time, sql_by_shape = Counter(), Counter(), Counter()
stage = defaultdict(float)
current = []


def shape(stmt):
    s = re.sub(r"\s+", " ", stmt)
    s = re.sub(r"\(\?(, \?)*\)", "(?…)", s)
    return s[:160]


@event.listens_for(get_engine(), "before_cursor_execute")
def _b(conn, cursor, stmt, params, context, many):
    context._t = time.perf_counter()


@event.listens_for(get_engine(), "after_cursor_execute")
def _a(conn, cursor, stmt, params, context, many):
    dt = time.perf_counter() - context._t
    who = current[-1] if current else "other"
    sql_count[who] += 1
    sql_time[who] += dt
    sql_by_shape[shape(stmt)] += 1


@contextmanager
def timed(name):
    current.append(name)
    t = time.perf_counter()
    try:
        yield
    finally:
        stage[name] += time.perf_counter() - t
        current.pop()


def wrap(mod, attr, name):
    orig = getattr(mod, attr)
    def w(*args, **kw):
        with timed(name):
            return orig(*args, **kw)
    setattr(mod, attr, w)
    return orig


calls = Counter()
orig_assess = sv.assess_event
def counted_assess(session, event_id, *a2, **kw):
    calls["assess_event"] += 1
    with timed("provenance (assess_event)"):
        return orig_assess(session, event_id, *a2, **kw)

orig_dev_view = sv.development_view
def timed_dev_view(*args, **kw):
    calls["development_view"] += 1
    with timed("development_view (rest: actors, items, excerpts, models)"):
        return orig_dev_view(*args, **kw)

orig_detail = sv.situation_detail
def timed_detail(*args, **kw):
    with timed("situation_detail (route query setup + loop)"):
        return orig_detail(*args, **kw)

client = TestClient(app)
client.__enter__()
for slug in a.slugs:
    for _ in range(1):                       # warm caches (gazetteer, normaliser, templates)
        client.get(f"/situations/{slug}")
    totals = []
    for _ in range(3):
        t = time.perf_counter(); r = client.get(f"/situations/{slug}"); totals.append(time.perf_counter() - t)
    assert r.status_code == 200, r.status_code
    size = len(r.content)
    # instrumented request
    sql_count.clear(); sql_time.clear(); sql_by_shape.clear(); stage.clear(); calls.clear()
    sv.assess_event, sv.development_view, sv.situation_detail = counted_assess, timed_dev_view, timed_detail
    canon_orig = wrap(sv, "_canonicalizer", "actor canonicalizer load")
    excerpt_orig = wrap(sv, "_excerpt", "excerpts")
    with timed("whole request"):
        r = client.get(f"/situations/{slug}")
    sv.assess_event, sv.development_view, sv.situation_detail = orig_assess, orig_dev_view, orig_detail
    sv._canonicalizer, sv._excerpt = canon_orig, excerpt_orig
    devs = calls["development_view"]
    whole = stage["whole request"]
    detail = stage["situation_detail (route query setup + loop)"]
    dview = stage["development_view (rest: actors, items, excerpts, models)"]
    assess = stage["provenance (assess_event)"]
    print(f"\n=== /situations/{slug}: {devs} Developments, {size // 1024} KB HTML")
    print(f"timed requests (s): " + ", ".join(f"{x:.2f}" for x in totals))
    print(f"instrumented whole request          {whole:7.3f} s")
    print(f"  situation_detail                  {detail:7.3f} s")
    print(f"    provenance assess_event x{calls['assess_event']:<3d}    {assess:7.3f} s   ({sql_count['provenance (assess_event)']} SQL, {sql_time['provenance (assess_event)']:.3f} s in SQLite)")
    print(f"    development_view rest           {dview - assess - stage['excerpts']:7.3f} s   ({sql_count['development_view (rest: actors, items, excerpts, models)']} SQL, {sql_time['development_view (rest: actors, items, excerpts, models)']:.3f} s in SQLite)")
    print(f"    excerpts                        {stage['excerpts']:7.3f} s")
    print(f"    canonicalizer load              {stage['actor canonicalizer load']:7.3f} s")
    print(f"    setup (situation + events)      {detail - dview - stage['actor canonicalizer load']:7.3f} s   ({sql_count['situation_detail (route query setup + loop)']} SQL)")
    print(f"  template render + response        {whole - detail:7.3f} s   ({sql_count['whole request']} SQL outside the view)")
    print(f"SQL total {sum(sql_count.values())}, distinct shapes {len(sql_by_shape)}; most repeated:")
    for s, n in sql_by_shape.most_common(6):
        print(f"  {n:5d}  {s}")

# cProfile of the largest
slug = a.slugs[-1]
pr = cProfile.Profile(); pr.enable(); client.get(f"/situations/{slug}"); pr.disable()
out = io.StringIO(); pstats.Stats(pr, stream=out).sort_stats("cumulative").print_stats(28)
print(f"\n=== cProfile /situations/{slug} (cumulative, top 28)")
print("\n".join(l for l in out.getvalue().splitlines() if l.strip())[:9000])
client.__exit__(None, None, None)
