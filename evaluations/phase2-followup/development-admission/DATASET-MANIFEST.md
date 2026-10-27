# Development admission: development dataset manifest

Frozen **before any variant is measured**. Hashes are sha256 over LF bytes. **Sealed holdouts are excluded and were
not opened**: `evaluations/relations/holdout/`, `evaluations/identity/holdout-xlang/`. The Phase 2 holdout window
(2026-08-31) is excluded from development and is used once, as a veto, after a candidate is frozen.

## Existing frozen sets (unchanged; referenced by commit and hash)

| Part | Source | Count | sha256 |
|---|---|---|---|
| Identity gold rev 2 (Phase 2 development pairs: windows 2026-08-21, 2026-09-25, 2026-09-30-multilingual; development split only) | `evaluations/identity/gold/identity-gold.yaml` @fix/identity-defects 7fdd674 | 158 scored (58 SAME, 100 DIFFERENT, 1 AMBIGUOUS excluded) | `cc98765b7506b9faa3b81913655978c23afc0d21202e8b69e85c1217ffa2cc58` |
| Identity gold rev 3/4 additions (windows 2026-09-30-multilingual, 2026-10-03-live, 2026-10-05-live) | `identity-gold-rev3-additions.yaml`, same commit | 74 (all development) | `a92b66f2309162c1378a2b0164a34c11534a2924da3ab88944abc75616825d6b` |
| Gold manifest (rev 4) | `evaluations/identity/gold/manifest.yaml` | | `0166da66fee5adb10267f4af2a309f70a96ebc136a0804773b26f179bbef9670` |
| Identity windows manifest | `evaluations/identity/manifest.yaml` | | `5707bbf514319b24fe1621aad2955a73bc9796ab9b65cd4a357ea6a6870e0a25` |
| Frozen defect set | `evaluations/identity/defects/defect-cases.json` @e98a0fe (unchanged at 7fdd674) | 128: 42 OVERMERGE, 23 controls (13 SAME, 10 DIFFERENT), 43 cross-language miss, 17 same-language recall miss, … | `fafc8abb4b7d5f1eec1e5286a251ab32a5a650e614e8e4fcc33dc3472764a681` |
| Defect set manifest | `evaluations/identity/defects/manifest.yaml` | | `b9837e6858f38284d0fcc6611d77cfc588ce5caa5654b00418953ec5a7b9d5f6` |
| Phase 2 development baseline (current code) | `evaluations/identity/runs/phase2-dev-actor-hygiene.json` @fix/actor-hygiene | precision 43/65, recall 43/58, DIFFERENT kept together 22/100, SAME kept apart 15/58, ID stability 16/19, mixed Developments 12/31 | `d40f671f6f0f546904a626f6923cd44668d2f85283daf9b8d069b4a1dcec85c7` |
| Relation BLOCKED_BY_IDENTITY cases (relation gold rev 2, development; not the sealed relation holdout) | `evaluations/relations/runtime-eligibility-rev2.yaml` @feat/phase3-relations bbae126 | 22 scored blocked cases in 11 Developments (28 with unscored; 13 canonical positives) | `0e92d0672af5a4776075c67e089a5d4b41b3cc4e5f6822b6eb104a48e56a3475` |
| Clustering out-of-sample cross-source SAME (segmentation v2 validation) | `evaluations/clustering/segmentation-compatibility.md` @main | 44/49 at the current code | (document) |

**Window item files** (replay inputs):

