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

## T001
**A** (2 item(s))
- 2026-08-22T16:20 [BBC World] Carney faces crucial test after walking away from Trump's deal
  > The Canadian prime minister will have to sell his gamble that walking away from talks with the White House will be worth the consequences.
- 2026-08-22T20:02 [BBC World] Carney faces crucial test after walking away from Trump's deal
  > The Canadian prime minister will have to sell his gamble that walking away from talks with the White House will be worth the consequences.
**B** (2 item(s))
- 2026-08-22T18:20 [BBC World] Carney calls Trump's fresh tariffs a 'miscalculation' after trade talks collapse
  > Canada's prime minister said he was "reluctantly" announcing retaliatory tariffs as he accused the US of starting a trade war.
- 2026-08-22T20:10 [BBC World] Carney calls Trump's fresh tariffs a 'miscalculation' after trade talks collapse
  > Canada's prime minister said he was "reluctantly" announcing retaliatory tariffs as he accused the US of starting a trade war.

## T002
**A** (1 item(s))
- 2026-08-21T12:32 [Al Jazeera] US allies in Asia wary as Trump moves military assets for Iran war
  > Allies worry about the US ability to deter China, even if the bulk of US forces remain in the region.
**B** (1 item(s))
- 2026-08-22T09:14 [Al Jazeera] Iran says new US sanctions violate sovereignty of other states
  > Foreign Ministry spokesman Esmaeil Baghaei slams Trump&#039;s latest threat as a return to &#039;full-scale classic colonialism&#039;.

## T003
**A** (1 item(s))
- 2026-09-29 10:26 [DW World] Malaysia repatriates Myanmar migrants despite UN warnings
  > Malaysia has started repatriating about 1,500 Myanmar nationals, defying warnings from the UN and rights groups. Malaysia, facing an uptick in anti-migrant sentiment, says the program is strictly voluntary.
**B** (1 item(s))
- 2026-09-29 12:00 [UN News] World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, new emergency funding released, Gaza and West Bank update
  > The UN chief on Tuesday strongly condemned an airstrike that reportedly killed at least 50 people at a market in Myanmar’s Rakhine state and called for those responsible to be held to account.

## T004
**A** (1 item(s))
- 2026-09-25T02:26 [Al Jazeera] Contrasting treatment of Israel and Palestine on display at the UN
  > Israel’s Prime Minister addressed the UN General Assembly in person, despite having an ICC arrest warrant.
**B** (1 item(s))
- 2026-09-25T03:49 [Al Jazeera] Jewish protestors join Free Palestine march to denounce Netanyahu
  > Al Jazeera’s Emma Withrow reports from a Free Palestine march, where Jewish demonstrators rejected Netanyahu.

## T005
**A** (1 item(s))
- 2026-09-27T19:16 [South China Morning Post] Trump expects new Iran talks despite rejecting deal offer
  > US President Donald Trump said on Sunday that he expects talks with Iran to resume in the coming week, despite his rejection of a truce proposal put forward by Tehran.
Iranian officials brought with them to the UN General Assembly in New York a plan for a seven-day truce followed by the reopening of
**B** (1 item(s))
- 2026-09-27T20:03 [Al Jazeera] Why has Trump rejected Iran’s peace proposal?
  > The US president has reportedly threatened to resume strikes on Iran.

## T006
**A** (1 item(s))
- 2026-09-28T01:33 [Al Jazeera] Ben-Gvir releases video threatening to kill senior Hamas figure in jail
  > Israel’s security minister Itamar Ben-Gvir has released a video in which he is seen threatening to kill Hassan Salameh.
**B** (1 item(s))
- 2026-09-28T10:11 [Al Jazeera] Palestinians denounce Israeli minister Ben-Gvir’s threats against prisoner
  > Footage of national security minister taunting Hassan Salama in his cell draws sharp condemnation from Palestinians.

## T007
**A** (1 item(s))
- 2026-09-27T13:17 [Al Jazeera] ‘Better deal’: What’s behind Trump’s rejection of Iran’s truce offer?
  > Experts say Trump sees economic sanctions as key to extracting more concessions but he risks losing leverage.
**B** (1 item(s))
- 2026-09-27T14:36 [Al Jazeera] Strait of Hormuz tensions linger as Iran and US move further from a deal
  > There are fears of renewed fighting between the US and Iran, after President Trump rejected a deal.

