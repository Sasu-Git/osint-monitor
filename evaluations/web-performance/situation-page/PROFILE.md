# Situation page profile (2026-11-02): no optimization implemented

**Method.** `GET /situations/<slug>` was run in-process (FastAPI TestClient, real app, `OSINT_DB_READONLY=1`)
against the 2026-11-02 12:55Z snapshot (sha `b5bb5728…`, see `evaluations/geolocation/2026-11-02/FREEZE.md`), with
the app code of `deploy-web-20261102` (`d06af11`).
- **Requests.** One warm-up, three timed requests and one instrumented request per Situation.
- **Instrumentation.** SQLAlchemy cursor events count and time every statement; wrappers time each stage. `cProfile`
  was run on `assess_event` for the heaviest Development.
- **Isolation.** Neither the live server nor the live DB was touched.

Script: `profile_situation_page.py`. Raw output stays with the snapshot (`situation-profile.txt`, `assess-profile.txt`).

## Timings

| Situation | Developments | Items | Request (s), 3 runs | `assess_event` | Rest of the view | Template | SQL statements |
|---|---|---|---|---|---|---|---|
| `sudan-civil-war` (small) | 2 | 35 | 0.30, 0.32, 0.30 | 0.22 s (69%) | 0.09 s | 0.007 s | 10 |
| `gaza-ceasefire` (medium) | 9 | 210 | 4.90, 4.84, 4.81 | 4.41 s (97%) | 0.13 s | 0.007 s | 38 |
| `russia-ukraine-war` (largest by count) | 26 | 217 | 6.29, 10.28, 8.39 | 6.61 s (93%) | 0.49 s | 0.014 s | 106 |
| `israel-palestine` (largest by items) | 18 | 527 | **56.8, 60.8, 114.2** | **124.1 s (99%)** | 1.3 s | 0.018 s | 74 |

- **SQLite time.** At most 1.2 s, even on the 125 s request. Statements are exactly 2 + 4 per Development:
  - the Situation and its Developments, once per page;
  - per Development: principal actors, items, provenance's item query and its claims query.

  That is N+1 by Development, but each query is cheap: the latency is not in SQL.
- **Template rendering:** 7–18 ms. The HTML is 4–23 KB, and there is no map payload on this page.
- **Actor canonicalizer:** 0.07–0.15 s per request. It is rebuilt every request (normaliser load); 0.76 s once under
  contention.
- **Excerpts:** at most 0.02 s.

Time per Development is set by its **item count**, not by the Situation:

| Development | Situation | Items | Body chars | `assess_event` |
|---|---|---|---|---|
| D514 | israel-palestine | 274 | 267,868 | **110.9 s** (187.6 s under cProfile) |
| D182 | gaza-ceasefire | 148 | 66,335 | 8.5 s |
| D124 | russia-ukraine-war | 105 | 16,303 | 1.65 s |
| D812 | israel-palestine | 87 | 15,415 | 1.07 s |
| typical | | 2–30 | | 0.2–0.3 s |

## Where the time goes

`assess_event` -> `assess_confidence` -> `resolve` -> **`_mark_syndicated_copies`** (`processors/provenance/resolve.py`)
accounts for 185.6 of 187.6 s on D514. For every item, in publication order, it compares the first 400 normalised
characters (2 × `syndication_min_chars` = 200) of its body with **every earlier item from another origin**, using
`difflib.SequenceMatcher(autojunk=False).ratio()`. It stops only at the first match >= 0.95.

- **The number of comparisons grows with the square of the item count.** 274 items gave 12,144 `ratio()` calls, 608k
  `find_longest_match` calls and 240M dict lookups. With `autojunk=False`, each comparison of two 400-character
  strings costs up to ~400² steps.
- **There is no cheap pre-check.** `real_quick_ratio()` and `quick_ratio()` are exact upper bounds on `ratio()`, but
  neither is used to reject pairs before the full comparison. Most pairs are clearly different, yet every one pays
  the full price.
- **The work is repeated on every request.** Nothing caches provenance:
  - each page view recomputes it for every Development on the page;
  - the Development detail page (`development_view`) recomputes it too;
  - the daemon recomputes it in corroboration (`processors/corroboration.py:193`) and in summaries
    (`processors/summaries.py:87`). See task 6.

Production consequence: opening `/situations/israel-palestine`, or `/developments/514`, on the live web server
(8790) takes about 1–2 minutes of one CPU core. The server is a single uvicorn process, so other requests slow down
meanwhile. The W-C1 baseline of 5.5–6 s for `russia-ukraine-war` was measured on the live server and matches the
6.3–10.3 s here.

## Top three bottlenecks

1. **All-pairs `SequenceMatcher` in `_mark_syndicated_copies`.** Quadratic in items per Development, with no
   upper-bound pre-check. 93–99% of request time on every non-trivial page.
2. **Provenance recomputed per request and per Development.** The same `assess_event` result is computed again by
   the Situation page, the Development page, and the daemon's corroboration and summary stages. Nothing is stored
   or reused, so a large Development pays bottleneck 1 again on every view.
3. **Per-request setup and N+1 queries.** The canonicalizer is rebuilt on each request (0.07–0.15 s), and there are
   4 queries per Development. Small today (under 1.5 s combined at the worst), but a fixed cost per Development
   that grows with Situation size.

## Likely intervention points (not implemented)

| # | Intervention | Effect | Risk |
|---|---|---|---|
| 1 | In `_mark_syndicated_copies`, skip a pair when `real_quick_ratio()` or `quick_ratio()` < `syndication_similarity`, before `ratio()` | Same result (both are exact upper bounds); removes most full comparisons | **Low**: no semantic change; testable by replaying `assess_event` on the snapshot and requiring identical output for every Development |
| 2 | Persist or cache the provenance assessment per Development, keyed by its item set (like corroboration is pre-cached on `Event`), and read it in the views | Page cost becomes a read; the daemon also stops recomputing | Medium: adds stored state; invalidation must follow membership changes; schema or cache design needed |
| 3 | Cheaper near-duplicate detection (hash of normalised prefix, shingles/MinHash) | Linear time | **Medium to high**: changes which items count as derivative copies, so confidence classes can change; needs its own evaluation |
| 4 | Load per-Development data in bulk (one query for principals, items and claims), and build the canonicalizer once per process | Removes the N+1 and per-request setup | Low: presentation only |
| 5 | Situation page: show recent Developments with summary counts, and load evidence on demand | Page cost bounded | Low to medium: UX change; owner decision |

Intervention 1 is the obvious first step: it is exact, local and testable against the frozen snapshot.
Interventions 1 and 2 also bear on task 6, because the same code runs in the daemon.
