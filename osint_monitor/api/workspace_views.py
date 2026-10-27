"""Read-only view model for the situational-awareness workspace: one selection of Developments drives the
feed, the map and the "what changed" rail, so the three always agree.

The selection is Today's (development_views): corroborated Developments updated in the window, in the
pipeline's ranking order, filtered by domain / Situation / confidence. On top of it, and only for
presentation:

- geography: where the Development happened, from its stored coordinates when the placement check agrees
  (api/geo.py); otherwise no map marker, never an invented one;
- relevance: which countries it concerns, separately as its location and as the states its principal
  actors act for (a US-China meeting in Geneva is located in Switzerland and concerns the US and China);
- personal priority: the reader's HIGH / NORMAL / LOW / MUTED settings for countries and topics
  (core/user_state.py) reorder, emphasise or hide it. They never change what the Development is, which
  Situation it belongs to, its confidence or its evidence; nothing here writes to the intelligence database.

There is no relevance score. Each reordered or hidden Development carries the plain reason.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from osint_monitor.api.development_views import (MIN_INDEPENDENT_SOURCES, TIME_RANGES, DevelopmentCard, _card,
                                                 matches, rank_order, window)
from osint_monitor.api.geo import CountryIndex, Placement, placement
from osint_monitor.api.situation_views import _canonicalizer
from osint_monitor.core.database import Entity, Event, EventEntity, EventItem, ItemEntity, Situation
from osint_monitor.core.models import EventDomain
from osint_monitor.core.user_state import Level, PriorityStore, Scope

LOCATION_ENTITY_TYPES = ("LOC", "GPE", "FAC", "LOCATION", "FACILITY")     # as processors/geocoding.py
DOMAINS = [d.value for d in EventDomain if d is not EventDomain.UNKNOWN]
LIFECYCLES = {"new": "New in this period", "updated": "Updated in this period"}
TIER = {Level.HIGH: 0, Level.NORMAL: 1, Level.LOW: 2, Level.MUTED: 3}
FEED_LIMIT = 60


class Filters(BaseModel):
    range: str = "24h"
    domain: str = ""
    situation: str = ""
    confidence: str = ""
    lifecycle: str = ""
    type: str = ""
    country: str = ""
    show_muted: bool = False

    def normalised(self) -> "Filters":
        f = self.model_copy()
        if f.range not in TIME_RANGES:
            f.range = "24h"
        if f.lifecycle not in LIFECYCLES:
            f.lifecycle = ""
        return f


class Priority(BaseModel):
    level: Level = Level.NORMAL
    because: list[str] = Field(default_factory=list)    # plain reasons, e.g. "HIGH country: China (actor)"

    @property
    def note(self) -> str | None:
        if not self.because:
            return None
        lead = {Level.HIGH: "Surfaced first because", Level.LOW: "De-emphasised because",
                Level.MUTED: "Muted because"}.get(self.level)
        return f"{lead}: {' + '.join(self.because)}" if lead else None


class Geography(BaseModel):
    mapped: bool = False
    lat: Optional[float] = None
    lon: Optional[float] = None
    place: Optional[str] = None                          # stored place name, shortened
    country: Optional[str] = None                        # country id of the place
    country_name: Optional[str] = None
    country_level: bool = False                          # the point is a whole country, not a place in it
    not_mapped_because: Optional[str] = None


class Item(BaseModel):
    """One Development in the workspace selection."""
    id: int
    priority: Priority
    geography: Geography
    involves: list[tuple[str, str]] = Field(default_factory=list)   # (country id, name) of the principal actors
    lifecycle: str = "updated"                                       # new / updated, from stored timestamps


class WorkspaceCard(BaseModel):
    card: DevelopmentCard
    item: Item


class SituationChange(BaseModel):
    slug: str
    title: str
    status: str
    developments: int                                    # in the selection
    new: int                                             # first reported in the window
    latest: str


class Workspace(BaseModel):
    anchor: Optional[datetime] = None
    since: Optional[datetime] = None
    filters: Filters = Field(default_factory=Filters)
    cards: list[WorkspaceCard] = Field(default_factory=list)
    total: int = 0                                       # Developments in the selection (before the feed limit)
    muted: int = 0                                       # hidden by MUTED priorities
    awaiting_corroboration: int = 0
    mapped: int = 0
    unmapped: int = 0
    new: int = 0
    updated: int = 0
    situations_changed: list[SituationChange] = Field(default_factory=list)
    domains: list[str] = Field(default_factory=list)
    types: list[str] = Field(default_factory=list)
    situations: list[tuple[str, str]] = Field(default_factory=list)
    focus_situation: Optional[SituationChange] = None
    focus_situation_actors: list[str] = Field(default_factory=list)
    focus_country: Optional[tuple[str, str]] = None


def priority_for(domain: str | None, countries: dict[str, set[str]], country_levels: dict[str, Level],
                 domain_levels: dict[str, Level], index: CountryIndex) -> Priority:
    """The reader's priority for one Development, with its reasons. Deterministic:

    - MUTED when its topic is muted, or when it concerns countries and every one of them is muted;
    - otherwise HIGH when its topic or any (unmuted) country it concerns is HIGH;
    - otherwise LOW when its topic is LOW, or every (unmuted) country it concerns is LOW;
    - otherwise NORMAL. Countries count as its location and as the states its principal actors act for.
    """
    def name(c: str) -> str:
        return f"{index.name(c)} ({' and '.join(sorted(countries[c]))})"

    topic = (domain or "").replace("_", " ").capitalize()
    d = domain_levels.get(domain or "", Level.NORMAL)
    if d is Level.MUTED:
        return Priority(level=Level.MUTED, because=[f"MUTED topic: {topic}"])
    levels = {c: country_levels.get(c, Level.NORMAL) for c in countries}
    if levels and all(v is Level.MUTED for v in levels.values()):
        return Priority(level=Level.MUTED, because=[f"MUTED country: {name(c)}" for c in sorted(levels)])
    active = {c: v for c, v in levels.items() if v is not Level.MUTED}
    highs = sorted(c for c, v in active.items() if v is Level.HIGH)
    if highs or d is Level.HIGH:
        return Priority(level=Level.HIGH, because=[f"HIGH country: {name(c)}" for c in highs]
                        + ([f"HIGH topic: {topic}"] if d is Level.HIGH else []))
    lows = sorted(c for c, v in active.items() if v is Level.LOW)
    if d is Level.LOW or (active and len(lows) == len(active)):
        return Priority(level=Level.LOW, because=([f"LOW country: {name(c)}" for c in lows] if len(lows) == len(active) else [])
                        + ([f"LOW topic: {topic}"] if d is Level.LOW else []))
    return Priority()


def _principal_keys(session: Session, ids: list[int], canon) -> dict[int, frozenset[str]]:
    names: dict[int, list[str]] = defaultdict(list)
    for chunk in (ids[i:i + 500] for i in range(0, len(ids), 500)):
        for eid, name in (session.query(EventEntity.event_id, Entity.canonical_name)
                          .join(Entity, Entity.id == EventEntity.entity_id)
                          .filter(EventEntity.event_id.in_(chunk), EventEntity.is_principal.is_(True))):
            names[eid].append(name)
    return {eid: canon.keys(n) for eid, n in names.items()}


def _place_mentions(session: Session, ids: list[int]) -> dict[int, Counter]:
    """Location mentions of each Development's items, counted as the geocoder counts them."""
    out: dict[int, Counter] = defaultdict(Counter)
    for chunk in (ids[i:i + 500] for i in range(0, len(ids), 500)):
        for eid, name in (session.query(EventItem.event_id, Entity.canonical_name)
                          .join(ItemEntity, ItemEntity.item_id == EventItem.item_id)
                          .join(Entity, Entity.id == ItemEntity.entity_id)
                          .filter(EventItem.event_id.in_(chunk), Entity.entity_type.in_(LOCATION_ENTITY_TYPES))):
            out[eid][name] += 1
    return out


