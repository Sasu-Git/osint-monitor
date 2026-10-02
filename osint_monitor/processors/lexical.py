"""Lexical identity evidence: where the *words* of two narrative items, rather than their
embeddings, bear on whether they report the same Development.

Production uses exactly one lexical link criterion, and it is here:

- ``same_source_update``: two items from the same outlet link only when their headlines are
  near-identical (a story update). Cross-source links are decided by embedding similarity
  (``clustering._linked``); no term, keyword or actor overlap links two items.

Other lexical rules that touch identity and stay where they are (not changed by this module):
exact-text dedup (``dedup.compute_content_hash``), the headline-form guard in development
segmentation (``development_segmentation.headline_kind``), entity alias resolution
(``entity_resolver``) and the region label (``clustering.region_scores``, a label, not identity).

The rest of the module is diagnostic: it extracts an item's terms, classifies them by how much
they say about *which* occurrence an item reports, and explains the overlap of two items
(``keyword_link_evidence``). Classes:

- ``high``: specific names -- people and organisations, sub-national places, named events and
  products (operations, treaties, ships, aircraft types);
- ``medium``: content words that are not common in the batch being compared (concrete actions,
  event-specific policy or legal terms, weapon types);
- ``generic``: country-level places and nationalities (context), and content words common in
  the batch (``generic_document_frequency``: "war", "attack", "talks" in a conflict-heavy feed)
  or listed in ``generic_terms``.

Classes come from entity types, the gazetteer and document frequency, not from a hand-written
blacklist; ``config/event_grouping.yaml`` (``lexical``) holds the policy. Same actors are never
treated as same Development: shared actors are reported, and only high/medium terms count as
event-specific evidence.

``guard`` is an optional candidate link rule evaluated on the frozen benchmark
(evaluations/clustering/lexical-identity.md). It is off unless enabled in config.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Iterable

from rapidfuzz import fuzz

from osint_monitor.core.config import LexicalConfig

HIGH, MEDIUM, GENERIC = "high", "medium", "generic"
ACTOR, PLACE, NAME, WORD = "actor", "place", "name", "word"

ACTOR_TYPES = ("PERSON", "ORG")
PLACE_TYPES = ("GPE", "LOC", "FAC", "FACILITY")
NAME_TYPES = ("EVENT", "PRODUCT", "WEAPON_SYSTEM", "LAW", "WORK_OF_ART")
CONTEXT_ACTOR_TYPES = ("NORP",)           # nationalities / groups: context, like country names

_WORD = re.compile(r"[a-z][a-z'\-]*[a-z]")


# --- configuration ---------------------------------------------------------------------------------

_override: LexicalConfig | None = None


@lru_cache(maxsize=1)
def _loaded() -> LexicalConfig:
    from osint_monitor.core.config import load_event_grouping_config
    return load_event_grouping_config().lexical


def settings() -> LexicalConfig:
    return _override or _loaded()


def use_settings(config: LexicalConfig | None) -> None:
    """Override the configured lexical settings (benchmark candidates, tests); None restores them."""
    global _override
    _override = config


# --- the production link criterion ------------------------------------------------------------------

def headline_ratio(a: str, b: str) -> float:
    return fuzz.ratio((a or "").lower(), (b or "").lower())


def same_source_update(a_title: str, b_title: str, config: LexicalConfig | None = None) -> bool:
    """Two items from one outlet are one Development only when the headline is near-identical."""
    return headline_ratio(a_title, b_title) >= (config or settings()).same_source_title_ratio


# --- terms -----------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Term:
    text: str              # normalised: alias-folded names, lower-case singular words
    kind: str              # actor | place | name | word
    cls: str = MEDIUM      # high | medium | generic
    reason: str = ""


@dataclass
class ItemTerms:
    item_id: int | str
    terms: dict[str, Term] = field(default_factory=dict)   # text -> term

    def of(self, *classes: str) -> set[str]:
        return {t for t, term in self.terms.items() if term.cls in classes}

    @property
    def actors(self) -> set[str]:
        return {t for t, term in self.terms.items() if term.kind == ACTOR}


def _fold(word: str) -> str:
    """Deterministic singular: strikes -> strike, talks -> talk; leaves -ss/-us/-is words."""
    word = word.strip("'-").removesuffix("'s")
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"                              # militias -> militia, but: casualties -> casualty
    if len(word) > 4 and word.endswith(("sses", "xes", "ches", "shes")):
        return word[:-2]                                    # glasses -> glass, taxes -> tax
    if len(word) > 3 and word.endswith("s") and not word.endswith(("ss", "us", "is")):
        return word[:-1]
    return word


@lru_cache(maxsize=1)
def _stop_words() -> frozenset[str]:
    from spacy.lang.en.stop_words import STOP_WORDS
    return frozenset(STOP_WORDS)


def content_words(text: str) -> list[str]:
    stop = _stop_words()
    return [_fold(w) for w in _WORD.findall((text or "").lower().replace("’", "'"))
            if len(w) >= 3 and w not in stop and _fold(w) not in stop]


class TermExtractor:
    """Terms of an item's headline and lead, with names folded through the actor and place
    aliases the rest of the pipeline uses (config/actors.yaml, config/geography.yaml)."""

    def __init__(self, normalizer=None, gazetteer=None, config: LexicalConfig | None = None):
        if normalizer is None:
            from osint_monitor.processors.actors import ActorNormalizer
            normalizer = ActorNormalizer.load()
        if gazetteer is None:
            from osint_monitor.processors.geography import Gazetteer
            gazetteer = Gazetteer.load()
        self.normalizer, self.gazetteer = normalizer, gazetteer
        self.config = config or settings()
        self.generic_terms = {_fold(w.lower()) for w in self.config.generic_terms}

    def raw_terms(self, title: str, lead: str, entities: Iterable[tuple[str, str]]) -> list[Term]:
        """Unclassified terms. ``entities``: (name, type) mentions of the item."""
        from osint_monitor.processors.entity_resolver import normalise
        terms: dict[str, Term] = {}
        name_words: set[str] = set()
        for name, etype in entities:
            etype = (etype or "").upper()
            if etype in PLACE_TYPES:
                key = self.gazetteer.canonical(name)
                kind = PLACE
            elif etype in ACTOR_TYPES or etype in CONTEXT_ACTOR_TYPES:
                key = self.normalizer.surface(name)
                if key and etype in CONTEXT_ACTOR_TYPES:
                    key = self.gazetteer.canonical(key)       # "Iranian" -> "iran": a country, context
                kind = ACTOR if etype in ACTOR_TYPES else PLACE
            elif etype in NAME_TYPES:
                key, kind = normalise(name), NAME
            else:
                continue
            if not key:
                continue
            name_words |= set(content_words(name)) | set(content_words(key))
            terms.setdefault(key, Term(key, kind))
        text = f"{title or ''} {lead or ''}"
        for w in content_words(text):
            if w not in name_words and w not in terms:
                terms[w] = Term(w, WORD)
        return list(terms.values())

    def _frequent(self, text: str, df: Counter | None, n_docs: int) -> float | None:
        c = self.config
        if df is None or n_docs < c.min_documents_for_frequency:
            return None
        share = df[text] / n_docs
        return share if share >= c.generic_document_frequency else None

    def classify(self, term: Term, df: Counter | None = None, n_docs: int = 0,
                 participants: set[str] | None = None) -> Term:
        """``participants``: actors the item's headline/lead shows taking part in the action
        (``principals.item_participants``); a named actor only mentioned is weaker evidence."""
        frequent = self._frequent(term.text, df, n_docs)
        if term.kind in (PLACE, ACTOR) and self.gazetteer.is_country(term.text):
            return Term(term.text, term.kind, GENERIC, "country: context")
        if term.kind == ACTOR:
            if participants is not None and term.text in participants:
                return Term(term.text, term.kind, HIGH, "participant in the reported action")
            if frequent is not None:
                return Term(term.text, term.kind, GENERIC, f"mentioned in {frequent:.0%} of the batch")
            if participants is not None:
                return Term(term.text, term.kind, MEDIUM, "mentioned, not a participant")
            return Term(term.text, term.kind, HIGH, "named person or organisation")
        if term.kind in (PLACE, NAME):
            label = "specific place" if term.kind == PLACE else "named event, product or system"
            if frequent is not None:
                return Term(term.text, term.kind, MEDIUM, f"{label}, in {frequent:.0%} of the batch")
            return Term(term.text, term.kind, HIGH, label)
        if term.text in self.generic_terms:
            return Term(term.text, term.kind, GENERIC, "configured generic term")
        if frequent is not None:
            return Term(term.text, term.kind, GENERIC, f"in {frequent:.0%} of the batch")
        return Term(term.text, term.kind, MEDIUM, "content word")

    def extract(self, item_id, title: str, lead: str, entities: Iterable[tuple[str, str]],
                df: Counter | None = None, n_docs: int = 0, participants: set[str] | None = None) -> ItemTerms:
        """extract + classify: the item's terms and their identity value."""
        out = ItemTerms(item_id)
        for t in self.raw_terms(title, lead, entities):
            out.terms[t.text] = self.classify(t, df, n_docs, participants)
        return out