## T008
**A** (1 item(s))
- 2026-09-29 12:14 [BBC World] Spain announces new housing measures after protests over 87-year-old woman's eviction
  > The measures include a proposed ban on evictions until 2030 and the automatic renewal of tenant contracts.
**B** (1 item(s))
- 2026-09-29 16:23 [BBC World] Spain announces ban on evictions after protests over 87-year-old woman's removal from flat
  > The ban is part of a number of proposals that must be approved in parliament within 30 days.

## T009
**A** (3 item(s))
- 2026-09-29T06:06 [BBC World] Malaysia begins controversial repatriation of asylum seekers to Myanmar
  > Human rights groups say some 5,000 returnees could face violence, persecution and forced conscription.
- 2026-09-29T07:00 [South China Morning Post] Malaysia begins sending thousands of Myanmar nationals back to war-torn homeland
  > Malaysia began an operation to send nearly 1,500 Myanmar nationals back to their war-torn homeland on Tuesday, pressing ahead with a government-to-government repatriation deal despite warnings that returnees could face persecution and forced conscription.
The first group of 1,476 is part of an agree
- 2026-09-29T09:27 [Al Jazeera] Malaysia begins sending back Rohingya refugees despite safety warnings
  > About 1,500 refugees are to be sent back in the first phase, despite criticism from rights groups.
**B** (1 item(s))
- 2026-09-29T11:22 [Al Jazeera] Malaysia gave refuge to Rohingya; now it wants them to go
  > Malaysia welcomed persecuted Muslim minority but now plans to send them back to Myanmar amid rising hate against them.

## T010
**A** (1 item(s))
- 2026-09-28T18:16 [Al Jazeera] Trump made the right decision to reject Iran’s offer
  > The US president has denied Tehran the opportunity to use the US midterm elections as a pressure point.
**B** (1 item(s))
- 2026-09-29T00:00 [Al Jazeera] Iran war live: Trump says he did not offer Tehran sanctions relief
  > US President Trump rejects a news report claiming his administration offered Iran sanctions relief and frozen funds.

## T011
**A** (1 item(s))
- 2026-09-28 20:30 [Defense.gov] Secretary of War Pete Hegseth Signs Directive to Defend 2026 Elections From Foreign Threats
  > Secretary of War Pete Hegseth signed a memorandum directing the War Department to mobilize a comprehensive, whole-of-government defense of the election infrastructure from foreign adversaries.
**B** (1 item(s))
- 2026-09-29 16:00 [War on the Rocks] What Will Hegseth’s “State of the Force” Reprise Reveal?
  > Secretary of Defense Pete Hegseth is expected to convene a high-profile meeting of military personnel for a &#8220;State of the Force&#8221; address this week. Will it show the U.S. armed forces as healthy? The answer may depend on how the audience responds, regardless of what Hegseth says. How the 

## T012
**A** (1 item(s))
- 2026-09-29 23:39 [BBC World] US Supreme Court denies Christa Pike's last-ditch bid to halt execution
  > The Tennessee inmate has been awaiting execution since she was sentenced to death in 1996 for the murder of a teenage classmate.
**B** (5 item(s))
- 2026-10-01 16:45 [BBC World] Tennessee halts executions after Christa Pike survives two lethal injection attempts
  > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
- 2026-10-02 03:02 [South China Morning Post] Christa Pike in ‘life-saving care’ after botched Tennessee execution
  > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from a prison execution c
- 2026-10-02 07:58 [Al Jazeera] Lawyers for US inmate who survived lethal injections demand release
  > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
- 2026-10-02 20:32 [BBC World] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say
  > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.

## T013
**A** (1 item(s))
- 2026-09-30 16:44 [Al Jazeera] US appeals court halts Tennessee execution of Christa Pike
  > Christa Pike was set to become the first woman executed by Tennessee in more than 200 years.
**B** (5 item(s))
- 2026-10-01 16:45 [BBC World] Tennessee halts executions after Christa Pike survives two lethal injection attempts
  > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
- 2026-10-02 03:02 [South China Morning Post] Christa Pike in ‘life-saving care’ after botched Tennessee execution
  > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from a prison execution c
- 2026-10-02 07:58 [Al Jazeera] Lawyers for US inmate who survived lethal injections demand release
  > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
- 2026-10-02 20:32 [BBC World] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say
  > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.

## T014
**A** (1 item(s))
- 2026-09-30 16:00 [South China Morning Post] US Tennessee’s first execution of a woman in 200 years halted
  > A US appeal court on Wednesday halted the ⁠execution of death row inmate Christa Pike in Tennessee, less than two hours before she was scheduled to become the first woman that state has put to death in more than 200 years.
