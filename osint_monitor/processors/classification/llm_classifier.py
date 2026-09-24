"""LLM-backed development classifier.

Provider-agnostic: works with any ``analysis.llm.LLMProvider``. The prompt lives in
``config/prompts/classify_development.md``; allowed values are injected from the
enums so the prompt can never drift from the schema.

Model output is untrusted: it is parsed leniently, invalid enum values are coerced
to ``unknown`` (flagged ``output_repaired``), unusable output is retried once and
then handed to the fallback classifier (flagged ``classifier_fallback``).
"""

from __future__ import annotations

import json
import logging
from enum import Enum
from typing import Any

from osint_monitor.analysis.llm import LLMProvider, get_llm
from osint_monitor.core.config import load_prompt
from osint_monitor.core.models import (
    ClusterContext,
    Concreteness,
    DevelopmentClassification,
    EventDomain,
    EventType,
    InteractionMode,
    SignificanceClass,
    UncertaintyFlag,
)
from osint_monitor.processors.classification.base import DevelopmentClassifier, context_flags
from osint_monitor.processors.classification.rules import RuleBasedClassifier

logger = logging.getLogger(__name__)

PROMPT_NAME = "classify_development"

_ENUM_FIELDS: dict[str, type[Enum]] = {
    "event_type": EventType,
    "event_domain": EventDomain,
    "interaction_mode": InteractionMode,
    "concreteness": Concreteness,
}
_LIST_FIELDS = ("actors", "countries", "organizations")
_TEXT_FIELDS = ("material_change", "why_it_matters", "classification_notes")

_DEFAULT_FALLBACK = object()


class ClassificationError(Exception):
    """Model output could not be turned into a classification."""


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

def build_system_prompt(template: str | None = None) -> str:
    template = template if template is not None else load_prompt(PROMPT_NAME)
    values = {
        "{{EVENT_TYPES}}": EventType,
        "{{EVENT_DOMAINS}}": EventDomain,
        "{{INTERACTION_MODES}}": InteractionMode,
        "{{CONCRETENESS}}": Concreteness,
        "{{SIGNIFICANCE_CLASSES}}": SignificanceClass,
        "{{UNCERTAINTY_FLAGS}}": UncertaintyFlag,
    }
    for placeholder, enum in values.items():
        template = template.replace(placeholder, ", ".join(e.value for e in enum))
    return template


def render_context(context: ClusterContext, max_items: int = 12, excerpt_chars: int = 600) -> str:
    """Render a cluster as plain text for the model. Deterministic."""
    items = context.items[:max_items]
    lines = [f"Development cluster: {len(context.items)} items from {len(context.distinct_sources)} sources."]
    if context.location_name:
        lines.append(f"Location detected: {context.location_name}")
    if context.entities:
        lines.append("Entities detected: " + ", ".join(f"{e.name} ({e.entity_type})" for e in context.entities))
    lines.append("")
    lines.append("Items:")
    for n, item in enumerate(items, 1):
        date = item.published_at.strftime("%Y-%m-%d %H:%M") if item.published_at else "undated"
        lines.append(f"[{n}] {date} | {item.source_name or 'unknown source'} | {item.title}")
        excerpt = " ".join(item.excerpt.split())[:excerpt_chars]
        if excerpt:
            lines.append(f"    {excerpt}")
    if len(context.items) > max_items:
        lines.append(f"({len(context.items) - max_items} more items omitted)")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Output parsing
# ---------------------------------------------------------------------------

def _extract_json_object(raw: str) -> dict[str, Any]:
    text = (raw or "").strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ClassificationError("no JSON object found")
    try:
        data = json.loads(text[start:end + 1])
    except json.JSONDecodeError as e:
        raise ClassificationError(f"invalid JSON: {e.msg}") from e
    if not isinstance(data, dict):
        raise ClassificationError("JSON is not an object")
    return data


def _coerce_enum(value: Any, enum: type[Enum]) -> Enum | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
    try:
        return enum(normalized)
    except ValueError:
        return None


def _coerce_str_list(value: Any) -> list[str] | None:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(v, str) for v in value):
        return value
    return None


