# Situation grouping after the actor improvements — 2026-09-25

Evidence for tuning, not a benchmark: one day of news, one reviewer.

The grouper code and thresholds are unchanged: join 0.60, ambiguous band 0.40, minimum actor coverage 0.5, create on an exact actor set that recurs ≥ 2 times.

**Reproduce:** `OSINT_DB_URL=sqlite:///data/eval/<db> python main.py inspect situations`

## Data

1. **Real events, three eval databases, principal actors recomputed with current code:**
   - 2026-09-24: 6 events with principals.
   - 2026-09-25 morning: 5.
   - 2026-09-25 afternoon: 6, from a fresh collect with the full Prompt 1–4 pipeline, run twice.
2. **Single-item developments, read-only.** The 90 news items of each 09-25 collect were grouped as if each were a development: principals, region and embedding per item. This asks what the grouper does with inputs that clustering currently drops.

## Answers

**1. Do seeded situations receive obvious developments?**
Yes, when the development exists.

| Development | Situation | Score |
|---|---|---|
| "Iran's president tells Trump it will never 'bend the knee'" | `us-iran` | 0.75 |
| "Multiple regions in Russia come under Ukrainian drone attacks" | `russia-ukraine-war` | 0.69 |

Both are single-outlet items, so neither became an event: the gap is clustering recall (see `clustering-recall-2026-09-25.md`), not grouping.

No real event of the three days belongs to a seeded storyline, because the seeds' stories never clustered. Seeded situations therefore have no member developments, so no centroid, and the semantic signal never runs for them.

**2. Are false joins still prevented?**
Yes, with one questionable case.
- The US–China summit reaches `eu-china-trade` at 0.44 and `us-iran` at 0.31, and stays out of both.
- Across 84 single-item developments, every other near candidate stayed at 0.31–0.44:
  - the Netanyahu UN protests, against `gaza-ceasefire`;
  - Chinese lifestyle and education stories, against `eu-china-trade`;
  - US-only defence stories, against `us-iran`.

**Questionable:** "CIA warned Europe of Russian drone attack from vessels in the Mediterranean" → `russia-ukraine-war` at 0.64. The evidence is one shared actor (Russia, coverage 0.5), the keyword "drone" and the region. It is a Russia–Europe hybrid threat, not the war itself. It is one case, so there is not enough evidence to raise `min_actor_coverage`.

**3. Does automatic creation fire with canonical principal sets?**
Yes. The fresh collect created `china-united-states` from two summit events, both scoring 0.97 on actor, region and semantic signals.
- The run 1 → run 2 check was idempotent: no assignment moved and no duplicate situation appeared.
- Nepal flood diplomacy (0.45) and the Air Force China think tank (0.51) stayed out.

**4. Is exact actor-set recurrence too restrictive?**
Not for membership:
- A created situation takes later developments through the normal coverage rule. {Australia, China, United States} joins `china-united-states` with coverage 1.0.
- In the single-item run, 9 summit pieces joined the created situation.

For creation, one real case is blocked by exactness. On 09-25, the Houthi attacks on Saudi facilities appear as:
- {Houthis, Saudi Arabia} in the morning collect;
- {France, Houthis, Saudi Arabia} in the afternoon collect.

Each exact set occurs once, so no situation is created, even though the pair recurs.

## Recommendation

Keep the architecture and all thresholds; the evidence does not support tuning.

For a later prompt, not implemented, a creation rule on a **recurring canonical actor pair**, where:
- the pair appears in ≥ 2 unassigned developments within the window;
- the developments are semantically similar (cosine to each other ≥ the grouper's semantic signal median, to be calibrated) and share a domain;
- the slug is the sorted pair, so creation stays canonical and a later {A, B, C} development joins by coverage instead of creating {A, B, C}.

Watch for:
- **Seeds for place-centred storylines.** `gaza-ceasefire` lists actors, but "Trump's Board of Peace unveils $2.45bn Gaza recovery plan" names neither Israel nor Hamas and never becomes a candidate. A keyword or place gate for seeds would be a separate change.
- **Principal noise that reaches situations:** "mooncakes", "scmp" and "intel" as actors. `CIA` isn't mapped to the United States.
