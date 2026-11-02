"""Read-only web deployment (OSINT_DB_READONLY=1): the web server reads the live intelligence DB but never writes it.

A separate writer engine stands in for the daemon: it owns the WAL file and keeps committing while the web app
(TestClient, real startup) reads through the read-only engine. "Nothing written by the web" is checked with the
writer's PRAGMA data_version, which changes only when ANOTHER connection commits to the database, plus a logical
dump of the content and the schema version. Personal priorities go to the per-test user-state DB (conftest.py).
"""

import argparse
import hashlib

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from osint_monitor.api.app import _check_user_state_separate, app
from osint_monitor.api.readonly import refusal
from osint_monitor.core.database import Alert, Event, ReadOnlyDatabaseError, get_session, init_db, reset_engine
from osint_monitor.core.migrations import current_version, head_version, run_migrations
from osint_monitor.core.user_state import Level, PriorityStore, Scope, default_path
from tests.test_situation_views import add_development


class Writer:
    """The daemon's side: one long-lived WAL connection that commits and watches for anyone else's commits."""

    def __init__(self, path):
        self.engine = create_engine(f"sqlite:///{path.as_posix()}")

        @event.listens_for(self.engine, "connect")
        def _wal(dbapi_conn, _):
            dbapi_conn.execute("PRAGMA journal_mode=WAL")

        run_migrations(self.engine)
        self.make = sessionmaker(bind=self.engine)
        self.conn = self.engine.raw_connection()   # held open like the daemon's: keeps the WAL and -shm alive

    def data_version(self) -> int:
        return self.conn.execute("PRAGMA data_version").fetchone()[0]

    def dump_hash(self) -> str:
        return hashlib.sha256("\n".join(self.conn.iterdump()).encode()).hexdigest()

    def add_development(self, title) -> int:
        s = self.make()
        try:
            e = add_development(s, None, title, ["Reuters", "BBC World"], 1, event_domain="military")
            s.commit()
            return e.id
        finally:
            s.close()

    def close(self):
        self.conn.close()
        self.engine.dispose()


@pytest.fixture()
def live(tmp_path, monkeypatch):
    """A migrated WAL intelligence DB with one Development and an open alert, served read-only."""
    path = tmp_path / "intel.db"
    writer = Writer(path)
    first = writer.add_development("Artillery strikes reported near the border")
    s = writer.make()
    s.add(Alert(alert_type="new_development", title="Open alert", acknowledged=False))
    s.commit()
    s.close()
    monkeypatch.setenv("OSINT_DB_URL", f"sqlite:///{path.as_posix()}")
    monkeypatch.setenv("OSINT_DB_READONLY", "1")
    reset_engine()
    yield writer, path, first
    reset_engine()   # the next test's default engine is the session's throwaway DB again
    writer.close()


def untouched(writer, before_version, before_hash):
    """No other connection committed (data_version) and the content and schema are the same."""
    assert writer.data_version() == before_version, "another connection committed to the intelligence DB"
    assert writer.dump_hash() == before_hash
    assert current_version(writer.engine) == head_version()


# --- the engine itself ------------------------------------------------------------------------------

def test_the_detector_sees_a_commit_from_another_connection(live):
    """untouched() is meaningful: a write from any other connection changes the writer's data_version."""
    writer, path, _ = live
    v = writer.data_version()
    other = create_engine(f"sqlite:///{path.as_posix()}")
    with other.begin() as c:
        c.execute(text("UPDATE alerts SET acknowledged = 1"))
    other.dispose()
    assert writer.data_version() != v


def test_readonly_engine_cannot_write_even_through_a_session(live):
    writer, _, _ = live
    v, h = writer.data_version(), writer.dump_hash()
    s = get_session()
    try:
        assert s.execute(text("PRAGMA query_only")).scalar() == 1
        assert s.query(Event).count() == 1
        with pytest.raises(OperationalError, match="readonly|read-only|query_only"):
            s.execute(text("INSERT INTO sources (name, type, url, credibility_score) VALUES ('x', 'rss', 'x', 0.5)"))
            s.commit()
    finally:
        s.rollback()
        s.close()
    untouched(writer, v, h)


