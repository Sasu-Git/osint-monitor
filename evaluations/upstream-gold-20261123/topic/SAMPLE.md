# Sample A: topic / event gold (proposal)

Governing spec: design/event-topic-model SPEC.md (frozen 2026-11-23, sha256 83cb5ae0e7b87354f40855d9fe3b371a2a9669840051fbbaeb370898610f6e47).

Snapshot: data/eval/upstream-gold-20261123/gold-snap.db, sha256 7463859a4f3537eb29447a755f252dbebc80cc01a1d855739c57b10489964c3c (verified, opened read-only, backup-API copy in a temp dir).
Script: ../sample.py (shared by both samples; run with the main .venv python, HF_HUB_OFFLINE=1, PYTHONPATH=worktree).
Exclusion inputs: situation-membership key.json sha256 \5817074a533be24cb7610eb6b6d5096e4369c8edb396d48d8ee5813b03042632; geolocation iter3 manifest.json sha256 \59a2e389fd325845874e2424c13490618eee9567421063600c9c55773f1ec6e4. Both exclusions are defensive: they hold ids <= 1341 only, so none of the frame was removed by them.

Eligibility: Developments with id > 1341 (839 in the snapshot), at least one report headline (headline_kind == report; all 839 qualified), dominant language = most common item_language(source, title) among members (en 684, es 106, it 49).

**Status: this sample is a PROPOSAL until the owner starts labelling.** Nothing has been labelled, scored or run through any model. After labelling starts, the sample, case files and this procedure are frozen; changes need a dated amendment.

## Procedure
Seed 20261123, `random.Random(seed)`, strata processed in order en, es, it; within a language "unknown" then "typed"; `rng.sample` over the ascending id pool. Quota per language: en 70, es 40, it 40, half unknown, half typed. "Unknown" = stored event_type NULL, empty or 'unknown'; everything else (including 'other') is typed. The stored type is used only to stratify and is never shown.

## Result: 130 of 150
| stratum | wanted | pool | drawn |
|---|---|---|---|
| en/unknown | 35 | 280 | 35 |
| en/typed | 35 | 404 | 35 |
| es/unknown | 20 | 93 | 20 |
| es/typed | 20 | 13 | 13 |
| it/unknown | 20 | 42 | 20 |
| it/typed | 20 | 7 | 7 |

**Shortfalls (taken whole, not refilled from other strata):** es/typed 13 of 20, it/typed 7 of 20. Total 130, not 150. The typed Spanish and Italian pools are small because most es/it Developments are stored as unknown.

## Files
manifest.json (ids, seed, strata, snapshot sha), cases.json (label input: headlines, leads of up to 600 characters, sources, up to 25 members), taxonomy.json (action types from config/development_types.yaml plus out_of_scope, unknown), labels.yaml (empty template), label_server.py.

## Labelling
`python label_server.py --port 8793` (127.0.0.1 only), then `--validate`, then `--freeze` (writes labels-freeze.json with label and history sha256; edits are refused afterwards). Every save is appended to label-history.jsonl; the first answer per case is the blind primary basis. The page shows headlines, leads and source names only. Fields: action_type, intent, agent, target, speaker, speaker_is_political, note. Intent is optional when action_type is out_of_scope.
