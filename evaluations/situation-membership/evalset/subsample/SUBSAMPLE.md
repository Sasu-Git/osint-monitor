# Situation membership: labelling subsample (2026-11-03)

**Status.** Drawn and frozen, **not labelled, not scored.** A stratified subsample of the frozen 379-case set
(`../cases.json`, sha256 `725d7a2d…`), so the owner labels about a third of the cases first. The full 379-case set is
unchanged and remains the **expansion set**: no file of it was edited, and its `../FREEZE.md` hashes still verify.

## 1. Why a subsample, and why 126

- 379 cases is too heavy for one labelling pass.
- About 120 cases keeps every open Situation represented and keeps the gate denominators usable:
  - all 10 positive seeds;
  - about 40–50 expected near-misses;
  - several dozen current members.
- A sampling fraction of 0.25 of each Situation's non-seed cases (at least 2 per Situation), plus all 29 seeds, gives
  **126**.

## 2. Blindness

`sample_subsample.py` reads only blind or public inputs:
- `../cases.json`, whose hash is verified before use;
- the seed list `SEED_CASES` in `../build_evalset.py` (CONTRACT-V2 section 4);
- the list of automatic Situations in `../scopes.json`.

It does **not** open:
- `../key.json`, which stays sealed until a labels freeze (PREREGISTRATION section 4);
- `owner-labels.yaml`;
- any score.

The manifest lists case ids only.

**Consequence.** The member and near-miss origins cannot be told apart before labelling. Near-misses are guaranteed
through a blind sub-stratum (below); their exact count is known only at scoring, from the key.

## 3. Strata

Seed strata:
- Every seed case is included. Each seed Development is a current member and appears in exactly one case, so its case
  is identified by Development id.

Per-Situation strata:
- All 28 open Situations are represented: 5 seeded, 23 automatic, with seeded or automatic read from `cases.json`.
- Within each Situation, the non-seed cases are split into two sub-strata, each sampled in proportion:
  - **repeated**: the Development appears in more than one case. Such a Development is unassigned, so each of these
    cases is a near-miss (PREREGISTRATION section 10).
  - **single**: the Development appears once. It is a current member or a near-miss, which only the key tells apart.
- Allocation per Situation is k = min(N, max(2, round(0.25·N))), with at least one case from each non-empty
  sub-stratum when k ≥ 2.
- Draws use `random.Random(20261103)` over sorted ids. Re-running the script gave byte-identical `manifest.json` and
  template.

| Stratum | Cases |
|---|---|
| seed_positive | 10 (6 in seeded Situations, all `russia-ukraine-war`; 2 `russia-united-states`; 2 `china-united-states`) |
| seed_negative | 10 |
| seed_boundary | 9 |
| repeated (near-miss) | 20 |
| single (member or near-miss) | 77 |
| **Total** | **126** (seeded Situations 36, automatic 90; 28/28 Situations) |

The per-Situation allocation is in `manifest.json` (`per_situation`).

## 4. Gates: PROPOSED, pending owner approval

The gates are the preregistered ones (PREREGISTRATION section 8), unchanged and still **PROPOSED**:
- ≥ 90% of owner-`MEMBER` kept;
- ≥ 70% of owner-`NOT_MEMBER` rejected;
- 0 seeded-Situation regressions on the positive seed cases.

**Seed gate basis.** The frozen gate text is "0 seeded-Situation regressions on the positive seed cases" (section 8,
line 136). Line 138–139 leaves open "whether the third gate counts all 10 positive seeds or only the 6 in seeded
Situations".
- `score_subsample.py` gates on the **6 positive seeds in seeded Situations**, which follows the gate's wording.
- It reports all 10 alongside, for information.
- This is a reading of an open point, not an approved value. The owner's gate approval settles it.

**PROPOSED, new for the subsample (not in the preregistration).** Because the subsample is a third of each Situation:
- The per-Situation metrics are reported but are **descriptive only**. Most Situations have 2–7 cases.
- Only the overall values are compared with the thresholds.

## 5. Files

| File | Role |
|---|---|
| `sample_subsample.py` | Draws the subsample and writes `manifest.json` and the labels template |
| `manifest.json` | The 126 case ids, seed, fraction, stratum counts and per-Situation allocation |
| `owner-labels-subsample.yaml` | Labels file, in the same schema as `../owner-labels.yaml`, restricted to the manifest. All 23 automatic Situations' scopes are included |
| `label_server.py` | Local labelling page (127.0.0.1). Blind: never reads `key.json`. Writes only the labels file |
| `labels_subsample.py` | `validate` / `freeze` → `LABELS-FREEZE-subsample.json`. Uses `../labels_tool.py`'s rules; that file is unchanged |
| `score_subsample.py` | Scoring with `../score.py`'s metrics restricted to the manifest. Needs the labels freeze and `--approval`. Only `--self-test` has run (synthetic) |

## 6. Order

1. The owner labels on the local page: scopes first, then the 126 cases.
2. `python labels_subsample.py validate`, then `python labels_subsample.py freeze`.
3. The owner approves the gates (this section's reading of the seed gate, or an amended one) and approves scoring
   separately.
4. Only then `python score_subsample.py --approval "<who, when>"`.
5. The rest of the 379 set is labelled later as expansion. Its own freeze and `score.py` are unchanged.
