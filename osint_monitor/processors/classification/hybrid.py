"""Rules first; a model only for the cases the rules find ambiguous.

The rule classifier reports ambiguity when no rule matches at all, or when headlines
split evenly between two substantive types (e.g. two "sanctions" headlines and two
"summit" headlines). Those go to the LLM classifier; everything else keeps the free,
deterministic rule result. If the model fails, the LLM classifier's own fallback
returns the rule result flagged ``classifier_fallback``.
"""

from __future__ import annotations

from osint_monitor.core.models import ClusterContext, DevelopmentClassification
from osint_monitor.processors.classification.llm_classifier import LLMClassifier
from osint_monitor.processors.classification.rules import RuleBasedClassifier


class HybridClassifier:
    def __init__(self, llm: LLMClassifier, rules: RuleBasedClassifier | None = None):
        self.rules = rules or RuleBasedClassifier()
        self.model = llm
        if self.model.fallback is None or isinstance(self.model.fallback, RuleBasedClassifier):
            self.model.fallback = self.rules

    @property
    def llm(self):
        """The provider (raises when the LLM backend cannot be configured)."""
        return self.model.llm

    @property
    def name(self) -> str:
        return f"hybrid(rules+{self.model.name})"

    def classify(self, context: ClusterContext) -> DevelopmentClassification:
        result, ambiguous = self.rules.assess(context)
        if not ambiguous:
            return result
        return self.model.classify(context)
