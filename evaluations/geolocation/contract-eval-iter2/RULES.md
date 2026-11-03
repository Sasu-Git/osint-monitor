# Location contract, iteration 2: rule changes (frozen before scoring, 2026-11-03)

Owner instruction (2026-11-03): three changes only, on the approved contract (U1a, U2a, U3a, U4a; U5 deferred; U6b).
Every other rule (L1–L8 as implemented in iteration 1, `62fe91d`) is unchanged. All thresholds and lexicons below are
`PROPOSED`. They were written from the contract text and general vocabulary, not from the evaluation cases, and are
not tuned after scoring.

## Change 1: frozen local gazetteer extension (stands in for L2's geocoder)

- **Source:** GeoNames `cities15000` + `countryInfo.txt`, downloaded once on 2026-11-03 (`../gazetteer-extension/SOURCE.md`).
  No live Nominatim and no network at evaluation time.
- **File:** `osint_monitor/processors/data/place_extension.json`, read only by `event_location.py`. The shared gazetteer
  (`config/geography.yaml`) is unchanged and always wins: a name the gazetteer knows is never looked up in the extension.
- **Use:** a headline or lead mention that the gazetteer does not know, and that the non-place filter (change 2) does
  not reject, is a **specific place** when the extension lists it, in any position (iteration 1 accepted unknown names
  only in locative position).
- **L2 resolution:** the extension gives the candidate countries and populations.
  - When the reports name countries through the gazetteer, only candidates inside them count. If there are none, the
    mention is rejected (`OUTSIDE_NAMED_COUNTRIES`). If several, the most populous wins.
  - When the reports name no country, the most populous candidate is used only when it is dominant (population ≥ 4× the
    next country's). Otherwise the place stays unresolved (no country).
- Then the existing L2 step (one named country → unresolved places lie in it) and L3–L6 apply unchanged.

## Change 2: non-place filter (L1, "a mention the gazetteer and the geocoder both fail to type as a place")

A mention the gazetteer does not know is rejected as `NON_PLACE`, in any position (locative included), when:
1. it contains a word from the frozen lexicon of organisations, competitions and bodies (league, liga, cup, club, FC,
   ministry, government, parliament, council, party, union, agency, bank, university, police, army, airline, …; full
   list in `_NON_PLACE_WORDS`); or
2. it is an institution in the registry (`config/institutions.yaml`) or a media outlet (`ActorNormalizer.is_media`),
   as L1 already specifies; or
3. it ends like a sports club name (City, United, Utd, Rovers, Wanderers, Hotspur, Albion, Athletic) **and** the
   extension does not list it either.

## Change 3: L1 revision, country-wide occurrence in the actor's own country

**Iteration 1 L1 (unchanged part):** a mention in actor position (a principal actor key, not in locative position) is
excluded as a location candidate.

**Revised rule:** such a mention is still excluded as a point or place candidate. But when:
- the mention names a **country** (or a U4 disputed entity);
- the same report's headline or lead states a **country-wide occurrence** (frozen lexicon: election, vote, polls,
  referendum, runoff, protests, unrest, nationwide, national, parliament, law, legislation, constitution, cabinet,
  government, budget, curfew, lockdown, state of emergency, martial law, coup, impeachment, general strike,
  earthquake, floods, wildfire, drought, cyclone, hurricane, blackout, outbreak, inflation, recession, economy, …;
  full list in `_COUNTRY_WIDE`); and
- the headline is **not a statement** (frozen statement-verb lexicon: says, warns, urges, calls on/for, vows,
  threatens, denies, rejects, condemns, accuses, claims, …), so U1 is unchanged: a statement with no stated place
  has no location,

then that country is held as a country-wide candidate. It is used only when **no supported point location exists**:
no specific place, and no other country named as a place. In that case the Development resolves to
`EVENT_COUNTRY` / `COUNTRY_ONLY` for the candidate with the most origins. A tie gives no location (L5).

This implements L4's first bullet ("the occurrence is stated as country-wide: election, nationwide protest, national
legislation"), which iteration 1 could not reach for an actor's own country.
