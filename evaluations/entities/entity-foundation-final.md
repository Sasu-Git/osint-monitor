# Entity foundation: final state of `feat/entity-resolution`

The entity layer as accepted after the owner review. History: `entity-resolution.md` (seven enforcement stages,
Claude-written gold rev 1), `owner-gold-rescore.md` (owner-reviewed gold rev 2, rescore of the saved runs, error
ledger, D07 fix). This note covers the final pre-foundation pass: one benchmark-label correction (gold rev 3),
the language-model degradation check and the final regression gates.

## Gold revisions

| Rev | Change | Hash history |
|---|---|---|
| 1 | Claude-written labels (owner review fields empty) | `manifest.yaml` `previous_revisions` |
| 2 | Owner-reviewed principals/roles (D05, D07, D10, D13, D15, D21, D23, D24, D25) | same |
| 3 | "Donald J. Trump" accepted as a name of Donald Trump | current `sha256` |

D24 (confirmed): principals `Iran`, `United States`; Donald Trump role `subject|representative`, `represents:
United States`; Trump is not an alternative principal.

Rev 3 rationale: the multilingual entity table has one full-name Trump entity (id 180, canonical "Donald J.
Trump", "Donald Trump" among its learned aliases); the runtime resolves "Donald Trump" to it. Same person: a gold
omission, fixed in the gold only. No runtime change. Audit (`scripts/gold_audit.py`, 10 checks): passes.

## Final benchmark (gold rev 3, `runs/r3/09-final.json`)

| Metric | baseline (main) | final | en | it | es | es+it |
|---|---:|---:|---:|---:|---:|---:|
| NER detection precision | 86% (370/431) | 96% (378/392) | 98% (356/365) | 77% (10/13) | 86% (12/14) | |
| NER detection recall | 94% (370/392) | 96% (378/392) | 96% (356/369) | 100% (10/10) | 92% (12/13) | |
| Entity typing accuracy | 92% (341/370) | 95% (359/378) | 95% (339/356) | 90% (9/10) | 92% (11/12) | |
| Canonical resolution accuracy | 93% (343/370) | 98% (372/378) | 99% (352/356) | 90% (9/10) | 92% (11/12) | |
| Canonical-name hygiene | 96% (354/370) | 99% (373/378) | 99% (351/356) | 100% (10/10) | 100% (12/12) | |
| Principal-actor precision | 31% (17/55) | 80% (20/25) | 77% (17/22) | - | 100% (2/2) | 100% (1/1) |
| Principal-actor recall | 65% (17/26) | 77% (20/26) | 74% (17/23) | - | 100% (2/2) | 100% (1/1) |
| Actor-role accuracy | 15% (18/119) | 58% (69/119) | 59% (66/112) | - | 67% (2/3) | 25% (1/4) |

Rev 2 -> rev 3 changes only canonical resolution: 5 units fixed (D23 x4, D24 x1), 0 introduced; Spanish 7/12 ->
11/12, Italian 8/10 -> 9/10. Principal and role metrics per Development; the es and es+it columns rest on one
Development each (D24, D23) and are anecdotes, not rates.

Remaining resolution misses (6): "Gobierno de Irán" (es, resolver does not map "Government of X"), "Pranzo alla
Casa Bianca" (it NER span), "U.S. Navy Award Contract" (title-case span), "Navy" and "The Air Force" (generic
labels falling through to legacy bare entities), "Chelsea, MA" (state suffix).

## Entity contract (runtime and persisted)

| Concept | Runtime | Persisted |
|---|---|---|
| canonical entity | `EntityResolver` (registry, demonym, trusted exact, normalised, provisional fuzzy, new) | `entities.canonical_name`, `entity_type`; `item_entities.resolution_method`, `resolution_evidence` |
| actor, participant, target, affected, institutional_context, subject, location | `actor_roles.development_roles` (per Development, from the parse) | `event_entities.actor_role` (smoke DB: actor, target, location observed) |
| principal | `principals.development_actors` (dominant role actor, support threshold, headline actors) | `event_entities.is_principal` |
| representative | **not a runtime role.** `config/actors.yaml` `represents` maps people and capitals to their state for Situation matching only; a leader who acts is `actor` | none |
| lead principal / secondary actor | **not runtime-native**: every sufficiently supported actor is a principal | none |

