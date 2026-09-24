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


MIGRATIONS: list[tuple[int, Callable[[Connection], None]]] = [
    (1, m001_legacy),
    (2, m002_situations),
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
