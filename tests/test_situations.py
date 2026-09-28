"""Situation grouping: joining, separation, canonical (non-duplicate) creation, updates."""

import json
from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from osint_monitor.core.config import SituationsConfig, load_situations_config
from osint_monitor.core.database import Entity, Event, EventEntity, Situation
from osint_monitor.core.models import (
    DevelopmentSignature, SituationMatchReason, SituationProfile, SituationStatus,
)
from osint_monitor.processors.actors import ActorNormalizer
from osint_monitor.processors.situations import (
    ActorCanonicalizer, LLMSituationArbiter, SituationGrouper, assign_situations, situation_overview,
)
from osint_monitor.processors.situations.arbiter import render_request
from osint_monitor.processors.situations.store import load_profiles, sync_seeds
from tests.helpers import FakeProvider

NOW = datetime(2026, 9, 24, 12, 0)
R = SituationMatchReason


@pytest.fixture(scope="module")
def config():
    return load_situations_config()


@pytest.fixture(scope="module")
def grouper(config):
    return SituationGrouper(config)


@pytest.fixture(scope="module")
def seeds(config):
    return [SituationProfile(slug=s.slug, title=s.title, region=s.region, primary_actors=s.primary_actors,
                             keywords=s.keywords, status=s.status) for s in config.situations]


def dev(title, *actors, id=None, region=None, hours_ago=1.0, embedding=None):
    return DevelopmentSignature(event_id=id, title=title, actors=list(actors), region=region,
                                occurred_at=NOW - timedelta(hours=hours_ago), embedding=embedding)


def slugs(assignments):
    return [a.slug for a in assignments]


# --- joining and separation --------------------------------------------------------------

def test_related_developments_join_the_same_situation(grouper, seeds):
    batch = [dev("US and Iran resume nuclear talks in Muscat", "USA", "Iran", id=1),
             dev("Iranian foreign minister meets US envoy again", "Iranian", "Washington", id=2),
             dev("Tehran rejects new US sanctions demand", "Tehran", "United States", id=3)]
    assignments, created = grouper.group(batch, seeds)
    assert slugs(assignments) == ["us-iran"] * 3
    assert not created
    assert R.ACTOR_OVERLAP in assignments[0].reasons and R.TOPIC_KEYWORDS in assignments[0].reasons


def test_unrelated_developments_stay_separate(grouper, seeds):
    batch = [dev("Russian drones strike Kyiv overnight", "Russia", "Ukraine", id=1),
             dev("US and Iran resume nuclear talks", "United States", "Iran", id=2),
             dev("Earthquake hits northern Japan", "Japan", id=3),
             dev("Putin hosts Xi for state visit", "Russia", "China", id=4)]
    assignments, created = grouper.group(batch, seeds)
    assert slugs(assignments) == ["russia-ukraine-war", "us-iran", None, None]
    assert not created


def test_mentioning_one_actor_is_not_enough(grouper, seeds):
    a = grouper.assign(dev("Iran hosts regional football championship", "Iran"), seeds)
    assert a.slug is None and a.reasons == [R.NO_MATCH]


def test_closed_situations_are_not_joined(grouper, seeds):
    closed = [s.model_copy(update={"status": SituationStatus.CLOSED}) if s.slug == "us-iran" else s for s in seeds]
    assert grouper.assign(dev("US and Iran resume nuclear talks", "United States", "Iran"), closed).slug is None


def test_semantic_similarity_separates_storylines_with_the_same_actors(config):
    a = SituationProfile(slug="us-iran-talks", title="Talks", primary_actors=["United States", "Iran"],
                         centroid=[1.0, 0.0])
    b = SituationProfile(slug="us-iran-maritime", title="Maritime", primary_actors=["United States", "Iran"],
                         centroid=[0.0, 1.0])
    g = SituationGrouper(config.model_copy(update={"situations": []}))
    near_b = dev("IRGC boats harass US destroyer", "Iran", "United States", embedding=[0.1, 0.99])
    result = g.assign(near_b, [a, b])
    assert result.slug == "us-iran-maritime"
    assert R.SEMANTIC_SIMILARITY in result.reasons


# --- canonical creation, no duplicates ---------------------------------------------------------

def test_recurring_actor_set_creates_one_canonical_situation(grouper, seeds):
    batch = [dev("Israel strikes air-defence sites in Iran", "Israel", "Iran", id=1, hours_ago=5),
             dev("Iran vows response to Israeli strikes", "Tehran", "Israeli", id=2, hours_ago=3),
             dev("Israeli and Iranian officials trade threats", "IDF", "Iranian", id=3, hours_ago=1)]
    assignments, created = grouper.group(batch, seeds)
    assert [c.slug for c in created] == ["iran-israel"]
    assert created[0].title == "Iran – Israel"
    assert slugs(assignments) == ["iran-israel"] * 3
    assert all(a.created and R.RECURRING_ACTORS in a.reasons for a in assignments)


