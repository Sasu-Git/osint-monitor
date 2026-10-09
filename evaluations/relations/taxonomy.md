# Development relation taxonomy (Phase 3, revision 1: owner decisions of 2026-10-07)

A relation connects **two distinct Developments**. A Development is one occurrence (Phase 2 contract,
`evaluations/identity/development-identity-contract.md`). Relations explain how occurrences connect. They never
merge Developments and never change Situation membership.

## Labels and named roles

Directed relations name each side's role; there are no generic arrows.

| Label | Kind | Roles | Definition | Required evidence |
|---|---|---|---|---|
| `same_calamity_lifecycle` | episode | – | Both are stages of **one** natural or health calamity in a bounded area: warning, evacuation, impact, rescue and death toll, damage and cost, recovery. | The same hazard event (the same storm, quake, flood episode or outbreak) and an overlapping area. |
| `same_convened_event` | episode | – | Both belong to **one bounded scheduled gathering** (a visit, summit, conference or assembly session): its distinct actions and stated outcomes. | The same occasion: participants, dates, venue. Later implementation of an outcome is `follow_up_to`. |
| `same_attack_wave` | episode | – | Both come from **one** bounded wave of attacks (one night, one operation). | The same wave: time span and attacker. |
| `reaction_to` | directed | **reaction → trigger** | The reaction is a statement or action by an actor that **explicitly responds** to the trigger: condemnation, rejection, welcome, counter-measure. | The reaction names the trigger occurrence or refers to it unambiguously. |
| `follow_up_to` | directed | **follow-up → original** | The follow-up is a later step of the same matter (the same case, decision, incident or procedure). | Explicit continuity. |
| `caused_by` | directed | **effect → cause** | The text explicitly states that the cause brought about the effect. | An attributed causal claim. |
| `commentary_on` | directed | **commentary → subject** | The commentary is analysis, an explainer or opinion about the subject occurrence. | The commentary is about the subject occurrence. |
| `co_caused_with` | symmetric | – | Both are explicitly attributed to the same identifiable cause, and neither causes the other. | Both texts name the common cause. |
| `NO_RELATION` | none | – | Distinct Developments without any of the relations above. | – |
| `AMBIGUOUS` | none | – | The evidence shown does not settle it. | – |

An identity question is not a relation. Set `SAME_DEVELOPMENT_SUSPECTED` when both sides look like one occurrence;
it is routed to identity review.

## Evidence rule

**Canonical relations are explicit-only.** The text must state the link: a named trigger, an attributed cause, an
explicit continuation.

A link the owner judges real but only inferable (a reaction to a general situation, a shared background cause) is
recorded with `evidence: inferred`. It is **non-canonical**: kept for later Situation/assessment logic, never
emitted at runtime.

## Third events

When both sides relate to a **third** occurrence that is not in the pair, the pair itself is `NO_RELATION`. The
links to the third event are recorded as external links. For example, two commentaries on the same decision are
each `commentary_on` that decision, not related to each other.

## Precedence (one primary label per pair)

1. **The same occurrence** → `SAME_DEVELOPMENT_SUSPECTED`. This is not a relation.
2. **Episode types**, when both sides are stages of one bounded episode.
3. **`reaction_to`** when a different actor responds. Then **`follow_up_to`** when the same matter continues. Then
   **`caused_by`**.
4. **`commentary_on`** when one side analyses the other.
5. **`co_caused_with`**.

## Never sufficient on its own

- shared actors, including broad bilateral pairs such as US–China;
- a shared place;
- temporal proximity;
- the same conflict, crisis, storyline or Situation;
- the same topic;
- high text similarity.

## Phase 3 runtime (owner decision, 2026-10-07)

| Plan | Types |
|---|---|
| **Implement** | `same_calamity_lifecycle`, `same_convened_event` |
| **Targeted batch first** | `reaction_to` |
| **Defer** | `same_attack_wave`, `follow_up_to`, `commentary_on` |
| **Dropped from Phase 3 runtime** | `caused_by`, `co_caused_with` (they stay in the gold taxonomy) |
