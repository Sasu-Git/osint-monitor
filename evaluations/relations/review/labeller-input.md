# Relation labelling input (blind)

Label every case using the definitions in `taxonomy.md` (included below).

- Side A is the earlier Development, side B the later one.
- Each side is one Development: one occurrence, possibly reported by several outlets.

Return, per case:

- `label`: one relation type, `NO_RELATION` or `AMBIGUOUS`;
- `direction`: `B->A` or `A->B` for a directed type, written source -> target, or `none`;
- `identity_flag`: `SAME_DEVELOPMENT_SUSPECTED` or null;
- `flag`: for example `commentary`, or null;
- `rationale`: one sentence that cites the evidence;
- `confidence`: high, medium or low.

---

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


---

## R001
**A** (1 item(s))
- 2026-08-21T00:30 [South China Morning Post] More Hong Kong consumers allege coercive beauty sales in wake of Opatra crackdown
  > More consumers in Hong Kong have come forward to allege aggressive sales tactics across the beauty sector, including credit card abuse, unwanted physical contact and pressure to buy costly products, on the back of a crackdown on the local operations of a UK-based brand.
Legal experts warned that suc
**B** (1 item(s))
- 2026-08-22T15:30 [Al Jazeera] Over 100 ex-diplomats urge France, UK to sanction Israel over Palestine
  > An open letter demands a ban on arms transfers and a freeze on EU-Israel and UK-Israel trade agreements.

## R002
**A** (1 item(s))
- 2026-09-01T20:05 [BBC World] Jurors in Lindsay Clancy trial deadlocked but judge asks them to keep trying
  > The Massachusetts mother is facing murder charges for killing her three children at their family home in 2023.
**B** (1 item(s))
- 2026-09-01T23:17 [BBC World] Not just guilty or not - The jury's options in Lindsay Clancy's murder trial
  > Jurors have five options before them as they decide the fate of the former nurse charged with murdering her three children.

## R003
**A** (3 item(s))
- 2026-08-31T04:18 [Al Jazeera] Russia, China leaders to meet at Shanghai Cooperation Organisation summit
  > The organisation is not officially anti-West, but Russian and Chinese leaders have used it to amplify their worldview.
- 2026-08-31T08:47 [Al Jazeera] Xi, Modi and Putin attend SCO summit: What’s on the agenda?
  > The two-day summit aims to promote a vision of a multipolar world and mutual trade ties amid Trump&#039;s unilateralism.
- 2026-08-31T08:47 [Al Jazeera] Xi, Modi and Putin set to meet for SCO summit: What’s on the agenda?
  > The two-day summit aims to promote a vision of a multipolar world and mutual trade ties amid Trump&#039;s unilateralism.
**B** (1 item(s))
- 2026-08-31T14:00 [South China Morning Post] Prediction markets have priced the Trump-Xi summit. Do the bets have any value?
  > US President Donald Trump has already announced the date: September 24.
That is when, Trump says, Chinese President Xi Jinping will come to the White House for a visit following the “America first” leader’s own three-day trip to Beijing in May.
But there is a diplomatic wrinkle.
The Trump administra

## R004
**A** (1 item(s))
- 2026-08-31T02:45 [South China Morning Post] Nepal floods: could foreign rescue teams have been brought in earlier?
  > The Nepalese government has appealed for rescue aid from other countries just two days after it reportedly refused help, as several hundred people are still believed to be trapped in hydropower tunnels and thousands remain missing following the catastrophic flash flooding at the border with China la
**B** (4 item(s))
- 2026-08-31T06:05 [South China Morning Post] Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000
  > Rescuers from China and Nepal continued searching landslide- and flood-affected areas on Monday while efforts to reopen roads to the heart of the disaster-hit area at Gyirong Port entered a “critical stage”.
The death toll in Nepal had risen to 903 as of 9am on Monday, with 4,247 people still missin
- 2026-08-31T07:34 [Al Jazeera] Nepal races to rescue trapped workers, as flood death toll surpasses 900
  > Nepal officials say rescuers focusing on reaching workers in hydropower project tunnels in flood-stricken region.
- 2026-09-01T06:02 [BBC World] The final minutes before floodwater crashed through Nepal-China border
  > More than 100 Indians are missing at a vital Nepal-China trade crossing after devastating Himalayan floods.
- 2026-09-01T16:11 [BBC World] River water smashed into tunnel and chased me for 20 minutes, Nepal worker tells BBC
  > Major efforts to rescue hydropower workers continue as Nepal's death toll exceeds 1,000.

## R005
**A** (1 item(s))
- 2026-09-25T03:57 [BBC World] Xi got Trump's red carpet welcome - but not everything he wanted
  > China wanted progress on trade, technology and Taiwan - but hasn't got as much as it would have hoped for.
**B** (1 item(s))
- 2026-09-25T05:55 [South China Morning Post] AI war, Taiwan and translation: SCMP answers your questions from Xi-Trump summit
  > This live article is freely available to our registered users. Please log in or create an account.
Xi’s US summit: Access real-time updates, geopolitical risk analysis, and exclusive reporting from an Asian perspective. Subscribe now with our limited-time offer to stay ahead.
Chinese President Xi Ji

## R006
**A** (1 item(s))
- 2026-09-28T20:35 [Al Jazeera] Slovenia’s U-turn towards Israel
  > Slovenia’s policy towards Palestine has changed sharply following a UNGA sideline meeting with Israeli PM Netanyahu.
**B** (1 item(s))
- 2026-09-29T00:10 [Al Jazeera] Inside Al Jazeera’s UNGA coverage
  > Here’s a look at what it was like behind the scenes of the coverage you saw online and on TV.

## R007
**A** (1 item(s))
- 2026-09-27T09:43 [South China Morning Post] ‘Right now, it’s fine’: Trump brushes off questions about summit talk on Taiwan
  > US President Donald Trump has sought to play down exchanges with his Chinese counterpart Xi Jinping on Taiwan, saying on Saturday that they touched on the subject only briefly.
“We didn’t talk about it too much. Right now, it’s fine. It’s just moving along,” Trump said. “We didn’t spend a lot of tim
**B** (1 item(s))
- 2026-09-28T04:06 [South China Morning Post] Trump asked Xi if Beijing wanted US weapons: a joke, a gambit or something more?
  > Donald Trump asked President Xi Jinping whether Beijing wanted to buy American weapons, the US ambassador to China said on Sunday, prompting the State Department to quickly rule out any such deal with Washington’s principal strategic competitor.
“He actually asked President Xi, would he like to buy 

## R008
**A** (1 item(s))
- 2026-08-21T01:00 [South China Morning Post] Hong Kong financiers press for tax breaks after Singapore unveils rival scheme
  > Hong Kong should press ahead with its proposed tax break on carried interest, the performance fees earned by hedge fund and private equity managers, after Singapore unveiled a rival tax-exemption scheme, according to industry participants.
The bill, submitted to lawmakers in June and expected to com
**B** (1 item(s))
- 2026-08-21T12:08 [South China Morning Post] Singapore’s carrots for fund managers set to sharpen competition with Hong Kong
  > Singapore’s latest package of tax breaks and visa incentives for fund managers could enhance its appeal as a leading asset management hub, as competition with Hong Kong intensifies for global capital and high-value financial talent, analysts have said.
While the measures would help maintain Singapor

## R009
**A** (1 item(s))
- 2026-08-21T06:53 [South China Morning Post] As Harry plans UK return, can he patch up royal rift with Prince William?
  > William and Harry were united in grief as children by the tragic death of their mother, Princess Diana, but their relationship as adults has been ripped apart by anger and hurt.
The pair – dubbed “the heir and the spare” from an early age – have failed to put aside their differences, despite their f
**B** (1 item(s))
- 2026-08-21T18:29 [BBC World] Meghan in talks for role in Netflix series The Gentlemen, BBC understands
  > This would be Meghan's first significant acting role since her marriage to Prince Harry.

## R010
**A** (2 item(s))
- 2026-09-24T19:02 [BBC World] Four civilians killed in Pakistani strikes in Afghanistan, Taliban says
  > Pakistan says it struck 10 targets, adding the strikes were "strictly limited to identified military objectives".
- 2026-09-25T04:22 [Al Jazeera] Pakistani forces kill Afghan Taliban fighters in border escalation
  > Pakistan&#039;s security forces report ongoing cross-border fire in latest fighting with Afghanistan.
**B** (1 item(s))
- 2026-09-25T03:35 [Al Jazeera] Saudi, Turkish, Pakistani chiefs plan urgent talks amid Yemen fighting
  > Saudi Arabia, Turkiye and Pakistan move to deepen defence coordination as Houthi attacks and Yemen fighting intensify.

## R011
**A** (1 item(s))
- 2026-09-28T04:30 [South China Morning Post] Xi–Trump body language, Thailand’s tourist backlash: 5 weekend reads you missed
  > We have put together stories from our coverage last weekend to help you stay informed about news across Asia and beyond. If you would like to see more of our reporting, please consider subscribing.
1. What Trump and Xi revealed in the body language with their wives

2. Australia just changed its vis
**B** (2 item(s))
- 2026-09-28T06:24 [Al Jazeera] US, China list goods recommended for tariff cuts following Trump-Xi summit
  > Washington and Beijing announce details of agreement to reduce tariffs on $60bn of trade.
- 2026-09-28T09:16 [South China Morning Post] China resuming US coal imports among thin list of summit outcomes
  > China agreed to import at least 10 million tonnes of US coal in each of the next two years, marking one of the few concrete results from President Xi Jinping’s state visit to the United States.
The country will also lower tariffs on 1,619 US products, including coal, under a deal to reduce levies on

## R012
**A** (1 item(s))
- 2026-09-29 01:12 [BBC World] Are Trump's US government funded ads illegal?
  > President Trump has faced criticism after fronting adverts which were paid for by the US government.
**B** (1 item(s))
- 2026-09-29 20:56 [France 24] Public service announcement or Donald Trump propaganda?
  > The White House calls them public service announcements - like those used in past administrations. Almost everyone else doesn't agree, with three taxpayer-funded advertisements that glorify President Donald Trump drawing criticism from across the partisan divide. Legal experts say the ads violate fe

## R013
**A** (1 item(s))
- 2026-08-21T03:12 [South China Morning Post] Canadian premier says ‘erratic’ Trump ‘not to be trusted’ amid US trade feud
  > The premier of a Canadian province launched a blistering attack on US President Donald Trump on Thursday, calling him a “bad person” and “not to be trusted” and urging Canada to keep fighting rather than rush to make concessions in trade talks with Washington.
Manitoba Premier Wab Kinew said Canada 
**B** (2 item(s))
- 2026-08-22T18:20 [BBC World] Carney calls Trump's fresh tariffs a 'miscalculation' after trade talks collapse
  > Canada's prime minister said he was "reluctantly" announcing retaliatory tariffs as he accused the US of starting a trade war.
- 2026-08-22T20:10 [BBC World] Carney calls Trump's fresh tariffs a 'miscalculation' after trade talks collapse
  > Canada's prime minister said he was "reluctantly" announcing retaliatory tariffs as he accused the US of starting a trade war.

## R014
**A** (1 item(s))
- 2026-09-27T00:00 [Al Jazeera] Iran war live: Tehran awaits official response as Trump rejects Hormuz plan
  > US president rejects Iran&#039;s seven-day plan to reopen the Strait of Hormuz, saying the deal is not &#039;acceptable&#039;.
**B** (2 item(s))
- 2026-09-27T17:46 [Al Jazeera] ‘Iran ready for doomsday war’, FM Araghchi says
  > Foreign Minister Abbas Araghchi says Iran is prepared for war to resume, ‘even if it comes to a doomsday war’.
- 2026-09-28T00:00 [Al Jazeera] Iran war live: Tehran open to ‘real diplomacy’, ready for ‘apocalyptic war’
  > Abbas Araghchi&#039;s warning comes after Washington rejected a seven-day roadmap to end the war and reopen Strait of Hormuz.

## R015
**A** (2 item(s))
- 2026-08-31T09:56 [Al Jazeera] Spain’s Sanchez says Russia, Israel spread disinformation on Ceuta crisis
  > Sanchez cited EU research which had found that Russia ⁠and ⁠Israel both spread disinformation during the crisis.
- 2026-08-31T13:39 [South China Morning Post] Spain PM blames Russia, Israel for Ceuta migrant crisis’ disinformation
  > Spanish Prime Minister Pedro Sanchez said on Monday there were signs Russia and Israel had spread the disinformation over Spain’s migration policy that triggered last month’s rush of migrants into Ceuta, but no evidence of Moroccan involvement.
Over 72,000 migrants irregularly crossed ‌from Morocco 
**B** (1 item(s))
- 2026-09-01T15:33 [BBC World] Sexual assaults happening almost every day in Ceuta, prosecutors say
  > Most migrants have returned to neighbouring Morocco, but as many as 5,000 remain in the Spanish exclave.

## R016
**A** (1 item(s))
- 2026-09-30 12:01 [South China Morning Post] Did Beijing and Washington agree on a crisis prevention deal, or not?
  > Disagreement over how to prevent conflicts could account for differences in how Chinese and US accounts have characterised discussion on the topic during last week’s summit, analysts said.
Speaking at a White House arrival ceremony, Chinese President Xi Jinping said the two militaries should maintai
**B** (1 item(s))
- 2026-09-30 15:00 [South China Morning Post] Why did Trump and Xi seal a deal on World War II soldiers’ missing remains?
  > A decades-long effort by Beijing and Washington to recover the remains of US servicemen missing in China since World War II has resurfaced in the wake of the summit between the nations’ leaders.
The commitment was included in an eight-point list of outcomes from Chinese President Xi Jinping’s three-

## R017
**A** (1 item(s))
- 2026-08-31T04:19 [Al Jazeera] People return to their flood-ravaged homes in Nepal
  > Survivors in Nepal’s Nuwakot district are digging through mud and debris for belongings left behind by flash floods.
**B** (4 item(s))
- 2026-08-31T06:05 [South China Morning Post] Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000
  > Rescuers from China and Nepal continued searching landslide- and flood-affected areas on Monday while efforts to reopen roads to the heart of the disaster-hit area at Gyirong Port entered a “critical stage”.
