# Sample B: location gold (proposal)

Governing spec: design/event-location-model SPEC.md (frozen 2026-11-23, amendment 1).

Snapshot: data/eval/upstream-gold-20261123/gold-snap.db, sha256 7463859a4f3537eb29447a755f252dbebc80cc01a1d855739c57b10489964c3c (verified, opened read-only, backup-API copy in a temp dir).
Script: ../sample.py (shared by both samples; run with the main .venv python, HF_HUB_OFFLINE=1, PYTHONPATH=worktree).
Exclusion inputs: situation-membership key.json sha256 \5817074a533be24cb7610eb6b6d5096e4369c8edb396d48d8ee5813b03042632; geolocation iter3 manifest.json sha256 \59a2e389fd325845874e2424c13490618eee9567421063600c9c55773f1ec6e4. Both exclusions are defensive: they hold ids <= 1341 only, so none of the frame was removed by them.

Eligibility: Developments with id > 1341 (839 in the snapshot), at least one report headline (headline_kind == report; all 839 qualified), dominant language = most common item_language(source, title) among members (en 684, es 106, it 49).

**Status: this sample is a PROPOSAL until the owner starts labelling.** Nothing has been labelled, scored or run through any model. After labelling starts, the sample, case files and this procedure are frozen; changes need a dated amendment.

## Procedure
Seed 20261124. Sample A is drawn first; B is disjoint from A (no overlap, checked), so B pools exclude A's ids. Per language: 40% (en 32, es 14, it 14) from Developments where any member headline matches the language's attack/strike word list, the rest (en 48, es 21, it 21) random from the remaining language pool (strike words may occur there). The word list is used only to stratify, is never shown, and is recorded in manifest.json (`strike_words`). Role subset: seeded 50-Development subset (seed 20261125, `random.sample` over the sorted B ids), marked `role_labels` in manifest.json and cases.json; those cases also ask for per-report place mentions with a role.

## Result: 133 of 150
| stratum | wanted | pool | drawn |
|---|---|---|---|
| en/strike | 32 | 94 | 32 |
| en/random | 48 | 582 | 48 |
| es/strike | 14 | 10 | 10 |
| es/random | 21 | 63 | 21 |
| it/strike | 14 | 1 | 1 |
| it/random | 21 | 21 | 21 |

**Shortfalls (taken whole, not refilled):** es/strike 10 of 14, it/strike 1 of 14. Total 133, not 150. Eligible Spanish and Italian Developments with a strike word are 18 and 9 in the whole frame; sample A (drawn first) took some of them.

## Files
manifest.json, cases.json, countries-iso3.json (suggestion list, from the iteration-3 page), labels.yaml (empty template), label_server.py.

## Labelling
`python label_server.py --port 8794` (127.0.0.1 only), then `--validate`, then `--freeze`. History in label-history.jsonl, first answer per case = blind primary. Fields: event_country (ISO3, NONE, MULTI, SEA_OR_REGION, DISPUTED), event_place, note; for the 50 role cases, per shown report `place | role` lines (roles: event, target, origin, actor_location, venue, reporting, mentioned; `none` if no place). Only headlines, leads and source names are shown.
