"""LLM classifier: prompt construction, output parsing, retry and fallback.

The external provider is never called; FakeProvider returns scripted replies.
"""

import json

import pytest
from pydantic import ValidationError

from osint_monitor.core.models import (
    Concreteness, DevelopmentClassification, EventType, InteractionMode,
    SignificanceClass, UncertaintyFlag,
)
from osint_monitor.processors.classification import (
    ClassificationError, DevelopmentClassifier, LLMClassifier,
)
from osint_monitor.processors.classification.llm_classifier import (
    build_system_prompt, parse_classification, render_context,
)
from tests.helpers import FakeProvider, make_context


def reply(**overrides) -> str:
    data = {
        "event_type": "bilateral_meeting",
        "event_domain": "diplomacy",
        "interaction_mode": "physical",
        "concreteness": "action",
        "significance_class": "major",
        "actors": ["Abbas Araghchi", "Steve Witkoff"],
        "countries": ["Iran", "United States"],
        "organizations": [],
        "location": "Muscat",
        "material_change": "First in-person round.",
        "why_it_matters": "Direct channel reopened.",
        "is_routine_commentary": False,
        "classification_notes": "Items place both in Muscat.",
        "uncertainty_flags": [],
    }
    data.update(overrides)
    return json.dumps(data)


MEETING = make_context("Araghchi meets Witkoff in Muscat", "Iran and US envoys hold talks in Oman")


# --- happy path --------------------------------------------------------------

def test_valid_reply_is_parsed():
    llm = FakeProvider(reply())
    r = LLMClassifier(llm).classify(MEETING)
    assert isinstance(LLMClassifier(llm), DevelopmentClassifier)
    assert r.event_type == EventType.BILATERAL_MEETING
    assert r.interaction_mode == InteractionMode.PHYSICAL
    assert r.concreteness == Concreteness.ACTION
    assert r.significance_class == SignificanceClass.MAJOR
    assert r.actors == ["Abbas Araghchi", "Steve Witkoff"]
    assert r.classifier == "llm:fake/fake-1"
    assert len(llm.calls) == 1


def test_classification_is_passed_through_not_ranked():
    r = LLMClassifier(FakeProvider(reply(event_type="commentary", concreteness="commentary",
                                    interaction_mode="none", is_routine_commentary=True,
                                    significance_class=None))).classify(MEETING)
    assert r.event_type == EventType.COMMENTARY
    assert r.is_routine_commentary
    assert r.significance_class is None


def test_context_flags_are_added_even_if_model_omits_them():
    ctx = make_context("Russia strikes Kharkiv", has_contradictions=True)
    r = LLMClassifier(FakeProvider(reply(event_type="military_action"))).classify(ctx)
    assert UncertaintyFlag.SINGLE_SOURCE in r.uncertainty_flags
    assert UncertaintyFlag.CONTRADICTORY_REPORTS in r.uncertainty_flags


def test_model_flags_are_kept_and_deduplicated():
    ctx = make_context("Russia strikes Kharkiv")
    r = LLMClassifier(FakeProvider(reply(uncertainty_flags=["single_source", "unconfirmed_completion"]))).classify(ctx)
    assert r.uncertainty_flags.count(UncertaintyFlag.SINGLE_SOURCE) == 1
    assert UncertaintyFlag.UNCONFIRMED_COMPLETION in r.uncertainty_flags


# --- prompt ------------------------------------------------------------------

def test_system_prompt_lists_every_allowed_value():
    prompt = build_system_prompt()
    assert "{{" not in prompt
    for enum in (EventType, InteractionMode, Concreteness, SignificanceClass, UncertaintyFlag):
        for member in enum:
            assert member.value in prompt


def test_request_contains_context_and_deterministic_settings():
    llm = FakeProvider(reply())
    LLMClassifier(llm).classify(MEETING)
    call = llm.calls[0]
    assert call["temperature"] == 0.0
    assert call["system"] == build_system_prompt()
    for item in MEETING.items:
        assert item.title in call["prompt"]
        assert item.source_name in call["prompt"]


