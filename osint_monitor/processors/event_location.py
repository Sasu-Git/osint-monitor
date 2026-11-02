"""Development location under the approved location contract (evaluations/geolocation/LOCATION-CONTRACT.md).

The location of a Development is where its occurrence happened, as its own reports state it: not the acting country,
not the reporting location (owner rulings U1-U4, 2026-11-02). Deterministic, offline; geocoding coordinates is a
separate step behind ``PlaceResolver`` and only inside the countries the reports name (L2).

Not wired into the pipeline: this module decides role, place, country and confidence; how they are stored is an
open schema decision (see the contract). Pure functions over ``OccurrenceMention`` records, so the decision is
testable without a database; ``mentions_for_event`` builds them from the database read-only.

Mentions are the **surface spans** of LOC/GPE/FAC entities (``item_entities.span_text``), not their canonical
entity: entity resolution files "Kyiv" under "Ukraine" and "Moscow" under "Russian", which would turn every city
into its country.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Protocol

from osint_monitor.processors.geography import Gazetteer


class Role(str, Enum):
    EVENT_PLACE = "EVENT_PLACE"
    EVENT_COUNTRY = "EVENT_COUNTRY"
    NONE = "NONE"


class Confidence(str, Enum):
    CONFIRMED_PLACE = "CONFIRMED_PLACE"      # a specific place named by >= 2 independent origins (PROPOSED: 2)
    PLACE = "PLACE"                          # a specific place named by 1 origin
    COUNTRY_ONLY = "COUNTRY_ONLY"
    REGION = "REGION"                        # only a sea, strait, continent or region: label, no marker (U3)
    NONE = "NONE"


# Rejection reasons recorded per mention (L7)
ACTOR_POSITION, NON_PLACE, REGION_ONLY, NOT_IN_LEAD = "ACTOR_POSITION", "NON_PLACE", "REGION", "NOT_IN_HEADLINE_OR_LEAD"

# U4 (owner ruling a): disputed or occupied territory is its own entity, contained in nothing. Location layer only;
# the shared gazetteer is not changed. The list itself is PROPOSED.
DISPUTED = {"west bank": "west bank", "gaza": "gaza", "gaza strip": "gaza", "east jerusalem": "east jerusalem",
            "crimea": "crimea", "western sahara": "western sahara"}

# U3: water bodies and supra-national areas are labels, never a map point. Gazetteer regions plus these (PROPOSED).
_REGION_WORDS = re.compile(r"\b(sea|strait|straits|gulf|ocean|channel|bay|peninsula)\b", re.I)
_REGIONS = {"europe", "africa", "asia", "americas", "latin america", "south america", "north america", "caribbean",
            "balkans", "arctic", "antarctica", "pacific", "atlantic", "mediterranean", "middle east", "sahel",
            "central africa", "west africa", "east africa", "horn of africa", "scandinavia", "eurasia"}
# A place named right after one of these in a headline is where something happened ("strike in Kyiv").
_LOCATIVE = re.compile(r"\b(in|at|near|outside|across|over|into|off|on|from|inside|around|towards?)\s+(the\s+)?"
                       r"((?:[A-Z][\w'’.-]*\s+){0,3})$")
LEAD_CHARS = 300


@dataclass(frozen=True)
class OccurrenceMention:
    """One place mention in one occurrence report."""
    item_id: int
    origin: str                  # provenance origin of the report (independent-origin counting)
    span: str                    # surface text, as written
    title: str
    lead: str                    # the report's first LEAD_CHARS characters of body text


@dataclass
class EventLocation:
    role: Role
    confidence: Confidence
    place: str | None = None                     # canonical place name (gazetteer form or the span)
    country: str | None = None                   # gazetteer country name, or a disputed entity (U4)
    places: list[str] = field(default_factory=list)       # the supported places when several (U2)
    region: str | None = None                    # the region label when only a region is supported (U3)
    support: dict[str, list[str]] = field(default_factory=dict)   # place -> origins naming it
    rejected: list[tuple[str, str]] = field(default_factory=list)  # (span, reason)
    reason: str = ""


class PlaceResolver(Protocol):
    """Coordinates for a place restricted to the given countries (L2: a hit outside them is no hit)."""
    def resolve(self, place: str, countries: set[str]) -> tuple[float, float] | None: ...


def _in_headline_or_lead(m: OccurrenceMention) -> bool:
    s = m.span.lower()
    return s in m.title.lower() or s in m.lead.lower()


def _locative(m: OccurrenceMention) -> bool:
    """The span appears in the headline right after a locative preposition (possessives allowed in between)."""
    for hit in re.finditer(re.escape(m.span), m.title, re.I):
        if _LOCATIVE.search(m.title[:hit.start()]):
            return True
    return False


def _is_region(name: str, geo: Gazetteer) -> bool:
    key = name.lower().strip()
    return key in _REGIONS or bool(_REGION_WORDS.search(key)) or key in getattr(geo, "regions", {})


def _country_of(name: str, geo: Gazetteer) -> tuple[str | None, bool]:
    """(country, is_country) for a place name: disputed entities are their own country (U4)."""
    key = geo.canonical(name)
    if key in DISPUTED or name.lower().strip() in DISPUTED:
        return DISPUTED.get(key) or DISPUTED[name.lower().strip()], False
    if key in geo.countries:
        return key, True
    inside = [a for a in geo.ancestors(key) if a in geo.countries]
    return (inside[0], False) if len(inside) == 1 else (None, False)


def decide(mentions: Iterable[OccurrenceMention], principal_keys: set[str], geo: Gazetteer,
           actor_key=lambda name: name.lower()) -> EventLocation:
    """The contract's L1-L6 over the occurrence reports' place mentions.

    principal_keys: canonical actor keys of the Development's principal actors (a place mention whose actor key is
    one of them is the actor, not the location, unless it is written in locative position).
    """
    mentions = list(mentions)
    rejected: list[tuple[str, str]] = []
    specific: dict[str, set[str]] = {}         # place -> origins
    country_of: dict[str, str | None] = {}
    countries: dict[str, set[str]] = {}         # country named as a place -> origins
    regions: dict[str, set[str]] = {}
    for m in mentions:
        if not _in_headline_or_lead(m):
            rejected.append((m.span, NOT_IN_LEAD))
            continue
        locative = _locative(m)
        if not locative and actor_key(m.span) in principal_keys:
            rejected.append((m.span, ACTOR_POSITION))       # "Russia strikes ..." (L1)
            continue
        if _is_region(m.span, geo):
            regions.setdefault(m.span.lower().strip(), set()).add(m.origin)
            continue
        country, is_country = _country_of(m.span, geo)
        if is_country:
            countries.setdefault(country, set()).add(m.origin)
        elif country is not None:
            place = DISPUTED.get(m.span.lower().strip()) or geo.canonical(m.span)
            specific.setdefault(place, set()).add(m.origin)
            country_of[place] = country
        elif locative:
            # unknown to the gazetteer but written as a location: a specific place whose country the geocoder
            # must establish within the reports' countries (L2); kept with no country here
            place = m.span.strip()
            specific.setdefault(place, set()).add(m.origin)
            country_of[place] = None
        else:
            rejected.append((m.span, NON_PLACE))             # "La Liga", "Man City", "Gobierno" (L1)

    # L2: a place the gazetteer does not know can only lie inside the countries the reports name; when exactly one
    # country is in play it is that one (the geocoder is then restricted to it), otherwise it stays unresolved
    named = set(countries) | {c for c in country_of.values() if c is not None}
    if len(named) == 1:
        for place, country in country_of.items():
            if country is None:
                country_of[place] = next(iter(named))
    support = {p: sorted(o) for p, o in {**countries, **specific}.items()}
    # a disputed entity named on its own is its own "country"-level place (U4)
    for place, country in list(country_of.items()):
        if place == country:
            countries.setdefault(country, set()).update(specific.pop(place))
            country_of.pop(place)

    if specific:
        by_country: dict[str | None, list[str]] = {}
        for place in specific:
            by_country.setdefault(country_of[place], []).append(place)
        top = max(len(o) for o in specific.values())
        leaders = [p for p, o in specific.items() if len(o) == top]
        leader_countries = {country_of[p] for p in leaders}
        if len(specific) == 1:
            place = leaders[0]
            return EventLocation(Role.EVENT_PLACE, Confidence.CONFIRMED_PLACE if top >= 2 else Confidence.PLACE,
                                 place=place, country=country_of[place], support=support, rejected=rejected,
                                 reason="one specific place")
        if len(by_country) == 1 and None not in by_country:
            country = next(iter(by_country))
            return EventLocation(Role.EVENT_COUNTRY, Confidence.COUNTRY_ONLY, country=country,
                                 places=sorted(by_country[country]), support=support, rejected=rejected,
                                 reason="several places in one country (U2: country ring, places listed)")
        if len(leaders) == 1 and len(leader_countries) == 1:
            place = leaders[0]                               # one place clearly dominant (more origins than any)
            return EventLocation(Role.EVENT_PLACE, Confidence.CONFIRMED_PLACE if top >= 2 else Confidence.PLACE,
                                 place=place, country=country_of[place], places=sorted(specific), support=support,
                                 rejected=rejected, reason="dominant specific place")
        return EventLocation(Role.NONE, Confidence.NONE, places=sorted(specific), support=support, rejected=rejected,
                             reason="several places in different countries, none dominant (L5)")
    if countries:
        top = max(len(o) for o in countries.values())
        leaders = [c for c, o in countries.items() if len(o) == top]
        if len(leaders) == 1:
            return EventLocation(Role.EVENT_COUNTRY, Confidence.COUNTRY_ONLY, country=leaders[0], support=support,
                                 rejected=rejected, reason="country named as the place (L4)")
        return EventLocation(Role.NONE, Confidence.NONE, places=sorted(countries), support=support, rejected=rejected,
                             reason="several countries, none dominant (L5)")
    if regions:
        top = max(len(o) for o in regions.values())
        leaders = sorted(r for r, o in regions.items() if len(o) == top)
        return EventLocation(Role.NONE, Confidence.REGION, region=leaders[0], support=support, rejected=rejected,
                             reason="only a sea, strait or region (U3: label, no marker)")
    return EventLocation(Role.NONE, Confidence.NONE, support=support, rejected=rejected,
                         reason="no place in the occurrence reports' headlines or leads" if mentions else
                         "no place mention")


def mentions_for_event(session, event_id: int, resolver=None) -> tuple[list[OccurrenceMention], set[str]]:
    """Occurrence mentions and principal actor keys of a Development (read-only).

    Occurrence reports are members whose headline is a REPORT (not analysis, live blog or roundup); origins come
    from the ProvenanceResolver, so wire copies count once.
    """
    from osint_monitor.core.database import Entity, EventEntity, ItemEntity, RawItem
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.development_segmentation import REPORT, headline_kind
    from osint_monitor.processors.provenance import ProvenanceResolver, build_evidence

    resolver = resolver or ProvenanceResolver()
    evidence = build_evidence(session, event_id)
    origins = {p.item_id: p.origin for p in resolver.resolve(evidence)}
    items = {r.id: r for r in session.query(RawItem).filter(RawItem.id.in_(list(origins)))}
    occurrence = {i for i, r in items.items() if headline_kind(r.title or "") == REPORT}
    out = []
    for item_id, span, etype in (session.query(ItemEntity.item_id, ItemEntity.span_text, Entity.entity_type)
                                 .join(Entity, Entity.id == ItemEntity.entity_id)
                                 .filter(ItemEntity.item_id.in_(sorted(occurrence)),
                                         Entity.entity_type.in_(("LOC", "GPE", "FAC")))
                                 .order_by(ItemEntity.item_id, ItemEntity.id)):
        if span:
            r = items[item_id]
            out.append(OccurrenceMention(item_id=item_id, origin=origins[item_id], span=span, title=r.title or "",
                                         lead=(r.content or "")[:LEAD_CHARS]))
    normalizer = ActorNormalizer.load()
    principals = {normalizer.key(n) for (n,) in session.query(Entity.canonical_name)
                  .join(EventEntity, EventEntity.entity_id == Entity.id)
                  .filter(EventEntity.event_id == event_id, EventEntity.is_principal.is_(True))} - {None, ""}
    return out, principals
