"""Lexical identity evidence (processors/lexical.py): deterministic term extraction and classes,
explanations, the production same-outlet rule, and the (default-off) candidate guard."""

from collections import Counter
from datetime import datetime

import numpy as np
import pytest

from osint_monitor.core.config import LexicalConfig, LexicalGuardConfig, load_event_grouping_config
from osint_monitor.processors import lexical as L
from osint_monitor.processors.clustering import _ClusterMember, _linked

T0 = datetime(2026, 9, 29, 12, 0)


@pytest.fixture(scope="module")
def ex():
    return L.TermExtractor(config=LexicalConfig(generic_terms=["said", "says"], min_documents_for_frequency=4,
                                                generic_document_frequency=0.5))


def terms(ex, title, entities=(), lead="", df=None, n=0, participants=None, item_id=1):
    return ex.extract(item_id, title, lead, entities, df, n, participants)


def test_extraction_is_deterministic_and_order_independent(ex):
    ents = [("Kyiv", "GPE"), ("Ukraine", "GPE"), ("Volodymyr Zelensky", "PERSON")]
    a = terms(ex, "Russian drones strike Kyiv power plant, Zelensky says", ents)
    b = terms(ex, "Russian drones strike Kyiv power plant, Zelensky says", list(reversed(ents)))
    assert a.terms == b.terms
    assert {"kyiv", "drone", "strike", "power", "plant"} <= set(a.terms)
    assert "say" not in a.terms and "says" not in a.terms           # configured generic / folded stop word


def test_aliases_fold_to_one_term(ex):
    us = [terms(ex, "t", [(n, "GPE")]).terms for n in ("US", "U.S.", "United States", "America")]
    assert all(set(t) == {"united states"} for t in us)
    assert set(terms(ex, "t", [("Iranian", "NORP")]).terms) == {"iran"}      # demonym -> country
    assert terms(ex, "t", [("Iranian", "NORP")]).terms["iran"].cls == L.GENERIC


def test_countries_and_batch_frequent_words_are_generic(ex):
    docs = [["war", "attack", "kyiv"], ["war", "attack"], ["war", "talk"], ["war", "election"]]
    df, n = L.document_frequencies(docs)
    t = terms(ex, "War attack on Kyiv", [("Kyiv", "GPE"), ("Ukraine", "GPE")], df=df, n=n)
    assert t.terms["war"].cls == L.GENERIC and t.terms["attack"].cls == L.GENERIC     # in >= 50% of the batch
    assert t.terms["ukraine"].cls == L.GENERIC and t.terms["kyiv"].cls == L.HIGH
    # below min_documents_for_frequency the batch is too small to call a word common
    assert terms(ex, "War attack", df=Counter(war=2), n=2).terms["war"].cls == L.MEDIUM


def test_same_actors_with_different_actions_is_not_event_specific_evidence(ex):
    ents = [("United States", "GPE"), ("China", "GPE")]
    a = terms(ex, "United States and China agree tariff truce", ents, item_id=1)
    b = terms(ex, "China warns United States over Taiwan Strait transit", ents + [("Taiwan Strait", "LOC")], item_id=2)
    ev = L.keyword_link_evidence(a, b)
    assert ev.shared_generic == ["china", "united states"] and not ev.event_specific
    assert ev.result == L.INSUFFICIENT
    c = terms(ex, "China and United States tariff truce holds", ents, item_id=3)
    assert L.keyword_link_evidence(a, c).event_specific == ["tariff", "truce"]


def test_named_actor_counts_fully_only_when_it_takes_part(ex):
    ents = [("Donald Trump", "PERSON")]
    part = terms(ex, "Trump signs order", ents, participants={"donald trump"})
    mention = terms(ex, "Senate passes bill opposed by Trump", ents, participants=set())
    assert part.terms["donald trump"].cls == L.HIGH and mention.terms["donald trump"].cls == L.MEDIUM
    df, n = Counter({"donald trump": 3}), 4
    assert terms(ex, "x", ents, df=df, n=n, participants=set()).terms["donald trump"].cls == L.GENERIC


def test_inflections_fold_but_synonyms_are_not_invented(ex):
    assert L.content_words("strikes militias glasses taxes talks") == ["strike", "militia", "glass", "tax", "talk"]
    a = terms(ex, "Missile strikes hit port", item_id=1)
    b = terms(ex, "Missile strike hits port", item_id=2)
    assert {"missile", "strike", "port", "hit"} <= set(L.keyword_link_evidence(a, b).shared_medium)
    c = terms(ex, "Rocket attack on harbour", item_id=3)
    assert L.keyword_link_evidence(a, c).result == L.NO_SHARED        # strike/attack, port/harbour: embeddings' job


def test_specific_places_are_distinct_terms(ex):
    kyiv = terms(ex, "Drone strike on Kyiv", [("Kyiv", "GPE")], item_id=1)
    odesa = terms(ex, "Drone strike on Odesa", [("Odesa", "GPE")], item_id=2)
    assert kyiv.terms["kyiv"].cls == L.HIGH
    ev = L.keyword_link_evidence(kyiv, odesa)
    assert "kyiv" not in ev.shared_high and ev.shared_medium == ["drone", "strike"]


