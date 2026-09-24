"""Behaviour of the deterministic rule-based classifier."""

import pytest

from osint_monitor.core.models import (
    Concreteness, EventType, InteractionMode, UncertaintyFlag,
)
from osint_monitor.processors.classification import DevelopmentClassifier, RuleBasedClassifier
from tests.helpers import make_context


@pytest.fixture(scope="module")
def clf():
    return RuleBasedClassifier()


def test_satisfies_protocol(clf):
    assert isinstance(clf, DevelopmentClassifier)


# --- physical meetings -------------------------------------------------------

@pytest.mark.parametrize("title", [
    "Putin meets Xi in Beijing",
    "Modi hosts Albanese for talks",
    "Macron and Scholz hold face-to-face talks",
])
def test_physical_meeting(clf, title):
    r = clf.classify(make_context(title, entities={"Putin": "PERSON", "Xi": "PERSON"}))
    assert r.event_type == EventType.BILATERAL_MEETING
    assert r.interaction_mode == InteractionMode.PHYSICAL
    assert r.concreteness == Concreteness.ACTION
    assert not r.is_routine_commentary
    assert UncertaintyFlag.INTERACTION_MODE_UNCLEAR not in r.uncertainty_flags


def test_multilateral_meeting(clf):
    r = clf.classify(make_context("G7 foreign ministers meet in Rome"))
    assert r.event_type == EventType.MULTILATERAL_MEETING
    assert r.interaction_mode == InteractionMode.PHYSICAL


def test_discussion_topic_does_not_become_event_type(clf):
    r = clf.classify(make_context("Blinken meets Wang Yi to discuss sanctions on Russia"))
    assert r.event_type == EventType.BILATERAL_MEETING


# --- phone / video vs physical ----------------------------------------------

@pytest.mark.parametrize("title, mode", [
    ("Biden and Xi hold phone call", InteractionMode.TELEPHONE),
    ("Macron spoke by phone with Zelensky", InteractionMode.TELEPHONE),
    ("Scholz and Macron hold video call on Ukraine aid", InteractionMode.VIDEO),
])
def test_remote_meeting_is_still_a_meeting(clf, title, mode):
    r = clf.classify(make_context(title))
    assert r.event_type == EventType.BILATERAL_MEETING
    assert r.interaction_mode == mode


def test_meeting_without_mode_evidence_is_unknown_and_flagged(clf):
    r = clf.classify(make_context("Blinken met Wang Yi"))
    assert r.event_type == EventType.BILATERAL_MEETING
    assert r.interaction_mode == InteractionMode.UNKNOWN
    assert UncertaintyFlag.INTERACTION_MODE_UNCLEAR in r.uncertainty_flags


# --- action vs commentary ----------------------------------------------------

def test_military_action(clf):
    r = clf.classify(make_context("Israeli air strikes hit targets in southern Lebanon"))
    assert r.event_type == EventType.MILITARY_ACTION
    assert r.concreteness == Concreteness.ACTION
    assert not r.is_routine_commentary


@pytest.mark.parametrize("title", [
    "Foreign ministry spokesperson says sanctions are illegal",
    "Analysis: what the Muscat talks mean for the region",
])
def test_commentary(clf, title):
    r = clf.classify(make_context(title))
    assert r.event_type == EventType.COMMENTARY
    assert r.concreteness == Concreteness.COMMENTARY
    assert r.interaction_mode == InteractionMode.NONE
    assert r.is_routine_commentary


# --- agreement vs negotiation ------------------------------------------------

def test_signed_agreement(clf):
    r = clf.classify(make_context("Armenia and Azerbaijan sign peace agreement"))
    assert r.event_type == EventType.AGREEMENT
    assert r.concreteness == Concreteness.AGREEMENT


def test_agreed_ceasefire(clf):
    r = clf.classify(make_context("Israel and Hamas agree ceasefire deal"))
    assert r.event_type == EventType.CEASEFIRE
    assert r.concreteness in {Concreteness.AGREEMENT, Concreteness.ACTION}


@pytest.mark.parametrize("title", [
    "Ceasefire talks resume in Cairo",
    "US and Iran hold indirect nuclear talks",
])
def test_talks_without_outcome_are_negotiation(clf, title):
    r = clf.classify(make_context(title))
    assert r.event_type == EventType.NEGOTIATION
    assert r.concreteness == Concreteness.NEGOTIATION


def test_expected_signing_is_not_an_agreement_yet(clf):
    r = clf.classify(make_context("Leaders expected to sign trade deal on Friday"))
    assert r.concreteness == Concreteness.DECLARATION
    assert UncertaintyFlag.UNCONFIRMED_COMPLETION in r.uncertainty_flags


