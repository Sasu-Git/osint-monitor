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
    variant = add(session, "the Milrem Robotics", "ORG", aliases=["Milrem Robotics’"])  # a surface variant stays trusted
    entity, r = resolve(session, "Milrem Robotics’", "ORG")
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
    entity, r = resolve(session, "the Milrem Robotics’s", "ORG")
    assert entity.canonical_name == "Milrem Robotics" and r.last_method == "new"


# --- 3. multilingual NER routing / unsupported-language safety -------------------------------------

from osint_monitor.processors import nlp as NLP  # noqa: E402
from osint_monitor.processors.language import detect_latin_language, item_language  # noqa: E402


def _has(model):
    import spacy.util
    return model in spacy.util.get_installed_models()


def test_a_missing_language_model_is_reported_not_silent(monkeypatch):
    import spacy.util
    monkeypatch.setattr(spacy.util, "is_package", lambda name: name != "it_core_news_md")
    status = NLP.ner_status()
    assert status["it"] == ("it_core_news_md", False) and status["es"][1] and status["en"][1]
    lines = NLP.format_ner_status(status)
    assert any(line.startswith("Italian NER: MISSING (it_core_news_md)") for line in lines)
    assert any(line.startswith("Spanish NER: available") for line in lines)


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


# --- 4. institutional hierarchy and canonical institution mapping --------------------------------

from osint_monitor.processors.institutions import item_qualifiers, registry  # noqa: E402


def test_institutions_resolve_to_the_lowest_acting_body_with_parents():
    reg = registry()
    for name, canonical in [("Pentagon", "US Department of Defense"), ("Department of War", "US Department of Defense"),
                            ("US Navy", "U.S. Navy"), ("UNGA 81", "UN General Assembly"), ("Casa Bianca", "White House"),
                            ("CBP", "U.S. Customs and Border Protection"), ("Nato", "NATO")]:
        assert reg.lookup(name).canonical == canonical
    assert reg.parents("U.S. Navy") == ["US Department of Defense", "United States"]
    assert reg.parents("UN Security Council") == ["United Nations"]
    assert reg.lookup("un") is None and reg.lookup("who") is None     # acronyms are case-sensitive


def test_generic_labels_resolve_only_from_context(session):
    r = EntityResolver(session)
    navy = r.resolve(ExtractedEntity(text="Navy", entity_type=EntityType.ORG),
                     item_qualifiers([("Boeing", "ORG"), ("American", "NORP")]))
    assert navy.canonical_name == "U.S. Navy" and r.last_method == "registry-context"
    council = r.resolve(ExtractedEntity(text="Council", entity_type=EntityType.ORG),
                        item_qualifiers([("Council", "ORG")], "Council of the EU Press"))
    assert council.canonical_name == "Council of the European Union"
    ambiguous = r.resolve(ExtractedEntity(text="Navy", entity_type=EntityType.ORG),
                          item_qualifiers([("US", "GPE"), ("UK", "GPE")]))
    assert ambiguous.canonical_name == "Navy" and "generic label" in r.last_evidence


def test_capitals_keep_their_identity_and_act_for_their_state(session):
    from osint_monitor.processors.actors import ActorNormalizer
    add(session, "Ukraine", "GPE", ["Ukrainian"])
    entity, _ = resolve(session, "Kyiv", "GPE")
    assert entity.canonical_name == "Kyiv"                       # identity: the city
    n = ActorNormalizer.load()
    assert n.surface("Kyiv") == "kyiv" and n.key("Kyiv") == "ukraine"   # role: acts for Ukraine
    assert n.key("European Commission") == "european union" and n.surface("European Commission") == "european commission"


# --- 5. actor roles --------------------------------------------------------------------------------

from osint_monitor.processors.actor_roles import development_roles  # noqa: E402


def roles_of(title, lead="", lang="en", source=None):
    return development_roles([{"title": title, "lead": lead, "lang": lang, "source": source}]).roles


@pytest.mark.parametrize("title, expected", [
    ("NATO deploys additional forces to Poland", {"nato": "actor", "poland": "affected"}),
    ("Poland asks NATO for more forces", {"poland": "actor", "nato": "target"}),
    ("WTO rules against US tariff measure", {"world trade organization": "actor", "united states": "target"}),
    ("G7 agrees new sanctions on Russia", {"g7": "actor", "russia": "target"}),
    ("Italy blocks G7 agreement", {"italy": "actor", "g7": "institutional_context"}),
    ("UN Security Council adopts sanctions", {"un security council": "actor"}),
])
def test_spec_role_examples(title, expected):
    got = roles_of(title)
    for holder, role in expected.items():
        assert got.get(holder) == role, (title, got)


