# Iteration 3, step 4: scoring rule (frozen before any system output is produced, 2026-11-11)

No scoring rule for the fresh sample existed in a frozen document. This one restates iteration 1/2's metric
definitions (`../contract-eval/evaluate.py`, frozen) with the owner's gold labels in place of the 2026-11-02 audit's
hand verdicts. No new gate is introduced. The gates below are iteration 1's, still `PROPOSED` (not approved), so every
pass/fail statement is **against PROPOSED gates, report-only**.

## Cases and gold

- The 100 frozen sample Developments (`../iter3-sample/manifest.json`, D1199–D1341), on snapshot
  `snap-20261105.db` (`d85cbac4…`).
- Two label bases, scored separately (owner, 2026-11-10):
  - **primary:** the blind first answer per case (first line per case in `owner-label-history.jsonl`, `23fe6fec…`);
  - **secondary:** the frozen final labels (`owner-labels.yaml`, `78b13748…`).
  - If a system's pass/fail against the PROPOSED gates differs between the bases, its result is **inconclusive**.
- Gold is `event_country` (ISO3) or `NONE`. `event_place` and `note` are not scored.

## Systems

| Id | System | Country it gives |
|---|---|---|
| `B0` | **baseline:** the deployed map, `d06af11` | stored point's country (`point_country`) when the map shows it (`shown`), else `NONE`; read from the frozen audit output `audit-all-20261105.json` (`07442444…`) |
| `B1` | **secondary baseline:** map with aliases, `346456f` | the same, from `audit.py` (`b794902`, `359fab29…`) re-run with `PYTHONPATH` = `346456f` and `d06af11`'s `config/sources.yaml` on the same snapshot |
| `I1` | iteration 1, module at `d842feb` (`afbd4baf…`) | location module country through the frozen lookup |
| `I2` | iteration 2, module at `a73b9f3` | same |
| `I3-2a`, `I3-3a`, `I3-4a`, `I3-5a`, `I3-all` | iteration 3 (`c5e45f4`, module blob `145a1a1e…`) with one rule, or all four | same |

Module country: `decide()`'s `country` mapped by the frozen lookup (`LOOKUP-FREEZE.md`); `NONE` when the role is
`NONE`, when only a region is given, or when the country has no code.
Consistency check (reported, not scored): `decide(rules=())` on the iteration-3 code must equal `I2` on every case
(RULES.md: with no rules, `decide()` is iteration 2 unchanged).

## Metrics (no composite), per system and per label basis

Outcome per case, system country S vs gold G:
- G is a country: `CORRECT` (S = G), `MISSED` (S = NONE), `WRONG_COUNTRY` (S another country);
- G is `NONE`: `CORRECT_NONE` (S = NONE), `SPURIOUS` (S a country).

Iteration 1/2 metrics, with the audit verdicts derived from gold and the baseline map (`B0`):
- **W set:** the map shows a point whose country ≠ G (G = `NONE` included). **W removed:** the system's country is
  not the map's wrong country (as `evaluate.py`: `REMOVED` when the contract does not put it in the stored point's
  country again).
- **C set:** the map shows a point whose country = G. **C preserved:** the system's country = G.
- **Unmapped set** (the map shows nothing): counts of `CORRECT`, `CORRECT_NONE`, `MISSED`, `WRONG_COUNTRY`,
  `SPURIOUS`.
- Overall: the outcome counts on all 100.

## Gates (iteration 1's, PROPOSED, not approved)

- W removed ≥ 80%;
- C preserved ≥ 90%.

A system "meets the PROPOSED gates" on a basis when both hold. For `B0` itself the W/C split is definitional (W removed
0%, C preserved 100%), so the baselines are reported by outcome counts only.

## Run (once)

1. `baseline_outputs.py` → `outputs/B0.json`, `outputs/B1.json` (B1 needs the `audit.py` re-run output).
2. `locate.py`, once per system, with `PYTHONPATH` = that system's code → `outputs/<id>.json`.
3. `score.py` → `results.json`, `RESULTS.md`. No rule, lookup, label or sample change after this point.

## Continuity (FREEZE.md step 5, second sentence)

Iterations 1 and 2 are re-scored on their own frozen inputs (2026-11-02 snapshot, audit cases, acceptance cases,
`evaluate.py` `a922…`) under the frozen lookup. `rescore_iter12.py` executes the frozen `evaluate.py` with exactly one
line replaced, the `iso` lookup line (asserted to occur once), and writes new files beside the historical
`results.json`, which are not overwritten.
