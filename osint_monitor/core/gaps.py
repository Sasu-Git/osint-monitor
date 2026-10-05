"""Read-only collection-gap and coverage reporting.

Answers "when were we actually collecting?" for a time window, from evidence the system already keeps:

- tier run starts: the run ledger (``pipeline_runs``, schema >= 5) or, for an older daemon, the
  ``Running job "<Tier> tier`` lines of a daemon log (local timestamps; pass their UTC offset);
- recorded gaps: ``data/logs/collection_gaps.jsonl`` (``core.scheduler.record_gap``);
- collector state transitions: ``data/logs/collector_events.jsonl`` (``collectors.status``).

Gap levels: ``tier`` (no tier runs at all), ``collector`` (the tier ran but a collector was failed),
``endpoint`` (the collector ran partially). A cause is stated only when the evidence names it:
a ``daemon_down`` record means the daemon process was not running; otherwise a tier silence is
``unknown`` -- host suspend, a blocked scheduler and a stopped process cannot be told apart. Nothing here
writes to a database or a log.
"""

from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DATA_LOGS = Path(__file__).resolve().parents[2] / "data" / "logs"
GAP_LOG = DATA_LOGS / "collection_gaps.jsonl"
EVENTS_LOG = DATA_LOGS / "collector_events.jsonl"
GAP_FACTOR = 3
GAP_MIN_SECONDS = 900
_LOG_TICK = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})[,.]\d+ .*Running job \"(Hot|Warm|Cold) tier", re.I)


def _dt(value) -> datetime:
    return value if isinstance(value, datetime) else datetime.fromisoformat(str(value).replace("Z", "")[:26])


# --- evidence readers ------------------------------------------------------------------------------------------------

def read_jsonl(path: Path) -> tuple[list[dict], int]:
    """(records, malformed line count). A missing file is no records."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return [], 0
    out, bad = [], 0
    for line in lines:
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
            if isinstance(rec, dict):
                out.append(rec)
            else:
                bad += 1
        except ValueError:
            bad += 1
    return out, bad


def read_gap_log(path: Path | None = None) -> list[dict]:
    recs, _ = read_jsonl(path or GAP_LOG)
    out = []
    for r in recs:
        try:
            out.append({**r, "from": _dt(r["from"]), "to": _dt(r["to"])})
        except (KeyError, ValueError, TypeError):
            continue
    return out


def ticks_from_log(path: Path, tier: str, utc_offset_hours: float) -> list[datetime]:
    """Tier run starts from a daemon log whose timestamps are local time ``UTC + utc_offset_hours``."""
    shift = timedelta(hours=utc_offset_hours)
    out = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = _LOG_TICK.match(line)
            if m and m.group(2).lower() == tier.lower():
                out.append(datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S") - shift)
    return sorted(out)


def sqlite_path(db_url: str) -> Path | None:
    return Path(db_url[len("sqlite:///"):]) if db_url.startswith("sqlite:///") else None


def open_readonly(db_url: str) -> sqlite3.Connection | None:
    """A read-only connection to a SQLite database (None when it is not SQLite or does not exist)."""
    path = sqlite_path(db_url)
    if path is None or not path.exists():
        return None
    return sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True)


def has_table(conn: sqlite3.Connection, table: str) -> bool:
    return conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone() is not None


def ticks_from_ledger(conn: sqlite3.Connection, tier: str, start: datetime, end: datetime) -> list[datetime] | None:
    """Tier run starts from ``pipeline_runs``; None when the ledger does not exist (schema < 5)."""
    if not has_table(conn, "pipeline_runs"):
        return None
    rows = conn.execute("SELECT started_at FROM pipeline_runs WHERE tier = ? AND started_at >= ? AND started_at < ? "
                        "ORDER BY started_at", (tier, (start - timedelta(days=1)).isoformat(sep=" "),
                                                end.isoformat(sep=" "))).fetchall()
    return [_dt(r[0]) for r in rows]


# --- computation (pure, deterministic) -------------------------------------------------------------------------------

def merge(intervals: list[tuple[datetime, datetime]]) -> list[tuple[datetime, datetime]]:
    out: list[list[datetime]] = []
    for a, b in sorted(intervals):
        if b <= a:
            continue
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return [(a, b) for a, b in out]


def overlap_seconds(gaps: list[dict], since: datetime, until: datetime) -> float:
    """Seconds of [since, until) covered by the union of the gaps' [from, to) intervals."""
    clipped = [(max(g["from"], since), min(g["to"], until)) for g in gaps]
    return sum((b - a).total_seconds() for a, b in merge(clipped))


def tier_coverage(ticks: list[datetime], interval_s: int, start: datetime, end: datetime) -> dict:
    """Coverage of [start, end) by tier runs (each run covers [tick, tick + interval)) and the tier gaps: spans
    of more than max(GAP_FACTOR x interval, GAP_MIN_SECONDS) without a run, including the window edges."""
    ticks = sorted(ticks)
    window = (end - start).total_seconds()
    step = timedelta(seconds=interval_s)
    covered = merge([(max(t, start), min(t + step, end)) for t in ticks if t + step > start and t < end])
    covered_s = sum((b - a).total_seconds() for a, b in covered)
    threshold = max(GAP_FACTOR * interval_s, GAP_MIN_SECONDS)
    gaps, prev = [], max([t for t in ticks if t <= start], default=None)
    for t in [t for t in ticks if start < t < end] + [end]:
        last = prev if prev is not None else start
        if (t - last).total_seconds() > threshold:
            gaps.append({"from": max(last, start), "to": t, "seconds": int((t - max(last, start)).total_seconds()),
                         "edge": prev is None or t == end})
        prev = t if t != end else prev
    return {"window_seconds": int(window), "covered_seconds": int(covered_s),
            "coverage": round(covered_s / window, 4) if window else 0.0, "runs": sum(1 for t in ticks if start <= t < end),
            "gaps": gaps, "threshold_seconds": threshold}


