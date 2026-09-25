"""Development classification: ClusterContext -> DevelopmentClassification.

Backends:
  rules  deterministic keyword classifier (default, free, offline)
  llm    any analysis.llm provider, falls back to rules on failure
  hybrid rules, and the LLM only for events the rules find ambiguous

Select with OSINT_CLASSIFIER_BACKEND; the LLM backend uses
OSINT_CLASSIFIER_LLM_PROVIDER / OSINT_CLASSIFIER_LLM_MODEL when set.
"""

from __future__ import annotations

from osint_monitor.core.config import get_settings
from osint_monitor.processors.classification.base import DevelopmentClassifier
from osint_monitor.processors.classification.hybrid import HybridClassifier
from osint_monitor.processors.classification.llm_classifier import ClassificationError, LLMClassifier
from osint_monitor.processors.classification.rules import RuleBasedClassifier

__all__ = [
    "ClassificationError",
    "DevelopmentClassifier",
    "HybridClassifier",
    "LLMClassifier",
    "RuleBasedClassifier",
    "get_classifier",
]


def get_classifier(backend: str | None = None) -> DevelopmentClassifier:
    settings = get_settings()
    backend = backend or settings.classifier_backend
    if backend == "rules":
        return RuleBasedClassifier()
    if backend in ("llm", "hybrid"):
        llm = LLMClassifier(
            provider=settings.classifier_llm_provider,
            model=settings.classifier_llm_model,
        )
        return llm if backend == "llm" else HybridClassifier(llm)
    raise ValueError(f"Unknown classifier backend: {backend!r}. Options: 'rules', 'llm', 'hybrid'")
