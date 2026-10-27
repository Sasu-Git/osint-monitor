# Membership-decision provenance

Observability only. One JSON line for every decision about Development membership: why an item joined, formed or
stayed out of a Development, and the evidence the decision used. Identity failures can then be explained from
stored records, instead of by re-executing the link code (`evaluations/phase2-followup/forensics/`).

**It changes no decision.**
- `reconcile` computes exactly the same decisions with logging on or off. The evidence is read from the links it
  already computed, and is gathered only when logging is on (test `test_logging_changes_no_membership_and_no_schema`).
- Nothing in the pipeline reads the log.
- No database table or migration is involved.

## Switch and settings (`AppSettings`, environment or `.env`)

| Setting | Default | Meaning |
|---|---|---|
| `OSINT_MEMBERSHIP_LOG` | `false` | **Off unless enabled.** `true` writes records |
| `OSINT_MEMBERSHIP_LOG_PATH` | `data/logs/membership_decisions.jsonl` | log file |
| `OSINT_MEMBERSHIP_LOG_MAX_BYTES` | `10000000` | rotate at 10 MB |
| `OSINT_MEMBERSHIP_LOG_BACKUPS` | `9` | keep `.1` … `.9`; the oldest is dropped (at most about 100 MB) |

## Where records come from

| Path | Writer | decision |
|---|---|---|
| `formation` | `persist_clusters`: a new Development | accepted |
| `late_attachment` | `persist_clusters`: an item continues an existing Development (the ordinary link path) | accepted |
| `structured` | `persist_clusters`: a structured record group | accepted |
| `held` | `persist_clusters`: an item stays below the Development layer (no link to a member, not linked, or single-source) | rejected |
| `dedup` | `pipeline._process_single_item`: a cross-source near-duplicate attached to its original's Development | accepted |

When an override admitted the best supporting link, it is recorded in `override` (`headline_6h` or `p7`); the path
stays the same.

## Fields

`at, run_id, item_id, event_id, decision, path, reason, supporting_member_ids` (top 5 by cosine), `n_links,
best_cosine, best_headline_cosine, similarity` (dedup), `override, segmentation, places_compatible,
actors_compatible, independent_origins` (new Developments), `competing_event_ids, cluster_fingerprint` (sha1 of the
cluster's sorted item ids, 12 characters), `core_check` (null until a Development-admission rule exists), `source`
(dedup).

**Explicit nulls, never guesses:**
- `actors_compatible` is always null: actors are not part of the current link rule.
- `places_compatible` is null when either item names no place.
- `run_id` is null outside a pipeline run.
- Fields that do not apply to a path are null.

**Example** (scratch database):

```json
{"at": "2026-10-27T16:58:41+00:00", "run_id": null, "item_id": 3, "event_id": 1, "decision": "accepted",
 "path": "late_attachment", "reason": "continues D1: 1 new item(s) linked to its members",
 "supporting_member_ids": [2, 1], "n_links": 2, "best_cosine": 0.8029, "best_headline_cosine": 0.8029,
 "similarity": null, "override": null, "segmentation": "no guard on the supporting link", "places_compatible": null,
 "actors_compatible": null, "independent_origins": null, "competing_event_ids": [], "cluster_fingerprint": "6025ce5fa76a",
 "core_check": null, "source": null}
```

## Volume

- **Record size:** about 0.5 KB.
- **Live rates (snapshot of 2026-10-14 to 2026-10-26):** 550–1,900 new items a day and 250–700 new memberships a
  day. Held items are recorded only when they reach `persist_clusters`, that is, when they were in a cluster.
- **Expected:** about 1–3k records, **0.5–1.7 MB a day**. The 10 MB × 10 rotation keeps roughly **2–6 months**.

## Safety

- **Appends and rotation share a process-wide lock.** The daemon's tiers are threads of one process.
- **A second process writing at the same moment** (a manual `collect` while the daemon runs) can interleave whole
  lines. It cannot fail either process.
- **Every error is swallowed and logged at debug:** an unwritable path, a full disk, a serialisation problem. The log
  never fails a pipeline run (test `test_write_failure_never_fails_the_pipeline`).
- **Cost when on:** the evidence for a decision is read from links `reconcile` already computed. The extra work is a
  few cosine and headline comparisons per recorded item.

## Deployment

Not deployed. Enabling it is a configuration step on the daemon host (`OSINT_MEMBERSHIP_LOG=true` in the daemon
worktree's `.env`), and it needs a deploy of this branch's code under the runbook, with its own approval.
