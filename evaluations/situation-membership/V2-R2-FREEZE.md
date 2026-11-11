# Situation membership v2 revision 2: freeze record (2026-11-11)

Owner rulings OD1–OD8 (2026-11-11) incorporated; contract and preregistration frozen before any v2 code exists.
Draft history: `fff0503`. The diagnostic set and its results (`57fef39`, `e8943fd`) are unchanged.

```sha256
115c8c183f196fd3b1ea2633a21caf9746787211379042a359996b82bf31a997  CONTRACT-V2-R2.md
226c899e332069d4c84011db91a973301eb7b0f5bf5bc096ec1514026ce4d30f  PREREGISTRATION-V2-R2.md
872db55551c3954a35ca447f700cd514988931d5135bfa43c6a22c13e1aa4e5a  scope-overrides/2026-11-10-owner-review.yaml
```

The contract fixes these parameters: family mapping v1, `generic_parties` v1, hazard lexicon v1, hedge lexicon v1,
`create_window_days` 7, single-party separation 24 h, `pending_days` 7 (contract §7).

**DEF items (the owner may amend before the holdout window opens):**
- the family mapping;
- the generic-party list;
- both lexicons;
- the single-party 24 h separation;
- the PENDING triggers and expiry;
- hazard Situations being exempt from the no-principals rule;
- pooled non-member rejection;
- the 5-point veto definition;
- the 14-day window;
- the 220-pair stratification.

An amendment is a new dated section here with new hashes. Any amendment after the window opens voids that window.

**Next:** build the candidate against the diagnostic set (no acceptance use), show the OD7 scope mapping to the owner,
freeze the code, open the window.
