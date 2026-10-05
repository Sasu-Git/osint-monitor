"""Read-only view models for the Today and Development pages.

Built only from what the pipeline stores (situation_views.DevelopmentView is reused for one
development). Two presentation rules, both from persisted fields, nothing inferred here:

- A Development is corroborated: its cluster has at least MIN_INDEPENDENT_SOURCES independent
  sources (Event.source_count, written by the corroboration stage from provenance). Clusters
  below that stay "awaiting corroboration" and are counted, not listed, on Today (a
  single-source story is not a first-class Development).
- Rank reasons are shown with the labels in config/ranking.yaml, split into reasons that
  raised a development and caveats; the numeric rank score is only used for ordering.

Nothing here writes to the database.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from functools import lru_cache
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from osint_monitor.api.situation_views import DevelopmentView, _canonicalizer, development_view
from osint_monitor.core.database import Event, Situation

MIN_INDEPENDENT_SOURCES = 2
TIME_RANGES = {"24h": 24, "3d": 72, "7d": 168}
CONFIDENCE_ORDER = ["confirmed", "probable", "possible", "disputed", "unverified"]
# rank reasons that lower or qualify a development (shown as caveats, not as "why it surfaced")
CAVEAT_REASONS = {"routine_commentary", "rhetoric_only", "single_source", "unconfirmed_report", "disputed",
                  "weak_evidence", "duplicate_commentary_penalty", "repeated_coverage_penalty",
                  "overshadowed_by_concrete", "concluded", "superseded", "stale"}


@lru_cache(maxsize=1)
def _reason_labels() -> dict[str, str]:
    from osint_monitor.core.config import load_ranking_config
    return {k.value if hasattr(k, "value") else str(k): v for k, v in load_ranking_config().reason_labels.items()}


def reason_label(reason: str) -> str:
    return _reason_labels().get(reason, reason.replace("_", " ").capitalize())


class Reasons(BaseModel):
    surfaced: list[str] = Field(default_factory=list)      # labels, strongest first
    caveats: list[str] = Field(default_factory=list)


def split_reasons(reasons: list[str]) -> Reasons:
    out = Reasons()
    for r in reasons:
        (out.caveats if r in CAVEAT_REASONS else out.surfaced).append(reason_label(r))
    return out


class DevelopmentCard(BaseModel):
    development: DevelopmentView
    rank: int                                             # position in the list, 1 = first
    situation_slug: Optional[str] = None
    situation_title: Optional[str] = None
    independent_sources: int = 0
    corroborated: bool = False
    reasons: Reasons = Field(default_factory=Reasons)


class TodayPage(BaseModel):
    anchor: Optional[datetime] = None                     # newest collected development: the window ends here
    range_key: str = "24h"
    developments: list[DevelopmentCard] = Field(default_factory=list)
    awaiting_corroboration: int = 0                       # clusters in the window below the corroboration bar
    domains: list[str] = Field(default_factory=list)      # filter options present in the window
    situations: list[tuple[str, str]] = Field(default_factory=list)   # (slug, title)
    filters: dict[str, str] = Field(default_factory=dict)


class DevelopmentPage(BaseModel):
    card: DevelopmentCard
    situation_status: Optional[str] = None
    situation_actors: list[str] = Field(default_factory=list)


def _card(session: Session, event: Event, rank: int, canon, situations: dict[int, Situation],
          with_evidence: bool = False) -> DevelopmentCard:
    view = development_view(session, event, canon, with_evidence=with_evidence)
    s = situations.get(event.situation_id) if event.situation_id else None
    independent = event.source_count or 0
    return DevelopmentCard(development=view, rank=rank, situation_slug=s.slug if s else None,
                           situation_title=s.title if s else None, independent_sources=independent,
                           corroborated=independent >= MIN_INDEPENDENT_SOURCES,
                           reasons=split_reasons(view.rank_reasons))


def today(session: Session, range_key: str = "24h", domain: str = "", situation: str = "",
          confidence: str = "", limit: int = 60) -> TodayPage:
    """Corroborated developments updated in the window, in ranking order."""
    range_key = range_key if range_key in TIME_RANGES else "24h"
    anchor = session.query(func.max(Event.last_updated_at)).scalar()
    page = TodayPage(anchor=anchor, range_key=range_key,
                     filters={"range": range_key, "domain": domain, "situation": situation, "confidence": confidence})
    if anchor is None:
        return page
    since = anchor - timedelta(hours=TIME_RANGES[range_key])
    events = session.query(Event).filter(Event.last_updated_at >= since).all()
    situations = {s.id: s for s in session.query(Situation)}
    page.domains = sorted({e.event_domain for e in events if e.event_domain and e.event_domain != "unknown"})
    used = {e.situation_id for e in events if e.situation_id}
    page.situations = sorted(((situations[i].slug, situations[i].title) for i in used if i in situations),
                             key=lambda x: x[1])
    corroborated = [e for e in events if (e.source_count or 0) >= MIN_INDEPENDENT_SOURCES]
    page.awaiting_corroboration = len(events) - len(corroborated)
    chosen = [e for e in corroborated
              if (not domain or (e.event_domain or "unknown") == domain)
              and (not situation or (situation == "none" and e.situation_id is None)
                   or (e.situation_id in situations and situations[e.situation_id].slug == situation))
              and (not confidence or (e.confidence_class or "") == confidence)]
    chosen.sort(key=lambda e: (e.rank_score is None, -(e.rank_score or 0.0),
                               -(e.last_updated_at.timestamp() if e.last_updated_at else 0), e.id))
    canon = _canonicalizer()
    page.developments = [_card(session, e, n, canon, situations) for n, e in enumerate(chosen[:limit], start=1)]
    return page


def development_page(session: Session, event_id: int) -> DevelopmentPage | None:
    event = session.get(Event, event_id)
    if event is None:
        return None
    situations = {s.id: s for s in session.query(Situation)}
    card = _card(session, event, 0, _canonicalizer(), situations, with_evidence=True)
    s = situations.get(event.situation_id) if event.situation_id else None
    return DevelopmentPage(card=card, situation_status=s.status if s else None,
                           situation_actors=list(s.primary_actors or []) if s else [])
