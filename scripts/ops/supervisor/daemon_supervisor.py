"""Supervise the live daemon: restart it, pinned to the approved code, when its process is gone (post-soak item 6).

    pythonw daemon_supervisor.py CONFIG.json          # one check; the Windows scheduled task runs it every 5 minutes

Each run:
1. does nothing while the hold file exists (a deliberate stop: a deploy, a rollback, maintenance);
   while the yield file exists (``daemon_yield.py``: the daemon gave its memory to other work) it does not restart
   the daemon before the yield's lease ends, then only once available memory reaches ``yield_resume_available_mb``,
   and removes the yield file when it restarts;
2. finds the daemon (a python process running ``main.py daemon`` whose command line names the daemon worktree);
3. if it is gone, restarts it only when
   - the daemon worktree's HEAD is the pinned commit (the supervisor never changes code: a different checkout is
     refused and logged, so a git update cannot silently change what runs), and
   - fewer than ``max_restarts_per_hour`` restarts happened in the last hour (no crash loop);
4. with ``keepawake: true``, restarts the keep-awake when it is gone, holding for ``keepawake_hours`` from now.

It does not detect a hung daemon (alive but not ticking): a host that was asleep looks the same from outside.
``main.py status`` and ``collection_gaps.jsonl`` show stalls.

Processes are created through WMI (``Win32_Process.Create``): detached from any console and not children of the
scheduled task, exactly as the manual runbook does (``data/deploy/LIVE-DAEMON.md``). Every decision is appended to
``log`` as one JSON line. The decision itself is the pure function ``decide`` (tests: tests/test_daemon_supervisor.py).

The daemon is started through ``daemon_launcher.py``, which records each start and exit (exit code, runtime, hold,
the tail of ``daemon.err.log``) in ``daemon-exits.jsonl``. When a start has no exit record and both processes are gone
(the launcher was killed with the daemon: a process-tree kill, a reboot, power loss), ``reconcile_exits`` records the
missing exit as unrecorded.
"""
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

NO_WINDOW = 0x08000000


@dataclass
class State:
    held: bool
    daemon_running: bool
    head: str | None
    keepawake_running: bool
    restarts_last_hour: int
    yielded: bool = False            # the yield file exists
    lease_active: bool = False       # ... and its lease has not ended
    available_mb: int | None = None  # available physical memory (free + standby)


def decide(state: State, pinned: str, max_restarts_per_hour: int, keepawake: bool = True,
           resume_available_mb: int = 2900) -> dict:
    """What to do about the daemon and the keep-awake (no side effects)."""
    if state.held:
        return {"daemon": "hold", "keepawake": "hold"}
    if state.daemon_running:
        daemon = "ok"
    elif state.yielded and state.lease_active:
        daemon = "yield"
    elif state.yielded and (state.available_mb is None or state.available_mb < resume_available_mb):
        daemon = "yield_wait_memory"
    elif not (state.head and pinned and len(pinned) >= 7 and state.head.startswith(pinned)):
        daemon = "refuse_pin_mismatch"
    elif state.restarts_last_hour >= max_restarts_per_hour:
        daemon = "refuse_throttled"
    else:
        daemon = "restart"
    return {"daemon": daemon, "keepawake": "ok" if state.keepawake_running or not keepawake else "start"}


def _ps(command: str) -> str:
    return subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", command], capture_output=True,
                          text=True, creationflags=NO_WINDOW, timeout=60).stdout


def processes() -> list[dict]:
    out = _ps("Get-CimInstance Win32_Process -Filter \"name='python.exe' or name='pythonw.exe'\" | "
              "Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress")
    rows = json.loads(out) if out.strip() else []
    return [rows] if isinstance(rows, dict) else rows


def wmi_start(command_line: str, cwd: str) -> dict:
    cmd = command_line.replace("'", "''")
    out = _ps(f"$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments "
              f"@{{CommandLine = '{cmd}'; CurrentDirectory = '{cwd}'}}; "
              f"@{{rc = $r.ReturnValue; pid = $r.ProcessId}} | ConvertTo-Json -Compress")
    return json.loads(out) if out.strip() else {"rc": None, "pid": None}


def reconcile_exits(exits: list[dict], running: bool, held: bool, now: datetime) -> dict | None:
    """The exit record to append when the last start has none and nothing it started is running, else None."""
    last = next((e for e in reversed(exits) if e.get("event") in ("start", "exit")), None)
    if not last or last["event"] != "start" or running:
        return None
    return {"event": "exit", "at": now.isoformat(timespec="seconds"), "daemon_pid": last.get("daemon_pid"),
            "exit_code": None, "recorded_by": "supervisor", "held": held,
            "cause": "unrecorded: the launcher ended with the daemon (process-tree kill, host reboot or power loss)"}


