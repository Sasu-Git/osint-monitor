# Entity resolution: Core Entity Resolution Principle, enforced in order

Branch `feat/entity-resolution` from main at ee93a3e. Specification: the "Core Entity Resolution Principle &
Enforcement Rules" appended to the entity review (2026-09-30). Implemented in the stated enforcement order,
one commit per stage, each measured on the frozen gold set before the next.

## Gold set (read first)

The review document's human fields were empty when the spec arrived, so the gold labels in
`gold/gold.yaml` were written by Claude from the item text and the spec's rules only, before any entity
code changed, and frozen with SHA-256 (`gold/manifest.yaml`; amended once, before the first run, to drop bare
generic labels such as "Navy" from accepted canonical names). 25 Developments, 87 items (headline + lead),
445 mention entries, 117 role entries, 30 principals. Contestable calls are commented in the file. These
labels are not the owner's: corrections to them would change the numbers below.

Reproduce: `python main.py inspect entity-benchmark [--compare RUN.json] [--out RUN.json]`; saved runs in
`runs/` (predictions included; `--rescore` scores them again). Every run uses temporary copies of the frozen
entity tables (`gold/entities-*.json`, with their learned aliases); no database is touched.

## Result: baseline -> final

| Metric | baseline all | final all | final en | final it | final es |
|---|---:|---:|---:|---:|---:|
| NER detection precision | 86% (370/431) | 96% (378/392) | 98% (356/365) | 77% (10/13) | 86% (12/14) |
| NER detection recall | 94% (370/392) | 96% (378/392) | 96% (356/369) | 100% (10/10) | 92% (12/13) |
| Entity typing accuracy | 92% (341/370) | 95% (359/378) | 95% (339/356) | 90% (9/10) | 92% (11/12) |
| Canonical resolution accuracy | 92% (340/370) | 97% (367/378) | 99% (352/356) | 80% (8/10) | 58% (7/12) |
| Canonical-name hygiene | 96% (354/370) | 99% (373/378) | 99% (351/356) | 100% (10/10) | 100% (12/12) |
| Principal-actor precision | 35% (19/54) | 91% (20/22) | 89% (17/19) | 100% (1/1) | 100% (2/2) |
| Principal-actor recall | 63% (19/30) | 67% (20/30) | 63% (17/27) | 100% (1/1) | 100% (2/2) |
| Actor-role accuracy | 15% (18/117) | 57% (67/117) | 58% (64/110) | 25% (1/4) | 67% (2/3) |

Principal and role rows are per Development; the Italian column for them is the mixed it+es Development
(D23). Alias pollution on the frozen entity tables (`scripts/alias_pollution.py`): learned aliases unlike their
entity (not seeded, not a substring, rapidfuzz < 90) all resolved to it before (66 English, 52 multilingual,
exact alias hits); with the final code 10 of 72 and 12 of 56 still do (the suspect count grows because
capitals no longer normalise to their state, so e.g. a "Moscow" alias on Russia now counts as suspect); the
survivors are same-identity variants (US Navy, Donald J. Trump, Teherán) or Spanish junk spans that the
multilingual NER no longer produces.

## What each stage changed

1. **Fuzzy matches never create durable truth** (entity_resolver): only canonical names, seeded aliases and
   surface variants resolve exactly; learned aliases are fuzzy evidence; fuzzy matches are provisional (never
   stored) and blocked by identity-critical tokens (numbers, country/nationality words, places, acronym
   letters, single-word names, differing name tokens). Method and evidence stored per mention (migration 4).
2. **Normalisation**: NER reads decoded, unglued text; canonical names are clean identities (no article unless
   identity-bearing, possessive, entity or stray punctuation); raw mentions stay on `span_text`.
3. **Multilingual NER**: Italian/Spanish items go to it_core_news_md / es_core_news_md; a language without a
   model yields no entities; clause-like spans fail validation in every language; item language from the feed
   configuration, else script, else function words. Gazetteer: accent-insensitive, it/es names of states.
