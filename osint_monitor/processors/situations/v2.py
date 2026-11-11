"""Situation membership v2 (contract CONTRACT-V2-R2, frozen bf57ed7): deterministic rules, replay only.

Not wired into the pipeline. Pure functions over precomputed Development features and Situation profiles; no
database access here. ``evaluations/situation-membership/v2-replay/replay_v2.py`` builds the inputs from a snapshot
copy and writes decisions in the frozen scorer's candidate format.

Section numbers refer to the contract. Parameters are those frozen in §7.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timedelta

CONTRACT_VERSION = "CONTRACT-V2-R2 (bf57ed7)"

# §1.1 topic families (DEF)
FAMILY_OF = {
    **{t: "armed_conflict" for t in ("military_action", "deployment", "military_exercise", "ceasefire",
                                     "arms_transfer")},
    **{t: "security" for t in ("security_incident", "threat", "warning")},
    **{t: "diplomacy" for t in ("bilateral_meeting", "multilateral_meeting", "summit", "negotiation",
                                "diplomatic_visit", "agreement", "treaty", "significant_statement")},
    **{t: "economic" for t in ("sanctions", "economic_action")},
    **{t: "politics" for t in ("election", "appointment", "resignation", "policy_change")},
}

# §3.2 generic parties v1 (DEF), as canonical actor keys
GENERIC_PARTIES = frozenset({"united states", "russia", "china", "united kingdom", "france", "european union", "nato",
                             "united nations"})
SUPRANATIONAL = frozenset({"european union", "nato", "united nations"})

# §1.4 hazard lexicon v1 (DEF), matched accent-folded and case-insensitive on whole words
HAZARD_LEXICON = {
    "storm": ["hurricane", "typhoon", "cyclone", "tropical storm", "huracan", "tormenta tropical", "ciclon",
              "uragano", "tempesta tropicale", "ciclone"],
    "earthquake": ["earthquake", "quake", "tremor", "terremoto", "sismo", "scossa"],
    "flood": ["flood", "flooding", "inundacion", "riada", "alluvione", "inondazione"],
    "wildfire": ["wildfire", "forest fire", "incendio forestal", "incendio boschivo"],
    "volcanic": ["eruption", "volcano", "erupcion", "volcan", "eruzione", "vulcano"],
    "tsunami": ["tsunami"],
    "landslide": ["landslide", "mudslide", "deslizamiento", "alud", "frana"],
}
_STORM_NAME = re.compile(r"\b(?:hurricane|typhoon|cyclone|tropical storm|storm|huracan|tormenta tropical|tormenta|"
                         r"ciclon|uragano|tempesta tropicale|tempesta|ciclone)\s+['\"]?([A-Z][a-z]+)")
# §4 hedge lexicon v1 (DEF)
HEDGE = re.compile(r"\b(suspected|alleged|allegedly|accused of|reportedly|claims?|sospechoso|presunto|presunta|"
                   r"supuestamente|sospetto|presumibilmente)\b", re.I)

CREATE_WINDOW = timedelta(days=7)
SINGLE_PARTY_SEPARATION = timedelta(hours=24)
PENDING_DAYS = 7


def fold(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text or "") if not unicodedata.combining(c))


def family_of(event_type: str | None) -> str | None:
    return FAMILY_OF.get(event_type or "")


def hazard_of(texts: list[str]) -> tuple[str, str | None] | None:
    """(hazard family, storm name or None) from headlines and leads; the first family in lexicon order wins."""
    blob = fold(" ".join(texts))
    low = blob.lower()
    for fam, words in HAZARD_LEXICON.items():
        if any(re.search(r"\b" + re.escape(w) + r"\b", low) for w in words):
            name = None
            if fam == "storm":
                m = _STORM_NAME.search(re.sub(r"(?i)\b(hurricane|typhoon|cyclone|storm|huracan|tormenta|ciclon|uragano|"
                                              r"tempesta|ciclone)\b", lambda x: x.group(0).lower(), blob))
                name = m.group(1).lower() if m else None
            return fam, name
    return None


def hedge_terms(text: str) -> list[str]:
    return sorted({m.group(0).lower() for m in HEDGE.finditer(fold(text or ""))})


@dataclass
class DevFeatures:
    event_id: int
    headline: str
    lead: str
    first_reported_at: datetime | None
    parties: frozenset[str]                     # Situation keys of the principal actors (variants collapsed)
    has_principals: bool
    family: str | None
    places: dict[str, str | None]               # specific place -> its country (None if unknown)
    event_country: str | None                   # interim: the single country of the specific places, else None
    report_share: float                         # share of member items whose headline is a report
    hazard: tuple[str, str | None] | None
    hedges: list[str]
    mixed: bool | None = None                   # precondition: no stored flag on main -> None (never fires)

    @property
    def occurrence(self) -> bool:               # E3
        return self.report_share > 0.5


@dataclass
class Situation2:
    slug: str
    mode: str                                   # seeded | actor_process | single_party | hazard
    anchors: frozenset[str]
    families: frozenset[str]
    place_scope: frozenset[str]                 # countries
    keywords: tuple[str, ...] = ()
    hazard: tuple[str, str, str | None] | None = None   # (family, country, name)
    status: str = "active"
    scope_source: str = "derived"
    scope_version: int = 1
    founders: tuple[int, ...] = ()
    note: str = ""

    @property
    def actor_keyed(self) -> bool:
        return self.mode in ("seeded", "actor_process", "single_party")

    def snapshot(self) -> dict:
        return {"anchors": sorted(self.anchors), "families": sorted(self.families),
                "place_scope": sorted(self.place_scope), "keywords": list(self.keywords),
                "hazard": list(self.hazard) if self.hazard else None, "scope_version": self.scope_version}


@dataclass
class Decision:
    outcome: str
    reason: str
    evidence: dict = field(default_factory=dict)


# -- §3 eligibility --------------------------------------------------------------------------------

def scope_signals(d: DevFeatures, s: Situation2) -> list[tuple[str, str]]:
    sig = []
    if d.family and d.family in s.families:
        sig.append(("family", d.family))
    for p, c in sorted(d.places.items()):
        if c and c in s.place_scope:
            sig.append(("place", p))
    if s.keywords:
        text = fold(f"{d.headline} {d.lead}").lower()
        for k in s.keywords:
            if re.search(r"\b" + re.escape(fold(k).lower()) + r"\b", text):
                sig.append(("keyword", k))
    return sig


def identity_match(d: DevFeatures, s: Situation2, signals: list[tuple[str, str]]) -> tuple[bool, str, dict]:
    """E1 (with §3.2 half coverage). Returns (passes, reason if not, evidence)."""
    if s.mode == "hazard":
        h = d.hazard
        ok = bool(h and s.hazard and h[0] == s.hazard[0] and d.event_country == s.hazard[1]
                  and (h[1] is None or s.hazard[2] is None or h[1] == s.hazard[2]))
        return ok, "" if ok else "NO_SHARED_ACTORS", {"hazard": list(h) if h else None}
    shared = d.parties & s.anchors
    cov = len(shared) / len(s.anchors) if s.anchors else 0.0
    ev = {"shared_parties": sorted(shared), "coverage": round(cov, 3),
          "generic_parties_matched": sorted(shared & GENERIC_PARTIES)}
    if s.mode == "single_party":
        return (bool(shared), "" if shared else "NO_SHARED_ACTORS", ev)
    if not shared:
        return False, "NO_SHARED_ACTORS", ev
    if cov >= 1.0:
        return True, "", ev
    need = -(-len(s.anchors) // 2) / len(s.anchors)        # ceil(50%)
    if cov < need:
        return False, "LOW_COVERAGE", ev
    in_scope_places = [(p, c) for p, c in d.places.items() if c and c in s.place_scope]
    if shared - GENERIC_PARTIES:
        ok = bool(signals) and bool(in_scope_places)
        ev["half_rule"] = "non_generic"
        return ok, "" if ok else "LOW_COVERAGE", ev
    own = {g for g in shared}
    strong = bool(d.family and d.family in s.families) and any(
        c and (own <= SUPRANATIONAL or c not in own) for _, c in in_scope_places)
    ev["half_rule"] = "generic_only"
    return strong, "" if strong else "GENERIC_ANCHOR_ONLY", ev


def _base(d: DevFeatures, s: Situation2) -> Decision:
    """§4 steps 1-6 for one Situation (no comparison with others yet)."""
    signals = scope_signals(d, s)
    ev = {"scope_signals": [list(x) for x in signals], "family": d.family, "event_country": d.event_country,
          "places": [{"name": p, "country": c, "in_scope": bool(c and c in s.place_scope)} for p, c in sorted(d.places.items())],
          "principal_parties": sorted(d.parties), "anchor_parties": sorted(s.anchors), "report_share": d.report_share,
          "mixed_flag": d.mixed, "hedge_terms": d.hedges, "scope_snapshot": s.snapshot(), "scope_source": s.scope_source,
          "situation_mode": s.mode, "contract_version": CONTRACT_VERSION}
    if s.actor_keyed and not d.has_principals:
        return Decision("NOT_MEMBER", "NO_PRINCIPALS", ev)
    ok, why, e1 = identity_match(d, s, signals)
    ev.update(e1)
    if ok and not d.occurrence:
        return Decision("CONTEXT", "COMMENTARY_ONLY", ev)
    if ok and d.mixed:
        return Decision("PENDING", "PENDING_MIXED", ev)
    if not ok:
        return Decision("NOT_MEMBER", why, ev)
    if s.mode == "single_party":
        if d.family != next(iter(s.families), None):
            return Decision("NOT_MEMBER", "OUT_OF_SCOPE_DOMAIN", ev)
        if d.event_country not in s.place_scope:
            return Decision("NOT_MEMBER", "OUT_OF_SCOPE_PLACE", ev)
    known = [c for c in d.places.values() if c]
    if d.family and d.family in s.families and known and not any(c in s.place_scope for c in known):
        return Decision("SPILLOVER", "OUT_OF_SCOPE_PLACE", ev)
    if not signals:
        return Decision("NOT_MEMBER", "NO_SCOPE_SIGNAL", ev)
    if d.family and s.families and d.family not in s.families:
        return Decision("NOT_MEMBER", "OUT_OF_SCOPE_DOMAIN", ev)
    return Decision("MEMBER", "CONTINUATION", ev)


def _strength(dec: Decision, s: Situation2) -> tuple:
    kinds = {k for k, _ in dec.evidence.get("scope_signals", [])}
    return (dec.evidence.get("coverage", 1.0), len(kinds), 1 if s.mode == "seeded" else 0)


def decide(d: DevFeatures, s: Situation2, others: list[Situation2]) -> Decision:
    """The full §4 order for (D, S), comparing with every other open Situation (steps 7-8)."""
    dec = _base(d, s)
    if dec.outcome != "MEMBER":
        return dec
    mine = _strength(dec, s)
    rivals = []
    for o in others:
        if o.slug == s.slug or o.status == "closed":
            continue
        od = _base(d, o)
        if od.outcome == "MEMBER":
            rivals.append((o, _strength(od, o)))
    better = [o.slug for o, st in rivals if st > mine]
    if better:
        dec.evidence["better_situation"] = better
        return Decision("OTHER_SITUATION", "BETTER_SITUATION", dec.evidence)
    ties = [o.slug for o, st in rivals if st == mine]
    if ties:
        dec.evidence["tied_with"] = ties
        return Decision("AMBIGUOUS", "AMBIGUOUS", dec.evidence)
    if d.hedges:
        return Decision("PENDING", "PENDING_ATTRIBUTION", dec.evidence)
    return dec


# -- §1 creation from founders (used to rebuild the v2 version of an existing Situation) -------------

def derive_automatic(slug: str, anchors: frozenset[str], founders: list[DevFeatures],
                     anchor_countries: set[str]) -> tuple[list[Situation2], str]:
    """The v2 Situation(s) its founders would create, or ([], why not). Founders are judged with v2 features."""
    occ = [f for f in founders if f.occurrence and not f.mixed]
    if len(anchors) >= 2:
        qual = [f for f in occ if f.has_principals and f.family and anchors <= f.parties]
        by_fam: dict[str, list[DevFeatures]] = {}
        for f in qual:
            by_fam.setdefault(f.family, []).append(f)
        made = []
        for fam, fs in sorted(by_fam.items()):
            if len(fs) >= 2 and _within(fs, CREATE_WINDOW):
                fams = frozenset({fam} | {f.family for f in founders if f.family})
                places = {c for f in founders for c in f.places.values() if c} | anchor_countries
                made.append(Situation2(f"{slug}~{fam}" if len(by_fam) > 1 else slug, "actor_process", anchors, fams,
                                       frozenset(places), founders=tuple(f.event_id for f in fs)))
        return made, "" if made else "no two founders share anchor parties and a family"
    if len(anchors) == 1:
        p = next(iter(anchors))
        if p in GENERIC_PARTIES:
            return [], "single party is generic (OD1/OD6)"
        qual = [f for f in occ if p in f.parties and f.family and f.event_country]
        groups: dict[tuple[str, str], list[DevFeatures]] = {}
        for f in qual:
            groups.setdefault((f.family, f.event_country), []).append(f)
        for (fam, c), fs in sorted(groups.items()):
            if len(fs) >= 2 and _within(fs, CREATE_WINDOW, SINGLE_PARTY_SEPARATION):
                return [Situation2(slug, "single_party", anchors, frozenset({fam}), frozenset({c}),
                                   founders=tuple(f.event_id for f in fs))], ""
        return [], "no two founders >= 24 h apart share the party, a family and an event country"
    hz = [f for f in occ if f.hazard and f.event_country]
    groups2: dict[tuple, list[DevFeatures]] = {}
    for f in hz:
        groups2.setdefault((f.hazard[0], f.event_country, f.hazard[1]), []).append(f)
    for (h, c, n), fs in sorted(groups2.items(), key=lambda kv: str(kv[0])):
        if len(fs) >= 2 and _within(fs, CREATE_WINDOW):
            return [Situation2(slug, "hazard", frozenset(), frozenset({"hazard"}), frozenset({c}), hazard=(h, c, n),
                               founders=tuple(f.event_id for f in fs))], ""
    return [], "no anchor parties and no two founders share a hazard and country"


def _within(fs: list[DevFeatures], window: timedelta, min_gap: timedelta = timedelta(0)) -> bool:
    """Some two founders were first reported within ``window`` of each other and at least ``min_gap`` apart."""
    ts = sorted(f.first_reported_at for f in fs if f.first_reported_at)
    return any(min_gap <= (b - a) <= window for i, a in enumerate(ts) for b in ts[i + 1:])
