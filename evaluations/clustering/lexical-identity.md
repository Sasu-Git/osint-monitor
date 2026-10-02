# Lexical identity: what "keyword-based clustering" is, and one candidate rule

Branch `feat/source-inventory-keyword-clustering`, from main at c7c5d4c. Development windows of
the frozen benchmark only (`2026-07-21`, `2026-08-07`, `2026-08-15`, `2026-08-21`, `2026-09-25`);
the hold-out windows have been run already (`holdout_runs.jsonl`) and were not run again.
Scripts: `scripts/lexical_identity/`.

## What counts as a "keyword" today

No production code links two items because they share keywords, terms or actors. Lexical logic
that bears on Development identity:

| where | what is compared | role |
|---|---|---|
| `clustering._linked` -> `lexical.same_source_update` | rapidfuzz ratio of two headlines from the **same outlet**, >= 90 | direct link criterion (same outlet only) |
| `dedup.compute_content_hash` | SHA-256 of normalised title + body | exact duplicate: item dropped |
| `development_segmentation.headline_kind` | headline regexes (analysis / rolling / report) | segmentation guard (cuts links), commentary assignment |
| `segment_groups` locations via `entity_resolver` + `geography` | NER place mentions, alias-resolved (fuzzy alias match at >= threshold) and containment | segmentation guard (disjoint places) |
| `segment_groups` actors | canonical actors | headline override only; `min_shared_actors: 0`, so unused |
| `clustering.region_scores` | configured region keywords in headline/body | `Event.region` label; Situation grouping signal, not identity |
| `situations.grouper` | situation topic keywords, actor overlap | Situation grouping |
| `benchmark.pairs` / `benchmark.rules` | shared actors, principals, organisations, places | offline diagnostics; frozen actor rule never shipped |

Cross-source links are embedding decisions: cosine >= 0.53 on `title + first 200 characters`.
Separately, `dedup` attaches a different-outlet near-duplicate (cosine >= 0.85) to the existing
item's event before clustering; that path is semantic, not lexical, and bypasses segmentation.

## Terms (new, `processors/lexical.py`)

`TermExtractor` turns headline + lead + NER mentions into terms, folding names through the aliases
the pipeline already uses (config/actors.yaml, config/geography.yaml):

- **high**: people and organisations that participate in the reported action
  (`principals.item_participants`), sub-national places, named events/products/systems;
- **medium**: content words not common in the batch; named actors only mentioned; specific
  places that are common in the batch;
- **generic**: countries and nationalities (context), words in >= 5% of the batch, frequent
  non-participant actors, and 14 configured reporting words (`said`, `report`, ...).

Classes come from entity type, the gazetteer and document frequency; the only list is the reporting
words. `keyword_link_evidence` explains a pair (shared actors, terms by class, a diagnostic
weighted overlap, the result and the decision contribution). Example from the live snapshot
(Al Jazeera, 2026-09-29, "Iran touts Hormuz attacks as oil flows increase despite tensions"):
high `hormuz`; medium `oil`, `flow`, `mediator`, `talk`, `washington`, ...; generic `iran`,
`united states`, `attack`.

## Audit: where lexical evidence could have decided (production config, segmentation on)

| pairs in final clusters or gold SAME | event-specific shared | only generic shared |
|---|---:|---:|
| true cross-source links (57) | 56 | 1 (indirect) |
| RELATED linked (78) | 61 | 17 |
| UNRELATED linked (3) | 3 | 0 |
| missed cross-source SAME (7) | 7 | 0 |

Direct links only: of 35 related-but-distinct pairs linked directly by embedding, 32 share
event-specific terms, 3 share only generic ones ("US ... Iran"; a Saudi-Turkiye-Pakistan pact story).
Every direct true cross-source link (56) shares event-specific terms.

Failure modes found:

- **same framing, different occurrence**: "US attacks Iran for 10th consecutive night" vs "11th"
  (same outlet, headline ratio >= 90) is linked as a story update; the ratio ignores ordinals.
- **dominant-story vocabulary**: in 2026-08-07, `pact`, `defence` and the three country names
  are frequent enough to be generic, so the gold-SAME pair "Saudi Arabia, Turkey and Pakistan sign
  defence pact" / "Trilateral Mecca defence pact signed" shares only generic terms and `sign`.
