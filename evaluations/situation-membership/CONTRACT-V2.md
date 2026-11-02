# Situation membership contract v2: testable form, PROPOSED (2026-11-02)

**Status.** Design only. No runtime, schema or config change. Every decision below is `PROPOSED` until the owner
approves it.

**Builds on.** `CONTRACT-DRAFT.md` (v1, `eval/soak-safe-20261102` `1c3fa7a`). Its evidence is reused, not re-derived:
the 2026-11-02 snapshot (sha `b5bb5728…`), `SituationGrouper.explain` on `main` `44e0357`, and the Situation code on
`main`. The Situation code is unchanged on `19b8754`, which only adds `SECURITY.md`.

**The question it answers.**

> What evidence is sufficient for a Development to enter an existing Situation, and what evidence disqualifies it?

## 1. The rule, in one table (PROPOSED)

**A Development enters an existing open Situation S only when all of these hold:**

| # | Requirement | Evidence | Today |
|---|---|---|---|
| E1 | **Principal actors cover S's actors** | canonical principal keys (after actor hygiene) ⊇ ⌈50%⌉ of S's primary actors | same rule, but mentioned-only actors may also qualify (fallback path) |
| E2 | **Scope match** | at least one of S's scope signals: a seed keyword in the headline or lead; an event type or domain in S's scope set; a specific place inside S's place scope | absent: semantic similarity to the centroid and a keyword are only weighted, not required |
| E3 | **Occurrence evidence** | an occurrence item (REPORT headline, not analysis, roundup or live blog) | absent |
| E4 | **Temporal relevance** | first reported while S is active, or a reactivation that itself passes E1–E3 | partly: dormant Situations wake on any join |
| E5 | **No better Situation** | no other open Situation passes E1–E4 with ≥ the same coverage, or it is handled as ambiguous | partly: runner-up margin on the score |

**Disqualifiers. Any one blocks automatic entry:**

| # | Disqualifier | Code |
|---|---|---|
| X1 | No principal actors (only mentioned entities) | `NO_PRINCIPALS` |
| X2 | Commentary only: every member item is analysis, roundup or live blog, or the Development is routine commentary | `COMMENTARY_ONLY` |
| X3 | Domain outside S's scope set (for example sport or culture for a war) | `OUT_OF_SCOPE_DOMAIN` |
| X4 | A specific place outside S's place scope, with no place inside it (unknown or country-level places never disqualify) | `OUT_OF_SCOPE_PLACE` |
| X5 | Ambiguous between two Situations that both pass | `AMBIGUOUS` |

## 2. The open decisions from v1, resolved as proposals

Each decision is given with its alternatives, real consequences on the snapshot, and the recommendation.

### D1. Seeded Situations: own reason or continuation?
- **Alternatives:**
  - (a) a separate `PREDEFINED_SITUATION` reason;
  - (b) continuation with `seeded: true` in the evidence.
- **Consequence:** none for decisions. It matters for reporting, which must distinguish seeded scope (owner-written)
  from derived scope.
- **PROPOSED:** (b). One reason, `CONTINUATION`, with `scope_source: seed | derived | manual`. Fewer codes, same audit
  value.

### D2. Commentary and analysis
- **Alternatives:**
  - (a) members;
  - (b) linked context, a separate relation that is not counted;
  - (c) excluded.
- **Real cases on the snapshot:**
  - D214 "Russia's military spending masks a longer-term strategy" (in `russia-ukraine-war`);
  - D242 "The price of doing business in Russia" (in `russia-ukraine-war`);
  - D112 "Can Europe still compete with the US and China?" (in `china-united-states`).

  Under (a) these stay members and widen the centroid, which pulls in more off-scope items. Under (c) the reader loses
  useful context on the Situation page.
- **PROPOSED:** (b). Commentary is linked to at most one Situation as context. It is shown under "Analysis" on the
  page, and is never a member, never used in the centroid, and never used for reactivation.
- **Dependency:** X2 needs a Development-level commentary test. The existing `headline_kind` per item and
  `is_routine_commentary` per Development exist. "All items commentary" is deterministic.

### D3. Developments without principal actors
- **Alternatives:**
  - (a) never join automatically;
  - (b) join seeded Situations only, with a strong scope signal.
