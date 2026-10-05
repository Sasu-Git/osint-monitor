# Deployment runbook: live daemon → current `main`

This runbook upgrades the live collection daemon from its old state to the accepted foundation. **Nothing in this
document has been executed against the live system.** The migration chain was rehearsed on a backup-API copy of
the live database. That rehearsal is in the evidence section at the end.

**Scripts.** All commands are PowerShell, run from the repository unless stated.

- `scripts/predeploy_check.py` (steps P1–P3) and `scripts/postdeploy_check.py` (M2, S2, C1) open the live
  database **read-only**.
- They write only under the output directory you give them: records, the backup, and the rehearsal copy that
  they migrate.

## 0. Scope and decisions to make first

| Item | Current value | Notes |
|---|---|---|
| Live daemon | PID `42048`, `C:\Users\EugenioVardiero\osint-monitor-daemon` at `a9edd18` (detached) | Command line: `…\osint-monitor\.venv\Scripts\python.exe …\osint-monitor-daemon\main.py daemon` |
| Live database | `C:\Users\EugenioVardiero\osint-monitor\data\eval\window-2026-09-25.db`, via `OSINT_DB_URL` | Schema **3**. It lives in the main checkout's `data\eval`, not the daemon worktree |
| Python / models | shared venv `osint-monitor\.venv`; spaCy `en_core_web_lg`, `it_core_news_md`, `es_core_news_md` | No `.env` in either worktree. Configuration is environment and `config\*.yaml` |
| Logs (old) | `osint-monitor-daemon\data\logs\daemon.{out,err}.log`, redirected, not rotated (23 MB) | The new code also writes a rotating `data\logs\daemon.log` (10 MB × 5) |
| Alert channels | `config\alerts.yaml`: desktop only (plyer 2.1.0 installed) | |

**Decision D1: target commit.**

| | `main` today (`10f4e7c`) | `main` after `feat/localhost-demo` is merged (`e5259d2` reconciled) |
|---|---|---|
| Migrations reached | 4 and 5 (head 5) | 4, 5 and 6 (head 6, development summary provenance columns) |
| Rehearsed | yes | yes |

The scripts read the head version from the target code, so the same steps cover both. The merge of
`feat/localhost-demo` is a separate owner decision and is **not** part of this branch.

**Decision D2: deploy in place.** Check the target out in the existing daemon worktree. Do not create a new
worktree. That way `data\logs` stays: the tier-tick file, collector status and gap log.

- A new worktree would start with no tick history, so the first gap after the upgrade would go unreported.
- Rollback is a checkout back to `a9edd18`.

Set these once per session:

```powershell
$REPO   = "C:\Users\EugenioVardiero\osint-monitor"
$DAEMON = "C:\Users\EugenioVardiero\osint-monitor-daemon"
$PY     = "$REPO\.venv\Scripts\python.exe"
$DB     = "$REPO\data\eval\window-2026-09-25.db"
$TARGET = "<target sha from D1>"
$OUT    = "$REPO\data\deploy\$(Get-Date -Format yyyyMMdd-HHmm)"   # records + backups (untracked: never commit)
$OLDPID = 42048
New-Item -ItemType Directory -Force $OUT | Out-Null
```

## P. Pre-deploy (daemon still running)

**P1. Check out the target in a scratch worktree** for the checks, and verify the SHA. The daemon worktree is
not touched yet.

```powershell
git -C $REPO worktree add --detach "$REPO-deploycheck" $TARGET
git -C "$REPO-deploycheck" rev-parse HEAD          # must equal $TARGET
git -C $DAEMON rev-parse HEAD                       # must be a9edd18c3dfb1a5328f98261564e727accb84c66
```

**P2. Record, back up and rehearse.** Run this with the target code on `PYTHONPATH`. It records:
- the live and target SHAs, and whether each worktree is dirty;
- the database path and size, and the schema version;
- row counts for `raw_items`, `events` (Developments), `event_items` (memberships), `situations`, `alerts`,
  `entities` and `sources`;
- duplicate memberships, the max ids and the Situation slugs;
- the NLP model status and the daemon log tail.

It then takes a SQLite online backup from a `mode=ro` source and verifies it with `PRAGMA integrity_check` and
SHA-256. It migrates a **copy** of the backup with the target code and runs every structural check (M2) on that
copy.

```powershell
$env:PYTHONPATH = "$REPO-deploycheck"
& $PY "$REPO-deploycheck\scripts\predeploy_check.py" --db $DB --live-worktree $DAEMON --out $OUT `
    --phase pre --daemon-pid $OLDPID --daemon-log "$DAEMON\data\logs\daemon.err.log"