def document_frequencies(items: Iterable[Iterable[str]]) -> tuple[Counter, int]:
    """(term -> number of items containing it, number of items), over raw term texts."""
    df, n = Counter(), 0
    for terms in items:
        df.update(set(terms))
        n += 1
    return df, n


def batch_terms(items, extractor: TermExtractor | None = None, nlp=None) -> dict:
    """ItemTerms for a batch of RawItems (the clustering window), with document frequencies
    taken over the batch and participants from each headline/lead. Keyed by item id."""
    from osint_monitor.processors.principals import item_participants
    if nlp is None:
        from osint_monitor.processors.nlp import get_nlp
        nlp = get_nlp()
    extractor = extractor or TermExtractor()
    mentions = {i.id: [(ie.entity.canonical_name, ie.entity.entity_type) for ie in i.item_entities if ie.entity]
                for i in items}
    raw = {i.id: extractor.raw_terms(i.title or "", lead_of(i.content), mentions[i.id]) for i in items}
    df, n = document_frequencies([[t.text for t in ts] for ts in raw.values()])
    out = {}
    for i in items:
        lead = lead_of(i.content)
        participants = item_participants(nlp, i.title or "", lead, extractor.normalizer)
        out[i.id] = extractor.extract(i.id, i.title or "", lead, mentions[i.id], df, n, participants)
    return out


