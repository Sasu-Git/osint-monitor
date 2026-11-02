# Situation membership evaluation set: preregistration (2026-11-02)

**Status.** Built, frozen, **not labelled, not scored.** Implements the design of `../CONTRACT-V2.md` section 4.
Scoring requires (1) owner labels frozen with `labels_tool.py freeze` and (2) a **separate owner approval to score**,
passed to `score.py --approval`. Neither exists yet. The gates below are **PROPOSED**, pending owner approval.

## 1. Population

Source: the frozen 2026-11-02 snapshot (sha256 `b5bb5728ce76d3eb28c70712b088b026268538243f4fa099744856dc2c29af40`),
opened read-only. Runtime code and config: `main`-line code at `38ffb79` (no runtime change on this branch).

A case is one (Development, Situation) pair. Three origins:

| Origin | Definition |
|---|---|
| `member` | every current member of every open Situation (status `active` or `dormant`; the 3 closed/retired Situations are excluded) |
| `near_miss` | an unassigned Development (`situation_id` null) that today's grouper scores in **[0.4, 0.6)** against an open Situation: `SituationGrouper().explain(signature_for_event(e), profile)` with profiles from `load_profiles`, `candidate` true and `0.4 <= score < 0.6` |
| `seed` | the 29 seed cases of CONTRACT-V2 section 4, each paired with its current Situation (all 29 are current members of an open Situation on the snapshot, so none needed the candidate fallback) |

A pair qualifying under several origins appears once; its origin is `seed` > `member` > `near_miss`, and the key keeps
every origin it qualifies under. A Development may appear in more than one case (near-miss against several Situations).

## 2. Sampling

- Seed: `20261102` (`random.Random`); case order is shuffled with `20261103`; case ids `S001..S379` follow the shuffle.
- Members and seeds: all, no sampling.
- Near-misses: 1,006 unassigned Developments were scanned against the 28 open Situations; 763 pairs fell in the band.
  Per Situation, all are kept if 10 or fewer, otherwise 10 are drawn without replacement (sorted ids, seeded draw).
  This keeps the broad actor pairs (`russia-united-states` 119 in band, `china-united-states` 127) and the seeds
  (`russia-ukraine-war`, `us-iran`) all represented without letting them dominate.
- The build is deterministic: re-running it on the snapshot produced byte-identical `cases.json`, `key.json`,
  `scopes.json` and `owner-labels.yaml` (outputs are written with LF line endings on every platform).
- Scores are today's: the Situation centroid is computed from the snapshot's current members, not the members at the
  time each Development arrived.

## 3. Counts

**Total: 379 cases**, 346 distinct Developments (31 appear in more than one case), 28 open Situations
(5 seeded with 101 cases, 23 automatic with 278 cases).

| Origin | Cases |
|---|---|
| member | 163 |
| seed | 29 (positive 10, negative 10, boundary 9; all current members) |
| near_miss | 187 (180 with principal actors, 7 on the mentioned-entities fallback) |

Current members in the set: 192 (163 `member` + 29 `seed`).

| Situation | Kind | member | seed | near_miss | in band (population) | cases |
|---|---|---|---|---|---|---|
| `russia-ukraine-war` | seeded | 14 | 12 | 10 | 35 | 36 |
| `russia-united-states` | automatic | 16 | 10 | 10 | 119 | 36 |
| `china-united-states` | automatic | 13 | 7 | 10 | 127 | 30 |
| `israel-palestine` | automatic | 18 | 0 | 10 | 19 | 28 |
| `us-iran` | seeded | 17 | 0 | 10 | 41 | 27 |
| `gaza-ceasefire` | seeded | 9 | 0 | 10 | 19 | 19 |
| `china-taiwan` | automatic | 8 | 0 | 10 | 27 | 18 |
| `donald-j-trump-united-states` | automatic | 7 | 0 | 10 | 83 | 17 |
| `european-union-russia` | automatic | 6 | 0 | 10 | 38 | 16 |
| `eu-china-trade` | seeded | 4 | 0 | 10 | 23 | 14 |
| `democrat-united-states` | automatic | 3 | 0 | 10 | 41 | 13 |
| `nato-russia` | automatic | 3 | 0 | 10 | 30 | 13 |
| `canada-european-union` | automatic | 2 | 0 | 10 | 22 | 12 |
| `china-chinas-long-march` | automatic | 2 | 0 | 10 | 27 | 12 |
| `eritrea-ethiopia` | automatic | 9 | 0 | 3 | 3 | 12 |
| `france-pope` | automatic | 2 | 0 | 10 | 21 | 12 |
| `international-criminal-court-united-states` | automatic | 2 | 0 | 10 | 37 | 12 |
| `mexico-united-states` | automatic | 2 | 0 | 10 | 37 | 12 |
| `christa-pike-pike` | automatic | 3 | 0 | 3 | 3 | 6 |
| `elon-musk-musk` | automatic | 5 | 0 | 1 | 1 | 6 |
| `malaysia-singapore` | automatic | 3 | 0 | 3 | 3 | 6 |
| `sudan-civil-war` | seeded | 2 | 0 | 3 | 3 | 5 |
| `javier-milei-milei` | automatic | 2 | 0 | 2 | 2 | 4 |
| `afghanistan-taliban` | automatic | 2 | 0 | 1 | 1 | 3 |
| `bukele-el-salvador-nayib-bukele` | automatic | 3 | 0 | 0 | 0 | 3 |
| `emmanuel-macron-france-macron` | automatic | 2 | 0 | 1 | 1 | 3 |
| `machado-maria-corina-machado` | automatic | 2 | 0 | 0 | 0 | 2 |
| `rachel-simon` | automatic | 2 | 0 | 0 | 0 | 2 |

