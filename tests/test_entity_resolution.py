"""Entity resolution per the Core Entity Resolution Principle (evaluations/entities/): fuzzy matches never
create durable truth, canonical-name hygiene, multilingual NER safety, institutional hierarchy, actor roles
and role-based principal selection."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.core.database import Base, Entity
from osint_monitor.core.models import EntityType, ExtractedEntity
from osint_monitor.processors.entity_resolver import EntityResolver, identity_conflict, variant_key


@pytest.fixture
def session(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'r.db'}")
    Base.metadata.create_all(engine)
    s = sessionmaker(bind=engine)()
    yield s
    s.close()
    engine.dispose()


def add(session, name, etype, aliases=()):
    e = Entity(canonical_name=name, entity_type=etype, aliases=list(aliases))
    session.add(e)
    session.commit()
    return e


def resolve(session, text, etype="ORG", resolver=None):
    resolver = resolver or EntityResolver(session)
    return resolver.resolve(ExtractedEntity(text=text, entity_type=EntityType(etype))), resolver


# --- 1. fuzzy matches must not create durable truth ---------------------------------------------

@pytest.mark.parametrize("mention, candidate", [("American", "Mexican"), ("England", "Nagaland"), ("Canada", "Cada"),
                                                ("Nation", "NATO"), ("U.S. 6th Fleet", "U.S. 5th Fleet"),
                                                ("Germany", "the German"), ("European Nato", "the European Union"),
                                                ("Zou", "Zhou"), ("UNSCR", "UNHCR")])
def test_identity_critical_tokens_block_fuzzy_substitution(mention, candidate):
    assert identity_conflict(mention, candidate)


@pytest.mark.parametrize("mention, candidate", [("Houthi", "Houthis"), ("US Navy", "the U.S. Navy"),
                                                ("Donald Trump", "Donald J. Trump"), ("Teherán", "Teheran")])
def test_variants_with_strong_evidence_are_allowed(mention, candidate):
    assert identity_conflict(mention, candidate) is None


@pytest.mark.parametrize("mention, etype, existing, etype2", [("American", "NORP", "Mexican", "NORP"),
                                                             ("England", "GPE", "Nagaland", "GPE"),
                                                             ("Canada", "GPE", "Cada", "GPE"),
                                                             ("Nation", "ORG", "NATO", "ORG"),
                                                             ("U.S. 6th Fleet", "ORG", "U.S. 5th Fleet", "ORG")])
def test_spec_examples_resolve_to_a_new_entity_not_the_lookalike(session, mention, etype, existing, etype2):
    wrong = add(session, existing, etype2)
    entity, r = resolve(session, mention, etype)
    assert entity.id != wrong.id                                   # never the lookalike, by any method


def test_a_fuzzy_match_is_provisional_and_never_stored_as_an_alias(session):
    houthis = add(session, "Houthis", "ORG")
    entity, r = resolve(session, "Houthi", "ORG")
    assert entity.id == houthis.id and r.last_method == "fuzzy-provisional"
    session.refresh(houthis)
    assert houthis.aliases == []                                   # no durable alias


def test_learned_aliases_are_not_trusted_for_exact_matches(session):
    polluted = add(session, "Mexican", "NORP", aliases=["American"])   # an alias an old fuzzy match stored
    entity, r = resolve(session, "American", "NORP")
    assert entity.id != polluted.id
    variant = add(session, "the U.S. Navy", "ORG", aliases=["US Navy"])  # a surface variant stays trusted
    entity, r = resolve(session, "US Navy", "ORG")
    assert entity.id == variant.id and r.last_method == "exact"


def test_seeded_aliases_resolve_directly(session):
    from osint_monitor.core.config import load_entities_config
    seed = next(s for s in load_entities_config() if s.aliases)
    add(session, seed.canonical_name, seed.entity_type, seed.aliases)
    entity, r = resolve(session, seed.aliases[0], seed.entity_type)
    assert entity.canonical_name == seed.canonical_name and r.last_method in ("exact", "normalised")


def test_variant_key_folds_surface_noise_only():
    assert variant_key("the U.S. Navy’s") == variant_key("US Navy")
    assert variant_key("American") != variant_key("Mexican")


# --- 2. canonical-name / text normalisation ------------------------------------------------------

from osint_monitor.processors.text_normalize import clean_name, clean_text  # noqa: E402


@pytest.mark.parametrize("raw, clean", [("the U.S. Navy", "U.S. Navy"), ("Saudi Arabia’s", "Saudi Arabia"),
                                        ("Jonathan McKinsey's", "Jonathan McKinsey"), ("Hamas&#039;s", "Hamas"),
                                        ("The Hague", "The Hague"), ("U.S.", "U.S."), ("El Salvador", "El Salvador"),
                                        ("“State of the Force”", "State of the Force")])
def test_canonical_names_are_clean_identities(raw, clean):
    assert clean_name(raw) == clean


def test_ner_text_is_decoded_and_unglued_but_otherwise_as_written():
    t = clean_text("Macron said on Thursday.Macron also said strikesRussian drones hit Hamas&#039;s ⁠base — McKinsey")
    assert "Thursday. Macron" in t and "strikes Russian" in t and "Hamas's base" in t
    assert "McKinsey" in t and "—" in t                           # names and dashes left alone


def test_new_entities_get_the_clean_name_and_keep_the_raw_mention(session):
    entity, r = resolve(session, "the U.S. Navy’s", "ORG")
    assert entity.canonical_name == "U.S. Navy" and r.last_method == "new"


# --- 3. multilingual NER routing / unsupported-language safety -------------------------------------

from osint_monitor.processors import nlp as NLP  # noqa: E402
from osint_monitor.processors.language import detect_latin_language, item_language  # noqa: E402


def _has(model):
    import spacy.util
    return model in spacy.util.get_installed_models()


@pytest.mark.skipif(not _has("es_core_news_md"), reason="Spanish model not installed")
def test_spanish_text_is_parsed_by_the_spanish_model_and_clauses_never_become_entities():
    got = [(m.text, m.entity_type.value) for m in NLP.extract_mentions(
        "Por la guerra y la incertidumbre económica, la moneda de Irán se hunde en un mínimo histórico", "es")]
    assert ("Irán", "GPE") in got
    assert not any(len(t.split()) > 3 for t, _ in got)            # no "la moneda de Irán se hunde en un"
    got = [(m.text, m.entity_type.value) for m in NLP.extract_mentions(
        "Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta", "es")]
    assert got == [("Irán", "GPE"), ("EEUU", "GPE")]


@pytest.mark.skipif(not _has("it_core_news_md"), reason="Italian model not installed")
def test_italian_names_are_typed_by_the_italian_model():
    got = {(m.text, m.entity_type.value) for m in NLP.extract_mentions("Trump, 'Usa valutano comitato di 10 persone'", "it")}
    assert {("Trump", "PERSON"), ("Usa", "GPE")} <= got


def test_a_language_without_a_trusted_model_yields_no_entities(monkeypatch):
    monkeypatch.setitem(NLP._language_instances, "es", None)
    assert NLP.extract_mentions("Irán confirma que recibió la respuesta de EEUU", "es") == []
    assert NLP.extract_mentions("Текст на русском", "ru") == []


def test_clause_like_spans_fail_validation_in_english_too():
    doc = NLP.get_nlp()("What Will Hegseth’s “State of the Force” Reprise Reveal? Israeli forces kill Izz al-Din al-Beik")
    names = [NLP.mention_span(e).text for e in doc.ents if NLP.mention_span(e) is not None]
    assert "Hegseth" in names and "Izz al-Din al-Beik" in names and "Will Hegseth" not in names


def test_item_language_prefers_the_feed_configuration_then_the_text():
    assert item_language("El País Internacional", "anything") == "es"
    assert item_language("ANSA Mondo", "anything") == "it"
    assert item_language(None, "Il governo ha approvato il decreto per le scuole della città") == "it"
    assert item_language(None, "El gobierno de España aprobó las medidas para los inquilinos") == "es"
    assert detect_latin_language("The government approved the measures for the tenants") == "en"
