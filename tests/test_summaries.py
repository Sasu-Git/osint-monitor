"""Development summaries (persisted, grounded in the development's own evidence) and evidence
grouping by provenance. Sources are real config/provenance.yaml entries: Reuters World (wire,
origin Reuters), BBC World (origin BBC), Defense.gov (primary official), @RALee85 (analysis)."""

import re
from datetime import datetime, timedelta

import numpy as np
import pytest

from osint_monitor.api.situation_views import (
    SourceEvidence, _canonicalizer, development_view, evidence_kind, group_evidence,
)
from osint_monitor.core.database import Event, EventItem, RawItem, Source
from osint_monitor.processors import summaries as S
from tests.test_situation_views import db  # noqa: F401  (file-backed DB fixture)

NOW = datetime(2026, 9, 29, 12, 0)
HEADLINE = "US grants Iraq waiver for Iranian electricity imports"


def bow(texts):
    """Deterministic stand-in for the embedding model: bag of words over a fixed vocabulary."""
    vocab = sorted({w for t in texts for w in re.findall(r"[a-z]+", t.lower())})
    index = {w: i for i, w in enumerate(vocab)}
    out = np.zeros((len(texts), max(1, len(vocab))))
    for r, t in enumerate(texts):
        for w in re.findall(r"[a-z]+", t.lower()):
            out[r, index[w]] += 1
    return out


def make_event(session, reports, headline=HEADLINE, hours_ago=1):
    """reports: (source name, title, content). Returns the event."""
    event = Event(summary=headline, first_reported_at=NOW - timedelta(hours=hours_ago),
                  last_updated_at=NOW - timedelta(hours=hours_ago))
    session.add(event)
    session.flush()
    for n, (name, title, content) in enumerate(reports):
        src = session.query(Source).filter_by(name=name).first()
        if src is None:
            src = Source(name=name, type="twitter" if name.startswith("@") else "rss", url=name, credibility_score=0.8)
            session.add(src)
            session.flush()
        item = RawItem(source_id=src.id, title=title, content=content, url=f"https://example.org/{event.id}/{n}",
                       content_hash=f"{event.id}-{n}", published_at=NOW - timedelta(hours=hours_ago, minutes=n),
                       fetched_at=NOW)
        session.add(item)
        session.flush()
        session.add(EventItem(event_id=event.id, item_id=item.id))
    session.commit()
    return event


WAIVER = [
    ("Reuters World", "US grants Iraq sanctions waiver on Iranian power",
     "The United States granted Iraq a 120-day waiver allowing it to keep paying Iran for electricity imports. "
     "The waiver extends an exemption from US sanctions that was due to expire on Friday."),
    ("BBC World", "Iraq can keep buying Iranian electricity, Washington says",
     "Washington renewed a waiver that lets Iraq continue importing electricity from Iran for another four months. "
     "Iraqi officials had warned of summer blackouts without the imports."),
]


def summarize(session, summarizer=None):
    return S.summarize_events(session, summarizer or S.ExtractiveSummarizer(embed=bow), now=NOW)


# --- summaries -----------------------------------------------------------------------------------

def test_summary_is_persisted_with_its_provenance(session):
    event = make_event(session, WAIVER)
    stats = summarize(session)
    session.refresh(event)
    assert stats["summarized"] == 1
    assert event.development_summary and event.summary_method == S.EXTRACTIVE
    assert event.summary_generated_at == NOW and event.summary_model is None
    item_ids = {ei.item_id for ei in session.query(EventItem).filter_by(event_id=event.id)}
    assert event.summary_item_ids and set(event.summary_item_ids) <= item_ids


def test_summary_states_the_occurrence_from_the_reports_not_the_headline(session):
    event = make_event(session, WAIVER)
    summarize(session)
    session.refresh(event)
    text = event.development_summary
    assert text != HEADLINE and HEADLINE.lower() not in text.lower()
    leads = " ".join(c for _, _, c in WAIVER)
    for sentence in re.split(r"(?<=\.)\s+", text):
        assert sentence in leads                       # verbatim from the evidence: nothing added
    assert "waiver" in text.lower()


