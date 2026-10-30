"""Anomaly detection and rolling metrics for entity trends.

Anomalies are measured against a baseline rebuilt from the items at each run, over a stable source cohort and by
event time (``detect_anomalies``), so a change in the source set or a collection outage is not read as a world
signal. Stored trend snapshots feed the dashboard's entity trend view, not the anomaly baseline."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

import numpy as np
from scipy import stats as scipy_stats
from sqlalchemy import func
from sqlalchemy.orm import Session

from osint_monitor.core.database import (
    Alert, Entity, ItemEntity, RawItem, TrendSnapshot,
    get_session, init_db,
)
from osint_monitor.core.models import AlertType, TrendPoint

logger = logging.getLogger(__name__)

# Windows for rolling metrics (hours)
WINDOWS = [6, 24, 168]  # 6h, 24h, 7d
ANOMALY_SIGMA = 2.0
HISTORICAL_DAYS = 30
# Baseline rules (post-soak item 2, docs/operations/deploy-20261005/PLAN.md)
COHORT_MIN_DAYS = 14         # a source counts once it has collected this long
MIN_BASELINE_DAYS = 7        # complete cohort days needed before any anomaly is raised
INCOMPLETE_DAY_RATIO = 0.5   # a day below this share of the median cohort volume is an outage, not a baseline day
MIN_CURRENT_MENTIONS = 5     # fewer mentions in the last 24 h are noise for a rare entity, whatever the sigma


def compute_entity_mention_counts(
    session: Session,
    window_hours: int = 24,
) -> dict[int, int]:
    """Count mentions per entity in the given window."""
    cutoff = datetime.utcnow() - timedelta(hours=window_hours)

    rows = (
        session.query(
            ItemEntity.entity_id,
            func.count(ItemEntity.id).label("mention_count"),
        )
        .join(RawItem, RawItem.id == ItemEntity.item_id)
        .filter(RawItem.fetched_at >= cutoff)
        .group_by(ItemEntity.entity_id)
        .all()
    )

    return {entity_id: count for entity_id, count in rows}


def snapshot_trends(session: Session):
    """Compute and store trend snapshots for all entities across all windows."""
    now = datetime.utcnow()

    for window_hours in WINDOWS:
        counts = compute_entity_mention_counts(session, window_hours)

        for entity_id, count in counts.items():
            snapshot = TrendSnapshot(
                entity_id=entity_id,
                metric_name="mention_count",
                metric_value=float(count),
                window_start=now - timedelta(hours=window_hours),
                window_end=now,
            )
            session.add(snapshot)

    session.commit()
    logger.info(f"Stored trend snapshots for {len(WINDOWS)} windows")


def trend_cohort(session: Session, now: datetime) -> tuple[set[int], datetime | None]:
    """Sources that have collected for at least COHORT_MIN_DAYS, and the time from which all of them were collecting.
    Baseline and current window use only these sources, so adding (or removing) a source cannot raise an anomaly by
    itself: a new source enters with COHORT_MIN_DAYS of its own history (docs/operations/deploy-20261005/PLAN.md)."""
    first = dict(session.query(RawItem.source_id, func.min(RawItem.fetched_at)).group_by(RawItem.source_id).all())
    cutoff = now - timedelta(days=COHORT_MIN_DAYS)
    members = {s for s, t in first.items() if t is not None and t <= cutoff}
    return members, (max(first[s] for s in members) if members else None)


def _event_time(item_published: datetime | None, item_fetched: datetime | None) -> datetime | None:
    return item_published or item_fetched


def cohort_daily_counts(session: Session, sources: set[int], start: datetime, end: datetime
                        ) -> tuple[dict[int, dict], dict, dict[int, int]]:
    """Per entity mentions per calendar day (event time), items per day, and per entity mentions in the last 24 h
    before ``end``, all from the cohort's items with an event time in [start, end)."""
    from collections import defaultdict
    per_entity: dict[int, dict] = defaultdict(lambda: defaultdict(int))
    current: dict[int, int] = defaultdict(int)
    volume: dict = defaultdict(int)
    window = end - timedelta(hours=24)
    items = (session.query(RawItem.id, RawItem.published_at, RawItem.fetched_at)
             .filter(RawItem.source_id.in_(sources), RawItem.fetched_at >= start - timedelta(days=2)).all())
    when = {}
    for item_id, pub, fetched in items:
        t = _event_time(pub, fetched)
        if t is not None and start <= t < end:
            when[item_id] = t
            volume[t.date()] += 1
    ids = list(when)
    for n in range(0, len(ids), 5000):                 # SQLite caps bound variables per statement
        for entity_id, item_id in session.query(ItemEntity.entity_id, ItemEntity.item_id).filter(
                ItemEntity.item_id.in_(ids[n:n + 5000])).all():
            t = when[item_id]
            if t >= window:
                current[entity_id] += 1
            else:
                per_entity[entity_id][t.date()] += 1
    return per_entity, volume, current