```

Proceed only on `PRE-DEPLOY OK` (exit 0).

**P3. Capture the operational state of the old daemon.** It has no collector-status file and no tick file, so
the log is the record.

```powershell
Get-Content "$DAEMON\data\logs\daemon.err.log" -Tail 200 > "$OUT\old-daemon-err-tail.log"
& $PY "$REPO-deploycheck\main.py" gaps --start (Get-Date).ToUniversalTime().AddDays(-2).ToString("s") `
    --end (Get-Date).ToUniversalTime().ToString("s") --log "$DAEMON\data\logs\daemon.err.log" --log-utc-offset 2 `
    > "$OUT\old-daemon-gaps.txt"
```

## X. Stop

**X1. Stop the daemon cleanly.** It was started detached, so there is no console to send Ctrl+C to.

1. Pause first: `& $PY "$DAEMON\main.py" pause`. Every tier then skips its next tick.
2. Wait until the current write finishes: the log shows no `Running job` / `Job ... executed` lines for two
   minutes.
3. Then stop the process:

```powershell
& $PY "$DAEMON\main.py" pause
Start-Sleep 150; Get-Content "$DAEMON\data\logs\daemon.err.log" -Tail 5
Stop-Process -Id $OLDPID
```

**X2. Verify no writer remains.**

```powershell
Get-Process -Id $OLDPID -ErrorAction SilentlyContinue      # must return nothing
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object CommandLine -match "main.py daemon"   # nothing
Get-Item "$DB-wal" -ErrorAction SilentlyContinue | Select-Object Length                          # absent or 0
```

**X3. Final authoritative backup and record.** `--phase final` refuses while the PID is alive or the WAL holds
data. **This backup is the one rollback restores.** The gap between it and the restart is recorded as a
collection gap.

```powershell
& $PY "$REPO-deploycheck\scripts\predeploy_check.py" --db $DB --live-worktree $DAEMON --out $OUT `
    --phase final --daemon-pid $OLDPID
(Get-Date).ToUniversalTime().ToString("s") > "$OUT\stopped-at-utc.txt"
```

## M. Migration

**M1. Apply the chain** with the target code, through migration 5 or 6 (D1).
- `run_migrations` takes its own pre-migration backup under `data\backups`.
- It applies each migration in a transaction and records the version after each.

```powershell
git -C $DAEMON fetch $REPO
git -C $DAEMON checkout --detach $TARGET
git -C $DAEMON rev-parse HEAD                                   # = $TARGET
$env:PYTHONPATH = $DAEMON; $env:OSINT_DB_URL = "sqlite:///$($DB -replace '\\','/')"
& $PY "$DAEMON\main.py" migrate
```

**M2. Verify the structure.**

```powershell
& $PY "$DAEMON\scripts\postdeploy_check.py" --db $DB --pre "$OUT\predeploy-final.json" --out $OUT
```

It checks:
- `schema_version` equals the head;
- `PRAGMA integrity_check` is ok, and `PRAGMA foreign_key_check` returns nothing;
- all tables and columns of the target model are present, as are its named indexes, and its unique constraints
  (checked by column set, since SQLite keeps named table constraints as anonymous autoindexes);
- there are no duplicate `(development, item)` memberships;
- no table lost rows, except that `event_items` may drop by exactly the duplicate count recorded in P2, which
  migration 5 removes;
- no historical membership (id ≤ the pre-deploy max) carries `added_at` or `added_run_id`;
- the run-provenance columns are present;
- at head 6, the summary provenance columns are present.

**Any FAIL is a rollback (R1–R3).**

## S. Start

**S1. Launch the new daemon** with the same database and the default log level (`OSINT_LOG_LEVEL` unset = INFO).
It is launched through WMI so that it outlives the terminal, like the old one.

```powershell
$cmd = "cmd /c cd /d $DAEMON && set OSINT_DB_URL=sqlite:///$($DB -replace '\\','/') && " +
       "`"$PY`" main.py daemon >> data\logs\daemon.out.log 2>> data\logs\daemon.err.log"
