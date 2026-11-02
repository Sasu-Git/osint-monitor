# Pair-matcher pre-check: deploy-candidate readiness (2026-11-02)

> **This is a performance-only candidate. Semantic output is expected to remain identical.**

No deploy tag has been created. Deploying needs an explicit owner go-ahead and the normal runbook
(`docs/operations/deployment-runbook.md`).

| | |
|---|---|
| Branch | `perf/pair-matcher-prefilter`, pushed (origin = local) |
| Runtime commit | `bc0d5c0` "perf(provenance): skip syndicated-copy pairs that cannot reach the threshold" (this readiness record is the only later commit, documentation only) |
| Base | `main` `44e0357` = `production-stable-20261102` app code (Candidate B). The branch contains current `main`; no merge was needed |
| Diff vs `main` (runtime) | `osint_monitor/processors/provenance/resolve.py` +22 / −5. Adds `quick_ratio_bound()` and a per-prefix `Counter`, and checks the bound before `SequenceMatcher.ratio()` in `_mark_syndicated_copies` |
| Diff vs `main` (other) | `tests/test_provenance_prefilter.py` (new, 11 tests); this file and `SOAK-CHECKLIST.md` |
| Migrations | **None.** Schema head 6, `core/migrations.py` and `core/database.py` unchanged |
| Config | **None.** `syndication_min_chars` 200 and `syndication_similarity` 0.95 unchanged |
| Dependencies | **None** (`collections.Counter`, `difflib`: standard library) |
| Not included | frontend / read-only web mode, membership provenance logging, collector fixes, Situation rules, DA work, repairs |

## Equivalence (`evaluations/performance/pair-matcher/EQUIVALENCE.md` on `eval/soak-safe-20261102`)

**Frozen benchmark** (32 Developments, frozen before any variant ran: `FREEZE.md`, `1def601`):
- provenance and corroboration outputs are **byte-identical** to the frozen P0 (sha `d704dba1…`). Re-confirmed on
  `bc0d5c0` at 15:1xZ on 11-02;
- the 4 accepted pairs are identical;
- 0 skipped pairs were P0 accepts;
- the pair order and first-match result are identical (the pair set P2 decides equals P0's).

**Full snapshot** (all 1,198 Developments): provenance and corroboration are byte-identical to `main` (sha
`9424ffce…`). **0 mismatches.**

**Boundary scan** (whole snapshot, 148,920 candidate pairs): the bound equals `quick_ratio()` 0 differences;
`ratio()` exceeds the bound 0 times. Pairs whose bound is exactly 0.95 still go to `ratio()`.

**Proof.** `ratio() = 2M/T <= 2m/T = quick_ratio()`, because the matching blocks are a sub-multiset of the shared
characters. So a skipped pair cannot reach the threshold, and the visit order is unchanged.

## Semantic regression gates (main `44e0357` vs branch `bc0d5c0`, same machine, same inputs; development splits only, no holdout opened)

| Gate | Result |
|---|---|
| Phase 2 identity (`score_identity.py`, identity gold rev 2, development windows) | **Identical** (only the run label differs). Also identical to the committed Candidate B gate run `phase2-dev-actor-hygiene-recheck-20261030.json`: 43/65, 43/58, 22/100, 15/58, 16/19, 12/31; 0 duplicate memberships |
| Clustering benchmark (`inspect clustering-benchmark --development`, 6 MB report) | **Identical** (only `generated_at` differs) |
| Segmentation benchmark (`... --development --segmentation`) | **Identical** (only `generated_at` differs) |
| Situation baseline (`inspect situations --full` on a copy of the 2026-11-02 snapshot) | **Byte-identical** (7,616 lines) |
| Entity benchmark (`inspect entity-benchmark`, gold rev 3) | **Byte-identical** |
| Matcher equivalence tests (`tests/test_provenance_prefilter.py`) + provenance tests | passed (see the test line below) |
| Corroboration tests | covered by `tests/test_provenance.py` (`compute_corroboration_score` cases); passed |
| Full pytest / smoke | see below |

Tests on `bc0d5c0`: full suite **738 passed, 3 xfailed** (727 on `main` + 11 new); smoke test **passed**;
provenance and equivalence tests 43 passed (11 new + 32 existing). All re-run on `bc0d5c0` on 2026-11-02 ~15:35Z
with identical results; schema head 6; no diff against `main` in migrations, database models, config or requirements.

## Offline performance (read-only, 2026-11-02 snapshot; `PERFORMANCE.md`)

| | `main` | candidate |
|---|---|---|
| Matcher, all 1,198 Developments | 451.8 s | 1.5 s (−99.7%) |
| Corroboration work, all Developments | 524.9 s | 100.6 s (−81%) |

**Giant Developments:** D449 190.5 s -> 2.0 s, D399 80.7 -> 1.3 s, D639 52.4 -> 0.8 s, D514 36.8 -> 0.9 s.

**Small Developments** (2–10 items): unchanged; the matcher adds at most about 1 ms.

## Expected production effect

**Corroboration stage.**
- **Now:** median 925–1,116 s live.
- **Expected:** drops by about 80%, to roughly 100–250 s, depending on host contention. What remains is per-Development
  overhead. The stage still rescans every Development per run (forensics cause 1, not addressed here).

**Knock-on.** Each tier run holds the SQLite writer for a shorter time, so other tiers' `lock_wait` (median
1,100–1,600 s) should fall and effective hot and warm cadence should improve. This is expected, not measured.

**Also faster:** the summaries stage (it calls the same provenance) and clustering's identity and segmentation, with
identical output.

## Deployment risks

| Risk | Assessment |
|---|---|
| Semantic drift | Proven impossible for the comparison as written, and verified at 0 differences on all snapshot Developments and every gate. Residual risk is only in data shapes the snapshot did not contain; the proof covers those too |
| New runtime failure | Low. The pure-Python `Counter` arithmetic has no I/O and no new exceptions. One `Counter` per item prefix (at most 400 characters) is kept during one `resolve()` call: memory is negligible |
| Hidden coupling | Identity and segmentation call `resolve()`. The gates above show identical results |
| Deploy mechanics | Standard daemon deploy: HOLD, stop, backup, checkout, no migration, start through the launcher, pin, release |
| Rollback | `production-stable-20261102` (`e2c7afe`); the code-only rollback needs no data restore (no schema or data change). The pre-deploy backup is kept anyway |
| Web | Not affected. The production web server (`deploy-web-20261102`) keeps the old matcher until it is redeployed separately |
| Future edits | If the similarity function, `autojunk`, or the prefix rule changes, the bound must be re-proved. The docstring and equivalence tests pin this |

Acceptance after deployment: `SOAK-CHECKLIST.md`.
