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

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Protocol

from osint_monitor.processors.geography import Gazetteer

# Iteration 2: the location layer's frozen gazetteer extension (GeoNames cities15000, built by
# evaluations/geolocation/gazetteer-extension/build_extension.py). Read by this module only; the shared gazetteer is
# unchanged and always takes precedence. name -> {gazetteer country: [population, lat, lon]}
EXTENSION = Path(__file__).parent / "data" / "place_extension.json"


@lru_cache(maxsize=1)
def load_extension() -> dict[str, dict[str, list]]:
    return json.loads(EXTENSION.read_text(encoding="utf-8")).get("places", {}) if EXTENSION.exists() else {}


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
OUTSIDE_NAMED = "OUTSIDE_NAMED_COUNTRIES"      # L2: an extension place none of whose countries the reports name

# Iteration 2, L1 non-place filter: a span the gazetteer does not know is not a place when it names an organisation,
# competition or body (frozen lexicon, any position, locative included: "in La Liga"), is an institution or media
# outlet, or ends like a sports club ("Man City") and the extension does not know it either. PROPOSED.
_NON_PLACE_WORDS = re.compile(
    r"\b(liga|league|serie a|premiership|bundesliga|ligue|eredivisie|cup|copa|coppa|championships?|tournament|"
    r"olympics?|grand prix|club|fc|cf|afc|ministry|ministerio|ministero|government|gobierno|governo|parliament|"
    r"parlamento|congress|senate|council|commission|committee|party|partido|partito|union|agency|bank|banco|"
    r"corporation|corp|inc|ltd|group|university|universidad|police|policía|polizia|army|forces|navy|airlines?|"
    r"airways)\b", re.I)
_CLUB_SUFFIX = re.compile(r"\b(city|united|utd|rovers|wanderers|hotspur|albion|athletic)$", re.I)

# Iteration 2, L1 revision (L4 first bullet): a principal-actor country mention is the event country when the report
# states a country-wide occurrence (frozen lexicon below, in its headline or lead) and its headline is not a statement
# (U1). Used only when no supported point location exists. PROPOSED.
_COUNTRY_WIDE = re.compile(
    r"\b(elections?|electoral|votes?|voters?|voting|polls?|ballots?|referendum|run-?off|primar(?:y|ies)|protests?|"
    r"protesters?|demonstrations?|unrest|riots?|nationwide|national|parliament(?:ary)?|legislation|laws?|"
    r"constitution(?:al)?|cabinet|coalition|government|budget|census|curfew|lockdown|state of emergency|martial law|"
    r"coup|impeach\w*|general strike|earthquake|quake|floods?|flooding|wildfires?|drought|heatwave|cyclone|typhoon|"
    r"hurricane|blackouts?|outbreak|epidemic|inflation|recession|economy|elecciones|elezioni|protestas|proteste)\b",
    re.I)
_STATEMENT = re.compile(
    r"\b(says?|said|warns?|urges?|calls (?:on|for)|vows?|threatens?|denies|rejects?|condemns?|accuses?|claims?|"
    r"insists?|blames?|slams?|demands?|tells?|pledges?|promises?|dice|afferma|afirma)\b", re.I)

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


@lru_cache(maxsize=1)
def _bodies():
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.institutions import registry
    return registry(), ActorNormalizer.load()


def _organisation(span: str) -> bool:
    """Lexicon word, institution or media outlet (the non-place filter's first part)."""
    if _NON_PLACE_WORDS.search(span):
        return True
    reg, normalizer = _bodies()
    return reg.lookup(span) is not None or normalizer.is_media(span)


def _country_wide(m: OccurrenceMention) -> bool:
    return bool(_COUNTRY_WIDE.search(m.title) or _COUNTRY_WIDE.search(m.lead)) and not _STATEMENT.search(m.title)


