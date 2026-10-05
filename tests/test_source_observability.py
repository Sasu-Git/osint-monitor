"""Collector health and collection-gap observability (collectors/status.py, core/gaps.py, core/opstatus.py):
execution health is kept apart from source freshness and from geopolitical findings; identity is the stable key,
not the display name; gaps are computed deterministically and causes are never invented."""

import json
import random
from datetime import datetime, timedelta

import pytest

from osint_monitor.collectors import status as S
from osint_monitor.core import gaps as G

T0 = datetime(2026, 10, 1, 12, 0)
INTERVALS = {"hot": 150, "warm": 600, "cold": 3600}


@pytest.fixture(autouse=True)
def fixed_intervals(monkeypatch):
    monkeypatch.setattr(S, "default_intervals", lambda: dict(INTERVALS))


def rec(name="Feed", items=5, errors=(), exc=None, when=T0, key="RSSCollector:https://f.invalid/rss", **kw):
    return S.record(name, items, list(errors), exc, 1.0, now=when, key=key, tier="warm", source_type="rss", **kw)


# --- health states ----------------------------------------------------------------------------------------------------

def test_partial_success_is_distinguishable_from_total_failure():
    partial = rec(items=3, errors=["one endpoint timed out"])
    assert partial["state"] == "partial" and partial["failure_scope"] == "some_endpoints_or_entries"
    assert S.health_of(partial, T0) == "partial" and partial["consecutive_failures"] == 0
    failed = rec(items=0, exc="ConnectionError: down", key="RSSCollector:https://g.invalid/rss", name="G")
    assert failed["state"] == "failed" and failed["failure_scope"] == "whole_collector"
    assert failed["last_error_class"] == "ConnectionError" and S.health_of(failed, T0) == "failed"
    empty_with_errors = rec(items=0, errors=["parse error"], key="k3", name="H")
    assert empty_with_errors["state"] == "failed"          # an empty result with errors is an outage


def test_stale_detection_uses_the_tier_freshness_window():
    e = rec(when=T0)
    window = S.freshness_window("warm", INTERVALS)               # max(3 x 600 s, 1800 s)
    assert S.health_of(e, T0 + timedelta(seconds=window - 1)) == "healthy"
    assert S.health_of(e, T0 + timedelta(seconds=window + 1)) == "stale"
    assert S.health_of(None, T0) == "not_run"
    assert S.health_of(e, T0, disabled=True) == "disabled"


def test_consecutive_failures_reset_after_success():
    for i in range(3):
        e = rec(items=0, exc="Timeout: x", when=T0 + timedelta(minutes=10 * i))
    assert e["consecutive_failures"] == 3
    e = rec(items=4, when=T0 + timedelta(minutes=40))
    assert e["consecutive_failures"] == 0 and e["last_success"] == (T0 + timedelta(minutes=40)).isoformat()
    assert e["last_failure"] == (T0 + timedelta(minutes=20)).isoformat()      # history kept


def test_health_survives_a_process_restart():
    rec(items=0, exc="HTTPError: 503")
    S._lock = type(S._lock)()                                   # nothing in memory carries over
    data = S.read()
    [entry] = data.values()
    assert entry["consecutive_failures"] == 1 and entry["state"] == "failed"
    report = S.health_report(data, T0, configured=[])
    assert report["counts"]["failed"] == 1


def test_display_name_changes_do_not_orphan_health_records():
    rec(name="Old Name", items=0, exc="E: x")
    rec(name="New Name", items=0, exc="E: y")
    data = S.read()
    assert len(data) == 1
    [entry] = data.values()
    assert entry["name"] == "New Name" and entry["consecutive_failures"] == 2


def test_a_legacy_name_keyed_file_is_adopted_once(tmp_path):
    S.STATUS_FILE.write_text(json.dumps({"Feed": {"state": "failed", "last_run": T0.isoformat(),
                                                  "consecutive_failures": 4, "last_failure": T0.isoformat()}}),
                             encoding="utf-8")
    legacy = S.read()
    assert list(legacy) == ["legacy:Feed"] and legacy["legacy:Feed"]["legacy"]
    e = rec(name="Feed", items=0, exc="E: again", when=T0 + timedelta(minutes=10))
    assert e["consecutive_failures"] == 5
    assert list(S.read()) == ["RSSCollector:https://f.invalid/rss"]


