# Runtime-eligible relation benchmark: design (pre-registered, 2026-10-09)

Owner decision 2026-10-09: relation endpoints stay Development IDs only. The 187-case revision 2 gold stays as
**semantic** relation gold (occurrence / item-set level). A second, **runtime** benchmark is built only from pairs of
two distinct Developments the system actually formed. Session 2 acceptance work is measured on it. This file fixes
the design before any case is drawn.

## Two metrics, always reported separately

1. **Semantic relation quality** (runtime benchmark): when both occurrences exist as distinct Developments, does the
   relation layer propose and accept the right relation? Per type: precision, recall, direction accuracy for
   `reaction_to`, false-positive rate per hard-negative family.
2. **End-to-end relation coverage** (semantic gold revision 2, `runtime-eligibility-rev2.yaml`): of the gold pairs,
   how many had both endpoints available as distinct Developments? Today: 2 of 173 scored cases (149 NOT_SURFACED,
   22 BLOCKED_BY_IDENTITY).

## Windows (development; no sealed holdout overlaps)

| window | span (UTC) | items | source |
|---|---|---|---|
| `2026-10-03-live` | 09-29 12:00 to 10-03 12:00 | 753 | existing frozen relation window |
| `2026-10-05-live` | 10-04 12:00 to 10-06 00:00 | 833 | existing frozen identity development window |
| `2026-10-08-live` | 10-08 00:00 to 10-08 21:00 | about 550 news items | **new**: news sources only, backup-API snapshot of the live DB, frozen by hash before replay |

Excluded: 10-06 00:00 to 10-08 00:00 (the sealed multilingual identity holdout) and the four sealed relation
holdout windows.

## Unit and pair universe

System Developments from a replay of each window with the current code (fixed replay clock). The pair universe is
every pair of distinct Developments in a window whose first reports are at most 7 days apart.

## Strata (seeded 20261009, per window)

| stratum | selects | cap per window | purpose |
|---|---|---|---|
| S1 `generator` | every pair the v1 candidate generator proposes | all | candidate precision; positives |
| S2 `probe` | pairs not in S1 sharing at least one principal actor or a compatible place, first reports within 72 h | 30 | recall of the generator, from pairs it did not select |
| S3 `hard_negative` | pairs not in S1/S2 that share a broad actor pair (US-China, US-Iran, Russia-Ukraine, Israel-Iran, Israel-Palestine, China-Taiwan, US-Russia, China-Japan) or the same Situation | 10 | false-link pressure |
| S4 `random` | uniform random remaining pairs | 10 | base rate |

Selecting stratum is hidden from the annotator and the owner. Recall is estimated from S1 + S2 with stratum
weights (S2 sampled share of its population), and reported with its count basis, not as a bare percentage.

## Labelling (the revision 1 protocol)

1. Blind draft by a separate-context annotator: item text, outlet, time and `taxonomy.md` only.
2. Owner verdicts in the review UI (`/eval/relations`, `RELATION_REVIEW_DIR` pointing at the new review folder).
3. Freeze by hash as `runtime-gold/` before any Session 2 acceptance logic is written.

A pair the owner judges to be one occurrence is `SAME_DEVELOPMENT_SUSPECTED` and goes to identity review.

## Holdout

The runtime benchmark is development data. Its holdout is prospective: after Session 2 acceptance logic is frozen,
a fresh live window collected after the freeze, drawn with the same strata, labelled once, scored once. The sealed
relation holdout (`holdout/`) stays sealed and is still scored once, on semantic quality and end-to-end coverage,
after the implementation is frozen.

## Size

About 25 generator pairs in total plus 50 per window: about 175 cases to label.
