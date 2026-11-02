# Pair-matcher pre-check: performance (2026-11-02)

**Measurement.** All runs are read-only on the 2026-11-02 snapshot (sha `b5bb5728…`), at below-normal CPU priority on
a 22-core host while the daemon and web server ran.
- **Full snapshot:** the full corroboration path for every Development, `main` (`44e0357`) vs
  `perf/pair-matcher-prefilter` (`bc0d5c0`): `harness.py run --variant impl --full` with each tree on `PYTHONPATH`.
- **Variants:** also measured on the frozen 32-Development benchmark.
- **Noise:** wall times include machine noise. The same Development measured 36.8 s here, 38.7 s in the corroboration
  forensics, and 111 s on a busy host earlier the same day. The ratios are the stable part.

Raw tables: `pm-perf-tables.txt`; gate data: `compare.json`.

## Totals

**Full snapshot, 1,198 Developments:**

| | `main` | branch | Saved | Reduction |
|---|---|---|---|---|
| Matcher (`_mark_syndicated_copies`) | 451.8 s | **1.5 s** | 450.2 s | 99.7% |
| Provenance (`assess_confidence`) | 467.7 s | 19.7 s | 448.0 s | 95.8% |
| Corroboration (`compute_corroboration_score`, the pipeline stage's work) | 524.9 s | **100.6 s** | 424.3 s | 80.8% |
| Matcher share of corroboration | 82% | 2% | | |

The remaining ~100 s of corroboration is the per-Development rest: queries, building evidence, grading, claims. The
corroboration forensics measured that part at 27 s on an idle core, so it is mostly contention here. It is now the
whole cost, and it still scales with the number of Developments (forensics cause 1, the full rescan, unchanged by
this work).

**Benchmark, 32 Developments:**

| | Matcher | Provenance | Corroboration |
|---|---|---|---|
| P0 / `impl` (main) | 320.6 s | 325.4 s | 316.4 s |
| P1 (`quick_ratio()` on a constructed `SequenceMatcher`) | 9.0 s | 12.9 s | 14.9 s |
| **P2** (bound from precomputed counts) | **0.7 s** | 4.6 s | 6.6 s |
| branch (`bc0d5c0`, = P2) | 0.7 s | 4.7 s | 6.4 s |

P2 beats P1 by about 13× on the matcher because it skips the per-pair `SequenceMatcher` set-up (`__chain_b`) as well
as `ratio()`.

## Giant Developments (provenance, s)

| Development | Items | `main` | branch | Speed-up |
|---|---|---|---|---|
| D449 | 520 | 190.53 | 2.00 | ×95 |
| D399 | 276 | 80.70 | 1.26 | ×64 |
| D639 | 267 | 52.41 | 0.81 | ×64 |
| D514 | 274 | 36.79 | 0.89 | ×42 |
| D398 | 682 | 24.37 | 1.13 | ×22 |
| D147 | 108 | 11.75 | 0.24 | ×49 |
| D162 | 76 | 10.43 | 0.19 | ×54 |

## Situation pages: the provenance part (sum over member Developments)

| Situation | Developments | `main` | branch |
|---|---|---|---|
| `russia-united-states` | 26 | 106.8 s | 2.9 s |
| `israel-palestine` | 18 | 37.3 s (57–125 s seen on the live web server) | 1.1 s |
| `gaza-ceasefire` | 9 | 2.9 s | 0.24 s |
| `russia-ukraine-war` | 26 | 1.0 s | 0.24 s |
| `china-united-states` | 20 | 0.42 s | 0.30 s |
| `sudan-civil-war` | 2 | 0.04 s | 0.02 s |

The rest of a Situation page costs at most about 1.5 s: queries, rebuilding the canonicaliser, templates
(`evaluations/web-performance/situation-page/PROFILE.md`). That part is unchanged.

## By size bucket (per-Development provenance, full snapshot)

| Items | Developments | `main` median / p90 | branch median / p90 | Median speed-up | Total `main` -> branch |
|---|---|---|---|---|---|
| 2–10 | 1,034 | 3.6 / 18.0 ms | 3.6 / 11.5 ms | ×1.0 | 8.2 -> 5.8 s |
| 11–50 | 139 | 55.7 / 342.8 ms | 26.0 / 70.1 ms | ×2.1 | 19.5 -> 4.6 s |
| 51–150 | 17 | 1.81 / 3.83 s | 0.12 / 0.24 s | ×8.2 | 44.3 -> 2.4 s |
| 151–300 | 5 | 36.8 / 52.4 s | 0.81 / 0.89 s | ×41.5 | 177.4 -> 3.5 s |
| 301+ | 3 | 24.4 s (median) | 1.13 s (median) | ×21.5 | 218.3 -> 3.5 s |

**Normal Developments are not slowed.**
- **Matcher cost:** the added work (building one `Counter` per prefix) costs +0.005 ms at the median and +1.07 ms at
  most per 2–10-item Development.
- **Individual provenance timings:** these vary by ±1–12 ms between runs whatever the code, so a third of small
  Developments look >20% slower and others faster. That is measurement noise at the millisecond scale.
- **Group total:** the 2–10-item group as a whole is faster, 8.2 s -> 5.8 s.

## Complexity

**Benchmark pair counts** (`compare.json`, P2 log vs P0 log):

| Items | Developments | Possible pairs n(n−1)/2 | Pairs P0 compared fully | P2 skipped by the bound | P2 full `ratio()` |
|---|---|---|---|---|---|
| 2–10 | 12 | 78 | 33 | 33 | 0 |
| 11–50 | 8 | 1,536 | 113 | 113 | 0 |
| 51–150 | 6 | 30,695 | 3,748 | 3,746 | 2 |
| 151–300 | 3 | 99,882 | 35,670 | 35,670 | 0 |
| 301+ | 3 | 421,446 | 73,545 | 73,543 | 2 |
| **all** | 32 | 553,637 | 113,109 | 113,105 | **4** |

- **Pairs that still reach `ratio()`:** 4 of 113,109 (a 99.996% reduction). Only near-copies get past the bound.
- **Fewer than n(n−1)/2 compared:** short bodies are skipped, same-origin pairs too, and the scan stops at the first
  match.
- **Scaling:** the loop over candidate pairs is still O(n²) per Development. What changes is the cost per pair.
  - Before: building a `SequenceMatcher` plus `ratio()`, about L² character steps on two 400-character prefixes;
    roughly 8–10 ms per pair.
  - After: a multiset intersection of two counters of about 40 distinct characters, a few microseconds.

  That is a constant about three orders of magnitude smaller. At current sizes the quadratic term no longer
  dominates: D449, the most expensive Development, drops from 190 s to 2 s. It would matter again only at tens of
  thousands of items in one Development.

## Expected production effect (not deployed)

**Daemon corroboration stage.**
- **Current:** median 925–1,116 s live, which includes contention.
- **Expected:** it falls by about 80%, to the per-Development rest. The full rescan remains and is the next lever
  (forensics intervention 2).
- **Knock-on:** each tier run holds the single SQLite write slot for a shorter time, so the other tiers' `lock_wait`
  (median 1,100–1,600 s) should fall with it. That is not measured here.

**Web (read-only server).** The provenance part of the worst Situation pages drops from a minute or more to about
1–3 s, and `/developments/514` from minutes to about 1 s. The server needs a redeploy for that, separate from the
daemon.

**Summaries stage and clustering identity/segmentation.** They use the same `resolve()` and get the same speed-up,
with identical output.
