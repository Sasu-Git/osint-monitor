# 24 h soak report: `deploy-candidate-20261005` (`5f046b3`, migration 6)

**Soak window:** 2026-10-05 13:00:53Z → 2026-10-06 13:06:04Z.

**Deployed code:** frozen at `5f046b3` throughout. The daemon worktree had no tracked changes, and all 385 runs
carry that SHA.

**Process:** one daemon process tree, PIDs 26088/16644, alive for the whole soak.

## 1. Full wall-clock soak

| | Value |
|---|---|
| Wall clock | 24.09 h |
| Pipeline runs | 385: hot 290, warm 81, cold 14. All `ok`, 0 failed. |
| Wall-clock coverage | warm 55.7%, hot 50.1%, cold 54.2% |
| New items / memberships | 1,933 / 597, all run-stamped |
| New Developments | 89. 26 came from the source-expansion backlog in the first 2 h. |
| New Situations | 3 (see section 5) |

## 2. Host-awake collection coverage

Coverage of the 13.45 h the host was awake:

| Tier | Coverage | Note |
|---|---|---|
| Warm | 96.1% | |
| Hot | 88.5% | DNS and BGP monitors run 60–128 s, so hot ticks are skipped (follow-up 4) |
| Cold | 78.6% | runs missed right after each wake are skipped, not replayed, by design |

## 3. Standby intervals and cause

Source: Kernel-Power 506/507 events, in UTC. Total standby: **10.63 h**.

| From | To | Length | Cause |
|---|---|---|---|
| 10-05 14:27 | 15:40 | 1.21 h | Modern Standby, **Idle Timeout**. The first keep-awake held `ES_SYSTEM_REQUIRED` only. Fixed at 15:45Z with `--display`. |
| 10-05 16:02 | 18:23 | 2.35 h | **Lid closed**, then **Battery Drain Budget** (on battery) |
| 10-05 23:06 | 10-06 05:32 | 6.43 h | **Lid closed**, then **Battery Drain Budget** |
| 10-06 05:50 | 06:28 | 0.63 h | **Lid closed** |

- **Power source.** The machine alternated between AC and battery, with 9 power-source changes. It is on battery
  (90%) at the time of this report.
- **No keep-awake can prevent these.** They are lid-close and battery standby.
- **The daemon handled every interval as designed:**
  - recorded `tier_silence` and `missed_run` gaps with cause `unknown`;
  - skipped stale runs instead of replaying them;
  - resumed by itself.
- **Not a daemon failure.** These are host-power interruptions.

## 4. Hard-trigger results

| Trigger | Result |
|---|---|
| Duplicate Development membership | **0**: PASS |
| Missing `pipeline_runs` / run provenance | 385 runs, all with the target SHA and a config hash. 1,933/1,933 items and 597/597 memberships stamped. Stage statuses are present on every run that had new items. The 285 "without stages" are no-op runs (follow-up 2). PASS |
| Integrity / FK | `integrity_check` ok, 0 FK violations: PASS |
| Collector outage generating a geopolitical finding | **None**. The imagery (FIRMS) outage was suppressed at every alert cycle. The outage-type alerts are below. PASS |
| Unexplained Development / Situation drift | Explained (see the two notes below): PASS |
| Alert delivery regression | None. Delivery **improved**: 168/168 dispatched alerts delivered, against 0/340 of the same types in the 7 days before. `trend` alerts were never dispatched, before or after. PASS |
| Daemon instability | 0 failed runs, no hang, no restart, stable across 4 standby/resume cycles: PASS |

**Outage-type alerts.** There were three, all non-geopolitical:
- one false "Signal restored: imagery" transition at 13:11Z (follow-up 1);
- two "Source resumed" alerts at 14:01Z, before any standby, with no gap history from the old daemon
  (follow-up 6).

**Development drift is explained.** The 89 new Developments are 3.7/h on wall clock and about 4.7/h of awake
time after the backlog.
- **More sources.** There are now 51 sources, against 23 before: GDELT plus es, it and institutional feeds.
- **All multi-source.** Single-source: 0.
- **Cross-language splits.** Some occurrences appear as separate en/es/it Developments, a known limitation of
  the English-only embeddings.
- **Off-interest topics.** Sports items surface, because relevance gating (P1) is not built.

**Situations are explained, one of them wrong:**
- `nato-russia`: genuine.
- `bolsonaro-fl-vio-bolsonaro`: Brazil election coverage; coherent.
- `estados-unidos-united-states`: **wrong** (follow-up 8).

## 5. New operational follow-ups (not patched, for the post-soak fix branch)

8. **Multilingual actor aliasing.** "Estados Unidos" is not normalised to United States. That produced the
   Situation `estados-unidos-united-states`, whose actor set is the United States twice. It groups one Fairford
   bomber occurrence reported in English (E135) and Spanish (E157). Add es/it country and organisation aliases.
   Also review the ambiguity of "Bolsonaro" (Jair vs Flávio). Situations are derived, so the bad one can be
   recomputed after the fix.
9. **Trend anomaly flood after the source expansion.** There were 377 `trend` alerts in 24 h, against about
   17/day before ("Anomalous activity: Bogota / Insurance / Sykes …"). Entity-mention baselines were built on
   the old source set, so the new sources read as anomalies. These are collection-change artefacts, not world
   signals.
   - They are not delivered, but they are stored as alerts.
   - Fix: reset or rebuild the trend baselines when the source set changes, or normalise per source.
   - Until then, treat trend alerts as untrusted.
10. **Host power for collection.** Lid-close and battery standby caused 10.6 h of the 24 h without collection.
    For production collection, use a host on AC with the lid open (or lid action "Do nothing"), or a
    non-sleeping machine. The runbook's pre-soak checklist should require AC and lid state.

Recorded earlier in `post-soak-followups.md`:

| # | Follow-up |
|---|---|
| 1 | false "Signal restored" transition |
| 2 | stage check on no-op runs |
| 3 | backlog-aware Development growth check |
| 4 | DNS / BGP latency and skipped hot ticks |
| 5 | Nitter / Lawfare / X-ForYou failures, plus US Congress and Financial Intelligence (Quant) |
| 6 | silence-break alerts without gap history |
| 7 | keep-awake `--display` on Modern Standby |

## Decision

**SOAK PASSED WITH FOLLOW-UPS**

No hard rollback trigger fired. Follow-ups 8 and 9 are data-quality issues introduced by the source expansion.
They should be the first items on the post-soak fix branch.
