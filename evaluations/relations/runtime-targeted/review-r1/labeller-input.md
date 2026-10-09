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

## P101
**A** (7 item(s))
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
**B** (3 item(s))
- 2026-10-07 23:08 [BBC Mundo] Por qué la mayor colonia de pingüinos del mundo ha perdido dos tercios de su población
  > Se atribuye al cambio climático el drástico declive de los pingüinos barbijo que habitan en una remota isla volcánica.
- 2026-10-08 02:44 [France 24 Español] Ecuador: jueza declara inocentes a 32 pescadores de lanchas atacadas por EE. UU. en el Pacífico
  > Una jueza declaró inocentes a 32 pescadores tripulantes de dos de las lanchas atacadas por Estados Unidos en el océano Pacífico, que habían sido procesados previamente por la Fiscalía por presunta asociación ilícita con grupos delincuenciales. Nuestra corresponsal Carolina Mella nos amplió la inform
- 2026-10-08 19:31 [Clarín Mundo] "El estrecho de Magallanes fue, es y será siempre chileno": la dura respuesta del canciller tras los dichos del embajador de Estados Unidos
  > Francisco Pérez Mackenna rechazó los dichos de Brandon Judd y remarcó que Chile cuenta con capacidad propia para resguardar el Estrecho de Magallanes. La controversia diplomática por la vía marítima se suma a la nota de protesta presentada semanas atrás contra la Argentina por una afirmación similar

## P102
**A** (2 item(s))
- 2026-10-03 12:22 [BBC Mundo] Lo que la fallida ejecución de Christa Pike revela sobre la pena de muerte en EE.UU.
  > Christa Pike, una mujer condenada a muerte en Tennessee, sobrevivió a la aplicación de dos inyecciones letales. Su caso ha vuelto a centrar la atención en la pena de muerte y en cómo se aplica en Estados Unidos.
- 2026-10-03 19:14 [Il Sole 24 Ore Mondo] Trump vuole estendere la pena di morte ai narcotrafficanti: il caso Pike riapre lo scontro
  > Il presidente promette di ampliare i reati punibili con la pena capitale. Il Tennessee sospende le esecuzioni dopo il caso Pike, mentre una sentenza della Corte Suprema del 2008 lascia aperto il nodo dei grandi narcotrafficanti
**B** (7 item(s))
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

## P103
**A** (2 item(s))
- 2026-10-08 11:18 [BBC Mundo] Cómo llegó Colombia a tener una deuda tan alta (y por qué De la Espriella tendrá que aumentarla)
  > El presupuesto presentado por el gobierno de De la Espriella prevee que la deuda llegará a 66,2% del PIB en 2027, la más alta de la historia del país.
- 2026-10-08 18:55 [France 24 Español] Directo Latam y el apoyo de De la Espriella a exmilitares acusados por asesinato de Jovenel Moïse
  > El presidente colombiano, Abelardo de la Espriella, ha manifestado su apoyo jurídico a 17 exmilitares acusados del magnicidio de Jovenel Moïse en 2021, quienes fueron trasladados a Estados Unidos para comparecer ante la Justicia. En paralelo, el mandatario busca implementar su Estatuto Antiterrorist
**B** (2 item(s))
- 2026-10-08 13:14 [Europa Press Internacional] Reino Unido y Alemania lanzan un plan conjunto para contrarrestar actos de sabotaje y ciberataques
  > El primer ministro de Reino Unido, Andy Burnham ha anunciado este jueves durante un encuentro con el canciller alemán, Friedrich Merz, el lanzamiento de un plan conjunto para hacer frente a acciones de sabotaje y ciberataques a medida que ambos países cooperan para impulsar a nivel sus industrias te
- 2026-10-08 15:54 [France 24 Español] Burnham y Merz firman un acuerdo de cooperación en seguridad en medio de la amenaza rusa
  > El primer ministro de Reino Unido, Andy Burnham, abre la puerta a Alemania para que se una al programa GCAP, para la construcción de un avión de combate de sexta generación en colaboración con Italia y Japón. El canciller alemán, Friedrich Merz, celebra la ratificación del Tratado de Kensington, mie

