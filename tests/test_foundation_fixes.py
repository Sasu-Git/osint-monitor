"""Phase 0 foundation fixes (evaluations/system/full-basis-audit.md, stop condition S4 and risks 7, 9): writes
that were silently lost, and collector failures that turned into signals."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.core.database import Base, Entity, EntityRelationship, RawItem, Source


@pytest.fixture
def db(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'f.db'}")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    yield factory
    engine.dispose()


# --- lost JSON writes ---------------------------------------------------------------------------

def test_an_alias_added_to_a_stored_entity_is_persisted(db):
    from osint_monitor.processors.entity_resolver import EntityResolver
    s = db()
    s.add(Entity(canonical_name="Pete Hegseth", entity_type="PERSON", aliases=["Hegseth"]))
    s.commit()
    s.close()

    s = db()
    resolver = EntityResolver(s)
    resolver._build_alias_map()
    resolver._register_alias(s.query(Entity).one(), "Pete Hegseth's")
    s.commit()
    s.close()

    assert db().query(Entity).one().aliases == ["Hegseth", "Pete Hegseth's"]


def _item(s):
    src = s.query(Source).filter_by(name="Test Wire").first()
    if src is None:
        src = Source(name="Test Wire", type="rss", url="https://x.invalid/")
        s.add(src)
        s.flush()
    n = s.query(RawItem).count()
    item = RawItem(source_id=src.id, title="t", content="c", url=f"https://x.invalid/{n}", external_id=str(n),
                   content_hash=f"h{n}")
    s.add(item)
    s.flush()
    return item.id


def test_relation_evidence_is_persisted_and_reruns_do_not_inflate_confidence(db):
    from osint_monitor.processors.relations import persist_relations
    rel = [{"subject": "Iran", "object": "Hezbollah", "predicate": "supports", "confidence": 0.5}]
    s = db()
    first, second = _item(s), _item(s)
    s.commit()
    persist_relations(s, first, rel)
    s.commit()
    persist_relations(s, second, rel)          # new evidence: recorded, confidence +0.05
    s.commit()
    for _ in range(3):
        persist_relations(s, second, rel)      # the same evidence again: no change
        s.commit()
    s.close()

    r = db().query(EntityRelationship).one()
    assert r.evidence_item_ids == [first, second]
    assert r.confidence == pytest.approx(0.55)


# --- alert recording and delivery ---------------------------------------------------------------

def _one_alert_engine(monkeypatch, key="corr:1:POSSIBLE→PROBABLE", severity=0.6):
    from osint_monitor.alerting import engine as E
    from osint_monitor.core.database import Alert
    for name in ("_tier1_iw_thresholds", "_tier1_corroboration_changes", "_tier1_fusion_convergence",
                 "_tier2_new_event_clusters", "_tier2_source_silence_break", "_tier3_signal_gaps",
                 "_tier4_first_report"):
        monkeypatch.setattr(E.AlertEngine, name, lambda self, *a, **k: [])
    monkeypatch.setattr(E.AlertEngine, "_tier1_corroboration_changes",
                        lambda self: [Alert(alert_type="corroboration_upgrade", severity=severity,
                                            title="Corroboration upgrade: test", trigger_key=key)])
    return E


def test_a_transition_in_quiet_hours_is_recorded_not_lost(db, monkeypatch):
    from osint_monitor.alerting.fatigue import FatigueManager
    from osint_monitor.core.database import Alert
    E = _one_alert_engine(monkeypatch)
    monkeypatch.setattr(FatigueManager, "_in_quiet_hours", lambda self: True)
    s = db()
    assert E.AlertEngine(s).evaluate_all() == []                 # nothing to notify now
    s.close()
    row = db().query(Alert).one()                                  # but the transition is on record
    assert row.trigger_key == "corr:1:POSSIBLE→PROBABLE" and row.delivered_via == E.QUIET_HOURS


def test_the_daemon_alert_job_delivers_and_records_the_channel(db, monkeypatch):
    from osint_monitor.alerting import channels as C
    from osint_monitor.core import scheduler
    from osint_monitor.core.database import Alert
    _one_alert_engine(monkeypatch)
    sent = []

    class Recorder(C.AlertChannel):
        def send(self, alert):
            sent.append(alert.title)                               # read after the job's session closed
            return True

    monkeypatch.setattr(scheduler, "get_session", db)
    monkeypatch.setattr(C, "build_channels", lambda cfg: [Recorder()])
    scheduler._run_alert_job()
    assert sent == ["Corroboration upgrade: test"]
    assert db().query(Alert).one().delivered_via == "Recorder"


# --- collector outages are not signals ---------------------------------------------------------------

@pytest.fixture
def no_sleep(monkeypatch):
    from osint_monitor.collectors import infrastructure as I
    monkeypatch.setattr(I.time, "sleep", lambda s: None)
    return I


def test_an_opensky_failure_is_no_measurement_not_zero_flights(no_sleep, monkeypatch):
    I = no_sleep
    monkeypatch.setattr(I.FlightRouteMonitor, "_count_commercial_traffic", lambda self, bbox: None)
    assert I.FlightRouteMonitor().collect() == []          # was: "FLIGHT AVOIDANCE ... only 0 commercial flights"


def test_a_failed_bgp_updates_check_never_reads_as_normal(no_sleep, monkeypatch):
    I = no_sleep
    asns = {"AS1": {"name": "Test Net", "country": "IR", "critical": True}}
    monkeypatch.setattr(I.BGPMonitor, "_check_bgp_updates", lambda self, asn, hours_back=6: None)
    monkeypatch.setattr(I.BGPMonitor, "_check_routing_status",
                        lambda self, asn: {"announced_prefixes": 120, "visibility_v4": 300})
    assert I.BGPMonitor(watched_asns=asns).collect() == []  # was: "BGP status: AS1 ... normal", ratio 0
    monkeypatch.setattr(I.BGPMonitor, "_check_routing_status",
                        lambda self, asn: {"announced_prefixes": 0, "visibility_v4": 300})
    [item] = I.BGPMonitor(watched_asns=asns).collect()      # a status anomaly is still reported
    assert item.title.startswith("BGP ANOMALY") and "unavailable (check failed)" in item.content


def test_an_unreachable_domain_is_a_verdict_only_when_our_own_network_works(no_sleep, monkeypatch):
    I = no_sleep
    domains = {"example.ir": {"country": "IR", "type": "government", "desc": "Test"}}
    monkeypatch.setattr(I.DNSHealthMonitor, "_check_dns", staticmethod(lambda d: {"resolves": True, "ips": ["1.2.3.4"]}))
    monkeypatch.setattr(I.DNSHealthMonitor, "_check_http", staticmethod(
        lambda d: {"reachable": False, "status_code": 0, "response_time_ms": 0, "scheme": ""}))
    monkeypatch.setattr(I.DNSHealthMonitor, "_local_network_ok", classmethod(lambda cls: False))
    assert I.DNSHealthMonitor(domains=domains).collect() == []   # was: "DOMAIN DOWN" after a resume
    monkeypatch.setattr(I.DNSHealthMonitor, "_local_network_ok", classmethod(lambda cls: True))
    [item] = I.DNSHealthMonitor(domains=domains).collect()
    assert item.title.startswith("DOMAIN DOWN: example.ir")


# --- collector run status is recorded and readable from any process ------------------------------------

def test_every_collector_run_is_recorded_with_its_state(tmp_path, monkeypatch, no_sleep):
    from osint_monitor.collectors import rss, status
    from osint_monitor.processors.pipeline import _run_single_collector
    I = no_sleep
    monkeypatch.setattr(status, "STATUS_FILE", tmp_path / "collector_status.json")

    class Broken(rss.RSSCollector):
        def collect(self):
            raise RuntimeError("boom")

    feed = rss.RSSCollector(name="Dead Feed", url="https://feed.invalid/rss")
    monkeypatch.setattr(rss._requests, "get", lambda *a, **k: (_ for _ in ()).throw(rss._requests.ConnectionError("down")))
    monkeypatch.setattr(rss.feedparser, "parse", lambda *a, **k: rss.feedparser.FeedParserDict(entries=[], status=503))
    monkeypatch.setattr(I.FlightRouteMonitor, "_count_commercial_traffic", lambda self, bbox: None)

    assert _run_single_collector(feed) == []
    assert _run_single_collector(Broken(name="Broken", url="https://x.invalid")) == []
    assert _run_single_collector(I.FlightRouteMonitor()) == []
    data = status.load()
    assert data["Dead Feed"]["state"] == "failed" and "down" in data["Dead Feed"]["last_error"]
    assert data["Broken"]["state"] == "failed" and data["Broken"]["last_error"] == "RuntimeError: boom"
    assert data["Flight Route Monitor"]["state"] == "failed"
    assert "OpenSky query failed" in data["Flight Route Monitor"]["last_error"]
    assert any("Dead Feed" in line for line in status.format_status(data))


# --- daemon observability ------------------------------------------------------------------------------

def test_a_daemon_restart_after_a_long_stop_is_recorded_as_a_gap(monkeypatch):
    from datetime import datetime, timedelta
    from osint_monitor.core import scheduler as sched
    monkeypatch.setattr(sched, "_intervals", {"warm": 600})
    monkeypatch.setattr(sched, "_last_tick", {})
    t0 = datetime(2026, 9, 30, 8, 0)
    assert sched.check_tier_gap("warm", now=t0) is None           # first tick ever: nothing to compare
    monkeypatch.setattr(sched, "_last_tick", {})                   # a new process: in-memory state gone
    gap = sched.check_tier_gap("warm", now=t0 + timedelta(hours=5))
    assert gap["kind"] == "daemon_down" and gap["seconds"] == 5 * 3600
    assert sched.check_tier_gap("warm", now=t0 + timedelta(hours=5, minutes=10)) is None


def test_the_daemon_log_file_receives_log_records(tmp_path):
    import logging
    from osint_monitor.cli import add_daemon_log_file
    handler = add_daemon_log_file(tmp_path / "daemon.log")
    try:
        logging.getLogger("osint_monitor.test").warning("written to the daemon log")
        handler.flush()
        assert "written to the daemon log" in (tmp_path / "daemon.log").read_text(encoding="utf-8")
    finally:
        logging.getLogger().removeHandler(handler)
        handler.close()
