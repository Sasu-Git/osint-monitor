"""Collector execution health, persisted so any process (``main.py status``, the API) can see it.

This is operational state about *our collection*, never a statement about the world: a failed or stale
collector is not a geopolitical finding (``analysis.fusion.detect_signal_gaps`` and the alert engine consult it,
so an outage is not reported as a modality "going dark" or a source "resuming").

While a collector runs, WARNING and ERROR records that collector code logs from that thread (under the
``osint_monitor.collectors`` logger namespace, including ``BaseCollector.record_error``) are captured as its
errors. Each run is recorded in ``data/logs/collector_status.json`` under the collector's **stable key**
(``BaseCollector.health_key``: endpoint URL, account or code-defined name; never the editable display name):

- run state ``ok``: no exception, nothing logged at WARNING or above;
- run state ``partial``: warnings or errors logged, but items returned (some endpoints or entries failed);
- run state ``failed``: an exception, or errors and no items (an empty result is then an outage, not "nothing new").

Derived health (``health_of``, evaluated at read time): ``healthy`` / ``partial`` / ``failed`` / ``stale`` (no
success within the freshness window) / ``disabled`` (configured off) / ``not_run`` (configured, never recorded).

State transitions (ok -> failed, failed -> ok, ...) are appended to ``data/logs/collector_events.jsonl`` so
collector-level outage periods can be reconstructed later (``core.gaps``) without a per-run log.
"""

from __future__ import annotations

import json
import logging
import os
import re
import tempfile
import threading
from datetime import datetime
from pathlib import Path

STATUS_FILE = Path(__file__).resolve().parents[2] / "data" / "logs" / "collector_status.json"
EVENTS_FILE = Path(__file__).resolve().parents[2] / "data" / "logs" / "collector_events.jsonl"
COLLECTOR_LOGGER = "osint_monitor.collectors"
MAX_ERRORS = 5
SCHEMA = 2
HEALTH_STATES = ("healthy", "partial", "failed", "stale", "disabled", "not_run")
STALE_FACTOR = 3                   # no success for > 3 tier intervals (and > STALE_MIN_SECONDS): stale
STALE_MIN_SECONDS = 1800

logger = logging.getLogger(__name__)
_lock = threading.Lock()

# credentials in URLs and headers: never stored or logged
_SECRET_QUERY = re.compile(r"(?i)([?&](?:api[_-]?key|key|token|access[_-]?token|apikey|secret|password|pass|auth|"
                           r"signature|sig|client[_-]?secret)=)[^&\s'\"]+")
_SECRET_HEADER = re.compile(r"(?i)\b(authorization|x-api-key|api-key|cookie)(\s*[:=]\s*)"
                            r"(?:bearer\s+|basic\s+)?[^\s,;'\"]+")
_URL_CREDS = re.compile(r"(?i)(https?://)[^/\s:@]+:[^/\s@]+@")
_SECRET_PAIR = re.compile(r"(?i)\b(password|passwd|pwd|secret|client_secret|api[_-]?key|access[_-]?token|token)"
                          r"(\s*[=:]\s*)(?!\[REDACTED\])[^\s&,;'\"]+")


def redact(text: str | None) -> str | None:
    """Remove credentials (query tokens, auth headers, key=value secrets, user:pass@ in URLs) from an error or
    log message."""
    if text is None:
        return None
    text = _SECRET_QUERY.sub(r"\1[REDACTED]", text)
    text = _SECRET_HEADER.sub(r"\1\2[REDACTED]", text)
    text = _SECRET_PAIR.sub(r"\1\2[REDACTED]", text)
    return _URL_CREDS.sub(r"\1[REDACTED]@", text)


class StatusFileError(ValueError):
    """The status file exists but cannot be parsed (reported explicitly, never silently treated as empty)."""


class _ThreadCapture(logging.Handler):
    def __init__(self, thread_id: int):
        super().__init__(level=logging.WARNING)
        self.thread_id = thread_id
        self.messages: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        if record.thread == self.thread_id:
            try:
                self.messages.append(redact(record.getMessage())[:300])
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