# --- announced plan vs implemented action -----------------------------------

def test_policy_announcement(clf):
    r = clf.classify(make_context("EU announces plan to ban Russian LNG imports"))
    assert r.event_type == EventType.POLICY_CHANGE
    assert r.concreteness == Concreteness.DECLARATION
    assert UncertaintyFlag.UNCONFIRMED_COMPLETION in r.uncertainty_flags


@pytest.mark.parametrize("title", [
    "Ban on Russian LNG imports takes effect",
    "Government issues decree raising conscription age",
])
def test_policy_implementation(clf, title):
    r = clf.classify(make_context(title))
    assert r.event_type == EventType.POLICY_CHANGE
    assert r.concreteness in {Concreteness.DECISION, Concreteness.ACTION}
    assert UncertaintyFlag.UNCONFIRMED_COMPLETION not in r.uncertainty_flags


def test_sanctions_imposed(clf):
    r = clf.classify(make_context("US Treasury imposes sanctions on Iranian oil network"))
    assert r.event_type == EventType.SANCTIONS
    assert r.concreteness in {Concreteness.DECISION, Concreteness.ACTION}


def test_sanctions_considered(clf):
    r = clf.classify(make_context("EU weighs new sanctions on Belarus"))
    assert r.event_type == EventType.SANCTIONS
    assert r.concreteness == Concreteness.DECLARATION
    assert UncertaintyFlag.UNCONFIRMED_COMPLETION in r.uncertainty_flags


def test_planned_meeting(clf):
    r = clf.classify(make_context("Trump to meet Putin in Alaska next week"))
    assert r.event_type == EventType.BILATERAL_MEETING
    assert r.concreteness == Concreteness.DECLARATION
    assert UncertaintyFlag.UNCONFIRMED_COMPLETION in r.uncertainty_flags


def test_plan_later_reported_as_done_is_completed(clf):
    r = clf.classify(make_context("Trump to meet Putin in Alaska", "Trump meets Putin in Anchorage"))
    assert r.concreteness == Concreteness.ACTION
    assert UncertaintyFlag.UNCONFIRMED_COMPLETION not in r.uncertainty_flags


# --- uncertainty -------------------------------------------------------------

def test_denial_flags_contradiction(clf):
    r = clf.classify(make_context(
        "US and Iran held secret talks in Oman, sources say",
        "Iran denies holding talks with US",
    ))
    assert UncertaintyFlag.CONTRADICTORY_REPORTS in r.uncertainty_flags


def test_upstream_contradiction_is_flagged(clf):
    r = clf.classify(make_context("Russia strikes Kharkiv", "Russian strikes on Kharkiv", has_contradictions=True))
    assert UncertaintyFlag.CONTRADICTORY_REPORTS in r.uncertainty_flags


def test_single_source_flag(clf):
    assert UncertaintyFlag.SINGLE_SOURCE in clf.classify(make_context("Russia strikes Kharkiv")).uncertainty_flags
    two = make_context("Russia strikes Kharkiv", "Russian missiles hit Kharkiv")
    assert UncertaintyFlag.SINGLE_SOURCE not in clf.classify(two).uncertainty_flags


@pytest.mark.parametrize("titles", [("Situation remains tense",), ()])
def test_insufficient_evidence_is_unknown(clf, titles):
    r = clf.classify(make_context(*titles))
    assert r.event_type == EventType.UNKNOWN
    assert UncertaintyFlag.INSUFFICIENT_CONTEXT in r.uncertainty_flags


# --- structured fields and determinism --------------------------------------

def test_entities_and_location_come_from_context(clf):
    r = clf.classify(make_context(
        "Araghchi meets Witkoff in Muscat",
        entities={"Abbas Araghchi": "PERSON", "Iran": "GPE", "United States": "GPE", "IAEA": "ORG"},
        location_name="Muscat",
    ))
    assert r.actors == ["Abbas Araghchi"]
    assert set(r.countries) == {"Iran", "United States"}
    assert r.organizations == ["IAEA"]
    assert r.location == "Muscat"
    assert r.significance_class is None   # rules do not rank
    assert r.classifier == "rules"


def test_deterministic(clf):
    ctx = make_context("Putin meets Xi in Beijing", "Xi hosts Putin for talks")
    assert clf.classify(ctx) == clf.classify(ctx)
    assert RuleBasedClassifier().classify(ctx) == clf.classify(ctx)