- **Real cases:**
  - D439 "El Papa llega al hospital Gemelli …" joined `russia-united-states` at 0.81 on mentioned entities;
  - D399 (Italian, Zelensky) and D712 (deportation of Ukrainians from the US) joined `russia-united-states`;
  - D858 (China's offshore tax crackdown) joined `china-united-states`;
  - D1084 (Trump and the Alaska ballot) joined `democrat-united-states`.

  Most of these are wrong or doubtful. The fallback path (100% coverage of mentioned entities, 0.8) is how
  broad actor-pair Situations absorb unrelated stories.
- **PROPOSED:** (a). Such a Development stays outside Situations until it gains principals, or the owner assigns it
  (`MANUAL`).

### D4. Half coverage (one actor of a pair)
- **Alternatives:**
  - (a) allowed with E2;
  - (b) allowed with E2 plus a specific place in scope;
  - (c) not allowed.
- **Real cases:**
  - D1086 "13 killed in Russian drone strike at Ukraine train station" (principal "Russia" only, 0.5): a true member;
  - D303 "Yandex data centre hit by drone" (0.5): a true member;
  - D1147 "US approves sale of 500 Patriot missiles to Ukraine" (0.5, in `russia-united-states`): wrong Situation;
  - D710 "Rubio visits India" (0.5, in `russia-united-states`): not a member.
- **PROPOSED:** (b). At half coverage, require E2 **and** a specific place in scope. D1086 and D303 pass (Ukraine and
  Russia places in the war's scope). D1147 and D710 fail.

### D5. Scope of automatic actor-pair Situations
- **Alternatives:**
  - (a) derived from the founders at creation (domains, event types, specific places) and frozen;
  - (b) derived, then owner-confirmed;
  - (c) seeds only have scope; automatic Situations have none.
- **Real case:** `russia-united-states` (created 10-07) holds sanctions and energy deals (D395, D884: true), but also
  Little Italy (D387), the Pope (D439), Rubio on Venezuela (D1010) and Western Sahara (D1145). That happens because it
  has no scope. Under (c) it keeps absorbing.
- **PROPOSED:** (a), with an owner override in `situations.yaml`.
  - The scope is the founders' domains, event types and specific places at creation, frozen like the occurrence core.
  - **Preserving scope:** it never widens automatically. A member outside it is rejected (X3, X4) even if the actors
    match.
  - Widening is an owner edit to the Situation's entry (an `override` block), recorded with a date.
- **Open sub-point:** does "domain" come from the classifier (rules backend)? Its reliability is unmeasured for this
  use. See the evaluation design.

### D6. Spillover
- **Real cases:**
  - D12 "Poland boosts air defence after Russian provocations";
  - D64 "Estonia blames Russia for arson on a supplier to Ukraine";
  - D811 "German military raises sabotage threat level".
- **Alternatives:**
  - (a) members of the war;
  - (b) a separate spillover Situation (for example `russia-nato-hybrid`);
  - (c) linked context.
- **Consequence:** under (a) every European security story with Russia joins the war Situation. Under (b) the actor
  pair Russia + Poland, Estonia or Germany founds separate small Situations through exact-set recurrence, which already
  happens: `nato-russia` and `european-union-russia` exist.
- **PROPOSED:** (b), through the normal creation rule. This needs no special case. Under E2/X4 the war's place scope
  is Ukraine and Russia, so spillover fails it.

### D7. Re-evaluating today's memberships
- **PROPOSED:** report-only dry run under the approved contract first. Any change to stored memberships is a
  per-Situation repair with its own approval and backup, as in the 10-16 repair. No automatic re-evaluation in the
  pipeline.

### D8. Provenance infrastructure
- **Existing:** the Development-membership decision log (`feat/development-membership-provenance` `a835815`,
  `core/membership_log.py`): JSONL, off by default, one record per identity decision. Its fields are item-level
  (supporting members, cosines, override, places).
- **Alternatives:**
  - (a) the same log, new record kind;
  - (b) a separate log;
  - (c) a persisted table now.
- **PROPOSED:** (a) for observation (`kind: situation_membership`, same writer, rotation and off-by-default switch),
  then a persisted `situation_memberships` table (v1 §4) only when membership must be queryable and auditable on
  pages. Shared writer and rotation; distinct record shape (below).

## 3. Reason codes and the record (PROPOSED)

**Entry reasons:** `CONTINUATION` (with `scope_source`), `EXACT_ACTOR_SET_RECURRENCE` (founders), `MANUAL`,
`ARBITER_CHOICE` (only if the arbiter is ever enabled).

**Rejection reasons:** `NO_SHARED_ACTORS`, `LOW_COVERAGE`, `NO_SCOPE_SIGNAL`, `NO_PRINCIPALS`, `COMMENTARY_ONLY`,
`OUT_OF_SCOPE_DOMAIN`, `OUT_OF_SCOPE_PLACE`, `NOT_ACTIVE`, `AMBIGUOUS`.

**Exit reasons** (a repair or owner action only): `SUPERSEDED`, `REPAIR:<name>`, `DEVELOPMENT_MERGED`,
`DEVELOPMENT_SPLIT`, `MANUAL`.

**Decision record** (JSONL, same writer as the membership log). Fields:
- identity: `at`, `run_id`, `kind: situation_membership`, `development_id`, `situation_slug`;
- decision: `decision` (`entered | rejected | linked_context`), `reason`, `contract_version`;
- evidence:
  - actors: `principal_keys`, `shared_keys`, `coverage`;
  - scope: `scope_signals` [{`kind`: keyword|domain|type|place, `value`}], `scope_source`;
  - place and occurrence: `place_check`, `occurrence_items`;
  - ranking: `runner_up`, `score_components` (if still computed);
- creation only: `founders`.

**Persisted membership** (future, when needed): as v1 §4, plus `scope_snapshot` (the Situation's scope at entry time),
so later scope edits don't rewrite history.

## 4. Future evaluation set (design only; not built, not scored)

**Population and sampling.** Every current member of every open Situation on a frozen snapshot (about 190), plus
near-miss candidates that today's grouper scores in 0.4–0.6 without joining. Sampled per Situation so that broad pairs
(`russia-united-states`, `china-united-states`) and seeds (`russia-ukraine-war`, `us-iran`) are all represented.

**Labels (owner, blind to the rule's outcome):**
- for each (Development, Situation): `MEMBER`, `CONTEXT` (commentary), `SPILLOVER`, `OTHER_SITUATION`, `NOT_MEMBER`,
  `AMBIGUOUS`;
- each with a one-line reason;
- for each automatic Situation: its intended scope (domains or types and places) as the owner sees it. This tests
  D5's derived scope.

**Seed cases (from v1 and the snapshot):**

| Group | Cases |
|---|---|
| Positive | D84, D99, D124, D417, D1086, D303 (war); D395, D884 (Russia–US energy/sanctions); D2, D497 (China–US summit, trade) |
| Negative | D959 (Olympics), D880 (US midterms disinformation), D387 (Little Italy), D439 (Pope), D49 (Pope on AI), D34 (pandas), D542 (spokeswoman), D1010 (Venezuela), D1145 (Western Sahara), D1138 (G20 photo) |
| Boundary | D12, D64, D811 (spillover); D214, D242, D112 (commentary); D1147 (Patriots to Ukraine: war or US–Russia?); D710 (Rubio in India); D188 (FBI arrests a Chinese agent in LA: China–US?) |

**Reported metrics (no composite):**
- precision and recall of `MEMBER` per Situation;
- members kept;
- off-scope members rejected;
- ambiguous rate;
- the share of decisions whose evidence record alone explains the label (auditability).

**Proposed gates (`PROPOSED`, to be fixed in the preregistration, not here):**
- ≥ 90% of owner-`MEMBER` kept;
- ≥ 70% of owner-`NOT_MEMBER` rejected;
- 0 seeded-Situation regressions on the positive seed cases.

**Order:**
1. owner decisions on D2–D6;
2. preregistration with frozen labels;
3. replay on frozen snapshots;
4. only then any runtime change.

## 5. Owner decisions needed

D2 (commentary), D3 (no principals), D4 (half coverage), D5 (scope of automatic Situations) and D6 (spillover) each
change which Developments enter Situations, so they are product decisions. D1, D7 and D8 are recommendations with no
semantic consequence beyond reporting and infrastructure.