- **related-but-distinct share specific terms**: `pilot`, `zone`, `tariff`, `fifa`, `hormuz`,
  `hegseth` appear in wrong links. Same story, different occurrence: terms cannot separate them.
- **missed joins are framing, not vocabulary**: Trump-Xi state dinner vs "Xi's security chief ...
  at White House banquet" (cosine 0.33), "Hundreds of thousands expected in Paris for Pope's visit"
  vs "Pope Leo heads to France" (0.34): synonyms (`dinner`/`banquet`), containment (Paris in France),
  different angles. One (OCCAR DDX destroyer contract, 0.524) shares 5 specific terms and sits
  just under 0.53.

## Candidate (one, pre-registered before its run)

`lexical.guard`: a cross-source embedding link with cosine below 0.60 stands only if the pair
shares at least one event-specific (high/medium) term. Principle: generic terms and co-mentioned
countries carry no identity weight on their own. Applied in `clustering._linked` for narrative
clustering (HDBSCAN refinement and noise attachment); segmentation builds its members without
terms, so its guards are unchanged. It was chosen after the audit above on the same windows:
the result is in-sample.

| development windows | baseline (= before refactor) | candidate |
|---|---:|---:|
| multi-source developments recovered | 32/37 (missed 4) | 31/37 (missed 5) |
| cross-source SAME pairs linked | 57/64 | 56/64 |
| RELATED_BUT_DISTINCT linked | 78 | 68 |
| UNRELATED linked | 3 | 3 |
| mixed clusters | 24/48 | 24/49 |
| before segmentation: RELATED / UNRELATED linked | 131 / 25 | 111 / 21 |

After segmentation: 11 links changed -- new true 0, lost true 1, false removed 10, false added 0.
Before segmentation: 26 changed -- lost true 2, false removed 24 (14 of them segmentation already cuts).

The refactor with the guard off reproduces the baseline exactly at both stages.

