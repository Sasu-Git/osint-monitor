"""Principal actors: the parties taking part in or driving a development.

Everything the NER finds in an article is an *entity*; only some are *principal*.
"Xi Jinping met the US president to discuss Taiwan" involves China and the US;
Taiwan is a topic. Situation grouping and ranking should look at principals only.

Rule (deterministic, no LLM):

1. Per item, parse the title (and, if the title names no participant, the lead
   sentence). An actor entity (PERSON / NORP / GPE / ORG) is a *participant* when,
   after climbing through modifiers (compound, amod, poss, conj, appos, "of"), it is
     - subject, object, dative or agent of a clause, or
     - the object of "with" / "between" / "against" / "by",
   and it is not the object of a topic verb ("discuss", "address", ...) or of a
   topic preposition ("on", "over", "amid", "about", "in", ...).
2. Across the event's items, an entity is principal when it is a participant in
   at least ``max(2, 25%)`` of the items (1 for events with 1-2 items). One
   headline that lists Iran among summit topics does not make Iran a principal
   of a US-China summit reported by ten outlets.
"""

from __future__ import annotations

import logging
import math
from collections import Counter
from datetime import datetime, timedelta

from sqlalchemy.orm import Session, joinedload

from osint_monitor.core.database import Entity, Event, EventEntity, EventItem, RawItem
from osint_monitor.processors.entity_resolver import normalise

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
TOPIC_VERBS = {"discuss", "debate", "address", "raise", "focus", "consider", "examine", "review",
               "weigh", "mull", "cite", "mention", "eye"}
# "Trade, AI and Iran top US-China talks": subjects of agenda verbs are topics
TOPIC_SUBJECT_VERBS = {"top", "dominate", "overshadow", "headline", "loom", "feature"}
WINDOW_DAYS = 3


def is_participant(span) -> bool:
    """Whether an entity span takes part in its sentence rather than being a topic or place."""
    tok = span.root
    for _ in range(12):                       # parse trees in headlines are shallow
        dep = tok.dep_
        if dep in CLIMB_DEPS and tok.head is not tok:
            tok = tok.head
            continue
        if dep == "pobj":
            prep = tok.head
            word = prep.lower_
            if word == "of" and prep.head is not prep:      # "president of Iran", "day of US visit"
                tok = prep.head
                continue
            if word in TARGET_PREPS and prep.head.lemma_.lower() in TARGET_HEADS:
                return True
            if word in PARTICIPANT_PREPS:
                return prep.head.lemma_.lower() not in TOPIC_VERBS
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


def item_participants(nlp, title: str, lead: str = "") -> set[str]:
    """Normalised keys of the actor entities that participate in an item's headline
    (or, when the headline names none, in its lead sentence)."""
    for text in (title, lead):
        if not text:
            continue
        doc = nlp(text[:500])
        keys = {normalise(ent.text) for ent in doc.ents if ent.label_ in ACTOR_LABELS and is_participant(ent)}
        keys.discard("")
        if keys:
            return keys
    return set()


def required_support(n_items: int) -> int:
    return 1 if n_items <= 2 else max(2, math.ceil(0.25 * n_items))


def principal_keys(nlp, items: list[tuple[str, str]]) -> set[str]:
    """Normalised keys of principal actors for an event given (title, lead) per item."""
    support: Counter[str] = Counter()
    for title, lead in items:
        support.update(item_participants(nlp, title, lead))
    need = required_support(len(items))
    return {k for k, n in support.items() if n >= need}


def _lead(content: str | None) -> str:
    text = (content or "").strip()
    for stop in (". ", "\n"):
        if stop in text:
            text = text.split(stop, 1)[0]
    return text[:300]


def mark_principal_actors(session: Session, now: datetime | None = None,
                          window_days: int = WINDOW_DAYS) -> dict:
    """Recompute EventEntity.is_principal for events updated in the window (idempotent)."""
    from osint_monitor.processors.nlp import get_nlp

    now = now or datetime.utcnow()
    nlp = get_nlp()
    events = session.query(Event).filter(Event.last_updated_at >= now - timedelta(days=window_days)).all()
    stats = {"events": len(events), "with_principals": 0, "without_principals": 0, "principal_links": 0}
    if not events:
        return stats

    by_key: dict[str, Entity] | None = None      # all entities, built only if an event needs it
    for event in events:
        rows = [(t, c) for t, c in session.query(RawItem.title, RawItem.content)
                .join(EventItem, EventItem.item_id == RawItem.id).filter(EventItem.event_id == event.id)]
        keys = principal_keys(nlp, [(t or "", _lead(c)) for t, c in rows])

        links = (session.query(EventEntity).options(joinedload(EventEntity.entity))
                 .filter(EventEntity.event_id == event.id).all())
        linked: dict[str, list[EventEntity]] = {}
        for ee in links:
            if ee.entity is None:
                continue
            names = [ee.entity.canonical_name, *(ee.entity.aliases or [])]
            for name in names:
                linked.setdefault(normalise(name), []).append(ee)

        principal_ids: set[int] = set()
        for key in keys:
            if key in linked:
                principal_ids.update(ee.entity_id for ee in linked[key])
                continue
            if by_key is None:
                by_key = _entity_index(session)
            entity = by_key.get(key)
            if entity is not None:                # named in a headline but not linked to the event yet
                ee = EventEntity(event_id=event.id, entity_id=entity.id, role="SUBJECT", is_principal=True)
                session.add(ee)
                links.append(ee)
                principal_ids.add(entity.id)
        for ee in links:
            ee.is_principal = ee.entity_id in principal_ids
        stats["principal_links"] += len(principal_ids)
        stats["with_principals" if principal_ids else "without_principals"] += 1
    session.commit()
    return stats


def _entity_index(session: Session) -> dict[str, Entity]:
    index: dict[str, Entity] = {}
    for entity in session.query(Entity):
        for name in [entity.canonical_name, *(entity.aliases or [])]:
            index.setdefault(normalise(name), entity)
    return index
