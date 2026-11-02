# Development location contract: PROPOSED (2026-11-02)

**Status.** Design only. No geocoder, pipeline, schema or frontend change. Every rule here is `PROPOSED` until the owner
approves it.

**Evidence.** The frozen geolocation audit (`evaluations/geolocation/2026-11-02/`, sha-pinned in its `FREEZE.md`;
inputs unchanged, not re-run): 1,166 located Developments; about 12% of stored points wrong; 45 correct points hidden by
the map. Acceptance cases: `acceptance-cases.yaml` (this folder), drawn from its `cases.json`.

## 1. The question

> What real-world location should the map associate with a Development?

**Proposed answer: where the occurrence happened.** The location is the place where the Development's occurrence took
place, as its own reports state it. It is not:
- who did it;
- who reported it;
- the country it concerns.

Everything else is context, kept separately.

## 2. Location roles (the same mention can play different roles in different stories)

| Role | Meaning | Example (audit) | Used as the map location? |
|---|---|---|---|
| **EVENT_PLACE** | specific place where it happened: city, facility, district, admin area | Kyiv bridge struck (D124); Tolyatti factory (D933); Strasbourg plenary (D747) | **yes**: a point |
| **EVENT_COUNTRY** | it happened country-wide, or only the country is stated | French nationwide protests (D626 family); Brazil election (D449 family) | **yes**: a whole-country ring |
| **TARGET** | the place acted upon, when different from the actor's home | "Russia strikes Kyiv" → Kyiv | yes, as the EVENT_PLACE (the target is where it happened) |
| **ACTOR_ORIGIN** | the actor's country | "Russia" in D124; "UK" in the RAF Fairford case (D1006) | **never** |
| **REPORTING_LOCATION** | dateline or where the outlet or speaker is | "reported from Seoul" (D1115); UN in New York (D541) | only when the occurrence is the statement itself (speech, press conference); see U1 |
| **REGION** | a sea, strait, continent or supra-national area | Black Sea (D291); Strait of Hormuz (D1052); Europe (D333) | **no point**: label only (U3) |
| **AMBIGUOUS / NONE** | no defensible place, or conflicting places | multi-country statements; non-place mentions ("La Liga" D654, "Man City" D382) | **no** |

## 3. Proposed deterministic rules

**L1. Candidates** (PROPOSED). Location candidates come only from:
- **occurrence evidence:** report headlines and leads of the Development's occurrence items, not analysis, live blogs or
  roundups;
- **mention types:** NER LOC, GPE or FAC.

Excluded:
- a mention in **actor position** (subject of the headline's main verb, or an actor key under the actor normaliser:
  "Russia strikes …", "UK police arrest …");
- media outlets and organisations, using the existing `ActorNormalizer.is_media` and the institution registry;
- a mention the gazetteer and the geocoder both fail to type as a place.

**L2. Context-constrained resolution** (PROPOSED). A candidate is resolved only inside the countries the Development's
reports name: the containment of the gazetteer, or the geocoder's country restriction. A hit outside every mentioned
country is **rejected, not stored**. This is the single rule that removes:
- Gaza → Mozambique (17 cases);
- West Bank → Minneapolis (4);
- Palestine → Texas (3);
- Athens → Georgia (US).

The result must also be an administrative or populated place, or a named natural feature, not a street, building or
business (this removes all 16 FIRST_RESULT_WINS cases).

**L3. Support** (PROPOSED).
- An EVENT_PLACE needs the place in the headline or lead of **at least one report**, and no conflicting EVENT_PLACE
  with more support.
- **Proposed confidence:**
  - **CONFIRMED_PLACE:** named by ≥ 2 independent provenance origins;
  - **PLACE:** named by 1;
  - **COUNTRY_ONLY:** only a country is supportable;
  - **REGION:** only a region or sea;
  - **NONE.**
- The numbers (≥ 2 origins) are `PROPOSED`.

**L4. Country level** (PROPOSED). EVENT_COUNTRY applies when:
- the occurrence is stated as country-wide (election, nationwide protest, national legislation); or
- every EVENT_PLACE candidate lies in one country but none has support; or
- the reports name only that country as the place of occurrence (not as an actor).