The older `item_entities.role` / `event_entities.role` column (SUBJECT / OBJECT / LOCATION) is the legacy NLP
role and is unrelated to `actor_role`. `representative` and `principal_roles` exist only in the benchmark gold.

## Language models

`ner_status()` mirrors the loaders without loading anything and is shown in `main.py status`, printed at daemon
startup (with a logged warning when degraded) and checked by smoke:

| Case | status / daemon | smoke | runtime |
|---|---|---|---|
| all installed | `English/Italian/Spanish NER: available (...)` | `NER models ... OK` | normal |
| `en_core_web_lg` missing, `en_core_web_sm` installed | `English NER: DEGRADED (... using en_core_web_sm, lower NER quality)` | `DEGRADED` | falls back to sm (warning) |
| no English model | `English NER: MISSING (...) -- the pipeline cannot extract entities` | `FAIL` | `get_nlp` raises `SpacyModelMissing` |
| `it_core_news_md` or `es_core_news_md` missing | `Italian NER: MISSING (...) -- it items get no entities, roles or principals` | `DEGRADED` | items of that language get no entities (warning logged) |

Verified: the four cases in unit tests (`test_a_missing_language_model_is_reported_not_silent`); the no-English
case end to end (`OSINT_SPACY_MODEL=<missing>`: status MISSING, smoke FAIL); an unloadable Italian model end to
end (status MISSING, `extract_entities(..., "it") == []`, warning logged). `en_core_web_sm` is not installed
here, so the fallback case is verified only in the unit test. No model was added.

## Known runtime limitations (deferred, not fixed here)

- **Lead principal vs secondary actor** not runtime-native (D05: Houthis and Pakistan are principals beside
  Saudi Arabia).
- **Representative semantics incomplete**: no representative role; a leader and the state it speaks for can both
  be principals (D10 Milei); representative units are scored wrong (D10, D13, D24).
- **Implicit institutional agents**: agentless notice headlines give no principal (D16 CBP, Federal Register).
- **Court/legal syntax**: "US court upholds" hands the court's role to the state; the genitive agent of the upheld
  action becomes an actor (D22).
- **Institution-heavy NER spans**: bare "Council"/"Commission" at headline start missed (D25); title-case spans
  swallow verbs (D03 "U.S. Navy Award Contract"); generic labels unresolved in ambiguous context (D07 Navy, D08
  Air Force).
- **Actor / participant / target / affected ambiguity**: 50 of 119 role units still wrong, classified in
  `owner-gold-rescore.md` (upstream NER 12, participant/target/affected 8, places 7, parse 5, institution vs
  context 6, quoted speakers 4, representative 3, actor vs participant 2, mixed Development 2, roundup 1).
- Remaining principal errors: 11 (5 false positives D05 x2, D10, D22 x2; 6 misses D03 x2, D16, D22, D25 x2).

## Regression results (final vs accepted pre-task state f69708e)

| Gate | Result |
|---|---|
| Gold consistency audit | passes (10 checks) |
| Entity benchmark | predictions identical to f69708e (`runs/r3/08` vs `09`); metric changes come only from the rev-3 label (5 resolution units) |
| Frozen clustering benchmark (`--development`) | identical except `generated_at` |
| Development segmentation (`--development --segmentation`) | identical except `generated_at` |
| Situation actor sets (214 events, 4 read-only working-copy DBs) | identical to f69708e |
| `pytest -q` | 547 passed, 3 xfailed (544 + 3 new language-model cases) |
| smoke | passes; `NER models ... OK English, Italian, Spanish` |

The only runtime change in this pass is diagnostic. `ner_status` now reports the English fallback model as
DEGRADED instead of MISSING, and smoke fails only when no English model exists. Entity extraction is untouched.
The clustering holdout was not run.

## Migration note

This branch adds migration 4 (`item_entities.resolution_method`, `item_entities.resolution_evidence`,
`event_entities.actor_role`). The unmerged `feat/localhost-demo` also adds a migration 4 (summaries). Whichever
branch lands second must renumber its migration to 5 and confirm `head_version()` and the recorded schema version
of existing databases agree before deploying.

## Decision

**ENTITY FOUNDATION READY TO COMMIT**

The remaining errors are documented runtime limitations and none is a regression against main. The owner gold
is frozen and consistent. Every gate is identical to the accepted state except the intended label correction and
the diagnostic fix. Missing language models are now visible and never silent.