def _known_to_gazetteer(name: str, geo: Gazetteer) -> bool:
    key = name.lower().strip()
    return key in DISPUTED or key in geo.known or geo.canonical(name) in geo.known


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
           actor_key=lambda name: name.lower(), extension: dict[str, dict[str, list]] | None = None) -> EventLocation:
    """The contract's L1-L6 over the occurrence reports' place mentions.

    principal_keys: canonical actor keys of the Development's principal actors (a place mention whose actor key is
    one of them is the actor, not the location, unless it is written in locative position).
    extension: the frozen gazetteer extension (default: place_extension.json); pass {} for the gazetteer alone.
    """
    ext = load_extension() if extension is None else extension
    mentions = list(mentions)
    rejected: list[tuple[str, str]] = []
    specific: dict[str, set[str]] = {}         # place -> origins
    country_of: dict[str, str | None] = {}
    countries: dict[str, set[str]] = {}         # country named as a place -> origins
    regions: dict[str, set[str]] = {}
    actor_countries: dict[str, set[str]] = {}   # actor country stated as country-wide occurrence -> origins (L1 rev.)
    ext_candidates: dict[str, dict[str, list]] = {}
    for m in mentions:
        if not _in_headline_or_lead(m):
            rejected.append((m.span, NOT_IN_LEAD))
            continue
        locative = _locative(m)
        if not locative and actor_key(m.span) in principal_keys:
            country, is_country = _country_of(m.span, geo)
            if (is_country or m.span.lower().strip() in DISPUTED) and _country_wide(m):
                actor_countries.setdefault(country, set()).add(m.origin)
            rejected.append((m.span, ACTOR_POSITION))       # "Russia strikes ..." (L1)
            continue
        if _is_region(m.span, geo):
            regions.setdefault(m.span.lower().strip(), set()).add(m.origin)
            continue
        known = _known_to_gazetteer(m.span, geo)
        if not known and _organisation(m.span):
            rejected.append((m.span, NON_PLACE))             # "in La Liga", "Gobierno" (L1 non-place filter)
            continue
        country, is_country = _country_of(m.span, geo)
        key = m.span.lower().strip()
        if is_country:
            countries.setdefault(country, set()).add(m.origin)
        elif country is not None:
            place = DISPUTED.get(key) or geo.canonical(m.span)
            specific.setdefault(place, set()).add(m.origin)
            country_of[place] = country
        elif not known and key in ext:
            # a real place the gazetteer lacks: its countries come from the extension, resolved under L2 below
            place = m.span.strip()
            specific.setdefault(place, set()).add(m.origin)
            country_of[place] = None
            ext_candidates[place] = ext[key]
        elif not known and _CLUB_SUFFIX.search(m.span.strip()):
            rejected.append((m.span, NON_PLACE))             # "at Man City"
        elif locative:
            # unknown to the gazetteer but written as a location: a specific place whose country the geocoder
            # must establish within the reports' countries (L2); kept with no country here
            place = m.span.strip()
            specific.setdefault(place, set()).add(m.origin)
            country_of[place] = None
        else:
            rejected.append((m.span, NON_PLACE))             # "La Liga", "Man City", "Gobierno" (L1)

    # L2 for extension places: only inside the countries the reports name through the gazetteer; with none named, the
    # most populous candidate when it is dominant (>= 4x the next country's), otherwise unresolved (PROPOSED: 4x)
    named = set(countries) | {c for c in country_of.values() if c is not None}
    for place, cands in ext_candidates.items():
        inside = {c: v for c, v in cands.items() if c in named} if named else cands
        if not inside:
            specific.pop(place)
            country_of.pop(place)
            rejected.append((place, OUTSIDE_NAMED))
            continue
        ranked = sorted(inside.items(), key=lambda kv: -kv[1][0])
        if len(ranked) == 1 or ranked[0][1][0] >= 4 * ranked[1][1][0]:
            country_of[place] = ranked[0][0]

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
    if actor_countries:
        # L1 revision (iteration 2): no supported point location, and the reports state a country-wide occurrence
        # in a principal actor's own country ("Brazil holds runoff", "Hong Kong police arrest ... under national
        # security law"): that country is the event country
        top = max(len(o) for o in actor_countries.values())
        leaders = [c for c, o in actor_countries.items() if len(o) == top]
        if len(leaders) == 1:
            return EventLocation(Role.EVENT_COUNTRY, Confidence.COUNTRY_ONLY, country=leaders[0],
                                 support={**support, leaders[0]: sorted(actor_countries[leaders[0]])},
                                 rejected=rejected, reason="country-wide occurrence in the actor's country (L1 rev.)")
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
