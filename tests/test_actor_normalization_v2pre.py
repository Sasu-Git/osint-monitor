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


# --- principal extraction, track 3 (evaluations/entities/principals-20261111/DIAGNOSIS.md, P-A) -----------------

class _Dev:
    def __init__(self, weights, headline):
        self.weights, self.headline_actors = weights, headline


def test_key_level_support_adds_one_name_of_a_split_actor():
    from osint_monitor.processors.principals import _key_level_principals
    norm = ActorNormalizer.load()
    dev = _Dev({"russia": {"actor": 1.0}, "kremlin": {"actor": 1.0}, "denmark": {"actor": 1.0}},
               {"russia", "kremlin", "denmark"})
    got = _key_level_principals({"russia", "kremlin", "denmark"}, set(), dev, 1.5, norm)
    assert got == {"russia"}                       # one actor, its own name; Denmark (one name, 1.0) stays out


def test_key_level_support_leaves_passing_and_single_name_actors_alone():
    from osint_monitor.processors.principals import _key_level_principals
    norm = ActorNormalizer.load()
    dev = _Dev({"united states": {"actor": 2.0}, "trump": {"actor": 1.0}, "iran": {"actor": 1.0}},
               {"united states", "trump", "iran"})
    assert _key_level_principals({"united states", "trump", "iran"}, {"united states"}, dev, 1.5, norm) == set()


def test_key_level_support_keeps_the_headline_gate():
    from osint_monitor.processors.principals import _key_level_principals
    norm = ActorNormalizer.load()
    dev = _Dev({"russia": {"actor": 1.0}, "kremlin": {"actor": 1.0}, "israel": {"actor": 2.0}}, {"israel"})
    assert _key_level_principals({"russia", "kremlin", "israel"}, {"israel"}, dev, 1.5, norm) == set()
