# Local demo runbook (situational-awareness workspace)

Runs the web UI from the frontend worktree (`feat/sa-workspace` @ 5e36c1c) on 127.0.0.1, against a scratch copy
of the live intelligence DB, with a separate demo user-state DB. Starts no daemon, no scheduler, no collector.

| What | Value |
|---|---|
| Worktree | `C:\Users\EugenioVardiero\osint-monitor-frontend` |
| Python | `C:\Users\EugenioVardiero\osint-monitor\.venv\Scripts\python.exe` (shared venv; `PYTHONPATH` = worktree) |
| Scratch intelligence DB | `data\demo\intel-scratch.db`: SQLite backup-API copy of `osint-monitor\data\eval\window-2026-09-25.db` (opened `mode=ro`) |
| Demo user-state DB | `data\demo\user_state-demo.db` (`OSINT_USER_STATE_DB`) |
| Bind | `127.0.0.1:8770`, `--no-reload` |
| Logs / state | `data\demo\server.out.log`, `server.err.log`, `server.json` |

`data/demo/` is gitignored.

The scratch copy stays writable: the app sets WAL mode on connect, and a read-only file refuses that. Anything it
writes stays in the copy.

```powershell
cd C:\Users\EugenioVardiero\osint-monitor-frontend
powershell -ExecutionPolicy Bypass -File .\scripts\demo\start_local_demo.ps1 -Refresh   # fresh copy + start
powershell -ExecutionPolicy Bypass -File .\scripts\demo\status_local_demo.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\demo\stop_local_demo.ps1
```

**Start refuses when:**
- the worktree is not on `feat/sa-workspace`, or its app code (`osint_monitor`, `web`, `config`, `main.py`)
  differs from the approved 5e36c1c, including uncommitted edits (override: `-AllowAnyCommit`);
- the worktree is the daemon worktree;
- a demo server is already running, or the port is in use;
- the scratch DB or user-state path resolves to the live DB, any `data\osint.db`, a default `user_state.db`, or
  anything under `osint-monitor-daemon`.

**Stop** kills only `python.exe` processes whose command line is `main.py serve ... --port <demo port>`.