# --- files: missing and malformed ------------------------------------------------------------------------------------

def test_missing_status_files_fail_safely():
    assert S.read() == {} and S.load() == {}
    assert S.format_status(configured=[]) == ["no collector runs recorded"]
    lines = S.format_status(configured=[{"key": "RSSCollector:u", "name": "Feed A", "collector_type": "RSSCollector",
                                         "tier": "warm", "source_type": "rss", "disabled": False}])
    assert "1 not_run" in lines[0] and "Feed A" in lines[1]
    assert G.read_gap_log() == [] and G.read_jsonl(G.EVENTS_LOG) == ([], 0)


@pytest.mark.parametrize("content", ["{not json", "[1, 2]", json.dumps({"schema": 2, "collectors": [1]}),
                                     json.dumps({"schema": 99})])
def test_malformed_status_data_is_handled_explicitly(content):
    S.STATUS_FILE.write_text(content, encoding="utf-8")
    with pytest.raises(S.StatusFileError):
        S.read()
    assert "MALFORMED" in S.format_status(configured=[])[0]
    rec(items=1)                                                # the next run sets the bad file aside
    assert list(S.STATUS_FILE.parent.glob("collector_status.corrupt-*.json"))
    assert len(S.read()) == 1


def test_credentials_are_redacted_from_stored_errors():
    e = rec(items=0, exc="HTTPError: 401 for https://api.x/feed?api_key=SECRET123&q=1 Authorization: Bearer abc.def",
            endpoint="https://user:pw@host/feed?token=T0K")
    blob = json.dumps(S.read())
    assert "SECRET123" not in blob and "abc.def" not in blob and "T0K" not in blob and "user:pw" not in blob
    assert "[REDACTED]" in e["last_error"]


def test_transitions_are_logged_for_outage_reconstruction():
    rec(items=5, when=T0)
    rec(items=0, exc="E: down", when=T0 + timedelta(hours=1))
    rec(items=0, exc="E: down", when=T0 + timedelta(hours=2))      # no new transition
    rec(items=5, when=T0 + timedelta(hours=3))
    events, bad = G.read_jsonl(S.EVENTS_FILE)
    assert [(e["from"], e["to"]) for e in events] == [(None, "ok"), ("ok", "failed"), ("failed", "ok")] and bad == 0
    [outage] = G.collector_outages(events, T0, T0 + timedelta(hours=6))
    assert outage["level"] == "collector" and outage["seconds"] == 2 * 3600 and outage["cause"] == "E"


# --- collector failure never becomes a finding -----------------------------------------------------------------------

def _strike_news(session, n=5):
    from osint_monitor.core.database import RawItem, Source
    src = Source(name="Wire", type="rss", url="u")
    session.add(src)
    session.flush()
    for i in range(n):
        session.add(RawItem(source_id=src.id, title=f"Airstrike hits depot {i}", content="airstrike", url=f"u{i}",
                            content_hash=f"h{i}", fetched_at=datetime.utcnow()))
    session.commit()


def test_a_collector_outage_never_creates_a_signal_finding(session):
    from osint_monitor.analysis.fusion import detect_signal_gaps
    _strike_news(session)
    down = {"narrative": True, "imagery": False, "infrastructure": False, "financial": False, "aviation": False}
    gaps = detect_signal_gaps(session, coverage=down)
    assert gaps and all(g["operational"] and g["gap_type"] == "collection_outage" for g in gaps)
    assert not any(g["gap_type"] in ("contradiction", "negative_confirmation") for g in gaps)
    # control: the same absence while FIRMS is collecting normally is an analytic contradiction
    up = {**down, "imagery": True}
    assert any(g["gap_type"] == "contradiction" and not g["operational"] for g in detect_signal_gaps(session, coverage=up))


