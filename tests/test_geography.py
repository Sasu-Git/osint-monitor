"""Geographic compatibility: containment is compatible, different places are not."""

import pytest

from osint_monitor.processors.geography import Gazetteer, clean


@pytest.fixture(scope="module")
def geo():
    return Gazetteer.load()


@pytest.mark.parametrize("a, b", [
    ("Northern Cyprus", "Cyprus"),
    ("California", "United States"),
    ("Bavaria", "Germany"),
    ("Gaza City", "Gaza"),
    ("US Northeast", "New York"),          # a region and one of its states
    ("New York City", "United States"),    # through the state
    ("eastern Ukraine", "Ukraine"),
    ("Britain", "London"),                 # alias, then containment
    ("DR Congo", "Kinshasa"),
])
def test_contained_places_are_compatible(geo, a, b):
    assert geo.same_or_contains(a, b) and geo.same_or_contains(b, a)


@pytest.mark.parametrize("a, b", [
    ("Nepal", "Japan"),
    ("Kyiv", "Khartoum"),
    ("Thailand", "Pakistan"),
    ("Kyiv", "Odesa"),                     # both in Ukraine, still different places
    ("New York", "Virginia"),
    ("South Africa", "Africa"),            # a country name is not a directional "part of"
])
def test_different_places_are_not_compatible(geo, a, b):
    assert not geo.same_or_contains(a, b)


def test_supra_national_regions_only_when_asked():
    assert not Gazetteer.load().same_or_contains("Middle East", "Iran")
    assert Gazetteer.load(use_regions=True).same_or_contains("Middle East", "Iran")


def test_set_compatibility_needs_one_compatible_pair(geo):
    assert geo.compatible({"kharkiv", "russia"}, {"ukraine"})
    assert not geo.compatible({"guyana"}, {"mauritania", "africa"})


def test_names_are_cleaned_before_lookup():
    assert clean("Hong Kong’s") == "hong kong"
    assert clean("Mali&#039;s") == "mali"
    assert clean("the Netherlands") == "netherlands"
