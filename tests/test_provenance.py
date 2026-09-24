"""Source provenance and confidence: independence of origins, not outlet counts."""

from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from osint_monitor.core.config import ProvenanceConfig, load_provenance_config
from osint_monitor.core.database import Claim, Event, EventItem, RawItem, Source
from osint_monitor.core.models import (
    ConfidenceClass, DevelopmentClassification, EventType, EvidenceItem, EvidenceType,
    ItemStance, ProvenanceFlag, RankingInput, RankReason, SignificanceClass, SourceRole,
)
from osint_monitor.processors.corroboration import compute_corroboration_score
from osint_monitor.processors.provenance import ProvenanceResolver, assess_confidence, build_evidence
from osint_monitor.processors.ranking import PolicyRanker

T0 = datetime(2026, 9, 24, 8, 0)
BODY = ("Iran's foreign minister and the US special envoy met in Muscat on Tuesday with Omani "
        "mediation, the first in-person round of talks since June, officials from both sides said. "
        "The meeting lasted three hours and ended without a joint statement, but both delegations "
        "agreed to meet again, according to people briefed on the discussions.")


@pytest.fixture(scope="module")
def resolver():
    return ProvenanceResolver()


def item(source, title="Iran and US envoys meet in Muscat", text="", *, category=None,
         collector="rss", hours=0.0, stance=ItemStance.SUPPORTS, item_id=None) -> EvidenceItem:
    return EvidenceItem(item_id=item_id, source_name=source, source_category=category, collector_type=collector,
                        title=title, text=text, published_at=T0 + timedelta(hours=hours), stance=stance)


def news(source, **kw):
    return item(source, category="news", **kw)


def assess(resolver, *items):
    return assess_confidence(list(items), resolver)


# --- independence ---------------------------------------------------------------

def test_two_genuinely_independent_confirmations(resolver):
    a = assess(resolver, news("BBC World", text="Our correspondent in Muscat saw both delegations arrive."),
               news("Al Jazeera", text="Omani officials told Al Jazeera the talks lasted three hours."))
    assert a.independent_origins == 2
    assert a.confidence_class == ConfidenceClass.PROBABLE
    assert ProvenanceFlag.DERIVATIVE_COLLAPSED not in a.flags
    assert ProvenanceFlag.SINGLE_ORIGIN not in a.flags


def test_official_source_plus_wire_is_confirmed(resolver):
    a = assess(resolver,
               item("State Department", title="Special Envoy's meeting with Iranian Foreign Minister", category="us_gov"),
               item("Reuters World", title="Iran, US envoys hold rare talks in Muscat",
                    text="MUSCAT (Reuters) - Iranian and US envoys met on Tuesday...", category="news"))
    assert a.confidence_class == ConfidenceClass.CONFIRMED
    assert ProvenanceFlag.PRIMARY_SOURCE in a.flags
    evidence = {p.source_name: p.evidence_type for p in a.items}
    assert evidence == {"State Department": EvidenceType.PRIMARY, "Reuters World": EvidenceType.INDEPENDENT}


def test_five_derivative_reports_from_one_wire_count_once(resolver):
    outlets = ["BBC World", "Al Jazeera", "South China Morning Post", "Defense News", "Daily Blog"]
    derivative = [news(o, text=f"MUSCAT (Reuters) - Iranian and US envoys met on Tuesday. [{o}]", hours=i + 1)
                  for i, o in enumerate(outlets)]
    a = assess(resolver, *derivative)
    assert a.independent_origins == 1
    assert [o.origin for o in a.origins] == ["Reuters"]
    assert a.origins[0].sources == outlets
    assert a.confidence_class == ConfidenceClass.POSSIBLE
    assert {ProvenanceFlag.DERIVATIVE_COLLAPSED, ProvenanceFlag.SINGLE_ORIGIN} <= set(a.flags)
    assert all(p.evidence_type == EvidenceType.DERIVATIVE and p.derived_from == "Reuters" for p in a.items)

    # the wire's own item joins the same origin
    with_wire = assess(resolver, news("Reuters World", text="MUSCAT (Reuters) - ..."), *derivative)
    assert with_wire.independent_origins == 1

    # the same five outlets reporting on their own would confirm it
    own = assess(resolver, *[news(o, text=f"{o} own reporting") for o in outlets])
    assert own.confidence_class == ConfidenceClass.CONFIRMED


@pytest.mark.parametrize("text, origin", [
    ("The two sides met for three hours, according to Reuters.", "Reuters"),
    ("An Omani official told Reuters the talks would continue.", "Reuters"),
    ("The envoys met, the Associated Press reported.", "Associated Press"),
    ("Citing AP, the ministry said a second round is planned.", "Associated Press"),
    ("Details were first reported via AFP.", "AFP"),
    ("A statement carried by state media, according to IRNA, confirmed the meeting.", "IRNA"),
])
def test_attribution_is_detected(resolver, text, origin):
    p = resolver.resolve([news("Some Outlet", text=text)])[0]
    assert p.evidence_type == EvidenceType.DERIVATIVE
    assert p.origin == origin


