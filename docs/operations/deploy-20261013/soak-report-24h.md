# 24 h soak report: `deploy-candidate-20261013` (`3eda6d0`, schema 6)

**Result.** Passed; promoted to **`production-stable-20261016`** (= `3eda6d0`) on 2026-10-16. That is the rollback
baseline for the next deployment; the previous stable is `production-stable-20261006` (`5f046b3`).

**Deployed.** 2026-10-13 10:51Z via the deployment runbook (supervisor HOLD, final backup, migrate/check, launch,
re-pin, release). Founder guard off (`founder_same_occurrence_hours: null`). Records: `data/deploy/20261013-1246/`
on the host (not in git).

## Checkpoints

| | Time (UTC) | Result |
|---|---|---|
| C1 (3 warm ticks) | 10-13 11:26 | POST-DEPLOY OK, 1 warning (pre-existing failed collectors) |
| ~2 h | 10-13 13:06 | POST-DEPLOY OK, same warning |
| C2 (~24 h) | 10-14 17:47 | POST-DEPLOY OK, 2 warnings (failed collectors; one "Source resumed" alert) |

C2 detail:

- **Runs and provenance:**
  - 560 runs, 0 failed, all carrying `3eda6d0` and a config hash.
  - All 171 runs that produced new items recorded their stages.
  - 2,316 new items and 817 new memberships, all stamped with their run.
- **Developments and Situations:**
  - 0 duplicate memberships.
  - 0 single-source Developments.
  - 61 new Developments in 30.9 h (1.97/h, against 1.27/h before deploy).
  - 3 new Situations (limit 3); none disappeared.
- **Daemon stability:** no restart. The daemon PIDs were unchanged from launch, and the supervisor task result was 0.
- **Coverage:**
  - 24 h coverage 84.4%.
  - The three tier gaps (1.1 h, 1.8 h, 0.8 h) match host Modern Standby or sleep (Kernel-Power 506/507/42/107).
- **The warning alert:** "Source resumed: Defense Stock Monitor (silent 24h)". The collector succeeded on every
  attempt (299 sampled). It emits items only on large price moves, so this is not an outage (follow-up 2).

## Live Situation repair (2026-10-16)

**Gate.** A dry-run on a read-only snapshot at C2 proposed exactly the three intended actor-identity retirements.
It was re-run on the live DB under pause immediately before applying and still proposed exactly those three. The
owner approved the apply.

**Pause window.** Paused 16:35:56Z, applied at 16:36:31Z, resumed 16:37:08Z.

**Applied.** `scripts/repair_situations.py --apply`, backup first (integrity verified). Retired:

- `bolsonaro-fl-vio-bolsonaro`: 4 Developments;
- `estados-unidos-united-states`: 93 Developments;
- `ucrania-ukraine`: 21 Developments.

Each was renamed `--retired-20261016` and closed. Their 118 Developments were detached for regrouping.

**Verified:**
- integrity ok, 0 foreign-key violations;
- item, Development, membership and alert counts unchanged;
- membership digest identical;
- no other Situation changed;
- every detached Development came from those three;
- none is left on a retired Situation.

`elon-musk-musk` and `rachel-simon` were deliberately left out of this repair (follow-up 1).

## Follow-ups (owner, 2026-10-16)

1. **Actor-identity defects created after deploy** go to the Phase 2 identity evaluation path. They are not repaired
   ad hoc.
   - `elon-musk-musk`: a surname alias that actor normalisation did not merge.
   - `rachel-simon`: first-name-only actors.
2. **Operational alerts: sparse or event-driven collectors.** "No items for 24 h" must not count as evidence of
   source silence when collection attempts are succeeding.
   - Example: Defense Stock Monitor emits only on price surges.
   - Added to the operational-alert backlog.
3. **Hot-tier latency: do not optimise DNS or BGP.** Baseline (`data/deploy/20261013-1246/hot-tier-baseline.md`),
   window 10-13 10:51Z to 10-14 12:00Z:
   - 433 hot ticks scheduled while awake: 303 completed, 136 skipped, about 171 missed while asleep.
   - DNS runs a steady ~59 s (r = 0.14 with hot duration).
   - Un-overlapped collection-only hot runs never exceed 150 s (0/92).
   - Hot runs overlapping a BGP (warm) run go long 88% of the time, against 4% otherwise. This is most likely
     positional: the hot write phase waits on `DB_WRITE_LOCK` behind the warm write phase. It is inferred, not
     instrumented.
   - Hot post-processing of its own new items takes a median 284 s, longer than the 150 s interval.
   - **Next:** instrument each tier run as collection, lock wait, DB write, post-processing, to tell whether write
     serialisation or post-processing is the dominant constraint before changing anything.
4. **14 failing collectors** are unchanged and pre-existing:
   - Nitter (DNS resolution);
   - Lawfare and Wikipedia (HTTP 403);
   - X-ForYou (no Chrome CDP);
   - US Congress (no key);
   - Financial Intelligence (`finance_agent` path).
