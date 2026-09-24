"""Daemon hang diagnostics (instrumentation only, no behaviour change).

- ``track_collector`` records which collector runs on which thread, since when,
  and its ``current_target`` if the collector sets one (e.g. the domain the DNS
  monitor is checking). Slow collectors are logged when they finish.
- ``start_watchdog`` runs a Python thread that logs collectors running longer than
  ``stuck_after`` seconds.
- ``arm_stack_dump`` uses faulthandler, whose timer runs in a C thread: if no tier
  job completes within ``timeout`` seconds, every thread's stack is written to
  data/logs/daemon-stacks.log -- even if the interpreter is frozen holding the GIL,
  which is what the 45-minute hang on 2026-09-24 looked like.
"""

from __future__ import annotations

import faulthandler
import logging
import threading
import time
from contextlib import contextmanager
from pathlib import Path

logger = logging.getLogger(__name__)

SLOW_COLLECTOR_SECONDS = 60
_active: dict[int, dict] = {}
_lock = threading.Lock()
_dump_file = None


@contextmanager
def track_collector(collector):
    thread = threading.current_thread()
    entry = {"name": getattr(collector, "name", type(collector).__name__), "collector": collector,
             "start": time.monotonic(), "started_at": time.strftime("%H:%M:%S"), "thread": thread.name}
    with _lock:
        _active[thread.ident] = entry
    try:
        yield
    finally:
        with _lock:
            _active.pop(thread.ident, None)
        elapsed = time.monotonic() - entry["start"]
        if elapsed > SLOW_COLLECTOR_SECONDS:
            logger.warning(f"Slow collector {entry['name']}: {elapsed:.0f}s on {entry['thread']}")


def active_collectors() -> list[dict]:
    now = time.monotonic()
    with _lock:
        return [{"name": e["name"], "thread": e["thread"], "started_at": e["started_at"],
                 "elapsed_s": round(now - e["start"]),
                 "target": getattr(e["collector"], "current_target", None)} for e in _active.values()]


def start_watchdog(interval: float = 60, stuck_after: float = 120) -> threading.Thread:
    def loop():
        while True:
            time.sleep(interval)
            for c in active_collectors():
                if c["elapsed_s"] >= stuck_after:
                    target = f" (target: {c['target']})" if c["target"] else ""
                    logger.warning(f"Collector still running: {c['name']} for {c['elapsed_s']}s "
                                   f"since {c['started_at']} on {c['thread']}{target}")

    t = threading.Thread(target=loop, name="collector-watchdog", daemon=True)
    t.start()
    return t


def arm_stack_dump(timeout: float = 900, log_dir: Path | None = None) -> None:
    """(Re)start the no-progress timer; call after every completed tier job."""
    global _dump_file
    if _dump_file is None:
        from osint_monitor.core.config import DATA_DIR
        log_dir = log_dir or DATA_DIR / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        _dump_file = open(log_dir / "daemon-stacks.log", "a", encoding="utf-8")
    faulthandler.cancel_dump_traceback_later()
    faulthandler.dump_traceback_later(timeout, repeat=False, file=_dump_file)


def disarm_stack_dump() -> None:
    faulthandler.cancel_dump_traceback_later()
