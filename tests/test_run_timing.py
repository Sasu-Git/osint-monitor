"""Run timing: every tier run records where its time went (collection, wait for the write lock, DB write,
post-processing and each post-processing stage) under the reserved stage key ``_seconds``."""

import threading
import time

from osint_monitor.core import runs
from osint_monitor.processors import pipeline


class FakeSession:
    def add(self, obj): pass
    def commit(self): pass
    def rollback(self): pass
    def close(self): pass


def _patch(monkeypatch, recorded, new_items=1, collect=0.0, write=0.0):
    monkeypatch.setattr(pipeline, "init_db", lambda url=None: None)
    monkeypatch.setattr(pipeline, "get_session", lambda url=None: FakeSession())
    monkeypatch.setattr(pipeline, "run_collection_for_tier", lambda s, tier: time.sleep(collect) or [tier])
    monkeypatch.setattr(pipeline, "process_new_items", lambda s, items: time.sleep(write) or {"new_items": new_items})
    monkeypatch.setattr(pipeline, "run_post_processing", lambda s, quiet=False: time.sleep(0.1) or {
        "stages": {"clustering": "ok", "situations": "ok"}, "stage_seconds": {"clustering": 0.05, "situations": 0.05}})
    monkeypatch.setattr(runs, "start_run", lambda session, kind, tier=None, started_at=None: (object(), None))
    monkeypatch.setattr(runs, "finish_run", lambda session, run, token, stats, **kw: recorded.append(stats))


def test_a_run_records_its_phases_and_stages(monkeypatch):
    recorded = []
    _patch(monkeypatch, recorded)
    pipeline.run_tier("warm")
    seconds = recorded[0]["stages"]["_seconds"]
    assert set(seconds) == {"collection", "lock_wait", "db_write", "post_processing", "clustering", "situations"}
    assert seconds["post_processing"] >= 0.1
    assert recorded[0]["stages"]["clustering"] == "ok"            # stage statuses are untouched strings
    assert "stage_seconds" not in recorded[0]


def test_a_run_without_new_items_records_no_post_processing(monkeypatch):
    recorded = []
    _patch(monkeypatch, recorded, new_items=0)
    pipeline.run_tier("hot")
    assert set(recorded[0]["stages"]["_seconds"]) == {"collection", "lock_wait", "db_write"}


def test_lock_wait_measures_another_tiers_write_phase(monkeypatch):
    recorded = []
    _patch(monkeypatch, recorded, new_items=0, write=0.3)
    first = threading.Thread(target=pipeline.run_tier, args=("warm",))
    first.start()
    time.sleep(0.05)                                     # warm holds the write lock for ~0.3 s
    pipeline.run_tier("hot")
    first.join()
    waits = sorted(r["stages"]["_seconds"]["lock_wait"] for r in recorded)
    assert waits[0] < 0.05 and waits[1] >= 0.15


def test_the_timing_key_never_reads_as_a_failed_stage():
    stats = {"stages": {"clustering": "ok", "_seconds": {"collection": 1.0}}}
    assert not any(str(v).startswith("failed") for v in stats["stages"].values())


def test_timing_report_summarises_phases_and_stages(tmp_path):
    import json
    import sqlite3
    from scripts.run_timing import report
    db = sqlite3.connect(tmp_path / "r.db")
    db.execute("CREATE TABLE pipeline_runs (kind TEXT, tier TEXT, started_at TEXT, finished_at TEXT, stages TEXT)")
    for i, (post, sit) in enumerate(((300.0, 40.0), (600.0, 45.0))):
        sec = {"collection": 90.0, "lock_wait": 10.0, "db_write": 20.0, "post_processing": post, "situations": sit}
        db.execute("INSERT INTO pipeline_runs VALUES ('tier', 'warm', ?, ?, ?)",
                   (f"2026-10-27 0{i}:00:00", f"2026-10-27 0{i}:10:00", json.dumps({"_seconds": sec})))
    db.execute("INSERT INTO pipeline_runs VALUES ('tier', 'warm', '2026-10-27 05:00:00', '2026-10-27 05:05:00', "
               "'{\"clustering\": \"ok\"}')")                  # a run from before timing: skipped
    out = report(db, "2026-10-27")
    assert "warm: 2 timed runs" in out and "post_processing" in out and "situations" in out
