"""NER and event extraction via spaCy."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import spacy
from spacy.language import Language

from osint_monitor.core.config import get_settings, load_entities_config
from osint_monitor.core.models import EntityRole, EntityType, ExtractedEntity

if TYPE_CHECKING:
    from spacy.tokens import Doc

logger = logging.getLogger(__name__)

# Map spaCy labels to our EntityType
SPACY_LABEL_MAP: dict[str, EntityType] = {
    "PERSON": EntityType.PERSON,
    "ORG": EntityType.ORG,
    "GPE": EntityType.GPE,
    "NORP": EntityType.NORP,
    "FAC": EntityType.FAC,
    "EVENT": EntityType.EVENT,
    "PRODUCT": EntityType.PRODUCT,
    "LOC": EntityType.LOC,
}

# Action verbs that indicate event types
EVENT_VERB_MAP: dict[str, str] = {
    "attack": "military_action",
    "strike": "military_action",
    "bomb": "military_action",
    "shell": "military_action",
    "invade": "military_action",
    "deploy": "military_deployment",
    "mobilize": "military_deployment",
    "move": "troop_movement",
    "launch": "missile_launch",
    "fire": "military_action",
    "sanction": "sanctions",
    "negotiate": "diplomacy",
    "sign": "diplomacy",
    "agree": "diplomacy",
    "meet": "diplomacy",
    "warn": "escalation",
    "threaten": "escalation",
    "test": "weapons_test",
    "detonate": "weapons_test",
    "arrest": "law_enforcement",
    "seize": "law_enforcement",
    "hack": "cyber_attack",
    "breach": "cyber_attack",
    "evacuate": "humanitarian",
    "flee": "humanitarian",
    "protest": "civil_unrest",
    "revolt": "civil_unrest",
    "coup": "regime_change",
    "elect": "political",
    "resign": "political",
    "assassinate": "assassination",
}

_nlp_instance: Language | None = None
FALLBACK_MODEL = "en_core_web_sm"


class SpacyModelMissing(RuntimeError):
    """The configured spaCy language model is not installed (it is not a pip dependency)."""

    def __init__(self, model_name: str):
        super().__init__(
            f"spaCy model '{model_name}' is not installed.\n"
            f"Install it into the project environment with:\n"
            f"    python -m spacy download {model_name}\n"
            f"(or set OSINT_SPACY_MODEL to a model you have installed)"
        )
        self.model_name = model_name


def get_nlp() -> Language:
    """Load spaCy model (cached singleton). Never downloads models at runtime."""
    global _nlp_instance
    if _nlp_instance is not None:
        return _nlp_instance

    settings = get_settings()
    model_name = settings.spacy_model

    try:
        _nlp_instance = spacy.load(model_name)
        logger.info(f"Loaded spaCy model: {model_name}")
    except OSError:
        if model_name == FALLBACK_MODEL:
            raise SpacyModelMissing(model_name) from None
        try:
            _nlp_instance = spacy.load(FALLBACK_MODEL)
        except OSError:
            raise SpacyModelMissing(model_name) from None
        logger.warning(f"spaCy model {model_name} not installed; using {FALLBACK_MODEL} "
                       f"(lower NER quality). Install with: python -m spacy download {model_name}")

    # Add custom EntityRuler for weapons systems etc.
    _add_entity_ruler(_nlp_instance)
    return _nlp_instance


def _add_entity_ruler(nlp: Language):
    """Add custom entity patterns from entities.yaml."""
    patterns = []
    try:
        entities = load_entities_config()
        for ent in entities:
            # Add canonical name pattern
            patterns.append({
                "label": ent.entity_type,
                "pattern": ent.canonical_name,
            })
            # Add alias patterns
            for alias in ent.aliases:
                patterns.append({
                    "label": ent.entity_type,
                    "pattern": alias,
                })
    except Exception as e:
        logger.debug(f"Could not load entity seeds: {e}")

    if patterns:
        ruler = nlp.add_pipe("entity_ruler", before="ner", config={"overwrite_ents": False})
        ruler.add_patterns(patterns)
        logger.info(f"Added {len(patterns)} custom entity patterns")


# --- language routing ----------------------------------------------------------------------------
# English uses settings.spacy_model. Italian and Spanish items get their own models; a language without an
# installed model gets no entities at all rather than English NER over foreign text (which turned clauses
# into "entities" and principals). Install: python -m spacy download it_core_news_md es_core_news_md
LANGUAGE_MODELS = {"it": "it_core_news_md", "es": "es_core_news_md"}
_language_instances: dict[str, Language | None] = {}
# it/es models label PER / ORG / LOC / MISC; LOC becomes GPE for places the gazetteer knows, MISC is dropped
UD_LABEL_MAP: dict[str, EntityType | None] = {"PER": EntityType.PERSON, "ORG": EntityType.ORG,
                                                "LOC": EntityType.LOC, "MISC": None}


def get_language_nlp(lang: str | None) -> Language | None:
    """The spaCy pipeline for ``lang`` ("en", "it", "es"), or None when no trusted model is installed."""
    lang = (lang or "en").split("-")[0].lower()
    if lang == "en":
        return get_nlp()
    if lang not in LANGUAGE_MODELS:
        return None
    if lang not in _language_instances:
        try:
            nlp = spacy.load(LANGUAGE_MODELS[lang])
            _add_entity_ruler(nlp)
            _language_instances[lang] = nlp
            logger.info(f"Loaded spaCy model: {LANGUAGE_MODELS[lang]}")
        except OSError:
            logger.warning(f"spaCy model {LANGUAGE_MODELS[lang]} not installed: no entities for '{lang}' items "
                           f"(install with: python -m spacy download {LANGUAGE_MODELS[lang]})")
            _language_instances[lang] = None
    return _language_instances[lang]


_GEO = None


def entity_type_of(label: str, text: str, lang: str = "en") -> EntityType | None:
    """Our entity type for a spaCy label: the English model's OntoNotes labels, or the it/es models'
    PER / ORG / LOC / MISC (the entity ruler adds our own labels to every model)."""
    global _GEO
    if lang == "en" or label not in UD_LABEL_MAP:
        return SPACY_LABEL_MAP.get(label)
    etype = UD_LABEL_MAP.get(label)
    if etype is EntityType.LOC:
        if _GEO is None:
            from osint_monitor.processors.geography import Gazetteer
            _GEO = Gazetteer.load()
        if _GEO.is_country(text) or _GEO.is_subnational(text):
            return EntityType.GPE
    return etype


# --- mention validation (all languages) -----------------------------------------------------------
_LEAD_DROP = {"AUX", "VERB", "SCONJ", "PRON", "ADP", "CCONJ", "PUNCT"}
_TRAIL_DROP = {"AUX", "VERB", "ADP", "DET", "CCONJ", "SCONJ", "PUNCT", "PRON"}
MAX_MENTION_TOKENS = 6


def mention_span(span):
    """The name inside an NER span, or None when the span is clause-like.

    Leading and trailing function words, verbs and lower-case common words are trimmed ("north Gaza" ->
    "Gaza", "oficial de EEUU" -> "EEUU", "What Will Hegseth" -> "Hegseth"); what remains must contain no verb,
    have at most MAX_MENTION_TOKENS tokens and contain a capital letter ("la moneda de Irán se hunde en un",
    "que recibió la respuesta" fail)."""
    start, end = span.start, span.end
    doc = span.doc

    def droppable_lead(t):
        return t.pos_ in _LEAD_DROP or (t.is_lower and t.pos_ not in ("PROPN",)) or (t.pos_ == "DET" and t.is_lower)

    def droppable_trail(t):
        return t.pos_ in _TRAIL_DROP or (t.is_lower and t.pos_ not in ("PROPN", "NUM"))

    while start < end and droppable_lead(doc[start]):
        start += 1
    while end > start and droppable_trail(doc[end - 1]):
        end -= 1
    if start >= end:
        return None
    core = doc[start:end]
    words = [t for t in core if not t.is_punct]              # "Izz al-Din al-Beik" is four words, not seven tokens
    if len(words) > MAX_MENTION_TOKENS or any(t.pos_ in ("VERB", "AUX") for t in core):
        return None
    if not any(ch.isupper() for ch in core.text) or any(t.text in (";", "?", "!") for t in core):
        return None
    return core


def extract_entities(text: str, lang: str = "en") -> list[ExtractedEntity]:
    """Extract named entities from text."""
    from osint_monitor.processors.text_normalize import clean_name, clean_text
    nlp = get_language_nlp(lang)
    if nlp is None:
        return []                          # no trusted model for this language: no entities, not wrong ones
    doc = nlp(clean_text(text)[:10000])  # limit input size

    entities: list[ExtractedEntity] = []
    seen: set[str] = set()

    for ent in doc.ents:
        span = mention_span(ent)
        if span is None:
            continue
        etype = entity_type_of(ent.label_, span.text, (lang or "en").split("-")[0].lower())
        if etype is None:
            continue
        name = clean_name(span.text)
        if not name:
            continue

        key = f"{name.lower()}:{etype}"
        if key in seen:
            continue
        seen.add(key)

        role = EntityRole.LOCATION if etype in (EntityType.GPE, EntityType.LOC, EntityType.FAC) else EntityRole.SUBJECT

        entities.append(ExtractedEntity(
            text=span.text,                # the mention as written (after text cleaning)
            entity_type=etype,
            role=role,
            confidence=1.0,
            canonical_name=name,           # the clean name an entity created from it gets
        ))

    return entities


def extract_mentions(text: str, lang: str = "en") -> list[ExtractedEntity]:
    """Entity mentions of one text written in ``lang``: the NER entry point the pipeline and the entity
    benchmark share."""
    return extract_entities(text, lang)


def extract_event_triples(text: str) -> list[dict]:
    """Extract (ACTOR, ACTION, TARGET) triples via dependency parsing."""
    nlp = get_nlp()
    doc = nlp(text[:10000])
    triples = []

    for token in doc:
        if token.pos_ != "VERB":
            continue

        lemma = token.lemma_.lower()
        event_type = EVENT_VERB_MAP.get(lemma)
        if event_type is None:
            continue

        # Find subject and object
        subj = None
        obj = None
        for child in token.children:
            if child.dep_ in ("nsubj", "nsubjpass") and child.ent_type_:
                subj = child.text
            elif child.dep_ in ("dobj", "pobj") and child.ent_type_:
                obj = child.text

        if subj or obj:
            triples.append({
                "actor": subj,
                "action": lemma,
                "target": obj,
                "event_type": event_type,
            })

    return triples