The 6th US Circuit Court of Appeals ordered a “short stay of execution” to gi
**B** (5 item(s))
- 2026-10-01 16:45 [BBC World] Tennessee halts executions after Christa Pike survives two lethal injection attempts
  > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
- 2026-10-02 03:02 [South China Morning Post] Christa Pike in ‘life-saving care’ after botched Tennessee execution
  > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from a prison execution c
- 2026-10-02 07:58 [Al Jazeera] Lawyers for US inmate who survived lethal injections demand release
  > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
- 2026-10-02 20:32 [BBC World] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say
  > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.

## T015
**A** (2 item(s))
- 2026-08-31T00:00 [South China Morning Post] Hong Kong, Singapore aren’t ‘enemies’, our competition is healthy, envoy says
  > Singapore and Hong Kong do not view each other as enemies, but rather admire one another’s accomplishments, the country’s top envoy to the city has said, calling for greater cooperation between the two jurisdictions often cast as fierce rivals.
Eric Teo Boon Hee, Singapore’s consul general in Hong K
- 2026-08-31T02:00 [South China Morning Post] Singapore firms keen to tap Northern Metropolis’ ‘massive potential’, envoy says
  > Singaporean businesses are keen to explore the “massive potential” emerging in Hong Kong’s Northern Metropolis megaproject after the country’s prime minister visited the site earlier this year, its top envoy to the city has said.
In an exclusive interview with the South China Morning Post, Singapore
**B** (1 item(s))
- 2026-08-31T00:43 [South China Morning Post] Hong Kong can play unique role in fostering robotics industry: Paul Chan
  > Hong Kong can serve a unique role in the development of the robotics industry, the financial chief has said as he welcomed the coming opening of the city’s first convenience stores operated by humanoid robots developed by a Beijing-based company.
Following an opening ceremony on Monday, the first “G

## T016
**A** (1 item(s))
- 2026-09-28 23:02 [UN Press] Security Council, 10231st Meeting (AM) Haiti
  > The Security Council today is expected to vote on a draft resolution re-authorizing the Gang Suppression Force in Haiti, put forward by the United States and Panama, the co-penholders on Haiti. The Council first authorized the Force on 30 September 2025 under resolution 2793 (2025) for an initial 12
**B** (3 item(s))
- 2026-09-28 23:02 [UN Press] Security Council, 10232nd Meeting (AM) Democratic Republic of the Congo/MONUSCO
  > Following its meeting concerning Haiti, the Council will convene to consider the situation in the Democratic Republic of the Congo. Anticipated briefers include James Swan, Head of the United Nations Organization Stabilization Mission in the Democratic Republic of the Congo (MONUSCO), as well as a r
- 2026-09-29 12:00 [UN News] Security Council LIVE: DRC peace deals fail to halt fighting as Ebola deepens crisis
  > The Security Council met in New York&nbsp;on the Democratic Republic of the Congo (DRC) Tuesday, where clashes between Government forces and M23 rebels continue in the east, despite a series of peace agreements. Ambassadors focused on ceasefire monitoring, rising tensions between the DRC and Rwanda 
- 2026-09-29 21:52 [UN Press] Commitments Must Yield Tangible Progress in Democratic Republic of Congo, Special Representative Tells Security Council
  > Serious challenges remain despite sustained diplomatic engagement to address the conflict in the eastern part of the Democratic Republic of the Congo, the Security Council heard today, as speakers welcomed the ceasefire monitoring and verification conducted by the UN mission in that country.

## T017
**A** (1 item(s))
- 2026-08-21T13:01 [Al Jazeera] Israeli soldiers throw belongings from besieged Palestinian home
  > Israeli soldiers were filmed throwing belongings from Palestinian homes in Qusra.
**B** (2 item(s))
- 2026-08-22T14:37 [Al Jazeera] Israeli drone strike on ‘civilian vehicle’ injures several in Syria
  > Syria condemns attack in southwest as a &#039;flagrant violation of sovereignty&#039; and a &#039;blatant breach of international law&#039;.
- 2026-08-22T21:42 [BBC World] Syria says Israeli strike near Damascus violation of international law
  > The latest incident comes days after reports emerged Israel had struck a military airbase close to the Turkish border.

