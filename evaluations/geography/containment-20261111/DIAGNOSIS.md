# Place containment gaps: diagnosis (2026-11-11, frozen before any change)

Track 4 of the Situation-v2 upstream hardening cycle: specific places that resolve to **no country** block valid
Situation scope matches (`v2-replay/RESULTS-DEV.md` on `feat/situation-membership-v2-candidate`). This stays
upstream of membership logic: only `config/geography.yaml` may change.

**Input.** Backup-API copy of `data/eval/geolocation-iter3/snap-20261102.db` (sha256
`b5bb5728ce76d3eb28c70712b088b026268538243f4fa099744856dc2c29af40`). Code `b695aa0`. Every specific place stored on
any Development (`situations.store._specific_places`, the helper Situation scope uses), resolved to country
ancestors with `Gazetteer.ancestors`.

## Counts before any change

| | Places | Development references |
|---|---|---|
| Distinct specific places | 1897 | |
| With zero countries | **1659** | 2849 |
| a: real sub-national place, 2+ Developments, missing a parent or an alias (fix) | 112 | 343 |
| a_left: real place left unmapped (ambiguous name, contested status, country absent from the list) | 39 | 124 |
| b: country spelling missing an alias, any frequency (fix) | 67 | 139 |
| c: sea, region, multi-country area (correctly no single country; left) | 60 | 481 |
| d: junk, organisation, person, generic word (left; for event-location upstream) | 137 | 518 |
| not classified: 1 Development and not a country spelling (out of scope) | 1244 | |

Per-place class and proposed target: `classes.yaml` (built by `build_classes.py` from `inventory-before.json`).

## Rules for the fix (fixed here)

- Class a: a `places:` entry (place -> parent) or, for a foreign spelling of a place the gazetteer already knows,
  an `aliases:` entry. Parents are existing gazetteer places or countries.
- Class b: an `aliases:` entry to an existing country.
- No containment for seas, regions or multi-country areas (c). No mapping for contested places (Jerusalem,
  Falklands, Western Sahara, Dongsha): those are owner decisions. No new countries: Palau, Grenada, Antigua and
  Barbuda and the Holy See are absent from the country list and stay unmapped.
- Actor configuration is not touched.

## Frozen files

| file | sha256 |
|---|---|
| inventory.py | `afb7b981e9eb21503d255607148a4c8eb46c13b6a7724a80ca2762ca887d7c70` |
| build_classes.py | `ca198c0f0f3ffb2dd2b09df071cb5e538ab8bb4812f476e023d9502c2051a2a7` |
| classes.yaml | `209fcba291117c20513c9e5973633f5323bb3ae7bb8e0f15188ffc68609c5ed9` |
| inventory-before.json | `e2e5339c38064b3f855361b91f9623fcdefbda812017d506346c93fb4d3bbee9` |
