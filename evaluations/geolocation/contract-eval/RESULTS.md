# Location contract, first evaluation (2026-11-02): NOT READY

**Scope.** Module `osint_monitor/processors/event_location.py` (`62fe91d`), offline, on frozen inputs (`FREEZE.md`,
committed before the first result; the two amendments are an import fix and YAML quoting, with no expectation, rule
or metric changed). No geocoder was used; the evaluation is gazetteer-only.

**Gates.** Both are `PROPOSED`, not established. The result is reported as measured; no rule was tuned after seeing
it.

| Measure | Result | PROPOSED gate |
|---|---|---|
| Audit W (wrong stored point) **removed**: not placed in the wrong country again | **91 / 94 (96.8%)** | ≥ 80%: met |
| Audit C (right stored point) **preserved** in the same country | **24 / 81 (29.6%)** | ≥ 90%: **not met** |
| C lost to NONE / C moved to another country | 36 / 21 | — |
| Audit P (partly right) | EVENT_COUNTRY 9, EVENT_PLACE 9, NONE 15 | — |
| Acceptance cases passed | 4 / 16 | — |

Acceptance passes: G02 (West Bank), G03 (Kyiv, not Russia), G04 (Tolyatti → Russia country ring), G06 (Black Sea →
region label).

## Why correct locations are lost (all mentions evaluated; 1,142 rejected mentions)

| Cause | Examples | Category |
|---|---|---|
| **No geocoder in the evaluation; gazetteer coverage.** Places the gazetteer doesn't hold are accepted only in locative position, otherwise they count as `NON_PLACE` (465 rejections) | Kaliningrad (D92), Altoona (D127), "Nueva York" (D146), Bosnia-Herzegovina / Banja Luka (D154), Gerusalemme (D151), Strasbourg (G09) | L2 assumes a country-restricted geocoder. Offline, unknown real places are indistinguishable from non-places ("La Liga", "Man City"). An **evaluation limitation**, and a contract dependency |
| **Actor-position rule on country-wide events** (388 rejections overall) | "South Sudan's road to elections" (D286), "Hong Kong national security police arrested…" (D96 / G08), Brazil election (G12) | The country is both the subject and where it happens. L1 as written excludes it, so L4 never fires. A **rule gap** |
| **Headline/lead window** (289 rejections) | Turin only in the body (D228); RAF Fairford (G04b) | L1 restricts to the headline and lead. Some reports state the place later |
| **Ties between countries** (12) | North Korea vs Seoul (G15), multi-country diplomacy | L5 returns NONE. Correct under the contract, but it costs C cases |
| **Non-places still accepted** when written after a preposition | "in La Liga" (G10), "at Man City" (G11) | The locative heuristic treats them as places |

The 3 W cases still wrong and the 21 C cases moved show the same causes: country-subject events, and actor countries
in locative phrasing ("Russia's strike on …").

## Reading

- **Removal works.** The contract's L2 and actor rules remove 97% of wrong stored points: Gaza → Mozambique, West Bank
  → Minneapolis, Palestine → Texas, the attacker-country points.
- **Preservation does not, as implemented and evaluated.** Most of the loss comes from two things:
  1. there is no place resolver beyond the gazetteer;
  2. L1's actor rule has no exception for country-wide events.
- **Not ready** for any runtime wiring or the next gate.

## What a second round needs (each a decision, not applied here)

1. **A place resolver for evaluation:** country-restricted geocoding (Nominatim `countrycodes` and `featuretype`), as
   L2 specifies. That means network calls, with rate limits and caching. **Owner decision:** may the evaluation call
   Nominatim, or should a frozen gazetteer extension (`api`-independent, location-layer only) be built instead?
2. **L1 rule refinement**, which is a contract change. A country that is the headline subject of a country-wide
   occurrence (elections, national security law, protests nationwide) is the event country, not an excluded actor.
   **Owner decision**, because it changes the contract's semantics.
3. **Locative non-place filter:** organisations and clubs after a preposition, via the existing media and institution
   registry. That is a deterministic L1 rule already implied by the contract.

The next evaluation round should be re-frozen with these changes, on the same audit and acceptance cases, and scored
once.
