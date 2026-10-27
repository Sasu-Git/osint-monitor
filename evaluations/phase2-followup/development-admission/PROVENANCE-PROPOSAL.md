# Membership-decision provenance: proposal (not implemented)

**Problem.** The forensics had to re-execute the link and guard code to explain D398. Decisions, their partners and
their reasons are not stored, and the cluster each decision saw is not recoverable. Future identity failures should
be explainable from stored records.

**Proposal.** One record per membership decision about a Development, written by `persist_clusters` (and by the dedup
path) at the moment of the decision. Observability only: it does not change any decision, and it is deployable
independently of any admission change, on its own approval.

## Record

| Field | Example | Notes |
|---|---|---|
| `run_id` | `33bb69c5…` | pipeline run (joins `pipeline_runs`) |
| `at` | `2026-10-13T09:45:11Z` | |
| `item_id` | 8908 | the candidate item |
| `event_id` | 398 | the Development considered (null for "held, no Development") |
| `decision` | `continued` / `created` / `held` / `rejected` / `dedup` | `rejected`: a local link existed but the Development-level test failed (admission variants only) |
| `path` | `continuation` / `creation` / `dedup` / `structured` | |
| `cluster_key` | sha1 of the sorted item ids of the cluster this decision came from | recovers the cluster without storing it |
| `supporting_member_ids` | `[8331]` | members with a compatible link, top 5 by cosine |
| `n_links` | 1 | all compatible links to this Development |
| `best_cosine`, `best_headline_cosine` | 0.5606, 0.598 | for the best supporting link |
| `guards` | `{"analysis":false,"headline":false,"place":false}` | which guards fired on the best link |
| `override` | `null` / `"p7"` / `"headline_6h"` | if the link needed an override |
| `places_compatible`, `shared_specific_anchors` | `true`, `[]` | |
| `competing_event_ids` | `[401]` | other Developments the item also linked to (the winner's tie-break is recorded) |
| `core_check` | `{"core":[8440,8561,8490],"quorum":"1/3","head":true,"place":true,"passed":false}` | admission variants only; null in DA0 |
| `reason` | `continues D398: 1 link (8331, 0.561)` | the human-readable reason, as `Decision.reasons` today |

## Storage

- **Where.** A rotating JSONL file, `data/logs/membership_decisions.jsonl`, keyed by `run_id`. This means **no schema
  migration**, and the same rotation as `daemon.log`. A database table can follow if queries need joins; that would
  need its own migration approval.
- **Volume.** Only decisions about Developments are written: continued, created, held after linking to an existing
  Development, rejected, and dedup. On the live snapshot (10-14 to 10-26) there were 550–1,900 new items a day (all
  kinds) and 250–700 new memberships a day, so roughly 1–3k records a day at about 400 bytes each, **under 1.5 MB a
  day**. 90-day retention is under about 130 MB.
- **Cost.** The values are already computed in `reconcile` (links, cosines, guards). Writing them adds no similarity
  computation.

## What it would have answered for D398 without forensics

- **The first wrong join and its partner:** 8908, via 8331 at 0.561.
- **Chain-only joins:** 8329's only supporting member was 8908.
- **The cluster each decision saw,** via `cluster_key`.
- **Which joins a core check would have refused,** once variants run.

## Out of scope

Logging every non-linked candidate pair (too large); and storing embeddings or headline vectors (they are already
stored, or can be recomputed).