def read_jsonl(path: Path, last: int = 200) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines()[-last:]:
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def available_mb() -> int | None:
    out = _ps("(Get-CimInstance Win32_PerfFormattedData_PerfOS_Memory).AvailableMBytes").strip()
    return int(out) if out.isdigit() else None


def read_yield(path: Path) -> dict | None:
    """The yield file's content (``daemon_yield.py``), or None without one; an unreadable file is a yield with no lease."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def lease_active(y: dict | None, now: datetime) -> bool:
    try:
        return bool(y) and now < datetime.fromisoformat(y["until"])
    except (KeyError, TypeError, ValueError):
        return False


def head_of(worktree: str) -> str | None:
    r = subprocess.run(["git", "-C", worktree, "rev-parse", "HEAD"], capture_output=True, text=True,
                       creationflags=NO_WINDOW, timeout=60)
    return r.stdout.strip() or None


def recent_restarts(log: Path, now: datetime) -> int:
    if not log.exists():
        return 0
    n = 0
    for line in log.read_text(encoding="utf-8").splitlines()[-500:]:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("daemon") == "restart" and now - datetime.fromisoformat(e["at"]) <= timedelta(hours=1):
            n += 1
    return n


def main(config_path: str) -> int:
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8-sig"))   # Windows PowerShell 5.1 writes a BOM
    log = Path(cfg["log"])
    log.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    worktree = cfg["daemon_worktree"]
    procs = processes()
    lower = lambda p: (p.get("CommandLine") or "").lower()  # noqa: E731
    daemon = [p for p in procs if "main.py daemon" in lower(p)]     # the daemon's python (its launcher is not matched)
    launcher = [p for p in procs if "daemon_launcher.py" in lower(p)]
    keep = [p for p in procs if "keepawake.py" in lower(p)]
    held = Path(cfg["hold_file"]).exists()
    exit_log = Path(cfg.get("exit_log") or log.with_name("daemon-exits.jsonl"))
    missing = reconcile_exits(read_jsonl(exit_log), bool(daemon or launcher), held, now)
    if missing:
        with open(exit_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(missing) + "\n")
    yield_file = Path(cfg.get("yield_file") or Path(cfg["hold_file"]).with_name("YIELD"))
    y = read_yield(yield_file)
    state = State(held=held, daemon_running=bool(daemon), head=head_of(worktree),
                  keepawake_running=bool(keep), restarts_last_hour=recent_restarts(log, now),
                  yielded=y is not None, lease_active=lease_active(y, now),
                  available_mb=available_mb() if y is not None and not daemon else None)
    resume_mb = cfg.get("yield_resume_available_mb", 2900)
    action = decide(state, cfg["pinned_commit"], cfg.get("max_restarts_per_hour", 3), cfg.get("keepawake", True),
                    resume_mb)
    entry = {"at": now.isoformat(timespec="seconds"), **action, "head": state.head, "pinned": cfg["pinned_commit"],
             "daemon_pids": [p["ProcessId"] for p in daemon], "restarts_last_hour": state.restarts_last_hour}
    if y is not None:
        entry["yield"] = {"by": y.get("by"), "until": y.get("until"), "available_mb": state.available_mb,
                          "resume_available_mb": resume_mb}
    if action["daemon"] == "restart" and y is not None:
        yield_file.unlink(missing_ok=True)       # the yield ends with the restart (lease over, memory available)
        entry["yield_ended"] = True
    if action["daemon"] == "restart":
        # the launcher runs the same command as the runbook and records how the daemon ends (daemon-exits.jsonl)
        launcher_script = cfg.get("launcher") or str(Path(__file__).with_name("daemon_launcher.py"))
        command = f'"{cfg["pythonw"]}" "{launcher_script}" "{Path(config_path).resolve()}"'
        entry["started"] = wmi_start(command, worktree)
    if action["keepawake"] == "start":
        until = (now + timedelta(hours=cfg.get("keepawake_hours", 24))).strftime("%Y-%m-%dT%H:%M:%SZ")
        command = f'"{cfg["pythonw"]}" {cfg["keepawake_script"]} {until} --display'
        entry["keepawake_started"] = wmi_start(command, str(Path(cfg["keepawake_script"]).parent))
    if action["daemon"] != "ok" or action["keepawake"] != "ok" or cfg.get("log_every_check"):
        with open(log, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