# --- persistence -----------------------------------------------------------------------------------------------------

def read(path: Path | None = None) -> dict:
    """Entries by stable key. Missing file: {}. Unparseable or wrong-shaped file: StatusFileError."""
    path = path or STATUS_FILE
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except OSError as e:
        raise StatusFileError(f"{path.name} unreadable: {e}") from e
    try:
        raw = json.loads(text)
    except ValueError as e:
        raise StatusFileError(f"{path.name} is not valid JSON: {e}") from e
    if not isinstance(raw, dict):
        raise StatusFileError(f"{path.name} has an unexpected shape ({type(raw).__name__})")
    if raw.get("schema") == SCHEMA:
        entries = raw.get("collectors")
        if not isinstance(entries, dict) or not all(isinstance(e, dict) for e in entries.values()):
            raise StatusFileError(f"{path.name}: 'collectors' is not a mapping of entries")
        return entries
    if "schema" in raw:
        raise StatusFileError(f"{path.name}: unknown schema {raw.get('schema')!r}")
    # schema 1 (keyed by display name, before stable keys): read as legacy entries
    return {f"legacy:{name}": {**e, "name": name, "key": f"legacy:{name}", "legacy": True}
            for name, e in raw.items() if isinstance(e, dict)}


def load(path: Path | None = None) -> dict:
    """Entries by stable key; {} when the file is missing or malformed (malformed is logged; callers that must
    tell the two apart use ``read``)."""
    try:
        return read(path)
    except StatusFileError as e:
        logger.warning("Collector status unavailable: %s", e)
        return {}


def by_name(data: dict, name: str) -> dict | None:
    """The entry whose display name is ``name`` (display names are labels, not keys)."""
    return next((e for e in data.values() if e.get("name") == name), None)


