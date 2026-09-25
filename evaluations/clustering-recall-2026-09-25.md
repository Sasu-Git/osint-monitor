# Narrative clustering recall — 2026-09-25

Evidence for tuning, not a benchmark: one day, one collect, 90 narrative items, one reviewer.

**Data:** the eval database from the real collect of 2026-09-25 (latest fetch 08:35 UTC), 48-hour window.
Six news feeds: Al Jazeera, BBC World, South China Morning Post, Breaking Defense, Defense News, War on the Rocks.
Structured feeds are excluded, because they are grouped by record identity instead.

**Reproduce:**
```
OSINT_DB_URL=sqlite:///data/eval/recall-2026-09-25.db python main.py inspect clustering --export review.json
python main.py inspect clustering --review evaluations/clustering-recall-2026-09-25.json
```

## Population

| | count |
|---|---|
| narrative items | 90 |
| clustered | 10 (5 clusters, all 2 items from 2 sources) |
| noise | 80 |

Noise, banded by cosine similarity to the nearest item from a different source:

| band | count |
|---|---|
| linkable, ≥ 0.53 | 0 |
| near, 0.45–0.53 | 15 |
| related, 0.35–0.45 | 26 |
| far, < 0.35 | 39 |

## Sample (40 items, seed 20260925; every near-band item was eligible, the rest random)

| label | count |
|---|---|
| legitimate singletons | 28 |
| low value (roundup, promo, reader Q&A) | 3 |
| missed event members | 1 |
| missed new events | 8 |
| of which multi-source | 7 |
| of which same-outlet follow-ups | 2 |

The rate of multi-source misses rises with similarity:
- **near:** 6 of 11 sampled items;
- **related:** 2 of 11;
- **far:** 1 of 18.

Weighting those rates by band gives about 15 of the 80 noise items (roughly 7 stories) that should have been clustered. That sits beside the 5 stories that were clustered. Recall for multi-outlet stories is therefore well under half.

## Causes of missed joins

1. **Paraphrased headlines of one story.** Cosine 0.52: "OCCAR awards $4.2B DDX destroyer contract…" and "Italy taps state-owned firms to build two naval destroyers…".
2. **Different angles on one development.** Cosine 0.48–0.49:
   - market reaction vs response: "Oil prices jump after Houthis claim attacks on Saudi facilities" and "France to protect key Saudi oil terminal";
   - colour piece vs substance on the Trump–Xi state dinner.
3. **Colour pieces around a larger event.** Cosine 0.40: "Trump autopen joke draws rare laugh from Xi" beside the summit cluster.
4. **Low-overlap wording.** Cosine 0.34: "Pope Leo heads to France…" and "Hundreds of thousands expected in Paris for Pope's visit".
5. **Same-outlet follow-ups.** Al Jazeera ran three pieces on the protests against Netanyahu's UN visit. Same-source items link only on near-identical titles, by design.

## Threshold check: all 11 cross-source pairs from 0.45 to 0.53

Cosine alone cannot separate these pairs: 6 are the same story and 5 are not. The false ones score as high as the true ones:
- "Ukrainian drone attacks on Russia" and "CIA warned Europe of Russian drone attack": cosine 0.50;
- "Jewish protestors denounce Netanyahu" and "Netanyahu defends military action as delegates walk out": 0.49.

**Lowering `LINK_SIMILARITY` would add as many false joins as true ones. It was not changed.**

One additional condition separated all 11 pairs:

> 0.45 ≤ cosine < 0.53, **and** published ≤ 6 h apart, **and** ≥ 2 shared canonical actors

| pairs | hours apart | shared actors |
|---|---|---|
| true | 1.2–4.1 h | 2–5 |
| false | 18 h, 36 h and 6.8 h | 2 |
| false | 3.1 h and 5.7 h | 1 ("israel") |

## Proposal (not implemented)

Add that secondary link to `_linked`, behind a config flag, only after a second review day confirms it. Only 11 pairs back it, and one false pair sits at 6.8 h, just past the 6 h limit.

Misses below 0.45 (items 3 and 4) need entity-based candidate generation, not a lower cosine. Defer that.
