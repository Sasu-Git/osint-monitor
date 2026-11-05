# Pair-matcher candidate: production soak checklist (prepared before deployment)

**Schedule.** C1 after ≥ 3 warm runs, about 2 h later, then C2 at about 24 h, as in the deployment runbook.

**Comparison baseline.** The Candidate B soak on `e2c7afe`: runs from 2026-10-30 14:20Z to the deploy, in the run
ledger and `data/deploy/20261030-candB/`. Use
`scripts/run_timing.py --db <live DB> --since <window start>` for both windows. Compare completed runs only, and
report host sleep and downtime separately, as at the Candidate A and B C2.

## Correctness (all must hold)

| # | Check | How | Pass |
|---|---|---|---|
| C1 | Failed runs attributable to the candidate | `postdeploy_check.py --runtime`; `daemon-exits.jsonl`; `daemon.err.log` tracebacks in `provenance/resolve.py` | **0** |
| C2 | Development membership drift on existing Developments | pre-deploy membership snapshot vs C2 (as in the Candidate A/B C2: memberships dropped or moved) | **0** dropped, **0** moved |
| C3 | Duplicate memberships | `postdeploy_check.py` | **0** |
| C4 | Single-source regression | `postdeploy_check.py` (new narrative Developments with < 2 sources) | **0** |
| C5 | Situation churn | new Situations within the post-deploy bound (≤ 3); none disappeared | as at Candidate B C2 |
| C6 | Identity / clustering gates | unchanged from the readiness gates (already identical offline). Re-run only if anything above fails | identical |
| C7 | Provenance output on live data | read-only: on a C2 snapshot, `assess_event` for the 20 newest and the 5 largest Developments under the deployed code vs `production-stable-20261102` code | byte-identical |

## Performance (material improvement; exact offline numbers are **not** required)

| # | Metric | Source | Expectation |
|---|---|---|---|
| P1 | Corroboration stage duration | `run_timing.py` per-stage `corroboration` | median **≥ 50% lower** than the baseline window (offline: −81%) |
| P2 | Provenance/matcher time where visible | the corroboration and summaries stages, which are dominated by provenance | lower; summaries not higher |
| P3 | Write-lock wait | `run_timing.py` `lock_wait` per tier | median lower than baseline (expected; recorded, not gated) |
| P4 | Warm cadence | finished warm runs per awake hour | higher or equal |
| P5 | Hot cadence | finished hot runs per awake hour | higher or equal |
| P6 | Skipped / silent ticks | `collection_gaps.jsonl` `tier_silence` while the host was awake | fewer or equal (host sleep excluded) |
| P7 | Total run time | `run_timing.py` `total` per tier | median lower |

**Verdict.**
- **PASS:** every correctness check holds, and P1 holds.
- **P3–P7:** reported. A regression in any of them, with the host awake, is investigated before promotion.
- **FAIL:** any correctness check fails. Roll back to `production-stable-20261102`; no data restore is needed.

## Not part of this soak

- **Web:** the production web server keeps `deploy-web-20261102`. Adopting the optimization there is a separate, later
  web redeploy after daemon acceptance.
- **Bundling:** no frontend, provenance-logging, collector or Situation-rule change ships with this candidate.
