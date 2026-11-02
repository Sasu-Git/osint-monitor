# Actor-hygiene fix: gate results (2026-10-16)

The fix is on `fix/actor-hygiene`, measured against `production-stable-20261016` (`3eda6d0`). The expectations and
the gate were frozen before any code changed (`README.md`, `FREEZE.md`). No live data was touched. The replays run
on backup-API copies of `data/eval/actor-defects-20261016.snapshot.db`.

## What changed

1. **Headline and body as separate sentences** (`nlp.ner_text`, used by the pipeline). Joined by a bare space, a
   headline's last words and the body's first words parsed as one name: "Elon Musk jab Musk", "Musk Anduril",
   "Ukraine Elon Musk" (D1c).
2. **A bare surname stands for the full name its own item gives** (`nlp._link_surnames`, resolved by
   `EntityResolver` through `ExtractedEntity.refers_to`; never stored as an alias). This happens only when exactly
   one person in the item has that surname: "Bolsonaro" next to both Jair and Flávio Bolsonaro stays unlinked. There
   is no linking across items and no global surname alias (D1b).
3. **One actor, one identity among a Development's principals** (`principals.mark_principal_actors`).
   - When several linked entities match one principal holder and they normalise to different actors ("Elon Musk's"
     and a PRODUCT "Musk"), only the entity of the best match's actor is flagged principal.
   - Entities that normalise alike ("Trump" for the United States, "EE.UU.") all stay, as before.
4. **Named storms are storm events** (`nlp.storm_names`). This covers English, Spanish and Italian storm words, a
   name right after one (quotes allowed), names listed with it, a plural storm word with a coordinated pair of bare
   names, and the same name standing alone elsewhere in the item.
   - Only PERSON and LOC mentions are retyped; products such as "Storm Shadow" are untouched.
   - Storm names are rejected as actor candidates (`principals.rejection`, `weather_system`) (D2).
5. **`scripts/repair_entity_names.py`**: renames stale canonical names ("Elon Musk's" to "Elon Musk") only when no
   other entity has the clean name. Collisions are reported, never merged. It is dry-run by default and is **not
   run** on live data (D1a).
   - Resolution never depended on it: "Elon Musk" already resolved to entity 1238 by a fuzzy match.
   - A resolver step that matched surface variants of canonical names was tried and removed. The entity benchmark
     showed it regressing: "Tehran" resolved to a polluted "Tehran&#039;s".

## Gate

| Gate | Result |
|---|---|
| Entity benchmark (gold rev 3) | **no unit changed** against the run of `3eda6d0` |
| Identity gold check | passed (checks 1-6) |
| Phase 2 identity (development windows) | 43/65, 43/58, 22/100, 15/58, 16/19, 12/31: **identical** to the 2026-10-13 candidate gate |
| pytest | 714 passed, 3 xfailed (22 new in `tests/test_actor_hygiene.py`) |
| smoke | passed |
| D1 (`gate_replay.py` on the snapshot) | no glued span. "Musk" resolves to the Elon Musk person in items naming him. Development 320's principals: `Elon Musk's` only (was plus PRODUCT `Musk`) |
| D2 | no PERSON Simon / Simón / Rachel in any defect item. Storm events instead (`Hurricane Simon`, `Hurricane Rachel`, `Storm Rachel`, `Cyclone Rachel`). Development 402 has no principals (was `Rachel`, `Simon`) |
| Situation regression | 99 Developments re-derived. 15 change principals. Exactly 4 Situations lose actor support, all actor-identity defects (below). Every other Situation's support is unchanged. The three retired Situations stay retired (no Development carries them) |
| No new actor merges | none. Every change drops a duplicate or polluted entity of an actor that stays, or a storm |

Situations that lose support (all four rest on one actor counted twice, or on storms):

| Situation | Developments carrying its actors | Why |
|---|---|---|
| `elon-musk-musk` | 1/2 -> 0/2 | D1 |
| `rachel-simon` | 1/2 -> 0/2 | D2 |
| `christa-pike-pike` | 2/2 -> 0/2 | same class as D1: a person and her own surname (`Christa Pike's`, `Pike`) |
| `donald-j-trump-united-states` | 3/3 -> 0/3 | `DONALD J. TRUMP` and `Trump`: one person, who represents the United States |

The other principal changes drop polluted or duplicate entities of an actor that stays:
- `Ukraine&#039;s`, `Ethiopia&#039;s`;
- `Ukraine Russia`, `Tigray Eritrea`, `Southwest Syria`;
- `Zacharia` next to `Katie Zacharia`.

One borderline case: Development 400 (in `gaza-ceasefire`) keeps `Ejército de Israel` and drops `Israel`. `Israel` was
principal there only through the surname rule ("israel" is the last word of "ejército de israel"). The Situation's
support is unchanged (3/7).

## Not done here

- **No live repair.** Applying this code does not change existing Situations. `christa-pike-pike` and
  `donald-j-trump-united-states` join `elon-musk-musk` and `rachel-simon` as candidates for a separate, approved
  repair once the code is deployed. A dry-run of the stale-name script on the live DB is also a separate step.
- **Residual:** a lone "Musk" with no full name in its item is still typed PRODUCT by the English model. That is
  deliberate: the owner's constraint is no global surname aliasing. It can no longer become a second principal
  next to the person (change 3).
- Development 447's over-merge belongs to the Development-identity follow-up.

Artifacts: `gate_replay.py` (both versions' outputs are in the session scratchpad, not committed).
