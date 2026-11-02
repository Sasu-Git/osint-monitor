# Corroboration stage forensics (2026-11-02): no fix implemented

**Question.** Why does the corroboration stage take about 1,000 s per run, and why does that grow with the database?

**Method.** Read-only work only:
- the run ledger of the live DB snapshot taken 2026-11-02 12:55Z (sha `b5bb5728…`), 296 runs since run-timing went
  live on 10-27;
- a per-Development replay of exactly what the stage does (`compute_corroboration_score` for every Development, as
  `processors/pipeline.py: _corroboration` calls it) on that snapshot, opened `mode=ro`, at below-normal CPU priority
  (`measure.py`). Raw outputs (`corr_per_event.csv`, `corr_ledger.txt`, `corr_model.txt`) stay with the snapshot.

Code on `main` `44e0357`.

## What the stage does

```python
events = session.query(Event).all()                 # every Development in the database
for ev in events:
    sc = compute_corroboration_score(session, ev.id)   # items, sources, provenance.assess_event, claims
    ev.source_count = ...; ev.confidence_class = ...   # cached on the Event
```

`compute_corroboration_score` loads the Development's items and sources and its claims, and calls
`provenance.assess_event`. That call resolves every item's origin, then runs `_mark_syndicated_copies`: each item's
first 400 normalised characters are compared with those of every earlier item from another origin, using
`difflib.SequenceMatcher(autojunk=False).ratio()`, stopping at the first match >= 0.95.

## Findings

| Question | Answer | Evidence |
|---|---|---|
| How many Developments per run? | **All of them**: 1,198 today, up from 1,003 on 10-27 | `session.query(Event).all()`; no filter on change, age or status |
| Historical rescan? | **Yes, every run** | as above |
| Proportional to new items or to DB size? | **To DB size, not to new items** | correlation(new items, stage seconds) = **0.00** over 165 runs. A hot run with 2 new items pays the same as a warm run with 37 (medians: hot 925 s, warm 937 s, cold 923 s) |
| No-op runs | Skipped: post-processing runs only when a tier brings >= 1 new item (131 of 296 runs had none) | `pipeline.py`: `if proc_stats["new_items"] > 0: run_post_processing(...)` |
| Recomputed despite unchanged inputs? | **Yes.** Nothing records which item set a cached result belongs to. The summaries stage, by contrast, skips unchanged Developments (`summary_generated_at >= last_updated_at`) | code |
| Duplicate work across tiers | Every hot, warm or cold run with a new item repeats the whole scan. Runs write to SQLite one at a time, so one run's 15–20 min stage becomes the other tiers' `lock_wait` (medians 1,100–1,600 s since 10-30) | ledger; run-timing |
| Duplicate work within a run | `assess_event` runs again in the summaries stage for each changed Development, and in every web Situation and Development page view | `summaries.py: occurrence_evidence`; `api/situation_views.py` |
| SQL and indexes | **Not the bottleneck.** 8.2 statements per Development, 9,777 per pass; everything except provenance is 27 s of 573 s | `measure.py` |
| Embeddings / similarity models | Not used by this stage. The similarity is `difflib` on text prefixes | code |
| Entity and source calculations | Per-Development `session.get(Source)` plus the provenance config load; small. Each Development reloads its sources | profile |

**Where the time goes** (one pass over 1,198 Developments, idle core): **573 s**.

| Part | Seconds | Share |
|---|---|---|
| `assess_event` (provenance) | 545.9 | 95% |
| of which `_mark_syndicated_copies` | 462.6 | **81%** |
| everything else (queries, grading, claims) | 27.4 | 5% |

**Concentration.** The cost sits in a handful of very large Developments:

| Development | Items | Seconds |
|---|---|---|
| D449 | 520 | 195.1 |
| D399 | 276 | 69.4 |
| D639 | 267 | 55.6 |
| D514 | 274 | 38.7 |
| D398 | 682 | 37.8 |