## T018
**A** (1 item(s))
- 2026-09-27T00:00 [Al Jazeera] Iran war live: Tehran awaits official response as Trump rejects Hormuz plan
  > US president rejects Iran&#039;s seven-day plan to reopen the Strait of Hormuz, saying the deal is not &#039;acceptable&#039;.
**B** (1 item(s))
- 2026-09-27T07:44 [BBC World] Iranian minister says only negotiation can end conflict after Trump rejects Hormuz deal
  > The foreign minister says Tehran is waiting for an official rejection of a deal, despite the US President's comments.

## T019
**A** (2 item(s))
- 2026-09-25T02:24 [Al Jazeera] More than 100 arrested as New Yorkers protest Netanyahu’s UN visit
  > Demonstrators blocked streets and marched towards UN headquarters as the Israeli PM addressed world leaders at UNGA.
- 2026-09-25T02:35 [Al Jazeera] NYC police arrest Susan Sarandon, other celebrities protesting Netanyahu
  > Rights groups accuse UN of hosting a &#039;war criminal&#039; as delegations walk out during Israeli prime minister&#039;s speech.
**B** (1 item(s))
- 2026-09-25T03:49 [Al Jazeera] Jewish protestors join Free Palestine march to denounce Netanyahu
  > Al Jazeera’s Emma Withrow reports from a Free Palestine march, where Jewish demonstrators rejected Netanyahu.

## T020
**A** (2 item(s))
- 2026-09-28T15:38 [Al Jazeera] At least 33 killed after Myanmar military air strike hits market
  > Dozens of people have been killed in a military air strike on an opposition-controlled area of Rakhine State, Myanmar.
- 2026-09-28T19:31 [Al Jazeera] Myanmar army air strike kills dozens in Rakhine state
  > Nearly half a million people are displaced in Rakhine as a result of the conflict between the military and rebel groups.
**B** (3 item(s))
- 2026-09-29T06:06 [BBC World] Malaysia begins controversial repatriation of asylum seekers to Myanmar
  > Human rights groups say some 5,000 returnees could face violence, persecution and forced conscription.
- 2026-09-29T07:00 [South China Morning Post] Malaysia begins sending thousands of Myanmar nationals back to war-torn homeland
  > Malaysia began an operation to send nearly 1,500 Myanmar nationals back to their war-torn homeland on Tuesday, pressing ahead with a government-to-government repatriation deal despite warnings that returnees could face persecution and forced conscription.
The first group of 1,476 is part of an agree
- 2026-09-29T09:27 [Al Jazeera] Malaysia begins sending back Rohingya refugees despite safety warnings
  > About 1,500 refugees are to be sent back in the first phase, despite criticism from rights groups.

## T021
**A** (4 item(s))
- 2026-08-31T00:00 [Al Jazeera] Iran war live: IRGC attacks US bases in Jordan after US bombs Larak Island
  > US Central Command says its forces bombed two rocket launchers of the IRGC on Larak Island.
- 2026-08-31T00:00 [Al Jazeera] Iran war live: Tehran says it attacked bases in Jordan, UAE after US strike
  > CENTCOM says US forces bombed two IRGC rocket launchers on Larak Island which presented an &#039;imminent threat&#039;.
- 2026-08-31T03:06 [Al Jazeera] Iran targets Jordan after first US attack in a month
  > The US has launched its first strikes on Iran in a month, hitting sites on Larak Island. Iran hit back targeting bases h
- 2026-08-31T09:19 [Al Jazeera] Iran attacks Jordan, UAE after US bombs Larak Island: What’s the latest?
  > The retaliatory attacks came after the US targeted two Iranian launchers on Larak Island in the Strait of Hormuz.
**B** (1 item(s))
- 2026-08-31T11:25 [Al Jazeera] UAE intercepts drone after US and Iran exchange attacks
  > The UAE says it intercepted a drone coming from Iran and rejected &#039;false&#039; reports of an attack on its Al Menhad airbase.

## T022
**A** (1 item(s))
- 2026-09-28T18:28 [South China Morning Post] US to grant sanctions waiver for flights between Iran and Iraq’s Najaf, source says
  > US President Donald Trump’s administration was set to grant a limited waiver to its Iran sanctions programme on Monday to allow for flights carrying Shiite Muslim religious pilgrims between Iran and Iraq, a person with direct knowledge of the matter said.
The source, who is involved ‌in the delibera
**B** (1 item(s))
- 2026-09-29T00:00 [Al Jazeera] Iran war live: Trump says he did not offer Tehran sanctions relief
  > US President Trump rejects a news report claiming his administration offered Iran sanctions relief and frozen funds.