def classify_tier_gap(gap: dict, recorded: list[dict], tier: str) -> dict:
    """Level and cause for a tier gap, from recorded gap records only. Never inferred beyond the evidence."""
    subject = f"{tier} tier"
    for r in recorded:
        if r.get("subject") == subject and r.get("kind") == "daemon_down" and r["to"] >= gap["from"] and r["from"] <= gap["to"]:
            return {**gap, "level": "tier", "cause": "daemon_not_running",
                    "evidence": f"daemon_down record {r['from']:%Y-%m-%d %H:%M} -> {r['to']:%Y-%m-%d %H:%M}; "
                                "why the process stopped is unknown"}
    return {**gap, "level": "tier", "cause": "unknown",
            "evidence": "no tier runs; host suspend, a blocked scheduler or a stopped process cannot be distinguished"}


def collector_outages(events: list[dict], start: datetime, end: datetime) -> list[dict]:
    """Collector-level (failed) and endpoint-level (partial) periods from state transitions within [start, end)."""
    by_key: dict[str, list[dict]] = {}
    for e in sorted(events, key=lambda e: (e.get("key", ""), e.get("at", ""))):
        if "at" in e and "key" in e:
            by_key.setdefault(e["key"], []).append(e)
    out = []
    for key, evs in by_key.items():
        for i, e in enumerate(evs):
            if e.get("to") not in ("failed", "partial"):
                continue
            a = _dt(e["at"])
            b = _dt(evs[i + 1]["at"]) if i + 1 < len(evs) else end
            a, b = max(a, start), min(b, end)
            if b > a:
                out.append({"key": key, "name": e.get("name"), "level": "collector" if e["to"] == "failed" else "endpoint",
                            "from": a, "to": b, "seconds": int((b - a).total_seconds()),
                            "cause": (e.get("error") or "").split(":", 1)[0] or "unknown",
                            "ongoing": i + 1 == len(evs)})
    return sorted(out, key=lambda o: (o["from"], o["key"]))


# --- report ----------------------------------------------------------------------------------------------------------

def report(start: datetime, end: datetime, tier: str = "warm", *, interval_s: int | None = None,
           db_url: str | None = None, log_path: Path | None = None, log_utc_offset: float = 0.0,
           gap_log: Path | None = None, events_log: Path | None = None) -> dict:
    """Coverage and gaps for one tier over [start, end), with the evidence each figure comes from."""
    if interval_s is None:
        from osint_monitor.collectors.status import default_intervals
        interval_s = default_intervals().get(tier, 600)
    ticks, source = None, None
    if log_path is not None:
        ticks, source = ticks_from_log(Path(log_path), tier, log_utc_offset), f"daemon log {Path(log_path).name}"
    else:
        if db_url is None:
            from osint_monitor.core.config import get_settings
            db_url = get_settings().db_url
        conn = open_readonly(db_url)
        if conn is not None:
            try:
                ticks = ticks_from_ledger(conn, tier, start, end)
                source = "run ledger (pipeline_runs)" if ticks is not None else None
            finally:
                conn.close()
    recorded = [g for g in read_gap_log(gap_log) if g["to"] > start and g["from"] < end]
    events, malformed = read_jsonl(events_log or EVENTS_LOG)
    out = {"tier": tier, "start": start, "end": end, "expected_every_seconds": interval_s, "tick_source": source,
           "recorded_gaps": recorded, "collector_outages": collector_outages(events, start, end),
           "malformed_event_lines": malformed}
    if ticks is None:
        out.update({"coverage": None, "gaps": [],
                    "note": "no tier run evidence: the database has no run ledger (schema < 5) or is unavailable; "
                            "pass a daemon log with --log"})
        return out
    cov = tier_coverage(ticks, interval_s, start, end)
    out.update({**cov, "gaps": [classify_tier_gap(g, recorded, tier) for g in cov["gaps"]]})
    return out


def format_report(r: dict) -> list[str]:
    lines = [f"{r['tier']} tier, {r['start']:%Y-%m-%d %H:%M} -> {r['end']:%Y-%m-%d %H:%M} UTC, "
             f"expected every {r['expected_every_seconds']}s"]
    if r.get("coverage") is None:
        lines.append(f"  coverage: unknown -- {r['note']}")
    else:
        lines.append(f"  coverage: {r['coverage']:.1%} ({r['covered_seconds'] / 3600:.1f} of "
                     f"{r['window_seconds'] / 3600:.1f} h, {r['runs']} runs; source: {r['tick_source']})")
        for g in r["gaps"]:
            lines.append(f"  GAP {g['from']:%m-%d %H:%M} -> {g['to']:%m-%d %H:%M} ({g['seconds'] / 3600:.1f} h) "
                         f"level={g['level']} cause={g['cause']}{' [window edge]' if g['edge'] else ''} -- {g['evidence']}")
    for o in r["collector_outages"]:
        lines.append(f"  {o['level'].upper()} {o['name'] or o['key']}: {o['from']:%m-%d %H:%M} -> {o['to']:%m-%d %H:%M} "
                     f"({o['seconds'] / 3600:.1f} h) cause={o['cause']}{' (ongoing)' if o['ongoing'] else ''}")
    if r.get("malformed_event_lines"):
        lines.append(f"  note: {r['malformed_event_lines']} malformed lines in collector_events.jsonl were skipped")
    return lines
