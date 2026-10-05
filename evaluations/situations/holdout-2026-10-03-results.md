# Situation creation hold-out: results and decision

Scored once on 2026-10-05, against the pre-registration in `holdout-2026-10-03.md`.
There were no implementation, threshold, label, grouping or benchmark changes after the hold-out data was seen.

## Frozen inputs

| Item | Value |
|---|---|
| Frozen branch | `feat/situation-coverage` = `ba723b3245b64351a23d86cf63854129579f8ee8`, not modified |
| Evaluation branch | `eval/situation-holdout-2026-10-03`, branched from `ba723b3`; it contains only evaluation artifacts |
| Daemon DB snapshot | SQLite backup API, source opened `mode=ro`. sha256 `1934c11a…7c83a`, `integrity_check` ok |
| Window | 2026-09-29 12:00 to 2026-10-03 12:00 UTC, end exclusive |
| Developments | 63, `developments.jsonl` sha256 `c10c776c…ed495`. Committed in `10fb9d6` before labelling |
| Candidate pairs | 11 development pairs that share a canonical principal-actor pair |
| Labels | Separate-context blind agent: 4 SAME_SITUATION, 5 DIFFERENT_SITUATION, 2 AMBIGUOUS. sha256 `54462177…`, committed in `79736b9` before scoring |
| Score | One `holdout_tool.py score` run. Output in `holdout-2026-10-03/score.json` |

**Collection gaps:** the window had 59.3 of 96 hours without warm-tier collection, caused by host suspend. The longest stall was 10-02 14:11 to 10-03 10:51, 20.7 h. The gaps were recorded before labelling in `holdout-2026-10-03/collection-gaps.json`. Recurrence is therefore sparser than with continuous collection. Per the pre-registration, the window was not extended.

## Seed assignments (separate from creation, identical under all policies)

| Seed | Developments |
|---|---|
| `russia-ukraine-war` | d84, d99, d101 |
| `gaza-ceasefire` | d65 |

Three of the four SAME_SITUATION pairs (d84–d99, d84–d101, d99–d101) are Russia-Ukraine pairs, and the seed already covers them. The score tool lists them as "missed" because it counts only joins made through creation. They are not missed persistent situations.

## Results by policy

Precision is computed over member pairs of created Situations. "Decided" excludes AMBIGUOUS pairs.

| Metric | A: exact actor set | B: actor pair ≥ 0.40 | Actor pair ≥ 0.50 |
|---|---|---|---|
| Situations created | 1 | 3 | 3 |
| Developments assigned through creation | 2 | 7 | 6 |
| Member pairs: SAME / DIFFERENT / AMBIGUOUS | 1 / 0 / 0 | 1 / 3 / 1 | 1 / 1 / 1 |
| **Creation precision, all pairs** | **1/1 = 1.00** | 1/5 = 0.20 | 1/3 = 0.33 |
| Creation precision, decided pairs | 1/1 = 1.00 | 1/4 = 0.25 | 1/2 = 0.50 |
| Correct Situations created | 1 (`eritrea-ethiopia`) | 1 (`eritrea-ethiopia`) | 1 (`eritrea-ethiopia`) |
| **False Situations created** (all member pairs DIFFERENT) | 0 | 1 (`china-united-states`) | 1 (`china-united-states`) |
| **False Situation joins** (DIFFERENT pairs joined) | 0 | 3 | 1 |
| Ambiguous Situations created | 0 | 1 (`raytheon-united-states`) | 1 (`raytheon-united-states`) |
| **Coverage**: SAME pairs captured by seed or creation | 4/4 | 4/4 | 4/4 |
| SAME pairs captured by creation, beyond the seeds | 1/1 | 1/1 | 1/1 |
| Coverage gain over A | none | **0 SAME pairs** (+5 developments, all in false or ambiguous groups) | **0 SAME pairs** (+4 developments, all in false or ambiguous groups) |
| **Missed persistent Situations** | 0 | 0 | 0 |

## Case-level results

**C1 `eritrea-ethiopia` (d86 + d110): correct under all three policies.**
The Ethiopia-Eritrea diplomatic rupture is tied to the Tigray fighting. Similarity is 0.92, and the exact actor set {Eritrea, Ethiopia} already founds this Situation. Actor-pair creation adds nothing here. The headline item of d86 is a Somalia/Baidoa piece, which is a clustering-level outlier and does not affect the Situation decision.

**C2 `china-united-states` at 0.40 (d88 + d120 + d112): false Situation creation, 3 false joins.**
The group contains:
- d88: the Xi-Trump summit and Xi's National Day speech;
- d120: China in Latin America (Cuba, Panama, a Latinobarómetro poll);
- d112: European competitiveness and Spain-China ties.

