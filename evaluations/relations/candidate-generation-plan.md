# Phase 3 Session 1: candidate generation (pre-registered, 2026-10-09)

Frozen before any candidate was generated or measured. Candidate generation only: no classifier, no acceptance, no
tuning. The rules below come from the taxonomy's evidence requirements (`runtime-contract.md`), not from the gold
cases. They are measured once on relation gold revision 2, development split. The sealed holdout is not opened.

## Unit

A **Development view**: one system Development with its first report time, the text of its member items (title plus
the first 300 characters of each item's body), its principal actors and the places named by its items.

## Rules (`osint_monitor/processors/relation_candidates.py`)

Every pair of distinct Developments is considered once. A pair may yield one candidate per type.

| Type | Proposed when | Max gap between first reports |
|---|---|---|
| `same_calamity_lifecycle` | both texts name a hazard of the **same hazard class** (earthquake, flood, storm, wildfire, landslide, eruption, drought/heat, disease outbreak, haze, tsunami; en / es / it terms) **and** the two Developments name compatible places (same place, or one contains the other; countries allowed) | 7 days |
| `same_convened_event` | both texts name a gathering (summit, visit, talks, conference, meeting, assembly, session, forum; en / es / it) **and** one of: at least 2 shared principal actors; the same named gathering (G7, G20, SCO, BRICS, ASEAN, APEC, NATO, UNGA, COPnn, OPEC); a shared specific (non-country) place | 7 days |
| `reaction_to` | the **later** Development's text has a reaction cue (condemn, denounce, reject, welcome, respond / response, react, slam, criticise, hail, retaliate, protest, "in response"; en / es / it) **and** the two share at least one principal actor; proposed as later = reaction, earlier = trigger | 72 hours |

The lexicons are fixed in code as written above and are not changed during this session.

## Measurement (once, development windows)

Replay: every relation development window with the current code (`evaluations/identity/scripts/replay_current.py`,
fixed clock), written to `runs-rev2/` (the revision 1 replays in `runs/` are left untouched).

Side mapping: a gold side (an item set, `gold/relation-sides-rev2.yaml`) is covered by every system Development
that contains at least one of its items. A scored case is:

- **NOT_SURFACED** when a side has no Development (an unclustered item is not a Development);
- **BLOCKED_BY_IDENTITY** when both sides map only to the same single Development;
- **COVERED** otherwise. A covered canonical positive of a runtime type is **recalled** when a candidate of that
  type exists between a Development of each side (for `reaction_to`, from the reaction side to the trigger side).

Reported, per runtime type:

1. canonical positives: COVERED / BLOCKED_BY_IDENTITY / NOT_SURFACED, and candidate recall on COVERED positives
   (with direction for `reaction_to`);
2. candidate volume: candidates per window, per Development, and the share of all Development pairs;
3. candidates on scored `NO_RELATION` cases, overall and per hard-negative family (`neg_*`,
   `situation_holdout_control`), as information about the classifier's later load; the candidate stage is
   expected to over-generate;
4. reference: candidates on `AMBIGUOUS`, `SAME_DEVELOPMENT_SUSPECTED`, inferred and gold-only-type positives.

No threshold is set and nothing is changed after the measurement in this session.

## Known bias

The gold cases were selected by crude cue and lifecycle lexicons (`README.md` §4) similar in spirit to these rules,
so candidate recall on the development gold is likely optimistic. The sealed holdout was selected by the same rules;
an honest recall estimate needs positives that no lexicon selected (a prospective live window).
