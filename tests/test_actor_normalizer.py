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
