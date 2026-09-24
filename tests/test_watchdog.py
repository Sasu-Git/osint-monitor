"""Daemon hang instrumentation records what is running and for how long."""

import logging
import threading

from osint_monitor.core import watchdog


class SlowCollector:
    name = "DNS Health Monitor"

    def __init__(self):
        self.current_target = None
        self.release = threading.Event()
        self.started = threading.Event()

    def collect(self):
        self.current_target = "kcna.kp"
        self.started.set()
        self.release.wait(5)
        return []


def test_running_collector_is_visible_with_target_and_thread():
    c = SlowCollector()

    def run():
        with watchdog.track_collector(c):
            c.collect()

    t = threading.Thread(target=run, name="tier-hot-worker")
    t.start()
    c.started.wait(5)
    [entry] = [a for a in watchdog.active_collectors() if a["name"] == "DNS Health Monitor"]
    assert entry["thread"] == "tier-hot-worker" and entry["target"] == "kcna.kp"
    c.release.set()
    t.join(5)
    assert not [a for a in watchdog.active_collectors() if a["name"] == "DNS Health Monitor"]


def test_slow_collector_is_logged_on_completion(monkeypatch, caplog):
    monkeypatch.setattr(watchdog, "SLOW_COLLECTOR_SECONDS", -1)
    with caplog.at_level(logging.WARNING, logger="osint_monitor.core.watchdog"):
        with watchdog.track_collector(SlowCollector()):
            pass
    assert "Slow collector DNS Health Monitor" in caplog.text


def test_stack_dump_timer_can_be_armed_and_disarmed(tmp_path, monkeypatch):
    monkeypatch.setattr(watchdog, "_dump_file", None)
    watchdog.arm_stack_dump(timeout=3600, log_dir=tmp_path)
    watchdog.disarm_stack_dump()
    assert (tmp_path / "daemon-stacks.log").exists()