def test_render_context_truncates_items():
    ctx = make_context(*[f"Headline {n}" for n in range(5)])
    text = render_context(ctx, max_items=2)
    assert "Headline 1" in text and "Headline 2" not in text
    assert "3 more items omitted" in text


# --- malformed output --------------------------------------------------------

@pytest.mark.parametrize("raw", [
    "```json\n" + reply() + "\n```",
    "Here is the classification:\n" + reply() + "\nHope this helps.",
])
def test_json_wrapped_in_text_is_accepted(raw):
    assert parse_classification(raw).event_type == EventType.BILATERAL_MEETING


@pytest.mark.parametrize("value", ["BILATERAL_MEETING", "Bilateral Meeting", "bilateral-meeting"])
def test_enum_spelling_variants_are_normalized(value):
    r = parse_classification(reply(event_type=value))
    assert r.event_type == EventType.BILATERAL_MEETING
    assert UncertaintyFlag.OUTPUT_REPAIRED not in r.uncertainty_flags


def test_invented_category_is_coerced_to_unknown_and_flagged():
    r = parse_classification(reply(event_type="phone_call", concreteness="very concrete"))
    assert r.event_type == EventType.UNKNOWN
    assert r.concreteness == Concreteness.UNKNOWN
    assert UncertaintyFlag.OUTPUT_REPAIRED in r.uncertainty_flags


def test_invalid_flag_and_significance_are_dropped():
    r = parse_classification(reply(uncertainty_flags=["vibes"], significance_class="huge"))
    assert r.significance_class is None
    assert r.uncertainty_flags == [UncertaintyFlag.OUTPUT_REPAIRED]


def test_loose_types_are_coerced():
    r = parse_classification(reply(actors="Xi Jinping", is_routine_commentary="true", location=42))
    assert r.actors == ["Xi Jinping"]
    assert r.is_routine_commentary is True
    assert r.location is None


@pytest.mark.parametrize("raw", ["not json at all", "[1, 2, 3]", '{"foo": 1}', '{"event_type": "summit"'])
def test_unusable_output_raises(raw):
    with pytest.raises(ClassificationError):
        parse_classification(raw)


def test_retry_once_then_succeed():
    llm = FakeProvider("garbage", reply())
    r = LLMClassifier(llm).classify(MEETING)
    assert r.event_type == EventType.BILATERAL_MEETING
    assert len(llm.calls) == 2
    assert UncertaintyFlag.CLASSIFIER_FALLBACK not in r.uncertainty_flags


def test_persistent_garbage_falls_back_to_rules():
    llm = FakeProvider("garbage", "[]")
    r = LLMClassifier(llm).classify(MEETING)
    assert len(llm.calls) == 2
    assert r.classifier.startswith("rules")
    assert r.event_type == EventType.BILATERAL_MEETING    # rules still classify the cluster
    assert UncertaintyFlag.CLASSIFIER_FALLBACK in r.uncertainty_flags


def test_provider_failure_falls_back():
    r = LLMClassifier(FakeProvider(RuntimeError("timeout"), RuntimeError("timeout"))).classify(MEETING)
    assert UncertaintyFlag.CLASSIFIER_FALLBACK in r.uncertainty_flags


def test_without_fallback_failure_raises():
    with pytest.raises(ClassificationError):
        LLMClassifier(FakeProvider("garbage", "garbage"), fallback=None).classify(MEETING)


# --- schema ------------------------------------------------------------------

def test_schema_rejects_values_outside_enums():
    with pytest.raises(ValidationError):
        DevelopmentClassification(event_type="phone_call")


def test_schema_normalizes_lists_and_location():
    r = DevelopmentClassification(actors=["Xi", "xi ", ""], location="  ",
                                  uncertainty_flags=["single_source", "single_source"])
    assert r.actors == ["Xi"]
    assert r.location is None
    assert r.uncertainty_flags == [UncertaintyFlag.SINGLE_SOURCE]
