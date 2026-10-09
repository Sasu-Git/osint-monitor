# Phase 3 status: PAUSED — evaluation-blocked by upstream Development identity/coverage

Owner decision, 2026-10-09. Phase 3 runtime relation inference is **paused, not rejected**: runtime-positive relation
cases are too sparse among the Developments the system forms to implement, tune or evaluate acceptance logic. No
relation acceptance logic exists and none is to be written until the upstream limits below are addressed.

## Evidence

| measurement | result |
|---|---|
| Semantic gold revision 2 (187 cases, 173 scored), runtime eligibility | 2 RUNTIME_ELIGIBLE, **149 NOT_SURFACED**, **22 BLOCKED_BY_IDENTITY** (scored); 0 canonical positives of the runtime types eligible |
| Unbiased runtime benchmark (155 pairs of distinct Developments, three live windows) | **0 runtime positives**; 147 NO_RELATION, 7 SAME_DEVELOPMENT_SUSPECTED, 1 `caused_by` (not a runtime type) |
| — of which v1 candidate proposals (fully enumerated) | 35: 0 runtime positives (29 NO_RELATION, 5 identity suspects, 1 `caused_by`) |
| — of which probe (random draw, shared actor or place, <= 72 h) | 0 positives in 90 (population 830) |
| Positive-targeted runtime batch (34 pairs, rounds 1-2) | **0 runtime positives**; 31 NO_RELATION, 3 SAME_DEVELOPMENT_SUSPECTED; eligible pairs: calamity 2, convened 0, reaction 50 |

## Upstream limitations (not relation-layer errors)

- **NOT_SURFACED.** Only 21% of window items (407 of 1946) belong to any system Development; a lone article never
  forms one. Most semantic gold sides are lone articles (explainers, commentary, one outlet's report). Endpoints stay
  Development IDs only (owner, 2026-10-09): raw items are evidence, not occurrences.
- **BLOCKED_BY_IDENTITY.** Whole sequences fall into one Development, so the pair a relation should connect does not
  exist: 22 scored gold pairs in 12 Developments (for example the Hormuz-rejection sequence, 9 pairs; the Christa Pike
  storyline, 14 items). Input: `runtime-eligibility-rev2.yaml`.
- **Identity splits found on the way.** 10 SAME_DEVELOPMENT_SUSPECTED pairs in the runtime benchmark (7) and the
  targeted batch (3), mostly one occurrence reported in two languages: the cross-language identity problem
  (`../identity/xlang-status.md`, paused).

## Preserved (do not delete)

| artifact | where |
|---|---|
| semantic relation gold revision 2 | `gold/relation-gold-rev2.yaml`, `gold/relation-sides-rev2.yaml`, `gold/manifest.yaml` |
| runtime taxonomy contract | `runtime-contract.md`; code `osint_monitor/processors/development_relations.py` |
| relation schema | `development_relations` table, migration 7 (`osint_monitor/core/migrations.py`) |
| persistence layer | `development_relations.check / record / relations_of` (not called by the pipeline) |
| candidate generator v1 | `osint_monitor/processors/relation_candidates.py` (not called by the pipeline); results `candidate-generation-results.md` |
| runtime eligibility | `runtime-eligibility-rev2.yaml` |
| unbiased runtime benchmark | `runtime/gold/` (frozen), design `runtime-benchmark-design.md` |
| targeted batch | `runtime-targeted/gold/` (frozen), design `runtime-targeted-design.md` |

## Holdouts

The sealed relation holdout (`holdout/`) and the sealed multilingual identity holdout
(`../identity/holdout-xlang/`) remain sealed and unopened.

## Resume conditions

Resume relation acceptance work only after upstream work changes the picture, and re-measure first:

1. the Phase 2 over-merge follow-up (the 22 BLOCKED_BY_IDENTITY pairs) and the identity splits;
2. Development coverage, if the owner chooses to work on it;
3. prospective continuous live data (the daemon was restarted detached on 2026-10-09) large enough to hold runtime
   positives. A targeted batch from it must be kept apart in time from the prospective check.

Semantic quality and end-to-end coverage are reported separately whenever this resumes.
