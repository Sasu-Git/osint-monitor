# Place containment, parents-only variant: gate results (2026-11-11)

**Code.** `fix/v2-upstream-places` `aa1d5a2`: a new commit after `2e704e9` (history not rewritten). It removes the
93 alias entries of `252640e` and keeps the 86 `places:` parent entries. Baseline `b695aa0`. Same inputs as
`RESULTS.md`: backup-API copies of `snap-20261102.db` (sha `b5bb5728…`). No live data. Nothing changed after these
results. The 93 aliases are **parked** for a future containment-only track (they also feed actor and entity
aliasing; see `RESULTS.md`).

## Gates (run one at a time)

| Gate | Result |
|---|---|
| Inventory, zero-country places | **1659 → 1569** places, 2849 → 2598 Development references (detail below) |
| Entity benchmark (gold rev 3) | **byte-identical** to the `b695aa0`-code run |
| Identity gold check | passed (checks 1–6) |
| Phase 2 identity, development windows | **identical**: 43/65, 43/58, 22/100, 15/58, 16/19, 12/31 (whole-storyline overmerges 17, as at `b695aa0`) |
| pytest | 764 passed, 3 xfailed |

**Inventory detail.**
- Class a 112 → 26. The 26 left are the foreign spellings of listed places (parked aliases).
- Class b 67 → 67 (all parked aliases).
- Unchanged by design: a_left 39, c 60, d 137.
- Unclassified single-Development places 1244 → 1240.
- Distinct specific places 1897 → 1893.

**Verdict: every gate passes.** The parents-only variant is the containment fix to carry forward. The Situation scope
gaps it closes include Rostov, Donetsk, Kharkiv and Dnipropetrovsk oblasts, El Fasher, Kordofan, Darnitsky and
Gloucestershire. Seas, regions and contested places stay unmapped by design.

Artifact: `inventory-after-parents.json`.
