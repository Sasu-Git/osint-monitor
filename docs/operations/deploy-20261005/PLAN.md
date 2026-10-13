# Post-soak fix plan (`fix/post-soak-20261006`)

**Base.** `production-stable-20261006` = `5f046b3`. The soak passed with follow-ups; the evidence is in
[soak-report-24h.md](soak-report-24h.md) and [post-soak-followups.md](post-soak-followups.md).

**The deployed code stays frozen.** Nothing from this branch reaches the live daemon until:

- the branch has its own tests and a passing regression gate (pytest, smoke, identity gold check, clustering
  benchmark, migration rehearsal);
- the owner has approved a new deploy candidate.

## Priority order (owner, 2026-10-06)

| # | Item | Why first | Done when |
|---|---|---|---|
| 1 | Spanish/Italian actor normalisation, and the Bolsonaro (Jair vs Flávio) ambiguity | The only follow-up that corrupts derived Situation identity (`estados-unidos-united-states`) | es/it country and organisation names normalise to their English canonical keys. "Bolsonaro" alone is not silently merged with "Flávio Bolsonaro". Tests cover both. A recompute plan exists for Situations on the live DB. |
| 2 | Trend baseline reset/rebuild | The source expansion invalidated the anomaly baseline: 377 trend alerts in 24 h | Baselines are rebuilt or normalised for the current source set, and a source-set change cannot raise an anomaly by itself. Trend alerts are treated as untrusted until then. |
| 3 | Post-deploy check fixes | False FAILs at every checkpoint | Stages are required only for runs that processed new items. The Development growth check excludes backlog (Developments first published before the deploy, or from first-time sources). |
| 4 | False operational alerts | Misleading operational alerts | No "Signal restored" when a stored analytic gap turns operational. "Source resumed" is suppressed when the silence predates the first ledger run, or when gaps are backfilled from the old daemon log. |
| 5 | Hot-tier latency | Hot awake coverage 88.5% | DNS/BGP runtime bounded (time budget or tier move). Skipped hot ticks are measured before and after. |
| 6 | Host power / deployment environment | 10.6 h of 24 h lost to lid close and battery standby | Runbook pre-soak checklist: AC power, lid state, `keepawake.py --display` (adopt the pythonw keep-awake). The deployment-host recommendation is documented. |

**Also open (no priority given):**
- the failing collectors: Nitter, Lawfare, X-ForYou, US Congress, Financial Intelligence (Quant);
- a "ledger starts at …" label in `main.py status`;
- the `python -c` import-probe note in the runbook.

## Status of item 1 (2026-10-06)

**Code.** `ActorNormalizer` changes:
- It reuses the gazetteer's es/it place names (`config/geography.yaml`) for mentions that are not already actor
  names.
- It matches accent-insensitively.
- `config/actors.yaml` gains es/it demonyms and organisation names (OTAN, ONU, Unión Europea, Casa Blanca …).
- `ambiguous_names: [Bolsonaro]`: a bare family name is not an actor; full names stay distinct.

**Gate versus `main`:**
- pytest 659 passed / 3 xfailed; smoke passed;
- entity benchmark: no unit changed;
- clustering benchmark (development): identical;
- identity scores (development): identical.

**Repair.** `scripts/repair_situations.py` is a dry run by default. `--apply` backs up first, then retires invalid
created Situations: status `closed`, slug renamed, members detached. `--regroup` runs the normal grouping stage
afterwards.

**Simulation on a backup-API copy of the live DB (2026-10-06 14:09Z):**
- **Retired**, exactly the two expected:
  - `estados-unidos-united-states` (actors collapse; E135, E157);
  - `bolsonaro-fl-vio-bolsonaro` (bare "Bolsonaro"; E114, E147, E148).
- **Kept:** `nato-russia`, and every seed.
- **Regroup:**
  - E227 (a Spanish Zelenskyy article) now joins the `russia-ukraine-war` seed;
  - a **new `russia-united-states` was founded by E159 (es) and E168 (en), which are one occurrence** (a Siberian
    lab-plague case in two languages).

