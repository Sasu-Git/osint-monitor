"""Behaviour of the policy ranker: ordering relationships, not score values."""

import random
from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from osint_monitor.core.config import RankingConfig, load_ranking_config
from osint_monitor.core.models import (
    Concreteness, ConfidenceClass, DevelopmentClassification, DevelopmentStatus, EventType,
    InteractionMode, RankingInput, RankReason, RoleClass, SignificanceClass, UncertaintyFlag,
)
from osint_monitor.processors.ranking import DevelopmentRanker, PolicyRanker, get_ranker

NOW = datetime(2026, 9, 24, 12, 0)


@pytest.fixture(scope="module")
def ranker():
    return PolicyRanker()


def dev(event_type: EventType, *, id: int | None = None, mode=InteractionMode.NONE,
        concreteness=Concreteness.ACTION, significance=None, routine=False, flags=(),
        countries=(), organizations=(), roles=(), confidence=ConfidenceClass.PROBABLE,
        sources=2, hours_ago=1.0, **kwargs) -> RankingInput:
    return RankingInput(
        development_id=id,
        classification=DevelopmentClassification(
            event_type=event_type, interaction_mode=mode, concreteness=concreteness,
            significance_class=significance, is_routine_commentary=routine,
            uncertainty_flags=list(flags), countries=list(countries), organizations=list(organizations),
        ),
        actor_roles=list(roles), confidence=confidence, independent_sources=sources,
        occurred_at=NOW - timedelta(hours=hours_ago), **kwargs,
    )


def physical_meeting(**kw):
    return dev(EventType.BILATERAL_MEETING, mode=InteractionMode.PHYSICAL,
               roles=kw.pop("roles", [RoleClass.HEAD_OF_STATE]), countries=["France", "Germany"], **kw)


def spokesperson_comment(**kw):
    return dev(EventType.COMMENTARY, concreteness=Concreteness.COMMENTARY, routine=True,
               roles=[RoleClass.SPOKESPERSON], **kw)


def order(ranker, *devs):
    """development_ids, most important first."""
    return [r.development_id for r in ranker.rank(list(devs), now=NOW)]


def outranks(ranker, a: RankingInput, b: RankingInput) -> bool:
    a = a.model_copy(update={"development_id": 1})
    b = b.model_copy(update={"development_id": 2})
    return order(ranker, a, b) == [1, 2] and order(ranker, b, a) == [1, 2]


def test_satisfies_protocol(ranker):
    assert isinstance(ranker, DevelopmentRanker)
    assert isinstance(get_ranker(), PolicyRanker)


# --- meetings vs rhetoric ------------------------------------------------------

def test_physical_bilateral_beats_routine_spokesperson_comment(ranker):
    assert outranks(ranker, physical_meeting(), spokesperson_comment())


def test_physical_meeting_beats_phone_call_beats_statement(ranker):
    phone = dev(EventType.BILATERAL_MEETING, mode=InteractionMode.TELEPHONE, roles=[RoleClass.HEAD_OF_STATE])
    statement = dev(EventType.SIGNIFICANT_STATEMENT, concreteness=Concreteness.DECLARATION,
                    roles=[RoleClass.HEAD_OF_STATE])
    assert outranks(ranker, physical_meeting(), phone)
    assert outranks(ranker, phone, statement)


def test_statement_on_same_topic_as_meeting_is_overshadowed(ranker):
    statement = dev(EventType.SIGNIFICANT_STATEMENT, concreteness=Concreteness.DECLARATION,
                    roles=[RoleClass.FOREIGN_MINISTER], topic_key="iran-talks", id=2)
    alone = ranker.rank([statement], now=NOW)[0]
    with_meeting = ranker.rank([physical_meeting(topic_key="iran-talks", id=1), statement], now=NOW)
    assert [r.development_id for r in with_meeting] == [1, 2]
    assert with_meeting[1].score < alone.score
    assert RankReason.OVERSHADOWED_BY_CONCRETE in with_meeting[1].reasons


# --- consequential developments can outrank a meeting --------------------------

