"""LLM arbiter for ambiguous situation assignments.

The model only chooses among existing candidate situations; it cannot create or
name situations. Anything that is not a candidate slug counts as "none".
"""

from __future__ import annotations

import json
import logging
import re
from typing import Sequence

from osint_monitor.analysis.llm import LLMProvider, get_llm
from osint_monitor.core.config import load_prompt
from osint_monitor.core.models import DevelopmentSignature, SituationProfile

logger = logging.getLogger(__name__)
_JSON_OBJECT = re.compile(r"\{.*\}", re.DOTALL)


def render_request(dev: DevelopmentSignature, candidates: Sequence[SituationProfile]) -> str:
    lines = [f"Development: {dev.title}"]
    if dev.actors:
        lines.append(f"Actors: {', '.join(dev.actors)}")
    if dev.region:
        lines.append(f"Region: {dev.region}")
    lines.append("\nCandidate situations:")
    for c in candidates:
        lines.append(f"- slug: {c.slug}\n  title: {c.title}\n  actors: {', '.join(c.primary_actors)}")
        if c.short_description:
            lines.append(f"  description: {c.short_description}")
    return "\n".join(lines)


def parse_choice(raw: str, candidates: Sequence[SituationProfile]) -> str | None:
    match = _JSON_OBJECT.search(raw or "")
    if not match:
        return None
    try:
        value = json.loads(match.group(0)).get("situation")
    except (json.JSONDecodeError, AttributeError):
        return None
    slugs = {c.slug for c in candidates}
    return value if isinstance(value, str) and value in slugs else None


class LLMSituationArbiter:
    def __init__(self, llm: LLMProvider | None = None, *, provider: str | None = None, model: str | None = None):
        self._llm = llm
        self._provider = provider
        self._model = model
        self._system = load_prompt("assign_situation")

    @property
    def llm(self) -> LLMProvider:
        if self._llm is None:
            kwargs = {"model": self._model} if self._model else {}
            self._llm = get_llm(self._provider, **kwargs)
        return self._llm

    def choose(self, development: DevelopmentSignature, candidates: Sequence[SituationProfile]) -> str | None:
        raw = self.llm.generate(render_request(development, candidates), system=self._system, temperature=0.0)
        choice = parse_choice(raw, candidates)
        if choice is None:
            logger.info("Situation arbiter chose none for event %s", development.event_id)
        return choice
