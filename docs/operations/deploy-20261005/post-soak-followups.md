# Post-soak follow-ups (deploy 2026-10-05, candidate `deploy-candidate-20261005` = `5f046b3`)

Recorded during the soak. **Deployed code stays frozen until the 24 h checkpoint.** These go to a post-soak fix
branch, not to the live candidate.

## 1. False "Signal restored" transition (FIRMS / imagery)

**Observed.** At 13:11Z there was one `signal_gap_closed` alert: "Signal restored: imagery reporting again".

**Cause.**
1. The old daemon had stored `missing_modality:imagery` in the alert state.
2. The new code classifies that gap as `collection_outage` (operational), because FIRMS (cold tier) had not run
   yet.
3. Operational gaps are skipped when the current gap set is built, so the stored gap counted as closed.

**Fix.** Emit "closed" only when the modality is collected *and* present. A gap that turns operational is held in
the state as suspended, with no alert.

## 2. Post-deploy check: legitimate no-op runs

**Observed.** "finished runs record stage statuses" FAILed on 7 runs. All had `items_new = 0`, which skips
post-processing.

**Fix.** Require stages only for runs with `items_new > 0`, or where post-processing ran.

## 3. Backlog-aware Development growth check

**Observed.** "no Development count explosion" FAILed: 25 new in 0.6 h, against 0.60/h before.

**Cause.** The source-expansion backlog:
- 28 sources contributed items for the first time;
- 385 of the 430 new items were published before the deploy;
- 22 of the 25 new Developments came from the first warm run.

**Fix.** Exclude Developments whose earliest publication predates the deploy, or whose sources are first-time.
Alternatively, compare the rate from the third warm run onwards, and report the backlog separately.

## 4. DNS monitor latency and skipped hot ticks

**Observed.** DNS Health Monitor took 66 s, so the hot tier ran about 2.5 min and one hot tick was skipped
("maximum number of running instances reached").

**Next step.** Measure over the soak. Then consider a time budget for DNS, or moving it to the warm tier.

## 5. Persistent collector failures

| Collector | State | Since |
|---|---|---|
| 9 Nitter accounts | every instance fails (connection) | pre-existing: 77 failures each in the old daemon's last log stretch, silent then |
| Lawfare (RSS) | 403 Forbidden | new feed (source expansion) |
| X-ForYou (browser) | Chrome CDP not available (port 9222) | pre-existing prerequisite |

**Decision needed.** For each: disable, replace (other Nitter instances), or fix the prerequisite. Not a soak
blocker. All three now show as `failed` in `main.py status`, with no findings generated.

## Also noted

- **Keep-awake.** The WMI `cmd /c powershell keepawake.ps1` launch died within minutes (`^C` in its log), the
  same failure as in earlier windows. It was replaced at 13:41Z by `keepawake/keepawake.py` under `pythonw.exe`
  (no console), still launched through WMI with `CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS`, PID 18660, until
  2026-10-06 18:00Z. The runbook should adopt this.
- **24 h warm coverage reads 0%.** `main.py status` shows this because the run ledger starts at the deploy. Label
  it "ledger starts at …" rather than as a window-edge gap.
- **Import probe.** `python -c` imports from the cwd before `PYTHONPATH`. Runbook probes of `osint_monitor.__file__`
  should run from the daemon worktree.

## 6. Silence-break alerts right after deploy have no gap history

**Observed.** At 14:01Z (before the standby) two `source_silence_break` alerts fired:
- "Commodity SIGINT (silent 73h)";
- "Breaking Defense (silent 63h)".

**Cause.** The silences spanned the weekend and the old daemon's uncollected periods (38.9% warm coverage in the
48 h before the deploy). The old code wrote no `collection_gaps.jsonl`, so the suppression rule had no evidence.
These are source-activity alerts, not geopolitical findings.

**Fix.** At deploy, backfill `collection_gaps.jsonl` from the old daemon log (`main.py gaps --log`). Or suppress
silence-break alerts for silences that started before the first recorded run in the ledger.

## 7. Keep-awake on Modern Standby (2-hour checkpoint)

**Observed.** Kernel-Power events (CEST):
- **16:26:51:** power source change; the machine has been on battery since.
- **16:27:03:** standby entered (lid), exited at 16:27:12 (lid).
- **16:27:49:** Modern Standby entered for "Idle Timeout", although `ES_SYSTEM_REQUIRED` was held.
- **17:40:41:** exited (lid).

**Effect.** About 70 min without collection: hot and warm `tier_silence`, cold and analysis `missed_run`, all
recorded with cause `unknown`. Some collectors also hit DNS failures during connected standby, while the network
was "Disconnected".

**Daemon behaviour was correct.** No hang, stale runs skipped rather than replayed, and the gaps recorded.

**Mitigation applied** (ops tooling, not deployed code). `keepawake.py --display` adds `ES_DISPLAY_REQUIRED` (PID
44140, from 15:45Z). It cannot stop lid-close or battery standby, so the machine must stay on AC with the lid
open.

**Runbook.** Use `--display` on Modern Standby hosts, and check power source and lid state before a soak.
