# Track: event-location and place-role extraction (opened 2026-11-11)

**Why.**
- Situation v2 needs an event country for single-party and hazard Situations, and in-scope places for scope signals.
  On the 2026-11-02 snapshot, 58% of Developments have no event country.
- Geolocation iteration 3 (closed as a negative result, `4e0ffb9`) showed that rules over the pooled places of a
  Development cannot recover where the occurrence happened. Members legitimately name launch sites, targets,
  reporting venues, datelines and analysis subjects.
- The owner's gold already encodes role decisions: a strike is located at its impact, not its launch site.

**Owner constraints.**
- No more map heuristics in the iteration-3 rule family.
- Structured extraction at the Development level.
- Upstream of Situation membership.
- Independent of actor geography: a place is not an actor, and an actor's country is not the event location.

## Goal

1. **Per item**, the places the text names, each with a **role**:
   - occurrence: where it happened;
   - target or impact;
   - origin or launch;
   - venue: a meeting or statement location;
   - dateline or reporting location;
   - mentioned only.
2. **Per Development**, an **event location** (place, country, confidence) chosen from the occurrence and target roles
   across members, with an explicit `NONE` for the occurrence-less (statements without venue, sea or global, multi-
   country).
3. Containment for regions and seas, as a property of the place, not of the Situation: what the 86 parent entries
   (`fix/v2-upstream-places`) did for oblasts. The 93 parked aliases get a containment-only path here, so they never
   feed actor or entity resolution.

## Constraints

- Local, offline, deterministic, as the topic track (no API keys on the VM).
- Candidates:
  - dependency roles around location mentions (prepositions, verbs of attack, meeting and statement);
  - dateline detection;
  - a learned role tagger only if the rule-plus-parse baseline is measured first.
- Must not change the deployed map until it beats it on the frozen gold.

## Evaluation

1. **Reuse** the frozen 100-case geolocation gold (`iter3-sample`, owner labels, `labels-freeze.json`) for the event
   country. It is development evidence now: iteration 3 already scored on it.
2. **New blind gold** for acceptance:
   - about 150 Developments from a fresh VM snapshot, drawn after this track's spec is frozen;
   - owner labels: event country, event place, and per-item place roles for a 50-Development subset;
   - stratified by language, with strike / attack stories oversampled (the role-sensitive class).
3. **Metrics, frozen before scoring:**
   - agreement with the gold event country (blind first answers primary, as before);
   - `NONE` precision;
   - role accuracy;
   - the deployed map (`d06af11`) as the baseline to beat on both label bases.

## First steps

1. `SPEC.md`: the role enum, the event-location decision procedure, and the `NONE` cases (from the owner's iteration-3
   rulings); owner review.
2. Containment-only path for the 93 aliases, with identity gates.
3. Gold sample design and freeze.

Not started beyond this charter.
