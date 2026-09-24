"""Classification and ranking as pipeline stages: persistence, failure handling, ordering."""

from datetime import datetime, timedelta

import pytest

from osint_monitor.analysis.llm import LLMConfigurationError
from osint_monitor.core.database import Entity, Event, EventEntity, EventItem, RawItem, Source
from osint_monitor.core.models import DevelopmentClassification, EventType, RankReason
from osint_monitor.processors.classification import LLMClassifier, RuleBasedClassifier
from osint_monitor.processors.development import classify_events, rank_events, usable_classifier

NOW = datetime(2026, 9, 24, 12, 0)


def add_event(session, *titles, hours_ago=1.0, sources=None, principals=()):
    sources = sources or [f"Outlet {i}" for i in range(len(titles))]
    event = Event(summary=titles[0], first_reported_at=NOW - timedelta(hours=hours_ago),
                  last_updated_at=NOW - timedelta(hours=hours_ago), source_count=len(set(sources)))
    session.add(event)
    session.flush()
    for n, (title, name) in enumerate(zip(titles, sources)):
        src = session.query(Source).filter_by(name=name).first() or Source(name=name, type="rss", url=name)
        session.add(src)
        session.flush()
        item = RawItem(source_id=src.id, title=title, content="", content_hash=f"{event.id}-{n}")
        session.add(item)
        session.flush()
        session.add(EventItem(event_id=event.id, item_id=item.id))
    for name, etype in principals:
        ent = session.query(Entity).filter_by(canonical_name=name).first() or Entity(canonical_name=name, entity_type=etype)
        session.add(ent)
        session.flush()
        session.add(EventEntity(event_id=event.id, entity_id=ent.id, role="SUBJECT", is_principal=True))
    session.commit()
    return event


# --- classification ------------------------------------------------------------------------

def test_classification_persists_structured_fields(session):
    event = add_event(session, "Putin meets Xi in Beijing", "Putin and Xi hold talks in Beijing")
    stats = classify_events(session, RuleBasedClassifier(), now=NOW)
    assert stats["classified"] == 1
    assert event.event_type == EventType.BILATERAL_MEETING.value
    assert event.interaction_mode == "physical" and event.concreteness == "action"
    assert event.classification_source == "rules" and event.classified_at == NOW
    assert isinstance(event.uncertainty_flags, list)


def test_only_new_or_changed_events_are_reclassified(session):
    event = add_event(session, "Putin meets Xi in Beijing")
    classify_events(session, RuleBasedClassifier(), now=NOW)
    assert classify_events(session, RuleBasedClassifier(), now=NOW)["candidates"] == 0
    event.last_updated_at = NOW + timedelta(minutes=5)
    session.commit()
    assert classify_events(session, RuleBasedClassifier(), now=NOW + timedelta(minutes=10))["classified"] == 1


def test_reclustering_the_same_items_does_not_mark_the_event_changed(session):
    from osint_monitor.processors.clustering import persist_clusters

    event = add_event(session, "Putin meets Xi in Beijing", "Putin and Xi hold talks in Beijing")
    item_ids = [ei.item_id for ei in session.query(EventItem).filter_by(event_id=event.id)]
    classify_events(session, RuleBasedClassifier(), now=NOW)
    before = event.last_updated_at
    assert persist_clusters(session, [{"item_ids": item_ids, "summary": "x"}]) == 0
    assert event.last_updated_at == before
    assert classify_events(session, RuleBasedClassifier(), now=NOW)["candidates"] == 0


class FlakyClassifier:
    name = "flaky"

    def __init__(self, fail_on: set[str]):
        self.fail_on = fail_on

    def classify(self, context):
        if context.items[0].title in self.fail_on:
            raise RuntimeError("model exploded")
        return RuleBasedClassifier().classify(context)


def test_one_failing_event_does_not_stop_the_stage(session):
    bad = add_event(session, "Unparseable story")
    good = add_event(session, "Putin meets Xi in Beijing")
    stats = classify_events(session, FlakyClassifier({"Unparseable story"}), now=NOW)
    assert (stats["classified"], stats["failed"]) == (1, 1)
    assert bad.classified_at is None and bad.event_type is None      # left unclassified, not guessed
    assert good.classified_at == NOW


def test_stage_fails_visibly_when_nothing_can_be_classified(session):
    add_event(session, "Unparseable story")
    with pytest.raises(RuntimeError, match="classification failed"):
        classify_events(session, FlakyClassifier({"Unparseable story"}), now=NOW)


def test_llm_backend_without_key_falls_back_to_rules(monkeypatch):
    clf = LLMClassifier(provider="openai")
    monkeypatch.setattr(type(clf), "llm", property(lambda self: (_ for _ in ()).throw(LLMConfigurationError("no key"))))
    assert isinstance(usable_classifier(clf), RuleBasedClassifier)


# --- ranking ------------------------------------------------------------------------------------

def test_ranking_persists_and_orders_concrete_action_above_routine_commentary(session):
    meeting = add_event(session, "Putin meets Xi in Beijing", "Putin and Xi hold talks in Beijing")
    comment = add_event(session, "Spokesperson says ministry is closely following the situation")
    classify_events(session, RuleBasedClassifier(), now=NOW)
    stats = rank_events(session, now=NOW)
    assert stats["ranked"] == 2
    assert meeting.rank_score > comment.rank_score
    assert meeting.ranked_at == NOW and isinstance(meeting.rank_reasons, list)
    assert RankReason.PHYSICAL_INTERACTION.value in meeting.rank_reasons


def test_unclassified_events_are_ranked_without_crashing(session):
    event = add_event(session, "Something happened")
    stats = rank_events(session, now=NOW)
    assert stats == {"ranked": 1, "unclassified_ranked": 1}
    assert event.rank_score is not None


def test_known_principal_leader_counts_as_senior_actor(session):
    event = add_event(session, "Putin meets Xi in Beijing", principals=[("Xi Jinping", "PERSON"), ("China", "GPE")])
    classify_events(session, RuleBasedClassifier(), now=NOW)
    rank_events(session, now=NOW)
    assert RankReason.SENIOR_ACTOR.value in event.rank_reasons


def test_events_outside_the_window_are_not_reranked(session):
    old = add_event(session, "Putin meets Xi in Beijing", hours_ago=24 * 30)
    assert rank_events(session, now=NOW)["ranked"] == 0
    assert old.rank_score is None