**L5. Several plausible places** (PROPOSED).
- **Same country, all supported** (a strike on Kyiv and Kharkiv): EVENT_COUNTRY plus the list of places as detail.
  No single point (see U2).
- **Different countries, none dominant:** NONE, with the candidate list kept as detail.
- **A place and its container** (Kyiv and Ukraine): the specific place wins.

**L6. No canonical location** (PROPOSED) when:
- there are no candidates after L1;
- every candidate is rejected by L2;
- L5 yields NONE;
- only REGION candidates exist (label only, until U3).

**L7. What to store** (PROPOSED). The chosen role; place name and id; coordinates; confidence class; the mention text;
the supporting item ids and origins; the resolver (gazetteer or geocoder query, plus country restriction); and the
rejected candidates with their reason (`ACTOR_POSITION`, `OUTSIDE_CONTEXT`, `NON_PLACE`, `NOT_ADMINISTRATIVE`,
`CONFLICT`).

**L8. Frontend** (PROPOSED).

| Confidence | Shown as |
|---|---|
| CONFIRMED_PLACE, PLACE | a point (PLACE could be drawn lighter) |
| COUNTRY_ONLY | the hollow ring (today's whole-country marker) |
| REGION, NONE | no marker; the feed shows "No confirmed location", plus the region or the candidate places as text |

The map's present placement check stays as a guard until stored locations follow this contract.

## 4. The "safe" frontend fix: aliases and containment in the country lookup

**It is semantic-neutral only if it stays a frontend-only lookup layer.**
- **Where the lookup gets its names:** the map's `CountryIndex` (`api/geo.py`, deploy-web-20261102) resolves names
  through the **shared** gazetteer (`config/geography.yaml`).
- **Who else reads that gazetteer:**
  - NER (`nlp.py`);
  - principal selection (`principals.py`);
  - entity resolution;
  - institutions;
  - segmentation's place guard (`development_segmentation.places_compatible`);
  - Situation founder places (`situations/grouper.py`, `store.py`).
- **The risk:** adding "Riad", "Nueva York", "Strasbourg" or "Hong Kong ⊂ China" there changes which links segmentation
  cuts and which actors become principals. That is a semantic change needing the identity gates.

**Neutral version** (PROPOSED):
- a separate alias and containment table read only by `CountryIndex` (for example `api/data/place_aliases.json`):
  es/it exonyms, the missing cities from the audit, Hong Kong / Macau → China, Vatican City, Ceuta / Melilla → Spain,
  Congo disambiguation;
- the pipeline never reads it;
- **effect on the frozen audit:** 28 of the 45 wrongly hidden points become visible, and no stored point or
  Development changes;
- **test:** rerun the placement on the frozen `cases.json`. Only C-verdict cases may flip from hidden to shown; no
  W-verdict case may flip.

**Not neutral, and a finding for the gazetteer owner:** the shared alias `america → united states`. "America" in "South
America" or "Latin America" becomes the US (D982, Pope's trip). Changing it changes NER and actor keys, so it is out of
scope here and listed as U5.

## 5. Unresolved product decisions (owner)

| # | Decision | Options | Proposal |
|---|---|---|---|
| U1 | Statements, speeches, press conferences: where are they? | the speaker's location (Moscow, Washington) / no location / the subject's location | the speaker's location only when the report states where it was made; otherwise NONE |
| U2 | Multi-place events in one country: one point or several? | one country ring / one point per place / the "primary" place | country ring plus places listed (L5) |
| U3 | Seas, straits and regions (Black Sea, Hormuz, Europe) | not on the map / a region shape / a representative point | not on the map until region shapes exist; label in the feed |
| U4 | Disputed or occupied territory (West Bank, Crimea, Western Sahara) | the gazetteer's containment / its own entity / follow the outline set (Natural Earth) | its own entity, contained in nothing, compatible with both claimants for matching only |
| U5 | Shared alias `america → united states` | keep / drop / keep for actors only | out of scope here; flag to the gazetteer and NER owner |
| U6 | Should a location ever be re-derived for stored Developments? | new Developments only / backfill with a repair | backfill only as a separately approved repair, with a dry run |

**Stop point.** L1's actor-position rule needs U1, and L5 needs U2. Until they're decided, the contract is not
implementable as written. The rest (L2, L3, L4, L6–L8) does not depend on them.