def test_init_db_checks_the_schema_and_never_migrates(live):
    writer, _, _ = live
    init_db()                                        # same version: passes, writes nothing
    with writer.engine.begin() as c:                 # the code is ahead of the database
        c.execute(text("UPDATE schema_meta SET value = '5' WHERE key = 'schema_version'"))
    reset_engine()
    with pytest.raises(ReadOnlyDatabaseError, match="schema version 5 != code schema version"):
        init_db()
    assert current_version(writer.engine) == 5       # still 5: nothing was migrated


def test_startup_fails_closed_on_mismatch_missing_db_or_shared_user_state(live, tmp_path, monkeypatch):
    writer, path, _ = live
    with writer.engine.begin() as c:
        c.execute(text("UPDATE schema_meta SET value = '5' WHERE key = 'schema_version'"))
    with pytest.raises(ReadOnlyDatabaseError):
        with TestClient(app):
            pass
    reset_engine()
    monkeypatch.setenv("OSINT_DB_URL", f"sqlite:///{(tmp_path / 'missing.db').as_posix()}")
    with pytest.raises(ReadOnlyDatabaseError, match="not found"):
        init_db()
    assert not (tmp_path / "missing.db").exists()    # mode=ro never creates the file
    monkeypatch.setenv("OSINT_DB_URL", f"sqlite:///{path.as_posix()}")
    for clash in (path, path.with_name(path.name + "-wal")):
        monkeypatch.setenv("OSINT_USER_STATE_DB", str(clash))
        with pytest.raises(ReadOnlyDatabaseError, match="must not be the intelligence database"):
            _check_user_state_separate()


# --- routes -----------------------------------------------------------------------------------------

READ_PAGES = ["/", "/map", "/situations", "/priorities", "/dashboard", "/alerts", "/briefings", "/indicators",
              "/events", "/api/events", "/api/alerts", "/api/situations", "/api/priorities", "/api/workspace/developments.geojson", "/ui/countries?q=ch",
              "/api/intel/indicators?hours_back=24"]


def test_read_routes_work_and_write_nothing(live):
    writer, _, first = live
    v, h = writer.data_version(), writer.dump_hash()
    with TestClient(app) as c:
        for url in READ_PAGES + [f"/developments/{first}", f"/api/events/{first}"]:
            r = c.get(url)
            assert r.status_code == 200, (url, r.status_code, r.text[:200])
    untouched(writer, v, h)


REFUSED = [
    ("POST", "/api/alerts/1/acknowledge", None),
    ("POST", "/api/ingest", {"items": [{"title": "t", "content": "c", "source_name": "s"}]}),
    ("POST", "/api/intel/webhook", {"source_name": "s", "title": "t", "content": "c"}),
    ("POST", "/api/briefings/generate", None),
    ("POST", "/api/intel/ach/1", None),
    ("POST", "/api/intel/imint/analyze", {}),
    ("POST", "/api/daemon/pause", None),
    ("POST", "/api/daemon/resume", None),
    ("POST", "/api/daemon/toggle", None),
    ("GET", "/api/daemon/status", None),
    ("GET", "/api/intel/report/cir/1", None),
    ("GET", "/api/intel/ach/1/markdown", None),
    ("GET", "/api/intel/indicators?use_llm=true", None),
    ("PUT", "/api/events/1", {}),
    ("DELETE", "/api/events/1", None),
]


def test_write_operational_and_llm_routes_are_refused_without_side_effects(live, tmp_path, monkeypatch):
    writer, _, _ = live
    from osint_monitor.analysis import briefing
    from osint_monitor.core import scheduler

    flag = tmp_path / "pause"
    monkeypatch.setattr(scheduler, "_PAUSE_FLAG", flag)
    called = []
    monkeypatch.setattr(briefing, "generate_daily_briefing", lambda *a, **k: called.append("briefing"))
    v, h = writer.data_version(), writer.dump_hash()
    with TestClient(app) as c:
        for method, url, body in REFUSED:
            r = c.request(method, url, json=body)
            assert r.status_code == 403, (method, url, r.status_code, r.text[:200])
            assert r.json()["read_only"] is True
    assert not flag.exists() and called == []
    s = writer.make()
    assert s.query(Alert).one().acknowledged is False
    s.close()
    untouched(writer, v, h)


