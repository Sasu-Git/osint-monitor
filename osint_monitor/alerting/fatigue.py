"""Alert deduplication via trigger_key.

Every alert carries a trigger_key that uniquely identifies the state transition
that caused it. An alert only fires if no existing alert has the same trigger_key.
This replaces the old cooldown-based fatigue system.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, time

from sqlalchemy.orm import Session

from osint_monitor.core.config import load_alerts_config
from osint_monitor.core.database import Alert

logger = logging.getLogger(__name__)


class FatigueManager:
    """Deduplicates alerts by trigger_key. An alert fires once per state transition."""

    def __init__(self, session: Session):
        self.session = session
        self._config = load_alerts_config()

    def is_duplicate(self, alert: Alert) -> bool:
        """True if this alert's trigger_key already exists (transition already alerted)."""
        # No trigger_key means legacy alert — let it through but log a warning
        if not alert.trigger_key:
            logger.warning(f"Alert without trigger_key: {alert.title}")
            return False
        return self.session.query(Alert.id).filter(Alert.trigger_key == alert.trigger_key).first() is not None

    def is_quiet(self, alert: Alert) -> bool:
        """True if a non-critical alert falls in quiet hours: it is recorded but not notified."""
        return alert.severity < 1.0 and self._in_quiet_hours()

    def should_fire(self, alert: Alert) -> bool:
        """True if the alert is new and may be notified now."""
        return not self.is_duplicate(alert) and not self.is_quiet(alert)

    def supersede(self, old_trigger_key: str, new_alert: Alert):
        """Mark a previous alert as superseded by a new one."""
        old = (
            self.session.query(Alert)
            .filter(Alert.trigger_key == old_trigger_key)
            .first()
        )
        if old and new_alert.id:
            old.superseded_by_id = new_alert.id

    def _in_quiet_hours(self) -> bool:
        """Check if current time is within quiet hours."""
        qh = self._config.quiet_hours
        if not qh or not qh.get("start") or not qh.get("end"):
            return False

        now = datetime.utcnow().time()
        try:
            start_parts = qh["start"].split(":")
            end_parts = qh["end"].split(":")
            start = time(int(start_parts[0]), int(start_parts[1]))
            end = time(int(end_parts[0]), int(end_parts[1]))

            if start <= end:
                return start <= now <= end
            else:
                return now >= start or now <= end
        except Exception:
            return False
