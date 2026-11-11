# Situation membership contract v2, revision 2 — FROZEN 2026-11-11

**Status.** Contract frozen (hash in `V2-R2-FREEZE.md`). Owner rulings OD1–OD8 (2026-11-11) are incorporated. No
runtime, schema or config change yet. Draft history: `fff0503`. The 2026-11-02 rulings in `CONTRACT-V2.md` (D2–D6)
are carried over unchanged. Any later change is a dated amendment, and an amendment after the holdout window opens
voids that window.

**Not fitted to cases.** Every rule is a general condition. The 126-case set (`FAILURE-ANALYSIS-126.md`) is diagnostic
only. Acceptance is on a fresh holdout (`PREREGISTRATION-V2-R2.md`).

**Provenance of each rule.** `D2`–`D6`: owner, 2026-11-02. `OD1`–`OD8`: owner, 2026-11-11. `DEF`: a deterministic
definition written to implement an owner ruling; the owner may amend it before the holdout window opens.

## 0. Preconditions owned upstream (reported, not fixed here)

- **Actor normalisation:** person-name variants merge ("Milei" ≡ "Javier Milei"); people map to the state they act for
  where configured; non-actor tokens are dropped (party or ideology words such as "Democrat", language names such as
  "English", hazard names, products and programmes).
- **Principal extraction** names the parties of the occurrence, in all collected languages.
- **Development segmentation** flags a Development whose members describe different occurrences (`mixed`).
- **Event-type classification** (`config/development_types.yaml`) and **geolocation** (event country per the
  geolocation contract) are as reliable as their own evaluations say. The taxonomy has no legal/justice and no hazard
  type; hazards use the lexicon in §1.4.

When a precondition fails, the contract degrades to "not `MEMBER`" or `PENDING`, never to a confident wrong `MEMBER`.

## 1. Situation identity

A Situation is a persistent process on one topic. Three creation modes exist; each has its own identity key.

### 1.1 Topic families (DEF, from the event-type taxonomy)

| Family | Event types |
|---|---|
| `armed_conflict` | `military_action`, `deployment`, `military_exercise`, `ceasefire`, `arms_transfer` |
| `security` | `security_incident`, `threat`, `warning` |
| `diplomacy` | `bilateral_meeting`, `multilateral_meeting`, `summit`, `negotiation`, `diplomatic_visit`, `agreement`, `treaty`, `significant_statement` |
| `economic` | `sanctions`, `economic_action` |
| `politics` | `election`, `appointment`, `resignation`, `policy_change` |
| `hazard` | none: set by the hazard lexicon (§1.4) |

`commentary`, `other` and `unknown` are **not** families. A Development with no family cannot found a Situation and
never satisfies a family-based scope signal.

### 1.2 Actor-process Situations (automatic; D5, OD4)

- **Key** = (anchor parties, family). Anchor parties are **at least two distinct canonical parties** after
  normalisation. Name variants of one person, or a person and the state that person represents, count as one party.
- **Creation:** at least two occurrence Developments (not commentary, not `mixed`, with principal actors, with a
  family) share the key within `create_window_days` (7), and no open Situation has that key.
- **Topic split (OD4):** the same anchor parties with a different family form a **separate** Situation.

### 1.3 Single-party Situations (OD1)

- **Key** = (party P, family F, context country C). P is one canonical party that is **not** in the generic list
  (§3.2).
- **Creation (DEF):** at least two occurrence Developments, each with P among its principal parties, each with family
  F, each with event country C (geolocation contract; `NONE` never qualifies), first reported **at least 24 hours
  apart**, within `create_window_days`. A single Development, or several reports of one occurrence, never creates one.
- If the same Developments also qualify for an actor-process Situation (§1.2), that mode wins.

### 1.4 Hazard Situations (OD2)

- **Key** = (hazard family H, affected country C, hazard name N or none).
- **Hazard family (DEF):** set from a frozen multilingual lexicon over the Development's headlines and leads:
  `storm` (hurricane, typhoon, cyclone, tropical storm; huracán, tormenta tropical, ciclón; uragano, tempesta
  tropicale, ciclone), `earthquake` (earthquake, quake, tremor; terremoto, sismo; terremoto, scossa), `flood`
  (flood, flooding; inundación, riada; alluvione, inondazione), `wildfire` (wildfire, forest fire; incendio
  forestal; incendio boschivo), `volcanic` (eruption, volcano; erupción, volcán; eruzione, vulcano), `tsunami`,
  `landslide` (landslide, mudslide; deslizamiento, alud; frana). The lexicon is frozen with this contract
  (`hazard-lexicon-v1` in `V2-R2-FREEZE.md`).
