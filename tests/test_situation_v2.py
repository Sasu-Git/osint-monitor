"""Situation membership v2 rules (CONTRACT-V2-R2): ordering and the owner rulings, on synthetic inputs."""
from datetime import datetime, timedelta

from osint_monitor.processors.situations import v2 as V

T0 = datetime(2026, 11, 1, 12)


def dev(parties=("russia", "ukraine"), family="armed_conflict", places=None, report_share=1.0, hedges=(), eid=1,
        has_principals=True, hazard=None, country=None, at=T0, headline="Strike on Kharkiv", mixed=None):
    places = places if places is not None else {"kharkiv": "ukraine"}
    cs = {c for c in places.values() if c}
    return V.DevFeatures(eid, headline, "", at, frozenset(parties), has_principals, family, places,
                         country or (next(iter(cs)) if len(cs) == 1 else None), report_share, hazard, list(hedges), mixed)


WAR = V.Situation2("war", "actor_process", frozenset({"russia", "ukraine"}), frozenset({"armed_conflict"}),
                   frozenset({"russia", "ukraine"}))


def test_member_needs_scope_signal_even_at_full_coverage():           # OD5
    assert V.decide(dev(), WAR, [WAR]).outcome == "MEMBER"
    assert V.decide(dev(family=None, places={}), WAR, [WAR]).reason == "NO_SCOPE_SIGNAL"


def test_commentary_is_context_and_no_principals_is_rejected():        # D2, D3
    assert V.decide(dev(report_share=0.0), WAR, [WAR]).outcome == "CONTEXT"
    assert V.decide(dev(has_principals=False), WAR, [WAR]).reason == "NO_PRINCIPALS"


def test_spillover_when_every_place_is_outside_scope():                # D6
    d = dev(parties=("russia", "ukraine"), places={"tallinn": "estonia"})
    assert V.decide(d, WAR, [WAR]).outcome == "SPILLOVER"


def test_generic_party_alone_needs_strong_match():                     # OD6
    us_ru = V.Situation2("ru-us", "actor_process", frozenset({"russia", "united states"}), frozenset({"economic"}),
                         frozenset({"russia", "united states"}))
    weak = dev(parties=("united states", "india"), family="diplomacy", places={"new delhi": "india"})
    assert V.decide(weak, us_ru, [us_ru]).reason == "GENERIC_ANCHOR_ONLY"
    strong = dev(parties=("united states",), family="economic", places={"moscow": "russia"})
    assert V.decide(strong, us_ru, [us_ru]).outcome == "MEMBER"


def test_better_situation_and_tie():
    seeded = V.Situation2("war-seed", "seeded", WAR.anchors, frozenset({"armed_conflict"}), WAR.place_scope)
    assert V.decide(dev(), WAR, [WAR, seeded]).outcome == "OTHER_SITUATION"
    twin = V.Situation2("twin", "actor_process", WAR.anchors, WAR.families, WAR.place_scope)
    assert V.decide(dev(), WAR, [WAR, twin]).outcome == "AMBIGUOUS"


def test_pending_attribution_and_mixed():                              # OD3
    assert V.decide(dev(hedges=["suspected"]), WAR, [WAR]).reason == "PENDING_ATTRIBUTION"
    assert V.decide(dev(mixed=True), WAR, [WAR]).reason == "PENDING_MIXED"


def test_single_party_creation_needs_two_developments_a_day_apart():  # OD1
    a = dev(parties=("javier milei",), family="politics", places={"buenos aires": "argentina"}, eid=1)
    b = dev(parties=("javier milei",), family="politics", places={"cordoba": "argentina"}, eid=2,
            at=T0 + timedelta(hours=30))
    made, _ = V.derive_automatic("milei", frozenset({"javier milei"}), [a, b], set())
    assert made and made[0].mode == "single_party"
    same_day = dev(parties=("javier milei",), family="politics", places={"cordoba": "argentina"}, eid=3,
                   at=T0 + timedelta(hours=2))
    assert V.derive_automatic("milei", frozenset({"javier milei"}), [a, same_day], set())[0] == []
    assert V.derive_automatic("us", frozenset({"united states"}), [a, b], set())[0] == []      # generic


def test_topic_split_and_hazard_mode():                                # OD4, OD2
    d1 = dev(eid=1)
    d2 = dev(eid=2, at=T0 + timedelta(hours=5))
    d3 = dev(eid=3, family="diplomacy")
    d4 = dev(eid=4, family="diplomacy", at=T0 + timedelta(hours=7))
    made, _ = V.derive_automatic("ru-ua", frozenset({"russia", "ukraine"}), [d1, d2, d3, d4], set())
    assert sorted(m.slug for m in made) == ["ru-ua~armed_conflict", "ru-ua~diplomacy"]
    h1 = dev(parties=(), has_principals=False, family=None, hazard=("storm", "rachel"), country="mexico", eid=5,
             places={"ensenada": "mexico"})
    h2 = dev(parties=(), has_principals=False, family=None, hazard=("storm", "rachel"), country="mexico", eid=6,
             places={"baja california": "mexico"}, at=T0 + timedelta(hours=6))
    made, _ = V.derive_automatic("rachel", frozenset(), [h1, h2], set())
    assert made[0].mode == "hazard"
    assert V.decide(h1, made[0], made).outcome == "MEMBER"                                     # no actors needed


def test_hazard_lexicon_and_storm_name():
    assert V.hazard_of(["Hurricane Rachel batters Mexico"]) == ("storm", "rachel")
    assert V.hazard_of(["Terremoto in Turchia"])[0] == "earthquake"
    assert V.hazard_of(["Talks resume in Geneva"]) is None
