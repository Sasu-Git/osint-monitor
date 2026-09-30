# Development identity benchmark

Measures whether a Development keeps one identity while it grows over ticks, and whether it splits or merges only
when the evidence says so. This is audit Phase 2's gate (`evaluations/system/full-basis-audit.md`, stop
condition S1).

## Hard gate

**No Phase 2 runtime change until the draft identity gold has been owner-reviewed and frozen.** The owner reviews
blind to the proposed Phase 2 algorithm, and the sheet says nothing about what any new matching logic would do.

## Protocol

| Step | What | Where | Status |
|---|---|---|---|
| 1 | Freeze replay windows and ticks before any labelling or identity code change | `manifest.yaml`, `windows/` | done (6af0ccf) |
| 2 | Replay the **current** pipeline tick by tick; generate candidate pairs from several rules | `scripts/replay_current.py` → `review/system-trace/` | done |
| 3 | Draft labels **blind**: the labeller sees only item text, outlet, publication time, language and the definition | `scripts/make_labeller_input.py` → `review/labeller-input.md`; labels → `review/draft-labels.json` | drafted |
| 4 | Reviewer sheet: current system columns, proposed label, rationale, confidence, blank owner verdict; structural flags listed separately | `scripts/build_review_sheet.py` → `review/identity-review-sheet.md`, `review/owner-verdicts.yaml` | awaiting owner |
| 5 | Apply owner verdicts, then freeze and hash the gold | `gold/` | after review |
| 6 | Only then implement stable identity against the frozen gold | – | blocked by 5 |

**Windows** (`manifest.yaml`): 4 ticks of 12 h each.

| Window | Split | Items | Notes |
|---|---|---:|---|
| 2026-08-21 | development | 162 | |
| 2026-09-25 | development | 90 | |
| 2026-09-30-multilingual | development | 392 | en/it/es, institutional sources, roundups, records |
| 2026-08-31 | holdout | 166 | no time overlap with development; not used while developing Phase 2 |

There is no multilingual holdout.

**Candidate rules** (`scripts/replay_current.py`):
- late attachment;
- same-tick members;
- least-similar members;
- near-duplicate Developments;
- unattached near misses;
- segmentation cuts;
- cross-tick similar pairs;
- cross-language entity/place overlap (the embedding model is English-only);
- below-threshold hard negatives.

Every rule is seeded and capped. The rules decide which pairs get labelled, never their labels.

## Gold format (after freezing)

One entry per case:

| Field | Values |
|---|---|
| items | a, b (window item ids) |
| label | `SAME_DEVELOPMENT` \| `DIFFERENT_DEVELOPMENT` \| `AMBIGUOUS` |
| note | optional relation |
| confidence | high \| medium \| low |
| verdict source | draft accepted \| owner corrected |

Scoring skips AMBIGUOUS cases and reports them separately.

## Metrics

A pair is **kept together** when, after the tick at which the later item arrives, both items belong to the same
Development ID. It is **continued** when they are kept together and the earlier item's Development ID did not
change.

- **Continuity precision:** of the pairs the system keeps under one ID, the share that are gold
  `SAME_DEVELOPMENT`.
- **Continuity recall:** of the gold `SAME_DEVELOPMENT` pairs, the share the system keeps under one ID (an earlier
  Development continued, not a new one created).
- **Split/merge correctness:** when the system records a split or a merge (explicit lineage), whether the gold
  supports it:
  - a split is correct if it separates gold `DIFFERENT_DEVELOPMENT` pairs and no gold `SAME_DEVELOPMENT` pair;
  - a merge is correct if every cross pair it joins is gold `SAME_DEVELOPMENT`.
  - Reported as correct / total for each.
- **ID stability:** the share of Developments whose ID survives every later tick while their gold-same members
  keep arriving.
- **Mixed-Development rate:** the share of multi-item Developments containing at least one gold
  `DIFFERENT_DEVELOPMENT` pair.

Each metric is reported per window and split, with raw numerator/denominator and no composite score. The holdout
is run once, after development is done.
