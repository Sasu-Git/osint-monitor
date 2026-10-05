"""Shared, read-only database checks for the deployment runbook (docs/operations/deployment-runbook.md).

Every function takes a sqlite3 connection the caller opened read-only (``ro``), except ``rehearse_migration``,
which migrates a *copy* it makes itself. Nothing here writes to the live database.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

COUNT_TABLES = ("raw_items", "events", "event_items", "situations", "alerts", "entities", "pipeline_runs", "sources")
RUN_STAMP_COLUMNS = {"raw_items": ["ingested_run_id"], "event_items": ["added_at", "added_run_id"],
                     "events": ["earliest_published_at"]}
SUMMARY_COLUMNS = ["development_summary", "summary_method", "summary_model", "summary_generated_at", "summary_item_ids"]


def ro(path: Path) -> sqlite3.Connection:
    if not Path(path).exists():
        raise FileNotFoundError(path)
    return sqlite3.connect(f"file:{Path(path).as_posix()}?mode=ro", uri=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def git_sha(worktree: Path) -> dict:
    def run(*args):
        return subprocess.run(["git", "-C", str(worktree), *args], capture_output=True, text=True).stdout.strip()
    return {"path": str(worktree), "sha": run("rev-parse", "HEAD") or None,
            "branch": run("rev-parse", "--abbrev-ref", "HEAD") or None,
            "dirty": bool(run("status", "--porcelain", "--untracked-files=no"))}


def tables(conn) -> set[str]:
    return {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}


def columns(conn, table: str) -> set[str]:
    return {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}


def indexes(conn) -> set[str]:
    return {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='index' AND name IS NOT NULL")}


def schema_version(conn) -> int | None:
    if "schema_meta" not in tables(conn):
        return None
    row = conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()
    return int(row[0]) if row else None


def counts(conn) -> dict:
    t = tables(conn)
    return {name: (conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0] if name in t else None)
            for name in COUNT_TABLES}


def duplicate_memberships(conn) -> int:
    """Rows beyond the first for each (event_id, item_id): what migration 5 removes, and what must stay 0 after."""
    if "event_items" not in tables(conn):
        return 0
    return conn.execute("SELECT COALESCE(SUM(n - 1), 0) FROM (SELECT COUNT(*) n FROM event_items "
                        "GROUP BY event_id, item_id HAVING n > 1)").fetchone()[0]


def max_id(conn, table: str) -> int | None:
    return conn.execute(f"SELECT MAX(id) FROM {table}").fetchone()[0] if table in tables(conn) else None


def integrity(conn) -> str:
    return conn.execute("PRAGMA integrity_check").fetchone()[0]


def foreign_key_violations(conn, limit: int = 20) -> list:
    return conn.execute(f"PRAGMA foreign_key_check").fetchmany(limit)


def snapshot(conn) -> dict:
    """Everything the runbook records about a database state."""
    return {"schema_version": schema_version(conn), "counts": counts(conn),
            "duplicate_memberships": duplicate_memberships(conn),
            "max_ids": {t: max_id(conn, t) for t in ("raw_items", "events", "event_items", "situations", "alerts")},
            "situation_slugs": sorted(r[0] for r in conn.execute("SELECT slug FROM situations"))
            if "situations" in tables(conn) else []}


def backup(source: Path, dest: Path) -> dict:
    """SQLite online backup from a read-only source connection; then verify the copy."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    src = ro(source)
    out = sqlite3.connect(dest)
    try:
        src.backup(out)
    finally:
        out.close()
        src.close()
    check = ro(dest)
    try:
        result = {"path": str(dest), "bytes": dest.stat().st_size, "sha256": sha256(dest),
                  "integrity": integrity(check), "snapshot": snapshot(check)}
    finally:
        check.close()
    result["ok"] = result["integrity"] == "ok"
    return result


# --- structural verification (after migration) ----------------------------------------------------------------------

def unique_sets(conn, table: str) -> set[tuple[str, ...]]:
    """Column sets covered by a UNIQUE index on ``table`` (named, or SQLite's autoindex for a table constraint)."""
    out = set()
    for row in conn.execute(f"PRAGMA index_list({table})"):
        if row[2]:                                            # unique
            out.add(tuple(sorted(r[2] for r in conn.execute(f"PRAGMA index_info('{row[1]}')"))))
    return out


def expected_schema() -> tuple[dict[str, set[str]], set[str], dict[str, set[tuple[str, ...]]], int]:
    """For the code on sys.path (the deploy target): tables -> columns, named indexes, tables -> unique column
    sets (SQLite keeps a named UNIQUE table constraint as an anonymous autoindex, so it is checked by columns),
    and the head schema version."""
    from osint_monitor.core.database import Base
    from osint_monitor.core.migrations import head_version
    cols = {name: {c.name for c in t.columns} for name, t in Base.metadata.tables.items()}
    idx = {i.name for t in Base.metadata.tables.values() for i in t.indexes if i.name and not i.unique}
    uniq: dict[str, set[tuple[str, ...]]] = {}
    for name, t in Base.metadata.tables.items():
        for c in t.constraints:
            if c.__class__.__name__ == "UniqueConstraint":
                uniq.setdefault(name, set()).add(tuple(sorted(col.name for col in c.columns)))
        for i in t.indexes:
            if i.unique:
                uniq.setdefault(name, set()).add(tuple(sorted(col.name for col in i.columns)))
    return cols, idx, uniq, head_version()


