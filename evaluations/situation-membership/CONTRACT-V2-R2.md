# Situation membership contract v2, revision 2 (2026-11-10): PROPOSED

**Status.** Design only. No runtime, schema or config change. Supersedes nothing yet: `CONTRACT-V2.md` stays the
record of the 2026-11-02 rulings. This revision keeps those rulings unchanged and adds what the 126-case diagnosis
(`FAILURE-ANALYSIS-126.md`) showed is missing: Situation identity, a rule-based (not score-based) eligibility test,
explicit outcomes and provenance.

**Not fitted to cases.** Every rule below is stated as a general condition. The 126 cases are cited only as examples
of a failure class, never as targets. Acceptance is on a fresh holdout (`PREREGISTRATION-V2-R2.md`).

**Labels.** `OWNER-RULED` = decided by the owner on 2026-11-02 (CONTRACT-V2 D2–D6), carried over unchanged.
`PROPOSED` = needs owner approval. `OWNER DECISION` = a product choice with real alternatives, listed in section 8.

## 0. Preconditions owned upstream (not part of this contract)

The contract assumes, and the evaluation reports separately, that:
- **Actor normalisation** merges person-name variants ("Milei" ≡ "Javier Milei"), maps people to the state they act
  for where configured, and drops non-actor tokens (party or ideology words such as "Democrat", language names such as
  "English", hazard names, products and programmes).
- **Principal extraction** names the parties of the occurrence.
- **Development segmentation** flags a Development whose members describe different occurrences (`mixed`).
- **Event-type classification** and **place extraction** are as reliable as their own evaluations say.

When a precondition fails, the contract must degrade to "not `MEMBER`", never to a confident wrong `MEMBER`
(sections 3–4).

## 1. Situation identity (PROPOSED)

A Situation is a **persistent process between distinct parties, on one topic**. It is not an actor pair.

**Identity key** = (anchor parties, topic family).
- **Anchor parties:** at least two **distinct canonical entities** after normalisation (precondition 0). Name variants
  of one person, or a person and the state that person represents, count as **one** party.
- **Topic family:** one of a fixed, small list of coarse families mapped from event types: `armed_conflict`,
  `security_incident`, `diplomacy`, `economic_coercion` (sanctions, trade measures), `politics_elections`,
  `legal_justice`, `hazard`, `other`. Coarse families are used because the fine event types are unreliable.
  `unknown` is not a family.

**Creation** (the automatic kind). A new Situation is created when **at least two occurrence Developments** that are
not commentary, not `mixed`, and have principal actors share the same identity key within `create_window_days`, and no
open Situation has that key. Founders are those Developments.
- Same anchor parties with a **different topic family** create a **separate** Situation (topic split).
- Founders whose families are all `unknown` do **not** create a Situation; they wait for a typed occurrence.

**Kinds.**
- `seeded`: identity, scope and keywords written by the owner in `config/situations.yaml` (unchanged).
- `automatic`: created by the rule above.
- `hazard` (`OWNER DECISION` OD2): keyed by (hazard family, affected country), not by actors, so a named storm or
  earthquake gathers its Developments without inventing actors.
- Single-party storylines (one person or organisation plus a topic) are **not** automatic Situations unless the owner
  decides otherwise (`OWNER DECISION` OD1).

**Name.** Generated from the identity key: "<Party A> – <Party B>: <topic family>". The name is cosmetic. It is never
evidence for membership.

## 2. Situation scope

**OWNER-RULED (D5):** scope is derived from the founders at creation and frozen; only the owner widens it.

| Part | Derived from | Frozen? |
|---|---|---|
| Anchor parties | identity key | yes |
| Topic families | the founders' families (the key family, plus any other founder family) | yes |
| Place scope | countries of the founders' in-scope specific places, plus the anchor parties' own countries | yes |
| Keywords | seeded Situations only (owner-written) | owner-edited |

- **Widening:** only an owner override in `situations.yaml` with a date. It never widens automatically.
- **Owner-intended scope wins.** Where the owner has recorded an intended scope (as in the 126-case review), it is
  entered as an override and replaces the derived scope from that date. Earlier decisions keep the scope snapshot they
  were made with (section 6).
- A Situation's scope snapshot has a version. Every membership decision records the version it used.