def detect_anomalies(session: Session, now: datetime | None = None) -> list[TrendPoint]:
    """Entities whose mentions in the last 24 h are at least ANOMALY_SIGMA above their daily baseline.

    The baseline is rebuilt from the items at every run (no stored baseline to go stale): the stable source cohort
    (``trend_cohort``), mentions counted by event time (publication, else collection), the complete days of the last
    HISTORICAL_DAYS on which every cohort source was collecting (a day with less than INCOMPLETE_DAY_RATIO of the
    median cohort volume is an outage and is skipped), at least MIN_BASELINE_DAYS of them. Days without a mention count
    as zero. The standard deviation is floored at the Poisson level, sqrt(mean) and at least 1, and an anomaly needs at
    least MIN_CURRENT_MENTIONS mentions in the last 24 h."""
    now = now or datetime.utcnow()
    sources, all_collecting = trend_cohort(session, now)
    if not sources:
        return []
    window_start = now - timedelta(hours=24)
    first_day = max(all_collecting, now - timedelta(days=HISTORICAL_DAYS))
    first_day = datetime.combine(first_day.date() + timedelta(days=1), datetime.min.time())   # first full day
    per_entity, volume, current = cohort_daily_counts(session, sources, first_day, now)
    days = [first_day.date() + timedelta(days=i) for i in range((window_start.date() - first_day.date()).days)]
    if not days:
        return []
    median = float(np.median([volume.get(d, 0) for d in days]))
    complete = [d for d in days if volume.get(d, 0) >= INCOMPLETE_DAY_RATIO * median and volume.get(d, 0) > 0]
    if len(complete) < MIN_BASELINE_DAYS:
        logger.info(f"Trend baseline: {len(complete)} complete cohort days (< {MIN_BASELINE_DAYS}); no anomalies")
        return []

    anomalies: list[TrendPoint] = []
    for entity_id, current_count in current.items():
        if current_count < MIN_CURRENT_MENTIONS:
            continue
        values = [per_entity.get(entity_id, {}).get(d, 0) for d in complete]
        mean = float(np.mean(values))
        std = max(float(np.std(values)), float(np.sqrt(mean)), 1.0)
        sigma = (current_count - mean) / std
        if sigma >= ANOMALY_SIGMA:
            entity = session.get(Entity, entity_id)
            anomalies.append(TrendPoint(
                entity_name=entity.canonical_name if entity else f"entity_{entity_id}",
                metric_name="mention_count_24h",
                metric_value=float(current_count),
                window_start=window_start,
                window_end=now,
                is_anomaly=True,
                sigma=sigma,
            ))
            logger.info(
                f"ANOMALY: {entity.canonical_name if entity else entity_id} "
                f"at {current_count} mentions ({sigma:.1f} sigma, baseline {mean:.1f}/day over {len(complete)} days)"
            )

    return anomalies


def create_trend_alerts(session: Session, anomalies: list[TrendPoint]):
    """Create TREND alerts for detected anomalies."""
    for anomaly in anomalies:
        alert = Alert(
            alert_type=AlertType.TREND.value,
            severity=min(0.5 + anomaly.sigma * 0.1, 1.0),
            title=f"Anomalous activity: {anomaly.entity_name}",
            detail=(
                f"{anomaly.entity_name} has {anomaly.metric_value:.0f} mentions "
                f"in the last 24h ({anomaly.sigma:.1f} sigma above 30-day average)"
            ),
        )
        session.add(alert)

    session.commit()


def get_entity_trend(
    session: Session,
    entity_id: int,
    days: int = 30,
) -> list[dict]:
    """Get trend data for a specific entity."""
    cutoff = datetime.utcnow() - timedelta(days=days)
    snapshots = (
        session.query(TrendSnapshot)
        .filter(
            TrendSnapshot.entity_id == entity_id,
            TrendSnapshot.window_end >= cutoff,
        )
        .order_by(TrendSnapshot.window_end)
        .all()
    )

    return [
        {
            "metric": s.metric_name,
            "value": s.metric_value,
            "window_start": s.window_start.isoformat(),
            "window_end": s.window_end.isoformat(),
        }
        for s in snapshots
    ]
