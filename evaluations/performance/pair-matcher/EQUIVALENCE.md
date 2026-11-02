# Pair-matcher pre-check: equivalence (2026-11-02)

**Result: 0 differences.** The `quick_ratio()` bound pre-check (variant P2, implemented on `perf/pair-matcher-prefilter`
`bc0d5c0`) gives byte-identical provenance and corroboration output to the current code (`main` `44e0357`) on the
frozen benchmark and on every Development of the snapshot. No semantic change.

## The shared matcher

| | |
|---|---|
| Function | `ProvenanceResolver._mark_syndicated_copies` (`osint_monitor/processors/provenance/resolve.py`), called at the end of `ProvenanceResolver.resolve()` |
| Inputs | a Development's `EvidenceItem`s (body text, publication time) and their provisional `ItemProvenance` (evidence type, origin) |
| Rule | in publication order, each item's normalised body prefix (first 400 characters; items under 200 skipped) is compared with every earlier item of **another origin**. The test is `SequenceMatcher(None, prefix, other_prefix, autojunk=False).ratio() >= syndication_similarity` (0.95). The first match makes the item `DERIVATIVE` of that origin. Primary and commentary items are never marked, but serve as originals |
| Output | the item's `ItemProvenance` (evidence type, origin, derived_from, note), so it sets independent-origin counts and confidence class |
| Complexity | up to n(n−1)/2 pairs per Development (early stop at the first match). Each `ratio()` is O(L²) in the 400-character prefix (autojunk off), plus building a fresh `SequenceMatcher` per pair |

**Callers** (all through `resolve()`):

| Caller | Path |
|---|---|
| Corroboration stage (daemon) | `pipeline._corroboration` -> `corroboration.compute_corroboration_score` -> `provenance.assess_event` -> `assess_confidence` -> `resolve` |
| Summaries stage (daemon) | `summaries.occurrence_evidence` -> `assess_event` |
| Development page and Situation page (web) | `api/situation_views.development_view` -> `assess_event` (once per Development on the page) |
| Development identity / segmentation (clustering) | `development_identity.py`, `development_segmentation.py` -> `ProvenanceResolver().resolve()` |

It is the same matcher behind the giant-page latency and behind about 82% of corroboration time. Measured on the
snapshot with the current code: matcher 451.8 s of corroboration's 524.9 s. On the giant Developments it is
97–99% of provenance time.

## Why the pre-check cannot change a decision

- **The bound.** `quick_ratio()` returns `2·m / (len(a)+len(b))`, where `m` is the size of the two strings' character
  multiset intersection. `ratio()` returns `2·M / (len(a)+len(b))`, where `M` is the total length of the matching
  blocks.
- **`M <= m`.** Every character in a matching block is paired with a distinct equal character of the other string.
- **Float safety.** With the same denominator, IEEE division is monotone, so `ratio() <= quick_ratio()` exactly, in
  floating point too.
- **Skipped means rejected.** A pair with `quick_ratio() < 0.95` would have been rejected by `ratio()`.
- **What P2 computes.** `quick_ratio_bound` uses `m = sum((Counter(a) & Counter(b)).values())`. That is exactly the
  `matches` count difflib's `quick_ratio()` builds, and P2 computes the result with the same expression
  (`2.0 * matches / length`, and `1.0` for empty strings).
- **No order dependence.** Pairs are visited in the same order, and only pairs that cannot match are skipped. So the
  first match, and hence the origin, `derived_from` and note, is the same item.

## Frozen dataset

See `FREEZE.md`, committed (`1def601`) before any variant ran.
- **Snapshot:** sha `b5bb5728…`.
- **Benchmark:** 32 Developments:
  - largest five: D398 (682 items), D449 (520), D397, D399, D514;
  - named D398, D449, D514;
  - 2 at 151–300, 6 at 51–150, 8 at 11–50, 12 at 2–10 (seed 20261102).
- **P0 log:** every pair P0 decided (113,109 unique pairs, 4 accepted).
- **P0 outputs:** every Development's serialised provenance assessment and corroboration score.

**Near-boundary pairs** (`boundary.py`, the whole snapshot, all 148,920 candidate pairs with no early stop). On the
77,826 pairs with a bound >= 0.80 it computed both `quick_ratio()` and `ratio()`:
- the bound differed from `quick_ratio()` **0** times;
- `ratio()` exceeded the bound **0** times;
- 22 pairs are recorded in `boundary_pairs.csv`:
  - 4 with a ratio of 0.90–0.95;
  - 11 at or above 0.95;
  - 6 whose bound reaches 0.95 while the ratio stays below. Two of these have a bound of **exactly 0.95**, which the
    `<` test correctly sends on to `ratio()`: D528 gives 0.905 and D564 gives 0.6925.

## Gate results (required: 0)

| Check | P1 | P2 | branch `bc0d5c0` |
|---|---|---|---|
| Provenance output differences, benchmark (32) | 0 | 0 | 0 |
| Corroboration output differences, benchmark (32) | 0 | 0 | 0 |
| Provenance output differences, full snapshot (1,198), vs `main` | — | 0 | 0 |
| Corroboration output differences, full snapshot (1,198), vs `main` | — | 0 | 0 |
| Accepted pair set identical to P0 (4 pairs) | yes | yes | (no pair log; outputs identical) |
| Skipped pairs that P0 accepted | 0 | 0 | — |
| Pairs decided identical to P0's set | yes | yes | — |
| Full-ratio decisions or values differing from P0 | 0 / 0 | 0 / 0 | — |
| Highest bound among skipped pairs | 0.945 | 0.945 | — |

- **P1 vs P2:** identical skip sets, and identical bound values on every skipped pair.
- **Output files byte-identical:**
  - benchmark: frozen P0, P1, P2 and the branch all have sha `d704dba1…`;
  - full snapshot: `main`, P2 and the branch all have sha `9424ffce…`.
- **The harness copy of the matcher is faithful:** `impl` (the unmodified `main` code) reproduces the frozen P0
  outputs exactly.

**Tests on the branch.**
- `tests/test_provenance_prefilter.py` (new, 11 tests):
  - the bound equals `quick_ratio()` and is >= `ratio()` on 1,500 random pairs, >50 of them within 0.90–0.99;
  - empty strings;
  - `resolve()` and `assess_confidence()` are identical to the verbatim old matcher on random corpora of 8, 60 and
    120 items with near-copies that straddle the threshold;
  - first-match order.
- Provenance and corroboration tests: 43 passed.
- Full suite: 738 passed, 3 xfailed.
- Smoke test: passed.

## Scope of the change

`osint_monitor/processors/provenance/resolve.py`: +22 / −5 lines.
- **Added:** `quick_ratio_bound`; a per-prefix `Counter` kept beside each earlier prefix; one `continue` before
  `ratio()`.
- **Unchanged:** thresholds, config, schema, API and dependencies.
- **Also covered:** identity and segmentation call `resolve()` too, so the identical-output proof covers them.

## Risks

- **Memory:** one `Counter` per item prefix (at most 400 characters, about 40 distinct keys) per Development
  resolved. Negligible.
- **Future edits:**
  - if the matcher's comparison ever changed, for example to a different similarity, `autojunk` on, or a
    different prefix length, the bound would have to be re-proved. `quick_ratio()` is an upper bound for
    `SequenceMatcher.ratio()` only;
  - the code comment and the equivalence test pin this.
- **Reference test cost:** about 40 s, mostly the verbatim old matcher used as reference. It is a deliberate cost.