def test_title_suffix_attribution(resolver):
    p = resolver.resolve([news("Yahoo News", title="Iran and US envoys meet in Muscat - Reuters")])[0]
    assert p.origin == "Reuters"


@pytest.mark.parametrize("text", [
    "Officials said the app would map the route.",           # 'ap' inside words
    "according to ap sources close to the talks",             # lowercase: not the agency
    "Reuters is a news agency.",                              # mention, not attribution
])
def test_no_false_attribution(resolver, text):
    p = resolver.resolve([news("Some Outlet", text=text)])[0]
    assert p.evidence_type == EvidenceType.INDEPENDENT
    assert p.origin == "Some Outlet"


def test_outlet_citing_itself_is_not_derivative(resolver):
    p = resolver.resolve([news("Reuters World", text="MUSCAT (Reuters) - envoys met.")])[0]
    assert p.evidence_type == EvidenceType.INDEPENDENT and p.origin == "Reuters"


def test_syndicated_copy_without_attribution_collapses(resolver):
    a = assess(resolver, news("Outlet A", text=BODY, hours=0),
               news("Outlet B", text=BODY.replace("Tuesday", "Tuesday,"), hours=2))
    assert a.independent_origins == 1
    assert ProvenanceFlag.SYNDICATED_COPY in a.flags
    assert a.items[1].origin == "Outlet A"


def test_similar_but_independent_stories_do_not_collapse(resolver):
    other = ("Oman hosted a meeting between Iranian and American negotiators in its capital, "
             "diplomats said, describing a cautious session focused on sequencing sanctions relief "
             "against nuclear limits. No joint communique followed, and neither side announced a date.")
    a = assess(resolver, news("Outlet A", text=BODY), news("Outlet B", text=other, hours=1))
    assert a.independent_origins == 2


def test_think_tanks_citing_one_primary_report_add_no_confidence(resolver):
    official = item("State Department", title="Readout of the Special Envoy's meeting", category="us_gov")
    think_tanks = [item(s, title=f"What the Muscat talks mean ({s})", text="According to the State Department readout...",
                        category="analysis", hours=i + 1)
                   for i, s in enumerate(["CSIS", "War on the Rocks", "Lawfare"])]
    alone = assess(resolver, official)
    with_analysis = assess(resolver, official, *think_tanks)
    assert with_analysis.confidence_class == alone.confidence_class
    assert with_analysis.independent_origins == alone.independent_origins == 1

    only_analysis = assess(resolver, *think_tanks)
    assert only_analysis.confidence_class == ConfidenceClass.UNVERIFIED
    assert ProvenanceFlag.COMMENTARY_ONLY in only_analysis.flags


def test_firsthand_reporting_is_labelled(resolver):
    p = resolver.resolve([news("BBC World", text="Our correspondent at the scene counted six vehicles.")])[0]
    assert p.evidence_type == EvidenceType.FIRSTHAND


# --- contradiction and single sources ---------------------------------------------

def test_conflicting_official_statements_are_disputed(resolver):
    a = assess(resolver,
               item("Defense.gov", title="US forces struck IRGC drone site", category="us_gov"),
               item("Iran MFA", title="Iran denies any strike took place", category="official",
                    stance=ItemStance.DENIES, hours=1),
               news("BBC World", title="US says it struck Iranian drone site", hours=2))
    assert a.confidence_class == ConfidenceClass.DISPUTED
    assert {ProvenanceFlag.DENIED, ProvenanceFlag.CONFLICTING_OFFICIAL_STATEMENTS} <= set(a.flags)


def test_single_reliable_source_is_possible(resolver):
    a = assess(resolver, news("BBC World"))
    assert a.confidence_class == ConfidenceClass.POSSIBLE
    assert ProvenanceFlag.SINGLE_ORIGIN in a.flags


def test_single_social_post_is_unverified(resolver):
    a = assess(resolver, item("@random_account", collector="twitter"))
    assert a.confidence_class == ConfidenceClass.UNVERIFIED
    assert {ProvenanceFlag.SINGLE_ORIGIN, ProvenanceFlag.LOW_RELIABILITY_ONLY} <= set(a.flags)


def test_unknown_provenance_is_exposed_not_trusted(resolver):
    a = assess(resolver, item("Mystery Feed", collector="custom"), item("Other Mystery", collector="custom", hours=1))
    assert ProvenanceFlag.PROVENANCE_UNKNOWN in a.flags
    assert a.reliable_origins == 0
    assert a.confidence_class == ConfidenceClass.POSSIBLE      # two origins, neither reliable
    assert all("unknown" in p.note for p in a.items)


# --- corrections / retractions --------------------------------------------------------

def test_wire_retraction_withdraws_all_its_derivatives(resolver):
    derivative = [news(o, text="MUSCAT (Reuters) - envoys met.", hours=1) for o in ["BBC World", "Al Jazeera"]]
    retraction = news("Reuters World", title="Reuters retracts story on Muscat meeting",
                      text="Reuters has withdrawn its report that envoys met in Muscat.", hours=5)
    a = assess(resolver, news("Reuters World", text="MUSCAT (Reuters) - envoys met."), *derivative, retraction)
    assert a.confidence_class == ConfidenceClass.UNVERIFIED
    assert ProvenanceFlag.FULLY_RETRACTED in a.flags
    assert a.independent_origins == 0