def test_modifiers_of_actions_act_and_places_do_not():
    got = roles_of("Israeli forces kill Hamas commander in Gaza attack")
    assert got["israel"] == "actor" and got["hamas"] == "target" and got["gaza"] == "location"
    got = roles_of("Houthi attacks on Saudi Arabia test regional pact")
    assert (got.get("houthi") or got.get("houthis")) == "actor" and got["saudi arabia"] == "target"


def test_a_capital_acting_stands_for_its_state():
    got = roles_of("Tallinn accuses Moscow of responsibility for the fire")
    assert got.get("estonia") == "actor" and got.get("russia") == "target"


def test_the_parties_to_a_joint_action_are_its_co_agents():
    got = roles_of("USS Klakring sent to the bottom of the Atlantic in joint US-UK SINKEX")
    assert got["united states"] == "actor" and got["united kingdom"] == "actor"
    got = roles_of("Drone strike on joint US-Iraqi base in Erbil wounds soldiers")   # a target stays a target
    assert got["united states"] == "target" and got["iraq"] == "target"


def test_media_outlets_report_they_do_not_act():
    got = roles_of("Inside Yemen's front-line city", "The BBC travels to the front line with pro-government soldiers.")
    assert got.get("bbc") == "subject"


@pytest.mark.skipif(not _has("es_core_news_md"), reason="Spanish model not installed")
def test_spanish_roles_from_universal_dependencies():
    got = roles_of("Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta", lang="es")
    assert got.get("iran") == "actor" and got.get("united states") == "actor"


# --- 6. principal actors from roles ----------------------------------------------------------------

from osint_monitor.processors.principals import development_actors  # noqa: E402


def principals_of(*titles, lead="", lang="en", source=None):
    return development_actors([{"title": t, "lead": lead, "lang": lang, "source": source} for t in titles]).principals


@pytest.mark.parametrize("titles, expected", [
    (["Israel strikes Hamas commander in Gaza"], {"israel"}),                      # Gaza: location; Hamas: target
    (["'Backpack' declared Alaska's Fat Bear Week winner"], set()),                # event name is no actor
    (["Accreditation and Approval of Intertek USA, Inc. (Chelsea, MA), as a Commercial Gauger"], set()),
    (["US and France push G7 sanctions proposal"], {"united states", "france"}),
    (["US vetoes Security Council resolution"], {"united states"}),
    (["Trump meets Xi at the White House"], {"trump", "xi"}),                      # co-actors of a meeting
    (["US, UK test SM-6, other missiles on SINKEX target frigate",                 # state-level co-principals
      "USS Klakring sent to the bottom of the Atlantic in joint US-UK SINKEX"], {"united states", "united kingdom"}),
])
def test_principal_status_comes_from_the_role(titles, expected):
    assert principals_of(*titles) == expected


def test_lead_sentences_add_no_principal_of_their_own():
    got = principals_of("Trump meets Xi at the White House", lead="The Pentagon declined to comment.")
    assert "us department of defense" not in got and {"trump", "xi"} <= got


# --- 7. round-up / multi-story safeguards ------------------------------------------------------------

from osint_monitor.processors.actor_roles import is_roundup  # noqa: E402


@pytest.mark.parametrize("title, roundup", [
    ("World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations", True),
    ("Live: Several people killed as Russia launches new round of strikes on Kyiv", True),
    ("Ukraine war latest: Record Russian military budget for 2027", True),
    ("Malaysia sends Rohingya back to Myanmar despite safety warnings", False),
])
def test_roundups_are_detected(title, roundup):
    assert is_roundup(title) is roundup


def test_a_roundup_contributes_no_actor_and_the_programme_is_never_one():
    got = development_actors([
        {"title": "Malaysia repatriates Myanmar migrants despite UN warnings", "lead": "", "lang": "en"},
        {"title": "World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, Gaza update",
         "lead": "The UN chief on Tuesday strongly condemned an airstrike in Myanmar.", "lang": "en"}]).principals
    assert got == {"malaysia"}