def atomic_write_json(path: Path, obj) -> None:
    """Write via a unique temp file in the same directory, then rename: concurrent writers (the daemon and a
    one-shot ``collect``) can lose an update but never interleave into a corrupt file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.stem}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=1, sort_keys=True)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def parse_time(value) -> datetime | None:
    """An ISO timestamp from a status entry, or None when missing or unparseable (never raises)."""
    try:
        return datetime.fromisoformat(value) if value else None
    except (TypeError, ValueError):
        return None


def _write(path: Path, entries: dict) -> None:
    atomic_write_json(path, {"schema": SCHEMA, "collectors": entries})


def _append_event(event: dict, path: Path | None = None) -> None:
    path = path or EVENTS_FILE
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, sort_keys=True) + "\n")
    except OSError:
        pass


def record(name: str, items: int, errors: list[str], exception: str | None, duration_s: float,
           now: datetime | None = None, path: Path | None = None, *, key: str | None = None,
           collector_type: str | None = None, source_type: str | None = None, tier: str | None = None,
           endpoint: str | None = None, http_status: int | None = None, fallback_used: bool = False,
           events_path: Path | None = None) -> dict:
    """Record one run of a collector; returns its updated entry. ``key`` is the stable identity (defaults to
    the name for callers without a better one); ``name`` is only the current display label."""
    path = path or STATUS_FILE
    key = key or name
    now_s = (now or datetime.utcnow()).isoformat(timespec="seconds")
    state = state_of(items, errors, exception)
    errors = [redact(e) for e in errors]
    exception = redact(exception)
    with _lock:
        try:
            data = read(path)
        except StatusFileError as e:
            # keep the evidence, start a clean file, and say so
            corrupt = path.with_name(f"{path.stem}.corrupt-{datetime.utcnow():%Y%m%d-%H%M%S}{path.suffix}")
            try:
                os.replace(path, corrupt)
                logger.error("Collector status file was malformed (%s); moved to %s and restarted", e, corrupt.name)
            except OSError as move_error:
                logger.error("Collector status file was malformed (%s) and could not be set aside (%s); "
                             "it is overwritten", e, move_error)
            data = {}
        entry = data.get(key)
        if entry is None:                                      # adopt a legacy (name-keyed) entry once
            legacy = data.pop(f"legacy:{name}", None)
            entry = {k: v for k, v in (legacy or {}).items() if k not in ("legacy", "key")}
        previous = entry.get("state")
        entry.update({"key": key, "name": name, "last_run": now_s, "last_attempt": now_s, "state": state,
                      "items": items, "duration_s": round(duration_s, 1), "http_status": http_status,
                      "fallback_used": bool(fallback_used),
                      "failure_scope": {"failed": "whole_collector",
                                        "partial": "some_endpoints_or_entries"}.get(state)})
        for field, value in (("collector_type", collector_type), ("source_type", source_type), ("tier", tier),
                             ("endpoint", redact(endpoint))):
            if value:
                entry[field] = value
        if state == "failed":
            entry["last_failure"] = now_s
            entry["last_error"] = exception or errors[0]
            entry["last_error_class"] = exception.split(":", 1)[0] if exception else "LoggedError"
            entry["consecutive_failures"] = int(entry.get("consecutive_failures") or 0) + 1
        else:
            entry["last_success"] = now_s
            entry["consecutive_failures"] = 0
        entry["errors"] = ([exception] if exception else []) + errors[:MAX_ERRORS]
        data[key] = entry
        try:
            _write(path, data)
        except OSError as e:
            logger.error("Collector status not written (%s): %s", path, e)
    if previous != state:
        _append_event({"at": now_s, "key": key, "name": name, "from": previous, "to": state,
                       "error": entry.get("last_error") if state == "failed" else None}, events_path)
    return {**entry, "previous_state": previous}


# --- derived health --------------------------------------------------------------------------------------------------

def default_intervals() -> dict[str, int]:
    try:
        from osint_monitor.core.config import load_sources_config
        t = load_sources_config().tiers
        return {"hot": t.hot_interval_seconds, "warm": t.warm_interval_seconds, "cold": t.cold_interval_seconds}
    except Exception:
        return {"hot": 150, "warm": 600, "cold": 3600}


def freshness_window(tier: str | None, intervals: dict[str, int] | None = None) -> int:
    interval = (intervals or default_intervals()).get(tier or "cold", 3600)
    return max(STALE_FACTOR * interval, STALE_MIN_SECONDS)


def health_of(entry: dict | None, now: datetime | None = None, *, disabled: bool = False,
              intervals: dict[str, int] | None = None) -> str:
    """healthy / partial / failed / stale / disabled / not_run for one collector entry at ``now``."""
    if disabled:
        return "disabled"
    if not entry or not entry.get("last_run"):
        return "not_run"
    if entry.get("state") == "failed":
        return "failed"
    now = now or datetime.utcnow()
    last_ok = parse_time(entry.get("last_success"))           # unparseable counts as no success
    if not last_ok or (now - last_ok).total_seconds() > freshness_window(entry.get("tier"), intervals):
        return "stale"
    return "partial" if entry.get("state") == "partial" else "healthy"


def configured_collectors() -> list[dict]:
    """Config-defined collectors (RSS feeds, Nitter accounts), enabled or not, with their stable keys. Code-defined
    collectors appear once they have run. No network, no database."""
    try:
        from osint_monitor.core.config import load_sources_config
        cfg = load_sources_config()
    except Exception:
        return []
    out = [{"key": f"RSSCollector:{feed.url}", "name": feed.name, "collector_type": "RSSCollector", "tier": "warm",
            "source_type": "rss", "disabled": not feed.enabled} for feed in cfg.rss_feeds]
    for acct in cfg.twitter_accounts:
        u = acct.username.lstrip("@")
        out.append({"key": f"NitterCollector:{u}", "name": f"@{u}", "collector_type": "NitterCollector",
                    "tier": "warm", "source_type": "twitter_nitter", "disabled": False})
    return out


def health_report(data: dict | None = None, now: datetime | None = None,
                  configured: list[dict] | None = None) -> dict:
    """Every known collector (recorded or configured) with its derived health, plus counts per state."""
    data = load() if data is None else data
    configured = configured_collectors() if configured is None else configured
    now = now or datetime.utcnow()
    intervals = default_intervals()
    legacy = {k: v for k, v in data.items() if v.get("legacy")}
    rows, used = {}, set()
    for c in configured:
        e = data.get(c["key"])
        if e is None and (le := by_name(legacy, c["name"])):
            e = le
        if e is not None:
            used.add(e.get("key"))
        rows[c["key"]] = {**(e or {}), **{k: v for k, v in c.items() if k != "name"},
                          "name": c["name"], "health": health_of(e, now, disabled=c["disabled"], intervals=intervals)}
    for k, e in data.items():
        if k not in rows and k not in used:
            rows[k] = {**e, "health": health_of(e, now, intervals=intervals)}
    counts = {s: sum(1 for r in rows.values() if r["health"] == s) for s in HEALTH_STATES}
    return {"rows": rows, "counts": counts, "at": now.isoformat(timespec="seconds")}


def format_status(data: dict | None = None, now: datetime | None = None, configured: list[dict] | None = None,
                  path: Path | None = None) -> list[str]:
    """A summary line, then one line per collector that is not healthy (failed, stale, partial, not run)."""
    if data is None:
        try:
            data = read(path)
        except StatusFileError as e:
            return [f"collector status file MALFORMED: {e} (set aside and restarted on the next collector run)"]
    report = health_report(data, now, configured)
    if not report["rows"]:
        return ["no collector runs recorded"]
    c = report["counts"]
    lines = [f"{len(report['rows'])} collectors: " + ", ".join(f"{c[s]} {s}" for s in HEALTH_STATES if c[s])]
    order = {"failed": 0, "stale": 1, "partial": 2}
    bad = sorted((r for r in report["rows"].values() if r["health"] in order),
                 key=lambda r: (order[r["health"]], r.get("name") or ""))
    never = sorted(r.get("name") or "?" for r in report["rows"].values() if r["health"] == "not_run")
    if never:
        lines.append(f"NOT_RUN  {len(never)} configured collectors never recorded: {', '.join(never[:6])}"
                     + (", ..." if len(never) > 6 else ""))
    for r in bad:
        detail = (f"last attempt {r.get('last_attempt') or r.get('last_run') or 'never'}, "
                  f"last success {r.get('last_success') or 'never'}, {r.get('items', 0)} items")
        if r.get("consecutive_failures"):
            detail += f", {r['consecutive_failures']} consecutive failures"
        if r.get("fallback_used"):
            detail += ", fallback used"
        err = (r.get("errors") or [None])[0]
        lines.append(f"{r['health'].upper():8s} {r.get('name')} [{r.get('collector_type') or '?'}]: {detail}"
                     + (f" -- {err}" if err and r["health"] in ("failed", "partial") else ""))
    return lines


def log_run(entry: dict) -> None:
    """Log one recorded run at a level that matches it: failure or partial = warning, recovery = info, a steady
    ok run = debug (no per-run noise at INFO)."""
    previous = entry.get("previous_state")
    if entry["state"] == "failed":
        logger.warning("Collector %s FAILED (%s consecutive): %s", entry["name"], entry.get("consecutive_failures"),
                       entry.get("last_error"))
    elif entry["state"] == "partial":
        logger.warning("Collector %s partial: %d items, %d errors (%s)", entry["name"], entry.get("items", 0),
                       len(entry.get("errors") or []), (entry.get("errors") or [""])[0])
    elif previous in ("failed", "partial"):
        logger.info("Collector %s recovered: %d items", entry["name"], entry.get("items", 0))
    else:
        logger.debug("Collector %s ok: %d items in %.1fs", entry["name"], entry.get("items", 0),
                     entry.get("duration_s", 0))


def outage_since(entry: dict | None, since: datetime) -> bool:
    """True when this collector's data since ``since`` may be missing for operational reasons: it failed after
    ``since``, has no recorded success since then, or has no record at all."""
    if not entry:
        return True
    last_fail, last_ok = parse_time(entry.get("last_failure")), parse_time(entry.get("last_success"))
    if last_fail and last_fail >= since:
        return True
    return not last_ok or last_ok < since