def test_retraction_by_one_origin_leaves_the_others(resolver):
    a = assess(resolver,
               news("BBC World", text="Our correspondent saw the delegations."),
               news("Al Jazeera", text="Omani officials confirmed the meeting."),
               news("Al Jazeera", title="Correction: Al Jazeera retracts report", hours=3))
    assert a.independent_origins == 1
    assert ProvenanceFlag.RETRACTED in a.flags
    assert a.confidence_class == ConfidenceClass.POSSIBLE


@pytest.mark.parametrize("title", [
    "Russia retracted its offer of a prisoner exchange",
    "Iran says the strike did not happen",
])
def test_news_about_withdrawals_is_not_a_retraction(resolver, title):
    assert resolver.resolve([news("BBC World", title=title)])[0].stance == ItemStance.SUPPORTS


def test_official_denial_stays_a_denial(resolver):
    denial = item("Iran MFA", title="Report retracted? No: the strike did not happen", category="official",
                  stance=ItemStance.DENIES)
    assert resolver.resolve([denial])[0].stance == ItemStance.DENIES


# --- confidence stays separate from significance ------------------------------------

def test_high_significance_with_low_confidence_is_representable(resolver):
    a = assess(resolver, item("@random_account", title="Reports of a strike on a nuclear site", collector="twitter"))
    assert a.confidence_class == ConfidenceClass.UNVERIFIED
    critical = DevelopmentClassification(event_type=EventType.MILITARY_ACTION,
                                         significance_class=SignificanceClass.CRITICAL)
    ranked = PolicyRanker().rank([RankingInput(classification=critical, confidence=a.confidence_class,
                                               independent_sources=a.independent_origins)])[0]
    assert RankReason.HIGH_SIGNIFICANCE in ranked.reasons
    assert RankReason.INDEPENDENTLY_CONFIRMED not in ranked.reasons
    assert not hasattr(a, "significance_class")


# --- database integration ---------------------------------------------------------------

def _event_with_items(session, rows):
    event = Event(summary="Envoys meet in Muscat")
    session.add(event)
    session.flush()
    for n, (source_name, text) in enumerate(rows):
        src = session.query(Source).filter_by(name=source_name).first()
        if not src:
            src = Source(name=source_name, type="rss", url=f"https://{n}.example")
            session.add(src)
            session.flush()
        ri = RawItem(source_id=src.id, title="Envoys meet in Muscat", content=text, content_hash=f"h{n}",
                     published_at=T0 + timedelta(hours=n))
        session.add(ri)
        session.flush()
        session.add(EventItem(event_id=event.id, item_id=ri.id))
    session.commit()
    return event


def test_corroboration_counts_origins_not_outlets(session):
    rows = [(o, "MUSCAT (Reuters) - envoys met.") for o in
            ["BBC World", "Al Jazeera", "South China Morning Post", "Defense News", "Daily Blog"]]
    event = _event_with_items(session, rows)
    result = compute_corroboration_score(session, event.id)
    assert result["outlets"] == 5
    assert result["independent_sources"] == 1
    assert result["corroboration_level"] != "CONFIRMED"
    assert result["confidence_class"] == "possible"
    assert "derivative_collapsed" in result["provenance_flags"]


def test_build_evidence_uses_feed_category_and_denial_claims(session):
    event = _event_with_items(session, [("BBC World", "Envoys met."), ("State Department", "No meeting took place.")])
    denial_item = session.query(RawItem).filter_by(content="No meeting took place.").one()
    session.add(Claim(item_id=denial_item.id, subject="State Department", verb="denied",
                      claim_text="The State Department denied a meeting", claim_type="denial",
                      source_name="State Department"))
    session.commit()
    evidence = {e.source_name: e for e in build_evidence(session, event.id)}
    assert evidence["BBC World"].source_category == "news"         # from sources.yaml
    assert evidence["State Department"].stance == ItemStance.DENIES


# --- configuration -----------------------------------------------------------------------

def test_config_validation():
    raw = load_provenance_config().model_dump(mode="json")
    with pytest.raises(ValidationError):
        ProvenanceConfig(**{**raw, "attribution_patterns": ["according to Reuters"]})
    with pytest.raises(ValidationError):
        ProvenanceConfig(**{**raw, "category_roles": {"news": "gossip"}})


def test_source_role_resolution_order(resolver):
    assert resolver.source_role(item("Reuters World", category="news")) == SourceRole.WIRE      # by name
    assert resolver.source_role(item("New Outlet", category="analysis")) == SourceRole.ANALYSIS  # by category
    assert resolver.source_role(item("@someone", collector="twitter")) == SourceRole.SOCIAL      # by collector
    assert resolver.source_role(item("Nothing Known", collector="rss")) == SourceRole.UNKNOWN
