# Geolocation quality audit (2026-11-02): findings

Read-only audit of the location stored on every Development, and of the map's placement check that decides
which stored points it shows. No fix is implemented. Inputs and hashes: `FREEZE.md`. Cases: `cases.json`
(168 suppressed + 40 shown, each with the stored place, coordinates, the country the point lies in, the places the
member items mention, source languages, the map's decision, the expected interpretation, the root cause and a
verdict). Counts: `stats.json`.

## How a Development gets its location today

`processors/geocoding.py: geocode_event` counts the LOC / GPE / FAC entities of the Development's items. It sends
the most-mentioned name, as plain text, to Nominatim and **keeps the first result**: no country bias, no type
filter, and no check against the other places mentioned. The result is cached in memory by name, so one bad first
hit repeats for every Development that mentions the name (all 17 Gaza cases share one Mozambique point). The
stored `location_name` is Nominatim's display string. Nothing records which mention was geocoded or when.

The map (`api/geo.py: placement`, deploy-web-20261102) plots a stored point only when the country it lies in is
the country of a most-mentioned place known to the gazetteer, or, failing that, of some mentioned place.

## Numbers (1,198 Developments)

| | Count | Share |
|---|---|---|
| Stored location | 1,166 | 97% |
| No stored location | 32 | 3% |
| **Shown on the map** | 998 | 86% of located |
| of which a whole-country point (no city) | 788 | 79% of shown |
| **Suppressed by the map** | 168 | 14% of located |

**Suppressed (all 168 hand-labelled):**

| Stored verdict | Count | Meaning |
|---|---|---|
| Wrong place (W) | 92 | correctly hidden |
| Partly right / no single place (P) | 31 | correctly hidden (a sea, a continent, several countries) |
| Right place (C) | **45** | **wrongly hidden**: a frontend-side defect |

**Shown (random sample of 40):** 36 right (C), 2 wrong (W), 2 partly right (P).

**Estimates:**

- **Wrong stored points.** 92 suppressed plus about 5% of the 998 shown (2/40 in the sample; with 40 cases the
  true rate could be anywhere from about 1% to 17%), about 50. Together roughly **140 of 1,166, about 12%**, and
  about 80 more that are only partly right.
- **What the map catches.** Of the wrong points, about 92 of ~140 are hidden: **about two thirds caught**.
- **How accurate the hiding is.** 123 of 168 hidden points (73%) deserve to be hidden; **45 (27%) are right points
  hidden** by the check.
- **Precision of shown points.** 79% are whole-country points, which are right but not precise.

## Root causes

Definitions: `AMBIGUOUS_NAME` (the name is another real place, e.g. Gaza, Mozambique); `FIRST_RESULT_WINS`
(the first hit is a street, building or business with that name, e.g. "West Bank", Minneapolis); `REGION_CITY_COLLISION`
(a country or region name hits a town, e.g. Palestine, Texas); `CAPITAL_COUNTRY_CONFUSION` (a capital standing for a
government, or the capital's surroundings); `MISSING_ALIAS` (the gazetteer cannot resolve a correct mention, e.g.
"Riad", "Nueva York", "Strasbourg"); `MISSING_CONTAINMENT` (a correct point in an outline the gazetteer files under
another country: Hong Kong, Vatican, Ceuta); `MULTIPLE_PLACES_NO_DOMINANT_LOCATION` (several countries
mentioned and the most-mentioned is the actor, not the location, e.g. "Russia" in a strike on Kyiv);
`WRONG_COUNTRY_MATCH` (a minor mention geocoded instead of the story's place); `INVALID_STORED_PLACE` (no usable
point). Added during the audit: `NON_PLACE_MENTION` (NER tagged a non-place as a place: "Man City", "La Liga",
"Gobierno", "Marte", "7.49am", "Epirus" the company) and `SUPRANATIONAL_REGION` (a sea, continent or region:
Europe, Africa, Black Sea, Caribbean, Gulf).