## T023
**A** (1 item(s))
- 2026-09-28T18:50 [Al Jazeera] Flights between Iraq’s Najaf and Iran resumed as Tehran protests US curbs
  > Tehran filed a UN complaint against US sanctions forcing regional cancellations of Iran flights.
**B** (1 item(s))
- 2026-09-29T00:00 [Al Jazeera] Iran war live: Trump says he did not offer Tehran sanctions relief
  > US President Trump rejects a news report claiming his administration offered Iran sanctions relief and frozen funds.

## T024
**A** (1 item(s))
- 2026-08-21T00:00 [South China Morning Post] Japan faces ‘nightmare scenario’ as it struggles to defend ICC judge
  > Japan has spent years casting the International Criminal Court as a pillar of the rules-based order. This week, its closest ally sanctioned the Japanese judge who leads it.
The move has left Tokyo in an uncomfortable bind: defend Tomoko Akane, the Japanese president of The Hague-based court, and ris
**B** (1 item(s))
- 2026-08-21T09:15 [South China Morning Post] Japan seeks record US$56 billion defence push amid growing regional tensions
  > Japan is preparing to spend more than ever on defence as analysts say Tokyo is being forced to respond to a convergence of regional threats, fast-changing military technology and growing uncertainty over the reliability of the US security umbrella.
The defence ministry is preparing to request a reco

## T025
**A** (1 item(s))
- 2026-09-29 21:32 [BBC World] More than 400 detained as France student protests escalate
  > Students have been protesting against conditions and resources in secondary schools since last week.
**B** (1 item(s))
- 2026-09-30 13:18 [BBC World] Dozens hurt and hundreds arrested in wave of French school protests
  > Students have been protesting against conditions and resources in secondary schools since last week.

## T026
**A** (1 item(s))
- 2026-08-21T15:58 [BBC World] UK, Canada and Australia condemn Israel for refusing criminal probe into aid worker killings in Gaza
  > Seven World Central Kitchen workers were killed in the Israeli strike on their convoy in 2024.
**B** (2 item(s))
- 2026-08-22T14:37 [Al Jazeera] Israeli drone strike on ‘civilian vehicle’ injures several in Syria
  > Syria condemns attack in southwest as a &#039;flagrant violation of sovereignty&#039; and a &#039;blatant breach of international law&#039;.
- 2026-08-22T21:42 [BBC World] Syria says Israeli strike near Damascus violation of international law
  > The latest incident comes days after reports emerged Israel had struck a military airbase close to the Turkish border.

## T027
**A** (1 item(s))
- 2026-09-29T00:30 [South China Morning Post] Can Hong Kong protect its eco-sensitive sites amid ‘golden week’ overtourism fears?
  > Hong Kong is bracing for a surge of mainland Chinese visitors to its eco-sensitive areas during the National Day “golden week” holiday, as strong interest in countryside attractions raises questions over whether the city can absorb crowds without overwhelming popular sites.
A review of discussions o
**B** (1 item(s))
- 2026-09-29T03:00 [South China Morning Post] 5 things to do over the National Day ‘golden week’ holiday in Hong Kong
  > Hong Kong is set to welcome 1.29 million mainland Chinese visitors over the National Day “golden week” break, fuelling questions online about what locals and tourists can do during the celebrations.
On popular mainland social media platform RedNote, many users have recommended a range of activities,

## T028
**A** (1 item(s))
- 2026-09-29 21:05 [France 24] Trump says he doesn't want to work with China on AI safety
  > US President Donald Trump discussed AI development with dozens of tech bosses at the White House on Tuesday. Ahead of his "super intelligence" luncheon, Trump launched a new AI-powered website for government services, vowing not to stifle the technology's growth. He also said he didn't want to work 
**B** (1 item(s))
- 2026-09-29 22:48 [France 24] AI companies sign voluntary accord on safety with Trump
  > US President Donald Trump and leaders of major AI companies signed a voluntary accord Tuesday to strengthen safety as the technology faces growing public concern. The agreement calls for internal controls, independent audits and board oversight while Trump rejected calls for government restrictions 

## T029
**A** (1 item(s))
- 2026-09-27T14:36 [Al Jazeera] Strait of Hormuz tensions linger as Iran and US move further from a deal
  > There are fears of renewed fighting between the US and Iran, after President Trump rejected a deal.
