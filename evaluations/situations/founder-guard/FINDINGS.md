# Founder-distinctness guard: census before building an evaluation set (2026-10-13)

**Status (owner, 2026-10-13): DEFERRED: no demonstrated incremental value after actor normalisation.** The guard stays
off and on this branch. Its evaluation starts only when a live census (`census.py`) finds one or more genuine
guard-positive founder pairs.

Owner request: a frozen evaluation set answering "does the guard suppress duplicate founders without suppressing
legitimate Situation creation?". Before drawing it, the founder-pair population was measured.

**Data:** the deploy's final verified backup, `data/deploy/20261013-1246/backup-final-20261013-105028.db` (live DB at
2026-10-13 10:50 UTC, read-only). **Code:** this branch (`1ef8f2b`: the item 1 actor normalisation as deployed, plus
the guard). `census.py` -> `census.json`.

## Population

A founder pair = two Developments with the same canonical principal actor set (>= 2 actors) whose first reports are
at most 7 days apart: what the exact actor-set rule counts as recurrence.

| | pairs |
|---|---|
| founder pairs | 69 (177 Developments, 151 actor sets) |
| cross-language | 12 |
| **cross-language, shared specific place, <= 48 h (the guard counts them once)** | **0** |
| same-language, shared place, <= 48 h (e.g. `france-pope`) | 6 |
| shared place, > 48 h apart | 3 |

## The motivating cases no longer found Situations

Under the deployed actor normalisation:

| case | founders | canonical actor sets | consequence |
|---|---|---|---|
| Fairford | E135 (en), E157 (es) | {United States}, {United States} | one actor: below `min_actors_to_create`, no Situation |
| Irkutsk plague | E159 (es/it), E168 (en) | {United States}, {Russia, United States} | different sets: no recurrence between them |
| Ucrania | E208, E227, E238 (all es) | {Ukraine}, {Russia, Ukraine}, {Ukraine} | same language: the bug was the actor collapse ("Ucrania"), not a cross-language duplicate |

`estados-unidos-united-states` and `ucrania-ukraine` were founded by actor-name splits that the normalisation removes
(they are among the three actor-identity retirements of the pending repair). None of the three cases needs the guard.

## Consequence

On current data the guard would not change a single Situation decision. A frozen labelled set drawn now would contain
no case the guard acts on, so it could not measure duplicate suppression; it could only confirm, trivially, that the
guard suppresses nothing. The guard stays off and on this branch. Building the labelled set is deferred until the
population contains guard-positive pairs: cross-language founders with a shared specific place within 48 h under the
normalised actor contract. The census is re-runnable (`census.py DB`) to check for them.
