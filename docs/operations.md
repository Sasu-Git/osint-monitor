# Running the daemon continuously

`python main.py daemon` runs three collection tiers on APScheduler (hot 150 s, warm 600 s, cold
3600 s), plus alert evaluation every 10 min, trend analysis every 2 h and a daily briefing. This page
covers what the daemon does when it is interrupted, and how to deploy it so it isn't.

## What happens after an interruption

When the host sleeps or the process is blocked, every job's next run passes unexecuted. On wake-up:

- **Stale runs are skipped, not replayed.** A run more than 30 s late (`MISFIRE_GRACE_SECONDS`) is
  skipped and coalesced into the job's next slot, and APScheduler logs "Run time of job ... was
  missed". Jobs do not all fire at the moment of resume.
- **Slots never coincide.** Every job's schedule has a fixed offset (`JOB_OFFSETS`: hot +0 s,
  alerts +20 s, warm +40 s, cold +80 s, analysis +100 s). With the default intervals no two jobs
  are ever due in the same second. Before this, hot, warm and alerts started together every 10
  minutes.
- **Tiers collect in parallel but write one at a time.** Collection is network-bound and runs
  concurrently. Processing and post-processing take `pipeline.DB_WRITE_LOCK`, as do the alert and
  trend jobs, so SQLite has one writer. The lock burst of 2026-09-29 (29 items lost to `database is
  locked`) came from the warm tier's backlog after a resume writing while the hot tier's
  post-processing held the write lock.

## SQLite locks

- Busy timeout: a writer waits up to 30 s for the lock (`SQLITE_BUSY_TIMEOUT_SECONDS`; pysqlite's
  default was 5 s).
- Items: a locked item write is rolled back to its savepoint and retried up to 3 times (1 s, 2 s,
  4 s), so nothing is half-written. If the lock persists, the item is skipped, the batch continues,
  and an ERROR reports how many items were not stored. They are collected again while they remain
  in their feeds. The tier stats carry `lock_failures`.
- Stages: a post-processing stage that hits a lock is rolled back and retried up to 3 times.
  Stages are idempotent and recompute from committed state. The stage status reads `ok (after N
  lock retries)` or `failed: ...`.
- Other errors are not retried and are logged as before.

## Collection gaps

The daemon does not keep the host awake. It reports when it was not running:

- `missed_run`: APScheduler skipped a run more than 15 minutes late. The reported duration is a
  lower bound (the latest skipped slot).
- `tier_silence`: a tier ticks after more than 3 intervals (and at least 15 minutes) without one.
  This gives the full idle period.

Each gap is logged as `WARNING Collection gap (...) ... cause unknown: host suspend, a blocked
scheduler or a stopped process cannot be told apart` (or, for `daemon_down`, that the process was
not running), and appended to `data/logs/collection_gaps.jsonl`. `python main.py status` shows the
heartbeat per tier and the last 24 h of warm coverage. `python main.py gaps --start ... --end ...`
reports coverage and gaps for any window, also from an old daemon's log. See
[operations/source-health.md](operations/source-health.md). Check coverage before using a
collection period for evaluation. Deployment and rollback:
[operations/deployment-runbook.md](operations/deployment-runbook.md).

## Deploying for continuous collection

Keep power management outside the application.

- **Windows.** For a dedicated collector machine, set sleep and hibernate to "Never" when plugged
  in (Settings > System > Power), or `powercfg /change standby-timeout-ac 0` and
  `powercfg /change hibernate-timeout-ac 0`. For a bounded period on a workstation, hold a
  `SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` request from a separate process.
  The evaluation windows used a small PowerShell script launched through WMI so it outlives the
  terminal (see `evaluations/situations/holdout-2026-10-03.md`). To survive logoff and reboot, run
  the daemon as a scheduled task ("Run whether user is logged on or not", "At startup") or as a
  service wrapper such as NSSM.
- **Linux.** Run the daemon as a systemd service. Hold sleep with
  `systemd-inhibit --what=sleep:idle python main.py daemon` or disable suspend targets on a
  dedicated host.
- **macOS.** `caffeinate -i python main.py daemon`.

An idle-sleep inhibitor does not prevent a manual sleep, a closed laptop lid configured to suspend,
a reboot or power loss. Keep collector machines on AC power, and read the gap log.

## Known limitations

- RSS catches up after a gap only as far as each feed's depth. Items published and rolled off a
  feed during a long gap are gone. Sensor feeds (ADS-B, DNS, markets) have no backfill.
- Collector concurrency (network) is unchanged. A slow collector delays its own tier only, within
  its time budget.
- The daily briefing job is not under the write lock. It runs once a day at 06:00 and writes
  little.
- The API server (`python main.py serve`) runs in another process. Its writes (pause/resume flag,
  reads) do not take the daemon's in-process lock. WAL mode lets its readers proceed; its rare
  writes rely on the busy timeout.