**B** (2 item(s))
- 2026-09-27T17:46 [Al Jazeera] ‘Iran ready for doomsday war’, FM Araghchi says
  > Foreign Minister Abbas Araghchi says Iran is prepared for war to resume, ‘even if it comes to a doomsday war’.
- 2026-09-28T00:00 [Al Jazeera] Iran war live: Tehran open to ‘real diplomacy’, ready for ‘apocalyptic war’
  > Abbas Araghchi&#039;s warning comes after Washington rejected a seven-day roadmap to end the war and reopen Strait of Hormuz.

## T030
**A** (1 item(s))
- 2026-08-21T00:00 [Al Jazeera] Iran war live: US vows toughest Iran sanctions, urges China support
  > US Treasury Secretary Bessent says new economic measures will &#039;collapse&#039; Iranian government.
**B** (1 item(s))
- 2026-08-22T09:14 [Al Jazeera] Iran says new US sanctions violate sovereignty of other states
  > Foreign Ministry spokesman Esmaeil Baghaei slams Trump&#039;s latest threat as a return to &#039;full-scale classic colonialism&#039;.

## T031
**A** (1 item(s))
- 2026-09-28T15:29 [Al Jazeera] Iran denies link to attack on airbase as UK minister warns of ‘proxies’
  > Tehran condemns &#039;unfounded and malicious speculation&#039;; British FM vows to &#039;act against the proxies of Iran&#039;.
**B** (1 item(s))
- 2026-09-29T00:00 [Al Jazeera] Iran war live: Trump says he did not offer Tehran sanctions relief
  > US President Trump rejects a news report claiming his administration offered Iran sanctions relief and frozen funds.

## T032
**A** (1 item(s))
- 2026-09-29 21:00 [France 24] Safeguards 'build a moat' around US AI firms, prevent open-source models from advancing, expert says
  > US President Donald Trump on Tuesday said the tech executives gathered at the White House to discuss regulating AI had signed a "morally binding" commitment to build adequate safeguards on the fast-moving technology. Speaking with FRANCE 24's Monte Francis, Harrison Rolfes, Senior Research Analyst a
**B** (1 item(s))
- 2026-09-29 22:48 [France 24] AI companies sign voluntary accord on safety with Trump
  > US President Donald Trump and leaders of major AI companies signed a voluntary accord Tuesday to strengthen safety as the technology faces growing public concern. The agreement calls for internal controls, independent audits and board oversight while Trump rejected calls for government restrictions 

## T033
**A** (1 item(s))
- 2026-09-29 14:45 [GDELT] Iran rial crashes past 2 . 5 million per dollar : War , sanctions push currency to new low
  > Domain: livemint.com | Language: English | Source country: India
**B** (3 item(s))
- 2026-09-29 22:45 [Clarín Mundo] Por la guerra y la incertidumbre económica, la moneda de Irán se hunde en un mínimo histórico
  > Las sanciones internacionales presionan a las finanzas de la república islámica. El régimen abre la puerta a nuevas negociaciones con Estados Unidos para terminar con el conflicto.
- 2026-09-30 01:15 [GDELT] Iran Currency Hits a New Record Low as War Erodes the Country Economic Stability
  > Domain: english.aawsat.com | Language: English | Source country: Syria
- 2026-09-30 08:42 [Europa Press Internacional] Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz
  > El Gobierno de Irán ha confirmado este miércoles que ha recibido la respuesta oficial de Estados Unidos a su propuesta para reactivar el proceso de conversaciones para un acuerdo de paz, días después de que el presidente estadounidense, Donald Trump, expresara su rechazo al plan presentado por Teher

## T034
**A** (1 item(s))
- 2026-09-29 17:54 [South China Morning Post] 87-year-old woman whose eviction sparked protests in Spain is returning home
  > Spain’s coalition government said it had agreed on proposals including banning evictions until 2030 to address the country’s housing crisis, as the 87-year-old woman whose forced removal last week triggered protests accepted an offer to return home.
Hundreds of ‌people remained camped in one of Madr
**B** (1 item(s))
- 2026-09-29 21:02 [Al Jazeera] Spain protests: Evicted 87-year-old woman to return to Madrid home
  > The real estate firm backs down and restores her old rent after mass protests over Spain&#039;s housing crisis.

