"""Principal actors: the parties taking part in or driving a development.

Everything the NER finds in an article is an *entity*; only some are *principal*.
"Xi Jinping met the US president to discuss Taiwan" involves China and the US;
Taiwan is a topic. Situation grouping and ranking should look at principals only.

Deterministic, no LLM. Five stages, each a function here:

1. **Candidates** (``item_candidates``): actor mentions in an item's headline and lead
   sentence -- NER spans labelled PERSON / NORP / GPE / ORG, plus tokens the actor
   config names that the NER missed or mislabelled ("Xi-Trump summit", Trump as
   WORK_OF_ART). Each gets a grammatical role (``is_participant``): after climbing
   through modifiers (compound, amod, poss, conj, appos, "of") it is a participant when
     - subject, object, dative, agent or complement of a clause,
     - the object of "with" / "between" / "against" / "by",
     - a modifier or guest of a meeting noun ("Trump-Xi summit", "Trump's state dinner
       for Xi", "visit to the US"), or the target of a coercive one ("sanctions on Russia"),
   and a topic when it is the object of a topic verb ("discuss"), the subject of an
   agenda verb ("top"), in a list with common nouns ("Trade, AI, Iran and Taiwan"), or
   the object of any other preposition ("on", "over", "amid", "in", ...).
2. **Normalisation** and 3. **canonical mapping** (``ActorNormalizer``): possessives and
   punctuation stripped, non-actors dropped, demonyms and aliases resolved, people
   mapped to the state they act for.
4. **Aggregation** (``aggregate``): support per canonical actor across the event's items.
   An item counts once per actor: 1.0 as a headline participant, 0.5 as a lead-sentence
   participant (1.0 when the headline names no participant at all). "Trump", "US" and
   "White House" in three headlines are one actor with three mentions.
5. **Selection** (``select_principals``): principal when support reaches 1 for 1-2 item
   events, else ``max(1.5, 25% of items)`` -- two headlines, or one headline backed by
   another outlet's lead. One headline listing Iran among summit topics does not make
   Iran a principal of a US-China summit reported by ten outlets.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from sqlalchemy.orm import Session, joinedload

from osint_monitor.core.database import Entity, Event, EventEntity, EventItem, RawItem
from osint_monitor.processors.actors import ActorNormalizer

logger = logging.getLogger(__name__)

ACTOR_LABELS = {"PERSON", "NORP", "GPE", "ORG"}
CLIMB_DEPS = {"compound", "amod", "poss", "nmod", "appos", "conj", "flat", "case", "nummod", "cc"}
PARTICIPANT_DEPS = {"nsubj", "nsubjpass", "csubj", "csubjpass", "dobj", "iobj", "dative", "agent",
                    "attr", "oprd", "ROOT"}
PARTICIPANT_PREPS = {"with", "between", "against", "by"}
TARGET_PREPS = {"on", "upon", "against"}
# "sanctions on Russia", "strike on Iran": the object of a coercive measure is a party to it
TARGET_HEADS = {"sanction", "strike", "attack", "tariff", "embargo", "ban", "blockade", "raid", "crackdown",
                "pressure", "assault", "offensive", "bombardment", "restriction", "curb", "war", "measure",
                "levy", "penalty", "duty"}
# "Trump-Xi summit", "Xi's visit to the US", "state dinner for Xi": the parties to a meeting
MEETING_HEADS = {"summit", "talk", "talks", "meeting", "visit", "call", "dinner", "banquet", "reception",
                 "welcome", "ceremony", "handshake", "negotiation", "negotiations", "dialogue", "deal", "pact",
                 "accord", "agreement", "treaty", "truce", "meet"}
MEETING_PREPS = {"for", "to", "with", "between", "by", "from"}
TOPIC_VERBS = {"discuss", "debate", "address", "raise", "focus", "consider", "examine", "review",
               "weigh", "mull", "cite", "mention", "eye"}
# "Trade, AI and Iran top US-China talks": subjects of agenda verbs are topics
TOPIC_SUBJECT_VERBS = {"top", "dominate", "overshadow", "headline", "loom", "feature"}
WINDOW_DAYS = 3
HEADLINE, LEAD = 1.0, 0.5


def is_participant(span, actor_tokens: set[int] | None = None) -> bool:
    """Whether an actor span takes part in its sentence rather than being a topic or place.

    ``actor_tokens``: indices of every actor candidate in the sentence, so a list of actors
    ("Trump and Xi") is told apart from a list of topics ("Trade, AI and Iran").
    """
    def named(t) -> bool:
        return bool(t.ent_type_) or (actor_tokens is not None and t.i in actor_tokens)

    tok = span.root
    for _ in range(12):                       # parse trees in headlines are shallow
        dep = tok.dep_
        if dep in CLIMB_DEPS and tok.head is not tok:
            if dep == "conj" and not named(tok.head):
                return False                  # listed with common nouns: "Trade, AI, Iran and Taiwan"
            tok = tok.head
            if dep in {"compound", "amod", "poss", "nmod"} and tok.lemma_.lower() in MEETING_HEADS:
                return True                   # "Trump-Xi summit", "Trump's state dinner"
            continue
        if dep == "pobj":
            prep = tok.head
            word = prep.lower_
            head = prep.head.lemma_.lower()
            if word == "of" and prep.head is not prep:      # "president of Iran", "day of US visit"
                tok = prep.head
                continue
            if word in TARGET_PREPS and head in TARGET_HEADS:
                return True
            if word in MEETING_PREPS and head in MEETING_HEADS:
                return True                   # "dinner for Xi", "visit to the US"
            if word in PARTICIPANT_PREPS:
                return head not in TOPIC_VERBS
            return False
        if dep in PARTICIPANT_DEPS:
            head = tok.head.lemma_.lower()
            if dep in {"nsubj", "nsubjpass", "csubj", "csubjpass"}:
                return head not in TOPIC_SUBJECT_VERBS
            if dep != "ROOT" and dep != "agent" and head in TOPIC_VERBS:
                return False
            return True
        return False
    return False


# --- stage 1: candidates -------------------------------------------------------------------

@dataclass(frozen=True)
class Candidate:
    text: str
    participant: bool
    field: str                  # "title" | "lead"


def _spans(doc, normalizer: ActorNormalizer):
    """Actor spans: NER actors, plus configured actors the NER missed or mislabelled."""
    covered: set[int] = set()
    for ent in doc.ents:
        if ent.label_ in ACTOR_LABELS or normalizer.is_known(ent.text):
            covered.update(range(ent.start, ent.end))
            yield ent
    for tok in doc:
        if tok.i not in covered and tok.pos_ == "PROPN" and normalizer.is_known(tok.text):
            yield doc[tok.i:tok.i + 1]


def item_candidates(nlp, title: str, lead: str = "", normalizer: ActorNormalizer | None = None) -> list[Candidate]:
    normalizer = normalizer or ActorNormalizer.load()
    out = []
    for fld, text in (("title", title), ("lead", lead)):
        if text:
            spans = list(_spans(nlp(text[:500]), normalizer))
            actor_tokens = {i for sp in spans for i in range(sp.start, sp.end)}
            out.extend(Candidate(sp.text, is_participant(sp, actor_tokens), fld) for sp in spans)
    return out


# --- stages 2-3: normalisation and canonical mapping ----------------------------------------

@dataclass
class ItemEvidence:
    """Participants of one item, per canonical actor key, with the surface names seen."""
    title: dict[str, set[str]] = field(default_factory=dict)
    lead: dict[str, set[str]] = field(default_factory=dict)


def item_evidence(candidates: list[Candidate], normalizer: ActorNormalizer) -> ItemEvidence:
    ev = ItemEvidence()
    for c in candidates:
        if not c.participant:
            continue
        surface = normalizer.surface(c.text)
        if not surface:
            continue
        target = ev.title if c.field == "title" else ev.lead
        target.setdefault(normalizer.represents(surface), set()).add(surface)
    return ev


def item_participants(nlp, title: str, lead: str = "", normalizer: ActorNormalizer | None = None) -> set[str]:
    """Canonical surface names of the actors that participate in an item's headline
    (or, when the headline names none, in its lead sentence)."""
    normalizer = normalizer or ActorNormalizer.load()
    ev = item_evidence(item_candidates(nlp, title, lead, normalizer), normalizer)
    chosen = ev.title or ev.lead
    return {s for surfaces in chosen.values() for s in surfaces}


# --- stages 4-5: aggregation and selection --------------------------------------------------

@dataclass
class PrincipalSelection:
    keys: set[str]                                  # canonical actors (state level)
    surfaces: dict[str, set[str]]                   # key -> surface names seen as participant
    support: dict[str, float]                       # key -> weighted support
    required: float


def aggregate(evidence: list[ItemEvidence]) -> tuple[dict[str, float], dict[str, set[str]]]:
    """Weighted support per canonical actor, and the names it was seen under. Names from
    lead sentences are kept only for actors no headline named ("The Pentagon declined to
    comment" supports the United States but does not make the Pentagon a principal)."""
    support: dict[str, float] = defaultdict(float)
    headline_names: dict[str, set[str]] = defaultdict(set)
    lead_names: dict[str, set[str]] = defaultdict(set)
    for ev in evidence:
        lead_weight = LEAD if ev.title else HEADLINE      # the lead stands in for an actor-less headline
        for key in set(ev.title) | set(ev.lead):
            support[key] += HEADLINE if key in ev.title else lead_weight
            headline_names[key] |= ev.title.get(key, set())
            lead_names[key] |= ev.lead.get(key, set())
    return dict(support), {k: headline_names[k] or lead_names[k] for k in support}


def required_support(n_items: int) -> float:
    return 1.0 if n_items <= 2 else max(1.5, 0.25 * n_items)


def select_principals(evidence: list[ItemEvidence]) -> PrincipalSelection:
    support, surfaces = aggregate(evidence)
    need = required_support(len(evidence))
    keys = {k for k, s in support.items() if s >= need}
    return PrincipalSelection(keys, {k: surfaces[k] for k in keys}, support, need)


def principal_selection(nlp, items: list[tuple[str, str]],
                        normalizer: ActorNormalizer | None = None) -> PrincipalSelection:
    normalizer = normalizer or ActorNormalizer.load()
    return select_principals([item_evidence(item_candidates(nlp, t, lead, normalizer), normalizer)
                              for t, lead in items])


def principal_keys(nlp, items: list[tuple[str, str]], normalizer: ActorNormalizer | None = None) -> set[str]:
    """Canonical (state-level) keys of principal actors for an event given (title, lead) per item."""
    return principal_selection(nlp, items, normalizer).keys


def _lead(content: str | None) -> str:
    text = (content or "").strip()
    for stop in (". ", "\n"):
        if stop in text:
            text = text.split(stop, 1)[0]
    return text[:300]


# --- persistence ------------------------------------------------------------------------------

def mark_principal_actors(session: Session, now: datetime | None = None,
                          window_days: int = WINDOW_DAYS, normalizer: ActorNormalizer | None = None) -> dict:
    """Recompute EventEntity.is_principal for events updated in the window (idempotent).

    A linked entity is flagged when its canonical name is one of the surfaces seen as a
    participant ("Trump" for a selected United States). When no linked entity matches, an
    existing entity with that name is linked to the event.
    """
    from osint_monitor.processors.nlp import get_nlp

    now = now or datetime.utcnow()
    nlp = get_nlp()
    normalizer = normalizer or ActorNormalizer.load()
    events = session.query(Event).filter(Event.last_updated_at >= now - timedelta(days=window_days)).all()
    stats = {"events": len(events), "with_principals": 0, "without_principals": 0, "principal_links": 0}
    if not events:
        return stats

    by_surface: dict[str, Entity] | None = None      # all entities, built only if an event needs it
    for event in events:
        rows = [(t, c) for t, c in session.query(RawItem.title, RawItem.content)
                .join(EventItem, EventItem.item_id == RawItem.id).filter(EventItem.event_id == event.id)]
        selection = principal_selection(nlp, [(t or "", _lead(c)) for t, c in rows], normalizer)

        links = (session.query(EventEntity).options(joinedload(EventEntity.entity))
                 .filter(EventEntity.event_id == event.id).all())
        principal_ids: set[int] = set()
        for key in selection.keys:
            names = selection.surfaces[key] | {key}
            # the entity's own name must stand for this actor: an "Americas" entity that the
            # resolver gave an "America" alias is not the United States
            matched = {ee.entity_id for ee in links if ee.entity is not None
                       and normalizer.key(ee.entity.canonical_name) == key
                       and any(normalizer.surface(n) in names
                               for n in [ee.entity.canonical_name, *(ee.entity.aliases or [])])}
            if not matched:
                if by_surface is None:
                    by_surface = _entity_index(session, normalizer)
                entity = next((by_surface[s] for s in sorted(names) if s in by_surface), None)
                if entity is not None:            # named in a headline but not linked to the event yet
                    ee = EventEntity(event_id=event.id, entity_id=entity.id, role="SUBJECT", is_principal=True)
                    session.add(ee)
                    links.append(ee)
                    matched = {entity.id}
            principal_ids |= matched
        for ee in links:
            ee.is_principal = ee.entity_id in principal_ids
        stats["principal_links"] += len(principal_ids)
        stats["with_principals" if principal_ids else "without_principals"] += 1
    session.commit()
    return stats


def _entity_index(session: Session, normalizer: ActorNormalizer) -> dict[str, Entity]:
    index: dict[str, Entity] = {}
    for entity in session.query(Entity):
        surface = normalizer.surface(entity.canonical_name)
        if surface:
            index.setdefault(surface, entity)
    return index
