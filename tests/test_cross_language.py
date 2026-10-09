"""Cross-language acceptance guard (processors/cross_language.py; evaluations/identity/xlang-guard-tuning-plan.md).

The guard components G1-G4 are off by default; with the defaults the stage behaves as it did before they existed.
"""
import numpy as np
import pytest

from osint_monitor.core.config import CrossLanguageConfig
from osint_monitor.processors.cross_language import Guard, Unit, XLink, broad_terms, judge, merge_units, propose


class Geo:
    """Minimal gazetteer: a place is the same as itself; ``inside`` maps a place to the region containing it."""
    inside = {"irkutsk": "siberia", "shelekhov": "siberia"}

    def same_or_contains(self, a, b):
        return a == b or self.inside.get(a) == b or self.inside.get(b) == a


def unit(items, lang, anchors=(), places=(), numbers=(), vector=None):
    return Unit(items=list(items), langs={lang}, first=None, vector=vector,
                anchors=set(anchors), places=set(places), numbers=set(numbers))


def link(a, b, cosine, accepted=True):
    return XLink(a, b, cosine, accepted, [f"multilingual cosine {cosine:.2f} (m)"])


# defaults: the original stage


def test_defaults_accept_any_single_anchor_class():
    geo = Geo()
    assert judge(unit([1], "en", anchors={"hamas"}), unit([2], "es", anchors={"hamas"}), 0.7, geo, "m").accepted
    assert judge(unit([1], "en", places={"gaza"}), unit([2], "es", places={"gaza"}), 0.7, geo, "m").accepted
    assert judge(unit([1], "en", numbers={"250"}), unit([2], "es", numbers={"250"}), 0.7, geo, "m").accepted
    assert judge(unit([1], "en", places={"irkutsk"}), unit([2], "es", places={"siberia"}), 0.7, geo, "m").accepted
    assert not judge(unit([1], "en"), unit([2], "es"), 0.95, geo, "m").accepted      # cosine alone never merges


def test_default_guard_matches_the_config_defaults_and_evidence_is_unchanged():
    assert Guard.of(CrossLanguageConfig(), []) == Guard()
    l = judge(unit([1], "en", anchors={"hamas"}, places={"gaza"}), unit([2], "es", anchors={"hamas"}, places={"gaza"}),
              0.71, Geo(), "m")
    assert l.evidence == ["multilingual cosine 0.71 (m)", "shared anchors ['hamas']",
                          "shared specific places ['gaza~gaza']"]


def test_a_place_conflict_still_rejects_under_every_guard():
    for g in (Guard(), Guard(require_anchor_classes=2), Guard(exact_places=True)):
        l = judge(unit([1], "en", anchors={"x"}, places={"gaza"}, numbers={"250"}),
                  unit([2], "es", anchors={"x"}, places={"madrid"}, numbers={"250"}), 0.8, Geo(), "m", g)
        assert not l.accepted and "place conflict" in l.evidence[-1]


# G1: two independent anchor classes


@pytest.mark.parametrize("a,b,ok", [
    (dict(anchors={"hamas"}), dict(anchors={"hamas"}), False),                          # actor only
    (dict(places={"gaza"}), dict(places={"gaza"}), False),                              # place only
    (dict(anchors={"hamas"}, places={"gaza"}), dict(anchors={"hamas"}, places={"gaza"}), True),
    (dict(anchors={"pike"}, numbers={"250"}), dict(anchors={"pike"}, numbers={"250"}), True),
    (dict(places={"fairford"}, numbers={"250"}), dict(places={"fairford"}, numbers={"250"}), True),
    (dict(anchors={"a", "b", "c"}), dict(anchors={"a", "b", "c"}), False),               # many anchors, one class
])
def test_g1_requires_two_anchor_classes(a, b, ok):
    l = judge(unit([1], "en", **a), unit([2], "es", **b), 0.8, Geo(), "m", Guard(require_anchor_classes=2))
    assert l.accepted is ok


# G2: broad anchors are not decisive


def test_g2_counts_units_and_marks_anchors_in_more_than_k_units():
    units = [unit([n], "en", anchors={"lula"} | ({"rare"} if n == 0 else set()), places={"gaza"} if n < 2 else set())
             for n in range(5)]
    anchors, places = broad_terms(units, 3)
    assert anchors == {"lula"} and places == set()
    assert broad_terms(units, None) == (frozenset(), frozenset())
    assert broad_terms(units, 1)[1] == {"gaza"}