Those five are 69% of the pass, and the top 10 are 75%. The 874 Developments with <= 5 items take 73 s together
(median 75 ms each). Cost per Development depends on how many items have a long body and how many pairs fail to
match early, not only on the item count. D398 has the most items (682) but costs less than D449, because many of its
bodies are short or match early.

**Live vs replay.** The daemon's stage median of 925–1,116 s is about 1.6–1.9× the 573 s replay. That is consistent
with CPU contention from the other stages and the host, and with Developments that were still growing during the
window.

## Cost model

```
corroboration seconds per run ≈ F + Σ over ALL Developments d of  c · P(d)
                                + ~0 · (new items in the run)

  F    ≈ 25–30 s   per pass: 8 SQL statements and grading per Development (≈ 23 ms × Developments)
  P(d) = pairs SequenceMatcher actually compares in d: up to L(d)²/2 for L(d) items with a body >= 200 characters,
         fewer when copies match early
  c    ≈ 8–10 ms per compared pair of 400-character prefixes (difflib, autojunk off)
```

**Fit.** Across Developments, `seconds ≈ a + b·items + c·items²` gives R² 0.50. Item count alone is a weak proxy for
P(d), because body length and early matches vary.

**Growth.** The cost grows with the database because:
- every new Development adds a small fixed term, about 25 ms;
- large Developments keep gaining items, and their quadratic term grows faster than linearly. This is the 713 s
  (10-27) -> 1,116 s (11-02) trend in the ledger, while the number of Developments grew only 19%.

New items cost almost nothing directly. Their real effect is to trigger a full pass.

## Top three scaling causes

1. **A full rescan on every run.** Corroboration is recomputed for every Development in the database whenever a
   tier brings one new item. The work is proportional to the archive, not to the change.
2. **Quadratic near-duplicate matching inside provenance.** `_mark_syndicated_copies` does an all-pairs
   `SequenceMatcher` with no cheap upper-bound pre-check (`real_quick_ratio` / `quick_ratio`). It is 81% of the
   stage, concentrated in the five largest Developments.
3. **No memoisation of an unchanged result.** Provenance and corroboration depend only on a Development's item set
   and the config, yet they are recomputed each run, again in summaries, and again per web page view. Each tier
   run's long stage also holds the single SQLite writer slot, so the cost multiplies as `lock_wait` in the other
   tiers.

**Nature of the problem.** Algorithmic (cause 2) and architectural (causes 1 and 3), **not database or query
bound**. Indexes are not the lever: SQL is 5% of the stage.

## Intervention points (not implemented; each needs its own approval and gate)

| # | Intervention | Effect | Risk |
|---|---|---|---|
| 1 | Pre-check `real_quick_ratio()` and `quick_ratio()` before `ratio()` in `_mark_syndicated_copies` | Most compared pairs rejected cheaply; identical result | **Low**: exact; gate by replaying every Development on the snapshot and requiring identical provenance output |
| 2 | Corroborate only Developments whose membership changed since their last corroboration (like the summaries stage), plus a periodic or forced full pass | Stage cost follows the change, not the archive | Low to medium: needs a "last corroborated" marker. A column is a migration; the existing `Event` fields could serve, with care. Config changes need a full pass |
| 3 | Cache provenance per Development keyed by its item-id set and config hash; reuse it in corroboration, summaries and the web views | Removes the repeats within a run and across page views | Medium: stored state and invalidation; same design question as the membership/provenance record |
| 4 | Linear near-duplicate detection (hashed prefix or shingles) | Removes the quadratic term | Medium to high: changes which items count as copies, hence confidence classes; needs an evaluation like the identity gates |

Expected order: 1 (exact, smallest) then 2 (largest steady-state effect), with 3 designed alongside the provenance
logging work. Each one is a runtime change, so it goes through the deploy runbook, not this task.
