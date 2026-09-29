"""Development summaries: what concretely happened, grounded only in the development's evidence.

Stored on the event (development_summary, summary_method, summary_model, summary_generated_at,
summary_item_ids) before anything is displayed; pages never generate text.

Evidence used: the development's own items that provenance classes as occurrence evidence
(primary, first-hand or independent reporting). Commentary, derivative copies and items whose
headline is analysis or live coverage are not used: they describe or repeat the occurrence.

Backends (OSINT_SUMMARY_BACKEND):

- ``extractive`` (default, deterministic): the lead sentence most central to the development's
  reports, plus at most one more from a different origin when it adds content. Sentences are
  taken verbatim from the reports, so nothing is added; headline repeats, questions, promotional
  lines and sentences naming the outlet itself are skipped.
- ``llm``: the existing LLM layer writes 1-3 sentences from those items only, with outside
  knowledge prohibited; any failure falls back to extractive.
- ``off``: no summaries.

No usable evidence -> no summary (summary_method "insufficient-evidence"), never the headline.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

import numpy as np
from rapidfuzz import fuzz
from sqlalchemy.orm import Session

from osint_monitor.core.database import Event, EventItem, RawItem

logger = logging.getLogger(__name__)

EXTRACTIVE = "extractive-leads-v1"
LLM = "llm"
INSUFFICIENT = "insufficient-evidence"
OCCURRENCE_EVIDENCE = {"primary", "firsthand", "independent"}
MIN_SENTENCE, MAX_SENTENCE, MAX_SUMMARY = 40, 320, 460
SECOND_SENTENCE_MAX_SIMILARITY = 0.85
SECOND_SENTENCE_MIN_CENTRALITY = 0.35

_SENTENCE_END = re.compile(r"(?<=[.!?])[\"'”’)]?\s+(?=[A-Z0-9“\"'‘(])"
                           r"|(?<=[a-z]{2}[.!?])(?=[A-Z](?:[a-z]|\.[A-Z]))")   # feeds glue description and body: "Iran.The", "Iran.U.S."
# Speculation and first/second-person voice mark commentary, not a report of what happened.
_NOT_OCCURRENCE = re.compile(r"\b(?:may|might)\b|(?:^|\s)(?:we|our|you|your)\s|\bwhat we\b", re.I)
_PROMO = re.compile(r"^(?:watch|listen|follow|live|click|sign up|subscribe|read more|here(?:'s| is| are)|in this|"
                    r"opinion|analysis|explainer|editor'?s note|advertisement)\b", re.I)


@dataclass
class Evidence:
    item_id: int
    source: str
    origin: str
    title: str
    text: str
    evidence_type: str


@dataclass
class Summary:
    text: str
    item_ids: list[int]
    method: str
    model: str | None = None


class Summarizer(Protocol):
    def summarize(self, headline: str, evidence: list[Evidence]) -> Summary | None: ...


# --- evidence ----------------------------------------------------------------------------------

def occurrence_evidence(session: Session, event_id: int) -> list[Evidence]:
    """The development's items that report the occurrence itself, with their provenance."""
    from osint_monitor.processors.development_segmentation import ANALYSIS, ROLLING, headline_kind
    from osint_monitor.processors.provenance import assess_event

    items = (session.query(RawItem).join(EventItem, EventItem.item_id == RawItem.id)
             .filter(EventItem.event_id == event_id).order_by(RawItem.published_at, RawItem.id).all())
    prov = {p.item_id: p for p in assess_event(session, event_id).items}
    out = []
    for i in items:
        p = prov.get(i.id)
        if p is None or p.evidence_type.value not in OCCURRENCE_EVIDENCE:
            continue
        if headline_kind(i.title or "") in (ANALYSIS, ROLLING):
            continue
        out.append(Evidence(item_id=i.id, source=i.source.name if i.source else "", origin=p.origin,
                            title=i.title or "", text=_clean(i.content), evidence_type=p.evidence_type.value))
    return out


def _clean(text: str | None) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = (text.replace("&#039;", "'").replace("&amp;", "&").replace("&quot;", '"')
            .replace("&#8217;", "’").replace("&nbsp;", " ").replace(" ", " ").replace("Â", ""))
    return " ".join(text.split())


def sentences(text: str, limit: int = 2) -> list[str]:
    return [s.strip() for s in _SENTENCE_END.split(text) if s.strip()][:limit]


# --- extractive --------------------------------------------------------------------------------

