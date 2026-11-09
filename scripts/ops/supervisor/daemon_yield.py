"""Give the live daemon's memory to other work, and take it back (installed next to ``daemon_supervisor.py``).

    pythonw/python daemon_yield.py yield --by NAME --reason TEXT [--minutes 120] [--wait-minutes 20] [--now]
    python daemon_yield.py resume [--by NAME]
    python daemon_yield.py status

``yield`` writes the yield file (``YIELD`` next to the hold file) with a lease, then stops the daemon gracefully:
it sets the daemon's pause flag, waits up to ``--wait-minutes`` for the pipeline run in progress to finish (``--now``
skips the wait; an interrupted SQLite write rolls back, so this is safe for the data), stops the daemon's python
process tree (not the launcher, so ``daemon-exits.jsonl`` records the exit with ``yielded: true``) and clears the
pause flag again for the next start.

While the yield file exists the supervisor does not restart the daemon before the lease ends; after it, only once
available memory (free + standby) reaches ``yield_resume_available_mb`` in ``config.json`` (default 2900 MB: the
daemon's measured peak working set, 2.4 GB on 2026-11-09, plus about 0.5 GB). It then restarts the pinned commit as
usual and removes the yield file. ``resume`` ends the yield at once and runs one supervisor check, which restarts the
daemon now. The hold file still overrides everything (deploys and rollbacks).

Every yield and resume is appended to ``yields.jsonl`` next to the supervisor log. The daemon's downtime is a
collection gap like any other (logged as ``daemon_down`` at the next start); in a soak it counts as downtime, not as
awake runtime.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import daemon_supervisor as sup  # noqa: E402

NO_WINDOW = 0x08000000


def paths(cfg: dict) -> dict:
    hold = Path(cfg["hold_file"])
    return {"hold": hold, "yield": Path(cfg.get("yield_file") or hold.with_name("YIELD")),
            "yields_log": Path(cfg["log"]).with_name("yields.jsonl"),
            "exits": Path(cfg.get("exit_log") or Path(cfg["log"]).with_name("daemon-exits.jsonl")),
            "pause": Path(cfg["daemon_worktree"]) / "data" / "pause"}


def record(cfg: dict, entry: dict) -> None:
    with open(paths(cfg)["yields_log"], "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def daemon_roots() -> list[int]:
    """PIDs of the daemon's python processes that are not children of another daemon python (the tree roots)."""
    out = sup._ps("Get-CimInstance Win32_Process -Filter \"name='python.exe'\" | "
                  "Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Compress")
    rows = json.loads(out) if out.strip() else []
    rows = [rows] if isinstance(rows, dict) else rows
    daemon = [r for r in rows if "main.py daemon" in (r.get("CommandLine") or "").lower()]
    pids = {r["ProcessId"] for r in daemon}
    return [r["ProcessId"] for r in daemon if r["ParentProcessId"] not in pids]


def runs_in_progress(cfg: dict) -> int:
    """Pipeline runs of the current daemon still running (started after its last recorded start)."""
    starts = [e for e in sup.read_jsonl(paths(cfg)["exits"]) if e.get("event") == "start"]
    since = datetime.fromisoformat(starts[-1]["at"]).astimezone(timezone.utc).replace(tzinfo=None) if starts else None
    db = cfg["db_url"].split("sqlite:///", 1)[1]
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=30)
    try:
        q = "select count(*) from pipeline_runs where status = 'running'"
        args = ()
        if since:
            q += " and started_at >= ?"
            args = (since.isoformat(sep=" "),)
        return con.execute(q, args).fetchone()[0]
    finally:
        con.close()


def do_yield(cfg: dict, by: str, reason: str, minutes: int, wait_minutes: int, now_flag: bool) -> int:
    p = paths(cfg)
    if p["hold"].exists():
        print("refused: the hold file exists (a deploy or maintenance is in progress)")
        return 2
    now = datetime.now(timezone.utc)
    lease = {"at": now.isoformat(timespec="seconds"), "by": by, "reason": reason,
             "until": (now + timedelta(minutes=minutes)).isoformat(timespec="seconds")}
    p["yield"].write_text(json.dumps(lease) + "\n", encoding="utf-8")      # first, so the supervisor stays away
    roots = daemon_roots()
    entry = {"event": "yield", **lease, "daemon_pids": roots, "available_mb_before": sup.available_mb()}
    if roots:
        p["pause"].parent.mkdir(parents=True, exist_ok=True)
        p["pause"].write_text(now.isoformat())
        deadline = time.monotonic() + (0 if now_flag else wait_minutes * 60)
        while (n := runs_in_progress(cfg)) and time.monotonic() < deadline:
            time.sleep(15)
        entry["interrupted_runs"] = n
        for pid in roots:
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, creationflags=NO_WINDOW)
        time.sleep(3)
        p["pause"].unlink(missing_ok=True)
        entry["stopped"] = not daemon_roots()
        entry["available_mb_after"] = sup.available_mb()
    record(cfg, entry)
    print(json.dumps(entry))
    return 0 if not roots or entry["stopped"] else 1


def do_resume(cfg: dict, config_path: str, by: str) -> int:
    p = paths(cfg)
    had = p["yield"].exists()
    p["yield"].unlink(missing_ok=True)
    record(cfg, {"event": "resume", "at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "by": by,
                 "had_yield": had, "available_mb": sup.available_mb()})
    sup.main(config_path)                      # one check now: restarts the pinned daemon unless held
    print(json.dumps({"resumed": True, "had_yield": had, "daemon_pids": daemon_roots()}))
    return 0


def do_status(cfg: dict) -> int:
    p = paths(cfg)
    y = sup.read_yield(p["yield"])
    now = datetime.now(timezone.utc)
    print(json.dumps({"daemon_pids": daemon_roots(), "held": p["hold"].exists(), "yield": y,
                      "lease_active": sup.lease_active(y, now), "available_mb": sup.available_mb(),
                      "resume_available_mb": cfg.get("yield_resume_available_mb", 2900)}, indent=1))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--config", default=str(HERE / "config.json"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    y = sub.add_parser("yield")
    y.add_argument("--by", required=True)
    y.add_argument("--reason", required=True)
    y.add_argument("--minutes", type=int, default=120, help="lease: no restart before it ends")
    y.add_argument("--wait-minutes", type=int, default=20, help="how long to let a running pipeline run finish")
    y.add_argument("--now", action="store_true", help="do not wait for the running pipeline run")
    r = sub.add_parser("resume")
    r.add_argument("--by", default="")
    sub.add_parser("status")
    a = ap.parse_args(argv)
    cfg = json.loads(Path(a.config).read_text(encoding="utf-8-sig"))
    if a.cmd == "yield":
        return do_yield(cfg, a.by, a.reason, a.minutes, a.wait_minutes, a.now)
    if a.cmd == "resume":
        return do_resume(cfg, a.config, a.by)
    return do_status(cfg)


if __name__ == "__main__":
    sys.exit(main())
