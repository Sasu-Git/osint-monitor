"""Deployment runbook scripts (scripts/predeploy_check.py, postdeploy_check.py, deploy_checks.py): the live
database is only read, the backup is verified, the migration is rehearsed on a copy, and the structural checks
catch what the runbook treats as rollback criteria."""

import hashlib
import json
import os
import sqlite3
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text

from osint_monitor.core.database import Base

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(SCRIPTS))
import deploy_checks as D  # noqa: E402
import postdeploy_check  # noqa: E402
import predeploy_check  # noqa: E402

from test_run_ledger import _insert, _v4_ddl  # noqa: E402  (v4 table shapes, as the live daemon DB has)

V5_INDEXES = {"uq_event_item", "ix_event_items_item", "ix_event_items_added_run_id", "ix_raw_items_ingested_run_id"}


def _legacy_db(path: Path, duplicate: bool = False) -> Path:
    engine = create_engine(f"sqlite:///{path.as_posix()}")
    with engine.begin() as conn:
        for table in ("raw_items", "events", "event_items"):
            conn.execute(text(_v4_ddl(engine, table)))
            for index in Base.metadata.tables[table].indexes:     # v4 already had the indexes migration 5 did not add
                if index.name not in V5_INDEXES:
                    index.create(conn)
    Base.metadata.create_all(engine)
    with engine.begin() as conn:
        conn.execute(text("INSERT OR REPLACE INTO schema_meta (key, value) VALUES ('schema_version', '4')"))
        _insert(conn, "sources", id=1, name="Wire", type="rss", url="u")
        _insert(conn, "sources", id=2, name="Other", type="rss", url="v")
        for n in (1, 2):
            _insert(conn, "raw_items", id=n, source_id=n, title="t", content_hash=f"h{n}",
                    published_at="2026-09-20 10:00:00")
        _insert(conn, "events", id=1, summary="e", first_reported_at="2026-09-21 01:00:00")
        rows = [(1, 1), (2, 2)] + ([(3, 1)] if duplicate else [])
        for i, item in rows:
            _insert(conn, "event_items", id=i, event_id=1, item_id=item)
    engine.dispose()
    return path


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_backup_is_verified_and_the_source_is_not_modified(tmp_path):
    db = _legacy_db(tmp_path / "live.db")
    before = digest(db)
    bk = D.backup(db, tmp_path / "out" / "b.db")
    assert bk["ok"] and bk["integrity"] == "ok" and bk["snapshot"]["schema_version"] == 4
    assert bk["snapshot"]["counts"]["event_items"] == 2
    assert digest(db) == before


def test_rehearsal_migrates_a_copy_and_passes_the_structural_checks(tmp_path):
    db = _legacy_db(tmp_path / "live.db", duplicate=True)
    before = digest(db)
    r = D.rehearse_migration(db, tmp_path / "rehearsal")
    assert r["ok"], [c for c in r["checks"] if not c["ok"]]
    assert (r["from_version"], r["to_version"]) == (4, D.expected_schema()[3])
    assert r["before"]["duplicate_memberships"] == 1 and r["after"]["duplicate_memberships"] == 0
    assert r["after"]["counts"]["event_items"] == 2              # the one duplicate removed, as allowed
    assert digest(db) == before                                   # only the copy was migrated


def test_structural_checks_catch_invented_timestamps_duplicates_and_lost_rows(tmp_path):
    db = _legacy_db(tmp_path / "live.db")
    r = D.rehearse_migration(db, tmp_path / "rehearsal")
    copy = Path(r["copy"])
    conn = sqlite3.connect(copy)
    conn.execute("UPDATE event_items SET added_at = '2026-10-05 00:00:00' WHERE id = 1")   # invented history
    conn.execute("DELETE FROM raw_items WHERE id = 2")                                     # lost row
    conn.execute("DROP INDEX uq_event_item")
    conn.execute("INSERT INTO event_items (id, event_id, item_id, similarity_score) VALUES (9, 1, 1, 0)")  # duplicate
    conn.commit()
    conn.close()
    failed = {c["check"] for c in D.verify_structure(D.ro(copy), r["before"]) if not c["ok"]}
    assert {"no invented membership timestamps on historical rows", "no unexpected row-count loss",
            "no duplicate (development, item) memberships", "expected unique constraints (by columns)"} <= failed


