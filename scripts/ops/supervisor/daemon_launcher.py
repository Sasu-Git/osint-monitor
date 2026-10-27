"""Run the live daemon and record how it ends (started by ``daemon_supervisor.py``; replaces the ``cmd /c`` wrapper).

    pythonw daemon_launcher.py CONFIG.json

Starts ``python main.py daemon`` in the daemon worktree with the same environment and log files as the runbook
(``OSINT_DB_URL``; stdout appended to ``data/logs/daemon.out.log``, stderr to ``data/logs/daemon.err.log``), waits for
it, and appends two JSON lines to ``exit_log`` (default ``daemon-exits.jsonl`` next to the supervisor log):

- ``start``: time, launcher pid, daemon pid, command, worktree HEAD;
- ``exit``: time, daemon pid, exit code (decimal and hex: 0xC0000005 is a native crash, 1 a forced termination or an
  unhandled Python error), runtime, whether the hold file existed (a deliberate stop: deploy, rollback, maintenance),
  and the last ``tail_lines`` lines of ``daemon.err.log``.

Nothing here restarts anything: restarts stay with the supervisor and its rules. To stop the daemon so that its exit is
recorded, stop the daemon's python process, not this launcher (``LIVE-DAEMON.md``). When the launcher itself is killed
(a process-tree kill, a reboot, power loss) the supervisor records the missing exit on its next check
(``daemon_supervisor.reconcile_exits``).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

NO_WINDOW = 0x08000000


def exit_log_path(cfg: dict) -> Path:
    return Path(cfg.get("exit_log") or Path(cfg["log"]).with_name("daemon-exits.jsonl"))


def append(path: Path, entry: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def tail(path: Path, lines: int) -> list[str]:
    """The last ``lines`` lines of a (possibly very large) log file, read from its end."""
    try:
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 64 * 1024))
            data = f.read().decode("utf-8", errors="replace")
    except OSError:
        return []
    return [line[:400] for line in data.splitlines()[-lines:]]


def head_of(worktree: str) -> str | None:
    r = subprocess.run(["git", "-C", worktree, "rev-parse", "HEAD"], capture_output=True, text=True,
                       creationflags=NO_WINDOW, timeout=60)
    return r.stdout.strip() or None


def run(cfg: dict, argv: list[str]) -> int:
    """Start the daemon, wait for it, record start and exit. Returns the daemon's exit code."""
    worktree = cfg["daemon_worktree"]
    logs = Path(worktree) / "data" / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    exits = exit_log_path(cfg)
    env = {**os.environ, "OSINT_DB_URL": cfg["db_url"]}
    started = datetime.now(timezone.utc)
    with open(logs / "daemon.out.log", "ab") as out, open(logs / "daemon.err.log", "ab") as err:
        proc = subprocess.Popen(argv, cwd=worktree, env=env, stdout=out, stderr=err, creationflags=NO_WINDOW)
        append(exits, {"event": "start", "at": started.isoformat(timespec="seconds"), "launcher_pid": os.getpid(),
                       "daemon_pid": proc.pid, "argv": argv, "head": head_of(worktree)})
        code = proc.wait()
    ended = datetime.now(timezone.utc)
    append(exits, {"event": "exit", "at": ended.isoformat(timespec="seconds"), "daemon_pid": proc.pid,
                   "exit_code": code, "exit_code_hex": f"0x{code & 0xFFFFFFFF:08X}",
                   "runtime_s": round((ended - started).total_seconds()),
                   "held": Path(cfg["hold_file"]).exists(),
                   "err_tail": tail(logs / "daemon.err.log", int(cfg.get("tail_lines", 20)))})
    return code


def main(config_path: str) -> int:
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8-sig"))   # Windows PowerShell 5.1 writes a BOM
    argv = [cfg["python"], *cfg.get("daemon_args", ["main.py", "daemon"])]
    run(cfg, argv)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