The death toll in Nepal had risen to 903 as of 9am on Monday, with 4,247 people still missin
- 2026-08-31T07:34 [Al Jazeera] Nepal races to rescue trapped workers, as flood death toll surpasses 900
  > Nepal officials say rescuers focusing on reaching workers in hydropower project tunnels in flood-stricken region.
- 2026-09-01T06:02 [BBC World] The final minutes before floodwater crashed through Nepal-China border
  > More than 100 Indians are missing at a vital Nepal-China trade crossing after devastating Himalayan floods.
- 2026-09-01T16:11 [BBC World] River water smashed into tunnel and chased me for 20 minutes, Nepal worker tells BBC
  > Major efforts to rescue hydropower workers continue as Nepal's death toll exceeds 1,000.

## R018
**A** (1 item(s))
- 2026-08-21T13:29 [Al Jazeera] Weddings in Gaza offer rare moments of joy amid genocide
  > In Gaza, weddings offer Palestinian families a brief escape from Israel’s genocidal war.
**B** (1 item(s))
- 2026-08-21T15:58 [BBC World] UK, Canada and Australia condemn Israel for refusing criminal probe into aid worker killings in Gaza
  > Seven World Central Kitchen workers were killed in the Israeli strike on their convoy in 2024.

## R019
**A** (2 item(s))
- 2026-09-27T17:46 [Al Jazeera] ‘Iran ready for doomsday war’, FM Araghchi says
  > Foreign Minister Abbas Araghchi says Iran is prepared for war to resume, ‘even if it comes to a doomsday war’.
- 2026-09-28T00:00 [Al Jazeera] Iran war live: Tehran open to ‘real diplomacy’, ready for ‘apocalyptic war’
  > Abbas Araghchi&#039;s warning comes after Washington rejected a seven-day roadmap to end the war and reopen Strait of Hormuz.
**B** (1 item(s))
- 2026-09-27T19:16 [South China Morning Post] Trump expects new Iran talks despite rejecting deal offer
  > US President Donald Trump said on Sunday that he expects talks with Iran to resume in the coming week, despite his rejection of a truce proposal put forward by Tehran.
Iranian officials brought with them to the UN General Assembly in New York a plan for a seven-day truce followed by the reopening of

## R020
**A** (1 item(s))
- 2026-09-28T15:29 [Al Jazeera] Iran denies link to attack on airbase as UK minister warns of ‘proxies’
  > Tehran condemns &#039;unfounded and malicious speculation&#039;; British FM vows to &#039;act against the proxies of Iran&#039;.
**B** (1 item(s))
- 2026-09-28T16:22 [Breaking Defense] UK to gather defense CEOs for ‘closed-door’ Russian security briefing
  > The government warned the Russian &#8220;state and its proxies knowingly seek to disrupt businesses and organisations that underpin the British way of life or are vital to the defence of Ukraine.&#8221;

## R021
**A** (1 item(s))
- 2026-08-21T14:00 [South China Morning Post] OpenAI-backed legal tech firm pivots to Chinese Kimi K3 open-weight model
  > A US artificial intelligence start-up backed by OpenAI has built its first in-house model on Chinese lab Moonshot AI’s Kimi K3, highlighting a growing shift by Western tech firms towards Chinese open-weight systems amid soaring development costs.
San Francisco-based legal tech provider Harvey, whose
**B** (1 item(s))
- 2026-08-21T15:00 [South China Morning Post] China and US push Southeast Asia over their AI blocs. Will it test region’s non-alignment?
  > Southeast Asian leaders have long insisted they will not be forced to pick sides in the great-power rivalry between the US and China. But their posture is about to be further tested.
This time, the battleground is AI. While Washington wants the region locked into Pax Silica – its bid to build a Chin

## R022
**A** (1 item(s))
- 2026-09-24T11:19 [Defense News] Report: CIA warned Europe of Russian drone attack from vessels in the Mediterranean
  > VIENNA — The CIA has warned European countries of a suspected Russian plot to launch Gerbera-type drones from aboard commercial vessels in the Mediterranean, a new report says.Major Spanish daily El Mundo published the article, which was based on testimony from an anonymous Lithuanian intelligence s
**B** (1 item(s))
- 2026-09-25T06:03 [South China Morning Post] France to protect key Saudi oil terminal as Houthis step up missile attacks
  > President Emmanuel Macron said France would send troops to defend an oil plant in Saudi Arabia as the Iran-backed Houthi militia took responsibility for new attacks on the kingdom.
Macron said in a television interview Thursday with TF1 and France 2 that he would send soldiers and military support t

## R023
**A** (1 item(s))
- 2026-09-29 21:05 [France 24] Trump says he doesn't want to work with China on AI safety
  > US President Donald Trump discussed AI development with dozens of tech bosses at the White House on Tuesday. Ahead of his "super intelligence" luncheon, Trump launched a new AI-powered website for government services, vowing not to stifle the technology's growth. He also said he didn't want to work 
**B** (1 item(s))
- 2026-09-30 03:00 [Al Jazeera] Trump backs AI self-regulation at tech summit but is it enough?
  > US President Donald Trump and leading tech companies have signed a voluntary agreement to regulate AI development.

## R024
**A** (1 item(s))
- 2026-09-25T00:44 [BBC World] Netanyahu defends Israeli military action as delegates walk out before UN speech
  > The Israeli leader labels those who left his speech at the UN General Assembly as "moral cowards".Â
**B** (1 item(s))
- 2026-09-25T03:49 [Al Jazeera] Jewish protestors join Free Palestine march to denounce Netanyahu
  > Al Jazeera’s Emma Withrow reports from a Free Palestine march, where Jewish demonstrators rejected Netanyahu.

## R025
**A** (1 item(s))
- 2026-09-29 22:00 [South China Morning Post] Xi-Trump summit drew Chinese CEOs. So why couldn’t they get a seat at the table?
  > As American billionaires gathered at the White House to honour Chinese President Xi Jinping and his wife Peng Liyuan last Thursday, a group of Chinese business leaders spent the evening on the sidelines.
They had travelled to the US capital to join the state dinner. But their invitations never arriv
**B** (2 item(s))
- 2026-10-01 14:00 [South China Morning Post] China backs Cuba, Beijing’s Panama threat, new UN chief: 7 Latin America relations reads
  > We have selected seven of the most interesting and important news stories covering Latin American relations from the past few weeks. If you would like to see more of our reporting, please consider subscribing.
1. China pledges to ‘firmly support’ Cuba as US escalates pressure on Havana

China will s
- 2026-10-02 20:52 [Al Jazeera] Latin America sees China as more positive global influence than US: Poll
  > Annual Latinobarometro survey finds views of China’s influence improving as perceptions of US influence worsen.

## R026
**A** (2 item(s))
- 2026-09-25T03:13 [South China Morning Post] Trump autopen joke at Biden’s expense draws rare laugh from China’s Xi
  > Chinese President Xi Jinping broke into rare laughter as his US counterpart Donald Trump showed him a framed “autopen” displayed in place of the former American leader Joe Biden’s portrait during a White House tour.
The viral moment stood out against the Chinese leader’s otherwise restrained demeano
- 2026-09-25T08:05 [South China Morning Post] Trump gives Xi a tour of his pet White House building projects, including the ballroom
  > Property developer-turned-president Donald Trump appeared to relish showing off the White House’s latest building works to Xi Jinping on Thursday, eager to give his Chinese counterpart a glimpse of his construction ambitions since they last met in China.
In May, Trump was hosted at Beijing’s Great H
**B** (1 item(s))
- 2026-09-25T03:57 [BBC World] Xi got Trump's red carpet welcome - but not everything he wanted
  > China wanted progress on trade, technology and Taiwan - but hasn't got as much as it would have hoped for.

## R027
**A** (1 item(s))
- 2026-09-28 19:59 [White House] Nominations Sent to the Senate
  > Nominations Sent to the Senate				
			
			
					
	
		
		
			Search
					
						
		
			
				
					Select Category				
				
																		
								All News							
																								
								Briefings &amp; Statements							
																								
																	
										All Presidentia
**B** (1 item(s))
- 2026-09-29 21:23 [White House] Eliminating Disease-Carrying Pests And Restoring Enjoyment Of The Great Outdoors
  > ELIMINATING DISEASE-CARRYING PESTS AND RESTORING ENJOYMENT OF THE GREAT OUTDOORS				
			
			
					
	
		
		
			Search
					
						
		
			
				
					Select Category				
				
																		
								All News							
																								
								Briefings &amp; Statements							
																		

## R028
**A** (2 item(s))
- 2026-09-25T03:13 [South China Morning Post] Trump autopen joke at Biden’s expense draws rare laugh from China’s Xi
  > Chinese President Xi Jinping broke into rare laughter as his US counterpart Donald Trump showed him a framed “autopen” displayed in place of the former American leader Joe Biden’s portrait during a White House tour.
The viral moment stood out against the Chinese leader’s otherwise restrained demeano
- 2026-09-25T08:05 [South China Morning Post] Trump gives Xi a tour of his pet White House building projects, including the ballroom
  > Property developer-turned-president Donald Trump appeared to relish showing off the White House’s latest building works to Xi Jinping on Thursday, eager to give his Chinese counterpart a glimpse of his construction ambitions since they last met in China.
In May, Trump was hosted at Beijing’s Great H
**B** (1 item(s))
- 2026-09-25T05:55 [South China Morning Post] AI war, Taiwan and translation: SCMP answers your questions from Xi-Trump summit
  > This live article is freely available to our registered users. Please log in or create an account.
Xi’s US summit: Access real-time updates, geopolitical risk analysis, and exclusive reporting from an Asian perspective. Subscribe now with our limited-time offer to stay ahead.
Chinese President Xi Ji

## R029
**A** (1 item(s))
- 2026-08-21T05:00 [BBC World] Israel re-establishes closed West Bank settlement, defying growing international protests
  > Thirty "pioneer families" have arrived on a wave of nationalism driven by Israel's government, but the rapid change has left nearby Palestinian residents fearful.
**B** (1 item(s))
- 2026-08-22T12:51 [Al Jazeera] Jewish activists push back against Israeli settlers
  > Jewish activists provide a ‘protective presence’ to deter settler violence in parts of the Occupied West Bank.

## R030
**A** (1 item(s))
- 2026-08-31T07:10 [South China Morning Post] Malaysia’s air quality turns hazardous as Indonesian wildfires burn
  > Air pollution in Malaysia’s Bornean state of Sarawak has surged into hazardous territory, with the air pollutant index (API) topping 400 in the worst-hit district, as forest fires raging in Indonesia continue to send thick smoke drifting across the border.
Serian in Sarawak, closest to the frontier 
**B** (1 item(s))
- 2026-08-31T22:05 [BBC World] Orangutans in danger as wildfires blaze through Borneo
  > Wildfires in Indonesia have destroyed part of the natural habitat of hundreds of orangutans, risking the survival of the species.

## R031
**A** (1 item(s))
- 2026-09-27T17:29 [Al Jazeera] One month after Nepal’s catastrophic floods, thousands remain missing
  > A month after floods tore through Nepal, 5,285 people remain missing and more than 1,100 are still in holding centres.
**B** (1 item(s))
- 2026-09-28T04:44 [Al Jazeera] 14 killed, a dozen missing as Nepal is hit by more floods and landslides
  > At least 14 people have been killed and 11 remain missing after heavy rain triggered floods and landslides across Nepal.

## R032
**A** (1 item(s))
- 2026-08-21T18:29 [BBC World] Meghan in talks for role in Netflix series The Gentlemen, BBC understands
  > This would be Meghan's first significant acting role since her marriage to Prince Harry.
**B** (1 item(s))
- 2026-08-22T00:03 [BBC World] As they return to the UK, Harry and Meghan search for a brand that sticks
  > They will not be working royals when they come back. So what could they be doing instead?

## R033
**A** (1 item(s))
- 2026-09-29 13:26 [Al Jazeera] Estonia says Russia ordered August arson attack on defence company
  > Tallinn accuses Moscow of responsibility for the fire at Estonian company Milrem Robotics, a supplier of unmanned ground vehicles to Ukraine.
**B** (1 item(s))
- 2026-10-01 14:13 [Defense News] Taiwan takes a page from Ukraine’s playbook in steeling society for an invasion
  > NEW TAIPEI CITY, Taiwan — Taiwan President Lai Ching-te told a forum in late September he was seeking “resilience through unity” with a new alliance that would let world officials and non-governmental groups prepare together in case of disaster.For Taiwan, that could mean an attack or blockade by th

## R034
**A** (1 item(s))
- 2026-09-30 23:13 [South China Morning Post] Trump claims he discussed release of political prisoners in China with Xi at summit
  > US President Donald Trump said on Wednesday that he discussed the release of political prisoners in China with his counterpart, Xi Jinping, in Washington last week.
“We talked, and I think we had some very, very important discussions. Hopefully fruitful discussions,” Trump told reporters in the Whit
**B** (1 item(s))
- 2026-10-01 19:10 [South China Morning Post] Xi leaves Washington, but keeps at least two places on the White House walls
  > Chinese President Xi Jinping has left Washington, but he still has a place at the White House. At least two, in fact.
Two different photographs of Xi with US President Donald Trump feature on its walls: a handshake image that Trump showed his guest during last week’s state visit, and another beside 

## R035
**A** (1 item(s))
- 2026-09-29 16:02 [Council of the EU Press] MFF 2028-2034: Council agrees negotiating position on future EU support for the fisheries sector
  > Council agrees partial negotiating position on the EU support to fisheries, aquaculture and maritime policy for 2028-2034.
**B** (1 item(s))
- 2026-09-29 22:00 [European Commission Press] Commission report finds devastating shifts in the Arctic and record-breaking marine heatwaves
  > European Commission Press release Brussels, 30 Sep 2026 The ocean is changing at an alarming pace with direct consequences for marine life, coastlines and communities all across the world. That is the main conclusion of the tenth report on the state of the ocean, published today by the Marine Enviro

