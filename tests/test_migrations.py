"""Versioned schema migrations: fresh DB, legacy DB, idempotence, failure."""

import pytest
from sqlalchemy import create_engine, inspect, text

from osint_monitor.core import migrations
from osint_monitor.core.migrations import current_version, head_version, run_migrations

# Shape of the tables m001/m002 touch as of commit 168abd7 (before versioned migrations).
LEGACY_DDL = [
    """CREATE TABLE sources (id INTEGER PRIMARY KEY, name VARCHAR(255) UNIQUE NOT NULL, type VARCHAR(50) NOT NULL,
       url VARCHAR(2048) NOT NULL, category VARCHAR(100), credibility_score FLOAT, priority INTEGER,
       poll_interval INTEGER, enabled BOOLEAN, created_at DATETIME)""",
    """CREATE TABLE raw_items (id INTEGER PRIMARY KEY, source_id INTEGER NOT NULL REFERENCES sources(id),
       external_id VARCHAR(512), title TEXT NOT NULL, content TEXT, url VARCHAR(2048), published_at DATETIME,
       fetched_at DATETIME, content_hash VARCHAR(64) NOT NULL, embedding BLOB)""",
    """CREATE TABLE events (id INTEGER PRIMARY KEY, summary TEXT NOT NULL, event_type VARCHAR(100), severity FLOAT,
       first_reported_at DATETIME, last_updated_at DATETIME, location_name VARCHAR(255), lat FLOAT, lon FLOAT,
       region VARCHAR(100), source_count INTEGER, admiralty_rating VARCHAR(10), corroboration_level VARCHAR(20),
       has_contradictions BOOLEAN)""",
    """CREATE TABLE alerts (id INTEGER PRIMARY KEY, alert_type VARCHAR(50), severity FLOAT, title TEXT NOT NULL,
       detail TEXT, event_id INTEGER, item_id INTEGER, created_at DATETIME, acknowledged BOOLEAN,
       delivered_via VARCHAR(50))""",
    "INSERT INTO sources (id, name, type, url) VALUES (1, 'Wire', 'rss', 'u')",
    """INSERT INTO raw_items (id, source_id, title, content_hash, fetched_at)
       VALUES (1, 1, 'old item', 'h1', '2026-01-01 00:00:00')""",
    "INSERT INTO events (id, summary) VALUES (1, 'old event')",
]


@pytest.fixture()
def legacy_engine(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'legacy.db'}")
    with engine.begin() as conn:
        for stmt in LEGACY_DDL:
            conn.execute(text(stmt))
    yield engine
    engine.dispose()


def test_fresh_database_starts_at_head(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'fresh.db'}")
    assert run_migrations(engine, backup_dir=tmp_path / "backups") == head_version()
    assert current_version(engine) == head_version()
    assert "situations" in inspect(engine).get_table_names()
    assert "situation_id" in {c["name"] for c in inspect(engine).get_columns("events")}
    assert not (tmp_path / "backups").exists()      # nothing to back up
    engine.dispose()


def test_legacy_database_migrates_to_head(legacy_engine, tmp_path):
    backups = tmp_path / "backups"
    assert run_migrations(legacy_engine, backup_dir=backups) == head_version()

    insp = inspect(legacy_engine)
    assert "situation_id" in {c["name"] for c in insp.get_columns("events")}
    assert {"trigger_key", "superseded_by_id"} <= {c["name"] for c in insp.get_columns("alerts")}
    assert "situations" in insp.get_table_names()
    with legacy_engine.connect() as conn:
        assert conn.execute(text("SELECT processed_at FROM raw_items")).scalar() is not None
        assert conn.execute(text("SELECT count(*) FROM events")).scalar() == 1   # data preserved
    [backup] = list(backups.iterdir())
    assert backup.name.startswith(f"osint-pre-v{head_version()}-")


def test_running_twice_is_a_no_op(legacy_engine, tmp_path):
    run_migrations(legacy_engine, backup_dir=tmp_path / "backups")
    with legacy_engine.begin() as conn:
        conn.execute(text("INSERT INTO raw_items (id, source_id, title, content_hash) VALUES (2, 1, 'new', 'h2')"))
    run_migrations(legacy_engine, backup_dir=tmp_path / "backups")
    with legacy_engine.connect() as conn:
        # the legacy backfill ran once, not on every startup
        assert conn.execute(text("SELECT processed_at FROM raw_items WHERE id = 2")).scalar() is None
    assert len(list((tmp_path / "backups").iterdir())) == 1


def test_failing_migration_raises_and_keeps_version(legacy_engine, tmp_path, monkeypatch):
    def broken(conn):
        conn.execute(text("ALTER TABLE no_such_table ADD COLUMN x INTEGER"))

    monkeypatch.setattr(migrations, "MIGRATIONS", [(1, migrations.m001_legacy), (2, broken)])
    with pytest.raises(Exception):
        run_migrations(legacy_engine, backup_dir=tmp_path / "backups")
    assert current_version(legacy_engine) == 1
