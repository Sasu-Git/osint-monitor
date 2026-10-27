"""Membership-decision provenance: one JSON line per decision about Development membership (observability only).

Off unless enabled (``OSINT_MEMBERSHIP_LOG=true``). When on, ``persist_clusters`` and the dedup path append a
record for every item they attach to a Development, create a Development with, or hold below the Development layer,
with the evidence the decision already used: supporting members, similarities, the override that admitted the
link, place compatibility, competing Developments, the cluster it came from. Nothing here is read back by the
pipeline, and writing never changes or fails a decision: any error is swallowed (and logged at debug).

Storage: rotating JSONL (``membership_log_path``, default ``data/logs/membership_decisions.jsonl``), rotated at
``membership_log_max_bytes`` (10 MB) keeping ``membership_log_backups`` (9) older files: at most about 100 MB.
Appends and rotation are serialised by a process-wide lock (the daemon's tiers are threads of one process); a
separate process writing at the same moment (a manual ``collect``) may interleave whole lines but never fails.

Record fields (absent knowledge is an explicit null, never a guess):
  at, run_id, item_id, event_id, decision (accepted | rejected), path (formation | late_attachment | dedup |
  structured | held), reason, supporting_member_ids, n_links, best_cosine, best_headline_cosine, similarity,
  override (null | "headline_6h" | "p7"), segmentation (guard verdict on the supporting link), places_compatible,
  actors_compatible, independent_origins, competing_event_ids, cluster_fingerprint, core_check, source.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)
_lock = threading.Lock()

FIELDS = ("at", "run_id", "item_id", "event_id", "decision", "path", "reason", "supporting_member_ids", "n_links",
          "best_cosine", "best_headline_cosine", "similarity", "override", "segmentation", "places_compatible",
          "actors_compatible", "independent_origins", "competing_event_ids", "cluster_fingerprint", "core_check",
          "source")


@dataclass(frozen=True)
class Writer:
    path: Path
    max_bytes: int
    backups: int

    def record(self, **fields) -> None:
        """Append one decision record. Never raises."""
        try:
            entry = {k: fields.get(k) for k in FIELDS}
            entry["at"] = entry["at"] or datetime.now(timezone.utc).isoformat(timespec="seconds")
            if entry["run_id"] is None:
                from osint_monitor.core.runs import current_run_id
                entry["run_id"] = current_run_id()
            line = json.dumps(entry, ensure_ascii=False, default=str) + "\n"
            with _lock:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                self._rotate(len(line.encode("utf-8")))
                with open(self.path, "a", encoding="utf-8") as f:
                    f.write(line)
        except Exception as e:                               # provenance must never fail the pipeline
            logger.debug(f"membership log write skipped: {e}")

    def _rotate(self, incoming: int) -> None:
        try:
            size = self.path.stat().st_size
        except FileNotFoundError:
            return
        if size + incoming <= self.max_bytes:
            return
        for n in range(self.backups, 0, -1):                 # .9 dropped, .8 -> .9, ..., current -> .1
            src = self.path.with_name(f"{self.path.name}.{n - 1}") if n > 1 else self.path
            dst = self.path.with_name(f"{self.path.name}.{n}")
            if src.exists():
                os.replace(src, dst)
        if self.backups == 0:
            self.path.unlink(missing_ok=True)


def writer() -> Writer | None:
    """The configured writer, or None when membership logging is off (the default) or the settings cannot load."""
    try:
        from osint_monitor.core.config import get_settings
        s = get_settings()
        if not s.membership_log:
            return None
        return Writer(Path(s.membership_log_path), max(1_000, int(s.membership_log_max_bytes)),
                      max(0, int(s.membership_log_backups)))
    except Exception as e:
        logger.debug(f"membership log disabled: {e}")
        return None


def cluster_fingerprint(item_ids) -> str | None:
    """A short, stable id of the cluster a decision came from (sha1 of its sorted item ids)."""
    try:
        return hashlib.sha1(",".join(str(i) for i in sorted(item_ids)).encode()).hexdigest()[:12]
    except Exception:
        return None
