"""Candidate generation for typed Development relations (Phase 3, Session 1).

Proposes pairs of Developments that *may* hold a runtime relation (``development_relations.RUNTIME_TYPES``). A
candidate is not a relation: it carries no claim and is never shown as one. Acceptance (explicit evidence) is a
later, separate stage. The rules are pre-registered in ``evaluations/relations/candidate-generation-plan.md`` and
come from the taxonomy's evidence requirements:

- ``same_calamity_lifecycle``: both name a hazard of the same class and compatible places, within 7 days;
- ``same_convened_event``: both name a gathering, plus 2 shared principals, the same named gathering or a shared
  specific place, within 7 days;
- ``reaction_to``: the later one has a reaction cue and they share a principal, within 72 hours (later = reaction).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from itertools import combinations

METHOD = "relation-candidates-v1"
EPISODE_GAP = timedelta(days=7)
REACTION_GAP = timedelta(hours=72)
BODY_CHARS = 300


def _terms(*words: str) -> re.Pattern:
    return re.compile(r"\b(?:" + "|".join(words) + r")", re.I)


HAZARDS: dict[str, re.Pattern] = {
    "earthquake": _terms("earthquake", "quake", "tremor", "aftershock", "seismic", "terremoto", "sismo"),
    "flood": _terms("flood", "flash flood", "inundat", "inundaci", "alluvion", "esondazion", "riada"),
    "storm": _terms("storm", "typhoon", "hurricane", "cyclone", "tornado", "tormenta", "temporal", "huracán",
                    "huracan", "tifón", "tifon", "ciclón", "ciclon", "tempesta", "uragano", "tifone", "ciclone"),
    "wildfire": _terms("wildfire", "bushfire", "forest fire", "blaze", "incendio forestal", "incendi boschiv",
                       "incendio boschivo"),
    "landslide": _terms("landslide", "mudslide", "deslizamiento", "alud", "frana", "smottamento"),
    "eruption": _terms("eruption", "volcan", "erupción", "erupcion", "eruzione", "vulcan"),
    "drought_heat": _terms("drought", "heatwave", "heat wave", "sequía", "sequia", "ola de calor", "siccità",
                           "siccita", "ondata di calore"),
    "outbreak": _terms("outbreak", "epidemic", "pandemic", "ebola", "cholera", "plague", "mpox", "measles",
                       "dengue", "brote", "epidemia", "ébola", "cólera", "colera", "peste", "focolaio"),
    "haze": _terms("haze", "smog", "calima", "foschia"),
    "tsunami": _terms("tsunami"),
}
GATHERING = _terms("summit", "state visit", "visit", "talks", "conference", "meeting", "assembly", "session",
                   "forum", "cumbre", "visita", "reunión", "reunion", "conferencia", "asamblea", "vertice",
                   "incontro", "conferenza", "assemblea")
NAMED_GATHERING = re.compile(r"\b(G7|G20|SCO|BRICS|ASEAN|APEC|NATO|UNGA|COP\s?\d{2}|OPEC)\b")
REACTION = re.compile(
    r"\b(?:condemn|denounc|reject|welcom|respond|response|react(?:s|ed|ing|ion|ions)?\b|slam(?:s|med)?\b|critici[sz]"
    r"|hail(?:s|ed|ing)?\b|retaliat|protest|in response"
    r"|conden[aó]|rechaz|respond|critic(?:a|an|ó|ano)\b|celebr[aó]\b"
    r"|condann|respin|rispond|protesta)", re.I)


@dataclass
class DevelopmentView:
    """What candidate generation sees of one Development."""
    id: int
    first: datetime | None
    texts: list[str]                                 # per member item: title + first BODY_CHARS of the body
    principals: set[str] = field(default_factory=set)
    places: set[str] = field(default_factory=set)    # canonical place names (gazetteer)

    @property
    def text(self) -> str:
        return "\n".join(self.texts)


@dataclass
class Candidate:
    relation_type: str
    source_event_id: int          # reaction_to: the reaction; symmetric: lower ID
    target_event_id: int
    rule: str
    signals: dict


def hazard_classes(text: str) -> set[str]:
    return {name for name, rx in HAZARDS.items() if rx.search(text)}


def _gap(a: DevelopmentView, b: DevelopmentView) -> timedelta | None:
    return abs(a.first - b.first) if a.first and b.first else None


def _compatible_places(a: set[str], b: set[str], geo) -> list[str]:
    return [f"{x}~{y}" for x in sorted(a) for y in sorted(b) if geo.same_or_contains(x, y)]


def _specific(places: set[str], geo) -> set[str]:
    return {p for p in places if not geo.is_country(p) and p in geo.known}


def generate(views: list[DevelopmentView], geo) -> list[Candidate]:
    """All candidates among the given Developments (each unordered pair once, at most one candidate per type)."""
    info = {v.id: (hazard_classes(v.text), bool(GATHERING.search(v.text)),
                   set(NAMED_GATHERING.findall(v.text)), bool(REACTION.search(v.text))) for v in views}
    out: list[Candidate] = []
    for a, b in combinations(sorted(views, key=lambda v: v.id), 2):
        gap = _gap(a, b)
        ha, ga, na, _ = info[a.id]
        hb, gb, nb, _ = info[b.id]
        if gap is not None and gap <= EPISODE_GAP:
            shared_hazard = ha & hb
            places = _compatible_places(a.places, b.places, geo)
            if shared_hazard and places:
                out.append(Candidate("same_calamity_lifecycle", a.id, b.id, "hazard+place",
                                     {"hazard": sorted(shared_hazard), "places": places[:4]}))
            if ga and gb:
                shared_principals = sorted(a.principals & b.principals)
                named = sorted({n.upper().replace(" ", "") for n in na} & {n.upper().replace(" ", "") for n in nb})
                specific = sorted(_specific(a.places, geo) & _specific(b.places, geo))
                if len(shared_principals) >= 2 or named or specific:
                    out.append(Candidate("same_convened_event", a.id, b.id, "gathering+participants",
                                         {"principals": shared_principals[:4], "named": named,
                                          "places": specific[:4]}))
        if a.first and b.first and a.first != b.first and gap <= REACTION_GAP:
            later, earlier = (a, b) if a.first > b.first else (b, a)
            shared = sorted(later.principals & earlier.principals)
            if info[later.id][3] and shared:
                out.append(Candidate("reaction_to", later.id, earlier.id, "cue+shared-principal",
                                     {"principals": shared[:4], "cue": REACTION.search(later.text).group(0)}))
    return out


def views_from_db(session, event_ids: list[int]) -> list[DevelopmentView]:
    """Development views for the given Developments, from the database (principals, member texts, places)."""
    from osint_monitor.core.database import Entity, EventEntity, EventItem, ItemEntity, RawItem
    from osint_monitor.processors.development_segmentation import LOCATION_TYPES, gazetteer
    from osint_monitor.processors.entity_resolver import normalise

    geo = gazetteer(False)
    views: dict[int, DevelopmentView] = {}
    members: dict[int, list[int]] = {}
    for event_id, item_id in session.query(EventItem.event_id, EventItem.item_id).filter(
            EventItem.event_id.in_(event_ids)):
        members.setdefault(event_id, []).append(item_id)
    items = {r.id: r for r in session.query(RawItem).filter(
        RawItem.id.in_([i for ids in members.values() for i in ids]))}
    places: dict[int, set[str]] = {}
    for item_id, name, etype in (session.query(ItemEntity.item_id, Entity.canonical_name, Entity.entity_type)
                                 .join(Entity, Entity.id == ItemEntity.entity_id)
                                 .filter(ItemEntity.item_id.in_(list(items)))):
        if etype in LOCATION_TYPES and name:
            places.setdefault(item_id, set()).add(geo.canonical(normalise(name)))
    principals: dict[int, set[str]] = {}
    for event_id, name in (session.query(EventEntity.event_id, Entity.canonical_name)
                           .join(Entity, Entity.id == EventEntity.entity_id)
                           .filter(EventEntity.event_id.in_(event_ids), EventEntity.is_principal.is_(True))):
        principals.setdefault(event_id, set()).add(name)
    for event_id, ids in members.items():
        rows = [items[i] for i in ids if i in items]
        times = [r.published_at or r.fetched_at for r in rows if r.published_at or r.fetched_at]
        views[event_id] = DevelopmentView(
            id=event_id, first=min(times) if times else None,
            texts=[f"{r.title or ''} {(r.content or '')[:BODY_CHARS]}" for r in rows],
            principals=principals.get(event_id, set()),
            places=set().union(*(places.get(r.id, set()) for r in rows)) if rows else set())
    return [views[e] for e in event_ids if e in views]