## R036
**A** (1 item(s))
- 2026-09-25T00:44 [BBC World] Netanyahu defends Israeli military action as delegates walk out before UN speech
  > The Israeli leader labels those who left his speech at the UN General Assembly as "moral cowards".Â
**B** (1 item(s))
- 2026-09-25T02:26 [Al Jazeera] Contrasting treatment of Israel and Palestine on display at the UN
  > Israel’s Prime Minister addressed the UN General Assembly in person, despite having an ICC arrest warrant.

## R037
**A** (1 item(s))
- 2026-09-28T04:44 [Al Jazeera] 14 killed, a dozen missing as Nepal is hit by more floods and landslides
  > At least 14 people have been killed and 11 remain missing after heavy rain triggered floods and landslides across Nepal.
**B** (1 item(s))
- 2026-09-28T05:28 [Al Jazeera] ‘Still a lockdown’: Deadly floods hit Nepal tourism as peak season begins
  > As Himalayan nation recovers from devastating floods, a million people dependent on tourism struggle to make ends meet.

## R038
**A** (1 item(s))
- 2026-09-29 22:00 [South China Morning Post] Xi-Trump summit drew Chinese CEOs. So why couldn’t they get a seat at the table?
  > As American billionaires gathered at the White House to honour Chinese President Xi Jinping and his wife Peng Liyuan last Thursday, a group of Chinese business leaders spent the evening on the sidelines.
They had travelled to the US capital to join the state dinner. But their invitations never arriv
**B** (1 item(s))
- 2026-10-01 09:40 [Al Jazeera] Can Europe still compete with the US and China?
  > Europe faces growing pressure from the US and China as it struggles to stay competitive.

## R039
**A** (1 item(s))
- 2026-09-27T14:36 [Al Jazeera] Strait of Hormuz tensions linger as Iran and US move further from a deal
  > There are fears of renewed fighting between the US and Iran, after President Trump rejected a deal.
**B** (1 item(s))
- 2026-09-27T20:34 [Al Jazeera] ‘Atrocious’ crime: Cuban official decries possibility of US military action
  > Cuba&#039;s deputy foreign minister slams US sanctions, labelling them &#039;equivalent to genocide&#039;.

## R040
**A** (1 item(s))
- 2026-08-21T13:01 [Al Jazeera] Israeli soldiers throw belongings from besieged Palestinian home
  > Israeli soldiers were filmed throwing belongings from Palestinian homes in Qusra.
**B** (1 item(s))
- 2026-08-21T16:00 [Al Jazeera] Israeli settlers set fire to heavy machinery at West Bank quarry
  > Israeli settlers entered a stone quarry in Wadi Al-Rakheem near Hebron overnight and set fire to heavy machinery

## R041
**A** (1 item(s))
- 2026-09-30 23:25 [BBC World] China has cracked down on AI relationships. Is it ahead of the game?
  > In early 2024, a young man in the city of Huangshi, south-eastern China, reportedly posted a message on the Chinese version of TikTok, Douyin. The caption read: "Farewell to this world."

Within minutes, the suicide prevention team at Douyin kicked into gear. The team, which is staffed 24 hours a da
**B** (1 item(s))
- 2026-10-01 02:00 [South China Morning Post] Chinese women spend top dollar on male model shoots, turning staged romance into viral trend
  > A growing number of young Chinese women are paying for romantic photo shoots with male models, seeking a brief taste of love through a novel form of emotional companionship.
This trend has gained significant traction on mainland social media, with customers spending up to 8,000 yuan (US$1,200) for a

## R042
**A** (1 item(s))
- 2026-08-31T00:41 [Al Jazeera] What are the implications of the US-Venezuela oil deal?
  > Opposition in Venezuela as interim leader insists the deal with Washington will help with the country&#039;s recovery.
**B** (1 item(s))
- 2026-08-31T10:18 [Al Jazeera] The looming failure of Operation Economic Outcast
  > The latest package of US sanctions on Iran is unlikely to achieve Washington’s objectives.

## R043
**A** (1 item(s))
- 2026-09-29 14:40 [Defense News] US forces exiting Iraq after 2 decades, leaving opening for Iran
  > U.S. forces are set to depart from their last bases in Iraq by Wednesday, a move celebrated as a victory by Iran and its allies, who now have deep influence in the country where 4,500 Americans died during more than two decades of war.Iraqi security experts say the withdrawal — agreed to in 2024 und
**B** (1 item(s))
- 2026-09-30 00:00 [Al Jazeera] Iran war live: Trump claims war will end ‘very soon’, gives no details
  > Top leadership in Iran reviews latest US response offer to end war as economic turmoil and political concerns rise.

## R044
**A** (1 item(s))
- 2026-10-01 09:40 [Al Jazeera] Can Europe still compete with the US and China?
  > Europe faces growing pressure from the US and China as it struggles to stay competitive.
**B** (2 item(s))
- 2026-10-01 14:00 [South China Morning Post] China backs Cuba, Beijing’s Panama threat, new UN chief: 7 Latin America relations reads
  > We have selected seven of the most interesting and important news stories covering Latin American relations from the past few weeks. If you would like to see more of our reporting, please consider subscribing.
1. China pledges to ‘firmly support’ Cuba as US escalates pressure on Havana

China will s
- 2026-10-02 20:52 [Al Jazeera] Latin America sees China as more positive global influence than US: Poll
  > Annual Latinobarometro survey finds views of China’s influence improving as perceptions of US influence worsen.

## R045
**A** (4 item(s))
- 2026-08-31T06:05 [South China Morning Post] Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000
  > Rescuers from China and Nepal continued searching landslide- and flood-affected areas on Monday while efforts to reopen roads to the heart of the disaster-hit area at Gyirong Port entered a “critical stage”.
The death toll in Nepal had risen to 903 as of 9am on Monday, with 4,247 people still missin
- 2026-08-31T07:34 [Al Jazeera] Nepal races to rescue trapped workers, as flood death toll surpasses 900
  > Nepal officials say rescuers focusing on reaching workers in hydropower project tunnels in flood-stricken region.
- 2026-09-01T06:02 [BBC World] The final minutes before floodwater crashed through Nepal-China border
  > More than 100 Indians are missing at a vital Nepal-China trade crossing after devastating Himalayan floods.
- 2026-09-01T16:11 [BBC World] River water smashed into tunnel and chased me for 20 minutes, Nepal worker tells BBC
  > Major efforts to rescue hydropower workers continue as Nepal's death toll exceeds 1,000.
**B** (1 item(s))
- 2026-08-31T10:17 [Al Jazeera] Nepal tunnel traps hinder flood rescue: How many are dead or missing?
  > Flash floods on the Nepal-Tibet border have left nearly 5,000 people missing, many trapped in hydropower tunnels.

## R046
**A** (2 item(s))
- 2026-09-27T09:16 [South China Morning Post] Pope meets victims of sex abuse, urges ‘wise leaders’ as French election looms
  > Pope Leo waved at believers on his way to mass on Sunday in the French pilgrimage town of Lourdes where he is to meet victims of clerical sex abuse on a third day of an official visit to France.
The leader of the world’s 1.4 billion Catholics is on a four-day trip to France, a secular country with d
- 2026-09-27T23:14 [Al Jazeera] Pope pledges action on clergy child abuse in meeting with French survivors
  > Head of the Roman Catholic Church holds &#039;emotional&#039; two-hour meeting with seven survivors in French town of Lourdes.
**B** (1 item(s))
- 2026-09-27T11:38 [BBC World] 'Scourge' of abuse must be rooted out, says Pope during Lourdes visit
  > Pope Leo spoke to bishops before leading a service attended by thousands of worshippers in France.

## R047
**A** (1 item(s))
- 2026-09-30 06:48 [Al Jazeera] Trump calls Kim Jong Un a ‘friend’ and plays down N Korea’s nuclear arsenal
  > US president&#039;s comments came after he was asked why North Korea can have nuclear weapons when Iran cannot.
**B** (1 item(s))
- 2026-10-02 14:00 [South China Morning Post] ‘America is back’, AI ‘conspiracy’, China’s Laos deal: 7 global relations reads
  > We have selected seven of the most interesting and important news stories covering global relations from the past few weeks. If you would like to see more of our reporting, please consider subscribing.
1. Trump condemns ‘sick conspiracy’ against AI, says he is only guardrail needed

US President Don

## R048
**A** (1 item(s))
- 2026-09-27T17:54 [South China Morning Post] UK Labour Party meets buoyed by Burnham but seeking concrete plans
  > Britain’s ruling Labour Party on Sunday launched its first annual conference under Andy Burnham’s leadership, buoyed by his debut as prime minister as he pledged to take the tough decisions needed to tackle looming challenges.
The former mayor of Manchester has injected new life into the centre-left
**B** (1 item(s))
- 2026-09-28T11:13 [Defense News] UK’s Healey puts defense in focus for reindustrialization push
  > LIVERPOOL, England — British finance minister John Healey will put his support firmly behind firms investing in defense on Monday, part of what he will describe as a new industrialization drive to try to spur the nation’s anaemic economic growth.In his first speech to the governing Labour Party’s an

## R049
**A** (1 item(s))
- 2026-09-27T14:07 [Al Jazeera] Yemen’s health system could collapse in some areas, minister warns
  > Yemen&#039;s healthcare system may not be able to support the population as war strains resources, minister tells Al Jazeera.
**B** (1 item(s))
- 2026-09-27T21:16 [BBC World] Inside Yemen's front-line city as Houthis battle for control
  > In rare access to Yemen's conflict zone the BBC travels to the front line with pro-government soldiers.

## R050
**A** (1 item(s))
- 2026-09-29 15:20 [Breaking Defense] House intel committee could investigate defense firm contributions to White House ballroom
  > Rep. Jim Himes, the top Democrat on the House Permanent Select Committee on Intelligence, sent a Sept. 28 letter to a defense trade group warning of a &#8220;likely&#8221; probe into the project.
**B** (1 item(s))
- 2026-09-30 04:36 [Al Jazeera] Democrats hope anger at Trump enough to get young people to vote
  > Political strategist Celinda Lake says that young voters don’t usually cast their ballots in midterm elections.

## R051
**A** (1 item(s))
- 2026-09-28T05:14 [South China Morning Post] Xiaomi-backed robotics chip designer clears hearing, eyes US$100m Hong Kong IPO: sources
  > Zhuhai Amicro Technology, a Xiaomi-backed chipmaker, is preparing to begin premarketing for a Hong Kong initial public offering (IPO) of more than US$100 million as early as this week, according to people familiar with the matter.
The company passed its listing hearing with bourse operator Hong Kong
**B** (1 item(s))
- 2026-09-28T09:29 [South China Morning Post] Hong Kong customs arrests 2, seizes HK$290,000 of ‘slimming injections’ from Japan
  > Hong Kong customs officers have seized 400 so-called slimming injections imported from Japan, with an estimated market value of about HK$290,000 (US$36,970), and arrested two local residents in an operation earlier this month.
The case came to light on September 5, when officers intercepted a suspic

## R052
**A** (1 item(s))
- 2026-09-29 23:33 [BBC World] Ukraine's prized steel industry left in ruins by Russian missile campaign
  > Ukraine's remaining steelworks, a vital part of its economy, have all but ground to a halt because of relentless attacks.
**B** (1 item(s))
- 2026-09-30 11:32 [Al Jazeera] Russian attacks on Ukraine’s Kyiv region kill four, target power grid
  > City officials say three killed in Ukraine&#039;s capital, as emergency services say child killed in the surrounding region.

## R053
**A** (1 item(s))
- 2026-08-31T06:05 [South China Morning Post] China warns of ‘major risk’ of glacier collapse as Tibet-Nepal death toll nears 1,000
  > China warned on Monday there was a “major risk” of further glacier collapses and landslides along the border with Nepal as the death toll from last week’s deadly mudslide rose to close to 1,000.
The Ministry of Water Resources said there was an ongoing threat along the Cuojian River in Nepal, a wate
**B** (1 item(s))
- 2026-08-31T10:17 [Al Jazeera] Nepal tunnel traps hinder flood rescue: How many are dead or missing?
  > Flash floods on the Nepal-Tibet border have left nearly 5,000 people missing, many trapped in hydropower tunnels.

## R054
**A** (1 item(s))
- 2026-08-31T04:19 [Al Jazeera] People return to their flood-ravaged homes in Nepal
  > Survivors in Nepal’s Nuwakot district are digging through mud and debris for belongings left behind by flash floods.
**B** (1 item(s))
- 2026-08-31T16:42 [BBC World] 'I haven't lost my hope' - the search for missing loved ones
  > Relatives of those still missing in the fatal floods in Nepal hold onto hope that their loved ones have survived.

## R055
**A** (1 item(s))
- 2026-09-27T08:06 [South China Morning Post] Why Southeast Asia feels relief and caution after the Xi-Trump summit
  > Southeast Asia welcomes the continued thaw in US-China ties after the Xi-Trump summit, with analysts saying that less friction between the two powers over issues such as the South China Sea could lower the pressure on the region.
Yet, caution persists as the summit left deeper disputes unresolved.
“
**B** (1 item(s))
- 2026-09-27T09:43 [South China Morning Post] ‘Right now, it’s fine’: Trump brushes off questions about summit talk on Taiwan
  > US President Donald Trump has sought to play down exchanges with his Chinese counterpart Xi Jinping on Taiwan, saying on Saturday that they touched on the subject only briefly.
“We didn’t talk about it too much. Right now, it’s fine. It’s just moving along,” Trump said. “We didn’t spend a lot of tim

## R056
**A** (1 item(s))
- 2026-08-21T00:00 [Al Jazeera] Iran war live: US vows toughest Iran sanctions, urges China support
  > US Treasury Secretary Bessent says new economic measures will &#039;collapse&#039; Iranian government.
**B** (1 item(s))
- 2026-08-21T12:12 [Al Jazeera] US designates Hezbollah an Iranian proxy, sanctions funding network
  > The US Treasury labels Lebanon-based group &#039;an extension&#039; of the IRGC&#039;s Quds Force and takes aim at financing.

## R057
**A** (2 item(s))
- 2026-09-28T12:08 [Al Jazeera] Child among three killed off French coast in Channel crossing attempt
  > France&#039;s maritime police ‌‌said ​they received a distress ​call from an inflatable dinghy carrying 105 people.
