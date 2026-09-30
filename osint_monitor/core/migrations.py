"""Versioned schema migrations.

``run_migrations`` creates any missing tables, then applies every migration newer
than ``schema_meta.schema_version``, each in its own transaction, recording the
version after it succeeds. A failing migration raises and leaves the version
unchanged. Fresh databases are created at the head schema and skip migrations.

Before migrating an existing SQLite file, a copy is written to
``<db dir>/backups/osint-pre-v<n>-<timestamp>.db``.
"""

from __future__ import annotations

import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Callable

from sqlalchemy import inspect, text
from sqlalchemy.engine import Connection, Engine

from osint_monitor.core.database import Base

logger = logging.getLogger(__name__)

VERSION_KEY = "schema_version"


class MigrationError(RuntimeError):
    """A migration or the pre-migration backup failed; the database was left as it was."""


def _columns(conn: Connection, table: str) -> set[str]:
    return {c["name"] for c in inspect(conn).get_columns(table)}


def _add_column(conn: Connection, table: str, column: str, ddl_type: str) -> None:
    if column not in _columns(conn, table):
        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {ddl_type}"))


def _datetime_type(conn: Connection) -> str:
    return "TIMESTAMP" if conn.dialect.name == "postgresql" else "DATETIME"


def m001_legacy(conn: Connection) -> None:
    """Columns previously added ad hoc on every startup."""
    _add_column(conn, "raw_items", "processed_at", _datetime_type(conn))
    _add_column(conn, "alerts", "trigger_key", "VARCHAR(500)")
    _add_column(conn, "alerts", "superseded_by_id", "INTEGER")
    # Items collected before incremental processing existed count as processed (once).
    conn.execute(text("UPDATE raw_items SET processed_at = fetched_at WHERE processed_at IS NULL"))


def m002_situations(conn: Connection) -> None:
    """events.situation_id (the situations table itself comes from create_all)."""
    _add_column(conn, "events", "situation_id", "INTEGER REFERENCES situations(id)")
    conn.execute(text("CREATE INDEX IF NOT EXISTS ix_events_situation_id ON events (situation_id)"))


def m003_development_fields(conn: Connection) -> None:
    """Classification, confidence and ranking on events; principal flag on event entities."""
    dt = _datetime_type(conn)
    for column, ddl in [
        ("event_domain", "VARCHAR(30)"), ("interaction_mode", "VARCHAR(20)"),
        ("concreteness", "VARCHAR(20)"), ("significance_class", "VARCHAR(20)"),
        ("change_summary", "TEXT"), ("why_it_matters", "TEXT"),
        ("is_routine_commentary", "BOOLEAN"), ("uncertainty_flags", "JSON"),
        ("classification_source", "VARCHAR(100)"), ("classification_notes", "TEXT"),
        ("classified_at", dt), ("confidence_class", "VARCHAR(20)"),
        ("rank_score", "FLOAT"), ("rank_reasons", "JSON"), ("ranked_at", dt),
    ]:
        _add_column(conn, "events", column, ddl)
    _add_column(conn, "event_entities", "is_principal", "BOOLEAN NOT NULL DEFAULT FALSE")


def m004_entity_resolution(conn: Connection) -> None:
    """How each mention was resolved (method + evidence) and each event entity's role in the development."""
    _add_column(conn, "item_entities", "resolution_method", "VARCHAR(30)")
    _add_column(conn, "item_entities", "resolution_evidence", "TEXT")
    _add_column(conn, "event_entities", "actor_role", "VARCHAR(30)")