## 4. Files

| File | Blind? | Content |
|---|---|---|
| `cases.json` | blind | per case: case id; the Situation as a reviewer sees it (slug, title, seeded/automatic, primary actors, description, region); the Development (id, headline, summary, first reported, principal actors, other mentioned actors, domain, event type, region, up to 8 report headlines with source and time, report count). No score, no membership flag, no origin, no seed group |
| `key.json` | **sealed** | per case: development, Situation, origin(s), seed group, current membership, the Development's current Situation, today's full `explain` output; counts. Not opened until `LABELS-FREEZE.json` exists |
| `scopes.json` | derived facts | each automatic open Situation's founders (derived, see the file's `founder_derivation`) and their domains, event types and specific places; each seeded Situation's given scope from `config/situations.yaml` |
| `owner-labels.yaml` | template | one entry per case (`label`, `reason`, `reviewer` all null) and one `situation_scopes` entry per automatic Situation (`domains_or_types`, `places`, `note`, `reviewer` all null) |
| `build_evalset.py`, `labels_tool.py`, `score.py` | | build, validate/freeze, score (scoring not run) |

## 5. Labels (copied from CONTRACT-V2 section 4, unchanged)

> **Labels (owner, blind to the rule's outcome):**
> - for each (Development, Situation): `MEMBER`, `CONTEXT` (commentary), `SPILLOVER`, `OTHER_SITUATION`, `NOT_MEMBER`,
>   `AMBIGUOUS`;
> - each with a one-line reason;
> - for each automatic Situation: its intended scope (domains or types and places) as the owner sees it. This tests
>   D5's derived scope.

The owner rulings of 2026-11-02 (CONTRACT-V2, top) apply as decided: commentary is linked context, not a member (D2);
spillover belongs to its own Situations (D6); automatic Situations have a scope derived from their founders that only
the owner widens (D5).

## 6. Reviewer instructions (blind)

1. Open only `cases.json`, `scopes.json` and `owner-labels.yaml`. Do not open `key.json`, the grouper's output, or the
   Situation pages of the live system; they reveal current membership.
2. Before labelling cases, fill `situation_scopes` in `owner-labels.yaml` for every automatic Situation: the domains or
   event types and the places you intend it to cover (lists; an empty list is allowed), with an optional note and your
   name. `scopes.json` shows what its founders looked like; it is evidence, not the answer.
3. For each case, read the Situation and the Development (headline, summary, report headlines, actors) and set `label`
   to exactly one of the six labels in section 5, `reason` to one line, and `reviewer` to your name. Judge the pair as
   it is shown; the same Development may appear with another Situation in another case, and each pair is judged on
   its own.
4. Do not add labels, fields or cases. Do not edit `cases.json`, `key.json`, `scopes.json` or the scripts.
5. Run `python labels_tool.py validate`; when valid, `python labels_tool.py freeze` writes `LABELS-FREEZE.json`. A
   freeze is never overwritten.

## 7. Metrics (CONTRACT-V2 section 4; no composite)

Reported per system (today's runtime = stored membership; a future candidate rule through the hook in `score.py`),
overall and per Situation:
- precision and recall of `MEMBER` (owner-`AMBIGUOUS` cases excluded and reported separately);
- members kept (owner-`MEMBER` cases the system keeps);
- off-scope members rejected (owner-`NOT_MEMBER` cases the system does not enter), and the same rate for `CONTEXT`,
  `SPILLOVER` and `OTHER_SITUATION`;
- ambiguous rate (owner `AMBIGUOUS`; for a candidate also its own `AMBIGUOUS` decisions);
- auditability: for a candidate, the share of decisions carrying a reason code and an evidence record. Whether the
  record alone explains the label is a reviewer judgement and is not computed by `score.py`.
- positive-seed regressions (positive seed cases the system does not enter), all and seeded-Situation subset.

## 8. Gates: PROPOSED, pending owner approval

Exactly as in CONTRACT-V2 section 4, **PROPOSED** (not approved):
- ≥ 90% of owner-`MEMBER` kept;
- ≥ 70% of owner-`NOT_MEMBER` rejected;
- 0 seeded-Situation regressions on the positive seed cases.

`score.py` reports each gate's value next to its threshold and labels them PROPOSED. Open point for approval: whether
the third gate counts all 10 positive seeds or only the 6 in seeded Situations (`score.py` reports both).

## 9. Order and approvals

1. Owner fills and freezes the labels (`LABELS-FREEZE.json`).
2. Owner approves the gates (this section's PROPOSED values or amended ones, recorded with a date) and separately
   approves scoring.
3. Only then `score.py --approval "<who, when>"`. No runtime change follows from this set without its own approval.

## 10. Known limitations

- Founders of automatic Situations are not stored; they are derived (members first reported at or before the
  Situation's `created_at`, preferring those whose principal actor set equals the Situation's). For `eritrea-ethiopia`
  no member has that exact set today, so all its pre-creation members are listed (flagged in `scopes.json`).
- Domains and event types come from the rules classifier, whose reliability for scope is unmeasured (CONTRACT-V2 D5).
- A Development that appears in more than one case is, by construction, a near-miss for at least one of them.
- Near-miss scores use today's centroids, not those at arrival time.