- 2026-09-28T13:48 [South China Morning Post] Child and 2 women ‘crushed to death’ during France to UK sea crossing
  > A 10-year-old child and two women died on Monday on the treacherous and illegal migration route across the English Channel from France, apparently trampled to death on a packed boat, French authorities said.
The dinghy left the area of Sangatte in northern France at around 5.15am carrying 105 people
**B** (1 item(s))
- 2026-09-28T16:37 [Al Jazeera] French police fire tear gas at migrants on beach
  > French police have used tear gas to disperse migrants attempting to cross the English Channel to Britain from France.

## R058
**A** (1 item(s))
- 2026-09-27T20:03 [Al Jazeera] Why has Trump rejected Iran’s peace proposal?
  > The US president has reportedly threatened to resume strikes on Iran.
**B** (1 item(s))
- 2026-09-28T11:18 [South China Morning Post] UK investigates if arrests near US-run base prevented Iran-linked attack
  > British police were holding five men on Monday and examining suspected explosives found near a US-operated air force base in England, as counterterror detectives investigated whether the arrests foiled an attempted attack linked to Iran.
The men were detained early on Sunday after three vans were sp

## R059
**A** (1 item(s))
- 2026-09-27T20:03 [Al Jazeera] Why has Trump rejected Iran’s peace proposal?
  > The US president has reportedly threatened to resume strikes on Iran.
**B** (1 item(s))
- 2026-09-28T09:17 [Al Jazeera] Oil prices surge after Trump rejects Iran’s plan to reopen Strait of Hormuz
  > Brent crude rises more than 3 percent to top $107 a barrel as Washington dismisses Tehran&#039;s proposal to end war.

## R060
**A** (1 item(s))
- 2026-08-22T12:51 [Al Jazeera] Jewish activists push back against Israeli settlers
  > Jewish activists provide a ‘protective presence’ to deter settler violence in parts of the Occupied West Bank.
**B** (1 item(s))
- 2026-08-22T15:45 [Al Jazeera] Settlers target Palestinian homes in Occupied West Bank’s Area B
  > Palestinians in Qaryut say Israeli settlers, backed by the military, are forcing families from their homes.

## R061
**A** (1 item(s))
- 2026-09-30 08:00 [South China Morning Post] EU weighs sweeping new trade powers against China before make-or-break October
  > Brussels and Berlin are steeling themselves for a make-or-break October with China, as the mood towards Beijing hardens in both capitals.
The month ahead could help set the course of the increasingly thorny EU-China relationship for years to come, as Europe gears up to present a slew of new tools fo
**B** (1 item(s))
- 2026-09-30 09:06 [European Commission Press] Daily News 30 / 09 / 2026
  > European Commission Daily news Brussels, 30 Sep 2026 European Centre for Democratic Resilience launches cooperation with stakeholders
The European Centre for Democratic Resilience launched the first phase of its S...

## R062
**A** (1 item(s))
- 2026-09-25T04:43 [South China Morning Post] Pitch perfect cultural diplomacy wins heart of China’s first lady Peng Liyuan
  > While their husbands held talks at the White House, Melania Trump hosted Peng Liyuan at the Smithsonian National Museum of Asian Art on Thursday, where the famed Chinese soprano softly hummed along to a youth choir’s performance of a familiar classic.
Footage shows the Hope Chinese School youth choi
**B** (2 item(s))
- 2026-09-25T06:56 [Al Jazeera] Nepal’s leader labels devastating flood a ‘warning to the world’
  > Prime Minister Balendra Shah says world leaders must act on climate change.
- 2026-09-25T07:02 [South China Morning Post] Flood-ravaged Nepal pushes for climate deal with India, China
  > Nepal’s Prime Minister Balendra Shah proposed a climate alliance with neighbouring India and China, urging action to protect the fragile Himalayan ecosystem after catastrophic flooding across the region.
“Glaciers and floods do not travel with stamps and passports,” Shah told world leaders at the Un

## R063
**A** (1 item(s))
- 2026-10-01 01:58 [South China Morning Post] Xi-Trump rapport is ‘most valuable strategic asset’ in US-China ties, envoy Xie says
  > The Chinese ambassador to the United States, Xie Feng, on Wednesday described the personal rapport and “mutual respect” between Chinese President Xi Jinping and US President Donald Trump as the “most valuable strategic asset in our bilateral relations”.
“Their personal connection and in-depth dialog
**B** (1 item(s))
- 2026-10-01 10:02 [South China Morning Post] Days after Xi-Trump summit, the US marks China’s National Day with pared-down note
  > Five days after Chinese President Xi Jinping left Washington, the US State Department marked the 77th anniversary of the People’s Republic of China with a greeting short enough to fit on a calling card.
US Secretary of State Marco Rubio’s congratulatory statement landed on Wednesday, a few hours bef

## R064
**A** (5 item(s))
- 2026-09-29 15:04 [BBC Mundo] La anciana Maricarmen podrá volver a su casa tras el desalojo que puso el foco en la crisis de vivienda en España
  > De acuerdo a lo señalada por la abogada, la empresa dueña del inmueble le dejará pagar un alquiler acorde a la pensión que recibe.
- 2026-09-29 18:08 [Clarín Mundo] Los reyes de España despliegan todo el protocolo para recibir a Emmanuel y Brigitte Macron en visita oficial
  > El rey Felipe y la reina Letizia le dieron la bienvenida al presidente de Francia en el Palacio Real de Madrid.Por la noche brindaron una cena de gala para los Macron en la que no faltaron la elegancia y la tiara del joyero de la reina.
- 2026-09-29 18:43 [Clarín Mundo] Presionado por las protestas, Pedro Sánchez anuncia decretos clave para enfrentar la crisis de la vivienda en España
  > Las medidas apuntan a frenar los desalojos y controlar los fondos buitres. Además,  los contratos de alquiler vigentes puedan extenderse automáticamente por dos años.Para que las normas mantengan sus efectos en el tiempo, el Parlamento tiene que aprobarlo dentro de los 30 días.
- 2026-09-29 22:57 [France 24 Español] Macron aboga en su visita a España por una "Europa más fuerte" ante el auge del "extremismo"
  > En el primer día de su visita de Estado a España, el presidente Emmanuel Macron pidió el martes 29 de septiembre una inversión masiva para una "Europa más fuerte" y para "recuperar el control" de las redes sociales y la inteligencia artificial, a las que consideró responsables del "cansancio democrá
**B** (1 item(s))
- 2026-09-30 09:13 [France 24] Attention turns to economy on final day of Macron’s visit to Spain
  > President Emmanuel Macron is in Spain for the final day of his two-day state visit, the first by a French president to the country since 2009. After being welcomed with a banquet at the Royal Palace by King Felipe VI on Tuesday, on today's agenda is the opening of the Franco-Spanish economic forum a

## R065
**A** (1 item(s))
- 2026-09-28T14:59 [Defense News] EU nails down five defense priority areas to channel common spending
  > PARIS — European Union member states approved five projects for joint defense-industrial investment in priority areas including drones and counter-drone systems as well as air and missile defense, part of efforts to encourage more cooperation on defense spending and avoid overlap in the 27-nation bl
**B** (1 item(s))
- 2026-09-29T07:31 [South China Morning Post] Beijing and Berlin ‘exchanged opinions’ amid reported plan to shut China out of EU market
  > Chinese Commerce Minister Wang Wentao held a video call with German Economy Minister Katherina Reiche on Monday, just over a week before the next round of trade talks between Beijing and Brussels, amid reports that Germany and France are pushing for a new tool that would enable the EU to swiftly shu

## R066
**A** (4 item(s))
- 2026-09-28 16:05 [Council of the EU Press] Council strengthens EU space threat response architecture
  > The Council has adopted a decision strengthening the EU Space Threat Response Architecture to respond to increased irresponsible and hostile behaviour in the space domain.
- 2026-09-29 22:00 [European Commission Press] Factsheet: EU Critical Communication System
  > European Commission Factsheet Brussels, 30 Sep 2026   Factsheet: EU Critical Communication System Factsheet: EU Critical Communication System
- 2026-09-29 22:00 [European Commission Press] Questions and answers on the European Union Critical Communication System
  > European Commission Questions and answers Brussels, 30 Sep 2026 What is the European Union Critical Communication System?
The European Union Critical Communication System (EUCCS) connects national critical communication syst...
- 2026-09-29 22:00 [European Commission Press] Commission proposes a new EU Critical Communication System for first responders
  > European Commission Press release Brussels, 30 Sep 2026 Today, the European Commission proposed to establish a new EU Critical Communication System to provide Europe's first responders with secure and resilient communication channels in crisis situations.
**B** (1 item(s))
- 2026-09-30 09:06 [European Commission Press] Daily News 30 / 09 / 2026
  > European Commission Daily news Brussels, 30 Sep 2026 European Centre for Democratic Resilience launches cooperation with stakeholders
The European Centre for Democratic Resilience launched the first phase of its S...

## R067
**A** (1 item(s))
- 2026-08-21T00:48 [South China Morning Post] Russia tests missiles near Japanese-claimed islands after Putin’s visit
  > Russia’s Pacific Fleet said on Thursday it has conducted a missile test off a group of Russian-held, Japanese-claimed islands amid an intensifying row over the disputed territory following President Vladimir Putin’s first-ever visit there last week.
While it was unclear exactly when the test was car
**B** (1 item(s))
- 2026-08-22T13:13 [BBC World] Rescuers dig through Ukraine mall wreckage as Zelensky condemns 'despicable' Russian strike
  > Four people are still missing after Friday's attack which killed 16 and left 130 injured, including a number of children.

## R068
**A** (1 item(s))
- 2026-08-21T13:30 [Al Jazeera] Ebola outbreak ‘growing faster, ⁠⁠wider’ as DRC death toll passes 2,500: UN
  > Epidemic remains out of control amid DR Congo conflict, funding shortages and attacks on health workers and facilities
**B** (2 item(s))
- 2026-08-22T10:13 [Al Jazeera] More than 16,000 doses of Ervebo vaccine arrive in Ebola-hit DR Congo
  > The doses are the first of 70,000 allocated for Kinshasa as experts warn of the virus&#039;s exponential spread.
- 2026-08-22T11:15 [Al Jazeera] Ebola continues to spread in the DRC as 16,000 vaccine doses arrive
  > Health authorities are warning that ‘approximately one person has been dying from Ebola every thirty minutes’.

## R069
**A** (2 item(s))
- 2026-09-28T17:06 [Al Jazeera] Russia strike sets National Academy of Sciences of Ukraine ablaze
  > A Russian drone struck the National Academy of Sciences of Ukraine in central Kyiv, killing one person
- 2026-09-28T17:37 [Al Jazeera] Photos: Russian drone strikes pound civilian targets across Kyiv
  > Russian drones have struck Ukraine’s National Academy of Sciences in the historic centre of Kyiv, as Moscow’s forces continue to pound the capital around the clock.

Ukrainian officials reported that at least seven people were killed and more than 80 wounded on Monday as Russian strikes hit apartmen
**B** (1 item(s))
- 2026-09-29T03:38 [Al Jazeera] Russia pounds Ukraine’s Kyiv after deadly strike on Academy of Sciences
  > Footage of attack on Academy shows people leaning out of windows as bright flames engulf part of the historic building.

## R070
**A** (1 item(s))
- 2026-08-31T04:29 [South China Morning Post] Asean urged to take on Big Tech after Meta’s record payout
  > Calls are growing for Asean to collectively crack down on Big Tech platforms that spread scams and harmful content, spurred on by Meta Platforms’ landmark US$18 billion US settlement last week.
Meta agreed on Wednesday to enact sweeping changes to Instagram and Facebook – including default time limi
**B** (1 item(s))
- 2026-08-31T21:28 [BBC World] Amazon rigged $20bn worth of ad prices, US lawsuit alleges
  > Amazon responded to the lawsuit, arguing the US Federal Trade Commission "misunderstands" their ad market.

## R071
**A** (1 item(s))
- 2026-08-31T11:25 [Al Jazeera] UAE intercepts drone after US and Iran exchange attacks
  > The UAE says it intercepted a drone coming from Iran and rejected &#039;false&#039; reports of an attack on its Al Menhad airbase.
**B** (1 item(s))
- 2026-08-31T14:57 [Al Jazeera] Why has Greece signed a $3.5bn missile deal with Israel?
  > Analysts say Greece is concerned about threats posed by the US-Israel war on Iran and Turkiye&#039;s growing capabilities.

## R072
**A** (1 item(s))
- 2026-08-31T06:05 [South China Morning Post] China warns of ‘major risk’ of glacier collapse as Tibet-Nepal death toll nears 1,000
  > China warned on Monday there was a “major risk” of further glacier collapses and landslides along the border with Nepal as the death toll from last week’s deadly mudslide rose to close to 1,000.
The Ministry of Water Resources said there was an ongoing threat along the Cuojian River in Nepal, a wate
**B** (4 item(s))
- 2026-08-31T06:05 [South China Morning Post] Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000
  > Rescuers from China and Nepal continued searching landslide- and flood-affected areas on Monday while efforts to reopen roads to the heart of the disaster-hit area at Gyirong Port entered a “critical stage”.
The death toll in Nepal had risen to 903 as of 9am on Monday, with 4,247 people still missin
- 2026-08-31T07:34 [Al Jazeera] Nepal races to rescue trapped workers, as flood death toll surpasses 900
  > Nepal officials say rescuers focusing on reaching workers in hydropower project tunnels in flood-stricken region.
- 2026-09-01T06:02 [BBC World] The final minutes before floodwater crashed through Nepal-China border
  > More than 100 Indians are missing at a vital Nepal-China trade crossing after devastating Himalayan floods.
- 2026-09-01T16:11 [BBC World] River water smashed into tunnel and chased me for 20 minutes, Nepal worker tells BBC
  > Major efforts to rescue hydropower workers continue as Nepal's death toll exceeds 1,000.

