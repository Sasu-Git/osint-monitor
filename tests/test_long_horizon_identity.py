"""Builder determinism and labelling-server freeze / blindness for evaluations/development-identity/long-horizon-v1."""

from __future__ import annotations

import importlib.util
import json
import sqlite3
import threading
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from http.server import ThreadingHTTPServer
from pathlib import Path

import numpy as np
import pytest

LH = Path(__file__).resolve().parents[1] / "evaluations" / "development-identity" / "long-horizon-v1"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(f"lhid_{name}", LH / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bs = _load("build_sample")
ls = _load("label_server")


# ------------------------------------------------------------------ synthetic snapshot

def _vec(rng, base, noise):
    v = base + noise * rng.standard_normal(base.shape)
    return (v / np.linalg.norm(v)).astype(np.float32)


def make_db(path: Path) -> sqlite3.Connection:
    rng = np.random.default_rng(7)
    c = sqlite3.connect(path)
    c.executescript("""
    create table sources(id integer primary key, name text);
    create table raw_items(id integer primary key, source_id int, title text, content text, url text,
        published_at text, fetched_at text, embedding blob);
    create table event_items(id integer primary key, event_id int, item_id int);
    """)
    c.executemany("insert into sources values(?,?)", [(1, "Outlet One"), (2, "Outlet Two")])
    t0 = datetime(2026, 11, 1)
    item = 0
    # (event id, span hours, size, drift): short, multi-day continuous, drifting, recurring (gap), long chain
    specs = [(10 + k, 20.0, 5, 0.0) for k in range(8)] + [(30 + k, 100.0, 12, 0.1) for k in range(8)] + \
            [(50 + k, 300.0, 40, 0.8) for k in range(6)] + [(70 + k, 400.0, 30, 0.2) for k in range(4)]
    for ev, span, size, drift in specs:
        base = rng.standard_normal(384)
        for k in range(size):
            frac = k / (size - 1)
            t = t0 + timedelta(hours=ev * 3 + span * frac)
            if 70 <= ev < 80 and frac > 0.5:
                t += timedelta(hours=120)                       # a long silent gap in the middle
            v = _vec(rng, base + drift * frac * 4 * rng.standard_normal(384), 0.05)
            item += 1
            c.execute("insert into raw_items values(?,?,?,?,?,?,?,?)",
                      (item, 1 + k % 2, f"headline {ev} {k}", f"<p>lead {ev} {k} &amp; more</p>", f"https://x.test/{item}",
                       t.isoformat(sep=" "), t.isoformat(sep=" "), v.tobytes()))
            c.execute("insert into event_items(event_id,item_id) values(?,?)", (ev, item))
    c.commit()
    return c


def link(a, b):          # stand-in for compatible_link; the real one is exercised by the builder run itself
    return True


PLAN = {"A_SHORT": (4, 1), "B_CONTINUOUS_MULTIDAY": (4, 1), "C_RECURRING_GAP": (4, 2), "D_DRIFT_MULTIDAY": (4, 2),
        "E_CHAIN_FAILURE": (4, 2)}


@pytest.fixture()
def conn(tmp_path):
    return make_db(tmp_path / "s.db")


def run(conn, seed=bs.SEED, excluded_devs=frozenset(), excluded_items=frozenset()):
    return bs.build(conn, link, set(excluded_devs), set(excluded_items), seed=seed, plan=PLAN, pinned={})


def test_builder_is_deterministic(conn):
    a, b = run(conn), run(conn)
    assert bs.blind_cases(a["cases"]) == bs.blind_cases(b["cases"])
    assert bs.key_of(a["cases"]) == bs.key_of(b["cases"])
    assert a["split"] == b["split"]
    assert run(conn, seed=1)["cases"] != a["cases"]


def test_builder_strata_and_exclusions(conn):
    r = run(conn)
    assert r["cases"] and set(c["stratum"] for c in r["cases"]) <= set(bs.STRATA)
    assert r["pool_sizes"]["A_SHORT"] >= 4
    # exclusion by Development id and by member item id
    some = r["cases"][0]["development_id"]
    r2 = run(conn, excluded_devs={some})
    assert some not in {c["development_id"] for c in r2["cases"]}
    item = r["cases"][0]["b_items"][0]
    r3 = run(conn, excluded_items={item})
    assert some not in {c["development_id"] for c in r3["cases"]}
    # sides never share an item; a Development's cases never reuse a B item
    seen = {}
    for c in r["cases"]:
        assert not set(c["a_items"]) & set(c["b_items"])
        used = seen.setdefault(c["development_id"], set())
        assert not used & set(c["b_items"])
        used |= set(c["b_items"])


def test_split_is_by_development_and_cases_json_is_blind(conn):
    r = run(conn)
    by_dev = {}
    for c in r["cases"]:
        by_dev.setdefault(c["development_id"], set()).add(r["split"][c["case_id"]])
    assert all(len(v) == 1 for v in by_dev.values())
    blind = json.dumps(bs.blind_cases(r["cases"]))
    for c in r["cases"]:
        assert c["stratum"] not in blind and c["band"] not in blind
    assert "development_id" not in blind and "item_id" not in blind and "cos" not in blind


# ------------------------------------------------------------------ server

CASES = {"cases": [{"case_id": f"LH00{k}", "a": {"items": [{"source": "S", "published_at": "2026-11-01 10:00",
                                                           "title": f"early {k}", "text": "lead A"}]},
                    "b": {"items": [{"source": "T", "published_at": "2026-11-09 10:00", "title": f"late {k}",
                                     "text": "lead B"}]}} for k in (1, 2)]}


@pytest.fixture()
def server(tmp_path):
    (tmp_path / "cases.json").write_text(json.dumps(CASES), encoding="utf-8")
    # a key.json with identifying data must never be read or served
    (tmp_path / "key.json").write_text(json.dumps({"cases": [{"case_id": "LH001", "development_id": 398,
                                                               "stratum": "E_CHAIN_FAILURE"}]}), encoding="utf-8")
    app = ls.App(tmp_path)
    srv = ThreadingHTTPServer(("127.0.0.1", 0), ls.make_handler(app))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield app, f"http://127.0.0.1:{srv.server_address[1]}", tmp_path
    srv.shutdown()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def post(url, **form):
    req = urllib.request.Request(url, urllib.parse.urlencode(form).encode(), method="POST")
    try:
        return urllib.request.build_opener(NoRedirect).open(req).status
    except urllib.error.HTTPError as e:
        return e.code


def get(url):
    return urllib.request.urlopen(url).read().decode()


def test_server_is_blind(server):
    app, base, d = server
    body = get(base + "/") + get(base + "/case/LH001")
    assert "398" not in body and "E_CHAIN_FAILURE" not in body and "stratum" not in body.lower()
    assert "early 1" in body and "late 1" in body
    assert post(base + "/case/LH001", label="SAME_EPISODE") == 303
    assert post(base + "/case/LH001", label="made_up") == 400


def test_history_first_answer_and_freeze(server):
    app, base, d = server
    assert post(base + "/case/LH001", label="DIFFERENT", note="x") == 303
    assert post(base + "/case/LH001", label="SAME_EPISODE") == 303          # edit allowed before freeze, history keeps both
    hist = [json.loads(x) for x in (d / "label-history.jsonl").read_text(encoding="utf-8").splitlines()]
    assert [h["label"] for h in hist] == ["DIFFERENT", "SAME_EPISODE"]
    assert ls.freeze(app) == 1                                               # LH002 unlabelled: refuses to freeze
    assert not (d / "labels-freeze.json").exists()
    assert post(base + "/case/LH002", label="CANNOT_TELL", confidence="low") == 303
    assert ls.freeze(app) == 0 and (d / "labels-freeze.json").exists()
    before = (d / "labels.yaml").read_bytes()
    assert post(base + "/case/LH001", label="DIFFERENT") == 403              # frozen: refused
    assert (d / "labels.yaml").read_bytes() == before
    assert ls.freeze(app) == 1                                               # no second freeze


def test_server_binds_localhost_only():
    src = (LH / "label_server.py").read_text(encoding="utf-8")
    assert '("127.0.0.1", a.port)' in src and "0.0.0.0" not in src
    assert 'default=8795' in src
    import ast
    tree = ast.parse(src)
    tree.body = tree.body[1:]                      # drop the module docstring, which names key.json
    assert "key.json" not in ast.unparse(tree)