## P104
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
**B** (2 item(s))
- 2026-10-08 13:14 [Europa Press Internacional] Reino Unido y Alemania lanzan un plan conjunto para contrarrestar actos de sabotaje y ciberataques
  > El primer ministro de Reino Unido, Andy Burnham ha anunciado este jueves durante un encuentro con el canciller alemán, Friedrich Merz, el lanzamiento de un plan conjunto para hacer frente a acciones de sabotaje y ciberataques a medida que ambos países cooperan para impulsar a nivel sus industrias te
- 2026-10-08 15:54 [France 24 Español] Burnham y Merz firman un acuerdo de cooperación en seguridad en medio de la amenaza rusa
  > El primer ministro de Reino Unido, Andy Burnham, abre la puerta a Alemania para que se una al programa GCAP, para la construcción de un avión de combate de sexta generación en colaboración con Italia y Japón. El canciller alemán, Friedrich Merz, celebra la ratificación del Tratado de Kensington, mie

## P105
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
- 2026-10-07 23:08 [BBC Mundo] Por qué la mayor colonia de pingüinos del mundo ha perdido dos tercios de su población
  > Se atribuye al cambio climático el drástico declive de los pingüinos barbijo que habitan en una remota isla volcánica.
- 2026-10-08 02:44 [France 24 Español] Ecuador: jueza declara inocentes a 32 pescadores de lanchas atacadas por EE. UU. en el Pacífico
  > Una jueza declaró inocentes a 32 pescadores tripulantes de dos de las lanchas atacadas por Estados Unidos en el océano Pacífico, que habían sido procesados previamente por la Fiscalía por presunta asociación ilícita con grupos delincuenciales. Nuestra corresponsal Carolina Mella nos amplió la inform
- 2026-10-08 19:31 [Clarín Mundo] "El estrecho de Magallanes fue, es y será siempre chileno": la dura respuesta del canciller tras los dichos del embajador de Estados Unidos
  > Francisco Pérez Mackenna rechazó los dichos de Brandon Judd y remarcó que Chile cuenta con capacidad propia para resguardar el Estrecho de Magallanes. La controversia diplomática por la vía marítima se suma a la nota de protesta presentada semanas atrás contra la Argentina por una afirmación similar

## P106
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
**B** (3 item(s))
- 2026-10-07 23:08 [BBC Mundo] Por qué la mayor colonia de pingüinos del mundo ha perdido dos tercios de su población
  > Se atribuye al cambio climático el drástico declive de los pingüinos barbijo que habitan en una remota isla volcánica.
- 2026-10-08 02:44 [France 24 Español] Ecuador: jueza declara inocentes a 32 pescadores de lanchas atacadas por EE. UU. en el Pacífico
  > Una jueza declaró inocentes a 32 pescadores tripulantes de dos de las lanchas atacadas por Estados Unidos en el océano Pacífico, que habían sido procesados previamente por la Fiscalía por presunta asociación ilícita con grupos delincuenciales. Nuestra corresponsal Carolina Mella nos amplió la inform
- 2026-10-08 19:31 [Clarín Mundo] "El estrecho de Magallanes fue, es y será siempre chileno": la dura respuesta del canciller tras los dichos del embajador de Estados Unidos
  > Francisco Pérez Mackenna rechazó los dichos de Brandon Judd y remarcó que Chile cuenta con capacidad propia para resguardar el Estrecho de Magallanes. La controversia diplomática por la vía marítima se suma a la nota de protesta presentada semanas atrás contra la Argentina por una afirmación similar

## P107
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
**B** (6 item(s))
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

## P108
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
**B** (3 item(s))
- 2026-10-04 12:33 [Rai News Esteri] Spagna, il Psoe in pressing su Sanchez per il voto anticipato. La destra soffia sulle piazze
  > Oltre mezzo milione di persone sfilano a Madrid, a Valencia la tensione sfocia in cariche e 5 arresti di fronte a un summit immobiliare. Il Congresso ha bocciato i decreti salva-affitti coi voti di centrodestra e indipendentisti catalani
- 2026-10-05 07:29 [ANSA Mondo] Sanchez, 'ho deciso di convocare le elezioni il 29 novembre'
  > Il premier in una dichiarazione istituzionale
- 2026-10-05 12:08 [Rai News Esteri] Sanchez porta la Spagna al voto il 29 novembre sull'onda delle proteste per la crisi abitativa
  > Il capo del governo di Madrid, pressato da giorni da richieste di elezioni anticipate, punta a capitalizzare un consenso "last minute" con i provvedimenti per la casa, una crisi che ha portato a proteste in tutto il Paese