## R073
**A** (1 item(s))
- 2026-09-30 22:01 [BBC World] Trekkers helicoptered off mountains as more deadly landslides hit Nepal
  > A month after mass catastrophic flooding, around 30 people have died in landslides and heavy rain.
**B** (1 item(s))
- 2026-10-02 06:45 [South China Morning Post] Missing Malaysian found safe in flood-ravaged Nepal after 37 days
  > One of the Malaysians unaccounted for following the devastating floods in Nepal has been confirmed safe and has returned to Malaysia, according to the group representing Malaysians missing in Nepal.
Malaysia Solidarity: Families in Hope (Masfih) spokesman Manivannan Rethinam said the person had repo

## R074
**A** (1 item(s))
- 2026-09-28T04:56 [Al Jazeera] Sudanese army impounds dozens of motorcycles in Blue Nile curfew
  > Dozens of motorcycles were impounded in Sudan’s Blue Nile State, after their riders were accused of flouting a curfew.
**B** (1 item(s))
- 2026-09-28T11:00 [Al Jazeera] Ethiopia accuses Sudan, Egypt of backing Tigray rebels as fighting rages
  > Sudan army denies backing Tigray fighters, says rival paramilitary RSF receiving support from within Ethiopia.

## R075
**A** (1 item(s))
- 2026-08-31T02:45 [South China Morning Post] Nepal floods: could foreign rescue teams have been brought in earlier?
  > The Nepalese government has appealed for rescue aid from other countries just two days after it reportedly refused help, as several hundred people are still believed to be trapped in hydropower tunnels and thousands remain missing following the catastrophic flash flooding at the border with China la
**B** (1 item(s))
- 2026-08-31T10:17 [Al Jazeera] Nepal tunnel traps hinder flood rescue: How many are dead or missing?
  > Flash floods on the Nepal-Tibet border have left nearly 5,000 people missing, many trapped in hydropower tunnels.

## R076
**A** (1 item(s))
- 2026-08-21T13:01 [Al Jazeera] Israeli soldiers throw belongings from besieged Palestinian home
  > Israeli soldiers were filmed throwing belongings from Palestinian homes in Qusra.
**B** (1 item(s))
- 2026-08-22T12:51 [Al Jazeera] Jewish activists push back against Israeli settlers
  > Jewish activists provide a ‘protective presence’ to deter settler violence in parts of the Occupied West Bank.

## R077
**A** (1 item(s))
- 2026-08-31T14:42 [Al Jazeera] War and heat: Why are wheat prices soaring?
  > Russia and Ukraine have stepped up attacks on their respective grain terminals in the Black Sea.
**B** (1 item(s))
- 2026-09-01T10:30 [BBC World] Russian attack hits rail workers in new deadly strikes on Kyiv
  > Ukrainian officials say 20 people, including two children, were injured in the capital and the wider region.

## R078
**A** (1 item(s))
- 2026-09-27T09:53 [South China Morning Post] 7 teens swept up in police crackdown on bicycle-related offences in Tseung Kwan O
  > Hong Kong police have clamped down on bicycle-related offences in Tseung Kwan O, with seven teenagers facing prosecution for allegedly failing to display bike lights at night and cycling on pavements.
In a social media post on Saturday, police in Tseung Kwan O district said officers had recently iss
**B** (1 item(s))
- 2026-09-27T13:58 [South China Morning Post] Hong Kong police hunt for man who stole HK$10,000 from claw machines using key
  > Hong Kong police are searching for a man who used a key to steal about HK$10,000 (US$1,275) from four claw machines’ deposit boxes at a store on Sunday.
The force said that the store owner, a 46-year-old man surnamed Cheung, had filed a police report at around 11.10am after witnessing the theft via 

## R079
**A** (1 item(s))
- 2026-09-28T17:43 [Al Jazeera] Iran touts Hormuz attacks as oil flows increase despite tensions
  > Mediators are trying to facilitate more talks, but Washington signals faith in its pressure tactics.
**B** (1 item(s))
- 2026-09-29T08:15 [Al Jazeera] US-Iran talks continue, but ‘deal unlikely’ before midterm elections
  > The US and Iran are talking through mediators, but there are major differences over what a deal should look like.

## R080
**A** (1 item(s))
- 2026-09-29T07:34 [Al Jazeera] Israeli forces kill Hamas commander Izz al-Din al-Beik in Gaza attack
  > Head of Hamas&#039;s armed wing in northern Gaza killed in ⁠an Israeli strike on an apartment building in Gaza City.
**B** (1 item(s))
- 2026-09-29T08:01 [Al Jazeera] Israeli settlers attack Jalud village in occupied West Bank, torch homes
  > A group of settlers attacked two homes belonging to the Al-Tubasi family in northern West Bank village.

## R081
**A** (1 item(s))
- 2026-08-31T04:30 [South China Morning Post] China-Nepal floods, Japan to deploy fighter jets to India: 5 weekend reads you missed
  > We have put together stories from our coverage last weekend to help you stay informed about news across Asia and beyond. If you would like to see more of our reporting, please consider subscribing.
1. What Japan’s coming fighter jet deployment to India means for China
Japan plans to deploy fighter j
**B** (1 item(s))
- 2026-08-31T12:00 [South China Morning Post] Why Japan’s hypersonic and underwater weapon plans might worry China
  > In its latest swipe at Tokyo’s military build-up, China singled out Japan’s plans to arm its submarine drones with long-range missiles and test hypersonic weapons in Australia.
Analysts say those moves could threaten People’s Liberation Army amphibious groups and surface combatants within the “first

## R082
**A** (1 item(s))
- 2026-08-21T13:44 [BBC World] Ebola vaccine trial to start in DR Congo as warning issued over speed of infections
  > About half of the 2,500 recorded deaths from Ebola happened in the last 20 days, the WHO says.
**B** (2 item(s))
- 2026-08-22T10:13 [Al Jazeera] More than 16,000 doses of Ervebo vaccine arrive in Ebola-hit DR Congo
  > The doses are the first of 70,000 allocated for Kinshasa as experts warn of the virus&#039;s exponential spread.
- 2026-08-22T11:15 [Al Jazeera] Ebola continues to spread in the DRC as 16,000 vaccine doses arrive
  > Health authorities are warning that ‘approximately one person has been dying from Ebola every thirty minutes’.

## R083
**A** (1 item(s))
- 2026-08-31T04:00 [South China Morning Post] Xi is in Bishkek for SCO summit. How does bloc fit China’s Eurasian strategy 25 years on?
  > As Washington’s strategic focus shifts and energy and grain supply disruptions continue to unsettle the Middle East, Beijing’s expanding presence across Central Asia is expected to be in focus as Kyrgyzstan hosts the Shanghai Cooperation Organisation (SCO) summit this week.
Chinese President Xi Jinp
**B** (3 item(s))
- 2026-08-31T04:18 [Al Jazeera] Russia, China leaders to meet at Shanghai Cooperation Organisation summit
  > The organisation is not officially anti-West, but Russian and Chinese leaders have used it to amplify their worldview.
- 2026-08-31T08:47 [Al Jazeera] Xi, Modi and Putin attend SCO summit: What’s on the agenda?
  > The two-day summit aims to promote a vision of a multipolar world and mutual trade ties amid Trump&#039;s unilateralism.
- 2026-08-31T08:47 [Al Jazeera] Xi, Modi and Putin set to meet for SCO summit: What’s on the agenda?
  > The two-day summit aims to promote a vision of a multipolar world and mutual trade ties amid Trump&#039;s unilateralism.

## R084
**A** (1 item(s))
- 2026-08-31T04:30 [South China Morning Post] China-Nepal floods, Japan to deploy fighter jets to India: 5 weekend reads you missed
  > We have put together stories from our coverage last weekend to help you stay informed about news across Asia and beyond. If you would like to see more of our reporting, please consider subscribing.
1. What Japan’s coming fighter jet deployment to India means for China
Japan plans to deploy fighter j
**B** (1 item(s))
- 2026-08-31T06:05 [South China Morning Post] China warns of ‘major risk’ of glacier collapse as Tibet-Nepal death toll nears 1,000
  > China warned on Monday there was a “major risk” of further glacier collapses and landslides along the border with Nepal as the death toll from last week’s deadly mudslide rose to close to 1,000.
The Ministry of Water Resources said there was an ongoing threat along the Cuojian River in Nepal, a wate

## R085
**A** (1 item(s))
- 2026-09-25T03:57 [BBC World] Xi got Trump's red carpet welcome - but not everything he wanted
  > China wanted progress on trade, technology and Taiwan - but hasn't got as much as it would have hoped for.
**B** (4 item(s))
- 2026-09-25T05:48 [South China Morning Post] From wine to ping-pong, Trump and Xi’s state dinner is heavy on historic symbolism
  > When US President Donald Trump hosted Chinese President Xi Jinping in the East Room, every detail of the state dinner was steeped in symbolism, with sparkling wine served as a nod to a pivotal moment in Sino-US relations and references to “ping-pong diplomacy”.
The meal opened with a toast of Schram
- 2026-09-25T07:00 [South China Morning Post] Xi-Trump dinner puts US tech titans in spotlight – what does it mean for China ties?
  > If the American guests seated at the head table with President Xi Jinping and US President Donald Trump at Thursday’s White House state dinner were any indication, Washington now views its relationship with Beijing largely through the prism of technology.
Analysts said the seating arrangement unders
- 2026-09-25T07:19 [South China Morning Post] Xi’s security chief among cohort of rising officials at White House banquet
  > Zhou Hongxu, the official who oversees President Xi Jinping’s security, made an appearance at the White House state banquet on Thursday night, alongside a cohort of other rising Chinese officials.
The banquet’s guest list described the 55-year-old People’s Liberation Army (PLA) major general as both
- 2026-09-25T08:09 [BBC World] Trump and Xi exchange warm words at state dinner but little progress on key issues
  > Despite diplomatic niceties and gifts, little was shared on substantial issues separating the leaders.

## R086
**A** (1 item(s))
- 2026-09-28T18:16 [Al Jazeera] Trump made the right decision to reject Iran’s offer
  > The US president has denied Tehran the opportunity to use the US midterm elections as a pressure point.
**B** (1 item(s))
- 2026-09-28T23:20 [South China Morning Post] Judge blocks Trump from tying anti-terrorism grants to election changes
  > A US judge blocked the Trump administration on Monday from conditioning counterterrorism funds to state and local ‌governments on changes to election administration.
The decision by Washington-based US District Judge Amir Ali marks the latest defeat for US President Donald Trump in his bid to increa

## R087
**A** (1 item(s))
- 2026-09-27T09:43 [South China Morning Post] ‘Right now, it’s fine’: Trump brushes off questions about summit talk on Taiwan
  > US President Donald Trump has sought to play down exchanges with his Chinese counterpart Xi Jinping on Taiwan, saying on Saturday that they touched on the subject only briefly.
“We didn’t talk about it too much. Right now, it’s fine. It’s just moving along,” Trump said. “We didn’t spend a lot of tim
**B** (2 item(s))
- 2026-09-28T06:24 [Al Jazeera] US, China list goods recommended for tariff cuts following Trump-Xi summit
  > Washington and Beijing announce details of agreement to reduce tariffs on $60bn of trade.
- 2026-09-28T09:16 [South China Morning Post] China resuming US coal imports among thin list of summit outcomes
  > China agreed to import at least 10 million tonnes of US coal in each of the next two years, marking one of the few concrete results from President Xi Jinping’s state visit to the United States.
The country will also lower tariffs on 1,619 US products, including coal, under a deal to reduce levies on

## R088
**A** (2 item(s))
- 2026-09-25T02:24 [Al Jazeera] More than 100 arrested as New Yorkers protest Netanyahu’s UN visit
  > Demonstrators blocked streets and marched towards UN headquarters as the Israeli PM addressed world leaders at UNGA.
- 2026-09-25T02:35 [Al Jazeera] NYC police arrest Susan Sarandon, other celebrities protesting Netanyahu
  > Rights groups accuse UN of hosting a &#039;war criminal&#039; as delegations walk out during Israeli prime minister&#039;s speech.
**B** (1 item(s))
- 2026-09-25T02:26 [Al Jazeera] Contrasting treatment of Israel and Palestine on display at the UN
  > Israel’s Prime Minister addressed the UN General Assembly in person, despite having an ICC arrest warrant.

## R089
**A** (1 item(s))
- 2026-09-29 14:50 [White House] Streamlining Access to Government Services Through America.gov
  > STREAMLINING ACCESS TO GOVERNMENT SERVICES THROUGH AMERICA.GOV				
			
			
					
	
		
		
			Search
					
						
		
			
				
					Select Category				
				
																		
								All News							
																								
								Briefings &amp; Statements							
																								
											
**B** (1 item(s))
- 2026-09-29 19:07 [White House] First Lady Melania Trump Announces 2026 Fall Garden Tours
  > oFFICE OF THE fIRST lADY				
			
							
					First Lady Melania Trump Announces 2026 Fall Garden Tours				
			
			
					
	
		
		
			Search
					
						
		
			
				
					Select Category				
				
																		
								All News							
																								
								Briefings &amp; Statements			

## R090
**A** (1 item(s))
- 2026-09-27T16:19 [Defense News] Terror suspects wanted to do ‘big damage’ to air base used by US, Trump says
  > British police on Sunday arrested five men near an air base used by U.S. forces on suspicion of explosive and terrorism offenses after a tip that three vans were heading to the military airfield, which has been used to strike Iran.U.S. President Donald Trump said the suspects had been looking to do 
**B** (1 item(s))
- 2026-09-27T20:03 [Al Jazeera] Why has Trump rejected Iran’s peace proposal?
  > The US president has reportedly threatened to resume strikes on Iran.

## R091
**A** (1 item(s))
- 2026-08-21T13:30 [Al Jazeera] Ebola outbreak ‘growing faster, ⁠⁠wider’ as DRC death toll passes 2,500: UN
  > Epidemic remains out of control amid DR Congo conflict, funding shortages and attacks on health workers and facilities
**B** (1 item(s))
- 2026-08-21T13:44 [BBC World] Ebola vaccine trial to start in DR Congo as warning issued over speed of infections
  > About half of the 2,500 recorded deaths from Ebola happened in the last 20 days, the WHO says.

