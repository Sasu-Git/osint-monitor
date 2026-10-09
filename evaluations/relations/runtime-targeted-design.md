# Positive-targeted runtime batch: design (pre-registered, 2026-10-09)

Owner decision 2026-10-09: the frozen 155-case runtime benchmark (`runtime/gold/`) is the unbiased baseline and is
not altered. Its probe stratum (0 positives in 90) stays the honest prevalence and recall signal. This separate batch
deliberately targets positives so Session 2 acceptance logic can be exercised. **It is never used to estimate
prevalence or unbiased recall.** Fresh continuous live data collected after Session 2 is frozen is the prospective
check.

## Pools

- **Primary:** the post-deploy live windows already frozen for the runtime benchmark: `2026-10-05-live` and
  `2026-10-08-live` (replays in `runtime/runs/`). Data collected after the daemon restart (2026-10-09 11:33 UTC) is
  not used: it is reserved for the prospective check.
- **Extension (only for a type below 8 confirmed positives after round 1):** `2026-10-03-live`.
- Excluded everywhere: pairs already in the 155-case benchmark, pairs inside one Development, the sealed holdouts
  (multilingual identity holdout 10-06 00:00 to 10-08 00:00 is not in any pool window).

## Targeting (selects pairs for review; never labels)

Units are system Developments. Similarity is the cosine of the two Developments' title centroids (production
embedding model). Per type, pairs are ranked by that cosine and the top ones are drawn:

| type | eligible pairs | max gap |
|---|---|---|
| `same_calamity_lifecycle` | both texts name any hazard (v1 lexicon), and they share the hazard class or a compatible place | 7 days |
| `same_convened_event` | both texts name a gathering (v1 lexicon) and share at least one principal actor | 7 days |
| `reaction_to` | the later text has a reaction cue (v1 lexicon) and they share a principal actor or have cosine >= 0.50 | 96 hours |

These are deliberately looser than the v1 generator (which proposed 0 runtime positives in the benchmark).

## Rounds

- **Round 1:** up to 30 pairs per type from the primary pool (at most 90 cases), shuffled, blind draft by
  separate-context annotators, owner verdicts in the review UI.
- **Round 2 (only if a type has fewer than 8 confirmed positives):** the next 30 pairs of that type from the
  extension pool, same protocol.
- Stop after round 2 whatever the yield, and report the yield per type. Targets: 8 to 12 confirmed positives per
  runtime type.

## Use in Session 2

Measured on this batch (engineering validation, not prevalence): per-type precision, `reaction_to` direction
accuracy, false-link rate on its negatives, and candidate-generation coverage of its confirmed positives. Always
reported next to the unbiased benchmark result and, later, the prospective check.
