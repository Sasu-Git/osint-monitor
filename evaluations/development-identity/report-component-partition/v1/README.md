# Report-component partition evidence, v1

Raw per-Development component evidence. Owner ruling 2026-11-23: no production schema change, no semantic
flag field, no downstream use.

## What the evidence is
`snap-7463859a.jsonl`: one line per Development with at least 1 member (2180 lines), sorted by `development_id`,
LF line endings. Keys: `development_id`, `algorithm_version` (`report-components-v1`), `report_item_count`,
`component_sizes` (descending ints; `[]` when no report items), `snapshot_sha256`, `run_id`
(`rcp-v1-20261123-7463859a`).

## Algorithm
Reused from the read-only diagnostic `evaluations/development-identity/mixed-flag-20261114/mixed_flag_diagnostic.py`
on `origin/eval/mixed-flag-diagnostic` (report-only component computation). Implemented in `build_partition.py`:
1. Rebuild SegmentItems with `development_segmentation.segment_items`, using the `development_segmentation`
   section of `load_event_grouping_config()`.
2. Keep only items with `headline_kind == "report"`.
3. Connected components over item pairs where `compatible_link` is true.
Unlike the diagnostic, Developments with a single member are included (the diagnostic skipped them).

Inputs and provenance:
- Snapshot `data/eval/upstream-gold-20261123/gold-snap.db`, sha256
  `7463859a4f3537eb29447a755f252dbebc80cc01a1d855739c57b10489964c3c` (verified before use; opened read-only,
  worked on a backup-API copy with `PRAGMA query_only=ON`).
- Code SHA (origin/main): `b92acc661bf52dc2bc53ae08916201c9f1b83a79`.
- Config: `config/event_grouping.yaml` sha256 `f3777650d116fa17e205f09bb0db238362b53326f73d8fac337355fc5350ac43`.
- Output sha256: `66dec13367890068c15e296f4cc22881ca192aee80472bb65336068bb75e89a6`.

Run: `HF_HUB_OFFLINE=1 PYTHONPATH=<worktree> <main .venv python> build_partition.py <snapshot> <sha256> <out.jsonl>`

## Deriving the owner's V4 condition
V4 is derived at read time: "at least two report-item components, each with at least two items". It is never
stored as a field. `python derive_v4.py [file.jsonl]` prints the derived count (12 on this snapshot).

## Status
Nothing consumes this file yet.