@pytest.mark.parametrize("consequential", [
    dev(EventType.TREATY, mode=InteractionMode.WRITTEN, concreteness=Concreteness.AGREEMENT,
        roles=[RoleClass.HEAD_OF_STATE]),
    dev(EventType.SANCTIONS, concreteness=Concreteness.DECISION, roles=[RoleClass.HEAD_OF_STATE]),
    dev(EventType.CEASEFIRE, concreteness=Concreteness.AGREEMENT, roles=[RoleClass.HEAD_OF_STATE]),
    dev(EventType.MILITARY_ACTION, concreteness=Concreteness.ACTION, roles=[RoleClass.HEAD_OF_STATE]),
    dev(EventType.POLICY_CHANGE, concreteness=Concreteness.DECISION, roles=[RoleClass.HEAD_OF_STATE]),
    dev(EventType.RESIGNATION, concreteness=Concreteness.DECISION, roles=[RoleClass.HEAD_OF_STATE]),
    dev(EventType.ELECTION, concreteness=Concreteness.ACTION, roles=[RoleClass.HEAD_OF_STATE]),
], ids=lambda d: d.classification.event_type.value)
def test_consequential_development_beats_physical_meeting(ranker, consequential):
    assert outranks(ranker, consequential, physical_meeting())


def test_signed_treaty_beats_physical_courtesy_meeting(ranker):
    treaty = dev(EventType.TREATY, mode=InteractionMode.WRITTEN, concreteness=Concreteness.AGREEMENT,
                 roles=[RoleClass.HEAD_OF_STATE])
    courtesy = physical_meeting(significance=SignificanceClass.BACKGROUND)
    assert outranks(ranker, treaty, courtesy)


# --- corroboration --------------------------------------------------------------

def test_confirmed_sanctions_beat_speculative_sanctions_report(ranker):
    confirmed = dev(EventType.SANCTIONS, concreteness=Concreteness.DECISION,
                    confidence=ConfidenceClass.CONFIRMED, sources=4)
    speculative = dev(EventType.SANCTIONS, concreteness=Concreteness.DECLARATION,
                      confidence=ConfidenceClass.UNVERIFIED, sources=1,
                      flags=[UncertaintyFlag.SINGLE_SOURCE, UncertaintyFlag.UNCONFIRMED_COMPLETION])
    assert outranks(ranker, confirmed, speculative)


@pytest.mark.parametrize("weaker, stronger", [
    ((ConfidenceClass.POSSIBLE, 1), (ConfidenceClass.PROBABLE, 2)),
    ((ConfidenceClass.PROBABLE, 2), (ConfidenceClass.CONFIRMED, 4)),
    ((ConfidenceClass.DISPUTED, 3), (ConfidenceClass.PROBABLE, 3)),
])
def test_identical_event_with_stronger_corroboration_ranks_higher(ranker, weaker, stronger):
    base = dict(concreteness=Concreteness.DECISION, roles=[RoleClass.FOREIGN_MINISTER])
    weak = dev(EventType.ECONOMIC_ACTION, confidence=weaker[0], sources=weaker[1], **base)
    strong = dev(EventType.ECONOMIC_ACTION, confidence=stronger[0], sources=stronger[1], **base)
    assert outranks(ranker, strong, weak)


# --- redundancy and novelty -----------------------------------------------------

def test_repeated_commentary_decays(ranker):
    comments = [spokesperson_comment(id=i, topic_key="hormuz", hours_ago=10 - i) for i in range(4)]
    ranked = {r.development_id: r for r in ranker.rank(comments, now=NOW)}
    scores = [ranked[i].score for i in range(4)]
    assert scores == sorted(scores, reverse=True) and len(set(scores)) == 4
    assert RankReason.DUPLICATE_COMMENTARY_PENALTY in ranked[3].reasons
    assert RankReason.DUPLICATE_COMMENTARY_PENALTY not in ranked[0].reasons


def test_repeats_from_earlier_batches_also_decay(ranker):
    first = spokesperson_comment(topic_key="hormuz")
    repeat = spokesperson_comment(topic_key="hormuz", prior_similar_count=3)
    assert outranks(ranker, first, repeat)


def test_major_policy_reversal_beats_repeated_summit_background_coverage(ranker):
    reversal = dev(EventType.POLICY_CHANGE, id=100, concreteness=Concreteness.DECISION,
                   significance=SignificanceClass.MAJOR, roles=[RoleClass.HEAD_OF_GOVERNMENT],
                   topic_key="us-tariffs", hours_ago=2)
    summit = [dev(EventType.SUMMIT, id=i, mode=InteractionMode.PHYSICAL,
                  significance=SignificanceClass.BACKGROUND, roles=[RoleClass.HEAD_OF_STATE],
                  organizations=["G20"], countries=["India", "Brazil", "South Africa"],
                  topic_key="g20-summit", hours_ago=8 - i)
              for i in range(5)]
    ranked = ranker.rank(summit + [reversal], now=NOW)
    ids = [r.development_id for r in ranked]
    assert all(ids.index(100) < ids.index(i) for i in range(1, 5))
    assert RankReason.REPEATED_COVERAGE_PENALTY in ranked[-1].reasons