- **Name (DEF):** the capitalised token after a storm term ("Hurricane Rachel", "huracán Simón"), accent-folded.
- **Affected country:** the Development's event country (geolocation contract). `NONE` cannot found or join.
- **Creation:** at least two occurrence Developments with the same (H, C, N) within `create_window_days`.
- **Actors are not required.** The no-principals exclusion (D3) governs actor-keyed modes. It does not apply to
  hazard Situations, which OD2 made a distinct mode not forced through actor identity.

### 1.5 Seeded Situations

Identity, scope and keywords are written by the owner in `config/situations.yaml` (unchanged).

**Names** are generated from the key ("Russia – United States: economic"; "storm Rachel – Mexico") and are never
evidence for membership.

## 2. Situation scope (D5, OD7)

| Part | Actor-process | Single-party | Hazard | Frozen? |
|---|---|---|---|---|
| Identity | anchor parties | P | H, N | yes |
| Families | founders' families | F | `hazard` | yes |
| Place scope | countries of founders' in-scope specific places + anchor parties' own countries | C | C | yes |
| Keywords | — | — | — | seeded only, owner-edited |

- Scope never widens automatically. Widening or narrowing is an **owner override**: a dated, versioned record with
  author, timestamp, previous value, new value and reason (OD7).
- **The 126-review scopes** are adopted as such overrides (`scope-overrides/2026-11-10-owner-review.yaml`). They are
  curated current scopes; they inform design and are not acceptance evidence. The owner's free-text entries are mapped
  to families and countries at implementation, and the mapping is shown to the owner before the code freeze.
- Each scope has a version. Every decision records the scope snapshot and version it used.

## 3. Membership eligibility

### 3.1 Requirements: D may enter S only if all hold

| # | Requirement | Rule | Source |
|---|---|---|---|
| E1 | Identity match | actor-process: D's principal parties cover all of S's anchor parties, or half under §3.2; single-party: P is a principal party of D; hazard: D's hazard family = H and event country = C and (N absent on either side, or equal) | D4, OD1, OD2 |
| E2 | Scope signal | at least one of: D's family in S's families; a specific place of D in S's place scope; a seed keyword in the headline or lead (seeded). **Required at every coverage level** | OD5 |
| E3 | Occurrence | the majority of D's member items are reports, not analysis, opinion, roundup or live blog | D2 |
| E4 | Lifecycle | S is active, or dormant and D itself passes E1–E3; closed Situations take no members | DEF |
| E5 | Integrity | D is not flagged `mixed` | DEF |

Single-party Situations additionally require D's family = F and event country = C. The decision is rule-based. A
similarity or score is recorded as evidence and used only to order otherwise-equal candidates.

### 3.2 Half coverage and generic parties (D4, OD6)

- **Generic parties (DEF, versioned config list `generic_parties` v1):** United States, Russia, China, United
  Kingdom, France, European Union, NATO, United Nations. These are the permanent Security Council members and the
  blocs that appear as parties in many unrelated processes. The owner edits the list; each edit is versioned.
