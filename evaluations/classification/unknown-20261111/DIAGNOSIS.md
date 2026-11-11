# Why Developments are `unknown`: frozen diagnosis (2026-11-11, before any code change)

**Input.** Backup-API copy of `data/eval/geolocation-iter3/snap-20261102.db` (sha256 `b5bb5728…`). Code
`fix/v2-upstream-topic` at `b695aa0` (= `feat/actor-normalization-v2pre`). Classifier backend `rules` (the
production default, `classifier_backend: rules`; no LLM key exists). `diagnose.py` recomputes every Development's
type with the running code. Recomputed equals stored on all but 13 of 1,198 (those were classified by older code).
Output: `diagnosis-base.json`.

## Rates

| | Developments | `unknown` | Rate |
|---|---|---|---|
| all | 1,198 | 547 | **45.7%** |
| English-dominant | 968 | 353 | 36.5% |
| Spanish-dominant | 136 | 108 | **79.4%** |
| Italian-dominant | 94 | 86 | **91.5%** |

(The ~30% quoted for the 126-case set is that subset's rate; the whole snapshot is higher.)

## How `unknown` arises (code)

`RuleBasedClassifier._match_type` votes over headlines, then over lead sentences, with `TYPE_RULES` and
`STATEMENT_TITLE`. **Every pattern is English.** A Development is `unknown` when no headline and no lead sentence
matches, or when the legal/migration guard suppresses every candidate type (by design: the taxonomy has no judicial
or migration type).

## Causes (deterministic split of the 547)

| Cause | Count | Meaning |
|---|---|---|
| `lexicon_gap_en` | 325 | English-dominant, no rule matched |
| `mixed_language_gap` | 102 | es/it-dominant, some English headline present, nothing matched |
| `non_english_headlines` | 91 | es/it headlines only; the English rules cannot match |
| `suppressed_legal` | 24 | legal/migration guard (honest `unknown` by design) |
| `statement_missed` | 5 | es/it statements a stray English token did not rescue (D423, D670, D719, D780, D1028) |

## Manual grouping of the seeded sample of 40 (`sample` in `diagnosis-base.json`, seed 20261111)

| Group | n | Examples | Typeable in the taxonomy? |
|---|---|---|---|
| **es/it headline states a taxonomy type in its own language** | 11 | D208 "Ucrania ataca la región de Moscú con 650 drones"; D840 "afirma haber atacado cuatro buques"; D1071 "Rusia derriba más de 1.200 drones"; D145 / D1082 "al voto", "presidenziali"; D967 "chiede un'inchiesta"; D673 "chiedono un incontro" | **yes**: the rules have no Spanish or Italian vocabulary |
| outside the taxonomy: disasters and weather | 6 | D111 landslides, D429 hurricanes, D476 / D742 floods, D1077 haze, D670 fire | no (no hazard type; §1.4 of the v2 contract handles hazards by lexicon) |
| outside the taxonomy: sport, obituaries, culture, science | 7 | D205 / D219 UEFA, D342 / D1101 deaths, D713 space probe, D373 stolen paintings | no |
| outside the taxonomy: economy data, markets, companies | 7 | D276 euro low, D324 inflation, D1053 Fed holds rates, D236 / D823 / D1068 corporate | no |
| outside the taxonomy: ordinary crime, accidents, health | 6 | D277 abuse charges (guard), D946 drug seizure, D471 rollercoaster, D1092 crash, D780 Ebola | no |
| English, typeable, phrased outside the lexicon | 3 | D394 "picked as new press secretary" (appointment), D293 "suspends plans" (policy), D647 "probed" | yes, but each is a single phrasing |

## Conclusion (frozen)

1. **The dominant typeable gap is language.** The rules are English-only, while 230 of 1,198 Developments are es/it
   dominant and 194 of them are `unknown`. In the sample, 11 of 40 unknowns state a taxonomy type in Spanish or
   Italian.
2. **Most English `unknown`s are correct.** They describe disasters, sport, obituaries, markets, ordinary crime,
   accidents and health, for which the taxonomy has no type. They must stay `unknown`.
3. English one-off phrasings (3 of 40) are not a pattern. They are not fixed here.

**Allowed fix:** Spanish and Italian equivalents of the existing English rules, used only when the English rules find
nothing in a Development, so no already-typed Development can change. No new types, no new semantics, no ML.