## T035
**A** (1 item(s))
- 2026-09-28 12:00 [UN News] Security Council LIVE: Ambassadors meet as West Bank tensions rise, Gaza plan stalls
  > The Security Council met Monday morning with prospects for peace in the Middle East under strain on two fronts. In the West Bank, settler violence and settlement expansion are raising fears for a two-State solution. In Gaza, a year-old peace plan has stalled while civilian suffering continues. The m
**B** (3 item(s))
- 2026-09-28 23:02 [UN Press] Security Council, 10232nd Meeting (AM) Democratic Republic of the Congo/MONUSCO
  > Following its meeting concerning Haiti, the Council will convene to consider the situation in the Democratic Republic of the Congo. Anticipated briefers include James Swan, Head of the United Nations Organization Stabilization Mission in the Democratic Republic of the Congo (MONUSCO), as well as a r
- 2026-09-29 12:00 [UN News] Security Council LIVE: DRC peace deals fail to halt fighting as Ebola deepens crisis
  > The Security Council met in New York&nbsp;on the Democratic Republic of the Congo (DRC) Tuesday, where clashes between Government forces and M23 rebels continue in the east, despite a series of peace agreements. Ambassadors focused on ceasefire monitoring, rising tensions between the DRC and Rwanda 
- 2026-09-29 21:52 [UN Press] Commitments Must Yield Tangible Progress in Democratic Republic of Congo, Special Representative Tells Security Council
  > Serious challenges remain despite sustained diplomatic engagement to address the conflict in the eastern part of the Democratic Republic of the Congo, the Security Council heard today, as speakers welcomed the ceasefire monitoring and verification conducted by the UN mission in that country.

## T036
**A** (1 item(s))
- 2026-08-31T00:43 [South China Morning Post] At your service: Hong Kong welcomes first humanoid robot-run convenience stores
  > Hong Kong’s first convenience stores operated by humanoid robots will open on Tuesday, with the Beijing-based company behind it planning to establish about 10 more outlets locally as it makes the city its first stop in “going overseas”.
Following an opening ceremony on Monday, the first “Galbot stor
**B** (1 item(s))
- 2026-08-31T00:43 [South China Morning Post] Hong Kong can play unique role in fostering robotics industry: Paul Chan
  > Hong Kong can serve a unique role in the development of the robotics industry, the financial chief has said as he welcomed the coming opening of the city’s first convenience stores operated by humanoid robots developed by a Beijing-based company.
Following an opening ceremony on Monday, the first “G

## T037
**A** (1 item(s))
- 2026-09-27T00:00 [Al Jazeera] Iran war live: Tehran awaits official response as Trump rejects Hormuz plan
  > US president rejects Iran&#039;s seven-day plan to reopen the Strait of Hormuz, saying the deal is not &#039;acceptable&#039;.
**B** (1 item(s))
- 2026-09-27T19:16 [South China Morning Post] Trump expects new Iran talks despite rejecting deal offer
  > US President Donald Trump said on Sunday that he expects talks with Iran to resume in the coming week, despite his rejection of a truce proposal put forward by Tehran.
Iranian officials brought with them to the UN General Assembly in New York a plan for a seven-day truce followed by the reopening of

## T038
**A** (1 item(s))
- 2026-08-21T13:47 [Al Jazeera] Trump’s ‘economic D-Day’ claims first victim: Not Iran, but US markets
  > The US and Israel&#039;s war on Iran has upended global financial and energy markets.
**B** (1 item(s))
- 2026-08-22T09:14 [Al Jazeera] Iran says new US sanctions violate sovereignty of other states
  > Foreign Ministry spokesman Esmaeil Baghaei slams Trump&#039;s latest threat as a return to &#039;full-scale classic colonialism&#039;.

## T039
**A** (1 item(s))
- 2026-09-29 16:30 [GDELT]   This is how the war will end : Iran currency hits new record low
  > Domain: fortune.com | Language: English | Source country: United States
**B** (3 item(s))
- 2026-09-29 22:45 [Clarín Mundo] Por la guerra y la incertidumbre económica, la moneda de Irán se hunde en un mínimo histórico
  > Las sanciones internacionales presionan a las finanzas de la república islámica. El régimen abre la puerta a nuevas negociaciones con Estados Unidos para terminar con el conflicto.
- 2026-09-30 01:15 [GDELT] Iran Currency Hits a New Record Low as War Erodes the Country Economic Stability
  > Domain: english.aawsat.com | Language: English | Source country: Syria
