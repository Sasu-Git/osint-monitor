"""Hybrid classifier: rules for clear cases, the model only for cases the rules find ambiguous."""

from osint_monitor.core.models import EventType, UncertaintyFlag
from osint_monitor.processors.classification import HybridClassifier, LLMClassifier, RuleBasedClassifier
from osint_monitor.processors.development import usable_classifier
from tests.helpers import FakeProvider, make_context

LLM_REPLY = ('{"event_type": "summit", "event_domain": "diplomacy", "interaction_mode": "physical", '
             '"concreteness": "action", "significance_class": null, "actors": [], "countries": [], '
             '"organizations": [], "location": null, "material_change": "Summit held.", "why_it_matters": "", '
             '"is_routine_commentary": false, "classification_notes": "summit headlines", "uncertainty_flags": []}')
AMBIGUOUS = ("Trump-Xi summit opens at the White House", "Summit day 1 highlights",
             "US imposes sanctions on Chinese chipmakers", "China sanctions US defence firms")


def test_hybrid_asks_the_model_only_when_the_rules_are_ambiguous():
    provider = FakeProvider(LLM_REPLY)
    hybrid = HybridClassifier(LLMClassifier(llm=provider))
    assert hybrid.classify(make_context("Russia strikes Kharkiv")).event_type == EventType.MILITARY_ACTION
    assert provider.calls == []
    assert hybrid.classify(make_context(*AMBIGUOUS)).event_type == EventType.SUMMIT
    assert len(provider.calls) == 1


def test_hybrid_keeps_the_rule_result_flagged_when_the_model_fails():
    hybrid = HybridClassifier(LLMClassifier(llm=FakeProvider(RuntimeError("down"), RuntimeError("down"))))
    r = hybrid.classify(make_context(*AMBIGUOUS))
    assert UncertaintyFlag.CLASSIFIER_FALLBACK in r.uncertainty_flags
    assert r.event_type == RuleBasedClassifier().classify(make_context(*AMBIGUOUS)).event_type


def test_hybrid_without_a_usable_model_runs_on_rules():
    hybrid = HybridClassifier(LLMClassifier(provider="no-such-provider"))
    assert isinstance(usable_classifier(hybrid), RuleBasedClassifier)
