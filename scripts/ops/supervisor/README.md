# Live-daemon supervisor (production architecture since 2026-10-13; post-soak item 6)

The live daemon stopped unattended twice in five days: a console `^C` on 2026-10-08 20:49 UTC, and a silent stop
(no traceback, no crash event) on 2026-10-09 21:05 UTC that cost 3 days 10 h of collection. The supervisor restarts
it, pinned to the approved code, when its process is gone.

## What it does (every 5 minutes, and at logon)

| situation | action |
|---|---|
| hold file `HOLD` exists in the runtime folder | nothing (deliberate stop: deploy, rollback, maintenance) |
| daemon running | nothing |
| daemon gone, daemon worktree HEAD = pinned commit, < 3 restarts in the last hour | restart it detached through WMI, same command as the runbook |
| daemon gone, HEAD is another commit | **refuse** and log: the supervisor never changes or starts other code |
| daemon gone, 3 restarts in the last hour | **refuse** and log: a crash loop needs a person |
| keep-awake gone (`keepawake: true`) | restart it for 24 h from now |

It does not detect a hung daemon (alive but not ticking): a host that was asleep looks the same from outside. Use
`main.py status` and `data/logs/collection_gaps.jsonl` for stalls.

## Install

```powershell
powershell -ExecutionPolicy Bypass -File scripts\ops\supervisor\install_supervisor.ps1
```

Copies `daemon_supervisor.py` and a `config.json` (pinned to `production-stable-20261006` = `5f046b3`) to
`C:\Users\EugenioVardiero\osint-monitor\data\deploy\supervisor\` (outside git) and registers the scheduled task
"OSINT daemon supervisor" (current user, interactive, runs on battery, one instance at a time, 3-minute limit).
Re-running refreshes the script and the task; it never overwrites `config.json`.

## Operating it

- **Deliberate stop** (deploy, rollback): create `data\deploy\supervisor\HOLD` first, delete it when done.
- **Deploying new code**: with the hold in place, deploy through `docs/operations/deployment-runbook.md`, then set
  `pinned_commit` in `config.json` to the new approved commit, then delete the hold.
- **Log**: `data\deploy\supervisor\supervisor.jsonl`, one line per action (restarts, refusals, keep-awake starts).
- **Remove**: `Unregister-ScheduledTask -TaskName "OSINT daemon supervisor" -Confirm:$false`.

Tests: `tests/test_daemon_supervisor.py` (the decision rules).
