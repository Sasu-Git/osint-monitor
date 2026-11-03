# Location contract: design options for a possible iteration 3 (2026-11-03)

**Status.** Design only. Nothing implemented or scored. Iteration 2 (`feat/geolocation-contract-iter2` `a73b9f3`,
freeze `a2ef830`) is a recorded negative result and is not patched. Every rule and threshold below is `PROPOSED` and
needs an owner decision (each is a contract change).

**Scope.** Only the five loss classes left open by iteration 2 (`../contract-eval-iter2/RESULTS.md`, "Why C is still
lost"). Of the 45 lost correct points:

| Class | C lost |
|---|---|
| Location only beyond the headline and lead | 13 |
| Place or country ties (L5) | 10 |
| Country named as the place, but the wrong country chosen | 17 (8 + 9) |
| "Congo" ambiguity | 3 |
| Hong Kong containment | 3 |

The remaining 2 (Vatican, Western Sahara ISO mapping) are a harness and U4 issue, outside this note.

## Evaluation caveat (applies to every option)

The 81 C and 94 W audit cases have now been read through two iterations, and their loss lists have been read case by
case. Any iteration-3 rule designed from those lists risks fitting them.

**PROPOSED:**
- Freeze the iteration-3 rules before scoring, as before.
- Score on the existing cases, **and** on a fresh, blind audit sample of newer Developments.
- Treat the fresh sample's result as the deciding one.

## 1. Location beyond the headline and lead (13)

**Cause.** L1's evidence window is the headline and lead only. The event place is stated later in the body.

| Option | Rule (deterministic) | Risk |
|---|---|---|
| 1a. **Dateline** | Parse a wire dateline at the start of the body ("KYIV, Nov 2 (Reuters) –", "GAZA CITY (AP) —"): an uppercase place token before a date or agency marker. It counts as a specific-place mention with headline weight. | The dateline is where the reporter files, not always the event (a Jerusalem dateline for a Gaza strike). Coverage is limited to wire-style copy. Needs the stored body text (`fulltext` stage); items without full text gain nothing. |
| 1b. **Widened window, locative only** | Extend the window to the first N body sentences (PROPOSED N = 3). Accept a mention there only in locative position ("in X", "near X", "X-based" excluded) and only when the headline and lead give no place. | Background places ("after talks in Doha", "the 2022 attack in X") enter. W removal falls. Each extra sentence adds noise. |
| 1c. **Cross-origin agreement** | A body-only place counts only when ≥ 2 independent origins (provenance origin groups, not syndicated copies) mention it in locative position. | Fewer Developments have two independent origins with full text. Recall gain may be small. |

**Recommended combination:** 1a + 1c. 1a's dateline-vs-event risk is bounded by requiring the dateline country to agree with any country the headline names.

## 2. Place or country ties (10)

**Cause.** L5 gives no location when several places or countries are equally supported.

| Option | Rule | Risk |
|---|---|---|
| 2a. **Containment collapse** | When all tied places lie in one country (gazetteer or extension containment), resolve to `COUNTRY_ONLY` for that country instead of none. | Low. Loses nothing that is now correct, because a tie gives no location today. |
| 2b. **Ordered tie-break** | Break the tie on (i) most independent origins, (ii) earliest position in the headline, (iii) locative over bare mention. Still a tie → none. | Two genuine locations (talks in Geneva about Gaza) get one arbitrary winner. W can rise. |
| 2c. **Multi-location output** | Keep all tied places as a list. The map shows no single marker; the feed lists the places. | Display and contract change. The evaluation would need a scoring rule for lists. |

**Recommendation:** 2a alone first. It is the only option with no new wrong-point path. 2b only if the fresh sample shows ties dominate the remaining loss.

## 3. Country named as the place, wrong country chosen (17)

**Cause.** A country mentioned as subject or actor ("Brasile" in a US story, D148; Bosnia's election resolved to Ukraine, D154) outranks, or ties with, the country where the event happens. Ceuta → Spain (D438) is a containment case of the same kind.

| Option | Rule | Risk |
|---|---|---|
| 3a. **Locative-only countries** | A bare country name counts as an event place only in locative position ("in Brazil") or as the container of a resolved specific place. Adjectival and subject mentions ("Brazilian", "US says") never count as place. | Country-wide events phrased without a preposition ("Brazil floods") are lost unless the iteration-2 country-wide lexicon admits them. That couples this rule to that lexicon. |
| 3b. **Container precedence** | When a specific place resolves, its country overrides every bare country mention. | A wrong homonym in the extension propagates (iteration 2: Antigua → Guatemala, D1160). Needs the extension's named-country filter to stay strict. |
| 3c. **Subject/place split by verb frame** | A country that is the grammatical subject of a statement or action verb in the headline ("X says", "X strikes") is an actor, never the place. | Depends on parse quality in three languages. The verb lexicons are hand-built and multilingual. |

**Recommendation:** 3a + 3b. Both are positional and lexicon-light. 3c is the most precise but also the most fragile.

## 4. "Congo" ambiguity (3)

**Cause.** "Congo" resolves to one entry. The Democratic Republic of the Congo (COD) and the Republic of the Congo (COG) are not separated.

| Option | Rule | Risk |
|---|---|---|
| 4a. **Cue lexicon** | Frozen cues decide:<br>• "DR", "DRC", "RDC", "Democratic", Kinshasa, Goma, Bukavu, Kivu, Ituri, M23 → COD<br>• Brazzaville, Pointe-Noire → COG<br>• Bare "Congo" with no cue → no country (not a default). | Small. Some genuine COD stories, which make up most of the volume, lose their country when no cue appears. |
| 4b. Split the shared gazetteer entry | Change `config/geography.yaml`. | **Rejected for this track:** the gazetteer is shared by NER, principals, segmentation and Situations. |

**Recommendation:** 4a, in the location module only.

## 5. Hong Kong containment (3)

**Cause.** The gazetteer files Hong Kong as a city in China. The iteration-2 L1 revision applies only to countries, so
Hong Kong as actor-and-place (D96, D1081, G08) cannot resolve to its own `COUNTRY_ONLY`.

| Option | Rule | Risk |
|---|---|---|
| 5a. **Module-local territory list** | Hong Kong and Macau join U4's disputed/territory set inside the location module. Each is its own `COUNTRY_ONLY` target (HKG/MAC), eligible for the L1 revision. | The location module and the rest of the pipeline disagree: Situations and actors still file Hong Kong under China. The map-only aliases already map HKG and MAC, so the display agrees. |
| 5b. General rule | Any gazetteer place with its own outline in `countries.json` counts as a territory. | Broader. It may pull in other dependent territories nobody reviewed (Gibraltar, Greenland and so on). |

**Recommendation:** 5a, with an explicit two-entry list.

## Expected effect (bound, not a forecast)

- **Upper bound:** if every listed class were fully recovered, C would reach at most about 79/81.
- **Overlap:** the classes overlap, and 1, 2b and 3 can also reintroduce wrong points.
- **Gate:** no option set is claimed to reach the proposed 90% retention.
- **Lowest wrong-point risk:** 2a, 4a and 5a. These are the natural first slice if a smaller iteration is preferred.

## Decisions needed before any iteration 3

1. Which options are in scope:
   - recommended full set: 1a + 1c, 2a, 3a + 3b, 4a, 5a;
   - or the low-risk slice: 2a, 4a, 5a.
2. Whether a fresh blind audit sample is required, and whether it decides (recommended: yes and yes).
3. Whether the frozen evaluation's ISO lookup may be amended **before** scoring for "south sudan" (D286). This is an
   evaluation-harness change, recorded as an amendment, not a rule change.