- 2026-09-30 08:42 [Europa Press Internacional] Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz
  > El Gobierno de Irán ha confirmado este miércoles que ha recibido la respuesta oficial de Estados Unidos a su propuesta para reactivar el proceso de conversaciones para un acuerdo de paz, días después de que el presidente estadounidense, Donald Trump, expresara su rechazo al plan presentado por Teher

## T040
**A** (1 item(s))
- 2026-10-01 02:35 [Al Jazeera] Christa Pike’s execution by lethal injection fails in Tennessee
  > Witnesses say Tennessee officials were unable to execute Christa Pike after a lethal injection attempt.
**B** (5 item(s))
- 2026-10-01 16:45 [BBC World] Tennessee halts executions after Christa Pike survives two lethal injection attempts
  > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
- 2026-10-02 03:02 [South China Morning Post] Christa Pike in ‘life-saving care’ after botched Tennessee execution
  > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from a prison execution c
- 2026-10-02 07:58 [Al Jazeera] Lawyers for US inmate who survived lethal injections demand release
  > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
- 2026-10-02 20:32 [BBC World] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say
  > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.

## T041
**A** (1 item(s))
- 2026-10-01 04:14 [South China Morning Post] Tennessee halts executions after Christa Pike survives 2 doses of lethal drug
  > Tennessee officials were unable to put Christa Pike to death on Wednesday for a 1995 murder after administering two doses of a lethal drug. A death penalty expert said it was an unprecedented failure, and Tennessee’s governor halted the remaining execution for the rest of the year.
Pike, 50, was ali
**B** (5 item(s))
- 2026-10-01 16:45 [BBC World] Tennessee halts executions after Christa Pike survives two lethal injection attempts
  > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
- 2026-10-02 03:02 [South China Morning Post] Christa Pike in ‘life-saving care’ after botched Tennessee execution
  > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from a prison execution c
- 2026-10-02 07:58 [Al Jazeera] Lawyers for US inmate who survived lethal injections demand release
  > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
- 2026-10-02 20:32 [BBC World] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say
  > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.

## T042
**A** (1 item(s))
- 2026-09-27T13:17 [Al Jazeera] ‘Better deal’: What’s behind Trump’s rejection of Iran’s truce offer?
  > Experts say Trump sees economic sanctions as key to extracting more concessions but he risks losing leverage.
**B** (1 item(s))
- 2026-09-27T19:16 [South China Morning Post] Trump expects new Iran talks despite rejecting deal offer
  > US President Donald Trump said on Sunday that he expects talks with Iran to resume in the coming week, despite his rejection of a truce proposal put forward by Tehran.
Iranian officials brought with them to the UN General Assembly in New York a plan for a seven-day truce followed by the reopening of

## T043
**A** (1 item(s))
- 2026-08-21T12:12 [Al Jazeera] US designates Hezbollah an Iranian proxy, sanctions funding network
  > The US Treasury labels Lebanon-based group &#039;an extension&#039; of the IRGC&#039;s Quds Force and takes aim at financing.
**B** (1 item(s))
- 2026-08-22T09:14 [Al Jazeera] Iran says new US sanctions violate sovereignty of other states
  > Foreign Ministry spokesman Esmaeil Baghaei slams Trump&#039;s latest threat as a return to &#039;full-scale classic colonialism&#039;.

## T044
**A** (1 item(s))
- 2026-09-28T13:18 [South China Morning Post] Hong Kong checkpoints to handle 7.44 million passenger trips for National Day break
  > Hong Kong’s checkpoints are expected to handle about 7.44 million passenger trips over mainland China’s National Day “golden week” break, while people movements are anticipated to peak this weekend.
The Immigration Department said on Monday that the figure would include inbound and outbound trips by
**B** (1 item(s))
- 2026-09-29T03:00 [South China Morning Post] 5 things to do over the National Day ‘golden week’ holiday in Hong Kong
  > Hong Kong is set to welcome 1.29 million mainland Chinese visitors over the National Day “golden week” break, fuelling questions online about what locals and tourists can do during the celebrations.
On popular mainland social media platform RedNote, many users have recommended a range of activities,

## T045
**A** (1 item(s))
- 2026-09-27T07:44 [BBC World] Iranian minister says only negotiation can end conflict after Trump rejects Hormuz deal
  > The foreign minister says Tehran is waiting for an official rejection of a deal, despite the US President's comments.
**B** (1 item(s))
- 2026-09-27T14:36 [Al Jazeera] Strait of Hormuz tensions linger as Iran and US move further from a deal
  > There are fears of renewed fighting between the US and Iran, after President Trump rejected a deal.

