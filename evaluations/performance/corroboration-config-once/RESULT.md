# Corroboration config-once + batched queries: equivalence and performance (2026-11-02)

**Result.** 0 output differences; the corroboration pass goes from **166.1 s to 23.8 s (−86%)** on the 2026-11-02
snapshot. Not deployed, not merged.

## Change (branch `perf/corroboration-config-once`, base `bc0d5c0`)

- **Shared scoring:** `compute_corroboration_score`'s scoring moves unchanged into `_score(...)`. The per-event entry
  point keeps its behaviour and default arguments, and gains optional `resolver` / `categories`.
- **New `score_events(session, ids)`:**
  - one `ProvenanceResolver` and one read of the `sources.yaml` feed categories per call;
  - members, items (with their sources) and claims loaded per chunk of 200 events;
  - the same `_score` on the same rows, in the same item order (ascending id, as the original `IN` query returned
    them, so float sums are identical);
  - a per-event exception is returned, not raised.
- **Evidence:** `build_evidence` gains an optional `categories`; its construction moves to `evidence_from_items`, now
  shared by both paths.
- **Provenance:** `assess_event` gains an optional `categories`.
- **Pipeline stage:** `_corroboration` calls `score_events`. The per-event failure handling is unchanged: a failed
  event becomes UNVERIFIED; the stage fails only if all events fail.
- **Callers:** every other caller (export, intelligence API, web views, summaries) is unchanged and uses default
  arguments.
- **Not changed:** no incremental or changed-only recomputation, cache, index, schema, config or threshold.

## Equivalence gate (required: 0)

**Reference:** frozen `bc0d5c0` per-Development provenance and corroboration outputs on the snapshot (sha `b5bb5728…`),
from the pair-matcher harness (`impl --full`, outputs sha `9424ffce…`).

| Path | Mismatches / 1,198 |
|---|---|
| `score_events` (the new stage path) vs frozen corroboration | **0** |
| `compute_corroboration_score(session, id)` (defaults) vs frozen corroboration | **0** |
| `assess_event(session, id)` (defaults) vs frozen provenance | **0** |
| `assess_event(session, id, shared resolver, categories once)` vs frozen provenance | **0** |
| Exceptions in the new path | 0 |

**Tests.**
- `tests/test_corroboration_batch.py` (new): `score_events` equals the per-event function over chunks, with
  contradictions on event and item claims, an empty event and a single source; configuration is read exactly once; a
  failing event doesn't stop the others.
- Provenance, prefilter and pipeline tests: 53 passed.
- Full suite: **740 passed, 3 xfailed**. Smoke test **passed**.

**Identity gates not re-run.** Development identity and segmentation call `ProvenanceResolver.resolve` directly,
which is unchanged here. Summaries and the web views use the unchanged default path (rows 2 and 3 above).

## Performance (same process, same snapshot, below-normal priority)

| | Old per-event loop (`bc0d5c0`) | New stage path | Change |
|---|---|---|---|
| Corroboration pass, 1,198 Developments | 166.1 s | **23.8 s** | −86% (−142 s) |
| Feed-category reads (`sources.yaml` parse) | 1,198 | 1 | |
| `ProvenanceResolver` constructions (config load + regex compile) | 1,198 | 1 | |
| SQL statements | 9,777 | **58** | −99.4% |

**Old-path breakdown** (`residual.json`, instrumented, 187.5 s):
- `sources.yaml` re-reads 44.3 s;
- resolver construction 26.0 s;
- SQL and ORM about 44 s;
- provenance resolve 29.1 s (matcher 2.1 s).

The new path removes the first two entirely and most of the third. What remains is mainly the per-item provenance
work (resolve) plus building the evidence objects.

**Production view.**
- **Now:** the first live candidate run (`bc0d5c0`, hot) spent 277.8 s in corroboration under daemon contention.
- **Expected:** this change would bring that to the order of 40–60 s. That's an estimate, not a measurement.
- **Still remaining:** the full rescan of all Developments (median 4 change per run). The changed-only design
  (`RESIDUAL.md`, approach C) stays paused, as instructed.

## Deployment

**Not deployed.** It would be its own performance candidate after the pair-matcher soak is accepted. It's stacked on
`bc0d5c0`, so it inherits that soak's acceptance first.