## 3. Membership eligibility: a Development D may enter Situation S only if all hold

| # | Requirement | Rule | Status |
|---|---|---|---|
| E1 | Party coverage | D's canonical principal parties cover **all** of S's anchor parties (full coverage), **or** at least half of them under E1-half | `OWNER-RULED` (D4) for the half rule |
| E1-half | Half coverage | at least ⌈50%⌉ coverage **and** an E2 signal **and** a specific place inside S's place scope. A generic state party (one that is an anchor of more than `generic_anchor_limit` open Situations, for example "United States") **does not count toward half coverage** on its own | D4 `OWNER-RULED`; the generic-anchor clause `PROPOSED` |
| E2 | Scope signal | at least one of: D's topic family is in S's families; a specific place in S's place scope; a seed keyword in the headline or lead (seeded only). Required at **full coverage too** | `PROPOSED` (v2 required it for half coverage only) |
| E3 | Occurrence | D is occurrence-led: the majority of its member items are reports, not analysis, opinion, roundup or live blog | `OWNER-RULED` (D2) via X2 |
| E4 | Lifecycle | S is active, or S is dormant and D itself passes E1–E3 (reactivation needs its own evidence); closed Situations take no members | `PROPOSED` |
| E5 | Development integrity | D is not flagged `mixed` by segmentation | `PROPOSED` |

The decision is **rule-based**. Semantic similarity to the centroid and score components may be recorded as evidence
and used only to order otherwise-equal candidates; they never admit or reject on their own.

## 4. Exclusions and outcomes

Applied in this order; the first that fires decides.

| Order | Condition | Outcome | Reason code | Status |
|---|---|---|---|---|
| 1 | D has no principal actors | `NOT_MEMBER` (owner may assign `MANUAL`) | `NO_PRINCIPALS` | `OWNER-RULED` (D3) |
| 2 | D fails E3 (commentary-led) and passes E1 | `CONTEXT` (linked as analysis; not a member, not in the centroid, never reactivates S) | `COMMENTARY_ONLY` | `OWNER-RULED` (D2) |
| 3 | D is `mixed` (fails E5) and passes E1 | `AMBIGUOUS` (or `PENDING`, OD3) until segmentation resolves it | `MIXED_DEVELOPMENT` | `PROPOSED` |
| 4 | D fails E1 | `NOT_MEMBER` | `LOW_COVERAGE` / `NO_SHARED_ACTORS` / `GENERIC_ANCHOR_ONLY` | `PROPOSED` codes |
| 5 | D passes E1, its family is in S's families, but **every** specific place is outside S's place scope (and at least one place is known) | `SPILLOVER`: not a member of S (the reason records S for reporting only; no link relation); D remains free to found or join its own Situation | `OUT_OF_SCOPE_PLACE` | `OWNER-RULED` (D6) |
| 6 | D passes E1 but fails E2, or its known family is outside S's families | `NOT_MEMBER` | `NO_SCOPE_SIGNAL` / `OUT_OF_SCOPE_DOMAIN` | `PROPOSED` |
| 7 | D passes E1–E5 for S **and** for another open Situation S′ with strictly better evidence (higher coverage; then more scope signals; then a seeded S′ over an automatic S) | `OTHER_SITUATION` for S; evaluated for S′ | `BETTER_SITUATION` | `PROPOSED` |
| 8 | D passes E1–E5 for two Situations and no rule in 7 separates them | `AMBIGUOUS` (no automatic assignment; owner queue) | `AMBIGUOUS` | `PROPOSED` |
| 9 | Otherwise | `MEMBER` | `CONTINUATION` (with `scope_source`) | `OWNER-RULED` (D1 shape) |

Notes:
- An `unknown` family never satisfies E2 and never triggers `OUT_OF_SCOPE_DOMAIN`. Unknown or country-level places
  never trigger `OUT_OF_SCOPE_PLACE`.
- **`PENDING`** (`OWNER DECISION` OD3): a conditional outcome. D is held against S with a named condition (for
  example "suspected → confirmed", or "segmentation resolves `mixed`") and re-evaluated when D gains members or the
  condition is met; it expires to `NOT_MEMBER` after `pending_days`. Without OD3, those cases are `AMBIGUOUS`.
