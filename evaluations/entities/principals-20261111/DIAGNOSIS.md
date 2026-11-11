# Principal-actor extraction: diagnosis (2026-11-11, frozen before any code change)

**Track.** Upstream hardening for Situation v2, track 3 (owner, 2026-11-11). Replay only: no live data, no deploy.
**Base code.** `fix/v2-upstream-principals` = `b695aa0` (actor-normalisation prerequisite included).
**Input.** Backup-API copy of `data/eval/geolocation-iter3/snap-20261102.db` (sha256 `b5bb5728…`), 1,198 Developments.
**Method.**
- `diagnose.py` re-derives principals (`development_actors`) for every Development. For each state or organisation
  that a non-round-up headline names but that did not become a principal, it records the stage that lost it.
- `filtered.py` sub-classifies the losses where the role was `actor`.
- Outputs: `diag-base-summary.json` and `filtered-base.json`.
- The headline probe is deliberately broad (any 1–3 word n-gram that maps to a country or configured actor), so most
  hits are legitimate non-principals: places, topics, counterparts.

## Missed keys by stage (1,636 key-misses in the snapshot)

| Stage | Count | Extraction defect? |
|---|---:|---|
| role `location` | 339 | No. Places in which something happens. Gaza (33) is a place standing for a party: a normalisation / role-modelling question (Gaza → Palestine), not extraction |
| role `subject` | 167 | No. Topics ("over Russian oil purchase") |
| role `participant` | 163 | No by design. Counterparts are not principals in the owner gold |
| role `target` | 61 | **No: owner convention.** The gold excludes targets of coercion (D06 Hamas, D08 Ukraine, D11/D12 Russia, D19 Iran/Russia are targets, not principals). "Russia warns NATO" therefore leaves NATO out |
| role `institutional_context` | 44 | No by design. A multilateral body framing an action (UN, NATO, EU) |
| role `affected` | 38 | No by design |
| `no_mention` | 297 | Mostly probe noise: "WHO" read as UN; GDELT boilerplate ("- Dominican Republic"); headlines of other stories in merged Developments. No repeated extraction pattern in the sample |
| `actor_filtered: below_support` | 458 | No by design. The actor appears as actor in one headline of a 3+-item Development, under the selection threshold (`max(1.5, 25% of items)`). Changing the threshold is a product decision, not a defect fix |
| `actor_filtered: headline_gate` | 11 | No by design. No headline names the actor as acting |
| **`actor_filtered: split_support`** | **43 (41 Developments)** | **Yes.** See P-A |
| `actor_filtered: other` | 5 | Too few to act on |

## P-A: actor support counted per surface holder instead of per actor (the one repeated defect)

`principals.py` documents aggregation at the canonical-actor level: "Trump", "US" and "White House" in three
headlines are one actor with three mentions. `development_actors` instead applies the threshold to each **role
holder** (a surface name: `united states`, `trump`, `rubio`, `kremlin`), because `actor_roles.development_roles`
keeps people and seats as separate holders. An actor named under two or more names therefore loses, though together
its names pass. Examples: Russia + Kremlin in "Russia carried out sabotage against Danish defense firms"; United
States + Rubio; Ukraine + Zelensky + Zelenskyy.

- **Extraction or normalisation?** Extraction / selection. The normaliser already maps every holder to the same key
  (`ActorNormalizer.key`); the loss happens when selection ignores that key.
- **Smallest fix:** in `development_actors`, sum "actor" support over the holders that share a canonical key. When
  no holder of a key passes alone but the key does, flag exactly one holder of that key: the one with the most actor
  weight, ties to the holder whose name is the key. The headline gate is applied at key level (some holder of the key
  acts in a headline). Holders that already pass alone are unchanged, so nothing else moves.

## Not fixed (by rule or out of scope)

- Coercion targets, participants, multilateral framing, the selection threshold: owner conventions or product
  choices, not extraction defects.
- Gaza / West Bank as places that stand for Palestine: normalisation (`represents`), out of this track.
- Animal names typed PERSON (pandas, D34), and a G20 forum read as the actor (D1138): single cases, not patterns.

## 30-case sample

