# Development relation review sheet (Phase 3 gold, development split)

One case is one pair of **distinct** Developments. Side A is the earlier Development.

**Definitions.** They are in `../taxonomy.md`. Labels:

- the relation types `same_calamity_lifecycle`, `same_visit_or_summit`, `same_attack_wave`,
  `reaction_to`, `follow_up_to`, `caused_by` and `co_caused_with`;
- `NO_RELATION`;
- `AMBIGUOUS`.

**Direction.** For a directed type, write it as source -> target. For example, `B->A` with
`reaction_to` means B reacts to A. Use `none` for symmetric types.

**How to review.** Fill in your verdict in `owner-verdicts.yaml`. You may correct the type, the
direction or both. Notes are kept verbatim. Set `identity_flag: SAME_DEVELOPMENT_SUSPECTED` when the two
sides look like one occurrence: that is an identity question, not a relation.

**About the draft labels.** A separate annotator wrote them, seeing only the evidence text and the
taxonomy. How a case was selected is deliberately not shown.

**Cases:** 2. Draft labels: NO_RELATION 2.

| Case | A | B | Draft label | Direction | Confidence |
|---|---|---|---|---|---|
| [P201](#p201) | Spain announces new housing measures after protests over 87- | Pot banging protests across Spain over housing crisis | NO_RELATION | none | medium |
| [P202](#p202) | Photos: French students protest, public workers strike befor | Pot banging protests across Spain over housing crisis | NO_RELATION | none | high |

---

## P201

**Development A** `2026-10-03-live:D3`

- **Members:** 5 item(s)
- **Sources:** Al Jazeera, BBC World, South China Morning Post
- **Times:** 2026-09-29 12:14 to 2026-09-29 21:02 UTC
- **Actors:** Spain
- **Places:** Madrid, Spain
- **System Development:** D3
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 12:14 [BBC World] **Spain announces new housing measures after protests over 87-year-old woman's eviction**
    > The measures include a proposed ban on evictions until 2030 and the automatic renewal of tenant contracts.
  - 2026-09-29 16:23 [BBC World] **Spain announces ban on evictions after protests over 87-year-old woman's removal from flat**
    > The ban is part of a number of proposals that must be approved in parliament within 30 days.
  - 2026-09-29 17:54 [South China Morning Post] **87-year-old woman whose eviction sparked protests in Spain is returning home**
    > Spain’s coalition government said it had agreed on proposals including banning evictions until 2030 to address the country’s housing crisis, as the 87-year-old woman whose forced removal last week triggered protests accepted an offer to return home.
Hundreds of ‌people remained c
  - 2026-09-29 18:57 [Al Jazeera] **Madrid residents feel the impact of Spain’s housing crisis**
    > Spain’s housing crisis is deepening as soaring rents and a shortage of homes put affordable housing out of reach.
  - 2026-09-29 21:02 [Al Jazeera] **Spain protests: Evicted 87-year-old woman to return to Madrid home**
    > The real estate firm backs down and restores her old rent after mass protests over Spain&#039;s housing crisis.

**Development B** `2026-10-03-live:D51`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera, BBC World
- **Times:** 2026-10-02 01:56 to 2026-10-03 11:35 UTC
- **Actors:** none extracted
- **Places:** Spain
- **System Development:** D51
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-02 01:56 [Al Jazeera] **Pot banging protests across Spain over housing crisis**
    > Hundreds of protesters across Spain took part in pot banging demonstrations to demand political action over housing
  - 2026-10-03 11:35 [BBC World] **Protesters across Spain demand action over housing crisis**
    > More than 50 protests are planned to take place on Saturday after the government failed to get emergency legislation through parliament.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | inferred |

**Rationale:** B's protests 'demand political action over housing' and follow the government's failure 'to get emergency legislation through parliament', which is a later third occurrence and the general housing crisis, not an explicit response to A's announcement of eviction-ban measures or the 87-year-old woman's return home.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## P202

**Development A** `2026-10-03-live:D5`

- **Members:** 12 item(s)
- **Sources:** Al Jazeera, BBC World, South China Morning Post
- **Times:** 2026-09-29 14:51 to 2026-10-02 21:13 UTC
- **Actors:** none extracted
- **Places:** France, Marseille, Paris
- **System Development:** D5
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 14:51 [Al Jazeera] **Photos: French students protest, public workers strike before budget cuts**
    > French high school students have blockaded dozens of schools and public sector workers have gone on strike, protesting planned budget cuts before next year’s presidential election.

Tuesday’s action comes seven months before the vote and just two days before the government is due
  - 2026-09-29 21:09 [Al Jazeera] **French students clash with police as protests over education cuts spread**
    > French school students have blocked schools across France, demanding better learning conditions.
  - 2026-09-29 21:32 [BBC World] **More than 400 detained as France student protests escalate**
    > Students have been protesting against conditions and resources in secondary schools since last week.
  - 2026-09-30 03:53 [Al Jazeera] **Public workers in France strike over pay as student protests turn violent**
    > Tens of thousands of workers march nationwide, as police arrest 440 students in clashes at schools.
  - 2026-09-30 13:18 [BBC World] **Dozens hurt and hundreds arrested in wave of French school protests**
    > Students have been protesting against conditions and resources in secondary schools since last week.
  - 2026-10-01 15:47 [South China Morning Post] **French school protests spread as fires, blockades deepen unrest**
    > A protest by French secondary school students over overcrowded classrooms, teacher shortages and crumbling facilities deepened on Thursday, with fires set outside schools and blockades in several cities.
More than 160 schools were shut down on Thursday, while university students 
  - 2026-10-01 16:34 [BBC World] **Fires break out at French schools as students protest nationwide**
    > The French government holds a crisis meeting as demonstrations grow and become violent in places.
  - 2026-10-01 18:18 [Al Jazeera] **School protests spread as fires, blockades deepen unrest in France**
    > Police have detained hundreds as students protest overcrowded classrooms, teacher shortages and crumbling facilities.
  - 2026-10-02 09:50 [South China Morning Post] **Hundreds of French high schools shut as new violence erupts**
    > French high school students lit fires outside schools and faced off with police on Friday as a protest movement that has forced the closure of some 400 establishments showed no sign of abating.
The movement, which began last week in the Paris region and rapidly spread nationwide,
  - 2026-10-02 12:43 [BBC World] **School protests send shivers down French government's spine**
    > A movement that started nearly two weeks ago has spread, and in France young people on the streets spells trouble, writes Hugh Schofield.
  - 2026-10-02 13:12 [Al Jazeera] **Protests shutter hundreds of French schools as violence flares**
    > Education minister declares students &#039;in danger&#039; as hundreds of injuries reported across the country.
  - 2026-10-02 21:13 [BBC World] **Riot police clash with students as education protests rage in France**
    > About 735 schools have faced disruption as violent protests over standards and lack of teachers continue.

**Development B** `2026-10-03-live:D51`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera, BBC World
- **Times:** 2026-10-02 01:56 to 2026-10-03 11:35 UTC
- **Actors:** none extracted
- **Places:** Spain
- **System Development:** D51
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-02 01:56 [Al Jazeera] **Pot banging protests across Spain over housing crisis**
    > Hundreds of protesters across Spain took part in pot banging demonstrations to demand political action over housing
  - 2026-10-03 11:35 [BBC World] **Protesters across Spain demand action over housing crisis**
    > More than 50 protests are planned to take place on Saturday after the government failed to get emergency legislation through parliament.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** A covers French school-student protests and public-worker strikes over education cuts, while B covers Spanish pot-banging protests over the housing crisis; they share only the protest topic and time window, and neither text refers to the other.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

