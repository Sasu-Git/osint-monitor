# Residual corroboration cost after the pair-matcher pre-check (2026-11-02): analysis only

**Status.** Read-only analysis; no optimisation.
- **Code:** `bc0d5c0` (= deployed `deploy-perf-pairmatcher-20261102`).
- **Snapshot:** the 2026-11-02 12:55Z copy of the live DB (sha `b5bb5728…`), opened `mode=ro`, at below-normal priority.
- **Method:** `measure_residual.py` replays the corroboration stage exactly (`compute_corroboration_score` for every
  Development) and times each part by wrapping the functions it calls; every SQL statement is counted.
- **Run ledger:** gives how many Developments each past run actually changed (new memberships stamped with the run).
- **Raw output:** `residual.json`.
- **Instrumentation overhead:** included in the totals. The shares are the stable part.

## Measured breakdown (one pass, 1,198 Developments: 187.5 s, median 131 ms per Development)

| Part | Seconds | Share | What it is |
|---|---|---|---|
| **Re-reading `sources.yaml`** (`provenance/context._feed_categories`, per Development) | **44.3** | 24% | YAML parse of the whole source config, 1,198 times per pass, to map feed names to categories |
| **Building a new `ProvenanceResolver`** (per Development) | **26.0** | 14% | `load_provenance_config()` and compiling every attribution, retraction and first-hand regex, 1,198 times. `compute_corroboration_score` calls `assess_event` without a resolver |
| Provenance resolve (roles, attribution regexes; matcher 2.1 s) | 29.1 | 16% | per-item work; the matcher is now 1% |
| `build_evidence` rest (items and claims queries, ORM objects) | 35.8 | 19% | of which SQL 17.5 s (2,396 statements) |
| Corroboration's own queries and grading | 52.1 | 28% | SQL 26.3 s over 7,381 statements: 6.2 per Development (event_items, raw_items, `session.get(Source)` per source, claims by event, then claims by item) |

**Run ledger** (165 post-processing runs since 10-27):
- a run changes the membership of a **median of 4 Developments: 0.38% of all, p90 1.1%**;
- every run recomputes all of them.

## Cost model

```
corroboration per run ≈  D · (c_config + c_query + c_resolve)       historical rescan, every Development
                       + Δ · (same per-Development cost)                the Developments that actually changed
  D = all Developments (1,198 and growing); Δ = changed Developments (median 4)
  c_config  ≈ 59 ms   (sources.yaml + resolver construction; identical every time)
  c_query   ≈ 52 ms   (≈ 7.2 SQL statements, ORM)
  c_resolve ≈ 24 ms median (grows with a Development's item count; the matcher term is now negligible)
```

**Avoidable share:**
- **Repeated configuration work** (c_config × D, about 70 s, 37%) is avoidable with **no change in output**: the
  config is identical within a run.
- **Historical rescan of unchanged Developments:** (D − Δ)/D ≈ **99.6%** of the remaining per-Development work, and
  avoidable **only with a correct invalidation key** (below).
- **Changed-data cost:** about Δ × 135 ms ≈ 1 s per run at the median.

## Top three remaining bottlenecks

1. **The full historical rescan.** Every Development is recomputed whenever a tier brings one new item, although a
   median of 4 changed. This is the dominant term, and it grows with the archive.
2. **Configuration re-parsed per Development** (`sources.yaml`, provenance config and regexes): 37% of a pass, pure
   repetition.
3. **N+1 queries and duplicated loading.**
   - `compute_corroboration_score` loads the items, then `build_evidence` loads them again with claims.
   - Sources are fetched one by one (`session.get`).
   - Claims are queried twice.

   Together about 44 s of SQL plus ORM overhead per pass.

## What is needed to skip unchanged Developments safely (invalidation)

A Development's corroboration output is a pure function of:
- its **member item ids**;
- each member's **text as used** (`content`, which the **fulltext stage can lengthen later** for items under 200
  characters: `processors/fulltext.py: enrich_item_content`), title, publication time and URL;
- each member's **source row** (name, type, category, credibility);
- **claims** on its items, and on the event;
- the **configuration** (`provenance.yaml`, the `sources.yaml` categories, the code version).

So "membership changed" alone is **not** a sufficient key; fulltext enrichment and source or config edits also change
the output.

**A safe key:** a hash over (sorted member ids; per-item hash of the used text and title; source ids and attributes;
claim ids and types; config hash; code SHA), stored with the cached result and compared before recomputing.

**Determinism risk if done wrong:** stale confidence classes after fulltext enrichment or config edits, silently.
Hence the key must include all inputs, plus a periodic or forced full pass, and a config or code change forces one.

## Candidate approaches (not implemented)

| # | Approach | Output | Expected effect | Risk |
|---|---|---|---|---|
| A | **Hoist configuration out of the loop**: load the `sources.yaml` categories and one `ProvenanceResolver` once per stage run and pass them in (`assess_event` already accepts a `resolver`) | identical | removes about 37% of the pass (≈ 70 s on this snapshot) | **low**: exact; same equivalence harness as the pair-matcher work |
| B | **Batch the per-Development queries**: one query each for the members, items, sources and claims of all Developments in a run, then dispatch in memory | identical | removes most of the 44 s of SQL and ORM overhead | low to medium: memory for one pass; same harness |
| C | **Changed-only corroboration with a complete input key** (above), stored per Development, plus a full pass on config or code change and once a day | identical by construction if the key is complete | the stage drops to Δ-proportional work (seconds) | **medium**: needs stored state (a column or table: a migration) and proof that the key is complete; same class of design as the provenance cache in `PROFILE.md` |

## Recommended next experiment (`PROPOSED`)

**A first, then B.** Both are exact, local, and testable with the existing pair-matcher harness: byte-identical
provenance and corroboration on the frozen benchmark and the full snapshot, plus the semantic gates. Run them as one
"configuration and query hoisting" performance candidate, separate from C.

- **`PROPOSED` target:** the corroboration pass at ≤ 50% of the post-pair-matcher pass on the same snapshot, with 0
  output differences.
- **C** gets its own design note first: the input key, the invalidation triggers, the full-pass schedule, and a
  ledger replay showing that a keyed pass would have recomputed every Development whose output actually changed.
  Owner approval comes before any stored state.

**Not done:** no index, no cache, no incremental state, no materialised result, no change to the deployed candidate.