def verify_structure(conn, before: dict | None = None) -> list[dict]:
    """Checks a migrated database against the target code. Each check: name, ok, detail. ``before`` is the
    pre-migration ``snapshot`` (row counts, duplicates, max ids) when available."""
    exp_cols, exp_idx, exp_uniq, head = expected_schema()
    have_t, have_i = tables(conn), indexes(conn)
    out = []

    def check(name, ok, detail=""):
        out.append({"check": name, "ok": bool(ok), "detail": detail})

    ver = schema_version(conn)
    check("schema_version == head", ver == head, f"db {ver}, code head {head}")
    res = integrity(conn)
    check("PRAGMA integrity_check", res == "ok", res)
    fk = foreign_key_violations(conn)
    check("PRAGMA foreign_key_check", not fk, f"{len(fk)} violations (first: {fk[:3]})" if fk else "none")
    missing_t = sorted(set(exp_cols) - have_t)
    check("expected tables", not missing_t, f"missing {missing_t}" if missing_t else f"{len(exp_cols)} present")
    missing_c = {t: sorted(c - columns(conn, t)) for t, c in exp_cols.items() if t in have_t and c - columns(conn, t)}
    check("expected columns", not missing_c, f"missing {missing_c}" if missing_c else "all present")
    missing_i = sorted(exp_idx - have_i)
    check("expected indexes", not missing_i, f"missing {missing_i}" if missing_i else f"{len(exp_idx)} present")
    missing_u = {t: sorted(sets - unique_sets(conn, t)) for t, sets in exp_uniq.items()
                 if t in have_t and sets - unique_sets(conn, t)}
    check("expected unique constraints (by columns)", not missing_u, f"missing {missing_u}" if missing_u else
          f"{sum(len(v) for v in exp_uniq.values())} present")
    dups = duplicate_memberships(conn)
    check("no duplicate (development, item) memberships", dups == 0, f"{dups} duplicate rows")
    stamps = {t: [c for c in cs if c not in columns(conn, t)] for t, cs in RUN_STAMP_COLUMNS.items() if t in have_t}
    check("run-provenance columns present", not any(stamps.values()), str({t: c for t, c in stamps.items() if c}) or "ok")
    if head >= 6:
        miss = [c for c in SUMMARY_COLUMNS if c not in columns(conn, "events")]
        check("summary provenance columns present (migration 6)", not miss, f"missing {miss}" if miss else "ok")
    if before is not None:
        now = counts(conn)
        lost = {}
        for t, n0 in before["counts"].items():
            if n0 is None or now.get(t) is None:
                continue
            allowed = before.get("duplicate_memberships", 0) if t == "event_items" else 0
            if now[t] < n0 - allowed:
                lost[t] = f"{n0} -> {now[t]} (allowed loss {allowed})"
        check("no unexpected row-count loss", not lost, str(lost) if lost else
              f"event_items may drop by the {before.get('duplicate_memberships', 0)} duplicates migration 5 removes")
        cutoff = (before.get("max_ids") or {}).get("event_items")
        if cutoff and "added_at" in columns(conn, "event_items"):
            invented = conn.execute("SELECT COUNT(*) FROM event_items WHERE id <= ? AND "
                                    "(added_at IS NOT NULL OR added_run_id IS NOT NULL)", (cutoff,)).fetchone()[0]
            check("no invented membership timestamps on historical rows", invented == 0,
                  f"{invented} pre-deploy memberships carry a time or run")
    return out


def rehearse_migration(backup_path: Path, workdir: Path | None = None) -> dict:
    """Copy a verified backup, migrate the copy with the target code (on sys.path), verify it. The live DB and
    the backup are not modified."""
    from sqlalchemy import create_engine

    from osint_monitor.core.migrations import run_migrations
    workdir = Path(workdir or tempfile.mkdtemp(prefix="osint-rehearsal-"))
    workdir.mkdir(parents=True, exist_ok=True)
    copy = workdir / "rehearsal.db"
    shutil.copyfile(backup_path, copy)
    conn = ro(copy)
    before = snapshot(conn)
    conn.close()
    engine = create_engine(f"sqlite:///{copy.as_posix()}")
    started = datetime.utcnow()
    try:
        version = run_migrations(engine, backup_dir=workdir / "backups")
        error = None
    except Exception as e:                      # reported, never raised: the rehearsal is evidence
        version, error = None, f"{type(e).__name__}: {e}"
    finally:
        engine.dispose()
    conn = ro(copy)
    try:
        checks = verify_structure(conn, before) if error is None else []
        after = snapshot(conn)
    finally:
        conn.close()
    return {"copy": str(copy), "from_version": before["schema_version"], "to_version": version, "error": error,
            "seconds": round((datetime.utcnow() - started).total_seconds(), 1), "before": before, "after": after,
            "checks": checks, "ok": error is None and all(c["ok"] for c in checks)}


def print_checks(checks: list[dict]) -> None:
    for c in checks:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['check']}: {c['detail']}")


def dump(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, default=str, ensure_ascii=False) + "\n", encoding="utf-8")