| Window | sha256 |
|---|---|
| clustering 2026-08-21 | `c4932b5c4acf7d7566efd87b27a25dcb3ce78410c836ae1565463336ea860814` |
| clustering 2026-09-25 | `dd84b77e1b99c487396e1dc46411ea626ec49b005f98840e6a2f4dbba6affaef` |
| clustering 2026-09-10 | `fb1aa49e45d3315a4e8acc8c9f00a5de6205e3384bcd76e95fe46b169f8b1374` |
| clustering 2026-09-27-live | `7909656a6398bba461bb682c0b61ea2e852f0879be2bb7eec156d26b58bb994a` |
| clustering 2026-09-29-live | `bc19462d9e00a996b1faf626bab783217d32fabc598877254edc656cc8c2d781` |
| identity 2026-09-30-multilingual | `492e17ce0ed0121d5e0ceafc0bdbb376e94fe4a0245880f74fd0cc1c3fb264d9` |
| identity 2026-10-03-live | `f66e02726930173fa10ca226a09cceb492700fc40441f481f2f2ff892c06fd46` |
| identity 2026-10-05-live | `3ea43a325af80b202d45dbcd4749c1282fe4d6535e247a3c0eb418c0cb5a4a2e` |

## New frozen parts (`dataset/`, built by `dataset/build_dataset.py`, seed 20261027)

**Input:**
- `data/eval/snapshot-20261027-forensic.db`, sha256
  `3c0b2cd9c9a6e2347a055c62b1f88b7800f9d7b82228370983d48203ad0b4a39`. A read-only copy of the 2026-10-27 live
  snapshot (SQLite backup API from a `mode=ro` source). Under the retention rule this is the sole input of a frozen
  evaluation: **keep it**.
- `../forensics/giant-developments/blast-radius.csv`.

| File | Contents | sha256 |
|---|---|---|
| `relay-set.json` | the 24 relay-signature Developments (forensic categories A and B: long + chain), 2,856 items | `e7580daeb7e393c9c06d6dca6ee4491d2d6024a4083f1d1a0aee7e6e40f7e68d` |
| `giant-label-sample.json` | the 8 giants: 38 founder items + 128 later members (4 attachment-time quartiles × 4), to be labelled | see `dataset/FREEZE.json` |
| `large-occurrence-candidates.json` | the 6 largest Developments that are neither relay-signature nor giant (D119, D124, D67, D162, D923, D786), 8 members each, for owner review as possible legitimate large occurrences | see `dataset/FREEZE.json` |
| `small-controls.json` | 60 random corroborated Developments with 2–5 members (stability controls) | see `dataset/FREEZE.json` |
| `FREEZE.json` | seed, input and output hashes | |

**Revision note.** The first freeze run included giant D182 among the large-occurrence candidates, because it lacks
the relay signature. Giants were then excluded from that list and the selection was re-frozen, before any labelling
or measurement. The hashes in `FREEZE.json` are the final ones.

## Owner labels still to be collected (frozen with their hash before step 3)

| Label set | Items | Labels |
|---|---|---|
| L1 founder occurrence | 38 founder items of the 8 giants | which founders form the founding occurrence |
| L2 giant members | 128 | SAME_AS_FOUNDER_OCCURRENCE / DIFFERENT / AMBIGUOUS |
| L3 large candidates | 48 + 6 Development-level answers | same labels; "one occurrence?" per Development |

That is about 214 judgments.

## SAME controls in the dataset

- **Late corroboration and ID stability:** the 19 cross-tick SAME pairs of Phase 2 development (16 retained today) and
  the multi-day SAME pairs of identity gold rev 4.
- **Owner-verified same-occurrence pairs left unattached today:** R012 (one matter, BBC / France 24), T034, T041.
  These are recall cases: a variant must not make them worse.
- **Owner-approved SAME across artifacts:**
  - the Commission proposal and its Q&A (C034, C103);
  - a Security Council record and its briefing (C064);
  - the drone crash during the overnight attack (C076);
  - the appointment and the audience with the King (C018, C082).
- **Large legitimate occurrences:** the L3 candidates the owner labels as one occurrence. If none qualifies, this
  control class is empty and the gate relies on the gold SAME pairs; the gate says so explicitly.
- **Multilingual SAME:** only pairs currently kept together (cross-language identity stays disabled). They must not
  be broken.

## Small controls

60 Developments with 2–5 members (`small-controls.json`) measure churn: membership identical to DA0 under H2.
