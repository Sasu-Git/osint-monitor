"""Daemon robustness: resume behaviour, one writer at a time, bounded SQLite lock retries,
collection gaps reported. No intelligence semantics are exercised here."""

import json
import threading
import time
from datetime import datetime, timedelta

import pytest
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_MISSED
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.exc import OperationalError

from osint_monitor.core import scheduler as sched
from osint_monitor.core.database import is_lock_error
from osint_monitor.core.models import RawItemModel
from osint_monitor.processors import pipeline

LOCKED = OperationalError("INSERT ...", {}, Exception("database is locked"))


@pytest.fixture()
def fast_retries(monkeypatch):
    monkeypatch.setattr(pipeline, "LOCK_BACKOFF_SECONDS", 0.0)


# --- resume: slots, misfires, stampede -----------------------------------------------------------

def test_no_two_jobs_ever_become_due_in_the_same_second():
    scheduler = sched.create_scheduler()
    try:
        scheduler.start(paused=True)
        jobs = [j for j in scheduler.get_jobs() if j.id != "daily_briefing"]
        horizon = min(j.next_run_time for j in jobs) + timedelta(hours=24)
        seen: dict[datetime, str] = {}
        for job in jobs:
            t = job.next_run_time
            while t < horizon:
                key = t.replace(microsecond=0)
                assert key not in seen, f"{job.id} and {seen[key]} both due at {key}"
                seen[key] = job.id
                t = job.trigger.get_next_fire_time(t, t)
    finally:
        scheduler.shutdown(wait=False)


def test_runs_missed_during_a_pause_are_skipped_once_not_replayed(monkeypatch, tmp_path):
    monkeypatch.setattr(sched, "GAP_MIN_SECONDS", 10)
    monkeypatch.setattr(sched, "_GAP_LOG", tmp_path / "gaps.jsonl")
    scheduler = BackgroundScheduler(job_defaults={"coalesce": True, "misfire_grace_time": sched.MISFIRE_GRACE_SECONDS,
                                                  "max_instances": 1})
    scheduler.add_listener(sched._on_job_missed, EVENT_JOB_MISSED)
    runs, missed = [], []
    scheduler.add_listener(lambda e: missed.append(e.job_id), EVENT_JOB_MISSED)
    scheduler.add_listener(lambda e: runs.append(e.job_id), EVENT_JOB_EXECUTED)
    scheduler.start(paused=True)
    try:
        now = datetime.now().astimezone()
        for job_id in ("tier_hot", "tier_warm", "tier_cold"):
            job = scheduler.add_job(lambda: None, "interval", seconds=3600, id=job_id)
            job.modify(next_run_time=now - timedelta(minutes=90))    # due 90 min ago: the host slept
        scheduler.resume()
        time.sleep(1.5)
    finally:
        scheduler.shutdown(wait=True)
    assert sorted(missed) == ["tier_cold", "tier_hot", "tier_warm"]    # each stale run reported once
    assert runs == []                                                    # and none replayed on wake-up
    gaps = [json.loads(line) for line in (tmp_path / "gaps.jsonl").read_text().splitlines()]
    assert {g["subject"] for g in gaps} == {"tier_hot", "tier_warm", "tier_cold"}
    # lateness of the latest skipped slot (a lower bound; tier_silence measures the full silence)
    assert all(g["kind"] == "missed_run" and g["seconds"] >= 30 * 60 - 5 for g in gaps)


def test_tiers_collect_concurrently_but_write_one_at_a_time(monkeypatch):
    active = {"collect": 0, "write": 0}
    peak = {"collect": 0, "write": 0}
    guard = threading.Lock()

    def phase(name, seconds):
        with guard:
            active[name] += 1
            peak[name] = max(peak[name], active[name])
        time.sleep(seconds)
        with guard:
            active[name] -= 1

    class FakeSession:               # run bookkeeping (core.runs) adds and commits the PipelineRun row
        def add(self, obj): pass
        def commit(self): pass
        def rollback(self): pass
        def close(self): pass

    monkeypatch.setattr(pipeline, "init_db", lambda url=None: None)
    monkeypatch.setattr(pipeline, "get_session", lambda url=None: FakeSession())
    monkeypatch.setattr(pipeline, "run_collection_for_tier", lambda s, tier: phase("collect", 0.3) or [tier])
    monkeypatch.setattr(pipeline, "process_new_items", lambda s, items: phase("write", 0.1) or {"new_items": 1})
    monkeypatch.setattr(pipeline, "run_post_processing", lambda s, quiet=False: phase("write", 0.2) or {})

    threads = [threading.Thread(target=pipeline.run_tier, args=(t,)) for t in ("hot", "warm", "cold")]
    for t in threads:
        t.start()                    # all three due at once, as after a resume
    for t in threads:
        t.join()
    assert peak["collect"] == 3      # collection stays parallel
    assert peak["write"] == 1        # the write phases never overlap