4. **Institutional hierarchy**: `config/institutions.yaml` (63 bodies, multilateral organisations and forums,
   parents, multilingual aliases) and context resolution of generic labels (Navy, Council, Commission...);
   capitals keep their own identity and act for their state through `represents` (role, not alias).
5. **Actor roles** (`processors/actor_roles.py`): actor / participant / target / affected /
   institutional_context / subject / location from the dependency parse (ClearNLP and UD labels).
6. **Principals from roles**: dominant role "actor" with the existing support threshold, headline evidence
   required when headlines name actors; lowest acting body; roles persisted (`event_entities.actor_role`).
   Nationality words resolve deterministically to their country.
7. **Round-ups**: rolling / in-brief / latest items give no actor evidence. Splitting a round-up into child
   Developments is **not implemented** (it changes the clustering model; left for a separate task).

No downstream blacklist was added. The only lists are data the spec calls for (institution registry, generic
labels, verb classes for roles).

## Downstream checks

- Frozen clustering benchmark (development split): production clusterer and development segmentation
  identical to the baseline. Stage 1 first moved segmentation (2026-07-21: 23 -> 21 cross-source SAME links)
  because "Canadian" had reached the Canada place entity only through a fuzzy match; the deterministic demonym
  step in stage 6 restores it. Offline rule and retrieval-path diagnostics differ (they read entity features).
- Situation matching and ranking key principals through `ActorNormalizer.key`, which maps institutions and
  people to their state, so their keys stay state-level. Principals are fewer and body-level; the owner
  should expect fewer, more precise Situation actor sets. Tests updated where they encoded the old semantics:
  "EU sanctions Russia" no longer makes Russia a principal (target), "Moscow" no longer normalises to Russia.
- `pytest -q`: 541 passed, 3 xfailed. `python main.py smoke`: passed.

## Known remaining failures

- D07: a misparsed headline ("US, UK test SM-6 ...") loses both principals and their actor roles.
- Role accuracy is 57%: quoted speakers counted as actors, Iran/Tehran protesting in D18, Federal Register
  notice structure (D16), the Pentagon's blacklisting upheld (D22, DoD predicted principal).
- Italian model: "AI" typed LOC, "Pranzo alla Casa Bianca" kept as one span; Spanish resolution 58%.
- Round-up splitting (above); the gold set is self-labelled (above).

## Stage tables

### NER detection precision

| Stage | all | en | it | es | es+it |
|---|---:|---:|---:|---:|---:|
| baseline (main) | 86% (370/431) | 98% (354/363) | 29% (8/28) | 20% (8/40) | - |
| 1 fuzzy-alias safety | 86% (370/431) | 98% (354/363) | 29% (8/28) | 20% (8/40) | - |
| 2 text/name normalisation | 86% (372/433) | 98% (356/365) | 29% (8/28) | 20% (8/40) | - |
| 3 multilingual NER | 96% (377/391) | 98% (356/365) | 75% (9/12) | 86% (12/14) | - |
| 4 institutional hierarchy | 96% (378/392) | 98% (356/365) | 77% (10/13) | 86% (12/14) | - |
| 5 actor roles | 96% (378/392) | 98% (356/365) | 77% (10/13) | 86% (12/14) | - |
| 6 principals from roles | 96% (378/392) | 98% (356/365) | 77% (10/13) | 86% (12/14) | - |
| 7 round-up safeguards | 96% (378/392) | 98% (356/365) | 77% (10/13) | 86% (12/14) | - |

### NER detection recall

