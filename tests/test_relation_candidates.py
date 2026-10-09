"""Relation candidate generation (processors/relation_candidates.py): rules of the pre-registered plan."""
from datetime import datetime, timedelta

from osint_monitor.processors.relation_candidates import REACTION, DevelopmentView, generate, hazard_classes

T0 = datetime(2026, 10, 1, 12)


class Geo:
    countries = {"nepal", "china", "spain", "france"}
    inside = {"kathmandu": "nepal", "tibet": "china", "madrid": "spain"}
    known = countries | set(inside)

    def same_or_contains(self, a, b):
        return a == b or self.inside.get(a) == b or self.inside.get(b) == a

    def is_country(self, p):
        return p in self.countries


def view(id, text, hours=0, principals=(), places=()):
    return DevelopmentView(id, T0 + timedelta(hours=hours), [text], set(principals), set(places))


def types(cands):
    return sorted((c.relation_type, c.source_event_id, c.target_event_id) for c in cands)


def test_hazard_classes_cover_three_languages():
    assert hazard_classes("Flash floods hit Kathmandu") == {"flood"}
    assert hazard_classes("Terremoto en el sur") == {"earthquake"}
    assert hazard_classes("Focolaio di ebola") == {"outbreak"}
    assert hazard_classes("Reactor safety review") == set()


def test_calamity_needs_the_same_hazard_class_and_compatible_places():
    flood = view(1, "Floods kill 20 in Kathmandu", 0, places={"kathmandu"})
    toll = view(2, "Nepal flood death toll rises", 30, places={"nepal"})
    quake = view(3, "Earthquake shakes Nepal", 30, places={"nepal"})
    elsewhere = view(4, "Floods in Madrid", 30, places={"madrid"})
    assert types(generate([flood, toll, quake, elsewhere], Geo())) == [("same_calamity_lifecycle", 1, 2)]


def test_episodes_are_limited_to_seven_days():
    a = view(1, "Floods in Nepal", 0, places={"nepal"})
    b = view(2, "Nepal flood recovery", 24 * 8, places={"nepal"})
    assert generate([a, b], Geo()) == []


def test_convened_event_needs_a_gathering_and_participants_or_venue():
    visit = view(1, "Macron begins state visit to Spain", 0, principals={"Macron", "Sanchez"})
    day2 = view(2, "Macron and Sanchez meeting on economy", 20, principals={"Macron", "Sanchez"})
    one_actor = view(3, "Sanchez attends conference", 20, principals={"Sanchez"})
    named = view(4, "SCO summit opens", 0)
    named2 = view(5, "Leaders arrive for SCO meeting", 10)
    found = types(generate([visit, day2, one_actor, named, named2], Geo()))
    assert ("same_convened_event", 1, 2) in found and ("same_convened_event", 4, 5) in found
    assert not any(c[0] == "same_convened_event" and 3 in c[1:] for c in found)


def test_reaction_is_proposed_from_the_later_cue_bearing_development_to_the_earlier():
    strike = view(1, "Israel strikes target in Syria", 0, principals={"Israel"})
    reaction = view(2, "UK condemns Israeli strike", 5, principals={"Israel", "UK"})
    assert types(generate([reaction, strike], Geo())) == [("reaction_to", 2, 1)]


def test_reaction_needs_a_shared_principal_and_72_hours():
    strike = view(1, "Israel strikes target in Syria", 0, principals={"Israel"})
    unrelated = view(2, "Brazil rejects tariff plan", 5, principals={"Brazil"})
    late = view(3, "UK condemns Israeli strike", 80, principals={"Israel"})
    assert generate([strike, unrelated, late], Geo()) == []


def test_reaction_cues_are_words_not_fragments():
    assert REACTION.search("Iran condemns sanctions") and REACTION.search("España rechaza el plan")
    assert REACTION.search("Roma respinge la proposta") and REACTION.search("in response to the vote")
    assert not REACTION.search("nuclear reactor restarts") and not REACTION.search("hailstorm damages crops")


def test_each_pair_gives_at_most_one_candidate_per_type_and_no_self_pairs():
    a = view(1, "Floods in Nepal; summit talks", 0, principals={"A", "B"}, places={"nepal"})
    b = view(2, "Nepal flood; leaders condemn delays at summit meeting", 5, principals={"A", "B"}, places={"nepal"})
    found = types(generate([a, b], Geo()))
    assert found == [("reaction_to", 2, 1), ("same_calamity_lifecycle", 1, 2), ("same_convened_event", 1, 2)]
