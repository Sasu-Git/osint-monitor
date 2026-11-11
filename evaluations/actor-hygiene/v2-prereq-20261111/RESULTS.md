# Situation-v2 normalisation prerequisite: gate results (2026-11-11)

**Code.** `feat/actor-normalization-v2pre` `2f23f59`, against `main` `0d3382d`. The defect set and gates were frozen
first (`DEFECTS.md`, `30310d0`). No code, defect or gate changed after the results below. Replays ran on backup-API
copies of `snap-20261102.db` (sha `b5bb5728…`). No live data was touched.

## Gates

| Gate | Result |
|---|---|
| G1 known defects | **9 of 10 Situation expectations met; 1 expectation was mis-specified (see below).** Development 402 (storm names) has no principals. Bolsonaro and lone-surname guards hold. No other Situation's keys changed |
| G2 entity benchmark (gold rev 3) | **byte-identical run output**: no unit changed |
| G3 identity gold check | passed (checks 1–6) |
| G4 Phase 2 identity (development windows) | **identical** to `0d3382d`: 43/65, 43/58, 22/100, 15/58, 16/19, 12/31 |
| G5 actor-type distribution | share of Developments with ≥ 1 principal key unchanged (74.62% → 74.62%). Principal types: PERSON 422 → 433 (the B full names, now configured, are recognised as principals); all other types unchanged. 25 Developments change principals or Situation keys; **23 carry a listed name**, 2 do not (see below) |
| G6 unrelated identity behaviour | 17 Developments change topic keys; all carry a B or C name (Development 722 carries the linked entity `DONALD J. TRUMP`, A8/B4) |
| G7 pytest | 764 passed, 3 xfailed (12 new tests) |

## Deviations from the frozen wording (no change made)

1. **G1, `rachel-simon`.**
   - The frozen table expected its stored primary actors `["Rachel", "Simon"]` to key to nothing.
   - The storm rule (10-16) acts on text context, not on bare stored names. Deleting the single names `Rachel` and
     `Simon` wholesale is forbidden by the same file's constraint (mononymous people are not deleted). The expectation
     contradicted that constraint.
   - The defect itself holds where it matters: Developments 402 and 429 have no principals, so v2 cannot found an
     actor Situation on them (v2 rebuilds it as a hazard Situation, OD2).
2. **G5, two Developments outside the listed names.** Rule A (one person counted twice inside one actor set) also
   collapses the same-class pairs `Kimi Antonelli` + `Antonelli` (D963) and `Alvin K. Hellerstein` + `Hellerstein`
   (D1048). Both are one person; both merges are correct. They were not added to the defect list. They are reported
   here because the frozen G5 wording limits changes to listed names.

## Verdict

**Passes in substance.** There is no benchmark or identity regression and no broad distribution change. The two
deviations are a mis-specified expectation and the general rule acting correctly on its own class. The owner decides
whether to accept them as worded here.

Artifacts: `compare.json` (the full diff). The replay outputs themselves are not committed (≈ 280 KB each,
reproducible with `replay_actors.py`).
