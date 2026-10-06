"""Actor normalisation: one canonical name per actor, whatever the spelling in the headline."""

import pytest

from osint_monitor.core.config import ActorsConfig
from osint_monitor.processors.actors import ActorNormalizer, clean
from osint_monitor.processors.situations import ActorCanonicalizer


@pytest.fixture(scope="module")
def actors():
    return ActorNormalizer.load()


@pytest.mark.parametrize("raw, expected", [
    ("Air Force’s", "Air Force"),
    ("China's", "China"),
    ("White House '", "White House"),
    ("Trump-", "Trump"),
    ("“Hamas”", "Hamas"),
])
def test_surface_cleanup(raw, expected):
    assert clean(raw) == expected


@pytest.mark.parametrize("name", ["AI", "A.I.", "Artificial Intelligence", "AI’s"])
def test_ai_is_never_an_actor(actors, name):
    assert actors.key(name) is None


@pytest.mark.parametrize("name", ["Aussie", "Australian", "Australians", "Australia’s", "Australia"])
def test_demonyms_and_variants_collapse_to_the_country(actors, name):
    assert actors.key(name) == "australia"


@pytest.mark.parametrize("name, state", [
    ("Trump", "united states"), ("White House", "united states"), ("US", "united states"),
    ("U.S.", "united states"), ("Xi Jinping", "china"), ("Chinese", "china"), ("Kremlin", "russia"),
    ("EU", "european union"), ("British", "united kingdom"), ("Russians", "russia"),
])
def test_people_and_bodies_map_to_the_state_they_act_for(actors, name, state):
    assert actors.key(name) == state


def test_surface_keeps_the_person_key_maps_to_the_state(actors):
    assert actors.surface("Trump’s") == "trump"
    assert actors.key("Trump’s") == "united states"


def test_a_state_less_military_branch_stays_an_organisation(actors):
    assert actors.key("Air Force’s") == "air force"
    assert actors.key("US Air Force") == "united states"


def test_situation_keys_use_the_same_normalisation(actors):
    canon = ActorCanonicalizer(normalizer=actors)
    assert canon.keys(["Aussie", "Australian", "AI", "Xi"]) == {"australia", "china"}


def test_situations_yaml_entries_still_extend_the_actor_config():
    extended = ActorNormalizer(ActorsConfig(), extra_aliases={"Tatmadaw": "Myanmar"},
                               extra_represents={"Min Aung Hlaing": "Myanmar"})
    assert extended.key("Tatmadaw") == extended.key("Min Aung Hlaing") == "myanmar"


# --- Spanish / Italian names (post-soak fix 1: "Estados Unidos" founded a United States - United States Situation) ---

@pytest.mark.parametrize("name, state", [
    ("Estados Unidos", "united states"), ("EE.UU.", "united states"), ("Stati Uniti", "united states"),
    ("estadounidense", "united states"), ("statunitensi", "united states"), ("Casa Blanca", "united states"),
    ("Rusia", "russia"), ("rusos", "russia"), ("russi", "russia"), ("Moscú", "russia"), ("Cremlino", "russia"),
    ("Irán", "iran"), ("iraní", "iran"), ("israelí", "israel"), ("israeliani", "israel"),
    ("Cina", "china"), ("cinesi", "china"), ("Pechino", "china"), ("Turquía", "turkey"), ("Regno Unito", "united kingdom"),
    ("Ucrania", "ukraine"), ("ucraini", "ukraine"), ("OTAN", "nato"), ("Unión Europea", "european union"),
])
def test_spanish_and_italian_names_reach_the_english_canonical_actor(actors, name, state):
    assert actors.key(name) == state


def test_one_country_in_two_languages_is_one_actor(actors):
    assert actors.keys(["Estados Unidos", "United States", "EE.UU.", "US"]) == frozenset({"united states"})


def test_place_names_do_not_override_an_existing_actor_name(actors):
    assert actors.key("Turkey") == "turkey"           # the gazetteer says "turkiye"; the actor name wins
    assert actors.key("Kyiv") == "ukraine" and actors.key("Washington") == "united states"


def test_an_ambiguous_family_name_is_not_an_actor_but_full_names_are(actors):
    assert actors.key("Bolsonaro") is None
    assert actors.keys(["Bolsonaro", "Flávio Bolsonaro", "Jair Bolsonaro"]) == frozenset(
        {"flávio bolsonaro", "jair bolsonaro"})
