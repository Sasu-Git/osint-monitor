"""Principal actors: participants vs incidental mentions, and the situation joins that depend on them."""

import pytest

from osint_monitor.core.config import load_situations_config
from osint_monitor.core.database import Entity, Event, EventEntity, EventItem, RawItem, Source
from osint_monitor.core.models import DevelopmentSignature, SituationProfile
from osint_monitor.processors.actors import ActorNormalizer
from osint_monitor.processors.principals import item_participants, mark_principal_actors, principal_keys
from osint_monitor.processors.situations import ActorCanonicalizer, SituationGrouper
from tests import live_fixtures as live


@pytest.fixture(scope="module")
def nlp():
    from osint_monitor.processors.nlp import SpacyModelMissing, get_nlp
    try:
        return get_nlp()
    except SpacyModelMissing:
        pytest.skip("needs the spaCy model: python -m spacy download en_core_web_lg")


@pytest.fixture(scope="module")
def config():
    return load_situations_config()


@pytest.fixture(scope="module")
def seeds(config):
    return [SituationProfile(slug=s.slug, title=s.title, region=s.region, primary_actors=s.primary_actors,
                             keywords=s.keywords) for s in config.situations]


def countries(config, keys):
    actors = ActorCanonicalizer(normalizer=ActorNormalizer.load())
    return actors.keys(keys)


# --- one headline ------------------------------------------------------------------------

@pytest.mark.parametrize("title, principal, incidental", [
    ("Xi Jinping met the US president to discuss Taiwan and NATO", {"xi jinping", "united states"}, {"taiwan", "nato"}),
    ("EU sanctions Russia over Ukraine", {"european union", "russia"}, {"ukraine"}),
    ("EU imposes new sanctions on Russia over Ukraine war", {"european union", "russia"}, {"ukraine"}),
    ("US and Iran resume nuclear talks in Muscat", {"united states", "iran"}, {"muscat"}),
    ("Israel strikes Iran as Hezbollah fires rockets from Lebanon", {"israel", "iran"}, {"lebanon"}),
])
def test_participants_vs_incidental_mentions(nlp, title, principal, incidental):
    found = item_participants(nlp, title)
    assert principal <= found
    assert not incidental & found


def test_topic_only_headline_has_no_participants(nlp):
    assert item_participants(nlp, "Gulf nations keep oil flowing amid Iran war, but it's getting costly") == set()


def test_lead_sentence_used_when_headline_names_no_actor(nlp):
    assert "russia" in item_participants(nlp, "Overnight drone wave hits energy grid",
                                         "Russia launched a wave of drones at Kyiv overnight.")


def test_aliases_survive_canonicalisation(nlp, config):
    keys = item_participants(nlp, "Iranian and U.S. negotiators meet in Muscat")
    assert countries(config, keys) >= {"iran", "united states"}


# --- across a cluster ----------------------------------------------------------------------

def test_one_headline_listing_a_topic_does_not_make_it_principal(nlp, config):
    keys = principal_keys(nlp, live.TRUMP_XI_SUMMIT)
    assert countries(config, keys) >= {"united states", "china"}
    assert "iran" not in countries(config, keys)


# --- the live false joins ------------------------------------------------------------------

def signature(nlp, items, title):
    keys = principal_keys(nlp, items)
    return DevelopmentSignature(title=title, actors=sorted(keys), actors_are_principal=bool(keys))


@pytest.mark.parametrize("items, title, wrong", [
    (live.TRUMP_XI_SUMMIT, "Trump-Xi summit live: Trade, AI, Iran and Taiwan top US-China talks", "us-iran"),
    (live.NAVY_CYBER, "Navy wants more offensive, 'expeditionary' cyber capabilities", "russia-ukraine-war"),
    (live.SYRIA_BASES, "Syria looks to end foreign military presence, have sovereignty over all bases", "us-iran"),
], ids=["trump-xi-not-us-iran", "navy-cyber-not-russia-ukraine", "syria-not-us-iran"])
def test_live_false_joins_are_prevented(nlp, config, seeds, items, title, wrong):
    assert SituationGrouper(config).assign(signature(nlp, items, title), seeds).slug != wrong


