"""APScheduler-based tiered pipeline orchestration.

Three collection tiers run at different intervals:
  - hot  (2.5 min): ADS-B, DNS, currency, commodities, defense stocks, seismic
  - warm (10 min):   RSS, Nitter, travel advisories, OONI, flight routes, GDELT, cables, BGP
  - cold (60 min):   FIRMS, USGS, ACLED, sanctions, NVD, UNHCR, IAEA, Wikipedia, SEC, finance

Each tier collects, processes deltas (dedup + NLP on new items only), and triggers
post-processing (clustering, fusion, I&W) only when new items appear. If a tier is
still running when its next tick fires, the tick is skipped.

Resume behaviour (host suspend, scheduler blocked): every job's slots are staggered by a
fixed offset (JOB_OFFSETS), so tiers never become due in the same second; a run more than
MISFIRE_GRACE_SECONDS late is skipped and coalesced into the next slot, never replayed; and
tiers collect concurrently but write one at a time (pipeline.DB_WRITE_LOCK). Long silences
are reported as collection gaps (log, status, data/logs/collection_gaps.jsonl): the daemon
does not keep the host awake -- see docs/operations.md.
"""

from __future__ import annotations

import json
import logging
import threading
from collections import deque
from datetime import datetime, timedelta, timezone
from pathlib import Path

from apscheduler.events import EVENT_JOB_MISSED
from apscheduler.schedulers.background import BackgroundScheduler

from osint_monitor.core.database import get_session, init_db

logger = logging.getLogger(__name__)

# Per-tier locks: if a tier is still running when its next tick fires, skip it.
_tier_locks = {
    "hot": threading.Lock(),
    "warm": threading.Lock(),
    "cold": threading.Lock(),
}

# Pause flag file: when this file exists, all tier jobs skip their tick.
_PAUSE_FLAG = Path(__file__).parent.parent.parent / "data" / "pause"

# Module-level reference to the active scheduler (set by create_scheduler)
_active_scheduler: BackgroundScheduler | None = None

# Fixed per-job offsets (seconds) added to the first run. With the default intervals (150 s,
# 600 s, 3600 s, 600 s, 7200 s) no two jobs ever share a slot.
JOB_OFFSETS = {"tier_hot": 0, "tier_warm": 40, "tier_cold": 80, "alerts": 20, "analysis": 100}
MISFIRE_GRACE_SECONDS = 30        # later than this: skip the stale run (coalesced), do not replay it
GAP_FACTOR = 3                    # a tier silent for > 3 intervals (and > GAP_MIN_SECONDS) is a gap
GAP_MIN_SECONDS = 900
_GAP_LOG = Path(__file__).parent.parent.parent / "data" / "logs" / "collection_gaps.jsonl"

_TICK_FILE = Path(__file__).parent.parent.parent / "data" / "logs" / "tier_ticks.json"

_last_tick: dict[str, datetime] = {}
_intervals: dict[str, int] = {}
_recent_gaps: deque = deque(maxlen=50)


def record_gap(kind: str, subject: str, since: datetime, until: datetime, expected_seconds: int | None = None) -> dict:
    """Report a collection gap: logged as a warning, kept for status, appended to the gap log."""
    seconds = int((until - since).total_seconds())
    gap = {"kind": kind, "subject": subject, "from": since.isoformat(timespec="seconds"),
           "to": until.isoformat(timespec="seconds"), "seconds": seconds, "expected_every": expected_seconds}
    logger.warning(f"Collection gap ({kind}): {subject} idle {timedelta(seconds=seconds)} "
                   f"from {gap['from']} to {gap['to']}"
                   + (f", expected every {expected_seconds}s" if expected_seconds else "")
                   + (" -- the daemon process was not running (why it stopped is unknown)" if kind == "daemon_down"
                      else " -- cause unknown: host suspend, a blocked scheduler or a stopped process cannot be "
                           "told apart"))
    _recent_gaps.append(gap)
    try:
        _GAP_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(_GAP_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(gap) + "\n")
    except OSError:
        pass
    return gap


def _load_ticks() -> dict[str, datetime]:
    try:
        return {k: datetime.fromisoformat(v) for k, v in json.loads(_TICK_FILE.read_text(encoding="utf-8")).items()}
    except (OSError, ValueError, TypeError):
        return {}


