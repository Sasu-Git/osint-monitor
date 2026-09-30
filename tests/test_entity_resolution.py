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