class ExtractiveSummarizer:
    """Lead sentences of the reports, selected by how central they are to the development."""

    def __init__(self, embed=None):
        self._embed = embed

    def _vectors(self, texts: list[str]) -> np.ndarray:
        if self._embed is None:
            from osint_monitor.processors.embeddings import embed_texts
            self._embed = embed_texts
        v = np.asarray(self._embed(texts), dtype=float)
        return v / np.maximum(np.linalg.norm(v, axis=1, keepdims=True), 1e-9)

    @staticmethod
    def _usable(sentence: str, ev: Evidence, headlines: list[str]) -> bool:
        s = sentence.strip()
        if not MIN_SENTENCE <= len(s) <= MAX_SENTENCE or s.endswith("?") or _PROMO.match(s):
            return False
        if _NOT_OCCURRENCE.search(s):
            return False                                   # speculation or the writer's own voice
        if any(fuzz.ratio(s.lower(), h.lower()) >= 85 for h in headlines):
            return False                                   # the headline again
        own = [w for w in re.split(r"\W+", ev.source) if len(w) > 2 and w.lower() not in {"world", "news", "the"}]
        return not any(re.search(rf"\b{re.escape(w)}\b", s) for w in own)   # "the BBC understands ..."

    def summarize(self, headline: str, evidence: list[Evidence]) -> Summary | None:
        headlines = [headline] + [e.title for e in evidence]
        candidates = [(s, e) for e in evidence for s in sentences(e.text) if self._usable(s, e, headlines)]
        if not candidates:
            return None
        vecs = self._vectors([s for s, _ in candidates] + [e.title for e in evidence])
        sent_v, head_v = vecs[:len(candidates)], vecs[len(candidates):]
        # central to the development: close to its reports' headlines and to the other leads
        centrality = (sent_v @ head_v.T).mean(axis=1)
        if len(candidates) > 1:
            sim = sent_v @ sent_v.T
            centrality = 0.5 * centrality + 0.5 * (sim.sum(axis=1) - 1) / (len(candidates) - 1)
        order = sorted(range(len(candidates)), key=lambda i: (-centrality[i], candidates[i][1].item_id))
        first = order[0]
        chosen = [first]
        seen = set(re.findall(r"[a-z]{4,}", candidates[first][0].lower()))
        for i in order[1:]:
            s, e = candidates[i]
            if e.origin == candidates[first][1].origin or centrality[i] < SECOND_SENTENCE_MIN_CENTRALITY:
                continue
            if float(sent_v[i] @ sent_v[first]) >= SECOND_SENTENCE_MAX_SIMILARITY:
                continue
            new = set(re.findall(r"[a-z]{4,}", s.lower())) - seen
            if len(new) >= 4 and len(candidates[first][0]) + 1 + len(s) <= MAX_SUMMARY:
                chosen.append(i)
            break
        text = " ".join(candidates[i][0] for i in chosen)
        return Summary(text=text, item_ids=[candidates[i][1].item_id for i in chosen], method=EXTRACTIVE)


# --- LLM ---------------------------------------------------------------------------------------

LLM_SYSTEM = (
    "You summarise one news development for an intelligence reader. Use ONLY the reports given. "
    "Do not add any fact, name, number, date, cause or context that is not stated in them; no outside "
    "knowledge. Write 1-3 plain factual sentences saying what concretely happened: who acted, what they "
    "did, the material outcome. No commentary, no significance, no prediction, no outlet names. Where "
    "reports disagree, say so neutrally. If the reports do not state a concrete occurrence, return an "
    "empty summary. Answer as JSON: {\"summary\": str, \"item_ids\": [ids of the reports you used]}."
)


class LLMSummarizer:
    """Evidence-only summary by the existing LLM layer; falls back to extractive on any failure."""

    def __init__(self, provider=None, provider_name: str | None = None, fallback: Summarizer | None = None):
        self._provider = provider
        self._name = provider_name
        self._fallback = fallback or ExtractiveSummarizer()

    def _llm(self):
        if self._provider is None:
            from osint_monitor.analysis.llm import get_llm
            self._provider = get_llm(self._name)
        return self._provider

    def summarize(self, headline: str, evidence: list[Evidence]) -> Summary | None:
        if not evidence:
            return None
        reports = "\n\n".join(f"[{e.item_id}] {e.title}\n{' '.join(sentences(e.text, 4))[:900]}" for e in evidence)
        try:
            llm = self._llm()
            raw = llm.generate(f"Reports:\n\n{reports}", system=LLM_SYSTEM, temperature=0.0)
            data = json.loads(raw[raw.index("{"): raw.rindex("}") + 1])
            text = " ".join(str(data.get("summary", "")).split())
            ids = [int(i) for i in data.get("item_ids", []) if int(i) in {e.item_id for e in evidence}]
            if not text:
                return None                                 # the model found no concrete occurrence
            model = f"{type(llm).__name__.removesuffix('Provider').lower()}/{getattr(llm, 'model', '?')}"
            return Summary(text=text, item_ids=ids or [e.item_id for e in evidence], method=LLM, model=model)
        except Exception as e:
            logger.warning(f"LLM summary failed ({e}); using the extractive summary")
            return self._fallback.summarize(headline, evidence)


def get_summarizer(backend: str | None = None) -> Summarizer | None:
    from osint_monitor.core.config import get_settings
    settings = get_settings()
    backend = backend or settings.summary_backend
    if backend == "off":
        return None
    if backend == "llm":
        return LLMSummarizer(provider_name=settings.summary_llm_provider or settings.default_llm_provider)
    return ExtractiveSummarizer()


# --- the pipeline stage --------------------------------------------------------------------------

def summarize_events(session: Session, summarizer: Summarizer | None = None, now: datetime | None = None) -> dict:
    """(Re)summarise events that are new or changed since their last summary. Idempotent."""
    summarizer = summarizer if summarizer is not None else get_summarizer()
    if summarizer is None:
        return {"summarized": 0, "insufficient": 0, "skipped": "off"}
    now = now or datetime.utcnow()
    stats = {"summarized": 0, "insufficient": 0}
    for event in session.query(Event).all():
        if event.summary_generated_at and event.last_updated_at and event.summary_generated_at >= event.last_updated_at:
            continue
        result = summarizer.summarize(event.summary or "", occurrence_evidence(session, event.id))
        event.summary_generated_at = now
        if result is None:
            event.development_summary, event.summary_method, event.summary_model = None, INSUFFICIENT, None
            event.summary_item_ids = []
            stats["insufficient"] += 1
        else:
            event.development_summary, event.summary_method = result.text, result.method
            event.summary_model, event.summary_item_ids = result.model, result.item_ids
            stats["summarized"] += 1
    session.commit()
    return stats
