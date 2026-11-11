"""Situation-v2 normalisation prerequisite (evaluations/actor-hygiene/v2-prereq-20261111/DEFECTS.md)."""
import pytest

from osint_monitor.processors.actors import ActorNormalizer
from osint_monitor.processors.situations.canonical import ActorCanonicalizer


@pytest.fixture(scope="module")
def canon():
    return ActorCanonicalizer(normalizer=ActorNormalizer.load())


@pytest.mark.parametrize("names,expected", [
    (["Javier Milei", "Milei"], {"javier milei"}),                       # A1
    (["Elon Musk's", "Musk"], {"elon musk"}),                            # A2
    (["Christa Pike's", "Pike"], {"christa pike"}),                      # A3
    (["Maria Corina Machado", "Machado"], {"maria corina machado"}),     # A4
    (["Nayib Bukele", "Bukele", "El Salvador"], {"el salvador"}),        # A5 + B2
    (["Emmanuel Macron", "Macron", "France"], {"france"}),               # A6 + B1
    (["America", "Vance", "J.D. Vance"], {"united states"}),            # A7 + B3
    (["DONALD J. TRUMP", "Trump"], {"united states"}),                   # A8 + B4
    (["Democrat", "United States"], {"united states"}),                  # C1
    (["China", "Chinas Long March"], {"china"}),                         # C3
])
def test_defect_sets_collapse(canon, names, expected):
    assert set(canon.keys(names)) == expected


@pytest.mark.parametrize("names,expected", [
    (["Jair Bolsonaro", "Flávio Bolsonaro", "Bolsonaro"], {"jair bolsonaro", "flávio bolsonaro"}),  # no merge
    (["Musk", "Germany"], {"musk", "germany"}),                          # a lone surname is never aliased
    (["Guinea", "Equatorial Guinea"], {"guinea", "equatorial guinea"}),  # places never collapse
    (["Sudan", "South Sudan"], {"sudan", "south sudan"}),
    (["Washington", "George Washington"], {"united states", "george washington"}),
])
def test_guards(canon, names, expected):
    assert set(canon.keys(names)) == expected


@pytest.mark.parametrize("word", ["English", "Democrat", "Democrats", "Democratic", "Republicans", "Democratici",
                                  "Long March", "Chinas Long March"])
def test_non_actor_words(word):
    assert ActorNormalizer.load().key(word) is None


def test_topic_keys_do_not_collapse_variants():
    """Development identity uses ActorNormalizer.keys, which is unchanged: no set-level collapse there."""
    assert ActorNormalizer.load().keys(["Javier Milei", "Milei"]) == frozenset({"javier milei", "milei"})