def test_final_phase_refuses_while_a_daemon_process_exists_but_not_for_a_nonempty_wal(tmp_path, capsys, monkeypatch):
    db = _legacy_db(tmp_path / "live.db")
    (tmp_path / "live.db-wal").write_bytes(b"\0" * 4096)        # normal for WAL databases: never blocking
    args = ["--db", str(db), "--live-worktree", str(tmp_path), "--out", str(tmp_path / "o"), "--phase", "final",
            "--daemon-pid", "4242", "--no-rehearse"]
    monkeypatch.setattr(D, "git_sha", lambda path: {"path": str(path), "sha": "x", "branch": "b", "dirty": False})
    monkeypatch.setattr(D, "writer_processes", lambda: ['"python.exe" "C:\\w\\main.py" daemon'])
    assert predeploy_check.main(args) == 1 and "daemon process is still running" in capsys.readouterr().out
    monkeypatch.setattr(D, "writer_processes", lambda: [])
    assert predeploy_check.main(args) == 0
    rec = json.loads((tmp_path / "o" / "predeploy-final.json").read_text(encoding="utf-8"))
    assert rec["writer"]["wal_bytes"] == 4096 and not rec["blocking"]


def test_the_backup_is_one_self_contained_file(tmp_path):
    db = _legacy_db(tmp_path / "live.db")
    conn = sqlite3.connect(db)
    conn.execute("PRAGMA journal_mode=WAL")                         # the live daemon DB is in WAL mode
    conn.close()
    bk = D.backup(db, tmp_path / "b.db")
    assert sqlite3.connect(bk["path"]).execute("PRAGMA journal_mode").fetchone()[0] == "delete"
    assert not Path(bk["path"] + "-wal").exists()


def test_scripts_refuse_the_wrong_code_tree_or_migration_head(tmp_path, capsys):
    repo = Path(__file__).resolve().parents[1]
    assert D.code_guard(repo, D.expected_schema()[3]) == []
    assert any("imported from" in p for p in D.code_guard(tmp_path, None))       # e.g. the editable install
    assert any("expected 99" in p for p in D.code_guard(repo, 99))
    db = _legacy_db(tmp_path / "live.db")
    code = predeploy_check.main(["--db", str(db), "--live-worktree", str(tmp_path), "--out", str(tmp_path / "o"),
                                 "--no-rehearse", "--expect-head", "99"])
    assert code == 1 and "expected 99" in capsys.readouterr().out
    assert postdeploy_check.main(["--db", str(db), "--pre", "unused.json", "--expect-head", "99"]) == 1


def test_single_source_check_exempts_structured_record_groups(tmp_path):
    db = _legacy_db(tmp_path / "live.db")
    r = D.rehearse_migration(db, tmp_path / "rehearsal")
    copy = Path(r["copy"])
    pre = {"live_state": r["before"], "target": {"sha": None}}
    engine = create_engine(f"sqlite:///{copy.as_posix()}")
    with engine.begin() as conn:
        _insert(conn, "sources", id=3, name="USGS", type="seismic", url="u")
        for item, src in ((10, 3), (11, 1)):
            _insert(conn, "raw_items", id=item, source_id=src, title="t", content_hash=f"x{item}")
        for ev, item in ((10, 10), (11, 11)):                      # one structured, one narrative single-source
            _insert(conn, "events", id=ev, summary="e", first_reported_at="2026-10-05 01:00:00")
            _insert(conn, "event_items", id=100 + ev, event_id=ev, item_id=item)
    engine.dispose()
    checks = postdeploy_check.runtime_checks(D.ro(copy), pre, __import__("datetime").datetime(2026, 10, 5),
                                             None, 3, 5.0)
    [single] = [c for c in checks if "single-source" in c["check"]]
    assert not single["ok"] and "[11]" in single["detail"]          # the narrative one only


