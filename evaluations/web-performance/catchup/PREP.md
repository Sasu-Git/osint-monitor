# Web catch-up: preparation (2026-11-02)

The production web server (`deploy-web-20261102`, `d06af11`, 127.0.0.1:8790) still runs the pre-optimisation
provenance code. This branch prepares its catch-up to the daemon candidate `bc0d5c0` (pair-matcher pre-check). Nothing
here was deployed; port 8790 was not touched.

## Branch

`web/catchup-prep` = `feat/sa-workspace` (`ab45312`) + `--no-ff` merge of `bc0d5c0`. Clean merge; the only runtime file
the merge brings in is `osint_monitor/provenance/resolve.py`. No schema change, no migration, no template change.

## Benchmark (`bench_pages.py`)

In-process (FastAPI TestClient, real app, `OSINT_DB_READONLY=1`) against a read-only backup snapshot of the live DB.
One warm-up request, then 3 timed requests per page; every response asserted 200. Before = the deployed web code
(`d06af11` app tree); after = this branch. Raw results: `before.json`, `after.json`.

| Page | Before (median s) | After (median s) | Change |
|---|---|---|---|
| Situation israel-palestine | 70.59 | 3.65 | −95% |
| Situation russia-united-states | 219.58 | 6.37 | −97% |
| Situation gaza-ceasefire | 6.68 | 1.43 | −79% |
| Situation russia-ukraine-war | 5.07 | 3.00 | −41% |
| Development 449 (520 items) | 353.60 | 3.17 | −99% |
| Development 514 (274 items) | 76.18 | 1.52 | −98% |
| Development 399 (276 items) | 146.34 | 1.94 | −99% |
| Situation sudan-civil-war (control) | 0.38 | 0.37 | = |
| Development 11 (control) | 0.31 | 0.33 | = |
| Today `/` (control) | 0.40 | 0.43 | = |
| Map `/map` (control) | 0.39 | 0.41 | = |

**Output parity.** Response sizes are identical before and after on all 11 pages (e.g. Development 449: 559,611 bytes
both). Together with the frozen 0-difference provenance check on `bc0d5c0`, the change is speed-only.

**Remaining slowest page:** russia-united-states at 6.4 s. The standalone candidate `perf/corroboration-config-once`
(`6d6e7c8`) is daemon-side and does not change these pages.

## Live latency after a web redeploy (method, not run)

After the web redeploy, time the same URLs against 127.0.0.1:8790 with plain GETs (one warm-up, 3 timed,
`curl -w %{time_total}`), and compare with this table's "after" column. Read-only, no server change. Live numbers are
expected to be higher than in-process (concurrent daemon writes, uvicorn overhead); the gate is the before/after ratio,
not absolute seconds. PROPOSED gate: every pathological page ≤ 10 s median, controls not slower by > 20%.

## Integration path

1. Daemon C2 passes for `bc0d5c0` → owner accepts → merge `perf/pair-matcher-prefilter` into `main`, tag
   `production-stable-*`.
2. Merge `main` into `feat/sa-workspace` (this branch's merge is the rehearsal; expected identical).
3. Optional, separate commits on top: polish (`feat/sa-polish`, `9fab4be`) and map aliases (`feat/sa-geo-aliases`,
   `bf013b1`), each only if owner-approved.
4. Full suite + this benchmark on the result; tag `deploy-web-*`.
5. Redeploy through the `WEB-LOCAL.md` runbook (stop 8790 server, check out tag, start read-only); live latency check
   above.

## Coupling

- **Polish** (`9fab4be`): `api/pages.py` (`day_bucket` filter), templates, CSS, JS, tests. No overlap with
  `provenance/resolve.py` and no semantic coupling; can ship with or without the catch-up. Templates were guarded
  with `is defined` earlier, so the order does not matter.
- **Map aliases** (`bf013b1`): `api/geo.py`, `api/data/place_aliases.json`, one test. Map placement only; no overlap.
  Pending owner decision (keep both exonyms: net +19 correct markers, or drop "nueva york" / "marsiglia").
- Recommendation: ship the catch-up alone first (pure speed, parity proven), then polish + aliases as a second web
  deploy, so a display change is never confounded with the performance change.
