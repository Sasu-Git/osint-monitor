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

**Cases:** 142. Draft labels: AMBIGUOUS 4, NO_RELATION 118, reaction_to 1, same_attack_wave 1, same_calamity_lifecycle 11, same_visit_or_summit 7.

| Case | A | B | Draft label | Direction | Confidence |
|---|---|---|---|---|---|
| [R001](#r001) | More Hong Kong consumers allege coercive beauty sales in wak | Over 100 ex-diplomats urge France, UK to sanction Israel ove | NO_RELATION | none | high |
| [R002](#r002) | Jurors in Lindsay Clancy trial deadlocked but judge asks the | Not just guilty or not - The jury's options in Lindsay Clanc | NO_RELATION | none | medium |
| [R003](#r003) | Russia, China leaders to meet at Shanghai Cooperation Organi | Prediction markets have priced the Trump-Xi summit. Do the b | NO_RELATION | none | high |
| [R004](#r004) | Nepal floods: could foreign rescue teams have been brought i | Rescue work intensifies as death toll in China-Nepal disaste | same_calamity_lifecycle | none | medium |
| [R005](#r005) | Xi got Trump's red carpet welcome - but not everything he wa | AI war, Taiwan and translation: SCMP answers your questions  | NO_RELATION | none | medium |
| [R006](#r006) | Slovenia’s U-turn towards Israel | Inside Al Jazeera’s UNGA coverage | NO_RELATION | none | high |
| [R007](#r007) | ‘Right now, it’s fine’: Trump brushes off questions about su | Trump asked Xi if Beijing wanted US weapons: a joke, a gambi | NO_RELATION | none | medium |
| [R008](#r008) | Hong Kong financiers press for tax breaks after Singapore un | Singapore’s carrots for fund managers set to sharpen competi | NO_RELATION | none | medium |
| [R009](#r009) | As Harry plans UK return, can he patch up royal rift with Pr | Meghan in talks for role in Netflix series The Gentlemen, BB | NO_RELATION | none | high |
| [R010](#r010) | Four civilians killed in Pakistani strikes in Afghanistan, T | Saudi, Turkish, Pakistani chiefs plan urgent talks amid Yeme | NO_RELATION | none | high |
| [R011](#r011) | Xi–Trump body language, Thailand’s tourist backlash: 5 weeke | US, China list goods recommended for tariff cuts following T | NO_RELATION | none | high |
| [R012](#r012) | Are Trump's US government funded ads illegal? | Public service announcement or Donald Trump propaganda? | NO_RELATION | none | medium |
| [R013](#r013) | Canadian premier says ‘erratic’ Trump ‘not to be trusted’ am | Carney calls Trump's fresh tariffs a 'miscalculation' after  | NO_RELATION | none | medium |
| [R014](#r014) | Iran war live: Tehran awaits official response as Trump reje | ‘Iran ready for doomsday war’, FM Araghchi says | reaction_to | B->A | medium |
| [R015](#r015) | Spain’s Sanchez says Russia, Israel spread disinformation on | Sexual assaults happening almost every day in Ceuta, prosecu | NO_RELATION | none | high |
| [R016](#r016) | Did Beijing and Washington agree on a crisis prevention deal | Why did Trump and Xi seal a deal on World War II soldiers’ m | NO_RELATION | none | medium |
| [R017](#r017) | People return to their flood-ravaged homes in Nepal | Rescue work intensifies as death toll in China-Nepal disaste | same_calamity_lifecycle | none | medium |
| [R018](#r018) | Weddings in Gaza offer rare moments of joy amid genocide | UK, Canada and Australia condemn Israel for refusing crimina | NO_RELATION | none | high |
| [R019](#r019) | ‘Iran ready for doomsday war’, FM Araghchi says | Trump expects new Iran talks despite rejecting deal offer | NO_RELATION | none | medium |
| [R020](#r020) | Iran denies link to attack on airbase as UK minister warns o | UK to gather defense CEOs for ‘closed-door’ Russian security | NO_RELATION | none | high |
| [R021](#r021) | OpenAI-backed legal tech firm pivots to Chinese Kimi K3 open | China and US push Southeast Asia over their AI blocs. Will i | NO_RELATION | none | high |
| [R022](#r022) | Report: CIA warned Europe of Russian drone attack from vesse | France to protect key Saudi oil terminal as Houthis step up  | NO_RELATION | none | high |
| [R023](#r023) | Trump says he doesn't want to work with China on AI safety | Trump backs AI self-regulation at tech summit but is it enou | same_visit_or_summit | none | medium |
| [R024](#r024) | Netanyahu defends Israeli military action as delegates walk  | Jewish protestors join Free Palestine march to denounce Neta | AMBIGUOUS | none | low |
| [R025](#r025) | Xi-Trump summit drew Chinese CEOs. So why couldn’t they get  | China backs Cuba, Beijing’s Panama threat, new UN chief: 7 L | NO_RELATION | none | high |
| [R026](#r026) | Trump autopen joke at Biden’s expense draws rare laugh from  | Xi got Trump's red carpet welcome - but not everything he wa | NO_RELATION | none | medium |
| [R027](#r027) | Nominations Sent to the Senate | Eliminating Disease-Carrying Pests And Restoring Enjoyment O | NO_RELATION | none | high |
| [R028](#r028) | Trump autopen joke at Biden’s expense draws rare laugh from  | AI war, Taiwan and translation: SCMP answers your questions  | NO_RELATION | none | medium |
| [R029](#r029) | Israel re-establishes closed West Bank settlement, defying g | Jewish activists push back against Israeli settlers | NO_RELATION | none | high |
| [R030](#r030) | Malaysia’s air quality turns hazardous as Indonesian wildfir | Orangutans in danger as wildfires blaze through Borneo | same_calamity_lifecycle | none | low |
| [R031](#r031) | One month after Nepal’s catastrophic floods, thousands remai | 14 killed, a dozen missing as Nepal is hit by more floods an | NO_RELATION | none | high |
| [R032](#r032) | Meghan in talks for role in Netflix series The Gentlemen, BB | As they return to the UK, Harry and Meghan search for a bran | NO_RELATION | none | high |
| [R033](#r033) | Estonia says Russia ordered August arson attack on defence c | Taiwan takes a page from Ukraine’s playbook in steeling soci | NO_RELATION | none | high |
| [R034](#r034) | Trump claims he discussed release of political prisoners in  | Xi leaves Washington, but keeps at least two places on the W | NO_RELATION | none | medium |
| [R035](#r035) | MFF 2028-2034: Council agrees negotiating position on future | Commission report finds devastating shifts in the Arctic and | NO_RELATION | none | high |
| [R036](#r036) | Netanyahu defends Israeli military action as delegates walk  | Contrasting treatment of Israel and Palestine on display at  | NO_RELATION | none | medium |
| [R037](#r037) | 14 killed, a dozen missing as Nepal is hit by more floods an | ‘Still a lockdown’: Deadly floods hit Nepal tourism as peak  | NO_RELATION | none | medium |
| [R038](#r038) | Xi-Trump summit drew Chinese CEOs. So why couldn’t they get  | Can Europe still compete with the US and China? | NO_RELATION | none | high |
| [R039](#r039) | Strait of Hormuz tensions linger as Iran and US move further | ‘Atrocious’ crime: Cuban official decries possibility of US  | NO_RELATION | none | high |
| [R040](#r040) | Israeli soldiers throw belongings from besieged Palestinian  | Israeli settlers set fire to heavy machinery at West Bank qu | NO_RELATION | none | high |
| [R041](#r041) | China has cracked down on AI relationships. Is it ahead of t | Chinese women spend top dollar on male model shoots, turning | NO_RELATION | none | high |
| [R042](#r042) | What are the implications of the US-Venezuela oil deal? | The looming failure of Operation Economic Outcast | NO_RELATION | none | high |
| [R043](#r043) | US forces exiting Iraq after 2 decades, leaving opening for  | Iran war live: Trump claims war will end ‘very soon’, gives  | NO_RELATION | none | high |
| [R044](#r044) | Can Europe still compete with the US and China? | China backs Cuba, Beijing’s Panama threat, new UN chief: 7 L | NO_RELATION | none | high |
| [R045](#r045) | Rescue work intensifies as death toll in China-Nepal disaste | Nepal tunnel traps hinder flood rescue: How many are dead or | NO_RELATION | none | medium |
| [R046](#r046) | Pope meets victims of sex abuse, urges ‘wise leaders’ as Fre | 'Scourge' of abuse must be rooted out, says Pope during Lour | same_visit_or_summit | none | high |
| [R047](#r047) | Trump calls Kim Jong Un a ‘friend’ and plays down N Korea’s  | ‘America is back’, AI ‘conspiracy’, China’s Laos deal: 7 glo | NO_RELATION | none | high |
| [R048](#r048) | UK Labour Party meets buoyed by Burnham but seeking concrete | UK’s Healey puts defense in focus for reindustrialization pu | same_visit_or_summit | none | high |
| [R049](#r049) | Yemen’s health system could collapse in some areas, minister | Inside Yemen's front-line city as Houthis battle for control | NO_RELATION | none | high |
| [R050](#r050) | House intel committee could investigate defense firm contrib | Democrats hope anger at Trump enough to get young people to  | NO_RELATION | none | high |
| [R051](#r051) | Xiaomi-backed robotics chip designer clears hearing, eyes US | Hong Kong customs arrests 2, seizes HK$290,000 of ‘slimming  | NO_RELATION | none | high |
| [R052](#r052) | Ukraine's prized steel industry left in ruins by Russian mis | Russian attacks on Ukraine’s Kyiv region kill four, target p | NO_RELATION | none | high |
| [R053](#r053) | China warns of ‘major risk’ of glacier collapse as Tibet-Nep | Nepal tunnel traps hinder flood rescue: How many are dead or | same_calamity_lifecycle | none | high |
| [R054](#r054) | People return to their flood-ravaged homes in Nepal | 'I haven't lost my hope' - the search for missing loved ones | same_calamity_lifecycle | none | medium |
| [R055](#r055) | Why Southeast Asia feels relief and caution after the Xi-Tru | ‘Right now, it’s fine’: Trump brushes off questions about su | NO_RELATION | none | medium |
| [R056](#r056) | Iran war live: US vows toughest Iran sanctions, urges China  | US designates Hezbollah an Iranian proxy, sanctions funding  | NO_RELATION | none | low |
| [R057](#r057) | Child among three killed off French coast in Channel crossin | French police fire tear gas at migrants on beach | NO_RELATION | none | medium |
| [R058](#r058) | Why has Trump rejected Iran’s peace proposal? | UK investigates if arrests near US-run base prevented Iran-l | NO_RELATION | none | high |
| [R059](#r059) | Why has Trump rejected Iran’s peace proposal? | Oil prices surge after Trump rejects Iran’s plan to reopen S | NO_RELATION | none | medium |
| [R060](#r060) | Jewish activists push back against Israeli settlers | Settlers target Palestinian homes in Occupied West Bank’s Ar | NO_RELATION | none | high |
| [R061](#r061) | EU weighs sweeping new trade powers against China before mak | Daily News 30 / 09 / 2026 | NO_RELATION | none | high |
| [R062](#r062) | Pitch perfect cultural diplomacy wins heart of China’s first | Nepal’s leader labels devastating flood a ‘warning to the wo | NO_RELATION | none | high |
| [R063](#r063) | Xi-Trump rapport is ‘most valuable strategic asset’ in US-Ch | Days after Xi-Trump summit, the US marks China’s National Da | NO_RELATION | none | high |
| [R064](#r064) | La anciana Maricarmen podrá volver a su casa tras el desaloj | Attention turns to economy on final day of Macron’s visit to | same_visit_or_summit | none | medium |
| [R065](#r065) | EU nails down five defense priority areas to channel common  | Beijing and Berlin ‘exchanged opinions’ amid reported plan t | NO_RELATION | none | high |
| [R066](#r066) | Council strengthens EU space threat response architecture | Daily News 30 / 09 / 2026 | AMBIGUOUS | none | low |
| [R067](#r067) | Russia tests missiles near Japanese-claimed islands after Pu | Rescuers dig through Ukraine mall wreckage as Zelensky conde | NO_RELATION | none | high |
| [R068](#r068) | Ebola outbreak ‘growing faster, ⁠⁠wider’ as DRC death toll p | More than 16,000 doses of Ervebo vaccine arrive in Ebola-hit | same_calamity_lifecycle | none | high |
| [R069](#r069) | Russia strike sets National Academy of Sciences of Ukraine a | Russia pounds Ukraine’s Kyiv after deadly strike on Academy  | same_attack_wave | none | medium |
| [R070](#r070) | Asean urged to take on Big Tech after Meta’s record payout | Amazon rigged $20bn worth of ad prices, US lawsuit alleges | NO_RELATION | none | high |
| [R071](#r071) | UAE intercepts drone after US and Iran exchange attacks | Why has Greece signed a $3.5bn missile deal with Israel? | NO_RELATION | none | high |
| [R072](#r072) | China warns of ‘major risk’ of glacier collapse as Tibet-Nep | Rescue work intensifies as death toll in China-Nepal disaste | same_calamity_lifecycle | none | high |
| [R073](#r073) | Trekkers helicoptered off mountains as more deadly landslide | Missing Malaysian found safe in flood-ravaged Nepal after 37 | NO_RELATION | none | medium |
| [R074](#r074) | Sudanese army impounds dozens of motorcycles in Blue Nile cu | Ethiopia accuses Sudan, Egypt of backing Tigray rebels as fi | NO_RELATION | none | high |
| [R075](#r075) | Nepal floods: could foreign rescue teams have been brought i | Nepal tunnel traps hinder flood rescue: How many are dead or | same_calamity_lifecycle | none | medium |
| [R076](#r076) | Israeli soldiers throw belongings from besieged Palestinian  | Jewish activists push back against Israeli settlers | NO_RELATION | none | high |
| [R077](#r077) | War and heat: Why are wheat prices soaring? | Russian attack hits rail workers in new deadly strikes on Ky | NO_RELATION | none | high |
| [R078](#r078) | 7 teens swept up in police crackdown on bicycle-related offe | Hong Kong police hunt for man who stole HK$10,000 from claw  | NO_RELATION | none | high |
| [R079](#r079) | Iran touts Hormuz attacks as oil flows increase despite tens | US-Iran talks continue, but ‘deal unlikely’ before midterm e | NO_RELATION | none | medium |
| [R080](#r080) | Israeli forces kill Hamas commander Izz al-Din al-Beik in Ga | Israeli settlers attack Jalud village in occupied West Bank, | NO_RELATION | none | high |
| [R081](#r081) | China-Nepal floods, Japan to deploy fighter jets to India: 5 | Why Japan’s hypersonic and underwater weapon plans might wor | NO_RELATION | none | high |
| [R082](#r082) | Ebola vaccine trial to start in DR Congo as warning issued o | More than 16,000 doses of Ervebo vaccine arrive in Ebola-hit | same_calamity_lifecycle | none | high |
| [R083](#r083) | Xi is in Bishkek for SCO summit. How does bloc fit China’s E | Russia, China leaders to meet at Shanghai Cooperation Organi | same_visit_or_summit | none | medium |
| [R084](#r084) | China-Nepal floods, Japan to deploy fighter jets to India: 5 | China warns of ‘major risk’ of glacier collapse as Tibet-Nep | NO_RELATION | none | high |
| [R085](#r085) | Xi got Trump's red carpet welcome - but not everything he wa | From wine to ping-pong, Trump and Xi’s state dinner is heavy | NO_RELATION | none | medium |
| [R086](#r086) | Trump made the right decision to reject Iran’s offer | Judge blocks Trump from tying anti-terrorism grants to elect | NO_RELATION | none | high |
| [R087](#r087) | ‘Right now, it’s fine’: Trump brushes off questions about su | US, China list goods recommended for tariff cuts following T | NO_RELATION | none | medium |
| [R088](#r088) | More than 100 arrested as New Yorkers protest Netanyahu’s UN | Contrasting treatment of Israel and Palestine on display at  | NO_RELATION | none | medium |
| [R089](#r089) | Streamlining Access to Government Services Through America.g | First Lady Melania Trump Announces 2026 Fall Garden Tours | NO_RELATION | none | high |
| [R090](#r090) | Terror suspects wanted to do ‘big damage’ to air base used b | Why has Trump rejected Iran’s peace proposal? | NO_RELATION | none | high |
| [R091](#r091) | Ebola outbreak ‘growing faster, ⁠⁠wider’ as DRC death toll p | Ebola vaccine trial to start in DR Congo as warning issued o | same_calamity_lifecycle | none | medium |
| [R092](#r092) | Xi-Trump summit drew Chinese CEOs. So why couldn’t they get  | US delivers F-16V fighter jets to Taiwan as island eyes thre | NO_RELATION | none | high |
| [R093](#r093) | Don’t leave Hong Kong parents to their own devices on child  | Singapore may require social media firms to set daily time l | NO_RELATION | none | high |
| [R094](#r094) | American and six Ukrainians released by India after six mont | US revokes visas from Latin American officials and families  | NO_RELATION | none | high |
| [R095](#r095) | Trump eases tariffs on ground beef imports for 90 days | Carney calls Trump's fresh tariffs a 'miscalculation' after  | NO_RELATION | none | high |
| [R096](#r096) | Thai police arrest jet skier after joyride through flooded B | At least 21 Hong Kong-Bangkok flights delayed amid flooding  | NO_RELATION | none | low |
| [R097](#r097) | In the US-China AI race, the real fight is keeping humans in | ‘Missed opportunity’: US soybean farmers question exclusion  | NO_RELATION | none | high |
| [R098](#r098) | DPR Korea tells UN its nuclear status is ‘irreversible’, rej | International Security Rapidly Deteriorates; General Assembl | AMBIGUOUS | none | low |
| [R099](#r099) | ‘Money is money’: US, UK firms still coming to Hong Kong, co | Hong Kong IPOs falter, China aids homebuyers, EU trade talks | NO_RELATION | none | high |
| [R100](#r100) | UAE confirms Netanyahu visit to Abu Dhabi | Israel security agency files complaint over TV report that N | same_visit_or_summit | none | medium |
| [R101](#r101) | Boeing wins Navy next-gen fighter F/A-XX competition | Why the Pentagon just dropped $450M on tungsten mining | NO_RELATION | none | high |
| [R102](#r102) | War on Iran: The US could focus on economically isolating Ir | Iran says new US sanctions violate sovereignty of other stat | NO_RELATION | none | medium |
| [R103](#r103) | FIFA could disburse millions to members as Infantino seeks r | In FIFA-UEFA tussle, European body accused of ‘misinformatio | NO_RELATION | none | medium |
| [R104](#r104) | Hong Kong police hunt for man who stole HK$10,000 from claw  | Police arrest man, 34, over hidden cameras found in Hong Kon | NO_RELATION | none | high |
| [R105](#r105) | Contrasting treatment of Israel and Palestine on display at  | Converging crises, chaos and walkouts dominate UNGA Day Thre | NO_RELATION | none | medium |
| [R106](#r106) | South African police probe mining feud shooting, 27 dead as  | 3 people killed and 4 injured in shooting at Michigan strip  | NO_RELATION | none | high |
| [R107](#r107) | Israeli settlers set fire to heavy machinery at West Bank qu | How Israel is expanding settlements in drive to reshape West | NO_RELATION | none | high |
| [R108](#r108) | DR Congo Ebola emergency: Calls grow for urgent humanitarian | DRC: Early access to care and oxygen decisive for Ebola pati | same_calamity_lifecycle | none | medium |
| [R109](#r109) | Who are the economic winners and losers of the US-Israel war | Can Iran use rockets to mine the Strait of Hormuz, as US cla | NO_RELATION | none | high |
| [R110](#r110) | Kuala Lumpur is world’s most polluted city due to haze, Sing | Missing Malaysian found safe in flood-ravaged Nepal after 37 | NO_RELATION | none | high |
| [R111](#r111) | Jerusalem Daily: Israeli opposition leaders unite to drive o | Stuck between Israeli military checkpoints | NO_RELATION | none | high |
| [R112](#r112) | Drone-hunting on the border, plus turmoil at an Air Force th | Restaurant named after Xi Jinping attacked by Chinese nation | NO_RELATION | none | high |
| [R113](#r113) | Iran denies link to attack on airbase as UK minister warns o | Iran court upholds lashes sentence for singer who performed  | NO_RELATION | none | high |
| [R114](#r114) | DR Congo Ebola emergency: Calls grow for urgent humanitarian | Security Council, 10232nd Meeting (AM) Democratic Republic o | NO_RELATION | none | medium |
| [R115](#r115) | Iran war live: Tehran awaits official response as Trump reje | Strait of Hormuz tensions linger as Iran and US move further | NO_RELATION | none | medium |
| [R116](#r116) | Indonesia-US joint military drills with allies kick off with | Prediction markets have priced the Trump-Xi summit. Do the b | NO_RELATION | none | high |
| [R117](#r117) | Legal aid chief denies stricter vetting as aid for policy ch | ‘Balanced and acceptable’: labour chief defends helper wage  | NO_RELATION | none | high |
| [R118](#r118) | Strait of Hormuz tensions linger as Iran and US move further | Mike Waltz: US offered to sell Iran uranium for civilian pro | NO_RELATION | none | medium |
| [R119](#r119) | Manchester City’s Maresca admits he needs time as Bournemout | Manchester City preview: Five key questions heading into 202 | NO_RELATION | none | high |
| [R120](#r120) | Indonesian quake survivors recall trauma of all-day intense  | Indonesia bolsters troop numbers to combat Borneo wildfires | NO_RELATION | none | high |
| [R121](#r121) | Japanese firms pull back from China amid geopolitical tensio | ‘180-degree flip’ sees global investors turn to China for di | NO_RELATION | none | high |
| [R122](#r122) | From wine to ping-pong, Trump and Xi’s state dinner is heavy | AI war, Taiwan and translation: SCMP answers your questions  | NO_RELATION | none | high |
| [R123](#r123) | Russia raises 2027 military spending by 27%, budget document | Putin signs decree adding 15,500 troops to Russian army | NO_RELATION | none | medium |
| [R124](#r124) | Pope Leo says concerns about AI doom scenarios are not ‘fake | Fighter jets escort Pope Leo on final day of his France tour | AMBIGUOUS | none | low |
| [R125](#r125) | Arming an adversary: Why Trump’s offer to sell China weapons | Iran war live: Trump says he did not offer Tehran sanctions  | NO_RELATION | none | high |
| [R126](#r126) | At your service: Hong Kong welcomes first humanoid robot-run | Don’t leave Hong Kong parents to their own devices on child  | NO_RELATION | none | high |
| [R127](#r127) | Russian strikes kill 6 people in Ukraine, day after shopping | Rescuers dig through Ukraine mall wreckage as Zelensky conde | NO_RELATION | none | medium |
| [R128](#r128) | US Navy launches drone command that could reshape Taiwan war | Trump claims he discussed release of political prisoners in  | NO_RELATION | none | high |
| [R129](#r129) | Thai police arrest jet skier after joyride through flooded B | One Bangkok flood battle after another as Thai Airways races | NO_RELATION | none | low |
| [R130](#r130) | As Harry plans UK return, can he patch up royal rift with Pr | Prince Harry and others ordered to pay initial US$13 million | NO_RELATION | none | high |
| [R131](#r131) | China warns Japan over WWII history as business delegation v | Japanese firms pull back from China amid geopolitical tensio | NO_RELATION | none | high |
| [R132](#r132) | Iranian minister says only negotiation can end conflict afte | Trump expects new Iran talks despite rejecting deal offer | NO_RELATION | none | medium |
| [R133](#r133) | Trump autopen joke at Biden’s expense draws rare laugh from  | From wine to ping-pong, Trump and Xi’s state dinner is heavy | same_visit_or_summit | none | high |
| [R134](#r134) | Hong Kong retail sales rise 4.5% in July, marking 15th strai | Hot property: Big banks, fashion stores seek ‘cheaper’, eye- | NO_RELATION | none | high |
| [R135](#r135) | Trump asked Xi if Beijing wanted US weapons: a joke, a gambi | Trump-Xi summit: What wasn't said might matter the most | NO_RELATION | none | high |
| [R136](#r136) | Ethiopians celebrate Meskel and call for peace amid fighting | Al Jazeera reports from near front line in Ethiopia’s Afar r | NO_RELATION | none | medium |
| [R137](#r137) | Pentagon awards Raytheon up to $20.7 billion to nearly doubl | US Navy awards RTX’s Raytheon $24.4B for SM-6 missiles amid  | NO_RELATION | none | high |
| [R138](#r138) | Trump lanza una página oficial de información sobre el Gobie | Trump says he doesn't want to work with China on AI safety | NO_RELATION | none | medium |
| [R139](#r139) | Mined, Melted, and Poured in America: President Trump Revers | Gli Usa prestano alle aziende energetiche 40 milioni di bari | NO_RELATION | none | high |
| [R140](#r140) | US-China conflict doesn’t have to become a self-fulfilling p | ‘No retreat’: Key Trump ally urges continued US-China engage | NO_RELATION | none | high |
| [R141](#r141) | Canadian premier says ‘erratic’ Trump ‘not to be trusted’ am | Carney faces crucial test after walking away from Trump's de | NO_RELATION | none | medium |
| [R142](#r142) | UN commemoration of Durban Declaration: What’s on agenda, wh | UNGA 81: Five key takeaways from general debate | NO_RELATION | none | medium |

---

## R001

**Development A** `2026-08-21:opatra-more-consumers-allege`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-21T00:30 to 2026-08-21T00:30 UTC
- **Actors:** Opatra
- **Places:** Hong Kong, UK
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T00:30 [South China Morning Post] **More Hong Kong consumers allege coercive beauty sales in wake of Opatra crackdown**
    > More consumers in Hong Kong have come forward to allege aggressive sales tactics across the beauty sector, including credit card abuse, unwanted physical contact and pressure to buy costly products, on the back of a crackdown on the local operations of a UK-based brand.
Legal exp

**Development B** `2026-08-21:ex-diplomats-urge-sanctions-on-israel`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-22T15:30 to 2026-08-22T15:30 UTC
- **Actors:** European Union
- **Places:** France, Israel, Palestine, UK
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T15:30 [Al Jazeera] **Over 100 ex-diplomats urge France, UK to sanction Israel over Palestine**
    > An open letter demands a ban on arms transfers and a freeze on EU-Israel and UK-Israel trade agreements.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Hong Kong beauty-sales allegations and ex-diplomats' letter on Israel share no actor, place or matter.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R002

**Development A** `2026-08-31:clancy-jury-deadlocked`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-01T20:05 to 2026-09-01T20:05 UTC
- **Actors:** Lindsay Clancy
- **Places:** Massachusetts
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-01T20:05 [BBC World] **Jurors in Lindsay Clancy trial deadlocked but judge asks them to keep trying**
    > The Massachusetts mother is facing murder charges for killing her three children at their family home in 2023.

**Development B** `2026-08-31:clancy-jury-options-explainer`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-01T23:17 to 2026-09-01T23:17 UTC
- **Actors:** Lindsay Clancy
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-01T23:17 [BBC World] **Not just guilty or not - The jury's options in Lindsay Clancy's murder trial**
    > Jurors have five options before them as they decide the fate of the former nurse charged with murdering her three children.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | commentary |

**Rationale:** B is an explainer of the jury's options in the Clancy trial, analysis rather than a new occurrence relating to A's deadlock.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R003

**Development A** `2026-08-31:sco-summit-preview`

- **Members:** 3 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-31T04:18 to 2026-08-31T08:47 UTC
- **Actors:** Modi, SCO, Shanghai Cooperation Organisation, Trump, Vladimir Putin, Xi Jinping
- **Places:** China, Russia
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T04:18 [Al Jazeera] **Russia, China leaders to meet at Shanghai Cooperation Organisation summit**
    > The organisation is not officially anti-West, but Russian and Chinese leaders have used it to amplify their worldview.
  - 2026-08-31T08:47 [Al Jazeera] **Xi, Modi and Putin attend SCO summit: What’s on the agenda?**
    > The two-day summit aims to promote a vision of a multipolar world and mutual trade ties amid Trump&#039;s unilateralism.
  - 2026-08-31T08:47 [Al Jazeera] **Xi, Modi and Putin set to meet for SCO summit: What’s on the agenda?**
    > The two-day summit aims to promote a vision of a multipolar world and mutual trade ties amid Trump&#039;s unilateralism.

**Development B** `2026-08-31:trump-xi-summit-prediction-markets`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T14:00 to 2026-08-31T14:00 UTC
- **Actors:** Donald Trump, Trump, White House, Xi Jinping
- **Places:** Beijing, China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T14:00 [South China Morning Post] **Prediction markets have priced the Trump-Xi summit. Do the bets have any value?**
    > US President Donald Trump has already announced the date: September 24.
That is when, Trump says, Chinese President Xi Jinping will come to the White House for a visit following the “America first” leader’s own three-day trip to Beijing in May.
But there is a diplomatic wrinkle.


| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** A is the SCO summit in Bishkek; B is commentary on prediction markets for the separate Trump-Xi White House summit.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R004

**Development A** `2026-08-31:nepal-foreign-rescue-teams-question`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T02:45 to 2026-08-31T02:45 UTC
- **Actors:** Nepalese
- **Places:** China, Kathmandu, Nepal
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T02:45 [South China Morning Post] **Nepal floods: could foreign rescue teams have been brought in earlier?**
    > The Nepalese government has appealed for rescue aid from other countries just two days after it reportedly refused help, as several hundred people are still believed to be trapped in hydropower tunnels and thousands remain missing following the catastrophic flash flooding at the 

**Development B** `2026-08-31:nepal-rescue-tunnel-workers-toll-900`

- **Members:** 4 item(s)
- **Sources:** Al Jazeera, BBC World, South China Morning Post
- **Times:** 2026-08-31T06:05 to 2026-09-01T16:11 UTC
- **Actors:** BBC Major, CCTV, Himalayan, Nepal
- **Places:** China, Gyirong Port, India, Nepal
- **System Development:** D1
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T06:05 [South China Morning Post] **Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000**
    > Rescuers from China and Nepal continued searching landslide- and flood-affected areas on Monday while efforts to reopen roads to the heart of the disaster-hit area at Gyirong Port entered a “critical stage”.
The death toll in Nepal had risen to 903 as of 9am on Monday, with 4,247
  - 2026-08-31T07:34 [Al Jazeera] **Nepal races to rescue trapped workers, as flood death toll surpasses 900**
    > Nepal officials say rescuers focusing on reaching workers in hydropower project tunnels in flood-stricken region.
  - 2026-09-01T06:02 [BBC World] **The final minutes before floodwater crashed through Nepal-China border**
    > More than 100 Indians are missing at a vital Nepal-China trade crossing after devastating Himalayan floods.
  - 2026-09-01T16:11 [BBC World] **River water smashed into tunnel and chased me for 20 minutes, Nepal worker tells BBC**
    > Major efforts to rescue hydropower workers continue as Nepal's death toll exceeds 1,000.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_calamity_lifecycle` | none | medium | none |

**Rationale:** A reports Nepal's appeal for foreign rescue aid and B the rescue effort and death toll for the same Nepal-China border flash flood with workers trapped in hydropower tunnels.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R005

**Development A** `2026-09-25:us-china-summit-outcome`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-25T03:57 to 2026-09-25T03:57 UTC
- **Actors:** Donald Trump, Trump, Xi Jinping
- **Places:** China, Taiwan
- **System Development:** D3
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T03:57 [BBC World] **Xi got Trump's red carpet welcome - but not everything he wanted**
    > China wanted progress on trade, technology and Taiwan - but hasn't got as much as it would have hoped for.

**Development B** `2026-09-25:scmp-summit-reader-qa`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-25T05:55 to 2026-09-25T05:55 UTC
- **Actors:** Asian, Donald Trump, SCMP, Xi Jinping
- **Places:** China, South, Taiwan, United States, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T05:55 [South China Morning Post] **AI war, Taiwan and translation: SCMP answers your questions from Xi-Trump summit**
    > This live article is freely available to our registered users. Please log in or create an account.
Xi’s US summit: Access real-time updates, geopolitical risk analysis, and exclusive reporting from an Asian perspective. Subscribe now with our limited-time offer to stay ahead.
Chi

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | commentary |

**Rationale:** Both are analysis pieces (BBC assessment of what Xi got, SCMP reader Q&A) about the same Xi state visit, not distinct occurrences.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R006

**Development A** `2026-09-29-live:slovenia-israel-u-turn`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T20:35 to 2026-09-28T20:35 UTC
- **Actors:** Benjamin Netanyahu, UN General Assembly
- **Places:** Israel Slovenia, Palestine, Slovenia
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T20:35 [Al Jazeera] **Slovenia’s U-turn towards Israel**
    > Slovenia’s policy towards Palestine has changed sharply following a UNGA sideline meeting with Israeli PM Netanyahu.

**Development B** `2026-09-29-live:inside-al-jazeera-unga-coverage`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T00:10 to 2026-09-29T00:10 UTC
- **Actors:** Al Jazeera, UN General Assembly
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T00:10 [Al Jazeera] **Inside Al Jazeera’s UNGA coverage**
    > Here’s a look at what it was like behind the scenes of the coverage you saw online and on TV.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** A is analysis of Slovenia's policy shift; B is a behind-the-scenes piece on Al Jazeera's UNGA coverage.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R007

**Development A** `2026-09-27-live:trump-downplays-taiwan-talk`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-27T09:43 to 2026-09-27T09:43 UTC
- **Actors:** Donald Trump, Trump, Xi Jinping
- **Places:** China, Taiwan, US, Washington
- **System Development:** D14
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T09:43 [South China Morning Post] **‘Right now, it’s fine’: Trump brushes off questions about summit talk on Taiwan**
    > US President Donald Trump has sought to play down exchanges with his Chinese counterpart Xi Jinping on Taiwan, saying on Saturday that they touched on the subject only briefly.
“We didn’t talk about it too much. Right now, it’s fine. It’s just moving along,” Trump said. “We didn’

**Development B** `2026-09-27-live:trump-asked-xi-weapons`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-28T04:06 to 2026-09-28T04:06 UTC
- **Actors:** David Perdue, Donald Trump, Fox News, Trump, US State Department, White House, Xi Jinping
- **Places:** Beijing, China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T04:06 [South China Morning Post] **Trump asked Xi if Beijing wanted US weapons: a joke, a gambit or something more?**
    > Donald Trump asked President Xi Jinping whether Beijing wanted to buy American weapons, the US ambassador to China said on Sunday, prompting the State Department to quickly rule out any such deal with Washington’s principal strategic competitor.
“He actually asked President Xi, w

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | none |

**Rationale:** Trump's remark on Taiwan talks and the ambassador's disclosure of the weapons question are separate post-summit statements; neither responds to the other.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R008

**Development A** `2026-08-21:hk-financiers-press-carried-interest`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-21T01:00 to 2026-08-21T01:00 UTC
- **Actors:** none extracted
- **Places:** Hong Kong, Singapore
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T01:00 [South China Morning Post] **Hong Kong financiers press for tax breaks after Singapore unveils rival scheme**
    > Hong Kong should press ahead with its proposed tax break on carried interest, the performance fees earned by hedge fund and private equity managers, after Singapore unveiled a rival tax-exemption scheme, according to industry participants.
The bill, submitted to lawmakers in June

**Development B** `2026-08-21:singapore-fund-manager-carrots-analysis`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-21T12:08 to 2026-08-21T12:08 UTC
- **Actors:** Ramkishen Rajan, Yong Pung
- **Places:** Hong Kong, Lee Kuan Yew School, Singapore
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T12:08 [South China Morning Post] **Singapore’s carrots for fund managers set to sharpen competition with Hong Kong**
    > Singapore’s latest package of tax breaks and visa incentives for fund managers could enhance its appeal as a leading asset management hub, as competition with Hong Kong intensifies for global capital and high-value financial talent, analysts have said.
While the measures would he

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | commentary |

**Rationale:** B is analysts' commentary on Singapore's fund-manager incentives; A reacts to Singapore's scheme, not to B.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R009

**Development A** `2026-08-21:harry-uk-return-royal-rift`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-21T06:53 to 2026-08-21T06:53 UTC
- **Actors:** Charles, Harry, Meghan, Prince Harry, Prince William, Princess Diana, William
- **Places:** Sussex, UK
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T06:53 [South China Morning Post] **As Harry plans UK return, can he patch up royal rift with Prince William?**
    > William and Harry were united in grief as children by the tragic death of their mother, Princess Diana, but their relationship as adults has been ripped apart by anger and hurt.
The pair – dubbed “the heir and the spare” from an early age – have failed to put aside their differen

**Development B** `2026-08-21:meghan-netflix-gentlemen-talks`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-08-21T18:29 to 2026-08-21T18:29 UTC
- **Actors:** BBC, Meghan, Netflix, Prince Harry
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T18:29 [BBC World] **Meghan in talks for role in Netflix series The Gentlemen, BBC understands**
    > This would be Meghan's first significant acting role since her marriage to Prince Harry.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** A is commentary on the Harry-William rift; B is Meghan's reported Netflix talks, with no stated link.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R010

**Development A** `2026-09-25:pakistan-afghanistan-cross-border-strikes`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera, BBC World
- **Times:** 2026-09-24T19:02 to 2026-09-25T04:22 UTC
- **Actors:** Pakistan, Taliban
- **Places:** Afghanistan, Pakistan
- **System Development:** D1
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-24T19:02 [BBC World] **Four civilians killed in Pakistani strikes in Afghanistan, Taliban says**
    > Pakistan says it struck 10 targets, adding the strikes were "strictly limited to identified military objectives".
  - 2026-09-25T04:22 [Al Jazeera] **Pakistani forces kill Afghan Taliban fighters in border escalation**
    > Pakistan&#039;s security forces report ongoing cross-border fire in latest fighting with Afghanistan.

**Development B** `2026-09-25:saudi-turkey-pakistan-defence-talks`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-25T03:35 to 2026-09-25T03:35 UTC
- **Actors:** Houthis
- **Places:** Pakistan, Saudi Arabia, Turkey, Turkiye, Yemen
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T03:35 [Al Jazeera] **Saudi, Turkish, Pakistani chiefs plan urgent talks amid Yemen fighting**
    > Saudi Arabia, Turkiye and Pakistan move to deepen defence coordination as Houthi attacks and Yemen fighting intensify.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Pakistani strikes in Afghanistan and Saudi-Turkish-Pakistani talks on Yemen are different matters sharing only Pakistan.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R011

**Development A** `2026-09-27-live:scmp-weekend-reads`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-28T04:30 to 2026-09-28T04:30 UTC
- **Actors:** Trump, Xi Jinping
- **Places:** Asia, Australia, China, Hong Kong, Thailand, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T04:30 [South China Morning Post] **Xi–Trump body language, Thailand’s tourist backlash: 5 weekend reads you missed**
    > We have put together stories from our coverage last weekend to help you stay informed about news across Asia and beyond. If you would like to see more of our reporting, please consider subscribing.
1. What Trump and Xi revealed in the body language with their wives

2. Australia 

**Development B** `2026-09-27-live:summit-trade-deliverables`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera, South China Morning Post
- **Times:** 2026-09-28T06:24 to 2026-09-28T09:16 UTC
- **Actors:** Trump, White House, Xi Jinping
- **Places:** Beijing, China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T06:24 [Al Jazeera] **US, China list goods recommended for tariff cuts following Trump-Xi summit**
    > Washington and Beijing announce details of agreement to reduce tariffs on $60bn of trade.
  - 2026-09-28T09:16 [South China Morning Post] **China resuming US coal imports among thin list of summit outcomes**
    > China agreed to import at least 10 million tonnes of US coal in each of the next two years, marking one of the few concrete results from President Xi Jinping’s state visit to the United States.
The country will also lower tariffs on 1,619 US products, including coal, under a deal

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** A is a weekend reading digest; B is the announced list of tariff cuts following the summit.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R012

**Development A** `2026-09-30-multilingual:sx-100`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-29T01:12 to 2026-09-29T01:12 UTC
- **Actors:** Trump
- **Places:** U.S.
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 01:12 [BBC World] **Are Trump's US government funded ads illegal?**
    > President Trump has faced criticism after fronting adverts which were paid for by the US government.

**Development B** `2026-09-30-multilingual:sx-170`

- **Members:** 1 item(s)
- **Sources:** France 24
- **Times:** 2026-09-29T20:56 to 2026-09-29T20:56 UTC
- **Actors:** Donald Trump, Emerald Maxwell, White House
- **Places:** France
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 20:56 [France 24] **Public service announcement or Donald Trump propaganda?**
    > The White House calls them public service announcements - like those used in past administrations. Almost everyone else doesn't agree, with three taxpayer-funded advertisements that glorify President Donald Trump drawing criticism from across the partisan divide. Legal experts sa

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | SAME_DEVELOPMENT_SUSPECTED, commentary |

**Rationale:** Both pieces analyse the criticism and legality of the same taxpayer-funded Trump ads, apparently the same matter in commentary form.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R013

**Development A** `2026-08-21:canadian-premier-attacks-trump`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-21T03:12 to 2026-08-21T03:12 UTC
- **Actors:** Canada, Carney, Donald Trump, Mark Carney, Trump, Wab Kinew
- **Places:** Canada, Manitoba, US, Washington
- **System Development:** D4
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T03:12 [South China Morning Post] **Canadian premier says ‘erratic’ Trump ‘not to be trusted’ amid US trade feud**
    > The premier of a Canadian province launched a blistering attack on US President Donald Trump on Thursday, calling him a “bad person” and “not to be trusted” and urging Canada to keep fighting rather than rush to make concessions in trade talks with Washington.
Manitoba Premier Wa

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
| `NO_RELATION` | none | medium | none |

**Rationale:** Manitoba premier's attack on Trump and Carney's retaliatory tariffs after talks collapsed share only the US-Canada trade feud; no explicit link.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R014

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
| `reaction_to` | B->A | medium | none |

**Rationale:** B's Araghchi warning is reported as coming after Washington rejected the seven-day Hormuz roadmap, which is A.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R015

**Development A** `2026-08-31:sanchez-blames-russia-israel-ceuta-disinfo`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera, South China Morning Post
- **Times:** 2026-08-31T09:56 to 2026-08-31T13:39 UTC
- **Actors:** European Union, Israel, Pedro Sanchez, Sanchez, Spain
- **Places:** Africa, Ceuta, Israel, Morocco, Russia, Spain
- **System Development:** D4
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T09:56 [Al Jazeera] **Spain’s Sanchez says Russia, Israel spread disinformation on Ceuta crisis**
    > Sanchez cited EU research which had found that Russia ⁠and ⁠Israel both spread disinformation during the crisis.
  - 2026-08-31T13:39 [South China Morning Post] **Spain PM blames Russia, Israel for Ceuta migrant crisis’ disinformation**
    > Spanish Prime Minister Pedro Sanchez said on Monday there were signs Russia and Israel had spread the disinformation over Spain’s migration policy that triggered last month’s rush of migrants into Ceuta, but no evidence of Moroccan involvement.
Over 72,000 migrants irregularly cr

**Development B** `2026-08-31:ceuta-sexual-assaults-prosecutors`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-01T15:33 to 2026-09-01T15:33 UTC
- **Actors:** none extracted
- **Places:** Ceuta, Morocco, Spain
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-01T15:33 [BBC World] **Sexual assaults happening almost every day in Ceuta, prosecutors say**
    > Most migrants have returned to neighbouring Morocco, but as many as 5,000 remain in the Spanish exclave.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Sanchez's disinformation accusation and prosecutors' report of sexual assaults in Ceuta share the Ceuta crisis but no relation.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R016

**Development A** `2026-10-03-live:s-1366`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-30T12:01 to 2026-09-30T12:01 UTC
- **Actors:** White House, Xi Jinping
- **Places:** Beijing, China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 12:01 [South China Morning Post] **Did Beijing and Washington agree on a crisis prevention deal, or not?**
    > Disagreement over how to prevent conflicts could account for differences in how Chinese and US accounts have characterised discussion on the topic during last week’s summit, analysts said.
Speaking at a White House arrival ceremony, Chinese President Xi Jinping said the two milit

**Development B** `2026-10-03-live:s-1407`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-30T15:00 to 2026-09-30T15:00 UTC
- **Actors:** Trump, Xi Jinping
- **Places:** Beijing, China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 15:00 [South China Morning Post] **Why did Trump and Xi seal a deal on World War II soldiers’ missing remains?**
    > A decades-long effort by Beijing and Washington to recover the remains of US servicemen missing in China since World War II has resurfaced in the wake of the summit between the nations’ leaders.
The commitment was included in an eight-point list of outcomes from Chinese President

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | commentary |

**Rationale:** Both are analysis pieces on separate aspects of the summit outcomes (crisis prevention, WWII remains).

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R017

**Development A** `2026-08-31:nuwakot-residents-return-home`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-31T04:19 to 2026-08-31T04:19 UTC
- **Actors:** none extracted
- **Places:** Nepal, Nuwakot
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T04:19 [Al Jazeera] **People return to their flood-ravaged homes in Nepal**
    > Survivors in Nepal’s Nuwakot district are digging through mud and debris for belongings left behind by flash floods.

**Development B** `2026-08-31:nepal-rescue-tunnel-workers-toll-900`

- **Members:** 4 item(s)
- **Sources:** Al Jazeera, BBC World, South China Morning Post
- **Times:** 2026-08-31T06:05 to 2026-09-01T16:11 UTC
- **Actors:** BBC Major, CCTV, Himalayan, Nepal
- **Places:** China, Gyirong Port, India, Nepal
- **System Development:** D1
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T06:05 [South China Morning Post] **Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000**
    > Rescuers from China and Nepal continued searching landslide- and flood-affected areas on Monday while efforts to reopen roads to the heart of the disaster-hit area at Gyirong Port entered a “critical stage”.
The death toll in Nepal had risen to 903 as of 9am on Monday, with 4,247
  - 2026-08-31T07:34 [Al Jazeera] **Nepal races to rescue trapped workers, as flood death toll surpasses 900**
    > Nepal officials say rescuers focusing on reaching workers in hydropower project tunnels in flood-stricken region.
  - 2026-09-01T06:02 [BBC World] **The final minutes before floodwater crashed through Nepal-China border**
    > More than 100 Indians are missing at a vital Nepal-China trade crossing after devastating Himalayan floods.
  - 2026-09-01T16:11 [BBC World] **River water smashed into tunnel and chased me for 20 minutes, Nepal worker tells BBC**
    > Major efforts to rescue hydropower workers continue as Nepal's death toll exceeds 1,000.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_calamity_lifecycle` | none | medium | none |

**Rationale:** A (survivors returning to flood-ravaged homes in Nuwakot) and B (rescue and death toll) are stages of the same late-August Nepal flash flood.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R018

**Development A** `2026-08-21:gaza-weddings`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-21T13:29 to 2026-08-21T13:29 UTC
- **Actors:** none extracted
- **Places:** Gaza, Israel, Palestine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T13:29 [Al Jazeera] **Weddings in Gaza offer rare moments of joy amid genocide**
    > In Gaza, weddings offer Palestinian families a brief escape from Israel’s genocidal war.

**Development B** `2026-08-21:uk-canada-australia-condemn-wck-probe-refusal`

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

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Gaza wedding feature and condemnation over the WCK probe share only the Gaza war.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R019

**Development A** `2026-09-27-live:araghchi-doomsday-war`

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
| `NO_RELATION` | none | medium | none |

**Rationale:** Araghchi's war warning and Trump's expectation of new talks are separate statements; B does not respond to A.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R020

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

**Development B** `2026-09-29-live:uk-defence-ceos-russia-briefing`

- **Members:** 1 item(s)
- **Sources:** Breaking Defense
- **Times:** 2026-09-28T16:22 to 2026-09-28T16:22 UTC
- **Actors:** none extracted
- **Places:** Russia, UK, Ukraine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T16:22 [Breaking Defense] **UK to gather defense CEOs for ‘closed-door’ Russian security briefing**
    > The government warned the Russian &#8220;state and its proxies knowingly seek to disrupt businesses and organisations that underpin the British way of life or are vital to the defence of Ukraine.&#8221;

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Iran's denial over the airbase attack and the UK briefing on Russian threats concern different actors and matters.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R021

**Development A** `2026-08-21:legal-tech-kimi-k3-pivot`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-21T14:00 to 2026-08-21T14:00 UTC
- **Actors:** Andreessen Horowitz, Harvey, Harvey Tenet, Kimi, Kimi K3, Moonshot AI, Sequoia Capital
- **Places:** China, San Francisco, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T14:00 [South China Morning Post] **OpenAI-backed legal tech firm pivots to Chinese Kimi K3 open-weight model**
    > A US artificial intelligence start-up backed by OpenAI has built its first in-house model on Chinese lab Moonshot AI’s Kimi K3, highlighting a growing shift by Western tech firms towards Chinese open-weight systems amid soaring development costs.
San Francisco-based legal tech pr

**Development B** `2026-08-21:us-china-ai-blocs-southeast-asia`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-21T15:00 to 2026-08-21T15:00 UTC
- **Actors:** AI, Pax Silica, South China Morning Post, Southeast Asian, World Artificial Intelligence Cooperation Organisation (Waico
- **Places:** Beijing, China, Southeast Asia, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T15:00 [South China Morning Post] **China and US push Southeast Asia over their AI blocs. Will it test region’s non-alignment?**
    > Southeast Asian leaders have long insisted they will not be forced to pick sides in the great-power rivalry between the US and China. But their posture is about to be further tested.
This time, the battleground is AI. While Washington wants the region locked into Pax Silica – its

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Harvey's pivot to Kimi K3 and US-China AI bloc competition in Southeast Asia share only the topic.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R022

**Development A** `2026-09-25:cia-warning-drones-from-vessels`

- **Members:** 1 item(s)
- **Sources:** Defense News
- **Times:** 2026-09-24T11:19 to 2026-09-24T11:19 UTC
- **Actors:** CIA, El Mundo, European, Gerbera
- **Places:** Europe, France, Italy, Lithuania, Mediterranean, Mediterranean VIENNA, Russia, Spain
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-24T11:19 [Defense News] **Report: CIA warned Europe of Russian drone attack from vessels in the Mediterranean**
    > VIENNA — The CIA has warned European countries of a suspected Russian plot to launch Gerbera-type drones from aboard commercial vessels in the Mediterranean, a new report says.Major Spanish daily El Mundo published the article, which was based on testimony from an anonymous Lithu

**Development B** `2026-09-25:france-troops-saudi-terminal`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-25T06:03 to 2026-09-25T06:03 UTC
- **Actors:** Emmanuel Macron, Houthis, Macron
- **Places:** France, Iran, Red Sea, Saudi Arabia, TF1, Yanbu
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T06:03 [South China Morning Post] **France to protect key Saudi oil terminal as Houthis step up missile attacks**
    > President Emmanuel Macron said France would send troops to defend an oil plant in Saudi Arabia as the Iran-backed Houthi militia took responsibility for new attacks on the kingdom.
Macron said in a television interview Thursday with TF1 and France 2 that he would send soldiers an

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** CIA warning of Russian drone plot and France protecting a Saudi terminal from Houthis are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R023

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

**Development B** `2026-09-30-multilingual:sx-209`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-30T03:00 to 2026-09-30T03:00 UTC
- **Actors:** AI, Donald Trump, Trump
- **Places:** U.S.
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 03:00 [Al Jazeera] **Trump backs AI self-regulation at tech summit but is it enough?**
    > US President Donald Trump and leading tech companies have signed a voluntary agreement to regulate AI development.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_visit_or_summit` | none | medium | none |

**Rationale:** A (Trump's AI remarks at the White House luncheon with tech bosses) and B (voluntary AI agreement signed at the tech summit) belong to the same White House AI meeting.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R024

**Development A** `2026-09-25:netanyahu-unga-speech-walkout`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-25T00:44 to 2026-09-25T00:44 UTC
- **Actors:** Benjamin Netanyahu, UN General Assembly, United Nations
- **Places:** Israel
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T00:44 [BBC World] **Netanyahu defends Israeli military action as delegates walk out before UN speech**
    > The Israeli leader labels those who left his speech at the UN General Assembly as "moral cowards".Â

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
| `AMBIGUOUS` | none | low | none |

**Rationale:** The march denouncing Netanyahu may be a protest at his UNGA appearance, but the text does not state its venue or link to the speech; that would settle same_visit_or_summit.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R025

**Development A** `2026-10-03-live:s-1235`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-29T22:00 to 2026-09-29T22:00 UTC
- **Actors:** Peng Liyuan, White House, Xi Jinping
- **Places:** Beijing, China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 22:00 [South China Morning Post] **Xi-Trump summit drew Chinese CEOs. So why couldn’t they get a seat at the table?**
    > As American billionaires gathered at the White House to honour Chinese President Xi Jinping and his wife Peng Liyuan last Thursday, a group of Chinese business leaders spent the evening on the sidelines.
They had travelled to the US capital to join the state dinner. But their inv

**Development B** `2026-10-03-live:D16`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera, South China Morning Post
- **Times:** 2026-10-01T14:00 to 2026-10-02T20:52 UTC
- **Actors:** Beijing, China, Guo Jiakun, Latin American, Panama, United Nations
- **Places:** Beijing, China, Cuba, Havana, Latin America, Panama, US, Washington
- **System Development:** D16
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 14:00 [South China Morning Post] **China backs Cuba, Beijing’s Panama threat, new UN chief: 7 Latin America relations reads**
    > We have selected seven of the most interesting and important news stories covering Latin American relations from the past few weeks. If you would like to see more of our reporting, please consider subscribing.
1. China pledges to ‘firmly support’ Cuba as US escalates pressure on 
  - 2026-10-02 20:52 [Al Jazeera] **Latin America sees China as more positive global influence than US: Poll**
    > Annual Latinobarometro survey finds views of China’s influence improving as perceptions of US influence worsen.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** A analyses Chinese CEOs at the state dinner; B is a Latin America reading digest and poll.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R026

**Development A** `2026-09-25:white-house-tour`

- **Members:** 2 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-25T03:13 to 2026-09-25T08:05 UTC
- **Actors:** Biden, Donald Trump, Joe Biden, Trump, White House, Xi Jinping
- **Places:** Beijing, China, Great Hall of the People, Oval Office, South Lawn, United States
- **System Development:** D3
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T03:13 [South China Morning Post] **Trump autopen joke at Biden’s expense draws rare laugh from China’s Xi**
    > Chinese President Xi Jinping broke into rare laughter as his US counterpart Donald Trump showed him a framed “autopen” displayed in place of the former American leader Joe Biden’s portrait during a White House tour.
The viral moment stood out against the Chinese leader’s otherwis
  - 2026-09-25T08:05 [South China Morning Post] **Trump gives Xi a tour of his pet White House building projects, including the ballroom**
    > Property developer-turned-president Donald Trump appeared to relish showing off the White House’s latest building works to Xi Jinping on Thursday, eager to give his Chinese counterpart a glimpse of his construction ambitions since they last met in China.
In May, Trump was hosted 

**Development B** `2026-09-25:us-china-summit-outcome`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-25T03:57 to 2026-09-25T03:57 UTC
- **Actors:** Donald Trump, Trump, Xi Jinping
- **Places:** China, Taiwan
- **System Development:** D3
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T03:57 [BBC World] **Xi got Trump's red carpet welcome - but not everything he wanted**
    > China wanted progress on trade, technology and Taiwan - but hasn't got as much as it would have hoped for.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | commentary |

**Rationale:** B is BBC analysis of the Xi visit's results rather than a distinct occurrence relating to the White House tour in A.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R027

**Development A** `2026-09-30-multilingual:sx-28`

- **Members:** 1 item(s)
- **Sources:** White House
- **Times:** 2026-09-28T19:59 to 2026-09-28T19:59 UTC
- **Actors:** All Presidential Actions, Briefings & Statements, Nominations & Appointments, Senate
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28 19:59 [White House] **Nominations Sent to the Senate**
    > Nominations Sent to the Senate				
			
			
					
	
		
		
			Search
					
						
		
			
				
					Select Category				
				
																		
								All News							
																								
								Briefings &amp; Statements							
																								
																	
					

**Development B** `2026-09-30-multilingual:sx-21`

- **Members:** 1 item(s)
- **Sources:** White House
- **Times:** 2026-09-29T21:23 to 2026-09-29T21:23 UTC
- **Actors:** All Presidential Actions, Briefings & Statements, Nominations & Appointments
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 21:23 [White House] **Eliminating Disease-Carrying Pests And Restoring Enjoyment Of The Great Outdoors**
    > ELIMINATING DISEASE-CARRYING PESTS AND RESTORING ENJOYMENT OF THE GREAT OUTDOORS				
			
			
					
	
		
		
			Search
					
						
		
			
				
					Select Category				
				
																		
								All News							
																								
								Briefings &amp; Statements						

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** White House nominations list and a pest-control order are unrelated documents.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R028

**Development A** `2026-09-25:white-house-tour`

- **Members:** 2 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-25T03:13 to 2026-09-25T08:05 UTC
- **Actors:** Biden, Donald Trump, Joe Biden, Trump, White House, Xi Jinping
- **Places:** Beijing, China, Great Hall of the People, Oval Office, South Lawn, United States
- **System Development:** D3
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T03:13 [South China Morning Post] **Trump autopen joke at Biden’s expense draws rare laugh from China’s Xi**
    > Chinese President Xi Jinping broke into rare laughter as his US counterpart Donald Trump showed him a framed “autopen” displayed in place of the former American leader Joe Biden’s portrait during a White House tour.
The viral moment stood out against the Chinese leader’s otherwis
  - 2026-09-25T08:05 [South China Morning Post] **Trump gives Xi a tour of his pet White House building projects, including the ballroom**
    > Property developer-turned-president Donald Trump appeared to relish showing off the White House’s latest building works to Xi Jinping on Thursday, eager to give his Chinese counterpart a glimpse of his construction ambitions since they last met in China.
In May, Trump was hosted 

**Development B** `2026-09-25:scmp-summit-reader-qa`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-25T05:55 to 2026-09-25T05:55 UTC
- **Actors:** Asian, Donald Trump, SCMP, Xi Jinping
- **Places:** China, South, Taiwan, United States, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T05:55 [South China Morning Post] **AI war, Taiwan and translation: SCMP answers your questions from Xi-Trump summit**
    > This live article is freely available to our registered users. Please log in or create an account.
Xi’s US summit: Access real-time updates, geopolitical risk analysis, and exclusive reporting from an Asian perspective. Subscribe now with our limited-time offer to stay ahead.
Chi

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | commentary |

**Rationale:** B is a reader Q&A live article on the summit, commentary rather than an occurrence linked to the tour in A.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R029

**Development A** `2026-08-21:israel-reestablishes-west-bank-settlement`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-08-21T05:00 to 2026-08-21T05:00 UTC
- **Actors:** Israel
- **Places:** Israel, Palestine, West Bank
- **System Development:** D5
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T05:00 [BBC World] **Israel re-establishes closed West Bank settlement, defying growing international protests**
    > Thirty "pioneer families" have arrived on a wave of nationalism driven by Israel's government, but the rapid change has left nearby Palestinian residents fearful.

**Development B** `2026-08-21:jewish-activists-protective-presence`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-22T12:51 to 2026-08-22T12:51 UTC
- **Actors:** Israel, Jewish
- **Places:** Israel, Occupied West Bank
- **System Development:** D5
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T12:51 [Al Jazeera] **Jewish activists push back against Israeli settlers**
    > Jewish activists provide a ‘protective presence’ to deter settler violence in parts of the Occupied West Bank.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Settlement re-establishment and Jewish activists' protective presence share only the West Bank topic.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R030

**Development A** `2026-08-31:sarawak-haze-indonesian-fires`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T07:10 to 2026-08-31T07:10 UTC
- **Actors:** API, Bornean, Indonesia, Malaysia, Serian, Sri Aman
- **Places:** Indonesia, Kuching, Malaysia, Samarahan, Sarawak, West Kalimantan
- **System Development:** D2
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T07:10 [South China Morning Post] **Malaysia’s air quality turns hazardous as Indonesian wildfires burn**
    > Air pollution in Malaysia’s Bornean state of Sarawak has surged into hazardous territory, with the air pollutant index (API) topping 400 in the worst-hit district, as forest fires raging in Indonesia continue to send thick smoke drifting across the border.
Serian in Sarawak, clos

**Development B** `2026-08-31:orangutans-borneo-wildfires`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-08-31T22:05 to 2026-08-31T22:05 UTC
- **Actors:** Indonesia, Malaysia
- **Places:** Borneo, Indonesia
- **System Development:** D2
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T22:05 [BBC World] **Orangutans in danger as wildfires blaze through Borneo**
    > Wildfires in Indonesia have destroyed part of the natural habitat of hundreds of orangutans, risking the survival of the species.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_calamity_lifecycle` | none | low | none |

**Rationale:** Haze in Sarawak from Indonesian forest fires and orangutan habitat destroyed by wildfires in Borneo appear to be effects of the same ongoing Indonesian Borneo fire episode on the same day.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R031

**Development A** `2026-09-27-live:nepal-floods-one-month-missing`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T17:29 to 2026-09-27T17:29 UTC
- **Actors:** none extracted
- **Places:** Nepal
- **System Development:** D9
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T17:29 [Al Jazeera] **One month after Nepal’s catastrophic floods, thousands remain missing**
    > A month after floods tore through Nepal, 5,285 people remain missing and more than 1,100 are still in holding centres.

**Development B** `2026-09-27-live:nepal-more-floods-14-dead`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T04:44 to 2026-09-28T04:44 UTC
- **Actors:** none extracted
- **Places:** Nepal
- **System Development:** D9
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T04:44 [Al Jazeera] **14 killed, a dozen missing as Nepal is hit by more floods and landslides**
    > At least 14 people have been killed and 11 remain missing after heavy rain triggered floods and landslides across Nepal.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** B is a new rain-triggered flood and landslide event, distinct from the August flood whose aftermath A reports.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R032

**Development A** `2026-08-21:meghan-netflix-gentlemen-talks`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-08-21T18:29 to 2026-08-21T18:29 UTC
- **Actors:** BBC, Meghan, Netflix, Prince Harry
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T18:29 [BBC World] **Meghan in talks for role in Netflix series The Gentlemen, BBC understands**
    > This would be Meghan's first significant acting role since her marriage to Prince Harry.

**Development B** `2026-08-21:harry-meghan-brand-on-return`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-08-22T00:03 to 2026-08-22T00:03 UTC
- **Actors:** Harry, Meghan
- **Places:** UK
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T00:03 [BBC World] **As they return to the UK, Harry and Meghan search for a brand that sticks**
    > They will not be working royals when they come back. So what could they be doing instead?

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** B is commentary on Harry and Meghan's brand; A is Meghan's Netflix talks.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R033

**Development A** `2026-10-03-live:s-1153`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T13:26 to 2026-09-29T13:26 UTC
- **Actors:** Milrem Robotics
- **Places:** Estonia, Moscow, Russia, Tallinn, Ukraine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 13:26 [Al Jazeera] **Estonia says Russia ordered August arson attack on defence company**
    > Tallinn accuses Moscow of responsibility for the fire at Estonian company Milrem Robotics, a supplier of unmanned ground vehicles to Ukraine.

**Development B** `2026-10-03-live:s-1654`

- **Members:** 1 item(s)
- **Sources:** Defense News
- **Times:** 2026-10-01T14:13 to 2026-10-01T14:13 UTC
- **Actors:** Lai, Lai Ching-te
- **Places:** China, NEW TAIPEI CITY, Taiwan, Ukraine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 14:13 [Defense News] **Taiwan takes a page from Ukraine’s playbook in steeling society for an invasion**
    > NEW TAIPEI CITY, Taiwan — Taiwan President Lai Ching-te told a forum in late September he was seeking “resilience through unity” with a new alliance that would let world officials and non-governmental groups prepare together in case of disaster.For Taiwan, that could mean an atta

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Estonia's arson accusation against Russia and Taiwan's resilience planning are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R034

**Development A** `2026-10-03-live:s-1486`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-30T23:13 to 2026-09-30T23:13 UTC
- **Actors:** Donald Trump, Families, Trump, White House, Xi Jinping
- **Places:** Beijing, China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 23:13 [South China Morning Post] **Trump claims he discussed release of political prisoners in China with Xi at summit**
    > US President Donald Trump said on Wednesday that he discussed the release of political prisoners in China with his counterpart, Xi Jinping, in Washington last week.
“We talked, and I think we had some very, very important discussions. Hopefully fruitful discussions,” Trump told r

**Development B** `2026-10-03-live:s-1701`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-10-01T19:10 to 2026-10-01T19:10 UTC
- **Actors:** Donald Trump, Jacqueline Alemany, Trump, White House, Xi Jinping
- **Places:** China, Russia, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 19:10 [South China Morning Post] **Xi leaves Washington, but keeps at least two places on the White House walls**
    > Chinese President Xi Jinping has left Washington, but he still has a place at the White House. At least two, in fact.
Two different photographs of Xi with US President Donald Trump feature on its walls: a handshake image that Trump showed his guest during last week’s state visit,

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | none |

**Rationale:** Trump's claim about discussing prisoners and a feature on Xi photos at the White House share only the summit context.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R035

**Development A** `2026-09-30-multilingual:sx-360`

- **Members:** 1 item(s)
- **Sources:** Council of the EU Press
- **Times:** 2026-09-29T16:02 to 2026-09-29T16:02 UTC
- **Actors:** Council of the European Union, European Union
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 16:02 [Council of the EU Press] **MFF 2028-2034: Council agrees negotiating position on future EU support for the fisheries sector**
    > Council agrees partial negotiating position on the EU support to fisheries, aquaculture and maritime policy for 2028-2034.

**Development B** `2026-09-30-multilingual:sx-353`

- **Members:** 1 item(s)
- **Sources:** European Commission Press
- **Times:** 2026-09-29T22:00 to 2026-09-29T22:00 UTC
- **Actors:** Copernicus, EU Earth, European Commission, Marine Environment Monitoring Service
- **Places:** Arctic, Brussels
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 22:00 [European Commission Press] **Commission report finds devastating shifts in the Arctic and record-breaking marine heatwaves**
    > European Commission Press release Brussels, 30 Sep 2026 The ocean is changing at an alarming pace with direct consequences for marine life, coastlines and communities all across the world. That is the main conclusion of the tenth report on the state of the ocean, published today 

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Council fisheries funding position and the Commission ocean report are separate EU acts.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R036

**Development A** `2026-09-25:netanyahu-unga-speech-walkout`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-25T00:44 to 2026-09-25T00:44 UTC
- **Actors:** Benjamin Netanyahu, UN General Assembly, United Nations
- **Places:** Israel
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T00:44 [BBC World] **Netanyahu defends Israeli military action as delegates walk out before UN speech**
    > The Israeli leader labels those who left his speech at the UN General Assembly as "moral cowards".Â

**Development B** `2026-09-25:israel-palestine-treatment-at-un`

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

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | commentary |

**Rationale:** B analyses the contrasting UN treatment of Israel and Palestine; it is commentary on A's speech, not a distinct occurrence.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R037

**Development A** `2026-09-27-live:nepal-more-floods-14-dead`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T04:44 to 2026-09-28T04:44 UTC
- **Actors:** none extracted
- **Places:** Nepal
- **System Development:** D9
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T04:44 [Al Jazeera] **14 killed, a dozen missing as Nepal is hit by more floods and landslides**
    > At least 14 people have been killed and 11 remain missing after heavy rain triggered floods and landslides across Nepal.

**Development B** `2026-09-27-live:nepal-floods-tourism`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T05:28 to 2026-09-28T05:28 UTC
- **Actors:** Himalayan
- **Places:** Nepal
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T05:28 [Al Jazeera] **‘Still a lockdown’: Deadly floods hit Nepal tourism as peak season begins**
    > As Himalayan nation recovers from devastating floods, a million people dependent on tourism struggle to make ends meet.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | none |

**Rationale:** B's tourism impact refers to the earlier devastating floods, not to the new floods and landslides in A.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R038

**Development A** `2026-10-03-live:s-1235`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-29T22:00 to 2026-09-29T22:00 UTC
- **Actors:** Peng Liyuan, White House, Xi Jinping
- **Places:** Beijing, China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 22:00 [South China Morning Post] **Xi-Trump summit drew Chinese CEOs. So why couldn’t they get a seat at the table?**
    > As American billionaires gathered at the White House to honour Chinese President Xi Jinping and his wife Peng Liyuan last Thursday, a group of Chinese business leaders spent the evening on the sidelines.
They had travelled to the US capital to join the state dinner. But their inv

**Development B** `2026-10-03-live:s-1585`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-10-01T09:40 to 2026-10-01T09:40 UTC
- **Actors:** none extracted
- **Places:** China, Europe, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 09:40 [Al Jazeera] **Can Europe still compete with the US and China?**
    > Europe faces growing pressure from the US and China as it struggles to stay competitive.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** State-dinner CEO analysis and European competitiveness discussion share no matter.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R039

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

**Development B** `2026-09-27-live:cuba-decries-us-military-action`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T20:34 to 2026-09-27T20:34 UTC
- **Actors:** none extracted
- **Places:** Cuba, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T20:34 [Al Jazeera] **‘Atrocious’ crime: Cuban official decries possibility of US military action**
    > Cuba&#039;s deputy foreign minister slams US sanctions, labelling them &#039;equivalent to genocide&#039;.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Hormuz tensions and a Cuban official decrying US sanctions share only the US as actor.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R040

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

**Development B** `2026-08-21:settlers-burn-hebron-quarry-machinery`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-21T16:00 to 2026-08-21T16:00 UTC
- **Actors:** none extracted
- **Places:** Hebron, Israel, Wadi Al-Rakheem, West Bank
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T16:00 [Al Jazeera] **Israeli settlers set fire to heavy machinery at West Bank quarry**
    > Israeli settlers entered a stone quarry in Wadi Al-Rakheem near Hebron overnight and set fire to heavy machinery

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Soldiers in Qusra and settlers burning machinery near Hebron are separate incidents in different places.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R041

**Development A** `2026-10-03-live:s-1482`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-30T23:25 to 2026-09-30T23:25 UTC
- **Actors:** Douyin, TikTok
- **Places:** China, Huangshi
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 23:25 [BBC World] **China has cracked down on AI relationships. Is it ahead of the game?**
    > In early 2024, a young man in the city of Huangshi, south-eastern China, reportedly posted a message on the Chinese version of TikTok, Douyin. The caption read: "Farewell to this world."

Within minutes, the suicide prevention team at Douyin kicked into gear. The team, which is s

**Development B** `2026-10-03-live:s-1532`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-10-01T02:00 to 2026-10-01T02:00 UTC
- **Actors:** Xue Dinge
- **Places:** China
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 02:00 [South China Morning Post] **Chinese women spend top dollar on male model shoots, turning staged romance into viral trend**
    > A growing number of young Chinese women are paying for romantic photo shoots with male models, seeking a brief taste of love through a novel form of emotional companionship.
This trend has gained significant traction on mainland social media, with customers spending up to 8,000 y

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** China's AI-relationship crackdown and paid romantic photo shoots share only a broad topic.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R042

**Development A** `2026-08-31:venezuela-oil-deal-implications`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-31T00:41 to 2026-08-31T00:41 UTC
- **Actors:** none extracted
- **Places:** US, Venezuela, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T00:41 [Al Jazeera] **What are the implications of the US-Venezuela oil deal?**
    > Opposition in Venezuela as interim leader insists the deal with Washington will help with the country&#039;s recovery.

**Development B** `2026-08-31:operation-economic-outcast-failing`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-31T10:18 to 2026-08-31T10:18 UTC
- **Actors:** Operation Economic Outcast
- **Places:** Iran, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T10:18 [Al Jazeera] **The looming failure of Operation Economic Outcast**
    > The latest package of US sanctions on Iran is unlikely to achieve Washington’s objectives.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** US-Venezuela oil deal analysis and Iran sanctions commentary are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R043

**Development A** `2026-10-03-live:s-1173`

- **Members:** 1 item(s)
- **Sources:** Defense News
- **Times:** 2026-09-29T14:40 to 2026-09-29T14:40 UTC
- **Actors:** Donald Trump, Islamic State, Joe Biden
- **Places:** Iran, Iraq, Tehran, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 14:40 [Defense News] **US forces exiting Iraq after 2 decades, leaving opening for Iran**
    > U.S. forces are set to depart from their last bases in Iraq by Wednesday, a move celebrated as a victory by Iran and its allies, who now have deep influence in the country where 4,500 Americans died during more than two decades of war.Iraqi security experts say the withdrawal — a

**Development B** `2026-10-03-live:s-1259`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-30T00:00 to 2026-09-30T00:00 UTC
- **Actors:** none extracted
- **Places:** Iran, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 00:00 [Al Jazeera] **Iran war live: Trump claims war will end ‘very soon’, gives no details**
    > Top leadership in Iran reviews latest US response offer to end war as economic turmoil and political concerns rise.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** US withdrawal from Iraq and Trump's claim the Iran war ends soon are not explicitly linked.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R044

**Development A** `2026-10-03-live:s-1585`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-10-01T09:40 to 2026-10-01T09:40 UTC
- **Actors:** none extracted
- **Places:** China, Europe, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 09:40 [Al Jazeera] **Can Europe still compete with the US and China?**
    > Europe faces growing pressure from the US and China as it struggles to stay competitive.

**Development B** `2026-10-03-live:D16`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera, South China Morning Post
- **Times:** 2026-10-01T14:00 to 2026-10-02T20:52 UTC
- **Actors:** Beijing, China, Guo Jiakun, Latin American, Panama, United Nations
- **Places:** Beijing, China, Cuba, Havana, Latin America, Panama, US, Washington
- **System Development:** D16
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 14:00 [South China Morning Post] **China backs Cuba, Beijing’s Panama threat, new UN chief: 7 Latin America relations reads**
    > We have selected seven of the most interesting and important news stories covering Latin American relations from the past few weeks. If you would like to see more of our reporting, please consider subscribing.
1. China pledges to ‘firmly support’ Cuba as US escalates pressure on 
  - 2026-10-02 20:52 [Al Jazeera] **Latin America sees China as more positive global influence than US: Poll**
    > Annual Latinobarometro survey finds views of China’s influence improving as perceptions of US influence worsen.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** European competitiveness discussion and Latin America digest/poll are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R045

**Development A** `2026-08-31:nepal-rescue-tunnel-workers-toll-900`

- **Members:** 4 item(s)
- **Sources:** Al Jazeera, BBC World, South China Morning Post
- **Times:** 2026-08-31T06:05 to 2026-09-01T16:11 UTC
- **Actors:** BBC Major, CCTV, Himalayan, Nepal
- **Places:** China, Gyirong Port, India, Nepal
- **System Development:** D1
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T06:05 [South China Morning Post] **Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000**
    > Rescuers from China and Nepal continued searching landslide- and flood-affected areas on Monday while efforts to reopen roads to the heart of the disaster-hit area at Gyirong Port entered a “critical stage”.
The death toll in Nepal had risen to 903 as of 9am on Monday, with 4,247
  - 2026-08-31T07:34 [Al Jazeera] **Nepal races to rescue trapped workers, as flood death toll surpasses 900**
    > Nepal officials say rescuers focusing on reaching workers in hydropower project tunnels in flood-stricken region.
  - 2026-09-01T06:02 [BBC World] **The final minutes before floodwater crashed through Nepal-China border**
    > More than 100 Indians are missing at a vital Nepal-China trade crossing after devastating Himalayan floods.
  - 2026-09-01T16:11 [BBC World] **River water smashed into tunnel and chased me for 20 minutes, Nepal worker tells BBC**
    > Major efforts to rescue hydropower workers continue as Nepal's death toll exceeds 1,000.

**Development B** `2026-08-31:nepal-tunnel-traps-how-many-dead`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-31T10:17 to 2026-08-31T10:17 UTC
- **Actors:** none extracted
- **Places:** Nepal, Tibet
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T10:17 [Al Jazeera] **Nepal tunnel traps hinder flood rescue: How many are dead or missing?**
    > Flash floods on the Nepal-Tibet border have left nearly 5,000 people missing, many trapped in hydropower tunnels.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | SAME_DEVELOPMENT_SUSPECTED |

**Rationale:** Both report the same Aug 31 rescue status and missing count for workers trapped in hydropower tunnels after the Nepal-Tibet flood.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R046

**Development A** `2026-09-27-live:pope-meets-abuse-survivors`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera, South China Morning Post
- **Times:** 2026-09-27T09:16 to 2026-09-27T23:14 UTC
- **Actors:** Catholics, Leo, Pope, Roman Catholic Church
- **Places:** France, Lourdes, US
- **System Development:** D2
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T09:16 [South China Morning Post] **Pope meets victims of sex abuse, urges ‘wise leaders’ as French election looms**
    > Pope Leo waved at believers on his way to mass on Sunday in the French pilgrimage town of Lourdes where he is to meet victims of clerical sex abuse on a third day of an official visit to France.
The leader of the world’s 1.4 billion Catholics is on a four-day trip to France, a se
  - 2026-09-27T23:14 [Al Jazeera] **Pope pledges action on clergy child abuse in meeting with French survivors**
    > Head of the Roman Catholic Church holds &#039;emotional&#039; two-hour meeting with seven survivors in French town of Lourdes.

**Development B** `2026-09-27-live:pope-bishops-abuse-speech`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-27T11:38 to 2026-09-27T11:38 UTC
- **Actors:** Leo, Pope
- **Places:** France, Lourdes
- **System Development:** D2
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T11:38 [BBC World] **'Scourge' of abuse must be rooted out, says Pope during Lourdes visit**
    > Pope Leo spoke to bishops before leading a service attended by thousands of worshippers in France.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_visit_or_summit` | none | high | none |

**Rationale:** Pope Leo's meeting with abuse survivors and his address to bishops both took place in Lourdes on the same day of his France visit.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R047

**Development A** `2026-10-03-live:s-1295`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-30T06:48 to 2026-09-30T06:48 UTC
- **Actors:** Kim Jong Un, Trump
- **Places:** Iran, N Korea, North Korea, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 06:48 [Al Jazeera] **Trump calls Kim Jong Un a ‘friend’ and plays down N Korea’s nuclear arsenal**
    > US president&#039;s comments came after he was asked why North Korea can have nuclear weapons when Iran cannot.

**Development B** `2026-10-03-live:s-1907`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-10-02T14:00 to 2026-10-02T14:00 UTC
- **Actors:** AI, Donald Trump
- **Places:** China, Laos, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-02 14:00 [South China Morning Post] **‘America is back’, AI ‘conspiracy’, China’s Laos deal: 7 global relations reads**
    > We have selected seven of the most interesting and important news stories covering global relations from the past few weeks. If you would like to see more of our reporting, please consider subscribing.
1. Trump condemns ‘sick conspiracy’ against AI, says he is only guardrail need

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** Trump's Kim remark and a global relations digest are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R048

**Development A** `2026-09-27-live:labour-conference-opens`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-27T17:54 to 2026-09-27T17:54 UTC
- **Actors:** Andy Burnham, Burnham, Keir Starmer, UK Labour Party
- **Places:** Britain, Downing Street, Liverpool, Manchester
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T17:54 [South China Morning Post] **UK Labour Party meets buoyed by Burnham but seeking concrete plans**
    > Britain’s ruling Labour Party on Sunday launched its first annual conference under Andy Burnham’s leadership, buoyed by his debut as prime minister as he pledged to take the tough decisions needed to tackle looming challenges.
The former mayor of Manchester has injected new life 

**Development B** `2026-09-27-live:healey-defence-reindustrialisation`

- **Members:** 1 item(s)
- **Sources:** Defense News
- **Times:** 2026-09-28T11:13 to 2026-09-28T11:13 UTC
- **Actors:** Andy Burnham, Healey, John Healey, Keir Starmer, UK Labour Party
- **Places:** Britain, Clyde, England, Liverpool, Scotland, UK
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T11:13 [Defense News] **UK’s Healey puts defense in focus for reindustrialization push**
    > LIVERPOOL, England — British finance minister John Healey will put his support firmly behind firms investing in defense on Monday, part of what he will describe as a new industrialization drive to try to spur the nation’s anaemic economic growth.In his first speech to the governi

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_visit_or_summit` | none | high | none |

**Rationale:** Healey's speech is explicitly his first speech to the Labour Party annual conference launched in A.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R049

**Development A** `2026-09-27-live:yemen-health-system-warning`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T14:07 to 2026-09-27T14:07 UTC
- **Actors:** Al Jazeera
- **Places:** Yemen
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T14:07 [Al Jazeera] **Yemen’s health system could collapse in some areas, minister warns**
    > Yemen&#039;s healthcare system may not be able to support the population as war strains resources, minister tells Al Jazeera.

**Development B** `2026-09-27-live:bbc-yemen-frontline-report`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-27T21:16 to 2026-09-27T21:16 UTC
- **Actors:** BBC, Houthis
- **Places:** Yemen
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T21:16 [BBC World] **Inside Yemen's front-line city as Houthis battle for control**
    > In rare access to Yemen's conflict zone the BBC travels to the front line with pro-government soldiers.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Yemen health minister warning and a front-line reportage share only the Yemen war.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R050

**Development A** `2026-10-03-live:s-1174`

- **Members:** 1 item(s)
- **Sources:** Breaking Defense
- **Times:** 2026-09-29T15:20 to 2026-09-29T15:20 UTC
- **Actors:** Democrat, House, House Permanent Select Committee on Intelligence, Jim Himes, White House
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 15:20 [Breaking Defense] **House intel committee could investigate defense firm contributions to White House ballroom**
    > Rep. Jim Himes, the top Democrat on the House Permanent Select Committee on Intelligence, sent a Sept. 28 letter to a defense trade group warning of a &#8220;likely&#8221; probe into the project.

**Development B** `2026-10-03-live:s-1250`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-30T04:36 to 2026-09-30T04:36 UTC
- **Actors:** Celinda Lake, Democrat, Trump
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 04:36 [Al Jazeera] **Democrats hope anger at Trump enough to get young people to vote**
    > Political strategist Celinda Lake says that young voters don’t usually cast their ballots in midterm elections.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Possible House probe into ballroom donations and Democrats' youth vote strategy are not linked.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R051

**Development A** `2026-09-27-live:amicro-hk-ipo`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-28T05:14 to 2026-09-28T05:14 UTC
- **Actors:** IPO, Zhuhai Amicro Technology
- **Places:** Hong Kong, Hong Kong Exchanges and Clearing
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T05:14 [South China Morning Post] **Xiaomi-backed robotics chip designer clears hearing, eyes US$100m Hong Kong IPO: sources**
    > Zhuhai Amicro Technology, a Xiaomi-backed chipmaker, is preparing to begin premarketing for a Hong Kong initial public offering (IPO) of more than US$100 million as early as this week, according to people familiar with the matter.
The company passed its listing hearing with bours

**Development B** `2026-09-27-live:hk-slimming-injections-seized`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-28T09:29 to 2026-09-28T09:29 UTC
- **Actors:** Air Mail Centre
- **Places:** Hong Kong, Japan
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T09:29 [South China Morning Post] **Hong Kong customs arrests 2, seizes HK$290,000 of ‘slimming injections’ from Japan**
    > Hong Kong customs officers have seized 400 so-called slimming injections imported from Japan, with an estimated market value of about HK$290,000 (US$36,970), and arrested two local residents in an operation earlier this month.
The case came to light on September 5, when officers 

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Amicro IPO and a customs seizure of slimming injections are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R052

**Development A** `2026-10-03-live:s-1303`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-29T23:33 to 2026-09-29T23:33 UTC
- **Actors:** none extracted
- **Places:** Russia, Ukraine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 23:33 [BBC World] **Ukraine's prized steel industry left in ruins by Russian missile campaign**
    > Ukraine's remaining steelworks, a vital part of its economy, have all but ground to a halt because of relentless attacks.

**Development B** `2026-10-03-live:s-1361`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-30T11:32 to 2026-09-30T11:32 UTC
- **Actors:** none extracted
- **Places:** Kyiv, Russia, Ukraine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 11:32 [Al Jazeera] **Russian attacks on Ukraine’s Kyiv region kill four, target power grid**
    > City officials say three killed in Ukraine&#039;s capital, as emergency services say child killed in the surrounding region.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** A describes the cumulative missile campaign on steelworks; B is a specific Kyiv strike with no stated link.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R053

**Development A** `2026-08-31:china-warns-glacier-collapse-risk`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T06:05 to 2026-08-31T06:05 UTC
- **Actors:** CCTV, Ministry of Water Resources
- **Places:** China, Cuojian River, Nepal, Purepuqiang River, Tibet
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T06:05 [South China Morning Post] **China warns of ‘major risk’ of glacier collapse as Tibet-Nepal death toll nears 1,000**
    > China warned on Monday there was a “major risk” of further glacier collapses and landslides along the border with Nepal as the death toll from last week’s deadly mudslide rose to close to 1,000.
The Ministry of Water Resources said there was an ongoing threat along the Cuojian Ri

**Development B** `2026-08-31:nepal-tunnel-traps-how-many-dead`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-31T10:17 to 2026-08-31T10:17 UTC
- **Actors:** none extracted
- **Places:** Nepal, Tibet
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T10:17 [Al Jazeera] **Nepal tunnel traps hinder flood rescue: How many are dead or missing?**
    > Flash floods on the Nepal-Tibet border have left nearly 5,000 people missing, many trapped in hydropower tunnels.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_calamity_lifecycle` | none | high | none |

**Rationale:** China's warning of further glacier collapse and Nepal's tunnel rescue both concern the same Tibet-Nepal border flood and mudslide.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R054

**Development A** `2026-08-31:nuwakot-residents-return-home`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-31T04:19 to 2026-08-31T04:19 UTC
- **Actors:** none extracted
- **Places:** Nepal, Nuwakot
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T04:19 [Al Jazeera] **People return to their flood-ravaged homes in Nepal**
    > Survivors in Nepal’s Nuwakot district are digging through mud and debris for belongings left behind by flash floods.

**Development B** `2026-08-31:nepal-families-search-missing`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-08-31T16:42 to 2026-08-31T16:42 UTC
- **Actors:** none extracted
- **Places:** Nepal
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T16:42 [BBC World] **'I haven't lost my hope' - the search for missing loved ones**
    > Relatives of those still missing in the fatal floods in Nepal hold onto hope that their loved ones have survived.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_calamity_lifecycle` | none | medium | none |

**Rationale:** Survivors returning home and relatives searching for the missing are stages of the same Nepal flash flood.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R055

**Development A** `2026-09-27-live:southeast-asia-summit-reaction`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-27T08:06 to 2026-09-27T08:06 UTC
- **Actors:** Lucio Blanco Pitlo III, Xi Jinping
- **Places:** China, South China Sea, Southeast Asia, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T08:06 [South China Morning Post] **Why Southeast Asia feels relief and caution after the Xi-Trump summit**
    > Southeast Asia welcomes the continued thaw in US-China ties after the Xi-Trump summit, with analysts saying that less friction between the two powers over issues such as the South China Sea could lower the pressure on the region.
Yet, caution persists as the summit left deeper di

**Development B** `2026-09-27-live:trump-downplays-taiwan-talk`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-27T09:43 to 2026-09-27T09:43 UTC
- **Actors:** Donald Trump, Trump, Xi Jinping
- **Places:** China, Taiwan, US, Washington
- **System Development:** D14
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T09:43 [South China Morning Post] **‘Right now, it’s fine’: Trump brushes off questions about summit talk on Taiwan**
    > US President Donald Trump has sought to play down exchanges with his Chinese counterpart Xi Jinping on Taiwan, saying on Saturday that they touched on the subject only briefly.
“We didn’t talk about it too much. Right now, it’s fine. It’s just moving along,” Trump said. “We didn’

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | commentary |

**Rationale:** A is analysts' commentary on Southeast Asian reaction to the summit; B is Trump's Taiwan remark.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R056

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

**Development B** `2026-08-21:us-designates-hezbollah-iranian-proxy`

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

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | low | none |

**Rationale:** Bessent's vow of toughest Iran sanctions and the Hezbollah designation are not explicitly linked as one package or follow-up.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R057

**Development A** `2026-09-29-live:channel-dinghy-deaths`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera, South China Morning Post
- **Times:** 2026-09-28T12:08 to 2026-09-28T13:48 UTC
- **Actors:** Child, English, François Xavier Lauch
- **Places:** France, Sangatte, UK
- **System Development:** D1
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T12:08 [Al Jazeera] **Child among three killed off French coast in Channel crossing attempt**
    > France&#039;s maritime police ‌‌said ​they received a distress ​call from an inflatable dinghy carrying 105 people.
  - 2026-09-28T13:48 [South China Morning Post] **Child and 2 women ‘crushed to death’ during France to UK sea crossing**
    > A 10-year-old child and two women died on Monday on the treacherous and illegal migration route across the English Channel from France, apparently trampled to death on a packed boat, French authorities said.
The dinghy left the area of Sangatte in northern France at around 5.15am

**Development B** `2026-09-29-live:french-police-tear-gas-beach`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T16:37 to 2026-09-28T16:37 UTC
- **Actors:** English
- **Places:** Britain, France
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T16:37 [Al Jazeera] **French police fire tear gas at migrants on beach**
    > French police have used tear gas to disperse migrants attempting to cross the English Channel to Britain from France.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | none |

**Rationale:** Channel crossing deaths and police tear gas on a beach share place and topic but no stated link.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R058

**Development A** `2026-09-27-live:why-trump-rejected-explainer`

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

**Development B** `2026-09-27-live:fairford-investigation-iran-link`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-28T11:18 to 2026-09-28T11:18 UTC
- **Actors:** RAF Fairford, UK
- **Places:** England, Iran, Middle East, UK, US
- **System Development:** D7
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T11:18 [South China Morning Post] **UK investigates if arrests near US-run base prevented Iran-linked attack**
    > British police were holding five men on Monday and examining suspected explosives found near a US-operated air force base in England, as counterterror detectives investigated whether the arrests foiled an attempted attack linked to Iran.
The men were detained early on Sunday afte

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** Analysis of Trump's rejection and UK arrests near a US base are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R059

**Development A** `2026-09-27-live:why-trump-rejected-explainer`

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

**Development B** `2026-09-27-live:oil-surges-after-rejection`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T09:17 to 2026-09-28T09:17 UTC
- **Actors:** Trump
- **Places:** Iran, Strait, Tehran, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T09:17 [Al Jazeera] **Oil prices surge after Trump rejects Iran’s plan to reopen Strait of Hormuz**
    > Brent crude rises more than 3 percent to top $107 a barrel as Washington dismisses Tehran&#039;s proposal to end war.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | commentary |

**Rationale:** A is analysis of why Trump rejected Iran's plan; B's oil surge is caused by the rejection itself, not by A.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R060

**Development A** `2026-08-21:jewish-activists-protective-presence`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-22T12:51 to 2026-08-22T12:51 UTC
- **Actors:** Israel, Jewish
- **Places:** Israel, Occupied West Bank
- **System Development:** D5
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T12:51 [Al Jazeera] **Jewish activists push back against Israeli settlers**
    > Jewish activists provide a ‘protective presence’ to deter settler violence in parts of the Occupied West Bank.

**Development B** `2026-08-21:settlers-target-qaryut-homes`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-22T15:45 to 2026-08-22T15:45 UTC
- **Actors:** Israel
- **Places:** Israel, Occupied West Bank, Palestine, Qaryut
- **System Development:** D5
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T15:45 [Al Jazeera] **Settlers target Palestinian homes in Occupied West Bank’s Area B**
    > Palestinians in Qaryut say Israeli settlers, backed by the military, are forcing families from their homes.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Jewish activists' protective presence and settler attacks in Qaryut share only the West Bank topic.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R061

**Development A** `2026-09-30-multilingual:sx-221`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-30T08:00 to 2026-09-30T08:00 UTC
- **Actors:** European Union, Maros Sefcovic
- **Places:** Beijing, Berlín, Brussels, China, Europe
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 08:00 [South China Morning Post] **EU weighs sweeping new trade powers against China before make-or-break October**
    > Brussels and Berlin are steeling themselves for a make-or-break October with China, as the mood towards Beijing hardens in both capitals.
The month ahead could help set the course of the increasingly thorny EU-China relationship for years to come, as Europe gears up to present a 

**Development B** `2026-09-30-multilingual:sx-347`

- **Members:** 1 item(s)
- **Sources:** European Commission Press
- **Times:** 2026-09-30T09:06 to 2026-09-30T09:06 UTC
- **Actors:** Daily News, Democratic Resilience, European Centre, European Centre for Democratic Resilience, European Commission
- **Places:** Brussels
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 09:06 [European Commission Press] **Daily News 30 / 09 / 2026**
    > European Commission Daily news Brussels, 30 Sep 2026 European Centre for Democratic Resilience launches cooperation with stakeholders
The European Centre for Democratic Resilience launched the first phase of its S...

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** EU trade-power deliberations and the Commission daily news item on Democratic Resilience are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R062

**Development A** `2026-09-25:first-ladies-smithsonian`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-25T04:43 to 2026-09-25T04:43 UTC
- **Actors:** Hope Chinese School, Melania Trump, Peng, Peng Liyuan, Smithsonian National Museum of Asian Art, White House
- **Places:** China, United States
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T04:43 [South China Morning Post] **Pitch perfect cultural diplomacy wins heart of China’s first lady Peng Liyuan**
    > While their husbands held talks at the White House, Melania Trump hosted Peng Liyuan at the Smithsonian National Museum of Asian Art on Thursday, where the famed Chinese soprano softly hummed along to a youth choir’s performance of a familiar classic.
Footage shows the Hope Chine

**Development B** `2026-09-25:nepal-flood-climate-appeal`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera, South China Morning Post
- **Times:** 2026-09-25T06:56 to 2026-09-25T07:02 UTC
- **Actors:** Balendra Shah, Himalayan, Nepal, Shah, UN General Assembly
- **Places:** China, Himalaya, India, Nepal, New York
- **System Development:** D4
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T06:56 [Al Jazeera] **Nepal’s leader labels devastating flood a ‘warning to the world’**
    > Prime Minister Balendra Shah says world leaders must act on climate change.
  - 2026-09-25T07:02 [South China Morning Post] **Flood-ravaged Nepal pushes for climate deal with India, China**
    > Nepal’s Prime Minister Balendra Shah proposed a climate alliance with neighbouring India and China, urging action to protect the fragile Himalayan ecosystem after catastrophic flooding across the region.
“Glaciers and floods do not travel with stamps and passports,” Shah told wor

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Peng Liyuan's museum visit and Nepal's climate appeal are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R063

**Development A** `2026-10-03-live:s-1533`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-10-01T01:58 to 2026-10-01T01:58 UTC
- **Actors:** Donald Trump, Xi Jinping, Xie, Xie Feng
- **Places:** China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 01:58 [South China Morning Post] **Xi-Trump rapport is ‘most valuable strategic asset’ in US-China ties, envoy Xie says**
    > The Chinese ambassador to the United States, Xie Feng, on Wednesday described the personal rapport and “mutual respect” between Chinese President Xi Jinping and US President Donald Trump as the “most valuable strategic asset in our bilateral relations”.
“Their personal connection

**Development B** `2026-10-03-live:s-1591`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-10-01T10:02 to 2026-10-01T10:02 UTC
- **Actors:** Marco Rubio, State, US State Department, Xi Jinping
- **Places:** Beijing, China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 10:02 [South China Morning Post] **Days after Xi-Trump summit, the US marks China’s National Day with pared-down note**
    > Five days after Chinese President Xi Jinping left Washington, the US State Department marked the 77th anniversary of the People’s Republic of China with a greeting short enough to fit on a calling card.
US Secretary of State Marco Rubio’s congratulatory statement landed on Wednes

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Ambassador Xie's remark and the US National Day note are separate acts sharing only the bilateral relationship.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R064

**Development A** `2026-09-30-multilingual:D9`

- **Members:** 5 item(s)
- **Sources:** BBC Mundo, Clarín Mundo, France 24 Español
- **Times:** 2026-09-29T15:04 to 2026-09-30T02:47 UTC
- **Actors:** Brigitte Macron, Consejo de Estado, Emmanuel, Emmanuel Macron, Letizia, Macron, Maricarmen, Parlamento, Pedro Sánchez, Senado de España
- **Places:** España, Estado a España, Europa, Francia, Palacio Real de Madrid
- **System Development:** D9
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 15:04 [BBC Mundo] **La anciana Maricarmen podrá volver a su casa tras el desalojo que puso el foco en la crisis de vivienda en España**
    > De acuerdo a lo señalada por la abogada, la empresa dueña del inmueble le dejará pagar un alquiler acorde a la pensión que recibe.
  - 2026-09-29 18:08 [Clarín Mundo] **Los reyes de España despliegan todo el protocolo para recibir a Emmanuel y Brigitte Macron en visita oficial**
    > El rey Felipe y la reina Letizia le dieron la bienvenida al presidente de Francia en el Palacio Real de Madrid.Por la noche brindaron una cena de gala para los Macron en la que no faltaron la elegancia y la tiara del joyero de la reina.
  - 2026-09-29 18:43 [Clarín Mundo] **Presionado por las protestas, Pedro Sánchez anuncia decretos clave para enfrentar la crisis de la vivienda en España**
    > Las medidas apuntan a frenar los desalojos y controlar los fondos buitres. Además,  los contratos de alquiler vigentes puedan extenderse automáticamente por dos años.Para que las normas mantengan sus efectos en el tiempo, el Parlamento tiene que aprobarlo dentro de los 30 días.
  - 2026-09-29 22:57 [France 24 Español] **Macron aboga en su visita a España por una "Europa más fuerte" ante el auge del "extremismo"**
    > En el primer día de su visita de Estado a España, el presidente Emmanuel Macron pidió el martes 29 de septiembre una inversión masiva para una "Europa más fuerte" y para "recuperar el control" de las redes sociales y la inteligencia artificial, a las que consideró responsables de

**Development B** `2026-09-30-multilingual:sx-155`

- **Members:** 1 item(s)
- **Sources:** France 24
- **Times:** 2026-09-30T09:13 to 2026-09-30T09:13 UTC
- **Actors:** Emmanuel Macron, Felipe VI, Franco, Macron, Pedro Sánchez
- **Places:** France, Royal Palace, Spain
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 09:13 [France 24] **Attention turns to economy on final day of Macron’s visit to Spain**
    > President Emmanuel Macron is in Spain for the final day of his two-day state visit, the first by a French president to the country since 2009. After being welcomed with a banquet at the Royal Palace by King Felipe VI on Tuesday, on today's agenda is the opening of the Franco-Span

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_visit_or_summit` | none | medium | none |

**Rationale:** A includes the Madrid welcome and first day of Macron's state visit; B is the final day of the same two-day visit.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R065

**Development A** `2026-09-29-live:eu-five-defense-priorities`

- **Members:** 1 item(s)
- **Sources:** Defense News
- **Times:** 2026-09-28T14:59 to 2026-09-28T14:59 UTC
- **Actors:** Council of the European Union, EDIP, European, European Commission, European Defence Industry Program, European Union
- **Places:** Europe, PARIS
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T14:59 [Defense News] **EU nails down five defense priority areas to channel common spending**
    > PARIS — European Union member states approved five projects for joint defense-industrial investment in priority areas including drones and counter-drone systems as well as air and missile defense, part of efforts to encourage more cooperation on defense spending and avoid overlap

**Development B** `2026-09-29-live:china-germany-trade-call`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-29T07:31 to 2026-09-29T07:31 UTC
- **Actors:** Commerce, European, European Union, Katherina Reiche, Reiche, Sino-European, Sino-German, Wang, Wang Wentao
- **Places:** Beijing, Berlin, Brussels, China, France, Germany
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T07:31 [South China Morning Post] **Beijing and Berlin ‘exchanged opinions’ amid reported plan to shut China out of EU market**
    > Chinese Commerce Minister Wang Wentao held a video call with German Economy Minister Katherina Reiche on Monday, just over a week before the next round of trade talks between Beijing and Brussels, amid reports that Germany and France are pushing for a new tool that would enable t

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** EU defence priority projects and Sino-German trade call are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R066

**Development A** `2026-09-30-multilingual:D1`

- **Members:** 4 item(s)
- **Sources:** Council of the EU Press, European Commission Press
- **Times:** 2026-09-28T16:05 to 2026-09-29T22:00 UTC
- **Actors:** Council of the European Union, EU Critical Communication System Factsheet, EU Space Threat Response Architecture, European Commission, European Union, European Union Critical Communication System
- **Places:** Brussels, Europe
- **System Development:** D1
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28 16:05 [Council of the EU Press] **Council strengthens EU space threat response architecture**
    > The Council has adopted a decision strengthening the EU Space Threat Response Architecture to respond to increased irresponsible and hostile behaviour in the space domain.
  - 2026-09-29 22:00 [European Commission Press] **Factsheet: EU Critical Communication System**
    > European Commission Factsheet Brussels, 30 Sep 2026   Factsheet: EU Critical Communication System Factsheet: EU Critical Communication System
  - 2026-09-29 22:00 [European Commission Press] **Questions and answers on the European Union Critical Communication System**
    > European Commission Questions and answers Brussels, 30 Sep 2026 What is the European Union Critical Communication System?
The European Union Critical Communication System (EUCCS) connects national critical communication syst...
  - 2026-09-29 22:00 [European Commission Press] **Commission proposes a new EU Critical Communication System for first responders**
    > European Commission Press release Brussels, 30 Sep 2026 Today, the European Commission proposed to establish a new EU Critical Communication System to provide Europe's first responders with secure and resilient communication channels in crisis situations.

**Development B** `2026-09-30-multilingual:sx-347`

- **Members:** 1 item(s)
- **Sources:** European Commission Press
- **Times:** 2026-09-30T09:06 to 2026-09-30T09:06 UTC
- **Actors:** Daily News, Democratic Resilience, European Centre, European Centre for Democratic Resilience, European Commission
- **Places:** Brussels
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 09:06 [European Commission Press] **Daily News 30 / 09 / 2026**
    > European Commission Daily news Brussels, 30 Sep 2026 European Centre for Democratic Resilience launches cooperation with stakeholders
The European Centre for Democratic Resilience launched the first phase of its S...

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `AMBIGUOUS` | none | low | none |

**Rationale:** The Daily News excerpt shows only the Democratic Resilience item; if its body lists the EUCCS proposal it is the same Development, otherwise no relation.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R067

**Development A** `2026-08-21:russia-missile-test-kuril-islands`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-21T00:48 to 2026-08-21T00:48 UTC
- **Actors:** Akira Muto, Pacific Fleet, Vladimir Putin
- **Places:** Etorofu, Japan, Russia
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T00:48 [South China Morning Post] **Russia tests missiles near Japanese-claimed islands after Putin’s visit**
    > Russia’s Pacific Fleet said on Thursday it has conducted a missile test off a group of Russian-held, Japanese-claimed islands amid an intensifying row over the disputed territory following President Vladimir Putin’s first-ever visit there last week.
While it was unclear exactly w

**Development B** `2026-08-21:ukraine-mall-strike-rescue`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-08-22T13:13 to 2026-08-22T13:13 UTC
- **Actors:** Volodymyr Zelenskyy
- **Places:** Russia, Ukraine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T13:13 [BBC World] **Rescuers dig through Ukraine mall wreckage as Zelensky condemns 'despicable' Russian strike**
    > Four people are still missing after Friday's attack which killed 16 and left 130 injured, including a number of children.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Russian missile test near Kuril islands and a strike on a Ukraine mall share only Russia.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R068

**Development A** `2026-08-21:un-ebola-growing-faster-2500-deaths`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-21T13:30 to 2026-08-21T13:30 UTC
- **Actors:** DRC, United Nations
- **Places:** Congo, DR
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T13:30 [Al Jazeera] **Ebola outbreak ‘growing faster, ⁠⁠wider’ as DRC death toll passes 2,500: UN**
    > Epidemic remains out of control amid DR Congo conflict, funding shortages and attacks on health workers and facilities

**Development B** `2026-08-21:ervebo-doses-arrive-drc`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-22T10:13 to 2026-08-22T11:15 UTC
- **Actors:** DRC
- **Places:** Congo, Kinshasa
- **System Development:** D3
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T10:13 [Al Jazeera] **More than 16,000 doses of Ervebo vaccine arrive in Ebola-hit DR Congo**
    > The doses are the first of 70,000 allocated for Kinshasa as experts warn of the virus&#039;s exponential spread.
  - 2026-08-22T11:15 [Al Jazeera] **Ebola continues to spread in the DRC as 16,000 vaccine doses arrive**
    > Health authorities are warning that ‘approximately one person has been dying from Ebola every thirty minutes’.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_calamity_lifecycle` | none | high | none |

**Rationale:** Ebola spread warning and vaccine doses arriving are stages of the same DRC Ebola outbreak.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R069

**Development A** `2026-09-29-live:kyiv-academy-of-sciences-strike`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T17:06 to 2026-09-28T17:37 UTC
- **Actors:** Dnipro, Kharkiv, Kyiv Russian, National Academy of Sciences, Odesa, Vitali Klitschko
- **Places:** Germany, Kyiv, Moscow, Russia, Ukraine, Zaporizhzhia
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T17:06 [Al Jazeera] **Russia strike sets National Academy of Sciences of Ukraine ablaze**
    > A Russian drone struck the National Academy of Sciences of Ukraine in central Kyiv, killing one person
  - 2026-09-28T17:37 [Al Jazeera] **Photos: Russian drone strikes pound civilian targets across Kyiv**
    > Russian drones have struck Ukraine’s National Academy of Sciences in the historic centre of Kyiv, as Moscow’s forces continue to pound the capital around the clock.

Ukrainian officials reported that at least seven people were killed and more than 80 wounded on Monday as Russian 

**Development B** `2026-09-29-live:russia-pounds-kyiv-after-academy`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T03:38 to 2026-09-29T03:38 UTC
- **Actors:** Academy, Academy of Sciences Footage
- **Places:** Kyiv, Russia, Ukraine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T03:38 [Al Jazeera] **Russia pounds Ukraine’s Kyiv after deadly strike on Academy of Sciences**
    > Footage of attack on Academy shows people leaning out of windows as bright flames engulf part of the historic building.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_attack_wave` | none | medium | none |

**Rationale:** B reports Russia continuing to pound Kyiv right after the Academy of Sciences strike in A, part of the same round-the-clock assault on the capital.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R070

**Development A** `2026-08-31:asean-big-tech-meta-payout`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T04:29 to 2026-08-31T04:29 UTC
- **Actors:** ASEAN, Big Tech, Facebook, Instagram, Meta, Meta Platforms
- **Places:** US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T04:29 [South China Morning Post] **Asean urged to take on Big Tech after Meta’s record payout**
    > Calls are growing for Asean to collectively crack down on Big Tech platforms that spread scams and harmful content, spurred on by Meta Platforms’ landmark US$18 billion US settlement last week.
Meta agreed on Wednesday to enact sweeping changes to Instagram and Facebook – includi

**Development B** `2026-08-31:ftc-amazon-ad-pricing-lawsuit`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-08-31T21:28 to 2026-08-31T21:28 UTC
- **Actors:** Amazon, US Federal Trade Commission
- **Places:** US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T21:28 [BBC World] **Amazon rigged $20bn worth of ad prices, US lawsuit alleges**
    > Amazon responded to the lawsuit, arguing the US Federal Trade Commission "misunderstands" their ad market.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Meta settlement prompting Asean calls and the FTC suit against Amazon are separate matters.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R071

**Development A** `2026-08-31:uae-intercepts-drone-denies-airbase-hit`

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

**Development B** `2026-08-31:why-greece-signed-israel-deal`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-31T14:57 to 2026-08-31T14:57 UTC
- **Actors:** none extracted
- **Places:** Greece, Iran, Israel, Turkiye, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T14:57 [Al Jazeera] **Why has Greece signed a $3.5bn missile deal with Israel?**
    > Analysts say Greece is concerned about threats posed by the US-Israel war on Iran and Turkiye&#039;s growing capabilities.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** UAE drone interception and analysis of Greece's missile deal are not linked.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R072

**Development A** `2026-08-31:china-warns-glacier-collapse-risk`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T06:05 to 2026-08-31T06:05 UTC
- **Actors:** CCTV, Ministry of Water Resources
- **Places:** China, Cuojian River, Nepal, Purepuqiang River, Tibet
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T06:05 [South China Morning Post] **China warns of ‘major risk’ of glacier collapse as Tibet-Nepal death toll nears 1,000**
    > China warned on Monday there was a “major risk” of further glacier collapses and landslides along the border with Nepal as the death toll from last week’s deadly mudslide rose to close to 1,000.
The Ministry of Water Resources said there was an ongoing threat along the Cuojian Ri

**Development B** `2026-08-31:nepal-rescue-tunnel-workers-toll-900`

- **Members:** 4 item(s)
- **Sources:** Al Jazeera, BBC World, South China Morning Post
- **Times:** 2026-08-31T06:05 to 2026-09-01T16:11 UTC
- **Actors:** BBC Major, CCTV, Himalayan, Nepal
- **Places:** China, Gyirong Port, India, Nepal
- **System Development:** D1
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T06:05 [South China Morning Post] **Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000**
    > Rescuers from China and Nepal continued searching landslide- and flood-affected areas on Monday while efforts to reopen roads to the heart of the disaster-hit area at Gyirong Port entered a “critical stage”.
The death toll in Nepal had risen to 903 as of 9am on Monday, with 4,247
  - 2026-08-31T07:34 [Al Jazeera] **Nepal races to rescue trapped workers, as flood death toll surpasses 900**
    > Nepal officials say rescuers focusing on reaching workers in hydropower project tunnels in flood-stricken region.
  - 2026-09-01T06:02 [BBC World] **The final minutes before floodwater crashed through Nepal-China border**
    > More than 100 Indians are missing at a vital Nepal-China trade crossing after devastating Himalayan floods.
  - 2026-09-01T16:11 [BBC World] **River water smashed into tunnel and chased me for 20 minutes, Nepal worker tells BBC**
    > Major efforts to rescue hydropower workers continue as Nepal's death toll exceeds 1,000.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_calamity_lifecycle` | none | high | none |

**Rationale:** Both are stages of the same China-Nepal border glacier/flood disaster: A is China's warning of further collapses as the toll nears 1,000, B the rescue operations and rising death toll.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R073

**Development A** `2026-10-03-live:s-1474`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-30T22:01 to 2026-09-30T22:01 UTC
- **Actors:** none extracted
- **Places:** Nepal
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 22:01 [BBC World] **Trekkers helicoptered off mountains as more deadly landslides hit Nepal**
    > A month after mass catastrophic flooding, around 30 people have died in landslides and heavy rain.

**Development B** `2026-10-03-live:s-1814`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-10-02T06:45 to 2026-10-02T06:45 UTC
- **Actors:** Malaysia Solidarity: Families in Hope, Manivannan Rethinam, Masfih
- **Places:** Kathmandu, Malaysia, Nepal
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-02 06:45 [South China Morning Post] **Missing Malaysian found safe in flood-ravaged Nepal after 37 days**
    > One of the Malaysians unaccounted for following the devastating floods in Nepal has been confirmed safe and has returned to Malaysia, according to the group representing Malaysians missing in Nepal.
Malaysia Solidarity: Families in Hope (Masfih) spokesman Manivannan Rethinam said

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | none |

**Rationale:** A reports new landslides from fresh heavy rain a month after the floods, while B is a missing person from the original August floods found safe; different hazard episodes.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R074

**Development A** `2026-09-27-live:sudan-blue-nile-motorcycles`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T04:56 to 2026-09-28T04:56 UTC
- **Actors:** none extracted
- **Places:** Blue Nile, Blue Nile State, Sudan
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T04:56 [Al Jazeera] **Sudanese army impounds dozens of motorcycles in Blue Nile curfew**
    > Dozens of motorcycles were impounded in Sudan’s Blue Nile State, after their riders were accused of flouting a curfew.

**Development B** `2026-09-27-live:ethiopia-accuses-sudan-egypt`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T11:00 to 2026-09-28T11:00 UTC
- **Actors:** RSF, Tigray
- **Places:** Egypt, Ethiopia, Sudan
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T11:00 [Al Jazeera] **Ethiopia accuses Sudan, Egypt of backing Tigray rebels as fighting rages**
    > Sudan army denies backing Tigray fighters, says rival paramilitary RSF receiving support from within Ethiopia.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** A Blue Nile curfew motorcycle seizure and Ethiopia's accusation over Tigray share only the region and actor Sudan.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R075

**Development A** `2026-08-31:nepal-foreign-rescue-teams-question`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T02:45 to 2026-08-31T02:45 UTC
- **Actors:** Nepalese
- **Places:** China, Kathmandu, Nepal
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T02:45 [South China Morning Post] **Nepal floods: could foreign rescue teams have been brought in earlier?**
    > The Nepalese government has appealed for rescue aid from other countries just two days after it reportedly refused help, as several hundred people are still believed to be trapped in hydropower tunnels and thousands remain missing following the catastrophic flash flooding at the 

**Development B** `2026-08-31:nepal-tunnel-traps-how-many-dead`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-31T10:17 to 2026-08-31T10:17 UTC
- **Actors:** none extracted
- **Places:** Nepal, Tibet
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T10:17 [Al Jazeera] **Nepal tunnel traps hinder flood rescue: How many are dead or missing?**
    > Flash floods on the Nepal-Tibet border have left nearly 5,000 people missing, many trapped in hydropower tunnels.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_calamity_lifecycle` | none | medium | none |

**Rationale:** Both concern the same Nepal-Tibet border flash flood: A Nepal's appeal for foreign rescue aid, B the rescue hindered in hydropower tunnels and the missing/dead count.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R076

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

**Development B** `2026-08-21:jewish-activists-protective-presence`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-22T12:51 to 2026-08-22T12:51 UTC
- **Actors:** Israel, Jewish
- **Places:** Israel, Occupied West Bank
- **System Development:** D5
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T12:51 [Al Jazeera] **Jewish activists push back against Israeli settlers**
    > Jewish activists provide a ‘protective presence’ to deter settler violence in parts of the Occupied West Bank.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Soldiers throwing belongings in Qusra and Jewish activists' protective presence share only the West Bank setting.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R077

**Development A** `2026-08-31:wheat-prices-black-sea-attacks`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-31T14:42 to 2026-08-31T14:42 UTC
- **Actors:** none extracted
- **Places:** Black Sea, Russia, Ukraine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T14:42 [Al Jazeera] **War and heat: Why are wheat prices soaring?**
    > Russia and Ukraine have stepped up attacks on their respective grain terminals in the Black Sea.

**Development B** `2026-08-31:kyiv-rail-workers-strike`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-01T10:30 to 2026-09-01T10:30 UTC
- **Actors:** Kyiv Ukrainian
- **Places:** Russia
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-01T10:30 [BBC World] **Russian attack hits rail workers in new deadly strikes on Kyiv**
    > Ukrainian officials say 20 people, including two children, were injured in the capital and the wider region.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** A is an explainer on wheat prices and grain terminal attacks; B is a separate Russian strike on Kyiv rail workers.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R078

**Development A** `2026-09-27-live:hk-bicycle-crackdown`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-27T09:53 to 2026-09-27T09:53 UTC
- **Actors:** Tseung Kwan O
- **Places:** Hong Kong, Tseung
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T09:53 [South China Morning Post] **7 teens swept up in police crackdown on bicycle-related offences in Tseung Kwan O**
    > Hong Kong police have clamped down on bicycle-related offences in Tseung Kwan O, with seven teenagers facing prosecution for allegedly failing to display bike lights at night and cycling on pavements.
In a social media post on Saturday, police in Tseung Kwan O district said offic

**Development B** `2026-09-27-live:hk-claw-machine-theft`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-27T13:58 to 2026-09-27T13:58 UTC
- **Actors:** Cheung, Tai Kok Tsui Road
- **Places:** Hong Kong
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T13:58 [South China Morning Post] **Hong Kong police hunt for man who stole HK$10,000 from claw machines using key**
    > Hong Kong police are searching for a man who used a key to steal about HK$10,000 (US$1,275) from four claw machines’ deposit boxes at a store on Sunday.
The force said that the store owner, a 46-year-old man surnamed Cheung, had filed a police report at around 11.10am after witne

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Bicycle offence crackdown and claw-machine theft are unrelated Hong Kong police matters.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R079

**Development A** `2026-09-29-live:iran-touts-hormuz-attacks`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T17:43 to 2026-09-28T17:43 UTC
- **Actors:** none extracted
- **Places:** Hormuz, Iran, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T17:43 [Al Jazeera] **Iran touts Hormuz attacks as oil flows increase despite tensions**
    > Mediators are trying to facilitate more talks, but Washington signals faith in its pressure tactics.

**Development B** `2026-09-29-live:us-iran-talks-deal-unlikely`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T08:15 to 2026-09-29T08:15 UTC
- **Actors:** none extracted
- **Places:** Iran, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T08:15 [Al Jazeera] **US-Iran talks continue, but ‘deal unlikely’ before midterm elections**
    > The US and Iran are talking through mediators, but there are major differences over what a deal should look like.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | none |

**Rationale:** Iran touting Hormuz attacks and an assessment that a US-Iran deal is unlikely share only the US-Iran pair; neither references the other.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R080

**Development A** `2026-09-29-live:hamas-commander-al-beik-killed`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T07:34 to 2026-09-29T07:34 UTC
- **Actors:** Hamas, Izz al-Din al-Beik
- **Places:** Gaza, Gaza City, Israel
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T07:34 [Al Jazeera] **Israeli forces kill Hamas commander Izz al-Din al-Beik in Gaza attack**
    > Head of Hamas&#039;s armed wing in northern Gaza killed in ⁠an Israeli strike on an apartment building in Gaza City.

**Development B** `2026-09-29-live:jalud-settler-attack`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T08:01 to 2026-09-29T08:01 UTC
- **Actors:** Al-Tubasi
- **Places:** Israel, Jalud, West Bank
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T08:01 [Al Jazeera] **Israeli settlers attack Jalud village in occupied West Bank, torch homes**
    > A group of settlers attacked two homes belonging to the Al-Tubasi family in northern West Bank village.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Gaza strike killing a Hamas commander and a settler attack on Jalud village are separate occurrences in the same conflict.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R081

**Development A** `2026-08-31:scmp-weekend-reads-asia`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T04:30 to 2026-08-31T04:30 UTC
- **Actors:** none extracted
- **Places:** Asia, China, India, Japan, Tokyo
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T04:30 [South China Morning Post] **China-Nepal floods, Japan to deploy fighter jets to India: 5 weekend reads you missed**
    > We have put together stories from our coverage last weekend to help you stay informed about news across Asia and beyond. If you would like to see more of our reporting, please consider subscribing.
1. What Japan’s coming fighter jet deployment to India means for China
Japan plans

**Development B** `2026-08-31:japan-hypersonic-plans-china`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T12:00 to 2026-08-31T12:00 UTC
- **Actors:** People's Liberation Army
- **Places:** Australia, China, Japan, Taiwan, Tokyo
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T12:00 [South China Morning Post] **Why Japan’s hypersonic and underwater weapon plans might worry China**
    > In its latest swipe at Tokyo’s military build-up, China singled out Japan’s plans to arm its submarine drones with long-range missiles and test hypersonic weapons in Australia.
Analysts say those moves could threaten People’s Liberation Army amphibious groups and surface combatan

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** A is a weekend-reads digest and B an analysis of Japanese weapons plans; no occurrence relation.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R082

**Development A** `2026-08-21:ebola-vaccine-trial-to-start`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-08-21T13:44 to 2026-08-21T13:44 UTC
- **Actors:** none extracted
- **Places:** DR Congo
- **System Development:** D3
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T13:44 [BBC World] **Ebola vaccine trial to start in DR Congo as warning issued over speed of infections**
    > About half of the 2,500 recorded deaths from Ebola happened in the last 20 days, the WHO says.

**Development B** `2026-08-21:ervebo-doses-arrive-drc`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-22T10:13 to 2026-08-22T11:15 UTC
- **Actors:** DRC
- **Places:** Congo, Kinshasa
- **System Development:** D3
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T10:13 [Al Jazeera] **More than 16,000 doses of Ervebo vaccine arrive in Ebola-hit DR Congo**
    > The doses are the first of 70,000 allocated for Kinshasa as experts warn of the virus&#039;s exponential spread.
  - 2026-08-22T11:15 [Al Jazeera] **Ebola continues to spread in the DRC as 16,000 vaccine doses arrive**
    > Health authorities are warning that ‘approximately one person has been dying from Ebola every thirty minutes’.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_calamity_lifecycle` | none | high | none |

**Rationale:** Both are stages of the same DR Congo Ebola outbreak: A the vaccine trial announcement and WHO warning, B the arrival of 16,000 Ervebo doses.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R083

**Development A** `2026-08-31:xi-bishkek-sco-eurasia-strategy`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T04:00 to 2026-08-31T04:00 UTC
- **Actors:** Eurasian, SCO, Shanghai Cooperation Organisation, Xi Jinping
- **Places:** Beijing, Bishkek, Central Asia, China, Kyrgyzstan, Middle East, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T04:00 [South China Morning Post] **Xi is in Bishkek for SCO summit. How does bloc fit China’s Eurasian strategy 25 years on?**
    > As Washington’s strategic focus shifts and energy and grain supply disruptions continue to unsettle the Middle East, Beijing’s expanding presence across Central Asia is expected to be in focus as Kyrgyzstan hosts the Shanghai Cooperation Organisation (SCO) summit this week.
Chine

**Development B** `2026-08-31:sco-summit-preview`

- **Members:** 3 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-31T04:18 to 2026-08-31T08:47 UTC
- **Actors:** Modi, SCO, Shanghai Cooperation Organisation, Trump, Vladimir Putin, Xi Jinping
- **Places:** China, Russia
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T04:18 [Al Jazeera] **Russia, China leaders to meet at Shanghai Cooperation Organisation summit**
    > The organisation is not officially anti-West, but Russian and Chinese leaders have used it to amplify their worldview.
  - 2026-08-31T08:47 [Al Jazeera] **Xi, Modi and Putin attend SCO summit: What’s on the agenda?**
    > The two-day summit aims to promote a vision of a multipolar world and mutual trade ties amid Trump&#039;s unilateralism.
  - 2026-08-31T08:47 [Al Jazeera] **Xi, Modi and Putin set to meet for SCO summit: What’s on the agenda?**
    > The two-day summit aims to promote a vision of a multipolar world and mutual trade ties amid Trump&#039;s unilateralism.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_visit_or_summit` | none | medium | none |

**Rationale:** Both concern the same SCO summit in Bishkek: A Xi's arrival for the summit, B Russian and Chinese leaders meeting at it.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R084

**Development A** `2026-08-31:scmp-weekend-reads-asia`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T04:30 to 2026-08-31T04:30 UTC
- **Actors:** none extracted
- **Places:** Asia, China, India, Japan, Tokyo
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T04:30 [South China Morning Post] **China-Nepal floods, Japan to deploy fighter jets to India: 5 weekend reads you missed**
    > We have put together stories from our coverage last weekend to help you stay informed about news across Asia and beyond. If you would like to see more of our reporting, please consider subscribing.
1. What Japan’s coming fighter jet deployment to India means for China
Japan plans

**Development B** `2026-08-31:china-warns-glacier-collapse-risk`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T06:05 to 2026-08-31T06:05 UTC
- **Actors:** CCTV, Ministry of Water Resources
- **Places:** China, Cuojian River, Nepal, Purepuqiang River, Tibet
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T06:05 [South China Morning Post] **China warns of ‘major risk’ of glacier collapse as Tibet-Nepal death toll nears 1,000**
    > China warned on Monday there was a “major risk” of further glacier collapses and landslides along the border with Nepal as the death toll from last week’s deadly mudslide rose to close to 1,000.
The Ministry of Water Resources said there was an ongoing threat along the Cuojian Ri

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** A is a weekend-reads digest that merely lists the floods; B is China's glacier-collapse warning.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R085

**Development A** `2026-09-25:us-china-summit-outcome`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-25T03:57 to 2026-09-25T03:57 UTC
- **Actors:** Donald Trump, Trump, Xi Jinping
- **Places:** China, Taiwan
- **System Development:** D3
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T03:57 [BBC World] **Xi got Trump's red carpet welcome - but not everything he wanted**
    > China wanted progress on trade, technology and Taiwan - but hasn't got as much as it would have hoped for.

**Development B** `2026-09-25:us-china-state-dinner`

- **Members:** 4 item(s)
- **Sources:** BBC World, South China Morning Post
- **Times:** 2026-09-25T05:48 to 2026-09-25T08:09 UTC
- **Actors:** Central Guard Bureau, Communist Party, Donald Trump, General Office, Peng Liyuan, People's Liberation Army, Richard Nixon, Schramsberg Blanc de Noirs, Sino-US, Trump, White House, Xi Jinping
- **Places:** Beijing, China, East Room, United States, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T05:48 [South China Morning Post] **From wine to ping-pong, Trump and Xi’s state dinner is heavy on historic symbolism**
    > When US President Donald Trump hosted Chinese President Xi Jinping in the East Room, every detail of the state dinner was steeped in symbolism, with sparkling wine served as a nod to a pivotal moment in Sino-US relations and references to “ping-pong diplomacy”.
The meal opened wi
  - 2026-09-25T07:00 [South China Morning Post] **Xi-Trump dinner puts US tech titans in spotlight – what does it mean for China ties?**
    > If the American guests seated at the head table with President Xi Jinping and US President Donald Trump at Thursday’s White House state dinner were any indication, Washington now views its relationship with Beijing largely through the prism of technology.
Analysts said the seatin
  - 2026-09-25T07:19 [South China Morning Post] **Xi’s security chief among cohort of rising officials at White House banquet**
    > Zhou Hongxu, the official who oversees President Xi Jinping’s security, made an appearance at the White House state banquet on Thursday night, alongside a cohort of other rising Chinese officials.
The banquet’s guest list described the 55-year-old People’s Liberation Army (PLA) m
  - 2026-09-25T08:09 [BBC World] **Trump and Xi exchange warm words at state dinner but little progress on key issues**
    > Despite diplomatic niceties and gifts, little was shared on substantial issues separating the leaders.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | commentary |

**Rationale:** A is a BBC assessment of what Xi did and did not obtain from the visit, commentary rather than a distinct occurrence related to B's state dinner.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R086

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

**Development B** `2026-09-29-live:judge-blocks-antiterror-grant-conditions`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-28T23:20 to 2026-09-28T23:20 UTC
- **Actors:** Amir Ali, Donald Trump, Republican, Trump, US Congress
- **Places:** US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T23:20 [South China Morning Post] **Judge blocks Trump from tying anti-terrorism grants to election changes**
    > A US judge blocked the Trump administration on Monday from conditioning counterterrorism funds to state and local ‌governments on changes to election administration.
The decision by Washington-based US District Judge Amir Ali marks the latest defeat for US President Donald Trump 

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** A is an opinion piece on Trump rejecting Iran's offer; B is a court ruling on anti-terrorism grants; unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R087

**Development A** `2026-09-27-live:trump-downplays-taiwan-talk`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-27T09:43 to 2026-09-27T09:43 UTC
- **Actors:** Donald Trump, Trump, Xi Jinping
- **Places:** China, Taiwan, US, Washington
- **System Development:** D14
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T09:43 [South China Morning Post] **‘Right now, it’s fine’: Trump brushes off questions about summit talk on Taiwan**
    > US President Donald Trump has sought to play down exchanges with his Chinese counterpart Xi Jinping on Taiwan, saying on Saturday that they touched on the subject only briefly.
“We didn’t talk about it too much. Right now, it’s fine. It’s just moving along,” Trump said. “We didn’

**Development B** `2026-09-27-live:summit-trade-deliverables`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera, South China Morning Post
- **Times:** 2026-09-28T06:24 to 2026-09-28T09:16 UTC
- **Actors:** Trump, White House, Xi Jinping
- **Places:** Beijing, China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T06:24 [Al Jazeera] **US, China list goods recommended for tariff cuts following Trump-Xi summit**
    > Washington and Beijing announce details of agreement to reduce tariffs on $60bn of trade.
  - 2026-09-28T09:16 [South China Morning Post] **China resuming US coal imports among thin list of summit outcomes**
    > China agreed to import at least 10 million tonnes of US coal in each of the next two years, marking one of the few concrete results from President Xi Jinping’s state visit to the United States.
The country will also lower tariffs on 1,619 US products, including coal, under a deal

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | none |

**Rationale:** A is Trump's later remark on Taiwan talk and B the publication of tariff-cut lists; both follow the summit but neither responds to or continues the other.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R088

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

**Development B** `2026-09-25:israel-palestine-treatment-at-un`

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

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | commentary |

**Rationale:** B is an analysis piece on the contrasting treatment of Israel and Palestine at the UN, commentary on Netanyahu's UNGA appearance rather than an occurrence linked to A's protests.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R089

**Development A** `2026-09-30-multilingual:sx-25`

- **Members:** 1 item(s)
- **Sources:** White House
- **Times:** 2026-09-29T14:50 to 2026-09-29T14:50 UTC
- **Actors:** All Presidential Actions, Briefings & Statements, Nominations & Appointments, Streamlining Access to Government Services
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 14:50 [White House] **Streamlining Access to Government Services Through America.gov**
    > STREAMLINING ACCESS TO GOVERNMENT SERVICES THROUGH AMERICA.GOV				
			
			
					
	
		
		
			Search
					
						
		
			
				
					Select Category				
				
																		
								All News							
																								
								Briefings &amp; Statements							
																

**Development B** `2026-09-30-multilingual:sx-24`

- **Members:** 1 item(s)
- **Sources:** White House
- **Times:** 2026-09-29T19:07 to 2026-09-29T19:07 UTC
- **Actors:** All Presidential Actions, Briefings & Statements, Nominations & Appointments
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 19:07 [White House] **First Lady Melania Trump Announces 2026 Fall Garden Tours**
    > oFFICE OF THE fIRST lADY				
			
							
					First Lady Melania Trump Announces 2026 Fall Garden Tours				
			
			
					
	
		
		
			Search
					
						
		
			
				
					Select Category				
				
																		
								All News							
																								
								Briefings

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** America.gov launch and the First Lady's garden tours are unrelated White House releases.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R090

**Development A** `2026-09-27-live:trump-on-fairford-suspects`

- **Members:** 1 item(s)
- **Sources:** Defense News
- **Times:** 2026-09-27T16:19 to 2026-09-27T16:19 UTC
- **Actors:** CIRCUMSTANCES"We, Donald Trump, RAF Fairford, Trump, UK, Vicki Evans
- **Places:** England, Iran, UK, US
- **System Development:** D7
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T16:19 [Defense News] **Terror suspects wanted to do ‘big damage’ to air base used by US, Trump says**
    > British police on Sunday arrested five men near an air base used by U.S. forces on suspicion of explosive and terrorism offenses after a tip that three vans were heading to the military airfield, which has been used to strike Iran.U.S. President Donald Trump said the suspects had

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
| `NO_RELATION` | none | high | none |

**Rationale:** UK terror arrests near an air base and an explainer on Trump rejecting Iran's peace proposal share no stated link.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R091

**Development A** `2026-08-21:un-ebola-growing-faster-2500-deaths`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-21T13:30 to 2026-08-21T13:30 UTC
- **Actors:** DRC, United Nations
- **Places:** Congo, DR
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T13:30 [Al Jazeera] **Ebola outbreak ‘growing faster, ⁠⁠wider’ as DRC death toll passes 2,500: UN**
    > Epidemic remains out of control amid DR Congo conflict, funding shortages and attacks on health workers and facilities

**Development B** `2026-08-21:ebola-vaccine-trial-to-start`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-08-21T13:44 to 2026-08-21T13:44 UTC
- **Actors:** none extracted
- **Places:** DR Congo
- **System Development:** D3
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T13:44 [BBC World] **Ebola vaccine trial to start in DR Congo as warning issued over speed of infections**
    > About half of the 2,500 recorded deaths from Ebola happened in the last 20 days, the WHO says.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_calamity_lifecycle` | none | medium | none |

**Rationale:** Both are about the same DRC Ebola outbreak passing 2,500 deaths: A the UN warning of faster spread, B the vaccine trial start (the warning overlaps).

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R092

**Development A** `2026-10-03-live:s-1235`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-29T22:00 to 2026-09-29T22:00 UTC
- **Actors:** Peng Liyuan, White House, Xi Jinping
- **Places:** Beijing, China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 22:00 [South China Morning Post] **Xi-Trump summit drew Chinese CEOs. So why couldn’t they get a seat at the table?**
    > As American billionaires gathered at the White House to honour Chinese President Xi Jinping and his wife Peng Liyuan last Thursday, a group of Chinese business leaders spent the evening on the sidelines.
They had travelled to the US capital to join the state dinner. But their inv

**Development B** `2026-10-03-live:D15`

- **Members:** 4 item(s)
- **Sources:** Al Jazeera, Breaking Defense, Defense News, South China Morning Post
- **Times:** 2026-10-02T08:26 to 2026-10-02T17:20 UTC
- **Actors:** Chihhang Air Base, Donald Trump, Taipai, Taiwan, Trump, US, Xi Jinping
- **Places:** Beijing, China, F-16V Block, Taipei, Taitung, Taiwan, US
- **System Development:** D15
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-02 08:26 [Al Jazeera] **US delivers F-16V fighter jets to Taiwan as island eyes threat from China**
    > Amid threats from China, Taipai is growing concerned about the Trump administration&#039;s commitment to arming the island.
  - 2026-10-02 10:00 [South China Morning Post] **Taiwan hails F-16V delivery as sign US support holds after Xi-Trump summit**
    > Taiwan has hailed the much-delayed arrival of two F-16V fighter jets as a demonstration of continuing US military support, despite the summit between President Xi Jinping and US President Donald Trump.
The two single-seat aircraft, which reached Chihhang Air Base in the eastern c
  - 2026-10-02 14:15 [Defense News] **Taiwan’s first two F-16V fighter jets arrive to bolster defenses against China**
    > TAITUNG, Taiwan — The first two of a batch of 66 new F-16V Block 70 fighter jets ordered in 2019 arrived in Taiwan on Friday after months of delays, helping to strengthen an air force that has to scramble almost daily to shadow China’s military.Taiwan faces a rising military thre
  - 2026-10-02 17:20 [Breaking Defense] **After yearslong delay, Taiwan receives first pair of new F-16s**
    > The two jets landed at an airbase in eastern Taiwan on Friday.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Chinese CEOs left out of the state dinner and F-16V delivery to Taiwan share only the US-China context.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R093

**Development A** `2026-08-31:hk-child-social-media-opinion`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T01:30 to 2026-08-31T01:30 UTC
- **Actors:** none extracted
- **Places:** Hong Kong
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T01:30 [South China Morning Post] **Don’t leave Hong Kong parents to their own devices on child social media use**
    > Hong Kong, a city of overachievers, especially when it comes to the young, is also filled with children who take to social media early. Almost 35 per cent of kindergarten pupils log at least one hour of recreational screen time daily. By the junior forms, 60 per cent exceed the i

**Development B** `2026-08-31:singapore-teen-social-media-limits`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T09:27 to 2026-08-31T09:27 UTC
- **Actors:** Digital Development and Information, Josephine Teo, Teo
- **Places:** Singapore
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T09:27 [South China Morning Post] **Singapore may require social media firms to set daily time limits for teens**
    > Singapore plans to introduce legislation early next year requiring social media platforms to roll out stronger safeguards for teens, including possibly setting a daily time limit, Minister for Digital Development and Information Josephine Teo has said.
If a platform could not or 

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** A is an opinion piece on Hong Kong child social media use; B is a Singapore legislative plan; same topic only.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R094

**Development A** `2026-09-29-live:india-releases-vandyke-ukrainians`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T19:02 to 2026-09-28T19:02 UTC
- **Actors:** Matthew VanDyke
- **Places:** India, US, Ukraine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T19:02 [Al Jazeera] **American and six Ukrainians released by India after six months in jail**
    > Matthew VanDyke and six Ukrainians were accused of smuggling weapons and drones to armed ethnic groups fighting India.

**Development B** `2026-09-29-live:us-revokes-latam-officials-visas`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-28T20:50 to 2026-09-28T20:50 UTC
- **Actors:** Donald Trump, Latin American, Marco Rubio, State, Trump
- **Places:** Bolivia, Colombia, Ecuador, Peru, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T20:50 [South China Morning Post] **US revokes visas from Latin American officials and families over accusations of corruption**
    > The Trump administration is revoking the visas of 27 Latin American officials, former officials and their families, including Bolivia’s attorney general, over accusations of corruption.
The officials and their families come from Bolivia, Colombia, Ecuador and Peru - all nations w

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** India releasing VanDyke and US revoking Latin American officials' visas are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R095

**Development A** `2026-08-21:trump-eases-beef-tariffs`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-21T12:05 to 2026-08-21T12:05 UTC
- **Actors:** Donald Trump
- **Places:** US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T12:05 [South China Morning Post] **Trump eases tariffs on ground beef imports for 90 days**
    > President Donald Trump announced on Friday that the United States would temporarily allow a greater volume of foreign beef imports, in his latest bid to lower costs for American consumers as midterm elections approach.
The US cattle herd has shrunk to its lowest level since the 1

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
| `NO_RELATION` | none | high | none |

**Rationale:** Canada's retaliatory tariffs respond to fresh US tariffs after talks collapsed, not to A's beef tariff easing.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R096

**Development A** `2026-09-29-live:bangkok-jet-skier-arrest`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T13:00 to 2026-09-28T13:00 UTC
- **Actors:** none extracted
- **Places:** Bangkok, Thailand
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T13:00 [Al Jazeera] **Thai police arrest jet skier after joyride through flooded Bangkok streets**
    > Thai police arrest jet skier after joyride through flooded Bangkok streets

**Development B** `2026-09-29-live:hk-bangkok-flights-delayed`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-28T13:11 to 2026-09-28T13:11 UTC
- **Actors:** Southeast Asian
- **Places:** Bangkok, Hong Kong, Hongkongers, Thailand
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T13:11 [South China Morning Post] **At least 21 Hong Kong-Bangkok flights delayed amid flooding in Thai capital**
    > At least 21 flights connecting Hong Kong and Bangkok were disrupted on Sunday and Monday, with passengers on one service leaving the Thai capital facing a nearly 24-hour delay after the Southeast Asian city was hit by its worst flood in 15 years.
Heavy rainfall lashed Bangkok – a

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | low | none |

**Rationale:** A jet skier's arrest during the Bangkok flood is a side incident, not a stage of the calamity like B's flight disruptions; shared flood context only.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R097

**Development A** `2026-09-29-live:opinion-us-china-ai-control`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-28T21:30 to 2026-09-28T21:30 UTC
- **Actors:** AI, Donald Trump, Trump, Xi Jinping
- **Places:** China, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T21:30 [South China Morning Post] **In the US-China AI race, the real fight is keeping humans in control**
    > The US-China AI competition faces a dilemma. Both countries see artificial intelligence as a source of economic, scientific and strategic power, so neither has much incentive to slow down. Yet the more capable and autonomous AI becomes, the more important the question of human co

**Development B** `2026-09-29-live:us-soybeans-excluded-tariff-cuts`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-28T22:48 to 2026-09-28T22:48 UTC
- **Actors:** Board of Trade, Donald Trump, Xi Jinping
- **Places:** Beijing, China, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T22:48 [South China Morning Post] **‘Missed opportunity’: US soybean farmers question exclusion from China tariff cuts**
    > US soybean farmers have described the exclusion of US soybeans from China’s import list under the newly announced Board of Trade mechanism as a “missed opportunity”, even as Beijing ramped up purchases of the crop ahead of last week’s summit between Chinese President Xi Jinping a

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** A is an opinion piece on AI control; B is soybean farmers' reaction to tariff cuts; unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R098

**Development A** `2026-09-30-multilingual:sx-405`

- **Members:** 1 item(s)
- **Sources:** UN News
- **Times:** 2026-09-28T12:00 to 2026-09-28T12:00 UTC
- **Actors:** DPR Korea, DPRK, State, UN General Assembly, United Nations
- **Places:** Korean Peninsula
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28 12:00 [UN News] **DPR Korea tells UN its nuclear status is ‘irreversible’, rejects outside pressure**
    > The Democratic People’s Republic of Korea (DPRK) told the UN General Assembly on Monday that its status as a nuclear-armed State was irreversible, arguing that its military capabilities were necessary to safeguard the country’s sovereignty and maintain peace on the Korean Peninsu

**Development B** `2026-09-30-multilingual:sx-424`

- **Members:** 2 item(s)
- **Sources:** UN Press
- **Times:** 2026-09-28T23:02 to 2026-09-29T16:41 UTC
- **Actors:** António Guterres, UN General Assembly, United Nations
- **Places:** Middle East, New York
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28 23:02 [UN Press] **International Security Rapidly Deteriorates; General Assembly Urges Nations to Address Weaker Global Arms Treaties and Heightened Nuclear Risks**
    > With nuclear arsenals expanding and arms control safeguards eroding worldwide, speakers today warned of mounting nuclear risks, from tensions in the Middle East and emerging technologies to the enduring consequences of nuclear testing, as the General Assembly held a high-level me
  - 2026-09-29 16:41 [UN Press] **At ‘Most Dangerous Nuclear Moment’ Since Cold War Ended, Secretary-General Observance Message Urges Changing Course, Replacing Threats with Dialogue**
    > Following are UN Secretary-General António Guterres’ remarks at the plenary meeting of the International Day for the Total Elimination of Nuclear Weapons, in New York today:

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `AMBIGUOUS` | none | low | none |

**Rationale:** DPRK's UNGA statement and the nuclear-elimination high-level meeting fall on the same day; whether DPRK spoke at that meeting or in the general debate would settle it.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R099

**Development A** `2026-10-03-live:s-1796`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-10-02T01:30 to 2026-10-02T01:30 UTC
- **Actors:** Algernon Yau Ying, Commerce and Economic Development
- **Places:** Britain, Hong Kong, Singapore, UK, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-02 01:30 [South China Morning Post] **‘Money is money’: US, UK firms still coming to Hong Kong, commerce chief says**
    > Companies from the United States, Britain and Singapore have been among the leading sources of inbound foreign capital in Hong Kong so far this year, the city’s commerce minister has said, insisting that “money is money” despite geopolitical instability.
In an exclusive, wide-ran

**Development B** `2026-10-03-live:s-1842`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-10-02T09:05 to 2026-10-02T09:05 UTC
- **Actors:** Bloomberg, European Union, Medcaptain Medical Technology, Shein
- **Places:** China, Hong Kong
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-02 09:05 [South China Morning Post] **Hong Kong IPOs falter, China aids homebuyers, EU trade talks**
    > Hong Kong stock debuts are losing steam as a deluge of initial public offerings (IPOs) overwhelms investor appetite.
Seven of September’s 12 IPOs fell on the first day of trading, raising the third-quarter total to 15 flops out of 31, based on Bloomberg data. By contrast, there w

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** A commerce chief interview on inbound capital and a markets newsletter on IPOs share only the Hong Kong economy topic.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R100

**Development A** `2026-09-29-live:uae-confirms-netanyahu-visit`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T19:42 to 2026-09-28T19:42 UTC
- **Actors:** Benjamin Netanyahu, Israel, Knesset, UAE
- **Places:** Abu Dhabi, Israel
- **System Development:** D8
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T19:42 [Al Jazeera] **UAE confirms Netanyahu visit to Abu Dhabi**
    > The visit takes place as the Israeli prime minister battles domestic turmoil ahead of October&#039;s Knesset elections

**Development B** `2026-09-29-live:shin-bet-complaint-uae-report`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-28T22:25 to 2026-09-28T22:25 UTC
- **Actors:** Benjamin Netanyahu, Channel 12, Israel, Shin Bet, UAE
- **Places:** Israel, UAE
- **System Development:** D8
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T22:25 [South China Morning Post] **Israel security agency files complaint over TV report that Netanyahu visited UAE**
    > Israel’s domestic security service filed a complaint against a television channel that reported Prime Minister Benjamin Netanyahu visited the UAE, his office said on Monday, the government’s first acknowledgement of the trip despite not naming the destination.
“This evening the S

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_visit_or_summit` | none | medium | none |

**Rationale:** Both concern Netanyahu's same visit to the UAE: A the UAE confirmation, B Shin Bet's complaint over a TV report of that trip.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R101

**Development A** `2026-09-30-multilingual:D11`

- **Members:** 3 item(s)
- **Sources:** Breaking Defense, Defense News, Defense.gov
- **Times:** 2026-09-29T21:26 to 2026-09-29T22:20 UTC
- **Actors:** Boeing, Michael P. Duffey, Northrop Grumman, U.S. Navy, U.S. Navy Award Contract, US Department of Defense, defense for Acquisition
- **Places:** U.S.
- **System Development:** D11
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 21:26 [Breaking Defense] **Boeing wins Navy next-gen fighter F/A-XX competition**
    > Boeing&#8217;s win gives it a monopoly on American sixth-gen fighters, following its 2025 selection to build the F-47.
  - 2026-09-29 21:30 [Defense.gov] **Department of War and U.S. Navy Award Contract for F/A-XX Program**
    > The War Department announced a contract awarded by the U.S. Navy to Boeing for the Sixth-Generation F/A-XX Strike Fighter under the Next Generation Air Dominance program.
  - 2026-09-29 22:20 [Defense News] **US Navy selects Boeing to build next-generation F/A-XX fighter**
    > Boeing has been selected to build the Navy’s sixth-generation carrier-based strike fighter, dubbed F/A-XX, icing out what was considered to be its biggest competitor in late-stage negotiations, Northrop Grumman. Inked at $20 billion for the full-scale development phase, the contr

**Development B** `2026-09-30-multilingual:sx-486`

- **Members:** 1 item(s)
- **Sources:** Defense News
- **Times:** 2026-09-30T00:03 to 2026-09-30T00:03 UTC
- **Actors:** DPRK, Elmet, Elmet Group, US Department of Defense
- **Places:** China, Iran, Russia, U.S.
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 00:03 [Defense News] **Why the Pentagon just dropped $450M on tungsten mining**
    > The Defense Department announced this month a $450 million investment in The Elmet Group to strengthen the U.S. supply chain for tungsten, a critical mineral used for manufacturing military weapons ranging from bullets to missiles. The investment comes as a federal procurement ru

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** F/A-XX award to Boeing and the tungsten mining investment are separate Pentagon decisions.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R102

**Development A** `2026-08-21:us-economic-isolation-strategy-analysis`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-21T13:59 to 2026-08-21T13:59 UTC
- **Actors:** none extracted
- **Places:** Iran, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T13:59 [Al Jazeera] **War on Iran: The US could focus on economically isolating Iran**
    > The US Treasury Secretary, has indicated a change in US strategy towards Iran, focusing on economic isolation.

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
| `NO_RELATION` | none | medium | commentary |

**Rationale:** A is analysis of a US Treasury strategy shift; B Iran condemns new US sanctions and a Trump threat without naming A's statement.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R103

**Development A** `2026-09-29-live:fifa-infantino-funding`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T07:10 to 2026-09-29T07:10 UTC
- **Actors:** FIFA, Infantino
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T07:10 [Al Jazeera] **FIFA could disburse millions to members as Infantino seeks re-election**
    > FIFA president Infantino is open to providing &#039;greatest level of additional funding&#039; to associations amid opposition.

**Development B** `2026-09-29-live:fifa-accuses-uefa`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T11:12 to 2026-09-29T11:12 UTC
- **Actors:** European, FIFA, FIFA-UEFA, Infantino, UEFA
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T11:12 [Al Jazeera] **In FIFA-UEFA tussle, European body accused of ‘misinformation campaign’**
    > FIFA accuses UEFA of attempting to influence its presidential election, in which Infantino is seeking a fourth term.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | none |

**Rationale:** Infantino's funding offer and FIFA accusing UEFA of misinformation share the FIFA election topic but neither responds to the other.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R104

**Development A** `2026-09-27-live:hk-claw-machine-theft`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-27T13:58 to 2026-09-27T13:58 UTC
- **Actors:** Cheung, Tai Kok Tsui Road
- **Places:** Hong Kong
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T13:58 [South China Morning Post] **Hong Kong police hunt for man who stole HK$10,000 from claw machines using key**
    > Hong Kong police are searching for a man who used a key to steal about HK$10,000 (US$1,275) from four claw machines’ deposit boxes at a store on Sunday.
The force said that the store owner, a 46-year-old man surnamed Cheung, had filed a police report at around 11.10am after witne

**Development B** `2026-09-27-live:hk-gym-hidden-cameras`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-27T14:58 to 2026-09-27T14:58 UTC
- **Actors:** 24/7 Fitness, Sha Tin
- **Places:** Hong Kong, Lek Yuen Street
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T14:58 [South China Morning Post] **Police arrest man, 34, over hidden cameras found in Hong Kong gym changing rooms**
    > Hong Kong police have arrested a 34-year-old gym user in connection with the installation of three suspected pinhole cameras found in changing rooms at a 24/7 Fitness branch in Sha Tin.
The arrest on Sunday came a day after police launched an investigation into the suspected voye

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Claw-machine theft and gym hidden cameras arrest are unrelated police cases.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R105

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

**Development B** `2026-09-25:unga-day-three-roundup`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-25T06:28 to 2026-09-25T06:28 UTC
- **Actors:** Benjamin Netanyahu, UN General Assembly
- **Places:** Kuwait, Yemen
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T06:28 [Al Jazeera] **Converging crises, chaos and walkouts dominate UNGA Day Three**
    > Dozens of delegates walked out on Netanyahu, Yemen’s government pleaded for help, and Kuwait riled against threats.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | commentary |

**Rationale:** A is an analysis of contrasting treatment at the UN; B is a UNGA Day Three roundup; commentary around the same address.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R106

**Development A** `2026-09-27-live:south-africa-two-mass-shootings`

- **Members:** 3 item(s)
- **Sources:** Al Jazeera, BBC World, South China Morning Post
- **Times:** 2026-09-27T12:07 to 2026-09-27T16:58 UTC
- **Actors:** none extracted
- **Places:** Cape Town, Johannesburg, South Africa
- **System Development:** D4
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T12:07 [South China Morning Post] **South African police probe mining feud shooting, 27 dead as elections near**
    > South African police on Sunday were hunting the perpetrators of two separate shootings that killed 27 people within hours of each other, in stark reminders of the country’s problem with gun violence.
Officials were still establishing the motives for the shootings near Johannesbur
  - 2026-09-27T14:09 [BBC World] **Two mass shootings in South Africa leave 27 dead**
    > The two attacks hours apart come as the country struggles to stop high levels of gang-related armed violence.
  - 2026-09-27T16:58 [Al Jazeera] **Dozens killed in two mass shootings in South Africa**
    > At least 27 people have been killed in two mass shootings across South Africa.

**Development B** `2026-09-27-live:detroit-strip-club-shooting`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera, South China Morning Post
- **Times:** 2026-09-27T18:44 to 2026-09-27T20:44 UTC
- **Actors:** Todd Bettison
- **Places:** Detroit, Michigan, US
- **System Development:** D10
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T18:44 [South China Morning Post] **3 people killed and 4 injured in shooting at Michigan strip club, police say**
    > Three people were killed and four others were injured when an argument led to gunfire at an after-hours strip club on Sunday morning in Detroit, officials said.
Police responding to the 7.21am shooting on a largely residential street found three men who had been fatally shot, Det
  - 2026-09-27T20:44 [Al Jazeera] **Three killed, four injured in shooting at Detroit, Michigan, strip club**
    > Police say the US shooting followed an altercation at an after-hours venue, and four people are in hospital.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** South African mass shootings and a Detroit strip club shooting are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R107

**Development A** `2026-08-21:settlers-burn-hebron-quarry-machinery`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-21T16:00 to 2026-08-21T16:00 UTC
- **Actors:** none extracted
- **Places:** Hebron, Israel, Wadi Al-Rakheem, West Bank
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T16:00 [Al Jazeera] **Israeli settlers set fire to heavy machinery at West Bank quarry**
    > Israeli settlers entered a stone quarry in Wadi Al-Rakheem near Hebron overnight and set fire to heavy machinery

**Development B** `2026-08-21:settlement-expansion-analysis`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-08-21T19:31 to 2026-08-21T19:31 UTC
- **Actors:** none extracted
- **Places:** Israel, Palestine, West Bank
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T19:31 [BBC World] **How Israel is expanding settlements in drive to reshape West Bank**
    > There has been a significant expansion of building and road construction on Palestinian land occupied by Israel in recent years.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** A is settler arson at a quarry; B is an analysis of settlement expansion; same topic only.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R108

**Development A** `2026-09-30-multilingual:sx-412`

- **Members:** 1 item(s)
- **Sources:** UN News
- **Times:** 2026-09-28T12:00 to 2026-09-28T12:00 UTC
- **Actors:** none extracted
- **Places:** Congo, Democratic Republic of the Congo
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28 12:00 [UN News] **DR Congo Ebola emergency: Calls grow for urgent humanitarian access**
    > Aid teams&nbsp;trying to keep deadly Ebola disease from spreading in the Democratic Republic of the Congo (DRC) are increasingly concerned about ongoing fighting and violence that has forced thousands of people to flee a displacement camp in the vast, resource-rich east of the co

**Development B** `2026-09-30-multilingual:sx-401`

- **Members:** 1 item(s)
- **Sources:** UN News
- **Times:** 2026-09-29T12:00 to 2026-09-29T12:00 UTC
- **Actors:** UN World Health Organization
- **Places:** Democratic Republic of the Congo
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 12:00 [UN News] **DRC: Early access to care and oxygen decisive for Ebola patients’ survival – WHO**
    > In the Democratic Republic of the Congo (DRC), health workers fighting the country’s largest-ever Ebola outbreak are struggling to overcome critical challenges to patient care, the UN World Health Organization (WHO) warned on Tuesday.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_calamity_lifecycle` | none | medium | none |

**Rationale:** Both are response-stage statements within the same DRC Ebola outbreak: calls for humanitarian access and the WHO warning on patient-care challenges.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R109

**Development A** `2026-08-31:iran-war-economic-winners-losers`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-31T12:01 to 2026-08-31T12:01 UTC
- **Actors:** none extracted
- **Places:** Iran, Israel, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T12:01 [Al Jazeera] **Who are the economic winners and losers of the US-Israel war on Iran?**
    > Airlines and automakers have taken a hit, while banks and energy firms have raked in big profits.

**Development B** `2026-08-31:can-iran-mine-hormuz-with-rockets`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-31T13:00 to 2026-08-31T13:00 UTC
- **Actors:** none extracted
- **Places:** Iran, Strait of Hormuz, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T13:00 [Al Jazeera] **Can Iran use rockets to mine the Strait of Hormuz, as US claims?**
    > Analysts say it&#039;s implausible but Iran is well-versed in adapting conventional weapons to suit its needs.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** Both are analysis pieces on the Iran war (economic winners/losers, rocket mining claim).

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R110

**Development A** `2026-10-03-live:s-1374`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-30T12:43 to 2026-09-30T12:43 UTC
- **Actors:** AQI, Air Quality, IQAir, Sumatra
- **Places:** Borneo, Indonesia, Kuala Lumpur, Malaysia, Singapore, Switzerland
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 12:43 [South China Morning Post] **Kuala Lumpur is world’s most polluted city due to haze, Singapore third, index shows**
    > Malaysia’s capital topped a global pollution ranking on Wednesday and nearby Singapore came in third, with smoke from wildfires in neighbouring Indonesia blamed for the unhealthy conditions.
A milky haze has shrouded the cities for more than a month as smoke drifted from fires on

**Development B** `2026-10-03-live:s-1814`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-10-02T06:45 to 2026-10-02T06:45 UTC
- **Actors:** Malaysia Solidarity: Families in Hope, Manivannan Rethinam, Masfih
- **Places:** Kathmandu, Malaysia, Nepal
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-02 06:45 [South China Morning Post] **Missing Malaysian found safe in flood-ravaged Nepal after 37 days**
    > One of the Malaysians unaccounted for following the devastating floods in Nepal has been confirmed safe and has returned to Malaysia, according to the group representing Malaysians missing in Nepal.
Malaysia Solidarity: Families in Hope (Masfih) spokesman Manivannan Rethinam said

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Kuala Lumpur haze ranking and a missing Malaysian found in Nepal share only Malaysia.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R111

**Development A** `2026-09-27-live:israeli-opposition-unites`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T16:53 to 2026-09-27T16:53 UTC
- **Actors:** Benjamin Netanyahu, Jerusalem Daily
- **Places:** Israel
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T16:53 [Al Jazeera] **Jerusalem Daily: Israeli opposition leaders unite to drive out Netanyahu**
    > Jerusalem Daily: Israeli opposition leaders unite to drive out Netanyahu

**Development B** `2026-09-27-live:west-bank-checkpoints-feature`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T19:04 to 2026-09-27T19:04 UTC
- **Actors:** none extracted
- **Places:** Israel, Palestine, West Bank
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T19:04 [Al Jazeera] **Stuck between Israeli military checkpoints**
    > Israeli road closures have become a part of daily life for Palestinians in the occupied West Bank.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Israeli opposition uniting and West Bank checkpoints are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R112

**Development A** `2026-09-30-multilingual:sx-513`

- **Members:** 1 item(s)
- **Sources:** Breaking Defense
- **Times:** 2026-09-29T14:22 to 2026-09-29T14:22 UTC
- **Actors:** Air Force, NORTHCOM
- **Places:** China
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 14:22 [Breaking Defense] **Drone-hunting on the border, plus turmoil at an Air Force think tank**
    > NORTHCOM is testing ways to counter drone incursions, while an Air Force institute focused on China faces questions about its future.

**Development B** `2026-09-30-multilingual:sx-91`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-30T04:21 to 2026-09-30T04:21 UTC
- **Actors:** Xi Jinping
- **Places:** China, South Korea
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 04:21 [BBC World] **Restaurant named after Xi Jinping attacked by Chinese nationals in South Korea**
    > The owner said he chose the name because he wanted to run the "best Chinese restaurant" in South Korea.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** NORTHCOM drone testing and an attack on a Xi-named restaurant in Korea are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R113

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

**Development B** `2026-09-29-live:iran-singer-lashes-upheld`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-28T17:15 to 2026-09-28T17:15 UTC
- **Actors:** Parastoo Ahmadi
- **Places:** Iran
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T17:15 [BBC World] **Iran court upholds lashes sentence for singer who performed without hijab**
    > Parastoo Ahmadi was convicted of "offending public decency" after singing while wearing a sleeveless dress during a livestreamed concert.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Iran denying an airbase attack link and an Iranian court upholding a singer's lashes share only Iran.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R114

**Development A** `2026-09-30-multilingual:sx-412`

- **Members:** 1 item(s)
- **Sources:** UN News
- **Times:** 2026-09-28T12:00 to 2026-09-28T12:00 UTC
- **Actors:** none extracted
- **Places:** Congo, Democratic Republic of the Congo
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28 12:00 [UN News] **DR Congo Ebola emergency: Calls grow for urgent humanitarian access**
    > Aid teams&nbsp;trying to keep deadly Ebola disease from spreading in the Democratic Republic of the Congo (DRC) are increasingly concerned about ongoing fighting and violence that has forced thousands of people to flee a displacement camp in the vast, resource-rich east of the co

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

**Rationale:** Ebola humanitarian access calls and a Security Council meeting on DRC conflict/MONUSCO share the DRC crisis but no stated link.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R115

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
| `NO_RELATION` | none | medium | commentary |

**Rationale:** B is an analysis of lingering Hormuz tensions after Trump's rejection, commentary on the same rejection reported in A.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R116

**Development A** `2026-08-31:indonesia-us-joint-drills`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T07:01 to 2026-08-31T07:01 UTC
- **Actors:** Southeast Asian
- **Places:** Asia, Beijing, China, Indonesia, Jakarta, Taiwan, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T07:01 [South China Morning Post] **Indonesia-US joint military drills with allies kick off with 4,700 soldiers**
    > Indonesia, the United States and more than a dozen allies launched annual joint military exercises on Monday to boost defence capabilities and “deter aggression” in the Asia-Pacific region.
Jakarta maintains a neutral foreign policy, what it calls “free and active”, as it walks a

**Development B** `2026-08-31:trump-xi-summit-prediction-markets`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T14:00 to 2026-08-31T14:00 UTC
- **Actors:** Donald Trump, Trump, White House, Xi Jinping
- **Places:** Beijing, China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T14:00 [South China Morning Post] **Prediction markets have priced the Trump-Xi summit. Do the bets have any value?**
    > US President Donald Trump has already announced the date: September 24.
That is when, Trump says, Chinese President Xi Jinping will come to the White House for a visit following the “America first” leader’s own three-day trip to Beijing in May.
But there is a diplomatic wrinkle.


| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Indonesia-US drills and an analysis of prediction markets on the Trump-Xi summit are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R117

**Development A** `2026-10-03-live:s-1158`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-29T14:05 to 2026-09-29T14:05 UTC
- **Actors:** Legal Aid Department
- **Places:** Hong Kong
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 14:05 [South China Morning Post] **Legal aid chief denies stricter vetting as aid for policy challenges hits decade low**
    > Hong Kong authorities approved only two legal aid applications for judicial review challenges against government policies and decisions last year, the fewest in the past decade, although its director has dismissed claims of tightened scrutiny or diminished access to justice.
The 

**Development B** `2026-10-03-live:s-2005`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-10-03T09:04 to 2026-10-03T09:04 UTC
- **Actors:** Chris Sun Yuk-han, Labour
- **Places:** Hong Kong
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-03 09:04 [South China Morning Post] **‘Balanced and acceptable’: labour chief defends helper wage rise amid criticism**
    > Hong Kong’s stronger economic performance over the past year was the reason for raising the monthly minimum wage for foreign domestic helpers by 2.35 per cent, the labour minister has said, amid disappointment from both unions and employers’ groups.
Defending the government’s dec

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Legal aid statistics and the helper wage defence are unrelated Hong Kong policy items.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R118

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

**Development B** `2026-09-27-live:waltz-uranium-offer`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T17:42 to 2026-09-27T17:42 UTC
- **Actors:** Mike Waltz
- **Places:** Iran, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T17:42 [Al Jazeera] **Mike Waltz: US offered to sell Iran uranium for civilian programme**
    > US ambassador says Iran refused to agree to an arrangement where uranium would be supplied by Washington.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | none |

**Rationale:** Waltz revealing a US uranium-sale offer is not stated as a response to or continuation of A's tensions report.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R119

**Development A** `2026-08-21:maresca-needs-time-bournemouth`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-21T14:36 to 2026-08-21T14:36 UTC
- **Actors:** EPL, Enzo Maresca, Maresca, Pep Guardiola
- **Places:** Bournemouth, Man City, Manchester City
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T14:36 [Al Jazeera] **Manchester City’s Maresca admits he needs time as Bournemouth visit in EPL**
    > Enzo Maresca replaced Pep Guardiola between seasons but says Man City may need patience before more trophies arrive.

**Development B** `2026-08-21:man-city-preview`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-22T10:09 to 2026-08-22T10:09 UTC
- **Actors:** Enzo Maresca, Pep Guardiola
- **Places:** Manchester City
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T10:09 [Al Jazeera] **Manchester City preview: Five key questions heading into 2026-27 season**
    > Enzo Maresca faces the formidable challenge of following the legendary manager Pep Guardiola as new season starts.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** A is Maresca's press comments and B a season preview analysis; same topic only.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R120

**Development A** `2026-08-21:flores-quake-survivors`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-21T08:03 to 2026-08-21T08:03 UTC
- **Actors:** Carolus Winfridus, Flores, Sikka Regency
- **Places:** Indonesia, Maumere
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T08:03 [South China Morning Post] **Indonesian quake survivors recall trauma of all-day intense aftershocks, self-rescue**
    > Carolus Winfridus was asleep when an earthquake struck off Indonesia’s island of Flores, as he was awoken by intense rumbling and saw his wardrobe doors flying open.
He and his family quickly scrambled for a way out of their house in the town of Maumere, Sikka Regency, one of nin

**Development B** `2026-08-21:indonesia-troops-borneo-wildfires`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-22T13:35 to 2026-08-22T13:35 UTC
- **Actors:** none extracted
- **Places:** Borneo, Indonesia
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T13:35 [Al Jazeera] **Indonesia bolsters troop numbers to combat Borneo wildfires**
    > Fires between January and July burned more than 200,000 hectares of land, says the government.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Flores earthquake survivors and Borneo wildfires are different hazards.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R121

**Development A** `2026-09-29-live:japanese-firms-pull-back-china`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-29T07:00 to 2026-09-29T07:00 UTC
- **Actors:** Teikoku
- **Places:** Beijing, China, Japan, Tokyo
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T07:00 [South China Morning Post] **Japanese firms pull back from China amid geopolitical tensions, supply chain shifts**
    > The number of Japanese companies operating in China has fallen nearly 30 per cent since its peak in 2012 and is down 22 per cent over the past two years, according to a survey conducted amid prolonged political tensions between Beijing and Tokyo.
As of June, 10,118 Japanese enter

**Development B** `2026-09-29-live:pimco-china-diversification`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-29T08:00 to 2026-09-29T08:00 UTC
- **Actors:** Pimco
- **Places:** China, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T08:00 [South China Morning Post] **‘180-degree flip’ sees global investors turn to China for diversification: Pimco president**
    > Global investors are turning to China again in search of alternatives to crowded US asset markets, with Pimco seeing Chinese bonds as one of the safest ways to diversify portfolios after sentiment towards the world’s second-largest economy “flipped 180 degrees”.
The US-based asse

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Japanese firms leaving China and Pimco on investors returning to China share only the topic.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R122

**Development A** `2026-09-25:us-china-state-dinner`

- **Members:** 4 item(s)
- **Sources:** BBC World, South China Morning Post
- **Times:** 2026-09-25T05:48 to 2026-09-25T08:09 UTC
- **Actors:** Central Guard Bureau, Communist Party, Donald Trump, General Office, Peng Liyuan, People's Liberation Army, Richard Nixon, Schramsberg Blanc de Noirs, Sino-US, Trump, White House, Xi Jinping
- **Places:** Beijing, China, East Room, United States, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T05:48 [South China Morning Post] **From wine to ping-pong, Trump and Xi’s state dinner is heavy on historic symbolism**
    > When US President Donald Trump hosted Chinese President Xi Jinping in the East Room, every detail of the state dinner was steeped in symbolism, with sparkling wine served as a nod to a pivotal moment in Sino-US relations and references to “ping-pong diplomacy”.
The meal opened wi
  - 2026-09-25T07:00 [South China Morning Post] **Xi-Trump dinner puts US tech titans in spotlight – what does it mean for China ties?**
    > If the American guests seated at the head table with President Xi Jinping and US President Donald Trump at Thursday’s White House state dinner were any indication, Washington now views its relationship with Beijing largely through the prism of technology.
Analysts said the seatin
  - 2026-09-25T07:19 [South China Morning Post] **Xi’s security chief among cohort of rising officials at White House banquet**
    > Zhou Hongxu, the official who oversees President Xi Jinping’s security, made an appearance at the White House state banquet on Thursday night, alongside a cohort of other rising Chinese officials.
The banquet’s guest list described the 55-year-old People’s Liberation Army (PLA) m
  - 2026-09-25T08:09 [BBC World] **Trump and Xi exchange warm words at state dinner but little progress on key issues**
    > Despite diplomatic niceties and gifts, little was shared on substantial issues separating the leaders.

**Development B** `2026-09-25:scmp-summit-reader-qa`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-25T05:55 to 2026-09-25T05:55 UTC
- **Actors:** Asian, Donald Trump, SCMP, Xi Jinping
- **Places:** China, South, Taiwan, United States, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T05:55 [South China Morning Post] **AI war, Taiwan and translation: SCMP answers your questions from Xi-Trump summit**
    > This live article is freely available to our registered users. Please log in or create an account.
Xi’s US summit: Access real-time updates, geopolitical risk analysis, and exclusive reporting from an Asian perspective. Subscribe now with our limited-time offer to stay ahead.
Chi

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** B is a live Q&A/analysis page on the summit, commentary rather than an occurrence related to A's state dinner.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R123

**Development A** `2026-09-29-live:russia-2027-defence-budget`

- **Members:** 1 item(s)
- **Sources:** Defense News
- **Times:** 2026-09-28T18:07 to 2026-09-28T18:07 UTC
- **Actors:** Reuters
- **Places:** Russia, Ukraine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T18:07 [Defense News] **Russia raises 2027 military spending by 27%, budget documents show**
    > Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027, around 27% more than the 13.5 trillion roubles, or $159.8 billion, originally budgeted and the highest figure since the start of the war in Ukraine in 2022, government documents seen by Reuters sh

**Development B** `2026-09-29-live:putin-decree-15500-troops`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-28T19:08 to 2026-09-28T19:08 UTC
- **Actors:** Vladimir Putin
- **Places:** Russia, Ukraine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T19:08 [South China Morning Post] **Putin signs decree adding 15,500 troops to Russian army**
    > Russian President Vladimir Putin signed a decree on Monday boosting the size of the army by 15,500 troops in the fourth such order this year.
Putin’s order comes as both Russia and Ukraine suffer mounting casualties in the more than four-and-a-half-year Ukraine war.
The decree di

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | none |

**Rationale:** Russia's 2027 defence budget rise and Putin's troop decree are separate acts; the decree gave no reason and no causal link is stated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R124

**Development A** `2026-09-29-live:pope-leo-ai-not-fake-news`

- **Members:** 2 item(s)
- **Sources:** Al Jazeera, South China Morning Post
- **Times:** 2026-09-28T21:45 to 2026-09-29T04:51 UTC
- **Actors:** AI, Catholic Church, Donald Trump, Leo
- **Places:** US
- **System Development:** D13
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T21:45 [South China Morning Post] **Pope Leo says concerns about AI doom scenarios are not ‘fake news’**
    > Pope Leo on Monday ⁠said concerns that artificial intelligence ⁠could destroy the world are not “fake news” and should be taken seriously, in an apparent rebuke of US President Donald Trump.
The first US pope, who has warned of the dangers of AI throughout his 16-month papacy, al
  - 2026-09-29T04:51 [Al Jazeera] **Pope Leo says AI risk concerns not ‘fake news’**
    > Leader of the Catholic Church says AI safety issues should be taken seriously and acted on.

**Development B** `2026-09-29-live:pope-leo-france-tour-final-day`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T03:00 to 2026-09-29T03:00 UTC
- **Actors:** Leo, Leo XIV, Metz
- **Places:** France
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T03:00 [Al Jazeera] **Fighter jets escort Pope Leo on final day of his France tour**
    > Pope Leo XIV was escorted by fighter jets to Metz, the final stop of his four-day France tour.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `AMBIGUOUS` | none | low | none |

**Rationale:** The Pope's AI remarks came on Monday during his four-day France tour, but the text does not say they were made on the tour; the venue would settle it.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R125

**Development A** `2026-09-29-live:trump-china-weapons-analysis`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T16:55 to 2026-09-28T16:55 UTC
- **Actors:** Trump
- **Places:** Beijing, China, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T16:55 [Al Jazeera] **Arming an adversary: Why Trump’s offer to sell China weapons belies US policy**
    > Analysts dismissed Trump&#039;s proposal as lacking any strategic logic – but said it revealed how he views Beijing.

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

**Rationale:** Analysis of Trump's China arms offer and Trump denying Iran sanctions relief are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R126

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

**Development B** `2026-08-31:hk-child-social-media-opinion`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T01:30 to 2026-08-31T01:30 UTC
- **Actors:** none extracted
- **Places:** Hong Kong
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T01:30 [South China Morning Post] **Don’t leave Hong Kong parents to their own devices on child social media use**
    > Hong Kong, a city of overachievers, especially when it comes to the young, is also filled with children who take to social media early. Almost 35 per cent of kindergarten pupils log at least one hour of recreational screen time daily. By the junior forms, 60 per cent exceed the i

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Robot convenience stores and a social media opinion piece are unrelated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R127

**Development A** `2026-08-21:russian-strikes-kill-six-day-after-mall`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-08-22T12:09 to 2026-08-22T12:09 UTC
- **Actors:** none extracted
- **Places:** Russia, Ukraine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T12:09 [Al Jazeera] **Russian strikes kill 6 people in Ukraine, day after shopping complex attack**
    > Meanwhile, Ukrainian drone hits home in southern Russia, killing two children and injuring their parents, officials say.

**Development B** `2026-08-21:ukraine-mall-strike-rescue`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-08-22T13:13 to 2026-08-22T13:13 UTC
- **Actors:** Volodymyr Zelenskyy
- **Places:** Russia, Ukraine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-22T13:13 [BBC World] **Rescuers dig through Ukraine mall wreckage as Zelensky condemns 'despicable' Russian strike**
    > Four people are still missing after Friday's attack which killed 16 and left 130 injured, including a number of children.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | none |

**Rationale:** A is new Russian strikes the day after the mall attack; B is rescue at the earlier mall strike; different days, not one wave.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R128

**Development A** `2026-10-03-live:s-1155`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-29T14:00 to 2026-09-29T14:00 UTC
- **Actors:** Autonomous Systems Warfighting Development Centre, People's Liberation Army, Robotic, U.S. Navy
- **Places:** Taiwan, US, Virginia
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 14:00 [South China Morning Post] **US Navy launches drone command that could reshape Taiwan war planning**
    > The US Navy has set up a dedicated command to turn its growing array of aerial, surface and underwater drones into an integrated fighting force – a capability US commanders have linked to disrupting a PLA attack on Taiwan.
The Robotic and Autonomous Systems Warfighting Developmen

**Development B** `2026-10-03-live:s-1486`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-30T23:13 to 2026-09-30T23:13 UTC
- **Actors:** Donald Trump, Families, Trump, White House, Xi Jinping
- **Places:** Beijing, China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 23:13 [South China Morning Post] **Trump claims he discussed release of political prisoners in China with Xi at summit**
    > US President Donald Trump said on Wednesday that he discussed the release of political prisoners in China with his counterpart, Xi Jinping, in Washington last week.
“We talked, and I think we had some very, very important discussions. Hopefully fruitful discussions,” Trump told r

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Navy drone command and Trump's political prisoners remark share only US-China context.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R129

**Development A** `2026-09-29-live:bangkok-jet-skier-arrest`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T13:00 to 2026-09-28T13:00 UTC
- **Actors:** none extracted
- **Places:** Bangkok, Thailand
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T13:00 [Al Jazeera] **Thai police arrest jet skier after joyride through flooded Bangkok streets**
    > Thai police arrest jet skier after joyride through flooded Bangkok streets

**Development B** `2026-09-29-live:thai-airways-baggage-backlog`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-29T06:33 to 2026-09-29T06:33 UTC
- **Actors:** Ekkapob Pianpises, Thai Airways
- **Places:** Bangkok, Thailand
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T06:33 [South China Morning Post] **One Bangkok flood battle after another as Thai Airways races to clear baggage backlog**
    > Standing water ⁠in Thailand’s capital is expected ⁠to clear within three days if there is no additional rainfall, the government said on Tuesday, as flag carrier Thai Airways struggled to resume regular services following heavy rain and flooding.
The ‌cabinet will discuss long-te

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | low | none |

**Rationale:** A jet skier's arrest is a side incident, not a calamity stage like B's flood recovery and baggage backlog; shared flood context only.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R130

**Development A** `2026-08-21:harry-uk-return-royal-rift`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-21T06:53 to 2026-08-21T06:53 UTC
- **Actors:** Charles, Harry, Meghan, Prince Harry, Prince William, Princess Diana, William
- **Places:** Sussex, UK
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T06:53 [South China Morning Post] **As Harry plans UK return, can he patch up royal rift with Prince William?**
    > William and Harry were united in grief as children by the tragic death of their mother, Princess Diana, but their relationship as adults has been ripped apart by anger and hurt.
The pair – dubbed “the heir and the spare” from an early age – have failed to put aside their differen

**Development B** `2026-08-21:harry-ordered-to-pay-legal-costs`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-21T13:39 to 2026-08-21T13:39 UTC
- **Actors:** Associated Newspapers, Daily Mail, Elton John, Matthew Nicklin, Prince Harry
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T13:39 [South China Morning Post] **Prince Harry and others ordered to pay initial US$13 million in failed lawsuit**
    > Prince Harry, Elton John ⁠and other high-profile claimants face paying ⁠millions of dollars out of their own pockets to cover the legal costs of the Daily Mail’s publisher after a judge ruled their failed privacy lawsuits were conducted in an unreasonable way.
Judge Matthew Nickl

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** A is analysis of the royal rift; B is a costs ruling in Harry's lawsuit; shared actor only.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R131

**Development A** `2026-09-29-live:wang-yi-meets-iwaya`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-29T06:00 to 2026-09-29T06:00 UTC
- **Actors:** Takeshi Iwaya, Wang, Wang Yi
- **Places:** Beijing, China, Japan
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T06:00 [South China Morning Post] **China warns Japan over WWII history as business delegation visits Beijing**
    > China’s top diplomat Wang Yi met Japan’s former foreign minister Takeshi Iwaya, who is leading a 50-member delegation of corporate executives, in Beijing on Monday, marking the highest-ranking Chinese official reception for a Japanese visit in nearly a year.
During the talks, Wan

**Development B** `2026-09-29-live:japanese-firms-pull-back-china`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-29T07:00 to 2026-09-29T07:00 UTC
- **Actors:** Teikoku
- **Places:** Beijing, China, Japan, Tokyo
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T07:00 [South China Morning Post] **Japanese firms pull back from China amid geopolitical tensions, supply chain shifts**
    > The number of Japanese companies operating in China has fallen nearly 30 per cent since its peak in 2012 and is down 22 per cent over the past two years, according to a survey conducted amid prolonged political tensions between Beijing and Tokyo.
As of June, 10,118 Japanese enter

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Wang Yi meeting a Japanese delegation and a survey of Japanese firms leaving China share only the bilateral pair.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R132

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
| `NO_RELATION` | none | medium | none |

**Rationale:** Both follow Trump's rejection of the Hormuz deal, but B's expectation of talks does not respond to A's Iranian minister statement.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R133

**Development A** `2026-09-25:white-house-tour`

- **Members:** 2 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-25T03:13 to 2026-09-25T08:05 UTC
- **Actors:** Biden, Donald Trump, Joe Biden, Trump, White House, Xi Jinping
- **Places:** Beijing, China, Great Hall of the People, Oval Office, South Lawn, United States
- **System Development:** D3
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T03:13 [South China Morning Post] **Trump autopen joke at Biden’s expense draws rare laugh from China’s Xi**
    > Chinese President Xi Jinping broke into rare laughter as his US counterpart Donald Trump showed him a framed “autopen” displayed in place of the former American leader Joe Biden’s portrait during a White House tour.
The viral moment stood out against the Chinese leader’s otherwis
  - 2026-09-25T08:05 [South China Morning Post] **Trump gives Xi a tour of his pet White House building projects, including the ballroom**
    > Property developer-turned-president Donald Trump appeared to relish showing off the White House’s latest building works to Xi Jinping on Thursday, eager to give his Chinese counterpart a glimpse of his construction ambitions since they last met in China.
In May, Trump was hosted 

**Development B** `2026-09-25:us-china-state-dinner`

- **Members:** 4 item(s)
- **Sources:** BBC World, South China Morning Post
- **Times:** 2026-09-25T05:48 to 2026-09-25T08:09 UTC
- **Actors:** Central Guard Bureau, Communist Party, Donald Trump, General Office, Peng Liyuan, People's Liberation Army, Richard Nixon, Schramsberg Blanc de Noirs, Sino-US, Trump, White House, Xi Jinping
- **Places:** Beijing, China, East Room, United States, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-25T05:48 [South China Morning Post] **From wine to ping-pong, Trump and Xi’s state dinner is heavy on historic symbolism**
    > When US President Donald Trump hosted Chinese President Xi Jinping in the East Room, every detail of the state dinner was steeped in symbolism, with sparkling wine served as a nod to a pivotal moment in Sino-US relations and references to “ping-pong diplomacy”.
The meal opened wi
  - 2026-09-25T07:00 [South China Morning Post] **Xi-Trump dinner puts US tech titans in spotlight – what does it mean for China ties?**
    > If the American guests seated at the head table with President Xi Jinping and US President Donald Trump at Thursday’s White House state dinner were any indication, Washington now views its relationship with Beijing largely through the prism of technology.
Analysts said the seatin
  - 2026-09-25T07:19 [South China Morning Post] **Xi’s security chief among cohort of rising officials at White House banquet**
    > Zhou Hongxu, the official who oversees President Xi Jinping’s security, made an appearance at the White House state banquet on Thursday night, alongside a cohort of other rising Chinese officials.
The banquet’s guest list described the 55-year-old People’s Liberation Army (PLA) m
  - 2026-09-25T08:09 [BBC World] **Trump and Xi exchange warm words at state dinner but little progress on key issues**
    > Despite diplomatic niceties and gifts, little was shared on substantial issues separating the leaders.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `same_visit_or_summit` | none | high | none |

**Rationale:** Trump's White House tour for Xi and the state dinner are parts of the same Xi state visit on the same day.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R134

**Development A** `2026-08-31:hk-retail-sales-july`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T08:56 to 2026-08-31T08:56 UTC
- **Actors:** Census
- **Places:** Hong Kong
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T08:56 [South China Morning Post] **Hong Kong retail sales rise 4.5% in July, marking 15th straight month of growth**
    > Hong Kong’s retail sector recorded growth for a 15th consecutive month in July, with the government reporting a 4.5 per cent increase year on year, although the pace of expansion slowed amid adverse weather and continued outbound travel by residents.
Retail sales value for the mo

**Development B** `2026-08-31:hk-prime-retail-leasing`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-31T09:00 to 2026-08-31T09:00 UTC
- **Actors:** Capitol Centre, Chanel, HSBC, Victoria
- **Places:** Causeway Bay, Hong Kong
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-31T09:00 [South China Morning Post] **Hot property: Big banks, fashion stores seek ‘cheaper’, eye-catching Hong Kong retail**
    > From big banks to fashion brands, tenants are taking advantage of potential lower rents for retail space in Hong Kong’s prime areas as they utilise eye-catching locations to boost visibility towards customers, according to agents.
HSBC is unveiling its first flagship branch at th

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** July retail sales figures and retail leasing trends share only the topic.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R135

**Development A** `2026-09-27-live:trump-asked-xi-weapons`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-28T04:06 to 2026-09-28T04:06 UTC
- **Actors:** David Perdue, Donald Trump, Fox News, Trump, US State Department, White House, Xi Jinping
- **Places:** Beijing, China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T04:06 [South China Morning Post] **Trump asked Xi if Beijing wanted US weapons: a joke, a gambit or something more?**
    > Donald Trump asked President Xi Jinping whether Beijing wanted to buy American weapons, the US ambassador to China said on Sunday, prompting the State Department to quickly rule out any such deal with Washington’s principal strategic competitor.
“He actually asked President Xi, w

**Development B** `2026-09-27-live:summit-what-wasnt-said`

- **Members:** 1 item(s)
- **Sources:** BBC World
- **Times:** 2026-09-28T07:52 to 2026-09-28T07:52 UTC
- **Actors:** Donald Trump, Trump, Xi Jinping
- **Places:** Washington
- **System Development:** D14
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T07:52 [BBC World] **Trump-Xi summit: What wasn't said might matter the most**
    > The most revealing thing about the summit in Washington may be what the two leaders did not say - and what we still don't know.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** B is an analysis of what was not said at the summit; commentary unrelated to A's weapons question.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R136

**Development A** `2026-09-27-live:ethiopia-meskel-peace-calls`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-27T13:34 to 2026-09-27T13:34 UTC
- **Actors:** Meskel
- **Places:** Ethiopia
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-27T13:34 [Al Jazeera] **Ethiopians celebrate Meskel and call for peace amid fighting**
    > Ethiopians celebrate Meskel and call for peace amid fighting

**Development B** `2026-09-27-live:aj-afar-frontline-report`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T09:44 to 2026-09-28T09:44 UTC
- **Actors:** Abiy Ahmed, Al Jazeera
- **Places:** Ethiopia
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T09:44 [Al Jazeera] **Al Jazeera reports from near front line in Ethiopia’s Afar region**
    > Al Jazeera reports from Ethiopia’s Afar region, where fighting has spread amid efforts to oust PM Abiy Ahmed.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | none |

**Rationale:** Meskel celebrations and a front-line report from Afar share only the Ethiopia conflict context.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R137

**Development A** `2026-10-03-live:s-1202`

- **Members:** 1 item(s)
- **Sources:** Defense News
- **Times:** 2026-09-29T16:18 to 2026-09-29T16:18 UTC
- **Actors:** Advanced Medium-Range Air, Arsenal of Freedom, Raytheon, U.S. Air Force, U.S. Navy, US Department of Defense
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 16:18 [Defense News] **Pentagon awards Raytheon up to $20.7 billion to nearly double AMRAAM production**
    > The Defense Department has awarded Raytheon a multiyear contract worth up to $20.7 billion to build Advanced Medium-Range Air-to-Air Missiles, or AMRAAMs. The Pentagon said the deal will nearly double AMRAAM production.The five-year contract, which includes two option years, is p

**Development B** `2026-10-03-live:D18`

- **Members:** 2 item(s)
- **Sources:** Breaking Defense, Defense News
- **Times:** 2026-10-01T22:05 to 2026-10-02T13:49 UTC
- **Actors:** Navy, RTX, Raytheon, Standard, U.S. Navy, US Department of Defense
- **Places:** Middle East, SM-6
- **System Development:** D18
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-01 22:05 [Defense News] **US Navy awards RTX’s Raytheon $24.4B for SM-6 missiles amid stockpile concerns**
    > RTX’s Raytheon unit won a multiyear contract worth up to $24.4 billion to produce Standard Missile-6 interceptors for the U.S. Navy, the service said on Thursday, as the Pentagon pushes to replenish munitions stockpiles depleted by conflicts in the Middle East.The five-year contr
  - 2026-10-02 13:49 [Breaking Defense] **Navy, Raytheon ink $24.4B deal for SM-6 ‘acceleration’**
    > The deal covers at least five-years of production for an undisclosed number of missiles.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** AMRAAM and SM-6 contracts are separate awards to the same contractor.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R138

**Development A** `2026-09-30-multilingual:D10`

- **Members:** 12 item(s)
- **Sources:** ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri
- **Times:** 2026-09-29T18:24 to 2026-09-30T08:09 UTC
- **Actors:** AI, Big Tech, Ciencia, Donald Trump, Gobierno de EE UU, Intelligenza Artificiale, MIT, Musk, OpenAI a Stanford, Sam Altman, Super Intelligence Pranzo alla Casa Bianca, Tecnología
- **Places:** Estados Unidos, Gobierno, Gobierno de EEUU, U.S.
- **System Development:** D10
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 18:24 [El País Internacional] **Trump lanza una página oficial de información sobre el Gobierno de EE UU que le desmiente**
    > El presidente de Estados Unidos, Donald Trump, en el acto de presentación de la plataforma America.gov.
  - 2026-09-29 19:04 [Il Sole 24 Ore Mondo] **Trump, per Ai solo autoregolamentazione. Firmato l’ordine che cambia il nome in Super Intelligence**
    > Pranzo alla Casa Bianca con decine di protagonisti dell’intelligenza artificiale americana per inaugurare la nuova era della Super Intelligenza. Nessuna menzione di rischi, crisi, e incidenti anche se forse nascerà un comitato consultivo di supervisione.
  - 2026-09-29 20:36 [Rai News Esteri] **Trump incontra i vertici Big Tech sulla sicurezza AI: "Autoregolazione e nessun controllo federale"**
    > Un impegno "moralmente vincolante" a predisporre misure di salvaguardia. Zuckerberg: "Controlli interni robusti". Musk: "L'esito più probabile? Un futuro di abbondanza"
  - 2026-09-29 20:36 [ANSA Mondo] **Trump, 'da vertici big tech impegno moralmente vincolante su sicurezza IA'**
    > 'Si autoregoleranno'

**Development B** `2026-09-30-multilingual:sx-168`

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

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | SAME_DEVELOPMENT_SUSPECTED |

**Rationale:** B covers the same White House AI luncheon and America.gov launch as A, with Trump's China remark made at that event.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R139

**Development A** `2026-09-30-multilingual:sx-29`

- **Members:** 1 item(s)
- **Sources:** White House
- **Times:** 2026-09-28T19:56 to 2026-09-28T19:56 UTC
- **Actors:** All Presidential Actions, Anti-Mining Policy News, Briefings & Statements, Nominations & Appointments, Trump
- **Places:** U.S.
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28 19:56 [White House] **Mined, Melted, and Poured in America: President Trump Reverses Years of Anti-Mining Policy**
    > News				
			
			
					
	
		
		
			Search
					
						
		
			
				
					Select Category				
				
																		
								All News							
																								
								Briefings &amp; Statements							
																								
																	
										All Presidential Acti

**Development B** `2026-09-30-multilingual:sx-133`

- **Members:** 1 item(s)
- **Sources:** Rai News Esteri
- **Times:** 2026-09-29T19:21 to 2026-09-29T19:21 UTC
- **Actors:** Wright
- **Places:** Paesi, U.S.
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29 19:21 [Rai News Esteri] **Gli Usa prestano alle aziende energetiche 40 milioni di barili di petrolio delle riserve strategiche**
    > Per contenere il caro carburante. Wright: "Anche i Paesi europei onorino gli impegni presi"

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | none |

**Rationale:** Mining policy reversal and the SPR oil loan are separate US energy actions.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R140

**Development A** `2026-10-03-live:s-1371`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-09-30T12:30 to 2026-09-30T12:30 UTC
- **Actors:** Donald Trump, White House, Xi Jinping
- **Places:** China, US
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-30 12:30 [South China Morning Post] **US-China conflict doesn’t have to become a self-fulfilling prophecy**
    > We are reminded seemingly daily of the great power transitions that ended in conflict. However, it is the exceptions – the ones that did not result in war – that could have real lessons to offer.
Today, the question is more than academic. Standing beside US President Donald Trump

**Development B** `2026-10-03-live:s-1942`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-10-02T22:00 to 2026-10-02T22:00 UTC
- **Actors:** Daines, Donald Trump, Republicans, Steve Daines, Xi Jinping
- **Places:** Beijing, China, US, Washington
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-10-02 22:00 [South China Morning Post] **‘No retreat’: Key Trump ally urges continued US-China engagement on rare earths**
    > US Republican Senator Steve Daines, a close aide to President Donald Trump and a key interlocutor between Washington and Beijing, has called on the two capitals to stay engaged and “not retreat” over differences on issues including rare earth supply chains.
Daines told the South 

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | high | commentary |

**Rationale:** A is an opinion piece; B is Daines urging engagement on rare earths; topic only.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R141

**Development A** `2026-08-21:canadian-premier-attacks-trump`

- **Members:** 1 item(s)
- **Sources:** South China Morning Post
- **Times:** 2026-08-21T03:12 to 2026-08-21T03:12 UTC
- **Actors:** Canada, Carney, Donald Trump, Mark Carney, Trump, Wab Kinew
- **Places:** Canada, Manitoba, US, Washington
- **System Development:** D4
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-08-21T03:12 [South China Morning Post] **Canadian premier says ‘erratic’ Trump ‘not to be trusted’ amid US trade feud**
    > The premier of a Canadian province launched a blistering attack on US President Donald Trump on Thursday, calling him a “bad person” and “not to be trusted” and urging Canada to keep fighting rather than rush to make concessions in trade talks with Washington.
Manitoba Premier Wa

**Development B** `2026-08-21:carney-crucial-test-analysis`

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

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | commentary |

**Rationale:** Manitoba premier's attack on Trump and an analysis of Carney walking away from talks share the trade feud only.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

---

## R142

**Development A** `2026-09-29-live:unga-durban-commemoration`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-28T13:38 to 2026-09-28T13:38 UTC
- **Actors:** UN General Assembly, United Nations
- **Places:** none extracted
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-28T13:38 [Al Jazeera] **UN commemoration of Durban Declaration: What’s on agenda, who will attend?**
    > UN General Assembly marks 25th anniversary of the 2011 Durban Declaration, which called for combating racism.

**Development B** `2026-09-29-live:unga-five-takeaways`

- **Members:** 1 item(s)
- **Sources:** Al Jazeera
- **Times:** 2026-09-29T08:30 to 2026-09-29T08:30 UTC
- **Actors:** AI, UN General Assembly
- **Places:** Palestine
- **System Development:** none (not surfaced: single source)
- **Situation (production, `actor_set`):** none
- **Evidence:**
  - 2026-09-29T08:30 [Al Jazeera] **UNGA 81: Five key takeaways from general debate**
    > The 81st United Nations General Assembly ends with AI, Palestine and wars dominating speeches.

| Proposed relation | Direction | Confidence | Flags |
|---|---|---|---|
| `NO_RELATION` | none | medium | commentary |

**Rationale:** A previews the Durban commemoration; B is a takeaways analysis of the general debate; no bounded link stated.

**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______