$r = Invoke-CimMethod Win32_Process -MethodName Create -Arguments @{ CommandLine = $cmd }
$r.ProcessId                                                         # the cmd wrapper PID
(Get-Date).ToUniversalTime().ToString("s") > "$OUT\started-at-utc.txt"
& $PY "$DAEMON\main.py" resume                                       # clear the X1 pause flag
```

**S2. Verify the start** within 5 minutes.

- **Code:** `git -C $DAEMON rev-parse HEAD` equals `$TARGET`. Every new `pipeline_runs.code_sha` equals it too
  (C1 checks this).
- **Config hash:** each new run carries `config_hash` (C1). Compare with
  `& $PY -c "from osint_monitor.core.runs import config_hash; print(config_hash())"` run in `$DAEMON`.
- **Log level and NER:** the startup banner in `daemon.out.log` prints `English/Italian/Spanish NER: available`.
  `daemon.log` exists and receives INFO lines.
- **Status files writable:** after the first warm tick, `data\logs\collector_status.json` exists with
  `"schema": 2`, and `data\logs\tier_ticks.json` exists.
- **Operator view:** `& $PY "$DAEMON\main.py" status` shows the heartbeat per tier, the latest pipeline run,
  collector health, the 24-hour warm coverage, NER and alert delivery.
- **Log rotation:** `daemon.log` is a `RotatingFileHandler`. To check the rollover mechanism once without waiting
  for 10 MB, run `& $PY -m pytest tests/test_source_observability.py -q` in `$DAEMON`. No live action is needed.
  `daemon.out.log` and `daemon.err.log` are shell redirects and are not rotated: archive them at deploy time
  (they are 23 MB).

## C. Immediate post-start checks (after ≥ 3 warm ticks, about 30 min)

**C1.**

```powershell
& $PY "$DAEMON\scripts\postdeploy_check.py" --db $DB --pre "$OUT\predeploy-final.json" --runtime `
    --since (Get-Content "$OUT\started-at-utc.txt") --logs-dir "$DAEMON\data\logs" --out $OUT
& $PY "$DAEMON\main.py" status > "$OUT\status-after-start.txt"
```

| Check | Pass condition | On failure |
|---|---|---|
| First `pipeline_run` recorded | ≥ 1 run since the start | R5 |
| Runs carry the target code SHA and a config hash | all | R5 |
| Stages have statuses | every finished run has a stage map | review; repeated `failed:` stages → R5 |
| New items carry run provenance | every `raw_items.id` > pre-max has `ingested_run_id` | R5 |
| New memberships carry `added_at` / `added_run_id` | all memberships with id > pre-max | R5 |
| No duplicate memberships | 0 | R6 |
| Single-source stays below the Development layer | every new Development has ≥ 2 sources | R8 |
| Collector failures are operational status | `collector_status.json` schema 2 is valid. Failed collectors appear in `status`, not as alerts. Any `signal_gap_opened` / `source_silence_break` alert since the start is reviewed (WARN) | R4 / R7 |
| Alerts generated and delivered | `alert_delivery.json` shows no failing channel | R9 |
| No unexpected Situation drift | ≤ 3 new Situation slugs (`--max-new-situations`) and none disappeared | R8 |
| No Development count explosion | new Developments per hour ≤ 5× the pre-deploy 7-day rate (`--explosion-factor`) | R8 |
| NER models | en/it/es available. en missing = FAIL; it/es missing = WARN | R5 if en is missing |

Exit codes: 0 = pass; 3 = warnings to review (record the decision in `$OUT`); 1 = rollback criterion.

**C2.** Repeat C1 at about 2 h and about 24 h. Then run the live soak checks: run ledger, membership timestamps,
no duplicates, single-source held back, collector degraded states, alert delivery, stable Development IDs.

## R. Rollback

### Criteria: abort or roll back on any of these

| # | Condition | Detected by |
|---|---|---|
| R1 | Migration integrity failure (`integrity_check` not `ok`, migration exception, schema version ≠ head) | M1 output, M2 |
| R2 | Foreign-key violations after migration | M2 |
| R3 | Missing tables / columns / indexes / unique constraints, or unexpected row loss | M2 |
| R4 | Collector-status corruption (unreadable, wrong schema, repeatedly set aside as `.corrupt-*`) | C1, `status` |
| R5 | Daemon cannot start or keep running; pipeline runs not written, or written without SHA, config hash or run provenance | S2, C1 |
| R6 | Any duplicate Development membership | M2, C1 |
| R7 | New false findings caused by collector outages: a signal-gap or silence-break alert that coincides with a failed or stale collector or a recorded collection gap | C1 WARN review, `status`, `main.py gaps` |
| R8 | Material unexplained Development or Situation drift (C1 bounds exceeded, Situations disappearing, single-source Developments) | C1 |
| R9 | Alert delivery regression: a channel that delivered before now fails | C1, `status` |

**Abort points.** Before M1 nothing has changed: abort = resume the old daemon (step R-4 only). After M1, roll
back fully.

### Steps