# --- SQLite locks --------------------------------------------------------------------------------

def items(*titles):
    return [RawItemModel(title=t, source_name="Test", source_type="rss") for t in titles]


def test_a_transient_lock_is_retried_and_the_item_is_stored(session, monkeypatch, fast_retries):
    calls = []

    def flaky(session, raw_item, dedup, resolver, stats):
        calls.append(raw_item.title)
        if len(calls) <= 2:
            raise LOCKED
        stats["new_items"] += 1

    monkeypatch.setattr(pipeline, "_process_single_item", flaky)
    stats = pipeline.process_new_items(session, items("one item"))
    assert calls == ["one item"] * 3
    assert stats["new_items"] == 1 and stats["lock_failures"] == 0


def test_a_persistent_lock_is_bounded_reported_and_the_session_recovers(session, monkeypatch, fast_retries, caplog):
    calls = []

    def always_locked_first(session, raw_item, dedup, resolver, stats):
        calls.append(raw_item.title)
        if raw_item.title == "stuck":
            raise LOCKED
        stats["new_items"] += 1

    monkeypatch.setattr(pipeline, "_process_single_item", always_locked_first)
    with caplog.at_level("ERROR", logger="osint_monitor.processors.pipeline"):
        stats = pipeline.process_new_items(session, items("stuck", "fine"))
    assert calls.count("stuck") == pipeline.LOCK_RETRIES + 1          # bounded
    assert stats["lock_failures"] == 1 and stats["new_items"] == 1     # the next item still went in
    assert any("not stored" in r.message and "locked" in r.message for r in caplog.records)   # not silent
    session.execute(__import__("sqlalchemy").text("SELECT 1"))          # session usable afterwards


def test_non_lock_errors_are_not_retried(session, monkeypatch, fast_retries):
    calls = []

    def broken(session, raw_item, dedup, resolver, stats):
        calls.append(1)
        raise ValueError("bad item")

    monkeypatch.setattr(pipeline, "_process_single_item", broken)
    stats = pipeline.process_new_items(session, items("bad"))
    assert calls == [1] and stats["lock_failures"] == 0


def test_a_post_processing_stage_retries_a_transient_lock(session, monkeypatch, fast_retries):
    import osint_monitor.processors.clustering as clustering
    calls = []

    def flaky_clusters(s):
        calls.append(1)
        if len(calls) == 1:
            raise LOCKED
        return []

    monkeypatch.setattr(clustering, "cluster_recent_items", flaky_clusters)
    stats = pipeline.run_post_processing(session, quiet=True, offline=True)
    assert stats["stages"]["clustering"] == "ok (after 1 lock retries)"


def test_lock_errors_are_recognised():
    assert is_lock_error(LOCKED)
    assert not is_lock_error(ValueError("database is fine"))


# --- collection gaps -----------------------------------------------------------------------------

def test_a_silent_tier_is_reported_as_a_gap(monkeypatch, tmp_path, caplog):
    monkeypatch.setattr(sched, "_GAP_LOG", tmp_path / "gaps.jsonl")
    monkeypatch.setattr(sched, "_last_tick", {})
    monkeypatch.setattr(sched, "_intervals", {"warm": 600})
    t0 = datetime(2026, 9, 28, 14, 27)
    assert sched.check_tier_gap("warm", t0) is None                        # first tick
    assert sched.check_tier_gap("warm", t0 + timedelta(minutes=10)) is None  # on schedule
    with caplog.at_level("WARNING", logger="osint_monitor.core.scheduler"):
        gap = sched.check_tier_gap("warm", t0 + timedelta(hours=4, minutes=30))
    assert gap["kind"] == "tier_silence" and gap["seconds"] == 4 * 3600 + 20 * 60
    assert any("Collection gap" in r.message and "suspend" in r.message for r in caplog.records)
    assert json.loads((tmp_path / "gaps.jsonl").read_text())["subject"] == "warm tier"
    assert sched.get_status()["recent_gaps"][-1]["subject"] == "warm tier"