def test_g2_a_broad_anchor_neither_accepts_nor_vetoes():
    g = Guard(broad_anchors=frozenset({"lula"}), broad_places=frozenset({"gaza"}))
    only_broad = judge(unit([1], "en", anchors={"lula"}, places={"gaza"}), unit([2], "es", anchors={"lula"},
                       places={"gaza"}), 0.86, Geo(), "m", g)
    assert not only_broad.accepted and "broad, not decisive" in only_broad.evidence[-1]
    with_specific = judge(unit([1], "en", anchors={"lula", "flavio bolsonaro"}),
                          unit([2], "es", anchors={"lula", "flavio bolsonaro"}), 0.86, Geo(), "m", g)
    assert with_specific.accepted


def test_g2_a_contained_place_is_broad_when_either_side_is():
    g = Guard(broad_places=frozenset({"siberia"}))
    l = judge(unit([1], "en", places={"irkutsk"}), unit([2], "es", places={"siberia"}), 0.7, Geo(), "m", g)
    assert not l.accepted


def test_g2_is_computed_per_run_in_propose():
    v = np.array([1.0, 0.0])
    units = [unit([n], lang, anchors={"hamas"}, vector=v) for n, lang in enumerate(["en", "es", "it", "en", "es"])]
    cl = CrossLanguageConfig(broad_anchor_units=3)
    assert not any(l.accepted for l in propose(units, type("C", (), {"cross_language": cl})(), Geo()))
    cl = CrossLanguageConfig(broad_anchor_units=5)
    assert all(l.accepted for l in propose(units, type("C", (), {"cross_language": cl})(), Geo()))


# G3: direct pairwise support


def test_g3_a_chain_does_not_merge_units_that_are_not_directly_linked():
    a, b, c = unit([1], "en"), unit([2], "es"), unit([3], "it")
    links = [link(a, b, 0.80), link(b, c, 0.70)]                                  # a and c: no link
    chained, _ = merge_units([a, b, c], links)
    assert chained == [[1, 2, 3]]                                                  # default: transitive
    direct, xlang = merge_units([a, b, c], links, direct_only=True)
    assert sorted(direct) == [[1, 2]]                                              # highest-cosine link kept
    assert [e["b"] for e in xlang[0]] == [[2]]


def test_g3_keeps_a_fully_linked_component_whole():
    a, b, c = unit([1], "en"), unit([2], "es"), unit([3], "it")
    links = [link(a, b, 0.80), link(b, c, 0.70), link(a, c, 0.65)]
    assert merge_units([a, b, c], links, direct_only=True)[0] == [[1, 2, 3]]


def test_g3_same_language_units_need_no_link_between_them():
    en1, en2, es = unit([1], "en"), unit([2], "en"), unit([3], "es")
    links = [link(en1, es, 0.80), link(en2, es, 0.75)]
    assert merge_units([en1, en2, es], links, direct_only=True)[0] == [[1, 2, 3]]


def test_g3_rejected_links_never_merge():
    a, b = unit([1], "en"), unit([2], "es")
    assert merge_units([a, b], [link(a, b, 0.9, accepted=False)], direct_only=True)[0] == []


def test_g3_two_separate_chains_resolve_independently():
    a, b, c = unit([1], "en"), unit([2], "es"), unit([3], "it")
    d, e = unit([4], "en"), unit([5], "es")
    links = [link(a, b, 0.70), link(b, c, 0.90), link(d, e, 0.66)]
    groups, _ = merge_units([a, b, c, d, e], links, direct_only=True)
    assert sorted(groups) == [[2, 3], [4, 5]]


# G4: exact specific places


def test_g4_containment_is_not_a_place_anchor_but_is_not_a_conflict():
    g = Guard(exact_places=True)
    contained = judge(unit([1], "en", places={"irkutsk"}), unit([2], "es", places={"siberia"}), 0.7, Geo(), "m", g)
    assert not contained.accepted and "place conflict" not in " ".join(contained.evidence)
    same = judge(unit([1], "en", places={"irkutsk"}), unit([2], "es", places={"irkutsk"}), 0.7, Geo(), "m", g)
    assert same.accepted and "shared specific places ['irkutsk~irkutsk']" in same.evidence