The labeller marked all three member pairs DIFFERENT_SITUATION. The similarities are d88–d112 0.35, d88–d120 0.51 and d112–d120 0.42. d112 entered with a similarity of 0.35 to the founder only because it is 0.42 from d120. This reproduces the pre-registered **"one close neighbour"** hypothesis, the same pattern as the in-sample Greenland and panda-loan joins. US-China is a broad pair, and it collapsed three unrelated storylines.

**C3 `china-united-states` at 0.50 (d88 + d120): false Situation creation, 1 false join.**
The 0.50 threshold removes the chained Europe piece (d112), but the founding pair (0.51) is itself DIFFERENT_SITUATION. The stricter threshold reduces the damage but does not prevent a false broad-pair Situation.

**C4 `raytheon-united-states` (d73 + d117): AMBIGUOUS, created at 0.40 and 0.50.**
The pair is two Raytheon multiyear missile contracts (AMRAAM $20.7B and SM-6 $24.4B), with similarity 0.68. A procurement ramp-up has a corporate actor pair, and it is unclear whether it is a geopolitical state of affairs. This is the same persistence question as `france-pope` in the development data.

**Non-joins that were correct:**
- **d115 (Taiwan F-16V delivery) did not join d88 under any policy.** That pair is labelled AMBIGUOUS, so no policy was penalised either way.
- **d115 did not join d112 or d120 under any policy.** Both pairs are labelled DIFFERENT.

**Broad pairs present:**
- **US-China:** collapsed under both actor-pair thresholds (C2, C3).
- **Russia-Ukraine:** handled entirely by the seed, with no created Situation.
- **US-Iran and Israel-Iran:** no qualifying recurrence in the window.

## Difference from in-sample results

| | In-sample (874 frozen benchmark developments, gold storylines) | Hold-out (63 developments, blind Situation labels) |
|---|---|---|
| A exact set | 20 Situations / 45 developments / precision 0.77 | 1 / 2 / 1.00 |
| B pair ≥ 0.40 | 22 / 57 / precision **0.89** | 3 / 7 / precision **0.20** (0.25 decided) |
| Pair ≥ 0.50 | Not recorded in the creation commit. On live development data it avoided the Greenland and panda joins | 3 / 6 / precision 0.33 (0.50 decided) |
| Gain from B over A | +2 Situations, +12 developments, precision +0.12 | +2 Situations, +5 developments, 0 extra correct pairs, precision −0.80 |

In-sample, the 0.40 rule raised precision over exact sets. On the hold-out it reversed: every development it added beyond exact sets landed in a false or ambiguous Situation.

Two caveats limit how far this can be read:
- **The hold-out is small.** It has 11 pairs, and 59 h of collection were lost to gaps.
- **The labels measure a different thing.** The in-sample gold was storyline continuity. The hold-out labels are persistent-Situation identity, under the stricter rule that a multi-day event is not a Situation by itself.

The failure is not random noise, however. The failure mode is the one pre-registered as a hypothesis from the development data: chaining through one close neighbour in a broad pair. It recurred on unseen data at both thresholds.

## Decision

Against the pre-registered rule:

- **ENABLE ACTOR-PAIR CREATION fails three of its four conditions:**
  - precision is not high (0.20);
  - false creation is not rare (1 of 3 created Situations is false, and 1 more is ambiguous);
  - the broad US-China pair collapsed unrelated storylines.

  It also gives no coverage gain over exact sets.
- **0.50 does not rescue it.** It still creates the false US-China Situation, and it adds no correct coverage. The pre-registration also defined 0.50 as diagnostic only.
- The result maps to the pre-registered **KEEP IMPLEMENTATION BUT DEFAULT OFF**. The mechanism is not shown useful here, and false joins are material. A single small window is not enough evidence to call actor-pair identity fundamentally broken (REJECT).

**Recommendation: KEEP EXACT ACTOR-SET.**
- Production stays on `create_by: actor_set`.
- `feat/situation-coverage` is not merged as configured: its config defaults to `actor_pair` 0.40.
- There is no tuning and no threshold change on the strength of this hold-out.
- Any future actor-pair work needs a new pre-registration and a fresh window. The window should have continuous collection, and the Situation-persistence criterion should be settled before labelling.

## Source count and modality summary

- **Evaluated:**
  - 63 developments in the window;
  - 922 raw items fetched in the window;
  - 11 labelled pairs;
  - 3 policies scored.
- **Modality:** the developments are news (RSS) clusters from the live daemon, worktree `a9edd18`, DB `data/eval/window-2026-09-25.db`.
- **No modality beyond news contributed:** Situation creation uses principal actors and embeddings only.
- **Collection coverage:** about 38%, which is 36.7 of 96 hours with warm-tier ticks.
