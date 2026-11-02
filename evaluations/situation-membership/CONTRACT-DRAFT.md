# Situation membership contract: draft (2026-11-02)

**Status: draft for owner review. No runtime change, no migration.** It states what must be true for a Development to
be in a Situation, and what has to be recorded so that the answer can be checked later. It does not choose the final
rule or thresholds; the open decisions are listed at the end.

Evidence: snapshot of 2026-11-02 12:55Z (`evaluations/geolocation/2026-11-02/FREEZE.md`, same file), with
`SituationGrouper.explain` from `main` `44e0357`. Scores below are **recomputed today**: they are not the scores at
join time, which were not stored. That gap is itself finding 4.

## 1. What happens today (code on `main`)

| Path | Rule (`processors/situations/`) |
|---|---|
| **Predefined** | Seeds in `config/situations.yaml` (5: `us-iran`, `russia-ukraine-war`, `eu-china-trade`, `gaza-ceasefire`, `sudan-civil-war`), upserted by slug each run, with title, region, primary actors, keywords |
| **Creation** | Unassigned Developments of the last 7 days whose **principal** actor set (canonical keys) has >= 2 actors and recurs in >= 2 Developments become a new Situation named after the actor set. Exact set recurrence, nothing else (`founder_same_occurrence_hours` off) |
| **Later membership** | An unassigned Development is a candidate for every open Situation it shares >= 1 actor with, at >= 50% of the Situation's actors (100% if it has no principal actors). Its score is the weighted mean of actor coverage 0.5, same region 0.1, cosine to the centroid of the 20 latest members 0.3, and a keyword hit in the title 0.2. It joins at >= 0.6 (0.8 without principals) when 0.1 clear of the runner-up; between 0.4 and the threshold it goes to the arbiter (off). |
| **Permanence** | "Developments already in a situation are never moved." No leave, no supersede; only closing a Situation (retire) |
| **Record** | `events.situation_id` only. No reason, time, run, score or evidence is kept |

## 2. Findings that motivate the contract

1. **Actor overlap is a topic filter, not a storyline test.** Every candidate needs a shared actor, and actor
   coverage carries half the weight. A story that merely names both belligerents scores 0.5 + region 0.1 before any
   content is compared. In `russia-ukraine-war` (26 members), 20 are clearly the war, 3 are borderline and 3 do not
   belong:

   | D | Story | Coverage | Semantic | Keyword | Score | Verdict |
   |---|---|---|---|---|---|---|
   | 959 | Russia to host first Olympic federation world event since the invasion | 1.0 | 0.40 | 0 | 0.65 | not the war: sport diplomacy |
   | 880 | Russian disinformation targets pro-Ukraine candidates ahead of US midterms | 1.0 | 0.64 | 0 | 0.72 | not the war: Russian influence operation in the US |
   | 242 | The price of doing business in Russia | 1.0 | 0.63 | 0 | 0.72 | not the war: economic analysis |
   | 214 | Russia's military spending masks a strategy for a prolonged war | 1.0 | 0.54 | 0 | 0.69 | borderline: analysis about the war |
   | 12 | Poland boosts air defence after "Russian provocations" | 1.0 | 0.78 | 0 | 0.76 | borderline: spillover |
   | 64 | Estonia blames Russia for arson on a supplier to Ukraine | 0.5 | 0.58 | 0 | 0.48 today | borderline: hybrid spillover |
   | 84, 99, 124, 417, 1086 | strikes on Kyiv and civilian targets | 0.5-1.0 | 0.72-0.99 | mostly 1 | 0.59-0.96 | the war |