def m005_run_ledger(conn: Connection) -> None:
    """Run ledger and membership time (the pipeline_runs table itself comes from create_all).

    Stamps: raw_items.ingested_run_id, event_items.added_at / added_run_id (NULL for existing rows: their time
    is unknown and is not invented), events.earliest_published_at (backfilled from member items: a derived
    fact). event_items gets UNIQUE(event_id, item_id); identical duplicate memberships, if any, are removed
    first (keeping the oldest row)."""
    dt = _datetime_type(conn)
    _add_column(conn, "raw_items", "ingested_run_id", "VARCHAR(32) REFERENCES pipeline_runs(id)")
    _add_column(conn, "event_items", "added_at", dt)
    _add_column(conn, "event_items", "added_run_id", "VARCHAR(32) REFERENCES pipeline_runs(id)")
    _add_column(conn, "events", "earliest_published_at", dt)
    conn.execute(text("DELETE FROM event_items WHERE id NOT IN "
                      "(SELECT MIN(id) FROM event_items GROUP BY event_id, item_id)"))
    conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS uq_event_item ON event_items (event_id, item_id)"))
    conn.execute(text("CREATE INDEX IF NOT EXISTS ix_event_items_item ON event_items (item_id)"))
    conn.execute(text("CREATE INDEX IF NOT EXISTS ix_event_items_added_run_id ON event_items (added_run_id)"))
    conn.execute(text("CREATE INDEX IF NOT EXISTS ix_raw_items_ingested_run_id ON raw_items (ingested_run_id)"))
    conn.execute(text(
        "UPDATE events SET earliest_published_at = (SELECT MIN(r.published_at) FROM event_items ei "
        "JOIN raw_items r ON r.id = ei.item_id WHERE ei.event_id = events.id)"))


MIGRATIONS: list[tuple[int, Callable[[Connection], None]]] = [
    (1, m001_legacy),
    (2, m002_situations),
    (3, m003_development_fields),
    (4, m004_entity_resolution),
    (5, m005_run_ledger),
]


def head_version() -> int:
    return max(v for v, _ in MIGRATIONS)


def current_version(engine: Engine) -> int:
    with engine.connect() as conn:
        if "schema_meta" not in inspect(conn).get_table_names():
            return 0
        row = conn.execute(text("SELECT value FROM schema_meta WHERE key = :k"), {"k": VERSION_KEY}).first()
        return int(row[0]) if row else 0


def _set_version(conn: Connection, version: int) -> None:
    updated = conn.execute(text("UPDATE schema_meta SET value = :v WHERE key = :k"),
                           {"v": str(version), "k": VERSION_KEY})
    if updated.rowcount == 0:
        conn.execute(text("INSERT INTO schema_meta (key, value) VALUES (:k, :v)"),
                     {"k": VERSION_KEY, "v": str(version)})


def _sqlite_file(engine: Engine) -> Path | None:
    if engine.dialect.name != "sqlite":
        return None
    db = engine.url.database
    return Path(db) if db and db != ":memory:" else None


def backup_sqlite(engine: Engine, version: int, backup_dir: Path | None = None) -> Path | None:
    """Copy the SQLite database with the online backup API. Returns the backup path."""
    db_file = _sqlite_file(engine)
    if db_file is None:
        return None
    backup_dir = backup_dir or db_file.parent / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    target = backup_dir / f"osint-pre-v{version}-{datetime.utcnow():%Y%m%d-%H%M%S}.db"
    raw = engine.raw_connection()
    dst = sqlite3.connect(target)
    try:
        raw.driver_connection.backup(dst)
    finally:
        dst.close()
        raw.close()
    logger.info("Database backed up to %s", target)
    return target


def run_migrations(engine: Engine, backup_dir: Path | None = None) -> int:
    """Bring the database to the head schema. Returns the resulting version."""
    with engine.connect() as conn:
        existing = set(inspect(conn).get_table_names())
    fresh = "events" not in existing
    Base.metadata.create_all(engine)

    if fresh:
        with engine.begin() as conn:
            _set_version(conn, head_version())
        return head_version()

    version = current_version(engine)
    pending = [(v, fn) for v, fn in MIGRATIONS if v > version]
    if not pending:
        return version

    try:
        backup = backup_sqlite(engine, pending[-1][0], backup_dir)
    except Exception as e:
        raise MigrationError(f"Could not back up the database before migrating ({e}); "
                             f"no migration was applied (schema version {version}).") from e
    for v, fn in pending:
        logger.info("Applying schema migration %d (%s)", v, fn.__name__)
        try:
            with engine.begin() as conn:
                fn(conn)
                _set_version(conn, v)
        except Exception as e:
            where = f" A backup from before the upgrade is at {backup}." if backup else ""
            raise MigrationError(f"Schema migration {v} ({fn.__name__}) failed: {e}. "
                                 f"The database is at schema version {version}.{where}") from e
        version = v
    return version