def test_operational_gaps_are_not_alerted(session, monkeypatch):
    from osint_monitor.alerting import engine as E
    from osint_monitor.analysis import fusion
    monkeypatch.setattr(fusion, "modality_coverage", lambda rows=None: {})          # every collector down
    _strike_news(session)
    eng = E.AlertEngine(session)
    assert eng._tier3_signal_gaps(24) == []


def test_a_failing_collector_yields_no_items_and_no_alert(session):
    from osint_monitor.collectors.base import BaseCollector
    from osint_monitor.core.database import Alert, Event, RawItem
    from osint_monitor.processors.pipeline import _run_single_collector

    class Down(BaseCollector):
        def collect(self):
            raise ConnectionError("feed unreachable")

    assert _run_single_collector(Down("Dead", "rss", "https://dead.invalid/rss")) == []
    assert session.query(RawItem).count() == session.query(Event).count() == session.query(Alert).count() == 0
    [entry] = S.read().values()
    assert entry["key"] == "Down:https://dead.invalid/rss" and entry["state"] == "failed"


def test_resumption_after_our_own_gap_is_not_a_silence_break(monkeypatch):
    from osint_monitor.alerting import engine as E
    from osint_monitor.core import scheduler
    since, until = T0, T0 + timedelta(hours=30)
    assert E._operational_silence("Wire", since, until) is None                 # we were collecting: a real silence
    scheduler.record_gap("tier_silence", "warm tier", T0 + timedelta(hours=1), T0 + timedelta(hours=25), 600)
    assert "collection gaps cover" in E._operational_silence("Wire", since, until)


# --- collection gaps ---------------------------------------------------------------------------------------------------

def _ticks():
    t, out = T0, []
    while t < T0 + timedelta(hours=12):
        if not (T0 + timedelta(hours=3) <= t < T0 + timedelta(hours=7)):      # 4 h silence
            out.append(t)
        t += timedelta(minutes=10)
    return out


def test_gap_calculation_is_deterministic_and_order_independent():
    ticks = _ticks()
    a = G.tier_coverage(ticks, 600, T0, T0 + timedelta(hours=12))
    shuffled = ticks[:]
    random.Random(7).shuffle(shuffled)
    assert G.tier_coverage(shuffled, 600, T0, T0 + timedelta(hours=12)) == a
    [gap] = a["gaps"]
    assert gap["from"] == T0 + timedelta(hours=2, minutes=50) and gap["to"] == T0 + timedelta(hours=7)
    assert a["covered_seconds"] == 8 * 3600 and a["coverage"] == round(8 / 12, 4)


def test_tier_gap_causes_are_unknown_unless_recorded():
    gap = {"from": T0, "to": T0 + timedelta(hours=4), "seconds": 4 * 3600, "edge": False}
    assert G.classify_tier_gap(gap, [], "warm")["cause"] == "unknown"
    recorded = [{"kind": "daemon_down", "subject": "warm tier", "from": T0, "to": T0 + timedelta(hours=4)}]
    assert G.classify_tier_gap(gap, recorded, "warm")["cause"] == "daemon_not_running"


def test_gap_report_reads_a_daemon_log_with_local_timestamps(tmp_path):
    log = tmp_path / "daemon.err.log"
    lines = [f"{(t + timedelta(hours=2)):%Y-%m-%d %H:%M:%S},123 [INFO] apscheduler: Running job \"Warm tier (x)\""
             for t in _ticks()]
    log.write_text("\n".join(lines) + "\n", encoding="utf-8")
    r = G.report(T0, T0 + timedelta(hours=12), "warm", interval_s=600, log_path=log, log_utc_offset=2)
    assert r["coverage"] == round(8 / 12, 4) and len(r["gaps"]) == 1 and r["gaps"][0]["cause"] == "unknown"


