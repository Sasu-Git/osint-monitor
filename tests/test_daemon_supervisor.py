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


# --- exit capture (daemon_launcher.py) and reconciling unrecorded exits ---------------------------------

NOW = datetime(2026, 10, 27, 12, tzinfo=timezone.utc)
START = {"event": "start", "at": "2026-10-27T11:00:00+00:00", "daemon_pid": 4242}


def test_a_start_without_exit_and_nothing_running_is_recorded_as_unrecorded():
    rec = sup.reconcile_exits([START], running=False, held=False, now=NOW)
    assert rec["event"] == "exit" and rec["exit_code"] is None and rec["daemon_pid"] == 4242
    assert rec["recorded_by"] == "supervisor" and rec["cause"].startswith("unrecorded")


@pytest.mark.parametrize("exits, running", [
    ([START], True),                                                   # still running
    ([START, {"event": "exit", "exit_code": 1}], False),               # the launcher recorded the exit
    ([], False),                                                       # nothing started through the launcher yet
])
def test_nothing_to_reconcile(exits, running):
    assert sup.reconcile_exits(exits, running=running, held=False, now=NOW) is None


def test_a_hold_at_the_time_is_kept_on_the_reconciled_exit():
    assert sup.reconcile_exits([START], running=False, held=True, now=NOW)["held"] is True


launch_spec = importlib.util.spec_from_file_location(
    "daemon_launcher", Path(__file__).resolve().parents[1] / "scripts" / "ops" / "supervisor" / "daemon_launcher.py")
launcher = importlib.util.module_from_spec(launch_spec)
launch_spec.loader.exec_module(launcher)


def _cfg(tmp_path, held=False):
    hold = tmp_path / "HOLD"
    if held:
        hold.write_text("deploy")
    return {"daemon_worktree": str(tmp_path / "wt"), "db_url": "sqlite:///x.db", "log": str(tmp_path / "sup.jsonl"),
            "hold_file": str(hold), "tail_lines": 3}


def test_the_launcher_records_start_exit_code_and_the_error_log_tail(tmp_path):
    cfg = _cfg(tmp_path)
    code = ("import sys, os; nl = chr(10); "
            "sys.stderr.write('boom 1' + nl + 'boom 2' + nl + os.environ['OSINT_DB_URL'] + nl); sys.exit(3)")
    assert launcher.run(cfg, [sys.executable, "-c", code]) == 3
    start, end = [json.loads(x) for x in (tmp_path / "daemon-exits.jsonl").read_text().splitlines()]
    assert start["event"] == "start" and start["daemon_pid"] == end["daemon_pid"]
    assert end["event"] == "exit" and end["exit_code"] == 3 and end["exit_code_hex"] == "0x00000003"
    assert end["held"] is False and end["err_tail"] == ["boom 1", "boom 2", "sqlite:///x.db"]
    assert (tmp_path / "wt" / "data" / "logs" / "daemon.err.log").exists()     # appended where the runbook writes


def test_a_deliberate_stop_is_marked_by_the_hold_file(tmp_path):
    cfg = _cfg(tmp_path, held=True)
    launcher.run(cfg, [sys.executable, "-c", "pass"])
    end = json.loads((tmp_path / "daemon-exits.jsonl").read_text().splitlines()[-1])
    assert end["exit_code"] == 0 and end["held"] is True


def test_tail_reads_only_the_end_of_a_large_log(tmp_path):
    log = tmp_path / "big.log"
    log.write_text("x" * 200_000 + "\n" + "\n".join(f"line {i}" for i in range(50)) + "\n", encoding="utf-8")
    assert launcher.tail(log, 2) == ["line 48", "line 49"]
    assert launcher.tail(tmp_path / "missing.log", 2) == []


# Yield (daemon_yield.py): the daemon gives its memory to other work for a lease, then comes back when memory allows.

def test_a_yield_lease_keeps_the_daemon_stopped():
    s = state(daemon_running=False, yielded=True, lease_active=True, available_mb=9000)
    assert sup.decide(s, PIN[:7], 3)["daemon"] == "yield"


def test_after_the_lease_the_daemon_waits_for_memory():
    s = state(daemon_running=False, yielded=True, lease_active=False, available_mb=1200)
    assert sup.decide(s, PIN[:7], 3, resume_available_mb=2900)["daemon"] == "yield_wait_memory"
    s = state(daemon_running=False, yielded=True, lease_active=False, available_mb=None)
    assert sup.decide(s, PIN[:7], 3)["daemon"] == "yield_wait_memory"          # unknown memory: keep waiting


def test_after_the_lease_with_memory_available_the_pinned_daemon_restarts():
    s = state(daemon_running=False, yielded=True, lease_active=False, available_mb=3100)
    assert sup.decide(s, PIN[:7], 3, resume_available_mb=2900)["daemon"] == "restart"
    s = state(daemon_running=False, yielded=True, lease_active=False, available_mb=3100, head=None)
    assert sup.decide(s, PIN[:7], 3)["daemon"] == "refuse_pin_mismatch"         # the pin still applies


def test_the_hold_overrides_a_yield_and_a_running_daemon_is_left_alone():
    assert sup.decide(state(held=True, yielded=True), PIN[:7], 3)["daemon"] == "hold"
    assert sup.decide(state(yielded=True, lease_active=True), PIN[:7], 3)["daemon"] == "ok"


def test_the_lease():
    now = datetime(2026, 11, 9, 12, tzinfo=timezone.utc)
    assert sup.lease_active({"until": "2026-11-09T13:00:00+00:00"}, now)
    assert not sup.lease_active({"until": "2026-11-09T11:00:00+00:00"}, now)
    assert not sup.lease_active({}, now) and not sup.lease_active(None, now)    # unreadable yield: no lease


def test_read_yield(tmp_path):
    f = tmp_path / "YIELD"
    assert sup.read_yield(f) is None
    f.write_text('{"by": "agent", "until": "2026-11-09T13:00:00+00:00"}')
    assert sup.read_yield(f)["by"] == "agent"
    f.write_text("not json")
    assert sup.read_yield(f) == {}


def test_a_yield_stop_is_marked_on_the_exit_record(tmp_path):
    cfg = _cfg(tmp_path)
    (tmp_path / "YIELD").write_text("{}")
    launcher.run(cfg, [sys.executable, "-c", "pass"])
    end = json.loads((tmp_path / "daemon-exits.jsonl").read_text().splitlines()[-1])
    assert end["yielded"] is True and end["held"] is False
