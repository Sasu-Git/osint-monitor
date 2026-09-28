"""Region assignment: headline-led, whole-word, not hijacked by incidental mentions."""

from types import SimpleNamespace

import pytest

from osint_monitor.core.config import load_sources_config
from osint_monitor.processors.clustering import _assign_region


@pytest.fixture(scope="module")
def regions():
    return load_sources_config().regions


def items(*pairs):
    return [SimpleNamespace(title=t, content=c) for t, c in pairs]


def test_ordinary_words_do_not_trigger_acronym_keywords(regions):
    # 'plan', 'plans', 'place' used to match the China keywords PLA / PLAN
    assert _assign_region(items(("Army awards Palantir $48M to modernize ammo plan",
                                 "The plan will take place over two years, officials explained.")), regions) is None


def test_incidental_china_mention_does_not_set_the_region(regions):
    assert _assign_region(items(
        ("US and Iran resume nuclear talks in Muscat", "Negotiators met in Muscat; China welcomed the talks."),
        ("Iran and US hold new round of talks in Oman", "Tehran said the talks were constructive."),
    ), regions) == "iran"


def test_headlines_outweigh_body_mentions(regions):
    assert _assign_region(items(
        ("China's next carrier could be its longest", "Analysts compare it with Russia's and Ukraine's fleets."),
    ), regions) == "china"


def test_evenly_mixed_reporting_stays_unlabelled(regions):
    assert _assign_region(items(("Iran and China sign oil deal", ""), ("Beijing and Tehran expand trade", "")), regions) is None


def test_single_body_mention_is_not_enough(regions):
    assert _assign_region(items(("Earthquake shakes northern Chile", "No damage reported. Iran sent condolences.")),
                          regions) is None
