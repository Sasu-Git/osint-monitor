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

**Cases:** 45. Draft labels: AMBIGUOUS 2, NO_RELATION 30, commentary_on 2, follow_up_to 5, reaction_to 4, same_attack_wave 1, same_convened_event 1.

| Case | A | B | Draft label | Direction | Confidence |
|---|---|---|---|---|---|
| [T001](#t001) | Carney faces crucial test after walking away from Trump's de | Carney calls Trump's fresh tariffs a 'miscalculation' after  | NO_RELATION | none | medium |
| [T002](#t002) | US allies in Asia wary as Trump moves military assets for Ir | Iran says new US sanctions violate sovereignty of other stat | NO_RELATION | none | high |
| [T003](#t003) | Malaysia repatriates Myanmar migrants despite UN warnings | World News in Brief: Deadly Myanmar strikes as Malaysia begi | AMBIGUOUS | none | low |
| [T004](#t004) | Contrasting treatment of Israel and Palestine on display at  | Jewish protestors join Free Palestine march to denounce Neta | NO_RELATION | none | medium |
| [T005](#t005) | Trump expects new Iran talks despite rejecting deal offer | Why has Trump rejected Iran’s peace proposal? | NO_RELATION | none | medium |
| [T006](#t006) | Ben-Gvir releases video threatening to kill senior Hamas fig | Palestinians denounce Israeli minister Ben-Gvir’s threats ag | reaction_to | B->A | high |
| [T007](#t007) | ‘Better deal’: What’s behind Trump’s rejection of Iran’s tru | Strait of Hormuz tensions linger as Iran and US move further | NO_RELATION | none | medium |
| [T008](#t008) | Spain announces new housing measures after protests over 87- | Spain announces ban on evictions after protests over 87-year | NO_RELATION | none | high |
| [T009](#t009) | Malaysia begins controversial repatriation of asylum seekers | Malaysia gave refuge to Rohingya; now it wants them to go | commentary_on | B->A | medium |
| [T010](#t010) | Trump made the right decision to reject Iran’s offer | Iran war live: Trump says he did not offer Tehran sanctions  | NO_RELATION | none | medium |
| [T011](#t011) | Secretary of War Pete Hegseth Signs Directive to Defend 2026 | What Will Hegseth’s “State of the Force” Reprise Reveal? | NO_RELATION | none | high |
| [T012](#t012) | US Supreme Court denies Christa Pike's last-ditch bid to hal | Tennessee halts executions after Christa Pike survives two l | follow_up_to | B->A | medium |
| [T013](#t013) | US appeals court halts Tennessee execution of Christa Pike | Tennessee halts executions after Christa Pike survives two l | follow_up_to | B->A | medium |
| [T014](#t014) | US Tennessee’s first execution of a woman in 200 years halte | Tennessee halts executions after Christa Pike survives two l | follow_up_to | B->A | medium |
| [T015](#t015) | Hong Kong, Singapore aren’t ‘enemies’, our competition is he | Hong Kong can play unique role in fostering robotics industr | NO_RELATION | none | high |
| [T016](#t016) | Security Council, 10231st Meeting (AM) Haiti | Security Council, 10232nd Meeting (AM) Democratic Republic o | NO_RELATION | none | medium |
| [T017](#t017) | Israeli soldiers throw belongings from besieged Palestinian  | Israeli drone strike on ‘civilian vehicle’ injures several i | NO_RELATION | none | high |
| [T018](#t018) | Iran war live: Tehran awaits official response as Trump reje | Iranian minister says only negotiation can end conflict afte | reaction_to | B->A | medium |
| [T019](#t019) | More than 100 arrested as New Yorkers protest Netanyahu’s UN | Jewish protestors join Free Palestine march to denounce Neta | NO_RELATION | none | low |
| [T020](#t020) | At least 33 killed after Myanmar military air strike hits ma | Malaysia begins controversial repatriation of asylum seekers | NO_RELATION | none | high |
| [T021](#t021) | Iran war live: IRGC attacks US bases in Jordan after US bomb | UAE intercepts drone after US and Iran exchange attacks | same_attack_wave | none | medium |
| [T022](#t022) | US to grant sanctions waiver for flights between Iran and Ir | Iran war live: Trump says he did not offer Tehran sanctions  | NO_RELATION | none | medium |
| [T023](#t023) | Flights between Iraq’s Najaf and Iran resumed as Tehran prot | Iran war live: Trump says he did not offer Tehran sanctions  | NO_RELATION | none | high |
| [T024](#t024) | Japan faces ‘nightmare scenario’ as it struggles to defend I | Japan seeks record US$56 billion defence push amid growing r | NO_RELATION | none | high |
| [T025](#t025) | More than 400 detained as France student protests escalate | Dozens hurt and hundreds arrested in wave of French school p | NO_RELATION | none | medium |
| [T026](#t026) | UK, Canada and Australia condemn Israel for refusing crimina | Israeli drone strike on ‘civilian vehicle’ injures several i | NO_RELATION | none | high |
| [T027](#t027) | Can Hong Kong protect its eco-sensitive sites amid ‘golden w | 5 things to do over the National Day ‘golden week’ holiday i | NO_RELATION | none | high |
| [T028](#t028) | Trump says he doesn't want to work with China on AI safety | AI companies sign voluntary accord on safety with Trump | same_convened_event | none | high |
| [T029](#t029) | Strait of Hormuz tensions linger as Iran and US move further | ‘Iran ready for doomsday war’, FM Araghchi says | NO_RELATION | none | medium |
| [T030](#t030) | Iran war live: US vows toughest Iran sanctions, urges China  | Iran says new US sanctions violate sovereignty of other stat | reaction_to | B->A | medium |
| [T031](#t031) | Iran denies link to attack on airbase as UK minister warns o | Iran war live: Trump says he did not offer Tehran sanctions  | NO_RELATION | none | high |
| [T032](#t032) | Safeguards 'build a moat' around US AI firms, prevent open-s | AI companies sign voluntary accord on safety with Trump | commentary_on | A->B | medium |
| [T033](#t033) | Iran rial crashes past 2 . 5 million per dollar : War , sanc | Por la guerra y la incertidumbre económica, la moneda de Irá | NO_RELATION | none | medium |
| [T034](#t034) | 87-year-old woman whose eviction sparked protests in Spain i | Spain protests: Evicted 87-year-old woman to return to Madri | NO_RELATION | none | high |
| [T035](#t035) | Security Council LIVE: Ambassadors meet as West Bank tension | Security Council, 10232nd Meeting (AM) Democratic Republic o | NO_RELATION | none | high |
| [T036](#t036) | At your service: Hong Kong welcomes first humanoid robot-run | Hong Kong can play unique role in fostering robotics industr | reaction_to | B->A | medium |
| [T037](#t037) | Iran war live: Tehran awaits official response as Trump reje | Trump expects new Iran talks despite rejecting deal offer | follow_up_to | B->A | low |
| [T038](#t038) | Trump’s ‘economic D-Day’ claims first victim: Not Iran, but  | Iran says new US sanctions violate sovereignty of other stat | NO_RELATION | none | medium |
| [T039](#t039) |   This is how the war will end : Iran currency hits new reco | Por la guerra y la incertidumbre económica, la moneda de Irá | NO_RELATION | none | medium |
| [T040](#t040) | Christa Pike’s execution by lethal injection fails in Tennes | Tennessee halts executions after Christa Pike survives two l | follow_up_to | B->A | low |
| [T041](#t041) | Tennessee halts executions after Christa Pike survives 2 dos | Tennessee halts executions after Christa Pike survives two l | NO_RELATION | none | medium |
| [T042](#t042) | ‘Better deal’: What’s behind Trump’s rejection of Iran’s tru | Trump expects new Iran talks despite rejecting deal offer | NO_RELATION | none | medium |
| [T043](#t043) | US designates Hezbollah an Iranian proxy, sanctions funding  | Iran says new US sanctions violate sovereignty of other stat | AMBIGUOUS | none | low |
| [T044](#t044) | Hong Kong checkpoints to handle 7.44 million passenger trips | 5 things to do over the National Day ‘golden week’ holiday i | NO_RELATION | none | high |
| [T045](#t045) | Iranian minister says only negotiation can end conflict afte | Strait of Hormuz tensions linger as Iran and US move further | NO_RELATION | none | medium |

---

## T001

**Development A** `2026-08-21:carney-crucial-test-analysis`

- **Members:** 2 item(s)
- **Sources:** BBC World
- **Times:** 2026-08-22T16:20 to 2026-08-22T20:02 UTC
- **Actors:** Carney, Trump, White House
- **Places:** Canada
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T16:20 [BBC World] **Carney faces crucial test after walking away from Trump's deal**
    > The Canadian prime minister will have to sell his gamble that walking away from talks with the White House will be worth the consequences.
  - 2026-08-22T20:02 [BBC World] **Carney faces crucial test after walking away from Trump's deal**
    > The Canadian prime minister will have to sell his gamble that walking away from talks with the White House will be worth the consequences.

**Development B** `2026-08-21:carney-retaliatory-tariffs`

- **Members:** 2 item(s)
- **Sources:** BBC World
- **Times:** 2026-08-22T18:20 to 2026-08-22T20:10 UTC
- **Actors:** Canada, Carney, Donald Trump, Mark Carney, Trump
- **Places:** Canada, US
- **System Development:** D4
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T18:20 [BBC World] **Carney calls Trump's fresh tariffs a 'miscalculation' after trade talks collapse**
    > Canada's prime minister said he was "reluctantly" announcing retaliatory tariffs as he accused the US of starting a trade war.
  - 2026-08-22T20:10 [BBC World] **Carney calls Trump's fresh tariffs a 'miscalculation' after trade talks collapse**
    > Canada's prime minister said he was "reluctantly" announcing retaliatory tariffs as he accused the US of starting a trade war.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | third_event |

**Rationale:** A is analysis of Carney 'walking away from talks' and B is Carney's retaliatory tariffs 'after trade talks collapse'; both hang on the talks collapse/Trump tariffs, and neither names the other.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T002

**Development A** `2026-08-21:asian-allies-wary-us-assets-iran-war`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-21T12:32 to 2026-08-21T12:32 UTC
- **Actors:** Trump
- **Places:** Asia, China, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T12:32 [Al Jazeera] **US allies in Asia wary as Trump moves military assets for Iran war**
    > Allies worry about the US ability to deter China, even if the bulk of US forces remain in the region.

**Development B** `2026-08-21:iran-rejects-new-us-sanctions`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-22T09:14 to 2026-08-22T09:14 UTC
- **Actors:** Esmaeil Baghaei, Foreign Ministry, Trump
- **Places:** Iran, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T09:14 [Al Jazeera] **Iran says new US sanctions violate sovereignty of other states**
    > Foreign Ministry spokesman Esmaeil Baghaei slams Trump&#039;s latest threat as a return to &#039;full-scale classic colonialism&#039;.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** A covers allies' wariness over US asset moves; B is Iran condemning new US sanctions. They share only the US-Iran context.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T003

**Development A** `2026-09-30-multilingual:sx-150`

- **Members:** 1 item(s)
- **Sources:** DW World
- **Times:** 2026-09-29T10:26 to 2026-09-29T10:26 UTC
- **Actors:** United Nations
- **Places:** Malaysia, Myanmar
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 10:26 [DW World] **Malaysia repatriates Myanmar migrants despite UN warnings**
    > Malaysia has started repatriating about 1,500 Myanmar nationals, defying warnings from the UN and rights groups. Malaysia, facing an uptick in anti-migrant sentiment, says the program is strictly voluntary.

**Development B** `2026-09-30-multilingual:sx-396`

- **Members:** 1 item(s)
- **Sources:** UN News
- **Times:** 2026-09-29T12:00 to 2026-09-29T12:00 UTC
- **Actors:** Rakhine, United Nations, World News
- **Places:** Gaza, Malaysia, Myanmar, West Bank
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 12:00 [UN News] **World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, new emergency funding released, Gaza and West Bank update**
    > The UN chief on Tuesday strongly condemned an airstrike that reportedly killed at least 50 people at a market in Myanmar’s Rakhine state and called for those responsible to be held to account.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `AMBIGUOUS` | none | low | none |

**Rationale:** B is a UN news roundup whose headline includes 'Malaysia begins deportations' (the same occurrence as A), but its lead text is the UN chief condemning a Myanmar airstrike, so it is unclear what B's Development is.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T004

**Development A** `2026-09-25:israel-palestine-treatment-at-un`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-25T02:26 to 2026-09-25T02:26 UTC
- **Actors:** UN General Assembly, UN Israel's Prime
- **Places:** Israel, Palestine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T02:26 [Al Jazeera] **Contrasting treatment of Israel and Palestine on display at the UN**
    > Israel’s Prime Minister addressed the UN General Assembly in person, despite having an ICC arrest warrant.

**Development B** `2026-09-25:jewish-march-against-netanyahu`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-25T03:49 to 2026-09-25T03:49 UTC
- **Actors:** Al Jazeera, Benjamin Netanyahu, Emma Withrow, Jewish
- **Places:** Palestine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T03:49 [Al Jazeera] **Jewish protestors join Free Palestine march to denounce Netanyahu**
    > Al Jazeera’s Emma Withrow reports from a Free Palestine march, where Jewish demonstrators rejected Netanyahu.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | third_event |

**Rationale:** A covers the contrasting treatment around Netanyahu's UNGA address and B a march 'to denounce Netanyahu'. Both relate to his UN appearance, and neither refers to the other.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T005

**Development A** `2026-09-27-live:trump-expects-new-iran-talks`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-27T19:16 to 2026-09-27T19:16 UTC
- **Actors:** Axios, Donald Trump, Iran, Tehran, Trump, UN General Assembly, US, Washington
- **Places:** Iran, New York, Strait of Hormuz, Tehran, US
- **System Development:** D3
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-27T19:16 [South China Morning Post] **Trump expects new Iran talks despite rejecting deal offer**
    > US President Donald Trump said on Sunday that he expects talks with Iran to resume in the coming week, despite his rejection of a truce proposal put forward by Tehran.
Iranian officials brought with them to the UN General Assembly in New York a plan for a seven-day truce followed

**Development B** `2026-09-27-live:why-trump-rejected-explainer`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T20:03 to 2026-09-27T20:03 UTC
- **Actors:** Trump
- **Places:** Iran, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T20:03 [Al Jazeera] **Why has Trump rejected Iran’s peace proposal?**
    > The US president has reportedly threatened to resume strikes on Iran.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | third_event |

**Rationale:** B ('Why has Trump rejected Iran's peace proposal?') is commentary on the rejection, while A's occurrence is Trump saying he 'expects talks with Iran to resume'. The rejection is a third occurrence.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T006

**Development A** `2026-09-27-live:ben-gvir-threat-video`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T01:33 to 2026-09-28T01:33 UTC
- **Actors:** Ben-Gvir, Hamas, Hassan Salameh, Itamar Ben-Gvir
- **Places:** Israel
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T01:33 [Al Jazeera] **Ben-Gvir releases video threatening to kill senior Hamas figure in jail**
    > Israel’s security minister Itamar Ben-Gvir has released a video in which he is seen threatening to kill Hassan Salameh.

**Development B** `2026-09-27-live:palestinians-denounce-ben-gvir`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T10:11 to 2026-09-28T10:11 UTC
- **Actors:** Ben-Gvir, Hassan Salama
- **Places:** Israel, Palestine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T10:11 [Al Jazeera] **Palestinians denounce Israeli minister Ben-Gvir’s threats against prisoner**
    > Footage of national security minister taunting Hassan Salama in his cell draws sharp condemnation from Palestinians.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `reaction_to` | B->A | high | none |

**Rationale:** B: 'Palestinians denounce Israeli minister Ben-Gvir's threats against prisoner', and its footage of him 'taunting Hassan Salama in his cell' is A's video.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T007

**Development A** `2026-09-27-live:behind-trump-rejection-analysis`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T13:17 to 2026-09-27T13:17 UTC
- **Actors:** Trump
- **Places:** Iran
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T13:17 [Al Jazeera] **‘Better deal’: What’s behind Trump’s rejection of Iran’s truce offer?**
    > Experts say Trump sees economic sanctions as key to extracting more concessions but he risks losing leverage.

**Development B** `2026-09-27-live:hormuz-tensions-linger`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T14:36 to 2026-09-27T14:36 UTC
- **Actors:** Donald Trump, Iran, Tehran, Trump, US, Washington
- **Places:** Hormuz, Iran, US
- **System Development:** D3
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-27T14:36 [Al Jazeera] **Strait of Hormuz tensions linger as Iran and US move further from a deal**
    > There are fears of renewed fighting between the US and Iran, after President Trump rejected a deal.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | third_event |

**Rationale:** A is expert analysis of 'Trump's rejection of Iran's truce offer' and B reports lingering tensions 'after President Trump rejected a deal'. Both concern the rejection, not each other.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T008

**Development A** `2026-10-03-live:s-1124`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-29T12:14 to 2026-09-29T12:14 UTC
- **Actors:** none extracted
- **Places:** Spain
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 12:14 [BBC World] **Spain announces new housing measures after protests over 87-year-old woman's eviction**
    > The measures include a proposed ban on evictions until 2030 and the automatic renewal of tenant contracts.

**Development B** `2026-10-03-live:s-1316`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-29T16:23 to 2026-09-29T16:23 UTC
- **Actors:** none extracted
- **Places:** Spain
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 16:23 [BBC World] **Spain announces ban on evictions after protests over 87-year-old woman's removal from flat**
    > The ban is part of a number of proposals that must be approved in parliament within 30 days.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | SAME_DEVELOPMENT_SUSPECTED |

**Rationale:** Both report Spain announcing housing measures including an eviction ban 'after protests over 87-year-old woman's eviction', on the same day.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T009

**Development A** `2026-09-29-live:malaysia-repatriation-to-myanmar`

- **Members:** 3 item(s)
- **Sources:** Al Jazeera, BBC World, South China Morning Post
- **Times:** 2026-09-29T06:06 to 2026-09-29T09:27 UTC
- **Actors:** Malaysia
- **Places:** Kuala Lumpur, Malaysia, Myanmar
- **System Development:** D16
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T06:06 [BBC World] **Malaysia begins controversial repatriation of asylum seekers to Myanmar**
    > Human rights groups say some 5,000 returnees could face violence, persecution and forced conscription.
  - 2026-09-29T07:00 [South China Morning Post] **Malaysia begins sending thousands of Myanmar nationals back to war-torn homeland**
    > Malaysia began an operation to send nearly 1,500 Myanmar nationals back to their war-torn homeland on Tuesday, pressing ahead with a government-to-government repatriation deal despite warnings that returnees could face persecution and forced conscription.
The first group of 1,476
  - 2026-09-29T09:27 [Al Jazeera] **Malaysia begins sending back Rohingya refugees despite safety warnings**
    > About 1,500 refugees are to be sent back in the first phase, despite criticism from rights groups.

**Development B** `2026-09-29-live:malaysia-rohingya-analysis`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T11:22 to 2026-09-29T11:22 UTC
- **Actors:** Malaysia, Muslims, Rohingya
- **Places:** Malaysia, Myanmar
- **System Development:** D16
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T11:22 [Al Jazeera] **Malaysia gave refuge to Rohingya; now it wants them to go**
    > Malaysia welcomed persecuted Muslim minority but now plans to send them back to Myanmar amid rising hate against them.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `commentary_on` | B->A | medium | commentary |

**Rationale:** B ('Malaysia gave refuge to Rohingya; now it wants them to go') is an explainer on the repatriation that A reports as beginning ('Malaysia begins sending back Rohingya refugees').

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T010

**Development A** `2026-09-29-live:opinion-trump-reject-iran-offer`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T18:16 to 2026-09-28T18:16 UTC
- **Actors:** Trump
- **Places:** Iran, Tehran, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T18:16 [Al Jazeera] **Trump made the right decision to reject Iran’s offer**
    > The US president has denied Tehran the opportunity to use the US midterm elections as a pressure point.

**Development B** `2026-09-29-live:iran-war-live-no-sanctions-relief`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T00:00 to 2026-09-29T00:00 UTC
- **Actors:** Trump, US
- **Places:** Iran, Tehran, US
- **System Development:** D6
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-29T00:00 [Al Jazeera] **Iran war live: Trump says he did not offer Tehran sanctions relief**
    > US President Trump rejects a news report claiming his administration offered Iran sanctions relief and frozen funds.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | third_event |

**Rationale:** A is an opinion piece on Trump's rejection of Iran's offer and B is Trump denying a report that he offered sanctions relief. Neither refers to the other.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T011

**Development A** `2026-09-30-multilingual:sx-5`

- **Members:** 1 item(s)
- **Sources:** Defense.gov
- **Times:** 2026-09-28T20:30 to 2026-09-28T20:30 UTC
- **Actors:** Pete Hegseth, US Department of Defense
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28 20:30 [Defense.gov] **Secretary of War Pete Hegseth Signs Directive to Defend 2026 Elections From Foreign Threats**
    > Secretary of War Pete Hegseth signed a memorandum directing the War Department to mobilize a comprehensive, whole-of-government defense of the election infrastructure from foreign adversaries.

**Development B** `2026-09-30-multilingual:sx-428`

- **Members:** 1 item(s)
- **Sources:** War on the Rocks
- **Times:** 2026-09-29T16:00 to 2026-09-29T16:00 UTC
- **Actors:** Defense, Donald Trump, Hegseth, Pete Hegseth, US Department of Defense
- **Places:** U.S.
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 16:00 [War on the Rocks] **What Will Hegseth’s “State of the Force” Reprise Reveal?**
    > Secretary of Defense Pete Hegseth is expected to convene a high-profile meeting of military personnel for a &#8220;State of the Force&#8221; address this week. Will it show the U.S. armed forces as healthy? The answer may depend on how the audience responds, regardless of what He

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Hegseth's election-defence directive (A) and a preview of his 'State of the Force' address (B) share only an actor.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T012

**Development A** `2026-10-03-live:s-1245`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-29T23:39 to 2026-09-29T23:39 UTC
- **Actors:** Christa Pike, U.S. Supreme Court
- **Places:** Tennessee
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 23:39 [BBC World] **US Supreme Court denies Christa Pike's last-ditch bid to halt execution**
    > The Tennessee inmate has been awaiting execution since she was sentenced to death in 1996 for the murder of a teenage classmate.

**Development B** `2026-10-03-live:D9`

- **Members:** 5 item(s)
- **Sources:** Al Jazeera, BBC World, South China Morning Post
- **Times:** 2026-10-01T16:45 to 2026-10-02T20:57 UTC
- **Actors:** Christa Pike, Pike, Randy Spivey
- **Places:** Nashville, Tennessee, US
- **System Development:** D9
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 16:45 [BBC World] **Tennessee halts executions after Christa Pike survives two lethal injection attempts**
    > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
  - 2026-10-02 03:02 [South China Morning Post] **Christa Pike in ‘life-saving care’ after botched Tennessee execution**
    > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from 
  - 2026-10-02 07:58 [Al Jazeera] **Lawyers for US inmate who survived lethal injections demand release**
    > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
  - 2026-10-02 20:32 [BBC World] **US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say**
    > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `follow_up_to` | B->A | medium | none |

**Rationale:** Both are steps in the same Christa Pike execution case: A is the Supreme Court denying her 'last-ditch bid to halt execution' and B the botched execution and its aftermath.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T013

**Development A** `2026-10-03-live:s-1421`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-30T16:44 to 2026-09-30T16:44 UTC
- **Actors:** Christa Pike Christa Pike
- **Places:** Tennessee, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 16:44 [Al Jazeera] **US appeals court halts Tennessee execution of Christa Pike**
    > Christa Pike was set to become the first woman executed by Tennessee in more than 200 years.

**Development B** `2026-10-03-live:D9`

- **Members:** 5 item(s)
- **Sources:** Al Jazeera, BBC World, South China Morning Post
- **Times:** 2026-10-01T16:45 to 2026-10-02T20:57 UTC
- **Actors:** Christa Pike, Pike, Randy Spivey
- **Places:** Nashville, Tennessee, US
- **System Development:** D9
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 16:45 [BBC World] **Tennessee halts executions after Christa Pike survives two lethal injection attempts**
    > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
  - 2026-10-02 03:02 [South China Morning Post] **Christa Pike in ‘life-saving care’ after botched Tennessee execution**
    > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from 
  - 2026-10-02 07:58 [Al Jazeera] **Lawyers for US inmate who survived lethal injections demand release**
    > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
  - 2026-10-02 20:32 [BBC World] **US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say**
    > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `follow_up_to` | B->A | medium | none |

**Rationale:** A is the appeals court halting Pike's execution and B the later failed lethal injections in the same execution procedure.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T014

**Development A** `2026-10-03-live:s-1404`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-30T16:00 to 2026-09-30T16:00 UTC
- **Actors:** Christa Pike, Pike
- **Places:** Tennessee, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 16:00 [South China Morning Post] **US Tennessee’s first execution of a woman in 200 years halted**
    > A US appeal court on Wednesday halted the ⁠execution of death row inmate Christa Pike in Tennessee, less than two hours before she was scheduled to become the first woman that state has put to death in more than 200 years.
The 6th US Circuit Court of Appeals ordered a “short stay

**Development B** `2026-10-03-live:D9`

- **Members:** 5 item(s)
- **Sources:** Al Jazeera, BBC World, South China Morning Post
- **Times:** 2026-10-01T16:45 to 2026-10-02T20:57 UTC
- **Actors:** Christa Pike, Pike, Randy Spivey
- **Places:** Nashville, Tennessee, US
- **System Development:** D9
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 16:45 [BBC World] **Tennessee halts executions after Christa Pike survives two lethal injection attempts**
    > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
  - 2026-10-02 03:02 [South China Morning Post] **Christa Pike in ‘life-saving care’ after botched Tennessee execution**
    > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from 
  - 2026-10-02 07:58 [Al Jazeera] **Lawyers for US inmate who survived lethal injections demand release**
    > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
  - 2026-10-02 20:32 [BBC World] **US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say**
    > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `follow_up_to` | B->A | medium | none |

**Rationale:** A is the 6th Circuit's 'short stay of execution' for Pike and B the subsequent failed execution and aftermath in the same case.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T015

**Development A** `2026-08-31:singapore-envoy-hk-interview`

- **Members:** 2 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T00:00 to 2026-08-31T02:00 UTC
- **Actors:** Eric Teo Boon Hee
- **Places:** Asia, Hong Kong, Northern Metropolis, Singapore, South
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T00:00 [South China Morning Post] **Hong Kong, Singapore aren’t ‘enemies’, our competition is healthy, envoy says**
    > Singapore and Hong Kong do not view each other as enemies, but rather admire one another’s accomplishments, the country’s top envoy to the city has said, calling for greater cooperation between the two jurisdictions often cast as fierce rivals.
Eric Teo Boon Hee, Singapore’s cons
  - 2026-08-31T02:00 [South China Morning Post] **Singapore firms keen to tap Northern Metropolis’ ‘massive potential’, envoy says**
    > Singaporean businesses are keen to explore the “massive potential” emerging in Hong Kong’s Northern Metropolis megaproject after the country’s prime minister visited the site earlier this year, its top envoy to the city has said.
In an exclusive interview with the South China Mor

**Development B** `2026-08-31:paul-chan-robotics-role`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T00:43 to 2026-08-31T00:43 UTC
- **Actors:** Galbot, Hung Hom, Kai Tak, Paul Chan Hong Kong, Wan Chai
- **Places:** Beijing, China, Hong Kong
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T00:43 [South China Morning Post] **Hong Kong can play unique role in fostering robotics industry: Paul Chan**
    > Hong Kong can serve a unique role in the development of the robotics industry, the financial chief has said as he welcomed the coming opening of the city’s first convenience stores operated by humanoid robots developed by a Beijing-based company.
Following an opening ceremony on 

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** A is a Singapore envoy interview and B is Paul Chan on robotics. They share only the Hong Kong setting.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T016

**Development A** `2026-09-30-multilingual:sx-425`

- **Members:** 1 item(s)
- **Sources:** UN Press
- **Times:** 2026-09-28T23:02 to 2026-09-28T23:02 UTC
- **Actors:** Force, Gang Suppression Force, Haitian National Police, Office, UN Security Council, UN Support Office, United Nations
- **Places:** Haiti, Panama, U.S.
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28 23:02 [UN Press] **Security Council, 10231st Meeting (AM) Haiti**
    > The Security Council today is expected to vote on a draft resolution re-authorizing the Gang Suppression Force in Haiti, put forward by the United States and Panama, the co-penholders on Haiti. The Council first authorized the Force on 30 September 2025 under resolution 2793 (202

**Development B** `2026-09-30-multilingual:sx-423`

- **Members:** 3 item(s)
- **Sources:** UN News, UN Press
- **Times:** 2026-09-28T23:02 to 2026-09-29T21:52 UTC
- **Actors:** James Swan, M23, UN Security Council, United Nations, United Nations Organization Stabilization Mission
- **Places:** Congo, DRC, Democratic Republic, Democratic Republic of Congo, Democratic Republic of the Congo, Haiti, New York, Rwanda
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28 23:02 [UN Press] **Security Council, 10232nd Meeting (AM) Democratic Republic of the Congo/MONUSCO**
    > Following its meeting concerning Haiti, the Council will convene to consider the situation in the Democratic Republic of the Congo. Anticipated briefers include James Swan, Head of the United Nations Organization Stabilization Mission in the Democratic Republic of the Congo (MONU
  - 2026-09-29 12:00 [UN News] **Security Council LIVE: DRC peace deals fail to halt fighting as Ebola deepens crisis**
    > The Security Council met in New York&nbsp;on the Democratic Republic of the Congo (DRC) Tuesday, where clashes between Government forces and M23 rebels continue in the east, despite a series of peace agreements. Ambassadors focused on ceasefire monitoring, rising tensions between
  - 2026-09-29 21:52 [UN Press] **Commitments Must Yield Tangible Progress in Democratic Republic of Congo, Special Representative Tells Security Council**
    > Serious challenges remain despite sustained diplomatic engagement to address the conflict in the eastern part of the Democratic Republic of the Congo, the Security Council heard today, as speakers welcomed the ceasefire monitoring and verification conducted by the UN mission in t

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | none |

**Rationale:** These are two separate Security Council meetings, the 10231st on Haiti and the 10232nd on DRC, with different agendas. Being back to back is not one convened event.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T017

**Development A** `2026-08-21:soldiers-throw-belongings-qusra`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-21T13:01 to 2026-08-21T13:01 UTC
- **Actors:** none extracted
- **Places:** Israel, Palestine, Qusra
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T13:01 [Al Jazeera] **Israeli soldiers throw belongings from besieged Palestinian home**
    > Israeli soldiers were filmed throwing belongings from Palestinian homes in Qusra.

**Development B** `2026-08-21:israeli-drone-strike-syria-southwest`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera, BBC World
- **Times:** 2026-08-22T14:37 to 2026-08-22T21:42 UTC
- **Actors:** Israel, Syria
- **Places:** Damascus, Israel, Syria, Turkey
- **System Development:** D7
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T14:37 [Al Jazeera] **Israeli drone strike on ‘civilian vehicle’ injures several in Syria**
    > Syria condemns attack in southwest as a &#039;flagrant violation of sovereignty&#039; and a &#039;blatant breach of international law&#039;.
  - 2026-08-22T21:42 [BBC World] **Syria says Israeli strike near Damascus violation of international law**
    > The latest incident comes days after reports emerged Israel had struck a military airbase close to the Turkish border.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Israeli soldiers in Qusra in the West Bank (A) and an Israeli strike in Syria (B) share only the actor.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T018

**Development A** `2026-09-27-live:trump-rejects-hormuz-plan`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T00:00 to 2026-09-27T00:00 UTC
- **Actors:** Donald Trump, Iran, Tehran, Trump, US, Washington
- **Places:** Hormuz, Iran, Strait of Hormuz, Tehran, US
- **System Development:** D3
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-27T00:00 [Al Jazeera] **Iran war live: Tehran awaits official response as Trump rejects Hormuz plan**
    > US president rejects Iran&#039;s seven-day plan to reopen the Strait of Hormuz, saying the deal is not &#039;acceptable&#039;.

**Development B** `2026-09-27-live:araghchi-only-negotiation`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-27T07:44 to 2026-09-27T07:44 UTC
- **Actors:** Donald Trump, Iran, Tehran, Trump, US, Washington
- **Places:** Hormuz, Iran, Tehran, US
- **System Development:** D3
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-27T07:44 [BBC World] **Iranian minister says only negotiation can end conflict after Trump rejects Hormuz deal**
    > The foreign minister says Tehran is waiting for an official rejection of a deal, despite the US President's comments.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `reaction_to` | B->A | medium | none |

**Rationale:** B: 'Iranian minister says only negotiation can end conflict after Trump rejects Hormuz deal', which explicitly responds to the rejection of 'Iran's seven-day plan to reopen the Strait of Hormuz' reported in A.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T019

**Development A** `2026-09-25:nyc-protest-arrests-netanyahu`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-25T02:24 to 2026-09-25T02:35 UTC
- **Actors:** Benjamin Netanyahu, New Yorkers, Susan Sarandon, UN General Assembly, United Nations
- **Places:** Israel, NYC
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T02:24 [Al Jazeera] **More than 100 arrested as New Yorkers protest Netanyahu’s UN visit**
    > Demonstrators blocked streets and marched towards UN headquarters as the Israeli PM addressed world leaders at UNGA.
  - 2026-09-25T02:35 [Al Jazeera] **NYC police arrest Susan Sarandon, other celebrities protesting Netanyahu**
    > Rights groups accuse UN of hosting a &#039;war criminal&#039; as delegations walk out during Israeli prime minister&#039;s speech.

**Development B** `2026-09-25:jewish-march-against-netanyahu`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-25T03:49 to 2026-09-25T03:49 UTC
- **Actors:** Al Jazeera, Benjamin Netanyahu, Emma Withrow, Jewish
- **Places:** Palestine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T03:49 [Al Jazeera] **Jewish protestors join Free Palestine march to denounce Netanyahu**
    > Al Jazeera’s Emma Withrow reports from a Free Palestine march, where Jewish demonstrators rejected Netanyahu.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | low | SAME_DEVELOPMENT_SUSPECTED |

**Rationale:** Both describe New York street protests against Netanyahu during his UNGA address on the same night; B's 'Free Palestine march' may be the same protest as A's.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T020

**Development A** `2026-09-29-live:myanmar-rakhine-market-airstrike`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T15:38 to 2026-09-28T19:31 UTC
- **Actors:** Rakhine, Rakhine State
- **Places:** Myanmar
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T15:38 [Al Jazeera] **At least 33 killed after Myanmar military air strike hits market**
    > Dozens of people have been killed in a military air strike on an opposition-controlled area of Rakhine State, Myanmar.
  - 2026-09-28T19:31 [Al Jazeera] **Myanmar army air strike kills dozens in Rakhine state**
    > Nearly half a million people are displaced in Rakhine as a result of the conflict between the military and rebel groups.

**Development B** `2026-09-29-live:malaysia-repatriation-to-myanmar`

- **Members:** 3 item(s)
- **Sources:** Al Jazeera, BBC World, South China Morning Post
- **Times:** 2026-09-29T06:06 to 2026-09-29T09:27 UTC
- **Actors:** Malaysia
- **Places:** Kuala Lumpur, Malaysia, Myanmar
- **System Development:** D16
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T06:06 [BBC World] **Malaysia begins controversial repatriation of asylum seekers to Myanmar**
    > Human rights groups say some 5,000 returnees could face violence, persecution and forced conscription.
  - 2026-09-29T07:00 [South China Morning Post] **Malaysia begins sending thousands of Myanmar nationals back to war-torn homeland**
    > Malaysia began an operation to send nearly 1,500 Myanmar nationals back to their war-torn homeland on Tuesday, pressing ahead with a government-to-government repatriation deal despite warnings that returnees could face persecution and forced conscription.
The first group of 1,476
  - 2026-09-29T09:27 [Al Jazeera] **Malaysia begins sending back Rohingya refugees despite safety warnings**
    > About 1,500 refugees are to be sent back in the first phase, despite criticism from rights groups.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** A Myanmar military air strike in Rakhine (A) and Malaysia beginning repatriations (B) share only the Myanmar context.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T021

**Development A** `2026-08-31:us-larak-strike-iran-retaliation`

- **Members:** 4 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-31T00:00 to 2026-08-31T09:19 UTC
- **Actors:** IRGC, U.S. Central Command
- **Places:** Iran, Jordan, Larak Island, Strait of Hormuz, UAE, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T00:00 [Al Jazeera] **Iran war live: IRGC attacks US bases in Jordan after US bombs Larak Island**
    > US Central Command says its forces bombed two rocket launchers of the IRGC on Larak Island.
  - 2026-08-31T00:00 [Al Jazeera] **Iran war live: Tehran says it attacked bases in Jordan, UAE after US strike**
    > CENTCOM says US forces bombed two IRGC rocket launchers on Larak Island which presented an &#039;imminent threat&#039;.
  - 2026-08-31T03:06 [Al Jazeera] **Iran targets Jordan after first US attack in a month**
    > The US has launched its first strikes on Iran in a month, hitting sites on Larak Island. Iran hit back targeting bases h
  - 2026-08-31T09:19 [Al Jazeera] **Iran attacks Jordan, UAE after US bombs Larak Island: What’s the latest?**
    > The retaliatory attacks came after the US targeted two Iranian launchers on Larak Island in the Strait of Hormuz.

**Development B** `2026-08-31:uae-intercepts-drone-denies-airbase-hit`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-31T11:25 to 2026-08-31T11:25 UTC
- **Actors:** Al Menhad
- **Places:** Iran, UAE, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T11:25 [Al Jazeera] **UAE intercepts drone after US and Iran exchange attacks**
    > The UAE says it intercepted a drone coming from Iran and rejected &#039;false&#039; reports of an attack on its Al Menhad airbase.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_attack_wave` | none | medium | none |

**Rationale:** A reports Iran's retaliatory attacks on 'bases in Jordan, UAE' after the Larak strike, and B the UAE intercepting 'a drone coming from Iran' after the same exchange. This is one wave.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T022

**Development A** `2026-09-29-live:us-waiver-najaf-iran-flights`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-28T18:28 to 2026-09-28T18:28 UTC
- **Actors:** Donald Trump, Iraqi Airways, Shiite, Shiite Muslim, US, US Treasury
- **Places:** Iran, Iraq, Najaf, US
- **System Development:** D6
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-28T18:28 [South China Morning Post] **US to grant sanctions waiver for flights between Iran and Iraq’s Najaf, source says**
    > US President Donald Trump’s administration was set to grant a limited waiver to its Iran sanctions programme on Monday to allow for flights carrying Shiite Muslim religious pilgrims between Iran and Iraq, a person with direct knowledge of the matter said.
The source, who is invol

**Development B** `2026-09-29-live:iran-war-live-no-sanctions-relief`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T00:00 to 2026-09-29T00:00 UTC
- **Actors:** Trump, US
- **Places:** Iran, Tehran, US
- **System Development:** D6
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-29T00:00 [Al Jazeera] **Iran war live: Trump says he did not offer Tehran sanctions relief**
    > US President Trump rejects a news report claiming his administration offered Iran sanctions relief and frozen funds.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | none |

**Rationale:** B denies a report of 'sanctions relief and frozen funds', which is not A's limited pilgrim-flight waiver. B does not name A.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T023

**Development A** `2026-09-29-live:najaf-iran-flights-resume`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T18:50 to 2026-09-28T18:50 UTC
- **Actors:** US, United Nations
- **Places:** Iran, Iraq, Najaf, Tehran, US
- **System Development:** D6
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-28T18:50 [Al Jazeera] **Flights between Iraq’s Najaf and Iran resumed as Tehran protests US curbs**
    > Tehran filed a UN complaint against US sanctions forcing regional cancellations of Iran flights.

**Development B** `2026-09-29-live:iran-war-live-no-sanctions-relief`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T00:00 to 2026-09-29T00:00 UTC
- **Actors:** Trump, US
- **Places:** Iran, Tehran, US
- **System Development:** D6
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-29T00:00 [Al Jazeera] **Iran war live: Trump says he did not offer Tehran sanctions relief**
    > US President Trump rejects a news report claiming his administration offered Iran sanctions relief and frozen funds.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Resumed Najaf flights and Tehran's UN complaint (A) are unrelated to Trump denying a sanctions-relief report (B), apart from the shared topic.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T024

**Development A** `2026-08-21:japan-icc-judge-sanctioned`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-21T00:00 to 2026-08-21T00:00 UTC
- **Actors:** Donald Trump, International Criminal Court, Tomoko Akane
- **Places:** Hague, Japan, Tokyo, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T00:00 [South China Morning Post] **Japan faces ‘nightmare scenario’ as it struggles to defend ICC judge**
    > Japan has spent years casting the International Criminal Court as a pillar of the rules-based order. This week, its closest ally sanctioned the Japanese judge who leads it.
The move has left Tokyo in an uncomfortable bind: defend Tomoko Akane, the Japanese president of The Hague-

**Development B** `2026-08-21:japan-record-defence-budget`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-21T09:15 to 2026-08-21T09:15 UTC
- **Actors:** none extracted
- **Places:** Japan, Tokyo, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T09:15 [South China Morning Post] **Japan seeks record US$56 billion defence push amid growing regional tensions**
    > Japan is preparing to spend more than ever on defence as analysts say Tokyo is being forced to respond to a convergence of regional threats, fast-changing military technology and growing uncertainty over the reliability of the US security umbrella.
The defence ministry is prepari

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** The ICC judge sanctions bind (A) and Japan's defence budget request (B) share only the actor. B cites general regional threats, not A.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T025

**Development A** `2026-10-03-live:s-1228`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-29T21:32 to 2026-09-29T21:32 UTC
- **Actors:** none extracted
- **Places:** France
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 21:32 [BBC World] **More than 400 detained as France student protests escalate**
    > Students have been protesting against conditions and resources in secondary schools since last week.

**Development B** `2026-10-03-live:s-1380`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-30T13:18 to 2026-09-30T13:18 UTC
- **Actors:** none extracted
- **Places:** France
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 13:18 [BBC World] **Dozens hurt and hundreds arrested in wave of French school protests**
    > Students have been protesting against conditions and resources in secondary schools since last week.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | SAME_DEVELOPMENT_SUSPECTED |

**Rationale:** Both report mass arrests in the French school protest wave with the identical summary 'Students have been protesting... since last week'. They are likely the same arrests reported twice.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T026

**Development A** `2026-08-21:uk-canada-australia-condemn-wck-probe-refusal`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-08-21T15:58 to 2026-08-21T15:58 UTC
- **Actors:** none extracted
- **Places:** Australia, Canada, Gaza, Israel, UK
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T15:58 [BBC World] **UK, Canada and Australia condemn Israel for refusing criminal probe into aid worker killings in Gaza**
    > Seven World Central Kitchen workers were killed in the Israeli strike on their convoy in 2024.

**Development B** `2026-08-21:israeli-drone-strike-syria-southwest`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera, BBC World
- **Times:** 2026-08-22T14:37 to 2026-08-22T21:42 UTC
- **Actors:** Israel, Syria
- **Places:** Damascus, Israel, Syria, Turkey
- **System Development:** D7
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T14:37 [Al Jazeera] **Israeli drone strike on ‘civilian vehicle’ injures several in Syria**
    > Syria condemns attack in southwest as a &#039;flagrant violation of sovereignty&#039; and a &#039;blatant breach of international law&#039;.
  - 2026-08-22T21:42 [BBC World] **Syria says Israeli strike near Damascus violation of international law**
    > The latest incident comes days after reports emerged Israel had struck a military airbase close to the Turkish border.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Condemnation over the WCK probe refusal (A) and Syria condemning an Israeli strike (B) share only Israel as actor.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T027

**Development A** `2026-09-29-live:hk-eco-sites-golden-week`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-29T00:30 to 2026-09-29T00:30 UTC
- **Actors:** Po Pin Chau, South China Morning Post
- **Places:** China, Hong Kong
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T00:30 [South China Morning Post] **Can Hong Kong protect its eco-sensitive sites amid ‘golden week’ overtourism fears?**
    > Hong Kong is bracing for a surge of mainland Chinese visitors to its eco-sensitive areas during the National Day “golden week” holiday, as strong interest in countryside attractions raises questions over whether the city can absorb crowds without overwhelming popular sites.
A rev

**Development B** `2026-09-29-live:hk-golden-week-things-to-do`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-29T03:00 to 2026-09-29T03:00 UTC
- **Actors:** Sai Kung, Unesco Global Geopark
- **Places:** China, Hong Kong
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T03:00 [South China Morning Post] **5 things to do over the National Day ‘golden week’ holiday in Hong Kong**
    > Hong Kong is set to welcome 1.29 million mainland Chinese visitors over the National Day “golden week” break, fuelling questions online about what locals and tourists can do during the celebrations.
On popular mainland social media platform RedNote, many users have recommended a 

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Both are golden-week Hong Kong features on overtourism and things to do, linked only by the same topic and holiday.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T028

**Development A** `2026-09-30-multilingual:sx-168`

- **Members:** 1 item(s)
- **Sources:** France 24
- **Times:** 2026-09-29T21:05 to 2026-09-29T21:05 UTC
- **Actors:** AI, Donald Trump, Trump, White House, Xi Jinping
- **Places:** China, South Korea, U.S.
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 21:05 [France 24] **Trump says he doesn't want to work with China on AI safety**
    > US President Donald Trump discussed AI development with dozens of tech bosses at the White House on Tuesday. Ahead of his "super intelligence" luncheon, Trump launched a new AI-powered website for government services, vowing not to stifle the technology's growth. He also said he 

**Development B** `2026-09-30-multilingual:sx-167`

- **Members:** 1 item(s)
- **Sources:** France 24
- **Times:** 2026-09-29T22:48 to 2026-09-29T22:48 UTC
- **Actors:** AI, Donald Trump, Trump, Trump US
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 22:48 [France 24] **AI companies sign voluntary accord on safety with Trump**
    > US President Donald Trump and leaders of major AI companies signed a voluntary accord Tuesday to strengthen safety as the technology faces growing public concern. The agreement calls for internal controls, independent audits and board oversight while Trump rejected calls for gove

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_convened_event` | none | high | none |

**Rationale:** Both come from Tuesday's White House meeting with AI tech bosses: A is Trump's remarks 'ahead of his super intelligence luncheon' and B the accord signed there.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T029

**Development A** `2026-09-27-live:hormuz-tensions-linger`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T14:36 to 2026-09-27T14:36 UTC
- **Actors:** Donald Trump, Iran, Tehran, Trump, US, Washington
- **Places:** Hormuz, Iran, US
- **System Development:** D3
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-27T14:36 [Al Jazeera] **Strait of Hormuz tensions linger as Iran and US move further from a deal**
    > There are fears of renewed fighting between the US and Iran, after President Trump rejected a deal.

**Development B** `2026-09-27-live:araghchi-doomsday-war`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T17:46 to 2026-09-28T00:00 UTC
- **Actors:** Abbas Araghchi, Donald Trump, FM Araghchi, Iran, Tehran, Trump, US, Washington
- **Places:** Hormuz, Iran, Strait, Tehran, Washington
- **System Development:** D3
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-27T17:46 [Al Jazeera] **‘Iran ready for doomsday war’, FM Araghchi says**
    > Foreign Minister Abbas Araghchi says Iran is prepared for war to resume, ‘even if it comes to a doomsday war’.
  - 2026-09-28T00:00 [Al Jazeera] **Iran war live: Tehran open to ‘real diplomacy’, ready for ‘apocalyptic war’**
    > Abbas Araghchi&#039;s warning comes after Washington rejected a seven-day roadmap to end the war and reopen Strait of Hormuz.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | third_event |

**Rationale:** B's Araghchi warning 'comes after Washington rejected a seven-day roadmap', a reaction to the rejection rather than to A's report of lingering tensions.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T030

**Development A** `2026-08-21:bessent-vows-toughest-iran-sanctions`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-21T00:00 to 2026-08-21T00:00 UTC
- **Actors:** Bessent, Treasury
- **Places:** China, Iran, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T00:00 [Al Jazeera] **Iran war live: US vows toughest Iran sanctions, urges China support**
    > US Treasury Secretary Bessent says new economic measures will &#039;collapse&#039; Iranian government.

**Development B** `2026-08-21:iran-rejects-new-us-sanctions`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-22T09:14 to 2026-08-22T09:14 UTC
- **Actors:** Esmaeil Baghaei, Foreign Ministry, Trump
- **Places:** Iran, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T09:14 [Al Jazeera] **Iran says new US sanctions violate sovereignty of other states**
    > Foreign Ministry spokesman Esmaeil Baghaei slams Trump&#039;s latest threat as a return to &#039;full-scale classic colonialism&#039;.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `reaction_to` | B->A | medium | none |

**Rationale:** B: 'Iran says new US sanctions violate sovereignty of other states', which slams the 'latest threat'. That matches A's 'US vows toughest Iran sanctions, urges China support'.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T031

**Development A** `2026-09-29-live:iran-denies-airbase-link`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T15:29 to 2026-09-28T15:29 UTC
- **Actors:** British FM
- **Places:** Iran, Tehran, UK
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T15:29 [Al Jazeera] **Iran denies link to attack on airbase as UK minister warns of ‘proxies’**
    > Tehran condemns &#039;unfounded and malicious speculation&#039;; British FM vows to &#039;act against the proxies of Iran&#039;.

**Development B** `2026-09-29-live:iran-war-live-no-sanctions-relief`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T00:00 to 2026-09-29T00:00 UTC
- **Actors:** Trump, US
- **Places:** Iran, Tehran, US
- **System Development:** D6
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-29T00:00 [Al Jazeera] **Iran war live: Trump says he did not offer Tehran sanctions relief**
    > US President Trump rejects a news report claiming his administration offered Iran sanctions relief and frozen funds.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Iran denying an airbase attack link (A) and Trump denying a sanctions-relief report (B) share only the actors.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T032

**Development A** `2026-09-30-multilingual:sx-169`

- **Members:** 1 item(s)
- **Sources:** France 24
- **Times:** 2026-09-29T21:00 to 2026-09-29T21:00 UTC
- **Actors:** AI, Donald Trump, Harrison Rolfes, Monte Francis, PitchBook, White House
- **Places:** France, U.S.
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 21:00 [France 24] **Safeguards 'build a moat' around US AI firms, prevent open-source models from advancing, expert says**
    > US President Donald Trump on Tuesday said the tech executives gathered at the White House to discuss regulating AI had signed a "morally binding" commitment to build adequate safeguards on the fast-moving technology. Speaking with FRANCE 24's Monte Francis, Harrison Rolfes, Senio

**Development B** `2026-09-30-multilingual:sx-167`

- **Members:** 1 item(s)
- **Sources:** France 24
- **Times:** 2026-09-29T22:48 to 2026-09-29T22:48 UTC
- **Actors:** AI, Donald Trump, Trump, Trump US
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 22:48 [France 24] **AI companies sign voluntary accord on safety with Trump**
    > US President Donald Trump and leaders of major AI companies signed a voluntary accord Tuesday to strengthen safety as the technology faces growing public concern. The agreement calls for internal controls, independent audits and board oversight while Trump rejected calls for gove

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `commentary_on` | A->B | medium | commentary |

**Rationale:** A is an expert interview arguing that the safeguards tech executives signed at the White House 'build a moat' around US AI firms, which is analysis of B's 'voluntary accord on safety'.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T033

**Development A** `2026-09-30-multilingual:sx-535`

- **Members:** 1 item(s)
- **Sources:** GDELT
- **Times:** 2026-09-29T14:45 to 2026-09-29T14:45 UTC
- **Actors:** English
- **Places:** India, Iran
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 14:45 [GDELT] **Iran rial crashes past 2 . 5 million per dollar : War , sanctions push currency to new low**
    > Domain: livemint.com | Language: English | Source country: India

**Development B** `2026-09-30-multilingual:D19`

- **Members:** 3 item(s)
- **Sources:** Clarín Mundo, Europa Press Internacional, GDELT
- **Times:** 2026-09-29T22:45 to 2026-09-30T08:42 UTC
- **Actors:** Donald Trump, English, Iran, Irán
- **Places:** EE.UU., Estados Unidos, Iran, Irán, Syria, Teheran
- **System Development:** D19
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 22:45 [Clarín Mundo] **Por la guerra y la incertidumbre económica, la moneda de Irán se hunde en un mínimo histórico**
    > Las sanciones internacionales presionan a las finanzas de la república islámica. El régimen abre la puerta a nuevas negociaciones con Estados Unidos para terminar con el conflicto.
  - 2026-09-30 01:15 [GDELT] **Iran Currency Hits a New Record Low as War Erodes the Country Economic Stability**
    > Domain: english.aawsat.com | Language: English | Source country: Syria
  - 2026-09-30 08:42 [Europa Press Internacional] **Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz**
    > El Gobierno de Irán ha confirmado este miércoles que ha recibido la respuesta oficial de Estados Unidos a su propuesta para reactivar el proceso de conversaciones para un acuerdo de paz, días después de que el presidente estadounidense, Donald Trump, expresara su rechazo al plan 

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | SAME_DEVELOPMENT_SUSPECTED |

**Rationale:** A ('Iran rial crashes... new low') and B's main items ('moneda de Iran se hunde en un minimo historico', 'Iran Currency Hits a New Record Low') report the same currency record low. B also contains a stray item on the US response.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T034

**Development A** `2026-10-03-live:s-1200`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-29T17:54 to 2026-09-29T17:54 UTC
- **Actors:** none extracted
- **Places:** Madrid, Spain
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 17:54 [South China Morning Post] **87-year-old woman whose eviction sparked protests in Spain is returning home**
    > Spain’s coalition government said it had agreed on proposals including banning evictions until 2030 to address the country’s housing crisis, as the 87-year-old woman whose forced removal last week triggered protests accepted an offer to return home.
Hundreds of ‌people remained c

**Development B** `2026-10-03-live:s-1233`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T21:02 to 2026-09-29T21:02 UTC
- **Actors:** none extracted
- **Places:** Madrid, Spain
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 21:02 [Al Jazeera] **Spain protests: Evicted 87-year-old woman to return to Madrid home**
    > The real estate firm backs down and restores her old rent after mass protests over Spain&#039;s housing crisis.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | SAME_DEVELOPMENT_SUSPECTED |

**Rationale:** Both report the evicted 87-year-old woman accepting an offer to return to her Madrid home.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T035

**Development A** `2026-09-30-multilingual:sx-410`

- **Members:** 1 item(s)
- **Sources:** UN News
- **Times:** 2026-09-28T12:00 to 2026-09-28T12:00 UTC
- **Actors:** Hamas, UN Security Council
- **Places:** Gaza, Israel, Middle East, West Bank
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28 12:00 [UN News] **Security Council LIVE: Ambassadors meet as West Bank tensions rise, Gaza plan stalls**
    > The Security Council met Monday morning with prospects for peace in the Middle East under strain on two fronts. In the West Bank, settler violence and settlement expansion are raising fears for a two-State solution. In Gaza, a year-old peace plan has stalled while civilian suffer

**Development B** `2026-09-30-multilingual:sx-423`

- **Members:** 3 item(s)
- **Sources:** UN News, UN Press
- **Times:** 2026-09-28T23:02 to 2026-09-29T21:52 UTC
- **Actors:** James Swan, M23, UN Security Council, United Nations, United Nations Organization Stabilization Mission
- **Places:** Congo, DRC, Democratic Republic, Democratic Republic of Congo, Democratic Republic of the Congo, Haiti, New York, Rwanda
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28 23:02 [UN Press] **Security Council, 10232nd Meeting (AM) Democratic Republic of the Congo/MONUSCO**
    > Following its meeting concerning Haiti, the Council will convene to consider the situation in the Democratic Republic of the Congo. Anticipated briefers include James Swan, Head of the United Nations Organization Stabilization Mission in the Democratic Republic of the Congo (MONU
  - 2026-09-29 12:00 [UN News] **Security Council LIVE: DRC peace deals fail to halt fighting as Ebola deepens crisis**
    > The Security Council met in New York&nbsp;on the Democratic Republic of the Congo (DRC) Tuesday, where clashes between Government forces and M23 rebels continue in the east, despite a series of peace agreements. Ambassadors focused on ceasefire monitoring, rising tensions between
  - 2026-09-29 21:52 [UN Press] **Commitments Must Yield Tangible Progress in Democratic Republic of Congo, Special Representative Tells Security Council**
    > Serious challenges remain despite sustained diplomatic engagement to address the conflict in the eastern part of the Democratic Republic of the Congo, the Security Council heard today, as speakers welcomed the ceasefire monitoring and verification conducted by the UN mission in t

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** These are separate Security Council meetings, Middle East on Monday and DRC on Tuesday, linked only by the venue.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T036

**Development A** `2026-08-31:hk-robot-convenience-stores-open`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T00:43 to 2026-08-31T00:43 UTC
- **Actors:** Galbot, Hung Hom, Kai Tak, Wan Chai
- **Places:** Beijing, China, Hong Kong
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T00:43 [South China Morning Post] **At your service: Hong Kong welcomes first humanoid robot-run convenience stores**
    > Hong Kong’s first convenience stores operated by humanoid robots will open on Tuesday, with the Beijing-based company behind it planning to establish about 10 more outlets locally as it makes the city its first stop in “going overseas”.
Following an opening ceremony on Monday, th

**Development B** `2026-08-31:paul-chan-robotics-role`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T00:43 to 2026-08-31T00:43 UTC
- **Actors:** Galbot, Hung Hom, Kai Tak, Paul Chan Hong Kong, Wan Chai
- **Places:** Beijing, China, Hong Kong
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T00:43 [South China Morning Post] **Hong Kong can play unique role in fostering robotics industry: Paul Chan**
    > Hong Kong can serve a unique role in the development of the robotics industry, the financial chief has said as he welcomed the coming opening of the city’s first convenience stores operated by humanoid robots developed by a Beijing-based company.
Following an opening ceremony on 

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `reaction_to` | B->A | medium | none |

**Rationale:** B: Paul Chan spoke 'as he welcomed the coming opening of the city's first convenience stores operated by humanoid robots', which explicitly welcomes A's store opening.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T037

**Development A** `2026-09-27-live:trump-rejects-hormuz-plan`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T00:00 to 2026-09-27T00:00 UTC
- **Actors:** Donald Trump, Iran, Tehran, Trump, US, Washington
- **Places:** Hormuz, Iran, Strait of Hormuz, Tehran, US
- **System Development:** D3
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-27T00:00 [Al Jazeera] **Iran war live: Tehran awaits official response as Trump rejects Hormuz plan**
    > US president rejects Iran&#039;s seven-day plan to reopen the Strait of Hormuz, saying the deal is not &#039;acceptable&#039;.

**Development B** `2026-09-27-live:trump-expects-new-iran-talks`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-27T19:16 to 2026-09-27T19:16 UTC
- **Actors:** Axios, Donald Trump, Iran, Tehran, Trump, UN General Assembly, US, Washington
- **Places:** Iran, New York, Strait of Hormuz, Tehran, US
- **System Development:** D3
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-27T19:16 [South China Morning Post] **Trump expects new Iran talks despite rejecting deal offer**
    > US President Donald Trump said on Sunday that he expects talks with Iran to resume in the coming week, despite his rejection of a truce proposal put forward by Tehran.
Iranian officials brought with them to the UN General Assembly in New York a plan for a seven-day truce followed

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `follow_up_to` | B->A | low | none |

**Rationale:** B is Trump's later statement that he 'expects talks... to resume... despite his rejection of a truce proposal', explicitly continuing A's rejection of Iran's seven-day plan by the same actor.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T038

**Development A** `2026-08-21:economic-d-day-hits-us-markets`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-21T13:47 to 2026-08-21T13:47 UTC
- **Actors:** Trump
- **Places:** Iran, Israel, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T13:47 [Al Jazeera] **Trump’s ‘economic D-Day’ claims first victim: Not Iran, but US markets**
    > The US and Israel&#039;s war on Iran has upended global financial and energy markets.

**Development B** `2026-08-21:iran-rejects-new-us-sanctions`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-22T09:14 to 2026-08-22T09:14 UTC
- **Actors:** Esmaeil Baghaei, Foreign Ministry, Trump
- **Places:** Iran, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T09:14 [Al Jazeera] **Iran says new US sanctions violate sovereignty of other states**
    > Foreign Ministry spokesman Esmaeil Baghaei slams Trump&#039;s latest threat as a return to &#039;full-scale classic colonialism&#039;.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | third_event |

**Rationale:** A is analysis of the market fallout of the 'economic D-Day' and B is Iran slamming new sanctions. Both relate to the sanctions push, not to each other.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T039

**Development A** `2026-09-30-multilingual:sx-540`

- **Members:** 1 item(s)
- **Sources:** GDELT
- **Times:** 2026-09-29T16:30 to 2026-09-29T16:30 UTC
- **Actors:** English
- **Places:** Iran, U.S.
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 16:30 [GDELT] **  This is how the war will end : Iran currency hits new record low**
    > Domain: fortune.com | Language: English | Source country: United States

**Development B** `2026-09-30-multilingual:D19`

- **Members:** 3 item(s)
- **Sources:** Clarín Mundo, Europa Press Internacional, GDELT
- **Times:** 2026-09-29T22:45 to 2026-09-30T08:42 UTC
- **Actors:** Donald Trump, English, Iran, Irán
- **Places:** EE.UU., Estados Unidos, Iran, Irán, Syria, Teheran
- **System Development:** D19
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 22:45 [Clarín Mundo] **Por la guerra y la incertidumbre económica, la moneda de Irán se hunde en un mínimo histórico**
    > Las sanciones internacionales presionan a las finanzas de la república islámica. El régimen abre la puerta a nuevas negociaciones con Estados Unidos para terminar con el conflicto.
  - 2026-09-30 01:15 [GDELT] **Iran Currency Hits a New Record Low as War Erodes the Country Economic Stability**
    > Domain: english.aawsat.com | Language: English | Source country: Syria
  - 2026-09-30 08:42 [Europa Press Internacional] **Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz**
    > El Gobierno de Irán ha confirmado este miércoles que ha recibido la respuesta oficial de Estados Unidos a su propuesta para reactivar el proceso de conversaciones para un acuerdo de paz, días después de que el presidente estadounidense, Donald Trump, expresara su rechazo al plan 

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | SAME_DEVELOPMENT_SUSPECTED |

**Rationale:** A ('Iran currency hits new record low') and B's main items report the same rial record low.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T040

**Development A** `2026-10-03-live:s-1510`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-10-01T02:35 to 2026-10-01T02:35 UTC
- **Actors:** Christa Pike
- **Places:** Tennessee
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 02:35 [Al Jazeera] **Christa Pike’s execution by lethal injection fails in Tennessee**
    > Witnesses say Tennessee officials were unable to execute Christa Pike after a lethal injection attempt.

**Development B** `2026-10-03-live:D9`

- **Members:** 5 item(s)
- **Sources:** Al Jazeera, BBC World, South China Morning Post
- **Times:** 2026-10-01T16:45 to 2026-10-02T20:57 UTC
- **Actors:** Christa Pike, Pike, Randy Spivey
- **Places:** Nashville, Tennessee, US
- **System Development:** D9
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 16:45 [BBC World] **Tennessee halts executions after Christa Pike survives two lethal injection attempts**
    > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
  - 2026-10-02 03:02 [South China Morning Post] **Christa Pike in ‘life-saving care’ after botched Tennessee execution**
    > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from 
  - 2026-10-02 07:58 [Al Jazeera] **Lawyers for US inmate who survived lethal injections demand release**
    > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
  - 2026-10-02 20:32 [BBC World] **US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say**
    > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `follow_up_to` | B->A | low | none |

**Rationale:** A reports the failed lethal injection, and B covers the subsequent halt of executions, the commutation request and hospitalisation 'following the botched execution'. That is the same case continuing, though B's items partly retell A.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T041

**Development A** `2026-10-03-live:s-1525`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-10-01T04:14 to 2026-10-01T04:14 UTC
- **Actors:** Christa Pike, Pike
- **Places:** Tennessee
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 04:14 [South China Morning Post] **Tennessee halts executions after Christa Pike survives 2 doses of lethal drug**
    > Tennessee officials were unable to put Christa Pike to death on Wednesday for a 1995 murder after administering two doses of a lethal drug. A death penalty expert said it was an unprecedented failure, and Tennessee’s governor halted the remaining execution for the rest of the yea

**Development B** `2026-10-03-live:D9`

- **Members:** 5 item(s)
- **Sources:** Al Jazeera, BBC World, South China Morning Post
- **Times:** 2026-10-01T16:45 to 2026-10-02T20:57 UTC
- **Actors:** Christa Pike, Pike, Randy Spivey
- **Places:** Nashville, Tennessee, US
- **System Development:** D9
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 16:45 [BBC World] **Tennessee halts executions after Christa Pike survives two lethal injection attempts**
    > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
  - 2026-10-02 03:02 [South China Morning Post] **Christa Pike in ‘life-saving care’ after botched Tennessee execution**
    > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from 
  - 2026-10-02 07:58 [Al Jazeera] **Lawyers for US inmate who survived lethal injections demand release**
    > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
  - 2026-10-02 20:32 [BBC World] **US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say**
    > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | SAME_DEVELOPMENT_SUSPECTED |

**Rationale:** A's headline 'Tennessee halts executions after Christa Pike survives 2 doses of lethal drug' matches B's lead item 'Tennessee halts executions after Christa Pike survives two lethal injection attempts'.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T042

**Development A** `2026-09-27-live:behind-trump-rejection-analysis`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T13:17 to 2026-09-27T13:17 UTC
- **Actors:** Trump
- **Places:** Iran
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T13:17 [Al Jazeera] **‘Better deal’: What’s behind Trump’s rejection of Iran’s truce offer?**
    > Experts say Trump sees economic sanctions as key to extracting more concessions but he risks losing leverage.

**Development B** `2026-09-27-live:trump-expects-new-iran-talks`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-27T19:16 to 2026-09-27T19:16 UTC
- **Actors:** Axios, Donald Trump, Iran, Tehran, Trump, UN General Assembly, US, Washington
- **Places:** Iran, New York, Strait of Hormuz, Tehran, US
- **System Development:** D3
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-27T19:16 [South China Morning Post] **Trump expects new Iran talks despite rejecting deal offer**
    > US President Donald Trump said on Sunday that he expects talks with Iran to resume in the coming week, despite his rejection of a truce proposal put forward by Tehran.
Iranian officials brought with them to the UN General Assembly in New York a plan for a seven-day truce followed

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | third_event |

**Rationale:** A is analysis of Trump's rejection of the truce offer and B is Trump expecting talks to resume. Both relate to the rejection, and A does not analyse B.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T043

**Development A** `2026-08-21:us-designates-hezbollah-iranian-proxy`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-21T12:12 to 2026-08-21T12:12 UTC
- **Actors:** Hezbollah, IRGC, Quds Force, US Treasury
- **Places:** Iran, Lebanon, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T12:12 [Al Jazeera] **US designates Hezbollah an Iranian proxy, sanctions funding network**
    > The US Treasury labels Lebanon-based group &#039;an extension&#039; of the IRGC&#039;s Quds Force and takes aim at financing.

**Development B** `2026-08-21:iran-rejects-new-us-sanctions`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-22T09:14 to 2026-08-22T09:14 UTC
- **Actors:** Esmaeil Baghaei, Foreign Ministry, Trump
- **Places:** Iran, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T09:14 [Al Jazeera] **Iran says new US sanctions violate sovereignty of other states**
    > Foreign Ministry spokesman Esmaeil Baghaei slams Trump&#039;s latest threat as a return to &#039;full-scale classic colonialism&#039;.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `AMBIGUOUS` | none | low | inferred |

**Rationale:** B condemns 'new US sanctions' as violating 'sovereignty of other states', which could target A's Hezbollah designation but does not name it.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T044

**Development A** `2026-09-29-live:hk-checkpoints-golden-week`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-28T13:18 to 2026-09-28T13:18 UTC
- **Actors:** Immigration Department
- **Places:** China, Hong Kong, Hongkongers
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T13:18 [South China Morning Post] **Hong Kong checkpoints to handle 7.44 million passenger trips for National Day break**
    > Hong Kong’s checkpoints are expected to handle about 7.44 million passenger trips over mainland China’s National Day “golden week” break, while people movements are anticipated to peak this weekend.
The Immigration Department said on Monday that the figure would include inbound a

**Development B** `2026-09-29-live:hk-golden-week-things-to-do`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-29T03:00 to 2026-09-29T03:00 UTC
- **Actors:** Sai Kung, Unesco Global Geopark
- **Places:** China, Hong Kong
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T03:00 [South China Morning Post] **5 things to do over the National Day ‘golden week’ holiday in Hong Kong**
    > Hong Kong is set to welcome 1.29 million mainland Chinese visitors over the National Day “golden week” break, fuelling questions online about what locals and tourists can do during the celebrations.
On popular mainland social media platform RedNote, many users have recommended a 

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Checkpoint passenger forecasts (A) and a things-to-do feature (B) share only the golden-week topic.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## T045

**Development A** `2026-09-27-live:araghchi-only-negotiation`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-27T07:44 to 2026-09-27T07:44 UTC
- **Actors:** Donald Trump, Iran, Tehran, Trump, US, Washington
- **Places:** Hormuz, Iran, Tehran, US
- **System Development:** D3
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-27T07:44 [BBC World] **Iranian minister says only negotiation can end conflict after Trump rejects Hormuz deal**
    > The foreign minister says Tehran is waiting for an official rejection of a deal, despite the US President's comments.

**Development B** `2026-09-27-live:hormuz-tensions-linger`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T14:36 to 2026-09-27T14:36 UTC
- **Actors:** Donald Trump, Iran, Tehran, Trump, US, Washington
- **Places:** Hormuz, Iran, US
- **System Development:** D3
- **Situation (production, `actor_set`):** us-iran
- **Evidence:**
  - 2026-09-27T14:36 [Al Jazeera] **Strait of Hormuz tensions linger as Iran and US move further from a deal**
    > There are fears of renewed fighting between the US and Iran, after President Trump rejected a deal.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | third_event |

**Rationale:** Both A (Iranian FM's response) and B (lingering tensions) follow from 'Trump rejects Hormuz deal'. B does not refer to A's statement.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