## P109
**A** (7 item(s))
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

## P110
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

## P111
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

## P112
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
**B** (11 item(s))
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

## P113
**A** (2 item(s))
- 2026-10-03 12:22 [BBC Mundo] Lo que la fallida ejecución de Christa Pike revela sobre la pena de muerte en EE.UU.
  > Christa Pike, una mujer condenada a muerte en Tennessee, sobrevivió a la aplicación de dos inyecciones letales. Su caso ha vuelto a centrar la atención en la pena de muerte y en cómo se aplica en Estados Unidos.
- 2026-10-03 19:14 [Il Sole 24 Ore Mondo] Trump vuole estendere la pena di morte ai narcotrafficanti: il caso Pike riapre lo scontro
  > Il presidente promette di ampliare i reati punibili con la pena capitale. Il Tennessee sospende le esecuzioni dopo il caso Pike, mentre una sentenza della Corte Suprema del 2008 lascia aperto il nodo dei grandi narcotrafficanti
**B** (11 item(s))
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

## P114
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

## P115
**A** (9 item(s))
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
**B** (2 item(s))
- 2026-10-08 13:14 [Europa Press Internacional] Reino Unido y Alemania lanzan un plan conjunto para contrarrestar actos de sabotaje y ciberataques
  > El primer ministro de Reino Unido, Andy Burnham ha anunciado este jueves durante un encuentro con el canciller alemán, Friedrich Merz, el lanzamiento de un plan conjunto para hacer frente a acciones de sabotaje y ciberataques a medida que ambos países cooperan para impulsar a nivel sus industrias te
- 2026-10-08 15:54 [France 24 Español] Burnham y Merz firman un acuerdo de cooperación en seguridad en medio de la amenaza rusa
  > El primer ministro de Reino Unido, Andy Burnham, abre la puerta a Alemania para que se una al programa GCAP, para la construcción de un avión de combate de sexta generación en colaboración con Italia y Japón. El canciller alemán, Friedrich Merz, celebra la ratificación del Tratado de Kensington, mie

## P116
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
**B** (11 item(s))
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

## P117
**A** (3 item(s))
- 2026-10-07 23:23 [Clarín Mundo] “El sufrimiento no comenzó ni terminó ese día”: el polémico mensaje del alcalde de Nueva York, Zohran Mamdani, a tres años de la masacre del 7-O
  > El funcionario se solidarizó por los "horrendos crímenes de guerra del 7 de octubre" y acusó al gobierno israelí de perpetrar un "devastador genocidio" en Gaza.La semana pasada había anunciado un plan para combatir el antisemitismo en la ciudad.
- 2026-10-08 01:32 [France 24 Español] Gaza: el panorama en el enclave tres años después de los ataques de Hamas del 7-O
  > Tres años después del ataque de Hamás contra Israel y la posterior respuesta israelí contra la Franja de Gaza, el enclave palestino está prácticamente irreconocible. El 80% de la infraestructura fue destruida o afectada por los ataques, el acceso al  agua potable es muy limitado y la mayoría de civi
- 2026-10-08 10:27 [El País Internacional] Mamdani es abucheado por manifestantes propalestinos por acudir a un acto de recuerdo de las víctimas del 7 de octubre
  > El alcalde de Nueva York, Zohran Mamdani, acude a la vigilia por el tercer aniversario de los ataques de Hamás en Israel, en Nueva York, el 7 de octubre de 2026.
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

## P118
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
**B** (11 item(s))
- 2026-10-08 03:28 [France 24] Live: French high school, university students call for fresh protests as funding demands grow
  > French high school and university students were called out to protest again on Thursday, two days after a large turnout demanding more funding, as the government made a series of conciliatory gestures aimed at ending the crisis. Follow our liveblog for all the latest developments.
- 2026-10-08 03:38 [BBC World] France's school protests: What lies behind the anger
  > Students' blockades and marches spring from real grievances â and from France's habit of settling policy on the street.
- 2026-10-08 06:27 [France 24] French students prepare for more marches as hundreds of schools close
  > FRANCE 24's Jamie Smith-Maillet reports from a high school in Paris as students across France prepare for more marches on Thursday.
- 2026-10-08 10:45 [South China Morning Post] French school blockades continue despite PM’s pledge to act
  > French teenagers blockaded some high schools and marched through cities on Thursday after the government promised to address their grievances about teacher shortages and dilapidated school buildings but gave no specific details.