| Root cause | Wrong points (W) | Right points wrongly hidden (C) |
|---|---|---|
| NON_PLACE_MENTION | **23** | 0 |
| MULTIPLE_PLACES_NO_DOMINANT_LOCATION | **22** | 12 |
| AMBIGUOUS_NAME | **20** (17 are Gaza -> Mozambique) | 4 ("Congo" -> Republic of the Congo for DR Congo stories) |
| FIRST_RESULT_WINS | **16** (4 are West Bank -> Minneapolis) | 0 |
| SUPRANATIONAL_REGION | 5 (+12 partly right) | 0 |
| WRONG_COUNTRY_MATCH | 3 | 0 |
| REGION_CITY_COLLISION | 3 (Palestine, Texas) | 1 (Georgia, the US state) |
| MISSING_ALIAS | 0 | **22** |
| MISSING_CONTAINMENT | 0 | **6** |

**What the stored errors have in common.** The geocoder asks for a name with no context: no country bias, no
feature-type filter, and no check against the Development's other places. Four causes account for 81 of the 92
wrong points: AMBIGUOUS_NAME, FIRST_RESULT_WINS, REGION_CITY_COLLISION and NON_PLACE_MENTION. In each, any
consistency check against the other mentioned countries, or a restriction to administrative places, would have
refused the hit. The `MULTIPLE_PLACES` errors are different: there the geocoded place is a real place in the
story, but it is the acting country, not where the event happened.

**What the map's check gets wrong.**
- **Missing aliases (22):** Spanish and Italian exonyms ("Riad", "Estambul", "Marsiglia", "Nueva York",
  "Jordania", "Palestina") and cities the gazetteer does not hold (Strasbourg, Assisi, Turin, Nancy, Yerevan,
  Kaliningrad, Altoona).
- **Containment (6):** Hong Kong, Vatican and Ceuta outlines.
- **Actor-dominated mentions (12):** the same multi-country problem as above, seen from the other side.

## Clustering by language, source and place type

- **Language.** Spanish and Italian Developments are hidden more often than English ones. Of located
  Developments whose dominant source language is known: English 13% hidden, Spanish 23%, Italian 19%.
- **Wrong rate by language.** English 7.6%, Spanish 14%, Italian 8%. Spanish suffers most from NON_PLACE_MENTION
  ("Gobierno", "Negros", "Pacifico", "Caribe"), because the English-trained NER tags Spanish common nouns as places.
  261 located Developments come from sources whose language is not declared in `sources.yaml`.
- **Place type.**
  - Names that are both a territory and a town elsewhere: Gaza, Palestine, West Bank, Santiago, Athens, Georgia.
  - Seas and continents: Europe, Africa, Black Sea, Caribbean, Gulf.
  - Organisations and clubs read as places: La Liga, Man City, RB Leipzig, Epirus, MRT, LPU.
- **Repetition.** A single bad hit repeats through the per-name cache: Gaza -> Mozambique 17 times, West Bank ->
  Minneapolis 4, "Negros" -> Philippines 5, "Gobierno" -> Managua 3, Europe -> continent point 7.

## Next likely intervention (not implemented)

Ordered by defects removed per unit of risk:

1. **Contextual geocoding** (pipeline, a semantic change that needs its own gate):
   - restrict Nominatim to administrative places, populated places and natural features (`featuretype`);
   - bias or limit the result to the countries the Development's mentions resolve to (`countrycodes`);
   - reject a hit whose country disagrees with every mentioned country instead of storing it;
   - record which mention was geocoded.

   Expected to remove most AMBIGUOUS_NAME, FIRST_RESULT_WINS and REGION_CITY_COLLISION errors (39 of the 92).
2. **Place-mention hygiene before geocoding:** drop organisation and club names, and common nouns in the source
   language. That is the NER layer, on the same footing as the actor-hygiene work. It targets NON_PLACE_MENTION (23).
3. **Gazetteer aliases and containment** (frontend data only, no pipeline change):
   - exonyms in es/it;
   - the missing cities;
   - Hong Kong, Vatican, Ceuta containment;
   - "Congo" disambiguation.

   This would stop 28 of the 45 right points being hidden. It is the cheapest change and safe to do first.
4. **Event location vs actor country:** choose the location from where-phrases ("in Kyiv", "near Tolyatti")
   rather than the most-mentioned country. Needs design; it is the root of the 34 MULTIPLE_PLACES cases.

Re-geocoding stored Developments is a data repair. Like the actor repairs, it needs its own dry run and approval.
