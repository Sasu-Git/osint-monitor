# Phase 1: run ledger and membership time

Addresses audit stop condition S3 (temporal semantics) at the data level (`full-basis-audit.md`, Phase 1).
It records facts only. No decision logic reads them yet: clustering, segmentation, principals, ranking and
Situations are unchanged.

## What is recorded

| Fact | Where | Written by |
|---|---|---|
| A pipeline run: opaque UUID (hex32, never time-derived), kind, tier, start and finish, status (running / ok / partial / failed), items collected and new, per-stage outcome, error, code SHA + dirty flag, config hash (SHA-256 over `config/`), NER models per language + embedding model | `pipeline_runs` | `core/runs.py` `start_run` / `finish_run`, called by `run_tier` (under the write lock) and the one-shot `run_pipeline` |
| The run that stored an item | `raw_items.ingested_run_id` | `_process_single_item` |
| When, and in which run, a membership was created | `event_items.added_at`, `added_run_id` | `persist_clusters` (new and extended events) and the near-duplicate link |
| Publication time of the earliest member item | `events.earliest_published_at` | `clustering.update_earliest_published` |
| A membership exists once | UNIQUE(`event_items.event_id`, `item_id`) | schema |

**Creation time is unchanged.** `events.first_reported_at` remains the row-creation (processing) time and is not
repurposed. `earliest_published_at` sits next to it.

**The facts stay raw.** They allow later logic to distinguish three cases, without Phase 1 deciding what any of
them means:
- **newly ingested item:** `ingested_run_id == added_run_id`;
- **existing item newly attached to a Development:** `ingested_run_id` is an earlier run than `added_run_id`;
- **reprocessing of an unchanged membership:** a run that created no `event_items` row for it.

**Not stamped (recorded as NULL):**
- items stored through `POST /api/ingest` or the webhook;
- the smoke harness;
- every membership created before migration 5. Their time is unknown and is not invented.

## Migration 5

Migration 5 adds the three stamp columns, `events.earliest_published_at` (backfilled from member items) and the
indexes. It removes identical duplicate memberships (keeping the oldest row) before creating the unique index.
The `pipeline_runs` table comes from `create_all`.

Tested on copies only, made with SQLite's online backup API from read-only sources:

| Shape | From → to | Integrity | FK violations | Row counts | Memberships stamped | `earliest_published_at` | Re-run |
|---|---|---|---|---|---|---|---|
| `data/osint.db` copy | v3 → v5 | ok | 0 | unchanged | 0 (none invented) | 15 / 19 events | no-op, no second backup |
| `data/eval/osint-eval-p1.db` copy | v3 → v5 | ok | 0 | unchanged | 0 | 8 / 8 | no-op |
| `data/backups/osint-pre-v3-*.db` copy (v2-era shape) | v2 → v5 | ok | 0 | unchanged | 0 | 15 / 19 | no-op |

The 4 events without a publication time in `osint.db` have no member item with a `published_at`.

Unit test `tests/test_run_ledger.py`:
- a v4 shape built from the model DDL without the v5 columns;
- a duplicate membership removed;
- no membership time invented;
- the backfill and the indexes present;
- a pre-migration backup taken.

**Migration numbering.** This branch now uses migrations 4 (entity resolution) and 5 (run ledger). The unmerged
`feat/localhost-demo` branch's own migration 4 (development summaries) is renumbered to **6** when that branch is
reconciled, not now. Its local `data/demo/osint-demo.db` records v4 with the demo's semantics and needs rebuilding
or explicit repair at that point.

## Gate: incremental replay

`scripts/phase1_replay.py` replays a frozen benchmark window in a temporary DB:
- run 1: the first half of the window, by publication time;
- run 2: the second half;
- run 3: post-processing with no new items.

Publication times are translated into the present by one common offset, so the clustering window (items
fetched and published within 48 h) holds them. Results are in `runs/phase1-replay-*.json`.

| Window | Items (run 1 / run 2 / run 3) | Memberships added (run 1 / 2 / 3) | New item, new membership | Existing item newly attached | Unstamped | Gate |
|---|---|---|---|---|---|---|
| 2026-07-21 | 92 / 92 / 0 (90 and 92 stored) | 7 / 35 / **0** | 36 | 6 | 0 | PASS |
| 2026-08-07 | 83 / 84 / 0 (81 and 83 stored) | 16 / 29 / **0** | 42 | 3 | 0 | PASS |

Across both windows:
- run 3 (reprocessing only) created **no** membership;
- items first stored in run 1 and attached only in run 2 are identified as such (6 and 3);
- every membership and every stored item carries its run;
- run ids are unique hex32 UUIDs;
- all runs recorded status ok, code SHA, config hash and model versions.

The gate condition in the script: run ids unique and hex32, no unstamped membership, no membership attached
before its item was stored, zero memberships from run 3, and at least one new-item membership.

## Unchanged (regression gates)

Compared with `main`:

| Gate | Result |
|---|---|
| `pytest -q` | 562 passed, 3 xfailed (5 new Phase 1 tests; one existing concurrency test's fake session gained `add` / `commit`) |
| smoke | passes (migrations OK) |
| entity benchmark / gold audit | no unit changed / passes |
| frozen clustering benchmark (`--development`) | identical except `generated_at` |
| development segmentation (`--segmentation`) | identical except `generated_at` |

No decision reads the new columns, so Development membership, principals, ranking and Situations are
unchanged by construction; the benchmarks confirm it for clustering and segmentation.
