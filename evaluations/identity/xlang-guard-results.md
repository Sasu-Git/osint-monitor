# Cross-language acceptance guard: results of the pre-registered experiments

Plan: `xlang-guard-tuning-plan.md` (frozen `d4790a9`, amendments 1 and 2 before any run). Code: `ab83607`. Each
experiment ran once, on the development windows only; neither holdout was opened. Raw results:
`runs/xlang-guard/*.json`, `runs/xlang-guard/summary.json`.

## Verification of the defaults

E0 (all switches at their defaults) reproduces `runs/rev4-xlang-clock.json` row for row on the 74 rev4 additions,
with the same 103 accepted links. OFF reproduces the stage-off rows. The switches change nothing when off.

## Results

Rev4 additions: TP / FP / FN with the stage on. "Added" is relative to the OFF run of the same code. Phase 2 new
false = DIFFERENT pairs of the Phase 2 identity gold together with the stage on and apart in OFF (amendment 1).
Mandatory = G12, G13 (RAF Fairford), G14 (Siberian plague).

| exp | components | TP/FP/FN | added true / false | Phase 2 new false | mandatory | R138 (G02, G03) | C006 | links | qualifies |
|---|---|---|---|---|---|---|---|---|---|
| E0 | none | 15/22/24 | 12 / 20 | C041, C078, C090 | pass | fail | fail | 103 | no |
| E1 | G1 | 5/6/34 | 2 / 4 | C041, C078, C090 | **fail** (G12, G13) | fail | fail | 21 | no |
| E2a | G2 k=3 | 11/5/28 | 8 / 3 | C041, C078, C090 | pass | fail | fail | 44 | no |
| E2b | G2 k=5 | 15/18/24 | 12 / 16 | C041, C078, C090 | pass | fail | fail | 83 | no |
| E3 | G3 | 14/18/25 | 11 / 16 | C090 | pass | fail | fail | 86 | no |
| E4 | G4 | 15/22/24 | 12 / 20 | C041, C078, C090 | pass | fail | fail | 101 | no |
| E5 | G2 k=3 + G3 + G4 | 11/5/28 | 8 / 3 | C090 | pass | fail | fail | 38 | no |
| E6 | G1 + G3 + G4 | 5/6/34 | 2 / 4 | C090 | **fail** (G12, G13) | fail | fail | 18 | no |
| E7 | G1 + G2 k=3 + G3 + G4 | 3/3/36 | 0 / 1 | C090 | **fail** (G12, G13) | fail | fail | 6 | no |

Link counts include links accepted again at later ticks of the same window; they compare between experiments, not
with gold.

k for E5 and E7: 3 (neither E2 variant qualifies; E2a has fewer stage-added false merges; amendment 2).

## Decision (plan section 6)

No variant qualifies: **KEEP DISABLED**. The reject condition (no variant under 5 stage-added false merges while
keeping 8 true merges) is not met: E2a and E5 reach 3 false merges with 8 true merges.

## Why the closest variant (E5) fails

E5 misses the bar by one stage-added false merge (3, limit 2) and one Phase 2 false merge (1, limit 0):

- **V027** (Brazil election): the broad names are caught (`bolsonaro`, `flavio bolsonaro`, `lula`,
  `luiz inacio lula da silva` are all marked broad), but surface variants of the same people are counted as separate
  anchors and are not broad: `jair bolsonaro`, `lula-bolsonaro`. G2 counts names, not people.
- **V037** (Siberian plague, commentary vs report): the number `200` recurs across the storyline's coverage and is
  accepted alone where the places are broad; `irkutsk~irkutsk` and `siberia~siberia` still match in the smaller
  units. The number class has no breadth test.
- **V057** (Hamas, commentary): `hamas` occurs in three units or fewer in that run, so it is not broad at k = 3, and
  the number `250` adds a second class.
- **C090** (Meloni on Regeni / Rome-Cairo thaw, analysis): `meloni` and `rome` are rare in the 48 h multilingual
  window, so neither is broad. Rome passes as a specific place because `actors.yaml` does not map it to Italy.

G1 (two anchor classes) is the only component that removes most false merges on its own, but it also removes the
RAF Fairford links (G12, G13: one specific place, no second class), which are mandatory. G3 removes chained merges
(C041, C078, V013, V018, V023, V036) at the cost of one true merge (V033).

## What the results say about the approach

- Breadth by name frequency (G2) works where a storyline is large (Brazil, Gaza) and fails where it is small (one
  Meloni statement, one Hamas commentary in a short window). Storyline-level co-reference is not visible from
  frequency within one 48 h run.
- The remaining false merges are commentary/analysis items joined to reports (V037, V057, C090). The same-language
  pipeline separates these with the analysis-headline guard; the cross-language stage does not apply it.
- R138 (G02, G03) is not recovered by any variant, and no accepted link touches its items in any run. G03's items
  have a multilingual cosine of 0.44 (below the 0.60 floor): never a candidate. G02's items score 0.72 and are 0.5 h
  apart, so the failure is either the unit centroid or the acceptance step: the shared actor is Trump, a leader,
  which is not an anchor, and the pair shares no specific place or number. Rejected candidates are not recorded, so
  the two cannot be told apart from these runs. No acceptance guard tested here can add a link.

Any further round needs a new pre-registered plan. Candidate directions, not tested here: count breadth by resolved
person (entity resolution) rather than surface name; apply the analysis-headline guard across languages; give the
number class a breadth test.
