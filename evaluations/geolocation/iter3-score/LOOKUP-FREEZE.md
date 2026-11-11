# Iteration 3, step 3: country lookup audited and frozen (2026-11-11)

Owner approval (2026-11-11): run FREEZE.md steps 3–5 exactly; do not change labels, sample, candidate rules or the
gazetteer extension. This step changes none of them.

## The lookup

The scoring lookup maps the location module's country output to ISO3:

1. `lookup-overrides.json` (new, evaluation-local);
2. then iteration 1/2's lookup unchanged: `DISPUTED_ISO` (west bank, gaza, east jerusalem → PSE; crimea → UKR;
   western sahara → ESH), then the web code's `CountryIndex.of_place` at `ab45312` (`osint_monitor/api/geo.py` and
   `osint_monitor/api/data/countries.json`), resolved through the shared gazetteer.

## Audit (`lookup_audit.py`)

Checked every country name `decide()` can emit (189: gazetteer countries, U4 disputed entities, rule-5a territories,
rule-4a Congo names, extension countries) and every gold code, on both label bases (final labels and blind first
answers).

| Check | Before (`lookup-audit-before.json`) | After (`lookup-audit-after.json`) |
|---|---|---|
| A. emittable names with no code | `south sudan` | none |
| A. names mapped to an id missing from `countries.json` | none | none |
| B. gold codes no emittable name can reach | `HKG` | none |
| C. gold codes outside the labeller list / `countries.json` | none / none | none / none |

Also found (not a missing code, a wrong equivalent): `hong kong` and `macau`, rule 5a's own entities, mapped to `CHN`
through the gazetteer's containment. A correct 5a output would have scored as China.

## Fixes (`lookup-overrides.json`, all three)

| Name | Code | Why |
|---|---|---|
| `hong kong` | `HKG` | rule 5a's entity; owner ruling 2026-11-10 keeps Hong Kong its own entity (never mapped back to CHN) |
| `macau` | `MAC` | rule 5a's second entity |
| `south sudan` | `SSD` | gazetteer country with no name match in the web lookup (iteration 2's D286 harness limitation) |

Without rule 5a the module emits `china` for Hong Kong places, so those outputs still map to `CHN` (by design: it is
what that rule set says). Iterations 1 and 2 never emit `hong kong` or `macau`; for them only `south sudan` changes.

## Frozen hashes (sha256)

| File | sha256 |
|---|---|
| `lookup-overrides.json` | `6a30949de6f4736a938233c45c6106153fbd20a4ad4300abbabf3ebe1004b277` |
| `lookup_audit.py` | `b220df3763a81080c60f02b8ef167b64f333e8eebd90199da2a23255d3649e3c` |
| `lookup-audit-before.json` | `6fadd3296111a1014536ec9119b00f5371a4020f49faa38d4f85f6b923b6cae5` |
| `lookup-audit-after.json` | `b9b80ede220d9086efdfd16abeb58ef28ab9a08bb3cb891e68a2842bcf84f8d7` |
| `ab45312:osint_monitor/api/geo.py` (git archive) | `5c3c6e2f68b8a3ba3a1d64ae24feb1ba93a6a654f7ca91e9d9e0a3c3af3ff723` |
| `ab45312:osint_monitor/api/data/countries.json` (git archive) | `804e425931b658d684799793bcca040c952b00f4b69c2ba7068ac1117c6c2d27` |
| `config/geography.yaml` (gazetteer, unchanged) | `21e0eb38ee9ae4e04a99ad7d27328ae581770ee02308822f369e21ac3072c2cb` |
| `osint_monitor/processors/data/place_extension.json` (unchanged) | `5924ddf2668243aa19ec570d07d6fdb1121010c7a0db1523c1021a98c600ba12` |

Inputs verified before the audit: snapshot `snap-20261105.db` `d85cbac4…`, `manifest.json` `f238d640…` (CRLF bytes on
disk), owner labels `78b13748…` (`labels-freeze.json`), label history `23fe6fec…`.
