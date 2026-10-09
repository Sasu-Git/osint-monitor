"""Typed relations between Developments (Phase 3): the runtime taxonomy contract and persistence.

The contract is ``evaluations/relations/taxonomy.md`` (revision 1) with the owner's runtime decision of 2026-10-07:

- three runtime types: ``same_calamity_lifecycle`` and ``same_convened_event`` (symmetric episode types) and
  ``reaction_to`` (directed: the **reaction** responds to the **trigger**);
- canonical relations are explicit-only: a relation is *accepted* only on ``explicit`` evidence; ``inferred`` links
  are never emitted at runtime;
- both endpoints are real Development IDs. There is no free-text endpoint: a link to an occurrence the system has no
  Development for is not stored (third-event links included);
- a relation never merges Developments and never changes Situation membership;
- shared actors, a shared place, temporal proximity, the same storyline or Situation, the same topic or high text
  similarity are never sufficient on their own (candidates may be *proposed* from them; acceptance needs evidence).

Gold-only types (``follow_up_to``, ``commentary_on``, ``same_attack_wave`` deferred; ``caused_by``,
``co_caused_with`` dropped from the Phase 3 runtime) cannot be stored.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy.orm import Session

from osint_monitor.core.database import DevelopmentRelation, Event, EventItem


@dataclass(frozen=True)
class RelationSpec:
    name: str
    directed: bool
    roles: tuple[str, str] | None      # (source role, target role) for directed types
    definition: str


RUNTIME_TYPES: dict[str, RelationSpec] = {
    "same_calamity_lifecycle": RelationSpec(
        "same_calamity_lifecycle", False, None,
        "both are stages of one natural or health calamity in a bounded area (the same hazard event, an "
        "overlapping area)"),
    "same_convened_event": RelationSpec(
        "same_convened_event", False, None,
        "both belong to one bounded scheduled gathering (the same visit, summit, conference or session)"),
    "reaction_to": RelationSpec(
        "reaction_to", True, ("reaction", "trigger"),
        "the reaction is a statement or action by an actor that explicitly responds to the trigger occurrence"),
}
GOLD_ONLY_TYPES = {"follow_up_to": "deferred", "commentary_on": "deferred", "same_attack_wave": "deferred",
                   "caused_by": "dropped from the Phase 3 runtime", "co_caused_with": "dropped from the Phase 3 runtime"}
STATUSES = ("candidate", "accepted", "rejected")
EVIDENCE_KINDS = ("explicit", "inferred", "none")


class RelationError(ValueError):
    """A relation that the contract does not allow."""


@dataclass
class Proposal:
    """One relation to record. For ``reaction_to``, ``source`` is the reaction and ``target`` the trigger; for
    symmetric types the order does not matter (stored lower ID first)."""
    relation_type: str
    source_event_id: int
    target_event_id: int
    status: str
    evidence_kind: str
    method: str
    evidence: list[dict] = field(default_factory=list)   # [{item_id, side: source|target, cue, text}]


def check(session: Session, p: Proposal) -> Proposal:
    """Validate a proposal against the contract; returns it normalised (symmetric types: lower ID first)."""
    spec = RUNTIME_TYPES.get(p.relation_type)
    if spec is None:
        why = GOLD_ONLY_TYPES.get(p.relation_type, "not in the taxonomy")
        raise RelationError(f"{p.relation_type!r} is not a runtime relation type ({why})")
    if not (isinstance(p.source_event_id, int) and isinstance(p.target_event_id, int)):
        raise RelationError("both endpoints must be Development IDs (int); free-text endpoints are not allowed")
    if p.source_event_id == p.target_event_id:
        raise RelationError("a relation connects two distinct Developments; one Development is an identity matter")
    if p.status not in STATUSES:
        raise RelationError(f"status {p.status!r} not in {STATUSES}")
    if p.evidence_kind not in EVIDENCE_KINDS:
        raise RelationError(f"evidence kind {p.evidence_kind!r} not in {EVIDENCE_KINDS}")
    if p.status == "accepted" and p.evidence_kind != "explicit":
        raise RelationError("only explicit evidence makes a canonical (accepted) relation; inferred links are "
                            "never emitted at runtime")
    if p.status == "accepted" and not p.evidence:
        raise RelationError("an accepted relation must cite the items and spans it rests on")
    found = {e for (e,) in session.query(Event.id).filter(Event.id.in_([p.source_event_id, p.target_event_id]))}
    missing = {p.source_event_id, p.target_event_id} - found
    if missing:
        raise RelationError(f"no Development with ID {sorted(missing)}")
    sides = {"source": p.source_event_id, "target": p.target_event_id}
    for ev in p.evidence:
        if ev.get("side") not in sides or not isinstance(ev.get("item_id"), int):
            raise RelationError(f"evidence entries need an item_id and side source|target: {ev}")
        member = session.query(EventItem.id).filter_by(event_id=sides[ev["side"]], item_id=ev["item_id"]).first()
        if member is None:
            raise RelationError(f"evidence item {ev['item_id']} is not a member of Development {sides[ev['side']]}")
    if not spec.directed and p.source_event_id > p.target_event_id:
        flip = {"source": "target", "target": "source"}
        return Proposal(p.relation_type, p.target_event_id, p.source_event_id, p.status, p.evidence_kind, p.method,
                        [{**ev, "side": flip[ev["side"]]} for ev in p.evidence])
    return p


def record(session: Session, p: Proposal, run_id: str | None = None,
           now: datetime | None = None) -> DevelopmentRelation:
    """Insert or update one relation (unique per type and endpoint pair). The caller commits."""
    p = check(session, p)
    now = now or datetime.utcnow()
    row = (session.query(DevelopmentRelation)
           .filter_by(relation_type=p.relation_type, source_event_id=p.source_event_id,
                      target_event_id=p.target_event_id).first())
    if row is None:
        row = DevelopmentRelation(relation_type=p.relation_type, source_event_id=p.source_event_id,
                                  target_event_id=p.target_event_id, created_at=now, created_run_id=run_id)
        session.add(row)
    row.status, row.evidence_kind, row.evidence, row.method = p.status, p.evidence_kind, p.evidence, p.method
    row.updated_at, row.updated_run_id = now, run_id
    session.flush()
    return row


def relations_of(session: Session, event_id: int, status: str | None = "accepted") -> list[DevelopmentRelation]:
    """Relations touching one Development (default: accepted only)."""
    q = session.query(DevelopmentRelation).filter(
        (DevelopmentRelation.source_event_id == event_id) | (DevelopmentRelation.target_event_id == event_id))
    if status:
        q = q.filter(DevelopmentRelation.status == status)
    return q.order_by(DevelopmentRelation.id).all()