def describe(session: Session, events: list[Event], store: PriorityStore, since: datetime | None,
             index: CountryIndex | None = None) -> dict[int, Item]:
    """Geography, relevance, lifecycle and the reader's priority for each Development."""
    index = index or CountryIndex.load()
    ids = [e.id for e in events]
    canon = _canonicalizer()
    keys = _principal_keys(session, ids, canon)
    mentions = _place_mentions(session, ids)
    country_levels, domain_levels = store.levels(Scope.COUNTRY), store.levels(Scope.DOMAIN)
    out = {}
    for e in events:
        p: Placement = placement(index, e.lat, e.lon, e.location_name, mentions.get(e.id, Counter()))
        # the states the principal actors act for, named as the actors are displayed ("United States")
        acting = {}
        for k in keys.get(e.id, ()):
            c = index.of_actor(k)
            if c:
                acting.setdefault(c, canon.display(k))
        involves = sorted(acting)
        roles: dict[str, set[str]] = defaultdict(set)
        if p.country:
            roles[p.country].add("location")
        for c in involves:
            roles[c].add("actor")
        geo = Geography(mapped=p.mapped, lat=e.lat if p.mapped else None, lon=e.lon if p.mapped else None,
                        place=p.label, country=p.country, country_name=index.name(p.country) if p.country else None,
                        country_level=p.country_level, not_mapped_because=None if p.mapped else p.reason)
        new = bool(since and e.first_reported_at and e.first_reported_at >= since)
        out[e.id] = Item(id=e.id, geography=geo, involves=sorted(acting.items(), key=lambda x: x[1]),
                         lifecycle="new" if new else "updated",
                         priority=priority_for(e.event_domain, roles, country_levels, domain_levels, index))
    return out


def concerns(item: Item, country: str) -> bool:
    return item.geography.country == country or any(c == country for c, _ in item.involves)


