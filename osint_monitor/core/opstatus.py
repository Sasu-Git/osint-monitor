"""Operator status (``python main.py status``): daemon heartbeat, latest pipeline runs, collector health,
collection gaps, NLP model degradation and alert delivery. Read-only: files under data/logs and, for SQLite, the
database opened with ``mode=ro``. Works with no daemon activity and no database."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

from osint_monitor.core import gaps as G


def _age(then: datetime, now: datetime) -> str:
    s = int((now - then).total_seconds())
    return f"{s // 3600}h{(s % 3600) // 60:02d}m" if s >= 3600 else f"{s // 60}m{s % 60:02d}s"


def daemon_lines(now: datetime) -> list[str]:
    from osint_monitor.collectors.status import default_intervals
    from osint_monitor.core import scheduler
    lines = [f"Pipeline: {'PAUSED (since ' + scheduler.get_status()['paused_since'] + ')' if scheduler.is_paused() else 'not paused'}"]
    try:
        ticks = {k: datetime.fromisoformat(v) for k, v in json.loads(scheduler._TICK_FILE.read_text(encoding="utf-8")).items()}
    except FileNotFoundError:
        ticks = {}
    except (OSError, ValueError, TypeError) as e:
        return lines + [f"Daemon heartbeat: tier tick file unreadable ({e})"]
    if not ticks:
        return lines + ["Daemon heartbeat: no tier ticks recorded (daemon never ran here, or ran before tick tracking)"]
    intervals = default_intervals()
    for tier in ("hot", "warm", "cold"):
        t = ticks.get(tier)
        if t is None:
            lines.append(f"  {tier:4s}: no tick recorded")
            continue
        late = (now - t).total_seconds() > max(G.GAP_FACTOR * intervals[tier], G.GAP_MIN_SECONDS)
        lines.append(f"  {tier:4s}: last tick {t:%Y-%m-%d %H:%M:%S} UTC ({_age(t, now)} ago, every {intervals[tier]}s)"
                     + ("  SILENT: daemon stopped, host asleep or scheduler blocked (cause unknown)" if late else ""))
    return lines


def pipeline_lines(db_url: str) -> list[str]:
    conn = G.open_readonly(db_url)
    if conn is None:
        path = G.sqlite_path(db_url)
        return [f"Latest pipeline runs: database not found ({path})" if path else
                "Latest pipeline runs: not shown for non-SQLite databases (read-only path is SQLite only)"]
    try:
        if not G.has_table(conn, "pipeline_runs"):
            ver = conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone() \
                if G.has_table(conn, "schema_meta") else None
            return [f"Latest pipeline runs: no run ledger (schema {ver[0] if ver else '?'} < 5; migrate to record runs)"]
        lines = ["Latest pipeline runs:"]
        for tier in ("hot", "warm", "cold", None):
            row = conn.execute("SELECT started_at, finished_at, status, items_collected, items_new, stages, code_sha, error "
                               "FROM pipeline_runs WHERE " + ("tier = ?" if tier else "tier IS NULL") +
                               " ORDER BY started_at DESC LIMIT 1", (tier,) if tier else ()).fetchone()
            if row is None:
                continue
            started, finished, status, collected, new, stages, sha, err = row
            try:
                stages = json.loads(stages) if isinstance(stages, str) else (stages or {})
            except ValueError:
                stages = {}
            failed = [k for k, v in stages.items() if str(v).startswith("failed")]
            lines.append(f"  {tier or 'oneshot':7s} {str(started)[:19]} {status.upper():8s} collected {collected}, new {new}"
                         + (f", FAILED stages: {', '.join(failed)}" if failed else "")
                         + (f", code {sha[:10]}" if sha else "") + (f" -- {err[:120]}" if err else "")
                         + ("" if finished else "  (still running or interrupted)"))
        return lines if len(lines) > 1 else ["Latest pipeline runs: none recorded yet"]
    finally:
        conn.close()


def gap_lines(db_url: str, now: datetime, hours: int = 24) -> list[str]:
    start = now - timedelta(hours=hours)
    rep = G.report(start, now, "warm", db_url=db_url)
    lines = [f"Collection, last {hours} h:"] + ["  " + x for x in G.format_report(rep)]
    recorded = rep["recorded_gaps"]
    if recorded:
        lines.append(f"  recorded gap events: {len(recorded)} (data/logs/collection_gaps.jsonl)")
    return lines


def alert_delivery_lines() -> list[str]:
    from osint_monitor.alerting.channels import load_delivery_status
    data = load_delivery_status()
    if not data:
        return ["Alert delivery: no delivery attempts recorded"]
    bad = {k: v for k, v in data.items() if v.get("consecutive_failures")}
    lines = [f"Alert delivery: {len(data)} channels, {len(bad)} failing"]
    for k, v in sorted(bad.items()):
        lines.append(f"  FAILING {k}: {v['consecutive_failures']} consecutive since {v.get('last_success') or 'never'} "
                     f"-- {v.get('last_error')}")
    return lines


def status_lines(now: datetime | None = None, db_url: str | None = None) -> list[str]:
    now = now or datetime.utcnow()
    if db_url is None:
        from osint_monitor.core.config import get_settings
        db_url = get_settings().db_url
    from osint_monitor.collectors.status import format_status
    from osint_monitor.processors.nlp import format_ner_status
    out = daemon_lines(now)
    out += [""] + pipeline_lines(db_url)
    out += ["", "Collectors (data/logs/collector_status.json):"] + ["  " + x for x in format_status(now=now)]
    out += [""] + gap_lines(db_url, now)
    out += ["", "Entity extraction:"] + ["  " + x for x in format_ner_status()]
    out += [""] + alert_delivery_lines()
    return out