**New finding (needs an owner decision before any live repair).** Cross-language Development splits count as
recurrence when a Situation is created. The English-only embeddings split one occurrence into en and es
Developments. With the actor names now aligned, those duplicates share an actor set and found a Situation. The
original `estados-unidos-united-states` was the same pattern (E135/E157 = one Fairford event).

**Options:**
- (a) Require the founding Developments to be distinct occurrences, for example not sharing a specific place
  within 48 h. This is a Situation-grouping change.
- (b) Fix cross-language identity first (Phase 2 known limit).
- (c) Accept and repair periodically.

**The live DB has not been touched.** The repair runs on live only with a new deploy candidate and owner
approval.

## Item 6 (2026-10-13): daemon supervisor

`scripts/ops/supervisor/` (`9b2d652`, `a3cdff4`), installed as the scheduled task "OSINT daemon supervisor" on the
live host: restarts the daemon when its process is gone, pinned commit only, at most 3 times an hour, HOLD file for
deliberate stops, keeps the keep-awake running. Trigger: a second unattended stop (2026-10-09 21:05 UTC, silent)
cost 3 days 10.5 h of collection. Operating notes in `data/deploy/LIVE-DAEMON.md` (host, outside git).

## Item 2 (2026-10-13): trend baseline (design fixed before code changes)

**Diagnosis** (backup-API copy of the live DB, 2026-10-13): `detect_anomalies` compares an entity's mentions in the
last 24 h (by `fetched_at`, every source) with the mean and standard deviation of its stored 24 h snapshots from
the last 30 days. The live DB starts on 2026-09-25 with 22 sources; the 2026-10-05 deploy added 30 sources and
daily items rose about 5x (250 to 1,300). Trend alerts went from 6-20 a day to 167 (10-05) and 307 (10-06).

**Rules:**
1. **Stable source cohort.** A source counts only once it has collected for at least 14 days (its first item is at
   least 14 days old). The baseline uses only days on which every cohort source was already collecting, so the
   baseline and the current window always cover the same sources: a source-set change cannot raise an anomaly by
   itself, and a new source enters with 14 days of its own history.
2. **Event time.** Mentions are counted by publication time (collection time when missing), so a backlog
   collected at once after an outage does not spike.
3. **Incomplete days.** A baseline day whose cohort item volume is below half of the median day is excluded
   (outages, partial collection).
4. **Baseline from raw items.** Daily counts are computed from the items at each run (no stored baseline to go
   stale or to reset); trend snapshots are still stored for the dashboard. At least 7 complete baseline days are
   required, and the standard deviation is floored at the Poisson level (`sqrt(mean)`, at least 1) so that a
   near-constant series cannot turn a small change into many sigmas. The anomaly threshold stays 2 sigma.

**Measurement:** replay detection at the end of each day on the DB copy, old method vs new, alerts per day; the
source-expansion days (10-05, 10-06) must not spike under the new rules.