def select(session: Session, filters: Filters, store: PriorityStore, situation_window: bool = False):
    """The workspace selection: (anchor, since, situations, events in display order, items, counters).

    With ``situation_window`` and a Situation filter, every Development of that Situation is selected
    whatever its age (the Situation page's map)."""
    f = filters.normalised()
    situations = {s.id: s for s in session.query(Situation)}
    if situation_window and f.situation and f.situation != "none":
        anchor = since = None
        events = (session.query(Event).join(Situation, Situation.id == Event.situation_id)
                  .filter(Situation.slug == f.situation).all())
    else:
        anchor, since, events = window(session, f.range)
    corroborated = [e for e in events if (e.source_count or 0) >= MIN_INDEPENDENT_SOURCES]
    chosen = [e for e in corroborated if matches(e, situations, f.domain, f.situation, f.confidence)
              and (not f.type or (e.event_type or "unknown") == f.type)]
    items = describe(session, chosen, store, since)
    if f.lifecycle:
        chosen = [e for e in chosen if items[e.id].lifecycle == f.lifecycle]
    if f.country:
        chosen = [e for e in chosen if concerns(items[e.id], f.country)]
    muted = [e for e in chosen if items[e.id].priority.level is Level.MUTED]
    shown = chosen if f.show_muted else [e for e in chosen if items[e.id].priority.level is not Level.MUTED]
    shown.sort(key=lambda e: (TIER[items[e.id].priority.level], *rank_order(e)))
    counters = {"events": events, "corroborated": corroborated, "muted": len(muted)}
    return anchor, since, situations, shown, items, counters


def workspace(session: Session, filters: Filters, store: PriorityStore, limit: int = FEED_LIMIT) -> Workspace:
    f = filters.normalised()
    anchor, since, situations, shown, items, counters = select(session, f, store)
    page = Workspace(anchor=anchor, since=since, filters=f)
    if anchor is None:
        return page
    events, corroborated = counters["events"], counters["corroborated"]
    page.awaiting_corroboration = len(events) - len(corroborated)
    page.domains = sorted({e.event_domain for e in events if e.event_domain and e.event_domain != "unknown"})
    page.types = sorted({e.event_type for e in corroborated if e.event_type and e.event_type != "unknown"})
    used = {e.situation_id for e in events if e.situation_id}
    page.situations = sorted(((situations[i].slug, situations[i].title) for i in used if i in situations),
                             key=lambda x: x[1])
    page.total, page.muted = len(shown), counters["muted"]
    page.mapped = sum(items[e.id].geography.mapped for e in shown)
    page.unmapped = page.total - page.mapped
    page.new = sum(items[e.id].lifecycle == "new" for e in shown)
    page.updated = page.total - page.new
    canon = _canonicalizer()
    page.cards = [WorkspaceCard(card=_card(session, e, n, canon, situations), item=items[e.id])
                  for n, e in enumerate(shown[:limit], start=1)]
    by_situation: dict[int, list[Event]] = defaultdict(list)
    for e in shown:
        if e.situation_id in situations:
            by_situation[e.situation_id].append(e)
    changes = []
    for sid, evs in by_situation.items():
        s = situations[sid]
        latest = max(evs, key=lambda e: (e.last_updated_at or datetime.min, e.id))
        changes.append(SituationChange(slug=s.slug, title=s.title, status=s.status, developments=len(evs),
                                       new=sum(items[e.id].lifecycle == "new" for e in evs), latest=latest.summary))
    changes.sort(key=lambda c: (-c.new, -c.developments, c.title))
    page.situations_changed = changes
    if f.situation and f.situation != "none":
        s = next((s for s in situations.values() if s.slug == f.situation), None)
        if s is not None:
            page.focus_situation = next((c for c in changes if c.slug == s.slug), None) or SituationChange(
                slug=s.slug, title=s.title, status=s.status, developments=0, new=0, latest="")
            page.focus_situation_actors = list(s.primary_actors or [])
    if f.country:
        page.focus_country = (f.country, CountryIndex.load().name(f.country))
    return page


def geojson(session: Session, filters: Filters, store: PriorityStore, situation_window: bool = False) -> dict:
    """Mapped Developments of the selection as GeoJSON points (only those whose placement is confirmed)."""
    _, _, situations, shown, items, _ = select(session, filters, store, situation_window=situation_window)
    canon = _canonicalizer()
    keys = _principal_keys(session, [e.id for e in shown], canon)
    features = []
    for e in shown:
        it = items[e.id]
        if not it.geography.mapped:
            continue
        s = situations.get(e.situation_id) if e.situation_id else None
        features.append({
            "type": "Feature", "id": e.id,
            "geometry": {"type": "Point", "coordinates": [round(it.geography.lon, 4), round(it.geography.lat, 4)]},
            "properties": {
                "id": e.id, "title": e.summary,
                "time": e.last_updated_at.isoformat() if e.last_updated_at else None,
                "actors": sorted(canon.display(k) for k in keys.get(e.id, ())),
                "situation": s.title if s else None, "situation_slug": s.slug if s else None,
                "sources": e.source_count or 0, "domain": e.event_domain, "confidence": e.confidence_class,
                "level": it.priority.level.value, "lifecycle": it.lifecycle,
                "place": it.geography.place, "country": it.geography.country,
                "country_level": it.geography.country_level,
            }})
    return {"type": "FeatureCollection", "features": features,
            "unmapped": sum(1 for e in shown if not items[e.id].geography.mapped)}