## R092
**A** (1 item(s))
- 2026-09-29 22:00 [South China Morning Post] Xi-Trump summit drew Chinese CEOs. So why couldn’t they get a seat at the table?
  > As American billionaires gathered at the White House to honour Chinese President Xi Jinping and his wife Peng Liyuan last Thursday, a group of Chinese business leaders spent the evening on the sidelines.
They had travelled to the US capital to join the state dinner. But their invitations never arriv
**B** (4 item(s))
- 2026-10-02 08:26 [Al Jazeera] US delivers F-16V fighter jets to Taiwan as island eyes threat from China
  > Amid threats from China, Taipai is growing concerned about the Trump administration&#039;s commitment to arming the island.
- 2026-10-02 10:00 [South China Morning Post] Taiwan hails F-16V delivery as sign US support holds after Xi-Trump summit
  > Taiwan has hailed the much-delayed arrival of two F-16V fighter jets as a demonstration of continuing US military support, despite the summit between President Xi Jinping and US President Donald Trump.
The two single-seat aircraft, which reached Chihhang Air Base in the eastern county of Taitung on 
- 2026-10-02 14:15 [Defense News] Taiwan’s first two F-16V fighter jets arrive to bolster defenses against China
  > TAITUNG, Taiwan — The first two of a batch of 66 new F-16V Block 70 fighter jets ordered in 2019 arrived in Taiwan on Friday after months of delays, helping to strengthen an air force that has to scramble almost daily to shadow China’s military.Taiwan faces a rising military threat from Beijing, whi
- 2026-10-02 17:20 [Breaking Defense] After yearslong delay, Taiwan receives first pair of new F-16s
  > The two jets landed at an airbase in eastern Taiwan on Friday.

## R093
**A** (1 item(s))
- 2026-08-31T01:30 [South China Morning Post] Don’t leave Hong Kong parents to their own devices on child social media use
  > Hong Kong, a city of overachievers, especially when it comes to the young, is also filled with children who take to social media early. Almost 35 per cent of kindergarten pupils log at least one hour of recreational screen time daily. By the junior forms, 60 per cent exceed the international two-hou
**B** (1 item(s))
- 2026-08-31T09:27 [South China Morning Post] Singapore may require social media firms to set daily time limits for teens
  > Singapore plans to introduce legislation early next year requiring social media platforms to roll out stronger safeguards for teens, including possibly setting a daily time limit, Minister for Digital Development and Information Josephine Teo has said.
If a platform could not or did not want to intr

## R094
**A** (1 item(s))
- 2026-09-28T19:02 [Al Jazeera] American and six Ukrainians released by India after six months in jail
  > Matthew VanDyke and six Ukrainians were accused of smuggling weapons and drones to armed ethnic groups fighting India.
**B** (1 item(s))
- 2026-09-28T20:50 [South China Morning Post] US revokes visas from Latin American officials and families over accusations of corruption
  > The Trump administration is revoking the visas of 27 Latin American officials, former officials and their families, including Bolivia’s attorney general, over accusations of corruption.
The officials and their families come from Bolivia, Colombia, Ecuador and Peru - all nations with right-leaning le

## R095
**A** (1 item(s))
- 2026-08-21T12:05 [South China Morning Post] Trump eases tariffs on ground beef imports for 90 days
  > President Donald Trump announced on Friday that the United States would temporarily allow a greater volume of foreign beef imports, in his latest bid to lower costs for American consumers as midterm elections approach.
The US cattle herd has shrunk to its lowest level since the 1950s – in part due t
**B** (2 item(s))
- 2026-08-22T18:20 [BBC World] Carney calls Trump's fresh tariffs a 'miscalculation' after trade talks collapse
  > Canada's prime minister said he was "reluctantly" announcing retaliatory tariffs as he accused the US of starting a trade war.
- 2026-08-22T20:10 [BBC World] Carney calls Trump's fresh tariffs a 'miscalculation' after trade talks collapse
  > Canada's prime minister said he was "reluctantly" announcing retaliatory tariffs as he accused the US of starting a trade war.

## R096
**A** (1 item(s))
- 2026-09-28T13:00 [Al Jazeera] Thai police arrest jet skier after joyride through flooded Bangkok streets
  > Thai police arrest jet skier after joyride through flooded Bangkok streets
**B** (1 item(s))
- 2026-09-28T13:11 [South China Morning Post] At least 21 Hong Kong-Bangkok flights delayed amid flooding in Thai capital
  > At least 21 flights connecting Hong Kong and Bangkok were disrupted on Sunday and Monday, with passengers on one service leaving the Thai capital facing a nearly 24-hour delay after the Southeast Asian city was hit by its worst flood in 15 years.
Heavy rainfall lashed Bangkok – a top travel destinat

## R097
**A** (1 item(s))
- 2026-09-28T21:30 [South China Morning Post] In the US-China AI race, the real fight is keeping humans in control
  > The US-China AI competition faces a dilemma. Both countries see artificial intelligence as a source of economic, scientific and strategic power, so neither has much incentive to slow down. Yet the more capable and autonomous AI becomes, the more important the question of human control.
Last week’s s
**B** (1 item(s))
- 2026-09-28T22:48 [South China Morning Post] ‘Missed opportunity’: US soybean farmers question exclusion from China tariff cuts
  > US soybean farmers have described the exclusion of US soybeans from China’s import list under the newly announced Board of Trade mechanism as a “missed opportunity”, even as Beijing ramped up purchases of the crop ahead of last week’s summit between Chinese President Xi Jinping and US President Dona

## R098
**A** (1 item(s))
- 2026-09-28 12:00 [UN News] DPR Korea tells UN its nuclear status is ‘irreversible’, rejects outside pressure
  > The Democratic People’s Republic of Korea (DPRK) told the UN General Assembly on Monday that its status as a nuclear-armed State was irreversible, arguing that its military capabilities were necessary to safeguard the country’s sovereignty and maintain peace on the Korean Peninsula.
**B** (2 item(s))
- 2026-09-28 23:02 [UN Press] International Security Rapidly Deteriorates; General Assembly Urges Nations to Address Weaker Global Arms Treaties and Heightened Nuclear Risks
  > With nuclear arsenals expanding and arms control safeguards eroding worldwide, speakers today warned of mounting nuclear risks, from tensions in the Middle East and emerging technologies to the enduring consequences of nuclear testing, as the General Assembly held a high-level meeting to mark the In
- 2026-09-29 16:41 [UN Press] At ‘Most Dangerous Nuclear Moment’ Since Cold War Ended, Secretary-General Observance Message Urges Changing Course, Replacing Threats with Dialogue
  > Following are UN Secretary-General António Guterres’ remarks at the plenary meeting of the International Day for the Total Elimination of Nuclear Weapons, in New York today:

## R099
**A** (1 item(s))
- 2026-10-02 01:30 [South China Morning Post] ‘Money is money’: US, UK firms still coming to Hong Kong, commerce chief says
  > Companies from the United States, Britain and Singapore have been among the leading sources of inbound foreign capital in Hong Kong so far this year, the city’s commerce minister has said, insisting that “money is money” despite geopolitical instability.
In an exclusive, wide-ranging interview with 
**B** (1 item(s))
- 2026-10-02 09:05 [South China Morning Post] Hong Kong IPOs falter, China aids homebuyers, EU trade talks
  > Hong Kong stock debuts are losing steam as a deluge of initial public offerings (IPOs) overwhelms investor appetite.
Seven of September’s 12 IPOs fell on the first day of trading, raising the third-quarter total to 15 flops out of 31, based on Bloomberg data. By contrast, there were only 14 declines

## R100
**A** (1 item(s))
- 2026-09-28T19:42 [Al Jazeera] UAE confirms Netanyahu visit to Abu Dhabi
  > The visit takes place as the Israeli prime minister battles domestic turmoil ahead of October&#039;s Knesset elections
**B** (1 item(s))
- 2026-09-28T22:25 [South China Morning Post] Israel security agency files complaint over TV report that Netanyahu visited UAE
  > Israel’s domestic security service filed a complaint against a television channel that reported Prime Minister Benjamin Netanyahu visited the UAE, his office said on Monday, the government’s first acknowledgement of the trip despite not naming the destination.
“This evening the Shin Bet filed a comp

## R101
**A** (3 item(s))
- 2026-09-29 21:26 [Breaking Defense] Boeing wins Navy next-gen fighter F/A-XX competition
  > Boeing&#8217;s win gives it a monopoly on American sixth-gen fighters, following its 2025 selection to build the F-47.
- 2026-09-29 21:30 [Defense.gov] Department of War and U.S. Navy Award Contract for F/A-XX Program
  > The War Department announced a contract awarded by the U.S. Navy to Boeing for the Sixth-Generation F/A-XX Strike Fighter under the Next Generation Air Dominance program.
- 2026-09-29 22:20 [Defense News] US Navy selects Boeing to build next-generation F/A-XX fighter
  > Boeing has been selected to build the Navy’s sixth-generation carrier-based strike fighter, dubbed F/A-XX, icing out what was considered to be its biggest competitor in late-stage negotiations, Northrop Grumman. Inked at $20 billion for the full-scale development phase, the contract, according to a 
**B** (1 item(s))
- 2026-09-30 00:03 [Defense News] Why the Pentagon just dropped $450M on tungsten mining
  > The Defense Department announced this month a $450 million investment in The Elmet Group to strengthen the U.S. supply chain for tungsten, a critical mineral used for manufacturing military weapons ranging from bullets to missiles. The investment comes as a federal procurement rule barring tungsten 

## R102
**A** (1 item(s))
- 2026-08-21T13:59 [Al Jazeera] War on Iran: The US could focus on economically isolating Iran
  > The US Treasury Secretary, has indicated a change in US strategy towards Iran, focusing on economic isolation.
**B** (1 item(s))
- 2026-08-22T09:14 [Al Jazeera] Iran says new US sanctions violate sovereignty of other states
  > Foreign Ministry spokesman Esmaeil Baghaei slams Trump&#039;s latest threat as a return to &#039;full-scale classic colonialism&#039;.

## R103
**A** (1 item(s))
- 2026-09-29T07:10 [Al Jazeera] FIFA could disburse millions to members as Infantino seeks re-election
  > FIFA president Infantino is open to providing &#039;greatest level of additional funding&#039; to associations amid opposition.
**B** (1 item(s))
- 2026-09-29T11:12 [Al Jazeera] In FIFA-UEFA tussle, European body accused of ‘misinformation campaign’
  > FIFA accuses UEFA of attempting to influence its presidential election, in which Infantino is seeking a fourth term.

## R104
**A** (1 item(s))
- 2026-09-27T13:58 [South China Morning Post] Hong Kong police hunt for man who stole HK$10,000 from claw machines using key
  > Hong Kong police are searching for a man who used a key to steal about HK$10,000 (US$1,275) from four claw machines’ deposit boxes at a store on Sunday.
The force said that the store owner, a 46-year-old man surnamed Cheung, had filed a police report at around 11.10am after witnessing the theft via 
**B** (1 item(s))
- 2026-09-27T14:58 [South China Morning Post] Police arrest man, 34, over hidden cameras found in Hong Kong gym changing rooms
  > Hong Kong police have arrested a 34-year-old gym user in connection with the installation of three suspected pinhole cameras found in changing rooms at a 24/7 Fitness branch in Sha Tin.
The arrest on Sunday came a day after police launched an investigation into the suspected voyeurism case at the ou

## R105
**A** (1 item(s))
- 2026-09-25T02:26 [Al Jazeera] Contrasting treatment of Israel and Palestine on display at the UN
  > Israel’s Prime Minister addressed the UN General Assembly in person, despite having an ICC arrest warrant.
**B** (1 item(s))
- 2026-09-25T06:28 [Al Jazeera] Converging crises, chaos and walkouts dominate UNGA Day Three
  > Dozens of delegates walked out on Netanyahu, Yemen’s government pleaded for help, and Kuwait riled against threats.

## R106
**A** (3 item(s))
- 2026-09-27T12:07 [South China Morning Post] South African police probe mining feud shooting, 27 dead as elections near
  > South African police on Sunday were hunting the perpetrators of two separate shootings that killed 27 people within hours of each other, in stark reminders of the country’s problem with gun violence.
Officials were still establishing the motives for the shootings near Johannesburg and Cape Town, but
- 2026-09-27T14:09 [BBC World] Two mass shootings in South Africa leave 27 dead
  > The two attacks hours apart come as the country struggles to stop high levels of gang-related armed violence.
- 2026-09-27T16:58 [Al Jazeera] Dozens killed in two mass shootings in South Africa
  > At least 27 people have been killed in two mass shootings across South Africa.
**B** (2 item(s))
- 2026-09-27T18:44 [South China Morning Post] 3 people killed and 4 injured in shooting at Michigan strip club, police say
  > Three people were killed and four others were injured when an argument led to gunfire at an after-hours strip club on Sunday morning in Detroit, officials said.
Police responding to the 7.21am shooting on a largely residential street found three men who had been fatally shot, Detroit Police Chief To
- 2026-09-27T20:44 [Al Jazeera] Three killed, four injured in shooting at Detroit, Michigan, strip club
  > Police say the US shooting followed an altercation at an after-hours venue, and four people are in hospital.

## R107
**A** (1 item(s))
- 2026-08-21T16:00 [Al Jazeera] Israeli settlers set fire to heavy machinery at West Bank quarry
  > Israeli settlers entered a stone quarry in Wadi Al-Rakheem near Hebron overnight and set fire to heavy machinery
**B** (1 item(s))
- 2026-08-21T19:31 [BBC World] How Israel is expanding settlements in drive to reshape West Bank
  > There has been a significant expansion of building and road construction on Palestinian land occupied by Israel in recent years.

## R108
**A** (1 item(s))
- 2026-09-28 12:00 [UN News] DR Congo Ebola emergency: Calls grow for urgent humanitarian access
  > Aid teams&nbsp;trying to keep deadly Ebola disease from spreading in the Democratic Republic of the Congo (DRC) are increasingly concerned about ongoing fighting and violence that has forced thousands of people to flee a displacement camp in the vast, resource-rich east of the country.
