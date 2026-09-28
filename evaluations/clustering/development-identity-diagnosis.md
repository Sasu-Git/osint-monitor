# Development identity: over-merge diagnosis and recommendation (Phases 1-4)

Written 2026-09-28 on branch `feat/development-identity`. Development windows only (2026-07-21,
08-07, 08-15, 08-21 blind; 2026-09-25 non-blind). The hold-out was not used. Production code is
unchanged. Analysis re-ran the production clustering stages on replayed vectors; it reproduced
the production clusters exactly in all 5 windows.

## Phase 1: diagnosis of current over-merges

- 54 clusters, **32 mixed**. 31 of them contain 2 or more gold developments; the other one joins a
  gold development with an unlisted item.
- Gold units per mixed cluster: 2 units (16 clusters), 3 (8), 4 (6), 6 (2). In total, 60 extra
  units were absorbed into another development's cluster.
- Time span: mixed clusters have a median span of 22.5 h (max 46 h); pure clusters have a median of
  5.0 h (max 24 h).

### Failure categories (60 absorbed units, relative to each cluster's core development)

| category | units | example |
|---|---|---|
| analysis / explainer | 14 | "Zelenskyy sacks Syrskii: How many generals have Ukraine, Russia fired?" into the sacking |
| different action, same actors | 13 | Infantino: BBC asks him to resign / Norway calls for resignation / backed in Colombia / denies claims |
| reaction | 8 | "Qatar denies it is detaining ... pilots" into "Iran urges Qatar to release pilots" |
| follow-up | 6 | Lebanese await return in 'pilot zone' (next day) into the army deployment |
| repeated action, different date | 6 | US strikes on Iran, nights 10 / 11 / 12; Israeli strikes on Lebanon on consecutive days |
| rolling coverage (live blog / daily roundup) | 4 | "Iran war live: ..." chaining the Mecca pact cluster to the Hormuz talks |
| unrelated, topical | 4 | Brazil AI supercomputer + China telecom AI revenue |
| unrelated, template | 3 | Guyana ferry + Afghanistan floods + Mauritania boat ("N dead after ...") |
| preview vs occurrence | 1 | "Trump softens tone ... before Rubio-Wang talks" into the meeting |
| policy response | 1 | Thai PM pledges gun laws, into the shooting |

### Cause attribution

| suspected cause | finding |
|---|---|
| pair links | **50 of 60** absorbed units link directly to the core (cosine >= 0.53 cross-source) |
| chaining through a third unit | 10 of 60, mostly via live blogs and roundups |
| HDBSCAN / global clustering | not the cause: the link graph re-decides every HDBSCAN candidate |
| noise attachment | 0 units joined only by attachment |
| embedding similarity | the joining links sit well above threshold (0.53-0.83; repeated actions 0.60-0.76), so no threshold change separates them without destroying recall |
| temporal window | 72 h link window. Absorbed units join across 2-43 h, median about 20 h; SAME pairs median 5 h |
| same actors | actor Jaccard is identical for SAME and RELATED linked pairs (median 0.33) |
| templated headlines | 3 template merges, plus 1 same-source templated pair ("11th consecutive night" vs "10th", fuzz ratio 98) |
| later articles absorbed into an older cluster | not measurable: replay is one-shot, and the daemon's incremental extension is not replayed |

## Phase 2: separating signals

The table covers all SAME pairs linked by the current clusterer (59), RELATED linked (53) and
UNRELATED linked (10). Each row gives the share of pairs a signal flags as "not the same
development". Flagging a SAME pair is recall cost.

| signal | SAME (cost) | RELATED | UNRELATED | note |
|---|---|---|---|---|
| analysis/explainer headline vs report headline | **0/59** | 12/53 | 1/10 | headline form: question, What/Why/How, "what we know", explainer |
| headline-only embedding similarity < 0.5 (cross-source) | 1/59 (0 blind) | 5/53 | **7/10** | catches template merges |
| disjoint location sets | **0/59** | 3/53 | 5/10 | |
| hours apart > 24 | 4/59 | 18/53 | 3/10 | the SAME losses are death-toll updates (Guyana 27 -> 41 -> 53) |
| hours apart > 18 | 8/59 | 30/53 | 4/10 | |
| preview headline marker | 2/59 | 6/53 | 0 | noisy ("will") |
| explicit weekday date conflict | 0 | 0 | 0 | weekday mentions almost absent in RSS titles and leads |
| ordinal conflict ("11th night", "Day 28") | 0 | 1 | 0 | rare |
| event type / domain / concreteness mismatch | 17-19/59 | 28-30/53 | | classifier output is too unstable for identity |
| no principal overlap | 21/59 | 23/53 | | no separation |
| different headline root verb | 50/59 | 48/53 | | no separation |
| lead-sentence similarity | median 0.50 vs 0.46 | | | no separation |

Hours apart by bucket, SAME (all) vs RELATED linked: 0-3 h 47 vs 3; 3-6 h 20 vs 2; 6-12 h 25 vs 6;
12-18 h 8 vs 12; 18-24 h 8 vs 12; 24-36 h 6 vs 13; over 36 h 0 vs 5. Time is the strongest single
signal, but its SAME cost falls on the long-tail updates of big developments.

Summary: headline form separates event from analysis almost for free. Headline-only similarity and
location separate template and unrelated merges. Nothing available separates **report vs report
within the same storyline** (reactions, different actions, repeated actions, follow-ups) except time,
which has a real recall cost. Explicit event dates would be the right signal for repeated actions,
but RSS descriptions rarely carry them.

## Phase 3: architectures compared

Offline, development windows. Blind = the 4 blind windows (baseline 29/30 multi-source recovered,
54/55 cross-source SAME pairs linked).