def test_refusal_rules():
    assert refusal("GET", "/api/events", {}) is None
    assert refusal("GET", "/api/intel/indicators", {"use_llm": "false"}) is None
    assert refusal("PUT", "/api/priorities/country/CHN", {}) is None
    assert refusal("DELETE", "/api/priorities", {}) is None
    assert refusal("POST", "/ui/priorities/reset", {}) is None
    assert refusal("POST", "/api/alerts/3/acknowledge", {})
    assert refusal("GET", "/api/daemon/status", {})
    assert refusal("GET", "/api/intel/indicators", {"use_llm": "True"})


def test_writable_mode_keeps_its_routes():
    """Without OSINT_DB_READONLY the gate is off: the same request reaches its route."""
    with TestClient(app) as c:
        r = c.get("/api/daemon/status")
        assert r.status_code == 200 and "read_only" not in r.json()


# --- personal priorities: user-state DB only --------------------------------------------------------

def test_priorities_write_only_the_user_state_db(live):
    writer, _, _ = live
    v, h = writer.data_version(), writer.dump_hash()
    with TestClient(app) as c:
        assert c.put("/api/priorities/country/CHN", json={"level": "HIGH"}).status_code == 200
        assert c.put("/api/priorities/domain/economic", json={"level": "LOW"}).status_code == 200
        assert c.post("/ui/priorities/country/RUS", data={"level": "MUTED"}).status_code == 200
        assert c.get("/").status_code == 200 and c.get("/map").status_code == 200
    store = PriorityStore(default_path())
    assert store.levels(Scope.COUNTRY) == {"CHN": Level.HIGH, "RUS": Level.MUTED}
    assert store.levels(Scope.DOMAIN) == {"economic": Level.LOW}
    untouched(writer, v, h)


# --- live reading -----------------------------------------------------------------------------------

def test_new_development_from_the_writer_is_visible_without_restart(live):
    writer, _, first = live
    with TestClient(app) as c:
        assert c.get(f"/developments/{first}").status_code == 200
        assert c.get(f"/developments/{first + 1}").status_code == 404          # not written yet
        new = writer.add_development("Ceasefire talks resume in Doha")          # the daemon commits
        assert new == first + 1
        assert c.get(f"/api/events/{new}").json()["summary"] == "Ceasefire talks resume in Doha"
        assert c.get(f"/developments/{new}").status_code == 200


def test_open_read_transaction_does_not_block_the_writer(live):
    writer, _, _ = live
    s = get_session()
    try:
        s.execute(text("SELECT count(*) FROM events")).scalar()                 # read transaction stays open
        new = writer.add_development("Port closed after drone attack")         # WAL: the writer still commits
        assert new
        s.rollback()                                                             # a new transaction sees it
        assert s.execute(text("SELECT count(*) FROM events WHERE id = :i"), {"i": new}).scalar() == 1
    finally:
        s.close()


# --- UI and CLI -------------------------------------------------------------------------------------

def test_ui_hides_refused_controls(live):
    with TestClient(app) as c:
        assert 'class="ro-badge"' in c.get("/").text
        assert "Read-only" in c.get("/dashboard").text
        assert "ackAlert(${a.id})" not in c.get("/alerts").text
        briefings = c.get("/briefings").text
        assert "Generate New Briefing" not in briefings and "generated by the daemon" in briefings
        assert 'id="use-llm" style="margin-right: 0.3rem;" disabled' in c.get("/indicators").text


def test_writable_ui_still_shows_controls():
    with TestClient(app) as c:
        assert 'class="ro-badge"' not in c.get("/").text
        assert "ackAlert(${a.id})" in c.get("/alerts").text
        assert "Generate New Briefing" in c.get("/briefings").text


@pytest.mark.parametrize("command", [None, "collect", "daemon", "migrate", "seed", "briefing", "pause", "resume"])
def test_cli_refuses_writing_commands(live, command):
    from osint_monitor.cli import _dispatch
    with pytest.raises(ReadOnlyDatabaseError, match="refused"):
        _dispatch(argparse.Namespace(command=command))
