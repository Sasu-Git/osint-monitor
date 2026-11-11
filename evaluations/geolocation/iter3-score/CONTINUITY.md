# Continuity: iterations 1 and 2 re-scored under the frozen iteration-3 lookup (2026-11-11)

FREEZE.md step 5, second sentence. Each iteration was re-run on its own frozen inputs (2026-11-02 snapshot
`b5bb5728…`, `audit-cases.json` `c11e52a5…`, `acceptance-cases.yaml` `92a30dd2…`) with the frozen `evaluate.py`
(`a9225547…`), changed in exactly one line, the ISO lookup, which now consults `lookup-overrides.json` first
(`rescore_iter12.py`). The historical `results.json` files are untouched. New files:
`../contract-eval/results-lookup-20261111.json`, `../contract-eval-iter2/results-lookup-20261111.json`.

| Measure | Iteration 1: historical → new lookup | Iteration 2: historical → new lookup |
|---|---|---|
| Audit W removed | 91/94 → 91/94 | 88/94 → 88/94 |
| Audit C preserved | 24/81 (29.6%) → 24/81 | **36/81 (44.4%) → 37/81 (45.7%)** |
| C moved to another country | 21 → 21 | 22 → 21 |
| Acceptance cases passed | 4/16 → 4/16 | 4/16 → 4/16 |

The only case that changed: **D286** (iteration 2), the L1 revision's "south sudan", now maps to `SSD` and scores
`PRESERVED` instead of `CHANGED`, the harness limitation iteration 2's RESULTS.md recorded. No other case or
acceptance check changed. Iteration 1 never emits "south sudan", "hong kong" or "macau", so it is identical.

**Byte note.** `audit-aliases-346456f.json` (the `B1` input) was written with CRLF; `outputs/B1.json` records the hash
of those bytes (`b5327a9d…`). The repository stores it with LF (`364c0e17…`, `.gitattributes`); the content is the same.