@pytest.mark.parametrize("items, title, right", [
    (live.US_IRAN_TALKS, "US and Iran resume nuclear talks in Muscat", "us-iran"),
    (live.RUSSIA_UKRAINE_STRIKES, "Russian drones strike Kyiv energy infrastructure overnight", "russia-ukraine-war"),
])
def test_correct_joins_still_happen(nlp, config, seeds, items, title, right):
    assert SituationGrouper(config).assign(signature(nlp, items, title), seeds).slug == right


def test_mention_only_signature_is_matched_strictly(config, seeds):
    # every seeded actor must be present and the evidence must be strong
    partial = DevelopmentSignature(title="Defense roundup", actors=["Russia", "Navy", "CIA"], actors_are_principal=False)
    assert SituationGrouper(config).assign(partial, seeds).slug is None


# --- persistence -----------------------------------------------------------------------------

def test_mark_principal_actors_flags_participants_only(session, nlp):
    src = Source(name="Wire", type="rss", url="u")
    session.add(src)
    session.flush()
    ents = {n: Entity(canonical_name=n, entity_type="GPE") for n in ["European Union", "Russia", "Ukraine"]}
    session.add_all(ents.values())
    event = Event(summary="EU sanctions Russia over Ukraine")
    session.add(event)
    session.flush()
    for n, title in enumerate(["EU sanctions Russia over Ukraine", "EU adopts new sanctions on Russia over Ukraine war"]):
        item = RawItem(source_id=src.id, title=title, content="", content_hash=f"h{n}")
        session.add(item)
        session.flush()
        session.add(EventItem(event_id=event.id, item_id=item.id))
    session.add_all([EventEntity(event_id=event.id, entity_id=e.id, role="LOCATION") for e in ents.values()])
    session.commit()

    stats = mark_principal_actors(session)
    flags = {ee.entity.canonical_name: ee.is_principal for ee in session.query(EventEntity).filter_by(event_id=event.id)}
    assert flags == {"European Union": True, "Russia": True, "Ukraine": False}
    assert stats["with_principals"] == 1
    mark_principal_actors(session)                                     # idempotent
    assert session.query(EventEntity).filter_by(event_id=event.id).count() == 3


# --- normalisation and cluster support (2026-09-24 eval regressions) -----------------------

@pytest.fixture(scope="module")
def actors():
    return ActorNormalizer.load()


def test_small_summit_cluster_has_both_states_and_no_ai(nlp, actors):
    # was {AI, China}: each outlet named Trump differently, so no single spelling reached support
    assert principal_keys(nlp, live.TRUMP_XI_SUMMIT_SMALL, actors) == {"united states", "china"}


def test_topic_listed_beside_a_summit_is_not_principal(nlp, actors):
    keys = principal_keys(nlp, live.TRUMP_XI_SUMMIT_SMALL[:1], actors)
    assert {"united states", "china"} <= keys
    assert not keys & {"iran", "taiwan"}


def test_demonym_variants_count_as_one_actor(nlp, actors):
    assert "australia" in principal_keys(nlp, live.F35_PARTS, actors)
    assert not {"aussie", "australian"} & principal_keys(nlp, live.F35_PARTS, actors)


def test_possessive_is_not_a_separate_actor(nlp, actors):
    keys = principal_keys(nlp, live.AIR_FORCE_CASI, actors)
    assert "air force" in keys and not any("’" in k or "'" in k for k in keys)