def test_overlap_of_recorded_gaps_merges_intervals():
    gaps = [{"from": T0, "to": T0 + timedelta(hours=2)}, {"from": T0 + timedelta(hours=1), "to": T0 + timedelta(hours=3)}]
    assert G.overlap_seconds(gaps, T0 + timedelta(minutes=30), T0 + timedelta(hours=10)) == 2.5 * 3600


# --- status command --------------------------------------------------------------------------------------------------

def test_status_works_with_no_daemon_activity_and_no_database(tmp_path, capsys, monkeypatch):
    from osint_monitor import cli
    from osint_monitor.core import opstatus
    monkeypatch.setattr(S, "configured_collectors", lambda: [])
    lines = opstatus.status_lines(now=T0, db_url=f"sqlite:///{(tmp_path / 'none.db').as_posix()}")
    text = "\n".join(lines)
    assert "no tier ticks recorded" in text and "database not found" in text
    assert "no collector runs recorded" in text and "coverage: unknown" in text
    assert "no delivery attempts recorded" in text
    assert not (tmp_path / "none.db").exists()                       # read-only: nothing created
    monkeypatch.setattr(opstatus, "status_lines", lambda **k: ["ok-line"])
    cli._cmd_status()
    assert "ok-line" in capsys.readouterr().out


def test_status_reports_the_latest_pipeline_run_read_only(tmp_path, monkeypatch):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from osint_monitor.core import opstatus
    from osint_monitor.core.database import Base, PipelineRun
    db = tmp_path / "r.db"
    engine = create_engine(f"sqlite:///{db.as_posix()}")
    Base.metadata.create_all(engine)
    s = sessionmaker(bind=engine)()
    s.add(PipelineRun(id="a" * 32, kind="tier", tier="warm", started_at=T0, finished_at=T0, status="partial",
                      items_collected=9, items_new=2, stages={"clustering": "ok", "geocoding": "failed: X"},
                      code_sha="abc1234567"))
    s.commit()
    s.close()
    engine.dispose()
    before = db.stat().st_mtime_ns
    lines = opstatus.pipeline_lines(f"sqlite:///{db.as_posix()}")
    assert any("PARTIAL" in x and "FAILED stages: geocoding" in x for x in lines)
    assert db.stat().st_mtime_ns == before


def test_alert_delivery_failures_are_recorded_and_shown():
    from osint_monitor.alerting import channels
    from osint_monitor.core import opstatus
    from osint_monitor.core.database import Alert

    class Broken(channels.AlertChannel):
        def send(self, alert):
            raise RuntimeError("smtp down password=hunter2")

    class Quiet(channels.AlertChannel):
        def send(self, alert):
            return False

    channels.dispatch_alerts([Alert(alert_type="x", title="t")], [Broken(), Quiet()])
    data = channels.load_delivery_status()
    assert data["Broken"]["consecutive_failures"] == 1 and "hunter2" not in data["Broken"]["last_error"]
    assert data["Quiet"]["last_error"] == "send() returned False"
    assert "2 failing" in opstatus.alert_delivery_lines()[0]


# --- logging -----------------------------------------------------------------------------------------------------------

def test_daemon_log_rotates_and_redacts_secrets(tmp_path):
    import logging
    from logging.handlers import RotatingFileHandler

    from osint_monitor import cli
    path = tmp_path / "daemon.log"
    handler = cli.add_daemon_log_file(path)
    try:
        assert isinstance(handler, RotatingFileHandler)
        assert (handler.maxBytes, handler.backupCount) == (10_000_000, 5)
        handler.maxBytes = 200                                     # force a rollover without writing 10 MB
        log = logging.getLogger("osint_monitor.test_rotation")
        log.setLevel(logging.INFO)
        for i in range(10):
            log.info("fetch https://api.example/feed?api_key=SECRET%d failed", i)
        handler.flush()
    finally:
        logging.getLogger().removeHandler(handler)
        handler.close()
    written = "".join(p.read_text(encoding="utf-8") for p in tmp_path.glob("daemon.log*"))
    assert (tmp_path / "daemon.log.1").exists()
    assert "SECRET" not in written and "api_key=[REDACTED]" in written