- Founders are members by construction. A Situation whose founders the owner rejects is an **identity** failure,
  repaired by the owner (`REPAIR:<name>`), not a membership decision.

## 5. Re-evaluation (OWNER-RULED D7, unchanged)

No automatic re-evaluation of stored memberships. Under the approved contract, a report-only dry run first. Any change
to stored memberships is a per-Situation repair with its own approval and backup. `PENDING` (if OD3 is approved) is the
only automatic re-check, and only for Developments that are still pending.

## 6. Provenance: one record per decision (PROPOSED; carries CONTRACT-V2 §3)

| Field | Content |
|---|---|
| identity | `at`, `run_id` (`added_in_run`), `kind: situation_membership`, `development_id`, `situation_slug`, `contract_version` |
| decision | `outcome` (`MEMBER`, `CONTEXT`, `SPILLOVER`, `OTHER_SITUATION`, `NOT_MEMBER`, `AMBIGUOUS`, `PENDING`), `reason` (one code from section 4), `decided_by` (`automatic`, `manual:<owner>`, `repair:<name>`) |
| evidence | `principal_parties`, `anchor_parties`, `shared_parties`, `coverage`, `generic_anchor_excluded`, `scope_signals` [{kind, value}], `family`, `places` [{name, in_scope}], `occurrence_items`, `mixed_flag`, `better_situation` (slug and why), `score_components` (record only) |
| scope | `scope_version` and `scope_snapshot` (anchor parties, families, place scope, keywords at decision time), `scope_source` (`seed`, `derived`, `owner_override`) |
| lifecycle | `added_at`; for later changes `superseded_by` / `removed_at` with an exit reason (`SUPERSEDED`, `REPAIR:<name>`, `DEVELOPMENT_MERGED`, `DEVELOPMENT_SPLIT`, `MANUAL`, `PENDING_EXPIRED`) |
| creation only | `identity_key`, `founders`, `variant_collapses` applied to the anchor parties |

Writer: the Development-membership decision log (`feat/development-membership-provenance`), new record kind, off by
default (CONTRACT-V2 D8). A persisted table only when pages must query it.

## 7. What this revision changes relative to CONTRACT-V2

| Area | CONTRACT-V2 (11-02) | This revision |
|---|---|---|
| Situation identity | actor pair, not addressed | distinct parties + topic family; topic split; variant collapse; hazard kind (OD2) |
| Eligibility | E1–E5 listed, score still weighted | rule-based decision; E2 required at full coverage; generic-anchor clause; E5 = Development integrity |
| Outcomes | entered / rejected / linked context | seven explicit outcomes with fixed precedence, including `SPILLOVER`, `OTHER_SITUATION`, `AMBIGUOUS`, optional `PENDING` |
| Scope | derived and frozen | plus owner-intended scope as a dated override, versioned scope snapshot per decision |
| Upstream defects | implicit | named preconditions; failures degrade to "not `MEMBER`" |
| Seeds | positive / negative / boundary cases as gold | not reusable as v2 acceptance cases (the owner's labels changed 6 of them) |

## 8. Owner decisions needed

| ID | Decision | Alternatives | Recommendation |
|---|---|---|---|
| OD1 | Single-party storylines | (a) never automatic; (b) one party + topic family allowed | (a) for v2; revisit with evidence |
| OD2 | Hazard Situations | (a) add `hazard` kind keyed by (hazard family, country); (b) none | (a) |
| OD3 | Conditional membership | (a) `PENDING` with condition and expiry; (b) `AMBIGUOUS` only | (b) for v2 (no new state); (a) later |
| OD4 | Topic split at creation | (a) identity = parties + family; (b) parties only | (a) |
| OD5 | E2 at full coverage | (a) required; (b) only at half coverage (v2 as written) | (a) |
| OD6 | Generic-anchor clause | (a) a party that anchors more than N open Situations does not count toward half coverage; (b) none | (a), N fixed before the holdout |
| OD7 | Adopt the 126-review intended scopes as overrides | (a) yes, dated; (b) no | owner's call; it changes only scopes, not labels |
| OD8 | Gates for the fresh holdout | see `PREREGISTRATION-V2-R2.md` | approve before scoring |

Stop here: no runtime implementation until the owner rules on OD1–OD6 and the contract is frozen.
