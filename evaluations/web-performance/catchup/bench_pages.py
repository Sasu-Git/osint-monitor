"""Page latency for the web catch-up: the previously pathological pages plus small controls, in-process
(FastAPI TestClient, real app, OSINT_DB_READONLY=1) against a read-only snapshot. No server, no live DB.

    PYTHONPATH=<web code tree> python bench_pages.py --db <snapshot> --label before|after --runs 3 --out <json>

Each URL: one untimed warm-up request (caches: gazetteer, normaliser, templates), then --runs timed requests.
"""
import argparse, json, os, statistics as st, sys, time

ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True)
ap.add_argument("--label", required=True)
ap.add_argument("--runs", type=int, default=3)
ap.add_argument("--out", required=True)
a = ap.parse_args()
os.environ["OSINT_DB_URL"] = "sqlite:///" + a.db.replace("\\", "/")
os.environ["OSINT_DB_READONLY"] = "1"
os.environ["OSINT_USER_STATE_DB"] = os.path.join(os.path.dirname(a.out), f"bench-user-state-{a.label}.db")
os.environ["HF_HUB_OFFLINE"] = "1"

from fastapi.testclient import TestClient
from osint_monitor.api.app import app

URLS = {
    # previously pathological (evaluations/web-performance/situation-page/PROFILE.md; pair-matcher PERFORMANCE.md)
    "situation israel-palestine": "/situations/israel-palestine",
    "situation russia-united-states": "/situations/russia-united-states",
    "situation gaza-ceasefire": "/situations/gaza-ceasefire",
    "situation russia-ukraine-war": "/situations/russia-ukraine-war",
    "development 449 (520 items)": "/developments/449",
    "development 514 (274 items)": "/developments/514",
    "development 399 (276 items)": "/developments/399",
    # controls
    "situation sudan-civil-war (small)": "/situations/sudan-civil-war",
    "development 11 (small)": "/developments/11",
    "today /": "/",
    "map /map": "/map",
}
out = {"label": a.label, "runs": a.runs, "pages": {}}
with TestClient(app) as c:
    for name, url in URLS.items():
        r = c.get(url)
        assert r.status_code == 200, (url, r.status_code)
        times = []
        for _ in range(a.runs):
            t = time.perf_counter(); r = c.get(url); times.append(time.perf_counter() - t)
            assert r.status_code == 200
        out["pages"][name] = {"url": url, "seconds": [round(x, 3) for x in times], "median": round(st.median(times), 3),
                              "bytes": len(r.content)}
        print(f"{a.label:6s} {name:36s} median {st.median(times):8.3f} s  runs {[round(x, 2) for x in times]}", flush=True)
json.dump(out, open(a.out, "w"), indent=1)
