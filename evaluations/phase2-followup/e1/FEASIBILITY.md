# E1 feasibility gate: result (2026-10-27)

**GATE FAILED. E1 stops here; nothing is implemented.** Recorded conclusion, as pre-registered: *action classes do not
separate cross-day occurrences* in the development data.

Run of `feasibility.py` (frozen in `c1d6669`, amendment 1) on development data only. Per-case output with input
hashes: `feasibility-results.json`. The Phase 2 holdout was not opened (gold `split: holdout` entries and the one
defect case in window 2026-08-31 are dropped unread). No pipeline replay, no live-host load beyond parsing a few
dozen headlines at below-normal priority.

## Gate

| | result | gate | |
|---|---|---|---|
| **F1** cross-day OVERMERGE pairs whose every link the guard cuts | **0 / 5** (0%) | >= 40% | **FAIL** |
| **F2** cross-day SAME pairs with a link the guard cuts | 0 / 7 | <= 1 | pass |

Secondary (information only): 1 of the 5 OVERMERGE pairs has at least one link cut (D101, 1 of 5 links); all
cross-day DIFFERENT pairs: 0 of 9 cut on every link. No label conflicts across sources.

## Why it fails

1. **Headline roots rarely carry a classed action.** Of the 5 OVERMERGE pairs, the links fail on "main action not
   classed" in every case, plus "same class" on D103. The roots found are reporting or colour verbs outside any
   general action class: *call*, *say*, *push*, *re-* (a tokenisation of "re-establishes"). In the multi-item Pike
   cases (D101, D103) most links fail the same way. The one link that fires (D101) is not enough to cut the case.
2. **The cross-day population is too small for E1 to pass even with perfect classes.** Of the 41 development
   OVERMERGE defect cases, **34 have every link within 24 h**, 1 mixes both, and only **6** have every link more than
   24 h apart (D004, D008, D009, D101, D102 at 24.0 h, D103); 5 of those pass the strict > 24 h precondition. The
   development acceptance needs at least 6 OVERMERGE cases fixed, so a cross-day guard could not reach it on this
   data whatever the lexicon. The Phase 2 development split failures add only A002 (= D004) to the cross-day set.

## What this changes

- **Overmerge is predominantly a same-day problem** in the frozen development data (34 of 41), the class for which
  the follow-up results (FR) found "no text signal separates them". The cross-day creep that motivated E1 (and T24)
  is real but small: 5-6 cases.
- The stop condition applies as written: no implementation, no lexicon revision (a revision is allowed only between
  development acceptance and rejection, after implementation), no holdout use.