def test_different_topics_do_not_count_as_repeats(ranker):
    a = physical_meeting(id=1, topic_key="iran-talks")
    b = physical_meeting(id=2, topic_key="ukraine-talks", hours_ago=0.5)
    ranked = ranker.rank([a, b], now=NOW)
    assert not any(RankReason.REPEATED_COVERAGE_PENALTY in r.reasons for r in ranked)


# --- lifecycle and recency ------------------------------------------------------

def test_fresh_development_beats_same_development_days_old(ranker):
    assert outranks(ranker, physical_meeting(hours_ago=2), physical_meeting(hours_ago=72))


def test_superseded_development_ranks_last(ranker):
    superseded = dev(EventType.MILITARY_ACTION, status=DevelopmentStatus.SUPERSEDED,
                     confidence=ConfidenceClass.CONFIRMED, sources=5)
    assert outranks(ranker, spokesperson_comment(), superseded)


def test_reopened_development_is_promoted(ranker):
    reopened = physical_meeting(status=DevelopmentStatus.DEVELOPING,
                                previous_status=DevelopmentStatus.CONCLUDED)
    steady = physical_meeting(status=DevelopmentStatus.DEVELOPING)
    assert outranks(ranker, reopened, steady)
    assert RankReason.STATUS_CHANGE in ranker.rank([reopened], now=NOW)[0].reasons


# --- determinism and explainability ---------------------------------------------

def test_ranking_is_deterministic_regardless_of_input_order(ranker):
    devs = [physical_meeting(id=1), spokesperson_comment(id=2),
            dev(EventType.TREATY, id=3, concreteness=Concreteness.AGREEMENT),
            dev(EventType.SANCTIONS, id=4, concreteness=Concreteness.DECISION),
            physical_meeting(id=5)]   # exact tie with 1: broken by id
    expected = order(ranker, *devs)
    rng = random.Random(7)
    for _ in range(10):
        shuffled = devs[:]
        rng.shuffle(shuffled)
        assert order(ranker, *shuffled) == expected
    assert expected.index(1) < expected.index(5)


def test_reasons_explain_the_ranking(ranker):
    top, bottom = ranker.rank([
        physical_meeting(confidence=ConfidenceClass.CONFIRMED, sources=4),
        spokesperson_comment(),
    ], now=NOW)
    assert {RankReason.PHYSICAL_INTERACTION, RankReason.SENIOR_ACTOR,
            RankReason.INDEPENDENTLY_CONFIRMED} <= set(top.reasons)
    assert RankReason.ROUTINE_COMMENTARY in bottom.reasons
    assert RankReason.PHYSICAL_INTERACTION not in bottom.reasons


def test_explanation_is_short_and_has_no_numbers(ranker):
    top = ranker.rank([physical_meeting(confidence=ConfidenceClass.CONFIRMED, sources=5)], now=NOW)[0]
    text = ranker.explain(top.reasons)
    assert text and not any(ch.isdigit() for ch in text)
    assert text.count(";") <= 1


def test_zero_weight_reasons_are_not_reported():
    cfg = load_ranking_config().model_copy(deep=True)
    cfg.interaction_mode_weights[InteractionMode.PHYSICAL] = 0
    top = PolicyRanker(cfg).rank([physical_meeting()], now=NOW)[0]
    assert RankReason.PHYSICAL_INTERACTION not in top.reasons


# --- configuration ---------------------------------------------------------------

def test_every_reason_has_a_label():
    assert set(load_ranking_config().reason_labels) == set(RankReason)


def test_config_changes_the_policy():
    cfg = load_ranking_config().model_copy(deep=True)
    comment, meeting = spokesperson_comment(), physical_meeting()
    assert outranks(PolicyRanker(cfg), meeting, comment)
    cfg.event_type_weights[EventType.COMMENTARY] = 100
    assert outranks(PolicyRanker(cfg), comment, meeting)


def test_config_rejects_unknown_or_missing_keys():
    raw = load_ranking_config().model_dump(mode="json")
    with pytest.raises(ValidationError):
        RankingConfig(**{**raw, "interaction_mode_weights": {"telepathy": 5}})
    with pytest.raises(ValidationError):
        RankingConfig(**{**raw, "event_type_weights": {"treaty": 10}})
    with pytest.raises(ValidationError):
        RankingConfig(**{**raw, "status_transition_weights": {"emerging=>developing": 1}})
