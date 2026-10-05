"""Pre-deploy record, verified backup and migration rehearsal (docs/operations/deployment-runbook.md, steps P1-P3).

    python scripts/predeploy_check.py --db LIVE.db --live-worktree PATH --out DIR [--phase pre|final]
           [--daemon-pid PID] [--daemon-log FILE] [--collector-status FILE] [--no-rehearse]

Run it with the *target* code on sys.path (from the target worktree, or PYTHONPATH=<target worktree>).

- The live database is opened read-only. The only files written are under --out:
  predeploy-<phase>.json, the backup copy, and the rehearsal copy (migrated with the target code).
- ``--phase pre``: daemon still running; a consistent online backup plus a rehearsal (to be redone after stop).
- ``--phase final``: daemon stopped; refuses unless the daemon PID is gone and no WAL content is pending. This
  backup is the one rollback restores.

Exit code 0: every check passed. 1: a blocking check failed (do not proceed). 2: usage error.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import deploy_checks as D  # noqa: E402

REPO = Path(__file__).resolve().parents[1]


def pid_alive(pid: int) -> bool:
    if os.name == "nt":
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout
        return str(pid) in out
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def tail(path: Path, n: int = 40) -> list[str]:
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return [line.rstrip("\n") for line in f.readlines()[-n:]]
    except OSError as e:
        return [f"(unreadable: {e})"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", required=True, type=Path)
    ap.add_argument("--live-worktree", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--phase", choices=["pre", "final"], default="pre")
    ap.add_argument("--daemon-pid", type=int)
    ap.add_argument("--daemon-log", type=Path)
    ap.add_argument("--collector-status", type=Path)
    ap.add_argument("--no-rehearse", action="store_true")
    ap.add_argument("--expect-head", type=int, help="required migration head of the target code (6 for this deploy)")
    a = ap.parse_args(argv)
    if not a.db.exists():
        print(f"database not found: {a.db}")
        return 2
    stamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    blocking: list[str] = []
    rec = {"phase": a.phase, "at_utc": datetime.utcnow().isoformat(timespec="seconds"),
           "live": D.git_sha(a.live_worktree), "target": D.git_sha(REPO),
           "db": {"path": str(a.db.resolve()), "bytes": a.db.stat().st_size}}

    blocking += D.code_guard(REPO, a.expect_head)

    # writer state. A non-empty -wal is normal for a WAL database (SQLite reuses the file without shrinking it, and
    # a stopped process leaves committed frames there); the online backup reads them. It is recorded, not blocking.
    wal = a.db.with_name(a.db.name + "-wal")
    daemons = D.writer_processes()
    rec["writer"] = {"daemon_pid": a.daemon_pid, "daemon_pid_alive": pid_alive(a.daemon_pid) if a.daemon_pid else None,
                     "daemon_processes": daemons, "wal_bytes": wal.stat().st_size if wal.exists() else 0}
    if a.phase == "final" and daemons:
        blocking.append(f"a daemon process is still running: {daemons}")

    conn = D.ro(a.db)
    try:
        rec["live_state"] = D.snapshot(conn)
    finally:
        conn.close()
    try:
        from osint_monitor.processors.nlp import ner_status
        rec["ner_models"] = {k: list(v) for k, v in ner_status().items()}
    except Exception as e:
        rec["ner_models"] = f"unavailable: {e}"
    if a.collector_status:
        try:
            rec["collector_status_raw"] = a.collector_status.read_text(encoding="utf-8")[:200_000]
        except OSError as e:
            rec["collector_status_raw"] = f"(unreadable: {e})"
    if a.daemon_log:
        rec["daemon_log_tail"] = tail(a.daemon_log)

    print(f"live   {rec['live']['sha']} ({rec['live']['branch']}, dirty={rec['live']['dirty']})")
    print(f"target {rec['target']['sha']} ({rec['target']['branch']}, dirty={rec['target']['dirty']})")
    print(f"db     {rec['db']['path']} {rec['db']['bytes']:,} bytes, schema {rec['live_state']['schema_version']}")
    print(f"counts {rec['live_state']['counts']}, duplicate memberships {rec['live_state']['duplicate_memberships']}")
    if rec["target"]["dirty"]:
        blocking.append("target worktree has uncommitted changes")

    # backup
    bk = D.backup(a.db, a.out / f"backup-{a.phase}-{stamp}.db")
    rec["backup"] = bk
    print(f"backup {bk['path']} sha256 {bk['sha256'][:16]} integrity {bk['integrity']}")
    if not bk["ok"]:
        blocking.append(f"backup integrity: {bk['integrity']}")

    # rehearsal on a copy of the backup
    if not a.no_rehearse and bk["ok"]:
        r = D.rehearse_migration(Path(bk["path"]), a.out / f"rehearsal-{a.phase}-{stamp}")
        rec["rehearsal"] = r
        print(f"rehearsal: schema {r['from_version']} -> {r['to_version']} in {r['seconds']}s"
              + (f"  ERROR {r['error']}" if r["error"] else ""))
        D.print_checks(r["checks"])
        if not r["ok"]:
            blocking.append("migration rehearsal failed")

    rec["blocking"] = blocking
    D.dump(rec, a.out / f"predeploy-{a.phase}.json")
    print(f"record: {a.out / f'predeploy-{a.phase}.json'}")
    for b in blocking:
        print(f"BLOCKING: {b}")
    print("PRE-DEPLOY OK" if not blocking else "PRE-DEPLOY FAILED: do not proceed")
    return 0 if not blocking else 1


if __name__ == "__main__":
    sys.exit(main())