| Stage | all | en | it | es | es+it |
|---|---:|---:|---:|---:|---:|
| baseline (main) | 94% (370/392) | 96% (354/369) | 80% (8/10) | 62% (8/13) | - |
| 1 fuzzy-alias safety | 94% (370/392) | 96% (354/369) | 80% (8/10) | 62% (8/13) | - |
| 2 text/name normalisation | 95% (372/392) | 96% (356/369) | 80% (8/10) | 62% (8/13) | - |
| 3 multilingual NER | 96% (377/392) | 96% (356/369) | 90% (9/10) | 92% (12/13) | - |
| 4 institutional hierarchy | 96% (378/392) | 96% (356/369) | 100% (10/10) | 92% (12/13) | - |
| 5 actor roles | 96% (378/392) | 96% (356/369) | 100% (10/10) | 92% (12/13) | - |
| 6 principals from roles | 96% (378/392) | 96% (356/369) | 100% (10/10) | 92% (12/13) | - |
| 7 round-up safeguards | 96% (378/392) | 96% (356/369) | 100% (10/10) | 92% (12/13) | - |

### Entity typing accuracy

| Stage | all | en | it | es | es+it |
|---|---:|---:|---:|---:|---:|
| baseline (main) | 92% (341/370) | 95% (335/354) | 25% (2/8) | 50% (4/8) | - |
| 1 fuzzy-alias safety | 92% (341/370) | 95% (335/354) | 25% (2/8) | 50% (4/8) | - |
| 2 text/name normalisation | 93% (345/372) | 95% (339/356) | 25% (2/8) | 50% (4/8) | - |
| 3 multilingual NER | 95% (358/377) | 95% (339/356) | 89% (8/9) | 92% (11/12) | - |
| 4 institutional hierarchy | 95% (359/378) | 95% (339/356) | 90% (9/10) | 92% (11/12) | - |
| 5 actor roles | 95% (359/378) | 95% (339/356) | 90% (9/10) | 92% (11/12) | - |
| 6 principals from roles | 95% (359/378) | 95% (339/356) | 90% (9/10) | 92% (11/12) | - |
| 7 round-up safeguards | 95% (359/378) | 95% (339/356) | 90% (9/10) | 92% (11/12) | - |

### Canonical resolution accuracy

| Stage | all | en | it | es | es+it |
|---|---:|---:|---:|---:|---:|
| baseline (main) | 92% (340/370) | 94% (334/354) | 75% (6/8) | 0% (0/8) | - |
| 1 fuzzy-alias safety | 92% (341/370) | 95% (335/354) | 75% (6/8) | 0% (0/8) | - |
| 2 text/name normalisation | 92% (343/372) | 95% (337/356) | 75% (6/8) | 0% (0/8) | - |
| 3 multilingual NER | 94% (353/377) | 95% (339/356) | 78% (7/9) | 58% (7/12) | - |
| 4 institutional hierarchy | 97% (367/378) | 99% (352/356) | 80% (8/10) | 58% (7/12) | - |
| 5 actor roles | 97% (367/378) | 99% (352/356) | 80% (8/10) | 58% (7/12) | - |
| 6 principals from roles | 97% (367/378) | 99% (352/356) | 80% (8/10) | 58% (7/12) | - |
| 7 round-up safeguards | 97% (367/378) | 99% (352/356) | 80% (8/10) | 58% (7/12) | - |

### Canonical-name hygiene

| Stage | all | en | it | es | es+it |
|---|---:|---:|---:|---:|---:|
| baseline (main) | 96% (354/370) | 95% (338/354) | 100% (8/8) | 100% (8/8) | - |
| 1 fuzzy-alias safety | 96% (354/370) | 95% (338/354) | 100% (8/8) | 100% (8/8) | - |
| 2 text/name normalisation | 96% (358/372) | 96% (342/356) | 100% (8/8) | 100% (8/8) | - |
| 3 multilingual NER | 96% (363/377) | 96% (342/356) | 100% (9/9) | 100% (12/12) | - |
| 4 institutional hierarchy | 99% (373/378) | 99% (351/356) | 100% (10/10) | 100% (12/12) | - |
| 5 actor roles | 99% (373/378) | 99% (351/356) | 100% (10/10) | 100% (12/12) | - |
| 6 principals from roles | 99% (373/378) | 99% (351/356) | 100% (10/10) | 100% (12/12) | - |
| 7 round-up safeguards | 99% (373/378) | 99% (351/356) | 100% (10/10) | 100% (12/12) | - |

