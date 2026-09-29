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


# --- legal, court, release and migration stories (2026-09 benchmark and live windows) -------------

def test_deportation_is_not_a_meeting(clf):
    t = kind(clf, "Malaysia begins sending thousands of Myanmar nationals back to war-torn homeland",
             "Malaysia begins sending back Rohingya refugees despite safety warnings",
             "Malaysia begins controversial repatriation of asylum seekers to Myanmar",
             excerpts=["Malaysia, which once welcomed Rohingya fleeing Myanmar, has started deportations.", "", ""])
    assert t not in {EventType.BILATERAL_MEETING, EventType.MULTILATERAL_MEETING, EventType.DIPLOMATIC_VISIT,
                     EventType.DEPLOYMENT}


def test_extradition_is_not_a_visit(clf):
    assert kind(clf, "Suspect extradited to Spain arrives in Madrid") != EventType.DIPLOMATIC_VISIT


def test_release_from_custody_after_an_insult_conviction_is_not_a_security_incident(clf):
    t = kind(clf, "Stand-up comic set for release after being convicted of insulting Erdoğan",
             "Stand-up comic released after being convicted of insulting Erdoğan",
             excerpts=["Turkish comedian Deniz Göktaş has been sentenced to almost 19 months, but is set to be "
                       "released due to time served.",
                       "Turkish comedian Deniz Göktaş also faces a travel ban but has been released due to time served."])
    assert t == EventType.UNKNOWN


def test_prisoner_release_is_not_an_election(clf):
    t = kind(clf, "Venezuela releases dozens of political prisoners as election calls grow",
             excerpts=["A slew of dissidents being released from long-term detention comes days after the nation's "
                       "interim leader met the US president."])
    assert t not in {EventType.ELECTION, EventType.BILATERAL_MEETING}


def test_arrests_for_ordinary_crime_are_not_security_incidents(clf):
    for title in ("Hong Kong police arrest 991 in crackdown on illegal gambling during World Cup",
                  "South Korea’s Unification Church leader Han Hak-ja jailed 2 years for bribing officials",
                  "Hong Kong boy, 14, arrested for animal cruelty after badly injured cat dies"):
        assert kind(clf, title) != EventType.SECURITY_INCIDENT, title


def test_court_ruling_is_not_a_policy_change_or_an_election(clf):
    assert kind(clf, "Judge blocks Trump from tying anti-terrorism grants to election changes") not in {
        EventType.POLICY_CHANGE, EventType.ELECTION}
    assert kind(clf, "Media outlets banned by Trump denied access to White House dinner despite judge's order") \
        != EventType.POLICY_CHANGE


def test_legal_proceedings_are_not_an_agreement(clf):
    assert kind(clf, "Court upholds conviction as defendants agree to appeal to supreme court") != EventType.AGREEMENT


def test_suspended_visits_and_party_conferences_are_not_meetings(clf):
    assert kind(clf, "Nigeria suspends official visits to South Africa over anti-migrant violence") \
        != EventType.DIPLOMATIC_VISIT
    assert kind(clf, "UK Labour Party meets buoyed by Burnham but seeking concrete plans") \
        != EventType.BILATERAL_MEETING


def test_one_explainer_among_reports_does_not_make_the_development_commentary(clf):
    t = kind(clf, "US prosecutors reopen case of alleged gang rape at Cornell University",
             "Why has a Cornell rape investigation been reopened?",
             "US prosecutors reopen case of alleged frat house gang rape at Cornell University")
    assert t != EventType.COMMENTARY
    assert kind(clf, "Why has a Cornell rape investigation been reopened?") == EventType.COMMENTARY


# counter-examples: true positives the legal and migration guards must keep

def test_arrests_and_verdicts_for_security_offences_stay_security_incidents(clf):
    for title in ("UK police arrest 5 on terrorism charges near airbase used by US in Iran war",
                  "Italian court convicts three Egyptian agents for kidnap of Giulio Regeni",
                  "Hong Kong man jailed 3 years for hammer attack on associate who later died",
                  "Man charged with espionage over drone flights near naval base"):
        assert kind(clf, title) == EventType.SECURITY_INCIDENT, title


def test_meetings_about_migration_stay_meetings(clf):
    assert kind(clf, "Meloni meets Libyan leader in Tripoli over migrants") in {
        EventType.BILATERAL_MEETING, EventType.MULTILATERAL_MEETING}


def test_genuine_policy_decisions_and_agreements_keep_their_type(clf):
    assert kind(clf, "Government bans TikTok on official devices, rules take effect Monday") == EventType.POLICY_CHANGE
    assert kind(clf, "US and India sign trade agreement in New Delhi") == EventType.AGREEMENT
    assert kind(clf, "Wang Yi visits Tokyo for talks with Japanese counterpart") in {
        EventType.DIPLOMATIC_VISIT, EventType.BILATERAL_MEETING, EventType.NEGOTIATION}
