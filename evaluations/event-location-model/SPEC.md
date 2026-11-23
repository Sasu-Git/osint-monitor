# SPEC (FROZEN 2026-11-23, owner rulings applied): event location and place roles

**Status.** Frozen 2026-11-23 with the owner's P/T/L rulings (`docs/upstream/DECISIONS.md`). Nothing implemented yet. Changes after this point are dated amendments; amendments after the acceptance gold is frozen void that gold. Items marked APPROVED 2026-11-23 refer to
`docs/upstream/DECISIONS.md` on `design/upstream-representation` (`b3ed3ef`). No map heuristics (owner, 2026-11-11):
the iteration-3 rule family is closed; this is per-item role extraction, independent of actor geography.

## 1. Output

**Per item**, each place mention with:

| Field | Meaning |
|---|---|
| `place` | gazetteer-canonical name, or the surface form when unknown |
| `role` | `event` (where it happened) · `target` (where an attack/measure lands) · `origin` (launch / departure) · `actor_location` (where an actor is based, "Tehran says") · `venue` (meeting/statement location) · `reporting` (dateline, "reports from") · `mentioned` |
| `container` | administrative containment chain (city → region → country), from the containment-only table (L6) |
| `region_or_sea` | set when the place is a sea, strait, or multi-country region (no country) |
| `disputed` | true for disputed territories (L4) |

**Per Development:**

| Field | Meaning |
|---|---|
| `event_location` | one place (event or target role) or null (L1, L2) |
| `event_country` | its country, or null for seas/regions/disputed |
| `target_location` | target-role place when distinct from the event location |
| `origin_location` | origin-role place, stored, never the event location for attacks (L2, `ALREADY FROZEN`) |
| `actor_location` | where acting parties are based (never used as event location) |
| `reporting_location` | datelines / reporting venue (never used as event location) |
| `confidence` | `high` · `medium` · `low` · `abstain` |
| `abstain_reason` | `NO_OCCURRENCE_PLACE` (statements without venue) · `MULTI` (occurrence places in several countries, L1) · `NO_TARGET` (launch reported, no target, L2) · `SEA_OR_REGION` (location is a sea/region, country null, L5) · `DISPUTED` (L4) · `LOW_EVIDENCE` (L8) · `MIXED` (mixed Development, M1) |

## 2. Role rules (parse-based, en/es/it)

- `event`: place governed by a locative preposition of the main occurrence clause ("in Kharkiv", "en Gaza",
  "a Kiev"), or a country-wide occurrence statement (L3).
- `target`: object/oblique of an attack or coercive action ("strike on Medina", "ataque contra", "attacco su").
- `origin`: source of a launch or departure ("fired from Yemen", "lanzado desde").
- `actor_location`: a capital/seat as the subject of a statement ("Tehran says") — already an actor via `represents`
  (`ALREADY FROZEN`); never an event location.
- `venue`: location of a meeting or statement ("talks in Geneva").
- `reporting`: datelines and "reporting from" — stripped from event evidence.
- `mentioned`: everything else.

## 3. Development event location (selection)

1. Candidates: `event` and `target` roles from report items (analysis items excluded).
2. Several valid locations: L1 (APPROVED 2026-11-23: one location, `MULTI` when countries differ).
3. Attacks: target over origin (`ALREADY FROZEN`, owner 2026-11-10).
4. Country-only: L3 (APPROVED 2026-11-23: valid only for stated country-wide occurrences;
   coercive measures get no location — their target is a role).
5. Seas/regions: L5 (APPROVED 2026-11-23: valid location with `event_country=null`).
6. Disputed: L4 (APPROVED 2026-11-23: own entity, `disputed=true`, never assigned to a state).
7. Evidence scope: L7 (APPROVED 2026-11-23: headline + lead first).
8. Minimum evidence: L8 (APPROVED 2026-11-23: one role in one report headline for single-item
   Developments, the same or a contained place in ≥ 2 items otherwise).
9. Mixed Developments: largest compatible component only (M1).

## 4. Containment

- Containment-only table (L6, APPROVED 2026-11-23; recommended): the 86 parent entries already gated
  (`fix/v2-upstream-places` `aa1d5a2`) plus the 93 parked aliases, read only by location and scope — never by actor
  or entity resolution, so Development identity cannot change.
- Seas, straits and multi-country regions are first-class places with no country (Black Sea, Strait of Hormuz,
  Middle East).

## 5. Relation to existing outputs

- The deployed map (`geocoding.py`) is unchanged until this model beats it on the frozen gold on both label bases.
- Actor geography (an actor's country) is never used as event location.
- Situation v2 consumes `event_country`, `event_location` and role-tagged places for scope signals.

## 6. Evaluation

1. Spec approved; decisions L1, L3–L8 taken.
2. Development evidence: the frozen 100-case geolocation gold (`iter3-sample`, owner labels) — already scored by
   iteration 3, so development only.
3. Acceptance gold, blind, from a fresh VM snapshot drawn after the spec is frozen: ~150 Developments (event country,
   event place; per-item roles on a 50-Development subset), stratified by language, strikes/attacks oversampled.
4. Frozen before scoring: agreement with gold event country (blind first answers primary), `NONE` precision, role
   accuracy, baseline = deployed map `d06af11` on both label bases. Evaluation runs via `eval-worker`.
