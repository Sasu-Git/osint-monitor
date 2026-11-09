# Corroboration config-once candidate: production soak checklist (frozen before deployment, 2026-11-05)

**Candidate.** `6d6e7c8` (`perf/corroboration-config-once`), stacked on `bc0d5c0` = `production-stable-20261105`.
Not deployed. Deployment needs owner go-ahead and the normal runbook.

**Schedule.** C1 after ≥ 3 warm runs, about 2 h later, then C2 at about 24 h of **awake** runtime, as for the
pair-matcher. Wall time, awake runtime and host outages are reported separately.

**Comparison baseline (owner ruling 2026-11-05).** The accepted pair-matcher C2 window on `bc0d5c0`: completed runs
from 2026-11-02 18:06Z to the C2 snapshot (2026-11-05 11:55:04Z), as reported by
`scripts/run_timing.py --since "2026-11-02 18:06"` in `data/deploy/20261102-perf/c2/run-timing.txt`
(sha256 `eb8c7ae3d57628d8fd09cc59aedc48de454505a5d1c1b26e4f2340bf96f2a0b5`). The candidate window is measured the
same way, from the candidate's deploy time. Completed runs only.

## Correctness (hard gates; all must hold)

| # | Check | How | Pass |
|---|---|---|---|
| E | Offline equivalence | `RESULT.md` on this branch (SHA unchanged, reused): 0 mismatches / 1,198 on every path | **0** (already met) |
| C1 | Failed runs attributable to the candidate | `postdeploy_check.py --runtime`; `daemon-exits.jsonl`; `daemon.err.log` tracebacks in `processors/corroboration.py` or `provenance/` | **0** |
| C2 | Development membership drift on existing Developments | pre-deploy membership snapshot vs C2: memberships dropped or moved | **0** dropped, **0** moved |
| C3 | Duplicate memberships | `postdeploy_check.py` | **0** |
| C4 | Single-source regression | `postdeploy_check.py` | **0** |
| C5 | Situation churn | new Situations within the post-deploy bound (≤ 3); none disappeared | as at the pair-matcher C2 |
| C6 | Identity / clustering gates | not touched by this candidate; re-run only if anything above fails | identical |
| C7 | Provenance and corroboration on live data | read-only, on a C2 snapshot: for the 20 newest and the 5 largest Developments, `assess_event` and `compute_corroboration_score` under the deployed code vs `production-stable-20261105` code | byte-identical |

## Speed non-regression (owner ruling 2026-11-05)

Stage: `corroboration`, per tier, from `run_timing.py`. Frozen baseline values (seconds):

| Tier | Baseline median | Baseline p90 | Baseline runs with the stage |
|---|---|---|---|
| hot | 232 | 291 | 52 |
| warm | 229 | 291 | 108 |
| cold | 230 | 299 | 9 |

| Outcome | Rule, per tier |
|---|---|
| **Regression flag** | candidate median > baseline p90 for that tier |
| **Strong improvement claim** | candidate p90 < baseline median for that tier |
| Neither | reported as no material change |

There is no required improvement percentage. The offline result (pass 166.1 → 23.8 s) is an estimate, not a gate.

## Descriptive (reported, not gated)

- Summaries stage (it calls the same provenance code), `lock_wait`, `total` per tier, hot/warm cadence per awake hour,
  `tier_silence` gaps while awake.
- The web server (`deploy-web-20261105`) was down for most of the baseline window and is up during the candidate
  window. Its reads are recorded as a difference between the windows, not corrected for.

## Verdict

- **FAIL:** any correctness check fails. Roll back to `production-stable-20261105` (`bc0d5c0`), code-only; no data
  restore needed. The final pre-deploy backup is kept.
- **Regression flag on any tier:** reported to the owner before acceptance. What follows is an owner decision.
- **PASS:** every correctness check holds and no tier raises a regression flag.
- After acceptance the web server needs a second catch-up: this candidate changes `provenance/resolve.py` and
  `corroboration.py`, which the web imports.