**B** (1 item(s))
- 2026-09-29 12:00 [UN News] DRC: Early access to care and oxygen decisive for Ebola patients’ survival – WHO
  > In the Democratic Republic of the Congo (DRC), health workers fighting the country’s largest-ever Ebola outbreak are struggling to overcome critical challenges to patient care, the UN World Health Organization (WHO) warned on Tuesday.

## R109
**A** (1 item(s))
- 2026-08-31T12:01 [Al Jazeera] Who are the economic winners and losers of the US-Israel war on Iran?
  > Airlines and automakers have taken a hit, while banks and energy firms have raked in big profits.
**B** (1 item(s))
- 2026-08-31T13:00 [Al Jazeera] Can Iran use rockets to mine the Strait of Hormuz, as US claims?
  > Analysts say it&#039;s implausible but Iran is well-versed in adapting conventional weapons to suit its needs.

## R110
**A** (1 item(s))
- 2026-09-30 12:43 [South China Morning Post] Kuala Lumpur is world’s most polluted city due to haze, Singapore third, index shows
  > Malaysia’s capital topped a global pollution ranking on Wednesday and nearby Singapore came in third, with smoke from wildfires in neighbouring Indonesia blamed for the unhealthy conditions.
A milky haze has shrouded the cities for more than a month as smoke drifted from fires on Borneo and Sumatra 
**B** (1 item(s))
- 2026-10-02 06:45 [South China Morning Post] Missing Malaysian found safe in flood-ravaged Nepal after 37 days
  > One of the Malaysians unaccounted for following the devastating floods in Nepal has been confirmed safe and has returned to Malaysia, according to the group representing Malaysians missing in Nepal.
Malaysia Solidarity: Families in Hope (Masfih) spokesman Manivannan Rethinam said the person had repo

## R111
**A** (1 item(s))
- 2026-09-27T16:53 [Al Jazeera] Jerusalem Daily: Israeli opposition leaders unite to drive out Netanyahu
  > Jerusalem Daily: Israeli opposition leaders unite to drive out Netanyahu
**B** (1 item(s))
- 2026-09-27T19:04 [Al Jazeera] Stuck between Israeli military checkpoints
  > Israeli road closures have become a part of daily life for Palestinians in the occupied West Bank.

## R112
**A** (1 item(s))
- 2026-09-29 14:22 [Breaking Defense] Drone-hunting on the border, plus turmoil at an Air Force think tank
  > NORTHCOM is testing ways to counter drone incursions, while an Air Force institute focused on China faces questions about its future.
**B** (1 item(s))
- 2026-09-30 04:21 [BBC World] Restaurant named after Xi Jinping attacked by Chinese nationals in South Korea
  > The owner said he chose the name because he wanted to run the "best Chinese restaurant" in South Korea.

## R113
**A** (1 item(s))
- 2026-09-28T15:29 [Al Jazeera] Iran denies link to attack on airbase as UK minister warns of ‘proxies’
  > Tehran condemns &#039;unfounded and malicious speculation&#039;; British FM vows to &#039;act against the proxies of Iran&#039;.
**B** (1 item(s))
- 2026-09-28T17:15 [BBC World] Iran court upholds lashes sentence for singer who performed without hijab
  > Parastoo Ahmadi was convicted of "offending public decency" after singing while wearing a sleeveless dress during a livestreamed concert.

## R114
**A** (1 item(s))
- 2026-09-28 12:00 [UN News] DR Congo Ebola emergency: Calls grow for urgent humanitarian access
  > Aid teams&nbsp;trying to keep deadly Ebola disease from spreading in the Democratic Republic of the Congo (DRC) are increasingly concerned about ongoing fighting and violence that has forced thousands of people to flee a displacement camp in the vast, resource-rich east of the country.
**B** (3 item(s))
- 2026-09-28 23:02 [UN Press] Security Council, 10232nd Meeting (AM) Democratic Republic of the Congo/MONUSCO
  > Following its meeting concerning Haiti, the Council will convene to consider the situation in the Democratic Republic of the Congo. Anticipated briefers include James Swan, Head of the United Nations Organization Stabilization Mission in the Democratic Republic of the Congo (MONUSCO), as well as a r
- 2026-09-29 12:00 [UN News] Security Council LIVE: DRC peace deals fail to halt fighting as Ebola deepens crisis
  > The Security Council met in New York&nbsp;on the Democratic Republic of the Congo (DRC) Tuesday, where clashes between Government forces and M23 rebels continue in the east, despite a series of peace agreements. Ambassadors focused on ceasefire monitoring, rising tensions between the DRC and Rwanda 
- 2026-09-29 21:52 [UN Press] Commitments Must Yield Tangible Progress in Democratic Republic of Congo, Special Representative Tells Security Council
  > Serious challenges remain despite sustained diplomatic engagement to address the conflict in the eastern part of the Democratic Republic of the Congo, the Security Council heard today, as speakers welcomed the ceasefire monitoring and verification conducted by the UN mission in that country.

## R115
**A** (1 item(s))
- 2026-09-27T00:00 [Al Jazeera] Iran war live: Tehran awaits official response as Trump rejects Hormuz plan
  > US president rejects Iran&#039;s seven-day plan to reopen the Strait of Hormuz, saying the deal is not &#039;acceptable&#039;.
**B** (1 item(s))
- 2026-09-27T14:36 [Al Jazeera] Strait of Hormuz tensions linger as Iran and US move further from a deal
  > There are fears of renewed fighting between the US and Iran, after President Trump rejected a deal.

## R116
**A** (1 item(s))
- 2026-08-31T07:01 [South China Morning Post] Indonesia-US joint military drills with allies kick off with 4,700 soldiers
  > Indonesia, the United States and more than a dozen allies launched annual joint military exercises on Monday to boost defence capabilities and “deter aggression” in the Asia-Pacific region.
Jakarta maintains a neutral foreign policy, what it calls “free and active”, as it walks a diplomatic tightrop
**B** (1 item(s))
- 2026-08-31T14:00 [South China Morning Post] Prediction markets have priced the Trump-Xi summit. Do the bets have any value?
  > US President Donald Trump has already announced the date: September 24.
That is when, Trump says, Chinese President Xi Jinping will come to the White House for a visit following the “America first” leader’s own three-day trip to Beijing in May.
But there is a diplomatic wrinkle.
The Trump administra

## R117
**A** (1 item(s))
- 2026-09-29 14:05 [South China Morning Post] Legal aid chief denies stricter vetting as aid for policy challenges hits decade low
  > Hong Kong authorities approved only two legal aid applications for judicial review challenges against government policies and decisions last year, the fewest in the past decade, although its director has dismissed claims of tightened scrutiny or diminished access to justice.
The Legal Aid Department
**B** (1 item(s))
- 2026-10-03 09:04 [South China Morning Post] ‘Balanced and acceptable’: labour chief defends helper wage rise amid criticism
  > Hong Kong’s stronger economic performance over the past year was the reason for raising the monthly minimum wage for foreign domestic helpers by 2.35 per cent, the labour minister has said, amid disappointment from both unions and employers’ groups.
Defending the government’s decision to raise the m

## R118
**A** (1 item(s))
- 2026-09-27T14:36 [Al Jazeera] Strait of Hormuz tensions linger as Iran and US move further from a deal
  > There are fears of renewed fighting between the US and Iran, after President Trump rejected a deal.
**B** (1 item(s))
- 2026-09-27T17:42 [Al Jazeera] Mike Waltz: US offered to sell Iran uranium for civilian programme
  > US ambassador says Iran refused to agree to an arrangement where uranium would be supplied by Washington.

## R119
**A** (1 item(s))
- 2026-08-21T14:36 [Al Jazeera] Manchester City’s Maresca admits he needs time as Bournemouth visit in EPL
  > Enzo Maresca replaced Pep Guardiola between seasons but says Man City may need patience before more trophies arrive.
**B** (1 item(s))
- 2026-08-22T10:09 [Al Jazeera] Manchester City preview: Five key questions heading into 2026-27 season
  > Enzo Maresca faces the formidable challenge of following the legendary manager Pep Guardiola as new season starts.

## R120
**A** (1 item(s))
- 2026-08-21T08:03 [South China Morning Post] Indonesian quake survivors recall trauma of all-day intense aftershocks, self-rescue
  > Carolus Winfridus was asleep when an earthquake struck off Indonesia’s island of Flores, as he was awoken by intense rumbling and saw his wardrobe doors flying open.
He and his family quickly scrambled for a way out of their house in the town of Maumere, Sikka Regency, one of nine regencies hit by S
**B** (1 item(s))
- 2026-08-22T13:35 [Al Jazeera] Indonesia bolsters troop numbers to combat Borneo wildfires
  > Fires between January and July burned more than 200,000 hectares of land, says the government.

## R121
**A** (1 item(s))
- 2026-09-29T07:00 [South China Morning Post] Japanese firms pull back from China amid geopolitical tensions, supply chain shifts
  > The number of Japanese companies operating in China has fallen nearly 30 per cent since its peak in 2012 and is down 22 per cent over the past two years, according to a survey conducted amid prolonged political tensions between Beijing and Tokyo.
As of June, 10,118 Japanese enterprises were identifi
**B** (1 item(s))
- 2026-09-29T08:00 [South China Morning Post] ‘180-degree flip’ sees global investors turn to China for diversification: Pimco president
  > Global investors are turning to China again in search of alternatives to crowded US asset markets, with Pimco seeing Chinese bonds as one of the safest ways to diversify portfolios after sentiment towards the world’s second-largest economy “flipped 180 degrees”.
The US-based asset manager, which ove

## R122
**A** (4 item(s))
- 2026-09-25T05:48 [South China Morning Post] From wine to ping-pong, Trump and Xi’s state dinner is heavy on historic symbolism
  > When US President Donald Trump hosted Chinese President Xi Jinping in the East Room, every detail of the state dinner was steeped in symbolism, with sparkling wine served as a nod to a pivotal moment in Sino-US relations and references to “ping-pong diplomacy”.
The meal opened with a toast of Schram
- 2026-09-25T07:00 [South China Morning Post] Xi-Trump dinner puts US tech titans in spotlight – what does it mean for China ties?
  > If the American guests seated at the head table with President Xi Jinping and US President Donald Trump at Thursday’s White House state dinner were any indication, Washington now views its relationship with Beijing largely through the prism of technology.
Analysts said the seating arrangement unders
- 2026-09-25T07:19 [South China Morning Post] Xi’s security chief among cohort of rising officials at White House banquet
  > Zhou Hongxu, the official who oversees President Xi Jinping’s security, made an appearance at the White House state banquet on Thursday night, alongside a cohort of other rising Chinese officials.
The banquet’s guest list described the 55-year-old People’s Liberation Army (PLA) major general as both
- 2026-09-25T08:09 [BBC World] Trump and Xi exchange warm words at state dinner but little progress on key issues
  > Despite diplomatic niceties and gifts, little was shared on substantial issues separating the leaders.
**B** (1 item(s))
- 2026-09-25T05:55 [South China Morning Post] AI war, Taiwan and translation: SCMP answers your questions from Xi-Trump summit
  > This live article is freely available to our registered users. Please log in or create an account.
Xi’s US summit: Access real-time updates, geopolitical risk analysis, and exclusive reporting from an Asian perspective. Subscribe now with our limited-time offer to stay ahead.
Chinese President Xi Ji

## R123
**A** (1 item(s))
- 2026-09-28T18:07 [Defense News] Russia raises 2027 military spending by 27%, budget documents show
  > Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027, around 27% more than the 13.5 trillion roubles, or $159.8 billion, originally budgeted and the highest figure since the start of the war in Ukraine in 2022, government documents seen by Reuters showed on Monday. Tota
**B** (1 item(s))
- 2026-09-28T19:08 [South China Morning Post] Putin signs decree adding 15,500 troops to Russian army
  > Russian President Vladimir Putin signed a decree on Monday boosting the size of the army by 15,500 troops in the fourth such order this year.
Putin’s order comes as both Russia and Ukraine suffer mounting casualties in the more than four-and-a-half-year Ukraine war.
The decree did not give a reason 

## R124
**A** (2 item(s))
- 2026-09-28T21:45 [South China Morning Post] Pope Leo says concerns about AI doom scenarios are not ‘fake news’
  > Pope Leo on Monday ⁠said concerns that artificial intelligence ⁠could destroy the world are not “fake news” and should be taken seriously, in an apparent rebuke of US President Donald Trump.
The first US pope, who has warned of the dangers of AI throughout his 16-month papacy, also directly criticis
- 2026-09-29T04:51 [Al Jazeera] Pope Leo says AI risk concerns not ‘fake news’
  > Leader of the Catholic Church says AI safety issues should be taken seriously and acted on.
**B** (1 item(s))
- 2026-09-29T03:00 [Al Jazeera] Fighter jets escort Pope Leo on final day of his France tour
  > Pope Leo XIV was escorted by fighter jets to Metz, the final stop of his four-day France tour.

## R125
**A** (1 item(s))
- 2026-09-28T16:55 [Al Jazeera] Arming an adversary: Why Trump’s offer to sell China weapons belies US policy
  > Analysts dismissed Trump&#039;s proposal as lacking any strategic logic – but said it revealed how he views Beijing.
**B** (1 item(s))
- 2026-09-29T00:00 [Al Jazeera] Iran war live: Trump says he did not offer Tehran sanctions relief
  > US President Trump rejects a news report claiming his administration offered Iran sanctions relief and frozen funds.

## R126
**A** (1 item(s))
- 2026-08-31T00:43 [South China Morning Post] At your service: Hong Kong welcomes first humanoid robot-run convenience stores
  > Hong Kong’s first convenience stores operated by humanoid robots will open on Tuesday, with the Beijing-based company behind it planning to establish about 10 more outlets locally as it makes the city its first stop in “going overseas”.
Following an opening ceremony on Monday, the first “Galbot stor
**B** (1 item(s))
- 2026-08-31T01:30 [South China Morning Post] Don’t leave Hong Kong parents to their own devices on child social media use
  > Hong Kong, a city of overachievers, especially when it comes to the young, is also filled with children who take to social media early. Almost 35 per cent of kindergarten pupils log at least one hour of recreational screen time daily. By the junior forms, 60 per cent exceed the international two-hou