def _save_tick(tier: str, when: datetime) -> None:
    try:
        ticks = {k: v.isoformat() for k, v in _load_ticks().items()}
        ticks[tier] = when.isoformat()
        _TICK_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = _TICK_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(ticks), encoding="utf-8")
        tmp.replace(_TICK_FILE)
    except OSError:
        pass


def check_tier_gap(tier: str, now: datetime | None = None) -> dict | None:
    """Called when a tier tick starts: a gap if the tier has been silent for too long. The last tick is
    also persisted, so the first tick after a daemon restart measures the silence since the previous
    process's last tick (a crash, a reboot or a stopped daemon is a gap too)."""
    now = now or datetime.utcnow()
    last, interval = _last_tick.get(tier), _intervals.get(tier)
    kind = "tier_silence"
    if last is None:
        last, kind = _load_ticks().get(tier), "daemon_down"
    _last_tick[tier] = now
    _save_tick(tier, now)
    if last is None or not interval:
        return None
    if (now - last).total_seconds() > max(GAP_FACTOR * interval, GAP_MIN_SECONDS):
        return record_gap(kind, f"{tier} tier", last, now, interval)
    return None


def _on_job_missed(event) -> None:
    """APScheduler skipped a run that was more than the misfire grace late. With coalescing it
    reports only the latest stale slot, so this is a lower bound on the gap; the full silence is
    measured by check_tier_gap on the tier's next tick."""
    late = datetime.now(event.scheduled_run_time.tzinfo) - event.scheduled_run_time
    if late.total_seconds() > GAP_MIN_SECONDS:
        # every gap record is naive UTC (scheduled_run_time is aware, in the scheduler's local zone)
        record_gap("missed_run", event.job_id,
                   event.scheduled_run_time.astimezone(timezone.utc).replace(tzinfo=None), datetime.utcnow())


def is_paused() -> bool:
    """Check whether the pipeline is paused."""
    return _PAUSE_FLAG.exists()


def pause():
    """Pause all tier collection. Creates the pause flag file."""
    _PAUSE_FLAG.parent.mkdir(parents=True, exist_ok=True)
    _PAUSE_FLAG.write_text(datetime.utcnow().isoformat())
    logger.info("Pipeline PAUSED")


def resume():
    """Resume tier collection. Removes the pause flag file."""
    try:
        _PAUSE_FLAG.unlink()
    except FileNotFoundError:
        pass
    logger.info("Pipeline RESUMED")


def get_status() -> dict:
    """Return current daemon status."""
    paused = is_paused()
    jobs = []
    if _active_scheduler:
        for job in _active_scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
            })
    return {
        "running": _active_scheduler is not None,
        "paused": paused,
        "paused_since": _PAUSE_FLAG.read_text().strip() if paused else None,
        "jobs": jobs,
        "last_tick": {t: v.isoformat(timespec="seconds") for t, v in _last_tick.items()},
        "recent_gaps": list(_recent_gaps)[-10:],
    }


def _run_tier_job(tier: str):
    """Run collection + delta processing for a single tier."""
    if is_paused():
        logger.debug(f"[{tier}] Pipeline paused, skipping")
        return

    lock = _tier_locks[tier]
    if not lock.acquire(blocking=False):
        logger.info(f"[{tier}] Still running from previous tick, skipping")
        return
    check_tier_gap(tier)
    try:
        from osint_monitor.processors.pipeline import run_tier
        stats = run_tier(tier, quiet=True)
        failed = {k: v for k, v in (stats.get("stages") or {}).items() if str(v).startswith("failed")}
        if failed:
            logger.warning(f"[{tier}] {len(failed)} post-processing stage(s) failed: "
                           + "; ".join(f"{k}: {v}" for k, v in failed.items()))
        new = stats.get("new_items", 0)
        if new > 0:
            logger.info(
                f"[{tier}] Tick complete: {new} new items, "
                f"{stats.get('events_created', 0)} events, "
                f"{stats.get('iw_elevated', 0)} I&W elevated"
            )
            # Push to SSE event bus
            try:
                from osint_monitor.api.websocket import broadcast
                broadcast({
                    "type": "tier_update",
                    "tier": tier,
                    "new_items": new,
                    "events_created": stats.get("events_created", 0),
                    "iw_elevated": stats.get("iw_elevated", 0),
                    "timestamp": datetime.utcnow().isoformat(),
                })
            except Exception:
                pass  # SSE not running (daemon-only mode)
    except Exception as e:
        logger.error(f"[{tier}] Tier job failed: {e}", exc_info=True)
    finally:
        lock.release()
        from osint_monitor.core.watchdog import arm_stack_dump
        arm_stack_dump()          # progress was made: restart the no-progress stack-dump timer