- **Half coverage** (at least ⌈50%⌉ of S's anchor parties) is allowed only if:
  - a **non-generic** anchor party is matched, plus E2, plus a specific place in S's place scope (D4); or
  - only a generic party is matched, plus a **strong scope match**: D's family is in S's families **and** D has a
    specific place in S's place scope that is **not** in the matched generic party's own country (for EU, NATO and UN,
    any in-scope place) (OD6).
- Otherwise: `NOT_MEMBER` with `GENERIC_ANCHOR_ONLY` or `LOW_COVERAGE`.

## 4. Exclusions and outcomes, in fixed order (the first that fires decides)

| Order | Condition | Outcome | Reason code |
|---|---|---|---|
| 1 | Actor-keyed S and D has no principal actors | `NOT_MEMBER` (owner may assign `MANUAL`) | `NO_PRINCIPALS` (D3) |
| 2 | D passes E1 and fails E3 | `CONTEXT`: linked as analysis; not a member, not in the centroid, never reactivates S | `COMMENTARY_ONLY` (D2) |
| 3 | D passes E1 and fails E5 | `PENDING` | `PENDING_MIXED` (OD3) |
| 4 | D fails E1 | `NOT_MEMBER` | `NO_SHARED_ACTORS` / `LOW_COVERAGE` / `GENERIC_ANCHOR_ONLY` |
| 5 | D passes E1; family in S's families; every known specific place outside S's place scope | `SPILLOVER`: not a member; the reason records S for reporting; D may found or join its own Situation | `OUT_OF_SCOPE_PLACE` (D6) |
| 6 | D passes E1 and fails E2, or D's known family is outside S's families | `NOT_MEMBER` | `NO_SCOPE_SIGNAL` / `OUT_OF_SCOPE_DOMAIN` |
| 7 | D passes E1–E5 for S and for another open S′ with strictly better evidence (higher coverage; then more scope-signal kinds; then seeded over automatic) | `OTHER_SITUATION` for S | `BETTER_SITUATION` |
| 8 | D passes E1–E5 for two Situations and step 7 does not separate them | `AMBIGUOUS` (owner queue, no assignment) | `AMBIGUOUS` |
| 9 | D's headline or lead attributes the occurrence with a hedge term from the frozen lexicon (suspected, alleged, accused of, reportedly, claims; sospechoso, presunto, supuestamente; sospetto, presunto, presumibilmente) | `PENDING` | `PENDING_ATTRIBUTION` (OD3) |
| 10 | Otherwise | `MEMBER` | `CONTINUATION` with `scope_source` |

An `unknown` family never satisfies E2 and never triggers `OUT_OF_SCOPE_DOMAIN`. Unknown or country-level places
never trigger `OUT_OF_SCOPE_PLACE`. Founders are members by construction. A founder the owner rejects is an identity
failure, repaired by the owner (`REPAIR:<name>`), not a membership decision.

### 4.1 PENDING lifecycle (OD3: no permanent limbo)

| Element | Rule |
|---|---|
| Reasons | only `PENDING_MIXED` and `PENDING_ATTRIBUTION` |
| Re-evaluation trigger | `PENDING_MIXED`: segmentation changes D's members or clears the flag. `PENDING_ATTRIBUTION`: D gains a member item whose headline and lead carry no hedge term. Only that (D, S) pair is re-run through §4 |
| Expiry | 7 days after `pending_since`: the pair becomes `NOT_MEMBER` with `PENDING_EXPIRED` and is listed in the owner review queue |
| No re-entry | a pair that expired never becomes `PENDING` again; at most one pending record per pair |
| Effect while pending | not a member, not in the centroid, never reactivates S; shown as "pending" with its reason |

## 5. Re-evaluation of stored memberships (D7, unchanged)

No automatic re-evaluation, except of `PENDING` pairs (§4.1). Changes to stored memberships go through a report-only
dry run, then a per-Situation repair with its own approval and backup.

## 6. Provenance: one record per decision

| Field | Content |
|---|---|
| identity | `at`, `run_id` (`added_in_run`), `kind: situation_membership`, `development_id`, `situation_slug`, `situation_mode` (`actor_process` / `single_party` / `hazard` / `seeded`), `contract_version` |
| decision | `outcome`, `reason`, `decided_by` (`automatic` / `manual:<owner>` / `repair:<name>`) |
| evidence | `principal_parties`, `anchor_parties`, `shared_parties`, `coverage`, `generic_parties_matched`, `scope_signals` [{kind, value}], `family`, `hazard` {family, name}, `places` [{name, country, in_scope}], `event_country`, `occurrence_items`, `mixed_flag`, `hedge_terms`, `better_situation`, `score_components` (record only) |
| scope | `scope_version`, `scope_snapshot`, `scope_source` (`seed` / `derived` / `owner_override`) |
| lifecycle | `added_at`; `pending_since`, `pending_trigger`, `pending_expires_at`; `superseded_by` / `removed_at` with exit reason (`SUPERSEDED`, `REPAIR:<name>`, `DEVELOPMENT_MERGED`, `DEVELOPMENT_SPLIT`, `MANUAL`, `PENDING_EXPIRED`) |
| creation | `identity_key`, `mode`, `founders`, `variant_collapses` |

Writer: the Development-membership decision log (`feat/development-membership-provenance`), new record kind, off by
default (D8 as proposed in CONTRACT-V2). A persisted table only when pages must query it.

## 7. Parameters frozen with the contract

`create_window_days` 7; single-party minimum separation 24 h; `pending_days` 7; `generic_parties` v1 (§3.2); hazard
lexicon v1 (§1.4); hedge lexicon v1 (§4); family mapping (§1.1).
