# Coverage diagnosis: why items are not surfaced (2026-10-13)

Observational only. No thresholds, guards or code changed.

- **DB:** deploy final backup `data/deploy/20261013-1246/backup-final-20261013-105028.db` (read-only), taken 2026-10-13 10:50Z.
- **Code:** `deploy-candidate-20261013` (3eda6d0).
- **Question:** of the items that reach no Development, what fraction is intentional policy and what fraction is recoverable recall loss?

## Answer

9,002 items in total:

- 3,073 (34%) are in a Development.
- 5,929 (66%) are not. This is the live counterpart of the 79% unsurfaced measured on the eval windows.

Of the unsurfaced items:

- **72% (4,240) are excluded by policy.** The current contract leaves them out on purpose.
- **28% (1,689) are an upper bound on recoverable recall loss.** These are the review categories. They also contain true negatives, so the true loss is lower. Estimating it needs a labelled sample (see below).

| Category | Items | Share | Kind | Rule |
|---|---|---|---|---|
| never_viable_cluster | 2,760 | 47% | policy | Best cross-source cosine within 48 h is below 0.45. No second report observed. |
| structured_record | 831 | 14% | policy | Not a narrative source. Grouped by record identity instead. |
| commentary_analysis | 572 | 10% | policy | Analysis, explainer or live-blog headline. |
| single_source_holdback | 77 | 1% | policy | Links compatibly, but every partner shares one origin. |
| below_link_threshold | 1,028 | 17% | review | Best cross-source cosine in [0.45, 0.53): a near miss. |
| segmentation_rejected | 379 | 6% | review | Links exist, but a segmentation guard cuts every one of them. |
| cross_language_candidate | 190 | 3% | review | No same-language link. A report in another language within 24 h scores ≥ 0.60 on multilingual MiniLM. |
| other_ambiguous | 92 | 2% | review | Compatible link to a second origin, yet no Development. |

## Where the review share concentrates

- **Language:**
  - English: 25% review.
  - Spanish: **69%** review.
  - Italian: **96%** review. 92 of the 166 Italian items are segmentation_rejected.
- **Sources:**
  - ANSA Mondo: 96% review (65 segmentation_rejected).
  - Europa Press Internacional: 100% review.
  - Kyiv Independent: 62%. European Commission Press: 60%.
  - GDELT: 29% review, but large in volume (438 below threshold).
- **Item type:**
  - Reports: 42% review.
  - GDELT headline-only items: 29% review.
  - Analysis, rolling and structured items are policy by definition.
- **Time window:**
  - Before 10-05 (22 sources): 84% policy.
  - From 10-05 (52 sources): 66% policy.
  - So most of the possible loss comes from the sources added at expansion, mainly the Spanish and Italian ones.
- **Segmentation guards involved** (counted per item, so a single item can involve more than one guard):
  - headline_similarity: 239.
  - disjoint_locations: 169.
  - analysis_headline: 90.

The full tables are in `coverage_slices.md`. The per-item rows are in `coverage.json`.

## Caveats

- **Below-threshold items:** calibration placed distinct occurrences at cosine ≤ 0.51, so many near misses are correct separations.
- **Cross-language candidates:** earlier multilingual precision was 0.36, so most of these are likely false.
- **Never-viable-cluster items** are counted as policy, because no second report was observed. Some of them may be a source-coverage gap rather than a deliberate exclusion.
- **headline_only** is a local slice label (GDELT metadata content). The deployed code has no such rule.

## Proposed next step (not run)

Label about 30 items from each of below_link_threshold, segmentation_rejected (stratified across es/it) and cross_language_candidate. The labelling estimates the recoverable fraction for each category before any threshold or guard work starts.

## Reproduce

```
PYTHONPATH=<worktree at 3eda6d0> python coverage_diag.py <db> coverage.json
python coverage_slices.py coverage.json > coverage_slices.md
```