The protest movement, now into its third week, has exposed deep tension
- 2026-10-08 11:03 [Al Jazeera] School protests, blockades resume in France despite PM’s promise to act
  > Dozens of people have been injured in the protests, including students, teachers, and police officers.
- 2026-10-08 12:48 [France 24] French teens keep up school blockades despite prime minister's pledge to act
  > French teenagers blockaded some high schools and marched through cities on Thursday after the government promised to address their grievances about teacher shortages and dilapidated school buildings. Reporting from Paris, France 24's Jamie Smith-Maillet says protesters he has spoken to see the gover
- 2026-10-08 13:45 [Al Jazeera] French PM vows changes as students keep up school protests
  > French PM Sebastien Lecornu has promised to address student concerns as protests force hundreds of schools to close.
- 2026-10-08 14:01 [Al Jazeera] ‘This is a crisis of hope’: Echoes of 1968 as France’s students rise up
  > As in 1968, when student protests triggered nationwide strikes, today’s crisis is about generational discontent.
- 2026-10-08 15:23 [France 24] Student protesters 'showing no signs of backing down'
  > Students who have been protesting classroom conditions in France for days are "not looking like they are willing to back down", says France 24 reporter Claire Paccalin, despite promises by the French prime minister to bring in measures to address their grievances.
- 2026-10-08 20:17 [France 24] 'Fighting for our future': France high school students vow no let-up
  > Over 70,000 people took part in demonstrations across France on Thursday demanding better education and less police brutality, as students protested nationwide despite government attempts to ease a crisis that has rocked the country for more than a week. Students have blocked entrances to hundreds o
- 2026-10-08 20:22 [France 24] ‘Nothing will stop us’: French student protests show few signs of ending
  > Students on Thursday barricaded a Parisian high school with garbage bins before police shot tear gas at them as France’s nationwide protests showed little sign of ending. At least a dozen demonstrations supporting the high school students’ movement were planned across the country while 375 schools w

## P119
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
**B** (11 item(s))
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

## P120
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

## P121
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

## P122
**A** (3 item(s))
- 2026-10-07 23:23 [Clarín Mundo] “El sufrimiento no comenzó ni terminó ese día”: el polémico mensaje del alcalde de Nueva York, Zohran Mamdani, a tres años de la masacre del 7-O
  > El funcionario se solidarizó por los "horrendos crímenes de guerra del 7 de octubre" y acusó al gobierno israelí de perpetrar un "devastador genocidio" en Gaza.La semana pasada había anunciado un plan para combatir el antisemitismo en la ciudad.
- 2026-10-08 01:32 [France 24 Español] Gaza: el panorama en el enclave tres años después de los ataques de Hamas del 7-O
  > Tres años después del ataque de Hamás contra Israel y la posterior respuesta israelí contra la Franja de Gaza, el enclave palestino está prácticamente irreconocible. El 80% de la infraestructura fue destruida o afectada por los ataques, el acceso al  agua potable es muy limitado y la mayoría de civi
- 2026-10-08 10:27 [El País Internacional] Mamdani es abucheado por manifestantes propalestinos por acudir a un acto de recuerdo de las víctimas del 7 de octubre
  > El alcalde de Nueva York, Zohran Mamdani, acude a la vigilia por el tercer aniversario de los ataques de Hamás en Israel, en Nueva York, el 7 de octubre de 2026.
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

## P123
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
**B** (3 item(s))
- 2026-10-04 12:33 [Rai News Esteri] Spagna, il Psoe in pressing su Sanchez per il voto anticipato. La destra soffia sulle piazze
  > Oltre mezzo milione di persone sfilano a Madrid, a Valencia la tensione sfocia in cariche e 5 arresti di fronte a un summit immobiliare. Il Congresso ha bocciato i decreti salva-affitti coi voti di centrodestra e indipendentisti catalani
- 2026-10-05 07:29 [ANSA Mondo] Sanchez, 'ho deciso di convocare le elezioni il 29 novembre'
  > Il premier in una dichiarazione istituzionale
- 2026-10-05 12:08 [Rai News Esteri] Sanchez porta la Spagna al voto il 29 novembre sull'onda delle proteste per la crisi abitativa
  > Il capo del governo di Madrid, pressato da giorni da richieste di elezioni anticipate, punta a capitalizzare un consenso "last minute" con i provvedimenti per la casa, una crisi che ha portato a proteste in tutto il Paese

