# Development relation taxonomy (Phase 3, draft for owner review)

A relation connects **two distinct Developments**. A Development is one occurrence (Phase 2 contract,
`evaluations/identity/development-identity-contract.md`). Relations explain how occurrences connect. They never
merge Developments and never change Situation membership.

## Labels

| Label | Kind | Direction | Definition | Required evidence |
|---|---|---|---|---|
| `same_calamity_lifecycle` | episode | symmetric | Both are stages of **one** natural or health calamity in a bounded area: warning, evacuation, impact, rescue and death toll, damage and cost, recovery. | The same hazard event (the same storm, quake, flood episode or outbreak) and an overlapping area. Same hazard type, same country or same season is not enough. |
| `same_visit_or_summit` | episode | symmetric | Both happen within **one** bounded visit, meeting or summit: its announcement, the meeting, signed outcomes, side meetings, protests at it. | The same occasion: participants, dates and venue. The same bilateral relationship over time is not enough. |
| `same_attack_wave` | episode | symmetric | Both come from **one** bounded wave of attacks (one night, one operation), including its side effects elsewhere. | The same wave: time span and attacker, explicitly or by the stated timing. Two days of strikes in the same war are not one wave. |
| `reaction_to` | directed | source → target | The source is a statement or action by an actor that **explicitly responds** to the target: condemnation, rejection, welcome, counter-measure announced as a response. | The source names the target occurrence or refers to it unambiguously. |
| `follow_up_to` | directed | source → target | The source is a **later step of the same matter** begun in the target, typically by the same institution or process: charges after an arrest, a verdict after a trial, implementation after a decision, an inquiry into an incident. | Explicit continuity: the same case, decision, incident or procedure. Later news on the same topic is not enough. |
| `caused_by` | directed | effect → cause | The text **explicitly states** that the target caused or triggered the source. | An attributed causal claim ("because of", "triggered by", "in the wake of" with stated causation). An inferred cause is not enough: label `AMBIGUOUS` or `NO_RELATION`. |
| `co_caused_with` | symmetric | none | Both are **explicitly attributed** to the same identifiable underlying cause (one event or decision), and neither causes the other. | Both texts name the common cause. |
| `NO_RELATION` | none | none | Distinct Developments without any of the relations above. | none |
| `AMBIGUOUS` | none | none | The evidence shown does not settle it. The note says what would. | none |

## Precedence (one primary label per pair)

1. **The same occurrence** is not a relation. It is an identity question: set `identity_flag: SAME_DEVELOPMENT_SUSPECTED`
   and leave the relation label `NO_RELATION`.
   - A release, its Q&A, its factsheet and the daily-news mention of one act are **one Development**. There is
     no `official_package` relation.
2. **Episode types first.** These are `same_calamity_lifecycle`, `same_visit_or_summit` and `same_attack_wave`.
   They take precedence when both Developments are stages of one bounded episode. Within an episode, the
   directed types are not used, even if one stage follows another.
3. **Then the directed types,** in this order:
   - `reaction_to`: a different actor responds;
   - `follow_up_to`: the same matter or process continues;
   - `caused_by`: any other explicit causal claim.
4. **`co_caused_with`** comes last.

## What is never sufficient on its own

- shared actors, including broad bilateral pairs such as US–China, US–Iran or Russia–Ukraine;
- a shared place;
- temporal proximity;
- the same conflict, crisis, storyline or Situation;
- the same topic;
- high text similarity.

The Situation hold-out (2026-10-05, `KEEP EXACT ACTOR-SET`) showed that a shared broad actor pair is no evidence
of a persistent connection. Broad pairs are therefore explicit negative controls in the gold.

## Out of scope

- **Commentary and analysis.** A piece analysing a Development is evidence with the COMMENTARY role. It is not
  a Development that relates to it.
  - If commentary appears as its own unit, label the pair `NO_RELATION` with `flag: commentary`.
  - Commentary that reports a **new** reaction (a named actor's statement) can support `reaction_to`.
- **Situation membership.** Relations do not imply it. A relation between Developments in two Situations does
  not move either of them.
- **Storyline grouping.** A whole storyline is not a relation. Relations are pairwise and evidence-bound.
