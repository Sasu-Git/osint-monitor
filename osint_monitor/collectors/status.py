"""Per-collector run status, persisted so any process (``main.py status``, the API) can see it.

While a collector runs, WARNING and ERROR records that collector code logs from that thread (under the
``osint_monitor.collectors`` logger namespace, including ``BaseCollector.record_error``) are captured as its
errors. Each run is then recorded in ``data/logs/collector_status.json``:

- ``ok``: no exception, nothing logged at WARNING or above;
- ``partial``: warnings or errors logged, but items returned;
- ``failed``: an exception, or errors and no items (an empty result is then an outage, not "nothing new").
"""

from __future__ import annotations

import json
import logging
import os
import threading
from datetime import datetime
from pathlib import Path

STATUS_FILE = Path(__file__).resolve().parents[2] / "data" / "logs" / "collector_status.json"
COLLECTOR_LOGGER = "osint_monitor.collectors"
MAX_ERRORS = 5

_lock = threading.Lock()


class _ThreadCapture(logging.Handler):
    def __init__(self, thread_id: int):
        super().__init__(level=logging.WARNING)
        self.thread_id = thread_id
        self.messages: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        if record.thread == self.thread_id:
            try:
                self.messages.append(record.getMessage()[:300])
            except Exception:
                pass


class capture_errors:
    """Context manager: the WARNING+ messages collector code logs in the current thread."""

    def __enter__(self) -> list[str]:
        self.handler = _ThreadCapture(threading.get_ident())
        logging.getLogger(COLLECTOR_LOGGER).addHandler(self.handler)
        return self.handler.messages

    def __exit__(self, *exc) -> None:
        logging.getLogger(COLLECTOR_LOGGER).removeHandler(self.handler)


def state_of(items: int, errors: list[str], exception: str | None) -> str:
    if exception or (errors and items == 0):
        return "failed"
    return "partial" if errors else "ok"


def load(path: Path | None = None) -> dict:
    path = path or STATUS_FILE
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def record(name: str, items: int, errors: list[str], exception: str | None, duration_s: float,
           now: datetime | None = None, path: Path | None = None) -> dict:
    """Record one run of collector ``name``; returns its updated status entry."""
    path = path or STATUS_FILE
    now_s = (now or datetime.utcnow()).isoformat(timespec="seconds")
    state = state_of(items, errors, exception)
    with _lock:
        data = load(path)
        entry = data.get(name, {})
        entry.update({"last_run": now_s, "state": state, "items": items, "duration_s": round(duration_s, 1)})
        if state == "failed":
            entry["last_failure"] = now_s
            entry["last_error"] = exception or errors[0]
        else:
            entry["last_success"] = now_s
        entry["errors"] = ([exception] if exception else []) + errors[:MAX_ERRORS]
        data[name] = entry
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_suffix(".tmp")
            tmp.write_text(json.dumps(data, indent=1, sort_keys=True), encoding="utf-8")
            os.replace(tmp, path)
        except OSError:
            pass
    return entry


def format_status(data: dict | None = None) -> list[str]:
    """One line per collector whose last run was not ok, most recent first; a summary line first."""
    data = load() if data is None else data
    if not data:
        return ["no collector runs recorded"]
    bad = sorted(((n, e) for n, e in data.items() if e.get("state") != "ok"),
                 key=lambda x: x[1].get("last_run", ""), reverse=True)
    lines = [f"{len(data)} collectors recorded, {len(bad)} not ok on their last run"]
    for name, e in bad:
        lines.append(f"{e.get('state', '?').upper():8s} {name}: last run {e.get('last_run')}, "
                     f"{e.get('items', 0)} items, last success {e.get('last_success', 'never')}"
                     + (f" -- {e['errors'][0]}" if e.get("errors") else ""))
    return lines