### Principal-actor precision

| Stage | all | en | it | es | es+it |
|---|---:|---:|---:|---:|---:|
| baseline (main) | 35% (19/54) | 38% (18/48) | - | 0% (0/5) | 100% (1/1) |
| 1 fuzzy-alias safety | 35% (19/54) | 38% (18/48) | - | 0% (0/5) | 100% (1/1) |
| 2 text/name normalisation | 35% (19/54) | 38% (18/48) | - | 0% (0/5) | 100% (1/1) |
| 3 multilingual NER | 42% (21/50) | 38% (18/47) | - | 100% (2/2) | 100% (1/1) |
| 4 institutional hierarchy | 42% (21/50) | 38% (18/47) | - | 100% (2/2) | 100% (1/1) |
| 5 actor roles | 42% (21/50) | 38% (18/47) | - | 100% (2/2) | 100% (1/1) |
| 6 principals from roles | 79% (19/24) | 76% (16/21) | - | 100% (2/2) | 100% (1/1) |
| 7 round-up safeguards | 91% (20/22) | 89% (17/19) | - | 100% (2/2) | 100% (1/1) |

### Principal-actor recall

| Stage | all | en | it | es | es+it |
|---|---:|---:|---:|---:|---:|
| baseline (main) | 63% (19/30) | 67% (18/27) | - | 0% (0/2) | 100% (1/1) |
| 1 fuzzy-alias safety | 63% (19/30) | 67% (18/27) | - | 0% (0/2) | 100% (1/1) |
| 2 text/name normalisation | 63% (19/30) | 67% (18/27) | - | 0% (0/2) | 100% (1/1) |
| 3 multilingual NER | 70% (21/30) | 67% (18/27) | - | 100% (2/2) | 100% (1/1) |
| 4 institutional hierarchy | 70% (21/30) | 67% (18/27) | - | 100% (2/2) | 100% (1/1) |
| 5 actor roles | 70% (21/30) | 67% (18/27) | - | 100% (2/2) | 100% (1/1) |
| 6 principals from roles | 63% (19/30) | 59% (16/27) | - | 100% (2/2) | 100% (1/1) |
| 7 round-up safeguards | 67% (20/30) | 63% (17/27) | - | 100% (2/2) | 100% (1/1) |

### Actor-role accuracy

| Stage | all | en | it | es | es+it |
|---|---:|---:|---:|---:|---:|
| baseline (main) | 15% (18/117) | 16% (18/110) | - | 0% (0/3) | 0% (0/4) |
| 1 fuzzy-alias safety | 15% (18/117) | 16% (18/110) | - | 0% (0/3) | 0% (0/4) |
| 2 text/name normalisation | 15% (18/117) | 16% (18/110) | - | 0% (0/3) | 0% (0/4) |
| 3 multilingual NER | 17% (20/117) | 16% (18/110) | - | 67% (2/3) | 0% (0/4) |
| 4 institutional hierarchy | 17% (20/117) | 16% (18/110) | - | 67% (2/3) | 0% (0/4) |
| 5 actor roles | 57% (67/117) | 58% (64/110) | - | 67% (2/3) | 25% (1/4) |
| 6 principals from roles | 58% (68/117) | 59% (65/110) | - | 67% (2/3) | 25% (1/4) |
| 7 round-up safeguards | 57% (67/117) | 58% (64/110) | - | 67% (2/3) | 25% (1/4) |

## Errors fixed and introduced per stage

### 1 fuzzy-alias safety

| Metric | fixed | introduced | Developments |
|---|---:|---:|---|
| Canonical resolution accuracy | 1 | 0 | D03 |