def _run_analysis_job():
    """Scheduled job: run trend analysis + anomaly detection."""
    from osint_monitor.analysis.trends import snapshot_trends, detect_anomalies, create_trend_alerts
    from osint_monitor.processors.pipeline import DB_WRITE_LOCK
    try:
        with DB_WRITE_LOCK:                  # writes: one writer at a time with the tiers
            session = get_session()
            snapshot_trends(session)
            anomalies = detect_anomalies(session)
            if anomalies:
                create_trend_alerts(session, anomalies)
            session.close()
    except Exception as e:
        logger.error(f"Analysis job failed: {e}")


def _run_alert_job():
    """Scheduled job: evaluate alert rules."""
    from osint_monitor.alerting.engine import AlertEngine
    from osint_monitor.alerting.channels import build_channels, dispatch_alerts, persist_deliveries
    from osint_monitor.core.config import load_alerts_config
    from osint_monitor.processors.pipeline import DB_WRITE_LOCK
    try:
        with DB_WRITE_LOCK:                  # writes alerts: one writer at a time with the tiers
            session = get_session()
            try:
                engine = AlertEngine(session)
                alerts = engine.evaluate_all(hours_back=1)
                engine.escalate_unacknowledged()
                for alert in alerts:
                    session.expunge(alert)   # loaded by evaluate_all: readable after the session closes
            finally:
                session.close()

        if alerts:                           # delivery is network I/O: outside the lock
            config = load_alerts_config()
            channels = build_channels([c.model_dump() for c in config.channels])
            deliveries = dispatch_alerts(alerts, channels)
            if deliveries:
                with DB_WRITE_LOCK:
                    session = get_session()
                    try:
                        persist_deliveries(session, deliveries)
                    finally:
                        session.close()
    except Exception as e:
        logger.error(f"Alert job failed: {e}", exc_info=True)


def _run_daily_briefing_job():
    """Scheduled job: generate daily briefing."""
    from osint_monitor.analysis.briefing import generate_daily_briefing
    try:
        result = generate_daily_briefing()
        logger.info(f"Daily briefing generated: {len(result.content_md)} chars")
    except Exception as e:
        logger.error(f"Daily briefing job failed: {e}")


def create_scheduler() -> BackgroundScheduler:
    """Create and configure the tiered background scheduler."""
    from osint_monitor.core.config import load_sources_config
    config = load_sources_config()
    tier_cfg = config.tiers

    global _active_scheduler
    scheduler = BackgroundScheduler(job_defaults={"coalesce": True, "misfire_grace_time": MISFIRE_GRACE_SECONDS,
                                                  "max_instances": 1})
    _active_scheduler = scheduler
    scheduler.add_listener(_on_job_missed, EVENT_JOB_MISSED)
    now = datetime.now().astimezone()

    def first_run(job_id: str, interval: int) -> datetime:
        return now + timedelta(seconds=interval + JOB_OFFSETS.get(job_id, 0))

    # --- Tiered collection ---
    for tier, interval in (("hot", tier_cfg.hot_interval_seconds), ("warm", tier_cfg.warm_interval_seconds),
                           ("cold", tier_cfg.cold_interval_seconds)):
        _intervals[tier] = interval
        scheduler.add_job(
            _run_tier_job,
            "interval",
            seconds=interval,
            start_date=first_run(f"tier_{tier}", interval),
            args=[tier],
            id=f"tier_{tier}",
            name=f"{tier.capitalize()} tier ({interval}s)",
        )

    # --- Non-collection jobs ---
    scheduler.add_job(
        _run_analysis_job,
        "interval",
        hours=2,
        start_date=first_run("analysis", 7200),
        id="analysis",
        name="Trend analysis",
    )

    scheduler.add_job(
        _run_alert_job,
        "interval",
        minutes=10,
        start_date=first_run("alerts", 600),
        id="alerts",
        name="Alert evaluation",
    )

    scheduler.add_job(
        _run_daily_briefing_job,
        "cron",
        hour=6,
        minute=0,
        id="daily_briefing",
        name="Daily briefing",
    )

    return scheduler