def lead_of(text: str | None, chars: int = 200) -> str:
    """The part of an item's body the clustering embedding sees (``embeddings.embed_item``)."""
    return (text or "")[:chars]


# --- evidence for one pair -------------------------------------------------------------------------

EVENT_SPECIFIC = "event-specific lexical evidence"
INSUFFICIENT = "insufficient event-specific lexical evidence"
NO_SHARED = "no shared terms"


@dataclass
class LexicalEvidence:
    shared_actors: list[str]
    shared_high: list[str]
    shared_medium: list[str]
    shared_generic: list[str]
    weighted_overlap: float
    result: str
    contribution: str = "diagnostic only"
    same_source: bool = False
    headline_ratio: float | None = None
    similarity: float | None = None

    @property
    def event_specific(self) -> list[str]:
        return self.shared_high + self.shared_medium

    def as_dict(self) -> dict:
        return {k: getattr(self, k) for k in ("shared_actors", "shared_high", "shared_medium", "shared_generic",
                                              "weighted_overlap", "result", "contribution", "same_source",
                                              "headline_ratio", "similarity")}

    def format(self) -> str:
        def block(title, values):
            return [f"{title}:"] + ([f"  {v}" for v in values] if values else ["  -"])
        lines = ["keyword evidence", "----------------"]
        lines += block("shared principal / named actors", self.shared_actors)
        lines += block("shared high-value terms", [t for t in self.shared_high if t not in self.shared_actors])
        lines += block("shared medium-value terms", self.shared_medium)
        lines += block("shared generic terms", self.shared_generic)
        lines += ["weighted lexical overlap:", f"  {self.weighted_overlap:.2f}"]
        if self.similarity is not None:
            lines += ["embedding similarity:", f"  {self.similarity:.3f}"]
        if self.same_source and self.headline_ratio is not None:
            lines += ["same-outlet headline ratio:", f"  {self.headline_ratio:.0f}"]
        lines += ["result:", f"  {self.result}", "decision contribution:", f"  {self.contribution}"]
        return "\n".join(lines)


