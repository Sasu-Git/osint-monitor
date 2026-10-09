# Cross-language Development identity: status (paused 2026-10-09)

Owner decision, 2026-10-09: stop the cross-language work here and return to Phase 3 relations.

| | status |
|---|---|
| stage | **disabled** (`cross_language.enabled: false`); production code at `5f046b3` has no cross-language stage |
| pre-registered guard experiments | complete, run once each: E0-E7 (`xlang-guard-results.md`, commit `712875e`) |
| decision | **KEEP DISABLED**: no variant qualifies |
| best observed variant | **E5** (G2 broad anchors k=3 + G3 direct links + G4 exact places): 8 stage-added true merges, 3 stage-added false merges (limit 2), 1 new Phase 2 false merge (C090, limit 0) |
| multilingual identity holdout | **sealed** (`holdout-xlang/`), never opened |
| branch | `fix/cross-language-identity`, paused at this commit |

Carried by this branch and not yet on `main`: the GDELT headline-only rule (owner-accepted, decision record
`decisions/2026-10-08-gdelt-headline-only.yaml`), the replay clock fix, identity gold revision 4, the guard
switches (default off), and the post-soak fix 1 commits it is based on.

## Backlog (round 2; not started)

A second round needs a materially different hypothesis and a fresh evaluation structure, not more tuning on the
same development set. Ideas recorded, not executed:

- **resolved-person breadth**: count anchor breadth per resolved person (entity resolution), not per surface name
  (`jair bolsonaro`, `lula-bolsonaro` escaped G2 in E5);
- **analysis-headline guard across languages**: apply the same-language analysis/commentary guard to
  cross-language links (V037, V057 and C090 are commentary or analysis joined to reports);
- **number breadth**: give the number anchor class a breadth test (`200` recurs across the Siberian plague
  coverage).

Known recall cases kept for a future round: R138 (G02, G03; never linked by any variant), C006 (GDELT recall case,
to be recovered without aggregator metadata).