2. **Broad actor-pair Situations absorb unrelated news.**
   - `russia-united-states` holds Trump on a New York map without Little Italy (D387, 0.86), the Pope's hospital
     visit (D439, 0.81, mentioned-entities fallback), Rubio on Venezuela (D1010) and Western Sahara at the UN (D1145).
   - `china-united-states` holds the Pope on AI doom (D49, 0.95), giant pandas (D34, 0.80), a new White House
     spokeswoman (D542) and media access to the White House (D11).

   The centroid of a broad Situation is broad. Semantic similarity to "US politics" is high for any US politics
   story, so it does not discriminate.
3. **Commentary and analysis join like reports.** D214, D242 and "Can Europe still compete with the US and China?"
   (D112) entered on actor overlap. Nothing distinguishes an occurrence from writing about a topic.
4. **Membership cannot be explained after the fact.** Several members score below the join threshold today or are not
   candidates at all:
   - D64: 0.48;
   - D11: 0.49;
   - D710: 0.42;
   - D1138 (G20 family photo): shares no actor with `russia-united-states` now.

   The centroid moved, the principals changed (Candidate B) and the Situation's members changed. Nothing stored says
   why they joined.
5. **Exact actor-set recurrence creates sound Situations, and some that are not.** It produced
   `afghanistan-taliban` and `canada-european-union`, but also the surname and storm pairs fixed by Candidate B
   (`elon-musk-musk`, `christa-pike-pike`, `rachel-simon`). Creation and later membership need separate contracts:
   creation is about whether a storyline exists, membership about whether one Development is part of it.

## 3. The contract

### 3.1 Definitions

- **Situation:** a persistent geopolitical storyline. Occurrences that share actors in **one conflict, negotiation,
  dispute or process**, so that each one changes the state of that process.
- **Member:** a Development that is an occurrence in that process, or a direct consequence of one, reported as news.
  Sharing actors is necessary for most reasons, but **never sufficient** on its own.

### 3.2 A Development is a member only with an explicit reason

Exactly one primary reason per membership, recorded at the time it is granted:

| Reason | When | Required evidence |
|---|---|---|
| `PREDEFINED_SITUATION` | The Development matches a seeded Situation's scope | The seed's actors (coverage rule), plus at least one **scope signal**: a seed keyword in the title or summary, or an event type or domain listed for the seed (e.g. `military`, `ceasefire_talks` for the war) |
| `EXACT_ACTOR_SET_RECURRENCE` | A founder of a Situation created from a recurring principal actor set | >= 2 founders that are **distinct occurrences** with the same canonical principal actor set (>= 2 actors), within the creation window. The actor keys must pass the actor-hygiene rules (no surname-of-same-person pairs) |
| `CONTINUATION_OF_EXISTING_SITUATION` | A later Development continues an existing Situation | Principal actor coverage per policy, **and** a scope signal (as above, or the Situation's learned domain/type profile), **and** temporal relevance (§3.4), **and** no disqualifier (§3.3) |
| `MANUAL_ASSIGNMENT` | Owner or analyst decision | Who, when, a free-text justification; overrides nothing automatically |
| `ARBITER_CHOICE` | The arbiter settled an ambiguous case (if ever enabled) | Model, prompt version, candidates and their scores |

The scope signal is what is missing today. Actor coverage says *who*; the scope signal says *which process*. A
Development with the right actors but none of the Situation's process markers is not a continuation; it is a
candidate for another Situation or for none.

### 3.3 Disqualifiers (any one blocks automatic membership)

- **Commentary or analysis.** `is_routine_commentary`, analysis or opinion source role, or `concreteness` = `analysis`
  or `commentary`. Such pieces may be **linked** to a Situation as context (§5), not counted as members. Open
  decision D2.
- **Actor present only as a mention.** No principal actors, or the shared actors are only mentioned. Automatic
  membership needs principal actors; the current fallback path (100% coverage, 0.8) is withdrawn for continuation.
  Open decision D3.
- **Incompatible domain.** The Development's domain (or type) is in the Situation's excluded set. Examples: `sport`,
  `culture` or `entertainment` for a war Situation; any domain outside a dispute's declared scope.
- **Incompatible place.** The Development names specific places, and none is in or contained by the Situation's places
  (when the Situation has any). Unknown or country-level places never disqualify, because geocoding is unreliable
  (geolocation audit, 12% wrong).
- **Another Situation fits better.** Another open Situation has a scope signal and the same or better coverage: the
  case is ambiguous and is not assigned automatically.

### 3.4 Temporal relevance

- A Development continues a Situation only if it was first reported within the Situation's **activity window**: since
  the Situation was created, and within `dormant_after_days` of its last member, or of reactivation by a member with
  a scope signal.
- A dormant Situation is woken only by a member that passes the full continuation test, never by actor overlap alone.
- Retrospective pieces (anniversaries, "one year on") are commentary under §3.3.

### 3.5 Actor overlap: its role

- **Necessary** for `EXACT_ACTOR_SET_RECURRENCE` and `CONTINUATION_OF_EXISTING_SITUATION`, on principal actors
  only, canonical keys after the actor-hygiene rules.
- **Not sufficient:** it gates candidacy, and the scope signal decides.
- **Coverage threshold** stays a policy number, but one shared actor of a two-actor pair (50%) should require a
  stronger scope signal than full coverage. Open decision D4.

### 3.6 Creation vs membership

| | Creation | Membership |
|---|---|---|
| Question | Does a new storyline exist? | Is this Development part of an existing storyline? |
| Evidence | Recurrence of a principal actor set across distinct occurrences; actor hygiene; optionally a shared domain among founders | Coverage + scope signal + time + no disqualifier |
| Who | Automatic, or seeded / manual | Automatic, or manual |
| Output | A Situation with **scope**: actors, domains/types, places (optional), keywords | A membership record (§4) |

New automatic Situations should get a **scope profile at creation**: the founders' domains, event types and specific
places. That gives continuation a scope signal for automatic Situations too, not only for seeds.

### 3.7 Leaving and superseding

- **Never silently.** Membership is append-only history. A Development leaves a Situation only through:
  - a **repair** (owner-approved, recorded with a reason, e.g. `RETIRED_SITUATION`, `ACTOR_DEFECT`), as in the
    10-16 repair;
  - a **manual reassignment** (`MANUAL_ASSIGNMENT` to another Situation; the old membership is closed as superseded);
  - a **re-evaluation under a new contract version**: a dry run first, then approval; never automatic in the
    pipeline.
- Development identity changes (merges and splits) carry memberships along. A merge keeps the union, with reasons
  preserved. A split keeps the membership on the part that holds the evidence, or drops it with a recorded reason.
- Pages show current memberships. The history stays queryable.

## 4. Proposed persisted membership record (future; no migration now)

```
situation_memberships
  id                    integer primary key
  situation_id          -> situations.id
  development_id        -> events.id
  reason                text   -- PREDEFINED_SITUATION | EXACT_ACTOR_SET_RECURRENCE | CONTINUATION_OF_EXISTING_SITUATION
                               --  | MANUAL_ASSIGNMENT | ARBITER_CHOICE
  contract_version      text   -- e.g. "membership-v1"
  added_at              datetime
  added_in_run          -> pipeline_runs.id (null for manual)
  evidence_basis        json   -- what passed, at the time:
                               --   {principal_actor_keys, shared_actor_keys, coverage,
                               --    scope_signals: [{kind: keyword|domain|type|place, value}],
                               --    score_components: {actor, region, semantic, keyword}, score, runner_up,
                               --    disqualifiers_checked: [...], founders: [ids] (creation only),
                               --    actor_normalizer_version, centroid_member_ids}
  added_by              text   -- "pipeline" | "repair:<id>" | "owner:<name>"
  removed_at            datetime null
  removed_in_run        -> pipeline_runs.id null
  removal_reason        text null   -- SUPERSEDED | REPAIR:<name> | DEVELOPMENT_MERGED | DEVELOPMENT_SPLIT | MANUAL
  superseded_by         -> situation_memberships.id null
  unique (situation_id, development_id, removed_at)   -- one open membership per pair
```

`events.situation_id` can stay as the denormalised current Situation (at most one open membership per Development,
today's contract) until the pages read memberships directly. The record is the same idea as the membership-
provenance JSONL log already built (`feat/development-membership-provenance`, off): it should be designed together
with that log, not separately.

## 5. Worked examples

**Valid Russia–Ukraine war Development.** D1086 "At least 13 killed in 'horrific' Russian drone strike at Ukraine
train station".
- Principal actors include Russia; Ukraine is the place.
- Scope signals: keyword `drone`, domain `military`.
- Within the active window; no disqualifier.
- **Member: `CONTINUATION_OF_EXISTING_SITUATION`** (or `PREDEFINED_SITUATION`, depending on decision D1).

**Olympic federation story.** D959 "Russia to host first Olympic federation world event since Ukraine invasion".
- Russia and Ukraine are principal, with full coverage.
- No seed keyword; the domain is sport or diplomacy, not military; it is not an occurrence in the war's process.
- **Not a member.** It disqualifies on domain and lacks a scope signal. Today it is in, at 0.65.

**US midterms disinformation story.** D880 "Russian disinformation campaign targets pro-Ukraine candidates ahead of
midterms".
- Russia and Ukraine are present: Ukraine as the topic of the candidates, Russia as the actor.
- The process is a Russian influence operation in US elections.
- **Not a member of `russia-ukraine-war`.** No war scope signal; the target country is the US.
- A candidate for a `russia-united-states` influence storyline, if one exists with that scope, or for none. Today it
  is in the war Situation at 0.72.

**Broad diplomacy.**
- **D387**, Trump on a New York map without Little Italy, in `russia-united-states`. Trump and Russia are only
  co-mentioned; it is not a Russia-US process. **Not a member** (no scope signal; actors not both principal in the
  process).
- **D395**, "Trump announces deal with Putin to release Russian diesel". Both principals, scope signal = trade or
  sanctions. **Member**, if `russia-united-states` is given a scope of sanctions, energy and negotiations.
- **D49**, the Pope on AI, in `china-united-states`. **Not a member.**
- **D1138**, the G20 photo, in `russia-united-states`. No shared principal actor today. **Not a member**, and its
  current membership cannot be explained, because nothing about why it joined was stored.

**Commentary.** D214 (Russia's military spending strategy) and D242 (doing business in Russia). Under §3.3 they are
**linked context, not members**, if decision D2 says so.

## 6. Open decisions (owner)

| # | Decision | Options |
|---|---|---|
| D1 | Does a seeded Situation use its own reason, or is it continuation with a seed scope? | separate `PREDEFINED_SITUATION` / one reason with `seeded: true` |
| D2 | Commentary and analysis: members, linked context, or excluded? | member / linked context (separate relation, not counted) / excluded |
| D3 | Developments without principal actors: allowed to join automatically? | never / only seeded Situations with a strong scope signal |
| D4 | Half coverage (one actor of a pair): what extra evidence? | keyword + domain / specific place / not allowed |
| D5 | Scope profile for automatic Situations: derived from founders, or owner-confirmed? | derived / derived + owner confirm / seeds only |
| D6 | Spillover (Poland air defence, Estonia arson): in the war Situation, a separate spillover Situation, or linked? | member / separate / linked context |
| D7 | Re-evaluation of current memberships under the contract: when, and repair path? | dry run report only / repair per Situation like the 10-16 repair |
| D8 | Is the membership record (§4) one design with the membership-provenance log? | yes (recommended) / separate |

Evaluation before any rule change: a labelled membership set from the current Situations (member / not / borderline
per Development, with the reason). Then a replay of the candidate rule on frozen snapshots, as for the Situation
holdout. No rule is proposed here without that evidence.