def parse_classification(raw: str) -> DevelopmentClassification:
    """Turn raw model text into a validated classification.

    Raises ClassificationError when the output is unusable (no JSON object, or
    none of the categorical fields present). Invalid individual values are
    repaired and flagged instead of failing the whole result.
    """
    data = _extract_json_object(raw)
    if not any(field in data for field in _ENUM_FIELDS):
        raise ClassificationError("none of the categorical fields present")

    repaired: list[str] = []
    clean: dict[str, Any] = {}

    for field, enum in _ENUM_FIELDS.items():
        value = _coerce_enum(data.get(field), enum)
        if value is None:
            repaired.append(field)
            value = enum("unknown")
        clean[field] = value

    significance = data.get("significance_class")
    if significance is not None:
        clean["significance_class"] = _coerce_enum(significance, SignificanceClass)
        if clean["significance_class"] is None:
            repaired.append("significance_class")

    for field in _LIST_FIELDS:
        values = _coerce_str_list(data.get(field))
        if values is None:
            repaired.append(field)
            values = []
        clean[field] = values

    for field in _TEXT_FIELDS:
        value = data.get(field)
        clean[field] = value.strip() if isinstance(value, str) else ""

    location = data.get("location")
    clean["location"] = location if isinstance(location, str) else None

    routine = data.get("is_routine_commentary", False)
    if isinstance(routine, str):
        routine = routine.strip().lower() == "true"
    clean["is_routine_commentary"] = bool(routine)

    flags: list[UncertaintyFlag] = []
    for raw_flag in data.get("uncertainty_flags") or []:
        flag = _coerce_enum(raw_flag, UncertaintyFlag)
        if flag is None:
            repaired.append("uncertainty_flags")
        else:
            flags.append(flag)

    if repaired:
        flags.append(UncertaintyFlag.OUTPUT_REPAIRED)
        note = f"Repaired invalid model values: {', '.join(sorted(set(repaired)))}."
        clean["classification_notes"] = f"{clean['classification_notes']} {note}".strip()
    clean["uncertainty_flags"] = flags

    return DevelopmentClassification(**clean)


# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------

class LLMClassifier:
    """Classifies developments with any LLMProvider; falls back to rules on failure."""

    def __init__(
        self,
        llm: LLMProvider | None = None,
        *,
        provider: str | None = None,
        model: str | None = None,
        fallback: DevelopmentClassifier | None | object = _DEFAULT_FALLBACK,
        retries: int = 1,
        max_items: int = 12,
        excerpt_chars: int = 600,
        prompt_template: str | None = None,
    ):
        self._llm = llm
        self._provider = provider
        self._model = model
        self.fallback = RuleBasedClassifier() if fallback is _DEFAULT_FALLBACK else fallback
        self.retries = retries
        self.max_items = max_items
        self.excerpt_chars = excerpt_chars
        self._system_prompt = build_system_prompt(prompt_template)

    @property
    def llm(self) -> LLMProvider:
        if self._llm is None:
            kwargs = {"model": self._model} if self._model else {}
            self._llm = get_llm(self._provider, **kwargs)
        return self._llm

    @property
    def name(self) -> str:
        provider = type(self.llm).__name__.removesuffix("Provider").lower()
        return f"llm:{provider}/{getattr(self.llm, 'model', 'unknown')}"

    def classify(self, context: ClusterContext) -> DevelopmentClassification:
        prompt = render_context(context, self.max_items, self.excerpt_chars)
        error = ""
        for attempt in range(self.retries + 1):
            request = prompt if not error else (
                f"{prompt}\n\nYour previous reply was unusable ({error}). "
                "Reply with the JSON object only."
            )
            try:
                raw = self.llm.generate(request, system=self._system_prompt, temperature=0.0)
                result = parse_classification(raw)
            except ClassificationError as e:
                error = str(e)
                logger.warning("Classifier output unusable (attempt %d): %s", attempt + 1, error)
                continue
            except Exception as e:  # provider/network failure
                error = f"provider error: {e}"
                logger.warning("Classifier provider call failed (attempt %d): %s", attempt + 1, e)
                continue
            return _updated(
                result,
                uncertainty_flags=result.uncertainty_flags + context_flags(context),
                classifier=self.name,
            )
        return self._fall_back(context, error)

    def _fall_back(self, context: ClusterContext, error: str) -> DevelopmentClassification:
        if self.fallback is None:
            raise ClassificationError(error)
        result = self.fallback.classify(context)
        return _updated(
            result,
            uncertainty_flags=result.uncertainty_flags + [UncertaintyFlag.CLASSIFIER_FALLBACK],
            classification_notes=f"{result.classification_notes} (LLM failed: {error})".strip(),
            classifier=f"{self.fallback.name} (fallback)",
        )


def _updated(result: DevelopmentClassification, **changes: Any) -> DevelopmentClassification:
    """Copy with changes, re-running validators (model_copy would skip them)."""
    return DevelopmentClassification.model_validate({**result.model_dump(), **changes})