**Item 2 amendment (after the first measurement, 2026-10-13).** Counting days without a mention as zero lets a
rare entity reach 2 sigma with two mentions: at the first evaluation with a cohort (2026-10-10 00:00 UTC), 15 of
the 23 anomalies had 2-4 mentions (Waze, Yandex, a single person's name), while those with 5 or more read as news
(Russia, ICC, Panama, Putin, Poland). The old rule avoided this only indirectly (it skipped entities with fewer than
5 snapshots). Added: an anomaly needs at least 5 mentions in the current 24 h (`MIN_CURRENT_MENTIONS`). Nothing else
changed.

**Item 2 result (2026-10-13).** Replayed at the end of each day on a backup-API copy of the live DB
(`data/eval/trends-20261013.snapshot.db`), old rule vs new:

| evaluated (UTC) | old | new |
|---|---|---|
| 09-26 .. 10-04 (before the expansion) | 0-13 a day | 0 (no source has 14 days yet) |
| 10-05 .. 10-09 (the source expansion) | 10, 39, 32, 32, 28 | **0** |
| 10-10 00:00 (first evaluation with a 14-day cohort) | 15 | 8: US Department of Defense, Russia, Panama, Putin, Poland, Washington, ICC, Army |
| 10-13 07:30 (after a 3.5-day outage) | 0 | 0 |

The 30 sources added on 2026-10-05 enter the cohort on 2026-10-19; until then trend anomalies come from the
original 22 sources only. Stored trend alerts from before this fix stay as they are (untrusted history).
Tests: `tests/test_trend_baseline.py` (steady series, real surge, new source, backlog, outage days, short history,
rare entity). pytest 677 passed / 3 xfailed; smoke passed. Not deployed: reaches the live daemon only with an approved
candidate.

## Item 1, option (a) (owner decision 2026-10-13): founders must be distinct occurrences

**Rule** (`SituationGrouper.distinct_occurrences`, policy `founder_same_occurrence_hours: 48`). A new Situation needs
`create_min_developments` distinct occurrences, not Developments. Two founders count as one occurrence when they
have **no language in common**, were first reported within 48 h of each other, and name a compatible specific place
(the same place or one containing the other; countries and places that stand for a state, such as Washington or
Moscow, do not count; a place the gazetteer does not know matches only the same name). Development signatures carry
their items' languages and specific places.

**Why cross-language only (amendment after the first live-copy check).** The first version, a shared place within
48 h in any language, would have retired `france-pope`: the Pope's AI speech in Paris and the Paris Mass are two
English-language occurrences of one visit. Identity keeps same-language occurrences apart; it is across languages that
one occurrence becomes two Developments (the cross-language stage stays disabled), so only those founders are suspect.

**Repair.** `scripts/repair_situations.py` also retires a created Situation that claims recurrence (at least
`create_min_developments` Developments) but whose Developments are fewer distinct occurrences ("invalid
recurrence"); actor-identity retirements keep their wording.

**Checks.**
- On the live-DB copy the founding pairs score as one occurrence: E159 (es) / E168 (en), the Irkutsk plague case;
  E135 (en) / E157 (es), the Fairford bombers.
- Dry run on a backup-API copy (2026-10-13): retires exactly `bolsonaro-fl-vio-bolsonaro`,
  `estados-unidos-united-states` and `ucrania-ukraine` (a third Spanish/English actor collapse created live since
  10-06). `france-pope` and `russia-united-states` stay: the latter now holds several distinct occurrences (plague,
  fuel prices, sanctions law, diesel deal).
- Tests: `tests/test_situations.py` (one occurrence in two languages, distinct occurrences, same place days apart, a
  third founder, no places, switch off, same-language visit, signatures from real items), `tests/test_repair_situations.py`.
  pytest 685 passed / 3 xfailed; smoke passed.

The live DB is not touched: the repair runs on live only with a new deploy candidate and owner approval.

## Owner decisions, 2026-10-13 (after items 6, 2 and 1a)

- **Item 1 option (a) is split out.** The founder-distinctness guard changes the Situation creation contract after
  the exact actor-set holdout was accepted, and it was derived from the Fairford, Irkutsk and Ucrania failures, so it
  needs its own evaluation. It lives on `feat/situation-founder-guard` (at `1ef8f2b`, guard on). On this branch the code
  stays but `founder_same_occurrence_hours` is **null (off)**, and the repair retires only actor-identity failures. No
  live Situation is repaired yet.
- **Exact actor set stays the Situation policy.** The guard may become a precondition on founder distinctness; it does
  not redefine Situation identity.
- **Next deploy candidate:** the safe fixes only: the trend baseline (item 2), post-deploy check false failures
  (item 3) and false operational alerts (item 4), plus the item 1 actor normalisation already gated.
- **Hot-tier latency (item 5) and failing collectors** move to the following pass unless they worsen.
- **Daemon supervision is production architecture**, not soak tooling. It runs host-side (scheduled task, config
  outside git) and is not part of the deployed application code; the deployment runbook now holds it before stopping
  the daemon (X0) and re-pins and releases it after the start (S3) or a rollback (R-4b).