def test_postdeploy_structure_passes_on_a_rehearsed_copy_and_reads_only(tmp_path, capsys):
    db = _legacy_db(tmp_path / "live.db")
    predeploy_check.main(["--db", str(db), "--live-worktree", str(tmp_path), "--out", str(tmp_path / "o")])
    rec = json.loads((tmp_path / "o" / "predeploy-pre.json").read_text(encoding="utf-8"))
    copy = Path(rec["rehearsal"]["copy"])
    before = digest(copy)
    assert postdeploy_check.main(["--db", str(copy), "--pre", str(tmp_path / "o" / "predeploy-pre.json")]) == 0
    assert digest(copy) == before
    # runtime checks with no new daemon activity fail (no pipeline runs): a rollback criterion, by design
    assert postdeploy_check.main(["--db", str(copy), "--pre", str(tmp_path / "o" / "predeploy-pre.json"),
                                  "--runtime", "--since", "2026-10-05T00:00"]) == 1
    assert "pipeline runs recorded since start: 0 runs" in capsys.readouterr().out


def _rehearsed(tmp_path):
    db = _legacy_db(tmp_path / "live.db")
    r = D.rehearse_migration(db, tmp_path / "rehearsal")
    return Path(r["copy"]), {"live_state": r["before"], "target": {"sha": None}}


def test_no_op_runs_are_exempt_from_the_stage_check_but_runs_with_new_items_are_not(tmp_path):
    copy, pre = _rehearsed(tmp_path)
    engine = create_engine(f"sqlite:///{copy.as_posix()}")
    with engine.begin() as conn:
        for rid, new, stages in (("a" * 32, 0, None), ("b" * 32, 0, "{}"), ("c" * 32, 4, '{"nlp": "ok"}')):
            _insert(conn, "pipeline_runs", id=rid, kind="tier", tier="warm", started_at="2026-10-05 02:00:00",
                    status="ok", stages=stages, items_new=new)
    engine.dispose()
    since = __import__("datetime").datetime(2026, 10, 5)
    [stage] = [c for c in postdeploy_check.runtime_checks(D.ro(copy), pre, since, None, 3, 5.0) if "stage" in c["check"]]
    assert stage["ok"] and "2 no-op runs exempt" in stage["detail"]
    engine = create_engine(f"sqlite:///{copy.as_posix()}")
    with engine.begin() as conn:
        _insert(conn, "pipeline_runs", id="d" * 32, kind="tier", tier="warm", started_at="2026-10-05 03:00:00",
                status="ok", stages=None, items_new=2)
    engine.dispose()
    [stage] = [c for c in postdeploy_check.runtime_checks(D.ro(copy), pre, since, None, 3, 5.0) if "stage" in c["check"]]
    assert not stage["ok"] and "1 of 2 without stages" in stage["detail"]


def test_development_growth_separates_backlog_from_fresh_developments(tmp_path):
    copy, pre = _rehearsed(tmp_path)
    engine = create_engine(f"sqlite:///{copy.as_posix()}")
    with engine.begin() as conn:
        _insert(conn, "sources", id=5, name="New outlet", type="rss", url="n")      # first item after the deploy
        items = ((20, 1, "2026-10-04 20:00:00"),     # published before the start: backlog
                 (21, 5, "2026-10-05 03:00:00"),     # only a first-time source: backlog
                 (22, 1, "2026-10-05 04:00:00"), (23, 2, "2026-10-05 04:10:00"))   # fresh, established sources
        for item, src, pub in items:
            _insert(conn, "raw_items", id=item, source_id=src, title="t", content_hash=f"g{item}", published_at=pub)
        for ev, members in ((20, (20,)), (21, (21,)), (22, (22, 23))):
            _insert(conn, "events", id=ev, summary="e", first_reported_at="2026-10-05 05:00:00")
            for item in members:
                _insert(conn, "event_items", id=200 + item, event_id=ev, item_id=item)
    engine.dispose()
    since = __import__("datetime").datetime(2026, 10, 5)
    assert postdeploy_check.development_growth(D.ro(copy), pre, since) == (1, 2)
    [growth] = [c for c in postdeploy_check.runtime_checks(D.ro(copy), pre, since, None, 3, 5.0)
                if "explosion" in c["check"]]
    assert "backlog not counted: 2" in growth["detail"]