def test_same_outlet_update_rule_uses_the_configured_ratio_and_is_explained(ex):
    a, b = "US attacks Iran for 10th consecutive night", "US attacks Iran for 11th consecutive night"
    # known limitation, pinned: one outlet's templated headlines of consecutive occurrences read as an update
    assert L.same_source_update(a, b)
    assert not L.same_source_update(a, b, LexicalConfig(same_source_title_ratio=100))
    assert not L.same_source_update(a, "Iran says talks with US are over")
    ev = L.keyword_link_evidence(terms(ex, a, item_id=1), terms(ex, b, item_id=2), same_source=True, a_title=a, b_title=b)
    assert ev.contribution == "same-outlet update link (headline ratio)" and ev.headline_ratio >= 90
    assert load_event_grouping_config().lexical.same_source_title_ratio == 90


def test_explanation_lists_actors_terms_overlap_and_contribution(ex):
    ents = [("China", "GPE"), ("United States", "GPE")]
    a = terms(ex, "China and United States tariff talks", ents, item_id=1)
    b = terms(ex, "United States, China resume tariff talks", ents, item_id=2)
    text = L.keyword_link_evidence(a, b, similarity=0.61, linked=True).format()
    for part in ("keyword evidence", "shared high-value terms:", "shared generic terms:", "  china", "  tariff",
                 "weighted lexical overlap:", "embedding similarity:", "decision contribution:",
                 "corroborating signal only"):
        assert part in text
    c = terms(ex, "China and United States security concerns", ents, item_id=3)
    rejected = L.keyword_link_evidence(a, c, linked=False)
    assert rejected.result == L.INSUFFICIENT and "insufficient event-specific lexical evidence" in rejected.format()
    assert 0.0 < rejected.weighted_overlap < L.keyword_link_evidence(a, b).weighted_overlap


def member(i, source, title, vec, t=None):
    return _ClusterMember(i, source, title, T0, np.array(vec, dtype=float), t)


def test_guard_is_off_by_default_and_production_links_are_unchanged(ex):
    assert load_event_grouping_config().lexical.guard.enabled is False and L.settings().guard.enabled is False
    generic_only = [terms(ex, "US and Iran", [("United States", "GPE"), ("Iran", "GPE")], item_id=i) for i in (1, 2)]
    a, b = member(1, 1, "a", [1, 0.9], generic_only[0]), member(2, 2, "b", [1, 1], generic_only[1])
    assert _linked(a, b)                               # cosine ~0.999 >= 0.53; guard off: terms ignored


def test_guard_candidate_vetoes_weak_links_supported_only_by_generic_terms(ex):
    config = LexicalConfig(guard=LexicalGuardConfig(enabled=True, max_similarity=0.6, min_event_specific=1))
    ents = [("United States", "GPE"), ("Iran", "GPE")]
    g1, g2 = (terms(ex, t, ents, item_id=i) for i, t in ((1, "US strikes Iran"), (2, "Iran vows revenge on US")))
    s1, s2 = (terms(ex, t, ents, item_id=i) for i, t in ((3, "US strikes Iran oil terminal"), (4, "Iran oil terminal hit")))
    weak = [1, 0], [0.55, 0.835]                       # cosine 0.55: inside the guarded band
    L.use_settings(config)
    try:
        assert not _linked(member(1, 1, "a", weak[0], g1), member(2, 2, "b", weak[1], g2))
        assert _linked(member(3, 1, "a", weak[0], s1), member(4, 2, "b", weak[1], s2))
        assert _linked(member(1, 1, "a", [1, 0], g1), member(2, 2, "b", [1, 0.2], g2))       # strong link: never vetoed
        assert not _linked(member(1, 1, "a", [1, 0], g1), member(2, 2, "b", [0, 1], g2))      # below 0.53 anyway
    finally:
        L.use_settings(None)


def test_structured_grouping_never_uses_lexical_functions(monkeypatch):
    import inspect
    from osint_monitor.core.database import RawItem, Source
    from osint_monitor.processors import event_grouping

    def boom(*a, **k):
        raise AssertionError("lexical logic used for structured records")
    for name in ("same_source_update", "keyword_link_evidence", "batch_terms", "guard_allows"):
        monkeypatch.setattr(L, name, boom)
    usgs = Source(name="USGS Seismic", type="structured_api", url="u")
    quakes = [RawItem(id=i, source=usgs, title=f"Earthquake M5.{i} - Somewhere", url=f"https://earthquake.usgs.gov/eventpage/us{i}",
                      content=f"Magnitude: 5.0\nLocation: {10.0 * i}, 20.0", published_at=T0, content_hash=str(i))
              for i in (1, 2)]                                   # same template, 1,100 km apart
    quakes.append(RawItem(id=3, source=usgs, title="Earthquake M5.1 - Somewhere", url="https://earthquake.usgs.gov/eventpage/us1",
                          content="", published_at=T0, content_hash="3"))
    assert event_grouping.group_structured(quakes) == [[1, 3]]       # identity: shared USGS event id only
    assert "lexical" not in inspect.getsource(event_grouping)