## R127
**A** (1 item(s))
- 2026-08-22T12:09 [Al Jazeera] Russian strikes kill 6 people in Ukraine, day after shopping complex attack
  > Meanwhile, Ukrainian drone hits home in southern Russia, killing two children and injuring their parents, officials say.
**B** (1 item(s))
- 2026-08-22T13:13 [BBC World] Rescuers dig through Ukraine mall wreckage as Zelensky condemns 'despicable' Russian strike
  > Four people are still missing after Friday's attack which killed 16 and left 130 injured, including a number of children.

## R128
**A** (1 item(s))
- 2026-09-29 14:00 [South China Morning Post] US Navy launches drone command that could reshape Taiwan war planning
  > The US Navy has set up a dedicated command to turn its growing array of aerial, surface and underwater drones into an integrated fighting force – a capability US commanders have linked to disrupting a PLA attack on Taiwan.
The Robotic and Autonomous Systems Warfighting Development Centre, formally e
**B** (1 item(s))
- 2026-09-30 23:13 [South China Morning Post] Trump claims he discussed release of political prisoners in China with Xi at summit
  > US President Donald Trump said on Wednesday that he discussed the release of political prisoners in China with his counterpart, Xi Jinping, in Washington last week.
“We talked, and I think we had some very, very important discussions. Hopefully fruitful discussions,” Trump told reporters in the Whit

## R129
**A** (1 item(s))
- 2026-09-28T13:00 [Al Jazeera] Thai police arrest jet skier after joyride through flooded Bangkok streets
  > Thai police arrest jet skier after joyride through flooded Bangkok streets
**B** (1 item(s))
- 2026-09-29T06:33 [South China Morning Post] One Bangkok flood battle after another as Thai Airways races to clear baggage backlog
  > Standing water ⁠in Thailand’s capital is expected ⁠to clear within three days if there is no additional rainfall, the government said on Tuesday, as flag carrier Thai Airways struggled to resume regular services following heavy rain and flooding.
The ‌cabinet will discuss long-term plans to address 

## R130
**A** (1 item(s))
- 2026-08-21T06:53 [South China Morning Post] As Harry plans UK return, can he patch up royal rift with Prince William?
  > William and Harry were united in grief as children by the tragic death of their mother, Princess Diana, but their relationship as adults has been ripped apart by anger and hurt.
The pair – dubbed “the heir and the spare” from an early age – have failed to put aside their differences, despite their f
**B** (1 item(s))
- 2026-08-21T13:39 [South China Morning Post] Prince Harry and others ordered to pay initial US$13 million in failed lawsuit
  > Prince Harry, Elton John ⁠and other high-profile claimants face paying ⁠millions of dollars out of their own pockets to cover the legal costs of the Daily Mail’s publisher after a judge ruled their failed privacy lawsuits were conducted in an unreasonable way.
Judge Matthew Nicklin’s judgment on cos

## R131
**A** (1 item(s))
- 2026-09-29T06:00 [South China Morning Post] China warns Japan over WWII history as business delegation visits Beijing
  > China’s top diplomat Wang Yi met Japan’s former foreign minister Takeshi Iwaya, who is leading a 50-member delegation of corporate executives, in Beijing on Monday, marking the highest-ranking Chinese official reception for a Japanese visit in nearly a year.
During the talks, Wang warned that bilate
**B** (1 item(s))
- 2026-09-29T07:00 [South China Morning Post] Japanese firms pull back from China amid geopolitical tensions, supply chain shifts
  > The number of Japanese companies operating in China has fallen nearly 30 per cent since its peak in 2012 and is down 22 per cent over the past two years, according to a survey conducted amid prolonged political tensions between Beijing and Tokyo.
As of June, 10,118 Japanese enterprises were identifi

## R132
**A** (1 item(s))
- 2026-09-27T07:44 [BBC World] Iranian minister says only negotiation can end conflict after Trump rejects Hormuz deal
  > The foreign minister says Tehran is waiting for an official rejection of a deal, despite the US President's comments.
**B** (1 item(s))
- 2026-09-27T19:16 [South China Morning Post] Trump expects new Iran talks despite rejecting deal offer
  > US President Donald Trump said on Sunday that he expects talks with Iran to resume in the coming week, despite his rejection of a truce proposal put forward by Tehran.
Iranian officials brought with them to the UN General Assembly in New York a plan for a seven-day truce followed by the reopening of

## R133
**A** (2 item(s))
- 2026-09-25T03:13 [South China Morning Post] Trump autopen joke at Biden’s expense draws rare laugh from China’s Xi
  > Chinese President Xi Jinping broke into rare laughter as his US counterpart Donald Trump showed him a framed “autopen” displayed in place of the former American leader Joe Biden’s portrait during a White House tour.
The viral moment stood out against the Chinese leader’s otherwise restrained demeano
- 2026-09-25T08:05 [South China Morning Post] Trump gives Xi a tour of his pet White House building projects, including the ballroom
  > Property developer-turned-president Donald Trump appeared to relish showing off the White House’s latest building works to Xi Jinping on Thursday, eager to give his Chinese counterpart a glimpse of his construction ambitions since they last met in China.
In May, Trump was hosted at Beijing’s Great H
**B** (4 item(s))
- 2026-09-25T05:48 [South China Morning Post] From wine to ping-pong, Trump and Xi’s state dinner is heavy on historic symbolism
  > When US President Donald Trump hosted Chinese President Xi Jinping in the East Room, every detail of the state dinner was steeped in symbolism, with sparkling wine served as a nod to a pivotal moment in Sino-US relations and references to “ping-pong diplomacy”.
The meal opened with a toast of Schram
- 2026-09-25T07:00 [South China Morning Post] Xi-Trump dinner puts US tech titans in spotlight – what does it mean for China ties?
  > If the American guests seated at the head table with President Xi Jinping and US President Donald Trump at Thursday’s White House state dinner were any indication, Washington now views its relationship with Beijing largely through the prism of technology.
Analysts said the seating arrangement unders
- 2026-09-25T07:19 [South China Morning Post] Xi’s security chief among cohort of rising officials at White House banquet
  > Zhou Hongxu, the official who oversees President Xi Jinping’s security, made an appearance at the White House state banquet on Thursday night, alongside a cohort of other rising Chinese officials.
The banquet’s guest list described the 55-year-old People’s Liberation Army (PLA) major general as both
- 2026-09-25T08:09 [BBC World] Trump and Xi exchange warm words at state dinner but little progress on key issues
  > Despite diplomatic niceties and gifts, little was shared on substantial issues separating the leaders.

## R134
**A** (1 item(s))
- 2026-08-31T08:56 [South China Morning Post] Hong Kong retail sales rise 4.5% in July, marking 15th straight month of growth
  > Hong Kong’s retail sector recorded growth for a 15th consecutive month in July, with the government reporting a 4.5 per cent increase year on year, although the pace of expansion slowed amid adverse weather and continued outbound travel by residents.
Retail sales value for the month reached HK$31 bi
**B** (1 item(s))
- 2026-08-31T09:00 [South China Morning Post] Hot property: Big banks, fashion stores seek ‘cheaper’, eye-catching Hong Kong retail
  > From big banks to fashion brands, tenants are taking advantage of potential lower rents for retail space in Hong Kong’s prime areas as they utilise eye-catching locations to boost visibility towards customers, according to agents.
HSBC is unveiling its first flagship branch at the Capitol Centre, wh

## R135
**A** (1 item(s))
- 2026-09-28T04:06 [South China Morning Post] Trump asked Xi if Beijing wanted US weapons: a joke, a gambit or something more?
  > Donald Trump asked President Xi Jinping whether Beijing wanted to buy American weapons, the US ambassador to China said on Sunday, prompting the State Department to quickly rule out any such deal with Washington’s principal strategic competitor.
“He actually asked President Xi, would he like to buy 
**B** (1 item(s))
- 2026-09-28T07:52 [BBC World] Trump-Xi summit: What wasn't said might matter the most
  > The most revealing thing about the summit in Washington may be what the two leaders did not say - and what we still don't know.

## R136
**A** (1 item(s))
- 2026-09-27T13:34 [Al Jazeera] Ethiopians celebrate Meskel and call for peace amid fighting
  > Ethiopians celebrate Meskel and call for peace amid fighting
**B** (1 item(s))
- 2026-09-28T09:44 [Al Jazeera] Al Jazeera reports from near front line in Ethiopia’s Afar region
  > Al Jazeera reports from Ethiopia’s Afar region, where fighting has spread amid efforts to oust PM Abiy Ahmed.

## R137
**A** (1 item(s))
- 2026-09-29 16:18 [Defense News] Pentagon awards Raytheon up to $20.7 billion to nearly double AMRAAM production
  > The Defense Department has awarded Raytheon a multiyear contract worth up to $20.7 billion to build Advanced Medium-Range Air-to-Air Missiles, or AMRAAMs. The Pentagon said the deal will nearly double AMRAAM production.The five-year contract, which includes two option years, is part of the Pentagon’
**B** (2 item(s))
- 2026-10-01 22:05 [Defense News] US Navy awards RTX’s Raytheon $24.4B for SM-6 missiles amid stockpile concerns
  > RTX’s Raytheon unit won a multiyear contract worth up to $24.4 billion to produce Standard Missile-6 interceptors for the U.S. Navy, the service said on Thursday, as the Pentagon pushes to replenish munitions stockpiles depleted by conflicts in the Middle East.The five-year contract, which includes 
- 2026-10-02 13:49 [Breaking Defense] Navy, Raytheon ink $24.4B deal for SM-6 ‘acceleration’
  > The deal covers at least five-years of production for an undisclosed number of missiles.

## R138
**A** (12 item(s))
- 2026-09-29 18:24 [El País Internacional] Trump lanza una página oficial de información sobre el Gobierno de EE UU que le desmiente
  > El presidente de Estados Unidos, Donald Trump, en el acto de presentación de la plataforma America.gov.
- 2026-09-29 19:04 [Il Sole 24 Ore Mondo] Trump, per Ai solo autoregolamentazione. Firmato l’ordine che cambia il nome in Super Intelligence
  > Pranzo alla Casa Bianca con decine di protagonisti dell’intelligenza artificiale americana per inaugurare la nuova era della Super Intelligenza. Nessuna menzione di rischi, crisi, e incidenti anche se forse nascerà un comitato consultivo di supervisione.
- 2026-09-29 20:36 [Rai News Esteri] Trump incontra i vertici Big Tech sulla sicurezza AI: "Autoregolazione e nessun controllo federale"
  > Un impegno "moralmente vincolante" a predisporre misure di salvaguardia. Zuckerberg: "Controlli interni robusti". Musk: "L'esito più probabile? Un futuro di abbondanza"
- 2026-09-29 20:36 [ANSA Mondo] Trump, 'da vertici big tech impegno moralmente vincolante su sicurezza IA'
  > 'Si autoregoleranno'
**B** (1 item(s))
- 2026-09-29 21:05 [France 24] Trump says he doesn't want to work with China on AI safety
  > US President Donald Trump discussed AI development with dozens of tech bosses at the White House on Tuesday. Ahead of his "super intelligence" luncheon, Trump launched a new AI-powered website for government services, vowing not to stifle the technology's growth. He also said he didn't want to work 

## R139
**A** (1 item(s))
- 2026-09-28 19:56 [White House] Mined, Melted, and Poured in America: President Trump Reverses Years of Anti-Mining Policy
  > News				
			
			
					
	
		
		
			Search
					
						
		
			
				
					Select Category				
				
																		
								All News							
																								
								Briefings &amp; Statements							
																								
																	
										All Presidential Actions									
							
**B** (1 item(s))
- 2026-09-29 19:21 [Rai News Esteri] Gli Usa prestano alle aziende energetiche 40 milioni di barili di petrolio delle riserve strategiche
  > Per contenere il caro carburante. Wright: "Anche i Paesi europei onorino gli impegni presi"

## R140
**A** (1 item(s))
- 2026-09-30 12:30 [South China Morning Post] US-China conflict doesn’t have to become a self-fulfilling prophecy
  > We are reminded seemingly daily of the great power transitions that ended in conflict. However, it is the exceptions – the ones that did not result in war – that could have real lessons to offer.
Today, the question is more than academic. Standing beside US President Donald Trump at the White House 
**B** (1 item(s))
- 2026-10-02 22:00 [South China Morning Post] ‘No retreat’: Key Trump ally urges continued US-China engagement on rare earths
  > US Republican Senator Steve Daines, a close aide to President Donald Trump and a key interlocutor between Washington and Beijing, has called on the two capitals to stay engaged and “not retreat” over differences on issues including rare earth supply chains.
Daines told the South China Morning Post t

## R141
**A** (1 item(s))
- 2026-08-21T03:12 [South China Morning Post] Canadian premier says ‘erratic’ Trump ‘not to be trusted’ amid US trade feud
  > The premier of a Canadian province launched a blistering attack on US President Donald Trump on Thursday, calling him a “bad person” and “not to be trusted” and urging Canada to keep fighting rather than rush to make concessions in trade talks with Washington.
Manitoba Premier Wab Kinew said Canada 
**B** (2 item(s))
- 2026-08-22T16:20 [BBC World] Carney faces crucial test after walking away from Trump's deal
  > The Canadian prime minister will have to sell his gamble that walking away from talks with the White House will be worth the consequences.
- 2026-08-22T20:02 [BBC World] Carney faces crucial test after walking away from Trump's deal
  > The Canadian prime minister will have to sell his gamble that walking away from talks with the White House will be worth the consequences.

## R142
**A** (1 item(s))
- 2026-09-28T13:38 [Al Jazeera] UN commemoration of Durban Declaration: What’s on agenda, who will attend?
  > UN General Assembly marks 25th anniversary of the 2011 Durban Declaration, which called for combating racism.
**B** (1 item(s))
- 2026-09-29T08:30 [Al Jazeera] UNGA 81: Five key takeaways from general debate
  > The 81st United Nations General Assembly ends with AI, Palestine and wars dominating speeches.

