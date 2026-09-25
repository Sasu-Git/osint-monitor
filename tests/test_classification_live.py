"""Rule classifier on real live failures (2026-09-24/25 collects) and the guards that fixed
them, plus counter-examples that must keep their type. Tests semantics, not notes."""

import pytest

from osint_monitor.core.models import Concreteness, EventDomain, EventType
from osint_monitor.processors.classification import RuleBasedClassifier
from tests.helpers import make_context


@pytest.fixture(scope="module")
def clf():
    return RuleBasedClassifier()


def kind(clf, *titles, excerpts=None):
    return clf.classify(make_context(*titles, excerpts=excerpts)).event_type


# --- live failures --------------------------------------------------------------------------

def test_eviction_story_mentioning_an_upcoming_election_is_not_an_election(clf):
    t = kind(clf, "Dramatic eviction of woman aged 87 highlights Spain's housing shortage",
             "Spain’s housing crisis in spotlight with eviction of pensioner, 87",
             excerpts=["The tenant of the flat in Madrid, Maricarmen, was unable to pay the rent set by the firm.",
                       "The eviction of an 87-year-old from her Madrid home has highlighted a political paralysis "
                       "that has thwarted efforts to resolve Spain’s chronic housing crisis, fuelling debate before "
                       "next year’s election."])
    assert t != EventType.ELECTION


def test_arrest_of_an_activist_is_a_security_incident(clf):
    r = clf.classify(make_context("Far-right UK activist Daniel Thomas arrested after slashing dinghy",
                                  "UK far-right activist arrested after migrant boat slashed in English Channel"))
    assert r.event_type == EventType.SECURITY_INCIDENT and r.event_domain == EventDomain.SECURITY


def test_ai_agent_hacking_a_government_is_a_security_incident(clf):
    assert kind(clf, "Rogue OpenAI agent 'infiltrated' Australian government website in world first",
                "OpenAI agents hack Australian government health data") == EventType.SECURITY_INCIDENT


def test_criminal_knife_attack_is_not_military_action(clf):
    assert kind(clf, "Priest killed and four injured in knife attack at Polish abbey") == EventType.SECURITY_INCIDENT


def test_cross_border_strikes_reported_with_attribution_are_military_action(clf):
    # was significant_statement: "..., Taliban says" matched before any military wording
    assert kind(clf, "Four civilians killed in Pakistani strikes in Afghanistan, Taliban says",
                "Pakistani forces kill Afghan Taliban fighters in border escalation") == EventType.MILITARY_ACTION


def test_ministers_agreeing_to_ban_something_is_a_policy_decision_not_an_agreement(clf):
    r = clf.classify(make_context("Italy ministers agree to ban burqa and niqab in school and cap foreigners in class",
                                  "Meloni government bans burqas, caps foreign students in Italian schools"))
    assert r.event_type == EventType.POLICY_CHANGE
    assert r.concreteness != Concreteness.AGREEMENT


def test_quoted_figure_of_speech_is_not_a_warning(clf):
    t = kind(clf, "Nepal’s leader labels devastating flood a ‘warning to the world’",
             "Flood-ravaged Nepal pushes for climate deal with India, China")
    assert t != EventType.WARNING and t == EventType.SIGNIFICANT_STATEMENT


# --- counter-examples: the guards must not over-reach ----------------------------------------

@pytest.mark.parametrize("titles, expected", [
    (("Japan's ruling party wins snap election",), EventType.ELECTION),
    (("Voters head to the polls as Moldova holds parliamentary elections",), EventType.ELECTION),
    (("US and China agree to cut tariffs for 90 days",), EventType.AGREEMENT),
    (("EU agrees with UK to extend fishing access",), EventType.AGREEMENT),
    (("Iran warns US of 'crushing response' to any attack",), EventType.WARNING),
    (("Russia launches missile attack on Kyiv",), EventType.MILITARY_ACTION),
    (("Israeli strikes kill 12 in Gaza",), EventType.MILITARY_ACTION),
])
def test_genuine_cases_keep_their_type(clf, titles, expected):
    assert kind(clf, *titles) == expected


def test_election_named_only_in_a_lead_sentence_still_counts_when_it_is_the_event(clf):
    assert kind(clf, "Moldova goes to the polls",
                excerpts=["Moldovans voted on Sunday in a parliamentary election seen as a test of the EU path."]
                ) == EventType.ELECTION


# --- evidence across headlines ---------------------------------------------------------------

def test_one_headline_cannot_outvote_the_rest_of_the_cluster(clf):
    assert kind(clf, "Trump-Xi summit opens at the White House", "Xi and Trump begin summit with red carpet",
                "Summit day 1: Trump and Xi trade compliments", "US weighs new sanctions on Chinese chipmakers"
                ) == EventType.SUMMIT


def test_even_split_between_substantive_types_is_reported_ambiguous(clf):
    _, ambiguous = clf.assess(make_context("Trump-Xi summit opens at the White House", "Summit day 1 highlights",
                                           "US imposes sanctions on Chinese chipmakers", "China sanctions US defence firms"))
    assert ambiguous


def test_clear_case_is_not_ambiguous_and_deeds_beat_words_on_a_tie(clf):
    r, ambiguous = clf.assess(make_context("Russia strikes Kharkiv", "Kremlin says strikes were retaliation"))
    assert r.event_type == EventType.MILITARY_ACTION and not ambiguous