## P124
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
**B** (2 item(s))
- 2026-10-08 13:14 [Europa Press Internacional] Reino Unido y Alemania lanzan un plan conjunto para contrarrestar actos de sabotaje y ciberataques
  > El primer ministro de Reino Unido, Andy Burnham ha anunciado este jueves durante un encuentro con el canciller alemán, Friedrich Merz, el lanzamiento de un plan conjunto para hacer frente a acciones de sabotaje y ciberataques a medida que ambos países cooperan para impulsar a nivel sus industrias te
- 2026-10-08 15:54 [France 24 Español] Burnham y Merz firman un acuerdo de cooperación en seguridad en medio de la amenaza rusa
  > El primer ministro de Reino Unido, Andy Burnham, abre la puerta a Alemania para que se una al programa GCAP, para la construcción de un avión de combate de sexta generación en colaboración con Italia y Japón. El canciller alemán, Friedrich Merz, celebra la ratificación del Tratado de Kensington, mie

## P125
**A** (7 item(s))
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
**B** (10 item(s))
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

## P126
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

## P127
**A** (2 item(s))
- 2026-10-03 12:22 [BBC Mundo] Lo que la fallida ejecución de Christa Pike revela sobre la pena de muerte en EE.UU.
  > Christa Pike, una mujer condenada a muerte en Tennessee, sobrevivió a la aplicación de dos inyecciones letales. Su caso ha vuelto a centrar la atención en la pena de muerte y en cómo se aplica en Estados Unidos.
- 2026-10-03 19:14 [Il Sole 24 Ore Mondo] Trump vuole estendere la pena di morte ai narcotrafficanti: il caso Pike riapre lo scontro
  > Il presidente promette di ampliare i reati punibili con la pena capitale. Il Tennessee sospende le esecuzioni dopo il caso Pike, mentre una sentenza della Corte Suprema del 2008 lascia aperto il nodo dei grandi narcotrafficanti
**B** (3 item(s))
- 2026-10-04 12:33 [Rai News Esteri] Spagna, il Psoe in pressing su Sanchez per il voto anticipato. La destra soffia sulle piazze
  > Oltre mezzo milione di persone sfilano a Madrid, a Valencia la tensione sfocia in cariche e 5 arresti di fronte a un summit immobiliare. Il Congresso ha bocciato i decreti salva-affitti coi voti di centrodestra e indipendentisti catalani
- 2026-10-05 07:29 [ANSA Mondo] Sanchez, 'ho deciso di convocare le elezioni il 29 novembre'
  > Il premier in una dichiarazione istituzionale
- 2026-10-05 12:08 [Rai News Esteri] Sanchez porta la Spagna al voto il 29 novembre sull'onda delle proteste per la crisi abitativa
  > Il capo del governo di Madrid, pressato da giorni da richieste di elezioni anticipate, punta a capitalizzare un consenso "last minute" con i provvedimenti per la casa, una crisi che ha portato a proteste in tutto il Paese

## P128
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

## P129
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

## P130
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

## P131
**A** (10 item(s))
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
**B** (3 item(s))
- 2026-10-05 11:51 [France 24 Español] Irán entrena a mujeres en las armas ante una posible invasión terrestre
  > En medio de las tensiones con Estados Unidos e Israel, Irán ha puesto en marcha programas de entrenamiento para civiles, incluidas numerosas mujeres, con el objetivo de prepararlas para responder ante una eventual invasión terrestre. En plazas y centros de entrenamiento de Teherán, las participantes
- 2026-10-05 14:49 [El País Internacional] Irán empieza a entrenar a voluntarios civiles para la “defensa nacional”
  > Voluntarias con rifles de asalto del tipo Kaláshnikov, en un curso de entrenamiento militar para civiles en la plaza Imán Hussein de Teherán, este domingo.
- 2026-10-05 15:47 [Europa Press Internacional] El presidente de Irán nombra a Mehrdad Ajlaqi nuevo ministro de Defensa
  > El presidente de Irán, Masud Pezeshkian, ha nombrado este lunes a Mehrdad Ajlaqi nuevo ministro de Defensa del país, por lo que la elección pasa ahora a manos del Parlamento para ser sometida a votación a medida que avanza el conflicto abierto en la región de Oriente Próximo a raíz de la ofensiva la

## P132
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

