# Relation labelling input (blind)

Label every case using the definitions in `taxonomy.md` (included below).

- Side A is the earlier Development, side B the later one.
- Each side is one Development: one occurrence, possibly reported by several outlets.

Return, per case:

- `label`: one relation type, `NO_RELATION` or `AMBIGUOUS`;
- `direction`: for a directed type, which side holds the first role: `A->B` means A is the reaction /
  follow-up / effect / commentary and B the trigger / original / cause / subject; `B->A` the reverse; else
  `none`;
- `identity_flag`: `SAME_DEVELOPMENT_SUSPECTED` or null;
- `flag`: for example `commentary`, or null;
- `rationale`: one sentence that cites the evidence;
- `confidence`: high, medium or low.

---

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


---

## P201
**A** (5 item(s))
- 2026-09-29 12:14 [BBC World] Spain announces new housing measures after protests over 87-year-old woman's eviction
  > The measures include a proposed ban on evictions until 2030 and the automatic renewal of tenant contracts.
- 2026-09-29 16:23 [BBC World] Spain announces ban on evictions after protests over 87-year-old woman's removal from flat
  > The ban is part of a number of proposals that must be approved in parliament within 30 days.
- 2026-09-29 17:54 [South China Morning Post] 87-year-old woman whose eviction sparked protests in Spain is returning home
  > Spain’s coalition government said it had agreed on proposals including banning evictions until 2030 to address the country’s housing crisis, as the 87-year-old woman whose forced removal last week triggered protests accepted an offer to return home.
Hundreds of ‌people remained camped in one of Madr
- 2026-09-29 18:57 [Al Jazeera] Madrid residents feel the impact of Spain’s housing crisis
  > Spain’s housing crisis is deepening as soaring rents and a shortage of homes put affordable housing out of reach.
- 2026-09-29 21:02 [Al Jazeera] Spain protests: Evicted 87-year-old woman to return to Madrid home
  > The real estate firm backs down and restores her old rent after mass protests over Spain&#039;s housing crisis.
**B** (2 item(s))
- 2026-10-02 01:56 [Al Jazeera] Pot banging protests across Spain over housing crisis
  > Hundreds of protesters across Spain took part in pot banging demonstrations to demand political action over housing
- 2026-10-03 11:35 [BBC World] Protesters across Spain demand action over housing crisis
  > More than 50 protests are planned to take place on Saturday after the government failed to get emergency legislation through parliament.

## P202
**A** (12 item(s))
- 2026-09-29 14:51 [Al Jazeera] Photos: French students protest, public workers strike before budget cuts
  > French high school students have blockaded dozens of schools and public sector workers have gone on strike, protesting planned budget cuts before next year’s presidential election.

Tuesday’s action comes seven months before the vote and just two days before the government is due to unveil its draft
- 2026-09-29 21:09 [Al Jazeera] French students clash with police as protests over education cuts spread
  > French school students have blocked schools across France, demanding better learning conditions.
- 2026-09-29 21:32 [BBC World] More than 400 detained as France student protests escalate
  > Students have been protesting against conditions and resources in secondary schools since last week.
- 2026-09-30 03:53 [Al Jazeera] Public workers in France strike over pay as student protests turn violent
  > Tens of thousands of workers march nationwide, as police arrest 440 students in clashes at schools.
- 2026-09-30 13:18 [BBC World] Dozens hurt and hundreds arrested in wave of French school protests
  > Students have been protesting against conditions and resources in secondary schools since last week.
- 2026-10-01 15:47 [South China Morning Post] French school protests spread as fires, blockades deepen unrest
  > A protest by French secondary school students over overcrowded classrooms, teacher shortages and crumbling facilities deepened on Thursday, with fires set outside schools and blockades in several cities.
More than 160 schools were shut down on Thursday, while university students joined the protests 
- 2026-10-01 16:34 [BBC World] Fires break out at French schools as students protest nationwide
  > The French government holds a crisis meeting as demonstrations grow and become violent in places.
- 2026-10-01 18:18 [Al Jazeera] School protests spread as fires, blockades deepen unrest in France
  > Police have detained hundreds as students protest overcrowded classrooms, teacher shortages and crumbling facilities.
- 2026-10-02 09:50 [South China Morning Post] Hundreds of French high schools shut as new violence erupts
  > French high school students lit fires outside schools and faced off with police on Friday as a protest movement that has forced the closure of some 400 establishments showed no sign of abating.
The movement, which began last week in the Paris region and rapidly spread nationwide, has seen teenage pu
- 2026-10-02 12:43 [BBC World] School protests send shivers down French government's spine
  > A movement that started nearly two weeks ago has spread, and in France young people on the streets spells trouble, writes Hugh Schofield.
- 2026-10-02 13:12 [Al Jazeera] Protests shutter hundreds of French schools as violence flares
  > Education minister declares students &#039;in danger&#039; as hundreds of injuries reported across the country.
- 2026-10-02 21:13 [BBC World] Riot police clash with students as education protests rage in France
  > About 735 schools have faced disruption as violent protests over standards and lack of teachers continue.
**B** (2 item(s))
- 2026-10-02 01:56 [Al Jazeera] Pot banging protests across Spain over housing crisis
  > Hundreds of protesters across Spain took part in pot banging demonstrations to demand political action over housing
- 2026-10-03 11:35 [BBC World] Protesters across Spain demand action over housing crisis
  > More than 50 protests are planned to take place on Saturday after the government failed to get emergency legislation through parliament.

