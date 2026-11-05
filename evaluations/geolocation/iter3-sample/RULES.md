# Iteration 3 rules (implemented 2026-11-05; not scored)

**Base.** Iteration 2 (`a73b9f3`), including its frozen gazetteer extension `place_extension.json`, which is
unchanged (owner ruling 2026-11-05). The extension's known bad exonyms ("nueva york", "marsiglia") stay in it, so
the experiment is not contaminated. The map-only alias branch is a separate frontend concern.

**Selection (owner, 2026-11-05).** 2a, 3a, 4a and 5a from `../iter3-design/DESIGN.md`. Not implemented: 1a, 1b, 1c,
2b, 2c, 3b, 3c, 4b, 5b.

**Switching.** `decide(..., rules=...)` takes any subset of `{"2a", "3a", "4a", "5a"}`. With none, `decide()` is
iteration 2 unchanged; this was checked against iteration 2's frozen `results.json` before any iteration-3 scoring.
Each rule is scored on its own and all four together.

| Rule | Behaviour in `osint_monitor/processors/event_location.py` |
|---|---|
| 2a containment collapse | The leading specific places tie on origins, and all of them lie in one country (gazetteer or extension containment). The result is `EVENT_COUNTRY` / `COUNTRY_ONLY` for that country instead of `NONE`. |
| 3a locative-only countries | A bare country mention counts as the event place only when it is in locative position in the headline, or when its headline or lead states a country-wide occurrence. That uses iteration 2's frozen `_COUNTRY_WIDE` lexicon and excludes statements (`_STATEMENT`); this is the coupling the design names. Other country mentions are rejected as `COUNTRY_NOT_LOCATIVE`. They still count as countries the reports name for L2 (they bound where an unknown or extension place can lie). |
| 4a Congo cues | A bare "Congo" / "the Congo" is decided by the frozen cue lexicon over the Development's occurrence headlines and leads, in the actor branch as well. |
| 5a territories | Hong Kong and Macau are their own country-level entity, like U4's disputed list (the explicit two-entry list). A gazetteer place inside one (for example Kowloon) belongs to it. The shared gazetteer is unchanged. |

**4a cue lexicon.**
- **COD:** `DR`, `DRC`, `RDC`, `M23` (case-sensitive), or `democratic`, `kinshasa`, `goma`, `bukavu`, `kivu`, `ituri`
  (case-insensitive, whole word).
- **COG:** `brazzaville`, `pointe-noire`.
- **Decision:** exactly one side's cues present decides. None or both gives no country (`AMBIGUOUS_CONGO`).
- **Known limit, as designed:** "Democratic" does not match Italian or Spanish "Democratica" / "Democrática".

**Not frozen yet.** The scoring rule, the gold labels and the country lookup are frozen later, in that order and
before the single scoring run (`FREEZE.md`, "Order from here").