@pytest.mark.parametrize("title, principal", [
    ("Trump-Xi summit opens in Washington", {"united states", "china"}),
    ("Xi-Trump summit day 1 highlights: Rubio defends visit", {"united states", "china"}),
    ("Trump meets Xi at the White House", {"united states", "china"}),
    ("Talks between Trump and Xi end without deal", {"united states", "china"}),
    ("Chinese CEOs await invites to Trump’s state dinner for Xi Jinping", {"united states", "china"}),
    ("Xi is the first Chinese leader to address Congress", {"china"}),
    ("EU sanctions Russia over Ukraine", {"european union", "russia"}),
])
def test_grammatical_forms_of_participation(nlp, actors, title, principal):
    assert principal <= principal_keys(nlp, [(title, "")], actors)


@pytest.mark.parametrize("title, topic", [
    ("Trump and Xi discuss Taiwan in Washington", "taiwan"),
    ("Talks between Trump and Xi end without deal on Taiwan", "taiwan"),
    ("Trump-Xi summit live: Trade, AI, Iran and Taiwan top US-China talks", "iran"),
    ("EU sanctions Russia over Ukraine", "ukraine"),
])
def test_subject_of_discussion_is_not_principal(nlp, actors, title, topic):
    assert topic not in principal_keys(nlp, [(title, "")], actors)


def test_a_single_lead_mention_does_not_make_a_principal_in_a_larger_cluster(nlp, actors):
    items = [("US and Iran resume nuclear talks in Muscat", "Oman hosted the talks."),
             ("Iran and US negotiators meet in Muscat", ""),
             ("US, Iran hold fresh round of talks", "Qatar also sent an envoy.")]
    keys = principal_keys(nlp, items, actors)
    assert keys == {"united states", "iran"}


def test_person_principal_flags_the_linked_person_entity(session, actors):
    src = Source(name="Wire", type="rss", url="u")
    session.add(src)
    session.flush()
    ents = {n: Entity(canonical_name=n, entity_type=t) for n, t in
            [("Donald Trump", "PERSON"), ("Xi Jinping", "PERSON"), ("Pentagon", "ORG"), ("Taiwan", "GPE")]}
    ents["Donald Trump"].aliases = ["Trump"]
    ents["Xi Jinping"].aliases = ["Xi"]
    session.add_all(ents.values())
    event = Event(summary="Trump meets Xi")
    session.add(event)
    session.flush()
    for n, title in enumerate(["Trump meets Xi at the White House", "Talks between Trump and Xi end without deal on Taiwan"]):
        item = RawItem(source_id=src.id, title=title, content="The Pentagon declined to comment.", content_hash=f"t{n}")
        session.add(item)
        session.flush()
        session.add(EventItem(event_id=event.id, item_id=item.id))
    session.add_all([EventEntity(event_id=event.id, entity_id=e.id, role="MENTION") for e in ents.values()])
    session.commit()

    mark_principal_actors(session, normalizer=actors)
    flags = {ee.entity.canonical_name: ee.is_principal for ee in session.query(EventEntity).filter_by(event_id=event.id)}
    # Pentagon also stands for the United States but was never a participant, so it stays a mention
    assert flags == {"Donald Trump": True, "Xi Jinping": True, "Pentagon": False, "Taiwan": False}


def test_entity_with_a_misleading_alias_is_not_flagged(session, actors):
    # live 09-24: the resolver merged "America" into an "Americas" entity, which then became principal
    src = Source(name="Wire", type="rss", url="u")
    session.add(src)
    session.flush()
    us = Entity(canonical_name="America", entity_type="GPE")
    americas = Entity(canonical_name="Americas", entity_type="LOC", aliases=["America"])
    greenland = Entity(canonical_name="Greenland", entity_type="GPE")
    session.add_all([us, americas, greenland])
    event = Event(summary="US signs Greenland pact")
    session.add(event)
    session.flush()
    for n, title in enumerate(["Greenland welcomes US military pact", "America signs Greenland security pact"]):
        item = RawItem(source_id=src.id, title=title, content="", content_hash=f"g{n}")
        session.add(item)
        session.flush()
        session.add(EventItem(event_id=event.id, item_id=item.id))
    session.add_all([EventEntity(event_id=event.id, entity_id=e.id, role="MENTION") for e in (us, americas, greenland)])
    session.commit()

    mark_principal_actors(session, normalizer=actors)
    flags = {ee.entity.canonical_name: ee.is_principal for ee in session.query(EventEntity).filter_by(event_id=event.id)}
    assert flags == {"America": True, "Americas": False, "Greenland": True}


