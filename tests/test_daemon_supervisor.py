"""Daemon supervisor decisions (scripts/ops/supervisor/daemon_supervisor.py): restart only the pinned code, never in a
hold, never in a crash loop."""
import importlib.util
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "daemon_supervisor", Path(__file__).resolve().parents[1] / "scripts" / "ops" / "supervisor" / "daemon_supervisor.py")
sup = importlib.util.module_from_spec(spec)
sys.modules["daemon_supervisor"] = sup          # dataclasses resolve the module by name
spec.loader.exec_module(sup)

PIN = "5f046b34fb1c0a6a1f9a5a2c3b4d5e6f70819a2b"


def state(**kw):
    base = dict(held=False, daemon_running=True, head=PIN, keepawake_running=True, restarts_last_hour=0)
    return sup.State(**{**base, **kw})


def test_a_running_daemon_is_left_alone():
    assert sup.decide(state(), PIN[:7], 3) == {"daemon": "ok", "keepawake": "ok"}


def test_a_stopped_daemon_on_the_pinned_commit_is_restarted():
    assert sup.decide(state(daemon_running=False), PIN[:7], 3)["daemon"] == "restart"


@pytest.mark.parametrize("head", ["0233855aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", None])
def test_another_checkout_is_never_started(head):
    assert sup.decide(state(daemon_running=False, head=head), PIN[:7], 3)["daemon"] == "refuse_pin_mismatch"


def test_a_short_or_missing_pin_refuses():
    assert sup.decide(state(daemon_running=False), "5f0", 3)["daemon"] == "refuse_pin_mismatch"
    assert sup.decide(state(daemon_running=False), "", 3)["daemon"] == "refuse_pin_mismatch"


def test_a_crash_loop_stops_restarting():
    assert sup.decide(state(daemon_running=False, restarts_last_hour=3), PIN[:7], 3)["daemon"] == "refuse_throttled"
    assert sup.decide(state(daemon_running=False, restarts_last_hour=2), PIN[:7], 3)["daemon"] == "restart"


def test_the_hold_file_stops_everything():
    assert sup.decide(state(held=True, daemon_running=False, keepawake_running=False), PIN[:7], 3) == \
        {"daemon": "hold", "keepawake": "hold"}


def test_keepawake_is_restarted_only_when_enabled():
    assert sup.decide(state(keepawake_running=False), PIN[:7], 3)["keepawake"] == "start"
    assert sup.decide(state(keepawake_running=False), PIN[:7], 3, keepawake=False)["keepawake"] == "ok"


def test_only_restarts_of_the_last_hour_count(tmp_path):
    now = datetime(2026, 10, 13, 12, tzinfo=timezone.utc)
    log = tmp_path / "supervisor.jsonl"
    rows = [{"at": (now - timedelta(minutes=m)).isoformat(), "daemon": d}
            for m, d in ((10, "restart"), (50, "restart"), (70, "restart"), (5, "refuse_throttled"))]
    log.write_text("\n".join(json.dumps(r) for r in rows) + "\nnot json\n", encoding="utf-8")
    assert sup.recent_restarts(log, now) == 2
    assert sup.recent_restarts(tmp_path / "missing.jsonl", now) == 0