### 2 text/name normalisation

| Metric | fixed | introduced | Developments |
|---|---:|---:|---|
| NER detection precision | 1 | 1 | D02 |
| NER detection recall | 2 | 0 | D03, D05 |
| Entity typing accuracy | 2 | 0 | D01, D06 |
| Canonical-name hygiene | 2 | 0 | D01, D06 |

Introduced:
- NER detection precision: D02 'Force' ORG (not in gold) (new prediction)

### 3 multilingual NER

| Metric | fixed | introduced | Developments |
|---|---:|---:|---|
| NER detection precision | 51 | 4 | D23, D24 |
| NER detection recall | 6 | 1 | D23, D24 |
| Entity typing accuracy | 10 | 0 | D23, D24 |
| Canonical resolution accuracy | 8 | 0 | D02, D05, D23, D24 |
| Principal-actor precision | 6 | 0 | D02, D24 |
| Principal-actor recall | 2 | 0 | D24 |
| Actor-role accuracy | 2 | 0 | D24 |

Introduced:
- NER detection precision: D23 'AI' LOC (not in gold) (new prediction)
- NER detection precision: D23 'AI' LOC (not in gold) (new prediction)
- NER detection precision: D23 'Van' PERSON (not in gold) (new prediction)
- NER detection precision: D23 'Gobierno' LOC (not in gold) (new prediction)
- NER detection recall: D23 'Corte Suprema' <- 'Suprema' => 'Corte Suprema' missed

### 4 institutional hierarchy

| Metric | fixed | introduced | Developments |
|---|---:|---:|---|
| NER detection recall | 1 | 0 | D23 |
| Canonical resolution accuracy | 13 | 0 | D03, D08, D11, D18, D19, D25 |
| Canonical-name hygiene | 9 | 0 | D02, D03, D22, D25 |

### 5 actor roles

| Metric | fixed | introduced | Developments |
|---|---:|---:|---|
| Actor-role accuracy | 49 | 2 | D02, D03, D04, D05, D06, D07, D08, D09, D10, D11, D12, D13, D14, D15, D16, D17, D18, D19, D20, D22, D23, D25 |

Introduced:
- Actor-role accuracy: D07 United Kingdom: actor (gold actor) => United Kingdom: location (gold actor)
- Actor-role accuracy: D07 United States: actor (gold actor) => United States: location (gold actor)

### 6 principals from roles

| Metric | fixed | introduced | Developments |
|---|---:|---:|---|
| Principal-actor precision | 25 | 1 | D02, D03, D04, D06, D08, D09, D10, D11, D12, D14, D16, D17, D18, D19, D21, D22, D25 |
| Principal-actor recall | 1 | 3 | D02, D05, D07 |
| Actor-role accuracy | 1 | 0 | D25 |

Introduced:
- Principal-actor precision: D22 predicted 'us department of defense' (not a gold principal) (new prediction)
- Principal-actor recall: D05 gold 'Pakistan|Shehbaz Sharif' => gold 'Pakistan|Shehbaz Sharif' missed (predicted ['houthis', 'saudi arabia'])
- Principal-actor recall: D07 gold 'United Kingdom' => gold 'United Kingdom' missed (predicted [])
- Principal-actor recall: D07 gold 'United States|U.S. Navy' => gold 'United States|U.S. Navy' missed (predicted [])

### 7 round-up safeguards

| Metric | fixed | introduced | Developments |
|---|---:|---:|---|
| Principal-actor precision | 3 | 0 | D18, D21 |
| Principal-actor recall | 1 | 0 | D05 |
| Actor-role accuracy | 1 | 2 | D08, D18, D21 |

Introduced:
- Actor-role accuracy: D08 Kyiv: location (gold location) => Kyiv: None (gold location)
- Actor-role accuracy: D18 Donald Trump: actor (gold actor) => Donald Trump: affected (gold actor)