def test_later_developments_join_the_created_situation_instead_of_duplicating(grouper, seeds):
    first, created = grouper.group([dev("Israel strikes Iran", "Israel", "Iran", id=1),
                                    dev("Iran answers Israel", "Iran", "Israel", id=2)], seeds)
    later, created_again = grouper.group([dev("Israel and Iran exchange fire again", "Israeli", "Iran", id=3)],
                                         seeds + created)
    assert slugs(later) == ["iran-israel"] and not later[0].created
    assert not created_again


def test_single_development_or_single_actor_does_not_create(grouper, seeds):
    one, created = grouper.group([dev("Israel strikes Iran", "Israel", "Iran")], seeds)
    assert slugs(one) == [None] and not created
    lone, created = grouper.group([dev("Japan passes defence budget", "Japan", id=1),
                                   dev("Japan launches new destroyer", "Japan", id=2)], seeds)
    assert slugs(lone) == [None, None] and not created


def test_no_new_situation_for_an_actor_set_that_already_has_one(config):
    seeded = SituationProfile(slug="us-iran", title="US–Iran", primary_actors=["United States", "Iran"],
                              region="iran", centroid=[1.0, 0.0])
    g = SituationGrouper(config)
    off_topic = [dev("US and Iran football teams draw", "USA", "Iran", id=i, region="sports", embedding=[0.0, 1.0])
                 for i in range(3)]
    assignments, created = g.group(off_topic, [seeded])
    assert not created                          # would have been a duplicate "Iran – United States"
    assert all(a.slug is None for a in assignments)


def test_canonical_slug_ignores_spelling_and_order(config):
    actors = ActorCanonicalizer(normalizer=ActorNormalizer.load())
    assert actors.slug(actors.keys(["USA", "Iranian"])) == actors.slug(actors.keys(["Tehran", "United States"]))


# --- ambiguous cases and the arbiter ------------------------------------------------------------

@pytest.fixture()
def twin_situations():
    return [SituationProfile(slug="us-iran-nuclear", title="US–Iran nuclear talks",
                             primary_actors=["United States", "Iran"]),
            SituationProfile(slug="us-iran-gulf", title="US–Iran Gulf incidents",
                             primary_actors=["United States", "Iran"])]


class ScriptedArbiter:
    def __init__(self, answer):
        self.answer, self.calls = answer, 0

    def choose(self, development, candidates):
        self.calls += 1
        return self.answer


def test_ambiguous_case_without_arbiter_stays_unassigned(config, twin_situations):
    a = SituationGrouper(config).assign(dev("US and Iran officials speak", "United States", "Iran"), twin_situations)
    assert a.slug is None and a.reasons == [R.AMBIGUOUS]
    assert set(a.candidates) == {"us-iran-nuclear", "us-iran-gulf"}


def test_arbiter_settles_ambiguous_case(config, twin_situations):
    arbiter = ScriptedArbiter("us-iran-gulf")
    a = SituationGrouper(config, arbiter).assign(dev("US and Iran officials speak", "United States", "Iran"),
                                                 twin_situations)
    assert a.slug == "us-iran-gulf" and R.ARBITER_CHOICE in a.reasons
    assert arbiter.calls == 1


def test_arbiter_cannot_invent_a_situation(config, twin_situations):
    a = SituationGrouper(config, ScriptedArbiter("us-iran-new-crisis")).assign(
        dev("US and Iran officials speak", "United States", "Iran"), twin_situations)
    assert a.slug is None and a.reasons == [R.AMBIGUOUS]


def test_arbiter_is_not_asked_about_clear_cases(grouper, seeds):
    arbiter = ScriptedArbiter("gaza-ceasefire")
    g = SituationGrouper(grouper.config, arbiter)
    assert g.assign(dev("US and Iran resume nuclear talks", "USA", "Iran"), seeds).slug == "us-iran"
    assert arbiter.calls == 0


def test_llm_arbiter_only_accepts_candidate_slugs(twin_situations):
    d = dev("US and Iran officials speak", "United States", "Iran")
    valid = FakeProvider(json.dumps({"situation": "us-iran-nuclear", "reason": "talks"}))
    assert LLMSituationArbiter(valid).choose(d, twin_situations) == "us-iran-nuclear"
    assert "us-iran-gulf" in valid.calls[0]["prompt"] and valid.calls[0]["temperature"] == 0.0
    for raw in ['{"situation": "iran-crisis-2026"}', '{"situation": "none"}', "no idea"]:
        assert LLMSituationArbiter(FakeProvider(raw)).choose(d, twin_situations) is None


def test_arbiter_request_lists_every_candidate(twin_situations):
    text = render_request(dev("x", "Iran"), twin_situations)
    assert all(s.slug in text for s in twin_situations)


# --- persistence ------------------------------------------------------------------------------

