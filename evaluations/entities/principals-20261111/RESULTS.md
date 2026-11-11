# Principal-actor extraction (track 3): gate results (2026-11-11)

**Code.** `fix/v2-upstream-principals` `74cdaea` against `b695aa0`. Diagnosis and gate were frozen first (`198bdac`).
Nothing changed after these results. Baselines for `b695aa0` are the normalisation-track runs (same code).
Replays ran on backup-API copies of `snap-20261102.db`.

## The change (P-A only)

Actor support is counted per canonical actor, not per name, as the module documents. When no name of an actor
reaches the threshold alone but its names together do, its best-supported name becomes principal; the headline gate
applies at actor level. Names that already pass are untouched.

## Gates

| Gate | Result |
|---|---|
| 1 Entity benchmark (gold rev 3) | **Fails as frozen ("no metric drops")**. Principal recall 20/26 → **22/26** (2 fixed: D03 U.S. Navy, D25 European Commission; 0 introduced). Principal precision 20/25 (80.0%) → 22/28 (78.6%): **1 introduced**, D05 `france`. In "Saudi Arabia allies line up support…" France (2.5) + Macron (2.0) pass the 3.0 threshold together; the gold lists France as a secondary actor, not a principal. Every other metric is identical |
| 2 Identity gold check | passed (checks 1–6) |
| 3 Phase 2 identity (development windows) | identical: 43/65, 43/58, 22/100, 15/58, 16/19, 12/31 |
| 4 Snapshot replay diff | **Fails as frozen on wording.** 34 Developments change, **0 lose a principal**, 30 are diagnosed `split_support` Developments. The other 4 are the same mechanism on names the English-centric diagnosis probe could not see: D270 Russia (`Mosca`, `Cremlino`, `Rusia`), D1051 European Union (`Ue`, `UE`), D436 and D538 UN Security Council. They are reported as unexplained, as the gate requires |
| 5 pytest | 767 passed, 3 xfailed (3 new tests) |

**Coverage.**

| Measure | `b695aa0` | `74cdaea` |
|---|---|---|
| Developments with principals | 74.79% | 76.13% |
| Developments with two or more Situation keys | 300 | 313 |

## Verdict

The defect is real and the fix does what the diagnosis said: +2 recall units, no lost principals, and 13 more
Developments that present two parties. It **does not pass the gate as frozen**. One precision unit (D05 France,
a secondary actor that is named twice) is introduced, and four changes fall outside the probe's list. On the four:
- D270 and D1051 look correct;
- D436 (Security Council "hears", Colombia) is multilateral framing that the owner's convention would not call a
  principal;
- D538 (Security Council adopts a Haiti resolution) is plausible.

The owner decides: accept with the D05 and D436 errors, or keep `b695aa0`'s behaviour. No further change was made.

## Remaining misses by pattern (from `DIAGNOSIS.md`; not extraction defects, or not repeated)

| Pattern | Missed keys | Owner of the decision |
|---|---:|---|
| One acting headline in a 3+-item Development (threshold) | 458 | product: selection threshold |
| Place standing for a party (Gaza → Palestine) | 33 (Gaza) of 339 `location` | normalisation (`represents`) |
| Coercion targets ("Russia warns NATO") | 61 | owner gold convention: not principals |
| Multilateral framing (UN, NATO, EU) | 44 | owner convention |
| Probe noise / merged Developments | most of 297 `no_mention` | segmentation (merged Developments) |
| Single cases (pandas as PERSON, G20 as the actor) | 2 | not acted on |