def test_no_summary_is_invented_when_the_evidence_has_no_usable_lead(session):
    event = make_event(session, [("Reuters World", HEADLINE, HEADLINE), ("BBC World", "Iraq waiver", "")])
    stats = summarize(session)
    session.refresh(event)
    assert stats["insufficient"] == 1
    assert event.development_summary is None and event.summary_method == S.INSUFFICIENT
    assert event.summary != event.development_summary          # the headline is not copied in


def test_commentary_and_derivative_items_are_not_summary_evidence(session):
    event = make_event(session, [
        ("@RALee85", "What the Iraq waiver means for Tehran",
         "Analysts argue the waiver is a lifeline for Tehran's finances and will embolden it in the region."),
        ("BBC World", "Iraq keeps buying Iranian power (Reuters)",
         "BAGHDAD (Reuters) - The waiver lets Iraq keep importing Iranian electricity for four months, officials said."),
    ])
    evidence = S.occurrence_evidence(session, event.id)
    assert evidence == []                                      # analysis and a copied wire report only
    summarize(session)
    session.refresh(event)
    assert event.development_summary is None and event.summary_method == S.INSUFFICIENT


def test_summaries_are_recomputed_only_when_the_development_changes(session):
    event = make_event(session, WAIVER)
    summarize(session)
    assert summarize(session)["summarized"] == 0               # unchanged: idempotent
    event.last_updated_at = NOW + timedelta(minutes=5)
    session.commit()
    assert S.summarize_events(session, S.ExtractiveSummarizer(embed=bow), now=NOW + timedelta(minutes=10))["summarized"] == 1


class FakeLLM:
    model = "fake-1"

    def __init__(self, reply=None, fail=False):
        self.reply, self.fail, self.prompts = reply, fail, []

    def generate(self, prompt, system="", temperature=0.3):
        self.prompts.append((system, prompt))
        if self.fail:
            raise RuntimeError("provider down")
        return self.reply


def test_llm_summary_uses_only_the_developments_evidence_and_records_the_model(session):
    event = make_event(session, WAIVER)
    make_event(session, [("Reuters World", "Unrelated vote in Chile", "Chile's senate passed a pension bill.")],
               headline="Unrelated vote in Chile")
    ids = [ei.item_id for ei in session.query(EventItem).filter_by(event_id=event.id)]
    llm = FakeLLM(reply='{"summary": "The United States renewed a waiver letting Iraq import Iranian electricity.", '
                        f'"item_ids": [{ids[0]}]}}')
    S.summarize_events(session, S.LLMSummarizer(provider=llm), now=NOW)
    session.refresh(event)
    system, prompt = llm.prompts[0]
    assert "Use ONLY the reports given" in system and "no outside" in system.lower()
    assert "Chile" not in prompt and "120-day waiver" in prompt
    assert event.summary_method == S.LLM and event.summary_model == "fakellm/fake-1" and event.summary_item_ids == [ids[0]]


def test_llm_failure_falls_back_to_the_extractive_summary(session):
    event = make_event(session, WAIVER)
    S.summarize_events(session, S.LLMSummarizer(provider=FakeLLM(fail=True),
                                                fallback=S.ExtractiveSummarizer(embed=bow)), now=NOW)
    session.refresh(event)
    assert event.summary_method == S.EXTRACTIVE and event.development_summary


def test_llm_that_finds_no_occurrence_stores_no_summary(session):
    event = make_event(session, WAIVER)
    S.summarize_events(session, S.LLMSummarizer(provider=FakeLLM(reply='{"summary": "", "item_ids": []}')), now=NOW)
    session.refresh(event)
    assert event.development_summary is None and event.summary_method == S.INSUFFICIENT