def add_event(session, title, *actors, hours_ago=1.0, region=None, principal=True, mentioned=()):
    """Event whose ``actors`` are principal (unless principal=False) plus incidental ``mentioned``."""
    event = Event(summary=title, region=region, first_reported_at=NOW - timedelta(hours=hours_ago),
                  last_updated_at=NOW - timedelta(hours=hours_ago))
    session.add(event)
    session.flush()
    for name, is_principal in [(a, principal) for a in actors] + [(m, False) for m in mentioned]:
        entity = session.query(Entity).filter_by(canonical_name=name).first()
        if entity is None:
            entity = Entity(canonical_name=name, entity_type="GPE")
            session.add(entity)
            session.flush()
        session.add(EventEntity(event_id=event.id, entity_id=entity.id, role="SUBJECT", is_principal=is_principal))
    session.commit()
    return event


def test_pipeline_stage_persists_assignments_and_is_idempotent(session, grouper):
    talks = add_event(session, "US and Iran resume nuclear talks", "United States", "Iran", hours_ago=3)
    quake = add_event(session, "Earthquake hits northern Japan", "Japan", hours_ago=2)
    strikes = [add_event(session, t, "Israel", "Iran", hours_ago=h)
               for t, h in [("Israel strikes Iran", 2), ("Iran answers Israel", 1)]]

    assign_situations(session, grouper, now=NOW)
    us_iran = session.query(Situation).filter_by(slug="us-iran").one()
    assert talks.situation_id == us_iran.id
    assert quake.situation_id is None
    assert strikes[0].situation_id == strikes[1].situation_id is not None

    count = session.query(Situation).count()
    assign_situations(session, grouper, now=NOW)
    assert session.query(Situation).count() == count            # no duplicates on re-run
    assert talks.situation_id == us_iran.id                     # never moved

    add_event(session, "Israel and Iran exchange fire again", "Israel", "Iran", hours_ago=0.5)
    assign_situations(session, grouper, now=NOW)
    assert session.query(Situation).filter_by(slug="iran-israel").count() == 1
    assert session.query(Event).filter_by(situation_id=strikes[0].situation_id).count() == 3


def test_new_development_updates_and_wakes_the_situation(session, grouper):
    sync_seeds(session, grouper.config, now=NOW - timedelta(days=30))
    situation = session.query(Situation).filter_by(slug="russia-ukraine-war").one()
    assign_situations(session, grouper, now=NOW - timedelta(days=15))
    assert situation.status == SituationStatus.DORMANT.value            # quiet for > 14 days

    add_event(session, "Russian drones strike Kyiv overnight", "Russia", "Ukraine", hours_ago=1)
    assign_situations(session, grouper, now=NOW)
    assert situation.status == SituationStatus.ACTIVE.value
    assert situation.updated_at == NOW - timedelta(hours=1)


def test_seed_sync_respects_yaml_closure_but_not_automatic_status(session, config):
    sync_seeds(session, config, now=NOW)
    row = session.query(Situation).filter_by(slug="sudan-civil-war").one()
    row.status = SituationStatus.DORMANT.value
    sync_seeds(session, config, now=NOW)
    assert row.status == SituationStatus.DORMANT.value                 # YAML 'active' does not override

    closed = config.model_copy(deep=True)
    next(s for s in closed.situations if s.slug == "sudan-civil-war").status = SituationStatus.CLOSED
    sync_seeds(session, closed, now=NOW)
    assert row.status == SituationStatus.CLOSED.value
    sync_seeds(session, config, now=NOW)
    assert row.status == SituationStatus.ACTIVE.value                  # reopened explicitly in YAML
    assert {p.slug for p in load_profiles(session, config)} >= {s.slug for s in config.situations}


def test_overview_answers_what_changed_recently(session, grouper):
    old = add_event(session, "US and Iran agree on talks venue", "United States", "Iran", hours_ago=24 * 10)
    old.last_updated_at = NOW - timedelta(days=10)
    session.commit()
    add_event(session, "US and Iran resume nuclear talks", "United States", "Iran", hours_ago=5)
    add_event(session, "Iran says nuclear talks were constructive", "Iran", "United States", hours_ago=2)
    assign_situations(session, grouper, now=NOW - timedelta(days=9))   # picks up the old one
    assign_situations(session, grouper, now=NOW)

    situation = session.query(Situation).filter_by(slug="us-iran").one()
    ov = situation_overview(session, situation.id, grouper.config, recent_days=7, now=NOW)
    assert ov.situation.title == situation.title and ov.situation.primary_actors == ["United States", "Iran"]
    assert ov.development_count == 3
    assert [d.title for d in ov.recent_developments] == [
        "Iran says nuclear talks were constructive", "US and Iran resume nuclear talks"]


# --- configuration -------------------------------------------------------------------------------

def test_config_rejects_duplicate_or_malformed_slugs(config):
    raw = config.model_dump(mode="json")
    seed = raw["situations"][0]
    with pytest.raises(ValidationError):
        SituationsConfig(**{**raw, "situations": raw["situations"] + [seed]})
    with pytest.raises(ValidationError):
        SituationsConfig(**{**raw, "situations": [{**seed, "slug": "US Iran!"}]})
