# Coverage-recoverability review: final score (2026-10-27)

Review complete: **120 of 120** frozen cases labelled, one verdict each, all by reviewer `owner` (44 on 2026-10-13/14,
76 on 2026-10-27). `python labels_tool.py validate`: 0 problems. The 44 earlier labels are byte-for-byte unchanged
(compared with the copy taken before the review resumed). Frozen files re-hashed over LF bytes and identical to
`FREEZE.md` (`build_sample.py`, `sample-manifest.json`, `review-cases.json`, `key.json`). Nothing was relabelled,
imported or overwritten.

Scored with `python score.py` (canonical scorer, unchanged since `d27f1bc`).

## Per stratum

| stratum | pool | labelled | SHOULD_JOIN | SHOULD_NOT_JOIN | AMBIGUOUS | recoverable rate (Wilson 95%) | upper bound (ambiguous recoverable) | pool estimate (range) |
|---|---|---|---|---|---|---|---|---|
| below_threshold | 1028 | 30/30 | 12 (40%) | 18 (60%) | 0 (0%) | 40% (25%-58%) | 40% | ~411 (253-593) |
| segmentation_es | 69 | 30/30 | 8 (27%) | 21 (70%) | 1 (3%) | 27% (14%-44%) | 30% | ~18 (10-31) |
| segmentation_it | 92 | 30/30 | 9 (30%) | 21 (70%) | 0 (0%) | 30% (17%-48%) | 30% | ~28 (15-44) |
| cross_language | 190 | 30/30 | 21 (70%) | 8 (27%) | 1 (3%) | 70% (52%-83%) | 73% | ~133 (99-158) |

Segmentation cases by the guard that cut the link (an item can involve more than one guard):

| guard | SHOULD_JOIN | SHOULD_NOT_JOIN | AMBIGUOUS |
|---|---|---|---|
| headline_similarity | 16 | 31 | 0 |
| disjoint_locations | 11 | 22 | 1 |
| analysis_headline | 5 | 9 | 0 |

No guard is concentrated: each is right about two times in three.

## Combined estimates (the four sampled strata, pool 1,379 of 5,929 unsurfaced items)

| | items | share of the 5,929 unsurfaced |
|---|---|---|
| Intentional / not recoverable: policy categories (counted, not sampled) | 4,240 | 72% |
| Intentional / not recoverable: sampled strata labelled SHOULD_NOT_JOIN (pool-scaled) | ~780 | 13% |
| **Empirically recoverable** (pool-scaled SHOULD_JOIN) | **~590** (stratified 95%: 410-771) | **~10%** (7-13%) |
| AMBIGUOUS (pool-scaled) | ~9 | 0.2% |
| Not sampled: segmentation_rejected in English (218) and other_ambiguous (92) | 310 | 5% |

- The stratified interval is a normal approximation with finite-population correction over the four strata; per
  stratum the Wilson intervals above apply.
- **AMBIGUOUS uncertainty is negligible**: 2 of 120 cases; counting both as recoverable moves the total by ~9 items.
- **Upper bound on recoverable loss** with every unsampled item counted recoverable: ~590 + 310 = ~900 (15%), down
  from the unlabelled upper bound of 1,689 (28%).
- In absolute terms the recoverable mass is below threshold (~411) and cross-language (~133). Segmentation (es + it)
  is ~46.

## Reading against the decision rules in `evaluations/phase2-followup/DECISION-MEMO.md` (section D)

- **Below threshold, 40%**: not high. Most near misses are correct separations; and the prior secondary-link rule
  (0.45-0.53) added 0 true and 13 false joins. Any recovery here is candidate generation, not a threshold change.
- **Segmentation, 27-30%**: low, and spread evenly over the three guards. Leave segmentation unchanged.
- **Cross-language, 70% (52-83%)**: now decision-grade (30 of 30). It measures whether a true counterpart exists among
  high-similarity candidates, not merge precision (0.375 when the stage was on). The KEEP DISABLED decision stands; a
  reopening would be candidate generation guarded by P7 anchors (owner scope 2026-10-07).