def keyword_overlap(a: ItemTerms, b: ItemTerms, config: LexicalConfig | None = None) -> float:
    """Shared term weight over the smaller item's term weight (diagnostic; not a probability)."""
    w = (config or settings()).class_weights
    def weight(terms: ItemTerms, keys: Iterable[str]) -> float:
        return sum(w.get(terms.terms[k].cls, 0.0) for k in keys)
    shared = a.terms.keys() & b.terms.keys()
    smaller = min(weight(a, a.terms), weight(b, b.terms))
    return round(weight(a, shared) / smaller, 3) if smaller else 0.0


def keyword_link_evidence(a: ItemTerms, b: ItemTerms, *, same_source: bool = False,
                          a_title: str = "", b_title: str = "", similarity: float | None = None,
                          linked: bool | None = None, config: LexicalConfig | None = None) -> LexicalEvidence:
    """Explain what the words of two items say about them being one Development.

    ``linked``: the production decision for the pair, when known, so the contribution can be
    stated (lexical evidence decides only same-outlet links; elsewhere it corroborates)."""
    config = config or settings()
    shared = sorted(a.terms.keys() & b.terms.keys())
    # a term's class is the less specific of its two classifications (document frequency is per batch)
    order = {GENERIC: 0, MEDIUM: 1, HIGH: 2}
    cls = {t: min(a.terms[t].cls, b.terms[t].cls, key=order.get) for t in shared}
    ev = LexicalEvidence(
        shared_actors=[t for t in shared if a.terms[t].kind == ACTOR],
        shared_high=[t for t in shared if cls[t] == HIGH],
        shared_medium=[t for t in shared if cls[t] == MEDIUM],
        shared_generic=[t for t in shared if cls[t] == GENERIC],
        weighted_overlap=keyword_overlap(a, b, config),
        result=NO_SHARED, same_source=same_source, similarity=similarity)
    if ev.event_specific:
        ev.result = EVENT_SPECIFIC
    elif shared:
        ev.result = INSUFFICIENT
    if same_source:
        ev.headline_ratio = headline_ratio(a_title, b_title)
        ev.contribution = ("same-outlet update link (headline ratio)" if ev.headline_ratio >= config.same_source_title_ratio
                           else "same-outlet link refused (headlines differ)")
    elif linked is not None:
        ev.contribution = "corroborating signal only" if linked else "none: the embedding link decides"
    return ev


# --- the candidate guard (off by default) -----------------------------------------------------------

def guard_allows(evidence: LexicalEvidence, similarity: float, config: LexicalConfig | None = None) -> bool:
    """Candidate rule: a cross-source embedding link below ``guard.max_similarity`` stands only if
    the pair shares at least ``guard.min_event_specific`` event-specific (high/medium) terms."""
    g = (config or settings()).guard
    if not g.enabled or similarity >= g.max_similarity:
        return True
    return len(evidence.event_specific) >= g.min_event_specific
