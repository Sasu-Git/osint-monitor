# Actor-identity defects found in the 2026-10-13 soak (frozen 2026-10-16, before any fix)

Two Situations were created on the live daemon after deploy-candidate-20261013 (`3eda6d0`, now
`production-stable-20261016`). Both rest on wrong actors. The owner ruled (2026-10-16):

- not to repair them ad hoc;
- not to add Situation-specific logic;
- to fix them in entity resolution / actor normalisation, gated by the entity gold (revision 3), the identity gold
  and a Situation regression.

The evidence is extracted from an immutable snapshot by `extract.py` into `evidence.json` (hashes in `FREEZE.md`).

## D1: `elon-musk-musk`, an alias / entity-resolution failure

**Situation.** Primary actors `["Elon Musk", "Musk"]`, founded by two Developments:

- Development 320: Starlink in India (SCMP, Al Jazeera);
- Development 447: Spanish-language US politics (Musk's midterm donations, plus Guilfoyle, White House press
  access and press secretary items).

**Observed** in the extracted mentions and entities:

1. **D1a: legacy unclean canonical name.**
   - Entity 1238 is `Elon Musk's` (PERSON, alias `Elon Musk’s`). It was created before possessive normalisation.
   - Clean mentions `Elon Musk` resolve to it `fuzzy-provisional` (score 90): "not stored as an alias".
   - Normalisation cleans new canonical names but never repairs an existing one.
2. **D1b: surname mention typed and resolved as a different entity.**
   - `Musk` resolves `exact` to entity 9920 `Musk`, typed **PRODUCT**.
   - This happens in items that also name `Elon Musk` (items 7717, 9382).
   - There is no within-item link from a surname to the full name already mentioned.
3. **D1c: glued spans become PERSON/ORG entities**, for example:
   - `Elon Musk jab Musk` (item 6668, `new`);
   - `Elon Musks Starlink`, `Elon Musks Spacex`, `Musk Anduril`, `Ukraine Elon Musk`, `Alex Gibneys Musk`.
4. **Separate observation, not part of this defect:** Development 447 merges unrelated Spanish items (Musk donations,
   the Greece ambassador, CNN access, the press secretary). That is a Development-identity over-merge, recorded for
   the identity defect review. It is not an entity fix.

**Expected after a fix:**

- One PERSON identity `Elon Musk`.
- A `Musk` mention in an item that names `Elon Musk` resolves to that person.
- No PRODUCT `Musk` principal.
- No glued span becomes an entity.
- Under the exact-actor-set Situation policy, these Developments no longer present two actors, so no
  `elon-musk-musk` Situation would be founded.

**Constraint (must not regress):**

- Surname-to-full-name linking must not reintroduce the Bolsonaro defect: a bare `Bolsonaro` stays ambiguous between
  Jair and Flávio.
- Linking is therefore only acceptable within the same item, and only when exactly one full-name candidate with that
  surname is present.
- Bare surnames never merge across items.

## D2: `rachel-simon`, a person-name extraction / principal-actor hygiene failure

**Situation.** Primary actors `["Rachel", "Simon"]`, founded by two Developments:

- Development 402: "Hurricane Simon, storm Rachel batter Mexico" (DW, Al Jazeera, GDELT);
- Development 429: "Huracanes en México: Simón y Rachel…" and a Europa Press item on "ciclón 'Rachel'".

**Observed:**

1. **D2a: named storms typed PERSON.**
   - `Hurricane Simon` is correctly an EVENT (entity 10744).
   - The bare names in coordinated or reduced forms are PERSON:
     - "Hurricanes Simon, Rachel remnants" → `Simon` and `Rachel`;
     - "Simón y Rachel";
     - "ciclón 'Rachel'".
   - `Simon` (10091) and `Rachel` (10777) are PERSON entities resolved `exact` thereafter.
   - The Spanish `Simón` resolves `fuzzy-provisional` (score 80) to `Simon`.
2. **D2b: single given-name PERSON entities become principal actors.** Development 402's only principals are
   `Simon` and `Rachel`.
3. **D2c: a quote-prefixed span.** `'Rachel` resolves to `Rachel` (a stray quote character in the span).

**Expected after a fix:**

- A name governed by a storm descriptor is the storm event, not a person. Descriptors include hurricane, storm,
  typhoon, cyclone and tropical storm, and their it/es forms (huracán, tormenta, ciclón, uragano, tempesta, ciclone).
  This includes the second name in a coordination ("Hurricanes Simon and Rachel").
- No PERSON principal from these items.
- No `rachel-simon` Situation would be founded.

**Constraint:** single-token person names that really are people (for example a mononymous leader) must not be
removed wholesale. The fix is about the storm context, and about principal eligibility of bare given names. It does
not delete single-token PERSON entities.

## Gate for a fix (pre-registered)

- **Entity benchmark** (`python main.py inspect entity-benchmark`, gold revision 3): no metric drops. Per-unit
  comparison against the `production-stable-20261016` run.
- **Identity gold check:** unchanged on all dev windows. The sealed holdouts are not opened.
- **Defect cases:** D1 and D2 expectations met when the extraction and resolution are re-run on these items from the
  snapshot.
- **Situation regression:** on a copy of the snapshot, re-derive the principals of every Development that
  belongs to a Situation.
  - No valid Situation loses its actor set.
  - `bolsonaro-*` stays retired.
  - No new actor merge appears.
- **pytest and smoke** pass.