```powershell
# R-1  stop the new daemon (pause, wait for the write, stop) and verify no writer, as in X1-X2
& $PY "$DAEMON\main.py" pause; Start-Sleep 150
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object CommandLine -match "main.py daemon" |
    ForEach-Object { Stop-Process -Id $_.ProcessId }

# R-2  restore the verified final backup (keep the failed state for diagnosis)
$final = (Get-Content "$OUT\predeploy-final.json" | ConvertFrom-Json).backup
Move-Item $DB "$OUT\failed-deploy.db"; Remove-Item "$DB-wal","$DB-shm" -ErrorAction SilentlyContinue
Copy-Item $final.path $DB
(Get-FileHash $DB -Algorithm SHA256).Hash.ToLower() -eq $final.sha256     # must be True

# R-3  restore the prior runtime: code back to a9edd18. The schema-2 status files are moved aside, because the
#      old code does not read them; the old daemon never wrote them.
git -C $DAEMON checkout --detach a9edd18c3dfb1a5328f98261564e727accb84c66
New-Item -ItemType Directory -Force "$OUT\new-runtime-logs" | Out-Null
Move-Item "$DAEMON\data\logs\collector_status.json","$DAEMON\data\logs\collector_events.jsonl",
          "$DAEMON\data\logs\alert_delivery.json","$DAEMON\data\logs\tier_ticks.json" "$OUT\new-runtime-logs" `
          -ErrorAction SilentlyContinue

# R-4  restart the prior daemon exactly as before, then clear the pause flag
$cmd = "cmd /c cd /d $DAEMON && set OSINT_DB_URL=sqlite:///$($DB -replace '\\','/') && " +
       "`"$PY`" main.py daemon >> data\logs\daemon.out.log 2>> data\logs\daemon.err.log"
Invoke-CimMethod Win32_Process -MethodName Create -Arguments @{ CommandLine = $cmd }
Remove-Item "$DAEMON\data\pause" -ErrorAction SilentlyContinue
```

**R-5. Verify the old state.**
- The schema version is 3.
- The row counts equal `predeploy-final.json` `live_state.counts`. Check with `scripts/predeploy_check.py
  --phase pre --no-rehearse` from `$REPO-deploycheck`, which reads only.
- `daemon.err.log` shows `Running job "Warm tier` lines again within 10 minutes.
- The SHA is `a9edd18`.

Record the rollback reason in `$OUT\ROLLBACK.md`. Items collected by the new daemon between the start and the
rollback are not in the restored database. They are recollected only while they remain in their feeds.

## Evidence: rehearsal on the live database shape (2026-10-05)

- **Source.** `data/eval/situation-holdout-2026-10-03.snapshot.db`, a backup-API copy of the live database taken
  read-only. Schema 3, 31.9 MB.
- **Contents.** 2,362 items, 137 Developments, 755 memberships, 8 Situations, 461 alerts, 0 duplicate memberships.
- **Copy.** The SHA-256 of the copy equalled the snapshot's (`1934c11a…`).

| Target | Chain | Time | Structural checks |
|---|---|---|---|
| `main` `10f4e7c` (+ this branch's scripts) | 3 → 5 | 1.2 s | all pass: integrity, FK, 16 tables, columns, 8 indexes, 7 unique sets, no duplicates, no row loss, no invented timestamps |
| `feat/localhost-demo` `e5259d2` | 3 → 6 | 2.0 s | all of the above, plus the summary provenance columns |

**First version of the check.** It flagged `uq_source_external` and `uq_item_entity_role` as missing. The legacy
database has them as `sqlite_autoindex_*` (same columns, unique), so the check now compares unique column sets.

**Runtime checks run against the rehearsal copy.** They fail as designed: no pipeline runs, no collector-status
file, no `daemon.log`. That is what an unstarted or broken daemon looks like.

## Known operational risks

- **Host suspend.** In the Situation hold-out window 59 of 96 h had no warm-tier runs. Coverage measured from the
  log was 39.8%. The daemon does not keep the host awake (`docs/operations.md`). Deploying does not fix this.
  `main.py status` and `main.py gaps` now make it visible.
- **Unrecoverable window.** Items published during the stop → final backup → restart window, and rolled off
  their feeds before the restart, are not recoverable.
- **Shared venv.** The daemon and the main checkout share `.venv`. Installing packages in the main checkout during
  the soak changes the daemon's environment.
- **Database location.** The live database lives under the main checkout's `data\eval`. Untracked, and easy to
  confuse with evaluation copies. Never run evaluation scripts with `OSINT_DB_URL` pointing at it.