# --- evidence grouping ---------------------------------------------------------------------------

def view(session, event):
    return development_view(session, event, _canonicalizer(), with_evidence=True)


def test_independent_origins_are_not_the_raw_item_count(session):
    event = make_event(session, [
        ("Reuters World", "US grants Iraq waiver", "WASHINGTON (Reuters) - The United States granted Iraq a waiver."),
        ("BBC World", "Iraq waiver renewed - Reuters", "BAGHDAD (Reuters) - Iraq will keep importing Iranian power."),
    ])
    v = view(session, event)
    assert v.counts.items == 2 and v.counts.independent_origins == 1
    kinds = {g.kind: g for g in v.evidence_groups}
    assert [o.origin for o in kinds["independent"].origins] == ["Reuters"]
    assert kinds["derivative"].origins[0].origin == "Reuters"         # grouped as a copy of Reuters
    assert v.counts.derivative_items == 1
    assert sum(g.item_count for g in v.evidence_groups) == 2          # no item disappears in grouping


def test_official_evidence_is_labelled_and_commentary_does_not_count(session):
    event = make_event(session, [
        ("Defense.gov", "Secretary announces new deployment", "The Department of Defense announced a deployment."),
        ("BBC World", "US to deploy more troops", "The Pentagon said more troops will be deployed to the region."),
        ("@RALee85", "Why this deployment matters", "This deployment signals a shift in posture, analysts say."),
    ])
    v = view(session, event)
    kinds = {g.kind: g for g in v.evidence_groups}
    assert "official" in kinds and v.counts.official_origins == 1
    assert "commentary" in kinds and v.counts.commentary_items == 1
    assert v.counts.independent_origins == 2                          # official + BBC; analysis is not confirmation


def test_items_without_assessed_provenance_are_shown_as_undetermined():
    e = SourceEvidence(item_id=1, source="Unknown Wire", title="Something happened")
    assert evidence_kind(e) == "undetermined"
    [group] = group_evidence([e])
    assert group.kind == "undetermined" and group.origins[0].items == [e]


def test_development_page_leads_with_summary_and_renders_groups_honestly(db):
    from fastapi.testclient import TestClient

    from osint_monitor.api.app import app
    make, _ = db
    session = make()
    event = make_event(session, WAIVER + [("@RALee85", "What the waiver means", "Analysts say it helps Tehran.")])
    summarize(session)
    session.refresh(event)
    summary, event_id = event.development_summary, event.id
    session.close()
    html = TestClient(app).get(f"/developments/{event_id}").text
    assert html.index(summary[:40]) < html.index("Evidence strength") < html.index("Supporting evidence")
    assert "independent origin" in html and "commentary, not counted" in html
    assert "Commentary and analysis" in html and "Used in summary" in html
    assert "lead sentences selected verbatim" in html               # provenance is inspectable


def test_feed_text_glued_without_a_space_still_splits_into_sentences():
    assert S.sentences(S._clean("Leaders met in Geneva.The summit ended without a deal."), 3) == [
        "Leaders met in Geneva.", "The summit ended without a deal."]
    assert S.sentences("Officials said the U.S. military struck. More followed.", 3)[0].startswith("Officials said the U.S.")
    assert S.sentences("used to strike Iran.U.S. officials confirmed it.", 3) == ["used to strike Iran.", "U.S. officials confirmed it."]


def test_speculative_or_first_person_sentences_are_not_summary_material():
    ev = S.Evidence(item_id=1, source="Reuters World", origin="Reuters", title="t", text="", evidence_type="independent")
    usable = lambda s: S.ExtractiveSummarizer._usable(s, ev, ["Headline"])      # noqa: E731
    assert not usable("The most revealing thing about the summit may be what the two leaders did not say.")
    assert not usable("What we still do not know is whether the ceasefire will hold at all.")
    assert usable("The mayor of Kyiv said three people were killed in the overnight strike on the city.")
