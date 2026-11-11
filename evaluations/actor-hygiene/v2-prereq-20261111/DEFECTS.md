# Actor normalisation for Situation v2: frozen defect set (2026-11-11, before any code change)

**Track.** Replay-only prerequisite for Situation membership v2 (`CONTRACT-V2-R2.md` §0, frozen `bf57ed7`). No live
daemon or database writes, no deploy, no fresh-holdout window, no future holdout. The v2 contract and OD1–OD8 are not
changed.

**Source of the defects.** Only the frozen 126-case diagnostic review: `evalset/subsample/` (labels `57fef39`),
`evalset/key.json` and `evalset/cases.json` on `eval/situation-membership-evalset`, built from the 2026-11-02 snapshot
`data/eval/geolocation-iter3/snap-20261102.db` (sha256 `b5bb5728ce76d3eb28c70712b088b026268538243f4fa099744856dc2c29af40`).
**No case is added after the replay.**

**Code base.** `main` `0d3382d` (= deployed `484dcc8` + ops-only files). It already contains the 10-16 actor-hygiene
fix (storm names, same-item surname linking, one actor one identity).

## Defects (evidence = case / Development / where the name appears)

### A. One person counted as several actors inside one actor set (variants)

| ID | Variants | Evidence |
|---|---|---|
| A1 | Milei, Javier Milei | S006/D760, S074/D619 (principals and Situation `javier-milei-milei`) |
| A2 | Musk, Elon Musk's | S140/D320 (principals; Situation `elon-musk-musk`) |
| A3 | Pike, Christa Pike's | S169/D254 (principals; Situation `christa-pike-pike`) |
| A4 | Machado, Maria Corina Machado | S238/D954 (principals; Situation `machado-maria-corina-machado`) |
| A5 | Bukele, Nayib Bukele | S023/D501, S301/D837 (principals; Situation `bukele-el-salvador-nayib-bukele`) |
| A6 | Macron, Emmanuel Macron | S302/D973, S318/D250 (principals; Situation `emmanuel-macron-france-macron`) |
| A7 | Vance, J.D. Vance | S372/D186 (principals) |
| A8 | DONALD J. TRUMP, Trump | S042/D754, S056/D351 (principals; Situation `donald-j-trump-united-states`) |

### B. A person and the state that person acts for counted as two actors

| ID | Person -> state | Evidence |
|---|---|---|
| B1 | Emmanuel Macron -> France | Situation `emmanuel-macron-france-macron` |
| B2 | Nayib Bukele -> El Salvador | Situation `bukele-el-salvador-nayib-bukele` |
| B3 | J.D. Vance -> United States | S132/D1060, S372/D186 (with Trump / America) |
| B4 | Donald J. Trump -> United States (a full-name variant of the configured `Trump`) | Situation `donald-j-trump-united-states` |

### C. Words that are not actors

| ID | Words | Evidence |
|---|---|---|
| C1 | party words: Democrat, Democrats, Democratic, Republican, Republicans, Democratici | Situation `democrat-united-states`; S045/D449 (`Democratici` in the signature); S055, S079, S101 (mentioned) |
| C2 | language name: English | 69 of 126 cases list `English` among mentioned actors (e.g. S008/D453, S027/D775) |
| C3 | a rocket: Chinas Long March, China's Long March, Long March | Situation `china-chinas-long-march` (S090/D947, S107/D666, S312/D990) |
| C4 | storm names: Rachel, Simon (Simón) | S096/D402 principals; Situation `rachel-simon`. Expected to be handled already by the 10-16 storm rule; verified here, no new code |

## Expected result (on a backup-API copy of the snapshot, principals re-derived with the candidate code)

- **A:** inside one actor set, a one-word name equal to the last word of exactly one other multi-word name in that set
  is the same actor. If two multi-word names share that last word, nothing merges (the Bolsonaro rule).
- **B:** each listed full name keys to its state.
- **C:** none of the listed words is an actor.
- **Situation keys re-derived from their stored primary actors:**

  | Situation | Key now | Key after |
  |---|---|---|
  | `javier-milei-milei` | 2 keys | {javier milei} |
  | `elon-musk-musk` | 2 keys | {elon musk} |
  | `christa-pike-pike` | 2 keys | {christa pike} |
  | `machado-maria-corina-machado` | 2 keys | {maria corina machado} |
  | `bukele-el-salvador-nayib-bukele` | 3 keys | {el salvador} |
  | `emmanuel-macron-france-macron` | 3 keys | {france} |
  | `donald-j-trump-united-states` | 2 keys | {united states} |
  | `democrat-united-states` | 2 keys | {united states} |
  | `china-chinas-long-march` | 2 keys | {china} |
  | `rachel-simon` | 2 keys | {} |

## Constraints (owner rulings that must not regress)

- **No global surname aliasing** (owner, 2026-10-16). A bare surname is never mapped to a person outside the actor set
  or item in which the full name appears. So a lone "Musk" or "Macron" stays as it is.
- **Bolsonaro:** a bare ambiguous name stays ambiguous.
- **Mononymous people** are not deleted wholesale.
- Only full names are added to `represents`.

## Smallest change allowed

1. `config/actors.yaml`:
   - `non_actors` += C1, C2, C3;
   - `aliases` += `Donald J. Trump: Trump`;
   - `represents` += `Emmanuel Macron: France`, `Nayib Bukele: El Salvador`, `J.D. Vance: United States`.
2. One set-level variant collapse (rule A), used where actor sets become Situation keys (`ActorCanonicalizer.keys`).
   It is not added to `ActorNormalizer.key`, so Development identity, segmentation and entity resolution do not
   see it.

## Gate (all must hold; measured against `0d3382d` on the same inputs)

| # | Gate | Pass condition |
|---|---|---|
| G1 | Known defects | every expectation above holds |
| G2 | Entity benchmark (`main.py inspect entity-benchmark`, gold rev 3) | no metric drops; per-unit diff limited to C-list words or none |
| G3 | Identity gold check (`evaluations/identity/scripts/gold_check.py`) | passes (checks 1–6); holdouts not opened |
| G4 | Phase 2 identity, development windows only (`score_identity.py`) | identical to `0d3382d`, or every change explained by a C-list word |
| G5 | Actor-type distribution, all Developments of the snapshot | principal entity-type mix and the distribution of principal-key counts per Development change only on Developments carrying an A/B/C name; the share of Developments with ≥ 1 principal key drops by < 1 point |
| G6 | Unrelated identity behaviour | the Development topic keys (`ActorNormalizer.keys`, used by `development.py`) differ from `0d3382d` only on Developments carrying a B or C name |
| G7 | pytest | full suite passes, with no new failure |
