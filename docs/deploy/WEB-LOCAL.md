# Read-only production-local web server

The situational-awareness workspace served from its own worktree on `127.0.0.1:8790`. It reads the **live
intelligence database read-only** and stores only personal priorities, in a separate database. It does not start or
stop the daemon, the supervisor or any collector, and it is not a pipeline deploy: no HOLD file, no pause.

| | |
|---|---|
| Web worktree | `C:\Users\EugenioVardiero\osint-monitor-web`, detached at an approved `deploy-web-*` tag. Not the daemon worktree, not the frontend development worktree, not the demo |
| Bind | `127.0.0.1:8790`, `--no-reload` |
| Intelligence DB | `C:\Users\EugenioVardiero\osint-monitor\data\eval\window-2026-09-25.db`, opened by SQLite with `mode=ro` (`OSINT_DB_READONLY=1`) |
| User-state DB | `C:\Users\EugenioVardiero\osint-monitor\data\web\user_state.db` (`OSINT_USER_STATE_DB`): priorities only; the pipeline never reads it |
| Logs | `osint-monitor\data\web\logs\web.out.log`, `web.err.log` (the previous run's logs are kept with a timestamp) |
| State | `osint-monitor\data\web\server.json` (running server), `osint-monitor\data\web\approved-tag.txt` (the approved tag) |
| Python | the shared venv `osint-monitor\.venv`, `PYTHONPATH` = the web worktree |
| Scripts | `scripts\web\start_local_web.ps1`, `status_local_web.ps1`, `stop_local_web.ps1` (settings in `web_config.ps1`) |

`data\web\` is under the main checkout, outside every worktree, so a redeploy or a new worktree keeps the priorities.

## What read-only mode does (`OSINT_DB_READONLY=1`)

- **Engine.** The intelligence DB is opened with `mode=ro` plus `PRAGMA query_only=ON`. There is no journal-mode
  change (the daemon owns WAL) and no file creation (a missing DB is an error).
- **Startup.** The server never migrates or creates tables. It checks that the DB schema version equals the code's
  and **refuses to start** otherwise. It also refuses when the user-state path is the intelligence DB (or its `-wal`,
  `-shm` or `-journal` file).
- **Routes.** Every POST, PUT, PATCH and DELETE returns **403** `{"read_only": true}`, except personal priorities
  (`/api/priorities...`, `/ui/priorities...`). That covers:
  - alert acknowledge, ingest, webhook, briefing generation, ACH, IMINT;
  - pause, resume and toggle.
- **More routes return 403:**
  - the language-model GET routes: CIR report, ACH markdown, and indicators with `use_llm=true`;
  - the whole `/api/daemon` API including status: in the web worktree its pause flag is not the daemon's, so it
    would mislead. Daemon control stays with the CLI in the daemon worktree.
- **UI.** A "Read-only" badge appears. The Acknowledge buttons and the briefing generator are removed, and the
  LLM-scoring box is disabled.
- **CLI.** `collect`, `daemon`, `migrate`, `seed`, `import`, `briefing`, `alerts`, `pause` and `resume` refuse to run.

## Deploy (only with owner approval of a specific tag)

The owner approves a commit of `feat/sa-workspace` and its tag, for example `deploy-web-20261103`, pushed to origin.

```powershell
$REPO = 'C:\Users\EugenioVardiero\osint-monitor'
$WEB  = 'C:\Users\EugenioVardiero\osint-monitor-web'
$TAG  = 'deploy-web-YYYYMMDD'                      # the approved tag

# W1. Worktree (first time: create; later: move to the new tag)
git -C $REPO fetch origin --tags
if (-not (Test-Path $WEB)) { git -C $REPO worktree add --detach $WEB $TAG } else { git -C $WEB checkout --detach $TAG }
git -C $WEB status --porcelain --untracked-files=no    # must be empty

# W2. Persistent web state; back up the user state before every deploy
New-Item -ItemType Directory -Force "$REPO\data\web\backups" | Out-Null
if (Test-Path "$REPO\data\web\user_state.db") {
    Copy-Item "$REPO\data\web\user_state.db" "$REPO\data\web\backups\user_state-$((Get-Date).ToUniversalTime().ToString('yyyyMMdd-HHmmss')).db"
}
Set-Content "$REPO\data\web\approved-tag.txt" $TAG -Encoding ASCII

# W3. Start (refuses: wrong worktree, HEAD not the approved tag, local edits, live DB missing,
#     user state = intelligence DB, server already running, port 8790 taken)
powershell -ExecutionPolicy Bypass -File "$WEB\scripts\web\start_local_web.ps1"
```

The start script runs `python main.py serve --host 127.0.0.1 --port 8790 --no-reload` hidden (`Start-Process`, its own
hidden console, so closing the PowerShell window does not stop it). `OSINT_DB_URL`, `OSINT_DB_READONLY=1`,
`OSINT_USER_STATE_DB`, `PYTHONPATH` and `HF_HUB_OFFLINE` are set for that process only. There is no autostart: after a
reboot, run W3 again.

## Verify

```powershell
powershell -ExecutionPolicy Bypass -File "$WEB\scripts\web\status_local_web.ps1"
```

Every line must be `[OK]`:

- the worktree is at the approved tag;
- the server listens on 127.0.0.1 only;
- `/`, `/map`, `/situations` and `/priorities` return 200;
- the newest live Development (`max(id)` read directly from the DB) is served;
- `POST /api/alerts/0/acknowledge`, `POST /api/daemon/pause` and `GET /api/daemon/status` return 403;
- there is no pause flag and no default `user_state.db` in the web worktree.

Then by hand:

1. **Priorities persist in `user_state.db`:** set a country to HIGH on `/priorities`. The status script's priority row
   count goes up, and the live DB is not modified by the server.
2. **Schema unchanged:** the status script prints the live schema version; it must still be 6.
3. **Daemon healthy:** after the next warm run, `main.py status` from the daemon worktree (see `LIVE-DAEMON.md`) shows
   recent ticks. `run_timing.py` shows no jump in `lock_wait` compared with before the web server started.

## Stop

```powershell
powershell -ExecutionPolicy Bypass -File "$WEB\scripts\web\stop_local_web.ps1"   # only main.py serve on 8790
```

It verifies that port 8790 is closed, and never stops the daemon or the demo (8770).

## Rollback

1. Stop the web server (above).
2. If the previous web version is wanted, check out the previous approved tag:
   `git -C $WEB checkout --detach <previous deploy-web tag>`, put that tag in `approved-tag.txt`, then start (W3).
3. Restore `data\web\user_state.db` from `data\web\backups\` only if the priorities themselves are damaged.

**There is no intelligence-database restore step:** the web server opens it read-only and cannot have changed it.

## Risks to watch

- **WAL checkpoints.** A long read keeps the daemon's WAL checkpoint from completing until the read ends, so the
  `-wal` file grows meanwhile. Web reads are short, but check the `-wal` size after a day of use.
- **Corroboration cost.** The daemon's corroboration stage is slow (over 1,000 s median). The web server only reads
  pre-cached values and adds no pipeline work.