**Decision: KEEP REFACTOR, SAME BEHAVIOR.** The candidate removes 10 related-but-distinct links in
two windows but no mixed cluster disappears and no unrelated link goes; it loses a true
cross-source link and one recovered multi-source development ("US attacks Iran for 10th
consecutive night" / BBC "US launches fresh strikes on Iran ..."). The gain is in-sample and
concentrated; no untouched hold-out exists to confirm it. `guard.enabled` stays false. Not re-tuned.

## Changed links (candidate vs baseline)

Cosine is the clustering embedding's (title + lead). Pairs listed between two items of one outlet
changed because a link elsewhere in their chain was vetoed.

### After segmentation (11 pairs)

| window | gold | A | B | cosine | shared event-specific | shared generic | lexical result | before -> after |
|---|---|---|---|---:|---|---|---|---|
| 2026-07-21 | related_but_distinct | Al Jazeera: Iranian missiles show deadly precision amid US-Iran war escalation | Al Jazeera: US attacks Iran for 11th consecutive night | 0.561 | - | iran, united states | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | related_but_distinct | Al Jazeera: Iranian missiles show deadly precision amid US-Iran war escalation | Al Jazeera: US attacks Iran for 10th consecutive night | 0.598 | - | iran, united states | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | related_but_distinct | Al Jazeera: US launches new strikes as Iran warns of regional turmoil | Al Jazeera: US attacks Iran for 11th consecutive night | 0.551 | tehran | iran, united states | event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | related_but_distinct | Al Jazeera: US launches new strikes as Iran warns of regional turmoil | Al Jazeera: US attacks Iran for 10th consecutive night | 0.492 | - | iran, united states | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | related_but_distinct | Al Jazeera: US attacks Iran for 11th consecutive night | Al Jazeera: Trump threatens to bomb Iranian bridges, power plants over ship attacks | 0.527 | tehran | attack, iran, united states | event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | related_but_distinct | Al Jazeera: US attacks Iran for 11th consecutive night | BBC World: US launches fresh strikes on Iran, as Trump warns of retaliation for deaths of soldiers | 0.537 | - | iran, united states | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | related_but_distinct | Al Jazeera: US attacks Iran for 10th consecutive night | Al Jazeera: Trump threatens to bomb Iranian bridges, power plants over ship attacks | 0.523 | - | attack, iran, united states | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | same_development | Al Jazeera: US attacks Iran for 10th consecutive night | BBC World: US launches fresh strikes on Iran, as Trump warns of retaliation for deaths of soldiers | 0.518 | - | iran, united states | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-08-07 | related_but_distinct | Al Jazeera: War on Iran: Saudi Arabia, Turkiye and Pakistan sign defence pact | Al Jazeera: Israel mulls Saudi, Turkiye, Pakistan pact as elections loom | 0.692 | - | defence, pact, pakistan, saudi arabia, turkiye | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-08-07 | related_but_distinct | BBC World: Saudi Arabia, Turkey and Pakistan sign defence pact | Al Jazeera: Israel mulls Saudi, Turkiye, Pakistan pact as elections loom | 0.541 | - | defence, pact, pakistan, saudi arabia, turkiye | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-08-07 | related_but_distinct | Al Jazeera: Israel mulls Saudi, Turkiye, Pakistan pact as elections loom | Al Jazeera: Saudi Arabia, Turkiye and Pakistan sign joint defence pact | 0.636 | - | defence, pact, pakistan, saudi arabia, turkiye | insufficient event-specific lexical evidence | linked -> not linked |

### Before segmentation (26 pairs)

| window | gold | A | B | cosine | shared event-specific | shared generic | lexical result | before -> after |
|---|---|---|---|---:|---|---|---|---|
| 2026-07-21 | related_but_distinct | Al Jazeera: Iranian missiles show deadly precision amid US-Iran war escalation | Al Jazeera: US attacks Iran for 11th consecutive night | 0.561 | - | iran, united states | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | related_but_distinct | Al Jazeera: Iranian missiles show deadly precision amid US-Iran war escalation | Al Jazeera: US attacks Iran for 10th consecutive night | 0.598 | - | iran, united states | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | related_but_distinct | Al Jazeera: US launches new strikes as Iran warns of regional turmoil | Al Jazeera: US attacks Iran for 11th consecutive night | 0.551 | tehran | iran, united states | event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | related_but_distinct | Al Jazeera: US launches new strikes as Iran warns of regional turmoil | Al Jazeera: US attacks Iran for 10th consecutive night | 0.492 | - | iran, united states | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | same_development | Al Jazeera: US expands strikes on 11th straight night of attacks | Al Jazeera: US attacks Iran for 11th consecutive night | 0.655 | consecutive, night | attack, iran, united states | event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | related_but_distinct | Al Jazeera: US expands strikes on 11th straight night of attacks | Al Jazeera: US attacks Iran for 10th consecutive night | 0.573 | consecutive, night | attack, iran, military, united states | event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | related_but_distinct | Al Jazeera: US attacks Iran for 11th consecutive night | Al Jazeera: Trump threatens to bomb Iranian bridges, power plants over ship attacks | 0.527 | tehran | attack, iran, united states | event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | related_but_distinct | Al Jazeera: US attacks Iran for 11th consecutive night | Al Jazeera: Iran war live: Tehran attacks Gulf states, says 2 tankers in Hormuz on fire | 0.51 | explosion, tehran | attack, iran, reported, united states | event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | related_but_distinct | Al Jazeera: US attacks Iran for 11th consecutive night | BBC World: US launches fresh strikes on Iran, as Trump warns of retaliation for deaths of soldiers | 0.537 | - | iran, united states | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | related_but_distinct | Al Jazeera: US attacks Iran for 10th consecutive night | Al Jazeera: Trump threatens to bomb Iranian bridges, power plants over ship attacks | 0.523 | - | attack, iran, united states | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | related_but_distinct | Al Jazeera: US attacks Iran for 10th consecutive night | Al Jazeera: Iran war live: Tehran attacks Gulf states, says 2 tankers in Hormuz on fire | 0.44 | - | attack, iran, united states | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-07-21 | same_development | Al Jazeera: US attacks Iran for 10th consecutive night | BBC World: US launches fresh strikes on Iran, as Trump warns of retaliation for deaths of soldiers | 0.518 | - | iran, united states | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-08-07 | related_but_distinct | Al Jazeera: War on Iran: Saudi Arabia, Turkiye and Pakistan sign defence pact | Al Jazeera: Israel mulls Saudi, Turkiye, Pakistan pact as elections loom | 0.692 | - | defence, pact, pakistan, saudi arabia, turkiye | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-08-07 | related_but_distinct | Al Jazeera: War on Iran: Saudi Arabia, Turkiye and Pakistan sign defence pact | Al Jazeera: Saudi-Pakistan-Turkiye pact: A new shield or strategic signal? | 0.8 | - | iran, pact, saudi arabia | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-08-07 | related_but_distinct | BBC World: Saudi Arabia, Turkey and Pakistan sign defence pact | Al Jazeera: Israel mulls Saudi, Turkiye, Pakistan pact as elections loom | 0.541 | - | defence, pact, pakistan, saudi arabia, turkiye | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-08-07 | related_but_distinct | BBC World: Saudi Arabia, Turkey and Pakistan sign defence pact | Al Jazeera: Saudi-Pakistan-Turkiye pact: A new shield or strategic signal? | 0.536 | - | pact, saudi arabia | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-08-07 | related_but_distinct | Al Jazeera: Israel mulls Saudi, Turkiye, Pakistan pact as elections loom | Al Jazeera: Will Pakistan-Saudi-Turkiye defence pact change US strategy? | 0.687 | - | defence, pact, pakistan | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-08-07 | related_but_distinct | Al Jazeera: Israel mulls Saudi, Turkiye, Pakistan pact as elections loom | Al Jazeera: Saudi-Pakistan-Turkiye pact: A new shield or strategic signal? | 0.75 | - | new, pact, saudi arabia | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-08-07 | related_but_distinct | Al Jazeera: Israel mulls Saudi, Turkiye, Pakistan pact as elections loom | Al Jazeera: Saudi Arabia, Turkiye and Pakistan sign joint defence pact | 0.636 | - | defence, pact, pakistan, saudi arabia, turkiye | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-08-07 | related_but_distinct | Al Jazeera: Will Pakistan-Saudi-Turkiye defence pact change US strategy? | Al Jazeera: Saudi-Pakistan-Turkiye pact: A new shield or strategic signal? | 0.757 | strategic | pact | event-specific lexical evidence | linked -> not linked |
| 2026-08-07 | related_but_distinct | Al Jazeera: Saudi-Pakistan-Turkiye pact: A new shield or strategic signal? | Al Jazeera: Saudi Arabia, Turkiye and Pakistan sign joint defence pact | 0.686 | agreement | pact, saudi arabia | event-specific lexical evidence | linked -> not linked |
| 2026-08-21 | unrelated | South China Morning Post: China’s telecoms giants bet on ‘token factories’ as AI drives revenue growth | Al Jazeera: Brazil launches AI supercomputer push while balancing US and Chinese tech | 0.558 | - | china | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-08-21 | related_but_distinct | BBC World: Robot horse and rider steal the spotlight at Chinese conference | Al Jazeera: Humanoid crashes during speed test as China’s robotics industry grows | 0.469 | robotic | china | event-specific lexical evidence | linked -> not linked |
| 2026-08-21 | unrelated | South China Morning Post: In the embodied AI race, China can opt to look beyond bigger models | Al Jazeera: Humanoid crashes during speed test as China’s robotics industry grows | 0.557 | - | china | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-08-21 | unrelated | South China Morning Post: China and US push Southeast Asia over their AI blocs. Will it test region’s non-alignment? | Al Jazeera: US allies in Asia wary as Trump moves military assets for Iran war | 0.575 | - | china, region, united states | insufficient event-specific lexical evidence | linked -> not linked |
| 2026-08-21 | unrelated | Al Jazeera: Humanoid crashes during speed test as China’s robotics industry grows | South China Morning Post: Embrace AI to boost competitiveness, Paul Chan says at tech festival opening | 0.455 | humanoid | - | event-specific lexical evidence | linked -> not linked |