| variant | blind multi-source | blind xs SAME | RELATED linked | UNRELATED linked | mixed clusters | collapsed units |
|---|---|---|---|---|---|---|
| baseline | 29/30 | 54/55 | 130 | 25 | 31/49 | 90 |
| A: link window 24 h (not 72 h) | 27/30 | 51/55 | 73 | 13 | 28/46 | 68 |
| A: link window 18 h | 24/30 | 46/55 | 47 | 9 | 22/42 | 53 |
| A: guard analysis only | 29/30 | 54/55 | 101 | 24 | 27/47 | 76 |
| A: guards analysis + location | 29/30 | 54/55 | 96 | 11 | 25/46 | 69 |
| **A or B: guards analysis + location + headline** | **29/30** | **54/55** | **76** | **3** | **23/44** | **60** |
| A or B: guards + edge <= 24 h | 27/30 (3 partial) | 51/55 | 49 | 2 | 21/42 | 48 |
| B: guards + edge <= 18 h | 24/30 | 46/55 | 31 | 0 | 15/38 | 34 |
| B: guards + temporal-gap split 12 h | 22/30 | 43/55 | 42 | 0 | 17/42 | 42 |
| C: guards + 24 h, only if span > 18 h or analysis | 27/30 | 51/55 | 49 | 3 | 22/43 | 50 |
| C: guards + 24 h, only if span > 24 h | 27/30 | 51/55 | 65 | 4 | 25/44 | 59 |

- **A (link guards) and B (post-cluster segmentation) give identical results for the same guards.**
  Almost every merge is a direct link, so cutting incompatible links inside the clusterer and
  re-splitting its clusters afterwards remove the same edges.
- The guard variant keeps every cross-source SAME pair on the blind windows. It loses 3 same-outlet
  SAME pairs that were bridged through a separated item (night-11 pair, Moscow drone attack pair,
  Ervebo doses pair) and 1 cross-source pair on 2026-09-25 (CASI, headline similarity 0.43). Single-
  and multi-item recovery of all multi-item developments falls from 32/45 to 29/45 on the blind
  windows.
- Any time cut costs multi-source recovery (29 -> 27 at 24 h, 24 at 18 h). Temporal-gap splitting
  (B, 12 h) is the worst on recall.
- Conditional segmentation (C) is no better than applying guards everywhere, and misses the short-span
  merges (reaction 2.2 h, rolling coverage 0.2 h).

## Phase 4: recommendation

**ADD INCOMPATIBILITY GUARDS**, implemented as a separate deterministic step after narrative
clustering (`segment(cluster) -> list[group]`), off by default and configurable:

1. analysis/explainer headline vs report headline: never the same development;
2. cross-source headline-only similarity below a threshold (0.5): not the same development;
3. disjoint location sets: not the same development.

Why this and not the others:

- It is the only variant with **no cross-source recall loss** on the blind windows (54/55, 29/30).
  It removes 42% of related-but-distinct links and 88% of unrelated links.
- As a post-cluster step it leaves HDBSCAN, the thresholds, the link graph and structured grouping
  untouched. It is reversible by one config flag, explainable per split (which guard fired on which
  pair), and costs one extra title embedding per item with the existing model. No LLM, no new
  dependency.
- A time cut is not recommended as a default. It is the only lever against repeated actions and
  same-storyline sequences, but on this benchmark every setting loses 2-8 multi-source developments.
  It can ship as a config option that defaults off, and be revisited if the event date can be
  extracted from full text.
- Full development segmentation (B with time), conditional segmentation (C) and a stricter global
  link threshold do not beat the guards on the recall/precision trade-off.

What it does not fix: after the guards, 76 related links remain, nearly all report vs report in one
storyline (reactions, different actions by the same actors, repeated actions on nearby days,
follow-ups). These are the next frontier. They need an explicit event date/time or an action
identity signal that this benchmark's RSS text does not provide.

Risk: the headline-form patterns and the 0.5 headline threshold were chosen on development windows.
The hold-out, run once after freezing, is the check. The live 2026-09-27+ window is the check for
the current source mix.

## Commentary / analysis rule (recommended)

Analysis, explainers, opinion and live blogs are **not evidence of a development**. They report no
new occurrence and must not count as corroborating sources.

- They never join a Development's evidence set. Guard 1 enforces this.
- They are kept as **commentary linked to the Development they discuss**, recorded on the pair
  that would have merged them. They roll up to that Development's Situation. If they discuss no
  single development, they attach to the Situation only.
- Live blogs and daily roundups are rolling coverage. They are treated like commentary unless their
  headline is a single concrete occurrence.

Phase 5 can at minimum return the separated items with the development they were cut from. Storing
and displaying commentary links is a separate UI/data step.

## Working definition of Development identity

> Two source items describe the same Development when they report the same concrete occurrence
> (an action, interaction, decision, statement or incident), with compatible actors, place and time,
> such that one could be a rewrite or an update of the other. Updates to the same occurrence
> (rising death toll, later details) stay in it. A reaction to it, a response or policy decision
> following it, a repeated occurrence of the same kind on another day, a preview before it, and
> analysis or explainers about it are different Developments, or commentary, in the same storyline
> or Situation, however similar the language or the actors.

Operational tests implied by the benchmark:

- Similarity decides candidacy, not identity.
- A report and an analysis piece are never the same Development.
- Different places are never the same Development.
- Headlines that do not describe the same thing (low headline similarity) are not the same
  Development, whatever the body similarity.
- Distance in time is evidence against identity, not proof.

## Not changed

No production code, thresholds, situation matching, principal extraction, classification, source
grouping or database was touched. The hold-out was not run for this work.