| Development | Key | Stage | First headline | Detail |
|---|---|---|---|---|
| D4 | france | split_support | Saudi Arabia allies line up support as Houthi attacks mount | holders france 2.5, emmanuel macron 2; need 3 |
| D76 | united states | split_support | Boeing wins Navy next-gen fighter F/A-XX competition | holders united states 1, us department of defense 1, u.s. navy 1, u.s. air force 1.5; need 1.75 |
| D82 | israel | split_support | FlyDubai flight to Israel diverted to Saudi Arabia after incident in cockpit | holders israel 5, benjamin netanyahu 7.5; need 11.75 |
| D85 | united states | split_support | Tennessee governor declines to halt execution of state's lone woman on death row | holders u.s. supreme court 2, united states 5; need 5.25 |
| D123 | ukraine | split_support | North Korea fires ballistic missile towards the sea, South Korea says | holders ukraine 1, zelensky 0.5, kyiv 0; need 1.5 |
| D123 | russia | split_support | (same Development) | holders russia 0.5, russian aerospace forces 1; need 1.5 |
| D132 | united nations | split_support | Iran tells US: there is "no military solution" to end the war | holders united nations 3.5, un general assembly 1; need 4.25 |
| D175 | united states | split_support | Irán entrena a mujeres en las armas ante una posible invasión terrestre | holders united states 0, trump 1, white house 0.5; need 1.5 |
| D190 | united states | split_support | We stay in Kyiv: Irish diplomats vow to stay in Ukraine despite Russian threat of strikes | holders united states 1, rubio 1; need 1.5 |
| D195 | united states | split_support | Justice Department Moves to Strip Citizenship from 40 Criminals | holders united states 1, trump 1; need 1.5 |
| D210 | united states | split_support | Joint Statement on Countering Iranian Terrorist Activity in the Western Hemisphere | holders united states 1.5, donald trump 3, white house 2, us department of defense 2; need 6.75 |
| D232 | united states | split_support | Qué hay que saber sobre los Premios Nobel de 2026 | holders donald trump 6, united states 3.5, marco rubio 0.5; need 8.75 |
| D1 | asean | below_support | Xi got Trump's red carpet welcome - but not everything he wanted | holders asean 1; need 5.75 |
| D2 | taiwan | below_support | Trump and Xi come face-to-face as US and China battle to win the AI race | holders taiwan 1.5; need 9.75 |
| D2 | asean | below_support | (same Development) | holders asean 1; need 9.75 |
| D4 | turkey | below_support | Saudi Arabia allies line up support as Houthi attacks mount | holders turkiye 1, ankara 0; need 3 |
| D6 | china | headline_gate | Air Force, civilian staff dispute status of China Aerospace Studies Institute | holders china 1; need 1 |
| D179 | france | headline_gate | France, Germany call for new weapon allowing "immediate cut off" of China | holders france 1.5; need 1.5 |
| D310 | united states | headline_gate | European Parliament Installs Gilded Nude Statue Mocking Trump | holders united states 0.5, donald trump 0.5; need 1 |
| D4 | iran | role:target | Saudi Arabia allies line up support as Houthi attacks mount | |
| D35 | netherlands | role:target | Israel revokes Dutch diplomats' status over sanctions on settlements | |
| D48 | qatar | role:target | UAE confirms Netanyahu visit to Abu Dhabi | |
| D59 | united kingdom | role:target | Argentina threatens legal action against UK over Falkland Islands oil exploration | |
| D26 | gaza | role:location | Republic of Ireland news conference delayed before controversial Israel game | |
| D48 | gaza | role:location | UAE confirms Netanyahu visit to Abu Dhabi | |
| D65 | gaza | role:location | Israeli forces kill Hamas commander Izz al-Din al-Beik in Gaza attack | |
| D2 | united nations | role:institutional_context | Trump and Xi come face-to-face as US and China battle to win the AI race | |
| D4 | united nations | role:institutional_context | Saudi Arabia allies line up support as Houthi attacks mount | |
| D9 | northern ethiopia | no_mention | Ethiopia's army says it has repelled attacks in first comment on fresh fighting | |
| D26 | ireland | no_mention | Republic of Ireland news conference delayed before controversial Israel game | |

Several sampled Developments are merged (the first headline is a different story from the rest). That is a
segmentation defect, outside this track.

## Gate for the P-A fix (frozen here)

1. Entity benchmark (gold rev 3): no metric drops against `b695aa0`.
2. Identity gold check passes.
3. Phase 2 identity (development windows only): no regression from 43/65, 43/58, 22/100, 15/58, 16/19, 12/31.
4. `replay_actors.py` diff against `b695aa0`: the share of Developments with principals may rise. Every changed
   Development must be a `split_support` Development in `filtered-base.json`; any other change is reported as
   unexplained.
5. Full pytest passes.
