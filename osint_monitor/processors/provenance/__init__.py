"""Source provenance and confidence: EvidenceItems -> ConfidenceAssessment.

Corroboration counts independent origins, not outlets: syndicated wire copy and
reports attributed to another outlet collapse into that origin, and analysis never
counts as confirmation. Confidence is kept separate from significance.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from osint_monitor.core.models import ConfidenceAssessment
from osint_monitor.processors.provenance.confidence import assess_confidence
from osint_monitor.processors.provenance.context import build_evidence
from osint_monitor.processors.provenance.resolve import ProvenanceResolver

__all__ = ["ProvenanceResolver", "assess_confidence", "assess_event", "build_evidence"]


def assess_event(session: Session, event_id: int,
                 resolver: ProvenanceResolver | None = None) -> ConfidenceAssessment:
    return assess_confidence(build_evidence(session, event_id), resolver)
