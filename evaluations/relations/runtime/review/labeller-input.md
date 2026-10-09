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

## U001
**A** (3 item(s))
- 2026-10-04 12:33 [Rai News Esteri] Spagna, il Psoe in pressing su Sanchez per il voto anticipato. La destra soffia sulle piazze
  > Oltre mezzo milione di persone sfilano a Madrid, a Valencia la tensione sfocia in cariche e 5 arresti di fronte a un summit immobiliare. Il Congresso ha bocciato i decreti salva-affitti coi voti di centrodestra e indipendentisti catalani
- 2026-10-05 07:29 [ANSA Mondo] Sanchez, 'ho deciso di convocare le elezioni il 29 novembre'
  > Il premier in una dichiarazione istituzionale
- 2026-10-05 12:08 [Rai News Esteri] Sanchez porta la Spagna al voto il 29 novembre sull'onda delle proteste per la crisi abitativa
  > Il capo del governo di Madrid, pressato da giorni da richieste di elezioni anticipate, punta a capitalizzare un consenso "last minute" con i provvedimenti per la casa, una crisi che ha portato a proteste in tutto il Paese
**B** (6 item(s))
- 2026-10-05 07:14 [Al Jazeera] Spanish Prime Minister Pedro Sanchez announces snap election
  > Sanchez calls early vote after parliament rejected housing relief measures proposed by his minority government.
- 2026-10-05 08:04 [South China Morning Post] Spain’s prime minister calls early election as housing becomes national flashpoint
  > Spanish Prime Minister Pedro Sanchez announced early elections Monday after his government suffered a bruising legislative defeat last week on emergency measures related to the country’s housing crisis.
The vote will be held on November 29.
In recent weeks, Spaniards have demanded solutions from the
- 2026-10-05 10:18 [BBC World] Spanish PM Sánchez calls early election after housing protests
  > Sánchez says Spain will head to the polls on 29 November after recent defeats on measures aimed at addressing the country's housing crisis.
- 2026-10-05 17:27 [Al Jazeera] Spain calls snap election amid housing crisis
  > Mounting anger over Spain’s housing crisis have led Prime Minister Sanchez to call an early election on November 29
- 2026-10-05 19:30 [BBC World] Spain PM pins hopes on housing crisis to help win snap election
  > Calling of a snap election was not a knee-jerk reaction from Pedro Sánchez but a carefully thought-out manoeuvre, Guy Hedgecoe reports from Madrid.
- 2026-10-05 19:31 [France 24] Sanchez chose 'best moment in a sea of troubles' to call for snap election, analyst says
  > Spanish Prime Minister Pedro Sanchez on Monday called an early election for November 29, aiming to increase his parliamentary support after lawmakers last week rejected proposals to address a housing crisis that has drawn nationwide protests. Speaking with FRANCE 24's Mark Owen, Javier Carbonell, Po

## U002
**A** (2 item(s))
- 2026-10-03 12:22 [BBC Mundo] Lo que la fallida ejecución de Christa Pike revela sobre la pena de muerte en EE.UU.
  > Christa Pike, una mujer condenada a muerte en Tennessee, sobrevivió a la aplicación de dos inyecciones letales. Su caso ha vuelto a centrar la atención en la pena de muerte y en cómo se aplica en Estados Unidos.
- 2026-10-03 19:14 [Il Sole 24 Ore Mondo] Trump vuole estendere la pena di morte ai narcotrafficanti: il caso Pike riapre lo scontro
  > Il presidente promette di ampliare i reati punibili con la pena capitale. Il Tennessee sospende le esecuzioni dopo il caso Pike, mentre una sentenza della Corte Suprema del 2008 lascia aperto il nodo dei grandi narcotrafficanti
**B** (5 item(s))
- 2026-10-04 15:16 [Al Jazeera] Dodik urges Serb turnout against ‘Sarajevo crooks’ in Bosnia election
  > Dodik urges Serb turnout against ‘Sarajevo crooks’ in Bosnia election
- 2026-10-04 20:36 [South China Morning Post] Serb separatist Dodik declares victory in Bosnia vote as ethnic tensions, EU hopes collide
  > Bosnian Serb nationalist politician Milorad Dodik has declared victory for his party in an election in Bosnia and Herzegovina on Sunday that was shaped by economic pressures, the prospect of the Balkan nation joining the European Union and ethnic tensions that have divided the country since its brut
- 2026-10-05 03:36 [Al Jazeera] Bosnian Serb nationalist claims party victory in Bosnia elections
  > Bosnian Serb nationalist Milorad Dodik claimed victory for his party in Bosnia’s elections.
- 2026-10-05 07:33 [Kyiv Independent] Pro-Russian Dodik claims party victory in Bosnian elections
  > "If it had not been for (U.S. President) Donald Trump's magnificent victory, we would probably be political corpses today," Milorad Dodik told his supporters, while also thanking Russian President Vladimir Putin.
- 2026-10-05 10:23 [DW World] Bosnia election: New technology might have stopped votes being cast on behalf of dead voters, but the result remains unchanged
  > New technology has stopped votes being cast on behalf of dead or absent voters, and turnout has fallen to a record low. But it was a case of deja vu in Bosnia's elections with the same parties winning.

## U003
**A** (5 item(s))
- 2026-10-08 05:06 [Al Jazeera] Signage at UK consulate in East Jerusalem removed as Israel’s deadline over
  > Thursday marks 30 days since Israel&#039;s foreign minister ordered the closure of the UK consulate in occupied East Jerusalem.
- 2026-10-08 07:06 [BBC World] Most UK diplomats to leave East Jerusalem consulate, Israel says, as Miliband says 'vital services' to remain
  > Israel said in September it would act in response to UK sanctions on illegal Israeli settlements in the West Bank.
- 2026-10-08 07:27 [South China Morning Post] Britain downscales and renames Jerusalem consulate after Israel orders closure
  > Britain said on Thursday its ⁠nearly 200-year-old consulate in Jerusalem ⁠would remain operating at a smaller scale, renamed ⁠as the “UK Mission” in the city, after Israel ordered it shut in a dispute over sanctions on settlements.
Israel last month issued a 30-day deadline for Britain to close the 
- 2026-10-08 08:25 [Al Jazeera] Video: Signs removed from British consulate in occupied East Jerusalem
  > Signs from the British consulate in occupied East Jerusalem were removed overnight as a deadline for its closure loomed.
- 2026-10-08 14:01 [Al Jazeera] King David Hotel bombing to consulate row: A timeline of UK-Israel tension
  > Israel&#039;s order to shut UK&#039;s Jerusalem consulate is the latest downturn in a relationship strained since before 1948.
**B** (3 item(s))
- 2026-10-08 14:09 [France 24] Search warrants for former prince Andrew's homes were unlawful, UK court rules
  > Police who searched the properties of Andrew Mountbatten-Windsor as part of investigations into his links to the late sex offender Jeffrey Epstein have agreed the search warrants were unlawful, a London judge said Thursday. The 66-year-old younger brother of King Charles II was arrested on February 
- 2026-10-08 15:20 [South China Morning Post] UK police accept ex-prince Andrew search warrants must be ‘legally quashed’
  > British police on Thursday said that search warrants they secured to search properties linked to Andrew Mountbatten-Windsor had been issued unlawfully and must be quashed, but that the investigation into King Charles’ younger brother was ongoing.
Mountbatten-Windsor, 66, was arrested on suspicion of
- 2026-10-08 15:53 [Al Jazeera] UK ex-prince Andrew search warrants quashed after police accept legal error
  > London-based judge says error &#039;does not bring investigation to an end&#039; as police probe disgraced former royal.

## U004
**A** (3 item(s))
- 2026-09-30 05:05 [Al Jazeera] Hegseth to cut number of US general and admiral positions by 20%
  > Pentagon official says the plan will be announced in the defence secretary&#039;s &#039;State of the Force&#039; address in Virginia.
- 2026-09-30 21:42 [South China Morning Post] Trump defence chief says US slashed number of generals and admirals by 20%
  > US Defence Secretary Pete Hegseth announced on Wednesday that the United States has slashed the number of its generals and admirals by 20 per cent, in a move he said is aimed at “accountability”.
Hegseth suggested the cuts targeted officers who failed to get on board with his efforts to ensure the m
- 2026-10-01 02:34 [Al Jazeera] Hegseth announces 20% cut to US military commanders
  > US Secretary of Defense Pete Hegseth says he’s firing 20% of the military’s generals and admirals.
**B** (2 item(s))
- 2026-09-30 16:29 [Defense News] US Army selects five companies for PrSM development
  > The U.S. Army on Tuesday signed agreements with Anduril, Castelion, Lockheed Martin, Mach Industries and RTX to create advanced long-range missile prototypes, Redstone Arsenal announced this week. Each company will develop capabilities for the Precision Strike Missile (PrSM) Increment 4 program, mak
- 2026-09-30 19:08 [Breaking Defense] Army taps 5 companies for PrSM Inc 4 prototypes
  > Anduril, Castelion, Lockheed Martin, RTX and Mach Industries were awarded Other Transaction Agreements for an undisclosed amount.

## U005
**A** (14 item(s))
- 2026-10-07 12:00 [UN News] Ukraine: UN condemns latest attacks and calls for civilian protection
  > The UN Humanitarian Coordinator for Ukraine on Wednesday&nbsp;called for an end to attacks against civilians following further overnight strikes by Russian forces that reportedly killed at least 19 in the Chernihiv Region.
- 2026-10-08 07:26 [Kyiv Independent] General Staff: Russia has lost 1,547,780 troops in Ukraine since Feb. 24, 2022
  > The number includes 1,880 casualties that Russian forces suffered over the past day.
- 2026-10-08 09:12 [Kyiv Independent] At least 12 dead after Russian glide bomb strikes Kramatorsk bus stop
  > "Russia comes to the Ukrainian land with death," Donetsk Governor Vadym Filashkin said.
- 2026-10-08 09:54 [Kyiv Independent] Russian drone barrage on Kyiv kills 3, injures 13, disrupts electricity, water supplies
  > At 10:00 a.m. local time, Ukraine’s biggest private energy firm DTEK announced emergency energy shutdowns in Brovary, Buchanskyi, Vyshgorod, and Boryspil districts of the capital.
- 2026-10-08 10:08 [France 24] Dozens killed in Russian strike on buses in Ukraine's Kramatorsk as Kyiv targets data centre
  > At least 30 people were killed in a Russian strike on two buses in the Ukrainian city of Kramatorsk in the eastern Donetsk region on Thursday. Earlier, a drone hit a data centre belonging to Russian technology company Yandex, causing a fire.
- 2026-10-08 10:16 [BBC World] Russian strike on buses kills 33, say officials, as deadly attacks on Ukraine surge
  > Ukraine accused Russia of targeting the crowded bus in the frontline city to kill as many civilians as possible.
- 2026-10-08 10:31 [Al Jazeera] Russian attack on Ukraine’s Kramatorsk kills at least 12 people
  > Fourteen people were wounded in the Russian strike on city in eastern Ukraine&#039;s Donetsk region, local authorities say.
- 2026-10-08 11:43 [Kyiv Independent] Russian strikes kill at least 10, injure 45 across Ukraine over past day
  > Russia attacked across Ukraine with 142 Shahed-type drones, 82 of which were jet-powered overnight on Oct. 8, Ukraine's Air Force said.
- 2026-10-08 12:00 [South China Morning Post] At least 33 dead in Russian bomb blast in east Ukraine stronghold
  > A ⁠Russian bomb attack on ⁠the eastern Ukrainian city of Kramatorsk ⁠killed at least 33 people, authorities said on Thursday, describing it as a targeted strike on civilians in the key stronghold sought by Moscow.
Another 18 people were wounded in one of the largest single attacks this year, ‌which 
- 2026-10-08 13:44 [France 24] 30 dead in strike on Ukraine bus as Russian attacks intensify
  > Thirty people were killed and at least 18 were injured by Russian strikes in eastern Ukraine that included an attack on a public bus, authorities said Thursday, as an intensive pre-winter wave of attacks continued.
- 2026-10-08 14:50 [Al Jazeera] More killed in Kramatorsk as Russia targets Ukraine’s transportation system
  > Russia’s attacks on trains, buses and ports are paralysing Ukraine’s transport network and endangering civilians.
- 2026-10-08 17:07 [Al Jazeera] Dozens killed in Russian strike on civilian buses in eastern Ukraine
  > At least 33 people were killed after a Russian strike hit two civilian buses in a city within the Donestsk region.
- 2026-10-08 17:11 [France 24] Russian attack on Ukraine busses part of 'a steady increase in attacks on civilians'
  > Ukrainian President Volodymyr Zelensky said Thursday there would be a response to a Russian strike that hit two buses in the frontline city of Kramatorsk, killing 30 people and wounding 18 others. France 24's Andrew Hilliar says it comes a bid a growing number of Russian attacks on civilians in the 
- 2026-10-08 17:55 [Kyiv Independent] Ukraine war latest: Russian glide bomb strikes in Kramatorsk kill at least 33
  > Key developments on Oct. 8:At least 33 dead after Russian glide bomb strikes Kramatorsk busesRussian drone barrage on Kyiv kills 4, injures 19, disrupts electricity, water suppliesPolish SIM cards found in Russian drones downed in PolandUS, Russia confirm Trump&apos;s latest Ukraine peace push is
**B** (7 item(s))
- 2026-10-07 22:15 [France 24 Español] Francia convoca al embajador iraní por la "desinformación" sobre las protestas estudiantiles
  > El Ministerio de Asuntos Exteriores francés convocó este miércoles 7 de octubre al embajador iraní para protestar contra una "campaña de desinformación llevada a cabo por las autoridades iraníes" con relación a las protestas estudiantiles que han sacudido Francia. La medida se produjo un día después
- 2026-10-08 03:30 [El País Internacional] La guerra en Irán reactiva el conficto civil en Yemen tras cuatro años de tregua
  > Un combatiente del Gobierno yemení, respaldado por Arabia Saudí, dispara un arma montada en un vehículo durante lo que, según las fuerzas gubernamentales, fue un avance contra los hutíes, respaldados por Irán, cerca de Dhubab, en la provincia de Taiz (Yemen), en esta imagen fija extraída de un vídeo
- 2026-10-08 04:34 [Europa Press Internacional] Irán asegura haber acordado con Omán rutas marítimas seguras en el estrecho de Ormuz
  > El portavoz del Ministerio de Exteriores de Irán, Esmail Baqaei, ha anunciado que Teherán y Mascate han alcanzado un acuerdo sobre las coordenadas geográficas para establecer rutas marítimas seguras de entrada y salida en el estrecho de Ormuz, un pacto bilateral que será notificado próximamente ante
- 2026-10-08 07:27 [France 24 Español] En Yemen, los hutíes se muestran tranquilos ante la contraofensiva respaldada por Riad
  > Tras varias semanas de reveses frente a los hutíes, las fuerzas gubernamentales yemenitas intentan recuperar la iniciativa ante los rebeldes proiraníes. Con el apoyo de la aviación saudita, aseguran haber lanzado una contraofensiva "estratégica" durante el fin de semana. Incluso reivindican avances 
- 2026-10-08 12:05 [El País Internacional] Los hutíes de Yemen amenazan a las compañías aéreas para que dejen de volar a Arabia Saudí
  > Una columna de humo se elevaba el 19 de septiembre desde el aeropuerto internacional Rey Jalid de Riad, atacado por primera vez por los hutíes de Yemen.
- 2026-10-08 16:08 [Europa Press Internacional] Los rebeldes yemeníes atacan de nuevo el aeropuerto de Riad, en Arabia Saudí
  > Al menos 23 hutíes heridos en nuevos ataques del Ejército de Yemen en Taiz     MADRID, 8 Oct. (EUROPA PRESS) -      Los rebeldes hutíes de Yemen han reivindicado este jueves un nuevo ataque contra el Aeropuerto Internacional Rey Jalid de Riad, la capital de Arabia Saudí, tras el lanzamiento de un mi
- 2026-10-08 20:24 [France 24 Español] Hutíes de Yemen atacan aeropuertos de Arabia Saudita
  > El Aeropuerto Internacional Rey Khalid suspendió operaciones este 8 de octubre tras nuevos ataques reivindicados por los hutíes de Yemen contra Arabia Saudita. En respuesta, Riad atacó centros de mando, sistemas y depósitos de misiles y armas en distintas ciudades. Los ataques reavivan los temores d

## U006
**A** (2 item(s))
- 2026-10-05 07:40 [ANSA Mondo] Ft, 'l'Estonia sposta le truppe più vicino al confine con la Russia'
  > Il Paese baltico si sta dotando di armi in gradi di colpire in profondità
- 2026-10-05 08:12 [Il Sole 24 Ore Mondo] Guerra in Ucraina, Ft: «Estonia sposta le truppe  al confine con la Russia»
  > Il Paese baltico potenzia le truppe e armamenti contro possibili minacce russe, mentre la Romania attiva caccia spagnoli per un sospetto bersaglio aereo
**B** (3 item(s))
- 2026-10-05 15:05 [Kyiv Independent] Russian drones strike cargo ship in Black Sea, kill captain, Zelensky says
  > Ukrainian President Volodymr Zelensky confirmed that a civilian ship was attacked by two Russian drones, adding that it was a Turkish-owned ship transporting corn.
- 2026-10-05 15:17 [BBC World] Zelensky condemns 'horrific' Russian strike on boat carrying corn in Black Sea
  > The vessel's captain was killed and 11 crew members were rescued after the attack on the Turkish-owned ship, Ukraine's leader says.
- 2026-10-05 20:03 [Al Jazeera] Ukraine says Russian drone attack sinks ship in Romanian waters
  > The latest suspected incursion on NATO&#039;s eastern flank increases fears that the war in Ukraine threatens to spill over.

## U007
**A** (2 item(s))
- 2026-09-29 20:25 [BBC World] Former American Idol contestant and pastor found guilty of murdering wife
  > Caleb Flynn shot his wife, Ashley, dead in their Ohio home in February before saying in a 9/11 call she was killed by burglars.
- 2026-09-30 10:35 [Al Jazeera] Former American Idol contestant found guilty of murdering wife
  > Former American Idol contestant found guilty of murdering wife
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

## U008
**A** (2 item(s))
- 2026-10-05 10:36 [Defense News] Missiles, satellites and warplanes — Ukraine, Europe advance key arms projects
  > WARSAW, Poland — Ukraine’s drone and missile maker Fire Point is developing an extended-range tactical ballistic missile after its FP-7 weapon was used in combat for the first time on Oct. 1, the company’s CEO Iryna Terekh said during this year’s Helsinki Security Forum.As European nations are braci
- 2026-10-05 12:26 [Kyiv Independent] New automatic gun turrets successfully down first Russian jet-powered drones, Air Force says
  > President Volodymyr Zelensky previously announced that twelve such turrets had been installed where Russian jet-powered drones have been particularly active, including around Kyiv.
**B** (3 item(s))
- 2026-10-05 15:05 [Kyiv Independent] Russian drones strike cargo ship in Black Sea, kill captain, Zelensky says
  > Ukrainian President Volodymr Zelensky confirmed that a civilian ship was attacked by two Russian drones, adding that it was a Turkish-owned ship transporting corn.
- 2026-10-05 15:17 [BBC World] Zelensky condemns 'horrific' Russian strike on boat carrying corn in Black Sea
  > The vessel's captain was killed and 11 crew members were rescued after the attack on the Turkish-owned ship, Ukraine's leader says.
- 2026-10-05 20:03 [Al Jazeera] Ukraine says Russian drone attack sinks ship in Romanian waters
  > The latest suspected incursion on NATO&#039;s eastern flank increases fears that the war in Ukraine threatens to spill over.

## U009
**A** (2 item(s))
- 2026-10-03 12:22 [BBC Mundo] Lo que la fallida ejecución de Christa Pike revela sobre la pena de muerte en EE.UU.
  > Christa Pike, una mujer condenada a muerte en Tennessee, sobrevivió a la aplicación de dos inyecciones letales. Su caso ha vuelto a centrar la atención en la pena de muerte y en cómo se aplica en Estados Unidos.
- 2026-10-03 19:14 [Il Sole 24 Ore Mondo] Trump vuole estendere la pena di morte ai narcotrafficanti: il caso Pike riapre lo scontro
  > Il presidente promette di ampliare i reati punibili con la pena capitale. Il Tennessee sospende le esecuzioni dopo il caso Pike, mentre una sentenza della Corte Suprema del 2008 lascia aperto il nodo dei grandi narcotrafficanti
**B** (3 item(s))
- 2026-10-05 11:51 [France 24 Español] Irán entrena a mujeres en las armas ante una posible invasión terrestre
  > En medio de las tensiones con Estados Unidos e Israel, Irán ha puesto en marcha programas de entrenamiento para civiles, incluidas numerosas mujeres, con el objetivo de prepararlas para responder ante una eventual invasión terrestre. En plazas y centros de entrenamiento de Teherán, las participantes
- 2026-10-05 14:49 [El País Internacional] Irán empieza a entrenar a voluntarios civiles para la “defensa nacional”
  > Voluntarias con rifles de asalto del tipo Kaláshnikov, en un curso de entrenamiento militar para civiles en la plaza Imán Hussein de Teherán, este domingo.
- 2026-10-05 15:47 [Europa Press Internacional] El presidente de Irán nombra a Mehrdad Ajlaqi nuevo ministro de Defensa
  > El presidente de Irán, Masud Pezeshkian, ha nombrado este lunes a Mehrdad Ajlaqi nuevo ministro de Defensa del país, por lo que la elección pasa ahora a manos del Parlamento para ser sometida a votación a medida que avanza el conflicto abierto en la región de Oriente Próximo a raíz de la ofensiva la

## U010
**A** (3 item(s))
- 2026-09-30 11:32 [Al Jazeera] Russian attacks on Ukraine’s Kyiv region kill four, target power grid
  > City officials say three killed in Ukraine&#039;s capital, as emergency services say child killed in the surrounding region.
- 2026-09-30 11:47 [BBC World] Russia launches largest attack on Ukraine energy infrastructure since spring
  > In total 11 regions of the country were attacked overnight, with residential buildings and railways also targeted, the Ukrainian PM says.
- 2026-10-01 12:13 [Defense News] Ukraine has struck Russian factory vital for Moscow’s missiles, private intelligence firm says
  > GLASGOW, Scotland — A Russian factory that Ukraine struck on Sept. 26 supplies electronics for a wide range of Russia’s missiles, potentially leaving Moscow without a fallback supplier, according to leaked documents obtained by the Ukrainian private intelligence firm Dallas Analytics.The documents a
**B** (4 item(s))
- 2026-09-30 14:19 [South China Morning Post] Russia sends nuclear warning to Nato over its Kaliningrad enclave
  > Russia has warned Nato it would be ready to resort to nuclear weapons if the Western alliance attempted to cut off Kaliningrad, a Russian exclave that borders the Baltic Sea.
In a document sent to Nato and seen by Reuters, Moscow accused the alliance of a “dangerous and reckless course” that entaile
- 2026-09-30 18:52 [Al Jazeera] Russia warns NATO of possible nuclear response if Kaliningrad is cut off
  > Moscow claims that NATO is preparing an air and naval blockade in the Baltic Sea.
- 2026-10-01 18:09 [BBC World] Putin warns West that Russia is ready to use every weapon to protect Kaliningrad
  > The Russian leader insists Moscow is "not threatening anyone" and is merely responding to statements by Western leaders.
- 2026-10-01 21:09 [South China Morning Post] Putin warns Russia will use ‘all weapons’ in arsenal if any of its territory is attacked
  > President Vladimir Putin on Thursday reiterated Moscow’s long-held position that Russia is not planning to attack European countries but will respond to aggression with “all weapons” in its arsenal.
In remarks at a foreign policy forum, Putin accused the West and Europe of escalating tensions by tal

## U011
**A** (8 item(s))
- 2026-09-29 14:40 [Defense News] US forces exiting Iraq after 2 decades, leaving opening for Iran
  > U.S. forces are set to depart from their last bases in Iraq by Wednesday, a move celebrated as a victory by Iran and its allies, who now have deep influence in the country where 4,500 Americans died during more than two decades of war.Iraqi security experts say the withdrawal — agreed to in 2024 und
- 2026-09-29 20:00 [Al Jazeera] US troops fully withdraw from Baghdad base after two decades
  > US Army soldiers have fully withdrawn from the US base in Baghdad.
- 2026-09-30 09:46 [South China Morning Post] US ends troop mission in Iraq, Baghdad to celebrate Sovereignty Day on October 1
  > A US-led coalition deployed in Iraq more than a decade ago to fight jihadists concluded its mission on Wednesday, a move celebrated by the country’s leaders, but which some fear will embolden pro-Iran armed factions.
Coalition troops deployed to Iraq and Syria in 2014 to fight Islamic State, which h
- 2026-09-30 11:36 [BBC World] Last UK and US troops leave Iraq as anti-Islamic State mission ends
  > The withdrawal of coalition forces, under a deal agreed two years ago, was a key demand of the Iraqi government.
- 2026-09-30 12:17 [Al Jazeera] Iraq celebrates National Sovereignty Day as US troops withdraw
  > Iraq’s security forces held parades in Baghdad and Najaf to celebrate ‘Sovereignty Day’ as US troops withdraw.
- 2026-09-30 14:04 [Breaking Defense] US withdraws last remaining troops out of Iraq
  > “As we step back and hand full primary responsibility for Iraq’s security to the Government of Iraq and the brave people of Iraq, US and Coalition forces stationed across the region will remain ready to respond to any ISIS threats that arise,” CENTCOM Commander Adm. Brad Cooper said.
- 2026-09-30 16:33 [Al Jazeera] Pentagon says US troop withdrawal from Iraq is complete
  > The withdrawal ends two decades of foreign intervention in Iraq as part of &#039;global war on terror&#039; and anti-ISIL fight.
- 2026-10-01 01:11 [Al Jazeera] Iraq celebrates Sovereignty Day as US troops complete withdrawal
  > Night time celebrations filled the air as Iraqis observed the start of a four-day holiday.
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

## U012
**A** (6 item(s))
- 2026-09-30 16:51 [South China Morning Post] UK PM says ‘strong indications’ Iran involved in bomb scare at US-run airbase
  > British Prime Minister Andy Burnham on Wednesday said there were “strong indications” that Iran was involved in suspicious activity at a UK airbase that triggered a major security incident this weekend.
“There are strong indications that Iran played a part in what happened over the weekend at RAF Fa
- 2026-09-30 18:09 [Al Jazeera] Strong indications’ Iran linked to suspected UK airbase plot
  > UK Prime Minister says there are ‘strong indications’ Iran played a part in the suspected RAF Fairford airbase plot.
- 2026-10-01 02:30 [Al Jazeera] UK says Iran may be linked to alleged airbase plot, drawing angry denial
  > Andy Burnham says UK has &#039;strong indications&#039; Iran involved in alleged security incident at RAF base used by US.
- 2026-10-01 16:55 [Al Jazeera] British police arrest UK-Iranian national over airbase incident
  > Counter Terrorism police also questioned a UK national, days after five others were arrested and released on bail.
- 2026-10-01 17:52 [South China Morning Post] UK-Iranian man arrested over suspected Fairford airbase plot
  > British counterterrorism police investigating ⁠a suspected plot involving ⁠an airbase used by the US ⁠to target Iran said on Thursday they had arrested a dual UK-Iranian national on suspicion of preparing terrorist acts.
In an incident which triggered a huge police response, raised alarm among Weste
- 2026-10-03 10:45 [BBC World] UK-Iranian dual national bailed after RAF Fairford incident arrest
  > The 25-year-old man was arrested in the London borough of Westminster on Thursday.
**B** (6 item(s))
- 2026-10-02 01:23 [Al Jazeera] Trump says US may ask Europe to release diesel reserves
  > Skyrocketing diesel prices have pushed Washington to weigh an export ban, raising alarm across European economies.
- 2026-10-02 05:26 [BBC World] US pressures Europe over diesel reserves as Trump threatens export ban
  > President Donald Trump has threatened to ban diesel exports in a bid to ease prices in the US ahead of the November elections.
- 2026-10-02 13:16 [Al Jazeera] Trump vs Europe as US presses for release of emergency diesel stocks
  > Europe&#039;s leaders are mulling proposals to respond to Trump&#039;s diesel demands.
- 2026-10-02 14:51 [South China Morning Post] G7 nations agree to release diesel and oil stocks after Trump pressure
  > Group ⁠of Seven countries agreed on Friday to release 100 million barrels of diesel and crude oil from emergency reserves and pledged to refrain from energy export restrictions after pressure from US President Donald Trump.
The US led a pressure campaign on the European Union to draw down emergency 
- 2026-10-02 19:01 [Al Jazeera] Trump says Europe agreed to release ‘massive amount’ of diesel reserves
  > US President Donald Trump says Europe agreed to release a ‘massive amount’ of diesel from emergency stockpiles.
- 2026-10-02 20:25 [BBC World] G7 to release 100 million barrels of oil and diesel after Trump export ban threat
  > The co-ordinated release is aimed at heading off further price spikes and avoiding a ban on US diesel exports.

## U013
**A** (2 item(s))
- 2026-10-04 15:06 [Al Jazeera] Iran tells US: there is ‘no military solution’ to end the war
  > Iranian Foreign Minister Abbas Araghchi says the era of “wasting time and dictating demands is over’.
- 2026-10-04 19:44 [South China Morning Post] Iran tells US there is no military solution to Middle East war
  > Iran’s top diplomat insisted on Sunday that there would be no military solution to the United States’ war against the Islamic republic, with talks on ending the conflict apparently at an impasse.
A campaign of heavy bombardment failed to bring a decisive close to the war launched by the US and Israe
**B** (5 item(s))
- 2026-10-04 23:23 [Clarín Mundo] Alerta en Rusia: murió una científica por un accidente con bacterias en un laboratorio y debieron aislar a 200 personas
  > Contó que se le rompió un tubo de ensayo recolectando muestras para analizar.Autoridades rusas dicen que el frío impediría la transmisión de un tipo de neumonía.Los funcionarios hablan de "una peste no especificada" y "una infección particularmente peligrosa".
- 2026-10-05 06:53 [Europa Press Internacional] Rusia asegura que la situación epidemiológica en Irkutsk es "estable" tras un supuesto accidente en un laboratorio
  > Las autoridades de Rusia han asegurado que la situación epidemiológica en la región de Irkutsk es "estable", después de activar una serie de medidas de emergencia durante los últimos días a causa de la muerte de una investigadora en un presunto accidente de laboratorio en Shelejov.
- 2026-10-05 10:17 [El País Internacional] Rusia pone bajo observación a cientos de personas tras morir una investigadora de un laboratorio contra la peste
  > Trabajos de desinfección de coranavirus en la estación de tren de Yaroslavsky en Moscú, el 10 de noviembre de 2022.
- 2026-10-05 14:34 [Europa Press Internacional] EEUU pide a Rusia compartir información "de forma rápida y transparente" tras supuesto caso de peste en Irkutsk
  > El Departamento de Estado estadounidense ha instado este lunes a las autoridades de Rusia a compartir información "de forma rápida y transparente" sobre el caso de presunta peste pulmonar en la región de Irkutsk, tras la muerte de una investigadora en un presunto accidente de laboratorio en Shelejov
- 2026-10-05 21:21 [BBC Mundo] EE.UU. "sigue de cerca" el caso de una científica rusa que falleció en un centro de investigación de la peste en Siberia
  > El secretario de Estado, Marco Rubio, expresó su preocupación de que el incidente pudiera haber provocado la propagación de la peste neumónica, aunque señaló que no había motivos para alarmarse.

## U014
**A** (56 item(s))
- 2026-10-04 03:30 [El País Internacional] Ni Bolsonaro, ni Lula: Trump se reserva (de momento) su apoyo en las elecciones de Brasil
  > Un asistente a un mitin de Flavio Bolsonaro disfrazado de Trump, el pasado domingo.
- 2026-10-04 04:00 [El País Internacional] La disputa entre Lula y Trump marca las elecciones brasileñas
  > Banderas de Flavio Bolsonaro y Luiz Inacio Lula da Silva en Brasilia, el 29 de septiembre.
- 2026-10-04 11:20 [Rai News Esteri] Urne aperte in Brasile per le elezioni presidenziali e legislative, sfida Lula-Bolsonaro
  > Gli ultimi sondaggi davano un testa a testa
- 2026-10-04 20:19 [El País Internacional] Brasil decide su futuro entre Lula y Bolsonaro, un estadista desgastado y el hijo de un ultra
  > El presidente Lula, el día 24 en São Gonçalo, y Flávio Bolsonaro, este sábado en Río.
- 2026-10-04 20:43 [Europa Press Internacional] Bolsonaro gana la primera vuelta en Brasil con el 47% de los votos y disputará contra Lula (45%) la segunda vuelta
  > El candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil e hijo del expresidente Jair Bolsonaro, Flávio Bolsonaro, ha ganado la primera vuelta de las elecciones en Brasil con un 47,17% de los sufragios. Su rival y presidente saliente, Luiz Inácio Lula da Silva, ha quedado cua
- 2026-10-04 22:25 [ANSA Mondo] Media, Lula e Bolsonaro andranno al ballottaggio il 25 ottobre
  > A metà scrutinio Bolsonaro al 49%, Lula a 42%
- 2026-10-04 23:00 [Clarín Mundo] Los Bolsonaro amplían su presencia en el Congreso con las elecciones en Brasil: entran la esposa del ex presidente y dos hermanos de Flavio
  > Michelle, la exprimera dama brasileña alcanzó el 28% de los votos en las elecciones legislativas del Distrito Federal.Otros dos hijos del expresidente Jair Bolsonaro compitieron por bancas legislativas en el estado de Santa Catarina.
- 2026-10-04 23:23 [Clarín Mundo] Elecciones en Brasil: Flávio Bolsonaro, un presidenciable a la sombra de su padre
  > Tiene 45 años y es el mayor de los cinco hijos del ex presidente. Elogia las políticas de seguridad de Nayib Bukele en El Salvador y promete la construcción de numerosas cárceles. Asimismo, presume de su buena relación con Donald Trump tras mantener una reunión privada en la Casa Blanca.
- 2026-10-04 23:23 [Clarín Mundo] Lula da Silva busca su reelección en Brasil: entre el freno a la ultraderecha y la defensa de su legado social
  > • A los 80 años, el mandatario brasileño busca la reelección apoyado en su historial de programas sociales como el Bolsa Familia, que actualmente beneficia a una cuarta parte de la población.
• Con vistas a un nuevo período, impulsa una reforma laboral para reducir la jornada semanal a cinco días y 
- 2026-10-05 00:09 [Rai News Esteri] Il sorpasso di Bolsonaro, la crisi di Lula
  > Flavio Bolsonaro, figlio dell'ex presidente di estrema destra tentato golpista, vince il primo turno sul presidente di sinistra Lula da Silva
- 2026-10-05 00:12 [Clarín Mundo] Elecciones en Brasil: un voto castigo que sorprendió a Lula da Silva y llegó desde su base tradicional de votantes
  > Un primer análisis indica que los sectores de menores ingresos se distanciaron de la elección y del líder del PT. El país es un éxito macro, con números notables, pero esos resultados no llegaron a los bolsillos de ese amplio espacio de votantes que se endeuda para pagar los gastos básicos.
- 2026-10-05 01:03 [Clarín Mundo] Lula acepta el impacto del triunfo de Bolsonaro: fue "un resultado inesperado"
  > El representante del socialista Partido de los Trabajadores busca su cuarto mandato, con la reelección en la gestión actual.Quedó detrás de Flavio Bolsonaro por apenas 2,15 puntos.
- 2026-10-05 01:08 [Clarín Mundo] Flavio Bolsonaro, tras ganar en primera vuelta ante Lula: "Brasil quiere un cambio"
  > Aseguró también que este resultado marcan "el fin de la era del PT" en su país.Dijo estar "feliz" con los números obtenidos frente al actual mandatario, Lula da Silva.
- 2026-10-05 01:41 [El País Internacional] Arrasadora victoria de la derecha en Brasil
  > Flavio Bolsonaro habla con la prensa en Río de Janeiro, este domingo.
- 2026-10-05 02:13 [Europa Press Internacional] Bolsonaro proclama "fin de la era del PT" y Lula apela a combatir su "pasado tenebroso" en la segunda vuelta en Brasil
  > Bolsonaro supera los 55 millones de apoyos (47,04%) y logra una ventaja de 2,3 millones de sufragios sobre el actual mandatario (45,15%)
- 2026-10-05 02:28 [El País Internacional] El apellido Bolsonaro gana desde la cárcel
  > Flávio Bolsonaro, candidato presidencial de Brasil, este domingo tras los resultados de la primera vuelta.
- 2026-10-05 02:39 [BBC Mundo] Cómo se compara Flávio Bolsonaro con su padre Jair y cuánto cambia el duelo con Lula por la presidencia de Brasil 4 años después
  > El senador derechista pasa fortalecido al balotaje contra el presidente de izquierda tras obtener más votos en la primera vuelta contra varios pronósticos, pero la elección sigue abierta.
- 2026-10-05 02:46 [France 24 Español] Simone Pitta: "Con esta primera vuelta se puede ver una consolidación del bolsonarismo en Brasil"
  > Pese a no haber estado en el poder en el último periodo presidencial de Brasil, y pese a las denuncias y condenas contra el expresidente Jair Bolsonaro por un intento de golpe de Estado, el bolsonarismo logró consolidarse de cara a los comicios de este 4 de octubre. Ahora, Flávio Bolsonaro busca pos
- 2026-10-05 02:47 [France 24 Español] Juan Agulló: "A diferencia de otros países de Latinoamérica, Brasil es un competidor directo"
  > En un escenario marcado por la polarización en Brasil, el candidato de ultraderecha y heredero político de su padre, Flávio Bolsonaro, y el actual presidente, Luiz Inácio Lula da Silva, quien busca un cuarto mandato, se disputan el balotaje. La sombra de Estados Unidos estuvo presente durante la pri
- 2026-10-05 02:54 [El País Internacional] Bolsonaro vence a Lula en primera vuelta de las elecciones y acaricia el retorno de la ultraderecha al poder en Brasil
  > Flávio Bolsonaro habla tras clasificarse para la segunda vuelta en Brasilia, Brasil, este domingo.
- 2026-10-05 03:19 [France 24 Español] Brasil: la derecha de Bolsonaro se fortalece en las regiones, con un triunfo holgado en São Paulo
  > Los comicios locales de Brasil se saldaron este domingo con un avance de la derecha que representan el candidato presidencial Flávio Bolsonaro y sus aliados. En tanto la izquierda del presidente y aspirante a la reelección, Luiz Inácio Lula da Silva perdía terreno. La victoria más cómoda fue en São 
- 2026-10-05 03:36 [El País Internacional] Las claves de la primera vuelta en Brasil: de la fuerza ultra al día después de Lula con América Latina pendiente
  > Flávio Bolsonaro vota en Río de Janeiro, este domingo.
- 2026-10-05 03:41 [France 24 Español] Flávio Bolsonaro tritura las encuestas: una ventaja pequeña, pero un escenario cuesta arriba para Lula
  > Brasil quedó inclinado hacia la tendencia de retorno a la derecha que sacude a América Latina, luego de que el senador e hijo del expresidente Jair Bolsonaro aventajara por casi dos puntos al izquierdista Luiz Inácio Lula da Silva en la primera vuelta de las elecciones. Lula ha reconocido el resulta
- 2026-10-05 04:08 [El País Internacional] Videoanálisis | Lula se enfrenta a una segunda vuelta electoral muy complicada
  > Videoanálisis | Lula Y Flávio Bolsonaro se enfrenta a una segunda vuelta electoral
- 2026-10-05 04:33 [Rai News Esteri] Brasile, avanzata del clan Bolsonaro: quattro eletti in Parlamento, Flavio al ballottaggio con Lula
  > L'ex first lady Michelle e Carlos, uno dei figli dell'ex presidente, conquistano un seggio al Senato. Alla Camera entrano il figlio più giovane Jair Renan e Renato, fratello di Jair
- 2026-10-05 05:14 [Il Sole 24 Ore Mondo] Brasile, Bolsonaro vince al primo turno con 47%, Lula al 45%: ballottaggio il 25 ottobre
  > Flavio Bolsonaro batte Lula al primo turno e si lancia come favorito nel ballottaggio del 25 ottobre che deciderà chi sarà il 40esimo presidente del Brasile. Il candidato trumpiano ha ottenuto il 47,14 % dei voti, il presidente uscente il 45.03 %, con una differenza tra i due di circa 2 milioni e me
- 2026-10-05 05:31 [Europa Press Internacional] Trump tacha de "corruptas" las elecciones de EEUU comparándolas con las de Brasil tras la victoria de Bolsonaro
  > El presidente de Estados Unidos, Donald Trump, ha vuelto a cargar contra el proceso electoral en su propio país, tachándolo de corrupto y contraponiéndolo la rapidez en el escrutinio de los votos de 125 millones de personas "en la primera vuelta de las elecciones presidenciales de Brasil", donde el 
- 2026-10-05 05:46 [Europa Press Internacional] Milei felicita a su "querido amigo" Flávio Bolsonaro por su "histórica elección" frente a Lula en Brasil
  > El presidente de Argentina, Javier Milei, ha felicitado al candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil, Flávio Bolsonaro, por su victoria en la primera vuelta de las elecciones presidenciales celebradas este domingo, en las que se ha impuesto con el 47,03% de los vo
- 2026-10-05 06:44 [ANSA Mondo] Brasile, l'ex giudice che condannò Lula eletto governatore
  > Sergio Moro guiderà l'esecutivo del suo stato natale, il Paranà
- 2026-10-05 07:14 [BBC Mundo] Elecciones en Brasil: Flávio Bolsonaro y Lula da Silva van a una segunda vuelta en la que el presidente enfrenta una difícil remontada
  > La mayor democracia de América Latina irá a balotaje el 25 de octubre. Lula lleva la desventaja frente a Bolsonaro, ya que históricamente nunca hubo una remontada en una segunda vuelta electoral en Brasil.
- 2026-10-05 07:46 [ANSA Mondo] In Brasile un 30enne di destra è il deputato più votato della storia
  > Nikolas Ferreira ha raccolto oltre 3,1 milioni di preferenze per la Camera
- 2026-10-05 10:46 [ANSA Mondo] Astensione record in Brasile, il 21,08% non ha votato al primo turno
  > Si tratta del livello più alto registrato dalle elezioni del 1998 (21,5%)
- 2026-10-05 11:42 [France 24 Español] Brasil irá a segunda vuelta: Flávio Bolsonaro lidera la primera ronda
  > Brasil se encamina a una segunda vuelta presidencial tras una elección marcada por la polarización. El senador Flávio Bolsonaro obtuvo el primer lugar en la primera vuelta, pero sin alcanzar la mayoría necesaria para evitar el balotaje. El próximo 25 de octubre se enfrentará al actual presidente, Lu
- 2026-10-05 12:20 [Rai News Esteri] Il primo turno delle presidenziali in Brasile, avanti Bolsonaro: ribaltati i pronostici pro-Lula
  > La sfida per il secondo turno del 25 ottobre è ancora aperta ma il presidente uscente non minimizza il peso di una pesante bocciatura delle sue politiche
- 2026-10-05 12:21 [Rai News Esteri] Presidenziali in Brasile, Flavio Bolsonaro a sorpresa supera Lula di 2 punti. Si va al ballottaggio
  > Il candidato di destra al 47%: "Il Brasile vuole cambiare". Il presidente uscente al 45%: "Sono bravo ai supplementari". Scelta rinviata al secondo turno del 25 ottobre
- 2026-10-05 12:29 [Clarín Mundo] Elecciones en Brasil 2026, EN VIVO: reacciones tras la victoria de Flávio Bolsonaro sobre Lula y últimas noticias del balotaje
  > Bolsonaro se impuso en la primera vuelta al superar por casi dos puntos al actual presidente Lula da Silva. El balotaje entre ambos se hará el 25 de octubre. Todas las repercusiones, minuto a minuto.
- 2026-10-05 12:31 [Clarín Mundo] Quién es Flávio Bolsonaro, el hijo de Jair que sorprendió a Lula y va por la presidencia de Brasil
  > Nacido en el estado de Río de Janeiro, Flávio es el mayor de los cinco hijos del expresidente y el que más se le parece físicamente.Este senador, de 45 años, enfrentará a Lula en el balotaje el próximo 25 de octubre.
- 2026-10-05 13:05 [France 24 Español] Informe desde Río de Janeiro: el Partido Liberal de Bolsonaro se fortalece en el Senado
  > Las elecciones legislativas en Brasil dejaron un resultado clave para el futuro político del país: el Partido Liberal (PL), formación vinculada al expresidente Jair Bolsonaro y que postuló a Flávio Bolsonaro para la Presidencia, amplió significativamente su presencia en el Senado. La bancada pasará 
- 2026-10-05 13:16 [Clarín Mundo] Elecciones en Brasil: los mercados celebran la ventaja de Flávio Bolsonaro sobre Lula y el principal índice de la Bolsa marca un nuevo récord
  > Los activos brasileños se dispararon este lunes y el real se apreció en la primera sesión de los mercados tras los comicios del domingo. El índice Ibovespa superó la marca de los 209.000 puntos por primera vez.
- 2026-10-05 13:57 [BBC Mundo] Quiénes son Lucas Pavanato y Nikolas Ferreira, los jóvenes influencers de derecha que lograron las mayores votaciones en la historia de la Cámara de Diputados de Brasil
  > Los flamantes legisladores comparten una agenda conservadora que incluye el rechazo a las políticas de género, el endurecimiento de las sanciones penales y la legalización del porte de armas como herramienta para combatir la delincuencia.
- 2026-10-05 14:50 [Clarín Mundo] Elecciones en Brasil: los resultados del domingo cambian por completo el diseño del país y ya asoma una amnistía para Jair Bolsonaro
  > La victoria del candidato conservador Flávio Bolsonaro sobre el presidente Lula da Silva en primera vuelta excede lo que pueda ocurrir en el balotaje.La ola de derecha se consolida con victorias en las gobernaciones y especialmente en el Parlamento.Aun si el líder petista lograra imponerse el 25 de 
- 2026-10-05 15:47 [Clarín Mundo] La reacción de los medios en Brasil tras la victoria de Bolsonaro: desde "el ciclo de Lula está terminado" hasta "el tsunami de lo peor de la derecha"
  > Los títulos, opiniones y análisis de la prensa en Brasil tras la primera vuelta de las presidenciales de este domingo.
- 2026-10-05 15:59 [France 24 Español] Flávio Bolsonaro y Lula da Silva se preparan para el balotaje en Brasil
  > 🇧🇷🗳️ Luiz Inácio Lula da Silva y Flávio Bolsonaro ofrecieron declaraciones después de que los resultados de los comicios presidenciales de Brasil confirmaran que deberán disputar el balotaje del 25 de octubre.
- 2026-10-05 16:02 [El País Internacional] El lulismo cruje ante la ofensiva ultra
  > Carteles del presidente Trump y del candidato Flavio Bolsonaro, en São Paulo, Brasil, este Lunes.
- 2026-10-05 16:10 [France 24 Español] "Solo faltan días para el rescate Brasil": Bolsonaro celebra la victoria sobre Lula
  > El senador del Partido Liberal (PL) y candidato presidencial, Flávio Bolsonaro, agradeció este lunes "a Dios" y al pueblo brasileño por su victoria en las elecciones del domingo ante el presidente Luiz Inácio Lula da Silva, en contra de los pronósticos. Además, celebró que el PL resultara el partido
- 2026-10-05 16:23 [Clarín Mundo] Elecciones en Brasil: a contrarreloj, Lula y el PT analizan cambios totales en la estrategia de campaña
  > Lo anticipan fuentes partidarias, pero no es claro en qué consistirán. Trascendió que ha habido tensiones internas sobre el manejo de la campaña.Y que debido a eso se perdieron oportunidades importantes para reducir el impulso del candidato opositor, Flávio Bolsonaro.
- 2026-10-05 16:36 [France 24 Español] Paraguay, refugio fiscal y político para la extrema derecha brasileña
  > En los últimos cinco años, las solicitudes de permisos de residencia de brasileños en Paraguay se han más que duplicado. Muchos de los recién llegados son simpatizantes de Jair Bolsonaro que temen una reelección del actual presidente, Luiz Inácio Lula da Silva, a quien responsabilizan de un deterior
- 2026-10-05 17:02 [ANSA Mondo] Brasile, Erika Hilton è la donna più votata della storia alla Camera
  > La politica brasiliana Erika

Hilton ha stabilito un nuovo record nella storia della Camera

dei deputati brasiliana, diventando la donna più votata di

sempre. La deputata trans del Partito socialismo e libertà

(Psol) di San Paolo è stata rieletta con 1.596.472 voti, pari al

5,9% dei voti espress
- 2026-10-05 17:30 [Clarín Mundo] El fantasma de Bolsonaro reaparece en Europa: los temores de Bruselas ante un eventual cambio de gobierno en Brasil
  > • Un cambio de gobierno en Brasil aportaría argumentos a los eurodiputados que buscan frenar la ratificación del entendimiento comercial.
• Si entre 50 y 80 legisladores modifican su postura en la votación prevista para los próximos meses, la aplicación provisional del pacto quedará suspendida.
- 2026-10-05 18:04 [France 24 Español] El mercado de valores de Brasil aplaude la ventaja de Bolsonaro en primera vuelta presidencial
  > El índice bursátil iBovespa, el más importante de la bolsa de São Paulo inició la jornada con un alza estrepitosa de casi el 9% y alcanzó máximo histórico, mientras el real brasileño gana 4,5% frente al dólar a media jornada, hasta situarse ligeramente por encima de los 5 reales por dólar. El buen r
- 2026-10-05 18:10 [France 24 Español] La dinastía Bolsonaro se fortalece: prensa brasileña sobre la primera vuelta electoral
  > La familia Bolsonaro no solo ganó la primera vuelta en Brasil, fortaleció su presencia en ambas cámaras del Congreso y conserva los respaldos de más de 10 gobernadores. 'O Globo' habla del bloque familiar que se ha hecho con varios cargos. Hermanos, hijos, esposa y exesposa tienen un puesto de elecc
- 2026-10-05 19:41 [El País Internacional] La ola conservadora de América Latina llega a Brasil
  > Flávio Bolsonaro (i) junto al presidente de EE.UU., Donald Trump, en el despacho oval de la Casa Blanca en Washington, el 26 de mayo de 2026.
- 2026-10-05 19:42 [El País Internacional] La victoria en primera vuelta de Bolsonaro impulsa a la ola ultra de América Latina
  > Transeúntes pasan ante pósteres dañados que muestran a Bolsonaro hijo con el presidente Trump, este lunes en São Paulo.
- 2026-10-05 19:47 [Clarín Mundo] Elecciones en Brasil: las urnas de la sorpresa
  > Tras el imprevisto triunfo de Flávio Bolsonaro sobre Lula en la primera vuelta, Brasil se encamina hacia un balotaje decisivo el próximo 25 de octubre. La contienda electoral ratifica la profunda polarización política del país y la consolidación del bolsonarismo como una fuerza de derecha permanente
- 2026-10-05 20:21 [ANSA Mondo] Trump, il risultato di Bolsonaro in Brasile una 'grande vittoria'
  > Il risultato di Flavio Bolsonaro

alle elezioni in Brasile è stata una "grande vittoria". Lo ha

detto Donald Trump.Quella di Bolsonaro "è una grande vittoria: combattuta, ma una

vittoria davvero enorme. Incredibile", ha detto Trump. Bolsonaro

si avvia al ballottaggio del 25 ottobre come favorito.
- 2026-10-05 22:09 [ANSA Mondo] Brasile, l'ex presidente Temer sostiene Bolsonaro al ballottaggio
  > L'ex presidente brasiliano

Michel Temer (2016-2018) ha dichiarato il suo sostegno a Flávio

Bolsonaro in vista del ballottaggio del 25 ottobre contro Luiz

Inácio Lula da Silva. In un video diffuso sui social, Temer ha

affermato che il risultato del primo turno mostra la volontà

degli elettori di
**B** (2 item(s))
- 2026-10-05 14:08 [South China Morning Post] France, Germany call for new weapon allowing ‘immediate cut off’ of China from EU market
  > In the strongest sign yet of a shifting European Union policy on China, the leaders of France and Germany have demanded a new trade weapon that would cut off access to the EU market when third countries cause severe distortions.
The tool would effectively act as a kill switch, allowing Brussels to r
- 2026-10-05 17:01 [France 24] France, Germany seek new EU rapid response tool against trade threats
  > France and Germany proposed a new legal tool to enable the EU to respond rapidly to trade wars or measures, such as dumping, that could economically harm the bloc. While French President Emmanuel Macron and German Chancellor Friedrich Merz said the proposal was not a direct response to the actions o

## U015
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
**B** (6 item(s))
- 2026-10-02 01:23 [Al Jazeera] Trump says US may ask Europe to release diesel reserves
  > Skyrocketing diesel prices have pushed Washington to weigh an export ban, raising alarm across European economies.
- 2026-10-02 05:26 [BBC World] US pressures Europe over diesel reserves as Trump threatens export ban
  > President Donald Trump has threatened to ban diesel exports in a bid to ease prices in the US ahead of the November elections.
- 2026-10-02 13:16 [Al Jazeera] Trump vs Europe as US presses for release of emergency diesel stocks
  > Europe&#039;s leaders are mulling proposals to respond to Trump&#039;s diesel demands.
- 2026-10-02 14:51 [South China Morning Post] G7 nations agree to release diesel and oil stocks after Trump pressure
  > Group ⁠of Seven countries agreed on Friday to release 100 million barrels of diesel and crude oil from emergency reserves and pledged to refrain from energy export restrictions after pressure from US President Donald Trump.
The US led a pressure campaign on the European Union to draw down emergency 
- 2026-10-02 19:01 [Al Jazeera] Trump says Europe agreed to release ‘massive amount’ of diesel reserves
  > US President Donald Trump says Europe agreed to release a ‘massive amount’ of diesel from emergency stockpiles.
- 2026-10-02 20:25 [BBC World] G7 to release 100 million barrels of oil and diesel after Trump export ban threat
  > The co-ordinated release is aimed at heading off further price spikes and avoiding a ban on US diesel exports.

## U016
**A** (14 item(s))
- 2026-10-07 12:00 [UN News] Ukraine: UN condemns latest attacks and calls for civilian protection
  > The UN Humanitarian Coordinator for Ukraine on Wednesday&nbsp;called for an end to attacks against civilians following further overnight strikes by Russian forces that reportedly killed at least 19 in the Chernihiv Region.
- 2026-10-08 07:26 [Kyiv Independent] General Staff: Russia has lost 1,547,780 troops in Ukraine since Feb. 24, 2022
  > The number includes 1,880 casualties that Russian forces suffered over the past day.
- 2026-10-08 09:12 [Kyiv Independent] At least 12 dead after Russian glide bomb strikes Kramatorsk bus stop
  > "Russia comes to the Ukrainian land with death," Donetsk Governor Vadym Filashkin said.
- 2026-10-08 09:54 [Kyiv Independent] Russian drone barrage on Kyiv kills 3, injures 13, disrupts electricity, water supplies
  > At 10:00 a.m. local time, Ukraine’s biggest private energy firm DTEK announced emergency energy shutdowns in Brovary, Buchanskyi, Vyshgorod, and Boryspil districts of the capital.
- 2026-10-08 10:08 [France 24] Dozens killed in Russian strike on buses in Ukraine's Kramatorsk as Kyiv targets data centre
  > At least 30 people were killed in a Russian strike on two buses in the Ukrainian city of Kramatorsk in the eastern Donetsk region on Thursday. Earlier, a drone hit a data centre belonging to Russian technology company Yandex, causing a fire.
- 2026-10-08 10:16 [BBC World] Russian strike on buses kills 33, say officials, as deadly attacks on Ukraine surge
  > Ukraine accused Russia of targeting the crowded bus in the frontline city to kill as many civilians as possible.
- 2026-10-08 10:31 [Al Jazeera] Russian attack on Ukraine’s Kramatorsk kills at least 12 people
  > Fourteen people were wounded in the Russian strike on city in eastern Ukraine&#039;s Donetsk region, local authorities say.
- 2026-10-08 11:43 [Kyiv Independent] Russian strikes kill at least 10, injure 45 across Ukraine over past day
  > Russia attacked across Ukraine with 142 Shahed-type drones, 82 of which were jet-powered overnight on Oct. 8, Ukraine's Air Force said.
- 2026-10-08 12:00 [South China Morning Post] At least 33 dead in Russian bomb blast in east Ukraine stronghold
  > A ⁠Russian bomb attack on ⁠the eastern Ukrainian city of Kramatorsk ⁠killed at least 33 people, authorities said on Thursday, describing it as a targeted strike on civilians in the key stronghold sought by Moscow.
Another 18 people were wounded in one of the largest single attacks this year, ‌which 
- 2026-10-08 13:44 [France 24] 30 dead in strike on Ukraine bus as Russian attacks intensify
  > Thirty people were killed and at least 18 were injured by Russian strikes in eastern Ukraine that included an attack on a public bus, authorities said Thursday, as an intensive pre-winter wave of attacks continued.
- 2026-10-08 14:50 [Al Jazeera] More killed in Kramatorsk as Russia targets Ukraine’s transportation system
  > Russia’s attacks on trains, buses and ports are paralysing Ukraine’s transport network and endangering civilians.
- 2026-10-08 17:07 [Al Jazeera] Dozens killed in Russian strike on civilian buses in eastern Ukraine
  > At least 33 people were killed after a Russian strike hit two civilian buses in a city within the Donestsk region.
- 2026-10-08 17:11 [France 24] Russian attack on Ukraine busses part of 'a steady increase in attacks on civilians'
  > Ukrainian President Volodymyr Zelensky said Thursday there would be a response to a Russian strike that hit two buses in the frontline city of Kramatorsk, killing 30 people and wounding 18 others. France 24's Andrew Hilliar says it comes a bid a growing number of Russian attacks on civilians in the 
- 2026-10-08 17:55 [Kyiv Independent] Ukraine war latest: Russian glide bomb strikes in Kramatorsk kill at least 33
  > Key developments on Oct. 8:At least 33 dead after Russian glide bomb strikes Kramatorsk busesRussian drone barrage on Kyiv kills 4, injures 19, disrupts electricity, water suppliesPolish SIM cards found in Russian drones downed in PolandUS, Russia confirm Trump&apos;s latest Ukraine peace push is
**B** (12 item(s))
- 2026-10-07 23:32 [Rai News Esteri] La protesta degli studenti blocca licei e università in Francia
  > Poche le risorse stanziate dal premier Le Corneu per la scuola pubblica così i ragazzi tornano in piazza e chiedono un incontro con il governo
- 2026-10-07 23:45 [Europa Press Internacional] Lecornu defiende la actuación policial ante los disturbios en Francia y promete diálogo ante las protestas estudiantiles
  > El primer ministro de Francia, Sébastien Lecornu, ha defendido este miércoles la labor de las fuerzas del orden durante las protestas estudiantiles de las últimas dos semanas, asegurando que su misión es "proteger a los jóvenes" y mantener el Estado de derecho, frente a las acusaciones de represión 
- 2026-10-08 02:27 [France 24 Español] Francia: Ejecutivo anuncia que mantendrá fuerza policial contra manifestaciones estudiantiles
  > Con cientos de miles de estudiantes movilizados en las calles, cientos de colegios cerrados y, tras más de dos semanas de protestas, el primer ministro francés, Sébastien Lecornu, reconoció este miércoles 7 de octubre que "la ira de los jóvenes no surge de la nada". Mientras las manifestaciones se m
- 2026-10-08 06:10 [France 24 Español] En directo: nuevas marchas estudiantiles en Francia entre promesas oficiales y denuncias de violencia policial
  > Los estudiantes de secundaria y universitarios franceses convocan nuevos bloqueos y marchas este jueves 8 de octubre, con el respaldo de varios sindicatos docentes, para exigir más financiación, 250.000 plazas universitarias adicionales y el fin de la selección mediante Parcoursup. Las organizacione
- 2026-10-08 11:36 [El País Internacional] Los estudiantes de Francia presentan 10 reivindicaciones para detener sus protestas
  > Estudiantes cortan la calle delante del liceo Helene-Boucher.
- 2026-10-08 14:44 [Clarín Mundo] "¡A tomar la Bastilla!": sindicatos, el campo y las universidades se unen a las barricadas estudiantiles en una cuarta movilización en Francia
  > En París, la manifestación se concentró en la Plaza de la Bastilla, donde se registraban incidentes.Otra marcha está prevista para el 13 de octubre.
- 2026-10-08 14:45 [Rai News Esteri] Proteste studentesche in Francia, l'abbraccio tra Mélenchon e il giovane Elwan diventa virale
  > “Quello che state facendo è straordinario. È il movimento giovanile più forte degli ultimi 50 anni”, ha dichiarato Mélenchon rivolgendosi ai manifestanti
- 2026-10-08 14:52 [Rai News Esteri] Chi è Elwan, simbolo delle proteste studentesche in Francia: 17 anni e milioni di visualizzazioni
  > Dall'abbraccio con il leader della sinistra Mélenchon allo scontro televisivo con Louise Montangon, il liceale è diventato un fenomeno social
- 2026-10-08 16:16 [BBC Mundo] Cuáles son los reclamos de los estudiantes que están participando en las violentas protestas que sacuden a Francia
  > Los bloqueos y las marchas estudiantiles surgen de agravios reales, y también de la costumbre francesa de decidir sus políticas en las calles.
- 2026-10-08 16:39 [France 24 Español] Directo París y el cuarto día de manifestaciones de estudiantes en Francia
  > Los estudiantes franceses siguen en las calles manifestándose por las condiciones educativas en el país. El primer ministro Sébastien Lecornu se pronunció al respecto, prometiendo medidas a finales de octubre y negando que las fuerzas de seguridad tengan instrucciones de actuar contra las protestas.
- 2026-10-08 17:31 [France 24 Español] Por qué Irán ataca a Francia aprovechando las protestas estudiantiles
  > Francia acusó este miércoles a Irán de lanzar una “campaña de desinformación” sobre las protestas estudiantiles y convocó al embajador iraní en París. Teherán cuestiona la actuación de las autoridades francesas frente a las movilizaciones, en una ofensiva que va más allá de la defensa de los manifes
- 2026-10-08 18:20 [Rai News Esteri] Francia, si allarga la protesta della scuola: "Basta repressione"
  > Cariche della polizia a Parigi, professori e sindacati al fianco degli studenti: "Il governo non dà risposte". I manifestanti: "Non tutti possono pagare la scuola privata"

## U017
**A** (3 item(s))
- 2026-10-04 13:18 [Kyiv Independent] Germany announces $1.46 billion in aid for Ukraine, including interceptor drones, air defense missiles
  > The package was announced by President Volodymyr Zelensky and German Chancellor Friedrich Merz at a joint press conference in Kyiv.
- 2026-10-04 16:38 [Al Jazeera] Germany’s Merz in Kyiv announces $1.5B in aid, urges Putin to end war
  > German Chancellor Friedrich Merz, on a surprise visit to Kyiv, announced $1.5 billion in military and reconstruction aid
- 2026-10-05 16:22 [Breaking Defense] Germany pledges $1.1B military aid package to Ukraine flush with drone interceptors
  > &#8220;Russia must know that we will take steps to defend ourselves against any further escalation,&#8221; said German Chancellor Friedrich Merz.
**B** (2 item(s))
- 2026-10-05 04:13 [Al Jazeera] FBI arrests ‘Chinese foreign agent’ for spying on Taiwan president’s son
  > A California woman allegedly sent photos and videos of President Lai&#039;s son and his family to Chinese officials.
- 2026-10-05 22:16 [South China Morning Post] US accuses mainland China of targeting Taiwan leader’s family in surveillance case
  > The United States has accused mainland China of hiring an American citizen of Chinese origin to surveil the family of Taiwanese leader William Lai Ching-te, days after President Xi Jinping’s state visit to Washington.
The Federal Bureau of Investigation on Sunday arrested 34-year-old Zhang Wanying a

## U018
**A** (5 item(s))
- 2026-10-05 04:07 [Al Jazeera] Russian lab worker dies of suspected plague in Siberia; US monitoring case
  > A Russian agency links the lab worker&#039;s death to &#039;pneumonia of unknown&#039; origin.
- 2026-10-05 17:14 [South China Morning Post] After plague death reports at Siberia lab, Russia says situation under control
  > Moscow on Monday downplayed reports that a laboratory technician had died of plague, stressing that postmortem tests had not detected the disease, while Washington said it was closely monitoring the situation.
Reports on Friday that plague had killed a 28-year-old woman named Darya Shipilova, who ha
- 2026-10-05 19:19 [France 24] Russian officials say 'situation under control' after plague reports
  > Moscow on Monday downplayed reports that a laboratory technician had died of plague, stressing that post-mortem tests had not detected the disease, while Washington said it was closely monitoring the situation. Reports on Friday that plague had killed a 28-year-old woman named Darya Shipilova, who h
- 2026-10-05 19:55 [BBC World] US 'watching closely' after plague researcher dies in Russia, Rubio says
  > The US says it is monitoring the case of a lab technician who died at a plague research centre in Siberia.
- 2026-10-05 21:03 [Al Jazeera] Trump says US ready to aid Russia with plague outbreak in Siberia
  > Russian authorities quarantine hospital, monitor 200 contacts after suspected pneumonic plague death in Siberia.
**B** (2 item(s))
- 2026-10-05 16:40 [ANSA English] Putin authorizes reorganization of UniCredit's Russian division
  > (ANSA) - ROME, 05 OTT - Russian President Vladimr Putin on Monday authorized the reorganization of the Russian division of Italy&#039;s second-biggest bank UniCredit.
Putin signed off on the rejigging of AO UniCredit Bank through the spin-off of a new company, the TASS news agency reported, publishi
- 2026-10-05 17:25 [Kyiv Independent] Putin allows Italy's UniCredit banking group to reorganize, sell Russian subsidiary
  > UniCredit, one of the few European banks still active in Russia, announced in May that it plans to sell most of its Russian subsidiary — UniCredit Bank Russia — to a private investor from the United Arab Emirates, while retaining control over its payments arm.

## U019
**A** (2 item(s))
- 2026-09-30 03:21 [South China Morning Post] US Supreme Court lets Trump resume deportations to third countries
  > The US Supreme Court on Tuesday let President Donald Trump’s administration continue swiftly deporting people to countries other than their own for now, while the justices consider whether the policy is legal.
The apparent 6-3 order temporarily lifts lower court requirements for migrants to get a ch
- 2026-10-01 17:35 [Al Jazeera] US Supreme Court agrees to take up Trump’s ICE detention policy
  > The case is the latest dispute over US President Donald Trump’s sweeping immigration crackdown.
**B** (6 item(s))
- 2026-10-02 01:23 [Al Jazeera] Trump says US may ask Europe to release diesel reserves
  > Skyrocketing diesel prices have pushed Washington to weigh an export ban, raising alarm across European economies.
- 2026-10-02 05:26 [BBC World] US pressures Europe over diesel reserves as Trump threatens export ban
  > President Donald Trump has threatened to ban diesel exports in a bid to ease prices in the US ahead of the November elections.
- 2026-10-02 13:16 [Al Jazeera] Trump vs Europe as US presses for release of emergency diesel stocks
  > Europe&#039;s leaders are mulling proposals to respond to Trump&#039;s diesel demands.
- 2026-10-02 14:51 [South China Morning Post] G7 nations agree to release diesel and oil stocks after Trump pressure
  > Group ⁠of Seven countries agreed on Friday to release 100 million barrels of diesel and crude oil from emergency reserves and pledged to refrain from energy export restrictions after pressure from US President Donald Trump.
The US led a pressure campaign on the European Union to draw down emergency 
- 2026-10-02 19:01 [Al Jazeera] Trump says Europe agreed to release ‘massive amount’ of diesel reserves
  > US President Donald Trump says Europe agreed to release a ‘massive amount’ of diesel from emergency stockpiles.
- 2026-10-02 20:25 [BBC World] G7 to release 100 million barrels of oil and diesel after Trump export ban threat
  > The co-ordinated release is aimed at heading off further price spikes and avoiding a ban on US diesel exports.

## U020
**A** (3 item(s))
- 2026-09-30 05:05 [Al Jazeera] Hegseth to cut number of US general and admiral positions by 20%
  > Pentagon official says the plan will be announced in the defence secretary&#039;s &#039;State of the Force&#039; address in Virginia.
- 2026-09-30 21:42 [South China Morning Post] Trump defence chief says US slashed number of generals and admirals by 20%
  > US Defence Secretary Pete Hegseth announced on Wednesday that the United States has slashed the number of its generals and admirals by 20 per cent, in a move he said is aimed at “accountability”.
Hegseth suggested the cuts targeted officers who failed to get on board with his efforts to ensure the m
- 2026-10-01 02:34 [Al Jazeera] Hegseth announces 20% cut to US military commanders
  > US Secretary of Defense Pete Hegseth says he’s firing 20% of the military’s generals and admirals.
**B** (2 item(s))
- 2026-09-30 17:01 [Breaking Defense] White House names nominees for SPACECOM, Navy No. 2
  > Overseeing the ongoing move of SPACECOM&#8217;s headquarters from its current home at Peterson SFB, Colo., to Huntsville, Ala., will be one of the first tasks Lt. Gen. David Miller will face if he is confirmed.
- 2026-09-30 18:49 [Defense News] White House nominates next general to helm US Space Command
  > The White House on Tuesday nominated Lt. Gen. David N. Miller Jr. to lead the U.S. Space Command as its general, according to a congressional notice.Miller is currently the deputy chief of Space Operations, Strategy, Plans, Programs and Requirements. He will, if confirmed, take over Space Command af

## U021
**A** (3 item(s))
- 2026-10-08 01:15 [Europa Press Internacional] Diosdado Cabello llama a cerrar filas con Delcy Rodríguez y reta a la oposición a medirse en las urnas
  > El ministro del Interior y secretario general del Partido Socialista Unido de Venezuela (PSUV), Diosdado Cabello, ha retado este martes a la oposición a presentarse a unas elecciones, mostrándose convencido de una nueva victoria del oficialismo en los hipotéticos comicios. Por su parte, la líder opo
- 2026-10-08 01:22 [ANSA Mondo] Venezuela, Delcy Rodríguez al Forum mondiale dell'alimentazione a Roma
  > La presidente ad interim del

Venezuela, Delcy Rodríguez, parteciperà il 12 ottobre a Roma al

Forum mondiale dell'alimentazione organizzato dalla Fao. Lo

riferisce Efe, citando il programma dell'evento. Rodríguez

interverrà alla cerimonia di apertura insieme, tra gli altri, al

presidente bolivia
- 2026-10-08 14:28 [France 24 Español] Estados Unidos presenta nuevos cargos contra Maduro y Cilia Flores por presuntas torturas a estadounidenses
  > Estados Unidos presenta nuevos cargos contra Nicolás Maduro y Cilia Flores por la presunta tortura de ciudadanos estadounidenses detenidos en Venezuela. La Fiscalía de Manhattan anunció este jueves las nuevas acusaciones, mientras la esposa del presidente venezolano pide salir de prisión para somete
**B** (3 item(s))
- 2026-10-08 16:48 [South China Morning Post] UK Ministry of Defence patrols arrest 2 Latvians near RAF base
  > UK Ministry of Defence security patrols arrested two Latvian men near an RAF (Royal Air Force) base that houses US and Nato intelligence operations, police said on Thursday.
The base, RAF Molesworth, 112km (70 miles) north of London, is operated by the US Air Force and includes intelligence staff fr
- 2026-10-08 16:57 [France 24] Two Latvian men arrested at UK base housing US and NATO intelligence hubs
  > British ​counter-terrorism police are investigating after two Latvian men were arrested Thursday near a Royal Air Force ​base in southeast England housing US and NATO intelligence operations, police said in a statement. The arrests come days after a major incident at another UK base led the US milit
- 2026-10-08 18:01 [Al Jazeera] Two Latvian men arrested inside UK military base after breach
  > Police say nothing so far suggests the incident at RAF Molesworth linked ​to events surrounding RAF Fairford last month.

## U022
**A** (56 item(s))
- 2026-10-04 03:30 [El País Internacional] Ni Bolsonaro, ni Lula: Trump se reserva (de momento) su apoyo en las elecciones de Brasil
  > Un asistente a un mitin de Flavio Bolsonaro disfrazado de Trump, el pasado domingo.
- 2026-10-04 04:00 [El País Internacional] La disputa entre Lula y Trump marca las elecciones brasileñas
  > Banderas de Flavio Bolsonaro y Luiz Inacio Lula da Silva en Brasilia, el 29 de septiembre.
- 2026-10-04 11:20 [Rai News Esteri] Urne aperte in Brasile per le elezioni presidenziali e legislative, sfida Lula-Bolsonaro
  > Gli ultimi sondaggi davano un testa a testa
- 2026-10-04 20:19 [El País Internacional] Brasil decide su futuro entre Lula y Bolsonaro, un estadista desgastado y el hijo de un ultra
  > El presidente Lula, el día 24 en São Gonçalo, y Flávio Bolsonaro, este sábado en Río.
- 2026-10-04 20:43 [Europa Press Internacional] Bolsonaro gana la primera vuelta en Brasil con el 47% de los votos y disputará contra Lula (45%) la segunda vuelta
  > El candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil e hijo del expresidente Jair Bolsonaro, Flávio Bolsonaro, ha ganado la primera vuelta de las elecciones en Brasil con un 47,17% de los sufragios. Su rival y presidente saliente, Luiz Inácio Lula da Silva, ha quedado cua
- 2026-10-04 22:25 [ANSA Mondo] Media, Lula e Bolsonaro andranno al ballottaggio il 25 ottobre
  > A metà scrutinio Bolsonaro al 49%, Lula a 42%
- 2026-10-04 23:00 [Clarín Mundo] Los Bolsonaro amplían su presencia en el Congreso con las elecciones en Brasil: entran la esposa del ex presidente y dos hermanos de Flavio
  > Michelle, la exprimera dama brasileña alcanzó el 28% de los votos en las elecciones legislativas del Distrito Federal.Otros dos hijos del expresidente Jair Bolsonaro compitieron por bancas legislativas en el estado de Santa Catarina.
- 2026-10-04 23:23 [Clarín Mundo] Elecciones en Brasil: Flávio Bolsonaro, un presidenciable a la sombra de su padre
  > Tiene 45 años y es el mayor de los cinco hijos del ex presidente. Elogia las políticas de seguridad de Nayib Bukele en El Salvador y promete la construcción de numerosas cárceles. Asimismo, presume de su buena relación con Donald Trump tras mantener una reunión privada en la Casa Blanca.
- 2026-10-04 23:23 [Clarín Mundo] Lula da Silva busca su reelección en Brasil: entre el freno a la ultraderecha y la defensa de su legado social
  > • A los 80 años, el mandatario brasileño busca la reelección apoyado en su historial de programas sociales como el Bolsa Familia, que actualmente beneficia a una cuarta parte de la población.
• Con vistas a un nuevo período, impulsa una reforma laboral para reducir la jornada semanal a cinco días y 
- 2026-10-05 00:09 [Rai News Esteri] Il sorpasso di Bolsonaro, la crisi di Lula
  > Flavio Bolsonaro, figlio dell'ex presidente di estrema destra tentato golpista, vince il primo turno sul presidente di sinistra Lula da Silva
- 2026-10-05 00:12 [Clarín Mundo] Elecciones en Brasil: un voto castigo que sorprendió a Lula da Silva y llegó desde su base tradicional de votantes
  > Un primer análisis indica que los sectores de menores ingresos se distanciaron de la elección y del líder del PT. El país es un éxito macro, con números notables, pero esos resultados no llegaron a los bolsillos de ese amplio espacio de votantes que se endeuda para pagar los gastos básicos.
- 2026-10-05 01:03 [Clarín Mundo] Lula acepta el impacto del triunfo de Bolsonaro: fue "un resultado inesperado"
  > El representante del socialista Partido de los Trabajadores busca su cuarto mandato, con la reelección en la gestión actual.Quedó detrás de Flavio Bolsonaro por apenas 2,15 puntos.
- 2026-10-05 01:08 [Clarín Mundo] Flavio Bolsonaro, tras ganar en primera vuelta ante Lula: "Brasil quiere un cambio"
  > Aseguró también que este resultado marcan "el fin de la era del PT" en su país.Dijo estar "feliz" con los números obtenidos frente al actual mandatario, Lula da Silva.
- 2026-10-05 01:41 [El País Internacional] Arrasadora victoria de la derecha en Brasil
  > Flavio Bolsonaro habla con la prensa en Río de Janeiro, este domingo.
- 2026-10-05 02:13 [Europa Press Internacional] Bolsonaro proclama "fin de la era del PT" y Lula apela a combatir su "pasado tenebroso" en la segunda vuelta en Brasil
  > Bolsonaro supera los 55 millones de apoyos (47,04%) y logra una ventaja de 2,3 millones de sufragios sobre el actual mandatario (45,15%)
- 2026-10-05 02:28 [El País Internacional] El apellido Bolsonaro gana desde la cárcel
  > Flávio Bolsonaro, candidato presidencial de Brasil, este domingo tras los resultados de la primera vuelta.
- 2026-10-05 02:39 [BBC Mundo] Cómo se compara Flávio Bolsonaro con su padre Jair y cuánto cambia el duelo con Lula por la presidencia de Brasil 4 años después
  > El senador derechista pasa fortalecido al balotaje contra el presidente de izquierda tras obtener más votos en la primera vuelta contra varios pronósticos, pero la elección sigue abierta.
- 2026-10-05 02:46 [France 24 Español] Simone Pitta: "Con esta primera vuelta se puede ver una consolidación del bolsonarismo en Brasil"
  > Pese a no haber estado en el poder en el último periodo presidencial de Brasil, y pese a las denuncias y condenas contra el expresidente Jair Bolsonaro por un intento de golpe de Estado, el bolsonarismo logró consolidarse de cara a los comicios de este 4 de octubre. Ahora, Flávio Bolsonaro busca pos
- 2026-10-05 02:47 [France 24 Español] Juan Agulló: "A diferencia de otros países de Latinoamérica, Brasil es un competidor directo"
  > En un escenario marcado por la polarización en Brasil, el candidato de ultraderecha y heredero político de su padre, Flávio Bolsonaro, y el actual presidente, Luiz Inácio Lula da Silva, quien busca un cuarto mandato, se disputan el balotaje. La sombra de Estados Unidos estuvo presente durante la pri
- 2026-10-05 02:54 [El País Internacional] Bolsonaro vence a Lula en primera vuelta de las elecciones y acaricia el retorno de la ultraderecha al poder en Brasil
  > Flávio Bolsonaro habla tras clasificarse para la segunda vuelta en Brasilia, Brasil, este domingo.
- 2026-10-05 03:19 [France 24 Español] Brasil: la derecha de Bolsonaro se fortalece en las regiones, con un triunfo holgado en São Paulo
  > Los comicios locales de Brasil se saldaron este domingo con un avance de la derecha que representan el candidato presidencial Flávio Bolsonaro y sus aliados. En tanto la izquierda del presidente y aspirante a la reelección, Luiz Inácio Lula da Silva perdía terreno. La victoria más cómoda fue en São 
- 2026-10-05 03:36 [El País Internacional] Las claves de la primera vuelta en Brasil: de la fuerza ultra al día después de Lula con América Latina pendiente
  > Flávio Bolsonaro vota en Río de Janeiro, este domingo.
- 2026-10-05 03:41 [France 24 Español] Flávio Bolsonaro tritura las encuestas: una ventaja pequeña, pero un escenario cuesta arriba para Lula
  > Brasil quedó inclinado hacia la tendencia de retorno a la derecha que sacude a América Latina, luego de que el senador e hijo del expresidente Jair Bolsonaro aventajara por casi dos puntos al izquierdista Luiz Inácio Lula da Silva en la primera vuelta de las elecciones. Lula ha reconocido el resulta
- 2026-10-05 04:08 [El País Internacional] Videoanálisis | Lula se enfrenta a una segunda vuelta electoral muy complicada
  > Videoanálisis | Lula Y Flávio Bolsonaro se enfrenta a una segunda vuelta electoral
- 2026-10-05 04:33 [Rai News Esteri] Brasile, avanzata del clan Bolsonaro: quattro eletti in Parlamento, Flavio al ballottaggio con Lula
  > L'ex first lady Michelle e Carlos, uno dei figli dell'ex presidente, conquistano un seggio al Senato. Alla Camera entrano il figlio più giovane Jair Renan e Renato, fratello di Jair
- 2026-10-05 05:14 [Il Sole 24 Ore Mondo] Brasile, Bolsonaro vince al primo turno con 47%, Lula al 45%: ballottaggio il 25 ottobre
  > Flavio Bolsonaro batte Lula al primo turno e si lancia come favorito nel ballottaggio del 25 ottobre che deciderà chi sarà il 40esimo presidente del Brasile. Il candidato trumpiano ha ottenuto il 47,14 % dei voti, il presidente uscente il 45.03 %, con una differenza tra i due di circa 2 milioni e me
- 2026-10-05 05:31 [Europa Press Internacional] Trump tacha de "corruptas" las elecciones de EEUU comparándolas con las de Brasil tras la victoria de Bolsonaro
  > El presidente de Estados Unidos, Donald Trump, ha vuelto a cargar contra el proceso electoral en su propio país, tachándolo de corrupto y contraponiéndolo la rapidez en el escrutinio de los votos de 125 millones de personas "en la primera vuelta de las elecciones presidenciales de Brasil", donde el 
- 2026-10-05 05:46 [Europa Press Internacional] Milei felicita a su "querido amigo" Flávio Bolsonaro por su "histórica elección" frente a Lula en Brasil
  > El presidente de Argentina, Javier Milei, ha felicitado al candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil, Flávio Bolsonaro, por su victoria en la primera vuelta de las elecciones presidenciales celebradas este domingo, en las que se ha impuesto con el 47,03% de los vo
- 2026-10-05 06:44 [ANSA Mondo] Brasile, l'ex giudice che condannò Lula eletto governatore
  > Sergio Moro guiderà l'esecutivo del suo stato natale, il Paranà
- 2026-10-05 07:14 [BBC Mundo] Elecciones en Brasil: Flávio Bolsonaro y Lula da Silva van a una segunda vuelta en la que el presidente enfrenta una difícil remontada
  > La mayor democracia de América Latina irá a balotaje el 25 de octubre. Lula lleva la desventaja frente a Bolsonaro, ya que históricamente nunca hubo una remontada en una segunda vuelta electoral en Brasil.
- 2026-10-05 07:46 [ANSA Mondo] In Brasile un 30enne di destra è il deputato più votato della storia
  > Nikolas Ferreira ha raccolto oltre 3,1 milioni di preferenze per la Camera
- 2026-10-05 10:46 [ANSA Mondo] Astensione record in Brasile, il 21,08% non ha votato al primo turno
  > Si tratta del livello più alto registrato dalle elezioni del 1998 (21,5%)
- 2026-10-05 11:42 [France 24 Español] Brasil irá a segunda vuelta: Flávio Bolsonaro lidera la primera ronda
  > Brasil se encamina a una segunda vuelta presidencial tras una elección marcada por la polarización. El senador Flávio Bolsonaro obtuvo el primer lugar en la primera vuelta, pero sin alcanzar la mayoría necesaria para evitar el balotaje. El próximo 25 de octubre se enfrentará al actual presidente, Lu
- 2026-10-05 12:20 [Rai News Esteri] Il primo turno delle presidenziali in Brasile, avanti Bolsonaro: ribaltati i pronostici pro-Lula
  > La sfida per il secondo turno del 25 ottobre è ancora aperta ma il presidente uscente non minimizza il peso di una pesante bocciatura delle sue politiche
- 2026-10-05 12:21 [Rai News Esteri] Presidenziali in Brasile, Flavio Bolsonaro a sorpresa supera Lula di 2 punti. Si va al ballottaggio
  > Il candidato di destra al 47%: "Il Brasile vuole cambiare". Il presidente uscente al 45%: "Sono bravo ai supplementari". Scelta rinviata al secondo turno del 25 ottobre
- 2026-10-05 12:29 [Clarín Mundo] Elecciones en Brasil 2026, EN VIVO: reacciones tras la victoria de Flávio Bolsonaro sobre Lula y últimas noticias del balotaje
  > Bolsonaro se impuso en la primera vuelta al superar por casi dos puntos al actual presidente Lula da Silva. El balotaje entre ambos se hará el 25 de octubre. Todas las repercusiones, minuto a minuto.
- 2026-10-05 12:31 [Clarín Mundo] Quién es Flávio Bolsonaro, el hijo de Jair que sorprendió a Lula y va por la presidencia de Brasil
  > Nacido en el estado de Río de Janeiro, Flávio es el mayor de los cinco hijos del expresidente y el que más se le parece físicamente.Este senador, de 45 años, enfrentará a Lula en el balotaje el próximo 25 de octubre.
- 2026-10-05 13:05 [France 24 Español] Informe desde Río de Janeiro: el Partido Liberal de Bolsonaro se fortalece en el Senado
  > Las elecciones legislativas en Brasil dejaron un resultado clave para el futuro político del país: el Partido Liberal (PL), formación vinculada al expresidente Jair Bolsonaro y que postuló a Flávio Bolsonaro para la Presidencia, amplió significativamente su presencia en el Senado. La bancada pasará 
- 2026-10-05 13:16 [Clarín Mundo] Elecciones en Brasil: los mercados celebran la ventaja de Flávio Bolsonaro sobre Lula y el principal índice de la Bolsa marca un nuevo récord
  > Los activos brasileños se dispararon este lunes y el real se apreció en la primera sesión de los mercados tras los comicios del domingo. El índice Ibovespa superó la marca de los 209.000 puntos por primera vez.
- 2026-10-05 13:57 [BBC Mundo] Quiénes son Lucas Pavanato y Nikolas Ferreira, los jóvenes influencers de derecha que lograron las mayores votaciones en la historia de la Cámara de Diputados de Brasil
  > Los flamantes legisladores comparten una agenda conservadora que incluye el rechazo a las políticas de género, el endurecimiento de las sanciones penales y la legalización del porte de armas como herramienta para combatir la delincuencia.
- 2026-10-05 14:50 [Clarín Mundo] Elecciones en Brasil: los resultados del domingo cambian por completo el diseño del país y ya asoma una amnistía para Jair Bolsonaro
  > La victoria del candidato conservador Flávio Bolsonaro sobre el presidente Lula da Silva en primera vuelta excede lo que pueda ocurrir en el balotaje.La ola de derecha se consolida con victorias en las gobernaciones y especialmente en el Parlamento.Aun si el líder petista lograra imponerse el 25 de 
- 2026-10-05 15:47 [Clarín Mundo] La reacción de los medios en Brasil tras la victoria de Bolsonaro: desde "el ciclo de Lula está terminado" hasta "el tsunami de lo peor de la derecha"
  > Los títulos, opiniones y análisis de la prensa en Brasil tras la primera vuelta de las presidenciales de este domingo.
- 2026-10-05 15:59 [France 24 Español] Flávio Bolsonaro y Lula da Silva se preparan para el balotaje en Brasil
  > 🇧🇷🗳️ Luiz Inácio Lula da Silva y Flávio Bolsonaro ofrecieron declaraciones después de que los resultados de los comicios presidenciales de Brasil confirmaran que deberán disputar el balotaje del 25 de octubre.
- 2026-10-05 16:02 [El País Internacional] El lulismo cruje ante la ofensiva ultra
  > Carteles del presidente Trump y del candidato Flavio Bolsonaro, en São Paulo, Brasil, este Lunes.
- 2026-10-05 16:10 [France 24 Español] "Solo faltan días para el rescate Brasil": Bolsonaro celebra la victoria sobre Lula
  > El senador del Partido Liberal (PL) y candidato presidencial, Flávio Bolsonaro, agradeció este lunes "a Dios" y al pueblo brasileño por su victoria en las elecciones del domingo ante el presidente Luiz Inácio Lula da Silva, en contra de los pronósticos. Además, celebró que el PL resultara el partido
- 2026-10-05 16:23 [Clarín Mundo] Elecciones en Brasil: a contrarreloj, Lula y el PT analizan cambios totales en la estrategia de campaña
  > Lo anticipan fuentes partidarias, pero no es claro en qué consistirán. Trascendió que ha habido tensiones internas sobre el manejo de la campaña.Y que debido a eso se perdieron oportunidades importantes para reducir el impulso del candidato opositor, Flávio Bolsonaro.
- 2026-10-05 16:36 [France 24 Español] Paraguay, refugio fiscal y político para la extrema derecha brasileña
  > En los últimos cinco años, las solicitudes de permisos de residencia de brasileños en Paraguay se han más que duplicado. Muchos de los recién llegados son simpatizantes de Jair Bolsonaro que temen una reelección del actual presidente, Luiz Inácio Lula da Silva, a quien responsabilizan de un deterior
- 2026-10-05 17:02 [ANSA Mondo] Brasile, Erika Hilton è la donna più votata della storia alla Camera
  > La politica brasiliana Erika

Hilton ha stabilito un nuovo record nella storia della Camera

dei deputati brasiliana, diventando la donna più votata di

sempre. La deputata trans del Partito socialismo e libertà

(Psol) di San Paolo è stata rieletta con 1.596.472 voti, pari al

5,9% dei voti espress
- 2026-10-05 17:30 [Clarín Mundo] El fantasma de Bolsonaro reaparece en Europa: los temores de Bruselas ante un eventual cambio de gobierno en Brasil
  > • Un cambio de gobierno en Brasil aportaría argumentos a los eurodiputados que buscan frenar la ratificación del entendimiento comercial.
• Si entre 50 y 80 legisladores modifican su postura en la votación prevista para los próximos meses, la aplicación provisional del pacto quedará suspendida.
- 2026-10-05 18:04 [France 24 Español] El mercado de valores de Brasil aplaude la ventaja de Bolsonaro en primera vuelta presidencial
  > El índice bursátil iBovespa, el más importante de la bolsa de São Paulo inició la jornada con un alza estrepitosa de casi el 9% y alcanzó máximo histórico, mientras el real brasileño gana 4,5% frente al dólar a media jornada, hasta situarse ligeramente por encima de los 5 reales por dólar. El buen r
- 2026-10-05 18:10 [France 24 Español] La dinastía Bolsonaro se fortalece: prensa brasileña sobre la primera vuelta electoral
  > La familia Bolsonaro no solo ganó la primera vuelta en Brasil, fortaleció su presencia en ambas cámaras del Congreso y conserva los respaldos de más de 10 gobernadores. 'O Globo' habla del bloque familiar que se ha hecho con varios cargos. Hermanos, hijos, esposa y exesposa tienen un puesto de elecc
- 2026-10-05 19:41 [El País Internacional] La ola conservadora de América Latina llega a Brasil
  > Flávio Bolsonaro (i) junto al presidente de EE.UU., Donald Trump, en el despacho oval de la Casa Blanca en Washington, el 26 de mayo de 2026.
- 2026-10-05 19:42 [El País Internacional] La victoria en primera vuelta de Bolsonaro impulsa a la ola ultra de América Latina
  > Transeúntes pasan ante pósteres dañados que muestran a Bolsonaro hijo con el presidente Trump, este lunes en São Paulo.
- 2026-10-05 19:47 [Clarín Mundo] Elecciones en Brasil: las urnas de la sorpresa
  > Tras el imprevisto triunfo de Flávio Bolsonaro sobre Lula en la primera vuelta, Brasil se encamina hacia un balotaje decisivo el próximo 25 de octubre. La contienda electoral ratifica la profunda polarización política del país y la consolidación del bolsonarismo como una fuerza de derecha permanente
- 2026-10-05 20:21 [ANSA Mondo] Trump, il risultato di Bolsonaro in Brasile una 'grande vittoria'
  > Il risultato di Flavio Bolsonaro

alle elezioni in Brasile è stata una "grande vittoria". Lo ha

detto Donald Trump.Quella di Bolsonaro "è una grande vittoria: combattuta, ma una

vittoria davvero enorme. Incredibile", ha detto Trump. Bolsonaro

si avvia al ballottaggio del 25 ottobre come favorito.
- 2026-10-05 22:09 [ANSA Mondo] Brasile, l'ex presidente Temer sostiene Bolsonaro al ballottaggio
  > L'ex presidente brasiliano

Michel Temer (2016-2018) ha dichiarato il suo sostegno a Flávio

Bolsonaro in vista del ballottaggio del 25 ottobre contro Luiz

Inácio Lula da Silva. In un video diffuso sui social, Temer ha

affermato che il risultato del primo turno mostra la volontà

degli elettori di
**B** (2 item(s))
- 2026-10-05 10:36 [Defense News] Missiles, satellites and warplanes — Ukraine, Europe advance key arms projects
  > WARSAW, Poland — Ukraine’s drone and missile maker Fire Point is developing an extended-range tactical ballistic missile after its FP-7 weapon was used in combat for the first time on Oct. 1, the company’s CEO Iryna Terekh said during this year’s Helsinki Security Forum.As European nations are braci
- 2026-10-05 12:26 [Kyiv Independent] New automatic gun turrets successfully down first Russian jet-powered drones, Air Force says
  > President Volodymyr Zelensky previously announced that twelve such turrets had been installed where Russian jet-powered drones have been particularly active, including around Kyiv.

## U023
**A** (2 item(s))
- 2026-10-08 08:06 [State Department] Secretary of State Marco Rubio Remarks to the Press
  > Marco Rubio, Secretary of State
Athens, Greece
Athens International Airport



	

		
		

			

		

		

			

				
				

					
						Secretary of State Marco Rubio Remarks to the Press
					
				

				

					

					
					
						Remarks

					
					
					
			

			
			

			
			October 8, 2026

			
				


- 2026-10-08 13:38 [Al Jazeera] Rubio praises nationalism and ties ‘America First’ values to ancient Greece
  > US Secretary of State Marco Rubio urged Western nations to prioritise their own interests in a speech in Athens.
**B** (2 item(s))
- 2026-10-08 15:23 [Rai News Esteri] Vance accusa Microsoft di frode sui visti, stop ai programmi sulle green card
  > "Per ogni lavoratore Usa licenziato, ne ha assunti uno e mezzo stranieri"
- 2026-10-08 17:52 [ANSA Mondo] Vance accusa Microsoft di frode sui visti, stop ai programmi sulle green card
  > Il vicepresidente americano JD

Vance ha annunciato un giro di vite contro le frodi legate ai

visti H-1B e per stranieri, puntando il dito nello specifico

contro Microsoft per aver licenziato 6.000 lavoratori Usa pur

avendo assunto personale tramite 6.300 visti H-1B e 3.000 green

card. "Facendo 

## U024
**A** (5 item(s))
- 2026-09-29 12:00 [South China Morning Post] US and China need shared risk vocabulary to manage AI threats: Beijing-linked think tank
  > Beijing and Washington should first develop a common language around AI risks rather than seek to resolve their broader technology rivalry, a leading Chinese think tank has advised.
The call from the China Institutes of Contemporary International Relations (CICIR), affiliated with the Ministry of St
- 2026-09-29 16:09 [BBC World] Trump rules out joint US-China venture to develop AI
  > The US president continues to push back on calls to establish guardrails around artificial intelligence, arguing it will stifle growth.
- 2026-09-29 19:32 [South China Morning Post] Trump rejects calls to work with China on AI safety despite Xi summit progress
  > US President Donald Trump said on Tuesday he does not want to work with China on addressing artificial intelligence (AI) risks, arguing that cooperation could undermine America’s lead in the fast-moving technology.
“Whoever wins superintelligence wins. You’re gonna have a winner and a loser, and you
- 2026-09-29 23:43 [Al Jazeera] Trump, tech bosses sign voluntary pact pledging ‘robust’ AI safeguards
  > US President Trump touts self-regulation amid the international community&#039;s and industry&#039;s calls for formal rules.
- 2026-09-30 05:00 [South China Morning Post] Chinese firms trail global peers on profits, but AI power boom offers bright spot: Natixis
  > China’s corporate sector remains considerably weaker than it was before the Covid-19 pandemic, but the country is emerging as a key beneficiary of the global artificial intelligence boom thanks to its ample power capacity, according to a Natixis survey of thousands of firms and a separate research r
**B** (6 item(s))
- 2026-09-30 16:51 [South China Morning Post] UK PM says ‘strong indications’ Iran involved in bomb scare at US-run airbase
  > British Prime Minister Andy Burnham on Wednesday said there were “strong indications” that Iran was involved in suspicious activity at a UK airbase that triggered a major security incident this weekend.
“There are strong indications that Iran played a part in what happened over the weekend at RAF Fa
- 2026-09-30 18:09 [Al Jazeera] Strong indications’ Iran linked to suspected UK airbase plot
  > UK Prime Minister says there are ‘strong indications’ Iran played a part in the suspected RAF Fairford airbase plot.
- 2026-10-01 02:30 [Al Jazeera] UK says Iran may be linked to alleged airbase plot, drawing angry denial
  > Andy Burnham says UK has &#039;strong indications&#039; Iran involved in alleged security incident at RAF base used by US.
- 2026-10-01 16:55 [Al Jazeera] British police arrest UK-Iranian national over airbase incident
  > Counter Terrorism police also questioned a UK national, days after five others were arrested and released on bail.
- 2026-10-01 17:52 [South China Morning Post] UK-Iranian man arrested over suspected Fairford airbase plot
  > British counterterrorism police investigating ⁠a suspected plot involving ⁠an airbase used by the US ⁠to target Iran said on Thursday they had arrested a dual UK-Iranian national on suspicion of preparing terrorist acts.
In an incident which triggered a huge police response, raised alarm among Weste
- 2026-10-03 10:45 [BBC World] UK-Iranian dual national bailed after RAF Fairford incident arrest
  > The 25-year-old man was arrested in the London borough of Westminster on Thursday.

## U025
**A** (8 item(s))
- 2026-09-29 14:40 [Defense News] US forces exiting Iraq after 2 decades, leaving opening for Iran
  > U.S. forces are set to depart from their last bases in Iraq by Wednesday, a move celebrated as a victory by Iran and its allies, who now have deep influence in the country where 4,500 Americans died during more than two decades of war.Iraqi security experts say the withdrawal — agreed to in 2024 und
- 2026-09-29 20:00 [Al Jazeera] US troops fully withdraw from Baghdad base after two decades
  > US Army soldiers have fully withdrawn from the US base in Baghdad.
- 2026-09-30 09:46 [South China Morning Post] US ends troop mission in Iraq, Baghdad to celebrate Sovereignty Day on October 1
  > A US-led coalition deployed in Iraq more than a decade ago to fight jihadists concluded its mission on Wednesday, a move celebrated by the country’s leaders, but which some fear will embolden pro-Iran armed factions.
Coalition troops deployed to Iraq and Syria in 2014 to fight Islamic State, which h
- 2026-09-30 11:36 [BBC World] Last UK and US troops leave Iraq as anti-Islamic State mission ends
  > The withdrawal of coalition forces, under a deal agreed two years ago, was a key demand of the Iraqi government.
- 2026-09-30 12:17 [Al Jazeera] Iraq celebrates National Sovereignty Day as US troops withdraw
  > Iraq’s security forces held parades in Baghdad and Najaf to celebrate ‘Sovereignty Day’ as US troops withdraw.
- 2026-09-30 14:04 [Breaking Defense] US withdraws last remaining troops out of Iraq
  > “As we step back and hand full primary responsibility for Iraq’s security to the Government of Iraq and the brave people of Iraq, US and Coalition forces stationed across the region will remain ready to respond to any ISIS threats that arise,” CENTCOM Commander Adm. Brad Cooper said.
- 2026-09-30 16:33 [Al Jazeera] Pentagon says US troop withdrawal from Iraq is complete
  > The withdrawal ends two decades of foreign intervention in Iraq as part of &#039;global war on terror&#039; and anti-ISIL fight.
- 2026-10-01 01:11 [Al Jazeera] Iraq celebrates Sovereignty Day as US troops complete withdrawal
  > Night time celebrations filled the air as Iraqis observed the start of a four-day holiday.
**B** (6 item(s))
- 2026-10-02 01:23 [Al Jazeera] Trump says US may ask Europe to release diesel reserves
  > Skyrocketing diesel prices have pushed Washington to weigh an export ban, raising alarm across European economies.
- 2026-10-02 05:26 [BBC World] US pressures Europe over diesel reserves as Trump threatens export ban
  > President Donald Trump has threatened to ban diesel exports in a bid to ease prices in the US ahead of the November elections.
- 2026-10-02 13:16 [Al Jazeera] Trump vs Europe as US presses for release of emergency diesel stocks
  > Europe&#039;s leaders are mulling proposals to respond to Trump&#039;s diesel demands.
- 2026-10-02 14:51 [South China Morning Post] G7 nations agree to release diesel and oil stocks after Trump pressure
  > Group ⁠of Seven countries agreed on Friday to release 100 million barrels of diesel and crude oil from emergency reserves and pledged to refrain from energy export restrictions after pressure from US President Donald Trump.
The US led a pressure campaign on the European Union to draw down emergency 
- 2026-10-02 19:01 [Al Jazeera] Trump says Europe agreed to release ‘massive amount’ of diesel reserves
  > US President Donald Trump says Europe agreed to release a ‘massive amount’ of diesel from emergency stockpiles.
- 2026-10-02 20:25 [BBC World] G7 to release 100 million barrels of oil and diesel after Trump export ban threat
  > The co-ordinated release is aimed at heading off further price spikes and avoiding a ban on US diesel exports.

## U026
**A** (56 item(s))
- 2026-10-04 03:30 [El País Internacional] Ni Bolsonaro, ni Lula: Trump se reserva (de momento) su apoyo en las elecciones de Brasil
  > Un asistente a un mitin de Flavio Bolsonaro disfrazado de Trump, el pasado domingo.
- 2026-10-04 04:00 [El País Internacional] La disputa entre Lula y Trump marca las elecciones brasileñas
  > Banderas de Flavio Bolsonaro y Luiz Inacio Lula da Silva en Brasilia, el 29 de septiembre.
- 2026-10-04 11:20 [Rai News Esteri] Urne aperte in Brasile per le elezioni presidenziali e legislative, sfida Lula-Bolsonaro
  > Gli ultimi sondaggi davano un testa a testa
- 2026-10-04 20:19 [El País Internacional] Brasil decide su futuro entre Lula y Bolsonaro, un estadista desgastado y el hijo de un ultra
  > El presidente Lula, el día 24 en São Gonçalo, y Flávio Bolsonaro, este sábado en Río.
- 2026-10-04 20:43 [Europa Press Internacional] Bolsonaro gana la primera vuelta en Brasil con el 47% de los votos y disputará contra Lula (45%) la segunda vuelta
  > El candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil e hijo del expresidente Jair Bolsonaro, Flávio Bolsonaro, ha ganado la primera vuelta de las elecciones en Brasil con un 47,17% de los sufragios. Su rival y presidente saliente, Luiz Inácio Lula da Silva, ha quedado cua
- 2026-10-04 22:25 [ANSA Mondo] Media, Lula e Bolsonaro andranno al ballottaggio il 25 ottobre
  > A metà scrutinio Bolsonaro al 49%, Lula a 42%
- 2026-10-04 23:00 [Clarín Mundo] Los Bolsonaro amplían su presencia en el Congreso con las elecciones en Brasil: entran la esposa del ex presidente y dos hermanos de Flavio
  > Michelle, la exprimera dama brasileña alcanzó el 28% de los votos en las elecciones legislativas del Distrito Federal.Otros dos hijos del expresidente Jair Bolsonaro compitieron por bancas legislativas en el estado de Santa Catarina.
- 2026-10-04 23:23 [Clarín Mundo] Elecciones en Brasil: Flávio Bolsonaro, un presidenciable a la sombra de su padre
  > Tiene 45 años y es el mayor de los cinco hijos del ex presidente. Elogia las políticas de seguridad de Nayib Bukele en El Salvador y promete la construcción de numerosas cárceles. Asimismo, presume de su buena relación con Donald Trump tras mantener una reunión privada en la Casa Blanca.
- 2026-10-04 23:23 [Clarín Mundo] Lula da Silva busca su reelección en Brasil: entre el freno a la ultraderecha y la defensa de su legado social
  > • A los 80 años, el mandatario brasileño busca la reelección apoyado en su historial de programas sociales como el Bolsa Familia, que actualmente beneficia a una cuarta parte de la población.
• Con vistas a un nuevo período, impulsa una reforma laboral para reducir la jornada semanal a cinco días y 
- 2026-10-05 00:09 [Rai News Esteri] Il sorpasso di Bolsonaro, la crisi di Lula
  > Flavio Bolsonaro, figlio dell'ex presidente di estrema destra tentato golpista, vince il primo turno sul presidente di sinistra Lula da Silva
- 2026-10-05 00:12 [Clarín Mundo] Elecciones en Brasil: un voto castigo que sorprendió a Lula da Silva y llegó desde su base tradicional de votantes
  > Un primer análisis indica que los sectores de menores ingresos se distanciaron de la elección y del líder del PT. El país es un éxito macro, con números notables, pero esos resultados no llegaron a los bolsillos de ese amplio espacio de votantes que se endeuda para pagar los gastos básicos.
- 2026-10-05 01:03 [Clarín Mundo] Lula acepta el impacto del triunfo de Bolsonaro: fue "un resultado inesperado"
  > El representante del socialista Partido de los Trabajadores busca su cuarto mandato, con la reelección en la gestión actual.Quedó detrás de Flavio Bolsonaro por apenas 2,15 puntos.
- 2026-10-05 01:08 [Clarín Mundo] Flavio Bolsonaro, tras ganar en primera vuelta ante Lula: "Brasil quiere un cambio"
  > Aseguró también que este resultado marcan "el fin de la era del PT" en su país.Dijo estar "feliz" con los números obtenidos frente al actual mandatario, Lula da Silva.
- 2026-10-05 01:41 [El País Internacional] Arrasadora victoria de la derecha en Brasil
  > Flavio Bolsonaro habla con la prensa en Río de Janeiro, este domingo.
- 2026-10-05 02:13 [Europa Press Internacional] Bolsonaro proclama "fin de la era del PT" y Lula apela a combatir su "pasado tenebroso" en la segunda vuelta en Brasil
  > Bolsonaro supera los 55 millones de apoyos (47,04%) y logra una ventaja de 2,3 millones de sufragios sobre el actual mandatario (45,15%)
- 2026-10-05 02:28 [El País Internacional] El apellido Bolsonaro gana desde la cárcel
  > Flávio Bolsonaro, candidato presidencial de Brasil, este domingo tras los resultados de la primera vuelta.
- 2026-10-05 02:39 [BBC Mundo] Cómo se compara Flávio Bolsonaro con su padre Jair y cuánto cambia el duelo con Lula por la presidencia de Brasil 4 años después
  > El senador derechista pasa fortalecido al balotaje contra el presidente de izquierda tras obtener más votos en la primera vuelta contra varios pronósticos, pero la elección sigue abierta.
- 2026-10-05 02:46 [France 24 Español] Simone Pitta: "Con esta primera vuelta se puede ver una consolidación del bolsonarismo en Brasil"
  > Pese a no haber estado en el poder en el último periodo presidencial de Brasil, y pese a las denuncias y condenas contra el expresidente Jair Bolsonaro por un intento de golpe de Estado, el bolsonarismo logró consolidarse de cara a los comicios de este 4 de octubre. Ahora, Flávio Bolsonaro busca pos
- 2026-10-05 02:47 [France 24 Español] Juan Agulló: "A diferencia de otros países de Latinoamérica, Brasil es un competidor directo"
  > En un escenario marcado por la polarización en Brasil, el candidato de ultraderecha y heredero político de su padre, Flávio Bolsonaro, y el actual presidente, Luiz Inácio Lula da Silva, quien busca un cuarto mandato, se disputan el balotaje. La sombra de Estados Unidos estuvo presente durante la pri
- 2026-10-05 02:54 [El País Internacional] Bolsonaro vence a Lula en primera vuelta de las elecciones y acaricia el retorno de la ultraderecha al poder en Brasil
  > Flávio Bolsonaro habla tras clasificarse para la segunda vuelta en Brasilia, Brasil, este domingo.
- 2026-10-05 03:19 [France 24 Español] Brasil: la derecha de Bolsonaro se fortalece en las regiones, con un triunfo holgado en São Paulo
  > Los comicios locales de Brasil se saldaron este domingo con un avance de la derecha que representan el candidato presidencial Flávio Bolsonaro y sus aliados. En tanto la izquierda del presidente y aspirante a la reelección, Luiz Inácio Lula da Silva perdía terreno. La victoria más cómoda fue en São 
- 2026-10-05 03:36 [El País Internacional] Las claves de la primera vuelta en Brasil: de la fuerza ultra al día después de Lula con América Latina pendiente
  > Flávio Bolsonaro vota en Río de Janeiro, este domingo.
- 2026-10-05 03:41 [France 24 Español] Flávio Bolsonaro tritura las encuestas: una ventaja pequeña, pero un escenario cuesta arriba para Lula
  > Brasil quedó inclinado hacia la tendencia de retorno a la derecha que sacude a América Latina, luego de que el senador e hijo del expresidente Jair Bolsonaro aventajara por casi dos puntos al izquierdista Luiz Inácio Lula da Silva en la primera vuelta de las elecciones. Lula ha reconocido el resulta
- 2026-10-05 04:08 [El País Internacional] Videoanálisis | Lula se enfrenta a una segunda vuelta electoral muy complicada
  > Videoanálisis | Lula Y Flávio Bolsonaro se enfrenta a una segunda vuelta electoral
- 2026-10-05 04:33 [Rai News Esteri] Brasile, avanzata del clan Bolsonaro: quattro eletti in Parlamento, Flavio al ballottaggio con Lula
  > L'ex first lady Michelle e Carlos, uno dei figli dell'ex presidente, conquistano un seggio al Senato. Alla Camera entrano il figlio più giovane Jair Renan e Renato, fratello di Jair
- 2026-10-05 05:14 [Il Sole 24 Ore Mondo] Brasile, Bolsonaro vince al primo turno con 47%, Lula al 45%: ballottaggio il 25 ottobre
  > Flavio Bolsonaro batte Lula al primo turno e si lancia come favorito nel ballottaggio del 25 ottobre che deciderà chi sarà il 40esimo presidente del Brasile. Il candidato trumpiano ha ottenuto il 47,14 % dei voti, il presidente uscente il 45.03 %, con una differenza tra i due di circa 2 milioni e me
- 2026-10-05 05:31 [Europa Press Internacional] Trump tacha de "corruptas" las elecciones de EEUU comparándolas con las de Brasil tras la victoria de Bolsonaro
  > El presidente de Estados Unidos, Donald Trump, ha vuelto a cargar contra el proceso electoral en su propio país, tachándolo de corrupto y contraponiéndolo la rapidez en el escrutinio de los votos de 125 millones de personas "en la primera vuelta de las elecciones presidenciales de Brasil", donde el 
- 2026-10-05 05:46 [Europa Press Internacional] Milei felicita a su "querido amigo" Flávio Bolsonaro por su "histórica elección" frente a Lula en Brasil
  > El presidente de Argentina, Javier Milei, ha felicitado al candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil, Flávio Bolsonaro, por su victoria en la primera vuelta de las elecciones presidenciales celebradas este domingo, en las que se ha impuesto con el 47,03% de los vo
- 2026-10-05 06:44 [ANSA Mondo] Brasile, l'ex giudice che condannò Lula eletto governatore
  > Sergio Moro guiderà l'esecutivo del suo stato natale, il Paranà
- 2026-10-05 07:14 [BBC Mundo] Elecciones en Brasil: Flávio Bolsonaro y Lula da Silva van a una segunda vuelta en la que el presidente enfrenta una difícil remontada
  > La mayor democracia de América Latina irá a balotaje el 25 de octubre. Lula lleva la desventaja frente a Bolsonaro, ya que históricamente nunca hubo una remontada en una segunda vuelta electoral en Brasil.
- 2026-10-05 07:46 [ANSA Mondo] In Brasile un 30enne di destra è il deputato più votato della storia
  > Nikolas Ferreira ha raccolto oltre 3,1 milioni di preferenze per la Camera
- 2026-10-05 10:46 [ANSA Mondo] Astensione record in Brasile, il 21,08% non ha votato al primo turno
  > Si tratta del livello più alto registrato dalle elezioni del 1998 (21,5%)
- 2026-10-05 11:42 [France 24 Español] Brasil irá a segunda vuelta: Flávio Bolsonaro lidera la primera ronda
  > Brasil se encamina a una segunda vuelta presidencial tras una elección marcada por la polarización. El senador Flávio Bolsonaro obtuvo el primer lugar en la primera vuelta, pero sin alcanzar la mayoría necesaria para evitar el balotaje. El próximo 25 de octubre se enfrentará al actual presidente, Lu
- 2026-10-05 12:20 [Rai News Esteri] Il primo turno delle presidenziali in Brasile, avanti Bolsonaro: ribaltati i pronostici pro-Lula
  > La sfida per il secondo turno del 25 ottobre è ancora aperta ma il presidente uscente non minimizza il peso di una pesante bocciatura delle sue politiche
- 2026-10-05 12:21 [Rai News Esteri] Presidenziali in Brasile, Flavio Bolsonaro a sorpresa supera Lula di 2 punti. Si va al ballottaggio
  > Il candidato di destra al 47%: "Il Brasile vuole cambiare". Il presidente uscente al 45%: "Sono bravo ai supplementari". Scelta rinviata al secondo turno del 25 ottobre
- 2026-10-05 12:29 [Clarín Mundo] Elecciones en Brasil 2026, EN VIVO: reacciones tras la victoria de Flávio Bolsonaro sobre Lula y últimas noticias del balotaje
  > Bolsonaro se impuso en la primera vuelta al superar por casi dos puntos al actual presidente Lula da Silva. El balotaje entre ambos se hará el 25 de octubre. Todas las repercusiones, minuto a minuto.
- 2026-10-05 12:31 [Clarín Mundo] Quién es Flávio Bolsonaro, el hijo de Jair que sorprendió a Lula y va por la presidencia de Brasil
  > Nacido en el estado de Río de Janeiro, Flávio es el mayor de los cinco hijos del expresidente y el que más se le parece físicamente.Este senador, de 45 años, enfrentará a Lula en el balotaje el próximo 25 de octubre.
- 2026-10-05 13:05 [France 24 Español] Informe desde Río de Janeiro: el Partido Liberal de Bolsonaro se fortalece en el Senado
  > Las elecciones legislativas en Brasil dejaron un resultado clave para el futuro político del país: el Partido Liberal (PL), formación vinculada al expresidente Jair Bolsonaro y que postuló a Flávio Bolsonaro para la Presidencia, amplió significativamente su presencia en el Senado. La bancada pasará 
- 2026-10-05 13:16 [Clarín Mundo] Elecciones en Brasil: los mercados celebran la ventaja de Flávio Bolsonaro sobre Lula y el principal índice de la Bolsa marca un nuevo récord
  > Los activos brasileños se dispararon este lunes y el real se apreció en la primera sesión de los mercados tras los comicios del domingo. El índice Ibovespa superó la marca de los 209.000 puntos por primera vez.
- 2026-10-05 13:57 [BBC Mundo] Quiénes son Lucas Pavanato y Nikolas Ferreira, los jóvenes influencers de derecha que lograron las mayores votaciones en la historia de la Cámara de Diputados de Brasil
  > Los flamantes legisladores comparten una agenda conservadora que incluye el rechazo a las políticas de género, el endurecimiento de las sanciones penales y la legalización del porte de armas como herramienta para combatir la delincuencia.
- 2026-10-05 14:50 [Clarín Mundo] Elecciones en Brasil: los resultados del domingo cambian por completo el diseño del país y ya asoma una amnistía para Jair Bolsonaro
  > La victoria del candidato conservador Flávio Bolsonaro sobre el presidente Lula da Silva en primera vuelta excede lo que pueda ocurrir en el balotaje.La ola de derecha se consolida con victorias en las gobernaciones y especialmente en el Parlamento.Aun si el líder petista lograra imponerse el 25 de 
- 2026-10-05 15:47 [Clarín Mundo] La reacción de los medios en Brasil tras la victoria de Bolsonaro: desde "el ciclo de Lula está terminado" hasta "el tsunami de lo peor de la derecha"
  > Los títulos, opiniones y análisis de la prensa en Brasil tras la primera vuelta de las presidenciales de este domingo.
- 2026-10-05 15:59 [France 24 Español] Flávio Bolsonaro y Lula da Silva se preparan para el balotaje en Brasil
  > 🇧🇷🗳️ Luiz Inácio Lula da Silva y Flávio Bolsonaro ofrecieron declaraciones después de que los resultados de los comicios presidenciales de Brasil confirmaran que deberán disputar el balotaje del 25 de octubre.
- 2026-10-05 16:02 [El País Internacional] El lulismo cruje ante la ofensiva ultra
  > Carteles del presidente Trump y del candidato Flavio Bolsonaro, en São Paulo, Brasil, este Lunes.
- 2026-10-05 16:10 [France 24 Español] "Solo faltan días para el rescate Brasil": Bolsonaro celebra la victoria sobre Lula
  > El senador del Partido Liberal (PL) y candidato presidencial, Flávio Bolsonaro, agradeció este lunes "a Dios" y al pueblo brasileño por su victoria en las elecciones del domingo ante el presidente Luiz Inácio Lula da Silva, en contra de los pronósticos. Además, celebró que el PL resultara el partido
- 2026-10-05 16:23 [Clarín Mundo] Elecciones en Brasil: a contrarreloj, Lula y el PT analizan cambios totales en la estrategia de campaña
  > Lo anticipan fuentes partidarias, pero no es claro en qué consistirán. Trascendió que ha habido tensiones internas sobre el manejo de la campaña.Y que debido a eso se perdieron oportunidades importantes para reducir el impulso del candidato opositor, Flávio Bolsonaro.
- 2026-10-05 16:36 [France 24 Español] Paraguay, refugio fiscal y político para la extrema derecha brasileña
  > En los últimos cinco años, las solicitudes de permisos de residencia de brasileños en Paraguay se han más que duplicado. Muchos de los recién llegados son simpatizantes de Jair Bolsonaro que temen una reelección del actual presidente, Luiz Inácio Lula da Silva, a quien responsabilizan de un deterior
- 2026-10-05 17:02 [ANSA Mondo] Brasile, Erika Hilton è la donna più votata della storia alla Camera
  > La politica brasiliana Erika

Hilton ha stabilito un nuovo record nella storia della Camera

dei deputati brasiliana, diventando la donna più votata di

sempre. La deputata trans del Partito socialismo e libertà

(Psol) di San Paolo è stata rieletta con 1.596.472 voti, pari al

5,9% dei voti espress
- 2026-10-05 17:30 [Clarín Mundo] El fantasma de Bolsonaro reaparece en Europa: los temores de Bruselas ante un eventual cambio de gobierno en Brasil
  > • Un cambio de gobierno en Brasil aportaría argumentos a los eurodiputados que buscan frenar la ratificación del entendimiento comercial.
• Si entre 50 y 80 legisladores modifican su postura en la votación prevista para los próximos meses, la aplicación provisional del pacto quedará suspendida.
- 2026-10-05 18:04 [France 24 Español] El mercado de valores de Brasil aplaude la ventaja de Bolsonaro en primera vuelta presidencial
  > El índice bursátil iBovespa, el más importante de la bolsa de São Paulo inició la jornada con un alza estrepitosa de casi el 9% y alcanzó máximo histórico, mientras el real brasileño gana 4,5% frente al dólar a media jornada, hasta situarse ligeramente por encima de los 5 reales por dólar. El buen r
- 2026-10-05 18:10 [France 24 Español] La dinastía Bolsonaro se fortalece: prensa brasileña sobre la primera vuelta electoral
  > La familia Bolsonaro no solo ganó la primera vuelta en Brasil, fortaleció su presencia en ambas cámaras del Congreso y conserva los respaldos de más de 10 gobernadores. 'O Globo' habla del bloque familiar que se ha hecho con varios cargos. Hermanos, hijos, esposa y exesposa tienen un puesto de elecc
- 2026-10-05 19:41 [El País Internacional] La ola conservadora de América Latina llega a Brasil
  > Flávio Bolsonaro (i) junto al presidente de EE.UU., Donald Trump, en el despacho oval de la Casa Blanca en Washington, el 26 de mayo de 2026.
- 2026-10-05 19:42 [El País Internacional] La victoria en primera vuelta de Bolsonaro impulsa a la ola ultra de América Latina
  > Transeúntes pasan ante pósteres dañados que muestran a Bolsonaro hijo con el presidente Trump, este lunes en São Paulo.
- 2026-10-05 19:47 [Clarín Mundo] Elecciones en Brasil: las urnas de la sorpresa
  > Tras el imprevisto triunfo de Flávio Bolsonaro sobre Lula en la primera vuelta, Brasil se encamina hacia un balotaje decisivo el próximo 25 de octubre. La contienda electoral ratifica la profunda polarización política del país y la consolidación del bolsonarismo como una fuerza de derecha permanente
- 2026-10-05 20:21 [ANSA Mondo] Trump, il risultato di Bolsonaro in Brasile una 'grande vittoria'
  > Il risultato di Flavio Bolsonaro

alle elezioni in Brasile è stata una "grande vittoria". Lo ha

detto Donald Trump.Quella di Bolsonaro "è una grande vittoria: combattuta, ma una

vittoria davvero enorme. Incredibile", ha detto Trump. Bolsonaro

si avvia al ballottaggio del 25 ottobre come favorito.
- 2026-10-05 22:09 [ANSA Mondo] Brasile, l'ex presidente Temer sostiene Bolsonaro al ballottaggio
  > L'ex presidente brasiliano

Michel Temer (2016-2018) ha dichiarato il suo sostegno a Flávio

Bolsonaro in vista del ballottaggio del 25 ottobre contro Luiz

Inácio Lula da Silva. In un video diffuso sui social, Temer ha

affermato che il risultato del primo turno mostra la volontà

degli elettori di
**B** (2 item(s))
- 2026-10-05 04:13 [Al Jazeera] FBI arrests ‘Chinese foreign agent’ for spying on Taiwan president’s son
  > A California woman allegedly sent photos and videos of President Lai&#039;s son and his family to Chinese officials.
- 2026-10-05 22:16 [South China Morning Post] US accuses mainland China of targeting Taiwan leader’s family in surveillance case
  > The United States has accused mainland China of hiring an American citizen of Chinese origin to surveil the family of Taiwanese leader William Lai Ching-te, days after President Xi Jinping’s state visit to Washington.
The Federal Bureau of Investigation on Sunday arrested 34-year-old Zhang Wanying a

## U027
**A** (5 item(s))
- 2026-10-07 23:20 [Al Jazeera] Christa Pike was nearly taken off life support before waking, lawyers say
  > Death row inmate who survived execution by lethal injection is said to be &#039;angry and confused&#039; about what happened.
- 2026-10-08 03:02 [BBC World] Texas carries out first US execution since Christa Pike's botched lethal injections
  > Lawyers for Jamaal Howard had asked a judge to pause the execution after Christa Pike's botched lethal injections.
- 2026-10-08 08:13 [BBC World] Christa Pike now walking after US execution went wrong, lawyer tells BBC
  > A lawyer says the murderer of Colleen Slemmer is moving around her hospital room after surviving two lethal injections.
- 2026-10-08 08:29 [Al Jazeera] Christa Pike almost taken off life support before she woke up
  > Death row inmate Christa Pike has regained consciousness following a botched execution in Tennessee, her lawyer says.
- 2026-10-08 09:53 [France 24] Christa Pike 'angry and confused' after Tennessee's failed execution effort
  > Christa Pike, sentenced to death for a 1995 murder, awoke "angry ​and confused" in a hospital this week with a long recuperation ahead after surviving Tennessee's botched effort to execute her, her lawyers said on Wednesday.
**B** (2 item(s))
- 2026-10-08 03:19 [BBC Mundo] Los israelíes exigen que se rindan cuentas por los errores del 7 de octubre, tres años después de los ataques de Hamás
  > El primer ministro israelí, Benjamin Netanyahu, se niega a asumir cualquier responsabilidad personal por lo sucedido o a ordenar una investigación estatal.
- 2026-10-08 16:38 [France 24 Español] Informe desde Beirut: se cumplen tres años de guerra de Israel en Líbano
  > Luego de los ataques de Hamás contra Israel el 7 de octubre de 2023, el Hezbolá libanés abrió un "frente de apoyo" a la milicia palestina. Este 2026 se cumplen tres años del conflicto, que ha provocado una ocupación israelí del sur de Líbano y el desplazamiento de cientos de personas. Aunque se espe

## U028
**A** (5 item(s))
- 2026-10-04 15:16 [Al Jazeera] Dodik urges Serb turnout against ‘Sarajevo crooks’ in Bosnia election
  > Dodik urges Serb turnout against ‘Sarajevo crooks’ in Bosnia election
- 2026-10-04 20:36 [South China Morning Post] Serb separatist Dodik declares victory in Bosnia vote as ethnic tensions, EU hopes collide
  > Bosnian Serb nationalist politician Milorad Dodik has declared victory for his party in an election in Bosnia and Herzegovina on Sunday that was shaped by economic pressures, the prospect of the Balkan nation joining the European Union and ethnic tensions that have divided the country since its brut
- 2026-10-05 03:36 [Al Jazeera] Bosnian Serb nationalist claims party victory in Bosnia elections
  > Bosnian Serb nationalist Milorad Dodik claimed victory for his party in Bosnia’s elections.
- 2026-10-05 07:33 [Kyiv Independent] Pro-Russian Dodik claims party victory in Bosnian elections
  > "If it had not been for (U.S. President) Donald Trump's magnificent victory, we would probably be political corpses today," Milorad Dodik told his supporters, while also thanking Russian President Vladimir Putin.
- 2026-10-05 10:23 [DW World] Bosnia election: New technology might have stopped votes being cast on behalf of dead voters, but the result remains unchanged
  > New technology has stopped votes being cast on behalf of dead or absent voters, and turnout has fallen to a record low. But it was a case of deja vu in Bosnia's elections with the same parties winning.
**B** (6 item(s))
- 2026-10-05 09:44 [France 24] Nobel Prize in Medicine jointly awarded to ​Karl Deisseroth, Peter Hegemann ​and Georg Nagel
  > The Nobel Prize in Medicine was awarded Monday to Karl Deisseroth, Peter Hegemann and Georg Nagel for their research into light-gated ion channels and optogenetics. The prize money this year is 12 million Swedish kronor (about $1.2 million).
- 2026-10-05 09:45 [South China Morning Post] Nobel Medicine Prize awarded to 3 scientists for optogenetics development
  > The 2026 Nobel Prize season opened on Monday with the Medicine Prize being awarded to Karl Deisseroth, Peter Hegemann and Georg Nagel for their research into light-gated ion channels and optogenetics.
The prize was announced at the Karolinska Institute in Stockholm, kicking off Nobels week.
Their wo
- 2026-10-05 09:47 [France 24] 🔴 Nobel Prize in Medicine jointly awarded to ​Karl Deisseroth, Peter Hegemann ​and Georg Nagel
- 2026-10-05 10:10 [BBC World] Nobel Prize awarded for showing how nerve cells shape feelings
  > US psychiatrist and neurologist Karl Deisseroth and his German colleagues Peter Hegemann and Georg Nagel have been awarded for their work.
- 2026-10-05 14:18 [Al Jazeera] Nobel medicine prize honours US and German scientists for optogenetics work
  > The winners of the Nobel Prizes in physics, chemistry, literature, peace and ‌economics will be announced in the week.
- 2026-10-05 21:56 [France 24] Switching on brain cells: the Nobel-winning science of optogenetics
  > The Nobel medicine prize was awarded Monday to US psychiatrist and neurologist Karl Deisseroth and German scientists Peter Hegemann and Georg Nagel for their pioneering work in the neuroscience field of optogenetics. In optogenetics, scientists control neurones by stimulating them with light -- pote

## U029
**A** (3 item(s))
- 2026-10-01 16:40 [BBC World] Renee Good: Family of US woman killed by ICE agent sues Trump officials
  > Lawyers for Good's family say US officials created "an unprecedented environment for state sponsored violence" in Minneapolis.
- 2026-10-01 17:28 [Al Jazeera] Renee Good’s family sues Trump administration over fatal ICE shooting
  > Lawsuits accuse Trump officials of recklessness and civil rights violations in Renee Good&#039;s fatal Minneapolis shooting .
- 2026-10-01 23:34 [South China Morning Post] Family of Renee Good, US woman killed by ICE agent, sues Trump administration
  > ⁠The family of Renee Good, one of two US citizens fatally shot by ⁠federal immigration agents in Minneapolis in January, sued the Trump administration on Thursday, saying there had been “no accountability” for her killing during deportation sweeps.
Good, 37, was shot dead in her car by a US Immigrat
**B** (2 item(s))
- 2026-10-01 18:38 [South China Morning Post] Canada fast-tracking oil pipeline designed to diversify economy away from US
  > Canada will fast track the approval process for a new proposed crude oil export pipeline to its west coast that could generate over C$20 billion (US$14 billion) a year in GDP, Prime Minister ‌Mark Carney said on Thursday.
The pipeline, which was announced in July, is a crucial part of Carney’s bid t
- 2026-10-01 18:56 [Al Jazeera] Canada to fast track oil pipeline meant to diversify economy away from US
  > Carney declared the pipeline a project of national interest, smoothening its way to a single federal regulatory review.

## U030
**A** (7 item(s))
- 2026-10-03 23:35 [Rai News Esteri] Marea sociale contro il caro-affitti in Spagna: le piazze spingono Sánchez verso le urne
  > Ondata di proteste da Madrid a tutte le principali città per il diritto alla casa dopo lo sfratto dell'ottantasettenne Mari Carmen; il rifiuto dei decreti da parte delle destre e dei catalani di Junts apre lo scenario di elezioni anticipate
- 2026-10-04 17:28 [Rai News Esteri] Casa e scuola: il filo rosso che lega le proteste in Europa
  > In Spagna per il diritto alla casa, in Francia l'erosione allo studio accende lo scontento dei più giovani
- 2026-10-04 23:15 [Rai News Esteri] La Spagna in piazza per il diritto alla casa. E Sanchez pensa al voto anticipato
  > Centinaia di migliaia di persone al fianco delle proteste di Madrid per la casa, il governo bocciato in Parlamento valuta elezioni a fine novembre
- 2026-10-05 06:21 [Il Sole 24 Ore Mondo] Caro casa, prezzi e affitti salgono nell’Ue. Il Governo studia le misure per giovani e locazioni
  > «Serve una formazione di qualità, un lavoro sicuro e stabile, una retribuzione adeguata, una casa a un prezzo equo», ha detto di recente la premier Giorgia Meloni
- 2026-10-05 10:27 [Rai News Esteri] La Spagna al voto: i sondaggi premiano le destre, l'area progressista frammentata
  > Il partito popolare e Vox arriverebbero al 52%, secondo un sondaggio per El Pais. Ma le rilevazioni sono state realizzate prima della crisi di governo e della bocciatura dei decreti presentati da Sanchez
- 2026-10-05 19:05 [Il Sole 24 Ore Mondo] Sanchez sfida le destre: Spagna al voto anticipato
  > Dopo la bocciatura sul piano casa, il premier socialista convoca le elezioni cavalcando le proteste di piazza: «Serve una maggioranza progressista per nuovi progressi sociali»
- 2026-10-05 21:04 [Rai News Esteri] Migliaia di persone a Barcellona in piazza per il diritto alla casa
  > Dopo Madrid e Valencia anche Barcellona stasera è scesa in piazza all'annuncio di elezioni anticipate, in migliai hanno sfilato per difendere il diritto alla casa
**B** (6 item(s))
- 2026-10-05 09:44 [France 24] Nobel Prize in Medicine jointly awarded to ​Karl Deisseroth, Peter Hegemann ​and Georg Nagel
  > The Nobel Prize in Medicine was awarded Monday to Karl Deisseroth, Peter Hegemann and Georg Nagel for their research into light-gated ion channels and optogenetics. The prize money this year is 12 million Swedish kronor (about $1.2 million).
- 2026-10-05 09:45 [South China Morning Post] Nobel Medicine Prize awarded to 3 scientists for optogenetics development
  > The 2026 Nobel Prize season opened on Monday with the Medicine Prize being awarded to Karl Deisseroth, Peter Hegemann and Georg Nagel for their research into light-gated ion channels and optogenetics.
The prize was announced at the Karolinska Institute in Stockholm, kicking off Nobels week.
Their wo
- 2026-10-05 09:47 [France 24] 🔴 Nobel Prize in Medicine jointly awarded to ​Karl Deisseroth, Peter Hegemann ​and Georg Nagel
- 2026-10-05 10:10 [BBC World] Nobel Prize awarded for showing how nerve cells shape feelings
  > US psychiatrist and neurologist Karl Deisseroth and his German colleagues Peter Hegemann and Georg Nagel have been awarded for their work.
- 2026-10-05 14:18 [Al Jazeera] Nobel medicine prize honours US and German scientists for optogenetics work
  > The winners of the Nobel Prizes in physics, chemistry, literature, peace and ‌economics will be announced in the week.
- 2026-10-05 21:56 [France 24] Switching on brain cells: the Nobel-winning science of optogenetics
  > The Nobel medicine prize was awarded Monday to US psychiatrist and neurologist Karl Deisseroth and German scientists Peter Hegemann and Georg Nagel for their pioneering work in the neuroscience field of optogenetics. In optogenetics, scientists control neurones by stimulating them with light -- pote

## U031
**A** (6 item(s))
- 2026-09-30 16:51 [South China Morning Post] UK PM says ‘strong indications’ Iran involved in bomb scare at US-run airbase
  > British Prime Minister Andy Burnham on Wednesday said there were “strong indications” that Iran was involved in suspicious activity at a UK airbase that triggered a major security incident this weekend.
“There are strong indications that Iran played a part in what happened over the weekend at RAF Fa
- 2026-09-30 18:09 [Al Jazeera] Strong indications’ Iran linked to suspected UK airbase plot
  > UK Prime Minister says there are ‘strong indications’ Iran played a part in the suspected RAF Fairford airbase plot.
- 2026-10-01 02:30 [Al Jazeera] UK says Iran may be linked to alleged airbase plot, drawing angry denial
  > Andy Burnham says UK has &#039;strong indications&#039; Iran involved in alleged security incident at RAF base used by US.
- 2026-10-01 16:55 [Al Jazeera] British police arrest UK-Iranian national over airbase incident
  > Counter Terrorism police also questioned a UK national, days after five others were arrested and released on bail.
- 2026-10-01 17:52 [South China Morning Post] UK-Iranian man arrested over suspected Fairford airbase plot
  > British counterterrorism police investigating ⁠a suspected plot involving ⁠an airbase used by the US ⁠to target Iran said on Thursday they had arrested a dual UK-Iranian national on suspicion of preparing terrorist acts.
In an incident which triggered a huge police response, raised alarm among Weste
- 2026-10-03 10:45 [BBC World] UK-Iranian dual national bailed after RAF Fairford incident arrest
  > The 25-year-old man was arrested in the London borough of Westminster on Thursday.
**B** (4 item(s))
- 2026-10-02 02:49 [BBC World] NY's governor appoints special prosecutor in Cornell frat rape investigation
  > The governor said she'd lost faith in prosecutors overseeing the case and handed it over to New York Attorney General Letitia James.
- 2026-10-02 17:10 [South China Morning Post] New York governor attacks handling of Cornell gang rape case, appoints special prosecutor
  > New York Governor Kathy Hochul on Friday faulted police and prosecutors for failing to fully investigate an alleged gang rape in 2024 at Cornell University, saying she was “deeply disturbed” by how the incident was handled.
Hochul was speaking at a press conference alongside state Attorney General L
- 2026-10-02 17:43 [Al Jazeera] ‘I want the truth’: NY governor appoints prosecutor in Cornell rape case
  > New York Governor Kathy Hochul says local authorities failed to properly investigate the 2024 allegations.
- 2026-10-02 17:44 [BBC World] Woman at centre of Cornell rape inquiry was 'failed' by officials, says New York governor
  > The woman, known as Jane Doe, alleges she was raped by seven students at a fraternity house at the university in 2024.

## U032
**A** (5 item(s))
- 2026-09-29 12:00 [South China Morning Post] US and China need shared risk vocabulary to manage AI threats: Beijing-linked think tank
  > Beijing and Washington should first develop a common language around AI risks rather than seek to resolve their broader technology rivalry, a leading Chinese think tank has advised.
The call from the China Institutes of Contemporary International Relations (CICIR), affiliated with the Ministry of St
- 2026-09-29 16:09 [BBC World] Trump rules out joint US-China venture to develop AI
  > The US president continues to push back on calls to establish guardrails around artificial intelligence, arguing it will stifle growth.
- 2026-09-29 19:32 [South China Morning Post] Trump rejects calls to work with China on AI safety despite Xi summit progress
  > US President Donald Trump said on Tuesday he does not want to work with China on addressing artificial intelligence (AI) risks, arguing that cooperation could undermine America’s lead in the fast-moving technology.
“Whoever wins superintelligence wins. You’re gonna have a winner and a loser, and you
- 2026-09-29 23:43 [Al Jazeera] Trump, tech bosses sign voluntary pact pledging ‘robust’ AI safeguards
  > US President Trump touts self-regulation amid the international community&#039;s and industry&#039;s calls for formal rules.
- 2026-09-30 05:00 [South China Morning Post] Chinese firms trail global peers on profits, but AI power boom offers bright spot: Natixis
  > China’s corporate sector remains considerably weaker than it was before the Covid-19 pandemic, but the country is emerging as a key beneficiary of the global artificial intelligence boom thanks to its ample power capacity, according to a Natixis survey of thousands of firms and a separate research r
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

## U033
**A** (14 item(s))
- 2026-10-04 11:15 [Al Jazeera] Brazil votes in deeply polarised election pitting Lula against Bolsonaro
  > Close race expected as left-wing leader Lula seeks fourth nonconsecutive term against right-wing Flavio Bolsonaro.
- 2026-10-04 17:48 [South China Morning Post] Brazilians head to polls in high-stakes, polarised election
  > Brazilians queued to vote on Sunday in the first round of a tight election, following a campaign dominated by corruption scandals, economic anxiety and accusations of US meddling.
The field of 13 candidates has been led by two clear front runners – leftist President Luiz Inacio Lula da Silva, 80, wh
- 2026-10-04 21:11 [BBC World] Polls close in Brazil as Lula and Flávio Bolsonaro remain neck and neck
  > If no candidate gets more than 50% of the vote, the election will go to a run-off on 25 October.
- 2026-10-05 00:27 [DW World] Brazil election: Bolsonaro and Lula head to runoff
  > Populist Flavio Bolsonaro has secured a thin lead over incumbent Luiz Inacio Lula da Silva, but the next president of Brazil will be decided in the runoff round, according to the country’s electoral court.
- 2026-10-05 03:16 [BBC World] Right-wing Flávio Bolsonaro wins first round of Brazil election
  > With neither candidate getting more than 50% of the vote, the election will go to a run-off on 25 October.
- 2026-10-05 04:51 [BBC World] Watch: How Brazil's dramatic election unfolded
  > Millions of Brazilians took to the polls on Sunday for the first round of the country's presidential elections.
- 2026-10-05 05:08 [Al Jazeera] Bolsonaro beats expectations in Brazil vote, faces Lula in runoff
  > Brazil’s presidential election is heading to a run-off after Bolsonaro and Lula both fell short of the 50% needed to win
- 2026-10-05 09:38 [France 24] Brazil heads to run-off as Bolsonaro pulls off shock first place finish in first round
  > Flavio Bolsonaro, a right-wing senator and son of former president Jair Bolsonaro, pulled off a surprise first-place finish ahead of President Luiz Inacio Lula da Silva in Brazil’s election Sunday. However, with neither candidate securing a majority the vote now heads to a run-off in three weeks.
- 2026-10-05 09:46 [South China Morning Post] Brazil-China ties in focus as Bolsonaro gets election edge over Lula
  > Brazil is set for a presidential run-off after right-wing challenger Flavio Bolsonaro won a surprise first-round victory, threatening Luiz Inacio Lula da Silva’s grip on power in South America’s largest economy.
Bolsonaro, son of imprisoned former president Jair Bolsonaro, took 47 per cent of the ba
- 2026-10-05 12:34 [Al Jazeera] Bolsonaro favourite to win: What Brazil’s first round of elections tells us
  > Analysts say Flavio Bolsonaro is projected to win the run-off vote on October 25 and become Brazil&#039;s next president.
- 2026-10-05 12:52 [France 24] Brazil presidential election: 'Bolsonaro being ahead is a surprise,' researcher says
  > Far-right candidate Flavio Bolsonaro has pulled off a surprise win in the first round of Brazil’s presidential election. He defied most polls to win with 47 percent, compared to 45 percent for leftist incumbent Luiz Inacio Lula de Silva. We spoke to Thomas Zicman de Barros, a research fellow at CEVI
- 2026-10-05 12:54 [France 24] 'Very bad result for Lula: Bolsonaro is far more effective at speaking to that growing middle class'
  > Eve Irvine is pleased to welcome Felipe Krause, the head of Oxford University's Brazilian Studies Programme. Brazil's election reflects a political landscape that has become increasingly polarized, explains Krause. And he describes the current mood as one of “tired polarization: People are just exha
- 2026-10-05 20:37 [France 24] Concerns of US interference weigh on Brazil vote
  > Conservative Senator Flavio Bolsonaro pulled off a surprise on Sunday in the first round of Brazil’s presidential election by finishing ahead of the incumbent left-wing President Lula, whom he will face in the runoff on October 25. Suspicions of U.S. interference have been hanging over the campaign,
- 2026-10-05 21:00 [Al Jazeera] Brazil’s presidential race head for a tough runoff
  > Brazil is heading into a fiercely contested presidential runoff after the first round revealed major gains for Bolsonaro
**B** (2 item(s))
- 2026-10-04 12:53 [Al Jazeera] Amid teen triumph and organisational chaos, Asian Games close in Japan
  > The continental competition hosted 17,000 athletes over two weeks in Aichi-Nagoya.
- 2026-10-05 13:01 [France 24] Japan bids farewell to Asian Games after fortnight of turmoil and records
  > The 20th Asian Games closed on Sunday after a rocky fortnight lit ​up by youthful brilliance in the sporting arenas but tempered by logistical dysfunction and subdued public interest. Olympic Council of Asia (OCA) President Sheikh Joaan bin Hamad Al Thani declared the Games closed at Mizuho Park Ath

## U034
**A** (14 item(s))
- 2026-09-29 23:39 [BBC World] US Supreme Court denies Christa Pike's last-ditch bid to halt execution
  > The Tennessee inmate has been awaiting execution since she was sentenced to death in 1996 for the murder of a teenage classmate.
- 2026-09-30 13:14 [Al Jazeera] Christa Pike seeks firing squad, not lethal injection: Inside US executions
  > Women make up about 1 percent of US executions. How do states put people to death, and why is it contested?
- 2026-09-30 15:29 [BBC World] Execution of US murderer Christa Pike halted shortly before it was due to happen
  > Pike was convicted and sentenced to death in 1996 for the murder of Colleen Slemmer.
- 2026-09-30 16:00 [South China Morning Post] US Tennessee’s first execution of a woman in 200 years halted
  > A US appeal court on Wednesday halted the ⁠execution of death row inmate Christa Pike in Tennessee, less than two hours before she was scheduled to become the first woman that state has put to death in more than 200 years.
The 6th US Circuit Court of Appeals ordered a “short stay of execution” to gi
- 2026-09-30 16:44 [Al Jazeera] US appeals court halts Tennessee execution of Christa Pike
  > Christa Pike was set to become the first woman executed by Tennessee in more than 200 years.
- 2026-09-30 23:42 [BBC World] US Supreme Court allows execution of Christa Pike to go ahead
  > The death by lethal injection was scheduled to happen earlier on Wednesday before judges from a lower court paused the execution.
- 2026-10-01 02:35 [Al Jazeera] Christa Pike’s execution by lethal injection fails in Tennessee
  > Witnesses say Tennessee officials were unable to execute Christa Pike after a lethal injection attempt.
- 2026-10-01 04:14 [South China Morning Post] Tennessee halts executions after Christa Pike survives 2 doses of lethal drug
  > Tennessee officials were unable to put Christa Pike to death on Wednesday for a 1995 murder after administering two doses of a lethal drug. A death penalty expert said it was an unprecedented failure, and Tennessee’s governor halted the remaining execution for the rest of the year.
Pike, 50, was ali
- 2026-10-01 04:55 [Al Jazeera] Execution of US woman Christa Pike fails after botched lethal injection
  > The high-profile execution of murderer Christa Pike is in disarray after two lethal injections failed to kill her.
- 2026-10-01 16:45 [BBC World] Tennessee halts executions after Christa Pike survives two lethal injection attempts
  > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
- 2026-10-02 03:02 [South China Morning Post] Christa Pike in ‘life-saving care’ after botched Tennessee execution
  > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from a prison execution c
- 2026-10-02 07:58 [Al Jazeera] Lawyers for US inmate who survived lethal injections demand release
  > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
- 2026-10-02 20:32 [BBC World] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say
  > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.
- 2026-10-02 20:57 [Al Jazeera] Christa Pike unconscious, on ventilator after botched execution: Lawyers
  > The Tennessee woman&#039;s legal team says doctors are working to clear doses of the drug pentobarbital from her system.
**B** (3 item(s))
- 2026-10-01 00:08 [BBC World] Swiss glaciers suffer 'disastrous' year of ice loss, threatening water supplies
  > Scientists say such rapid melting is no longer surprising given the pace of climate change.
- 2026-10-01 02:19 [South China Morning Post] Expert gives grim warning after Swiss glaciers shrink 20% in 5 years
  > Switzerland’s glaciers, which are disproportionately impacted by climate change, have lost nearly 20 per cent of their mass in five years, experts said on Thursday, with 2026 registering the second biggest melt on record.
Swiss glaciers saw 5.5 per cent of their volume melt away this year, the Glaci
- 2026-10-01 04:58 [Al Jazeera] ‘Catastrophic year’ as Swiss glaciers lose 5% of ice after heatwaves
  > Scientists are warning that Switzerland&#039;s glaciers have lost an ‘enormous’ amount of ice this year.

## U035
**A** (3 item(s))
- 2026-10-04 12:12 [South China Morning Post] India election chief faces calls to resign from protesters, opposition
  > Thousands of young protesters and opposition parties staged protests in the national ⁠capital and Mumbai on ⁠Sunday, demanding the resignation of Election Commission Chief ⁠Gyanesh Kumar, as police detained demonstrators for a third consecutive day.
Opposition leaders Raj Thackeray and Uddhav Thacke
- 2026-10-04 16:55 [Al Jazeera] Mass protests demanding poll chief resignation shake India for third day
  > Protesters say the election commission’s voter-roll revision has removed millions of eligible voters to benefit PM Modi.
- 2026-10-05 11:04 [France 24] Indian police detain demonstrators as protests over voter roll revision intensify
  > Thousands of youth protesters and opposition supporters rallied in Delhi and Mumbai on Sunday to demand the resignation of India's election commission chief over changes to ​voter rolls as ‌police detained some demonstrators for a third day.
**B** (2 item(s))
- 2026-10-05 16:08 [Rai News Esteri] Emergenza su volo British Airways per Chicago, aereo rientra a Londra
  > Unvolo British Airways diretto da Londra a Chicagoha dichiaratoun'emergenza e invertito la rottasopra l'Irlanda dopo una brusca discesa da circa 11.300 a 2.700 metri di quota. Lo riferisce il sito specializzato AirLive.

Il volo BA295, operato da un Boeing 777-200ER,era decollato da Heathrow alle 11
- 2026-10-05 17:00 [ANSA Mondo] Calano le maschere d'ossigeno durante il volo, aereo della British per Chicago torna a Londra
  > E' stato un problema di depressurizzazione nella cabina, secondo le prime ricostruzioni, a causare oggi l'emergenza che ha coinvolto un aereo passeggeri della British Airways, decollato stamattina da Londra in direzione Chicago, negli Usa, ma costretto a invertire la rotta a un'ora dalla partenza pe

## U036
**A** (12 item(s))
- 2026-10-03 17:24 [BBC Mundo] En fotos: las multitudinarias protestas en España contra la crisis de la vivienda
  > En decenas de ciudades se registraron manifestaciones después de que el Gobierno fracasara en su intento de lograr la aprobación parlamentaria de las medidas destinadas a frenar la subida de los alquileres y el precio de la vivienda.
- 2026-10-05 07:18 [Clarín Mundo] Pedro Sánchez adelantó las elecciones generales en España para el 29 de noviembre
  > El presidente español emitió un mensaje desde el Palacio de La Moncloa.En su discurso llamó a los españoles a decidir si quieren sumarse "a la ola derechista o seguir siendo un baluarte de justicia social".
- 2026-10-05 08:54 [France 24 Español] Pedro Sánchez anuncia elecciones anticipadas en España para el 29 de noviembre
  > El presidente del Gobierno español, el socialista Pedro Sánchez, anunció este lunes el adelanto de las elecciones generales al 29 de noviembre. Esto tras el rechazo por parte del Congreso de los diputados, el pasado viernes de los dos decretos sobre la vivienda en medio de masivas protestas de inqui
- 2026-10-05 10:09 [France 24 Español] Pedro Sánchez adelanta las elecciones en España al 29 de noviembre tras el revés parlamentario por la vivienda
  > El presidente del Gobierno español, Pedro Sánchez, decidió adelantar las elecciones generales al 29 de noviembre, después de que su Ejecutivo sufriera un nuevo revés parlamentario con el rechazo de sus medidas sobre vivienda. La convocatoria pone fin a la intención de agotar la legislatura hasta 202
- 2026-10-05 10:50 [France 24 Español] “Necesitamos una mayoría más amplia”: España adelanta las elecciones al 29 de noviembre
  > El presidente del gobierno español, Pedro Sánchez, anunció este lunes la disolución de las Cortes y el adelanto de las elecciones generales, después de que el Congreso de los Diputados rechazara el viernes dos decretos impulsados por el Ejecutivo con medidas para aliviar la crisis de vivienda. Las e
- 2026-10-05 10:54 [France 24 Español] Informe desde Barcelona: Pedro Sánchez convoca elecciones anticipadas en España
  > España se encamina a unas elecciones generales anticipadas después de que el presidente del Gobierno, Pedro Sánchez, anunciara la disolución de las Cortes y la convocatoria de comicios para el próximo 29 de noviembre. La decisión llega tras la derrota parlamentaria de los decretos de vivienda impuls
- 2026-10-05 12:31 [BBC Mundo] Pedro Sánchez convoca elecciones anticipadas tras el fracaso en el Congreso de sus decretos para enfrentar la crisis de la vivienda en España
  > El anuncio de Sánchez se produce tras varios días de protestas en el país europeo, surgidas a raíz del desalojo de la anciana Maricarmen. Las elecciones se celebrarán el próximo 29 de noviembre.
- 2026-10-05 14:39 [France 24 Español] Ruth Forero:"La intención de Pedro Sánchez es aprovechar la movilización en las calles"
  > España se encamina a unas elecciones generales anticipadas después de que el presidente del Gobierno, Pedro Sánchez, anunciara la disolución de las Cortes y la convocatoria de comicios para el 29 de noviembre. La decisión llega tras el rechazo parlamentario de los decretos de vivienda impulsados por
- 2026-10-05 19:00 [France 24 Español] La derecha celebra, la izquierda se organiza: así reacciona la política en España al adelanto electoral
  > El líder opositor Alberto Núñez Feijóo, que llevaba meses reclamando comicios anticipados, destacó que "por fin votaremos y España podrá elegir el país que quiere ser". Su Partido Popular encabeza las encuestas y, para él, las elecciones "van de que España gane a Sánchez y lo que representa". Desde 
- 2026-10-05 21:00 [Clarín Mundo] La sombra de la extrema derecha sobre Europa: de las presidenciales en Francia al adelantamiento electoral en España
  > • Un tercio de los gobiernos del bloque continental renovará sus mandatos a lo largo de los próximos doce meses.
• La masa de votantes definirá las administraciones de las principales potencias de la región, salvo en el caso alemán.
- 2026-10-05 21:40 [BBC Mundo] Por qué Pedro Sánchez decidió convocar elecciones anticipadas en España ahora
  > El llamado a elecciones anticipadas no fue una reacción impulsiva, sino una maniobra cuidadosamente meditada.
- 2026-10-05 22:03 [France 24 Español] Directo a... Madrid y el adelanto de las elecciones en España en medio de la crisis de vivienda
  > La crisis de vivienda en España y el rechazo del Congreso a las propuestas temporales para aliviar la situación empujó al presidente de Gobierno, Pedro Sánchez, a convocar elecciones anticipadas, estimadas para 2027, y disolvió las Cortes. Nuestra corresponsal Marina Colorado nos amplió la informaci
**B** (5 item(s))
- 2026-10-05 04:07 [Al Jazeera] Russian lab worker dies of suspected plague in Siberia; US monitoring case
  > A Russian agency links the lab worker&#039;s death to &#039;pneumonia of unknown&#039; origin.
- 2026-10-05 17:14 [South China Morning Post] After plague death reports at Siberia lab, Russia says situation under control
  > Moscow on Monday downplayed reports that a laboratory technician had died of plague, stressing that postmortem tests had not detected the disease, while Washington said it was closely monitoring the situation.
Reports on Friday that plague had killed a 28-year-old woman named Darya Shipilova, who ha
- 2026-10-05 19:19 [France 24] Russian officials say 'situation under control' after plague reports
  > Moscow on Monday downplayed reports that a laboratory technician had died of plague, stressing that post-mortem tests had not detected the disease, while Washington said it was closely monitoring the situation. Reports on Friday that plague had killed a 28-year-old woman named Darya Shipilova, who h
- 2026-10-05 19:55 [BBC World] US 'watching closely' after plague researcher dies in Russia, Rubio says
  > The US says it is monitoring the case of a lab technician who died at a plague research centre in Siberia.
- 2026-10-05 21:03 [Al Jazeera] Trump says US ready to aid Russia with plague outbreak in Siberia
  > Russian authorities quarantine hospital, monitor 200 contacts after suspected pneumonic plague death in Siberia.

## U037
**A** (2 item(s))
- 2026-09-30 03:00 [South China Morning Post] Boom News founder Tang Ho-wing, 1 other arrested by Hong Kong national security police
  > Hong Kong national security police have arrested two people, including the founder of online media outlet Boom News on suspicion of “incitement by spreading disinformation”, the South China Morning Post has learned
A source familiar with the matter said journalist Tang Ho-wing, the 37-year-old found
- 2026-09-30 22:16 [Al Jazeera] Hong Kong journalist arrested on sedition charge
  > Authorities detain media founder over Prince Edward station clash video, as press freedom groups voice concern.
**B** (3 item(s))
- 2026-09-30 15:04 [BBC World] Ethiopia fighting escalates in Tigray killing 52 civilians, medic tells the BBC
  > The deadly fighting has also spread to neighbouring regions, stranding tourists in Lalibela.
- 2026-10-01 11:25 [BBC World] Explosions heard in Ethiopia's capital after drone flights banned
  > It comes a week after fighting erupted north of the capital between the army and a new alliance of armed groups.
- 2026-10-01 13:25 [Al Jazeera] Blasts heard in Addis Ababa as Ethiopia conflict widens in the north
  > Thousands flee Mekelle amid advancing troops and disrupted services as tensions rise in Ethiopia&#039;s northern territories.

## U038
**A** (3 item(s))
- 2026-09-29 16:13 [Al Jazeera] ‘New path’: UK’s Burnham promises huge expansion of public services
  > UK prime minister tells his first Labour Party conference &#039;fundamental rethink&#039; needed to set Britain on right course.
- 2026-09-29 20:16 [South China Morning Post] PM Burnham vows big shake-up for UK in high-risk political speech
  > New British Prime Minister Andy Burnham set out a sweeping political vision on Tuesday, pledging to give Britain “a new social contract for the 21st century”, reform the country’s electoral system and reset its relationship with its European neighbours.
But he acknowledged that economic constraints 
- 2026-09-30 08:48 [Al Jazeera] UK‘s PM Burnham sets out plans to reshape public services
  > UK&#039;s PM Andy Burnham is promising a major improvement to public services including social care, housing and energy.
**B** (6 item(s))
- 2026-09-30 16:51 [South China Morning Post] UK PM says ‘strong indications’ Iran involved in bomb scare at US-run airbase
  > British Prime Minister Andy Burnham on Wednesday said there were “strong indications” that Iran was involved in suspicious activity at a UK airbase that triggered a major security incident this weekend.
“There are strong indications that Iran played a part in what happened over the weekend at RAF Fa
- 2026-09-30 18:09 [Al Jazeera] Strong indications’ Iran linked to suspected UK airbase plot
  > UK Prime Minister says there are ‘strong indications’ Iran played a part in the suspected RAF Fairford airbase plot.
- 2026-10-01 02:30 [Al Jazeera] UK says Iran may be linked to alleged airbase plot, drawing angry denial
  > Andy Burnham says UK has &#039;strong indications&#039; Iran involved in alleged security incident at RAF base used by US.
- 2026-10-01 16:55 [Al Jazeera] British police arrest UK-Iranian national over airbase incident
  > Counter Terrorism police also questioned a UK national, days after five others were arrested and released on bail.
- 2026-10-01 17:52 [South China Morning Post] UK-Iranian man arrested over suspected Fairford airbase plot
  > British counterterrorism police investigating ⁠a suspected plot involving ⁠an airbase used by the US ⁠to target Iran said on Thursday they had arrested a dual UK-Iranian national on suspicion of preparing terrorist acts.
In an incident which triggered a huge police response, raised alarm among Weste
- 2026-10-03 10:45 [BBC World] UK-Iranian dual national bailed after RAF Fairford incident arrest
  > The 25-year-old man was arrested in the London borough of Westminster on Thursday.

## U039
**A** (2 item(s))
- 2026-10-03 12:22 [BBC Mundo] Lo que la fallida ejecución de Christa Pike revela sobre la pena de muerte en EE.UU.
  > Christa Pike, una mujer condenada a muerte en Tennessee, sobrevivió a la aplicación de dos inyecciones letales. Su caso ha vuelto a centrar la atención en la pena de muerte y en cómo se aplica en Estados Unidos.
- 2026-10-03 19:14 [Il Sole 24 Ore Mondo] Trump vuole estendere la pena di morte ai narcotrafficanti: il caso Pike riapre lo scontro
  > Il presidente promette di ampliare i reati punibili con la pena capitale. Il Tennessee sospende le esecuzioni dopo il caso Pike, mentre una sentenza della Corte Suprema del 2008 lascia aperto il nodo dei grandi narcotrafficanti
**B** (10 item(s))
- 2026-10-04 21:31 [South China Morning Post] US Air Force removes all bombers from UK airbase targeted by suspected terror attack
  > The US Air Force has brought home its bombers stationed at a US-run military airbase in England used to strike Iran following an investigation into a planned terror attack at the RAF Fairford base.
The bombers were redeployed back to their home bases in the United States, according to a Pentagon off
- 2026-10-04 22:23 [Al Jazeera] US withdraws B-1 bomber aircraft from UK’s Fairford base amid Iran fears
  > The abrupt redeployment to the US comes after several &#039;terrorism-related&#039; arrests were made outside RAF Fairford.
- 2026-10-05 04:58 [BBC World] US air force removes all bombers from British military base RAF Fairford
  > A statement says all bombers deployed to RAF Fairford have been "re-deployed to their home stations" in the US.
- 2026-10-05 07:40 [Defense News] US removes B-1 bombers from UK base amid security concerns
  > NEW YORK — The United States removed its B-1 bombers from a U.K. air base one week after several men were arrested there on suspicion of preparing terrorist acts, a Pentagon official said on Sunday. A dozen B-1 bombers were stationed at RAF Fairford air base, located northwest of London. The planes 
- 2026-10-05 09:49 [France 24] US withdraws all bombers from UK base at centre of suspected terror attack
  > The United States has removed its B-1 bombers from a British air base one week after five men were arrested nearby on suspicion of preparing terrorist acts, a ‌suspected plot that British Prime Minister Andy Burnham said was likely backed by Iran. The planes had been ⁠stationed at RAF Fairford, whic
- 2026-10-05 11:09 [Al Jazeera] US abruptly withdraws bombers from UK’s RAF Fairford
  > The US has abruptly withdrawn all of its aircraft from the UK’s RAF Fairford, citing concerns about a potential attack.
- 2026-10-05 12:07 [BBC World] No10 insists UK military base RAF Fairford is safe after US withdraws bombers
  > US media reported a new threat led to the bombers being removed on Sunday, following an incident near the base last week.
- 2026-10-05 17:34 [Al Jazeera] Rubio: No direct link between US bombers removal and UK base incident
  > Rubio stresses US base security, following the removal of B-1 bombers amid alleged threats targeting UK military assets.
- 2026-10-05 19:58 [BBC World] Trump says 'threat' led US to pull bombers from RAF Fairford
  > The Pentagon confirmed on Sunday it had removed the B1 bombers from the base in England back to their home stations in America.
- 2026-10-05 21:40 [South China Morning Post] US bombers moved from UK airbase due to Iran-linked threats, Trump says
  > US President Donald Trump said on Monday that a threat linked to Iran ⁠had prompted the removal of American B-1 bombers from a British airbase.
The planes had been stationed at RAF Fairford, the preferred European base for US bombers, and had recently been used in US strikes on Iran. Last week, five

## U040
**A** (3 item(s))
- 2026-09-30 15:04 [BBC World] Ethiopia fighting escalates in Tigray killing 52 civilians, medic tells the BBC
  > The deadly fighting has also spread to neighbouring regions, stranding tourists in Lalibela.
- 2026-10-01 11:25 [BBC World] Explosions heard in Ethiopia's capital after drone flights banned
  > It comes a week after fighting erupted north of the capital between the army and a new alliance of armed groups.
- 2026-10-01 13:25 [Al Jazeera] Blasts heard in Addis Ababa as Ethiopia conflict widens in the north
  > Thousands flee Mekelle amid advancing troops and disrupted services as tensions rise in Ethiopia&#039;s northern territories.
**B** (4 item(s))
- 2026-10-01 20:10 [Al Jazeera] Eritrea severs diplomatic ties with Ethiopia in tit-for-tat move
  > Ethiopia says it will shut its embassy in Asmara, declares 10 Eritrean diplomats persona non grata.
- 2026-10-02 03:49 [South China Morning Post] Ethiopia and Eritrea sever diplomatic ties as northern fighting escalates
  > Ethiopia and Eritrea broke diplomatic ties on Thursday, accusing each other of stoking internal conflicts as fighting continued in northern Ethiopia.
Long-standing tensions between the two neighbours reached a crisis point after heavy fighting broke out last week between Ethiopian forces and the Tig
- 2026-10-02 04:40 [Al Jazeera] Eritrea severs diplomatic ties with Ethiopia in row over Tigray
  > Eritrea has severed diplomatic ties with Ethiopia after Addis Ababa closed its embassy in Asmara
- 2026-10-02 05:42 [BBC World] Ethiopia and Eritrea cut diplomatic ties as northern conflict escalates
  > The diplomatic fallout comes as Ethiopian forces battle rebel fighters across its northern region.

## U041
**A** (2 item(s))
- 2026-10-01 14:00 [South China Morning Post] China backs Cuba, Beijing’s Panama threat, new UN chief: 7 Latin America relations reads
  > We have selected seven of the most interesting and important news stories covering Latin American relations from the past few weeks. If you would like to see more of our reporting, please consider subscribing.
1. China pledges to ‘firmly support’ Cuba as US escalates pressure on Havana

China will s
- 2026-10-02 20:52 [Al Jazeera] Latin America sees China as more positive global influence than US: Poll
  > Annual Latinobarometro survey finds views of China’s influence improving as perceptions of US influence worsen.
**B** (6 item(s))
- 2026-10-02 01:23 [Al Jazeera] Trump says US may ask Europe to release diesel reserves
  > Skyrocketing diesel prices have pushed Washington to weigh an export ban, raising alarm across European economies.
- 2026-10-02 05:26 [BBC World] US pressures Europe over diesel reserves as Trump threatens export ban
  > President Donald Trump has threatened to ban diesel exports in a bid to ease prices in the US ahead of the November elections.
- 2026-10-02 13:16 [Al Jazeera] Trump vs Europe as US presses for release of emergency diesel stocks
  > Europe&#039;s leaders are mulling proposals to respond to Trump&#039;s diesel demands.
- 2026-10-02 14:51 [South China Morning Post] G7 nations agree to release diesel and oil stocks after Trump pressure
  > Group ⁠of Seven countries agreed on Friday to release 100 million barrels of diesel and crude oil from emergency reserves and pledged to refrain from energy export restrictions after pressure from US President Donald Trump.
The US led a pressure campaign on the European Union to draw down emergency 
- 2026-10-02 19:01 [Al Jazeera] Trump says Europe agreed to release ‘massive amount’ of diesel reserves
  > US President Donald Trump says Europe agreed to release a ‘massive amount’ of diesel from emergency stockpiles.
- 2026-10-02 20:25 [BBC World] G7 to release 100 million barrels of oil and diesel after Trump export ban threat
  > The co-ordinated release is aimed at heading off further price spikes and avoiding a ban on US diesel exports.

## U042
**A** (2 item(s))
- 2026-10-04 15:06 [Al Jazeera] Iran tells US: there is ‘no military solution’ to end the war
  > Iranian Foreign Minister Abbas Araghchi says the era of “wasting time and dictating demands is over’.
- 2026-10-04 19:44 [South China Morning Post] Iran tells US there is no military solution to Middle East war
  > Iran’s top diplomat insisted on Sunday that there would be no military solution to the United States’ war against the Islamic republic, with talks on ending the conflict apparently at an impasse.
A campaign of heavy bombardment failed to bring a decisive close to the war launched by the US and Israe
**B** (2 item(s))
- 2026-10-05 04:13 [Al Jazeera] FBI arrests ‘Chinese foreign agent’ for spying on Taiwan president’s son
  > A California woman allegedly sent photos and videos of President Lai&#039;s son and his family to Chinese officials.
- 2026-10-05 22:16 [South China Morning Post] US accuses mainland China of targeting Taiwan leader’s family in surveillance case
  > The United States has accused mainland China of hiring an American citizen of Chinese origin to surveil the family of Taiwanese leader William Lai Ching-te, days after President Xi Jinping’s state visit to Washington.
The Federal Bureau of Investigation on Sunday arrested 34-year-old Zhang Wanying a

## U043
**A** (10 item(s))
- 2026-10-04 21:31 [South China Morning Post] US Air Force removes all bombers from UK airbase targeted by suspected terror attack
  > The US Air Force has brought home its bombers stationed at a US-run military airbase in England used to strike Iran following an investigation into a planned terror attack at the RAF Fairford base.
The bombers were redeployed back to their home bases in the United States, according to a Pentagon off
- 2026-10-04 22:23 [Al Jazeera] US withdraws B-1 bomber aircraft from UK’s Fairford base amid Iran fears
  > The abrupt redeployment to the US comes after several &#039;terrorism-related&#039; arrests were made outside RAF Fairford.
- 2026-10-05 04:58 [BBC World] US air force removes all bombers from British military base RAF Fairford
  > A statement says all bombers deployed to RAF Fairford have been "re-deployed to their home stations" in the US.
- 2026-10-05 07:40 [Defense News] US removes B-1 bombers from UK base amid security concerns
  > NEW YORK — The United States removed its B-1 bombers from a U.K. air base one week after several men were arrested there on suspicion of preparing terrorist acts, a Pentagon official said on Sunday. A dozen B-1 bombers were stationed at RAF Fairford air base, located northwest of London. The planes 
- 2026-10-05 09:49 [France 24] US withdraws all bombers from UK base at centre of suspected terror attack
  > The United States has removed its B-1 bombers from a British air base one week after five men were arrested nearby on suspicion of preparing terrorist acts, a ‌suspected plot that British Prime Minister Andy Burnham said was likely backed by Iran. The planes had been ⁠stationed at RAF Fairford, whic
- 2026-10-05 11:09 [Al Jazeera] US abruptly withdraws bombers from UK’s RAF Fairford
  > The US has abruptly withdrawn all of its aircraft from the UK’s RAF Fairford, citing concerns about a potential attack.
- 2026-10-05 12:07 [BBC World] No10 insists UK military base RAF Fairford is safe after US withdraws bombers
  > US media reported a new threat led to the bombers being removed on Sunday, following an incident near the base last week.
- 2026-10-05 17:34 [Al Jazeera] Rubio: No direct link between US bombers removal and UK base incident
  > Rubio stresses US base security, following the removal of B-1 bombers amid alleged threats targeting UK military assets.
- 2026-10-05 19:58 [BBC World] Trump says 'threat' led US to pull bombers from RAF Fairford
  > The Pentagon confirmed on Sunday it had removed the B1 bombers from the base in England back to their home stations in America.
- 2026-10-05 21:40 [South China Morning Post] US bombers moved from UK airbase due to Iran-linked threats, Trump says
  > US President Donald Trump said on Monday that a threat linked to Iran ⁠had prompted the removal of American B-1 bombers from a British airbase.
The planes had been stationed at RAF Fairford, the preferred European base for US bombers, and had recently been used in US strikes on Iran. Last week, five
**B** (3 item(s))
- 2026-10-05 03:37 [BBC World] Trump unveils 'Super Intelligence Force' to oversee AI policy
  > The president named his national intelligence chief as the taskforce's head as worries over AI grow.
- 2026-10-05 10:03 [BBC World] Trump chooses top spy boss to run new AI taskforce
  > The US president said his national intelligence chief will lead the group as worries over AI grow.
- 2026-10-05 10:09 [France 24] Trump names Jay Clayton as AI czar to lead 'Super Intelligence Force'
  > US President Donald Trump has named his National Intelligence Director Jay Clayton as America's "Super Intelligence" czar, as fears over AI grow. Also, oil markets react to Houthi attacks as well as export data, and France's fiscal woes drive the euro to a 17-month low.

## U044
**A** (2 item(s))
- 2026-09-30 16:29 [Defense News] US Army selects five companies for PrSM development
  > The U.S. Army on Tuesday signed agreements with Anduril, Castelion, Lockheed Martin, Mach Industries and RTX to create advanced long-range missile prototypes, Redstone Arsenal announced this week. Each company will develop capabilities for the Precision Strike Missile (PrSM) Increment 4 program, mak
- 2026-09-30 19:08 [Breaking Defense] Army taps 5 companies for PrSM Inc 4 prototypes
  > Anduril, Castelion, Lockheed Martin, RTX and Mach Industries were awarded Other Transaction Agreements for an undisclosed amount.
**B** (5 item(s))
- 2026-09-30 22:13 [Al Jazeera] Russian drone crashes into Kyiv playground without exploding
  > A Russian attack drone crashed into a children’s playground in Kyiv, Ukraine without exploding.
- 2026-10-01 07:09 [South China Morning Post] Ukraine scrambles as Russia’s jet drones breach Kyiv’s defences
  > Russia’s new class of jet-powered drones rip across the night sky in Kyiv at hundreds of kilometres per hour, leaving Ukrainian air-defence units only moments to intercept them. It’s rarely enough time.
With many of the drones getting through to the capital, defence manufacturers are scrambling to d
- 2026-10-01 13:06 [Al Jazeera] Russian drone hits school in Ukraine’s Kyiv as Moscow presses air assault
  > Russian drone strikes hit a school in Kyiv and the main bridge, disrupting transport in the latest wave of attacks.
- 2026-10-02 08:03 [Al Jazeera] Russia tries to freeze Ukraine as it suffers record casualties and retreats
  > Moscow has suffered further losses of occupied territory, but is using new drones to beat Ukraine&#039;s defences.
- 2026-10-02 12:47 [Al Jazeera] Ukraine calls for tighter sanctions as Russian attacks spark Kyiv gridlock
  > Closure of bridges struck by drones in Ukrainian capital causes traffic chaos.

## U045
**A** (3 item(s))
- 2026-10-01 16:40 [BBC World] Renee Good: Family of US woman killed by ICE agent sues Trump officials
  > Lawyers for Good's family say US officials created "an unprecedented environment for state sponsored violence" in Minneapolis.
- 2026-10-01 17:28 [Al Jazeera] Renee Good’s family sues Trump administration over fatal ICE shooting
  > Lawsuits accuse Trump officials of recklessness and civil rights violations in Renee Good&#039;s fatal Minneapolis shooting .
- 2026-10-01 23:34 [South China Morning Post] Family of Renee Good, US woman killed by ICE agent, sues Trump administration
  > ⁠The family of Renee Good, one of two US citizens fatally shot by ⁠federal immigration agents in Minneapolis in January, sued the Trump administration on Thursday, saying there had been “no accountability” for her killing during deportation sweeps.
Good, 37, was shot dead in her car by a US Immigrat
**B** (6 item(s))
- 2026-10-02 01:23 [Al Jazeera] Trump says US may ask Europe to release diesel reserves
  > Skyrocketing diesel prices have pushed Washington to weigh an export ban, raising alarm across European economies.
- 2026-10-02 05:26 [BBC World] US pressures Europe over diesel reserves as Trump threatens export ban
  > President Donald Trump has threatened to ban diesel exports in a bid to ease prices in the US ahead of the November elections.
- 2026-10-02 13:16 [Al Jazeera] Trump vs Europe as US presses for release of emergency diesel stocks
  > Europe&#039;s leaders are mulling proposals to respond to Trump&#039;s diesel demands.
- 2026-10-02 14:51 [South China Morning Post] G7 nations agree to release diesel and oil stocks after Trump pressure
  > Group ⁠of Seven countries agreed on Friday to release 100 million barrels of diesel and crude oil from emergency reserves and pledged to refrain from energy export restrictions after pressure from US President Donald Trump.
The US led a pressure campaign on the European Union to draw down emergency 
- 2026-10-02 19:01 [Al Jazeera] Trump says Europe agreed to release ‘massive amount’ of diesel reserves
  > US President Donald Trump says Europe agreed to release a ‘massive amount’ of diesel from emergency stockpiles.
- 2026-10-02 20:25 [BBC World] G7 to release 100 million barrels of oil and diesel after Trump export ban threat
  > The co-ordinated release is aimed at heading off further price spikes and avoiding a ban on US diesel exports.

## U046
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
- 2026-09-29 16:56 [BBC World] Eiffel Tower chief to quit after female staff replaced by men during religious visit
  > The company that runs the Eiffel Tower said the removal of female staff during the visit earlier this month was "unacceptable".
- 2026-09-29 17:36 [South China Morning Post] Eiffel Tower chief stepping down over removal of women staff for Hindu group’s visit
  > The operating company that runs the Eiffel Tower said Tuesday its chief would step down at the end of this year in the wake of a controversy over the removal of women staff during a visit by a Hindu religious group.
Patrick Branco Ruivo, who has been director general of the Paris landmark since 2018

## U047
**A** (3 item(s))
- 2026-10-08 01:23 [France 24 Español] Directo a... Washington y las dudas generadas por fallida ejecución de Christa Pike
  > Christa Pike, condenada a muerte por el asesinato de una compañera de estudios en 1995, es la única persona que ha sobrevivido tras recibir fármacos de inyección letal, según el Centro de Información sobre la Pena de Muerte. Una semana después de su fallida ejecución, la mujer se encuentra despierta
- 2026-10-08 02:09 [ANSA Mondo] Giustiziato in Texas con iniezione letale, prima esecuzione dopo il caso Pike
  > Jamaal Howard, un americano di

46 anni, è stato giustiziato in Texas tramite una iniezione

letale, in quella che è la prima esecuzione dopo il tentativo

più volte fallito contro Christa Pike in Tennessee, appena una

settimana prima.Quella di Howard, condannato a morte per aver ucciso un

addetto
- 2026-10-08 02:52 [Rai News Esteri] Giustiziato Jamaal Howard: per gli Usa è la trentesima esecuzione dell'anno
  > L'uomo era condannato per l'omicidio di un commesso nel 2000. Primo caso dopo la vicenda di Christa Pike
**B** (2 item(s))
- 2026-10-08 11:18 [BBC Mundo] Cómo llegó Colombia a tener una deuda tan alta (y por qué De la Espriella tendrá que aumentarla)
  > El presupuesto presentado por el gobierno de De la Espriella prevee que la deuda llegará a 66,2% del PIB en 2027, la más alta de la historia del país.
- 2026-10-08 18:55 [France 24 Español] Directo Latam y el apoyo de De la Espriella a exmilitares acusados por asesinato de Jovenel Moïse
  > El presidente colombiano, Abelardo de la Espriella, ha manifestado su apoyo jurídico a 17 exmilitares acusados del magnicidio de Jovenel Moïse en 2021, quienes fueron trasladados a Estados Unidos para comparecer ante la Justicia. En paralelo, el mandatario busca implementar su Estatuto Antiterrorist

## U048
**A** (3 item(s))
- 2026-10-04 13:18 [Kyiv Independent] Germany announces $1.46 billion in aid for Ukraine, including interceptor drones, air defense missiles
  > The package was announced by President Volodymyr Zelensky and German Chancellor Friedrich Merz at a joint press conference in Kyiv.
- 2026-10-04 16:38 [Al Jazeera] Germany’s Merz in Kyiv announces $1.5B in aid, urges Putin to end war
  > German Chancellor Friedrich Merz, on a surprise visit to Kyiv, announced $1.5 billion in military and reconstruction aid
- 2026-10-05 16:22 [Breaking Defense] Germany pledges $1.1B military aid package to Ukraine flush with drone interceptors
  > &#8220;Russia must know that we will take steps to defend ourselves against any further escalation,&#8221; said German Chancellor Friedrich Merz.
**B** (2 item(s))
- 2026-10-05 10:36 [Defense News] Missiles, satellites and warplanes — Ukraine, Europe advance key arms projects
  > WARSAW, Poland — Ukraine’s drone and missile maker Fire Point is developing an extended-range tactical ballistic missile after its FP-7 weapon was used in combat for the first time on Oct. 1, the company’s CEO Iryna Terekh said during this year’s Helsinki Security Forum.As European nations are braci
- 2026-10-05 12:26 [Kyiv Independent] New automatic gun turrets successfully down first Russian jet-powered drones, Air Force says
  > President Volodymyr Zelensky previously announced that twelve such turrets had been installed where Russian jet-powered drones have been particularly active, including around Kyiv.

## U049
**A** (3 item(s))
- 2026-09-30 05:05 [Al Jazeera] Hegseth to cut number of US general and admiral positions by 20%
  > Pentagon official says the plan will be announced in the defence secretary&#039;s &#039;State of the Force&#039; address in Virginia.
- 2026-09-30 21:42 [South China Morning Post] Trump defence chief says US slashed number of generals and admirals by 20%
  > US Defence Secretary Pete Hegseth announced on Wednesday that the United States has slashed the number of its generals and admirals by 20 per cent, in a move he said is aimed at “accountability”.
Hegseth suggested the cuts targeted officers who failed to get on board with his efforts to ensure the m
- 2026-10-01 02:34 [Al Jazeera] Hegseth announces 20% cut to US military commanders
  > US Secretary of Defense Pete Hegseth says he’s firing 20% of the military’s generals and admirals.
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

## U050
**A** (14 item(s))
- 2026-09-29 23:39 [BBC World] US Supreme Court denies Christa Pike's last-ditch bid to halt execution
  > The Tennessee inmate has been awaiting execution since she was sentenced to death in 1996 for the murder of a teenage classmate.
- 2026-09-30 13:14 [Al Jazeera] Christa Pike seeks firing squad, not lethal injection: Inside US executions
  > Women make up about 1 percent of US executions. How do states put people to death, and why is it contested?
- 2026-09-30 15:29 [BBC World] Execution of US murderer Christa Pike halted shortly before it was due to happen
  > Pike was convicted and sentenced to death in 1996 for the murder of Colleen Slemmer.
- 2026-09-30 16:00 [South China Morning Post] US Tennessee’s first execution of a woman in 200 years halted
  > A US appeal court on Wednesday halted the ⁠execution of death row inmate Christa Pike in Tennessee, less than two hours before she was scheduled to become the first woman that state has put to death in more than 200 years.
The 6th US Circuit Court of Appeals ordered a “short stay of execution” to gi
- 2026-09-30 16:44 [Al Jazeera] US appeals court halts Tennessee execution of Christa Pike
  > Christa Pike was set to become the first woman executed by Tennessee in more than 200 years.
- 2026-09-30 23:42 [BBC World] US Supreme Court allows execution of Christa Pike to go ahead
  > The death by lethal injection was scheduled to happen earlier on Wednesday before judges from a lower court paused the execution.
- 2026-10-01 02:35 [Al Jazeera] Christa Pike’s execution by lethal injection fails in Tennessee
  > Witnesses say Tennessee officials were unable to execute Christa Pike after a lethal injection attempt.
- 2026-10-01 04:14 [South China Morning Post] Tennessee halts executions after Christa Pike survives 2 doses of lethal drug
  > Tennessee officials were unable to put Christa Pike to death on Wednesday for a 1995 murder after administering two doses of a lethal drug. A death penalty expert said it was an unprecedented failure, and Tennessee’s governor halted the remaining execution for the rest of the year.
Pike, 50, was ali
- 2026-10-01 04:55 [Al Jazeera] Execution of US woman Christa Pike fails after botched lethal injection
  > The high-profile execution of murderer Christa Pike is in disarray after two lethal injections failed to kill her.
- 2026-10-01 16:45 [BBC World] Tennessee halts executions after Christa Pike survives two lethal injection attempts
  > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
- 2026-10-02 03:02 [South China Morning Post] Christa Pike in ‘life-saving care’ after botched Tennessee execution
  > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from a prison execution c
- 2026-10-02 07:58 [Al Jazeera] Lawyers for US inmate who survived lethal injections demand release
  > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
- 2026-10-02 20:32 [BBC World] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say
  > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.
- 2026-10-02 20:57 [Al Jazeera] Christa Pike unconscious, on ventilator after botched execution: Lawyers
  > The Tennessee woman&#039;s legal team says doctors are working to clear doses of the drug pentobarbital from her system.
**B** (2 item(s))
- 2026-09-30 05:01 [BBC World] 'Backpack' declared Alaska's Fat Bear Week winner
  > "Backpack" defeated a bear known only as "910" in the final round of the annual competition.
- 2026-09-30 06:57 [Al Jazeera] Gentle giant Backpack wins Alaska’s Fat Bear Week
  > The contest celebrates the resilience of the 2,200 brown bears that live in the preserve on the Alaska Peninsula.

## U051
**A** (2 item(s))
- 2026-10-08 02:48 [Al Jazeera] Tanker hit by multiple projectiles off north coast of Qatar, UKMTO says
  > The UK maritime agency has reported a rise in attacks on vessels in the vital Strait of Hormuz.
- 2026-10-08 10:07 [BBC World] Tanker hit by multiple projectiles in Gulf off Qatar, maritime agency says
  > Casualties have been reported on the vessel, identified by a maritime intelligence firm as the oil and chemical tanker, Acers.
**B** (2 item(s))
- 2026-10-08 13:14 [Europa Press Internacional] Reino Unido y Alemania lanzan un plan conjunto para contrarrestar actos de sabotaje y ciberataques
  > El primer ministro de Reino Unido, Andy Burnham ha anunciado este jueves durante un encuentro con el canciller alemán, Friedrich Merz, el lanzamiento de un plan conjunto para hacer frente a acciones de sabotaje y ciberataques a medida que ambos países cooperan para impulsar a nivel sus industrias te
- 2026-10-08 15:54 [France 24 Español] Burnham y Merz firman un acuerdo de cooperación en seguridad en medio de la amenaza rusa
  > El primer ministro de Reino Unido, Andy Burnham, abre la puerta a Alemania para que se una al programa GCAP, para la construcción de un avión de combate de sexta generación en colaboración con Italia y Japón. El canciller alemán, Friedrich Merz, celebra la ratificación del Tratado de Kensington, mie

## U052
**A** (2 item(s))
- 2026-10-08 12:14 [State Department] United States and Zambia Sign Five-Year Global Health Partnership under the Trump Administration’s America First Global Health Strategy
  > Thomas &quot;Tommy&quot; Pigott, SpokesmanOffice of the Spokesman



	

		
		

			

		

		

			

				
				

					
						United States and Zambia Sign Five-Year Global Health Partnership under the Trump Administration’s America First Global Health Strategy 
					
				

				

					

					
					
						
- 2026-10-08 16:24 [BBC World] Zambia signs US health deal after disputes over data-sharing
  > The US will provide $1.5bn (£1.1bn) under the deal that was negotiated after Trump cut USAID funding.
**B** (3 item(s))
- 2026-10-08 14:09 [France 24] Search warrants for former prince Andrew's homes were unlawful, UK court rules
  > Police who searched the properties of Andrew Mountbatten-Windsor as part of investigations into his links to the late sex offender Jeffrey Epstein have agreed the search warrants were unlawful, a London judge said Thursday. The 66-year-old younger brother of King Charles II was arrested on February 
- 2026-10-08 15:20 [South China Morning Post] UK police accept ex-prince Andrew search warrants must be ‘legally quashed’
  > British police on Thursday said that search warrants they secured to search properties linked to Andrew Mountbatten-Windsor had been issued unlawfully and must be quashed, but that the investigation into King Charles’ younger brother was ongoing.
Mountbatten-Windsor, 66, was arrested on suspicion of
- 2026-10-08 15:53 [Al Jazeera] UK ex-prince Andrew search warrants quashed after police accept legal error
  > London-based judge says error &#039;does not bring investigation to an end&#039; as police probe disgraced former royal.

## U053
**A** (3 item(s))
- 2026-09-30 18:01 [Al Jazeera] Trump set to announce $200bn in energy investments from South Korea
  > The investments come as Trump seeks to tout the Republican Party&#039;s economic record ahead of the US midterm races.
- 2026-10-01 01:44 [South China Morning Post] Trump touts US$200 billion South Korean energy deal ahead of US midterms
  > US President Donald Trump has announced US$200 billion in energy investments from South Korea, including US$54 billion towards a long-discussed liquefied natural gas project in Alaska and more than US$100 billion in planned longer-term nuclear power investments.
Besides the Alaska LNG project and pi
- 2026-10-01 10:36 [South China Morning Post] South Korea hits back at Trump’s investment claims in ‘tit-for-tat move’
  > US President Donald Trump’s unilateral announcement of a “colossal” South Korean investment package has prompted Seoul to clarify that the deal is far from finalised, laying bare stark differences between the allies over the terms of their trade agreement, observers have said.
On Wednesday, Trump an
**B** (2 item(s))
- 2026-10-02 02:07 [Al Jazeera] Everything you need to know about Brazil’s tight presidential race
  > Voters will soon decide between President Luiz Inácio Lula da Silva and the son of former President Jair Bolsonaro.
- 2026-10-02 06:21 [South China Morning Post] Lula and Bolsonaro clash in final scramble for Brazil presidency
  > Brazil’s President Luiz Inacio Lula da Silva and his election rival Flavio Bolsonaro are leaving no controversy unturned in their last-ditch efforts to discredit each other and win over voters ahead of Sunday’s nail-biter election.
A campaign dominated by scandals and insults has done little to ease

## U054
**A** (12 item(s))
- 2026-10-04 18:42 [South China Morning Post] Hundreds of schools to close on Monday as education protests rock France
  > Up to 500 schools across France will be totally or partly closed on Monday because of a wave of pupil protests that has shaken the country, the education minister said.
Lessons will be “totally or partly suspended” in some “400-500” high schools as the security conditions “have not been fulfilled”, 
- 2026-10-04 19:41 [Al Jazeera] France to shutter up to 500 schools as more student protests called
  > Education minister cites safety concerns for closures as organisers call for resumption of protests.
- 2026-10-05 04:49 [BBC World] France closes up to 500 schools Monday over student protests
  > Lessons will be "totally or partly suspended" in some high schools after clashes between riot police and student protesters, France's education minister says.
- 2026-10-05 05:48 [DW World] Hundreds of French schools closed amid protests
  > The student protests that rocked France last week have prompted authorities to keep up to 500 schools closed on Monday. More protests are planned for Tuesday.
- 2026-10-05 05:48 [DW World] Hundreds of French schools shut, teen loses hand in protests
  > The student protests that rocked France last week have prompted authorities to keep up to 500 schools closed on Monday. A teenage boy lost his hand, seemingly while trying to pick up a police tear gas grenade.
- 2026-10-05 08:46 [France 24] Up to 500 French schools to be closed Monday as protests continue
  > Up to 500 French high ⁠schools will begin a second week of total or partial closures on Monday as protests over dilapidated schools and classrooms, overcrowding and teacher shortages precede a nationwide day of demonstrations on Tuesday. Reporting from outside a high school in the Paris suburb of Au
- 2026-10-05 12:25 [Al Jazeera] Students continue to protest in France as hundreds of schools close
  > Education Minister Edouard Geffray said on Sunday about 500 schools likely to be fully or partially closed on Monday.
- 2026-10-05 14:20 [South China Morning Post] France school protests: teenager’s hand blown off after picking up grenade
  > A 15-year-old student lost a hand on Monday picking up a police grenade as part of nationwide protests in France over classroom conditions that have disrupted lessons at hundreds of schools since last week.
Some students returned to classrooms but others maintained actions outside their schools, ahe
- 2026-10-05 15:01 [France 24] 'I could feel the petrol dripping': The violent attacks that have marred France school protests
  > Between 400-500 schools across France are expected to stay closed this Monday, as student protests continue. Pupils are calling for smaller class sizes and better equipped classrooms. More than 70 schoolteachers have been injured since the unrest began. Ellen Gainsford & France 2 take a look at some
- 2026-10-05 15:03 [France 24] French school protests continue with larger demonstrations set for Tuesday
  > Lessons were suspended at hundreds of French high schools on Monday, as part of a wave of student protest over learning conditions that have rocked the country. An even larger day of demonstrations is expected on Tuesday.
- 2026-10-05 20:08 [France 24] 'We are effectively maiming young people' - expert questions France's response to student protests
  > A 15-year-old lost a hand on Monday picking up a police grenade amid nationwide school protests demanding better funding and classroom conditions. Speaking with FRANCE 24's Mark Owen, Ariane Bogain, Senior Lecturer in French Politics at Northumbria University, says that "there is a definite issue wi
- 2026-10-05 21:18 [BBC World] France braces for national day of school protests after injuries and mass arrests
  > France prepares for a day of protests in support of students who’ve been demanding more investment in education.
**B** (3 item(s))
- 2026-10-05 03:37 [BBC World] Trump unveils 'Super Intelligence Force' to oversee AI policy
  > The president named his national intelligence chief as the taskforce's head as worries over AI grow.
- 2026-10-05 10:03 [BBC World] Trump chooses top spy boss to run new AI taskforce
  > The US president said his national intelligence chief will lead the group as worries over AI grow.
- 2026-10-05 10:09 [France 24] Trump names Jay Clayton as AI czar to lead 'Super Intelligence Force'
  > US President Donald Trump has named his National Intelligence Director Jay Clayton as America's "Super Intelligence" czar, as fears over AI grow. Also, oil markets react to Houthi attacks as well as export data, and France's fiscal woes drive the euro to a 17-month low.

## U055
**A** (2 item(s))
- 2026-10-07 18:40 [BBC World] Eritrean troops move deep into Ethiopia's Tigray region, residents tell BBC
  > Residents of Adigrat tell the BBC they have seen truck loads of soldiers from Eritrea moving south.
- 2026-10-08 10:30 [France 24] Eritrean troops reportedly enter Ethiopia’s Tigray region
  > Eritrean troops have deployed in Ethiopia's northern Tigray region, multiple sources said Wednesday, threatening to turn an internal conflict into a wider regional war. Fighting broke out between the rebel Tigray People's Liberation Front (TPLF) and Ethiopian federal forces on September 23, sparking
**B** (3 item(s))
- 2026-10-08 14:09 [France 24] Search warrants for former prince Andrew's homes were unlawful, UK court rules
  > Police who searched the properties of Andrew Mountbatten-Windsor as part of investigations into his links to the late sex offender Jeffrey Epstein have agreed the search warrants were unlawful, a London judge said Thursday. The 66-year-old younger brother of King Charles II was arrested on February 
- 2026-10-08 15:20 [South China Morning Post] UK police accept ex-prince Andrew search warrants must be ‘legally quashed’
  > British police on Thursday said that search warrants they secured to search properties linked to Andrew Mountbatten-Windsor had been issued unlawfully and must be quashed, but that the investigation into King Charles’ younger brother was ongoing.
Mountbatten-Windsor, 66, was arrested on suspicion of
- 2026-10-08 15:53 [Al Jazeera] UK ex-prince Andrew search warrants quashed after police accept legal error
  > London-based judge says error &#039;does not bring investigation to an end&#039; as police probe disgraced former royal.

## U056
**A** (3 item(s))
- 2026-10-08 14:09 [France 24] Search warrants for former prince Andrew's homes were unlawful, UK court rules
  > Police who searched the properties of Andrew Mountbatten-Windsor as part of investigations into his links to the late sex offender Jeffrey Epstein have agreed the search warrants were unlawful, a London judge said Thursday. The 66-year-old younger brother of King Charles II was arrested on February 
- 2026-10-08 15:20 [South China Morning Post] UK police accept ex-prince Andrew search warrants must be ‘legally quashed’
  > British police on Thursday said that search warrants they secured to search properties linked to Andrew Mountbatten-Windsor had been issued unlawfully and must be quashed, but that the investigation into King Charles’ younger brother was ongoing.
Mountbatten-Windsor, 66, was arrested on suspicion of
- 2026-10-08 15:53 [Al Jazeera] UK ex-prince Andrew search warrants quashed after police accept legal error
  > London-based judge says error &#039;does not bring investigation to an end&#039; as police probe disgraced former royal.
**B** (3 item(s))
- 2026-10-08 15:50 [South China Morning Post] US suspends Microsoft, major IT firms from green card programme
  > The US government ⁠is suspending Microsoft, Adobe and ⁠several large IT firms from a programme that allows skilled foreign workers to gain permanent residency, senior US officials have announced, citing alleged fraud, and as part ‌of an effort to push companies to hire more Americans.
“Our message t
- 2026-10-08 17:25 [Al Jazeera] US suspends Microsoft and Adobe from visa programme amid fraud claims
  > Visa probe also targets universities for allegedly exploiting international students to reduce US wage costs.
- 2026-10-08 19:05 [South China Morning Post] US investigates 9 universities over alleged visa fraud, with focus on China
  > The Trump administration is launching an investigation into nine US universities over alleged J-1 visa fraud, with officials raising concerns about Chinese scholars and the Chinese government.
The J-1 programme covers exchange visitors including international researchers, scholars and students, who 

## U057
**A** (3 item(s))
- 2026-10-01 16:40 [BBC World] Renee Good: Family of US woman killed by ICE agent sues Trump officials
  > Lawyers for Good's family say US officials created "an unprecedented environment for state sponsored violence" in Minneapolis.
- 2026-10-01 17:28 [Al Jazeera] Renee Good’s family sues Trump administration over fatal ICE shooting
  > Lawsuits accuse Trump officials of recklessness and civil rights violations in Renee Good&#039;s fatal Minneapolis shooting .
- 2026-10-01 23:34 [South China Morning Post] Family of Renee Good, US woman killed by ICE agent, sues Trump administration
  > ⁠The family of Renee Good, one of two US citizens fatally shot by ⁠federal immigration agents in Minneapolis in January, sued the Trump administration on Thursday, saying there had been “no accountability” for her killing during deportation sweeps.
Good, 37, was shot dead in her car by a US Immigrat
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

## U058
**A** (2 item(s))
- 2026-09-30 17:06 [South China Morning Post] UK-France deal targeting migrants crossing English Channel is scrapped
  > A pilot programme between the UK and France that aimed to curb the number of migrants crossing the English Channel in small boats has been scrapped, Britain’s government said on Wednesday.
In a statement, the Home Office said the so-called “one in, one out” deal is “no longer processing new cases”.

- 2026-09-30 17:11 [BBC World] UK-France 'one in, one out' migrant scheme scrapped
  > Some 1,500 people have been removed to France since the scheme began just over a year ago.
**B** (3 item(s))
- 2026-09-30 17:07 [Al Jazeera] MI5 warns UK academics to cut ties with Chinese group over alleged spying
  > UK intelligence agency accuses Chinese institute of funding academic research to boost Beijing’s espionage capability.
- 2026-09-30 18:16 [South China Morning Post] UK accuses China of using academics to spy on AI and other tech research
  > Britain’s MI5 spy agency issued an unprecedented alert on Wednesday to warn that a Chinese organisation was involved in funding academic research into topics such as AI on behalf of Beijing’s state security service.
In its “Espionage Alert”, MI5 said more than 100 UK-based academics had contributed 
- 2026-10-01 16:28 [Al Jazeera] Chinese hackers impersonated AI experts to target US policy minds
  > TA419 hackers used deceptive tactics to impersonate real figures, such as a former White House AI official.

## U059
**A** (11 item(s))
- 2026-10-04 03:42 [BBC World] 'Anger in the streets': Tens of thousands protest in Spain over housing crisis
  > More than 50 protests took place on Saturday after the government failed to get emergency legislation through parliament.
- 2026-10-05 08:21 [Rai News Esteri] La protesta degli studenti a Parigi: in fiamme il portone di un liceo, sassaiola contro gli agenti
  > I liceali hanno affrontato la polizia sparando fuochi d'artificio
- 2026-10-05 12:02 [ANSA Mondo] Ségolène Royal denuncia la 'repressione' degli studenti in Francia
  > 'I govani bisogna amarli, non picchiarli.Se scompare l'empatia la barbarie non è distante'
- 2026-10-05 13:50 [France 24 Español] Más de 400 colegios bloqueados en Francia en la segunda semana de protestas estudiantiles
  > Al menos 413 institutos de secundaria en Francia se paralizaron el lunes debido a la prolongación de las protestas estudiantiles, según el Ministerio de Educación. Los manifestantes piden más profesores, una mejora de las infraestructuras y una reducción de la jornada escolar. El martes está convoca
- 2026-10-05 13:54 [Rai News Esteri] La protesta degli studenti in Francia, a Parigi vetrine dei negozi prese d'assalto dai manifestanti
  > Cassonetti rovesciati, sassaiole contro la polizia, fumogeni e cori intonati per strada: lo scenario delle proteste dei liceali francesi nella capitale
- 2026-10-05 14:37 [France 24 Español] Directo París y el panorama de las protestas estudiantiles en Francia
  > Francia vive una de las mayores olas de protestas estudiantiles de los últimos años. Aunque el ambiente se encuentra más tranquilo, cerca de 400 escuelas permanecen cerradas y en algunas ciudades se han presentado disturbios. El primer ministro Lecornu presentó una hoja de ruta para abordar la situa
- 2026-10-05 17:26 [ANSA Mondo] Gli studenti tornano in piazza, la Francia teme il caos generale
  > Gli studenti tornano in piazza in tutta la Francia e crescono i timori che le nuove manifestazioni posano innesecare un caos generale. La situazione alla vigilia del 'terzo atto' della protesta dei liceali, ormai appoggiati anche dai colleghi di diverse universitrà, è apparsa incandescente. A poco s
- 2026-10-05 17:31 [France 24 Español] Francia: más de 400 escuelas permanecen cerradas mientras continúan las protestas estudiantiles
  > Las protestas estudiantiles continúan en Francia, donde cientos de escuelas e institutos se han visto afectados por bloqueos y movilizaciones. Los estudiantes denuncian la falta de profesores, las aulas masificadas, el deterioro de las condiciones de aprendizaje y de las infraestructuras. Ante la cr
- 2026-10-05 17:45 [El País Internacional] Francia encara una nueva semana de protestas estudiantiles, las mayores en décadas
  > Estudiantes franceses de secundaria se manifiestan frente al instituto Sophie Germain de París este lunes.
- 2026-10-05 17:53 [Il Sole 24 Ore Mondo] Francia, allarme governatore banca centrale: «Strozzati dai tassi»
  > Se la Francia non adotta un piano di bilancio in grado di ridurre la spesa e il deficit rischia di vedersi “progressivamente strangolare dal rialzo dei tassi di interesse”. È...
- 2026-10-05 18:28 [Rai News Esteri] Protesta studenti, oltre 5.000 fermi. Domani il corteo a Parigi con i sindacati
  > Nonostante le dure contestazioni subite dagli studenti, il ministro dell'Educazione nazionale Édouard Geffray ha definito "legittima" la mobilitazione nazionale prevista per domani, pur condannando fermamente le violenze
**B** (2 item(s))
- 2026-10-05 14:08 [South China Morning Post] France, Germany call for new weapon allowing ‘immediate cut off’ of China from EU market
  > In the strongest sign yet of a shifting European Union policy on China, the leaders of France and Germany have demanded a new trade weapon that would cut off access to the EU market when third countries cause severe distortions.
The tool would effectively act as a kill switch, allowing Brussels to r
- 2026-10-05 17:01 [France 24] France, Germany seek new EU rapid response tool against trade threats
  > France and Germany proposed a new legal tool to enable the EU to respond rapidly to trade wars or measures, such as dumping, that could economically harm the bloc. While French President Emmanuel Macron and German Chancellor Friedrich Merz said the proposal was not a direct response to the actions o

## U060
**A** (56 item(s))
- 2026-10-04 03:30 [El País Internacional] Ni Bolsonaro, ni Lula: Trump se reserva (de momento) su apoyo en las elecciones de Brasil
  > Un asistente a un mitin de Flavio Bolsonaro disfrazado de Trump, el pasado domingo.
- 2026-10-04 04:00 [El País Internacional] La disputa entre Lula y Trump marca las elecciones brasileñas
  > Banderas de Flavio Bolsonaro y Luiz Inacio Lula da Silva en Brasilia, el 29 de septiembre.
- 2026-10-04 11:20 [Rai News Esteri] Urne aperte in Brasile per le elezioni presidenziali e legislative, sfida Lula-Bolsonaro
  > Gli ultimi sondaggi davano un testa a testa
- 2026-10-04 20:19 [El País Internacional] Brasil decide su futuro entre Lula y Bolsonaro, un estadista desgastado y el hijo de un ultra
  > El presidente Lula, el día 24 en São Gonçalo, y Flávio Bolsonaro, este sábado en Río.
- 2026-10-04 20:43 [Europa Press Internacional] Bolsonaro gana la primera vuelta en Brasil con el 47% de los votos y disputará contra Lula (45%) la segunda vuelta
  > El candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil e hijo del expresidente Jair Bolsonaro, Flávio Bolsonaro, ha ganado la primera vuelta de las elecciones en Brasil con un 47,17% de los sufragios. Su rival y presidente saliente, Luiz Inácio Lula da Silva, ha quedado cua
- 2026-10-04 22:25 [ANSA Mondo] Media, Lula e Bolsonaro andranno al ballottaggio il 25 ottobre
  > A metà scrutinio Bolsonaro al 49%, Lula a 42%
- 2026-10-04 23:00 [Clarín Mundo] Los Bolsonaro amplían su presencia en el Congreso con las elecciones en Brasil: entran la esposa del ex presidente y dos hermanos de Flavio
  > Michelle, la exprimera dama brasileña alcanzó el 28% de los votos en las elecciones legislativas del Distrito Federal.Otros dos hijos del expresidente Jair Bolsonaro compitieron por bancas legislativas en el estado de Santa Catarina.
- 2026-10-04 23:23 [Clarín Mundo] Elecciones en Brasil: Flávio Bolsonaro, un presidenciable a la sombra de su padre
  > Tiene 45 años y es el mayor de los cinco hijos del ex presidente. Elogia las políticas de seguridad de Nayib Bukele en El Salvador y promete la construcción de numerosas cárceles. Asimismo, presume de su buena relación con Donald Trump tras mantener una reunión privada en la Casa Blanca.
- 2026-10-04 23:23 [Clarín Mundo] Lula da Silva busca su reelección en Brasil: entre el freno a la ultraderecha y la defensa de su legado social
  > • A los 80 años, el mandatario brasileño busca la reelección apoyado en su historial de programas sociales como el Bolsa Familia, que actualmente beneficia a una cuarta parte de la población.
• Con vistas a un nuevo período, impulsa una reforma laboral para reducir la jornada semanal a cinco días y 
- 2026-10-05 00:09 [Rai News Esteri] Il sorpasso di Bolsonaro, la crisi di Lula
  > Flavio Bolsonaro, figlio dell'ex presidente di estrema destra tentato golpista, vince il primo turno sul presidente di sinistra Lula da Silva
- 2026-10-05 00:12 [Clarín Mundo] Elecciones en Brasil: un voto castigo que sorprendió a Lula da Silva y llegó desde su base tradicional de votantes
  > Un primer análisis indica que los sectores de menores ingresos se distanciaron de la elección y del líder del PT. El país es un éxito macro, con números notables, pero esos resultados no llegaron a los bolsillos de ese amplio espacio de votantes que se endeuda para pagar los gastos básicos.
- 2026-10-05 01:03 [Clarín Mundo] Lula acepta el impacto del triunfo de Bolsonaro: fue "un resultado inesperado"
  > El representante del socialista Partido de los Trabajadores busca su cuarto mandato, con la reelección en la gestión actual.Quedó detrás de Flavio Bolsonaro por apenas 2,15 puntos.
- 2026-10-05 01:08 [Clarín Mundo] Flavio Bolsonaro, tras ganar en primera vuelta ante Lula: "Brasil quiere un cambio"
  > Aseguró también que este resultado marcan "el fin de la era del PT" en su país.Dijo estar "feliz" con los números obtenidos frente al actual mandatario, Lula da Silva.
- 2026-10-05 01:41 [El País Internacional] Arrasadora victoria de la derecha en Brasil
  > Flavio Bolsonaro habla con la prensa en Río de Janeiro, este domingo.
- 2026-10-05 02:13 [Europa Press Internacional] Bolsonaro proclama "fin de la era del PT" y Lula apela a combatir su "pasado tenebroso" en la segunda vuelta en Brasil
  > Bolsonaro supera los 55 millones de apoyos (47,04%) y logra una ventaja de 2,3 millones de sufragios sobre el actual mandatario (45,15%)
- 2026-10-05 02:28 [El País Internacional] El apellido Bolsonaro gana desde la cárcel
  > Flávio Bolsonaro, candidato presidencial de Brasil, este domingo tras los resultados de la primera vuelta.
- 2026-10-05 02:39 [BBC Mundo] Cómo se compara Flávio Bolsonaro con su padre Jair y cuánto cambia el duelo con Lula por la presidencia de Brasil 4 años después
  > El senador derechista pasa fortalecido al balotaje contra el presidente de izquierda tras obtener más votos en la primera vuelta contra varios pronósticos, pero la elección sigue abierta.
- 2026-10-05 02:46 [France 24 Español] Simone Pitta: "Con esta primera vuelta se puede ver una consolidación del bolsonarismo en Brasil"
  > Pese a no haber estado en el poder en el último periodo presidencial de Brasil, y pese a las denuncias y condenas contra el expresidente Jair Bolsonaro por un intento de golpe de Estado, el bolsonarismo logró consolidarse de cara a los comicios de este 4 de octubre. Ahora, Flávio Bolsonaro busca pos
- 2026-10-05 02:47 [France 24 Español] Juan Agulló: "A diferencia de otros países de Latinoamérica, Brasil es un competidor directo"
  > En un escenario marcado por la polarización en Brasil, el candidato de ultraderecha y heredero político de su padre, Flávio Bolsonaro, y el actual presidente, Luiz Inácio Lula da Silva, quien busca un cuarto mandato, se disputan el balotaje. La sombra de Estados Unidos estuvo presente durante la pri
- 2026-10-05 02:54 [El País Internacional] Bolsonaro vence a Lula en primera vuelta de las elecciones y acaricia el retorno de la ultraderecha al poder en Brasil
  > Flávio Bolsonaro habla tras clasificarse para la segunda vuelta en Brasilia, Brasil, este domingo.
- 2026-10-05 03:19 [France 24 Español] Brasil: la derecha de Bolsonaro se fortalece en las regiones, con un triunfo holgado en São Paulo
  > Los comicios locales de Brasil se saldaron este domingo con un avance de la derecha que representan el candidato presidencial Flávio Bolsonaro y sus aliados. En tanto la izquierda del presidente y aspirante a la reelección, Luiz Inácio Lula da Silva perdía terreno. La victoria más cómoda fue en São 
- 2026-10-05 03:36 [El País Internacional] Las claves de la primera vuelta en Brasil: de la fuerza ultra al día después de Lula con América Latina pendiente
  > Flávio Bolsonaro vota en Río de Janeiro, este domingo.
- 2026-10-05 03:41 [France 24 Español] Flávio Bolsonaro tritura las encuestas: una ventaja pequeña, pero un escenario cuesta arriba para Lula
  > Brasil quedó inclinado hacia la tendencia de retorno a la derecha que sacude a América Latina, luego de que el senador e hijo del expresidente Jair Bolsonaro aventajara por casi dos puntos al izquierdista Luiz Inácio Lula da Silva en la primera vuelta de las elecciones. Lula ha reconocido el resulta
- 2026-10-05 04:08 [El País Internacional] Videoanálisis | Lula se enfrenta a una segunda vuelta electoral muy complicada
  > Videoanálisis | Lula Y Flávio Bolsonaro se enfrenta a una segunda vuelta electoral
- 2026-10-05 04:33 [Rai News Esteri] Brasile, avanzata del clan Bolsonaro: quattro eletti in Parlamento, Flavio al ballottaggio con Lula
  > L'ex first lady Michelle e Carlos, uno dei figli dell'ex presidente, conquistano un seggio al Senato. Alla Camera entrano il figlio più giovane Jair Renan e Renato, fratello di Jair
- 2026-10-05 05:14 [Il Sole 24 Ore Mondo] Brasile, Bolsonaro vince al primo turno con 47%, Lula al 45%: ballottaggio il 25 ottobre
  > Flavio Bolsonaro batte Lula al primo turno e si lancia come favorito nel ballottaggio del 25 ottobre che deciderà chi sarà il 40esimo presidente del Brasile. Il candidato trumpiano ha ottenuto il 47,14 % dei voti, il presidente uscente il 45.03 %, con una differenza tra i due di circa 2 milioni e me
- 2026-10-05 05:31 [Europa Press Internacional] Trump tacha de "corruptas" las elecciones de EEUU comparándolas con las de Brasil tras la victoria de Bolsonaro
  > El presidente de Estados Unidos, Donald Trump, ha vuelto a cargar contra el proceso electoral en su propio país, tachándolo de corrupto y contraponiéndolo la rapidez en el escrutinio de los votos de 125 millones de personas "en la primera vuelta de las elecciones presidenciales de Brasil", donde el 
- 2026-10-05 05:46 [Europa Press Internacional] Milei felicita a su "querido amigo" Flávio Bolsonaro por su "histórica elección" frente a Lula en Brasil
  > El presidente de Argentina, Javier Milei, ha felicitado al candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil, Flávio Bolsonaro, por su victoria en la primera vuelta de las elecciones presidenciales celebradas este domingo, en las que se ha impuesto con el 47,03% de los vo
- 2026-10-05 06:44 [ANSA Mondo] Brasile, l'ex giudice che condannò Lula eletto governatore
  > Sergio Moro guiderà l'esecutivo del suo stato natale, il Paranà
- 2026-10-05 07:14 [BBC Mundo] Elecciones en Brasil: Flávio Bolsonaro y Lula da Silva van a una segunda vuelta en la que el presidente enfrenta una difícil remontada
  > La mayor democracia de América Latina irá a balotaje el 25 de octubre. Lula lleva la desventaja frente a Bolsonaro, ya que históricamente nunca hubo una remontada en una segunda vuelta electoral en Brasil.
- 2026-10-05 07:46 [ANSA Mondo] In Brasile un 30enne di destra è il deputato più votato della storia
  > Nikolas Ferreira ha raccolto oltre 3,1 milioni di preferenze per la Camera
- 2026-10-05 10:46 [ANSA Mondo] Astensione record in Brasile, il 21,08% non ha votato al primo turno
  > Si tratta del livello più alto registrato dalle elezioni del 1998 (21,5%)
- 2026-10-05 11:42 [France 24 Español] Brasil irá a segunda vuelta: Flávio Bolsonaro lidera la primera ronda
  > Brasil se encamina a una segunda vuelta presidencial tras una elección marcada por la polarización. El senador Flávio Bolsonaro obtuvo el primer lugar en la primera vuelta, pero sin alcanzar la mayoría necesaria para evitar el balotaje. El próximo 25 de octubre se enfrentará al actual presidente, Lu
- 2026-10-05 12:20 [Rai News Esteri] Il primo turno delle presidenziali in Brasile, avanti Bolsonaro: ribaltati i pronostici pro-Lula
  > La sfida per il secondo turno del 25 ottobre è ancora aperta ma il presidente uscente non minimizza il peso di una pesante bocciatura delle sue politiche
- 2026-10-05 12:21 [Rai News Esteri] Presidenziali in Brasile, Flavio Bolsonaro a sorpresa supera Lula di 2 punti. Si va al ballottaggio
  > Il candidato di destra al 47%: "Il Brasile vuole cambiare". Il presidente uscente al 45%: "Sono bravo ai supplementari". Scelta rinviata al secondo turno del 25 ottobre
- 2026-10-05 12:29 [Clarín Mundo] Elecciones en Brasil 2026, EN VIVO: reacciones tras la victoria de Flávio Bolsonaro sobre Lula y últimas noticias del balotaje
  > Bolsonaro se impuso en la primera vuelta al superar por casi dos puntos al actual presidente Lula da Silva. El balotaje entre ambos se hará el 25 de octubre. Todas las repercusiones, minuto a minuto.
- 2026-10-05 12:31 [Clarín Mundo] Quién es Flávio Bolsonaro, el hijo de Jair que sorprendió a Lula y va por la presidencia de Brasil
  > Nacido en el estado de Río de Janeiro, Flávio es el mayor de los cinco hijos del expresidente y el que más se le parece físicamente.Este senador, de 45 años, enfrentará a Lula en el balotaje el próximo 25 de octubre.
- 2026-10-05 13:05 [France 24 Español] Informe desde Río de Janeiro: el Partido Liberal de Bolsonaro se fortalece en el Senado
  > Las elecciones legislativas en Brasil dejaron un resultado clave para el futuro político del país: el Partido Liberal (PL), formación vinculada al expresidente Jair Bolsonaro y que postuló a Flávio Bolsonaro para la Presidencia, amplió significativamente su presencia en el Senado. La bancada pasará 
- 2026-10-05 13:16 [Clarín Mundo] Elecciones en Brasil: los mercados celebran la ventaja de Flávio Bolsonaro sobre Lula y el principal índice de la Bolsa marca un nuevo récord
  > Los activos brasileños se dispararon este lunes y el real se apreció en la primera sesión de los mercados tras los comicios del domingo. El índice Ibovespa superó la marca de los 209.000 puntos por primera vez.
- 2026-10-05 13:57 [BBC Mundo] Quiénes son Lucas Pavanato y Nikolas Ferreira, los jóvenes influencers de derecha que lograron las mayores votaciones en la historia de la Cámara de Diputados de Brasil
  > Los flamantes legisladores comparten una agenda conservadora que incluye el rechazo a las políticas de género, el endurecimiento de las sanciones penales y la legalización del porte de armas como herramienta para combatir la delincuencia.
- 2026-10-05 14:50 [Clarín Mundo] Elecciones en Brasil: los resultados del domingo cambian por completo el diseño del país y ya asoma una amnistía para Jair Bolsonaro
  > La victoria del candidato conservador Flávio Bolsonaro sobre el presidente Lula da Silva en primera vuelta excede lo que pueda ocurrir en el balotaje.La ola de derecha se consolida con victorias en las gobernaciones y especialmente en el Parlamento.Aun si el líder petista lograra imponerse el 25 de 
- 2026-10-05 15:47 [Clarín Mundo] La reacción de los medios en Brasil tras la victoria de Bolsonaro: desde "el ciclo de Lula está terminado" hasta "el tsunami de lo peor de la derecha"
  > Los títulos, opiniones y análisis de la prensa en Brasil tras la primera vuelta de las presidenciales de este domingo.
- 2026-10-05 15:59 [France 24 Español] Flávio Bolsonaro y Lula da Silva se preparan para el balotaje en Brasil
  > 🇧🇷🗳️ Luiz Inácio Lula da Silva y Flávio Bolsonaro ofrecieron declaraciones después de que los resultados de los comicios presidenciales de Brasil confirmaran que deberán disputar el balotaje del 25 de octubre.
- 2026-10-05 16:02 [El País Internacional] El lulismo cruje ante la ofensiva ultra
  > Carteles del presidente Trump y del candidato Flavio Bolsonaro, en São Paulo, Brasil, este Lunes.
- 2026-10-05 16:10 [France 24 Español] "Solo faltan días para el rescate Brasil": Bolsonaro celebra la victoria sobre Lula
  > El senador del Partido Liberal (PL) y candidato presidencial, Flávio Bolsonaro, agradeció este lunes "a Dios" y al pueblo brasileño por su victoria en las elecciones del domingo ante el presidente Luiz Inácio Lula da Silva, en contra de los pronósticos. Además, celebró que el PL resultara el partido
- 2026-10-05 16:23 [Clarín Mundo] Elecciones en Brasil: a contrarreloj, Lula y el PT analizan cambios totales en la estrategia de campaña
  > Lo anticipan fuentes partidarias, pero no es claro en qué consistirán. Trascendió que ha habido tensiones internas sobre el manejo de la campaña.Y que debido a eso se perdieron oportunidades importantes para reducir el impulso del candidato opositor, Flávio Bolsonaro.
- 2026-10-05 16:36 [France 24 Español] Paraguay, refugio fiscal y político para la extrema derecha brasileña
  > En los últimos cinco años, las solicitudes de permisos de residencia de brasileños en Paraguay se han más que duplicado. Muchos de los recién llegados son simpatizantes de Jair Bolsonaro que temen una reelección del actual presidente, Luiz Inácio Lula da Silva, a quien responsabilizan de un deterior
- 2026-10-05 17:02 [ANSA Mondo] Brasile, Erika Hilton è la donna più votata della storia alla Camera
  > La politica brasiliana Erika

Hilton ha stabilito un nuovo record nella storia della Camera

dei deputati brasiliana, diventando la donna più votata di

sempre. La deputata trans del Partito socialismo e libertà

(Psol) di San Paolo è stata rieletta con 1.596.472 voti, pari al

5,9% dei voti espress
- 2026-10-05 17:30 [Clarín Mundo] El fantasma de Bolsonaro reaparece en Europa: los temores de Bruselas ante un eventual cambio de gobierno en Brasil
  > • Un cambio de gobierno en Brasil aportaría argumentos a los eurodiputados que buscan frenar la ratificación del entendimiento comercial.
• Si entre 50 y 80 legisladores modifican su postura en la votación prevista para los próximos meses, la aplicación provisional del pacto quedará suspendida.
- 2026-10-05 18:04 [France 24 Español] El mercado de valores de Brasil aplaude la ventaja de Bolsonaro en primera vuelta presidencial
  > El índice bursátil iBovespa, el más importante de la bolsa de São Paulo inició la jornada con un alza estrepitosa de casi el 9% y alcanzó máximo histórico, mientras el real brasileño gana 4,5% frente al dólar a media jornada, hasta situarse ligeramente por encima de los 5 reales por dólar. El buen r
- 2026-10-05 18:10 [France 24 Español] La dinastía Bolsonaro se fortalece: prensa brasileña sobre la primera vuelta electoral
  > La familia Bolsonaro no solo ganó la primera vuelta en Brasil, fortaleció su presencia en ambas cámaras del Congreso y conserva los respaldos de más de 10 gobernadores. 'O Globo' habla del bloque familiar que se ha hecho con varios cargos. Hermanos, hijos, esposa y exesposa tienen un puesto de elecc
- 2026-10-05 19:41 [El País Internacional] La ola conservadora de América Latina llega a Brasil
  > Flávio Bolsonaro (i) junto al presidente de EE.UU., Donald Trump, en el despacho oval de la Casa Blanca en Washington, el 26 de mayo de 2026.
- 2026-10-05 19:42 [El País Internacional] La victoria en primera vuelta de Bolsonaro impulsa a la ola ultra de América Latina
  > Transeúntes pasan ante pósteres dañados que muestran a Bolsonaro hijo con el presidente Trump, este lunes en São Paulo.
- 2026-10-05 19:47 [Clarín Mundo] Elecciones en Brasil: las urnas de la sorpresa
  > Tras el imprevisto triunfo de Flávio Bolsonaro sobre Lula en la primera vuelta, Brasil se encamina hacia un balotaje decisivo el próximo 25 de octubre. La contienda electoral ratifica la profunda polarización política del país y la consolidación del bolsonarismo como una fuerza de derecha permanente
- 2026-10-05 20:21 [ANSA Mondo] Trump, il risultato di Bolsonaro in Brasile una 'grande vittoria'
  > Il risultato di Flavio Bolsonaro

alle elezioni in Brasile è stata una "grande vittoria". Lo ha

detto Donald Trump.Quella di Bolsonaro "è una grande vittoria: combattuta, ma una

vittoria davvero enorme. Incredibile", ha detto Trump. Bolsonaro

si avvia al ballottaggio del 25 ottobre come favorito.
- 2026-10-05 22:09 [ANSA Mondo] Brasile, l'ex presidente Temer sostiene Bolsonaro al ballottaggio
  > L'ex presidente brasiliano

Michel Temer (2016-2018) ha dichiarato il suo sostegno a Flávio

Bolsonaro in vista del ballottaggio del 25 ottobre contro Luiz

Inácio Lula da Silva. In un video diffuso sui social, Temer ha

affermato che il risultato del primo turno mostra la volontà

degli elettori di
**B** (3 item(s))
- 2026-10-04 22:00 [European Commission Press] Commission unlocks €157 million to Moldova for reform progress under the Growth Plan
  > European Commission Press release Brussels, 05 Oct 2026 Today, at the 10th EU-Moldova Association Council, the European Commission disbursed an additional €157 million to Moldova, reaffirming the EU's support for the country's reform path.
- 2026-10-05 11:22 [Kyiv Independent] Moldova aims to complete EU technical talks by 2028, join bloc by 2030
  > Moldova has "taken major strides towards membership," the EU's top diplomat Kaja Kallas said at the end of the 10th EU-Moldova Association Council meeting in Brussels.
- 2026-10-05 14:50 [Council of the EU Press] The European Union and Moldova reiterate their strong partnership and announce the disbursement of €157 million under Growth Plan funding at the 10th EU-Moldova Association Council
  > On 5 October 2026, the European Union and the Republic of Moldova held their 10th Association Council Meeting where EU and Moldova reiterated their strong partnership and announce the disbursement of €157 million under Growth Plan funding.

## U061
**A** (7 item(s))
- 2026-10-03 23:35 [Rai News Esteri] Marea sociale contro il caro-affitti in Spagna: le piazze spingono Sánchez verso le urne
  > Ondata di proteste da Madrid a tutte le principali città per il diritto alla casa dopo lo sfratto dell'ottantasettenne Mari Carmen; il rifiuto dei decreti da parte delle destre e dei catalani di Junts apre lo scenario di elezioni anticipate
- 2026-10-04 17:28 [Rai News Esteri] Casa e scuola: il filo rosso che lega le proteste in Europa
  > In Spagna per il diritto alla casa, in Francia l'erosione allo studio accende lo scontento dei più giovani
- 2026-10-04 23:15 [Rai News Esteri] La Spagna in piazza per il diritto alla casa. E Sanchez pensa al voto anticipato
  > Centinaia di migliaia di persone al fianco delle proteste di Madrid per la casa, il governo bocciato in Parlamento valuta elezioni a fine novembre
- 2026-10-05 06:21 [Il Sole 24 Ore Mondo] Caro casa, prezzi e affitti salgono nell’Ue. Il Governo studia le misure per giovani e locazioni
  > «Serve una formazione di qualità, un lavoro sicuro e stabile, una retribuzione adeguata, una casa a un prezzo equo», ha detto di recente la premier Giorgia Meloni
- 2026-10-05 10:27 [Rai News Esteri] La Spagna al voto: i sondaggi premiano le destre, l'area progressista frammentata
  > Il partito popolare e Vox arriverebbero al 52%, secondo un sondaggio per El Pais. Ma le rilevazioni sono state realizzate prima della crisi di governo e della bocciatura dei decreti presentati da Sanchez
- 2026-10-05 19:05 [Il Sole 24 Ore Mondo] Sanchez sfida le destre: Spagna al voto anticipato
  > Dopo la bocciatura sul piano casa, il premier socialista convoca le elezioni cavalcando le proteste di piazza: «Serve una maggioranza progressista per nuovi progressi sociali»
- 2026-10-05 21:04 [Rai News Esteri] Migliaia di persone a Barcellona in piazza per il diritto alla casa
  > Dopo Madrid e Valencia anche Barcellona stasera è scesa in piazza all'annuncio di elezioni anticipate, in migliai hanno sfilato per difendere il diritto alla casa
**B** (14 item(s))
- 2026-10-04 11:15 [Al Jazeera] Brazil votes in deeply polarised election pitting Lula against Bolsonaro
  > Close race expected as left-wing leader Lula seeks fourth nonconsecutive term against right-wing Flavio Bolsonaro.
- 2026-10-04 17:48 [South China Morning Post] Brazilians head to polls in high-stakes, polarised election
  > Brazilians queued to vote on Sunday in the first round of a tight election, following a campaign dominated by corruption scandals, economic anxiety and accusations of US meddling.
The field of 13 candidates has been led by two clear front runners – leftist President Luiz Inacio Lula da Silva, 80, wh
- 2026-10-04 21:11 [BBC World] Polls close in Brazil as Lula and Flávio Bolsonaro remain neck and neck
  > If no candidate gets more than 50% of the vote, the election will go to a run-off on 25 October.
- 2026-10-05 00:27 [DW World] Brazil election: Bolsonaro and Lula head to runoff
  > Populist Flavio Bolsonaro has secured a thin lead over incumbent Luiz Inacio Lula da Silva, but the next president of Brazil will be decided in the runoff round, according to the country’s electoral court.
- 2026-10-05 03:16 [BBC World] Right-wing Flávio Bolsonaro wins first round of Brazil election
  > With neither candidate getting more than 50% of the vote, the election will go to a run-off on 25 October.
- 2026-10-05 04:51 [BBC World] Watch: How Brazil's dramatic election unfolded
  > Millions of Brazilians took to the polls on Sunday for the first round of the country's presidential elections.
- 2026-10-05 05:08 [Al Jazeera] Bolsonaro beats expectations in Brazil vote, faces Lula in runoff
  > Brazil’s presidential election is heading to a run-off after Bolsonaro and Lula both fell short of the 50% needed to win
- 2026-10-05 09:38 [France 24] Brazil heads to run-off as Bolsonaro pulls off shock first place finish in first round
  > Flavio Bolsonaro, a right-wing senator and son of former president Jair Bolsonaro, pulled off a surprise first-place finish ahead of President Luiz Inacio Lula da Silva in Brazil’s election Sunday. However, with neither candidate securing a majority the vote now heads to a run-off in three weeks.
- 2026-10-05 09:46 [South China Morning Post] Brazil-China ties in focus as Bolsonaro gets election edge over Lula
  > Brazil is set for a presidential run-off after right-wing challenger Flavio Bolsonaro won a surprise first-round victory, threatening Luiz Inacio Lula da Silva’s grip on power in South America’s largest economy.
Bolsonaro, son of imprisoned former president Jair Bolsonaro, took 47 per cent of the ba
- 2026-10-05 12:34 [Al Jazeera] Bolsonaro favourite to win: What Brazil’s first round of elections tells us
  > Analysts say Flavio Bolsonaro is projected to win the run-off vote on October 25 and become Brazil&#039;s next president.
- 2026-10-05 12:52 [France 24] Brazil presidential election: 'Bolsonaro being ahead is a surprise,' researcher says
  > Far-right candidate Flavio Bolsonaro has pulled off a surprise win in the first round of Brazil’s presidential election. He defied most polls to win with 47 percent, compared to 45 percent for leftist incumbent Luiz Inacio Lula de Silva. We spoke to Thomas Zicman de Barros, a research fellow at CEVI
- 2026-10-05 12:54 [France 24] 'Very bad result for Lula: Bolsonaro is far more effective at speaking to that growing middle class'
  > Eve Irvine is pleased to welcome Felipe Krause, the head of Oxford University's Brazilian Studies Programme. Brazil's election reflects a political landscape that has become increasingly polarized, explains Krause. And he describes the current mood as one of “tired polarization: People are just exha
- 2026-10-05 20:37 [France 24] Concerns of US interference weigh on Brazil vote
  > Conservative Senator Flavio Bolsonaro pulled off a surprise on Sunday in the first round of Brazil’s presidential election by finishing ahead of the incumbent left-wing President Lula, whom he will face in the runoff on October 25. Suspicions of U.S. interference have been hanging over the campaign,
- 2026-10-05 21:00 [Al Jazeera] Brazil’s presidential race head for a tough runoff
  > Brazil is heading into a fiercely contested presidential runoff after the first round revealed major gains for Bolsonaro

## U062
**A** (3 item(s))
- 2026-10-08 01:23 [France 24 Español] Directo a... Washington y las dudas generadas por fallida ejecución de Christa Pike
  > Christa Pike, condenada a muerte por el asesinato de una compañera de estudios en 1995, es la única persona que ha sobrevivido tras recibir fármacos de inyección letal, según el Centro de Información sobre la Pena de Muerte. Una semana después de su fallida ejecución, la mujer se encuentra despierta
- 2026-10-08 02:09 [ANSA Mondo] Giustiziato in Texas con iniezione letale, prima esecuzione dopo il caso Pike
  > Jamaal Howard, un americano di

46 anni, è stato giustiziato in Texas tramite una iniezione

letale, in quella che è la prima esecuzione dopo il tentativo

più volte fallito contro Christa Pike in Tennessee, appena una

settimana prima.Quella di Howard, condannato a morte per aver ucciso un

addetto
- 2026-10-08 02:52 [Rai News Esteri] Giustiziato Jamaal Howard: per gli Usa è la trentesima esecuzione dell'anno
  > L'uomo era condannato per l'omicidio di un commesso nel 2000. Primo caso dopo la vicenda di Christa Pike
**B** (2 item(s))
- 2026-10-08 12:14 [State Department] United States and Zambia Sign Five-Year Global Health Partnership under the Trump Administration’s America First Global Health Strategy
  > Thomas &quot;Tommy&quot; Pigott, SpokesmanOffice of the Spokesman



	

		
		

			

		

		

			

				
				

					
						United States and Zambia Sign Five-Year Global Health Partnership under the Trump Administration’s America First Global Health Strategy 
					
				

				

					

					
					
						
- 2026-10-08 16:24 [BBC World] Zambia signs US health deal after disputes over data-sharing
  > The US will provide $1.5bn (£1.1bn) under the deal that was negotiated after Trump cut USAID funding.

## U063
**A** (5 item(s))
- 2026-09-29 12:00 [South China Morning Post] US and China need shared risk vocabulary to manage AI threats: Beijing-linked think tank
  > Beijing and Washington should first develop a common language around AI risks rather than seek to resolve their broader technology rivalry, a leading Chinese think tank has advised.
The call from the China Institutes of Contemporary International Relations (CICIR), affiliated with the Ministry of St
- 2026-09-29 16:09 [BBC World] Trump rules out joint US-China venture to develop AI
  > The US president continues to push back on calls to establish guardrails around artificial intelligence, arguing it will stifle growth.
- 2026-09-29 19:32 [South China Morning Post] Trump rejects calls to work with China on AI safety despite Xi summit progress
  > US President Donald Trump said on Tuesday he does not want to work with China on addressing artificial intelligence (AI) risks, arguing that cooperation could undermine America’s lead in the fast-moving technology.
“Whoever wins superintelligence wins. You’re gonna have a winner and a loser, and you
- 2026-09-29 23:43 [Al Jazeera] Trump, tech bosses sign voluntary pact pledging ‘robust’ AI safeguards
  > US President Trump touts self-regulation amid the international community&#039;s and industry&#039;s calls for formal rules.
- 2026-09-30 05:00 [South China Morning Post] Chinese firms trail global peers on profits, but AI power boom offers bright spot: Natixis
  > China’s corporate sector remains considerably weaker than it was before the Covid-19 pandemic, but the country is emerging as a key beneficiary of the global artificial intelligence boom thanks to its ample power capacity, according to a Natixis survey of thousands of firms and a separate research r
**B** (8 item(s))
- 2026-09-29 14:40 [Defense News] US forces exiting Iraq after 2 decades, leaving opening for Iran
  > U.S. forces are set to depart from their last bases in Iraq by Wednesday, a move celebrated as a victory by Iran and its allies, who now have deep influence in the country where 4,500 Americans died during more than two decades of war.Iraqi security experts say the withdrawal — agreed to in 2024 und
- 2026-09-29 20:00 [Al Jazeera] US troops fully withdraw from Baghdad base after two decades
  > US Army soldiers have fully withdrawn from the US base in Baghdad.
- 2026-09-30 09:46 [South China Morning Post] US ends troop mission in Iraq, Baghdad to celebrate Sovereignty Day on October 1
  > A US-led coalition deployed in Iraq more than a decade ago to fight jihadists concluded its mission on Wednesday, a move celebrated by the country’s leaders, but which some fear will embolden pro-Iran armed factions.
Coalition troops deployed to Iraq and Syria in 2014 to fight Islamic State, which h
- 2026-09-30 11:36 [BBC World] Last UK and US troops leave Iraq as anti-Islamic State mission ends
  > The withdrawal of coalition forces, under a deal agreed two years ago, was a key demand of the Iraqi government.
- 2026-09-30 12:17 [Al Jazeera] Iraq celebrates National Sovereignty Day as US troops withdraw
  > Iraq’s security forces held parades in Baghdad and Najaf to celebrate ‘Sovereignty Day’ as US troops withdraw.
- 2026-09-30 14:04 [Breaking Defense] US withdraws last remaining troops out of Iraq
  > “As we step back and hand full primary responsibility for Iraq’s security to the Government of Iraq and the brave people of Iraq, US and Coalition forces stationed across the region will remain ready to respond to any ISIS threats that arise,” CENTCOM Commander Adm. Brad Cooper said.
- 2026-09-30 16:33 [Al Jazeera] Pentagon says US troop withdrawal from Iraq is complete
  > The withdrawal ends two decades of foreign intervention in Iraq as part of &#039;global war on terror&#039; and anti-ISIL fight.
- 2026-10-01 01:11 [Al Jazeera] Iraq celebrates Sovereignty Day as US troops complete withdrawal
  > Night time celebrations filled the air as Iraqis observed the start of a four-day holiday.

## U064
**A** (2 item(s))
- 2026-09-29 20:25 [BBC World] Former American Idol contestant and pastor found guilty of murdering wife
  > Caleb Flynn shot his wife, Ashley, dead in their Ohio home in February before saying in a 9/11 call she was killed by burglars.
- 2026-09-30 10:35 [Al Jazeera] Former American Idol contestant found guilty of murdering wife
  > Former American Idol contestant found guilty of murdering wife
**B** (2 item(s))
- 2026-10-01 14:00 [South China Morning Post] China backs Cuba, Beijing’s Panama threat, new UN chief: 7 Latin America relations reads
  > We have selected seven of the most interesting and important news stories covering Latin American relations from the past few weeks. If you would like to see more of our reporting, please consider subscribing.
1. China pledges to ‘firmly support’ Cuba as US escalates pressure on Havana

China will s
- 2026-10-02 20:52 [Al Jazeera] Latin America sees China as more positive global influence than US: Poll
  > Annual Latinobarometro survey finds views of China’s influence improving as perceptions of US influence worsen.

## U065
**A** (5 item(s))
- 2026-10-08 05:06 [Al Jazeera] Signage at UK consulate in East Jerusalem removed as Israel’s deadline over
  > Thursday marks 30 days since Israel&#039;s foreign minister ordered the closure of the UK consulate in occupied East Jerusalem.
- 2026-10-08 07:06 [BBC World] Most UK diplomats to leave East Jerusalem consulate, Israel says, as Miliband says 'vital services' to remain
  > Israel said in September it would act in response to UK sanctions on illegal Israeli settlements in the West Bank.
- 2026-10-08 07:27 [South China Morning Post] Britain downscales and renames Jerusalem consulate after Israel orders closure
  > Britain said on Thursday its ⁠nearly 200-year-old consulate in Jerusalem ⁠would remain operating at a smaller scale, renamed ⁠as the “UK Mission” in the city, after Israel ordered it shut in a dispute over sanctions on settlements.
Israel last month issued a 30-day deadline for Britain to close the 
- 2026-10-08 08:25 [Al Jazeera] Video: Signs removed from British consulate in occupied East Jerusalem
  > Signs from the British consulate in occupied East Jerusalem were removed overnight as a deadline for its closure loomed.
- 2026-10-08 14:01 [Al Jazeera] King David Hotel bombing to consulate row: A timeline of UK-Israel tension
  > Israel&#039;s order to shut UK&#039;s Jerusalem consulate is the latest downturn in a relationship strained since before 1948.
**B** (2 item(s))
- 2026-10-08 18:11 [Al Jazeera] Israel opens first-ever pavilion at Morocco defence show
  > Israel opened its first national pavilion at Morocco&#039;s Marrakech Air Show, joined by Israel&#039;s top military contractors.
- 2026-10-08 20:23 [Breaking Defense] In first, Israeli firms, delegation display at Morocco’s Marrakech Airshow
  > “This marks Israel&#8217;s first official participation in the defense exhibition held in Morocco since the signing of the Abraham Accords,” Israel’s Ministry of Defense said.

## U066
**A** (2 item(s))
- 2026-10-03 12:22 [BBC Mundo] Lo que la fallida ejecución de Christa Pike revela sobre la pena de muerte en EE.UU.
  > Christa Pike, una mujer condenada a muerte en Tennessee, sobrevivió a la aplicación de dos inyecciones letales. Su caso ha vuelto a centrar la atención en la pena de muerte y en cómo se aplica en Estados Unidos.
- 2026-10-03 19:14 [Il Sole 24 Ore Mondo] Trump vuole estendere la pena di morte ai narcotrafficanti: il caso Pike riapre lo scontro
  > Il presidente promette di ampliare i reati punibili con la pena capitale. Il Tennessee sospende le esecuzioni dopo il caso Pike, mentre una sentenza della Corte Suprema del 2008 lascia aperto il nodo dei grandi narcotrafficanti
**B** (3 item(s))
- 2026-10-05 03:37 [BBC World] Trump unveils 'Super Intelligence Force' to oversee AI policy
  > The president named his national intelligence chief as the taskforce's head as worries over AI grow.
- 2026-10-05 10:03 [BBC World] Trump chooses top spy boss to run new AI taskforce
  > The US president said his national intelligence chief will lead the group as worries over AI grow.
- 2026-10-05 10:09 [France 24] Trump names Jay Clayton as AI czar to lead 'Super Intelligence Force'
  > US President Donald Trump has named his National Intelligence Director Jay Clayton as America's "Super Intelligence" czar, as fears over AI grow. Also, oil markets react to Houthi attacks as well as export data, and France's fiscal woes drive the euro to a 17-month low.

## U067
**A** (3 item(s))
- 2026-10-07 23:23 [Clarín Mundo] “El sufrimiento no comenzó ni terminó ese día”: el polémico mensaje del alcalde de Nueva York, Zohran Mamdani, a tres años de la masacre del 7-O
  > El funcionario se solidarizó por los "horrendos crímenes de guerra del 7 de octubre" y acusó al gobierno israelí de perpetrar un "devastador genocidio" en Gaza.La semana pasada había anunciado un plan para combatir el antisemitismo en la ciudad.
- 2026-10-08 01:32 [France 24 Español] Gaza: el panorama en el enclave tres años después de los ataques de Hamas del 7-O
  > Tres años después del ataque de Hamás contra Israel y la posterior respuesta israelí contra la Franja de Gaza, el enclave palestino está prácticamente irreconocible. El 80% de la infraestructura fue destruida o afectada por los ataques, el acceso al  agua potable es muy limitado y la mayoría de civi
- 2026-10-08 10:27 [El País Internacional] Mamdani es abucheado por manifestantes propalestinos por acudir a un acto de recuerdo de las víctimas del 7 de octubre
  > El alcalde de Nueva York, Zohran Mamdani, acude a la vigilia por el tercer aniversario de los ataques de Hamás en Israel, en Nueva York, el 7 de octubre de 2026.
**B** (5 item(s))
- 2026-10-08 05:06 [Al Jazeera] Signage at UK consulate in East Jerusalem removed as Israel’s deadline over
  > Thursday marks 30 days since Israel&#039;s foreign minister ordered the closure of the UK consulate in occupied East Jerusalem.
- 2026-10-08 07:06 [BBC World] Most UK diplomats to leave East Jerusalem consulate, Israel says, as Miliband says 'vital services' to remain
  > Israel said in September it would act in response to UK sanctions on illegal Israeli settlements in the West Bank.
- 2026-10-08 07:27 [South China Morning Post] Britain downscales and renames Jerusalem consulate after Israel orders closure
  > Britain said on Thursday its ⁠nearly 200-year-old consulate in Jerusalem ⁠would remain operating at a smaller scale, renamed ⁠as the “UK Mission” in the city, after Israel ordered it shut in a dispute over sanctions on settlements.
Israel last month issued a 30-day deadline for Britain to close the 
- 2026-10-08 08:25 [Al Jazeera] Video: Signs removed from British consulate in occupied East Jerusalem
  > Signs from the British consulate in occupied East Jerusalem were removed overnight as a deadline for its closure loomed.
- 2026-10-08 14:01 [Al Jazeera] King David Hotel bombing to consulate row: A timeline of UK-Israel tension
  > Israel&#039;s order to shut UK&#039;s Jerusalem consulate is the latest downturn in a relationship strained since before 1948.

## U068
**A** (8 item(s))
- 2026-09-29 14:40 [Defense News] US forces exiting Iraq after 2 decades, leaving opening for Iran
  > U.S. forces are set to depart from their last bases in Iraq by Wednesday, a move celebrated as a victory by Iran and its allies, who now have deep influence in the country where 4,500 Americans died during more than two decades of war.Iraqi security experts say the withdrawal — agreed to in 2024 und
- 2026-09-29 20:00 [Al Jazeera] US troops fully withdraw from Baghdad base after two decades
  > US Army soldiers have fully withdrawn from the US base in Baghdad.
- 2026-09-30 09:46 [South China Morning Post] US ends troop mission in Iraq, Baghdad to celebrate Sovereignty Day on October 1
  > A US-led coalition deployed in Iraq more than a decade ago to fight jihadists concluded its mission on Wednesday, a move celebrated by the country’s leaders, but which some fear will embolden pro-Iran armed factions.
Coalition troops deployed to Iraq and Syria in 2014 to fight Islamic State, which h
- 2026-09-30 11:36 [BBC World] Last UK and US troops leave Iraq as anti-Islamic State mission ends
  > The withdrawal of coalition forces, under a deal agreed two years ago, was a key demand of the Iraqi government.
- 2026-09-30 12:17 [Al Jazeera] Iraq celebrates National Sovereignty Day as US troops withdraw
  > Iraq’s security forces held parades in Baghdad and Najaf to celebrate ‘Sovereignty Day’ as US troops withdraw.
- 2026-09-30 14:04 [Breaking Defense] US withdraws last remaining troops out of Iraq
  > “As we step back and hand full primary responsibility for Iraq’s security to the Government of Iraq and the brave people of Iraq, US and Coalition forces stationed across the region will remain ready to respond to any ISIS threats that arise,” CENTCOM Commander Adm. Brad Cooper said.
- 2026-09-30 16:33 [Al Jazeera] Pentagon says US troop withdrawal from Iraq is complete
  > The withdrawal ends two decades of foreign intervention in Iraq as part of &#039;global war on terror&#039; and anti-ISIL fight.
- 2026-10-01 01:11 [Al Jazeera] Iraq celebrates Sovereignty Day as US troops complete withdrawal
  > Night time celebrations filled the air as Iraqis observed the start of a four-day holiday.
**B** (14 item(s))
- 2026-09-29 23:39 [BBC World] US Supreme Court denies Christa Pike's last-ditch bid to halt execution
  > The Tennessee inmate has been awaiting execution since she was sentenced to death in 1996 for the murder of a teenage classmate.
- 2026-09-30 13:14 [Al Jazeera] Christa Pike seeks firing squad, not lethal injection: Inside US executions
  > Women make up about 1 percent of US executions. How do states put people to death, and why is it contested?
- 2026-09-30 15:29 [BBC World] Execution of US murderer Christa Pike halted shortly before it was due to happen
  > Pike was convicted and sentenced to death in 1996 for the murder of Colleen Slemmer.
- 2026-09-30 16:00 [South China Morning Post] US Tennessee’s first execution of a woman in 200 years halted
  > A US appeal court on Wednesday halted the ⁠execution of death row inmate Christa Pike in Tennessee, less than two hours before she was scheduled to become the first woman that state has put to death in more than 200 years.
The 6th US Circuit Court of Appeals ordered a “short stay of execution” to gi
- 2026-09-30 16:44 [Al Jazeera] US appeals court halts Tennessee execution of Christa Pike
  > Christa Pike was set to become the first woman executed by Tennessee in more than 200 years.
- 2026-09-30 23:42 [BBC World] US Supreme Court allows execution of Christa Pike to go ahead
  > The death by lethal injection was scheduled to happen earlier on Wednesday before judges from a lower court paused the execution.
- 2026-10-01 02:35 [Al Jazeera] Christa Pike’s execution by lethal injection fails in Tennessee
  > Witnesses say Tennessee officials were unable to execute Christa Pike after a lethal injection attempt.
- 2026-10-01 04:14 [South China Morning Post] Tennessee halts executions after Christa Pike survives 2 doses of lethal drug
  > Tennessee officials were unable to put Christa Pike to death on Wednesday for a 1995 murder after administering two doses of a lethal drug. A death penalty expert said it was an unprecedented failure, and Tennessee’s governor halted the remaining execution for the rest of the year.
Pike, 50, was ali
- 2026-10-01 04:55 [Al Jazeera] Execution of US woman Christa Pike fails after botched lethal injection
  > The high-profile execution of murderer Christa Pike is in disarray after two lethal injections failed to kill her.
- 2026-10-01 16:45 [BBC World] Tennessee halts executions after Christa Pike survives two lethal injection attempts
  > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
- 2026-10-02 03:02 [South China Morning Post] Christa Pike in ‘life-saving care’ after botched Tennessee execution
  > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from a prison execution c
- 2026-10-02 07:58 [Al Jazeera] Lawyers for US inmate who survived lethal injections demand release
  > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
- 2026-10-02 20:32 [BBC World] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say
  > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.
- 2026-10-02 20:57 [Al Jazeera] Christa Pike unconscious, on ventilator after botched execution: Lawyers
  > The Tennessee woman&#039;s legal team says doctors are working to clear doses of the drug pentobarbital from her system.

## U069
**A** (3 item(s))
- 2026-10-07 23:08 [BBC Mundo] Por qué la mayor colonia de pingüinos del mundo ha perdido dos tercios de su población
  > Se atribuye al cambio climático el drástico declive de los pingüinos barbijo que habitan en una remota isla volcánica.
- 2026-10-08 02:44 [France 24 Español] Ecuador: jueza declara inocentes a 32 pescadores de lanchas atacadas por EE. UU. en el Pacífico
  > Una jueza declaró inocentes a 32 pescadores tripulantes de dos de las lanchas atacadas por Estados Unidos en el océano Pacífico, que habían sido procesados previamente por la Fiscalía por presunta asociación ilícita con grupos delincuenciales. Nuestra corresponsal Carolina Mella nos amplió la inform
- 2026-10-08 19:31 [Clarín Mundo] "El estrecho de Magallanes fue, es y será siempre chileno": la dura respuesta del canciller tras los dichos del embajador de Estados Unidos
  > Francisco Pérez Mackenna rechazó los dichos de Brandon Judd y remarcó que Chile cuenta con capacidad propia para resguardar el Estrecho de Magallanes. La controversia diplomática por la vía marítima se suma a la nota de protesta presentada semanas atrás contra la Argentina por una afirmación similar
**B** (2 item(s))
- 2026-10-08 14:26 [Rai News Esteri] Donald Trump: "Merito ancora il Nobel per la pace, ho evitato la distruzione del mondo"
  > Un anno fa il riconoscimento all'oppositrice venezuelana Maria Corina Machado che il presidente degli Stati Uniti non ha mai digerito
- 2026-10-08 16:44 [Clarín Mundo] Donald Trump mete presión para que le den el Premio Nobel de la Paz 2026: "He evitado la destrucción total del mundo"
  > El presidente de los Estados Unidos volvió a reclamar el premio, luego de que el año pasado se lo entregaran a la opositora venezolana María Corina Machado.También cuestionó que se lo hayan otorgado a Obama en 2009. “Yo he hecho mucho más y no me lo dan”, afirmó.

## U070
**A** (2 item(s))
- 2026-09-30 05:01 [BBC World] 'Backpack' declared Alaska's Fat Bear Week winner
  > "Backpack" defeated a bear known only as "910" in the final round of the annual competition.
- 2026-09-30 06:57 [Al Jazeera] Gentle giant Backpack wins Alaska’s Fat Bear Week
  > The contest celebrates the resilience of the 2,200 brown bears that live in the preserve on the Alaska Peninsula.
**B** (3 item(s))
- 2026-09-30 18:01 [Al Jazeera] Trump set to announce $200bn in energy investments from South Korea
  > The investments come as Trump seeks to tout the Republican Party&#039;s economic record ahead of the US midterm races.
- 2026-10-01 01:44 [South China Morning Post] Trump touts US$200 billion South Korean energy deal ahead of US midterms
  > US President Donald Trump has announced US$200 billion in energy investments from South Korea, including US$54 billion towards a long-discussed liquefied natural gas project in Alaska and more than US$100 billion in planned longer-term nuclear power investments.
Besides the Alaska LNG project and pi
- 2026-10-01 10:36 [South China Morning Post] South Korea hits back at Trump’s investment claims in ‘tit-for-tat move’
  > US President Donald Trump’s unilateral announcement of a “colossal” South Korean investment package has prompted Seoul to clarify that the deal is far from finalised, laying bare stark differences between the allies over the terms of their trade agreement, observers have said.
On Wednesday, Trump an

## U071
**A** (2 item(s))
- 2026-09-29 19:08 [South China Morning Post] China expands overseas military presence with new Laos air force centre
  > China has launched a rare air force support and training centre in Laos, the Ministry of Defence announced on Tuesday.
The China-Laos Joint Support and Training Centre and the China-Laos Friendship Aviation Academy are now in operation at the Ban Keun Airport, aiming to help the Laotian Air Force tr
- 2026-09-30 16:33 [Breaking Defense] China opens training center with Laos, marking third overseas military base
  > Satellite imagery shows the new facility is built in part on a purported old US airstrip used during the Vietnam War.
**B** (6 item(s))
- 2026-10-02 01:23 [Al Jazeera] Trump says US may ask Europe to release diesel reserves
  > Skyrocketing diesel prices have pushed Washington to weigh an export ban, raising alarm across European economies.
- 2026-10-02 05:26 [BBC World] US pressures Europe over diesel reserves as Trump threatens export ban
  > President Donald Trump has threatened to ban diesel exports in a bid to ease prices in the US ahead of the November elections.
- 2026-10-02 13:16 [Al Jazeera] Trump vs Europe as US presses for release of emergency diesel stocks
  > Europe&#039;s leaders are mulling proposals to respond to Trump&#039;s diesel demands.
- 2026-10-02 14:51 [South China Morning Post] G7 nations agree to release diesel and oil stocks after Trump pressure
  > Group ⁠of Seven countries agreed on Friday to release 100 million barrels of diesel and crude oil from emergency reserves and pledged to refrain from energy export restrictions after pressure from US President Donald Trump.
The US led a pressure campaign on the European Union to draw down emergency 
- 2026-10-02 19:01 [Al Jazeera] Trump says Europe agreed to release ‘massive amount’ of diesel reserves
  > US President Donald Trump says Europe agreed to release a ‘massive amount’ of diesel from emergency stockpiles.
- 2026-10-02 20:25 [BBC World] G7 to release 100 million barrels of oil and diesel after Trump export ban threat
  > The co-ordinated release is aimed at heading off further price spikes and avoiding a ban on US diesel exports.

## U072
**A** (9 item(s))
- 2026-10-07 09:30 [El País Internacional] Lourdes M. Rosado, presidenta de LatinoJustice: “Estas elecciones son la oportunidad para decirle a Trump que sus políticas no son aceptables”
  > Lourdes M. Rosado, abogada y presidenta de LatinoJustice.
- 2026-10-07 21:28 [France 24 Español] "Bolsonaro nunca más": miles marchan en Río contra Flávio Bolsonaro antes del balotaje
  > Miles de personas se manifestaron el miércoles en Río de Janeiro contra Flávio Bolsonaro y un posible regreso de la ultraderecha al poder en Brasil, al inicio de la campaña para la segunda vuelta del 25 de octubre. Bajo la consigna "Bolsonaro nunca más", los participantes expresaron su temor a los r
- 2026-10-08 01:31 [ANSA Mondo] Brasile, migliaia di studenti in piazza a Rio per Lula
  > Migliaia di studenti hanno

manifestato oggi nel centro di Rio de Janeiro a sostegno del

presidente Luiz Inácio Lula da Silva e contro Flávio Bolsonaro,

suo avversario al ballottaggio del prossimo25 ottobre. Lo

riferisce Efe. La mobilitazione, organizzata da associazioni

studentesche, è partita 
- 2026-10-08 01:42 [France 24 Español] "Dictadura nunca más": marcha masiva en Río contra Bolsonaro a días del balotaje con Lula
  > Miles de personas, en su mayoría estudiantes, marcharon este miércoles 7 de octubre en Río de Janeiro para rechazar el avance de la extrema derecha y del candidato Flávio Bolsonaro. Los manifestantes también mostraron su apoyo a la continuidad del Gobierno del izquierdista Luiz Inácio Lula da Silva 
- 2026-10-08 07:53 [ANSA Mondo] La moglie di Lula criticata per il flop della campagna elettorale
  > A pochi giorni dal ballottaggio

presidenziale in Brasile, si spacca il fronte di maggioranza che

appoggia la candidatura del presidente di sinistra uscente Luiz

Inacio Lula da Silva, uscito sconfitto dal primo turno contro il

senatore di destra Flavio Bolsonaro. Una riunione dei

coordinatori de
- 2026-10-08 09:22 [ANSA Mondo] Flavio Bolsonaro, 'ho ricevuto oltre duemila minacce di morte'
  > Il candidato alla

presidenza del Brasile, Flávio Bolsonaro, ha dichiarato di aver

ricevuto "oltre 2.000 minacce di morte" a causa della sua

posizione contro la criminalità organizzata.Il senatore di destra ha condiviso una conversazione

pubblicata sui social da un uomo che lui descrive come "uno
- 2026-10-08 13:11 [ANSA Mondo] Sondaggio, Bolsonaro ha il 53% dei voti validi per il ballottaggio
  > Il candidato di destra alla

presidenza del Brasile, Flavio Bolsonaro, raccoglie il 53% dei

voti validi in vista del ballottaggio del 25 ottobre contro il

presidente di sinistra uscente, Luiz Inácio Lula da Silva, che

ha invece il 47% delle preferenze: è quanto emerge dall'ultima

rilevazione del
- 2026-10-08 16:09 [Clarín Mundo] Balotaje en Brasil: con las encuestas a favor, Flávio Bolsonaro dice que quiere poner fin a la reelección y ampliar el mandato a 5 años
  > El candidato presidencial afirma que pretende utilizar el capital político desde el inicio de un posible mandato para aprobar una enmienda constitucional sobre el tema.Se enfrentará a Lula en segunda vuelta el 25 de octubre.
- 2026-10-08 20:04 [ANSA Mondo] Brasile, Moraes ordina il carcere per Eduardo Bolsonaro e cancella i suoi passaporti
  > L'ex deputato deve scontare 4 anni per aver cercato di influenzare il processo al padre
**B** (3 item(s))
- 2026-10-07 22:21 [Clarín Mundo] Peste neumónica en Rusia: en el pueblo de la muerte sospechosa, "nadie parece preocuparse"
  > La muerte de una técnica de un laboratorio especializado en enfermedades infecciosas inquieta a Estados Unidos y otros países.Moscú minimiza el riesgo y en la ciudad de Irkutsk, donde ocurrió el fallecimiento, los habitantes siguen su vida.
- 2026-10-08 09:33 [ANSA Mondo] Agenzia sanitaria russa, 'sono false le voci su secondo caso di presunta peste'
  > Sono "false" le voci su un presunto

secondo caso di peste nella regione siberiana russa di Irktusk.Lo afferma l'agenzia sanitaria russa Rospotrebnadzor, citata da

Ria Novosti."In merito alle false informazioni apparse sui social media

riguardo a un secondo caso della malattia in una persona che h
- 2026-10-08 14:18 [Il Sole 24 Ore Mondo] Peste in Siberia, la madre della ricercatrice: «Hanno lasciato morire mia figlia»
  > Sale la tensione fra Russia e Stati Uniti sul caso di peste in Siberia. Dopo giorni di inviti pubblici a fare chiarezza, Washington ha inviato a Mosca una nota ufficiale...

## U073
**A** (4 item(s))
- 2026-10-04 15:23 [South China Morning Post] Supporters of Imran Khan begin ‘long march’ to Islamabad
  > A march protesting against the imprisonment of former Pakistani prime minister Imran Khan kicked off in northwest Pakistan on Sunday after talks to avoid the demonstration stalled.
Authorities have been preparing for weeks for the possible arrival of demonstrators in Islamabad, with the march planne
- 2026-10-04 19:20 [Al Jazeera] Pro-Imran Khan mass rally launched after Pakistan government talks fail
  > Supporters of jailed former prime minister have set off from northwest Pakistan towards Islamabad.
- 2026-10-04 19:53 [Al Jazeera] Imran Khan’s party launches march to Islamabad demanding his release
  > Supporters of jailed former Pakistani prime minister Imran Khan have launched a long march towards Islamabad.
- 2026-10-05 05:28 [BBC World] Supporters of jailed ex-PM Imran Khan march to Pakistan capital
  > Thousands have taken to the streets after talks between authorities and Khan's party ended in deadlock.
**B** (2 item(s))
- 2026-10-05 18:32 [Rai News Esteri] A Riyadh si è tenuta la riunione del patto di difesa della Mecca
  > Turchia, Arabia Saudita e Pakistan si sono riuniti nella capitale dell'Arabia Saudita nel quadro del cosiddetto "Patto di Difesa della Mecca", l'alleanza  militare strategica firmata il 7 agosto scorso dai tre paesi.
- 2026-10-05 18:35 [Europa Press Internacional] Turquía y Pakistán enviarán tropas en apoyo a Arabia Saudí tras los ataques de los hutíes
  > Turquía y Pakistán han anunciado este lunes el envío de fuerzas militares en apoyo a Arabia Saudí después de que este país, con el que comparten la Alianza de La Meca, denunciara ataques de los rebeldes hutíes yemeníes contra su territorio.

## U074
**A** (2 item(s))
- 2026-10-08 08:06 [State Department] Secretary of State Marco Rubio Remarks to the Press
  > Marco Rubio, Secretary of State
Athens, Greece
Athens International Airport



	

		
		

			

		

		

			

				
				

					
						Secretary of State Marco Rubio Remarks to the Press
					
				

				

					

					
					
						Remarks

					
					
					
			

			
			

			
			October 8, 2026

			
				


- 2026-10-08 13:38 [Al Jazeera] Rubio praises nationalism and ties ‘America First’ values to ancient Greece
  > US Secretary of State Marco Rubio urged Western nations to prioritise their own interests in a speech in Athens.
**B** (3 item(s))
- 2026-10-08 15:50 [South China Morning Post] US suspends Microsoft, major IT firms from green card programme
  > The US government ⁠is suspending Microsoft, Adobe and ⁠several large IT firms from a programme that allows skilled foreign workers to gain permanent residency, senior US officials have announced, citing alleged fraud, and as part ‌of an effort to push companies to hire more Americans.
“Our message t
- 2026-10-08 17:25 [Al Jazeera] US suspends Microsoft and Adobe from visa programme amid fraud claims
  > Visa probe also targets universities for allegedly exploiting international students to reduce US wage costs.
- 2026-10-08 19:05 [South China Morning Post] US investigates 9 universities over alleged visa fraud, with focus on China
  > The Trump administration is launching an investigation into nine US universities over alleged J-1 visa fraud, with officials raising concerns about Chinese scholars and the Chinese government.
The J-1 programme covers exchange visitors including international researchers, scholars and students, who 

## U075
**A** (5 item(s))
- 2026-10-07 23:20 [Al Jazeera] Christa Pike was nearly taken off life support before waking, lawyers say
  > Death row inmate who survived execution by lethal injection is said to be &#039;angry and confused&#039; about what happened.
- 2026-10-08 03:02 [BBC World] Texas carries out first US execution since Christa Pike's botched lethal injections
  > Lawyers for Jamaal Howard had asked a judge to pause the execution after Christa Pike's botched lethal injections.
- 2026-10-08 08:13 [BBC World] Christa Pike now walking after US execution went wrong, lawyer tells BBC
  > A lawyer says the murderer of Colleen Slemmer is moving around her hospital room after surviving two lethal injections.
- 2026-10-08 08:29 [Al Jazeera] Christa Pike almost taken off life support before she woke up
  > Death row inmate Christa Pike has regained consciousness following a botched execution in Tennessee, her lawyer says.
- 2026-10-08 09:53 [France 24] Christa Pike 'angry and confused' after Tennessee's failed execution effort
  > Christa Pike, sentenced to death for a 1995 murder, awoke "angry ​and confused" in a hospital this week with a long recuperation ahead after surviving Tennessee's botched effort to execute her, her lawyers said on Wednesday.
**B** (5 item(s))
- 2026-10-08 02:35 [Europa Press Internacional] Trump vuelve a hipotetizar sobre ataques iraníes en Los Ángeles y San Diego pese a la polémica generada
  > El presidente de Estados Unidos, Donald Trump, ha reiterado sus controvertidos comentarios acerca de hipotéticos bombardeos iraníes contra las ciudades de Los Ángeles y San Diego --ambas gobernadas por demócratas-- presentando tales eventos como "trauma", "problemas" o "espectáculo de terror" antes 
- 2026-10-08 04:57 [Il Sole 24 Ore Mondo] Guerra in Iran, ultime notizie. «Da Pentagono ordine alle forze armate Usa per eventuale ripresa degli attacchi»
- 2026-10-08 12:26 [El País Internacional] Dos asesores de Trump viajaron a Bosnia-Herzegovina para ayudar al prorruso Milorad Dodik a ganar las elecciones
  > Chris LaCivita, en el centro, viajaba en Estados Unidos junto a Donald Trump a bordo de su avión, conocido como Trump Force One, el lunes 13 de marzo de 2023.
- 2026-10-08 16:35 [Europa Press Internacional] Trump asegura que el Ejército de EEUU no atacará Irán "antes" de las elecciones del 3 de noviembre
  > El presidente de Estados Unidos, Donald Trump, ha asegurado este jueves que no ordenará "ningún" ataque contra Irán antes de las elecciones legislativas, previstas para el próximo 3 de noviembre, mientras las autoridades iraníes sostienen que responderán "en unos días" a la última propuesta de paz p
- 2026-10-08 17:52 [ANSA Mondo] Trump, 'non attaccheremo Iran prima delle midterm, colloqui produttivi con Teheran'
  > "Non attaccheremo l'Iran prima

delle elezioni di metà mandato". Lo afferma Donald Trump sul suo

social Truth, sottolineando che gli Stati Uniti stanno avendo

"discussioni produttive" con l'Iran.

Riproduzione riservata © Copyright ANSA

## U076
**A** (10 item(s))
- 2026-10-04 21:31 [South China Morning Post] US Air Force removes all bombers from UK airbase targeted by suspected terror attack
  > The US Air Force has brought home its bombers stationed at a US-run military airbase in England used to strike Iran following an investigation into a planned terror attack at the RAF Fairford base.
The bombers were redeployed back to their home bases in the United States, according to a Pentagon off
- 2026-10-04 22:23 [Al Jazeera] US withdraws B-1 bomber aircraft from UK’s Fairford base amid Iran fears
  > The abrupt redeployment to the US comes after several &#039;terrorism-related&#039; arrests were made outside RAF Fairford.
- 2026-10-05 04:58 [BBC World] US air force removes all bombers from British military base RAF Fairford
  > A statement says all bombers deployed to RAF Fairford have been "re-deployed to their home stations" in the US.
- 2026-10-05 07:40 [Defense News] US removes B-1 bombers from UK base amid security concerns
  > NEW YORK — The United States removed its B-1 bombers from a U.K. air base one week after several men were arrested there on suspicion of preparing terrorist acts, a Pentagon official said on Sunday. A dozen B-1 bombers were stationed at RAF Fairford air base, located northwest of London. The planes 
- 2026-10-05 09:49 [France 24] US withdraws all bombers from UK base at centre of suspected terror attack
  > The United States has removed its B-1 bombers from a British air base one week after five men were arrested nearby on suspicion of preparing terrorist acts, a ‌suspected plot that British Prime Minister Andy Burnham said was likely backed by Iran. The planes had been ⁠stationed at RAF Fairford, whic
- 2026-10-05 11:09 [Al Jazeera] US abruptly withdraws bombers from UK’s RAF Fairford
  > The US has abruptly withdrawn all of its aircraft from the UK’s RAF Fairford, citing concerns about a potential attack.
- 2026-10-05 12:07 [BBC World] No10 insists UK military base RAF Fairford is safe after US withdraws bombers
  > US media reported a new threat led to the bombers being removed on Sunday, following an incident near the base last week.
- 2026-10-05 17:34 [Al Jazeera] Rubio: No direct link between US bombers removal and UK base incident
  > Rubio stresses US base security, following the removal of B-1 bombers amid alleged threats targeting UK military assets.
- 2026-10-05 19:58 [BBC World] Trump says 'threat' led US to pull bombers from RAF Fairford
  > The Pentagon confirmed on Sunday it had removed the B1 bombers from the base in England back to their home stations in America.
- 2026-10-05 21:40 [South China Morning Post] US bombers moved from UK airbase due to Iran-linked threats, Trump says
  > US President Donald Trump said on Monday that a threat linked to Iran ⁠had prompted the removal of American B-1 bombers from a British airbase.
The planes had been stationed at RAF Fairford, the preferred European base for US bombers, and had recently been used in US strikes on Iran. Last week, five
**B** (5 item(s))
- 2026-10-04 23:23 [Clarín Mundo] Alerta en Rusia: murió una científica por un accidente con bacterias en un laboratorio y debieron aislar a 200 personas
  > Contó que se le rompió un tubo de ensayo recolectando muestras para analizar.Autoridades rusas dicen que el frío impediría la transmisión de un tipo de neumonía.Los funcionarios hablan de "una peste no especificada" y "una infección particularmente peligrosa".
- 2026-10-05 06:53 [Europa Press Internacional] Rusia asegura que la situación epidemiológica en Irkutsk es "estable" tras un supuesto accidente en un laboratorio
  > Las autoridades de Rusia han asegurado que la situación epidemiológica en la región de Irkutsk es "estable", después de activar una serie de medidas de emergencia durante los últimos días a causa de la muerte de una investigadora en un presunto accidente de laboratorio en Shelejov.
- 2026-10-05 10:17 [El País Internacional] Rusia pone bajo observación a cientos de personas tras morir una investigadora de un laboratorio contra la peste
  > Trabajos de desinfección de coranavirus en la estación de tren de Yaroslavsky en Moscú, el 10 de noviembre de 2022.
- 2026-10-05 14:34 [Europa Press Internacional] EEUU pide a Rusia compartir información "de forma rápida y transparente" tras supuesto caso de peste en Irkutsk
  > El Departamento de Estado estadounidense ha instado este lunes a las autoridades de Rusia a compartir información "de forma rápida y transparente" sobre el caso de presunta peste pulmonar en la región de Irkutsk, tras la muerte de una investigadora en un presunto accidente de laboratorio en Shelejov
- 2026-10-05 21:21 [BBC Mundo] EE.UU. "sigue de cerca" el caso de una científica rusa que falleció en un centro de investigación de la peste en Siberia
  > El secretario de Estado, Marco Rubio, expresó su preocupación de que el incidente pudiera haber provocado la propagación de la peste neumónica, aunque señaló que no había motivos para alarmarse.

## U077
**A** (5 item(s))
- 2026-09-29 21:26 [Breaking Defense] Boeing wins Navy next-gen fighter F/A-XX competition
  > Boeing&#8217;s win gives it a monopoly on American sixth-gen fighters, following its 2025 selection to build the F-47.
- 2026-09-29 22:20 [Defense News] US Navy selects Boeing to build next-generation F/A-XX fighter
  > Boeing has been selected to build the Navy’s sixth-generation carrier-based strike fighter, dubbed F/A-XX, icing out what was considered to be its biggest competitor in late-stage negotiations, Northrop Grumman. Inked at $20 billion for the full-scale development phase, the contract, according to a 
- 2026-09-30 03:52 [South China Morning Post] Pentagon picks Boeing to build new carrier fighter jet to replace F/A-18
  > The Pentagon has chosen Boeing to build the US Navy’s next-generation fighter jets in a contract valued at US$20 billion, officials announced Tuesday.
The contract is to produce F/A-XX aircraft or “strike fighters” under the “Next Generation Air Dominance Program,” a Pentagon statement said, adding 
- 2026-09-30 16:21 [Breaking Defense] Boeing nabs $2.4 billion deal for more F-15EX fighters
  > The award came on the same day that the planemaker secured a contract to build a sixth-generation fighter jet for the US Navy.
- 2026-09-30 19:21 [Defense News] US Air Force awards $2.38B contract to Boeing for 22 F-15EX
  > The U.S. Air Force tapped Boeing for a $2.38 billion contract to produce 22 F-15EX Eagle II aircraft, using previously available funds from the congressionally provided reconciliation to maintain procurement before the fiscal year deadline.The award is under Lot 7, which accounts for current program
**B** (2 item(s))
- 2026-10-01 18:38 [South China Morning Post] Canada fast-tracking oil pipeline designed to diversify economy away from US
  > Canada will fast track the approval process for a new proposed crude oil export pipeline to its west coast that could generate over C$20 billion (US$14 billion) a year in GDP, Prime Minister ‌Mark Carney said on Thursday.
The pipeline, which was announced in July, is a crucial part of Carney’s bid t
- 2026-10-01 18:56 [Al Jazeera] Canada to fast track oil pipeline meant to diversify economy away from US
  > Carney declared the pipeline a project of national interest, smoothening its way to a single federal regulatory review.

## U078
**A** (5 item(s))
- 2026-09-29 12:07 [South China Morning Post] Estonia blames Russia for arson attack on company supplying vehicles to Ukraine
  > Estonian authorities said on Tuesday they had concluded that an arson attack in mid-August on a defence company that provides military vehicles to Ukraine was an act of sabotage commissioned by Russian security services.
Foreign Minister Margus Tsahkna said that “such actions are absolutely unaccept
- 2026-09-29 13:15 [BBC World] Estonia blames Russia for arson at defence company supplying Ukraine
  > Russia has been accused of launching sabotage attacks across a number of European Nato countries which have been helping Ukraine.
- 2026-09-29 13:26 [Al Jazeera] Estonia says Russia ordered August arson attack on defence company
  > Tallinn accuses Moscow of responsibility for the fire at Estonian company Milrem Robotics, a supplier of unmanned ground vehicles to Ukraine.
- 2026-09-29 14:42 [Breaking Defense] Estonia accuses Russia of ordering August arson attack on Milrem
  > Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to undermine our unity and support for Ukraine,” NATO Secretary General Mark Rutte said today.
- 2026-09-29 14:52 [Defense News] Estonia blames Russia in arson attack on military robotics firm Milrem
  > GLASGOW, Scotland — Russian special services were behind the fire at a building used by an Estonian military robotics company last month, the government in Tallinn said on Tuesday. The finding comes after a six-week investigation by the Estonian Internal Security Service. In a press statement, the g
**B** (5 item(s))
- 2026-09-30 22:13 [Al Jazeera] Russian drone crashes into Kyiv playground without exploding
  > A Russian attack drone crashed into a children’s playground in Kyiv, Ukraine without exploding.
- 2026-10-01 07:09 [South China Morning Post] Ukraine scrambles as Russia’s jet drones breach Kyiv’s defences
  > Russia’s new class of jet-powered drones rip across the night sky in Kyiv at hundreds of kilometres per hour, leaving Ukrainian air-defence units only moments to intercept them. It’s rarely enough time.
With many of the drones getting through to the capital, defence manufacturers are scrambling to d
- 2026-10-01 13:06 [Al Jazeera] Russian drone hits school in Ukraine’s Kyiv as Moscow presses air assault
  > Russian drone strikes hit a school in Kyiv and the main bridge, disrupting transport in the latest wave of attacks.
- 2026-10-02 08:03 [Al Jazeera] Russia tries to freeze Ukraine as it suffers record casualties and retreats
  > Moscow has suffered further losses of occupied territory, but is using new drones to beat Ukraine&#039;s defences.
- 2026-10-02 12:47 [Al Jazeera] Ukraine calls for tighter sanctions as Russian attacks spark Kyiv gridlock
  > Closure of bridges struck by drones in Ukrainian capital causes traffic chaos.

## U079
**A** (56 item(s))
- 2026-10-04 03:30 [El País Internacional] Ni Bolsonaro, ni Lula: Trump se reserva (de momento) su apoyo en las elecciones de Brasil
  > Un asistente a un mitin de Flavio Bolsonaro disfrazado de Trump, el pasado domingo.
- 2026-10-04 04:00 [El País Internacional] La disputa entre Lula y Trump marca las elecciones brasileñas
  > Banderas de Flavio Bolsonaro y Luiz Inacio Lula da Silva en Brasilia, el 29 de septiembre.
- 2026-10-04 11:20 [Rai News Esteri] Urne aperte in Brasile per le elezioni presidenziali e legislative, sfida Lula-Bolsonaro
  > Gli ultimi sondaggi davano un testa a testa
- 2026-10-04 20:19 [El País Internacional] Brasil decide su futuro entre Lula y Bolsonaro, un estadista desgastado y el hijo de un ultra
  > El presidente Lula, el día 24 en São Gonçalo, y Flávio Bolsonaro, este sábado en Río.
- 2026-10-04 20:43 [Europa Press Internacional] Bolsonaro gana la primera vuelta en Brasil con el 47% de los votos y disputará contra Lula (45%) la segunda vuelta
  > El candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil e hijo del expresidente Jair Bolsonaro, Flávio Bolsonaro, ha ganado la primera vuelta de las elecciones en Brasil con un 47,17% de los sufragios. Su rival y presidente saliente, Luiz Inácio Lula da Silva, ha quedado cua
- 2026-10-04 22:25 [ANSA Mondo] Media, Lula e Bolsonaro andranno al ballottaggio il 25 ottobre
  > A metà scrutinio Bolsonaro al 49%, Lula a 42%
- 2026-10-04 23:00 [Clarín Mundo] Los Bolsonaro amplían su presencia en el Congreso con las elecciones en Brasil: entran la esposa del ex presidente y dos hermanos de Flavio
  > Michelle, la exprimera dama brasileña alcanzó el 28% de los votos en las elecciones legislativas del Distrito Federal.Otros dos hijos del expresidente Jair Bolsonaro compitieron por bancas legislativas en el estado de Santa Catarina.
- 2026-10-04 23:23 [Clarín Mundo] Elecciones en Brasil: Flávio Bolsonaro, un presidenciable a la sombra de su padre
  > Tiene 45 años y es el mayor de los cinco hijos del ex presidente. Elogia las políticas de seguridad de Nayib Bukele en El Salvador y promete la construcción de numerosas cárceles. Asimismo, presume de su buena relación con Donald Trump tras mantener una reunión privada en la Casa Blanca.
- 2026-10-04 23:23 [Clarín Mundo] Lula da Silva busca su reelección en Brasil: entre el freno a la ultraderecha y la defensa de su legado social
  > • A los 80 años, el mandatario brasileño busca la reelección apoyado en su historial de programas sociales como el Bolsa Familia, que actualmente beneficia a una cuarta parte de la población.
• Con vistas a un nuevo período, impulsa una reforma laboral para reducir la jornada semanal a cinco días y 
- 2026-10-05 00:09 [Rai News Esteri] Il sorpasso di Bolsonaro, la crisi di Lula
  > Flavio Bolsonaro, figlio dell'ex presidente di estrema destra tentato golpista, vince il primo turno sul presidente di sinistra Lula da Silva
- 2026-10-05 00:12 [Clarín Mundo] Elecciones en Brasil: un voto castigo que sorprendió a Lula da Silva y llegó desde su base tradicional de votantes
  > Un primer análisis indica que los sectores de menores ingresos se distanciaron de la elección y del líder del PT. El país es un éxito macro, con números notables, pero esos resultados no llegaron a los bolsillos de ese amplio espacio de votantes que se endeuda para pagar los gastos básicos.
- 2026-10-05 01:03 [Clarín Mundo] Lula acepta el impacto del triunfo de Bolsonaro: fue "un resultado inesperado"
  > El representante del socialista Partido de los Trabajadores busca su cuarto mandato, con la reelección en la gestión actual.Quedó detrás de Flavio Bolsonaro por apenas 2,15 puntos.
- 2026-10-05 01:08 [Clarín Mundo] Flavio Bolsonaro, tras ganar en primera vuelta ante Lula: "Brasil quiere un cambio"
  > Aseguró también que este resultado marcan "el fin de la era del PT" en su país.Dijo estar "feliz" con los números obtenidos frente al actual mandatario, Lula da Silva.
- 2026-10-05 01:41 [El País Internacional] Arrasadora victoria de la derecha en Brasil
  > Flavio Bolsonaro habla con la prensa en Río de Janeiro, este domingo.
- 2026-10-05 02:13 [Europa Press Internacional] Bolsonaro proclama "fin de la era del PT" y Lula apela a combatir su "pasado tenebroso" en la segunda vuelta en Brasil
  > Bolsonaro supera los 55 millones de apoyos (47,04%) y logra una ventaja de 2,3 millones de sufragios sobre el actual mandatario (45,15%)
- 2026-10-05 02:28 [El País Internacional] El apellido Bolsonaro gana desde la cárcel
  > Flávio Bolsonaro, candidato presidencial de Brasil, este domingo tras los resultados de la primera vuelta.
- 2026-10-05 02:39 [BBC Mundo] Cómo se compara Flávio Bolsonaro con su padre Jair y cuánto cambia el duelo con Lula por la presidencia de Brasil 4 años después
  > El senador derechista pasa fortalecido al balotaje contra el presidente de izquierda tras obtener más votos en la primera vuelta contra varios pronósticos, pero la elección sigue abierta.
- 2026-10-05 02:46 [France 24 Español] Simone Pitta: "Con esta primera vuelta se puede ver una consolidación del bolsonarismo en Brasil"
  > Pese a no haber estado en el poder en el último periodo presidencial de Brasil, y pese a las denuncias y condenas contra el expresidente Jair Bolsonaro por un intento de golpe de Estado, el bolsonarismo logró consolidarse de cara a los comicios de este 4 de octubre. Ahora, Flávio Bolsonaro busca pos
- 2026-10-05 02:47 [France 24 Español] Juan Agulló: "A diferencia de otros países de Latinoamérica, Brasil es un competidor directo"
  > En un escenario marcado por la polarización en Brasil, el candidato de ultraderecha y heredero político de su padre, Flávio Bolsonaro, y el actual presidente, Luiz Inácio Lula da Silva, quien busca un cuarto mandato, se disputan el balotaje. La sombra de Estados Unidos estuvo presente durante la pri
- 2026-10-05 02:54 [El País Internacional] Bolsonaro vence a Lula en primera vuelta de las elecciones y acaricia el retorno de la ultraderecha al poder en Brasil
  > Flávio Bolsonaro habla tras clasificarse para la segunda vuelta en Brasilia, Brasil, este domingo.
- 2026-10-05 03:19 [France 24 Español] Brasil: la derecha de Bolsonaro se fortalece en las regiones, con un triunfo holgado en São Paulo
  > Los comicios locales de Brasil se saldaron este domingo con un avance de la derecha que representan el candidato presidencial Flávio Bolsonaro y sus aliados. En tanto la izquierda del presidente y aspirante a la reelección, Luiz Inácio Lula da Silva perdía terreno. La victoria más cómoda fue en São 
- 2026-10-05 03:36 [El País Internacional] Las claves de la primera vuelta en Brasil: de la fuerza ultra al día después de Lula con América Latina pendiente
  > Flávio Bolsonaro vota en Río de Janeiro, este domingo.
- 2026-10-05 03:41 [France 24 Español] Flávio Bolsonaro tritura las encuestas: una ventaja pequeña, pero un escenario cuesta arriba para Lula
  > Brasil quedó inclinado hacia la tendencia de retorno a la derecha que sacude a América Latina, luego de que el senador e hijo del expresidente Jair Bolsonaro aventajara por casi dos puntos al izquierdista Luiz Inácio Lula da Silva en la primera vuelta de las elecciones. Lula ha reconocido el resulta
- 2026-10-05 04:08 [El País Internacional] Videoanálisis | Lula se enfrenta a una segunda vuelta electoral muy complicada
  > Videoanálisis | Lula Y Flávio Bolsonaro se enfrenta a una segunda vuelta electoral
- 2026-10-05 04:33 [Rai News Esteri] Brasile, avanzata del clan Bolsonaro: quattro eletti in Parlamento, Flavio al ballottaggio con Lula
  > L'ex first lady Michelle e Carlos, uno dei figli dell'ex presidente, conquistano un seggio al Senato. Alla Camera entrano il figlio più giovane Jair Renan e Renato, fratello di Jair
- 2026-10-05 05:14 [Il Sole 24 Ore Mondo] Brasile, Bolsonaro vince al primo turno con 47%, Lula al 45%: ballottaggio il 25 ottobre
  > Flavio Bolsonaro batte Lula al primo turno e si lancia come favorito nel ballottaggio del 25 ottobre che deciderà chi sarà il 40esimo presidente del Brasile. Il candidato trumpiano ha ottenuto il 47,14 % dei voti, il presidente uscente il 45.03 %, con una differenza tra i due di circa 2 milioni e me
- 2026-10-05 05:31 [Europa Press Internacional] Trump tacha de "corruptas" las elecciones de EEUU comparándolas con las de Brasil tras la victoria de Bolsonaro
  > El presidente de Estados Unidos, Donald Trump, ha vuelto a cargar contra el proceso electoral en su propio país, tachándolo de corrupto y contraponiéndolo la rapidez en el escrutinio de los votos de 125 millones de personas "en la primera vuelta de las elecciones presidenciales de Brasil", donde el 
- 2026-10-05 05:46 [Europa Press Internacional] Milei felicita a su "querido amigo" Flávio Bolsonaro por su "histórica elección" frente a Lula en Brasil
  > El presidente de Argentina, Javier Milei, ha felicitado al candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil, Flávio Bolsonaro, por su victoria en la primera vuelta de las elecciones presidenciales celebradas este domingo, en las que se ha impuesto con el 47,03% de los vo
- 2026-10-05 06:44 [ANSA Mondo] Brasile, l'ex giudice che condannò Lula eletto governatore
  > Sergio Moro guiderà l'esecutivo del suo stato natale, il Paranà
- 2026-10-05 07:14 [BBC Mundo] Elecciones en Brasil: Flávio Bolsonaro y Lula da Silva van a una segunda vuelta en la que el presidente enfrenta una difícil remontada
  > La mayor democracia de América Latina irá a balotaje el 25 de octubre. Lula lleva la desventaja frente a Bolsonaro, ya que históricamente nunca hubo una remontada en una segunda vuelta electoral en Brasil.
- 2026-10-05 07:46 [ANSA Mondo] In Brasile un 30enne di destra è il deputato più votato della storia
  > Nikolas Ferreira ha raccolto oltre 3,1 milioni di preferenze per la Camera
- 2026-10-05 10:46 [ANSA Mondo] Astensione record in Brasile, il 21,08% non ha votato al primo turno
  > Si tratta del livello più alto registrato dalle elezioni del 1998 (21,5%)
- 2026-10-05 11:42 [France 24 Español] Brasil irá a segunda vuelta: Flávio Bolsonaro lidera la primera ronda
  > Brasil se encamina a una segunda vuelta presidencial tras una elección marcada por la polarización. El senador Flávio Bolsonaro obtuvo el primer lugar en la primera vuelta, pero sin alcanzar la mayoría necesaria para evitar el balotaje. El próximo 25 de octubre se enfrentará al actual presidente, Lu
- 2026-10-05 12:20 [Rai News Esteri] Il primo turno delle presidenziali in Brasile, avanti Bolsonaro: ribaltati i pronostici pro-Lula
  > La sfida per il secondo turno del 25 ottobre è ancora aperta ma il presidente uscente non minimizza il peso di una pesante bocciatura delle sue politiche
- 2026-10-05 12:21 [Rai News Esteri] Presidenziali in Brasile, Flavio Bolsonaro a sorpresa supera Lula di 2 punti. Si va al ballottaggio
  > Il candidato di destra al 47%: "Il Brasile vuole cambiare". Il presidente uscente al 45%: "Sono bravo ai supplementari". Scelta rinviata al secondo turno del 25 ottobre
- 2026-10-05 12:29 [Clarín Mundo] Elecciones en Brasil 2026, EN VIVO: reacciones tras la victoria de Flávio Bolsonaro sobre Lula y últimas noticias del balotaje
  > Bolsonaro se impuso en la primera vuelta al superar por casi dos puntos al actual presidente Lula da Silva. El balotaje entre ambos se hará el 25 de octubre. Todas las repercusiones, minuto a minuto.
- 2026-10-05 12:31 [Clarín Mundo] Quién es Flávio Bolsonaro, el hijo de Jair que sorprendió a Lula y va por la presidencia de Brasil
  > Nacido en el estado de Río de Janeiro, Flávio es el mayor de los cinco hijos del expresidente y el que más se le parece físicamente.Este senador, de 45 años, enfrentará a Lula en el balotaje el próximo 25 de octubre.
- 2026-10-05 13:05 [France 24 Español] Informe desde Río de Janeiro: el Partido Liberal de Bolsonaro se fortalece en el Senado
  > Las elecciones legislativas en Brasil dejaron un resultado clave para el futuro político del país: el Partido Liberal (PL), formación vinculada al expresidente Jair Bolsonaro y que postuló a Flávio Bolsonaro para la Presidencia, amplió significativamente su presencia en el Senado. La bancada pasará 
- 2026-10-05 13:16 [Clarín Mundo] Elecciones en Brasil: los mercados celebran la ventaja de Flávio Bolsonaro sobre Lula y el principal índice de la Bolsa marca un nuevo récord
  > Los activos brasileños se dispararon este lunes y el real se apreció en la primera sesión de los mercados tras los comicios del domingo. El índice Ibovespa superó la marca de los 209.000 puntos por primera vez.
- 2026-10-05 13:57 [BBC Mundo] Quiénes son Lucas Pavanato y Nikolas Ferreira, los jóvenes influencers de derecha que lograron las mayores votaciones en la historia de la Cámara de Diputados de Brasil
  > Los flamantes legisladores comparten una agenda conservadora que incluye el rechazo a las políticas de género, el endurecimiento de las sanciones penales y la legalización del porte de armas como herramienta para combatir la delincuencia.
- 2026-10-05 14:50 [Clarín Mundo] Elecciones en Brasil: los resultados del domingo cambian por completo el diseño del país y ya asoma una amnistía para Jair Bolsonaro
  > La victoria del candidato conservador Flávio Bolsonaro sobre el presidente Lula da Silva en primera vuelta excede lo que pueda ocurrir en el balotaje.La ola de derecha se consolida con victorias en las gobernaciones y especialmente en el Parlamento.Aun si el líder petista lograra imponerse el 25 de 
- 2026-10-05 15:47 [Clarín Mundo] La reacción de los medios en Brasil tras la victoria de Bolsonaro: desde "el ciclo de Lula está terminado" hasta "el tsunami de lo peor de la derecha"
  > Los títulos, opiniones y análisis de la prensa en Brasil tras la primera vuelta de las presidenciales de este domingo.
- 2026-10-05 15:59 [France 24 Español] Flávio Bolsonaro y Lula da Silva se preparan para el balotaje en Brasil
  > 🇧🇷🗳️ Luiz Inácio Lula da Silva y Flávio Bolsonaro ofrecieron declaraciones después de que los resultados de los comicios presidenciales de Brasil confirmaran que deberán disputar el balotaje del 25 de octubre.
- 2026-10-05 16:02 [El País Internacional] El lulismo cruje ante la ofensiva ultra
  > Carteles del presidente Trump y del candidato Flavio Bolsonaro, en São Paulo, Brasil, este Lunes.
- 2026-10-05 16:10 [France 24 Español] "Solo faltan días para el rescate Brasil": Bolsonaro celebra la victoria sobre Lula
  > El senador del Partido Liberal (PL) y candidato presidencial, Flávio Bolsonaro, agradeció este lunes "a Dios" y al pueblo brasileño por su victoria en las elecciones del domingo ante el presidente Luiz Inácio Lula da Silva, en contra de los pronósticos. Además, celebró que el PL resultara el partido
- 2026-10-05 16:23 [Clarín Mundo] Elecciones en Brasil: a contrarreloj, Lula y el PT analizan cambios totales en la estrategia de campaña
  > Lo anticipan fuentes partidarias, pero no es claro en qué consistirán. Trascendió que ha habido tensiones internas sobre el manejo de la campaña.Y que debido a eso se perdieron oportunidades importantes para reducir el impulso del candidato opositor, Flávio Bolsonaro.
- 2026-10-05 16:36 [France 24 Español] Paraguay, refugio fiscal y político para la extrema derecha brasileña
  > En los últimos cinco años, las solicitudes de permisos de residencia de brasileños en Paraguay se han más que duplicado. Muchos de los recién llegados son simpatizantes de Jair Bolsonaro que temen una reelección del actual presidente, Luiz Inácio Lula da Silva, a quien responsabilizan de un deterior
- 2026-10-05 17:02 [ANSA Mondo] Brasile, Erika Hilton è la donna più votata della storia alla Camera
  > La politica brasiliana Erika

Hilton ha stabilito un nuovo record nella storia della Camera

dei deputati brasiliana, diventando la donna più votata di

sempre. La deputata trans del Partito socialismo e libertà

(Psol) di San Paolo è stata rieletta con 1.596.472 voti, pari al

5,9% dei voti espress
- 2026-10-05 17:30 [Clarín Mundo] El fantasma de Bolsonaro reaparece en Europa: los temores de Bruselas ante un eventual cambio de gobierno en Brasil
  > • Un cambio de gobierno en Brasil aportaría argumentos a los eurodiputados que buscan frenar la ratificación del entendimiento comercial.
• Si entre 50 y 80 legisladores modifican su postura en la votación prevista para los próximos meses, la aplicación provisional del pacto quedará suspendida.
- 2026-10-05 18:04 [France 24 Español] El mercado de valores de Brasil aplaude la ventaja de Bolsonaro en primera vuelta presidencial
  > El índice bursátil iBovespa, el más importante de la bolsa de São Paulo inició la jornada con un alza estrepitosa de casi el 9% y alcanzó máximo histórico, mientras el real brasileño gana 4,5% frente al dólar a media jornada, hasta situarse ligeramente por encima de los 5 reales por dólar. El buen r
- 2026-10-05 18:10 [France 24 Español] La dinastía Bolsonaro se fortalece: prensa brasileña sobre la primera vuelta electoral
  > La familia Bolsonaro no solo ganó la primera vuelta en Brasil, fortaleció su presencia en ambas cámaras del Congreso y conserva los respaldos de más de 10 gobernadores. 'O Globo' habla del bloque familiar que se ha hecho con varios cargos. Hermanos, hijos, esposa y exesposa tienen un puesto de elecc
- 2026-10-05 19:41 [El País Internacional] La ola conservadora de América Latina llega a Brasil
  > Flávio Bolsonaro (i) junto al presidente de EE.UU., Donald Trump, en el despacho oval de la Casa Blanca en Washington, el 26 de mayo de 2026.
- 2026-10-05 19:42 [El País Internacional] La victoria en primera vuelta de Bolsonaro impulsa a la ola ultra de América Latina
  > Transeúntes pasan ante pósteres dañados que muestran a Bolsonaro hijo con el presidente Trump, este lunes en São Paulo.
- 2026-10-05 19:47 [Clarín Mundo] Elecciones en Brasil: las urnas de la sorpresa
  > Tras el imprevisto triunfo de Flávio Bolsonaro sobre Lula en la primera vuelta, Brasil se encamina hacia un balotaje decisivo el próximo 25 de octubre. La contienda electoral ratifica la profunda polarización política del país y la consolidación del bolsonarismo como una fuerza de derecha permanente
- 2026-10-05 20:21 [ANSA Mondo] Trump, il risultato di Bolsonaro in Brasile una 'grande vittoria'
  > Il risultato di Flavio Bolsonaro

alle elezioni in Brasile è stata una "grande vittoria". Lo ha

detto Donald Trump.Quella di Bolsonaro "è una grande vittoria: combattuta, ma una

vittoria davvero enorme. Incredibile", ha detto Trump. Bolsonaro

si avvia al ballottaggio del 25 ottobre come favorito.
- 2026-10-05 22:09 [ANSA Mondo] Brasile, l'ex presidente Temer sostiene Bolsonaro al ballottaggio
  > L'ex presidente brasiliano

Michel Temer (2016-2018) ha dichiarato il suo sostegno a Flávio

Bolsonaro in vista del ballottaggio del 25 ottobre contro Luiz

Inácio Lula da Silva. In un video diffuso sui social, Temer ha

affermato che il risultato del primo turno mostra la volontà

degli elettori di
**B** (5 item(s))
- 2026-10-04 23:23 [Clarín Mundo] Alerta en Rusia: murió una científica por un accidente con bacterias en un laboratorio y debieron aislar a 200 personas
  > Contó que se le rompió un tubo de ensayo recolectando muestras para analizar.Autoridades rusas dicen que el frío impediría la transmisión de un tipo de neumonía.Los funcionarios hablan de "una peste no especificada" y "una infección particularmente peligrosa".
- 2026-10-05 06:53 [Europa Press Internacional] Rusia asegura que la situación epidemiológica en Irkutsk es "estable" tras un supuesto accidente en un laboratorio
  > Las autoridades de Rusia han asegurado que la situación epidemiológica en la región de Irkutsk es "estable", después de activar una serie de medidas de emergencia durante los últimos días a causa de la muerte de una investigadora en un presunto accidente de laboratorio en Shelejov.
- 2026-10-05 10:17 [El País Internacional] Rusia pone bajo observación a cientos de personas tras morir una investigadora de un laboratorio contra la peste
  > Trabajos de desinfección de coranavirus en la estación de tren de Yaroslavsky en Moscú, el 10 de noviembre de 2022.
- 2026-10-05 14:34 [Europa Press Internacional] EEUU pide a Rusia compartir información "de forma rápida y transparente" tras supuesto caso de peste en Irkutsk
  > El Departamento de Estado estadounidense ha instado este lunes a las autoridades de Rusia a compartir información "de forma rápida y transparente" sobre el caso de presunta peste pulmonar en la región de Irkutsk, tras la muerte de una investigadora en un presunto accidente de laboratorio en Shelejov
- 2026-10-05 21:21 [BBC Mundo] EE.UU. "sigue de cerca" el caso de una científica rusa que falleció en un centro de investigación de la peste en Siberia
  > El secretario de Estado, Marco Rubio, expresó su preocupación de que el incidente pudiera haber provocado la propagación de la peste neumónica, aunque señaló que no había motivos para alarmarse.

## U080
**A** (2 item(s))
- 2026-09-30 03:21 [South China Morning Post] US Supreme Court lets Trump resume deportations to third countries
  > The US Supreme Court on Tuesday let President Donald Trump’s administration continue swiftly deporting people to countries other than their own for now, while the justices consider whether the policy is legal.
The apparent 6-3 order temporarily lifts lower court requirements for migrants to get a ch
- 2026-10-01 17:35 [Al Jazeera] US Supreme Court agrees to take up Trump’s ICE detention policy
  > The case is the latest dispute over US President Donald Trump’s sweeping immigration crackdown.
**B** (2 item(s))
- 2026-09-30 23:34 [South China Morning Post] Woman told Cornell police 2 years ago she was 100% sure she was raped, transcript shows
  > A woman who filed a lawsuit saying she was sexually assaulted by seven men at a Cornell University fraternity house told police weeks after the incident that she could “say with 100 per cent confidence I was raped”, according to a report by CBS New York, which said it obtained a transcript of her in
- 2026-10-01 19:47 [Al Jazeera] Cornell rape allegations renew push to change New York sexual assault law
  > New York law treats intoxicated victims differently depending on whether they willingly consumed alcohol or drugs.

## U081
**A** (8 item(s))
- 2026-09-29 14:40 [Defense News] US forces exiting Iraq after 2 decades, leaving opening for Iran
  > U.S. forces are set to depart from their last bases in Iraq by Wednesday, a move celebrated as a victory by Iran and its allies, who now have deep influence in the country where 4,500 Americans died during more than two decades of war.Iraqi security experts say the withdrawal — agreed to in 2024 und
- 2026-09-29 20:00 [Al Jazeera] US troops fully withdraw from Baghdad base after two decades
  > US Army soldiers have fully withdrawn from the US base in Baghdad.
- 2026-09-30 09:46 [South China Morning Post] US ends troop mission in Iraq, Baghdad to celebrate Sovereignty Day on October 1
  > A US-led coalition deployed in Iraq more than a decade ago to fight jihadists concluded its mission on Wednesday, a move celebrated by the country’s leaders, but which some fear will embolden pro-Iran armed factions.
Coalition troops deployed to Iraq and Syria in 2014 to fight Islamic State, which h
- 2026-09-30 11:36 [BBC World] Last UK and US troops leave Iraq as anti-Islamic State mission ends
  > The withdrawal of coalition forces, under a deal agreed two years ago, was a key demand of the Iraqi government.
- 2026-09-30 12:17 [Al Jazeera] Iraq celebrates National Sovereignty Day as US troops withdraw
  > Iraq’s security forces held parades in Baghdad and Najaf to celebrate ‘Sovereignty Day’ as US troops withdraw.
- 2026-09-30 14:04 [Breaking Defense] US withdraws last remaining troops out of Iraq
  > “As we step back and hand full primary responsibility for Iraq’s security to the Government of Iraq and the brave people of Iraq, US and Coalition forces stationed across the region will remain ready to respond to any ISIS threats that arise,” CENTCOM Commander Adm. Brad Cooper said.
- 2026-09-30 16:33 [Al Jazeera] Pentagon says US troop withdrawal from Iraq is complete
  > The withdrawal ends two decades of foreign intervention in Iraq as part of &#039;global war on terror&#039; and anti-ISIL fight.
- 2026-10-01 01:11 [Al Jazeera] Iraq celebrates Sovereignty Day as US troops complete withdrawal
  > Night time celebrations filled the air as Iraqis observed the start of a four-day holiday.
**B** (2 item(s))
- 2026-10-01 14:00 [South China Morning Post] China backs Cuba, Beijing’s Panama threat, new UN chief: 7 Latin America relations reads
  > We have selected seven of the most interesting and important news stories covering Latin American relations from the past few weeks. If you would like to see more of our reporting, please consider subscribing.
1. China pledges to ‘firmly support’ Cuba as US escalates pressure on Havana

China will s
- 2026-10-02 20:52 [Al Jazeera] Latin America sees China as more positive global influence than US: Poll
  > Annual Latinobarometro survey finds views of China’s influence improving as perceptions of US influence worsen.

## U082
**A** (2 item(s))
- 2026-10-07 22:27 [France 24] DNC sues Trump administration over taxpayer-funded TV ads promoting president
  > The Democratic National Committee sued President Donald Trump’s administration on Wednesday over taxpayer-funded television ads promoting his political message, alleging illegal government propaganda. The lawsuit seeks to halt federal funding for the ads, which have cost more than $12 million to air
- 2026-10-08 01:21 [Al Jazeera] Democrats sue US President Trump over taxpayer-funded ad campaign
  > Trump has faced a bipartisan backlash over ads that critics say violate prohibitions on taxpayer-funded propaganda.
**B** (6 item(s))
- 2026-10-08 00:56 [Europa Press Internacional] Maduro y Flores podrían ser acusados este jueves de haber torturado a estadounidenses venezolanos
  > El presidente de Venezuela, Nicolás Maduro, y su esposa, Cilia Flores, podrían ser acusados por estar vinculados a delitos de tortura contra ciudadanos estadounidenses que estuvieron bajo custodia de su gobierno en los últimos años, ha informado la prensa estadounidense.
- 2026-10-08 14:52 [Clarín Mundo] Torturas: Estados Unidos suma una nueva acusación contra Nicolás Maduro
  > El derrocado presidente de Venezuela ya enfrenta delitos de narcotráfico.Maduro y su esposa, Cilia Flores, permanecen tras las rejas en Nueva York desde principios de enero.
- 2026-10-08 15:13 [France 24 Español] EE. UU. suma a Maduro y Cilia Flores un cargo por conspiración para torturar a opositores
- 2026-10-08 15:20 [El País Internacional] Nicolás Maduro y Cilia Flores, acusados en EE UU de nuevos cargos de tortura y represión
  > Ilustración de Nicolás Maduro y Cilia Flores en el tribunal de Nueva York, en julio.
- 2026-10-08 15:21 [BBC Mundo] Presentan nuevos cargos contra Maduro y su esposa por presuntas torturas a ciudadanos de estadounidenses ante un tribunal de Nueva York
  > El expresidente de Venezuela y su esposa fueron acusados por el Departamento de Justicia de EE.UU. de haber participado en la tortura de estadounidenses detenidos en Caracas.
- 2026-10-08 15:32 [Europa Press Internacional] EEUU imputa a Maduro y su esposa por liderar un sistema de represión y torturas en Venezuela
  > La Fiscalía de Estados Unidos ha imputado este jueves al presidente de Venezuela, Nicolás Maduro, y su esposa, Cilia Flores, por delitos de tortura contra personas detenidas, incluyendo ciudadanos estadounidenses, en el marco de un "sistema de represión que recurría a la violencia contra la oposició

## U083
**A** (5 item(s))
- 2026-09-29 21:26 [Breaking Defense] Boeing wins Navy next-gen fighter F/A-XX competition
  > Boeing&#8217;s win gives it a monopoly on American sixth-gen fighters, following its 2025 selection to build the F-47.
- 2026-09-29 22:20 [Defense News] US Navy selects Boeing to build next-generation F/A-XX fighter
  > Boeing has been selected to build the Navy’s sixth-generation carrier-based strike fighter, dubbed F/A-XX, icing out what was considered to be its biggest competitor in late-stage negotiations, Northrop Grumman. Inked at $20 billion for the full-scale development phase, the contract, according to a 
- 2026-09-30 03:52 [South China Morning Post] Pentagon picks Boeing to build new carrier fighter jet to replace F/A-18
  > The Pentagon has chosen Boeing to build the US Navy’s next-generation fighter jets in a contract valued at US$20 billion, officials announced Tuesday.
The contract is to produce F/A-XX aircraft or “strike fighters” under the “Next Generation Air Dominance Program,” a Pentagon statement said, adding 
- 2026-09-30 16:21 [Breaking Defense] Boeing nabs $2.4 billion deal for more F-15EX fighters
  > The award came on the same day that the planemaker secured a contract to build a sixth-generation fighter jet for the US Navy.
- 2026-09-30 19:21 [Defense News] US Air Force awards $2.38B contract to Boeing for 22 F-15EX
  > The U.S. Air Force tapped Boeing for a $2.38 billion contract to produce 22 F-15EX Eagle II aircraft, using previously available funds from the congressionally provided reconciliation to maintain procurement before the fiscal year deadline.The award is under Lot 7, which accounts for current program
**B** (3 item(s))
- 2026-09-30 05:05 [Al Jazeera] Hegseth to cut number of US general and admiral positions by 20%
  > Pentagon official says the plan will be announced in the defence secretary&#039;s &#039;State of the Force&#039; address in Virginia.
- 2026-09-30 21:42 [South China Morning Post] Trump defence chief says US slashed number of generals and admirals by 20%
  > US Defence Secretary Pete Hegseth announced on Wednesday that the United States has slashed the number of its generals and admirals by 20 per cent, in a move he said is aimed at “accountability”.
Hegseth suggested the cuts targeted officers who failed to get on board with his efforts to ensure the m
- 2026-10-01 02:34 [Al Jazeera] Hegseth announces 20% cut to US military commanders
  > US Secretary of Defense Pete Hegseth says he’s firing 20% of the military’s generals and admirals.

## U084
**A** (7 item(s))
- 2026-10-03 23:35 [Rai News Esteri] Marea sociale contro il caro-affitti in Spagna: le piazze spingono Sánchez verso le urne
  > Ondata di proteste da Madrid a tutte le principali città per il diritto alla casa dopo lo sfratto dell'ottantasettenne Mari Carmen; il rifiuto dei decreti da parte delle destre e dei catalani di Junts apre lo scenario di elezioni anticipate
- 2026-10-04 17:28 [Rai News Esteri] Casa e scuola: il filo rosso che lega le proteste in Europa
  > In Spagna per il diritto alla casa, in Francia l'erosione allo studio accende lo scontento dei più giovani
- 2026-10-04 23:15 [Rai News Esteri] La Spagna in piazza per il diritto alla casa. E Sanchez pensa al voto anticipato
  > Centinaia di migliaia di persone al fianco delle proteste di Madrid per la casa, il governo bocciato in Parlamento valuta elezioni a fine novembre
- 2026-10-05 06:21 [Il Sole 24 Ore Mondo] Caro casa, prezzi e affitti salgono nell’Ue. Il Governo studia le misure per giovani e locazioni
  > «Serve una formazione di qualità, un lavoro sicuro e stabile, una retribuzione adeguata, una casa a un prezzo equo», ha detto di recente la premier Giorgia Meloni
- 2026-10-05 10:27 [Rai News Esteri] La Spagna al voto: i sondaggi premiano le destre, l'area progressista frammentata
  > Il partito popolare e Vox arriverebbero al 52%, secondo un sondaggio per El Pais. Ma le rilevazioni sono state realizzate prima della crisi di governo e della bocciatura dei decreti presentati da Sanchez
- 2026-10-05 19:05 [Il Sole 24 Ore Mondo] Sanchez sfida le destre: Spagna al voto anticipato
  > Dopo la bocciatura sul piano casa, il premier socialista convoca le elezioni cavalcando le proteste di piazza: «Serve una maggioranza progressista per nuovi progressi sociali»
- 2026-10-05 21:04 [Rai News Esteri] Migliaia di persone a Barcellona in piazza per il diritto alla casa
  > Dopo Madrid e Valencia anche Barcellona stasera è scesa in piazza all'annuncio di elezioni anticipate, in migliai hanno sfilato per difendere il diritto alla casa
**B** (6 item(s))
- 2026-10-05 07:14 [Al Jazeera] Spanish Prime Minister Pedro Sanchez announces snap election
  > Sanchez calls early vote after parliament rejected housing relief measures proposed by his minority government.
- 2026-10-05 08:04 [South China Morning Post] Spain’s prime minister calls early election as housing becomes national flashpoint
  > Spanish Prime Minister Pedro Sanchez announced early elections Monday after his government suffered a bruising legislative defeat last week on emergency measures related to the country’s housing crisis.
The vote will be held on November 29.
In recent weeks, Spaniards have demanded solutions from the
- 2026-10-05 10:18 [BBC World] Spanish PM Sánchez calls early election after housing protests
  > Sánchez says Spain will head to the polls on 29 November after recent defeats on measures aimed at addressing the country's housing crisis.
- 2026-10-05 17:27 [Al Jazeera] Spain calls snap election amid housing crisis
  > Mounting anger over Spain’s housing crisis have led Prime Minister Sanchez to call an early election on November 29
- 2026-10-05 19:30 [BBC World] Spain PM pins hopes on housing crisis to help win snap election
  > Calling of a snap election was not a knee-jerk reaction from Pedro Sánchez but a carefully thought-out manoeuvre, Guy Hedgecoe reports from Madrid.
- 2026-10-05 19:31 [France 24] Sanchez chose 'best moment in a sea of troubles' to call for snap election, analyst says
  > Spanish Prime Minister Pedro Sanchez on Monday called an early election for November 29, aiming to increase his parliamentary support after lawmakers last week rejected proposals to address a housing crisis that has drawn nationwide protests. Speaking with FRANCE 24's Mark Owen, Javier Carbonell, Po

## U085
**A** (6 item(s))
- 2026-10-05 09:44 [France 24] Nobel Prize in Medicine jointly awarded to ​Karl Deisseroth, Peter Hegemann ​and Georg Nagel
  > The Nobel Prize in Medicine was awarded Monday to Karl Deisseroth, Peter Hegemann and Georg Nagel for their research into light-gated ion channels and optogenetics. The prize money this year is 12 million Swedish kronor (about $1.2 million).
- 2026-10-05 09:45 [South China Morning Post] Nobel Medicine Prize awarded to 3 scientists for optogenetics development
  > The 2026 Nobel Prize season opened on Monday with the Medicine Prize being awarded to Karl Deisseroth, Peter Hegemann and Georg Nagel for their research into light-gated ion channels and optogenetics.
The prize was announced at the Karolinska Institute in Stockholm, kicking off Nobels week.
Their wo
- 2026-10-05 09:47 [France 24] 🔴 Nobel Prize in Medicine jointly awarded to ​Karl Deisseroth, Peter Hegemann ​and Georg Nagel
- 2026-10-05 10:10 [BBC World] Nobel Prize awarded for showing how nerve cells shape feelings
  > US psychiatrist and neurologist Karl Deisseroth and his German colleagues Peter Hegemann and Georg Nagel have been awarded for their work.
- 2026-10-05 14:18 [Al Jazeera] Nobel medicine prize honours US and German scientists for optogenetics work
  > The winners of the Nobel Prizes in physics, chemistry, literature, peace and ‌economics will be announced in the week.
- 2026-10-05 21:56 [France 24] Switching on brain cells: the Nobel-winning science of optogenetics
  > The Nobel medicine prize was awarded Monday to US psychiatrist and neurologist Karl Deisseroth and German scientists Peter Hegemann and Georg Nagel for their pioneering work in the neuroscience field of optogenetics. In optogenetics, scientists control neurones by stimulating them with light -- pote
**B** (3 item(s))
- 2026-10-05 11:51 [France 24 Español] Irán entrena a mujeres en las armas ante una posible invasión terrestre
  > En medio de las tensiones con Estados Unidos e Israel, Irán ha puesto en marcha programas de entrenamiento para civiles, incluidas numerosas mujeres, con el objetivo de prepararlas para responder ante una eventual invasión terrestre. En plazas y centros de entrenamiento de Teherán, las participantes
- 2026-10-05 14:49 [El País Internacional] Irán empieza a entrenar a voluntarios civiles para la “defensa nacional”
  > Voluntarias con rifles de asalto del tipo Kaláshnikov, en un curso de entrenamiento militar para civiles en la plaza Imán Hussein de Teherán, este domingo.
- 2026-10-05 15:47 [Europa Press Internacional] El presidente de Irán nombra a Mehrdad Ajlaqi nuevo ministro de Defensa
  > El presidente de Irán, Masud Pezeshkian, ha nombrado este lunes a Mehrdad Ajlaqi nuevo ministro de Defensa del país, por lo que la elección pasa ahora a manos del Parlamento para ser sometida a votación a medida que avanza el conflicto abierto en la región de Oriente Próximo a raíz de la ofensiva la

## U086
**A** (5 item(s))
- 2026-10-08 02:35 [Europa Press Internacional] Trump vuelve a hipotetizar sobre ataques iraníes en Los Ángeles y San Diego pese a la polémica generada
  > El presidente de Estados Unidos, Donald Trump, ha reiterado sus controvertidos comentarios acerca de hipotéticos bombardeos iraníes contra las ciudades de Los Ángeles y San Diego --ambas gobernadas por demócratas-- presentando tales eventos como "trauma", "problemas" o "espectáculo de terror" antes 
- 2026-10-08 04:57 [Il Sole 24 Ore Mondo] Guerra in Iran, ultime notizie. «Da Pentagono ordine alle forze armate Usa per eventuale ripresa degli attacchi»
- 2026-10-08 12:26 [El País Internacional] Dos asesores de Trump viajaron a Bosnia-Herzegovina para ayudar al prorruso Milorad Dodik a ganar las elecciones
  > Chris LaCivita, en el centro, viajaba en Estados Unidos junto a Donald Trump a bordo de su avión, conocido como Trump Force One, el lunes 13 de marzo de 2023.
- 2026-10-08 16:35 [Europa Press Internacional] Trump asegura que el Ejército de EEUU no atacará Irán "antes" de las elecciones del 3 de noviembre
  > El presidente de Estados Unidos, Donald Trump, ha asegurado este jueves que no ordenará "ningún" ataque contra Irán antes de las elecciones legislativas, previstas para el próximo 3 de noviembre, mientras las autoridades iraníes sostienen que responderán "en unos días" a la última propuesta de paz p
- 2026-10-08 17:52 [ANSA Mondo] Trump, 'non attaccheremo Iran prima delle midterm, colloqui produttivi con Teheran'
  > "Non attaccheremo l'Iran prima

delle elezioni di metà mandato". Lo afferma Donald Trump sul suo

social Truth, sottolineando che gli Stati Uniti stanno avendo

"discussioni produttive" con l'Iran.

Riproduzione riservata © Copyright ANSA
**B** (2 item(s))
- 2026-10-08 11:18 [BBC Mundo] Cómo llegó Colombia a tener una deuda tan alta (y por qué De la Espriella tendrá que aumentarla)
  > El presupuesto presentado por el gobierno de De la Espriella prevee que la deuda llegará a 66,2% del PIB en 2027, la más alta de la historia del país.
- 2026-10-08 18:55 [France 24 Español] Directo Latam y el apoyo de De la Espriella a exmilitares acusados por asesinato de Jovenel Moïse
  > El presidente colombiano, Abelardo de la Espriella, ha manifestado su apoyo jurídico a 17 exmilitares acusados del magnicidio de Jovenel Moïse en 2021, quienes fueron trasladados a Estados Unidos para comparecer ante la Justicia. En paralelo, el mandatario busca implementar su Estatuto Antiterrorist

## U087
**A** (10 item(s))
- 2026-10-04 21:31 [South China Morning Post] US Air Force removes all bombers from UK airbase targeted by suspected terror attack
  > The US Air Force has brought home its bombers stationed at a US-run military airbase in England used to strike Iran following an investigation into a planned terror attack at the RAF Fairford base.
The bombers were redeployed back to their home bases in the United States, according to a Pentagon off
- 2026-10-04 22:23 [Al Jazeera] US withdraws B-1 bomber aircraft from UK’s Fairford base amid Iran fears
  > The abrupt redeployment to the US comes after several &#039;terrorism-related&#039; arrests were made outside RAF Fairford.
- 2026-10-05 04:58 [BBC World] US air force removes all bombers from British military base RAF Fairford
  > A statement says all bombers deployed to RAF Fairford have been "re-deployed to their home stations" in the US.
- 2026-10-05 07:40 [Defense News] US removes B-1 bombers from UK base amid security concerns
  > NEW YORK — The United States removed its B-1 bombers from a U.K. air base one week after several men were arrested there on suspicion of preparing terrorist acts, a Pentagon official said on Sunday. A dozen B-1 bombers were stationed at RAF Fairford air base, located northwest of London. The planes 
- 2026-10-05 09:49 [France 24] US withdraws all bombers from UK base at centre of suspected terror attack
  > The United States has removed its B-1 bombers from a British air base one week after five men were arrested nearby on suspicion of preparing terrorist acts, a ‌suspected plot that British Prime Minister Andy Burnham said was likely backed by Iran. The planes had been ⁠stationed at RAF Fairford, whic
- 2026-10-05 11:09 [Al Jazeera] US abruptly withdraws bombers from UK’s RAF Fairford
  > The US has abruptly withdrawn all of its aircraft from the UK’s RAF Fairford, citing concerns about a potential attack.
- 2026-10-05 12:07 [BBC World] No10 insists UK military base RAF Fairford is safe after US withdraws bombers
  > US media reported a new threat led to the bombers being removed on Sunday, following an incident near the base last week.
- 2026-10-05 17:34 [Al Jazeera] Rubio: No direct link between US bombers removal and UK base incident
  > Rubio stresses US base security, following the removal of B-1 bombers amid alleged threats targeting UK military assets.
- 2026-10-05 19:58 [BBC World] Trump says 'threat' led US to pull bombers from RAF Fairford
  > The Pentagon confirmed on Sunday it had removed the B1 bombers from the base in England back to their home stations in America.
- 2026-10-05 21:40 [South China Morning Post] US bombers moved from UK airbase due to Iran-linked threats, Trump says
  > US President Donald Trump said on Monday that a threat linked to Iran ⁠had prompted the removal of American B-1 bombers from a British airbase.
The planes had been stationed at RAF Fairford, the preferred European base for US bombers, and had recently been used in US strikes on Iran. Last week, five
**B** (2 item(s))
- 2026-10-05 10:36 [Defense News] Missiles, satellites and warplanes — Ukraine, Europe advance key arms projects
  > WARSAW, Poland — Ukraine’s drone and missile maker Fire Point is developing an extended-range tactical ballistic missile after its FP-7 weapon was used in combat for the first time on Oct. 1, the company’s CEO Iryna Terekh said during this year’s Helsinki Security Forum.As European nations are braci
- 2026-10-05 12:26 [Kyiv Independent] New automatic gun turrets successfully down first Russian jet-powered drones, Air Force says
  > President Volodymyr Zelensky previously announced that twelve such turrets had been installed where Russian jet-powered drones have been particularly active, including around Kyiv.

## U088
**A** (3 item(s))
- 2026-10-04 13:18 [Kyiv Independent] Germany announces $1.46 billion in aid for Ukraine, including interceptor drones, air defense missiles
  > The package was announced by President Volodymyr Zelensky and German Chancellor Friedrich Merz at a joint press conference in Kyiv.
- 2026-10-04 16:38 [Al Jazeera] Germany’s Merz in Kyiv announces $1.5B in aid, urges Putin to end war
  > German Chancellor Friedrich Merz, on a surprise visit to Kyiv, announced $1.5 billion in military and reconstruction aid
- 2026-10-05 16:22 [Breaking Defense] Germany pledges $1.1B military aid package to Ukraine flush with drone interceptors
  > &#8220;Russia must know that we will take steps to defend ourselves against any further escalation,&#8221; said German Chancellor Friedrich Merz.
**B** (2 item(s))
- 2026-10-05 14:08 [South China Morning Post] France, Germany call for new weapon allowing ‘immediate cut off’ of China from EU market
  > In the strongest sign yet of a shifting European Union policy on China, the leaders of France and Germany have demanded a new trade weapon that would cut off access to the EU market when third countries cause severe distortions.
The tool would effectively act as a kill switch, allowing Brussels to r
- 2026-10-05 17:01 [France 24] France, Germany seek new EU rapid response tool against trade threats
  > France and Germany proposed a new legal tool to enable the EU to respond rapidly to trade wars or measures, such as dumping, that could economically harm the bloc. While French President Emmanuel Macron and German Chancellor Friedrich Merz said the proposal was not a direct response to the actions o

## U089
**A** (2 item(s))
- 2026-09-29 19:08 [South China Morning Post] China expands overseas military presence with new Laos air force centre
  > China has launched a rare air force support and training centre in Laos, the Ministry of Defence announced on Tuesday.
The China-Laos Joint Support and Training Centre and the China-Laos Friendship Aviation Academy are now in operation at the Ban Keun Airport, aiming to help the Laotian Air Force tr
- 2026-09-30 16:33 [Breaking Defense] China opens training center with Laos, marking third overseas military base
  > Satellite imagery shows the new facility is built in part on a purported old US airstrip used during the Vietnam War.
**B** (2 item(s))
- 2026-09-30 03:21 [South China Morning Post] US Supreme Court lets Trump resume deportations to third countries
  > The US Supreme Court on Tuesday let President Donald Trump’s administration continue swiftly deporting people to countries other than their own for now, while the justices consider whether the policy is legal.
The apparent 6-3 order temporarily lifts lower court requirements for migrants to get a ch
- 2026-10-01 17:35 [Al Jazeera] US Supreme Court agrees to take up Trump’s ICE detention policy
  > The case is the latest dispute over US President Donald Trump’s sweeping immigration crackdown.

## U090
**A** (7 item(s))
- 2026-10-03 23:35 [Rai News Esteri] Marea sociale contro il caro-affitti in Spagna: le piazze spingono Sánchez verso le urne
  > Ondata di proteste da Madrid a tutte le principali città per il diritto alla casa dopo lo sfratto dell'ottantasettenne Mari Carmen; il rifiuto dei decreti da parte delle destre e dei catalani di Junts apre lo scenario di elezioni anticipate
- 2026-10-04 17:28 [Rai News Esteri] Casa e scuola: il filo rosso che lega le proteste in Europa
  > In Spagna per il diritto alla casa, in Francia l'erosione allo studio accende lo scontento dei più giovani
- 2026-10-04 23:15 [Rai News Esteri] La Spagna in piazza per il diritto alla casa. E Sanchez pensa al voto anticipato
  > Centinaia di migliaia di persone al fianco delle proteste di Madrid per la casa, il governo bocciato in Parlamento valuta elezioni a fine novembre
- 2026-10-05 06:21 [Il Sole 24 Ore Mondo] Caro casa, prezzi e affitti salgono nell’Ue. Il Governo studia le misure per giovani e locazioni
  > «Serve una formazione di qualità, un lavoro sicuro e stabile, una retribuzione adeguata, una casa a un prezzo equo», ha detto di recente la premier Giorgia Meloni
- 2026-10-05 10:27 [Rai News Esteri] La Spagna al voto: i sondaggi premiano le destre, l'area progressista frammentata
  > Il partito popolare e Vox arriverebbero al 52%, secondo un sondaggio per El Pais. Ma le rilevazioni sono state realizzate prima della crisi di governo e della bocciatura dei decreti presentati da Sanchez
- 2026-10-05 19:05 [Il Sole 24 Ore Mondo] Sanchez sfida le destre: Spagna al voto anticipato
  > Dopo la bocciatura sul piano casa, il premier socialista convoca le elezioni cavalcando le proteste di piazza: «Serve una maggioranza progressista per nuovi progressi sociali»
- 2026-10-05 21:04 [Rai News Esteri] Migliaia di persone a Barcellona in piazza per il diritto alla casa
  > Dopo Madrid e Valencia anche Barcellona stasera è scesa in piazza all'annuncio di elezioni anticipate, in migliai hanno sfilato per difendere il diritto alla casa
**B** (5 item(s))
- 2026-10-04 23:23 [Clarín Mundo] Alerta en Rusia: murió una científica por un accidente con bacterias en un laboratorio y debieron aislar a 200 personas
  > Contó que se le rompió un tubo de ensayo recolectando muestras para analizar.Autoridades rusas dicen que el frío impediría la transmisión de un tipo de neumonía.Los funcionarios hablan de "una peste no especificada" y "una infección particularmente peligrosa".
- 2026-10-05 06:53 [Europa Press Internacional] Rusia asegura que la situación epidemiológica en Irkutsk es "estable" tras un supuesto accidente en un laboratorio
  > Las autoridades de Rusia han asegurado que la situación epidemiológica en la región de Irkutsk es "estable", después de activar una serie de medidas de emergencia durante los últimos días a causa de la muerte de una investigadora en un presunto accidente de laboratorio en Shelejov.
- 2026-10-05 10:17 [El País Internacional] Rusia pone bajo observación a cientos de personas tras morir una investigadora de un laboratorio contra la peste
  > Trabajos de desinfección de coranavirus en la estación de tren de Yaroslavsky en Moscú, el 10 de noviembre de 2022.
- 2026-10-05 14:34 [Europa Press Internacional] EEUU pide a Rusia compartir información "de forma rápida y transparente" tras supuesto caso de peste en Irkutsk
  > El Departamento de Estado estadounidense ha instado este lunes a las autoridades de Rusia a compartir información "de forma rápida y transparente" sobre el caso de presunta peste pulmonar en la región de Irkutsk, tras la muerte de una investigadora en un presunto accidente de laboratorio en Shelejov
- 2026-10-05 21:21 [BBC Mundo] EE.UU. "sigue de cerca" el caso de una científica rusa que falleció en un centro de investigación de la peste en Siberia
  > El secretario de Estado, Marco Rubio, expresó su preocupación de que el incidente pudiera haber provocado la propagación de la peste neumónica, aunque señaló que no había motivos para alarmarse.

## U091
**A** (10 item(s))
- 2026-10-08 00:00 [Al Jazeera] Yemen war live: Gov’t forces claim key heights, Houthi attacks continue
  > Saudi-backed Yemeni forces claim advances in western Taiz&#039;s mountain belt overlooking the coast.
- 2026-10-08 00:16 [Al Jazeera] Saudi Arabia confirms three dead in Houthi strikes on its airports
  > Saudi Arabia has confirmed that Houthi strikes on two of its international airports have killed three people.
- 2026-10-08 01:02 [Al Jazeera] Yemeni government forces claim 1,860 Houthis ‘neutralised’
  > Yemeni government forces said in a social media post that they carried out 2,103 &#039;precise targeting operations&#039;.
- 2026-10-08 01:54 [South China Morning Post] Houthi strikes on Saudi airports leave 3 dead, dozens wounded
  > Saudi authorities said Wednesday that three people were killed in attacks on two of the kingdom’s international airports, including in the capital Riyadh, after Yemen’s Houthis claimed to have fired on both transport hubs.
The Iran-backed fighters earlier took responsibility for a flurry of attacks 
- 2026-10-08 03:02 [France 24] Saudi Arabia says it will retaliate after deadly Houthi attacks on airports
  > Saudi authorities said Wednesday three people were killed and 36 wounded in attacks on Abha and Riyadh’s King Khalid international airports claimed by Yemen’s Iran-backed Houthis. The Saudi-led coalition said it destroyed the ballistic missile launch platform used to attack Riyadh, as fighting with 
- 2026-10-08 03:32 [BBC World] Three people killed in Houthi attacks on Saudi Arabia airports, officials say
  > The Houthis have claimed responsibility for the attacks, which mark an escalation in the conflict.
- 2026-10-08 06:50 [Al Jazeera] Yemen’s government needs tribes to defeat the Houthis. Will they join?
  > Yemen&#039;s tribes could prove crucial to government&#039;s fight against the Houthis, but many may wait before choosing sides.
- 2026-10-08 09:55 [France 24] Houthis claim new attack on Riyadh airport as fighting continues in Yemen
  > Yemen's Houthi rebels said Thursday they had struck Riyadh airport with another ballistic missile as Saudi authorities said three people were killed and 36 wounded in previous Houthi strikes on Riyadh and Abha international airports earlier this week. The Saudi-led coalition said it destroyed 82 Hou
- 2026-10-08 12:52 [France 24] Conflict in Yemen: What are the Houthis’ aims?
  > Saudi authorities said Wednesday three people were killed in attacks on two of the kingdom's international airports, including in the capital Riyadh, after Yemen's Houthis claimed to have fired on both transport hubs. The Iran-backed Houthis have claimed a wave of attacks on Saudi civilian infrastru
- 2026-10-08 14:43 [Al Jazeera] Saudi-led coalition says it intercepts three Houthi ballistic missiles
  > Houthi military spokesman claims Yemeni group fired one ballistic missile towards airport in Saudi capital, Riyadh.
**B** (5 item(s))
- 2026-10-08 01:15 [Al Jazeera] Death of 87-year old sparks furious Spain housing protests
  > Hundreds of protesters gather outside Spain’s Parliament, demanding action over soaring rents.
- 2026-10-08 09:56 [France 24] Anger mounts in Spain as woman whose eviction ignited housing protests dies
  > Maricarmen ​Abascal, the 87-year-old Spanish woman whose dramatic eviction last month sparked mass housing protests that led to an early election, has died, the Madrid tenants' union said on Wednesday, as thousands demonstrated over her death. France 24's correspondent in Madrid Sarah Morris has the
- 2026-10-08 10:35 [France 24] Evicted pensioner Maricarmen, symbol of Spain's housing crisis, dies at 87
  > PRESS REVIEW – Thursday, October 8: Maricarmen, the evicted Spanish pensioner who became the face of Spain's housing crisis, dies in hospital. Also, France braces for "Act Four" of high school student protests against dilapidated schools and poor staff presence. Finally, actress Zendaya sparks a row
- 2026-10-08 10:48 [Al Jazeera] Photos: Protests erupt after 87-year-old evicted woman dies in Madrid
  > Nationwide outrage grows after the death of woman whose eviction sparked protests and political tensions.
- 2026-10-08 11:54 [France 24] Maricarmen, the 87-year-old woman whose eviction shook Spain, dies
  > María del Carmen Abascal, the 87-year-old woman whose eviction from her longtime Madrid home sparked nationwide protests across Spain and unleashed a political crisis, died on Wednesday while hospitalised.

## U092
**A** (2 item(s))
- 2026-10-07 22:27 [France 24] DNC sues Trump administration over taxpayer-funded TV ads promoting president
  > The Democratic National Committee sued President Donald Trump’s administration on Wednesday over taxpayer-funded television ads promoting his political message, alleging illegal government propaganda. The lawsuit seeks to halt federal funding for the ads, which have cost more than $12 million to air
- 2026-10-08 01:21 [Al Jazeera] Democrats sue US President Trump over taxpayer-funded ad campaign
  > Trump has faced a bipartisan backlash over ads that critics say violate prohibitions on taxpayer-funded propaganda.
**B** (3 item(s))
- 2026-10-08 16:48 [South China Morning Post] UK Ministry of Defence patrols arrest 2 Latvians near RAF base
  > UK Ministry of Defence security patrols arrested two Latvian men near an RAF (Royal Air Force) base that houses US and Nato intelligence operations, police said on Thursday.
The base, RAF Molesworth, 112km (70 miles) north of London, is operated by the US Air Force and includes intelligence staff fr
- 2026-10-08 16:57 [France 24] Two Latvian men arrested at UK base housing US and NATO intelligence hubs
  > British ​counter-terrorism police are investigating after two Latvian men were arrested Thursday near a Royal Air Force ​base in southeast England housing US and NATO intelligence operations, police said in a statement. The arrests come days after a major incident at another UK base led the US milit
- 2026-10-08 18:01 [Al Jazeera] Two Latvian men arrested inside UK military base after breach
  > Police say nothing so far suggests the incident at RAF Molesworth linked ​to events surrounding RAF Fairford last month.

## U093
**A** (2 item(s))
- 2026-10-07 23:45 [Al Jazeera] EU-China trade talks begin in Beijing amid escalating pressure
  > Talks will focus on the €1bn daily deficit and rare earth export restrictions.
- 2026-10-08 03:00 [South China Morning Post] As China and the EU begin crunch trade talks, optimism is in short supply
  > As China and the European Union began a fresh round of trade talks in Beijing on Thursday, observers on both sides appeared to agree on one thing: a big breakthrough was unlikely.
Chinese firms based in Europe said they hoped the talks could achieve some “limited progress” to help stabilise the trad
**B** (6 item(s))
- 2026-10-08 00:56 [Europa Press Internacional] Maduro y Flores podrían ser acusados este jueves de haber torturado a estadounidenses venezolanos
  > El presidente de Venezuela, Nicolás Maduro, y su esposa, Cilia Flores, podrían ser acusados por estar vinculados a delitos de tortura contra ciudadanos estadounidenses que estuvieron bajo custodia de su gobierno en los últimos años, ha informado la prensa estadounidense.
- 2026-10-08 14:52 [Clarín Mundo] Torturas: Estados Unidos suma una nueva acusación contra Nicolás Maduro
  > El derrocado presidente de Venezuela ya enfrenta delitos de narcotráfico.Maduro y su esposa, Cilia Flores, permanecen tras las rejas en Nueva York desde principios de enero.
- 2026-10-08 15:13 [France 24 Español] EE. UU. suma a Maduro y Cilia Flores un cargo por conspiración para torturar a opositores
- 2026-10-08 15:20 [El País Internacional] Nicolás Maduro y Cilia Flores, acusados en EE UU de nuevos cargos de tortura y represión
  > Ilustración de Nicolás Maduro y Cilia Flores en el tribunal de Nueva York, en julio.
- 2026-10-08 15:21 [BBC Mundo] Presentan nuevos cargos contra Maduro y su esposa por presuntas torturas a ciudadanos de estadounidenses ante un tribunal de Nueva York
  > El expresidente de Venezuela y su esposa fueron acusados por el Departamento de Justicia de EE.UU. de haber participado en la tortura de estadounidenses detenidos en Caracas.
- 2026-10-08 15:32 [Europa Press Internacional] EEUU imputa a Maduro y su esposa por liderar un sistema de represión y torturas en Venezuela
  > La Fiscalía de Estados Unidos ha imputado este jueves al presidente de Venezuela, Nicolás Maduro, y su esposa, Cilia Flores, por delitos de tortura contra personas detenidas, incluyendo ciudadanos estadounidenses, en el marco de un "sistema de represión que recurría a la violencia contra la oposició

## U094
**A** (7 item(s))
- 2026-10-03 23:35 [Rai News Esteri] Marea sociale contro il caro-affitti in Spagna: le piazze spingono Sánchez verso le urne
  > Ondata di proteste da Madrid a tutte le principali città per il diritto alla casa dopo lo sfratto dell'ottantasettenne Mari Carmen; il rifiuto dei decreti da parte delle destre e dei catalani di Junts apre lo scenario di elezioni anticipate
- 2026-10-04 17:28 [Rai News Esteri] Casa e scuola: il filo rosso che lega le proteste in Europa
  > In Spagna per il diritto alla casa, in Francia l'erosione allo studio accende lo scontento dei più giovani
- 2026-10-04 23:15 [Rai News Esteri] La Spagna in piazza per il diritto alla casa. E Sanchez pensa al voto anticipato
  > Centinaia di migliaia di persone al fianco delle proteste di Madrid per la casa, il governo bocciato in Parlamento valuta elezioni a fine novembre
- 2026-10-05 06:21 [Il Sole 24 Ore Mondo] Caro casa, prezzi e affitti salgono nell’Ue. Il Governo studia le misure per giovani e locazioni
  > «Serve una formazione di qualità, un lavoro sicuro e stabile, una retribuzione adeguata, una casa a un prezzo equo», ha detto di recente la premier Giorgia Meloni
- 2026-10-05 10:27 [Rai News Esteri] La Spagna al voto: i sondaggi premiano le destre, l'area progressista frammentata
  > Il partito popolare e Vox arriverebbero al 52%, secondo un sondaggio per El Pais. Ma le rilevazioni sono state realizzate prima della crisi di governo e della bocciatura dei decreti presentati da Sanchez
- 2026-10-05 19:05 [Il Sole 24 Ore Mondo] Sanchez sfida le destre: Spagna al voto anticipato
  > Dopo la bocciatura sul piano casa, il premier socialista convoca le elezioni cavalcando le proteste di piazza: «Serve una maggioranza progressista per nuovi progressi sociali»
- 2026-10-05 21:04 [Rai News Esteri] Migliaia di persone a Barcellona in piazza per il diritto alla casa
  > Dopo Madrid e Valencia anche Barcellona stasera è scesa in piazza all'annuncio di elezioni anticipate, in migliai hanno sfilato per difendere il diritto alla casa
**B** (2 item(s))
- 2026-10-04 18:17 [South China Morning Post] Dozens detained at a rally in Moscow held by Kremlin-friendly Communist Party, party says
  > Police in Moscow detained about 60 people at a rally on Sunday held by Russia’s Kremlin-friendly Communist Party, the party said.
The party said in a statement that the detentions happened as the rally was ending and that its Moscow branch was working to get those who were detained – mostly young pe
- 2026-10-04 23:30 [Kyiv Independent] Dozens detained at authorized Russian Communist Party rally after chants of 'Down with the Tsar'
  > The event had been authorized by Moscow authorities, but detentions reportedly intensified as the rally was ending and participants shifted toward more directly anti-Kremlin slogans.

## U095
**A** (14 item(s))
- 2026-10-07 12:00 [UN News] Ukraine: UN condemns latest attacks and calls for civilian protection
  > The UN Humanitarian Coordinator for Ukraine on Wednesday&nbsp;called for an end to attacks against civilians following further overnight strikes by Russian forces that reportedly killed at least 19 in the Chernihiv Region.
- 2026-10-08 07:26 [Kyiv Independent] General Staff: Russia has lost 1,547,780 troops in Ukraine since Feb. 24, 2022
  > The number includes 1,880 casualties that Russian forces suffered over the past day.
- 2026-10-08 09:12 [Kyiv Independent] At least 12 dead after Russian glide bomb strikes Kramatorsk bus stop
  > "Russia comes to the Ukrainian land with death," Donetsk Governor Vadym Filashkin said.
- 2026-10-08 09:54 [Kyiv Independent] Russian drone barrage on Kyiv kills 3, injures 13, disrupts electricity, water supplies
  > At 10:00 a.m. local time, Ukraine’s biggest private energy firm DTEK announced emergency energy shutdowns in Brovary, Buchanskyi, Vyshgorod, and Boryspil districts of the capital.
- 2026-10-08 10:08 [France 24] Dozens killed in Russian strike on buses in Ukraine's Kramatorsk as Kyiv targets data centre
  > At least 30 people were killed in a Russian strike on two buses in the Ukrainian city of Kramatorsk in the eastern Donetsk region on Thursday. Earlier, a drone hit a data centre belonging to Russian technology company Yandex, causing a fire.
- 2026-10-08 10:16 [BBC World] Russian strike on buses kills 33, say officials, as deadly attacks on Ukraine surge
  > Ukraine accused Russia of targeting the crowded bus in the frontline city to kill as many civilians as possible.
- 2026-10-08 10:31 [Al Jazeera] Russian attack on Ukraine’s Kramatorsk kills at least 12 people
  > Fourteen people were wounded in the Russian strike on city in eastern Ukraine&#039;s Donetsk region, local authorities say.
- 2026-10-08 11:43 [Kyiv Independent] Russian strikes kill at least 10, injure 45 across Ukraine over past day
  > Russia attacked across Ukraine with 142 Shahed-type drones, 82 of which were jet-powered overnight on Oct. 8, Ukraine's Air Force said.
- 2026-10-08 12:00 [South China Morning Post] At least 33 dead in Russian bomb blast in east Ukraine stronghold
  > A ⁠Russian bomb attack on ⁠the eastern Ukrainian city of Kramatorsk ⁠killed at least 33 people, authorities said on Thursday, describing it as a targeted strike on civilians in the key stronghold sought by Moscow.
Another 18 people were wounded in one of the largest single attacks this year, ‌which 
- 2026-10-08 13:44 [France 24] 30 dead in strike on Ukraine bus as Russian attacks intensify
  > Thirty people were killed and at least 18 were injured by Russian strikes in eastern Ukraine that included an attack on a public bus, authorities said Thursday, as an intensive pre-winter wave of attacks continued.
- 2026-10-08 14:50 [Al Jazeera] More killed in Kramatorsk as Russia targets Ukraine’s transportation system
  > Russia’s attacks on trains, buses and ports are paralysing Ukraine’s transport network and endangering civilians.
- 2026-10-08 17:07 [Al Jazeera] Dozens killed in Russian strike on civilian buses in eastern Ukraine
  > At least 33 people were killed after a Russian strike hit two civilian buses in a city within the Donestsk region.
- 2026-10-08 17:11 [France 24] Russian attack on Ukraine busses part of 'a steady increase in attacks on civilians'
  > Ukrainian President Volodymyr Zelensky said Thursday there would be a response to a Russian strike that hit two buses in the frontline city of Kramatorsk, killing 30 people and wounding 18 others. France 24's Andrew Hilliar says it comes a bid a growing number of Russian attacks on civilians in the 
- 2026-10-08 17:55 [Kyiv Independent] Ukraine war latest: Russian glide bomb strikes in Kramatorsk kill at least 33
  > Key developments on Oct. 8:At least 33 dead after Russian glide bomb strikes Kramatorsk busesRussian drone barrage on Kyiv kills 4, injures 19, disrupts electricity, water suppliesPolish SIM cards found in Russian drones downed in PolandUS, Russia confirm Trump&apos;s latest Ukraine peace push is
**B** (2 item(s))
- 2026-10-08 03:41 [BBC World] Veteran Indian actor Nana Patekar dies at 75
  > Known for his intense performances, Patekar carved out a distinctive place in Indian cinema.
- 2026-10-08 06:30 [Al Jazeera] Acclaimed Indian actor Nana Patekar dies aged 75
  > Patekar won three National Film Awards and received the Padma Shri, one of the country&#039;s highest civilian honours.

## U096
**A** (11 item(s))
- 2026-10-04 03:42 [BBC World] 'Anger in the streets': Tens of thousands protest in Spain over housing crisis
  > More than 50 protests took place on Saturday after the government failed to get emergency legislation through parliament.
- 2026-10-05 08:21 [Rai News Esteri] La protesta degli studenti a Parigi: in fiamme il portone di un liceo, sassaiola contro gli agenti
  > I liceali hanno affrontato la polizia sparando fuochi d'artificio
- 2026-10-05 12:02 [ANSA Mondo] Ségolène Royal denuncia la 'repressione' degli studenti in Francia
  > 'I govani bisogna amarli, non picchiarli.Se scompare l'empatia la barbarie non è distante'
- 2026-10-05 13:50 [France 24 Español] Más de 400 colegios bloqueados en Francia en la segunda semana de protestas estudiantiles
  > Al menos 413 institutos de secundaria en Francia se paralizaron el lunes debido a la prolongación de las protestas estudiantiles, según el Ministerio de Educación. Los manifestantes piden más profesores, una mejora de las infraestructuras y una reducción de la jornada escolar. El martes está convoca
- 2026-10-05 13:54 [Rai News Esteri] La protesta degli studenti in Francia, a Parigi vetrine dei negozi prese d'assalto dai manifestanti
  > Cassonetti rovesciati, sassaiole contro la polizia, fumogeni e cori intonati per strada: lo scenario delle proteste dei liceali francesi nella capitale
- 2026-10-05 14:37 [France 24 Español] Directo París y el panorama de las protestas estudiantiles en Francia
  > Francia vive una de las mayores olas de protestas estudiantiles de los últimos años. Aunque el ambiente se encuentra más tranquilo, cerca de 400 escuelas permanecen cerradas y en algunas ciudades se han presentado disturbios. El primer ministro Lecornu presentó una hoja de ruta para abordar la situa
- 2026-10-05 17:26 [ANSA Mondo] Gli studenti tornano in piazza, la Francia teme il caos generale
  > Gli studenti tornano in piazza in tutta la Francia e crescono i timori che le nuove manifestazioni posano innesecare un caos generale. La situazione alla vigilia del 'terzo atto' della protesta dei liceali, ormai appoggiati anche dai colleghi di diverse universitrà, è apparsa incandescente. A poco s
- 2026-10-05 17:31 [France 24 Español] Francia: más de 400 escuelas permanecen cerradas mientras continúan las protestas estudiantiles
  > Las protestas estudiantiles continúan en Francia, donde cientos de escuelas e institutos se han visto afectados por bloqueos y movilizaciones. Los estudiantes denuncian la falta de profesores, las aulas masificadas, el deterioro de las condiciones de aprendizaje y de las infraestructuras. Ante la cr
- 2026-10-05 17:45 [El País Internacional] Francia encara una nueva semana de protestas estudiantiles, las mayores en décadas
  > Estudiantes franceses de secundaria se manifiestan frente al instituto Sophie Germain de París este lunes.
- 2026-10-05 17:53 [Il Sole 24 Ore Mondo] Francia, allarme governatore banca centrale: «Strozzati dai tassi»
  > Se la Francia non adotta un piano di bilancio in grado di ridurre la spesa e il deficit rischia di vedersi “progressivamente strangolare dal rialzo dei tassi di interesse”. È...
- 2026-10-05 18:28 [Rai News Esteri] Protesta studenti, oltre 5.000 fermi. Domani il corteo a Parigi con i sindacati
  > Nonostante le dure contestazioni subite dagli studenti, il ministro dell'Educazione nazionale Édouard Geffray ha definito "legittima" la mobilitazione nazionale prevista per domani, pur condannando fermamente le violenze
**B** (2 item(s))
- 2026-10-04 22:36 [Al Jazeera] Nicaragua says it will withdraw from Central American Parliament
  > The Central American country&#039; crackdown on human rights has left it increasingly isolated in Latin America.
- 2026-10-05 09:37 [ANSA Mondo] Il Nicaragua ha deciso di ritirarsi dal Parlamento centroamericano
  > Il Paese guidato da Ortega e Murilo sempre più isolato internazionalmente

## U097
**A** (3 item(s))
- 2026-09-30 18:01 [Al Jazeera] Trump set to announce $200bn in energy investments from South Korea
  > The investments come as Trump seeks to tout the Republican Party&#039;s economic record ahead of the US midterm races.
- 2026-10-01 01:44 [South China Morning Post] Trump touts US$200 billion South Korean energy deal ahead of US midterms
  > US President Donald Trump has announced US$200 billion in energy investments from South Korea, including US$54 billion towards a long-discussed liquefied natural gas project in Alaska and more than US$100 billion in planned longer-term nuclear power investments.
Besides the Alaska LNG project and pi
- 2026-10-01 10:36 [South China Morning Post] South Korea hits back at Trump’s investment claims in ‘tit-for-tat move’
  > US President Donald Trump’s unilateral announcement of a “colossal” South Korean investment package has prompted Seoul to clarify that the deal is far from finalised, laying bare stark differences between the allies over the terms of their trade agreement, observers have said.
On Wednesday, Trump an
**B** (6 item(s))
- 2026-10-02 01:23 [Al Jazeera] Trump says US may ask Europe to release diesel reserves
  > Skyrocketing diesel prices have pushed Washington to weigh an export ban, raising alarm across European economies.
- 2026-10-02 05:26 [BBC World] US pressures Europe over diesel reserves as Trump threatens export ban
  > President Donald Trump has threatened to ban diesel exports in a bid to ease prices in the US ahead of the November elections.
- 2026-10-02 13:16 [Al Jazeera] Trump vs Europe as US presses for release of emergency diesel stocks
  > Europe&#039;s leaders are mulling proposals to respond to Trump&#039;s diesel demands.
- 2026-10-02 14:51 [South China Morning Post] G7 nations agree to release diesel and oil stocks after Trump pressure
  > Group ⁠of Seven countries agreed on Friday to release 100 million barrels of diesel and crude oil from emergency reserves and pledged to refrain from energy export restrictions after pressure from US President Donald Trump.
The US led a pressure campaign on the European Union to draw down emergency 
- 2026-10-02 19:01 [Al Jazeera] Trump says Europe agreed to release ‘massive amount’ of diesel reserves
  > US President Donald Trump says Europe agreed to release a ‘massive amount’ of diesel from emergency stockpiles.
- 2026-10-02 20:25 [BBC World] G7 to release 100 million barrels of oil and diesel after Trump export ban threat
  > The co-ordinated release is aimed at heading off further price spikes and avoiding a ban on US diesel exports.

## U098
**A** (2 item(s))
- 2026-09-29 20:25 [BBC World] Former American Idol contestant and pastor found guilty of murdering wife
  > Caleb Flynn shot his wife, Ashley, dead in their Ohio home in February before saying in a 9/11 call she was killed by burglars.
- 2026-09-30 10:35 [Al Jazeera] Former American Idol contestant found guilty of murdering wife
  > Former American Idol contestant found guilty of murdering wife
**B** (14 item(s))
- 2026-09-29 23:39 [BBC World] US Supreme Court denies Christa Pike's last-ditch bid to halt execution
  > The Tennessee inmate has been awaiting execution since she was sentenced to death in 1996 for the murder of a teenage classmate.
- 2026-09-30 13:14 [Al Jazeera] Christa Pike seeks firing squad, not lethal injection: Inside US executions
  > Women make up about 1 percent of US executions. How do states put people to death, and why is it contested?
- 2026-09-30 15:29 [BBC World] Execution of US murderer Christa Pike halted shortly before it was due to happen
  > Pike was convicted and sentenced to death in 1996 for the murder of Colleen Slemmer.
- 2026-09-30 16:00 [South China Morning Post] US Tennessee’s first execution of a woman in 200 years halted
  > A US appeal court on Wednesday halted the ⁠execution of death row inmate Christa Pike in Tennessee, less than two hours before she was scheduled to become the first woman that state has put to death in more than 200 years.
The 6th US Circuit Court of Appeals ordered a “short stay of execution” to gi
- 2026-09-30 16:44 [Al Jazeera] US appeals court halts Tennessee execution of Christa Pike
  > Christa Pike was set to become the first woman executed by Tennessee in more than 200 years.
- 2026-09-30 23:42 [BBC World] US Supreme Court allows execution of Christa Pike to go ahead
  > The death by lethal injection was scheduled to happen earlier on Wednesday before judges from a lower court paused the execution.
- 2026-10-01 02:35 [Al Jazeera] Christa Pike’s execution by lethal injection fails in Tennessee
  > Witnesses say Tennessee officials were unable to execute Christa Pike after a lethal injection attempt.
- 2026-10-01 04:14 [South China Morning Post] Tennessee halts executions after Christa Pike survives 2 doses of lethal drug
  > Tennessee officials were unable to put Christa Pike to death on Wednesday for a 1995 murder after administering two doses of a lethal drug. A death penalty expert said it was an unprecedented failure, and Tennessee’s governor halted the remaining execution for the rest of the year.
Pike, 50, was ali
- 2026-10-01 04:55 [Al Jazeera] Execution of US woman Christa Pike fails after botched lethal injection
  > The high-profile execution of murderer Christa Pike is in disarray after two lethal injections failed to kill her.
- 2026-10-01 16:45 [BBC World] Tennessee halts executions after Christa Pike survives two lethal injection attempts
  > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
- 2026-10-02 03:02 [South China Morning Post] Christa Pike in ‘life-saving care’ after botched Tennessee execution
  > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from a prison execution c
- 2026-10-02 07:58 [Al Jazeera] Lawyers for US inmate who survived lethal injections demand release
  > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
- 2026-10-02 20:32 [BBC World] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say
  > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.
- 2026-10-02 20:57 [Al Jazeera] Christa Pike unconscious, on ventilator after botched execution: Lawyers
  > The Tennessee woman&#039;s legal team says doctors are working to clear doses of the drug pentobarbital from her system.

## U099
**A** (14 item(s))
- 2026-09-29 23:39 [BBC World] US Supreme Court denies Christa Pike's last-ditch bid to halt execution
  > The Tennessee inmate has been awaiting execution since she was sentenced to death in 1996 for the murder of a teenage classmate.
- 2026-09-30 13:14 [Al Jazeera] Christa Pike seeks firing squad, not lethal injection: Inside US executions
  > Women make up about 1 percent of US executions. How do states put people to death, and why is it contested?
- 2026-09-30 15:29 [BBC World] Execution of US murderer Christa Pike halted shortly before it was due to happen
  > Pike was convicted and sentenced to death in 1996 for the murder of Colleen Slemmer.
- 2026-09-30 16:00 [South China Morning Post] US Tennessee’s first execution of a woman in 200 years halted
  > A US appeal court on Wednesday halted the ⁠execution of death row inmate Christa Pike in Tennessee, less than two hours before she was scheduled to become the first woman that state has put to death in more than 200 years.
The 6th US Circuit Court of Appeals ordered a “short stay of execution” to gi
- 2026-09-30 16:44 [Al Jazeera] US appeals court halts Tennessee execution of Christa Pike
  > Christa Pike was set to become the first woman executed by Tennessee in more than 200 years.
- 2026-09-30 23:42 [BBC World] US Supreme Court allows execution of Christa Pike to go ahead
  > The death by lethal injection was scheduled to happen earlier on Wednesday before judges from a lower court paused the execution.
- 2026-10-01 02:35 [Al Jazeera] Christa Pike’s execution by lethal injection fails in Tennessee
  > Witnesses say Tennessee officials were unable to execute Christa Pike after a lethal injection attempt.
- 2026-10-01 04:14 [South China Morning Post] Tennessee halts executions after Christa Pike survives 2 doses of lethal drug
  > Tennessee officials were unable to put Christa Pike to death on Wednesday for a 1995 murder after administering two doses of a lethal drug. A death penalty expert said it was an unprecedented failure, and Tennessee’s governor halted the remaining execution for the rest of the year.
Pike, 50, was ali
- 2026-10-01 04:55 [Al Jazeera] Execution of US woman Christa Pike fails after botched lethal injection
  > The high-profile execution of murderer Christa Pike is in disarray after two lethal injections failed to kill her.
- 2026-10-01 16:45 [BBC World] Tennessee halts executions after Christa Pike survives two lethal injection attempts
  > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
- 2026-10-02 03:02 [South China Morning Post] Christa Pike in ‘life-saving care’ after botched Tennessee execution
  > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from a prison execution c
- 2026-10-02 07:58 [Al Jazeera] Lawyers for US inmate who survived lethal injections demand release
  > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
- 2026-10-02 20:32 [BBC World] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say
  > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.
- 2026-10-02 20:57 [Al Jazeera] Christa Pike unconscious, on ventilator after botched execution: Lawyers
  > The Tennessee woman&#039;s legal team says doctors are working to clear doses of the drug pentobarbital from her system.
**B** (6 item(s))
- 2026-10-02 01:23 [Al Jazeera] Trump says US may ask Europe to release diesel reserves
  > Skyrocketing diesel prices have pushed Washington to weigh an export ban, raising alarm across European economies.
- 2026-10-02 05:26 [BBC World] US pressures Europe over diesel reserves as Trump threatens export ban
  > President Donald Trump has threatened to ban diesel exports in a bid to ease prices in the US ahead of the November elections.
- 2026-10-02 13:16 [Al Jazeera] Trump vs Europe as US presses for release of emergency diesel stocks
  > Europe&#039;s leaders are mulling proposals to respond to Trump&#039;s diesel demands.
- 2026-10-02 14:51 [South China Morning Post] G7 nations agree to release diesel and oil stocks after Trump pressure
  > Group ⁠of Seven countries agreed on Friday to release 100 million barrels of diesel and crude oil from emergency reserves and pledged to refrain from energy export restrictions after pressure from US President Donald Trump.
The US led a pressure campaign on the European Union to draw down emergency 
- 2026-10-02 19:01 [Al Jazeera] Trump says Europe agreed to release ‘massive amount’ of diesel reserves
  > US President Donald Trump says Europe agreed to release a ‘massive amount’ of diesel from emergency stockpiles.
- 2026-10-02 20:25 [BBC World] G7 to release 100 million barrels of oil and diesel after Trump export ban threat
  > The co-ordinated release is aimed at heading off further price spikes and avoiding a ban on US diesel exports.

## U100
**A** (3 item(s))
- 2026-10-07 22:50 [BBC World] Former Venezuelan President Nicolás Maduro expected to face more charges this week
  > The new charges are expected to accuse Maduro and his wife of playing a role in the torture of Americans in Venezuelan prisons, US media reports.
- 2026-10-08 15:07 [BBC World] Venezuela's ex-leader Nicolás Maduro charged with conspiracy to commit torture
  > The new accusations relate to the alleged torture of US citizens held in Venezuela while Maduro was in power.
- 2026-10-08 15:20 [Al Jazeera] Venezuela’s Nicolas Maduro and his wife charged over torture allegations
  > The new US charge adds to the existing drug trafficking case against Venezuela’s former president and first lady.
**B** (2 item(s))
- 2026-10-08 08:06 [State Department] Secretary of State Marco Rubio Remarks to the Press
  > Marco Rubio, Secretary of State
Athens, Greece
Athens International Airport



	

		
		

			

		

		

			

				
				

					
						Secretary of State Marco Rubio Remarks to the Press
					
				

				

					

					
					
						Remarks

					
					
					
			

			
			

			
			October 8, 2026

			
				


- 2026-10-08 13:38 [Al Jazeera] Rubio praises nationalism and ties ‘America First’ values to ancient Greece
  > US Secretary of State Marco Rubio urged Western nations to prioritise their own interests in a speech in Athens.

## U101
**A** (14 item(s))
- 2026-10-04 11:15 [Al Jazeera] Brazil votes in deeply polarised election pitting Lula against Bolsonaro
  > Close race expected as left-wing leader Lula seeks fourth nonconsecutive term against right-wing Flavio Bolsonaro.
- 2026-10-04 17:48 [South China Morning Post] Brazilians head to polls in high-stakes, polarised election
  > Brazilians queued to vote on Sunday in the first round of a tight election, following a campaign dominated by corruption scandals, economic anxiety and accusations of US meddling.
The field of 13 candidates has been led by two clear front runners – leftist President Luiz Inacio Lula da Silva, 80, wh
- 2026-10-04 21:11 [BBC World] Polls close in Brazil as Lula and Flávio Bolsonaro remain neck and neck
  > If no candidate gets more than 50% of the vote, the election will go to a run-off on 25 October.
- 2026-10-05 00:27 [DW World] Brazil election: Bolsonaro and Lula head to runoff
  > Populist Flavio Bolsonaro has secured a thin lead over incumbent Luiz Inacio Lula da Silva, but the next president of Brazil will be decided in the runoff round, according to the country’s electoral court.
- 2026-10-05 03:16 [BBC World] Right-wing Flávio Bolsonaro wins first round of Brazil election
  > With neither candidate getting more than 50% of the vote, the election will go to a run-off on 25 October.
- 2026-10-05 04:51 [BBC World] Watch: How Brazil's dramatic election unfolded
  > Millions of Brazilians took to the polls on Sunday for the first round of the country's presidential elections.
- 2026-10-05 05:08 [Al Jazeera] Bolsonaro beats expectations in Brazil vote, faces Lula in runoff
  > Brazil’s presidential election is heading to a run-off after Bolsonaro and Lula both fell short of the 50% needed to win
- 2026-10-05 09:38 [France 24] Brazil heads to run-off as Bolsonaro pulls off shock first place finish in first round
  > Flavio Bolsonaro, a right-wing senator and son of former president Jair Bolsonaro, pulled off a surprise first-place finish ahead of President Luiz Inacio Lula da Silva in Brazil’s election Sunday. However, with neither candidate securing a majority the vote now heads to a run-off in three weeks.
- 2026-10-05 09:46 [South China Morning Post] Brazil-China ties in focus as Bolsonaro gets election edge over Lula
  > Brazil is set for a presidential run-off after right-wing challenger Flavio Bolsonaro won a surprise first-round victory, threatening Luiz Inacio Lula da Silva’s grip on power in South America’s largest economy.
Bolsonaro, son of imprisoned former president Jair Bolsonaro, took 47 per cent of the ba
- 2026-10-05 12:34 [Al Jazeera] Bolsonaro favourite to win: What Brazil’s first round of elections tells us
  > Analysts say Flavio Bolsonaro is projected to win the run-off vote on October 25 and become Brazil&#039;s next president.
- 2026-10-05 12:52 [France 24] Brazil presidential election: 'Bolsonaro being ahead is a surprise,' researcher says
  > Far-right candidate Flavio Bolsonaro has pulled off a surprise win in the first round of Brazil’s presidential election. He defied most polls to win with 47 percent, compared to 45 percent for leftist incumbent Luiz Inacio Lula de Silva. We spoke to Thomas Zicman de Barros, a research fellow at CEVI
- 2026-10-05 12:54 [France 24] 'Very bad result for Lula: Bolsonaro is far more effective at speaking to that growing middle class'
  > Eve Irvine is pleased to welcome Felipe Krause, the head of Oxford University's Brazilian Studies Programme. Brazil's election reflects a political landscape that has become increasingly polarized, explains Krause. And he describes the current mood as one of “tired polarization: People are just exha
- 2026-10-05 20:37 [France 24] Concerns of US interference weigh on Brazil vote
  > Conservative Senator Flavio Bolsonaro pulled off a surprise on Sunday in the first round of Brazil’s presidential election by finishing ahead of the incumbent left-wing President Lula, whom he will face in the runoff on October 25. Suspicions of U.S. interference have been hanging over the campaign,
- 2026-10-05 21:00 [Al Jazeera] Brazil’s presidential race head for a tough runoff
  > Brazil is heading into a fiercely contested presidential runoff after the first round revealed major gains for Bolsonaro
**B** (12 item(s))
- 2026-10-04 12:48 [Al Jazeera] Yemen’s leader announces military operation to retake Houthi-held territory
  > Rashad al-Alimi says the campaign aims to restore state authority throughout Yemen.
- 2026-10-04 16:51 [BBC World] Yemen's government announces all-out war to reclaim land from Houthis
  > The Yemeni president's announcement comes amid an exchange of strikes between the Houthis and the Saudi-led coalition.
- 2026-10-04 19:50 [Defense News] Yemeni government launches offensive to seize all areas from Iran-backed Houthis
  > Yemen’s Saudi-backed, internationally recognized government said on Sunday it was launching a major military campaign to recapture all areas of the country controlled by the Iran-backed Houthis.The government’s armed forces would press the offensive “until the country is liberated from the grip of t
- 2026-10-05 00:00 [Al Jazeera] Iran war live: Yemen fighting intensifies; Tehran says ready for US attacks
  > Yemeni government announces major offensive against Houthis, as Iran says it is ready to defend itself if US attacks.
- 2026-10-05 03:11 [Al Jazeera] Yemen gov’t forces commence major combat operation against Houthis
  > Yemeni government forces have declared a ‘battle for liberation’ to retake remaining territory held by the Houthis.
- 2026-10-05 09:37 [France 24] Yemen's government declares major operation against Houthis
  > The Yemeni military announced a broad set of strikes against Houthi targets on Monday, after the government declared a new campaign to retake all territory even as the Iran-backed group made fresh gains on the ground. France 24's Kethevane Gorjestani takes a look at the reasons behind this latest es
- 2026-10-05 09:40 [Al Jazeera] Yemen forces claim to seize Dhubab, sites near Bab al-Mandeb from Houthis
  > Yemeni forces claim to seize key positions near waterway as Pakistani, Saudi and Turkish officials to meet.
- 2026-10-05 13:23 [South China Morning Post] Yemeni government forces seize control of Bab el-Mandeb Strait, minister says
  > Saudi-backed Yemeni government forces have secured effective control of the Bab el-Mandeb Strait, Yemen’s Information Minister Moammar al-Eryani has said, though fighting continues with Houthi forces in the area.
The government forces advanced rapidly along the coast with heavy Saudi air support to 
- 2026-10-05 14:37 [BBC World] Yemeni government forces say they have 'secured' Bab al-Mandab Strait
  > Saudi-backed forces gave conflicting reports of whether they had also seized the port city of Mokha, near the Bab al-Mandab Strait.
- 2026-10-05 14:59 [France 24] Yemen government forces announce offensive on Houthi-held territory
  > The internationally recognised Yemeni government announced on Sunday the launch of an offensive ‌to recapture territory held by Houthi rebels, with President Rashad al-Alimi swearing to fight "until the country is liberated from the grip of the terrorist militia".
- 2026-10-05 15:29 [Al Jazeera] Yemeni gov’t forces aim for Sanaa, but Houthi defeat will be a challenge
  > Yemeni government forces claim strategic advances near Bab al-Mandeb strait amid a major anti-Houthi offensive.
- 2026-10-05 19:17 [France 24] Saudi-backed Yemeni forces expel the Houthis from several areas around key strait, officials say
  > Saudi-backed Yemeni government forces staged a lightning advance on ​Monday to retake the coast around the Bab el-Mandeb Strait up to the city of Mocha, the government said, pushing the Iran-backed Houthis out of most of the areas they seized last month. FRANCE 24's Monte Francis reports.

## U102
**A** (3 item(s))
- 2026-10-08 14:09 [France 24] Search warrants for former prince Andrew's homes were unlawful, UK court rules
  > Police who searched the properties of Andrew Mountbatten-Windsor as part of investigations into his links to the late sex offender Jeffrey Epstein have agreed the search warrants were unlawful, a London judge said Thursday. The 66-year-old younger brother of King Charles II was arrested on February 
- 2026-10-08 15:20 [South China Morning Post] UK police accept ex-prince Andrew search warrants must be ‘legally quashed’
  > British police on Thursday said that search warrants they secured to search properties linked to Andrew Mountbatten-Windsor had been issued unlawfully and must be quashed, but that the investigation into King Charles’ younger brother was ongoing.
Mountbatten-Windsor, 66, was arrested on suspicion of
- 2026-10-08 15:53 [Al Jazeera] UK ex-prince Andrew search warrants quashed after police accept legal error
  > London-based judge says error &#039;does not bring investigation to an end&#039; as police probe disgraced former royal.
**B** (2 item(s))
- 2026-10-08 14:26 [Rai News Esteri] Donald Trump: "Merito ancora il Nobel per la pace, ho evitato la distruzione del mondo"
  > Un anno fa il riconoscimento all'oppositrice venezuelana Maria Corina Machado che il presidente degli Stati Uniti non ha mai digerito
- 2026-10-08 16:44 [Clarín Mundo] Donald Trump mete presión para que le den el Premio Nobel de la Paz 2026: "He evitado la destrucción total del mundo"
  > El presidente de los Estados Unidos volvió a reclamar el premio, luego de que el año pasado se lo entregaran a la opositora venezolana María Corina Machado.También cuestionó que se lo hayan otorgado a Obama en 2009. “Yo he hecho mucho más y no me lo dan”, afirmó.

## U103
**A** (10 item(s))
- 2026-10-04 21:31 [South China Morning Post] US Air Force removes all bombers from UK airbase targeted by suspected terror attack
  > The US Air Force has brought home its bombers stationed at a US-run military airbase in England used to strike Iran following an investigation into a planned terror attack at the RAF Fairford base.
The bombers were redeployed back to their home bases in the United States, according to a Pentagon off
- 2026-10-04 22:23 [Al Jazeera] US withdraws B-1 bomber aircraft from UK’s Fairford base amid Iran fears
  > The abrupt redeployment to the US comes after several &#039;terrorism-related&#039; arrests were made outside RAF Fairford.
- 2026-10-05 04:58 [BBC World] US air force removes all bombers from British military base RAF Fairford
  > A statement says all bombers deployed to RAF Fairford have been "re-deployed to their home stations" in the US.
- 2026-10-05 07:40 [Defense News] US removes B-1 bombers from UK base amid security concerns
  > NEW YORK — The United States removed its B-1 bombers from a U.K. air base one week after several men were arrested there on suspicion of preparing terrorist acts, a Pentagon official said on Sunday. A dozen B-1 bombers were stationed at RAF Fairford air base, located northwest of London. The planes 
- 2026-10-05 09:49 [France 24] US withdraws all bombers from UK base at centre of suspected terror attack
  > The United States has removed its B-1 bombers from a British air base one week after five men were arrested nearby on suspicion of preparing terrorist acts, a ‌suspected plot that British Prime Minister Andy Burnham said was likely backed by Iran. The planes had been ⁠stationed at RAF Fairford, whic
- 2026-10-05 11:09 [Al Jazeera] US abruptly withdraws bombers from UK’s RAF Fairford
  > The US has abruptly withdrawn all of its aircraft from the UK’s RAF Fairford, citing concerns about a potential attack.
- 2026-10-05 12:07 [BBC World] No10 insists UK military base RAF Fairford is safe after US withdraws bombers
  > US media reported a new threat led to the bombers being removed on Sunday, following an incident near the base last week.
- 2026-10-05 17:34 [Al Jazeera] Rubio: No direct link between US bombers removal and UK base incident
  > Rubio stresses US base security, following the removal of B-1 bombers amid alleged threats targeting UK military assets.
- 2026-10-05 19:58 [BBC World] Trump says 'threat' led US to pull bombers from RAF Fairford
  > The Pentagon confirmed on Sunday it had removed the B1 bombers from the base in England back to their home stations in America.
- 2026-10-05 21:40 [South China Morning Post] US bombers moved from UK airbase due to Iran-linked threats, Trump says
  > US President Donald Trump said on Monday that a threat linked to Iran ⁠had prompted the removal of American B-1 bombers from a British airbase.
The planes had been stationed at RAF Fairford, the preferred European base for US bombers, and had recently been used in US strikes on Iran. Last week, five
**B** (2 item(s))
- 2026-10-05 13:05 [France 24] Trump heads to Nebraska as Republicans fear strongholds could flip
  > US President ​Donald Trump will visit Nebraska on Monday to rally Republicans and promote his economic ​record, taking his message of new investment and manufacturing to a state where farmers and truckers face sharply higher diesel prices and voters worry about inflation. His stop in ​the ‌city of G
- 2026-10-05 17:02 [White House] President Trump and Republicans Are Delivering Real Results for Nebraska
  > News				
			
			
					
	
		
		
			Search
					
						
		
			
				
					Select Category				
				
																		
								All News							
																								
								Briefings &amp; Statements							
																								
																	
										All Presidential Actions									
							

## U104
**A** (5 item(s))
- 2026-09-29 21:26 [Breaking Defense] Boeing wins Navy next-gen fighter F/A-XX competition
  > Boeing&#8217;s win gives it a monopoly on American sixth-gen fighters, following its 2025 selection to build the F-47.
- 2026-09-29 22:20 [Defense News] US Navy selects Boeing to build next-generation F/A-XX fighter
  > Boeing has been selected to build the Navy’s sixth-generation carrier-based strike fighter, dubbed F/A-XX, icing out what was considered to be its biggest competitor in late-stage negotiations, Northrop Grumman. Inked at $20 billion for the full-scale development phase, the contract, according to a 
- 2026-09-30 03:52 [South China Morning Post] Pentagon picks Boeing to build new carrier fighter jet to replace F/A-18
  > The Pentagon has chosen Boeing to build the US Navy’s next-generation fighter jets in a contract valued at US$20 billion, officials announced Tuesday.
The contract is to produce F/A-XX aircraft or “strike fighters” under the “Next Generation Air Dominance Program,” a Pentagon statement said, adding 
- 2026-09-30 16:21 [Breaking Defense] Boeing nabs $2.4 billion deal for more F-15EX fighters
  > The award came on the same day that the planemaker secured a contract to build a sixth-generation fighter jet for the US Navy.
- 2026-09-30 19:21 [Defense News] US Air Force awards $2.38B contract to Boeing for 22 F-15EX
  > The U.S. Air Force tapped Boeing for a $2.38 billion contract to produce 22 F-15EX Eagle II aircraft, using previously available funds from the congressionally provided reconciliation to maintain procurement before the fiscal year deadline.The award is under Lot 7, which accounts for current program
**B** (6 item(s))
- 2026-09-30 16:51 [South China Morning Post] UK PM says ‘strong indications’ Iran involved in bomb scare at US-run airbase
  > British Prime Minister Andy Burnham on Wednesday said there were “strong indications” that Iran was involved in suspicious activity at a UK airbase that triggered a major security incident this weekend.
“There are strong indications that Iran played a part in what happened over the weekend at RAF Fa
- 2026-09-30 18:09 [Al Jazeera] Strong indications’ Iran linked to suspected UK airbase plot
  > UK Prime Minister says there are ‘strong indications’ Iran played a part in the suspected RAF Fairford airbase plot.
- 2026-10-01 02:30 [Al Jazeera] UK says Iran may be linked to alleged airbase plot, drawing angry denial
  > Andy Burnham says UK has &#039;strong indications&#039; Iran involved in alleged security incident at RAF base used by US.
- 2026-10-01 16:55 [Al Jazeera] British police arrest UK-Iranian national over airbase incident
  > Counter Terrorism police also questioned a UK national, days after five others were arrested and released on bail.
- 2026-10-01 17:52 [South China Morning Post] UK-Iranian man arrested over suspected Fairford airbase plot
  > British counterterrorism police investigating ⁠a suspected plot involving ⁠an airbase used by the US ⁠to target Iran said on Thursday they had arrested a dual UK-Iranian national on suspicion of preparing terrorist acts.
In an incident which triggered a huge police response, raised alarm among Weste
- 2026-10-03 10:45 [BBC World] UK-Iranian dual national bailed after RAF Fairford incident arrest
  > The 25-year-old man was arrested in the London borough of Westminster on Thursday.

## U105
**A** (5 item(s))
- 2026-09-30 22:13 [Al Jazeera] Russian drone crashes into Kyiv playground without exploding
  > A Russian attack drone crashed into a children’s playground in Kyiv, Ukraine without exploding.
- 2026-10-01 07:09 [South China Morning Post] Ukraine scrambles as Russia’s jet drones breach Kyiv’s defences
  > Russia’s new class of jet-powered drones rip across the night sky in Kyiv at hundreds of kilometres per hour, leaving Ukrainian air-defence units only moments to intercept them. It’s rarely enough time.
With many of the drones getting through to the capital, defence manufacturers are scrambling to d
- 2026-10-01 13:06 [Al Jazeera] Russian drone hits school in Ukraine’s Kyiv as Moscow presses air assault
  > Russian drone strikes hit a school in Kyiv and the main bridge, disrupting transport in the latest wave of attacks.
- 2026-10-02 08:03 [Al Jazeera] Russia tries to freeze Ukraine as it suffers record casualties and retreats
  > Moscow has suffered further losses of occupied territory, but is using new drones to beat Ukraine&#039;s defences.
- 2026-10-02 12:47 [Al Jazeera] Ukraine calls for tighter sanctions as Russian attacks spark Kyiv gridlock
  > Closure of bridges struck by drones in Ukrainian capital causes traffic chaos.
**B** (2 item(s))
- 2026-10-03 07:46 [South China Morning Post] Latvia holds election as concerns over Russia, inflation dominate
  > Latvia will vote on Saturday in an election shaped by concerns over neighbouring Russia and the cost of living, but the result is not expected to steer the country off its pro-European and pro-Ukrainian course.
The centre-right United List party of incumbent Prime Minister Andris Kulbergs is at the 
- 2026-10-03 08:21 [Al Jazeera] Polls open in Latvia against backdrop of perceived Russia threat
  > Latvia is not expected to shift its pro-Europe and pro-Ukraine trajectory, but coalition negotiations could be complex.

## U106
**A** (5 item(s))
- 2026-10-05 04:07 [Al Jazeera] Russian lab worker dies of suspected plague in Siberia; US monitoring case
  > A Russian agency links the lab worker&#039;s death to &#039;pneumonia of unknown&#039; origin.
- 2026-10-05 17:14 [South China Morning Post] After plague death reports at Siberia lab, Russia says situation under control
  > Moscow on Monday downplayed reports that a laboratory technician had died of plague, stressing that postmortem tests had not detected the disease, while Washington said it was closely monitoring the situation.
Reports on Friday that plague had killed a 28-year-old woman named Darya Shipilova, who ha
- 2026-10-05 19:19 [France 24] Russian officials say 'situation under control' after plague reports
  > Moscow on Monday downplayed reports that a laboratory technician had died of plague, stressing that post-mortem tests had not detected the disease, while Washington said it was closely monitoring the situation. Reports on Friday that plague had killed a 28-year-old woman named Darya Shipilova, who h
- 2026-10-05 19:55 [BBC World] US 'watching closely' after plague researcher dies in Russia, Rubio says
  > The US says it is monitoring the case of a lab technician who died at a plague research centre in Siberia.
- 2026-10-05 21:03 [Al Jazeera] Trump says US ready to aid Russia with plague outbreak in Siberia
  > Russian authorities quarantine hospital, monitor 200 contacts after suspected pneumonic plague death in Siberia.
**B** (3 item(s))
- 2026-10-05 15:05 [Kyiv Independent] Russian drones strike cargo ship in Black Sea, kill captain, Zelensky says
  > Ukrainian President Volodymr Zelensky confirmed that a civilian ship was attacked by two Russian drones, adding that it was a Turkish-owned ship transporting corn.
- 2026-10-05 15:17 [BBC World] Zelensky condemns 'horrific' Russian strike on boat carrying corn in Black Sea
  > The vessel's captain was killed and 11 crew members were rescued after the attack on the Turkish-owned ship, Ukraine's leader says.
- 2026-10-05 20:03 [Al Jazeera] Ukraine says Russian drone attack sinks ship in Romanian waters
  > The latest suspected incursion on NATO&#039;s eastern flank increases fears that the war in Ukraine threatens to spill over.

## U107
**A** (2 item(s))
- 2026-10-01 14:00 [South China Morning Post] China backs Cuba, Beijing’s Panama threat, new UN chief: 7 Latin America relations reads
  > We have selected seven of the most interesting and important news stories covering Latin American relations from the past few weeks. If you would like to see more of our reporting, please consider subscribing.
1. China pledges to ‘firmly support’ Cuba as US escalates pressure on Havana

China will s
- 2026-10-02 20:52 [Al Jazeera] Latin America sees China as more positive global influence than US: Poll
  > Annual Latinobarometro survey finds views of China’s influence improving as perceptions of US influence worsen.
**B** (2 item(s))
- 2026-10-01 18:38 [South China Morning Post] Canada fast-tracking oil pipeline designed to diversify economy away from US
  > Canada will fast track the approval process for a new proposed crude oil export pipeline to its west coast that could generate over C$20 billion (US$14 billion) a year in GDP, Prime Minister ‌Mark Carney said on Thursday.
The pipeline, which was announced in July, is a crucial part of Carney’s bid t
- 2026-10-01 18:56 [Al Jazeera] Canada to fast track oil pipeline meant to diversify economy away from US
  > Carney declared the pipeline a project of national interest, smoothening its way to a single federal regulatory review.

## U108
**A** (6 item(s))
- 2026-09-30 16:51 [South China Morning Post] UK PM says ‘strong indications’ Iran involved in bomb scare at US-run airbase
  > British Prime Minister Andy Burnham on Wednesday said there were “strong indications” that Iran was involved in suspicious activity at a UK airbase that triggered a major security incident this weekend.
“There are strong indications that Iran played a part in what happened over the weekend at RAF Fa
- 2026-09-30 18:09 [Al Jazeera] Strong indications’ Iran linked to suspected UK airbase plot
  > UK Prime Minister says there are ‘strong indications’ Iran played a part in the suspected RAF Fairford airbase plot.
- 2026-10-01 02:30 [Al Jazeera] UK says Iran may be linked to alleged airbase plot, drawing angry denial
  > Andy Burnham says UK has &#039;strong indications&#039; Iran involved in alleged security incident at RAF base used by US.
- 2026-10-01 16:55 [Al Jazeera] British police arrest UK-Iranian national over airbase incident
  > Counter Terrorism police also questioned a UK national, days after five others were arrested and released on bail.
- 2026-10-01 17:52 [South China Morning Post] UK-Iranian man arrested over suspected Fairford airbase plot
  > British counterterrorism police investigating ⁠a suspected plot involving ⁠an airbase used by the US ⁠to target Iran said on Thursday they had arrested a dual UK-Iranian national on suspicion of preparing terrorist acts.
In an incident which triggered a huge police response, raised alarm among Weste
- 2026-10-03 10:45 [BBC World] UK-Iranian dual national bailed after RAF Fairford incident arrest
  > The 25-year-old man was arrested in the London borough of Westminster on Thursday.
**B** (3 item(s))
- 2026-09-30 17:07 [Al Jazeera] MI5 warns UK academics to cut ties with Chinese group over alleged spying
  > UK intelligence agency accuses Chinese institute of funding academic research to boost Beijing’s espionage capability.
- 2026-09-30 18:16 [South China Morning Post] UK accuses China of using academics to spy on AI and other tech research
  > Britain’s MI5 spy agency issued an unprecedented alert on Wednesday to warn that a Chinese organisation was involved in funding academic research into topics such as AI on behalf of Beijing’s state security service.
In its “Espionage Alert”, MI5 said more than 100 UK-based academics had contributed 
- 2026-10-01 16:28 [Al Jazeera] Chinese hackers impersonated AI experts to target US policy minds
  > TA419 hackers used deceptive tactics to impersonate real figures, such as a former White House AI official.

## U109
**A** (3 item(s))
- 2026-09-30 11:32 [Al Jazeera] Russian attacks on Ukraine’s Kyiv region kill four, target power grid
  > City officials say three killed in Ukraine&#039;s capital, as emergency services say child killed in the surrounding region.
- 2026-09-30 11:47 [BBC World] Russia launches largest attack on Ukraine energy infrastructure since spring
  > In total 11 regions of the country were attacked overnight, with residential buildings and railways also targeted, the Ukrainian PM says.
- 2026-10-01 12:13 [Defense News] Ukraine has struck Russian factory vital for Moscow’s missiles, private intelligence firm says
  > GLASGOW, Scotland — A Russian factory that Ukraine struck on Sept. 26 supplies electronics for a wide range of Russia’s missiles, potentially leaving Moscow without a fallback supplier, according to leaked documents obtained by the Ukrainian private intelligence firm Dallas Analytics.The documents a
**B** (3 item(s))
- 2026-09-30 17:07 [Al Jazeera] MI5 warns UK academics to cut ties with Chinese group over alleged spying
  > UK intelligence agency accuses Chinese institute of funding academic research to boost Beijing’s espionage capability.
- 2026-09-30 18:16 [South China Morning Post] UK accuses China of using academics to spy on AI and other tech research
  > Britain’s MI5 spy agency issued an unprecedented alert on Wednesday to warn that a Chinese organisation was involved in funding academic research into topics such as AI on behalf of Beijing’s state security service.
In its “Espionage Alert”, MI5 said more than 100 UK-based academics had contributed 
- 2026-10-01 16:28 [Al Jazeera] Chinese hackers impersonated AI experts to target US policy minds
  > TA419 hackers used deceptive tactics to impersonate real figures, such as a former White House AI official.

## U110
**A** (6 item(s))
- 2026-10-08 00:56 [Europa Press Internacional] Maduro y Flores podrían ser acusados este jueves de haber torturado a estadounidenses venezolanos
  > El presidente de Venezuela, Nicolás Maduro, y su esposa, Cilia Flores, podrían ser acusados por estar vinculados a delitos de tortura contra ciudadanos estadounidenses que estuvieron bajo custodia de su gobierno en los últimos años, ha informado la prensa estadounidense.
- 2026-10-08 14:52 [Clarín Mundo] Torturas: Estados Unidos suma una nueva acusación contra Nicolás Maduro
  > El derrocado presidente de Venezuela ya enfrenta delitos de narcotráfico.Maduro y su esposa, Cilia Flores, permanecen tras las rejas en Nueva York desde principios de enero.
- 2026-10-08 15:13 [France 24 Español] EE. UU. suma a Maduro y Cilia Flores un cargo por conspiración para torturar a opositores
- 2026-10-08 15:20 [El País Internacional] Nicolás Maduro y Cilia Flores, acusados en EE UU de nuevos cargos de tortura y represión
  > Ilustración de Nicolás Maduro y Cilia Flores en el tribunal de Nueva York, en julio.
- 2026-10-08 15:21 [BBC Mundo] Presentan nuevos cargos contra Maduro y su esposa por presuntas torturas a ciudadanos de estadounidenses ante un tribunal de Nueva York
  > El expresidente de Venezuela y su esposa fueron acusados por el Departamento de Justicia de EE.UU. de haber participado en la tortura de estadounidenses detenidos en Caracas.
- 2026-10-08 15:32 [Europa Press Internacional] EEUU imputa a Maduro y su esposa por liderar un sistema de represión y torturas en Venezuela
  > La Fiscalía de Estados Unidos ha imputado este jueves al presidente de Venezuela, Nicolás Maduro, y su esposa, Cilia Flores, por delitos de tortura contra personas detenidas, incluyendo ciudadanos estadounidenses, en el marco de un "sistema de represión que recurría a la violencia contra la oposició
**B** (3 item(s))
- 2026-10-08 01:15 [Europa Press Internacional] Diosdado Cabello llama a cerrar filas con Delcy Rodríguez y reta a la oposición a medirse en las urnas
  > El ministro del Interior y secretario general del Partido Socialista Unido de Venezuela (PSUV), Diosdado Cabello, ha retado este martes a la oposición a presentarse a unas elecciones, mostrándose convencido de una nueva victoria del oficialismo en los hipotéticos comicios. Por su parte, la líder opo
- 2026-10-08 01:22 [ANSA Mondo] Venezuela, Delcy Rodríguez al Forum mondiale dell'alimentazione a Roma
  > La presidente ad interim del

Venezuela, Delcy Rodríguez, parteciperà il 12 ottobre a Roma al

Forum mondiale dell'alimentazione organizzato dalla Fao. Lo

riferisce Efe, citando il programma dell'evento. Rodríguez

interverrà alla cerimonia di apertura insieme, tra gli altri, al

presidente bolivia
- 2026-10-08 14:28 [France 24 Español] Estados Unidos presenta nuevos cargos contra Maduro y Cilia Flores por presuntas torturas a estadounidenses
  > Estados Unidos presenta nuevos cargos contra Nicolás Maduro y Cilia Flores por la presunta tortura de ciudadanos estadounidenses detenidos en Venezuela. La Fiscalía de Manhattan anunció este jueves las nuevas acusaciones, mientras la esposa del presidente venezolano pide salir de prisión para somete

## U111
**A** (2 item(s))
- 2026-10-07 23:45 [Al Jazeera] EU-China trade talks begin in Beijing amid escalating pressure
  > Talks will focus on the €1bn daily deficit and rare earth export restrictions.
- 2026-10-08 03:00 [South China Morning Post] As China and the EU begin crunch trade talks, optimism is in short supply
  > As China and the European Union began a fresh round of trade talks in Beijing on Thursday, observers on both sides appeared to agree on one thing: a big breakthrough was unlikely.
Chinese firms based in Europe said they hoped the talks could achieve some “limited progress” to help stabilise the trad
**B** (2 item(s))
- 2026-10-08 07:38 [South China Morning Post] US AI firm Anthropic enables Chinese-language options for Claude chatbot
  > US artificial intelligence company Anthropic has introduced Chinese-language options to its Claude chatbot in supported markets, even as it continues to block users from mainland China.
Checks by the South China Morning Post on Thursday confirmed that Claude’s web interface now lets users select sim
- 2026-10-08 09:37 [BBC Mundo] Por qué China considera una amenaza la IA que imita las relaciones humanas
  > Pekín ha intensificado la represión contra los chatbots de IA capaces de replicar las relaciones humanas. Los expertos se preguntan si esta medida es la correcta.

## U112
**A** (2 item(s))
- 2026-10-08 02:48 [Al Jazeera] Tanker hit by multiple projectiles off north coast of Qatar, UKMTO says
  > The UK maritime agency has reported a rise in attacks on vessels in the vital Strait of Hormuz.
- 2026-10-08 10:07 [BBC World] Tanker hit by multiple projectiles in Gulf off Qatar, maritime agency says
  > Casualties have been reported on the vessel, identified by a maritime intelligence firm as the oil and chemical tanker, Acers.
**B** (3 item(s))
- 2026-10-08 14:09 [France 24] Search warrants for former prince Andrew's homes were unlawful, UK court rules
  > Police who searched the properties of Andrew Mountbatten-Windsor as part of investigations into his links to the late sex offender Jeffrey Epstein have agreed the search warrants were unlawful, a London judge said Thursday. The 66-year-old younger brother of King Charles II was arrested on February 
- 2026-10-08 15:20 [South China Morning Post] UK police accept ex-prince Andrew search warrants must be ‘legally quashed’
  > British police on Thursday said that search warrants they secured to search properties linked to Andrew Mountbatten-Windsor had been issued unlawfully and must be quashed, but that the investigation into King Charles’ younger brother was ongoing.
Mountbatten-Windsor, 66, was arrested on suspicion of
- 2026-10-08 15:53 [Al Jazeera] UK ex-prince Andrew search warrants quashed after police accept legal error
  > London-based judge says error &#039;does not bring investigation to an end&#039; as police probe disgraced former royal.

## U113
**A** (5 item(s))
- 2026-09-29 12:00 [South China Morning Post] US and China need shared risk vocabulary to manage AI threats: Beijing-linked think tank
  > Beijing and Washington should first develop a common language around AI risks rather than seek to resolve their broader technology rivalry, a leading Chinese think tank has advised.
The call from the China Institutes of Contemporary International Relations (CICIR), affiliated with the Ministry of St
- 2026-09-29 16:09 [BBC World] Trump rules out joint US-China venture to develop AI
  > The US president continues to push back on calls to establish guardrails around artificial intelligence, arguing it will stifle growth.
- 2026-09-29 19:32 [South China Morning Post] Trump rejects calls to work with China on AI safety despite Xi summit progress
  > US President Donald Trump said on Tuesday he does not want to work with China on addressing artificial intelligence (AI) risks, arguing that cooperation could undermine America’s lead in the fast-moving technology.
“Whoever wins superintelligence wins. You’re gonna have a winner and a loser, and you
- 2026-09-29 23:43 [Al Jazeera] Trump, tech bosses sign voluntary pact pledging ‘robust’ AI safeguards
  > US President Trump touts self-regulation amid the international community&#039;s and industry&#039;s calls for formal rules.
- 2026-09-30 05:00 [South China Morning Post] Chinese firms trail global peers on profits, but AI power boom offers bright spot: Natixis
  > China’s corporate sector remains considerably weaker than it was before the Covid-19 pandemic, but the country is emerging as a key beneficiary of the global artificial intelligence boom thanks to its ample power capacity, according to a Natixis survey of thousands of firms and a separate research r
**B** (6 item(s))
- 2026-10-02 01:23 [Al Jazeera] Trump says US may ask Europe to release diesel reserves
  > Skyrocketing diesel prices have pushed Washington to weigh an export ban, raising alarm across European economies.
- 2026-10-02 05:26 [BBC World] US pressures Europe over diesel reserves as Trump threatens export ban
  > President Donald Trump has threatened to ban diesel exports in a bid to ease prices in the US ahead of the November elections.
- 2026-10-02 13:16 [Al Jazeera] Trump vs Europe as US presses for release of emergency diesel stocks
  > Europe&#039;s leaders are mulling proposals to respond to Trump&#039;s diesel demands.
- 2026-10-02 14:51 [South China Morning Post] G7 nations agree to release diesel and oil stocks after Trump pressure
  > Group ⁠of Seven countries agreed on Friday to release 100 million barrels of diesel and crude oil from emergency reserves and pledged to refrain from energy export restrictions after pressure from US President Donald Trump.
The US led a pressure campaign on the European Union to draw down emergency 
- 2026-10-02 19:01 [Al Jazeera] Trump says Europe agreed to release ‘massive amount’ of diesel reserves
  > US President Donald Trump says Europe agreed to release a ‘massive amount’ of diesel from emergency stockpiles.
- 2026-10-02 20:25 [BBC World] G7 to release 100 million barrels of oil and diesel after Trump export ban threat
  > The co-ordinated release is aimed at heading off further price spikes and avoiding a ban on US diesel exports.

## U114
**A** (2 item(s))
- 2026-10-08 07:38 [South China Morning Post] US AI firm Anthropic enables Chinese-language options for Claude chatbot
  > US artificial intelligence company Anthropic has introduced Chinese-language options to its Claude chatbot in supported markets, even as it continues to block users from mainland China.
Checks by the South China Morning Post on Thursday confirmed that Claude’s web interface now lets users select sim
- 2026-10-08 09:37 [BBC Mundo] Por qué China considera una amenaza la IA que imita las relaciones humanas
  > Pekín ha intensificado la represión contra los chatbots de IA capaces de replicar las relaciones humanas. Los expertos se preguntan si esta medida es la correcta.
**B** (2 item(s))
- 2026-10-08 08:06 [State Department] Secretary of State Marco Rubio Remarks to the Press
  > Marco Rubio, Secretary of State
Athens, Greece
Athens International Airport



	

		
		

			

		

		

			

				
				

					
						Secretary of State Marco Rubio Remarks to the Press
					
				

				

					

					
					
						Remarks

					
					
					
			

			
			

			
			October 8, 2026

			
				


- 2026-10-08 13:38 [Al Jazeera] Rubio praises nationalism and ties ‘America First’ values to ancient Greece
  > US Secretary of State Marco Rubio urged Western nations to prioritise their own interests in a speech in Athens.

## U115
**A** (5 item(s))
- 2026-10-04 15:16 [Al Jazeera] Dodik urges Serb turnout against ‘Sarajevo crooks’ in Bosnia election
  > Dodik urges Serb turnout against ‘Sarajevo crooks’ in Bosnia election
- 2026-10-04 20:36 [South China Morning Post] Serb separatist Dodik declares victory in Bosnia vote as ethnic tensions, EU hopes collide
  > Bosnian Serb nationalist politician Milorad Dodik has declared victory for his party in an election in Bosnia and Herzegovina on Sunday that was shaped by economic pressures, the prospect of the Balkan nation joining the European Union and ethnic tensions that have divided the country since its brut
- 2026-10-05 03:36 [Al Jazeera] Bosnian Serb nationalist claims party victory in Bosnia elections
  > Bosnian Serb nationalist Milorad Dodik claimed victory for his party in Bosnia’s elections.
- 2026-10-05 07:33 [Kyiv Independent] Pro-Russian Dodik claims party victory in Bosnian elections
  > "If it had not been for (U.S. President) Donald Trump's magnificent victory, we would probably be political corpses today," Milorad Dodik told his supporters, while also thanking Russian President Vladimir Putin.
- 2026-10-05 10:23 [DW World] Bosnia election: New technology might have stopped votes being cast on behalf of dead voters, but the result remains unchanged
  > New technology has stopped votes being cast on behalf of dead or absent voters, and turnout has fallen to a record low. But it was a case of deja vu in Bosnia's elections with the same parties winning.
**B** (3 item(s))
- 2026-10-05 11:51 [France 24 Español] Irán entrena a mujeres en las armas ante una posible invasión terrestre
  > En medio de las tensiones con Estados Unidos e Israel, Irán ha puesto en marcha programas de entrenamiento para civiles, incluidas numerosas mujeres, con el objetivo de prepararlas para responder ante una eventual invasión terrestre. En plazas y centros de entrenamiento de Teherán, las participantes
- 2026-10-05 14:49 [El País Internacional] Irán empieza a entrenar a voluntarios civiles para la “defensa nacional”
  > Voluntarias con rifles de asalto del tipo Kaláshnikov, en un curso de entrenamiento militar para civiles en la plaza Imán Hussein de Teherán, este domingo.
- 2026-10-05 15:47 [Europa Press Internacional] El presidente de Irán nombra a Mehrdad Ajlaqi nuevo ministro de Defensa
  > El presidente de Irán, Masud Pezeshkian, ha nombrado este lunes a Mehrdad Ajlaqi nuevo ministro de Defensa del país, por lo que la elección pasa ahora a manos del Parlamento para ser sometida a votación a medida que avanza el conflicto abierto en la región de Oriente Próximo a raíz de la ofensiva la

## U116
**A** (56 item(s))
- 2026-10-04 03:30 [El País Internacional] Ni Bolsonaro, ni Lula: Trump se reserva (de momento) su apoyo en las elecciones de Brasil
  > Un asistente a un mitin de Flavio Bolsonaro disfrazado de Trump, el pasado domingo.
- 2026-10-04 04:00 [El País Internacional] La disputa entre Lula y Trump marca las elecciones brasileñas
  > Banderas de Flavio Bolsonaro y Luiz Inacio Lula da Silva en Brasilia, el 29 de septiembre.
- 2026-10-04 11:20 [Rai News Esteri] Urne aperte in Brasile per le elezioni presidenziali e legislative, sfida Lula-Bolsonaro
  > Gli ultimi sondaggi davano un testa a testa
- 2026-10-04 20:19 [El País Internacional] Brasil decide su futuro entre Lula y Bolsonaro, un estadista desgastado y el hijo de un ultra
  > El presidente Lula, el día 24 en São Gonçalo, y Flávio Bolsonaro, este sábado en Río.
- 2026-10-04 20:43 [Europa Press Internacional] Bolsonaro gana la primera vuelta en Brasil con el 47% de los votos y disputará contra Lula (45%) la segunda vuelta
  > El candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil e hijo del expresidente Jair Bolsonaro, Flávio Bolsonaro, ha ganado la primera vuelta de las elecciones en Brasil con un 47,17% de los sufragios. Su rival y presidente saliente, Luiz Inácio Lula da Silva, ha quedado cua
- 2026-10-04 22:25 [ANSA Mondo] Media, Lula e Bolsonaro andranno al ballottaggio il 25 ottobre
  > A metà scrutinio Bolsonaro al 49%, Lula a 42%
- 2026-10-04 23:00 [Clarín Mundo] Los Bolsonaro amplían su presencia en el Congreso con las elecciones en Brasil: entran la esposa del ex presidente y dos hermanos de Flavio
  > Michelle, la exprimera dama brasileña alcanzó el 28% de los votos en las elecciones legislativas del Distrito Federal.Otros dos hijos del expresidente Jair Bolsonaro compitieron por bancas legislativas en el estado de Santa Catarina.
- 2026-10-04 23:23 [Clarín Mundo] Elecciones en Brasil: Flávio Bolsonaro, un presidenciable a la sombra de su padre
  > Tiene 45 años y es el mayor de los cinco hijos del ex presidente. Elogia las políticas de seguridad de Nayib Bukele en El Salvador y promete la construcción de numerosas cárceles. Asimismo, presume de su buena relación con Donald Trump tras mantener una reunión privada en la Casa Blanca.
- 2026-10-04 23:23 [Clarín Mundo] Lula da Silva busca su reelección en Brasil: entre el freno a la ultraderecha y la defensa de su legado social
  > • A los 80 años, el mandatario brasileño busca la reelección apoyado en su historial de programas sociales como el Bolsa Familia, que actualmente beneficia a una cuarta parte de la población.
• Con vistas a un nuevo período, impulsa una reforma laboral para reducir la jornada semanal a cinco días y 
- 2026-10-05 00:09 [Rai News Esteri] Il sorpasso di Bolsonaro, la crisi di Lula
  > Flavio Bolsonaro, figlio dell'ex presidente di estrema destra tentato golpista, vince il primo turno sul presidente di sinistra Lula da Silva
- 2026-10-05 00:12 [Clarín Mundo] Elecciones en Brasil: un voto castigo que sorprendió a Lula da Silva y llegó desde su base tradicional de votantes
  > Un primer análisis indica que los sectores de menores ingresos se distanciaron de la elección y del líder del PT. El país es un éxito macro, con números notables, pero esos resultados no llegaron a los bolsillos de ese amplio espacio de votantes que se endeuda para pagar los gastos básicos.
- 2026-10-05 01:03 [Clarín Mundo] Lula acepta el impacto del triunfo de Bolsonaro: fue "un resultado inesperado"
  > El representante del socialista Partido de los Trabajadores busca su cuarto mandato, con la reelección en la gestión actual.Quedó detrás de Flavio Bolsonaro por apenas 2,15 puntos.
- 2026-10-05 01:08 [Clarín Mundo] Flavio Bolsonaro, tras ganar en primera vuelta ante Lula: "Brasil quiere un cambio"
  > Aseguró también que este resultado marcan "el fin de la era del PT" en su país.Dijo estar "feliz" con los números obtenidos frente al actual mandatario, Lula da Silva.
- 2026-10-05 01:41 [El País Internacional] Arrasadora victoria de la derecha en Brasil
  > Flavio Bolsonaro habla con la prensa en Río de Janeiro, este domingo.
- 2026-10-05 02:13 [Europa Press Internacional] Bolsonaro proclama "fin de la era del PT" y Lula apela a combatir su "pasado tenebroso" en la segunda vuelta en Brasil
  > Bolsonaro supera los 55 millones de apoyos (47,04%) y logra una ventaja de 2,3 millones de sufragios sobre el actual mandatario (45,15%)
- 2026-10-05 02:28 [El País Internacional] El apellido Bolsonaro gana desde la cárcel
  > Flávio Bolsonaro, candidato presidencial de Brasil, este domingo tras los resultados de la primera vuelta.
- 2026-10-05 02:39 [BBC Mundo] Cómo se compara Flávio Bolsonaro con su padre Jair y cuánto cambia el duelo con Lula por la presidencia de Brasil 4 años después
  > El senador derechista pasa fortalecido al balotaje contra el presidente de izquierda tras obtener más votos en la primera vuelta contra varios pronósticos, pero la elección sigue abierta.
- 2026-10-05 02:46 [France 24 Español] Simone Pitta: "Con esta primera vuelta se puede ver una consolidación del bolsonarismo en Brasil"
  > Pese a no haber estado en el poder en el último periodo presidencial de Brasil, y pese a las denuncias y condenas contra el expresidente Jair Bolsonaro por un intento de golpe de Estado, el bolsonarismo logró consolidarse de cara a los comicios de este 4 de octubre. Ahora, Flávio Bolsonaro busca pos
- 2026-10-05 02:47 [France 24 Español] Juan Agulló: "A diferencia de otros países de Latinoamérica, Brasil es un competidor directo"
  > En un escenario marcado por la polarización en Brasil, el candidato de ultraderecha y heredero político de su padre, Flávio Bolsonaro, y el actual presidente, Luiz Inácio Lula da Silva, quien busca un cuarto mandato, se disputan el balotaje. La sombra de Estados Unidos estuvo presente durante la pri
- 2026-10-05 02:54 [El País Internacional] Bolsonaro vence a Lula en primera vuelta de las elecciones y acaricia el retorno de la ultraderecha al poder en Brasil
  > Flávio Bolsonaro habla tras clasificarse para la segunda vuelta en Brasilia, Brasil, este domingo.
- 2026-10-05 03:19 [France 24 Español] Brasil: la derecha de Bolsonaro se fortalece en las regiones, con un triunfo holgado en São Paulo
  > Los comicios locales de Brasil se saldaron este domingo con un avance de la derecha que representan el candidato presidencial Flávio Bolsonaro y sus aliados. En tanto la izquierda del presidente y aspirante a la reelección, Luiz Inácio Lula da Silva perdía terreno. La victoria más cómoda fue en São 
- 2026-10-05 03:36 [El País Internacional] Las claves de la primera vuelta en Brasil: de la fuerza ultra al día después de Lula con América Latina pendiente
  > Flávio Bolsonaro vota en Río de Janeiro, este domingo.
- 2026-10-05 03:41 [France 24 Español] Flávio Bolsonaro tritura las encuestas: una ventaja pequeña, pero un escenario cuesta arriba para Lula
  > Brasil quedó inclinado hacia la tendencia de retorno a la derecha que sacude a América Latina, luego de que el senador e hijo del expresidente Jair Bolsonaro aventajara por casi dos puntos al izquierdista Luiz Inácio Lula da Silva en la primera vuelta de las elecciones. Lula ha reconocido el resulta
- 2026-10-05 04:08 [El País Internacional] Videoanálisis | Lula se enfrenta a una segunda vuelta electoral muy complicada
  > Videoanálisis | Lula Y Flávio Bolsonaro se enfrenta a una segunda vuelta electoral
- 2026-10-05 04:33 [Rai News Esteri] Brasile, avanzata del clan Bolsonaro: quattro eletti in Parlamento, Flavio al ballottaggio con Lula
  > L'ex first lady Michelle e Carlos, uno dei figli dell'ex presidente, conquistano un seggio al Senato. Alla Camera entrano il figlio più giovane Jair Renan e Renato, fratello di Jair
- 2026-10-05 05:14 [Il Sole 24 Ore Mondo] Brasile, Bolsonaro vince al primo turno con 47%, Lula al 45%: ballottaggio il 25 ottobre
  > Flavio Bolsonaro batte Lula al primo turno e si lancia come favorito nel ballottaggio del 25 ottobre che deciderà chi sarà il 40esimo presidente del Brasile. Il candidato trumpiano ha ottenuto il 47,14 % dei voti, il presidente uscente il 45.03 %, con una differenza tra i due di circa 2 milioni e me
- 2026-10-05 05:31 [Europa Press Internacional] Trump tacha de "corruptas" las elecciones de EEUU comparándolas con las de Brasil tras la victoria de Bolsonaro
  > El presidente de Estados Unidos, Donald Trump, ha vuelto a cargar contra el proceso electoral en su propio país, tachándolo de corrupto y contraponiéndolo la rapidez en el escrutinio de los votos de 125 millones de personas "en la primera vuelta de las elecciones presidenciales de Brasil", donde el 
- 2026-10-05 05:46 [Europa Press Internacional] Milei felicita a su "querido amigo" Flávio Bolsonaro por su "histórica elección" frente a Lula en Brasil
  > El presidente de Argentina, Javier Milei, ha felicitado al candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil, Flávio Bolsonaro, por su victoria en la primera vuelta de las elecciones presidenciales celebradas este domingo, en las que se ha impuesto con el 47,03% de los vo
- 2026-10-05 06:44 [ANSA Mondo] Brasile, l'ex giudice che condannò Lula eletto governatore
  > Sergio Moro guiderà l'esecutivo del suo stato natale, il Paranà
- 2026-10-05 07:14 [BBC Mundo] Elecciones en Brasil: Flávio Bolsonaro y Lula da Silva van a una segunda vuelta en la que el presidente enfrenta una difícil remontada
  > La mayor democracia de América Latina irá a balotaje el 25 de octubre. Lula lleva la desventaja frente a Bolsonaro, ya que históricamente nunca hubo una remontada en una segunda vuelta electoral en Brasil.
- 2026-10-05 07:46 [ANSA Mondo] In Brasile un 30enne di destra è il deputato più votato della storia
  > Nikolas Ferreira ha raccolto oltre 3,1 milioni di preferenze per la Camera
- 2026-10-05 10:46 [ANSA Mondo] Astensione record in Brasile, il 21,08% non ha votato al primo turno
  > Si tratta del livello più alto registrato dalle elezioni del 1998 (21,5%)
- 2026-10-05 11:42 [France 24 Español] Brasil irá a segunda vuelta: Flávio Bolsonaro lidera la primera ronda
  > Brasil se encamina a una segunda vuelta presidencial tras una elección marcada por la polarización. El senador Flávio Bolsonaro obtuvo el primer lugar en la primera vuelta, pero sin alcanzar la mayoría necesaria para evitar el balotaje. El próximo 25 de octubre se enfrentará al actual presidente, Lu
- 2026-10-05 12:20 [Rai News Esteri] Il primo turno delle presidenziali in Brasile, avanti Bolsonaro: ribaltati i pronostici pro-Lula
  > La sfida per il secondo turno del 25 ottobre è ancora aperta ma il presidente uscente non minimizza il peso di una pesante bocciatura delle sue politiche
- 2026-10-05 12:21 [Rai News Esteri] Presidenziali in Brasile, Flavio Bolsonaro a sorpresa supera Lula di 2 punti. Si va al ballottaggio
  > Il candidato di destra al 47%: "Il Brasile vuole cambiare". Il presidente uscente al 45%: "Sono bravo ai supplementari". Scelta rinviata al secondo turno del 25 ottobre
- 2026-10-05 12:29 [Clarín Mundo] Elecciones en Brasil 2026, EN VIVO: reacciones tras la victoria de Flávio Bolsonaro sobre Lula y últimas noticias del balotaje
  > Bolsonaro se impuso en la primera vuelta al superar por casi dos puntos al actual presidente Lula da Silva. El balotaje entre ambos se hará el 25 de octubre. Todas las repercusiones, minuto a minuto.
- 2026-10-05 12:31 [Clarín Mundo] Quién es Flávio Bolsonaro, el hijo de Jair que sorprendió a Lula y va por la presidencia de Brasil
  > Nacido en el estado de Río de Janeiro, Flávio es el mayor de los cinco hijos del expresidente y el que más se le parece físicamente.Este senador, de 45 años, enfrentará a Lula en el balotaje el próximo 25 de octubre.
- 2026-10-05 13:05 [France 24 Español] Informe desde Río de Janeiro: el Partido Liberal de Bolsonaro se fortalece en el Senado
  > Las elecciones legislativas en Brasil dejaron un resultado clave para el futuro político del país: el Partido Liberal (PL), formación vinculada al expresidente Jair Bolsonaro y que postuló a Flávio Bolsonaro para la Presidencia, amplió significativamente su presencia en el Senado. La bancada pasará 
- 2026-10-05 13:16 [Clarín Mundo] Elecciones en Brasil: los mercados celebran la ventaja de Flávio Bolsonaro sobre Lula y el principal índice de la Bolsa marca un nuevo récord
  > Los activos brasileños se dispararon este lunes y el real se apreció en la primera sesión de los mercados tras los comicios del domingo. El índice Ibovespa superó la marca de los 209.000 puntos por primera vez.
- 2026-10-05 13:57 [BBC Mundo] Quiénes son Lucas Pavanato y Nikolas Ferreira, los jóvenes influencers de derecha que lograron las mayores votaciones en la historia de la Cámara de Diputados de Brasil
  > Los flamantes legisladores comparten una agenda conservadora que incluye el rechazo a las políticas de género, el endurecimiento de las sanciones penales y la legalización del porte de armas como herramienta para combatir la delincuencia.
- 2026-10-05 14:50 [Clarín Mundo] Elecciones en Brasil: los resultados del domingo cambian por completo el diseño del país y ya asoma una amnistía para Jair Bolsonaro
  > La victoria del candidato conservador Flávio Bolsonaro sobre el presidente Lula da Silva en primera vuelta excede lo que pueda ocurrir en el balotaje.La ola de derecha se consolida con victorias en las gobernaciones y especialmente en el Parlamento.Aun si el líder petista lograra imponerse el 25 de 
- 2026-10-05 15:47 [Clarín Mundo] La reacción de los medios en Brasil tras la victoria de Bolsonaro: desde "el ciclo de Lula está terminado" hasta "el tsunami de lo peor de la derecha"
  > Los títulos, opiniones y análisis de la prensa en Brasil tras la primera vuelta de las presidenciales de este domingo.
- 2026-10-05 15:59 [France 24 Español] Flávio Bolsonaro y Lula da Silva se preparan para el balotaje en Brasil
  > 🇧🇷🗳️ Luiz Inácio Lula da Silva y Flávio Bolsonaro ofrecieron declaraciones después de que los resultados de los comicios presidenciales de Brasil confirmaran que deberán disputar el balotaje del 25 de octubre.
- 2026-10-05 16:02 [El País Internacional] El lulismo cruje ante la ofensiva ultra
  > Carteles del presidente Trump y del candidato Flavio Bolsonaro, en São Paulo, Brasil, este Lunes.
- 2026-10-05 16:10 [France 24 Español] "Solo faltan días para el rescate Brasil": Bolsonaro celebra la victoria sobre Lula
  > El senador del Partido Liberal (PL) y candidato presidencial, Flávio Bolsonaro, agradeció este lunes "a Dios" y al pueblo brasileño por su victoria en las elecciones del domingo ante el presidente Luiz Inácio Lula da Silva, en contra de los pronósticos. Además, celebró que el PL resultara el partido
- 2026-10-05 16:23 [Clarín Mundo] Elecciones en Brasil: a contrarreloj, Lula y el PT analizan cambios totales en la estrategia de campaña
  > Lo anticipan fuentes partidarias, pero no es claro en qué consistirán. Trascendió que ha habido tensiones internas sobre el manejo de la campaña.Y que debido a eso se perdieron oportunidades importantes para reducir el impulso del candidato opositor, Flávio Bolsonaro.
- 2026-10-05 16:36 [France 24 Español] Paraguay, refugio fiscal y político para la extrema derecha brasileña
  > En los últimos cinco años, las solicitudes de permisos de residencia de brasileños en Paraguay se han más que duplicado. Muchos de los recién llegados son simpatizantes de Jair Bolsonaro que temen una reelección del actual presidente, Luiz Inácio Lula da Silva, a quien responsabilizan de un deterior
- 2026-10-05 17:02 [ANSA Mondo] Brasile, Erika Hilton è la donna più votata della storia alla Camera
  > La politica brasiliana Erika

Hilton ha stabilito un nuovo record nella storia della Camera

dei deputati brasiliana, diventando la donna più votata di

sempre. La deputata trans del Partito socialismo e libertà

(Psol) di San Paolo è stata rieletta con 1.596.472 voti, pari al

5,9% dei voti espress
- 2026-10-05 17:30 [Clarín Mundo] El fantasma de Bolsonaro reaparece en Europa: los temores de Bruselas ante un eventual cambio de gobierno en Brasil
  > • Un cambio de gobierno en Brasil aportaría argumentos a los eurodiputados que buscan frenar la ratificación del entendimiento comercial.
• Si entre 50 y 80 legisladores modifican su postura en la votación prevista para los próximos meses, la aplicación provisional del pacto quedará suspendida.
- 2026-10-05 18:04 [France 24 Español] El mercado de valores de Brasil aplaude la ventaja de Bolsonaro en primera vuelta presidencial
  > El índice bursátil iBovespa, el más importante de la bolsa de São Paulo inició la jornada con un alza estrepitosa de casi el 9% y alcanzó máximo histórico, mientras el real brasileño gana 4,5% frente al dólar a media jornada, hasta situarse ligeramente por encima de los 5 reales por dólar. El buen r
- 2026-10-05 18:10 [France 24 Español] La dinastía Bolsonaro se fortalece: prensa brasileña sobre la primera vuelta electoral
  > La familia Bolsonaro no solo ganó la primera vuelta en Brasil, fortaleció su presencia en ambas cámaras del Congreso y conserva los respaldos de más de 10 gobernadores. 'O Globo' habla del bloque familiar que se ha hecho con varios cargos. Hermanos, hijos, esposa y exesposa tienen un puesto de elecc
- 2026-10-05 19:41 [El País Internacional] La ola conservadora de América Latina llega a Brasil
  > Flávio Bolsonaro (i) junto al presidente de EE.UU., Donald Trump, en el despacho oval de la Casa Blanca en Washington, el 26 de mayo de 2026.
- 2026-10-05 19:42 [El País Internacional] La victoria en primera vuelta de Bolsonaro impulsa a la ola ultra de América Latina
  > Transeúntes pasan ante pósteres dañados que muestran a Bolsonaro hijo con el presidente Trump, este lunes en São Paulo.
- 2026-10-05 19:47 [Clarín Mundo] Elecciones en Brasil: las urnas de la sorpresa
  > Tras el imprevisto triunfo de Flávio Bolsonaro sobre Lula en la primera vuelta, Brasil se encamina hacia un balotaje decisivo el próximo 25 de octubre. La contienda electoral ratifica la profunda polarización política del país y la consolidación del bolsonarismo como una fuerza de derecha permanente
- 2026-10-05 20:21 [ANSA Mondo] Trump, il risultato di Bolsonaro in Brasile una 'grande vittoria'
  > Il risultato di Flavio Bolsonaro

alle elezioni in Brasile è stata una "grande vittoria". Lo ha

detto Donald Trump.Quella di Bolsonaro "è una grande vittoria: combattuta, ma una

vittoria davvero enorme. Incredibile", ha detto Trump. Bolsonaro

si avvia al ballottaggio del 25 ottobre come favorito.
- 2026-10-05 22:09 [ANSA Mondo] Brasile, l'ex presidente Temer sostiene Bolsonaro al ballottaggio
  > L'ex presidente brasiliano

Michel Temer (2016-2018) ha dichiarato il suo sostegno a Flávio

Bolsonaro in vista del ballottaggio del 25 ottobre contro Luiz

Inácio Lula da Silva. In un video diffuso sui social, Temer ha

affermato che il risultato del primo turno mostra la volontà

degli elettori di
**B** (14 item(s))
- 2026-10-04 11:15 [Al Jazeera] Brazil votes in deeply polarised election pitting Lula against Bolsonaro
  > Close race expected as left-wing leader Lula seeks fourth nonconsecutive term against right-wing Flavio Bolsonaro.
- 2026-10-04 17:48 [South China Morning Post] Brazilians head to polls in high-stakes, polarised election
  > Brazilians queued to vote on Sunday in the first round of a tight election, following a campaign dominated by corruption scandals, economic anxiety and accusations of US meddling.
The field of 13 candidates has been led by two clear front runners – leftist President Luiz Inacio Lula da Silva, 80, wh
- 2026-10-04 21:11 [BBC World] Polls close in Brazil as Lula and Flávio Bolsonaro remain neck and neck
  > If no candidate gets more than 50% of the vote, the election will go to a run-off on 25 October.
- 2026-10-05 00:27 [DW World] Brazil election: Bolsonaro and Lula head to runoff
  > Populist Flavio Bolsonaro has secured a thin lead over incumbent Luiz Inacio Lula da Silva, but the next president of Brazil will be decided in the runoff round, according to the country’s electoral court.
- 2026-10-05 03:16 [BBC World] Right-wing Flávio Bolsonaro wins first round of Brazil election
  > With neither candidate getting more than 50% of the vote, the election will go to a run-off on 25 October.
- 2026-10-05 04:51 [BBC World] Watch: How Brazil's dramatic election unfolded
  > Millions of Brazilians took to the polls on Sunday for the first round of the country's presidential elections.
- 2026-10-05 05:08 [Al Jazeera] Bolsonaro beats expectations in Brazil vote, faces Lula in runoff
  > Brazil’s presidential election is heading to a run-off after Bolsonaro and Lula both fell short of the 50% needed to win
- 2026-10-05 09:38 [France 24] Brazil heads to run-off as Bolsonaro pulls off shock first place finish in first round
  > Flavio Bolsonaro, a right-wing senator and son of former president Jair Bolsonaro, pulled off a surprise first-place finish ahead of President Luiz Inacio Lula da Silva in Brazil’s election Sunday. However, with neither candidate securing a majority the vote now heads to a run-off in three weeks.
- 2026-10-05 09:46 [South China Morning Post] Brazil-China ties in focus as Bolsonaro gets election edge over Lula
  > Brazil is set for a presidential run-off after right-wing challenger Flavio Bolsonaro won a surprise first-round victory, threatening Luiz Inacio Lula da Silva’s grip on power in South America’s largest economy.
Bolsonaro, son of imprisoned former president Jair Bolsonaro, took 47 per cent of the ba
- 2026-10-05 12:34 [Al Jazeera] Bolsonaro favourite to win: What Brazil’s first round of elections tells us
  > Analysts say Flavio Bolsonaro is projected to win the run-off vote on October 25 and become Brazil&#039;s next president.
- 2026-10-05 12:52 [France 24] Brazil presidential election: 'Bolsonaro being ahead is a surprise,' researcher says
  > Far-right candidate Flavio Bolsonaro has pulled off a surprise win in the first round of Brazil’s presidential election. He defied most polls to win with 47 percent, compared to 45 percent for leftist incumbent Luiz Inacio Lula de Silva. We spoke to Thomas Zicman de Barros, a research fellow at CEVI
- 2026-10-05 12:54 [France 24] 'Very bad result for Lula: Bolsonaro is far more effective at speaking to that growing middle class'
  > Eve Irvine is pleased to welcome Felipe Krause, the head of Oxford University's Brazilian Studies Programme. Brazil's election reflects a political landscape that has become increasingly polarized, explains Krause. And he describes the current mood as one of “tired polarization: People are just exha
- 2026-10-05 20:37 [France 24] Concerns of US interference weigh on Brazil vote
  > Conservative Senator Flavio Bolsonaro pulled off a surprise on Sunday in the first round of Brazil’s presidential election by finishing ahead of the incumbent left-wing President Lula, whom he will face in the runoff on October 25. Suspicions of U.S. interference have been hanging over the campaign,
- 2026-10-05 21:00 [Al Jazeera] Brazil’s presidential race head for a tough runoff
  > Brazil is heading into a fiercely contested presidential runoff after the first round revealed major gains for Bolsonaro

## U117
**A** (6 item(s))
- 2026-10-02 01:23 [Al Jazeera] Trump says US may ask Europe to release diesel reserves
  > Skyrocketing diesel prices have pushed Washington to weigh an export ban, raising alarm across European economies.
- 2026-10-02 05:26 [BBC World] US pressures Europe over diesel reserves as Trump threatens export ban
  > President Donald Trump has threatened to ban diesel exports in a bid to ease prices in the US ahead of the November elections.
- 2026-10-02 13:16 [Al Jazeera] Trump vs Europe as US presses for release of emergency diesel stocks
  > Europe&#039;s leaders are mulling proposals to respond to Trump&#039;s diesel demands.
- 2026-10-02 14:51 [South China Morning Post] G7 nations agree to release diesel and oil stocks after Trump pressure
  > Group ⁠of Seven countries agreed on Friday to release 100 million barrels of diesel and crude oil from emergency reserves and pledged to refrain from energy export restrictions after pressure from US President Donald Trump.
The US led a pressure campaign on the European Union to draw down emergency 
- 2026-10-02 19:01 [Al Jazeera] Trump says Europe agreed to release ‘massive amount’ of diesel reserves
  > US President Donald Trump says Europe agreed to release a ‘massive amount’ of diesel from emergency stockpiles.
- 2026-10-02 20:25 [BBC World] G7 to release 100 million barrels of oil and diesel after Trump export ban threat
  > The co-ordinated release is aimed at heading off further price spikes and avoiding a ban on US diesel exports.
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

## U118
**A** (2 item(s))
- 2026-10-08 11:18 [BBC Mundo] Cómo llegó Colombia a tener una deuda tan alta (y por qué De la Espriella tendrá que aumentarla)
  > El presupuesto presentado por el gobierno de De la Espriella prevee que la deuda llegará a 66,2% del PIB en 2027, la más alta de la historia del país.
- 2026-10-08 18:55 [France 24 Español] Directo Latam y el apoyo de De la Espriella a exmilitares acusados por asesinato de Jovenel Moïse
  > El presidente colombiano, Abelardo de la Espriella, ha manifestado su apoyo jurídico a 17 exmilitares acusados del magnicidio de Jovenel Moïse en 2021, quienes fueron trasladados a Estados Unidos para comparecer ante la Justicia. En paralelo, el mandatario busca implementar su Estatuto Antiterrorist
**B** (3 item(s))
- 2026-10-08 14:09 [France 24] Search warrants for former prince Andrew's homes were unlawful, UK court rules
  > Police who searched the properties of Andrew Mountbatten-Windsor as part of investigations into his links to the late sex offender Jeffrey Epstein have agreed the search warrants were unlawful, a London judge said Thursday. The 66-year-old younger brother of King Charles II was arrested on February 
- 2026-10-08 15:20 [South China Morning Post] UK police accept ex-prince Andrew search warrants must be ‘legally quashed’
  > British police on Thursday said that search warrants they secured to search properties linked to Andrew Mountbatten-Windsor had been issued unlawfully and must be quashed, but that the investigation into King Charles’ younger brother was ongoing.
Mountbatten-Windsor, 66, was arrested on suspicion of
- 2026-10-08 15:53 [Al Jazeera] UK ex-prince Andrew search warrants quashed after police accept legal error
  > London-based judge says error &#039;does not bring investigation to an end&#039; as police probe disgraced former royal.

## U119
**A** (2 item(s))
- 2026-10-01 14:00 [South China Morning Post] China backs Cuba, Beijing’s Panama threat, new UN chief: 7 Latin America relations reads
  > We have selected seven of the most interesting and important news stories covering Latin American relations from the past few weeks. If you would like to see more of our reporting, please consider subscribing.
1. China pledges to ‘firmly support’ Cuba as US escalates pressure on Havana

China will s
- 2026-10-02 20:52 [Al Jazeera] Latin America sees China as more positive global influence than US: Poll
  > Annual Latinobarometro survey finds views of China’s influence improving as perceptions of US influence worsen.
**B** (2 item(s))
- 2026-10-02 02:07 [Al Jazeera] Everything you need to know about Brazil’s tight presidential race
  > Voters will soon decide between President Luiz Inácio Lula da Silva and the son of former President Jair Bolsonaro.
- 2026-10-02 06:21 [South China Morning Post] Lula and Bolsonaro clash in final scramble for Brazil presidency
  > Brazil’s President Luiz Inacio Lula da Silva and his election rival Flavio Bolsonaro are leaving no controversy unturned in their last-ditch efforts to discredit each other and win over voters ahead of Sunday’s nail-biter election.
A campaign dominated by scandals and insults has done little to ease

## U120
**A** (8 item(s))
- 2026-09-29 14:40 [Defense News] US forces exiting Iraq after 2 decades, leaving opening for Iran
  > U.S. forces are set to depart from their last bases in Iraq by Wednesday, a move celebrated as a victory by Iran and its allies, who now have deep influence in the country where 4,500 Americans died during more than two decades of war.Iraqi security experts say the withdrawal — agreed to in 2024 und
- 2026-09-29 20:00 [Al Jazeera] US troops fully withdraw from Baghdad base after two decades
  > US Army soldiers have fully withdrawn from the US base in Baghdad.
- 2026-09-30 09:46 [South China Morning Post] US ends troop mission in Iraq, Baghdad to celebrate Sovereignty Day on October 1
  > A US-led coalition deployed in Iraq more than a decade ago to fight jihadists concluded its mission on Wednesday, a move celebrated by the country’s leaders, but which some fear will embolden pro-Iran armed factions.
Coalition troops deployed to Iraq and Syria in 2014 to fight Islamic State, which h
- 2026-09-30 11:36 [BBC World] Last UK and US troops leave Iraq as anti-Islamic State mission ends
  > The withdrawal of coalition forces, under a deal agreed two years ago, was a key demand of the Iraqi government.
- 2026-09-30 12:17 [Al Jazeera] Iraq celebrates National Sovereignty Day as US troops withdraw
  > Iraq’s security forces held parades in Baghdad and Najaf to celebrate ‘Sovereignty Day’ as US troops withdraw.
- 2026-09-30 14:04 [Breaking Defense] US withdraws last remaining troops out of Iraq
  > “As we step back and hand full primary responsibility for Iraq’s security to the Government of Iraq and the brave people of Iraq, US and Coalition forces stationed across the region will remain ready to respond to any ISIS threats that arise,” CENTCOM Commander Adm. Brad Cooper said.
- 2026-09-30 16:33 [Al Jazeera] Pentagon says US troop withdrawal from Iraq is complete
  > The withdrawal ends two decades of foreign intervention in Iraq as part of &#039;global war on terror&#039; and anti-ISIL fight.
- 2026-10-01 01:11 [Al Jazeera] Iraq celebrates Sovereignty Day as US troops complete withdrawal
  > Night time celebrations filled the air as Iraqis observed the start of a four-day holiday.
**B** (2 item(s))
- 2026-09-30 03:21 [South China Morning Post] US Supreme Court lets Trump resume deportations to third countries
  > The US Supreme Court on Tuesday let President Donald Trump’s administration continue swiftly deporting people to countries other than their own for now, while the justices consider whether the policy is legal.
The apparent 6-3 order temporarily lifts lower court requirements for migrants to get a ch
- 2026-10-01 17:35 [Al Jazeera] US Supreme Court agrees to take up Trump’s ICE detention policy
  > The case is the latest dispute over US President Donald Trump’s sweeping immigration crackdown.

## U121
**A** (56 item(s))
- 2026-10-04 03:30 [El País Internacional] Ni Bolsonaro, ni Lula: Trump se reserva (de momento) su apoyo en las elecciones de Brasil
  > Un asistente a un mitin de Flavio Bolsonaro disfrazado de Trump, el pasado domingo.
- 2026-10-04 04:00 [El País Internacional] La disputa entre Lula y Trump marca las elecciones brasileñas
  > Banderas de Flavio Bolsonaro y Luiz Inacio Lula da Silva en Brasilia, el 29 de septiembre.
- 2026-10-04 11:20 [Rai News Esteri] Urne aperte in Brasile per le elezioni presidenziali e legislative, sfida Lula-Bolsonaro
  > Gli ultimi sondaggi davano un testa a testa
- 2026-10-04 20:19 [El País Internacional] Brasil decide su futuro entre Lula y Bolsonaro, un estadista desgastado y el hijo de un ultra
  > El presidente Lula, el día 24 en São Gonçalo, y Flávio Bolsonaro, este sábado en Río.
- 2026-10-04 20:43 [Europa Press Internacional] Bolsonaro gana la primera vuelta en Brasil con el 47% de los votos y disputará contra Lula (45%) la segunda vuelta
  > El candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil e hijo del expresidente Jair Bolsonaro, Flávio Bolsonaro, ha ganado la primera vuelta de las elecciones en Brasil con un 47,17% de los sufragios. Su rival y presidente saliente, Luiz Inácio Lula da Silva, ha quedado cua
- 2026-10-04 22:25 [ANSA Mondo] Media, Lula e Bolsonaro andranno al ballottaggio il 25 ottobre
  > A metà scrutinio Bolsonaro al 49%, Lula a 42%
- 2026-10-04 23:00 [Clarín Mundo] Los Bolsonaro amplían su presencia en el Congreso con las elecciones en Brasil: entran la esposa del ex presidente y dos hermanos de Flavio
  > Michelle, la exprimera dama brasileña alcanzó el 28% de los votos en las elecciones legislativas del Distrito Federal.Otros dos hijos del expresidente Jair Bolsonaro compitieron por bancas legislativas en el estado de Santa Catarina.
- 2026-10-04 23:23 [Clarín Mundo] Elecciones en Brasil: Flávio Bolsonaro, un presidenciable a la sombra de su padre
  > Tiene 45 años y es el mayor de los cinco hijos del ex presidente. Elogia las políticas de seguridad de Nayib Bukele en El Salvador y promete la construcción de numerosas cárceles. Asimismo, presume de su buena relación con Donald Trump tras mantener una reunión privada en la Casa Blanca.
- 2026-10-04 23:23 [Clarín Mundo] Lula da Silva busca su reelección en Brasil: entre el freno a la ultraderecha y la defensa de su legado social
  > • A los 80 años, el mandatario brasileño busca la reelección apoyado en su historial de programas sociales como el Bolsa Familia, que actualmente beneficia a una cuarta parte de la población.
• Con vistas a un nuevo período, impulsa una reforma laboral para reducir la jornada semanal a cinco días y 
- 2026-10-05 00:09 [Rai News Esteri] Il sorpasso di Bolsonaro, la crisi di Lula
  > Flavio Bolsonaro, figlio dell'ex presidente di estrema destra tentato golpista, vince il primo turno sul presidente di sinistra Lula da Silva
- 2026-10-05 00:12 [Clarín Mundo] Elecciones en Brasil: un voto castigo que sorprendió a Lula da Silva y llegó desde su base tradicional de votantes
  > Un primer análisis indica que los sectores de menores ingresos se distanciaron de la elección y del líder del PT. El país es un éxito macro, con números notables, pero esos resultados no llegaron a los bolsillos de ese amplio espacio de votantes que se endeuda para pagar los gastos básicos.
- 2026-10-05 01:03 [Clarín Mundo] Lula acepta el impacto del triunfo de Bolsonaro: fue "un resultado inesperado"
  > El representante del socialista Partido de los Trabajadores busca su cuarto mandato, con la reelección en la gestión actual.Quedó detrás de Flavio Bolsonaro por apenas 2,15 puntos.
- 2026-10-05 01:08 [Clarín Mundo] Flavio Bolsonaro, tras ganar en primera vuelta ante Lula: "Brasil quiere un cambio"
  > Aseguró también que este resultado marcan "el fin de la era del PT" en su país.Dijo estar "feliz" con los números obtenidos frente al actual mandatario, Lula da Silva.
- 2026-10-05 01:41 [El País Internacional] Arrasadora victoria de la derecha en Brasil
  > Flavio Bolsonaro habla con la prensa en Río de Janeiro, este domingo.
- 2026-10-05 02:13 [Europa Press Internacional] Bolsonaro proclama "fin de la era del PT" y Lula apela a combatir su "pasado tenebroso" en la segunda vuelta en Brasil
  > Bolsonaro supera los 55 millones de apoyos (47,04%) y logra una ventaja de 2,3 millones de sufragios sobre el actual mandatario (45,15%)
- 2026-10-05 02:28 [El País Internacional] El apellido Bolsonaro gana desde la cárcel
  > Flávio Bolsonaro, candidato presidencial de Brasil, este domingo tras los resultados de la primera vuelta.
- 2026-10-05 02:39 [BBC Mundo] Cómo se compara Flávio Bolsonaro con su padre Jair y cuánto cambia el duelo con Lula por la presidencia de Brasil 4 años después
  > El senador derechista pasa fortalecido al balotaje contra el presidente de izquierda tras obtener más votos en la primera vuelta contra varios pronósticos, pero la elección sigue abierta.
- 2026-10-05 02:46 [France 24 Español] Simone Pitta: "Con esta primera vuelta se puede ver una consolidación del bolsonarismo en Brasil"
  > Pese a no haber estado en el poder en el último periodo presidencial de Brasil, y pese a las denuncias y condenas contra el expresidente Jair Bolsonaro por un intento de golpe de Estado, el bolsonarismo logró consolidarse de cara a los comicios de este 4 de octubre. Ahora, Flávio Bolsonaro busca pos
- 2026-10-05 02:47 [France 24 Español] Juan Agulló: "A diferencia de otros países de Latinoamérica, Brasil es un competidor directo"
  > En un escenario marcado por la polarización en Brasil, el candidato de ultraderecha y heredero político de su padre, Flávio Bolsonaro, y el actual presidente, Luiz Inácio Lula da Silva, quien busca un cuarto mandato, se disputan el balotaje. La sombra de Estados Unidos estuvo presente durante la pri
- 2026-10-05 02:54 [El País Internacional] Bolsonaro vence a Lula en primera vuelta de las elecciones y acaricia el retorno de la ultraderecha al poder en Brasil
  > Flávio Bolsonaro habla tras clasificarse para la segunda vuelta en Brasilia, Brasil, este domingo.
- 2026-10-05 03:19 [France 24 Español] Brasil: la derecha de Bolsonaro se fortalece en las regiones, con un triunfo holgado en São Paulo
  > Los comicios locales de Brasil se saldaron este domingo con un avance de la derecha que representan el candidato presidencial Flávio Bolsonaro y sus aliados. En tanto la izquierda del presidente y aspirante a la reelección, Luiz Inácio Lula da Silva perdía terreno. La victoria más cómoda fue en São 
- 2026-10-05 03:36 [El País Internacional] Las claves de la primera vuelta en Brasil: de la fuerza ultra al día después de Lula con América Latina pendiente
  > Flávio Bolsonaro vota en Río de Janeiro, este domingo.
- 2026-10-05 03:41 [France 24 Español] Flávio Bolsonaro tritura las encuestas: una ventaja pequeña, pero un escenario cuesta arriba para Lula
  > Brasil quedó inclinado hacia la tendencia de retorno a la derecha que sacude a América Latina, luego de que el senador e hijo del expresidente Jair Bolsonaro aventajara por casi dos puntos al izquierdista Luiz Inácio Lula da Silva en la primera vuelta de las elecciones. Lula ha reconocido el resulta
- 2026-10-05 04:08 [El País Internacional] Videoanálisis | Lula se enfrenta a una segunda vuelta electoral muy complicada
  > Videoanálisis | Lula Y Flávio Bolsonaro se enfrenta a una segunda vuelta electoral
- 2026-10-05 04:33 [Rai News Esteri] Brasile, avanzata del clan Bolsonaro: quattro eletti in Parlamento, Flavio al ballottaggio con Lula
  > L'ex first lady Michelle e Carlos, uno dei figli dell'ex presidente, conquistano un seggio al Senato. Alla Camera entrano il figlio più giovane Jair Renan e Renato, fratello di Jair
- 2026-10-05 05:14 [Il Sole 24 Ore Mondo] Brasile, Bolsonaro vince al primo turno con 47%, Lula al 45%: ballottaggio il 25 ottobre
  > Flavio Bolsonaro batte Lula al primo turno e si lancia come favorito nel ballottaggio del 25 ottobre che deciderà chi sarà il 40esimo presidente del Brasile. Il candidato trumpiano ha ottenuto il 47,14 % dei voti, il presidente uscente il 45.03 %, con una differenza tra i due di circa 2 milioni e me
- 2026-10-05 05:31 [Europa Press Internacional] Trump tacha de "corruptas" las elecciones de EEUU comparándolas con las de Brasil tras la victoria de Bolsonaro
  > El presidente de Estados Unidos, Donald Trump, ha vuelto a cargar contra el proceso electoral en su propio país, tachándolo de corrupto y contraponiéndolo la rapidez en el escrutinio de los votos de 125 millones de personas "en la primera vuelta de las elecciones presidenciales de Brasil", donde el 
- 2026-10-05 05:46 [Europa Press Internacional] Milei felicita a su "querido amigo" Flávio Bolsonaro por su "histórica elección" frente a Lula en Brasil
  > El presidente de Argentina, Javier Milei, ha felicitado al candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil, Flávio Bolsonaro, por su victoria en la primera vuelta de las elecciones presidenciales celebradas este domingo, en las que se ha impuesto con el 47,03% de los vo
- 2026-10-05 06:44 [ANSA Mondo] Brasile, l'ex giudice che condannò Lula eletto governatore
  > Sergio Moro guiderà l'esecutivo del suo stato natale, il Paranà
- 2026-10-05 07:14 [BBC Mundo] Elecciones en Brasil: Flávio Bolsonaro y Lula da Silva van a una segunda vuelta en la que el presidente enfrenta una difícil remontada
  > La mayor democracia de América Latina irá a balotaje el 25 de octubre. Lula lleva la desventaja frente a Bolsonaro, ya que históricamente nunca hubo una remontada en una segunda vuelta electoral en Brasil.
- 2026-10-05 07:46 [ANSA Mondo] In Brasile un 30enne di destra è il deputato più votato della storia
  > Nikolas Ferreira ha raccolto oltre 3,1 milioni di preferenze per la Camera
- 2026-10-05 10:46 [ANSA Mondo] Astensione record in Brasile, il 21,08% non ha votato al primo turno
  > Si tratta del livello più alto registrato dalle elezioni del 1998 (21,5%)
- 2026-10-05 11:42 [France 24 Español] Brasil irá a segunda vuelta: Flávio Bolsonaro lidera la primera ronda
  > Brasil se encamina a una segunda vuelta presidencial tras una elección marcada por la polarización. El senador Flávio Bolsonaro obtuvo el primer lugar en la primera vuelta, pero sin alcanzar la mayoría necesaria para evitar el balotaje. El próximo 25 de octubre se enfrentará al actual presidente, Lu
- 2026-10-05 12:20 [Rai News Esteri] Il primo turno delle presidenziali in Brasile, avanti Bolsonaro: ribaltati i pronostici pro-Lula
  > La sfida per il secondo turno del 25 ottobre è ancora aperta ma il presidente uscente non minimizza il peso di una pesante bocciatura delle sue politiche
- 2026-10-05 12:21 [Rai News Esteri] Presidenziali in Brasile, Flavio Bolsonaro a sorpresa supera Lula di 2 punti. Si va al ballottaggio
  > Il candidato di destra al 47%: "Il Brasile vuole cambiare". Il presidente uscente al 45%: "Sono bravo ai supplementari". Scelta rinviata al secondo turno del 25 ottobre
- 2026-10-05 12:29 [Clarín Mundo] Elecciones en Brasil 2026, EN VIVO: reacciones tras la victoria de Flávio Bolsonaro sobre Lula y últimas noticias del balotaje
  > Bolsonaro se impuso en la primera vuelta al superar por casi dos puntos al actual presidente Lula da Silva. El balotaje entre ambos se hará el 25 de octubre. Todas las repercusiones, minuto a minuto.
- 2026-10-05 12:31 [Clarín Mundo] Quién es Flávio Bolsonaro, el hijo de Jair que sorprendió a Lula y va por la presidencia de Brasil
  > Nacido en el estado de Río de Janeiro, Flávio es el mayor de los cinco hijos del expresidente y el que más se le parece físicamente.Este senador, de 45 años, enfrentará a Lula en el balotaje el próximo 25 de octubre.
- 2026-10-05 13:05 [France 24 Español] Informe desde Río de Janeiro: el Partido Liberal de Bolsonaro se fortalece en el Senado
  > Las elecciones legislativas en Brasil dejaron un resultado clave para el futuro político del país: el Partido Liberal (PL), formación vinculada al expresidente Jair Bolsonaro y que postuló a Flávio Bolsonaro para la Presidencia, amplió significativamente su presencia en el Senado. La bancada pasará 
- 2026-10-05 13:16 [Clarín Mundo] Elecciones en Brasil: los mercados celebran la ventaja de Flávio Bolsonaro sobre Lula y el principal índice de la Bolsa marca un nuevo récord
  > Los activos brasileños se dispararon este lunes y el real se apreció en la primera sesión de los mercados tras los comicios del domingo. El índice Ibovespa superó la marca de los 209.000 puntos por primera vez.
- 2026-10-05 13:57 [BBC Mundo] Quiénes son Lucas Pavanato y Nikolas Ferreira, los jóvenes influencers de derecha que lograron las mayores votaciones en la historia de la Cámara de Diputados de Brasil
  > Los flamantes legisladores comparten una agenda conservadora que incluye el rechazo a las políticas de género, el endurecimiento de las sanciones penales y la legalización del porte de armas como herramienta para combatir la delincuencia.
- 2026-10-05 14:50 [Clarín Mundo] Elecciones en Brasil: los resultados del domingo cambian por completo el diseño del país y ya asoma una amnistía para Jair Bolsonaro
  > La victoria del candidato conservador Flávio Bolsonaro sobre el presidente Lula da Silva en primera vuelta excede lo que pueda ocurrir en el balotaje.La ola de derecha se consolida con victorias en las gobernaciones y especialmente en el Parlamento.Aun si el líder petista lograra imponerse el 25 de 
- 2026-10-05 15:47 [Clarín Mundo] La reacción de los medios en Brasil tras la victoria de Bolsonaro: desde "el ciclo de Lula está terminado" hasta "el tsunami de lo peor de la derecha"
  > Los títulos, opiniones y análisis de la prensa en Brasil tras la primera vuelta de las presidenciales de este domingo.
- 2026-10-05 15:59 [France 24 Español] Flávio Bolsonaro y Lula da Silva se preparan para el balotaje en Brasil
  > 🇧🇷🗳️ Luiz Inácio Lula da Silva y Flávio Bolsonaro ofrecieron declaraciones después de que los resultados de los comicios presidenciales de Brasil confirmaran que deberán disputar el balotaje del 25 de octubre.
- 2026-10-05 16:02 [El País Internacional] El lulismo cruje ante la ofensiva ultra
  > Carteles del presidente Trump y del candidato Flavio Bolsonaro, en São Paulo, Brasil, este Lunes.
- 2026-10-05 16:10 [France 24 Español] "Solo faltan días para el rescate Brasil": Bolsonaro celebra la victoria sobre Lula
  > El senador del Partido Liberal (PL) y candidato presidencial, Flávio Bolsonaro, agradeció este lunes "a Dios" y al pueblo brasileño por su victoria en las elecciones del domingo ante el presidente Luiz Inácio Lula da Silva, en contra de los pronósticos. Además, celebró que el PL resultara el partido
- 2026-10-05 16:23 [Clarín Mundo] Elecciones en Brasil: a contrarreloj, Lula y el PT analizan cambios totales en la estrategia de campaña
  > Lo anticipan fuentes partidarias, pero no es claro en qué consistirán. Trascendió que ha habido tensiones internas sobre el manejo de la campaña.Y que debido a eso se perdieron oportunidades importantes para reducir el impulso del candidato opositor, Flávio Bolsonaro.
- 2026-10-05 16:36 [France 24 Español] Paraguay, refugio fiscal y político para la extrema derecha brasileña
  > En los últimos cinco años, las solicitudes de permisos de residencia de brasileños en Paraguay se han más que duplicado. Muchos de los recién llegados son simpatizantes de Jair Bolsonaro que temen una reelección del actual presidente, Luiz Inácio Lula da Silva, a quien responsabilizan de un deterior
- 2026-10-05 17:02 [ANSA Mondo] Brasile, Erika Hilton è la donna più votata della storia alla Camera
  > La politica brasiliana Erika

Hilton ha stabilito un nuovo record nella storia della Camera

dei deputati brasiliana, diventando la donna più votata di

sempre. La deputata trans del Partito socialismo e libertà

(Psol) di San Paolo è stata rieletta con 1.596.472 voti, pari al

5,9% dei voti espress
- 2026-10-05 17:30 [Clarín Mundo] El fantasma de Bolsonaro reaparece en Europa: los temores de Bruselas ante un eventual cambio de gobierno en Brasil
  > • Un cambio de gobierno en Brasil aportaría argumentos a los eurodiputados que buscan frenar la ratificación del entendimiento comercial.
• Si entre 50 y 80 legisladores modifican su postura en la votación prevista para los próximos meses, la aplicación provisional del pacto quedará suspendida.
- 2026-10-05 18:04 [France 24 Español] El mercado de valores de Brasil aplaude la ventaja de Bolsonaro en primera vuelta presidencial
  > El índice bursátil iBovespa, el más importante de la bolsa de São Paulo inició la jornada con un alza estrepitosa de casi el 9% y alcanzó máximo histórico, mientras el real brasileño gana 4,5% frente al dólar a media jornada, hasta situarse ligeramente por encima de los 5 reales por dólar. El buen r
- 2026-10-05 18:10 [France 24 Español] La dinastía Bolsonaro se fortalece: prensa brasileña sobre la primera vuelta electoral
  > La familia Bolsonaro no solo ganó la primera vuelta en Brasil, fortaleció su presencia en ambas cámaras del Congreso y conserva los respaldos de más de 10 gobernadores. 'O Globo' habla del bloque familiar que se ha hecho con varios cargos. Hermanos, hijos, esposa y exesposa tienen un puesto de elecc
- 2026-10-05 19:41 [El País Internacional] La ola conservadora de América Latina llega a Brasil
  > Flávio Bolsonaro (i) junto al presidente de EE.UU., Donald Trump, en el despacho oval de la Casa Blanca en Washington, el 26 de mayo de 2026.
- 2026-10-05 19:42 [El País Internacional] La victoria en primera vuelta de Bolsonaro impulsa a la ola ultra de América Latina
  > Transeúntes pasan ante pósteres dañados que muestran a Bolsonaro hijo con el presidente Trump, este lunes en São Paulo.
- 2026-10-05 19:47 [Clarín Mundo] Elecciones en Brasil: las urnas de la sorpresa
  > Tras el imprevisto triunfo de Flávio Bolsonaro sobre Lula en la primera vuelta, Brasil se encamina hacia un balotaje decisivo el próximo 25 de octubre. La contienda electoral ratifica la profunda polarización política del país y la consolidación del bolsonarismo como una fuerza de derecha permanente
- 2026-10-05 20:21 [ANSA Mondo] Trump, il risultato di Bolsonaro in Brasile una 'grande vittoria'
  > Il risultato di Flavio Bolsonaro

alle elezioni in Brasile è stata una "grande vittoria". Lo ha

detto Donald Trump.Quella di Bolsonaro "è una grande vittoria: combattuta, ma una

vittoria davvero enorme. Incredibile", ha detto Trump. Bolsonaro

si avvia al ballottaggio del 25 ottobre come favorito.
- 2026-10-05 22:09 [ANSA Mondo] Brasile, l'ex presidente Temer sostiene Bolsonaro al ballottaggio
  > L'ex presidente brasiliano

Michel Temer (2016-2018) ha dichiarato il suo sostegno a Flávio

Bolsonaro in vista del ballottaggio del 25 ottobre contro Luiz

Inácio Lula da Silva. In un video diffuso sui social, Temer ha

affermato che il risultato del primo turno mostra la volontà

degli elettori di
**B** (2 item(s))
- 2026-10-04 15:06 [Al Jazeera] Iran tells US: there is ‘no military solution’ to end the war
  > Iranian Foreign Minister Abbas Araghchi says the era of “wasting time and dictating demands is over’.
- 2026-10-04 19:44 [South China Morning Post] Iran tells US there is no military solution to Middle East war
  > Iran’s top diplomat insisted on Sunday that there would be no military solution to the United States’ war against the Islamic republic, with talks on ending the conflict apparently at an impasse.
A campaign of heavy bombardment failed to bring a decisive close to the war launched by the US and Israe

## U122
**A** (2 item(s))
- 2026-10-04 15:06 [Al Jazeera] Iran tells US: there is ‘no military solution’ to end the war
  > Iranian Foreign Minister Abbas Araghchi says the era of “wasting time and dictating demands is over’.
- 2026-10-04 19:44 [South China Morning Post] Iran tells US there is no military solution to Middle East war
  > Iran’s top diplomat insisted on Sunday that there would be no military solution to the United States’ war against the Islamic republic, with talks on ending the conflict apparently at an impasse.
A campaign of heavy bombardment failed to bring a decisive close to the war launched by the US and Israe
**B** (2 item(s))
- 2026-10-04 18:17 [South China Morning Post] Dozens detained at a rally in Moscow held by Kremlin-friendly Communist Party, party says
  > Police in Moscow detained about 60 people at a rally on Sunday held by Russia’s Kremlin-friendly Communist Party, the party said.
The party said in a statement that the detentions happened as the rally was ending and that its Moscow branch was working to get those who were detained – mostly young pe
- 2026-10-04 23:30 [Kyiv Independent] Dozens detained at authorized Russian Communist Party rally after chants of 'Down with the Tsar'
  > The event had been authorized by Moscow authorities, but detentions reportedly intensified as the rally was ending and participants shifted toward more directly anti-Kremlin slogans.

## U123
**A** (2 item(s))
- 2026-10-03 12:22 [BBC Mundo] Lo que la fallida ejecución de Christa Pike revela sobre la pena de muerte en EE.UU.
  > Christa Pike, una mujer condenada a muerte en Tennessee, sobrevivió a la aplicación de dos inyecciones letales. Su caso ha vuelto a centrar la atención en la pena de muerte y en cómo se aplica en Estados Unidos.
- 2026-10-03 19:14 [Il Sole 24 Ore Mondo] Trump vuole estendere la pena di morte ai narcotrafficanti: il caso Pike riapre lo scontro
  > Il presidente promette di ampliare i reati punibili con la pena capitale. Il Tennessee sospende le esecuzioni dopo il caso Pike, mentre una sentenza della Corte Suprema del 2008 lascia aperto il nodo dei grandi narcotrafficanti
**B** (10 item(s))
- 2026-10-04 20:31 [El País Internacional] El Gobierno de Yemen anuncia una ofensiva para recuperar los territorios en manos de los hutíes
  > El humo se eleva desde el lugar donde se ha producido un ataque aéreo saudí en Saná, Yemen, este domingo.
- 2026-10-05 05:25 [Il Sole 24 Ore Mondo] Yemen, forze governative riprendono controllo di Bab el Mandeb e attaccano Houthi nella capitale Sanaa
- 2026-10-05 08:21 [ANSA Mondo] Media, forze governative yemenite attaccano gli Houthi vicino a Bab el Mandeb
  > Ieri il governo riconosciuto ha lanciato contro-offensiva
- 2026-10-05 09:51 [ANSA Mondo] Forze governative Yemen, ripreso il controllo di Bab el Mandeb
  > E dell'aeroporto di Dhubab
- 2026-10-05 15:55 [Europa Press Internacional] Rubio asegura que EEUU cumplirá sus pactos de seguridad con Arabia Saudí en plena contraofensiva en Yemen
  > El secretario de Estado estadounidense, Marco Rubio, ha señalado este lunes la intención de Washington de cumplir los pactos en materia de seguridad con Arabia Saudí, sin entrar en más detalles sobre el apoyo estadounidense en plena contraofensiva en Yemen en el que la coalición internacional lidera
- 2026-10-05 17:10 [ANSA Mondo] Lo Yemen riconquista il controllo dello Stretto di Bab el-Mandeb
  > Gli Houthi hanno affermato di aver colpito l'aeroporto di Riad e una raffineria del colosso energetico saudita Aramco, oltre a diversi siti nel sud del Regno. Gli attacchi, condotti soprattutto con droni, missili balistici e da crociera, "hanno preso di mira l'aeroporto internazionale di Riad", ha d
- 2026-10-05 19:05 [El País Internacional] El Gobierno yemení asegura haber arrebatado el control del estrecho de Bab el Mandeb a los hutíes
  > Refuerzos militares yemeníes se desplazan por la carretera costera entre Adén y Mokha, en Yemen, este lunes.
- 2026-10-05 19:09 [ANSA Mondo] Turchia e Pakistan invieranno forze militari in Arabia Saudita
  > (v. 'Lo Yemen riconquista il controllo...' delle 20:37)

(ANSA-AFP) - RIAD, 05 OTT - La Turchia e il Pakistan, legati

all'Arabia Saudita da un patto di difesa reciproca, hanno

annunciato in un comunicato congiunto l'invio di forze militari

nel Regno, bersaglio di attacchi regolari da parte dei

c
- 2026-10-05 20:33 [Europa Press Internacional] Los hutíes lanzan una oleada de misiles y drones contra objetivos militares y económicos saudíes
  > Las milicias hutíes de Yemen han informado este lunes del lanzamiento de una serie de misiles y drones contra objetivos militares y económicos dentro del territorio saudí en represalia por los bombardeos saudíes en Yemen.
- 2026-10-05 20:54 [Rai News Esteri] Yemen: l'avanzata di una milizia sostenuta dall'Arabia Saudita
  > Una milizia sostenuta dall’Arabia Saudita rivendica “avanzate significative” a Dhubab

## U124
**A** (5 item(s))
- 2026-10-04 23:23 [Clarín Mundo] Alerta en Rusia: murió una científica por un accidente con bacterias en un laboratorio y debieron aislar a 200 personas
  > Contó que se le rompió un tubo de ensayo recolectando muestras para analizar.Autoridades rusas dicen que el frío impediría la transmisión de un tipo de neumonía.Los funcionarios hablan de "una peste no especificada" y "una infección particularmente peligrosa".
- 2026-10-05 06:53 [Europa Press Internacional] Rusia asegura que la situación epidemiológica en Irkutsk es "estable" tras un supuesto accidente en un laboratorio
  > Las autoridades de Rusia han asegurado que la situación epidemiológica en la región de Irkutsk es "estable", después de activar una serie de medidas de emergencia durante los últimos días a causa de la muerte de una investigadora en un presunto accidente de laboratorio en Shelejov.
- 2026-10-05 10:17 [El País Internacional] Rusia pone bajo observación a cientos de personas tras morir una investigadora de un laboratorio contra la peste
  > Trabajos de desinfección de coranavirus en la estación de tren de Yaroslavsky en Moscú, el 10 de noviembre de 2022.
- 2026-10-05 14:34 [Europa Press Internacional] EEUU pide a Rusia compartir información "de forma rápida y transparente" tras supuesto caso de peste en Irkutsk
  > El Departamento de Estado estadounidense ha instado este lunes a las autoridades de Rusia a compartir información "de forma rápida y transparente" sobre el caso de presunta peste pulmonar en la región de Irkutsk, tras la muerte de una investigadora en un presunto accidente de laboratorio en Shelejov
- 2026-10-05 21:21 [BBC Mundo] EE.UU. "sigue de cerca" el caso de una científica rusa que falleció en un centro de investigación de la peste en Siberia
  > El secretario de Estado, Marco Rubio, expresó su preocupación de que el incidente pudiera haber provocado la propagación de la peste neumónica, aunque señaló que no había motivos para alarmarse.
**B** (5 item(s))
- 2026-10-05 04:07 [Al Jazeera] Russian lab worker dies of suspected plague in Siberia; US monitoring case
  > A Russian agency links the lab worker&#039;s death to &#039;pneumonia of unknown&#039; origin.
- 2026-10-05 17:14 [South China Morning Post] After plague death reports at Siberia lab, Russia says situation under control
  > Moscow on Monday downplayed reports that a laboratory technician had died of plague, stressing that postmortem tests had not detected the disease, while Washington said it was closely monitoring the situation.
Reports on Friday that plague had killed a 28-year-old woman named Darya Shipilova, who ha
- 2026-10-05 19:19 [France 24] Russian officials say 'situation under control' after plague reports
  > Moscow on Monday downplayed reports that a laboratory technician had died of plague, stressing that post-mortem tests had not detected the disease, while Washington said it was closely monitoring the situation. Reports on Friday that plague had killed a 28-year-old woman named Darya Shipilova, who h
- 2026-10-05 19:55 [BBC World] US 'watching closely' after plague researcher dies in Russia, Rubio says
  > The US says it is monitoring the case of a lab technician who died at a plague research centre in Siberia.
- 2026-10-05 21:03 [Al Jazeera] Trump says US ready to aid Russia with plague outbreak in Siberia
  > Russian authorities quarantine hospital, monitor 200 contacts after suspected pneumonic plague death in Siberia.

## U125
**A** (3 item(s))
- 2026-10-07 23:08 [BBC Mundo] Por qué la mayor colonia de pingüinos del mundo ha perdido dos tercios de su población
  > Se atribuye al cambio climático el drástico declive de los pingüinos barbijo que habitan en una remota isla volcánica.
- 2026-10-08 02:44 [France 24 Español] Ecuador: jueza declara inocentes a 32 pescadores de lanchas atacadas por EE. UU. en el Pacífico
  > Una jueza declaró inocentes a 32 pescadores tripulantes de dos de las lanchas atacadas por Estados Unidos en el océano Pacífico, que habían sido procesados previamente por la Fiscalía por presunta asociación ilícita con grupos delincuenciales. Nuestra corresponsal Carolina Mella nos amplió la inform
- 2026-10-08 19:31 [Clarín Mundo] "El estrecho de Magallanes fue, es y será siempre chileno": la dura respuesta del canciller tras los dichos del embajador de Estados Unidos
  > Francisco Pérez Mackenna rechazó los dichos de Brandon Judd y remarcó que Chile cuenta con capacidad propia para resguardar el Estrecho de Magallanes. La controversia diplomática por la vía marítima se suma a la nota de protesta presentada semanas atrás contra la Argentina por una afirmación similar
**B** (3 item(s))
- 2026-10-08 14:09 [France 24] Search warrants for former prince Andrew's homes were unlawful, UK court rules
  > Police who searched the properties of Andrew Mountbatten-Windsor as part of investigations into his links to the late sex offender Jeffrey Epstein have agreed the search warrants were unlawful, a London judge said Thursday. The 66-year-old younger brother of King Charles II was arrested on February 
- 2026-10-08 15:20 [South China Morning Post] UK police accept ex-prince Andrew search warrants must be ‘legally quashed’
  > British police on Thursday said that search warrants they secured to search properties linked to Andrew Mountbatten-Windsor had been issued unlawfully and must be quashed, but that the investigation into King Charles’ younger brother was ongoing.
Mountbatten-Windsor, 66, was arrested on suspicion of
- 2026-10-08 15:53 [Al Jazeera] UK ex-prince Andrew search warrants quashed after police accept legal error
  > London-based judge says error &#039;does not bring investigation to an end&#039; as police probe disgraced former royal.

## U126
**A** (3 item(s))
- 2026-10-07 23:08 [BBC Mundo] Por qué la mayor colonia de pingüinos del mundo ha perdido dos tercios de su población
  > Se atribuye al cambio climático el drástico declive de los pingüinos barbijo que habitan en una remota isla volcánica.
- 2026-10-08 02:44 [France 24 Español] Ecuador: jueza declara inocentes a 32 pescadores de lanchas atacadas por EE. UU. en el Pacífico
  > Una jueza declaró inocentes a 32 pescadores tripulantes de dos de las lanchas atacadas por Estados Unidos en el océano Pacífico, que habían sido procesados previamente por la Fiscalía por presunta asociación ilícita con grupos delincuenciales. Nuestra corresponsal Carolina Mella nos amplió la inform
- 2026-10-08 19:31 [Clarín Mundo] "El estrecho de Magallanes fue, es y será siempre chileno": la dura respuesta del canciller tras los dichos del embajador de Estados Unidos
  > Francisco Pérez Mackenna rechazó los dichos de Brandon Judd y remarcó que Chile cuenta con capacidad propia para resguardar el Estrecho de Magallanes. La controversia diplomática por la vía marítima se suma a la nota de protesta presentada semanas atrás contra la Argentina por una afirmación similar
**B** (2 item(s))
- 2026-10-08 08:06 [State Department] Secretary of State Marco Rubio Remarks to the Press
  > Marco Rubio, Secretary of State
Athens, Greece
Athens International Airport



	

		
		

			

		

		

			

				
				

					
						Secretary of State Marco Rubio Remarks to the Press
					
				

				

					

					
					
						Remarks

					
					
					
			

			
			

			
			October 8, 2026

			
				


- 2026-10-08 13:38 [Al Jazeera] Rubio praises nationalism and ties ‘America First’ values to ancient Greece
  > US Secretary of State Marco Rubio urged Western nations to prioritise their own interests in a speech in Athens.

## U127
**A** (5 item(s))
- 2026-09-29 12:00 [South China Morning Post] US and China need shared risk vocabulary to manage AI threats: Beijing-linked think tank
  > Beijing and Washington should first develop a common language around AI risks rather than seek to resolve their broader technology rivalry, a leading Chinese think tank has advised.
The call from the China Institutes of Contemporary International Relations (CICIR), affiliated with the Ministry of St
- 2026-09-29 16:09 [BBC World] Trump rules out joint US-China venture to develop AI
  > The US president continues to push back on calls to establish guardrails around artificial intelligence, arguing it will stifle growth.
- 2026-09-29 19:32 [South China Morning Post] Trump rejects calls to work with China on AI safety despite Xi summit progress
  > US President Donald Trump said on Tuesday he does not want to work with China on addressing artificial intelligence (AI) risks, arguing that cooperation could undermine America’s lead in the fast-moving technology.
“Whoever wins superintelligence wins. You’re gonna have a winner and a loser, and you
- 2026-09-29 23:43 [Al Jazeera] Trump, tech bosses sign voluntary pact pledging ‘robust’ AI safeguards
  > US President Trump touts self-regulation amid the international community&#039;s and industry&#039;s calls for formal rules.
- 2026-09-30 05:00 [South China Morning Post] Chinese firms trail global peers on profits, but AI power boom offers bright spot: Natixis
  > China’s corporate sector remains considerably weaker than it was before the Covid-19 pandemic, but the country is emerging as a key beneficiary of the global artificial intelligence boom thanks to its ample power capacity, according to a Natixis survey of thousands of firms and a separate research r
**B** (14 item(s))
- 2026-09-29 23:39 [BBC World] US Supreme Court denies Christa Pike's last-ditch bid to halt execution
  > The Tennessee inmate has been awaiting execution since she was sentenced to death in 1996 for the murder of a teenage classmate.
- 2026-09-30 13:14 [Al Jazeera] Christa Pike seeks firing squad, not lethal injection: Inside US executions
  > Women make up about 1 percent of US executions. How do states put people to death, and why is it contested?
- 2026-09-30 15:29 [BBC World] Execution of US murderer Christa Pike halted shortly before it was due to happen
  > Pike was convicted and sentenced to death in 1996 for the murder of Colleen Slemmer.
- 2026-09-30 16:00 [South China Morning Post] US Tennessee’s first execution of a woman in 200 years halted
  > A US appeal court on Wednesday halted the ⁠execution of death row inmate Christa Pike in Tennessee, less than two hours before she was scheduled to become the first woman that state has put to death in more than 200 years.
The 6th US Circuit Court of Appeals ordered a “short stay of execution” to gi
- 2026-09-30 16:44 [Al Jazeera] US appeals court halts Tennessee execution of Christa Pike
  > Christa Pike was set to become the first woman executed by Tennessee in more than 200 years.
- 2026-09-30 23:42 [BBC World] US Supreme Court allows execution of Christa Pike to go ahead
  > The death by lethal injection was scheduled to happen earlier on Wednesday before judges from a lower court paused the execution.
- 2026-10-01 02:35 [Al Jazeera] Christa Pike’s execution by lethal injection fails in Tennessee
  > Witnesses say Tennessee officials were unable to execute Christa Pike after a lethal injection attempt.
- 2026-10-01 04:14 [South China Morning Post] Tennessee halts executions after Christa Pike survives 2 doses of lethal drug
  > Tennessee officials were unable to put Christa Pike to death on Wednesday for a 1995 murder after administering two doses of a lethal drug. A death penalty expert said it was an unprecedented failure, and Tennessee’s governor halted the remaining execution for the rest of the year.
Pike, 50, was ali
- 2026-10-01 04:55 [Al Jazeera] Execution of US woman Christa Pike fails after botched lethal injection
  > The high-profile execution of murderer Christa Pike is in disarray after two lethal injections failed to kill her.
- 2026-10-01 16:45 [BBC World] Tennessee halts executions after Christa Pike survives two lethal injection attempts
  > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
- 2026-10-02 03:02 [South China Morning Post] Christa Pike in ‘life-saving care’ after botched Tennessee execution
  > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from a prison execution c
- 2026-10-02 07:58 [Al Jazeera] Lawyers for US inmate who survived lethal injections demand release
  > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
- 2026-10-02 20:32 [BBC World] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say
  > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.
- 2026-10-02 20:57 [Al Jazeera] Christa Pike unconscious, on ventilator after botched execution: Lawyers
  > The Tennessee woman&#039;s legal team says doctors are working to clear doses of the drug pentobarbital from her system.

## U128
**A** (14 item(s))
- 2026-09-29 23:39 [BBC World] US Supreme Court denies Christa Pike's last-ditch bid to halt execution
  > The Tennessee inmate has been awaiting execution since she was sentenced to death in 1996 for the murder of a teenage classmate.
- 2026-09-30 13:14 [Al Jazeera] Christa Pike seeks firing squad, not lethal injection: Inside US executions
  > Women make up about 1 percent of US executions. How do states put people to death, and why is it contested?
- 2026-09-30 15:29 [BBC World] Execution of US murderer Christa Pike halted shortly before it was due to happen
  > Pike was convicted and sentenced to death in 1996 for the murder of Colleen Slemmer.
- 2026-09-30 16:00 [South China Morning Post] US Tennessee’s first execution of a woman in 200 years halted
  > A US appeal court on Wednesday halted the ⁠execution of death row inmate Christa Pike in Tennessee, less than two hours before she was scheduled to become the first woman that state has put to death in more than 200 years.
The 6th US Circuit Court of Appeals ordered a “short stay of execution” to gi
- 2026-09-30 16:44 [Al Jazeera] US appeals court halts Tennessee execution of Christa Pike
  > Christa Pike was set to become the first woman executed by Tennessee in more than 200 years.
- 2026-09-30 23:42 [BBC World] US Supreme Court allows execution of Christa Pike to go ahead
  > The death by lethal injection was scheduled to happen earlier on Wednesday before judges from a lower court paused the execution.
- 2026-10-01 02:35 [Al Jazeera] Christa Pike’s execution by lethal injection fails in Tennessee
  > Witnesses say Tennessee officials were unable to execute Christa Pike after a lethal injection attempt.
- 2026-10-01 04:14 [South China Morning Post] Tennessee halts executions after Christa Pike survives 2 doses of lethal drug
  > Tennessee officials were unable to put Christa Pike to death on Wednesday for a 1995 murder after administering two doses of a lethal drug. A death penalty expert said it was an unprecedented failure, and Tennessee’s governor halted the remaining execution for the rest of the year.
Pike, 50, was ali
- 2026-10-01 04:55 [Al Jazeera] Execution of US woman Christa Pike fails after botched lethal injection
  > The high-profile execution of murderer Christa Pike is in disarray after two lethal injections failed to kill her.
- 2026-10-01 16:45 [BBC World] Tennessee halts executions after Christa Pike survives two lethal injection attempts
  > Pikeâs lawyers have asked for her death sentence to be commuted following the botched execution.
- 2026-10-02 03:02 [South China Morning Post] Christa Pike in ‘life-saving care’ after botched Tennessee execution
  > A condemned female murderer who survived two lethal injections during a botched execution by the US state of Tennessee was in critical condition and receiving “life-saving care”, her lawyer said on Thursday.
In an extraordinary chain of events, Christa Pike, 50, was whisked from a prison execution c
- 2026-10-02 07:58 [Al Jazeera] Lawyers for US inmate who survived lethal injections demand release
  > Christa Pike is in critical condition after two failed attempts to execute her by lethal injection, her lawyer says.
- 2026-10-02 20:32 [BBC World] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say
  > As of Thursday night, Pike remained critically ill and is being treated at a hospital in Nashville, Tennessee.
- 2026-10-02 20:57 [Al Jazeera] Christa Pike unconscious, on ventilator after botched execution: Lawyers
  > The Tennessee woman&#039;s legal team says doctors are working to clear doses of the drug pentobarbital from her system.
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

## U129
**A** (14 item(s))
- 2026-10-04 11:15 [Al Jazeera] Brazil votes in deeply polarised election pitting Lula against Bolsonaro
  > Close race expected as left-wing leader Lula seeks fourth nonconsecutive term against right-wing Flavio Bolsonaro.
- 2026-10-04 17:48 [South China Morning Post] Brazilians head to polls in high-stakes, polarised election
  > Brazilians queued to vote on Sunday in the first round of a tight election, following a campaign dominated by corruption scandals, economic anxiety and accusations of US meddling.
The field of 13 candidates has been led by two clear front runners – leftist President Luiz Inacio Lula da Silva, 80, wh
- 2026-10-04 21:11 [BBC World] Polls close in Brazil as Lula and Flávio Bolsonaro remain neck and neck
  > If no candidate gets more than 50% of the vote, the election will go to a run-off on 25 October.
- 2026-10-05 00:27 [DW World] Brazil election: Bolsonaro and Lula head to runoff
  > Populist Flavio Bolsonaro has secured a thin lead over incumbent Luiz Inacio Lula da Silva, but the next president of Brazil will be decided in the runoff round, according to the country’s electoral court.
- 2026-10-05 03:16 [BBC World] Right-wing Flávio Bolsonaro wins first round of Brazil election
  > With neither candidate getting more than 50% of the vote, the election will go to a run-off on 25 October.
- 2026-10-05 04:51 [BBC World] Watch: How Brazil's dramatic election unfolded
  > Millions of Brazilians took to the polls on Sunday for the first round of the country's presidential elections.
- 2026-10-05 05:08 [Al Jazeera] Bolsonaro beats expectations in Brazil vote, faces Lula in runoff
  > Brazil’s presidential election is heading to a run-off after Bolsonaro and Lula both fell short of the 50% needed to win
- 2026-10-05 09:38 [France 24] Brazil heads to run-off as Bolsonaro pulls off shock first place finish in first round
  > Flavio Bolsonaro, a right-wing senator and son of former president Jair Bolsonaro, pulled off a surprise first-place finish ahead of President Luiz Inacio Lula da Silva in Brazil’s election Sunday. However, with neither candidate securing a majority the vote now heads to a run-off in three weeks.
- 2026-10-05 09:46 [South China Morning Post] Brazil-China ties in focus as Bolsonaro gets election edge over Lula
  > Brazil is set for a presidential run-off after right-wing challenger Flavio Bolsonaro won a surprise first-round victory, threatening Luiz Inacio Lula da Silva’s grip on power in South America’s largest economy.
Bolsonaro, son of imprisoned former president Jair Bolsonaro, took 47 per cent of the ba
- 2026-10-05 12:34 [Al Jazeera] Bolsonaro favourite to win: What Brazil’s first round of elections tells us
  > Analysts say Flavio Bolsonaro is projected to win the run-off vote on October 25 and become Brazil&#039;s next president.
- 2026-10-05 12:52 [France 24] Brazil presidential election: 'Bolsonaro being ahead is a surprise,' researcher says
  > Far-right candidate Flavio Bolsonaro has pulled off a surprise win in the first round of Brazil’s presidential election. He defied most polls to win with 47 percent, compared to 45 percent for leftist incumbent Luiz Inacio Lula de Silva. We spoke to Thomas Zicman de Barros, a research fellow at CEVI
- 2026-10-05 12:54 [France 24] 'Very bad result for Lula: Bolsonaro is far more effective at speaking to that growing middle class'
  > Eve Irvine is pleased to welcome Felipe Krause, the head of Oxford University's Brazilian Studies Programme. Brazil's election reflects a political landscape that has become increasingly polarized, explains Krause. And he describes the current mood as one of “tired polarization: People are just exha
- 2026-10-05 20:37 [France 24] Concerns of US interference weigh on Brazil vote
  > Conservative Senator Flavio Bolsonaro pulled off a surprise on Sunday in the first round of Brazil’s presidential election by finishing ahead of the incumbent left-wing President Lula, whom he will face in the runoff on October 25. Suspicions of U.S. interference have been hanging over the campaign,
- 2026-10-05 21:00 [Al Jazeera] Brazil’s presidential race head for a tough runoff
  > Brazil is heading into a fiercely contested presidential runoff after the first round revealed major gains for Bolsonaro
**B** (5 item(s))
- 2026-10-04 23:23 [Clarín Mundo] Alerta en Rusia: murió una científica por un accidente con bacterias en un laboratorio y debieron aislar a 200 personas
  > Contó que se le rompió un tubo de ensayo recolectando muestras para analizar.Autoridades rusas dicen que el frío impediría la transmisión de un tipo de neumonía.Los funcionarios hablan de "una peste no especificada" y "una infección particularmente peligrosa".
- 2026-10-05 06:53 [Europa Press Internacional] Rusia asegura que la situación epidemiológica en Irkutsk es "estable" tras un supuesto accidente en un laboratorio
  > Las autoridades de Rusia han asegurado que la situación epidemiológica en la región de Irkutsk es "estable", después de activar una serie de medidas de emergencia durante los últimos días a causa de la muerte de una investigadora en un presunto accidente de laboratorio en Shelejov.
- 2026-10-05 10:17 [El País Internacional] Rusia pone bajo observación a cientos de personas tras morir una investigadora de un laboratorio contra la peste
  > Trabajos de desinfección de coranavirus en la estación de tren de Yaroslavsky en Moscú, el 10 de noviembre de 2022.
- 2026-10-05 14:34 [Europa Press Internacional] EEUU pide a Rusia compartir información "de forma rápida y transparente" tras supuesto caso de peste en Irkutsk
  > El Departamento de Estado estadounidense ha instado este lunes a las autoridades de Rusia a compartir información "de forma rápida y transparente" sobre el caso de presunta peste pulmonar en la región de Irkutsk, tras la muerte de una investigadora en un presunto accidente de laboratorio en Shelejov
- 2026-10-05 21:21 [BBC Mundo] EE.UU. "sigue de cerca" el caso de una científica rusa que falleció en un centro de investigación de la peste en Siberia
  > El secretario de Estado, Marco Rubio, expresó su preocupación de que el incidente pudiera haber provocado la propagación de la peste neumónica, aunque señaló que no había motivos para alarmarse.

## U130
**A** (12 item(s))
- 2026-10-07 23:32 [Rai News Esteri] La protesta degli studenti blocca licei e università in Francia
  > Poche le risorse stanziate dal premier Le Corneu per la scuola pubblica così i ragazzi tornano in piazza e chiedono un incontro con il governo
- 2026-10-07 23:45 [Europa Press Internacional] Lecornu defiende la actuación policial ante los disturbios en Francia y promete diálogo ante las protestas estudiantiles
  > El primer ministro de Francia, Sébastien Lecornu, ha defendido este miércoles la labor de las fuerzas del orden durante las protestas estudiantiles de las últimas dos semanas, asegurando que su misión es "proteger a los jóvenes" y mantener el Estado de derecho, frente a las acusaciones de represión 
- 2026-10-08 02:27 [France 24 Español] Francia: Ejecutivo anuncia que mantendrá fuerza policial contra manifestaciones estudiantiles
  > Con cientos de miles de estudiantes movilizados en las calles, cientos de colegios cerrados y, tras más de dos semanas de protestas, el primer ministro francés, Sébastien Lecornu, reconoció este miércoles 7 de octubre que "la ira de los jóvenes no surge de la nada". Mientras las manifestaciones se m
- 2026-10-08 06:10 [France 24 Español] En directo: nuevas marchas estudiantiles en Francia entre promesas oficiales y denuncias de violencia policial
  > Los estudiantes de secundaria y universitarios franceses convocan nuevos bloqueos y marchas este jueves 8 de octubre, con el respaldo de varios sindicatos docentes, para exigir más financiación, 250.000 plazas universitarias adicionales y el fin de la selección mediante Parcoursup. Las organizacione
- 2026-10-08 11:36 [El País Internacional] Los estudiantes de Francia presentan 10 reivindicaciones para detener sus protestas
  > Estudiantes cortan la calle delante del liceo Helene-Boucher.
- 2026-10-08 14:44 [Clarín Mundo] "¡A tomar la Bastilla!": sindicatos, el campo y las universidades se unen a las barricadas estudiantiles en una cuarta movilización en Francia
  > En París, la manifestación se concentró en la Plaza de la Bastilla, donde se registraban incidentes.Otra marcha está prevista para el 13 de octubre.
- 2026-10-08 14:45 [Rai News Esteri] Proteste studentesche in Francia, l'abbraccio tra Mélenchon e il giovane Elwan diventa virale
  > “Quello che state facendo è straordinario. È il movimento giovanile più forte degli ultimi 50 anni”, ha dichiarato Mélenchon rivolgendosi ai manifestanti
- 2026-10-08 14:52 [Rai News Esteri] Chi è Elwan, simbolo delle proteste studentesche in Francia: 17 anni e milioni di visualizzazioni
  > Dall'abbraccio con il leader della sinistra Mélenchon allo scontro televisivo con Louise Montangon, il liceale è diventato un fenomeno social
- 2026-10-08 16:16 [BBC Mundo] Cuáles son los reclamos de los estudiantes que están participando en las violentas protestas que sacuden a Francia
  > Los bloqueos y las marchas estudiantiles surgen de agravios reales, y también de la costumbre francesa de decidir sus políticas en las calles.
- 2026-10-08 16:39 [France 24 Español] Directo París y el cuarto día de manifestaciones de estudiantes en Francia
  > Los estudiantes franceses siguen en las calles manifestándose por las condiciones educativas en el país. El primer ministro Sébastien Lecornu se pronunció al respecto, prometiendo medidas a finales de octubre y negando que las fuerzas de seguridad tengan instrucciones de actuar contra las protestas.
- 2026-10-08 17:31 [France 24 Español] Por qué Irán ataca a Francia aprovechando las protestas estudiantiles
  > Francia acusó este miércoles a Irán de lanzar una “campaña de desinformación” sobre las protestas estudiantiles y convocó al embajador iraní en París. Teherán cuestiona la actuación de las autoridades francesas frente a las movilizaciones, en una ofensiva que va más allá de la defensa de los manifes
- 2026-10-08 18:20 [Rai News Esteri] Francia, si allarga la protesta della scuola: "Basta repressione"
  > Cariche della polizia a Parigi, professori e sindacati al fianco degli studenti: "Il governo non dà risposte". I manifestanti: "Non tutti possono pagare la scuola privata"
**B** (9 item(s))
- 2026-10-08 06:47 [Europa Press Internacional] Moldavia denuncia una violación de su espacio aéreo durante el último "ataque masivo" de Rusia contra Ucrania
  > El Gobierno de Moldavia ha denunciado una violación de su espacio aéreo durante la tarde del miércoles en el marco del último "ataque masivo" lanzado por Rusia contra Ucrania, concretamente en el caso de un objeto no especificado que sobrevoló el país durante cerca de un minuto antes de dirigirse a 
- 2026-10-08 08:34 [ANSA Mondo] Kiev, 'raid russo su un autobus a Kramatorsk, 12 morti'
  > A Kramatorsk, nella regione di

Donetsk, un raid russo ha colpito un autobus, uccidendo 12

persone e ferendone 14. Lo affermano le autorità locali come

riporta Ukrainska Pravda.

Riproduzione riservata © Copyright ANSA
- 2026-10-08 10:04 [Il Sole 24 Ore Mondo] Ucraina, 30 morti in raid russo su Kramatorsk. Rubio: «Preoccupati che conflitto si estenda»
  > In territorio ucraino continuano a piovere bombe. Le ultime vittime civili sono 30 passeggeri di due autobus, colpiti da un raid russo a Kramatorsk, nella regione di Donetsk. Oltre alle...
- 2026-10-08 10:04 [France 24 Español] Ataques rusos dejan más de 40 civiles muertos en Ucrania en dos días
  > Un ataque ruso que alcanzó un autobús de transporte público dejó al menos 12 muertos este jueves en Kramatorsk, en el este de Ucrania, y elevó a más de 40 el número de civiles fallecidos en dos días de bombardeos, según las autoridades ucranianas. El presidente Volodímir Zelenski pidió a sus aliados
- 2026-10-08 10:34 [Europa Press Internacional] Mueren 33 personas en un ataque de Rusia en la ciudad ucraniana de Kramatorsk
  > Al menos 33 personas han muerto y otra veintena más ha resultado herida como consecuencia de un ataque del Ejército ruso en la ciudad ucraniana de Kramatorsk, la mayoría de ellos después de que el impacto alcanzara dos autobuses.
- 2026-10-08 10:44 [El País Internacional] Rusia mata al menos a 33 personas en un ataque contra la ciudad ucrania de Kramatorsk
  > Un bombero trabaja este jueves en el lugar del ataque, en la ciudad ucrania de Kramatorsk.
- 2026-10-08 10:44 [El País Internacional] Rusia mata al menos a 33 personas en la ciudad de Kramatorsk en su segundo día de ataques masivos contra civiles
  > Agentes retiran una de las víctimas del ataque contra un autobús ruso en Kramatorsk (Ucrania), este jueves.
- 2026-10-08 11:09 [Clarín Mundo] Mortal ataque de Rusia a dos ómnibuses civiles en Ucrania: hay 33 muertos
  > Otras 18 personas resultaron heridas. Ocurrió en la ciudad de Kramatorsk, en la línea del frente.
- 2026-10-08 18:57 [France 24 Español] Ataques rusos contra Ucrania alcanzan dos buses en Kramatorsk
  > Un ataque ruso impactó dos minibuses en Kramatorsk, dejando varios muertos este 8 de octubre. Casi cinco años después del inicio de la guerra, Moscú ha intensificado sus ataques, lanzando múltiples misiles y drones casi a diario contra Ucrania. En Kiev, estudiantes toman sus clases bajo tierra, en u

## U131
**A** (7 item(s))
- 2026-10-03 23:35 [Rai News Esteri] Marea sociale contro il caro-affitti in Spagna: le piazze spingono Sánchez verso le urne
  > Ondata di proteste da Madrid a tutte le principali città per il diritto alla casa dopo lo sfratto dell'ottantasettenne Mari Carmen; il rifiuto dei decreti da parte delle destre e dei catalani di Junts apre lo scenario di elezioni anticipate
- 2026-10-04 17:28 [Rai News Esteri] Casa e scuola: il filo rosso che lega le proteste in Europa
  > In Spagna per il diritto alla casa, in Francia l'erosione allo studio accende lo scontento dei più giovani
- 2026-10-04 23:15 [Rai News Esteri] La Spagna in piazza per il diritto alla casa. E Sanchez pensa al voto anticipato
  > Centinaia di migliaia di persone al fianco delle proteste di Madrid per la casa, il governo bocciato in Parlamento valuta elezioni a fine novembre
- 2026-10-05 06:21 [Il Sole 24 Ore Mondo] Caro casa, prezzi e affitti salgono nell’Ue. Il Governo studia le misure per giovani e locazioni
  > «Serve una formazione di qualità, un lavoro sicuro e stabile, una retribuzione adeguata, una casa a un prezzo equo», ha detto di recente la premier Giorgia Meloni
- 2026-10-05 10:27 [Rai News Esteri] La Spagna al voto: i sondaggi premiano le destre, l'area progressista frammentata
  > Il partito popolare e Vox arriverebbero al 52%, secondo un sondaggio per El Pais. Ma le rilevazioni sono state realizzate prima della crisi di governo e della bocciatura dei decreti presentati da Sanchez
- 2026-10-05 19:05 [Il Sole 24 Ore Mondo] Sanchez sfida le destre: Spagna al voto anticipato
  > Dopo la bocciatura sul piano casa, il premier socialista convoca le elezioni cavalcando le proteste di piazza: «Serve una maggioranza progressista per nuovi progressi sociali»
- 2026-10-05 21:04 [Rai News Esteri] Migliaia di persone a Barcellona in piazza per il diritto alla casa
  > Dopo Madrid e Valencia anche Barcellona stasera è scesa in piazza all'annuncio di elezioni anticipate, in migliai hanno sfilato per difendere il diritto alla casa
**B** (3 item(s))
- 2026-10-04 12:33 [Rai News Esteri] Spagna, il Psoe in pressing su Sanchez per il voto anticipato. La destra soffia sulle piazze
  > Oltre mezzo milione di persone sfilano a Madrid, a Valencia la tensione sfocia in cariche e 5 arresti di fronte a un summit immobiliare. Il Congresso ha bocciato i decreti salva-affitti coi voti di centrodestra e indipendentisti catalani
- 2026-10-05 07:29 [ANSA Mondo] Sanchez, 'ho deciso di convocare le elezioni il 29 novembre'
  > Il premier in una dichiarazione istituzionale
- 2026-10-05 12:08 [Rai News Esteri] Sanchez porta la Spagna al voto il 29 novembre sull'onda delle proteste per la crisi abitativa
  > Il capo del governo di Madrid, pressato da giorni da richieste di elezioni anticipate, punta a capitalizzare un consenso "last minute" con i provvedimenti per la casa, una crisi che ha portato a proteste in tutto il Paese

## U132
**A** (3 item(s))
- 2026-09-30 18:01 [Al Jazeera] Trump set to announce $200bn in energy investments from South Korea
  > The investments come as Trump seeks to tout the Republican Party&#039;s economic record ahead of the US midterm races.
- 2026-10-01 01:44 [South China Morning Post] Trump touts US$200 billion South Korean energy deal ahead of US midterms
  > US President Donald Trump has announced US$200 billion in energy investments from South Korea, including US$54 billion towards a long-discussed liquefied natural gas project in Alaska and more than US$100 billion in planned longer-term nuclear power investments.
Besides the Alaska LNG project and pi
- 2026-10-01 10:36 [South China Morning Post] South Korea hits back at Trump’s investment claims in ‘tit-for-tat move’
  > US President Donald Trump’s unilateral announcement of a “colossal” South Korean investment package has prompted Seoul to clarify that the deal is far from finalised, laying bare stark differences between the allies over the terms of their trade agreement, observers have said.
On Wednesday, Trump an
**B** (3 item(s))
- 2026-10-01 14:02 [Defense News] Neros, Perennial Autonomy lead in Pentagon’s drone competition
  > Two California-based startups took the top spots in the latest phase of the Drone Dominance competition, a Pentagon effort to find companies that can produce high-quality, low-cost commercial drones at scale.According to the competition’s leaderboard, Neros Technologies scored highest in the confine
- 2026-10-01 14:29 [Breaking Defense] Battling sand and wind, Pentagon evaluates counter-drone tech at southern border exercise
  > A dozen vendors came to Yuma Proving Ground during Falcon Peak 26.2 to test their counter drone tech. Their goal: win a Pentagon contract.
- 2026-10-02 16:38 [Breaking Defense] Pentagon partners with CIA’s In-Q-Tel for ‘technology scouting’
  > The CIA-funded investment firm, which has helped finance startups from Anduril to Palantir, is now formally coordinating with the Pentagon’s Critical Technologies office.

## U133
**A** (2 item(s))
- 2026-09-29 19:08 [South China Morning Post] China expands overseas military presence with new Laos air force centre
  > China has launched a rare air force support and training centre in Laos, the Ministry of Defence announced on Tuesday.
The China-Laos Joint Support and Training Centre and the China-Laos Friendship Aviation Academy are now in operation at the Ban Keun Airport, aiming to help the Laotian Air Force tr
- 2026-09-30 16:33 [Breaking Defense] China opens training center with Laos, marking third overseas military base
  > Satellite imagery shows the new facility is built in part on a purported old US airstrip used during the Vietnam War.
**B** (3 item(s))
- 2026-09-30 18:01 [Al Jazeera] Trump set to announce $200bn in energy investments from South Korea
  > The investments come as Trump seeks to tout the Republican Party&#039;s economic record ahead of the US midterm races.
- 2026-10-01 01:44 [South China Morning Post] Trump touts US$200 billion South Korean energy deal ahead of US midterms
  > US President Donald Trump has announced US$200 billion in energy investments from South Korea, including US$54 billion towards a long-discussed liquefied natural gas project in Alaska and more than US$100 billion in planned longer-term nuclear power investments.
Besides the Alaska LNG project and pi
- 2026-10-01 10:36 [South China Morning Post] South Korea hits back at Trump’s investment claims in ‘tit-for-tat move’
  > US President Donald Trump’s unilateral announcement of a “colossal” South Korean investment package has prompted Seoul to clarify that the deal is far from finalised, laying bare stark differences between the allies over the terms of their trade agreement, observers have said.
On Wednesday, Trump an

## U134
**A** (3 item(s))
- 2026-10-07 22:21 [Clarín Mundo] Peste neumónica en Rusia: en el pueblo de la muerte sospechosa, "nadie parece preocuparse"
  > La muerte de una técnica de un laboratorio especializado en enfermedades infecciosas inquieta a Estados Unidos y otros países.Moscú minimiza el riesgo y en la ciudad de Irkutsk, donde ocurrió el fallecimiento, los habitantes siguen su vida.
- 2026-10-08 09:33 [ANSA Mondo] Agenzia sanitaria russa, 'sono false le voci su secondo caso di presunta peste'
  > Sono "false" le voci su un presunto

secondo caso di peste nella regione siberiana russa di Irktusk.Lo afferma l'agenzia sanitaria russa Rospotrebnadzor, citata da

Ria Novosti."In merito alle false informazioni apparse sui social media

riguardo a un secondo caso della malattia in una persona che h
- 2026-10-08 14:18 [Il Sole 24 Ore Mondo] Peste in Siberia, la madre della ricercatrice: «Hanno lasciato morire mia figlia»
  > Sale la tensione fra Russia e Stati Uniti sul caso di peste in Siberia. Dopo giorni di inviti pubblici a fare chiarezza, Washington ha inviato a Mosca una nota ufficiale...
**B** (9 item(s))
- 2026-10-08 06:47 [Europa Press Internacional] Moldavia denuncia una violación de su espacio aéreo durante el último "ataque masivo" de Rusia contra Ucrania
  > El Gobierno de Moldavia ha denunciado una violación de su espacio aéreo durante la tarde del miércoles en el marco del último "ataque masivo" lanzado por Rusia contra Ucrania, concretamente en el caso de un objeto no especificado que sobrevoló el país durante cerca de un minuto antes de dirigirse a 
- 2026-10-08 08:34 [ANSA Mondo] Kiev, 'raid russo su un autobus a Kramatorsk, 12 morti'
  > A Kramatorsk, nella regione di

Donetsk, un raid russo ha colpito un autobus, uccidendo 12

persone e ferendone 14. Lo affermano le autorità locali come

riporta Ukrainska Pravda.

Riproduzione riservata © Copyright ANSA
- 2026-10-08 10:04 [Il Sole 24 Ore Mondo] Ucraina, 30 morti in raid russo su Kramatorsk. Rubio: «Preoccupati che conflitto si estenda»
  > In territorio ucraino continuano a piovere bombe. Le ultime vittime civili sono 30 passeggeri di due autobus, colpiti da un raid russo a Kramatorsk, nella regione di Donetsk. Oltre alle...
- 2026-10-08 10:04 [France 24 Español] Ataques rusos dejan más de 40 civiles muertos en Ucrania en dos días
  > Un ataque ruso que alcanzó un autobús de transporte público dejó al menos 12 muertos este jueves en Kramatorsk, en el este de Ucrania, y elevó a más de 40 el número de civiles fallecidos en dos días de bombardeos, según las autoridades ucranianas. El presidente Volodímir Zelenski pidió a sus aliados
- 2026-10-08 10:34 [Europa Press Internacional] Mueren 33 personas en un ataque de Rusia en la ciudad ucraniana de Kramatorsk
  > Al menos 33 personas han muerto y otra veintena más ha resultado herida como consecuencia de un ataque del Ejército ruso en la ciudad ucraniana de Kramatorsk, la mayoría de ellos después de que el impacto alcanzara dos autobuses.
- 2026-10-08 10:44 [El País Internacional] Rusia mata al menos a 33 personas en un ataque contra la ciudad ucrania de Kramatorsk
  > Un bombero trabaja este jueves en el lugar del ataque, en la ciudad ucrania de Kramatorsk.
- 2026-10-08 10:44 [El País Internacional] Rusia mata al menos a 33 personas en la ciudad de Kramatorsk en su segundo día de ataques masivos contra civiles
  > Agentes retiran una de las víctimas del ataque contra un autobús ruso en Kramatorsk (Ucrania), este jueves.
- 2026-10-08 11:09 [Clarín Mundo] Mortal ataque de Rusia a dos ómnibuses civiles en Ucrania: hay 33 muertos
  > Otras 18 personas resultaron heridas. Ocurrió en la ciudad de Kramatorsk, en la línea del frente.
- 2026-10-08 18:57 [France 24 Español] Ataques rusos contra Ucrania alcanzan dos buses en Kramatorsk
  > Un ataque ruso impactó dos minibuses en Kramatorsk, dejando varios muertos este 8 de octubre. Casi cinco años después del inicio de la guerra, Moscú ha intensificado sus ataques, lanzando múltiples misiles y drones casi a diario contra Ucrania. En Kiev, estudiantes toman sus clases bajo tierra, en u

## U135
**A** (3 item(s))
- 2026-10-05 03:37 [BBC World] Trump unveils 'Super Intelligence Force' to oversee AI policy
  > The president named his national intelligence chief as the taskforce's head as worries over AI grow.
- 2026-10-05 10:03 [BBC World] Trump chooses top spy boss to run new AI taskforce
  > The US president said his national intelligence chief will lead the group as worries over AI grow.
- 2026-10-05 10:09 [France 24] Trump names Jay Clayton as AI czar to lead 'Super Intelligence Force'
  > US President Donald Trump has named his National Intelligence Director Jay Clayton as America's "Super Intelligence" czar, as fears over AI grow. Also, oil markets react to Houthi attacks as well as export data, and France's fiscal woes drive the euro to a 17-month low.
**B** (2 item(s))
- 2026-10-05 14:08 [South China Morning Post] France, Germany call for new weapon allowing ‘immediate cut off’ of China from EU market
  > In the strongest sign yet of a shifting European Union policy on China, the leaders of France and Germany have demanded a new trade weapon that would cut off access to the EU market when third countries cause severe distortions.
The tool would effectively act as a kill switch, allowing Brussels to r
- 2026-10-05 17:01 [France 24] France, Germany seek new EU rapid response tool against trade threats
  > France and Germany proposed a new legal tool to enable the EU to respond rapidly to trade wars or measures, such as dumping, that could economically harm the bloc. While French President Emmanuel Macron and German Chancellor Friedrich Merz said the proposal was not a direct response to the actions o

## U136
**A** (2 item(s))
- 2026-10-03 12:22 [BBC Mundo] Lo que la fallida ejecución de Christa Pike revela sobre la pena de muerte en EE.UU.
  > Christa Pike, una mujer condenada a muerte en Tennessee, sobrevivió a la aplicación de dos inyecciones letales. Su caso ha vuelto a centrar la atención en la pena de muerte y en cómo se aplica en Estados Unidos.
- 2026-10-03 19:14 [Il Sole 24 Ore Mondo] Trump vuole estendere la pena di morte ai narcotrafficanti: il caso Pike riapre lo scontro
  > Il presidente promette di ampliare i reati punibili con la pena capitale. Il Tennessee sospende le esecuzioni dopo il caso Pike, mentre una sentenza della Corte Suprema del 2008 lascia aperto il nodo dei grandi narcotrafficanti
**B** (3 item(s))
- 2026-10-04 22:56 [South China Morning Post] US Coast Guard suspends search for 6 aboard crashed medical aircraft
  > US Authorities on Sunday suspended the search off the Massachusetts coast for six people on an air ambulance that disappeared during a flight from Bermuda to Boston.
The US Coast Guard said authorities searched more than 7,081km (4,400 miles) over a span of 66 hours for the four Canadians and two pe
- 2026-10-05 03:22 [Al Jazeera] US coastguard suspends search for six on board crashed medical jet
  > Debris found off Nantucket island after the air ambulance disappeared while flying from Bermuda to Boston.
- 2026-10-05 04:00 [BBC World] All six passengers presumed dead after plane went missing off US coast
  > The aircraft lost communication with flight controllers after significantly dropping in altitude, according to flight data.

## U137
**A** (2 item(s))
- 2026-10-08 03:19 [BBC Mundo] Los israelíes exigen que se rindan cuentas por los errores del 7 de octubre, tres años después de los ataques de Hamás
  > El primer ministro israelí, Benjamin Netanyahu, se niega a asumir cualquier responsabilidad personal por lo sucedido o a ordenar una investigación estatal.
- 2026-10-08 16:38 [France 24 Español] Informe desde Beirut: se cumplen tres años de guerra de Israel en Líbano
  > Luego de los ataques de Hamás contra Israel el 7 de octubre de 2023, el Hezbolá libanés abrió un "frente de apoyo" a la milicia palestina. Este 2026 se cumplen tres años del conflicto, que ha provocado una ocupación israelí del sur de Líbano y el desplazamiento de cientos de personas. Aunque se espe
**B** (5 item(s))
- 2026-10-08 05:06 [Al Jazeera] Signage at UK consulate in East Jerusalem removed as Israel’s deadline over
  > Thursday marks 30 days since Israel&#039;s foreign minister ordered the closure of the UK consulate in occupied East Jerusalem.
- 2026-10-08 07:06 [BBC World] Most UK diplomats to leave East Jerusalem consulate, Israel says, as Miliband says 'vital services' to remain
  > Israel said in September it would act in response to UK sanctions on illegal Israeli settlements in the West Bank.
- 2026-10-08 07:27 [South China Morning Post] Britain downscales and renames Jerusalem consulate after Israel orders closure
  > Britain said on Thursday its ⁠nearly 200-year-old consulate in Jerusalem ⁠would remain operating at a smaller scale, renamed ⁠as the “UK Mission” in the city, after Israel ordered it shut in a dispute over sanctions on settlements.
Israel last month issued a 30-day deadline for Britain to close the 
- 2026-10-08 08:25 [Al Jazeera] Video: Signs removed from British consulate in occupied East Jerusalem
  > Signs from the British consulate in occupied East Jerusalem were removed overnight as a deadline for its closure loomed.
- 2026-10-08 14:01 [Al Jazeera] King David Hotel bombing to consulate row: A timeline of UK-Israel tension
  > Israel&#039;s order to shut UK&#039;s Jerusalem consulate is the latest downturn in a relationship strained since before 1948.

## U138
**A** (12 item(s))
- 2026-10-04 12:48 [Al Jazeera] Yemen’s leader announces military operation to retake Houthi-held territory
  > Rashad al-Alimi says the campaign aims to restore state authority throughout Yemen.
- 2026-10-04 16:51 [BBC World] Yemen's government announces all-out war to reclaim land from Houthis
  > The Yemeni president's announcement comes amid an exchange of strikes between the Houthis and the Saudi-led coalition.
- 2026-10-04 19:50 [Defense News] Yemeni government launches offensive to seize all areas from Iran-backed Houthis
  > Yemen’s Saudi-backed, internationally recognized government said on Sunday it was launching a major military campaign to recapture all areas of the country controlled by the Iran-backed Houthis.The government’s armed forces would press the offensive “until the country is liberated from the grip of t
- 2026-10-05 00:00 [Al Jazeera] Iran war live: Yemen fighting intensifies; Tehran says ready for US attacks
  > Yemeni government announces major offensive against Houthis, as Iran says it is ready to defend itself if US attacks.
- 2026-10-05 03:11 [Al Jazeera] Yemen gov’t forces commence major combat operation against Houthis
  > Yemeni government forces have declared a ‘battle for liberation’ to retake remaining territory held by the Houthis.
- 2026-10-05 09:37 [France 24] Yemen's government declares major operation against Houthis
  > The Yemeni military announced a broad set of strikes against Houthi targets on Monday, after the government declared a new campaign to retake all territory even as the Iran-backed group made fresh gains on the ground. France 24's Kethevane Gorjestani takes a look at the reasons behind this latest es
- 2026-10-05 09:40 [Al Jazeera] Yemen forces claim to seize Dhubab, sites near Bab al-Mandeb from Houthis
  > Yemeni forces claim to seize key positions near waterway as Pakistani, Saudi and Turkish officials to meet.
- 2026-10-05 13:23 [South China Morning Post] Yemeni government forces seize control of Bab el-Mandeb Strait, minister says
  > Saudi-backed Yemeni government forces have secured effective control of the Bab el-Mandeb Strait, Yemen’s Information Minister Moammar al-Eryani has said, though fighting continues with Houthi forces in the area.
The government forces advanced rapidly along the coast with heavy Saudi air support to 
- 2026-10-05 14:37 [BBC World] Yemeni government forces say they have 'secured' Bab al-Mandab Strait
  > Saudi-backed forces gave conflicting reports of whether they had also seized the port city of Mokha, near the Bab al-Mandab Strait.
- 2026-10-05 14:59 [France 24] Yemen government forces announce offensive on Houthi-held territory
  > The internationally recognised Yemeni government announced on Sunday the launch of an offensive ‌to recapture territory held by Houthi rebels, with President Rashad al-Alimi swearing to fight "until the country is liberated from the grip of the terrorist militia".
- 2026-10-05 15:29 [Al Jazeera] Yemeni gov’t forces aim for Sanaa, but Houthi defeat will be a challenge
  > Yemeni government forces claim strategic advances near Bab al-Mandeb strait amid a major anti-Houthi offensive.
- 2026-10-05 19:17 [France 24] Saudi-backed Yemeni forces expel the Houthis from several areas around key strait, officials say
  > Saudi-backed Yemeni government forces staged a lightning advance on ​Monday to retake the coast around the Bab el-Mandeb Strait up to the city of Mocha, the government said, pushing the Iran-backed Houthis out of most of the areas they seized last month. FRANCE 24's Monte Francis reports.
**B** (2 item(s))
- 2026-10-05 20:28 [France 24] Ethiopia again demands access to the Red Sea
  > In tonight's edition, Ethiopia's leader Abiy Ahmed secures another term, but his country is sliding back into conflict. Also, several major cities across Senegal are battered by torrential rains. And some of the migrants being deported from the US fear the return to countries criminalizing homosexua
- 2026-10-05 21:10 [Al Jazeera] Ethiopia’s PM insists on access to Red Sea despite regional conflict threat
  > Neighbouring countries say coastal states must govern Red Sea as fighting escalates in northern Ethiopia.

## U139
**A** (2 item(s))
- 2026-09-29 20:25 [BBC World] Former American Idol contestant and pastor found guilty of murdering wife
  > Caleb Flynn shot his wife, Ashley, dead in their Ohio home in February before saying in a 9/11 call she was killed by burglars.
- 2026-09-30 10:35 [Al Jazeera] Former American Idol contestant found guilty of murdering wife
  > Former American Idol contestant found guilty of murdering wife
**B** (6 item(s))
- 2026-10-02 01:23 [Al Jazeera] Trump says US may ask Europe to release diesel reserves
  > Skyrocketing diesel prices have pushed Washington to weigh an export ban, raising alarm across European economies.
- 2026-10-02 05:26 [BBC World] US pressures Europe over diesel reserves as Trump threatens export ban
  > President Donald Trump has threatened to ban diesel exports in a bid to ease prices in the US ahead of the November elections.
- 2026-10-02 13:16 [Al Jazeera] Trump vs Europe as US presses for release of emergency diesel stocks
  > Europe&#039;s leaders are mulling proposals to respond to Trump&#039;s diesel demands.
- 2026-10-02 14:51 [South China Morning Post] G7 nations agree to release diesel and oil stocks after Trump pressure
  > Group ⁠of Seven countries agreed on Friday to release 100 million barrels of diesel and crude oil from emergency reserves and pledged to refrain from energy export restrictions after pressure from US President Donald Trump.
The US led a pressure campaign on the European Union to draw down emergency 
- 2026-10-02 19:01 [Al Jazeera] Trump says Europe agreed to release ‘massive amount’ of diesel reserves
  > US President Donald Trump says Europe agreed to release a ‘massive amount’ of diesel from emergency stockpiles.
- 2026-10-02 20:25 [BBC World] G7 to release 100 million barrels of oil and diesel after Trump export ban threat
  > The co-ordinated release is aimed at heading off further price spikes and avoiding a ban on US diesel exports.

## U140
**A** (2 item(s))
- 2026-10-01 14:00 [South China Morning Post] China backs Cuba, Beijing’s Panama threat, new UN chief: 7 Latin America relations reads
  > We have selected seven of the most interesting and important news stories covering Latin American relations from the past few weeks. If you would like to see more of our reporting, please consider subscribing.
1. China pledges to ‘firmly support’ Cuba as US escalates pressure on Havana

China will s
- 2026-10-02 20:52 [Al Jazeera] Latin America sees China as more positive global influence than US: Poll
  > Annual Latinobarometro survey finds views of China’s influence improving as perceptions of US influence worsen.
**B** (4 item(s))
- 2026-10-01 19:03 [Al Jazeera] Saudi-led coalition says power station attacked in Medina, blames Houthis
  > At the same time in Yemen, the Saudi-backed government army says it is inflicting heavy losses on the Houthis in Taiz.
- 2026-10-01 19:05 [Al Jazeera] After Red Sea losses, Yemen’s government forces hold the line
  > Air strikes and difficult terrain have prevented the Houthis from turning coastal gains into a wider breakthrough.
- 2026-10-02 19:00 [Defense News] Saudis plan assault on Houthis to break Red Sea chokehold
  > Saudi Arabia is planning an offensive against Iran-backed Houthi militants in Yemen, with options being considered, including a coastal push to secure the Red Sea shipping route or an assault on multiple fronts, regional and Western officials told Reuters.The operation, expected to be launched in th
- 2026-10-03 08:00 [South China Morning Post] As Saudi Arabia steps up war against Yemen’s Houthis, Pakistan set to play support role
  > Pakistani troops are expected to take over various defensive functions for Saudi Arabia to enable the Middle East country to fight an all-out war aimed at defeating Yemen’s Iran-backed Houthi rebels.
According to defence analysts, Pakistani troops are not expected to participate directly in ground o

## U141
**A** (8 item(s))
- 2026-09-29 14:40 [Defense News] US forces exiting Iraq after 2 decades, leaving opening for Iran
  > U.S. forces are set to depart from their last bases in Iraq by Wednesday, a move celebrated as a victory by Iran and its allies, who now have deep influence in the country where 4,500 Americans died during more than two decades of war.Iraqi security experts say the withdrawal — agreed to in 2024 und
- 2026-09-29 20:00 [Al Jazeera] US troops fully withdraw from Baghdad base after two decades
  > US Army soldiers have fully withdrawn from the US base in Baghdad.
- 2026-09-30 09:46 [South China Morning Post] US ends troop mission in Iraq, Baghdad to celebrate Sovereignty Day on October 1
  > A US-led coalition deployed in Iraq more than a decade ago to fight jihadists concluded its mission on Wednesday, a move celebrated by the country’s leaders, but which some fear will embolden pro-Iran armed factions.
Coalition troops deployed to Iraq and Syria in 2014 to fight Islamic State, which h
- 2026-09-30 11:36 [BBC World] Last UK and US troops leave Iraq as anti-Islamic State mission ends
  > The withdrawal of coalition forces, under a deal agreed two years ago, was a key demand of the Iraqi government.
- 2026-09-30 12:17 [Al Jazeera] Iraq celebrates National Sovereignty Day as US troops withdraw
  > Iraq’s security forces held parades in Baghdad and Najaf to celebrate ‘Sovereignty Day’ as US troops withdraw.
- 2026-09-30 14:04 [Breaking Defense] US withdraws last remaining troops out of Iraq
  > “As we step back and hand full primary responsibility for Iraq’s security to the Government of Iraq and the brave people of Iraq, US and Coalition forces stationed across the region will remain ready to respond to any ISIS threats that arise,” CENTCOM Commander Adm. Brad Cooper said.
- 2026-09-30 16:33 [Al Jazeera] Pentagon says US troop withdrawal from Iraq is complete
  > The withdrawal ends two decades of foreign intervention in Iraq as part of &#039;global war on terror&#039; and anti-ISIL fight.
- 2026-10-01 01:11 [Al Jazeera] Iraq celebrates Sovereignty Day as US troops complete withdrawal
  > Night time celebrations filled the air as Iraqis observed the start of a four-day holiday.
**B** (4 item(s))
- 2026-10-02 02:49 [BBC World] NY's governor appoints special prosecutor in Cornell frat rape investigation
  > The governor said she'd lost faith in prosecutors overseeing the case and handed it over to New York Attorney General Letitia James.
- 2026-10-02 17:10 [South China Morning Post] New York governor attacks handling of Cornell gang rape case, appoints special prosecutor
  > New York Governor Kathy Hochul on Friday faulted police and prosecutors for failing to fully investigate an alleged gang rape in 2024 at Cornell University, saying she was “deeply disturbed” by how the incident was handled.
Hochul was speaking at a press conference alongside state Attorney General L
- 2026-10-02 17:43 [Al Jazeera] ‘I want the truth’: NY governor appoints prosecutor in Cornell rape case
  > New York Governor Kathy Hochul says local authorities failed to properly investigate the 2024 allegations.
- 2026-10-02 17:44 [BBC World] Woman at centre of Cornell rape inquiry was 'failed' by officials, says New York governor
  > The woman, known as Jane Doe, alleges she was raped by seven students at a fraternity house at the university in 2024.

## U142
**A** (2 item(s))
- 2026-09-30 03:21 [South China Morning Post] US Supreme Court lets Trump resume deportations to third countries
  > The US Supreme Court on Tuesday let President Donald Trump’s administration continue swiftly deporting people to countries other than their own for now, while the justices consider whether the policy is legal.
The apparent 6-3 order temporarily lifts lower court requirements for migrants to get a ch
- 2026-10-01 17:35 [Al Jazeera] US Supreme Court agrees to take up Trump’s ICE detention policy
  > The case is the latest dispute over US President Donald Trump’s sweeping immigration crackdown.
**B** (4 item(s))
- 2026-10-02 02:49 [BBC World] NY's governor appoints special prosecutor in Cornell frat rape investigation
  > The governor said she'd lost faith in prosecutors overseeing the case and handed it over to New York Attorney General Letitia James.
- 2026-10-02 17:10 [South China Morning Post] New York governor attacks handling of Cornell gang rape case, appoints special prosecutor
  > New York Governor Kathy Hochul on Friday faulted police and prosecutors for failing to fully investigate an alleged gang rape in 2024 at Cornell University, saying she was “deeply disturbed” by how the incident was handled.
Hochul was speaking at a press conference alongside state Attorney General L
- 2026-10-02 17:43 [Al Jazeera] ‘I want the truth’: NY governor appoints prosecutor in Cornell rape case
  > New York Governor Kathy Hochul says local authorities failed to properly investigate the 2024 allegations.
- 2026-10-02 17:44 [BBC World] Woman at centre of Cornell rape inquiry was 'failed' by officials, says New York governor
  > The woman, known as Jane Doe, alleges she was raped by seven students at a fraternity house at the university in 2024.

## U143
**A** (6 item(s))
- 2026-10-07 22:41 [Clarín Mundo] La muerte de Maricarmen, la mártir de los inquilinos que reclaman por una vivienda digna y puso en jaque al gobierno de Sánchez
  > La mujer de 87 años falleció en el hospital Gregorio Marañón tras ser desalojada del departamento madrileño donde residía desde su juventud. La escalada del conflicto impulsó además la convocatoria a una huelga general fijada para el 11 de noviembre.
- 2026-10-08 03:07 [France 24 Español] Falleció Maricarmen Abascal, mujer desahuciada que se convirtió en símbolo de lucha por la vivienda
  > Maricarmen Abascal, la jubilada de 87 años cuyo desahucio en Madrid la ha convertido en símbolo de las recientes protestas masivas por la crisis de vivienda en España, murió este miércoles 7 de octubre, según confirmó el Sindicato de Inquilinas. Sin desearlo, la mujer se había convertido en el rostr
- 2026-10-08 08:38 [ANSA Mondo] La morte di Maricarmen Abascal, un minuto di silenzio fuori dall'Assemblea di Madrid
  > Si è tenuto fuori dall'emiciclo dell'Assemblea di Madrid il minuto di silenzio promosso dalla forza della sinistra alternativa Mas Madrid e dal Partito socialista spagnolo (Psoe-M) in memoria di Maricarmen Abascal, la donna di 87 anni sgomberata dalla propria abitazione il 23 settembre e morta ieri 
- 2026-10-08 11:22 [Rai News Esteri] La storia di Maricarmen: sfrattata a 87 anni e diventata il simbolo della protesta per la casa
  > È morta all'ospedale di Madrid, dov'era ricoverata dallo scorso 23 settembre. "Chiedo che quello che ho passato io non debba capitare a nessun altro", aveva detto
- 2026-10-08 13:59 [Rai News Esteri] Madrid, fanno scudo a una famiglia con tre figli e fermano lo sfratto: "Tamara non sei sola"
  > Mobilitazione a San Blas, il giorno dopo la morte di Maricarmen, simbolo crisi abitativa
- 2026-10-08 15:19 [Il Sole 24 Ore Mondo] Polizia britannica riconosce l’illegalità delle perquisizioni a casa di Andrea nel caso Epstein
  > La polizia britannica ha ammesso oggi l’illegittimità delle perquisizioni compiute a febbraio in due residenze dell’ex principe Andrea che condussero anche a un’umiliante arresto temporaneo di circa 24...
**B** (5 item(s))
- 2026-10-08 01:15 [Al Jazeera] Death of 87-year old sparks furious Spain housing protests
  > Hundreds of protesters gather outside Spain’s Parliament, demanding action over soaring rents.
- 2026-10-08 09:56 [France 24] Anger mounts in Spain as woman whose eviction ignited housing protests dies
  > Maricarmen ​Abascal, the 87-year-old Spanish woman whose dramatic eviction last month sparked mass housing protests that led to an early election, has died, the Madrid tenants' union said on Wednesday, as thousands demonstrated over her death. France 24's correspondent in Madrid Sarah Morris has the
- 2026-10-08 10:35 [France 24] Evicted pensioner Maricarmen, symbol of Spain's housing crisis, dies at 87
  > PRESS REVIEW – Thursday, October 8: Maricarmen, the evicted Spanish pensioner who became the face of Spain's housing crisis, dies in hospital. Also, France braces for "Act Four" of high school student protests against dilapidated schools and poor staff presence. Finally, actress Zendaya sparks a row
- 2026-10-08 10:48 [Al Jazeera] Photos: Protests erupt after 87-year-old evicted woman dies in Madrid
  > Nationwide outrage grows after the death of woman whose eviction sparked protests and political tensions.
- 2026-10-08 11:54 [France 24] Maricarmen, the 87-year-old woman whose eviction shook Spain, dies
  > María del Carmen Abascal, the 87-year-old woman whose eviction from her longtime Madrid home sparked nationwide protests across Spain and unleashed a political crisis, died on Wednesday while hospitalised.

## U144
**A** (3 item(s))
- 2026-10-07 22:21 [Clarín Mundo] Peste neumónica en Rusia: en el pueblo de la muerte sospechosa, "nadie parece preocuparse"
  > La muerte de una técnica de un laboratorio especializado en enfermedades infecciosas inquieta a Estados Unidos y otros países.Moscú minimiza el riesgo y en la ciudad de Irkutsk, donde ocurrió el fallecimiento, los habitantes siguen su vida.
- 2026-10-08 09:33 [ANSA Mondo] Agenzia sanitaria russa, 'sono false le voci su secondo caso di presunta peste'
  > Sono "false" le voci su un presunto

secondo caso di peste nella regione siberiana russa di Irktusk.Lo afferma l'agenzia sanitaria russa Rospotrebnadzor, citata da

Ria Novosti."In merito alle false informazioni apparse sui social media

riguardo a un secondo caso della malattia in una persona che h
- 2026-10-08 14:18 [Il Sole 24 Ore Mondo] Peste in Siberia, la madre della ricercatrice: «Hanno lasciato morire mia figlia»
  > Sale la tensione fra Russia e Stati Uniti sul caso di peste in Siberia. Dopo giorni di inviti pubblici a fare chiarezza, Washington ha inviato a Mosca una nota ufficiale...
**B** (3 item(s))
- 2026-10-08 01:23 [France 24 Español] Directo a... Washington y las dudas generadas por fallida ejecución de Christa Pike
  > Christa Pike, condenada a muerte por el asesinato de una compañera de estudios en 1995, es la única persona que ha sobrevivido tras recibir fármacos de inyección letal, según el Centro de Información sobre la Pena de Muerte. Una semana después de su fallida ejecución, la mujer se encuentra despierta
- 2026-10-08 02:09 [ANSA Mondo] Giustiziato in Texas con iniezione letale, prima esecuzione dopo il caso Pike
  > Jamaal Howard, un americano di

46 anni, è stato giustiziato in Texas tramite una iniezione

letale, in quella che è la prima esecuzione dopo il tentativo

più volte fallito contro Christa Pike in Tennessee, appena una

settimana prima.Quella di Howard, condannato a morte per aver ucciso un

addetto
- 2026-10-08 02:52 [Rai News Esteri] Giustiziato Jamaal Howard: per gli Usa è la trentesima esecuzione dell'anno
  > L'uomo era condannato per l'omicidio di un commesso nel 2000. Primo caso dopo la vicenda di Christa Pike

## U145
**A** (5 item(s))
- 2026-10-07 23:20 [Al Jazeera] Christa Pike was nearly taken off life support before waking, lawyers say
  > Death row inmate who survived execution by lethal injection is said to be &#039;angry and confused&#039; about what happened.
- 2026-10-08 03:02 [BBC World] Texas carries out first US execution since Christa Pike's botched lethal injections
  > Lawyers for Jamaal Howard had asked a judge to pause the execution after Christa Pike's botched lethal injections.
- 2026-10-08 08:13 [BBC World] Christa Pike now walking after US execution went wrong, lawyer tells BBC
  > A lawyer says the murderer of Colleen Slemmer is moving around her hospital room after surviving two lethal injections.
- 2026-10-08 08:29 [Al Jazeera] Christa Pike almost taken off life support before she woke up
  > Death row inmate Christa Pike has regained consciousness following a botched execution in Tennessee, her lawyer says.
- 2026-10-08 09:53 [France 24] Christa Pike 'angry and confused' after Tennessee's failed execution effort
  > Christa Pike, sentenced to death for a 1995 murder, awoke "angry ​and confused" in a hospital this week with a long recuperation ahead after surviving Tennessee's botched effort to execute her, her lawyers said on Wednesday.
**B** (6 item(s))
- 2026-10-08 11:23 [ANSA English] New election law gives voters choice, ensures stable govts says Meloni
  > (ANSA) - ROME, 08 OTT - Premier Giorgia Meloni on Thursday expressed satisfaction after the Lower House gave final approval to the ruling coalition&#039;s bill for a new election law, saying it gives voters greater choice about who represents them and will ensure future governments are stable.
&#034
- 2026-10-08 11:31 [Europa Press Internacional] Italia aprueba la reforma electoral impulsada por Meloni que otorga una prima a la coalición ganadora
  > La Cámara de Diputados italiana ha adoptado este jueves en votación final la reforma electoral impulsada por la primera ministra del país, Giorgia Meloni, que contempla una prima de 70 escaños para la coalición ganadora que llegue al 42% de los votos, una medida con la que se busca aumentar la estab
- 2026-10-08 11:44 [El País Internacional] Italia aprueba la controvertida reforma electoral de Meloni y se acerca a unas elecciones anticipadas
  > La bancada progresista de la Cámara de Diputados italiana manifiesta su descontento con la nueva ley electoral.
- 2026-10-08 12:02 [BBC World] Italy overhauls electoral system after fiercely contested debate
  > Prime Minister Giorgia Meloni says the move will deliver more stable government, but opposition parties say her aim is to stay in power.
- 2026-10-08 12:10 [Al Jazeera] Italian law to give election winners bonus seats: Why that’s controversial
  > Critics say the proposed law is undemocratic, potentially granting a winning coalition outsized power in parliament.
- 2026-10-08 12:32 [France 24 Español] Italia aprueba una nueva ley electoral que cambia las reglas para las próximas elecciones
  > El Parlamento italiano aprobó este jueves la reforma electoral impulsada por el Gobierno de Giorgia Meloni, que reemplazará el actual sistema mixto por uno proporcional con un mecanismo de premio de mayoría. La nueva ley será la base de las próximas elecciones generales, previstas para 2027, y llega

## U146
**A** (56 item(s))
- 2026-10-04 03:30 [El País Internacional] Ni Bolsonaro, ni Lula: Trump se reserva (de momento) su apoyo en las elecciones de Brasil
  > Un asistente a un mitin de Flavio Bolsonaro disfrazado de Trump, el pasado domingo.
- 2026-10-04 04:00 [El País Internacional] La disputa entre Lula y Trump marca las elecciones brasileñas
  > Banderas de Flavio Bolsonaro y Luiz Inacio Lula da Silva en Brasilia, el 29 de septiembre.
- 2026-10-04 11:20 [Rai News Esteri] Urne aperte in Brasile per le elezioni presidenziali e legislative, sfida Lula-Bolsonaro
  > Gli ultimi sondaggi davano un testa a testa
- 2026-10-04 20:19 [El País Internacional] Brasil decide su futuro entre Lula y Bolsonaro, un estadista desgastado y el hijo de un ultra
  > El presidente Lula, el día 24 en São Gonçalo, y Flávio Bolsonaro, este sábado en Río.
- 2026-10-04 20:43 [Europa Press Internacional] Bolsonaro gana la primera vuelta en Brasil con el 47% de los votos y disputará contra Lula (45%) la segunda vuelta
  > El candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil e hijo del expresidente Jair Bolsonaro, Flávio Bolsonaro, ha ganado la primera vuelta de las elecciones en Brasil con un 47,17% de los sufragios. Su rival y presidente saliente, Luiz Inácio Lula da Silva, ha quedado cua
- 2026-10-04 22:25 [ANSA Mondo] Media, Lula e Bolsonaro andranno al ballottaggio il 25 ottobre
  > A metà scrutinio Bolsonaro al 49%, Lula a 42%
- 2026-10-04 23:00 [Clarín Mundo] Los Bolsonaro amplían su presencia en el Congreso con las elecciones en Brasil: entran la esposa del ex presidente y dos hermanos de Flavio
  > Michelle, la exprimera dama brasileña alcanzó el 28% de los votos en las elecciones legislativas del Distrito Federal.Otros dos hijos del expresidente Jair Bolsonaro compitieron por bancas legislativas en el estado de Santa Catarina.
- 2026-10-04 23:23 [Clarín Mundo] Elecciones en Brasil: Flávio Bolsonaro, un presidenciable a la sombra de su padre
  > Tiene 45 años y es el mayor de los cinco hijos del ex presidente. Elogia las políticas de seguridad de Nayib Bukele en El Salvador y promete la construcción de numerosas cárceles. Asimismo, presume de su buena relación con Donald Trump tras mantener una reunión privada en la Casa Blanca.
- 2026-10-04 23:23 [Clarín Mundo] Lula da Silva busca su reelección en Brasil: entre el freno a la ultraderecha y la defensa de su legado social
  > • A los 80 años, el mandatario brasileño busca la reelección apoyado en su historial de programas sociales como el Bolsa Familia, que actualmente beneficia a una cuarta parte de la población.
• Con vistas a un nuevo período, impulsa una reforma laboral para reducir la jornada semanal a cinco días y 
- 2026-10-05 00:09 [Rai News Esteri] Il sorpasso di Bolsonaro, la crisi di Lula
  > Flavio Bolsonaro, figlio dell'ex presidente di estrema destra tentato golpista, vince il primo turno sul presidente di sinistra Lula da Silva
- 2026-10-05 00:12 [Clarín Mundo] Elecciones en Brasil: un voto castigo que sorprendió a Lula da Silva y llegó desde su base tradicional de votantes
  > Un primer análisis indica que los sectores de menores ingresos se distanciaron de la elección y del líder del PT. El país es un éxito macro, con números notables, pero esos resultados no llegaron a los bolsillos de ese amplio espacio de votantes que se endeuda para pagar los gastos básicos.
- 2026-10-05 01:03 [Clarín Mundo] Lula acepta el impacto del triunfo de Bolsonaro: fue "un resultado inesperado"
  > El representante del socialista Partido de los Trabajadores busca su cuarto mandato, con la reelección en la gestión actual.Quedó detrás de Flavio Bolsonaro por apenas 2,15 puntos.
- 2026-10-05 01:08 [Clarín Mundo] Flavio Bolsonaro, tras ganar en primera vuelta ante Lula: "Brasil quiere un cambio"
  > Aseguró también que este resultado marcan "el fin de la era del PT" en su país.Dijo estar "feliz" con los números obtenidos frente al actual mandatario, Lula da Silva.
- 2026-10-05 01:41 [El País Internacional] Arrasadora victoria de la derecha en Brasil
  > Flavio Bolsonaro habla con la prensa en Río de Janeiro, este domingo.
- 2026-10-05 02:13 [Europa Press Internacional] Bolsonaro proclama "fin de la era del PT" y Lula apela a combatir su "pasado tenebroso" en la segunda vuelta en Brasil
  > Bolsonaro supera los 55 millones de apoyos (47,04%) y logra una ventaja de 2,3 millones de sufragios sobre el actual mandatario (45,15%)
- 2026-10-05 02:28 [El País Internacional] El apellido Bolsonaro gana desde la cárcel
  > Flávio Bolsonaro, candidato presidencial de Brasil, este domingo tras los resultados de la primera vuelta.
- 2026-10-05 02:39 [BBC Mundo] Cómo se compara Flávio Bolsonaro con su padre Jair y cuánto cambia el duelo con Lula por la presidencia de Brasil 4 años después
  > El senador derechista pasa fortalecido al balotaje contra el presidente de izquierda tras obtener más votos en la primera vuelta contra varios pronósticos, pero la elección sigue abierta.
- 2026-10-05 02:46 [France 24 Español] Simone Pitta: "Con esta primera vuelta se puede ver una consolidación del bolsonarismo en Brasil"
  > Pese a no haber estado en el poder en el último periodo presidencial de Brasil, y pese a las denuncias y condenas contra el expresidente Jair Bolsonaro por un intento de golpe de Estado, el bolsonarismo logró consolidarse de cara a los comicios de este 4 de octubre. Ahora, Flávio Bolsonaro busca pos
- 2026-10-05 02:47 [France 24 Español] Juan Agulló: "A diferencia de otros países de Latinoamérica, Brasil es un competidor directo"
  > En un escenario marcado por la polarización en Brasil, el candidato de ultraderecha y heredero político de su padre, Flávio Bolsonaro, y el actual presidente, Luiz Inácio Lula da Silva, quien busca un cuarto mandato, se disputan el balotaje. La sombra de Estados Unidos estuvo presente durante la pri
- 2026-10-05 02:54 [El País Internacional] Bolsonaro vence a Lula en primera vuelta de las elecciones y acaricia el retorno de la ultraderecha al poder en Brasil
  > Flávio Bolsonaro habla tras clasificarse para la segunda vuelta en Brasilia, Brasil, este domingo.
- 2026-10-05 03:19 [France 24 Español] Brasil: la derecha de Bolsonaro se fortalece en las regiones, con un triunfo holgado en São Paulo
  > Los comicios locales de Brasil se saldaron este domingo con un avance de la derecha que representan el candidato presidencial Flávio Bolsonaro y sus aliados. En tanto la izquierda del presidente y aspirante a la reelección, Luiz Inácio Lula da Silva perdía terreno. La victoria más cómoda fue en São 
- 2026-10-05 03:36 [El País Internacional] Las claves de la primera vuelta en Brasil: de la fuerza ultra al día después de Lula con América Latina pendiente
  > Flávio Bolsonaro vota en Río de Janeiro, este domingo.
- 2026-10-05 03:41 [France 24 Español] Flávio Bolsonaro tritura las encuestas: una ventaja pequeña, pero un escenario cuesta arriba para Lula
  > Brasil quedó inclinado hacia la tendencia de retorno a la derecha que sacude a América Latina, luego de que el senador e hijo del expresidente Jair Bolsonaro aventajara por casi dos puntos al izquierdista Luiz Inácio Lula da Silva en la primera vuelta de las elecciones. Lula ha reconocido el resulta
- 2026-10-05 04:08 [El País Internacional] Videoanálisis | Lula se enfrenta a una segunda vuelta electoral muy complicada
  > Videoanálisis | Lula Y Flávio Bolsonaro se enfrenta a una segunda vuelta electoral
- 2026-10-05 04:33 [Rai News Esteri] Brasile, avanzata del clan Bolsonaro: quattro eletti in Parlamento, Flavio al ballottaggio con Lula
  > L'ex first lady Michelle e Carlos, uno dei figli dell'ex presidente, conquistano un seggio al Senato. Alla Camera entrano il figlio più giovane Jair Renan e Renato, fratello di Jair
- 2026-10-05 05:14 [Il Sole 24 Ore Mondo] Brasile, Bolsonaro vince al primo turno con 47%, Lula al 45%: ballottaggio il 25 ottobre
  > Flavio Bolsonaro batte Lula al primo turno e si lancia come favorito nel ballottaggio del 25 ottobre che deciderà chi sarà il 40esimo presidente del Brasile. Il candidato trumpiano ha ottenuto il 47,14 % dei voti, il presidente uscente il 45.03 %, con una differenza tra i due di circa 2 milioni e me
- 2026-10-05 05:31 [Europa Press Internacional] Trump tacha de "corruptas" las elecciones de EEUU comparándolas con las de Brasil tras la victoria de Bolsonaro
  > El presidente de Estados Unidos, Donald Trump, ha vuelto a cargar contra el proceso electoral en su propio país, tachándolo de corrupto y contraponiéndolo la rapidez en el escrutinio de los votos de 125 millones de personas "en la primera vuelta de las elecciones presidenciales de Brasil", donde el 
- 2026-10-05 05:46 [Europa Press Internacional] Milei felicita a su "querido amigo" Flávio Bolsonaro por su "histórica elección" frente a Lula en Brasil
  > El presidente de Argentina, Javier Milei, ha felicitado al candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil, Flávio Bolsonaro, por su victoria en la primera vuelta de las elecciones presidenciales celebradas este domingo, en las que se ha impuesto con el 47,03% de los vo
- 2026-10-05 06:44 [ANSA Mondo] Brasile, l'ex giudice che condannò Lula eletto governatore
  > Sergio Moro guiderà l'esecutivo del suo stato natale, il Paranà
- 2026-10-05 07:14 [BBC Mundo] Elecciones en Brasil: Flávio Bolsonaro y Lula da Silva van a una segunda vuelta en la que el presidente enfrenta una difícil remontada
  > La mayor democracia de América Latina irá a balotaje el 25 de octubre. Lula lleva la desventaja frente a Bolsonaro, ya que históricamente nunca hubo una remontada en una segunda vuelta electoral en Brasil.
- 2026-10-05 07:46 [ANSA Mondo] In Brasile un 30enne di destra è il deputato più votato della storia
  > Nikolas Ferreira ha raccolto oltre 3,1 milioni di preferenze per la Camera
- 2026-10-05 10:46 [ANSA Mondo] Astensione record in Brasile, il 21,08% non ha votato al primo turno
  > Si tratta del livello più alto registrato dalle elezioni del 1998 (21,5%)
- 2026-10-05 11:42 [France 24 Español] Brasil irá a segunda vuelta: Flávio Bolsonaro lidera la primera ronda
  > Brasil se encamina a una segunda vuelta presidencial tras una elección marcada por la polarización. El senador Flávio Bolsonaro obtuvo el primer lugar en la primera vuelta, pero sin alcanzar la mayoría necesaria para evitar el balotaje. El próximo 25 de octubre se enfrentará al actual presidente, Lu
- 2026-10-05 12:20 [Rai News Esteri] Il primo turno delle presidenziali in Brasile, avanti Bolsonaro: ribaltati i pronostici pro-Lula
  > La sfida per il secondo turno del 25 ottobre è ancora aperta ma il presidente uscente non minimizza il peso di una pesante bocciatura delle sue politiche
- 2026-10-05 12:21 [Rai News Esteri] Presidenziali in Brasile, Flavio Bolsonaro a sorpresa supera Lula di 2 punti. Si va al ballottaggio
  > Il candidato di destra al 47%: "Il Brasile vuole cambiare". Il presidente uscente al 45%: "Sono bravo ai supplementari". Scelta rinviata al secondo turno del 25 ottobre
- 2026-10-05 12:29 [Clarín Mundo] Elecciones en Brasil 2026, EN VIVO: reacciones tras la victoria de Flávio Bolsonaro sobre Lula y últimas noticias del balotaje
  > Bolsonaro se impuso en la primera vuelta al superar por casi dos puntos al actual presidente Lula da Silva. El balotaje entre ambos se hará el 25 de octubre. Todas las repercusiones, minuto a minuto.
- 2026-10-05 12:31 [Clarín Mundo] Quién es Flávio Bolsonaro, el hijo de Jair que sorprendió a Lula y va por la presidencia de Brasil
  > Nacido en el estado de Río de Janeiro, Flávio es el mayor de los cinco hijos del expresidente y el que más se le parece físicamente.Este senador, de 45 años, enfrentará a Lula en el balotaje el próximo 25 de octubre.
- 2026-10-05 13:05 [France 24 Español] Informe desde Río de Janeiro: el Partido Liberal de Bolsonaro se fortalece en el Senado
  > Las elecciones legislativas en Brasil dejaron un resultado clave para el futuro político del país: el Partido Liberal (PL), formación vinculada al expresidente Jair Bolsonaro y que postuló a Flávio Bolsonaro para la Presidencia, amplió significativamente su presencia en el Senado. La bancada pasará 
- 2026-10-05 13:16 [Clarín Mundo] Elecciones en Brasil: los mercados celebran la ventaja de Flávio Bolsonaro sobre Lula y el principal índice de la Bolsa marca un nuevo récord
  > Los activos brasileños se dispararon este lunes y el real se apreció en la primera sesión de los mercados tras los comicios del domingo. El índice Ibovespa superó la marca de los 209.000 puntos por primera vez.
- 2026-10-05 13:57 [BBC Mundo] Quiénes son Lucas Pavanato y Nikolas Ferreira, los jóvenes influencers de derecha que lograron las mayores votaciones en la historia de la Cámara de Diputados de Brasil
  > Los flamantes legisladores comparten una agenda conservadora que incluye el rechazo a las políticas de género, el endurecimiento de las sanciones penales y la legalización del porte de armas como herramienta para combatir la delincuencia.
- 2026-10-05 14:50 [Clarín Mundo] Elecciones en Brasil: los resultados del domingo cambian por completo el diseño del país y ya asoma una amnistía para Jair Bolsonaro
  > La victoria del candidato conservador Flávio Bolsonaro sobre el presidente Lula da Silva en primera vuelta excede lo que pueda ocurrir en el balotaje.La ola de derecha se consolida con victorias en las gobernaciones y especialmente en el Parlamento.Aun si el líder petista lograra imponerse el 25 de 
- 2026-10-05 15:47 [Clarín Mundo] La reacción de los medios en Brasil tras la victoria de Bolsonaro: desde "el ciclo de Lula está terminado" hasta "el tsunami de lo peor de la derecha"
  > Los títulos, opiniones y análisis de la prensa en Brasil tras la primera vuelta de las presidenciales de este domingo.
- 2026-10-05 15:59 [France 24 Español] Flávio Bolsonaro y Lula da Silva se preparan para el balotaje en Brasil
  > 🇧🇷🗳️ Luiz Inácio Lula da Silva y Flávio Bolsonaro ofrecieron declaraciones después de que los resultados de los comicios presidenciales de Brasil confirmaran que deberán disputar el balotaje del 25 de octubre.
- 2026-10-05 16:02 [El País Internacional] El lulismo cruje ante la ofensiva ultra
  > Carteles del presidente Trump y del candidato Flavio Bolsonaro, en São Paulo, Brasil, este Lunes.
- 2026-10-05 16:10 [France 24 Español] "Solo faltan días para el rescate Brasil": Bolsonaro celebra la victoria sobre Lula
  > El senador del Partido Liberal (PL) y candidato presidencial, Flávio Bolsonaro, agradeció este lunes "a Dios" y al pueblo brasileño por su victoria en las elecciones del domingo ante el presidente Luiz Inácio Lula da Silva, en contra de los pronósticos. Además, celebró que el PL resultara el partido
- 2026-10-05 16:23 [Clarín Mundo] Elecciones en Brasil: a contrarreloj, Lula y el PT analizan cambios totales en la estrategia de campaña
  > Lo anticipan fuentes partidarias, pero no es claro en qué consistirán. Trascendió que ha habido tensiones internas sobre el manejo de la campaña.Y que debido a eso se perdieron oportunidades importantes para reducir el impulso del candidato opositor, Flávio Bolsonaro.
- 2026-10-05 16:36 [France 24 Español] Paraguay, refugio fiscal y político para la extrema derecha brasileña
  > En los últimos cinco años, las solicitudes de permisos de residencia de brasileños en Paraguay se han más que duplicado. Muchos de los recién llegados son simpatizantes de Jair Bolsonaro que temen una reelección del actual presidente, Luiz Inácio Lula da Silva, a quien responsabilizan de un deterior
- 2026-10-05 17:02 [ANSA Mondo] Brasile, Erika Hilton è la donna più votata della storia alla Camera
  > La politica brasiliana Erika

Hilton ha stabilito un nuovo record nella storia della Camera

dei deputati brasiliana, diventando la donna più votata di

sempre. La deputata trans del Partito socialismo e libertà

(Psol) di San Paolo è stata rieletta con 1.596.472 voti, pari al

5,9% dei voti espress
- 2026-10-05 17:30 [Clarín Mundo] El fantasma de Bolsonaro reaparece en Europa: los temores de Bruselas ante un eventual cambio de gobierno en Brasil
  > • Un cambio de gobierno en Brasil aportaría argumentos a los eurodiputados que buscan frenar la ratificación del entendimiento comercial.
• Si entre 50 y 80 legisladores modifican su postura en la votación prevista para los próximos meses, la aplicación provisional del pacto quedará suspendida.
- 2026-10-05 18:04 [France 24 Español] El mercado de valores de Brasil aplaude la ventaja de Bolsonaro en primera vuelta presidencial
  > El índice bursátil iBovespa, el más importante de la bolsa de São Paulo inició la jornada con un alza estrepitosa de casi el 9% y alcanzó máximo histórico, mientras el real brasileño gana 4,5% frente al dólar a media jornada, hasta situarse ligeramente por encima de los 5 reales por dólar. El buen r
- 2026-10-05 18:10 [France 24 Español] La dinastía Bolsonaro se fortalece: prensa brasileña sobre la primera vuelta electoral
  > La familia Bolsonaro no solo ganó la primera vuelta en Brasil, fortaleció su presencia en ambas cámaras del Congreso y conserva los respaldos de más de 10 gobernadores. 'O Globo' habla del bloque familiar que se ha hecho con varios cargos. Hermanos, hijos, esposa y exesposa tienen un puesto de elecc
- 2026-10-05 19:41 [El País Internacional] La ola conservadora de América Latina llega a Brasil
  > Flávio Bolsonaro (i) junto al presidente de EE.UU., Donald Trump, en el despacho oval de la Casa Blanca en Washington, el 26 de mayo de 2026.
- 2026-10-05 19:42 [El País Internacional] La victoria en primera vuelta de Bolsonaro impulsa a la ola ultra de América Latina
  > Transeúntes pasan ante pósteres dañados que muestran a Bolsonaro hijo con el presidente Trump, este lunes en São Paulo.
- 2026-10-05 19:47 [Clarín Mundo] Elecciones en Brasil: las urnas de la sorpresa
  > Tras el imprevisto triunfo de Flávio Bolsonaro sobre Lula en la primera vuelta, Brasil se encamina hacia un balotaje decisivo el próximo 25 de octubre. La contienda electoral ratifica la profunda polarización política del país y la consolidación del bolsonarismo como una fuerza de derecha permanente
- 2026-10-05 20:21 [ANSA Mondo] Trump, il risultato di Bolsonaro in Brasile una 'grande vittoria'
  > Il risultato di Flavio Bolsonaro

alle elezioni in Brasile è stata una "grande vittoria". Lo ha

detto Donald Trump.Quella di Bolsonaro "è una grande vittoria: combattuta, ma una

vittoria davvero enorme. Incredibile", ha detto Trump. Bolsonaro

si avvia al ballottaggio del 25 ottobre come favorito.
- 2026-10-05 22:09 [ANSA Mondo] Brasile, l'ex presidente Temer sostiene Bolsonaro al ballottaggio
  > L'ex presidente brasiliano

Michel Temer (2016-2018) ha dichiarato il suo sostegno a Flávio

Bolsonaro in vista del ballottaggio del 25 ottobre contro Luiz

Inácio Lula da Silva. In un video diffuso sui social, Temer ha

affermato che il risultato del primo turno mostra la volontà

degli elettori di
**B** (2 item(s))
- 2026-10-05 09:51 [France 24] Messi set for final emotional farewell in Argentina send-off
  > When Lionel Messi takes to the pitch on Tuesday for his final appearance for Argentina, it will bring an end to a journey that started with football authorities not even knowing his name and evolved into one of the most enduring relationships in sporting history. After announcing his retirement from
- 2026-10-05 12:30 [Al Jazeera] Lionel Messi to join Argentina for farewell match against Benin
  > The friendly marks a symbolic passing of the torch for a player whose international legacy includes a World Cup title.

## U147
**A** (5 item(s))
- 2026-09-29 12:07 [South China Morning Post] Estonia blames Russia for arson attack on company supplying vehicles to Ukraine
  > Estonian authorities said on Tuesday they had concluded that an arson attack in mid-August on a defence company that provides military vehicles to Ukraine was an act of sabotage commissioned by Russian security services.
Foreign Minister Margus Tsahkna said that “such actions are absolutely unaccept
- 2026-09-29 13:15 [BBC World] Estonia blames Russia for arson at defence company supplying Ukraine
  > Russia has been accused of launching sabotage attacks across a number of European Nato countries which have been helping Ukraine.
- 2026-09-29 13:26 [Al Jazeera] Estonia says Russia ordered August arson attack on defence company
  > Tallinn accuses Moscow of responsibility for the fire at Estonian company Milrem Robotics, a supplier of unmanned ground vehicles to Ukraine.
- 2026-09-29 14:42 [Breaking Defense] Estonia accuses Russia of ordering August arson attack on Milrem
  > Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to undermine our unity and support for Ukraine,” NATO Secretary General Mark Rutte said today.
- 2026-09-29 14:52 [Defense News] Estonia blames Russia in arson attack on military robotics firm Milrem
  > GLASGOW, Scotland — Russian special services were behind the fire at a building used by an Estonian military robotics company last month, the government in Tallinn said on Tuesday. The finding comes after a six-week investigation by the Estonian Internal Security Service. In a press statement, the g
**B** (2 item(s))
- 2026-09-30 16:29 [Defense News] US Army selects five companies for PrSM development
  > The U.S. Army on Tuesday signed agreements with Anduril, Castelion, Lockheed Martin, Mach Industries and RTX to create advanced long-range missile prototypes, Redstone Arsenal announced this week. Each company will develop capabilities for the Precision Strike Missile (PrSM) Increment 4 program, mak
- 2026-09-30 19:08 [Breaking Defense] Army taps 5 companies for PrSM Inc 4 prototypes
  > Anduril, Castelion, Lockheed Martin, RTX and Mach Industries were awarded Other Transaction Agreements for an undisclosed amount.

## U148
**A** (2 item(s))
- 2026-10-03 12:22 [BBC Mundo] Lo que la fallida ejecución de Christa Pike revela sobre la pena de muerte en EE.UU.
  > Christa Pike, una mujer condenada a muerte en Tennessee, sobrevivió a la aplicación de dos inyecciones letales. Su caso ha vuelto a centrar la atención en la pena de muerte y en cómo se aplica en Estados Unidos.
- 2026-10-03 19:14 [Il Sole 24 Ore Mondo] Trump vuole estendere la pena di morte ai narcotrafficanti: il caso Pike riapre lo scontro
  > Il presidente promette di ampliare i reati punibili con la pena capitale. Il Tennessee sospende le esecuzioni dopo il caso Pike, mentre una sentenza della Corte Suprema del 2008 lascia aperto il nodo dei grandi narcotrafficanti
**B** (56 item(s))
- 2026-10-04 03:30 [El País Internacional] Ni Bolsonaro, ni Lula: Trump se reserva (de momento) su apoyo en las elecciones de Brasil
  > Un asistente a un mitin de Flavio Bolsonaro disfrazado de Trump, el pasado domingo.
- 2026-10-04 04:00 [El País Internacional] La disputa entre Lula y Trump marca las elecciones brasileñas
  > Banderas de Flavio Bolsonaro y Luiz Inacio Lula da Silva en Brasilia, el 29 de septiembre.
- 2026-10-04 11:20 [Rai News Esteri] Urne aperte in Brasile per le elezioni presidenziali e legislative, sfida Lula-Bolsonaro
  > Gli ultimi sondaggi davano un testa a testa
- 2026-10-04 20:19 [El País Internacional] Brasil decide su futuro entre Lula y Bolsonaro, un estadista desgastado y el hijo de un ultra
  > El presidente Lula, el día 24 en São Gonçalo, y Flávio Bolsonaro, este sábado en Río.
- 2026-10-04 20:43 [Europa Press Internacional] Bolsonaro gana la primera vuelta en Brasil con el 47% de los votos y disputará contra Lula (45%) la segunda vuelta
  > El candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil e hijo del expresidente Jair Bolsonaro, Flávio Bolsonaro, ha ganado la primera vuelta de las elecciones en Brasil con un 47,17% de los sufragios. Su rival y presidente saliente, Luiz Inácio Lula da Silva, ha quedado cua
- 2026-10-04 22:25 [ANSA Mondo] Media, Lula e Bolsonaro andranno al ballottaggio il 25 ottobre
  > A metà scrutinio Bolsonaro al 49%, Lula a 42%
- 2026-10-04 23:00 [Clarín Mundo] Los Bolsonaro amplían su presencia en el Congreso con las elecciones en Brasil: entran la esposa del ex presidente y dos hermanos de Flavio
  > Michelle, la exprimera dama brasileña alcanzó el 28% de los votos en las elecciones legislativas del Distrito Federal.Otros dos hijos del expresidente Jair Bolsonaro compitieron por bancas legislativas en el estado de Santa Catarina.
- 2026-10-04 23:23 [Clarín Mundo] Elecciones en Brasil: Flávio Bolsonaro, un presidenciable a la sombra de su padre
  > Tiene 45 años y es el mayor de los cinco hijos del ex presidente. Elogia las políticas de seguridad de Nayib Bukele en El Salvador y promete la construcción de numerosas cárceles. Asimismo, presume de su buena relación con Donald Trump tras mantener una reunión privada en la Casa Blanca.
- 2026-10-04 23:23 [Clarín Mundo] Lula da Silva busca su reelección en Brasil: entre el freno a la ultraderecha y la defensa de su legado social
  > • A los 80 años, el mandatario brasileño busca la reelección apoyado en su historial de programas sociales como el Bolsa Familia, que actualmente beneficia a una cuarta parte de la población.
• Con vistas a un nuevo período, impulsa una reforma laboral para reducir la jornada semanal a cinco días y 
- 2026-10-05 00:09 [Rai News Esteri] Il sorpasso di Bolsonaro, la crisi di Lula
  > Flavio Bolsonaro, figlio dell'ex presidente di estrema destra tentato golpista, vince il primo turno sul presidente di sinistra Lula da Silva
- 2026-10-05 00:12 [Clarín Mundo] Elecciones en Brasil: un voto castigo que sorprendió a Lula da Silva y llegó desde su base tradicional de votantes
  > Un primer análisis indica que los sectores de menores ingresos se distanciaron de la elección y del líder del PT. El país es un éxito macro, con números notables, pero esos resultados no llegaron a los bolsillos de ese amplio espacio de votantes que se endeuda para pagar los gastos básicos.
- 2026-10-05 01:03 [Clarín Mundo] Lula acepta el impacto del triunfo de Bolsonaro: fue "un resultado inesperado"
  > El representante del socialista Partido de los Trabajadores busca su cuarto mandato, con la reelección en la gestión actual.Quedó detrás de Flavio Bolsonaro por apenas 2,15 puntos.
- 2026-10-05 01:08 [Clarín Mundo] Flavio Bolsonaro, tras ganar en primera vuelta ante Lula: "Brasil quiere un cambio"
  > Aseguró también que este resultado marcan "el fin de la era del PT" en su país.Dijo estar "feliz" con los números obtenidos frente al actual mandatario, Lula da Silva.
- 2026-10-05 01:41 [El País Internacional] Arrasadora victoria de la derecha en Brasil
  > Flavio Bolsonaro habla con la prensa en Río de Janeiro, este domingo.
- 2026-10-05 02:13 [Europa Press Internacional] Bolsonaro proclama "fin de la era del PT" y Lula apela a combatir su "pasado tenebroso" en la segunda vuelta en Brasil
  > Bolsonaro supera los 55 millones de apoyos (47,04%) y logra una ventaja de 2,3 millones de sufragios sobre el actual mandatario (45,15%)
- 2026-10-05 02:28 [El País Internacional] El apellido Bolsonaro gana desde la cárcel
  > Flávio Bolsonaro, candidato presidencial de Brasil, este domingo tras los resultados de la primera vuelta.
- 2026-10-05 02:39 [BBC Mundo] Cómo se compara Flávio Bolsonaro con su padre Jair y cuánto cambia el duelo con Lula por la presidencia de Brasil 4 años después
  > El senador derechista pasa fortalecido al balotaje contra el presidente de izquierda tras obtener más votos en la primera vuelta contra varios pronósticos, pero la elección sigue abierta.
- 2026-10-05 02:46 [France 24 Español] Simone Pitta: "Con esta primera vuelta se puede ver una consolidación del bolsonarismo en Brasil"
  > Pese a no haber estado en el poder en el último periodo presidencial de Brasil, y pese a las denuncias y condenas contra el expresidente Jair Bolsonaro por un intento de golpe de Estado, el bolsonarismo logró consolidarse de cara a los comicios de este 4 de octubre. Ahora, Flávio Bolsonaro busca pos
- 2026-10-05 02:47 [France 24 Español] Juan Agulló: "A diferencia de otros países de Latinoamérica, Brasil es un competidor directo"
  > En un escenario marcado por la polarización en Brasil, el candidato de ultraderecha y heredero político de su padre, Flávio Bolsonaro, y el actual presidente, Luiz Inácio Lula da Silva, quien busca un cuarto mandato, se disputan el balotaje. La sombra de Estados Unidos estuvo presente durante la pri
- 2026-10-05 02:54 [El País Internacional] Bolsonaro vence a Lula en primera vuelta de las elecciones y acaricia el retorno de la ultraderecha al poder en Brasil
  > Flávio Bolsonaro habla tras clasificarse para la segunda vuelta en Brasilia, Brasil, este domingo.
- 2026-10-05 03:19 [France 24 Español] Brasil: la derecha de Bolsonaro se fortalece en las regiones, con un triunfo holgado en São Paulo
  > Los comicios locales de Brasil se saldaron este domingo con un avance de la derecha que representan el candidato presidencial Flávio Bolsonaro y sus aliados. En tanto la izquierda del presidente y aspirante a la reelección, Luiz Inácio Lula da Silva perdía terreno. La victoria más cómoda fue en São 
- 2026-10-05 03:36 [El País Internacional] Las claves de la primera vuelta en Brasil: de la fuerza ultra al día después de Lula con América Latina pendiente
  > Flávio Bolsonaro vota en Río de Janeiro, este domingo.
- 2026-10-05 03:41 [France 24 Español] Flávio Bolsonaro tritura las encuestas: una ventaja pequeña, pero un escenario cuesta arriba para Lula
  > Brasil quedó inclinado hacia la tendencia de retorno a la derecha que sacude a América Latina, luego de que el senador e hijo del expresidente Jair Bolsonaro aventajara por casi dos puntos al izquierdista Luiz Inácio Lula da Silva en la primera vuelta de las elecciones. Lula ha reconocido el resulta
- 2026-10-05 04:08 [El País Internacional] Videoanálisis | Lula se enfrenta a una segunda vuelta electoral muy complicada
  > Videoanálisis | Lula Y Flávio Bolsonaro se enfrenta a una segunda vuelta electoral
- 2026-10-05 04:33 [Rai News Esteri] Brasile, avanzata del clan Bolsonaro: quattro eletti in Parlamento, Flavio al ballottaggio con Lula
  > L'ex first lady Michelle e Carlos, uno dei figli dell'ex presidente, conquistano un seggio al Senato. Alla Camera entrano il figlio più giovane Jair Renan e Renato, fratello di Jair
- 2026-10-05 05:14 [Il Sole 24 Ore Mondo] Brasile, Bolsonaro vince al primo turno con 47%, Lula al 45%: ballottaggio il 25 ottobre
  > Flavio Bolsonaro batte Lula al primo turno e si lancia come favorito nel ballottaggio del 25 ottobre che deciderà chi sarà il 40esimo presidente del Brasile. Il candidato trumpiano ha ottenuto il 47,14 % dei voti, il presidente uscente il 45.03 %, con una differenza tra i due di circa 2 milioni e me
- 2026-10-05 05:31 [Europa Press Internacional] Trump tacha de "corruptas" las elecciones de EEUU comparándolas con las de Brasil tras la victoria de Bolsonaro
  > El presidente de Estados Unidos, Donald Trump, ha vuelto a cargar contra el proceso electoral en su propio país, tachándolo de corrupto y contraponiéndolo la rapidez en el escrutinio de los votos de 125 millones de personas "en la primera vuelta de las elecciones presidenciales de Brasil", donde el 
- 2026-10-05 05:46 [Europa Press Internacional] Milei felicita a su "querido amigo" Flávio Bolsonaro por su "histórica elección" frente a Lula en Brasil
  > El presidente de Argentina, Javier Milei, ha felicitado al candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil, Flávio Bolsonaro, por su victoria en la primera vuelta de las elecciones presidenciales celebradas este domingo, en las que se ha impuesto con el 47,03% de los vo
- 2026-10-05 06:44 [ANSA Mondo] Brasile, l'ex giudice che condannò Lula eletto governatore
  > Sergio Moro guiderà l'esecutivo del suo stato natale, il Paranà
- 2026-10-05 07:14 [BBC Mundo] Elecciones en Brasil: Flávio Bolsonaro y Lula da Silva van a una segunda vuelta en la que el presidente enfrenta una difícil remontada
  > La mayor democracia de América Latina irá a balotaje el 25 de octubre. Lula lleva la desventaja frente a Bolsonaro, ya que históricamente nunca hubo una remontada en una segunda vuelta electoral en Brasil.
- 2026-10-05 07:46 [ANSA Mondo] In Brasile un 30enne di destra è il deputato più votato della storia
  > Nikolas Ferreira ha raccolto oltre 3,1 milioni di preferenze per la Camera
- 2026-10-05 10:46 [ANSA Mondo] Astensione record in Brasile, il 21,08% non ha votato al primo turno
  > Si tratta del livello più alto registrato dalle elezioni del 1998 (21,5%)
- 2026-10-05 11:42 [France 24 Español] Brasil irá a segunda vuelta: Flávio Bolsonaro lidera la primera ronda
  > Brasil se encamina a una segunda vuelta presidencial tras una elección marcada por la polarización. El senador Flávio Bolsonaro obtuvo el primer lugar en la primera vuelta, pero sin alcanzar la mayoría necesaria para evitar el balotaje. El próximo 25 de octubre se enfrentará al actual presidente, Lu
- 2026-10-05 12:20 [Rai News Esteri] Il primo turno delle presidenziali in Brasile, avanti Bolsonaro: ribaltati i pronostici pro-Lula
  > La sfida per il secondo turno del 25 ottobre è ancora aperta ma il presidente uscente non minimizza il peso di una pesante bocciatura delle sue politiche
- 2026-10-05 12:21 [Rai News Esteri] Presidenziali in Brasile, Flavio Bolsonaro a sorpresa supera Lula di 2 punti. Si va al ballottaggio
  > Il candidato di destra al 47%: "Il Brasile vuole cambiare". Il presidente uscente al 45%: "Sono bravo ai supplementari". Scelta rinviata al secondo turno del 25 ottobre
- 2026-10-05 12:29 [Clarín Mundo] Elecciones en Brasil 2026, EN VIVO: reacciones tras la victoria de Flávio Bolsonaro sobre Lula y últimas noticias del balotaje
  > Bolsonaro se impuso en la primera vuelta al superar por casi dos puntos al actual presidente Lula da Silva. El balotaje entre ambos se hará el 25 de octubre. Todas las repercusiones, minuto a minuto.
- 2026-10-05 12:31 [Clarín Mundo] Quién es Flávio Bolsonaro, el hijo de Jair que sorprendió a Lula y va por la presidencia de Brasil
  > Nacido en el estado de Río de Janeiro, Flávio es el mayor de los cinco hijos del expresidente y el que más se le parece físicamente.Este senador, de 45 años, enfrentará a Lula en el balotaje el próximo 25 de octubre.
- 2026-10-05 13:05 [France 24 Español] Informe desde Río de Janeiro: el Partido Liberal de Bolsonaro se fortalece en el Senado
  > Las elecciones legislativas en Brasil dejaron un resultado clave para el futuro político del país: el Partido Liberal (PL), formación vinculada al expresidente Jair Bolsonaro y que postuló a Flávio Bolsonaro para la Presidencia, amplió significativamente su presencia en el Senado. La bancada pasará 
- 2026-10-05 13:16 [Clarín Mundo] Elecciones en Brasil: los mercados celebran la ventaja de Flávio Bolsonaro sobre Lula y el principal índice de la Bolsa marca un nuevo récord
  > Los activos brasileños se dispararon este lunes y el real se apreció en la primera sesión de los mercados tras los comicios del domingo. El índice Ibovespa superó la marca de los 209.000 puntos por primera vez.
- 2026-10-05 13:57 [BBC Mundo] Quiénes son Lucas Pavanato y Nikolas Ferreira, los jóvenes influencers de derecha que lograron las mayores votaciones en la historia de la Cámara de Diputados de Brasil
  > Los flamantes legisladores comparten una agenda conservadora que incluye el rechazo a las políticas de género, el endurecimiento de las sanciones penales y la legalización del porte de armas como herramienta para combatir la delincuencia.
- 2026-10-05 14:50 [Clarín Mundo] Elecciones en Brasil: los resultados del domingo cambian por completo el diseño del país y ya asoma una amnistía para Jair Bolsonaro
  > La victoria del candidato conservador Flávio Bolsonaro sobre el presidente Lula da Silva en primera vuelta excede lo que pueda ocurrir en el balotaje.La ola de derecha se consolida con victorias en las gobernaciones y especialmente en el Parlamento.Aun si el líder petista lograra imponerse el 25 de 
- 2026-10-05 15:47 [Clarín Mundo] La reacción de los medios en Brasil tras la victoria de Bolsonaro: desde "el ciclo de Lula está terminado" hasta "el tsunami de lo peor de la derecha"
  > Los títulos, opiniones y análisis de la prensa en Brasil tras la primera vuelta de las presidenciales de este domingo.
- 2026-10-05 15:59 [France 24 Español] Flávio Bolsonaro y Lula da Silva se preparan para el balotaje en Brasil
  > 🇧🇷🗳️ Luiz Inácio Lula da Silva y Flávio Bolsonaro ofrecieron declaraciones después de que los resultados de los comicios presidenciales de Brasil confirmaran que deberán disputar el balotaje del 25 de octubre.
- 2026-10-05 16:02 [El País Internacional] El lulismo cruje ante la ofensiva ultra
  > Carteles del presidente Trump y del candidato Flavio Bolsonaro, en São Paulo, Brasil, este Lunes.
- 2026-10-05 16:10 [France 24 Español] "Solo faltan días para el rescate Brasil": Bolsonaro celebra la victoria sobre Lula
  > El senador del Partido Liberal (PL) y candidato presidencial, Flávio Bolsonaro, agradeció este lunes "a Dios" y al pueblo brasileño por su victoria en las elecciones del domingo ante el presidente Luiz Inácio Lula da Silva, en contra de los pronósticos. Además, celebró que el PL resultara el partido
- 2026-10-05 16:23 [Clarín Mundo] Elecciones en Brasil: a contrarreloj, Lula y el PT analizan cambios totales en la estrategia de campaña
  > Lo anticipan fuentes partidarias, pero no es claro en qué consistirán. Trascendió que ha habido tensiones internas sobre el manejo de la campaña.Y que debido a eso se perdieron oportunidades importantes para reducir el impulso del candidato opositor, Flávio Bolsonaro.
- 2026-10-05 16:36 [France 24 Español] Paraguay, refugio fiscal y político para la extrema derecha brasileña
  > En los últimos cinco años, las solicitudes de permisos de residencia de brasileños en Paraguay se han más que duplicado. Muchos de los recién llegados son simpatizantes de Jair Bolsonaro que temen una reelección del actual presidente, Luiz Inácio Lula da Silva, a quien responsabilizan de un deterior
- 2026-10-05 17:02 [ANSA Mondo] Brasile, Erika Hilton è la donna più votata della storia alla Camera
  > La politica brasiliana Erika

Hilton ha stabilito un nuovo record nella storia della Camera

dei deputati brasiliana, diventando la donna più votata di

sempre. La deputata trans del Partito socialismo e libertà

(Psol) di San Paolo è stata rieletta con 1.596.472 voti, pari al

5,9% dei voti espress
- 2026-10-05 17:30 [Clarín Mundo] El fantasma de Bolsonaro reaparece en Europa: los temores de Bruselas ante un eventual cambio de gobierno en Brasil
  > • Un cambio de gobierno en Brasil aportaría argumentos a los eurodiputados que buscan frenar la ratificación del entendimiento comercial.
• Si entre 50 y 80 legisladores modifican su postura en la votación prevista para los próximos meses, la aplicación provisional del pacto quedará suspendida.
- 2026-10-05 18:04 [France 24 Español] El mercado de valores de Brasil aplaude la ventaja de Bolsonaro en primera vuelta presidencial
  > El índice bursátil iBovespa, el más importante de la bolsa de São Paulo inició la jornada con un alza estrepitosa de casi el 9% y alcanzó máximo histórico, mientras el real brasileño gana 4,5% frente al dólar a media jornada, hasta situarse ligeramente por encima de los 5 reales por dólar. El buen r
- 2026-10-05 18:10 [France 24 Español] La dinastía Bolsonaro se fortalece: prensa brasileña sobre la primera vuelta electoral
  > La familia Bolsonaro no solo ganó la primera vuelta en Brasil, fortaleció su presencia en ambas cámaras del Congreso y conserva los respaldos de más de 10 gobernadores. 'O Globo' habla del bloque familiar que se ha hecho con varios cargos. Hermanos, hijos, esposa y exesposa tienen un puesto de elecc
- 2026-10-05 19:41 [El País Internacional] La ola conservadora de América Latina llega a Brasil
  > Flávio Bolsonaro (i) junto al presidente de EE.UU., Donald Trump, en el despacho oval de la Casa Blanca en Washington, el 26 de mayo de 2026.
- 2026-10-05 19:42 [El País Internacional] La victoria en primera vuelta de Bolsonaro impulsa a la ola ultra de América Latina
  > Transeúntes pasan ante pósteres dañados que muestran a Bolsonaro hijo con el presidente Trump, este lunes en São Paulo.
- 2026-10-05 19:47 [Clarín Mundo] Elecciones en Brasil: las urnas de la sorpresa
  > Tras el imprevisto triunfo de Flávio Bolsonaro sobre Lula en la primera vuelta, Brasil se encamina hacia un balotaje decisivo el próximo 25 de octubre. La contienda electoral ratifica la profunda polarización política del país y la consolidación del bolsonarismo como una fuerza de derecha permanente
- 2026-10-05 20:21 [ANSA Mondo] Trump, il risultato di Bolsonaro in Brasile una 'grande vittoria'
  > Il risultato di Flavio Bolsonaro

alle elezioni in Brasile è stata una "grande vittoria". Lo ha

detto Donald Trump.Quella di Bolsonaro "è una grande vittoria: combattuta, ma una

vittoria davvero enorme. Incredibile", ha detto Trump. Bolsonaro

si avvia al ballottaggio del 25 ottobre come favorito.
- 2026-10-05 22:09 [ANSA Mondo] Brasile, l'ex presidente Temer sostiene Bolsonaro al ballottaggio
  > L'ex presidente brasiliano

Michel Temer (2016-2018) ha dichiarato il suo sostegno a Flávio

Bolsonaro in vista del ballottaggio del 25 ottobre contro Luiz

Inácio Lula da Silva. In un video diffuso sui social, Temer ha

affermato che il risultato del primo turno mostra la volontà

degli elettori di

## U149
**A** (3 item(s))
- 2026-10-05 03:37 [BBC World] Trump unveils 'Super Intelligence Force' to oversee AI policy
  > The president named his national intelligence chief as the taskforce's head as worries over AI grow.
- 2026-10-05 10:03 [BBC World] Trump chooses top spy boss to run new AI taskforce
  > The US president said his national intelligence chief will lead the group as worries over AI grow.
- 2026-10-05 10:09 [France 24] Trump names Jay Clayton as AI czar to lead 'Super Intelligence Force'
  > US President Donald Trump has named his National Intelligence Director Jay Clayton as America's "Super Intelligence" czar, as fears over AI grow. Also, oil markets react to Houthi attacks as well as export data, and France's fiscal woes drive the euro to a 17-month low.
**B** (5 item(s))
- 2026-10-05 04:07 [Al Jazeera] Russian lab worker dies of suspected plague in Siberia; US monitoring case
  > A Russian agency links the lab worker&#039;s death to &#039;pneumonia of unknown&#039; origin.
- 2026-10-05 17:14 [South China Morning Post] After plague death reports at Siberia lab, Russia says situation under control
  > Moscow on Monday downplayed reports that a laboratory technician had died of plague, stressing that postmortem tests had not detected the disease, while Washington said it was closely monitoring the situation.
Reports on Friday that plague had killed a 28-year-old woman named Darya Shipilova, who ha
- 2026-10-05 19:19 [France 24] Russian officials say 'situation under control' after plague reports
  > Moscow on Monday downplayed reports that a laboratory technician had died of plague, stressing that post-mortem tests had not detected the disease, while Washington said it was closely monitoring the situation. Reports on Friday that plague had killed a 28-year-old woman named Darya Shipilova, who h
- 2026-10-05 19:55 [BBC World] US 'watching closely' after plague researcher dies in Russia, Rubio says
  > The US says it is monitoring the case of a lab technician who died at a plague research centre in Siberia.
- 2026-10-05 21:03 [Al Jazeera] Trump says US ready to aid Russia with plague outbreak in Siberia
  > Russian authorities quarantine hospital, monitor 200 contacts after suspected pneumonic plague death in Siberia.

## U150
**A** (5 item(s))
- 2026-10-08 02:35 [Europa Press Internacional] Trump vuelve a hipotetizar sobre ataques iraníes en Los Ángeles y San Diego pese a la polémica generada
  > El presidente de Estados Unidos, Donald Trump, ha reiterado sus controvertidos comentarios acerca de hipotéticos bombardeos iraníes contra las ciudades de Los Ángeles y San Diego --ambas gobernadas por demócratas-- presentando tales eventos como "trauma", "problemas" o "espectáculo de terror" antes 
- 2026-10-08 04:57 [Il Sole 24 Ore Mondo] Guerra in Iran, ultime notizie. «Da Pentagono ordine alle forze armate Usa per eventuale ripresa degli attacchi»
- 2026-10-08 12:26 [El País Internacional] Dos asesores de Trump viajaron a Bosnia-Herzegovina para ayudar al prorruso Milorad Dodik a ganar las elecciones
  > Chris LaCivita, en el centro, viajaba en Estados Unidos junto a Donald Trump a bordo de su avión, conocido como Trump Force One, el lunes 13 de marzo de 2023.
- 2026-10-08 16:35 [Europa Press Internacional] Trump asegura que el Ejército de EEUU no atacará Irán "antes" de las elecciones del 3 de noviembre
  > El presidente de Estados Unidos, Donald Trump, ha asegurado este jueves que no ordenará "ningún" ataque contra Irán antes de las elecciones legislativas, previstas para el próximo 3 de noviembre, mientras las autoridades iraníes sostienen que responderán "en unos días" a la última propuesta de paz p
- 2026-10-08 17:52 [ANSA Mondo] Trump, 'non attaccheremo Iran prima delle midterm, colloqui produttivi con Teheran'
  > "Non attaccheremo l'Iran prima

delle elezioni di metà mandato". Lo afferma Donald Trump sul suo

social Truth, sottolineando che gli Stati Uniti stanno avendo

"discussioni produttive" con l'Iran.

Riproduzione riservata © Copyright ANSA
**B** (3 item(s))
- 2026-10-08 14:09 [France 24] Search warrants for former prince Andrew's homes were unlawful, UK court rules
  > Police who searched the properties of Andrew Mountbatten-Windsor as part of investigations into his links to the late sex offender Jeffrey Epstein have agreed the search warrants were unlawful, a London judge said Thursday. The 66-year-old younger brother of King Charles II was arrested on February 
- 2026-10-08 15:20 [South China Morning Post] UK police accept ex-prince Andrew search warrants must be ‘legally quashed’
  > British police on Thursday said that search warrants they secured to search properties linked to Andrew Mountbatten-Windsor had been issued unlawfully and must be quashed, but that the investigation into King Charles’ younger brother was ongoing.
Mountbatten-Windsor, 66, was arrested on suspicion of
- 2026-10-08 15:53 [Al Jazeera] UK ex-prince Andrew search warrants quashed after police accept legal error
  > London-based judge says error &#039;does not bring investigation to an end&#039; as police probe disgraced former royal.

## U151
**A** (12 item(s))
- 2026-10-03 17:24 [BBC Mundo] En fotos: las multitudinarias protestas en España contra la crisis de la vivienda
  > En decenas de ciudades se registraron manifestaciones después de que el Gobierno fracasara en su intento de lograr la aprobación parlamentaria de las medidas destinadas a frenar la subida de los alquileres y el precio de la vivienda.
- 2026-10-05 07:18 [Clarín Mundo] Pedro Sánchez adelantó las elecciones generales en España para el 29 de noviembre
  > El presidente español emitió un mensaje desde el Palacio de La Moncloa.En su discurso llamó a los españoles a decidir si quieren sumarse "a la ola derechista o seguir siendo un baluarte de justicia social".
- 2026-10-05 08:54 [France 24 Español] Pedro Sánchez anuncia elecciones anticipadas en España para el 29 de noviembre
  > El presidente del Gobierno español, el socialista Pedro Sánchez, anunció este lunes el adelanto de las elecciones generales al 29 de noviembre. Esto tras el rechazo por parte del Congreso de los diputados, el pasado viernes de los dos decretos sobre la vivienda en medio de masivas protestas de inqui
- 2026-10-05 10:09 [France 24 Español] Pedro Sánchez adelanta las elecciones en España al 29 de noviembre tras el revés parlamentario por la vivienda
  > El presidente del Gobierno español, Pedro Sánchez, decidió adelantar las elecciones generales al 29 de noviembre, después de que su Ejecutivo sufriera un nuevo revés parlamentario con el rechazo de sus medidas sobre vivienda. La convocatoria pone fin a la intención de agotar la legislatura hasta 202
- 2026-10-05 10:50 [France 24 Español] “Necesitamos una mayoría más amplia”: España adelanta las elecciones al 29 de noviembre
  > El presidente del gobierno español, Pedro Sánchez, anunció este lunes la disolución de las Cortes y el adelanto de las elecciones generales, después de que el Congreso de los Diputados rechazara el viernes dos decretos impulsados por el Ejecutivo con medidas para aliviar la crisis de vivienda. Las e
- 2026-10-05 10:54 [France 24 Español] Informe desde Barcelona: Pedro Sánchez convoca elecciones anticipadas en España
  > España se encamina a unas elecciones generales anticipadas después de que el presidente del Gobierno, Pedro Sánchez, anunciara la disolución de las Cortes y la convocatoria de comicios para el próximo 29 de noviembre. La decisión llega tras la derrota parlamentaria de los decretos de vivienda impuls
- 2026-10-05 12:31 [BBC Mundo] Pedro Sánchez convoca elecciones anticipadas tras el fracaso en el Congreso de sus decretos para enfrentar la crisis de la vivienda en España
  > El anuncio de Sánchez se produce tras varios días de protestas en el país europeo, surgidas a raíz del desalojo de la anciana Maricarmen. Las elecciones se celebrarán el próximo 29 de noviembre.
- 2026-10-05 14:39 [France 24 Español] Ruth Forero:"La intención de Pedro Sánchez es aprovechar la movilización en las calles"
  > España se encamina a unas elecciones generales anticipadas después de que el presidente del Gobierno, Pedro Sánchez, anunciara la disolución de las Cortes y la convocatoria de comicios para el 29 de noviembre. La decisión llega tras el rechazo parlamentario de los decretos de vivienda impulsados por
- 2026-10-05 19:00 [France 24 Español] La derecha celebra, la izquierda se organiza: así reacciona la política en España al adelanto electoral
  > El líder opositor Alberto Núñez Feijóo, que llevaba meses reclamando comicios anticipados, destacó que "por fin votaremos y España podrá elegir el país que quiere ser". Su Partido Popular encabeza las encuestas y, para él, las elecciones "van de que España gane a Sánchez y lo que representa". Desde 
- 2026-10-05 21:00 [Clarín Mundo] La sombra de la extrema derecha sobre Europa: de las presidenciales en Francia al adelantamiento electoral en España
  > • Un tercio de los gobiernos del bloque continental renovará sus mandatos a lo largo de los próximos doce meses.
• La masa de votantes definirá las administraciones de las principales potencias de la región, salvo en el caso alemán.
- 2026-10-05 21:40 [BBC Mundo] Por qué Pedro Sánchez decidió convocar elecciones anticipadas en España ahora
  > El llamado a elecciones anticipadas no fue una reacción impulsiva, sino una maniobra cuidadosamente meditada.
- 2026-10-05 22:03 [France 24 Español] Directo a... Madrid y el adelanto de las elecciones en España en medio de la crisis de vivienda
  > La crisis de vivienda en España y el rechazo del Congreso a las propuestas temporales para aliviar la situación empujó al presidente de Gobierno, Pedro Sánchez, a convocar elecciones anticipadas, estimadas para 2027, y disolvió las Cortes. Nuestra corresponsal Marina Colorado nos amplió la informaci
**B** (6 item(s))
- 2026-10-05 07:14 [Al Jazeera] Spanish Prime Minister Pedro Sanchez announces snap election
  > Sanchez calls early vote after parliament rejected housing relief measures proposed by his minority government.
- 2026-10-05 08:04 [South China Morning Post] Spain’s prime minister calls early election as housing becomes national flashpoint
  > Spanish Prime Minister Pedro Sanchez announced early elections Monday after his government suffered a bruising legislative defeat last week on emergency measures related to the country’s housing crisis.
The vote will be held on November 29.
In recent weeks, Spaniards have demanded solutions from the
- 2026-10-05 10:18 [BBC World] Spanish PM Sánchez calls early election after housing protests
  > Sánchez says Spain will head to the polls on 29 November after recent defeats on measures aimed at addressing the country's housing crisis.
- 2026-10-05 17:27 [Al Jazeera] Spain calls snap election amid housing crisis
  > Mounting anger over Spain’s housing crisis have led Prime Minister Sanchez to call an early election on November 29
- 2026-10-05 19:30 [BBC World] Spain PM pins hopes on housing crisis to help win snap election
  > Calling of a snap election was not a knee-jerk reaction from Pedro Sánchez but a carefully thought-out manoeuvre, Guy Hedgecoe reports from Madrid.
- 2026-10-05 19:31 [France 24] Sanchez chose 'best moment in a sea of troubles' to call for snap election, analyst says
  > Spanish Prime Minister Pedro Sanchez on Monday called an early election for November 29, aiming to increase his parliamentary support after lawmakers last week rejected proposals to address a housing crisis that has drawn nationwide protests. Speaking with FRANCE 24's Mark Owen, Javier Carbonell, Po

## U152
**A** (10 item(s))
- 2026-10-04 21:31 [South China Morning Post] US Air Force removes all bombers from UK airbase targeted by suspected terror attack
  > The US Air Force has brought home its bombers stationed at a US-run military airbase in England used to strike Iran following an investigation into a planned terror attack at the RAF Fairford base.
The bombers were redeployed back to their home bases in the United States, according to a Pentagon off
- 2026-10-04 22:23 [Al Jazeera] US withdraws B-1 bomber aircraft from UK’s Fairford base amid Iran fears
  > The abrupt redeployment to the US comes after several &#039;terrorism-related&#039; arrests were made outside RAF Fairford.
- 2026-10-05 04:58 [BBC World] US air force removes all bombers from British military base RAF Fairford
  > A statement says all bombers deployed to RAF Fairford have been "re-deployed to their home stations" in the US.
- 2026-10-05 07:40 [Defense News] US removes B-1 bombers from UK base amid security concerns
  > NEW YORK — The United States removed its B-1 bombers from a U.K. air base one week after several men were arrested there on suspicion of preparing terrorist acts, a Pentagon official said on Sunday. A dozen B-1 bombers were stationed at RAF Fairford air base, located northwest of London. The planes 
- 2026-10-05 09:49 [France 24] US withdraws all bombers from UK base at centre of suspected terror attack
  > The United States has removed its B-1 bombers from a British air base one week after five men were arrested nearby on suspicion of preparing terrorist acts, a ‌suspected plot that British Prime Minister Andy Burnham said was likely backed by Iran. The planes had been ⁠stationed at RAF Fairford, whic
- 2026-10-05 11:09 [Al Jazeera] US abruptly withdraws bombers from UK’s RAF Fairford
  > The US has abruptly withdrawn all of its aircraft from the UK’s RAF Fairford, citing concerns about a potential attack.
- 2026-10-05 12:07 [BBC World] No10 insists UK military base RAF Fairford is safe after US withdraws bombers
  > US media reported a new threat led to the bombers being removed on Sunday, following an incident near the base last week.
- 2026-10-05 17:34 [Al Jazeera] Rubio: No direct link between US bombers removal and UK base incident
  > Rubio stresses US base security, following the removal of B-1 bombers amid alleged threats targeting UK military assets.
- 2026-10-05 19:58 [BBC World] Trump says 'threat' led US to pull bombers from RAF Fairford
  > The Pentagon confirmed on Sunday it had removed the B1 bombers from the base in England back to their home stations in America.
- 2026-10-05 21:40 [South China Morning Post] US bombers moved from UK airbase due to Iran-linked threats, Trump says
  > US President Donald Trump said on Monday that a threat linked to Iran ⁠had prompted the removal of American B-1 bombers from a British airbase.
The planes had been stationed at RAF Fairford, the preferred European base for US bombers, and had recently been used in US strikes on Iran. Last week, five
**B** (2 item(s))
- 2026-10-05 09:07 [South China Morning Post] Ex-prince Andrew takes UK police to court to ‘quash’ Epstein affair search warrants
  > Britain’s disgraced former prince, Andrew Mountbatten-Windsor, has launched a High Court challenge “to quash search warrants” obtained by police ahead of his arrest earlier this year, the judiciary has confirmed.
The London court was set to hold a private hearing on Thursday, the judiciary said in a
- 2026-10-05 10:38 [Al Jazeera] Former Prince Andrew launches challenge to ‘quash’ police search warrants
  > A London court is likely to hold a private hearing on Thursday as Mountbatten-Windsor challenges Thames Valley Police.

## U153
**A** (56 item(s))
- 2026-10-04 03:30 [El País Internacional] Ni Bolsonaro, ni Lula: Trump se reserva (de momento) su apoyo en las elecciones de Brasil
  > Un asistente a un mitin de Flavio Bolsonaro disfrazado de Trump, el pasado domingo.
- 2026-10-04 04:00 [El País Internacional] La disputa entre Lula y Trump marca las elecciones brasileñas
  > Banderas de Flavio Bolsonaro y Luiz Inacio Lula da Silva en Brasilia, el 29 de septiembre.
- 2026-10-04 11:20 [Rai News Esteri] Urne aperte in Brasile per le elezioni presidenziali e legislative, sfida Lula-Bolsonaro
  > Gli ultimi sondaggi davano un testa a testa
- 2026-10-04 20:19 [El País Internacional] Brasil decide su futuro entre Lula y Bolsonaro, un estadista desgastado y el hijo de un ultra
  > El presidente Lula, el día 24 en São Gonçalo, y Flávio Bolsonaro, este sábado en Río.
- 2026-10-04 20:43 [Europa Press Internacional] Bolsonaro gana la primera vuelta en Brasil con el 47% de los votos y disputará contra Lula (45%) la segunda vuelta
  > El candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil e hijo del expresidente Jair Bolsonaro, Flávio Bolsonaro, ha ganado la primera vuelta de las elecciones en Brasil con un 47,17% de los sufragios. Su rival y presidente saliente, Luiz Inácio Lula da Silva, ha quedado cua
- 2026-10-04 22:25 [ANSA Mondo] Media, Lula e Bolsonaro andranno al ballottaggio il 25 ottobre
  > A metà scrutinio Bolsonaro al 49%, Lula a 42%
- 2026-10-04 23:00 [Clarín Mundo] Los Bolsonaro amplían su presencia en el Congreso con las elecciones en Brasil: entran la esposa del ex presidente y dos hermanos de Flavio
  > Michelle, la exprimera dama brasileña alcanzó el 28% de los votos en las elecciones legislativas del Distrito Federal.Otros dos hijos del expresidente Jair Bolsonaro compitieron por bancas legislativas en el estado de Santa Catarina.
- 2026-10-04 23:23 [Clarín Mundo] Elecciones en Brasil: Flávio Bolsonaro, un presidenciable a la sombra de su padre
  > Tiene 45 años y es el mayor de los cinco hijos del ex presidente. Elogia las políticas de seguridad de Nayib Bukele en El Salvador y promete la construcción de numerosas cárceles. Asimismo, presume de su buena relación con Donald Trump tras mantener una reunión privada en la Casa Blanca.
- 2026-10-04 23:23 [Clarín Mundo] Lula da Silva busca su reelección en Brasil: entre el freno a la ultraderecha y la defensa de su legado social
  > • A los 80 años, el mandatario brasileño busca la reelección apoyado en su historial de programas sociales como el Bolsa Familia, que actualmente beneficia a una cuarta parte de la población.
• Con vistas a un nuevo período, impulsa una reforma laboral para reducir la jornada semanal a cinco días y 
- 2026-10-05 00:09 [Rai News Esteri] Il sorpasso di Bolsonaro, la crisi di Lula
  > Flavio Bolsonaro, figlio dell'ex presidente di estrema destra tentato golpista, vince il primo turno sul presidente di sinistra Lula da Silva
- 2026-10-05 00:12 [Clarín Mundo] Elecciones en Brasil: un voto castigo que sorprendió a Lula da Silva y llegó desde su base tradicional de votantes
  > Un primer análisis indica que los sectores de menores ingresos se distanciaron de la elección y del líder del PT. El país es un éxito macro, con números notables, pero esos resultados no llegaron a los bolsillos de ese amplio espacio de votantes que se endeuda para pagar los gastos básicos.
- 2026-10-05 01:03 [Clarín Mundo] Lula acepta el impacto del triunfo de Bolsonaro: fue "un resultado inesperado"
  > El representante del socialista Partido de los Trabajadores busca su cuarto mandato, con la reelección en la gestión actual.Quedó detrás de Flavio Bolsonaro por apenas 2,15 puntos.
- 2026-10-05 01:08 [Clarín Mundo] Flavio Bolsonaro, tras ganar en primera vuelta ante Lula: "Brasil quiere un cambio"
  > Aseguró también que este resultado marcan "el fin de la era del PT" en su país.Dijo estar "feliz" con los números obtenidos frente al actual mandatario, Lula da Silva.
- 2026-10-05 01:41 [El País Internacional] Arrasadora victoria de la derecha en Brasil
  > Flavio Bolsonaro habla con la prensa en Río de Janeiro, este domingo.
- 2026-10-05 02:13 [Europa Press Internacional] Bolsonaro proclama "fin de la era del PT" y Lula apela a combatir su "pasado tenebroso" en la segunda vuelta en Brasil
  > Bolsonaro supera los 55 millones de apoyos (47,04%) y logra una ventaja de 2,3 millones de sufragios sobre el actual mandatario (45,15%)
- 2026-10-05 02:28 [El País Internacional] El apellido Bolsonaro gana desde la cárcel
  > Flávio Bolsonaro, candidato presidencial de Brasil, este domingo tras los resultados de la primera vuelta.
- 2026-10-05 02:39 [BBC Mundo] Cómo se compara Flávio Bolsonaro con su padre Jair y cuánto cambia el duelo con Lula por la presidencia de Brasil 4 años después
  > El senador derechista pasa fortalecido al balotaje contra el presidente de izquierda tras obtener más votos en la primera vuelta contra varios pronósticos, pero la elección sigue abierta.
- 2026-10-05 02:46 [France 24 Español] Simone Pitta: "Con esta primera vuelta se puede ver una consolidación del bolsonarismo en Brasil"
  > Pese a no haber estado en el poder en el último periodo presidencial de Brasil, y pese a las denuncias y condenas contra el expresidente Jair Bolsonaro por un intento de golpe de Estado, el bolsonarismo logró consolidarse de cara a los comicios de este 4 de octubre. Ahora, Flávio Bolsonaro busca pos
- 2026-10-05 02:47 [France 24 Español] Juan Agulló: "A diferencia de otros países de Latinoamérica, Brasil es un competidor directo"
  > En un escenario marcado por la polarización en Brasil, el candidato de ultraderecha y heredero político de su padre, Flávio Bolsonaro, y el actual presidente, Luiz Inácio Lula da Silva, quien busca un cuarto mandato, se disputan el balotaje. La sombra de Estados Unidos estuvo presente durante la pri
- 2026-10-05 02:54 [El País Internacional] Bolsonaro vence a Lula en primera vuelta de las elecciones y acaricia el retorno de la ultraderecha al poder en Brasil
  > Flávio Bolsonaro habla tras clasificarse para la segunda vuelta en Brasilia, Brasil, este domingo.
- 2026-10-05 03:19 [France 24 Español] Brasil: la derecha de Bolsonaro se fortalece en las regiones, con un triunfo holgado en São Paulo
  > Los comicios locales de Brasil se saldaron este domingo con un avance de la derecha que representan el candidato presidencial Flávio Bolsonaro y sus aliados. En tanto la izquierda del presidente y aspirante a la reelección, Luiz Inácio Lula da Silva perdía terreno. La victoria más cómoda fue en São 
- 2026-10-05 03:36 [El País Internacional] Las claves de la primera vuelta en Brasil: de la fuerza ultra al día después de Lula con América Latina pendiente
  > Flávio Bolsonaro vota en Río de Janeiro, este domingo.
- 2026-10-05 03:41 [France 24 Español] Flávio Bolsonaro tritura las encuestas: una ventaja pequeña, pero un escenario cuesta arriba para Lula
  > Brasil quedó inclinado hacia la tendencia de retorno a la derecha que sacude a América Latina, luego de que el senador e hijo del expresidente Jair Bolsonaro aventajara por casi dos puntos al izquierdista Luiz Inácio Lula da Silva en la primera vuelta de las elecciones. Lula ha reconocido el resulta
- 2026-10-05 04:08 [El País Internacional] Videoanálisis | Lula se enfrenta a una segunda vuelta electoral muy complicada
  > Videoanálisis | Lula Y Flávio Bolsonaro se enfrenta a una segunda vuelta electoral
- 2026-10-05 04:33 [Rai News Esteri] Brasile, avanzata del clan Bolsonaro: quattro eletti in Parlamento, Flavio al ballottaggio con Lula
  > L'ex first lady Michelle e Carlos, uno dei figli dell'ex presidente, conquistano un seggio al Senato. Alla Camera entrano il figlio più giovane Jair Renan e Renato, fratello di Jair
- 2026-10-05 05:14 [Il Sole 24 Ore Mondo] Brasile, Bolsonaro vince al primo turno con 47%, Lula al 45%: ballottaggio il 25 ottobre
  > Flavio Bolsonaro batte Lula al primo turno e si lancia come favorito nel ballottaggio del 25 ottobre che deciderà chi sarà il 40esimo presidente del Brasile. Il candidato trumpiano ha ottenuto il 47,14 % dei voti, il presidente uscente il 45.03 %, con una differenza tra i due di circa 2 milioni e me
- 2026-10-05 05:31 [Europa Press Internacional] Trump tacha de "corruptas" las elecciones de EEUU comparándolas con las de Brasil tras la victoria de Bolsonaro
  > El presidente de Estados Unidos, Donald Trump, ha vuelto a cargar contra el proceso electoral en su propio país, tachándolo de corrupto y contraponiéndolo la rapidez en el escrutinio de los votos de 125 millones de personas "en la primera vuelta de las elecciones presidenciales de Brasil", donde el 
- 2026-10-05 05:46 [Europa Press Internacional] Milei felicita a su "querido amigo" Flávio Bolsonaro por su "histórica elección" frente a Lula en Brasil
  > El presidente de Argentina, Javier Milei, ha felicitado al candidato ultraderechista del Partido Liberal (PL) a la Presidencia de Brasil, Flávio Bolsonaro, por su victoria en la primera vuelta de las elecciones presidenciales celebradas este domingo, en las que se ha impuesto con el 47,03% de los vo
- 2026-10-05 06:44 [ANSA Mondo] Brasile, l'ex giudice che condannò Lula eletto governatore
  > Sergio Moro guiderà l'esecutivo del suo stato natale, il Paranà
- 2026-10-05 07:14 [BBC Mundo] Elecciones en Brasil: Flávio Bolsonaro y Lula da Silva van a una segunda vuelta en la que el presidente enfrenta una difícil remontada
  > La mayor democracia de América Latina irá a balotaje el 25 de octubre. Lula lleva la desventaja frente a Bolsonaro, ya que históricamente nunca hubo una remontada en una segunda vuelta electoral en Brasil.
- 2026-10-05 07:46 [ANSA Mondo] In Brasile un 30enne di destra è il deputato più votato della storia
  > Nikolas Ferreira ha raccolto oltre 3,1 milioni di preferenze per la Camera
- 2026-10-05 10:46 [ANSA Mondo] Astensione record in Brasile, il 21,08% non ha votato al primo turno
  > Si tratta del livello più alto registrato dalle elezioni del 1998 (21,5%)
- 2026-10-05 11:42 [France 24 Español] Brasil irá a segunda vuelta: Flávio Bolsonaro lidera la primera ronda
  > Brasil se encamina a una segunda vuelta presidencial tras una elección marcada por la polarización. El senador Flávio Bolsonaro obtuvo el primer lugar en la primera vuelta, pero sin alcanzar la mayoría necesaria para evitar el balotaje. El próximo 25 de octubre se enfrentará al actual presidente, Lu
- 2026-10-05 12:20 [Rai News Esteri] Il primo turno delle presidenziali in Brasile, avanti Bolsonaro: ribaltati i pronostici pro-Lula
  > La sfida per il secondo turno del 25 ottobre è ancora aperta ma il presidente uscente non minimizza il peso di una pesante bocciatura delle sue politiche
- 2026-10-05 12:21 [Rai News Esteri] Presidenziali in Brasile, Flavio Bolsonaro a sorpresa supera Lula di 2 punti. Si va al ballottaggio
  > Il candidato di destra al 47%: "Il Brasile vuole cambiare". Il presidente uscente al 45%: "Sono bravo ai supplementari". Scelta rinviata al secondo turno del 25 ottobre
- 2026-10-05 12:29 [Clarín Mundo] Elecciones en Brasil 2026, EN VIVO: reacciones tras la victoria de Flávio Bolsonaro sobre Lula y últimas noticias del balotaje
  > Bolsonaro se impuso en la primera vuelta al superar por casi dos puntos al actual presidente Lula da Silva. El balotaje entre ambos se hará el 25 de octubre. Todas las repercusiones, minuto a minuto.
- 2026-10-05 12:31 [Clarín Mundo] Quién es Flávio Bolsonaro, el hijo de Jair que sorprendió a Lula y va por la presidencia de Brasil
  > Nacido en el estado de Río de Janeiro, Flávio es el mayor de los cinco hijos del expresidente y el que más se le parece físicamente.Este senador, de 45 años, enfrentará a Lula en el balotaje el próximo 25 de octubre.
- 2026-10-05 13:05 [France 24 Español] Informe desde Río de Janeiro: el Partido Liberal de Bolsonaro se fortalece en el Senado
  > Las elecciones legislativas en Brasil dejaron un resultado clave para el futuro político del país: el Partido Liberal (PL), formación vinculada al expresidente Jair Bolsonaro y que postuló a Flávio Bolsonaro para la Presidencia, amplió significativamente su presencia en el Senado. La bancada pasará 
- 2026-10-05 13:16 [Clarín Mundo] Elecciones en Brasil: los mercados celebran la ventaja de Flávio Bolsonaro sobre Lula y el principal índice de la Bolsa marca un nuevo récord
  > Los activos brasileños se dispararon este lunes y el real se apreció en la primera sesión de los mercados tras los comicios del domingo. El índice Ibovespa superó la marca de los 209.000 puntos por primera vez.
- 2026-10-05 13:57 [BBC Mundo] Quiénes son Lucas Pavanato y Nikolas Ferreira, los jóvenes influencers de derecha que lograron las mayores votaciones en la historia de la Cámara de Diputados de Brasil
  > Los flamantes legisladores comparten una agenda conservadora que incluye el rechazo a las políticas de género, el endurecimiento de las sanciones penales y la legalización del porte de armas como herramienta para combatir la delincuencia.
- 2026-10-05 14:50 [Clarín Mundo] Elecciones en Brasil: los resultados del domingo cambian por completo el diseño del país y ya asoma una amnistía para Jair Bolsonaro
  > La victoria del candidato conservador Flávio Bolsonaro sobre el presidente Lula da Silva en primera vuelta excede lo que pueda ocurrir en el balotaje.La ola de derecha se consolida con victorias en las gobernaciones y especialmente en el Parlamento.Aun si el líder petista lograra imponerse el 25 de 
- 2026-10-05 15:47 [Clarín Mundo] La reacción de los medios en Brasil tras la victoria de Bolsonaro: desde "el ciclo de Lula está terminado" hasta "el tsunami de lo peor de la derecha"
  > Los títulos, opiniones y análisis de la prensa en Brasil tras la primera vuelta de las presidenciales de este domingo.
- 2026-10-05 15:59 [France 24 Español] Flávio Bolsonaro y Lula da Silva se preparan para el balotaje en Brasil
  > 🇧🇷🗳️ Luiz Inácio Lula da Silva y Flávio Bolsonaro ofrecieron declaraciones después de que los resultados de los comicios presidenciales de Brasil confirmaran que deberán disputar el balotaje del 25 de octubre.
- 2026-10-05 16:02 [El País Internacional] El lulismo cruje ante la ofensiva ultra
  > Carteles del presidente Trump y del candidato Flavio Bolsonaro, en São Paulo, Brasil, este Lunes.
- 2026-10-05 16:10 [France 24 Español] "Solo faltan días para el rescate Brasil": Bolsonaro celebra la victoria sobre Lula
  > El senador del Partido Liberal (PL) y candidato presidencial, Flávio Bolsonaro, agradeció este lunes "a Dios" y al pueblo brasileño por su victoria en las elecciones del domingo ante el presidente Luiz Inácio Lula da Silva, en contra de los pronósticos. Además, celebró que el PL resultara el partido
- 2026-10-05 16:23 [Clarín Mundo] Elecciones en Brasil: a contrarreloj, Lula y el PT analizan cambios totales en la estrategia de campaña
  > Lo anticipan fuentes partidarias, pero no es claro en qué consistirán. Trascendió que ha habido tensiones internas sobre el manejo de la campaña.Y que debido a eso se perdieron oportunidades importantes para reducir el impulso del candidato opositor, Flávio Bolsonaro.
- 2026-10-05 16:36 [France 24 Español] Paraguay, refugio fiscal y político para la extrema derecha brasileña
  > En los últimos cinco años, las solicitudes de permisos de residencia de brasileños en Paraguay se han más que duplicado. Muchos de los recién llegados son simpatizantes de Jair Bolsonaro que temen una reelección del actual presidente, Luiz Inácio Lula da Silva, a quien responsabilizan de un deterior
- 2026-10-05 17:02 [ANSA Mondo] Brasile, Erika Hilton è la donna più votata della storia alla Camera
  > La politica brasiliana Erika

Hilton ha stabilito un nuovo record nella storia della Camera

dei deputati brasiliana, diventando la donna più votata di

sempre. La deputata trans del Partito socialismo e libertà

(Psol) di San Paolo è stata rieletta con 1.596.472 voti, pari al

5,9% dei voti espress
- 2026-10-05 17:30 [Clarín Mundo] El fantasma de Bolsonaro reaparece en Europa: los temores de Bruselas ante un eventual cambio de gobierno en Brasil
  > • Un cambio de gobierno en Brasil aportaría argumentos a los eurodiputados que buscan frenar la ratificación del entendimiento comercial.
• Si entre 50 y 80 legisladores modifican su postura en la votación prevista para los próximos meses, la aplicación provisional del pacto quedará suspendida.
- 2026-10-05 18:04 [France 24 Español] El mercado de valores de Brasil aplaude la ventaja de Bolsonaro en primera vuelta presidencial
  > El índice bursátil iBovespa, el más importante de la bolsa de São Paulo inició la jornada con un alza estrepitosa de casi el 9% y alcanzó máximo histórico, mientras el real brasileño gana 4,5% frente al dólar a media jornada, hasta situarse ligeramente por encima de los 5 reales por dólar. El buen r
- 2026-10-05 18:10 [France 24 Español] La dinastía Bolsonaro se fortalece: prensa brasileña sobre la primera vuelta electoral
  > La familia Bolsonaro no solo ganó la primera vuelta en Brasil, fortaleció su presencia en ambas cámaras del Congreso y conserva los respaldos de más de 10 gobernadores. 'O Globo' habla del bloque familiar que se ha hecho con varios cargos. Hermanos, hijos, esposa y exesposa tienen un puesto de elecc
- 2026-10-05 19:41 [El País Internacional] La ola conservadora de América Latina llega a Brasil
  > Flávio Bolsonaro (i) junto al presidente de EE.UU., Donald Trump, en el despacho oval de la Casa Blanca en Washington, el 26 de mayo de 2026.
- 2026-10-05 19:42 [El País Internacional] La victoria en primera vuelta de Bolsonaro impulsa a la ola ultra de América Latina
  > Transeúntes pasan ante pósteres dañados que muestran a Bolsonaro hijo con el presidente Trump, este lunes en São Paulo.
- 2026-10-05 19:47 [Clarín Mundo] Elecciones en Brasil: las urnas de la sorpresa
  > Tras el imprevisto triunfo de Flávio Bolsonaro sobre Lula en la primera vuelta, Brasil se encamina hacia un balotaje decisivo el próximo 25 de octubre. La contienda electoral ratifica la profunda polarización política del país y la consolidación del bolsonarismo como una fuerza de derecha permanente
- 2026-10-05 20:21 [ANSA Mondo] Trump, il risultato di Bolsonaro in Brasile una 'grande vittoria'
  > Il risultato di Flavio Bolsonaro

alle elezioni in Brasile è stata una "grande vittoria". Lo ha

detto Donald Trump.Quella di Bolsonaro "è una grande vittoria: combattuta, ma una

vittoria davvero enorme. Incredibile", ha detto Trump. Bolsonaro

si avvia al ballottaggio del 25 ottobre come favorito.
- 2026-10-05 22:09 [ANSA Mondo] Brasile, l'ex presidente Temer sostiene Bolsonaro al ballottaggio
  > L'ex presidente brasiliano

Michel Temer (2016-2018) ha dichiarato il suo sostegno a Flávio

Bolsonaro in vista del ballottaggio del 25 ottobre contro Luiz

Inácio Lula da Silva. In un video diffuso sui social, Temer ha

affermato che il risultato del primo turno mostra la volontà

degli elettori di
**B** (2 item(s))
- 2026-10-05 13:05 [France 24] Trump heads to Nebraska as Republicans fear strongholds could flip
  > US President ​Donald Trump will visit Nebraska on Monday to rally Republicans and promote his economic ​record, taking his message of new investment and manufacturing to a state where farmers and truckers face sharply higher diesel prices and voters worry about inflation. His stop in ​the ‌city of G
- 2026-10-05 17:02 [White House] President Trump and Republicans Are Delivering Real Results for Nebraska
  > News				
			
			
					
	
		
		
			Search
					
						
		
			
				
					Select Category				
				
																		
								All News							
																								
								Briefings &amp; Statements							
																								
																	
										All Presidential Actions									
							

## U154
**A** (12 item(s))
- 2026-10-04 12:48 [Al Jazeera] Yemen’s leader announces military operation to retake Houthi-held territory
  > Rashad al-Alimi says the campaign aims to restore state authority throughout Yemen.
- 2026-10-04 16:51 [BBC World] Yemen's government announces all-out war to reclaim land from Houthis
  > The Yemeni president's announcement comes amid an exchange of strikes between the Houthis and the Saudi-led coalition.
- 2026-10-04 19:50 [Defense News] Yemeni government launches offensive to seize all areas from Iran-backed Houthis
  > Yemen’s Saudi-backed, internationally recognized government said on Sunday it was launching a major military campaign to recapture all areas of the country controlled by the Iran-backed Houthis.The government’s armed forces would press the offensive “until the country is liberated from the grip of t
- 2026-10-05 00:00 [Al Jazeera] Iran war live: Yemen fighting intensifies; Tehran says ready for US attacks
  > Yemeni government announces major offensive against Houthis, as Iran says it is ready to defend itself if US attacks.
- 2026-10-05 03:11 [Al Jazeera] Yemen gov’t forces commence major combat operation against Houthis
  > Yemeni government forces have declared a ‘battle for liberation’ to retake remaining territory held by the Houthis.
- 2026-10-05 09:37 [France 24] Yemen's government declares major operation against Houthis
  > The Yemeni military announced a broad set of strikes against Houthi targets on Monday, after the government declared a new campaign to retake all territory even as the Iran-backed group made fresh gains on the ground. France 24's Kethevane Gorjestani takes a look at the reasons behind this latest es
- 2026-10-05 09:40 [Al Jazeera] Yemen forces claim to seize Dhubab, sites near Bab al-Mandeb from Houthis
  > Yemeni forces claim to seize key positions near waterway as Pakistani, Saudi and Turkish officials to meet.
- 2026-10-05 13:23 [South China Morning Post] Yemeni government forces seize control of Bab el-Mandeb Strait, minister says
  > Saudi-backed Yemeni government forces have secured effective control of the Bab el-Mandeb Strait, Yemen’s Information Minister Moammar al-Eryani has said, though fighting continues with Houthi forces in the area.
The government forces advanced rapidly along the coast with heavy Saudi air support to 
- 2026-10-05 14:37 [BBC World] Yemeni government forces say they have 'secured' Bab al-Mandab Strait
  > Saudi-backed forces gave conflicting reports of whether they had also seized the port city of Mokha, near the Bab al-Mandab Strait.
- 2026-10-05 14:59 [France 24] Yemen government forces announce offensive on Houthi-held territory
  > The internationally recognised Yemeni government announced on Sunday the launch of an offensive ‌to recapture territory held by Houthi rebels, with President Rashad al-Alimi swearing to fight "until the country is liberated from the grip of the terrorist militia".
- 2026-10-05 15:29 [Al Jazeera] Yemeni gov’t forces aim for Sanaa, but Houthi defeat will be a challenge
  > Yemeni government forces claim strategic advances near Bab al-Mandeb strait amid a major anti-Houthi offensive.
- 2026-10-05 19:17 [France 24] Saudi-backed Yemeni forces expel the Houthis from several areas around key strait, officials say
  > Saudi-backed Yemeni government forces staged a lightning advance on ​Monday to retake the coast around the Bab el-Mandeb Strait up to the city of Mocha, the government said, pushing the Iran-backed Houthis out of most of the areas they seized last month. FRANCE 24's Monte Francis reports.
**B** (5 item(s))
- 2026-10-04 15:16 [Al Jazeera] Dodik urges Serb turnout against ‘Sarajevo crooks’ in Bosnia election
  > Dodik urges Serb turnout against ‘Sarajevo crooks’ in Bosnia election
- 2026-10-04 20:36 [South China Morning Post] Serb separatist Dodik declares victory in Bosnia vote as ethnic tensions, EU hopes collide
  > Bosnian Serb nationalist politician Milorad Dodik has declared victory for his party in an election in Bosnia and Herzegovina on Sunday that was shaped by economic pressures, the prospect of the Balkan nation joining the European Union and ethnic tensions that have divided the country since its brut
- 2026-10-05 03:36 [Al Jazeera] Bosnian Serb nationalist claims party victory in Bosnia elections
  > Bosnian Serb nationalist Milorad Dodik claimed victory for his party in Bosnia’s elections.
- 2026-10-05 07:33 [Kyiv Independent] Pro-Russian Dodik claims party victory in Bosnian elections
  > "If it had not been for (U.S. President) Donald Trump's magnificent victory, we would probably be political corpses today," Milorad Dodik told his supporters, while also thanking Russian President Vladimir Putin.
- 2026-10-05 10:23 [DW World] Bosnia election: New technology might have stopped votes being cast on behalf of dead voters, but the result remains unchanged
  > New technology has stopped votes being cast on behalf of dead or absent voters, and turnout has fallen to a record low. But it was a case of deja vu in Bosnia's elections with the same parties winning.

## U155
**A** (5 item(s))
- 2026-09-29 12:00 [South China Morning Post] US and China need shared risk vocabulary to manage AI threats: Beijing-linked think tank
  > Beijing and Washington should first develop a common language around AI risks rather than seek to resolve their broader technology rivalry, a leading Chinese think tank has advised.
The call from the China Institutes of Contemporary International Relations (CICIR), affiliated with the Ministry of St
- 2026-09-29 16:09 [BBC World] Trump rules out joint US-China venture to develop AI
  > The US president continues to push back on calls to establish guardrails around artificial intelligence, arguing it will stifle growth.
- 2026-09-29 19:32 [South China Morning Post] Trump rejects calls to work with China on AI safety despite Xi summit progress
  > US President Donald Trump said on Tuesday he does not want to work with China on addressing artificial intelligence (AI) risks, arguing that cooperation could undermine America’s lead in the fast-moving technology.
“Whoever wins superintelligence wins. You’re gonna have a winner and a loser, and you
- 2026-09-29 23:43 [Al Jazeera] Trump, tech bosses sign voluntary pact pledging ‘robust’ AI safeguards
  > US President Trump touts self-regulation amid the international community&#039;s and industry&#039;s calls for formal rules.
- 2026-09-30 05:00 [South China Morning Post] Chinese firms trail global peers on profits, but AI power boom offers bright spot: Natixis
  > China’s corporate sector remains considerably weaker than it was before the Covid-19 pandemic, but the country is emerging as a key beneficiary of the global artificial intelligence boom thanks to its ample power capacity, according to a Natixis survey of thousands of firms and a separate research r
**B** (2 item(s))
- 2026-09-29 20:25 [BBC World] Former American Idol contestant and pastor found guilty of murdering wife
  > Caleb Flynn shot his wife, Ashley, dead in their Ohio home in February before saying in a 9/11 call she was killed by burglars.
- 2026-09-30 10:35 [Al Jazeera] Former American Idol contestant found guilty of murdering wife
  > Former American Idol contestant found guilty of murdering wife

