# Place containment fix: gate results (2026-11-11)

**Code.** `fix/v2-upstream-places` `252640e` (fix) against base `b695aa0`. The diagnosis was frozen first (`59625d8`).
Nothing in the fix changed after these results. Inputs: backup-API copies of `snap-20261102.db` (sha `b5bb5728…`); no
live data.

**The fix.** `config/geography.yaml` only:
- 86 `places:` parents for class a sub-national places in 2+ Developments;
- 93 `aliases:` for class b country spellings and class a foreign spellings of listed places.

## Gates

| Gate | Result |
|---|---|
| (a) inventory, zero-country places | **1659 → 1476** places, 2849 → 2363 Development references. Class a 112 → 0, class b 67 → 0. Left unchanged by design: a_left 39, c 60, d 137. Unclassified single-Development places 1244 → 1240. Distinct specific places 1897 → 1801: country spellings are now countries, and spellings merge with their place |
| (b) geolocation continuity | **not applicable on this branch.** The geolocation module and the iteration-2 scorer are not on this lineage (they live on the geolocation branches and use their own frozen commits). The deployed map (`geocoding.py`) does not read `geography.yaml`, so stored map behaviour cannot change |
| (c) entity benchmark (gold rev 3) | **byte-identical** to the `b695aa0`-code run |
| (d) pytest | 764 passed, 3 xfailed |
| extra: identity gold check | passed (checks 1–6) |
| extra: Phase 2 identity, development windows (`score_identity.py`) | **changed (regression).** Continuity precision 43/65 → 43/67; split failures 22/100 → 24/100; mixed Developments 12/31 → 13/31; whole-storyline overmerges 17 → 19 |

## Cause of the identity change (diagnostic run, not committed)

With only the 86 `places:` parents (the aliases block removed temporarily), Phase 2 identity is **identical** to
`b695aa0`: 43/65, 43/58, 22/100, 15/58, 12/31, 17 overmerges. The whole regression comes from the 93 aliases.
Aliases in `geography.yaml` do not only feed place containment:
- `ActorNormalizer` uses them as place aliases for actor mentions ("bielorrusia" becomes the actor key `belarus`);
- entity resolution and NLP read them too.

So they change actor keys and Development grouping.

## Verdict

- **Parents (86 entries): pass every gate.** They are upstream containment only and safe to use for Situation scope.
- **Aliases (93 entries): fail the identity continuity check** (2 more overmerges, 2 more split failures, 1 more
  mixed Development on the development windows). They should not go forward as committed. Before they are reused,
  they need their own track, which either:
  - adds them to containment only, without the actor and entity alias paths; or
  - adds them with their own identity diagnosis.

  That needs a code change, which was outside this track's allowed change.
- The Situation scope gaps named in `RESULTS-DEV.md` are covered by the parents:
  - Rostov, Donetsk and Kharkiv oblasts, El Fasher, Kordofan, Darnitsky and Gloucestershire now resolve;
  - seas (Black Sea, Azov), regions and contested places do not, by design.

Artifacts: `inventory-after.json`. The identity run outputs are kept outside the repository (session scratchpad).