# --- places, non-actors and context organisations (2026-09 live windows) -----------------------

def keys(nlp, *items):
    return principal_keys(nlp, [(t, lead) for t, lead in items], ActorNormalizer.load())


def test_city_as_destination_is_not_a_principal(nlp):
    assert keys(nlp, ("UAE confirms Netanyahu visit to Abu Dhabi", "")) == {"united arab emirates", "israel"}


def test_state_as_location_modifier_is_not_a_principal(nlp):
    assert "iowa" not in keys(nlp, ("Trump announcing new Iowa steel plant the White House says will be biggest in US", ""))


def test_city_in_a_list_of_places_is_not_a_principal(nlp):
    k = keys(nlp, ("US to grant sanctions waiver for flights between Iran and Iraq’s Najaf, source says", ""))
    assert "najaf" not in k and {"united states", "iran"} <= k


def test_capitalised_common_noun_is_not_a_principal(nlp):
    assert "child" not in keys(nlp, ("Child among three killed off French coast in Channel crossing attempt", ""))


def test_abstract_concept_is_not_a_principal(nlp):
    k = keys(nlp, ("French far-right’s Bardella denies alleged anti-Semitism comments, files defamation lawsuit", ""))
    assert "anti-semitism" not in k and "bardella" in k


def test_named_storm_and_its_path_are_not_principals(nlp):
    k = keys(nlp, ("Tropical Storm Lala expected to strengthen as it nears Hawaii", ""))
    assert not k & {"storm lala", "lala", "hawaii"}


def test_reporting_outlet_and_employer_are_not_principals(nlp):
    assert "bbc" not in keys(nlp, ("Hunter Biden tells BBC his pardon was 'not good' for US or his father", ""))
    assert "new york times" not in keys(nlp, ("New York Times executive fatally shot by elderly in-laws, police say", ""))


def test_capital_as_subject_is_the_state_it_speaks_for(nlp):
    assert keys(nlp, ("Seoul suspects North Korean mines behind DMZ blast", "")) >= {"south korea", "north korea"}
    assert "seoul" not in keys(nlp, ("Seoul suspects North Korean mines behind DMZ blast", ""))


def test_role_prefix_is_dropped_from_a_named_official(nlp):
    assert "fm araghchi" not in keys(nlp, ("‘Iran ready for doomsday war’, FM Araghchi says", ""))


# genuine principals the filters must keep

def test_governments_and_named_officials_stay_principals(nlp):
    assert keys(nlp, ("Argentina threatens legal action against UK over Falkland Islands oil exploration", "")) \
        >= {"argentina", "united kingdom"}
    assert "carney" in keys(nlp, ("Carney calls Trump's fresh tariffs a 'miscalculation' after trade talks collapse", ""))


def test_military_organisations_companies_and_international_bodies_stay_principals(nlp):
    assert "taliban" in keys(nlp, ("Four civilians killed in Pakistani strikes in Afghanistan, Taliban says", ""))
    assert "meta" in keys(nlp, ("Court orders Meta to pay $567m over harm to youths", ""))
    assert "nato" in keys(nlp, ("NATO deploys extra jets to Poland after airspace violation", ""))


def test_regional_government_acting_stays_a_principal(nlp):
    assert "british columbia" in keys(nlp, ("British Columbia issues evacuation orders ahead of fast-moving wildfire", ""))
