# Full basis audit of `main` (f7b01d5)

Date: 2026-09-30. Scope: the whole pipeline as the foundation for persistent Situation state, change history,
follows / last-seen, deterministic assistant actions and later LLM orchestration.

**Method.** Read-only.
- Code was traced at f7b01d5.
- Real data came from read-only copies of two pipeline snapshots taken 2026-09-30:
  - `inventory-2026-09-30.db`: 1335 items, 82 events, 7 situations;
  - `source-expansion-2026-09-30.db`: 560 items, 25 events, 5 situations.
- Both snapshots are at schema v3, produced before the entity-resolution merge. For sampled events,
  current-main principals were recomputed with the pure `development_actors`.
- Sampling scripts and traces are in `lineage/`, seed 20261001.
- `data/osint.db` and the live daemon DB were not opened.
- No runtime code was changed. The frozen Situation holdout (`feat/situation-coverage`) was not touched.

**Claims I verified myself:**
- `persist_clusters` overlap-merge and no split (code);
- `first_reported_at = utcnow()` (code);
- JSON alias append lost on persisted rows (in-memory reproduction);
- alert dispatch from a closed session (code).

Items marked *(inferred)* are read from code and were not executed.

---

## Executive finding

**FOUNDATION SOUND WITH BLOCKERS**

Four stop conditions were triggered: S1 identity, S2 Situation persistence, S3 time and S4 write loss (see *Stop
conditions*). Every readiness verdict in this document is conditional on them. **Build gate:** NO-BUILD for
Situation state + change history until Phases 0-2 land (see *Build / no-build gate*).

**Sound.** These layers are sound and can be built on:
- evidence capture: append-only raw items with unique (source, external id), no deletes anywhere;
- the entity contract: frozen owner-reviewed gold, fuzzy matching non-durable, roles from the parse, visible
  model degradation;
- provenance origin grouping;
- the migration framework;
- the frozen benchmark discipline.

**Not yet contracts.** The three objects every planned capability references are Development, Situation and
time. For each, the system stores the current state only. It keeps no record of how, when or why that state
was reached, and Development identity drifts under a fixed ID.

**The blockers are specific and additive:**
- a run ledger;
- membership timestamps;
- an explicit Development reconciliation rule;
- persisted Situation assignment decisions;
- separated time fields;
- a change log.

They do not require replacing SQLite or re-architecting the pipeline. They must land before follows,
last-seen, `get_changes_since` or an LLM layer. Everything built on the current Development and Situation rows
would otherwise inherit silent drift.

---

## Stop conditions

The audit was completed in full. Four blocker-level conditions were found, one per protected area. **Every
readiness conclusion below (temporal/change readiness, Situation readiness, assistant actions, build gate) is
conditional on S1–S4 being resolved.** No "ready" verdict holds while any of them stands.

| ID | Area | Condition | Evidence |
|---|---|---|---|
| **S1** | Identity stability | A Development ID does not pin its referent. Overlapping clusters are merged via an unordered `.first()`, items are never removed, and events are never split. | `processors/clustering.py:437-464` (`persist_clusters`), `:548-557` (`_find_overlapping_event`); `event_items` has no UNIQUE constraint (`core/database.py:202-208`). Data: INV E1/E2 share 13 items; E49 ⊂ E2 (6/6); E45 ⊂ E18; 24 items in two events. |
| **S2** | Situation persistence | Membership is write-once and unexplained. The grouper's reasons and candidates are discarded, and member content drifts under a fixed membership. | `processors/situations/store.py:98-118` (`assign_situations`), `core/models.py:472-478` (`SituationAssignment.reasons` not persisted); `events.situation_id` is the only record. Data: `china-united-states` holds E11 (CNN / Air Force One), E34 (pandas), E49 (Pope on AI), E25 (Greenland), with no stored reason. |
| **S3** | Temporal semantics | The main Development timestamps are processing times. Membership has no time. New evidence and reprocessing are indistinguishable. | `clustering.py:472` (`first_reported_at=datetime.utcnow()`), `:455` (`last_updated_at` on any membership add); `event_items` has no timestamp or run. Data: all 107 sampled events. INV E1 `first_reported_at` 09-25 09:44 vs earliest item 09-23 22:01; SX all 25 events first = last = 09-30 09:43. |
| **S4** | Data corruption risk | Silent write loss and duplicated membership. | `entity_resolver.py:459-465` (`_register_alias`) and `relations.py:399-403`: in-place JSON mutation is not persisted (reproduced: an alias appended to a stored row is lost); relation confidence climbs on reruns (3 of 21 relationships at 1.0 with one evidence item); 24 items in two events (S1); `scheduler.py:211-219` dispatches alerts from a closed session *(inferred)*. |

---

## Architecture map

### Orchestration

`run_tier` (`processors/pipeline.py:629`) does the following on each tick:
1. `init_db()` (`:642`), which also runs migrations.
2. Parallel collection (`:328-353`).
3. `process_new_items` under `DB_WRITE_LOCK` (`:650`).
4. `run_post_processing`, **only if new items > 0** (`:652-657`).

Post-processing runs these stages in order. Each goes through `_stage()`, which retries lock errors, rolls back,
logs and continues (`:445-463`).

| # | Stage | Definition | Scope | Writes | Main consumers | Tests / benchmarks |
|---|---|---|---|---|---|---|
| 0 | collectors | `BaseCollector.collect` (`collectors/base.py:30`), built in `pipeline.py:91-248`, tier map `:50-88` | per tier | none (returns `RawItemModel`) | storage | collector_bounds, source_expansion, vessel_parser, inventory |
| 0a | storage + dedup | `_process_single_item` (`pipeline.py:748-873`), `Deduplicator` (`dedup.py:80-146`) | new items | `sources` (`ensure_source :261-284`), `raw_items`, near-dup `event_items` (`:859-873`) | all | test_dedup (hash only) |
| 0b | NLP / entities / claims | `extract_entities` (`nlp.py`), `EntityResolver.resolve`, `extract_and_classify_claims` | new items | `entities`, `item_entities` (+ `resolution_method/evidence`), `claims` | clustering segmentation (places), principals, classifier, analysis | entity gold (25 Devs), test_entity_resolution, test_principals |
| 1 | clustering + segmentation | `cluster_recent_items` (`clustering.py:54-90`), `segment_groups` (`development_segmentation.py:186-227`), `persist_clusters` (`clustering.py:431-494`) | items fetched in the last 48 h | `events`, `event_items`, `event_entities` (legacy role) | everything downstream | clustering benchmark (9 windows), segmentation benchmark |
| 1b | principals / roles | `mark_principal_actors` (`principals.py:333-388`) | events updated in the last 3 days | `event_entities.is_principal`, `actor_role` | situations, ranking topic, UI | entity gold |
| 2 | fulltext | `fulltext.py` | ≤ 30 short items, last 24 h | overwrites `raw_items.content` (`:737-739`) | display | none |
| 2b | classification | `classify_events` (`development.py:89-113`), rules by default | events where `last_updated_at > classified_at` | `events.event_type…change_summary…classified_at` | ranking, UI | classification tests |
| 3 | relations | `persist_relations` (`relations.py:410`) | last 50 items | `entity_relationships` | graph | none |
| 4 | geocoding | `geocoding.py:343-349` | all events with a null region or lat | `events.region/lat/lon` | map, situations | none |
| 5 | corroboration | `compute_corroboration_score` (`corroboration.py:143-276`) + provenance | **all events ever** (`pipeline.py:551`) | `events.source_count/admiralty/corroboration_level/confidence_class` | alerts, ranking, UI | test_provenance |
| 5a | ranking | `rank_events` (`development.py:143-177`) | events updated in the last 7 days | `events.rank_score/rank_reasons/ranked_at` | UI (reasons), inspect | test_ranking |
| 5b | situations | `assign_situations` (`situations/store.py:88-122`) | unassigned events updated in the last 7 days | `situations`, `events.situation_id` | UI, ranking topic (next run) | test_situations, one 1-day review |
| 6-7 | I&W, fusion | `evaluate_indicators`, `fuse_signals` | last 24 h | none (counts only) | alert engine recomputes | test_indicators; fusion none |
| – | alerts | `AlertEngine.evaluate_all` (`alerting/engine.py:51-83`), a separate 10-min job (`core/scheduler.py:203-222`) | last 1 h | `alerts`, `state_snapshots` | channels, UI | **none** |
| – | trends / briefing | `trends.py`, `briefing.py:46-118` (06:00 **local** cron, `scheduler.py:284-291`) | windows | `trend_snapshots`, `alerts`, `briefings` | UI | **none** |
| – | API / UI | `api/app.py`, `api/situation_views.py`, SSE `api/websocket.py` | read side, plus 4 writers (ingest, webhook, ack, briefing-generate) | as listed | user | test_api_pages (render only), test_situation_views |

**Where the code differs from CLAUDE.md:**
- alerting is not a pipeline stage;
- ranking runs **before** situations, yet ranks by the situation topic (`development.py:163-167`);
- the briefing cron runs at local time, while `cli.py:276` prints "UTC";
- the default LLM is `gpt-4o-mini` (`config.py:331`), not gpt-5-mini;
- `/api/intel/webhook` stores items with no dedup, embedding or NLP (`api/routes/intelligence.py:200-232`), so
  they can never cluster.

---

## Domain-object contracts

| Object | Storage / id | Creator → mutators | Lifecycle / history | Status |
|---|---|---|---|---|
| Source identity | `sources.name` UNIQUE (`core/database.py:27-39`) | `ensure_source`; `type` corrected once | Never updated. `url` is the first item's URL; credibility frozen at creation (`pipeline.py:264-274`). `sources.yaml identity` is used only by the inventory | **implicit identity** (name = feed) |
| Source endpoint | not persisted (`collectors/inventory.py:1-25`) | – | – | **implicit** |
| Evidence item | `raw_items`, UNIQUE(source_id, external_id) | `_process_single_item`; `content` overwritten by fulltext; webhook | Append-only rows, but content is mutable with no revision. `processed_at` is never written | mostly stable |
| Claim | `claims` | stance; `event_id` set only when a new event is created (`clustering.py:491`) | Append-only; 258 claims in the snapshot are unlinked to their item's event | partial |
| Entity | `entities.canonical_name` UNIQUE | resolver, seed | Never merged or renamed. **Alias appends to a persisted row are lost** (`entity_resolver.py:459-465`, in-place JSON mutation, reproduced) | stable id, lossy aliases |
| Item–entity link | `item_entities` UNIQUE(item, entity, role) | ingest only | Write-once; records the resolver state at ingest | stable |
| Actor role / principal | `event_entities.is_principal/actor_role`, **no uniqueness** | `mark_principal_actors` | Overwritten each run for events in the 3-day window; older events are frozen under old logic; no history. `actor_role` has **no reader** | overwritten |
| Development | `events.id` | `persist_clusters` → classification, corroboration, rank, geocode, situation | Never deleted, split or merged. Grows by overlap. `summary` frozen at creation | **id stable, referent drifts** |
| Development membership | `event_items`, **no UNIQUE, no index, no timestamp** | clustering, near-dup link | Append-only; 24 items belong to two events | **implicit history** |
| Situation | `situations.slug` UNIQUE | `sync_seeds`, grouper | Never deleted. Seed title/description/actors overwritten from YAML every run (`store.py:37-38`) | stable id, mutable meaning |
| Situation membership | `events.situation_id` | `assign_situations` (only when NULL, `store.py:98-117`) | Write-once. Reasons and candidates **discarded** (`core/models.py:472-478`) | **unexplained** |
| Situation status | `situations.status` | seeds, `_touch`, `refresh_statuses` | Overwritten, no timestamp, no log | overwritten |
| Summary | `events.summary` (frozen headline); `change_summary`, `why_it_matters` | clustering / classifier | Overwritten on reclassify; no Situation summary | overwritten |
| Alert | `alerts`; `trigger_key` not unique; `superseded_by_id` no FK | engine, trends | Append-only. `supersede()` never called; `delivered_via` never persisted | append-only, lossy |
| Briefing | `briefings` | briefing | Append-only; stores no input ids; `model_used` = provider or "default" | append-only |
| I&W / fusion / signal gaps | **not persisted**; latest state only in `state_snapshots` (`alerting/state.py:34-43`) | – | Overwritten | **implicit** |
| Pipeline run | **does not exist** | – | – | **missing** |

---

## Identity stability

- **Item IDs:** stable within one DB (integer rowid, nothing deletes). They are DB-local, so a rebuild renumbers
  them. The natural key (source, external_id) is sound.
- **Development IDs** are never deleted. **Their referent is not stable:**
  - `persist_clusters` appends any new cluster sharing *one* item to the first matching event, via `.first()` with
    no ordering (`clustering.py:437-464,548-557`);
  - items are never removed;
  - events are never split or merged;
  - segmentation therefore protects only brand-new events. Once persisted, every segmented half that overlaps
    returns to the same event.
  - Observed:
    - E1 and E2 share 13 items;
    - E49 is entirely inside E2;
    - E45 is inside E18;
    - 24 items sit in two events.
- **Can segmentation recreate a Development under a different ID?** Yes, partially. A cluster with no overlap
  becomes a new event even if its items duplicate another event's story. Language-split twins exist: SX E5
  (Italian) vs E10 (English) vs INV E82.
- **Situation IDs:** stable by slug.
  - Renaming or removing a seed orphans the old row, which stays active (`store.py:28-41`).
  - Auto-created Situations can be neither renamed nor closed.
- **Does a Development move Situation?** Never; `situation_id` is write-once. But the Development's own content,
  principals and classification keep changing under that fixed membership.
- **Entity merges** do not exist, so there is no retroactive reinterpretation. Principal flags are recomputed
  under current config only inside the 3-day window, so history is mixed.
- **Can a followed Situation later mean something materially different?** Yes, in three ways:
  - member events absorb other occurrences;
  - seed text is overwritten;
  - member classifications are overwritten.

  There is no baseline to diff against.
- **Relationships:** overwritten in place. None are versioned.

---

## Stable identifiers vs display identifiers

Question: are user-facing names, slugs or titles used as persistent foreign keys or identity anchors?

**Foreign keys between tables are all integer ids, and none is a name.** The name-based anchors sit at the
boundaries: config ↔ DB, cross-run matching, and URLs.

| Object | Integer id used as FK? | Name / slug used as identity anchor | Consequence | Verdict |
|---|---|---|---|---|
| Source | yes (`raw_items.source_id`) | **`sources.name` (the feed display name) is the identity.** Lookups in `ensure_source` (`pipeline.py:263`) and the webhook (`api/routes/intelligence.py:214`) match on it. Provenance origin is keyed by lowercase feed name (`provenance/resolve.py:64-66`). Credibility is frozen at creation under that name. | Renaming a feed in `sources.yaml` creates a new Source row and a new origin. History splits, and independence counting changes. The `identity` field exists only in the inventory. | **FAIL**: display name is the identity |
| Development | yes (`event_items.event_id`, `/events/{event_id}`) | `summary` is display only (frozen headline). Seed keywords match against it (`grouper.py:263-266`). | ID anchor is sound. Referent is unstable (S1) | PASS (anchor) / S1 |
| Situation | yes (`events.situation_id`) | **`slug` is the public URL anchor** (`/situations/{slug}`, `api/app.py:98`) and the cross-run join key: seeds upsert by slug (`store.py:28-41`), assignments resolve by slug (`store.py:111-116`), ranking topic uses slug (`development.py:160-165`). Auto-created slugs are **derived from display-level actor keys** (`situations/canonical.py:397-401`). | A change in `ActorNormalizer` output (a new `represents` entry, a registry parent) yields a different slug for the same actor set, so a new Situation is created and the old one is orphaned. A seed slug rename orphans the row. Anything keyed by slug (URLs today, follows tomorrow) breaks. | **FAIL** for future user state; must key on `situations.id` |
| Entity | yes (`item_entities.entity_id`, `/entities/{entity_id}`) | **`canonical_name` UNIQUE is identity and display at once.** Principal links are re-joined **by name**: `mark_principal_actors` maps holder names to entities through a surface index and links "an existing entity with that name" (`principals.py:350-378`). Situation `primary_actors` stores display names (`store.py:33-38`, `grouper.py:343-346`) re-keyed at match time. `actors.yaml`, `institutions.yaml` and `represents` are all name-keyed. | The same person is "Donald Trump" in one DB and "Donald J. Trump" in another. Principal flags and Situation actor sets depend on surface-name matching, so a canonical-name difference changes downstream identity (`key("Donald J. Trump")` ≠ `united states`). | **PARTIAL**: ids are the FKs, names drive the joins |
| Actor key | n/a (computed) | `ActorNormalizer.key` lowercase names are used as ranking topics (`development.py:161-166`), Situation match keys and slugs | Not persisted except through slugs and `primary_actors` | PARTIAL |
| Alert | n/a | `trigger_key` embeds ids for events, sources and items (`alerting/engine.py:174,185,253,297,398`), but **config names** for I&W indicators and fusion patterns (`engine.py:136,220`) | Renaming an indicator key in config re-fires or loses dedup | PARTIAL |
| Indicator / scenario | n/a | `/indicators/{scenario_key}` is a config name (`api/routes/intelligence.py:113`) | Config name is the only identity (not persisted) | PARTIAL |
| Future user state | – | – | Must reference `situations.id` / `events.id`, **never** slug, title or `canonical_name` | requirement |

---

## Temporal / change readiness

### Timestamp inventory
All timestamps are naive UTC, except that some collectors pass tz-aware values.

| Column | Class | Problem |
|---|---|---|
| `raw_items.published_at` | publication (RSS) / **collection** (sensors, markets) / synthetic (UNHCR Jan 1) | overloaded; null for UN and OFAC sanctions (57 rows); stale historic dates (OONI 2020-25, NVD 2000, CSIS 2016); Council of the EU items dated ~1 h after fetch |
| `raw_items.fetched_at` | ingestion | sound |
| `raw_items.processed_at` | – | dead: 0 rows set |
| `events.first_reported_at` | **processing**, named like publication | all 107 sampled events; mean +11 h, max +42 h after their earliest item. The UI timeline sorts by it (`situation_views.py:162`) |
| `events.last_updated_at` | processing of a membership addition | new evidence and re-clustering are indistinguishable; the near-dup link adds members without bumping it; it triggers classify, principals, rank and situations |
| `classified_at`, `ranked_at` | processing | sound |
| `situations.updated_at` | "last member assigned" | not bumped by member growth, so a Situation goes dormant while its members update, and the UI shows a recent `last_changed` on a dormant Situation |
| `alerts.created_at` | state-change detection | quiet hours drop the transition permanently |
| `event_items`, principal/role, corroboration, geocode, assignment, status | **none** | no time at all |
| user observation | **none** | – |

### Can the system truthfully answer these today?
| Question | Answer |
|---|---|
| What changed since 08:00? | **Partially.** It can say which items were fetched, which events were created, and which events gained members. It cannot say what changed in classification, corroboration, principals, assignment or status. |
| What became known since yesterday? | **Items only.** Derived knowledge has no knowledge time. Dropped duplicates and same-source updates are not recorded. |
| Which Situation changed most recently? | **Only as** `max(member.last_updated_at)`. `Situation.updated_at` is wrong for this. |
| Was this evidence newly collected or merely reprocessed? | **No.** There is no membership timestamp and no run id. |

### Minimum missing temporal primitives
1. A `pipeline_runs` ledger: id, tier, start/finish, per-stage status and counts.
2. `event_items.added_at` + `run_id`, with UNIQUE(event, item).
3. Development `earliest_published_at` / `occurred_at`, distinct from `created_at`. Rename or re-derive
   `first_reported_at`.
4. An append-only change log for Development fields (corroboration, principals, classification, membership)
   and Situation fields (status, title).
5. `situation_memberships`: assigned_at, run, reasons, candidates, rule version.
6. A per-user observation record: last_seen per object.

**Can we reliably implement "what changed since I last checked?" today? No** (conditional on S1-S4; S3 alone
is sufficient to block it). Membership has no time. Most state
changes are overwritten with no log. The main change timestamp mixes new evidence with reprocessing. No
user-observation record exists. Any implementation today would be a heuristic over `fetched_at` and
`last_updated_at`, and it would misreport reprocessing as change.

### Change semantics per change type
| Change | Semantics |
|---|---|
| New Development | append |
| New evidence on a Development | append, untimed; claims not linked |
| New primary source | not modelled (computed at read time) |
| Stronger corroboration | overwritten for all events every run; lossy trace in alerts |
| Actor-role change | overwritten |
| Principal change | overwritten |
| Situation membership change | impossible after first assignment; the assignment itself is unlogged |
| Situation status change | overwritten, untimed |
| Summary regeneration | headline never regenerated; `change_summary` overwritten |

`get_changes_since(T)` would need primitives 1, 2, 4 and 5 at minimum. `state_snapshots` holds only the latest
state and cannot serve as history.

---

## Development integrity

An Event is a set of linked narrative items. It is not guaranteed to be one real-world development.

- **Clustering:**
  - 48 h pool;
  - HDBSCAN plus a link graph at cosine ≥ 0.53 (`clustering.py:26-38,177-187`);
  - minimum size 2;
  - segmentation cuts analysis↔report pairs, low headline similarity across outlets, and incompatible places
    (`development_segmentation.py:117-128`), within the batch only.
- **Measured** (`evaluations/clustering/segmentation-compatibility.md`):
  - mixed clusters go from 32/54 to 24/48 on development windows, and from 5/17 to 4/16 on a fresh live window;
  - 33 of 46 mixed clusters are storyline-level (`phase-c-holdout.md`): reaction, follow-up, same actors doing a
    different action. Thresholds cannot separate them.
- **Observed in the sample:**
  - INV E2: 32 items mixing the Xi summit, Pope Leo on AI, a Trump tech pact and a Natixis note.
  - INV E81: a Slovakia school killing merged with a Malaysia school beating.
  - INV E17: EU $7.5bn release merged with a US $307M obligation.
  - SX E9: a Madrid eviction, the royals receiving Macron, Sánchez decrees and French arrests.
  - SX E6: US SPR loan, EU gas warning and a diesel export ban.
  - SX E16: Iran's currency and the US reply.
  - SX E23: Council space act merged with a Commission communication system.
  - SX E22: US senators and Tigray.
  - Entity gold D05: 13 items covering at least 7 occurrences.
- **Roundups and analysis:**
  - rolling↔report and analysis↔analysis links survive segmentation;
  - roundup headlines become summaries: SX E12, E13, E15 (in E15 the roundup is half the evidence);
  - an analysis headline became the summary of INV E25;
  - only actor-role extraction drops roundups;
  - the diagnosis rule that live and roundup items must not count as corroboration
    (`development-identity-diagnosis.md:144-152`) is **not implemented**.
- **Single-source policy:** there is no gate. A same-outlet pair becomes an event:
  - INV E53: one BBC article at `#0`/`#1` URLs, rank 7.4;
  - SX E17: two unrelated Federal Register notices.

  It is flagged SINGLE_SOURCE only.
- **Structured and sensor records:** correctly never text-clustered with news. Only seismic has a grouping
  strategy, and it formed 0 groups in the snapshot; everything else is standalone.
- **Cross-language:**
  - no en+it or en+es merge was observed;
  - it/es stories duplicate English Developments;
  - the White House primary document stayed unclustered, at cosine 0.18-0.48 to its Italian and Spanish
    coverage.
- **Downstream consumers assume more coherence than clustering guarantees:**
  - corroboration counts origins across all items, so sources about *different* occurrences corroborate each
    other and a mixed Event can reach CONFIRMED;
  - the "corroboration upgrade" and "new event (N sources)" alerts;
  - one classification per Event;
  - ranking's "widely reported";
  - one flat principal set;
  - whole-Event Situation assignment;
  - a frozen summary.

  The only coherence check, the low-cohesion warning (`diagnostics.py:20,40-48`), gates nothing.

---

## Situation readiness

**Is Situation a persistent geopolitical state or a cluster of Developments?** It is an **actor-set bucket**
with a staleness clock:
- no state variables, phases or assessment;
- status = active / dormant (14 days since the last *new* member) / closed (seeds only);
- identity = a YAML slug (seed) or a sorted actor-key slug (auto-created, `grouper.py:316-354`);
- matching = state-level `ActorNormalizer.key` coverage ≥ 0.5, plus region, centroid and seed keywords, joining at
  ≥ 0.6 (`grouper.py:235-299`, `config/situations.yaml`).

**Observed:**
- `china-united-states` (auto-created) holds CNN barred from Air Force One (E11), pandas (E34), Pope Leo on AI
  (E49) and Greenland (E25);
- `france-pope` is an auto-created Situation for one papal visit, with `updated_at` stuck at creation;
- 17% (INV) and 8% (SX) of events have a Situation.

**Computed:** a single shared actor plus one keyword can clear the join threshold, because a missing region
raises the score: (0.5·0.5 + 0.2)/0.7 = 0.64. So a US-only development with "sanctions" in the title can join
`us-iran`.

**Explainability:** none persisted. `inspect situations` recomputes with the current profiles and the `none`
arbiter (`cli.py:398`). It is not a record.

**Is Situation stable enough to become the primary followed object? No, not yet** (conditional on S1-S4; S1 and S2
block it directly). The ID is stable. Three things
are not:
- **Content:** member Events drift and seed text is overwritten.
- **Semantics:** it is a bucket, not a state, and the arbiter or join rules can admit single-actor matches.
- **Accountability:** there is no assignment record, no status history, and the dormancy clock is inconsistent
  with member activity.

A follow built on it today could not tell the user *why* something is in their Situation or *what* changed.

---

## Entity-contract downstream audit

The entity layer is the regression-protected baseline (`evaluations/entities/entity-foundation-final.md`).
Its downstream use is not protected.

| Consumer path | Finding |
|---|---|
| `ActorNormalizer.key` (state level) used by the grouper, ranking topic, UI principal display and segmentation override | Institutions collapse to their **top** parent (`actors.py:56-70`). U.S. Navy, courts and CENTCOM → United States; Commission and Council → European Union; IAEA, WHO, ICJ, UNSC → United Nations. "IAEA censures Iran" keys to {united nations} and never reaches `us-iran`, although IAEA is one of that seed's keywords. The UI shows "United States" for a court ruling. This contradicts the registry's own "lowest meaningful acting body" rule. |
| Leader → state (`actors.yaml represents`) | Covers about 15 people and depends on the surface form. "Donald J. Trump", the multilingual canonical, keys to a person, not the United States. MBS, Sharif, Macron, Milei and Meloni are unmapped. |
| Multilateral bodies | NATO, G7 and OPEC stay their own keys (displayed "Nato", "Opec"). EU-body principals match EU-keyed seeds at 0.5 coverage. |
| Target exclusion | Honoured by principal consumers. **Not honoured** by the consumers that use every mentioned entity (listed below the table). |
| `event_entities.actor_role` | **Write-only.** No reader. `RankingInput.actor_roles` is a name collision (office seniority). |
| Legacy `item_entities.role` / `event_entities.role` (SUBJECT/LOCATION, type-derived) | Still shown in the Event and Entity detail pages (`api/routes/events.py:113`, `web/templates/event_detail.html:94`), where a country acting is shown as LOCATION. It also duplicates `EventEntity` rows per role. |
| Lead vs secondary actor | Not native. The flat principal set fragments exact-set Situation creation ({Houthis, Saudi Arabia} vs {France, Houthis, Saudi Arabia}) and distorts coverage. |
| Freshness | Principals are recomputed for 3 days; Situation assignment is one-shot on the first signature; the ranking topic changes between runs (ranking before situations). |

Consumers that use every mentioned entity, so targets, places and outlets count as actors:
- **Situation fallback** when an event has no principals: every GPE/ORG/NORP mention, with coverage 1.0 and join
  0.8 (`processors/situations/store.py:77-80`).
- **Classifier:** `actors` / `countries` and the ACTORS_UNCLEAR check (`classification/base.py:45-55`,
  `rules.py:273-275`); the LLM classifier receives every detected entity (`llm_classifier.py:79-80`).
- **Flash briefing:** "ENTITIES INVOLVED" lists every item entity (`analysis/briefing.py:136-152`).
- **Graph:** co-occurrence edges over every `EventEntity` (`analysis/graph.py:69-81`).
- **Event detail API:** lists all entities with the legacy role and exposes neither `is_principal` nor
  `actor_role` (`api/routes/events.py:106-114`).
- **Event detail UI:** renders that list (`web/templates/event_detail.html:88-94`).

The owner-reviewed entity metrics hold at the entity layer. Downstream, three things are unguarded: the
state-level reduction, grouper decisions and UI projections. They reinterpret those entities with no gold.

---

## Invariant matrix

| # | Invariant | Status | Evidence |
|---|---|---|---|
| 1 | Raw evidence is reconstructable | PARTIAL | Rows are append-only with unique (source, external_id). Exceptions: fulltext overwrites `content` (`fulltext.py:737-739`); exact-hash copies from another outlet and same-source updates are dropped with no record (`dedup.py:99-115`, `pipeline.py:757-781`); webhook items skip processing |
| 2 | Provenance survives processing | PARTIAL | `source_id` and `url` are kept. Syndication and evidence role are computed at read time, never persisted (`provenance/resolve.py`). Translation is not persisted. GDELT collapses all outlets to one origin |
| 3 | Source identity ≠ endpoint | PARTIAL | Identity lives in `sources.yaml` (inventory only) and `provenance.yaml` origin. The DB `Source` is keyed by feed name, and endpoints are not persisted |
| 4 | Derivative evidence cannot fake independence | PARTIAL | Origin grouping holds (`confidence.py:184-194`, tested). CONFIRMED uses `high_rel_count` over *outlets* (`corroboration.py:205-212`). Silent fallback to outlet count (`:190-197`). Roundups and analysis count as independent; `url#0/#1` duplicates inflate item counts |
| 5 | Development = coherent action/change | FAIL | 24/48 to 4/16 mixed clusters measured; E2, E81, E17, SX E6/E9/E16/E22/E23 observed; persistence re-merges segmented halves |
| 6 | Single-source evidence cannot become a first-class Development | FAIL | No gate; INV E53, SX E17 exist and are ranked; flag only (`classification/base.py:37-38`) |
| 7 | Development IDs stable enough for references | PARTIAL | IDs are never deleted, but the referent drifts: overlap-merge via `.first()`, nested events (E49⊂E2), 24 items in two events |
| 8 | Reprocessing is historically attributable | FAIL | No run id, code SHA or config hash in production; mixed recompute windows (3 d / 7 d / all / frozen) |
| 9 | Canonical identity ≠ display form | PARTIAL | `canonical_name` doubles as display; canonical is first-seen per DB ("Donald J. Trump" vs "Donald Trump"); key display "Nato" |
| 10 | Fuzzy matching cannot create durable truth | PASS | Fuzzy is provisional and never stored (entity stage 1, gold-tested). Separately, even trusted alias appends are lost (bug) |
| 11 | Actor role ≠ entity type | PARTIAL | `actor_role` comes from the parse (gold-tested), but it has no consumer and the UI shows the type-derived legacy role |
| 12 | Targets are not principals | PASS | `principals.py:310` requires role actor; gold 0 target principals. The Situation fallback still uses targets when there are no principals (see #17) |
| 13 | Publishers are not actors | PASS | Media outlet rule (`actor_roles.py`); gold audit check 7 |
| 14 | Institution hierarchy is explicit | PASS | `config/institutions.yaml` with parents; `InstitutionRegistry.parents/top`. Downstream collapses it to the top parent (risk 8) |
| 15 | State/body representation is explicit and contextual | PARTIAL | `represents` covers ~15 people and is surface-dependent; top-parent reduction is unconditional, not contextual |
| 16 | Situation is persistent context | FAIL | Actor-set bucket with a staleness clock; no state model |
| 17 | Situation membership is explainable | FAIL | Reasons discarded (`store.py:113-118`); fallback on all mentions |
| 18 | Situation ID stable enough for follow/mute | PARTIAL | Slug is stable and never deleted. Seed rename orphans rows; auto-created can't be closed; meaning drifts |
| 19 | Historical membership can be reconstructed | PARTIAL | Membership never changes, so current = history, but there is no `assigned_at`, and member content changes are unversioned |
| 20 | Publication / ingestion / processing / change time are distinguishable | FAIL | `first_reported_at` is processing time; `published_at` is overloaded; no occurred time; no change times |
| 21 | New evidence ≠ reprocessing | FAIL | `last_updated_at` conflates them; no membership timestamp or run id |
| 22 | "What changed since T" supportable from data, not logs | FAIL | Overwrite semantics; no change log |
| 23 | Collection failures are visible | FAIL | RSS/Nitter `print` and return `[]` (`collectors/rss.py:40-42`); many collectors log at DEBUG under a hardcoded INFO level (`cli.py:131-134`); **outages become false signals**: OpenSky failure gives "only 0 commercial flights" (`infrastructure.py:418-457`), BGP failure gives ratio 0, HTTP failure gives "DOMAIN DOWN". Status is blind outside the daemon process |
| 24 | Processing is recoverable / idempotent | PARTIAL | Nothing deletes; stages recompute and heal. But `persist_clusters` depends on `.first()` order; relation confidence climbs on reruns (lost evidence append); poison items retry forever; the CLI `alerts` command advances daemon state |
| 25 | Concurrent DB behaviour is defined | PARTIAL | WAL, busy_timeout 30 s, an in-process RLock serialises tiers and alerts. Outside the lock: the briefing job and the API process writers (ingest has no savepoints). Network I/O (geocode, fulltext, LLM) runs while holding the write lock *(inferred)* |
| 26 | Missing NLP models fail visibly | PASS | `ner_status` in status, daemon startup and smoke (58682db). An English model missing entirely aborts the batch loudly |
| 27 | LLM output cannot silently become canonical truth | PARTIAL | Defaults are rules and arbiter `none`. When enabled, the LLM classifier writes `change_summary`, shown as FACT (`situation_views.py:66`), and arbiter choices become membership indistinguishable from rules |
| 28 | Persisted LLM output has provenance | PARTIAL | `classification_source = llm:<p>/<model>`. Briefing `model_used` is the provider or "default"; no prompt version or input ids anywhere; arbiter choice not recorded |
| 29 | High-risk identity logic has frozen benchmarks | PARTIAL | Entity gold and clustering windows are hash-frozen. **None** for Development identity across incremental runs, Situation identity or membership. Hold-out "run once" is advisory |
| 30 | Benchmark changes separable from implementation | PARTIAL | Gold, labels and items are in their own commits and hash-checked. Some entity feature commits also change the scorer and commit runs (75ae7b5, 7670cd1, 372e8dd, 7f77fd3, bf39b7a) |
| 31 | Critical future contracts have evaluation coverage | FAIL | None for Development/Situation identity stability, temporal or change correctness, alerts, fusion, briefing, dedup beyond hashing, or cross-language clustering |

Totals: 5 PASS, 16 PARTIAL, 10 FAIL, 0 UNKNOWN.

---

## Top structural risks

Every high or critical risk cites file, function and table, plus a concrete data example from the snapshot copies
(`lineage/`). Where none was observable, the table says so.

| # | Risk | Severity | Code evidence (file · function · table) | Data example | Why it matters | Affects | Order |
|---|---|---|---|---|---|---|---|
| 1 | Development persistence is overlap-merge, append-only, order-dependent (S1) | Critical | `processors/clustering.py` · `persist_clusters` (`:431-494`), `_find_overlapping_event` (`:548-557`, unordered `.first()`) · `event_items` (no UNIQUE, no index, `core/database.py:202-208`) | INV E1/E2 share 13 items; E49 ⊂ E2 (6/6); E45 ⊂ E18 (3/3); 24 items in two events | A reference to a Development can later point at other occurrences; segmentation cannot fix persisted events | references, follows, change history, corroboration, Situations | 2 |
| 2 | No run ledger, membership time or change log | Critical | no `pipeline_runs` table; `event_items` has no `added_at`/`run_id`; overwrites in `principals.py` · `mark_principal_actors` (`:381-384`), `pipeline.py` · corroboration loop (`:549-565`), `store.py` · `refresh_statuses` (`:136-141`) | 3 INV events have members fetched after their `last_updated_at` (near-dup path `pipeline.py:859-873`); no row anywhere records when a corroboration level or principal changed | "what changed", "new vs reprocessed" and audits are impossible from data | get_changes_since, last-seen, assistant explanations | 1 |
| 3 | Overloaded time fields (S3) | High | `clustering.py` · `persist_clusters` (`:472`, `first_reported_at=utcnow()`) · `events`; `collectors/adsb_tracks.py:358`, `infrastructure.py:204` (`published_at` = collection time) · `raw_items`; `api/situation_views.py:162` sorts the timeline by it | all 107 events; INV E1 created 09-25 09:44, earliest item 09-23 22:01 (mean +11 h, max +42 h); 57 sanctions rows with null `published_at`; OONI 2020-25, NVD 2000, CSIS 2016 dates; Council of the EU items ~1 h after fetch | Timelines, "since T" and ordering are wrong | timeline UI, changes-since, Situation clocks | 1 |
| 4 | Situation is an unexplained actor bucket (S2) | High | `situations/store.py` · `assign_situations` (`:98-118`), `_touch` (`:125-133`) · `events.situation_id`, `situations.updated_at`; `grouper.py` · `_score` (`:235-271`) | `china-united-states`: E11, E34 (pandas), E49, E25; `france-pope` auto-created for one visit, `updated_at` stuck at creation; situations 1, 6, 7 have members updated after `situations.updated_at` | Can't be the followed object or explain itself | follow/mute, get_situation_state | 3 |
| 5 | Confidence and alerts attach to storylines, not occurrences | High | `processors/corroboration.py` · `compute_corroboration_score` (`:176-212`: origins over all items; CONFIRMED via `high_rel_count` over outlets) · `events.corroboration_level`; `alerting/engine.py:142-172,233-251` | **Mixed Events rated CONFIRMED / C1:** INV E2 (32 items, Xi summit + Pope AI + Natixis), E38 (avalanche + Nepal floods), E54 (two rape cases in different countries), E12 (Poland air defence + Danish intel + steelmaker); SX E15 is half roundup; 28 of 82 INV events are CONFIRMED | Overstated confidence on mixed Events: the analytic core | briefings, alerts, ranking, assistant claims | 2 |
| 6 | Reprocessing unattributable | High | no model, config or code stamp on `events`, `event_entities`, `raw_items.embedding`; windows: `principals.py:84` (3 d), `development.py:36` (7 d), `pipeline.py:551` (all), `development.py:95` (frozen until touched) | INV ranked once (09-30 09:13): 75/82 events `stale`, 54 both `stale` and `new_development`; v3-DB principals on 96% of events vs 79% under current main code, and nothing records which logic produced the stored ones | Historical outputs can't be explained after any change | reproducibility, audits, LLM grounding | 1 |
| 7 | Silent collection failures and false signals | High | `collectors/rss.py:40-42` · `RSSCollector.collect` (print + `[]`); `collectors/infrastructure.py:418-457` (OpenSky failure → 0 counts → avoidance items), `:130-132` (BGP ratio 0), `:302-330` (HTTP failure → "DOMAIN DOWN"); `core/scheduler.py:124-142` (status in-process only), `:57,84-87` (no gap across restarts) | INV holds "FLIGHT AVOIDANCE: Black Sea – only 0 commercial flights" (the exact zero the failure path produces; cause not verified) and 8 "DOMAIN DOWN" items (cause not verified); fusion/I&W alerts 12-21 "Infrastructure Strike (70%)" repeated | False I&W/fusion inputs; outages invisible | alerts, fusion, trust | 0 |
| 8 | State-level top-parent reduction downstream | Medium | `processors/actors.py` · `ActorNormalizer.load` (`:56-70`, `reg.top()`); `situations/grouper.py:222-223`; `api/situation_views.py:123` | "Donald J. Trump" (multilingual canonical) keys to a person, not the US; INV E1 principals include both "xi" and "xi jinping" | Situations, UI and ranking hide the acting body and miss matches | Situation matching, actor activity | 3 |
| 9 | Persistence bugs losing writes (S4) | High | `processors/entity_resolver.py` · `_register_alias` (`:459-465`) · `entities.aliases`; `processors/relations.py` · `persist_relations` (`:399-403`) · `entity_relationships.evidence_item_ids`; `core/scheduler.py` · `_run_alert_job` (`:211-219`) · `alerts.delivered_via`; `alerting/fatigue.py:36-38` + `engine.py:139,186` (quiet hours) | reproduced in memory: an alias appended to a stored row is lost after commit; INV: 3 of 21 relationships at confidence 1.0 with one evidence item; `delivered_via` NULL on 232/232 alerts | In-memory and DB state diverge; resolution changes after a restart; alert delivery likely never works in the daemon *(inferred)* | entity resolution, alerts | 0 |
| 10 | Concurrency and backup procedure | Medium | `api/routes/ingest.py:51-74` (no savepoints, no lock); `core/scheduler.py:225-232` (briefing outside `DB_WRITE_LOCK`); network I/O inside write transactions in `geocoding.py:292-297`, `fulltext.py:737-739`, `development.py:110` *(inferred)*; no backup job | one demonstrated loss: 29 items to `database is locked` on 2026-09-29 06:02 UTC, fixed in-process (commit 8d2353d) | Data loss on crash; stalls | user-state writes from the UI, reliability | 1 |

No evidence of a SQLite capacity limit was found: 1335 items and 82 events over 5 days. Replacement is not
indicated.

---

## Hidden coupling

- **Ranking and Situations.** Ranking runs before Situations but uses `situation_id` as its topic
  (`development.py:163-167`). A new event's repeat/overshadow bucket changes on the next run.
- **Segmentation and NER.** Segmentation reads persisted place entities, so NER, resolver or demonym changes move
  clustering. This happened in entity stage 1 (Canadian); the entity work contained it with the frozen gate.
- **The near-duplicate link** attaches items straight to an event (`pipeline.py:859-873`). It bypasses
  segmentation, does not bump `last_updated_at` and adds no `event_entities`, so classification and principals
  never see the item.
- **Corroboration** rewrites every event on every run, so any provenance config change silently rewrites
  history.
- **The alert engine** recomputes I&W and fusion itself. The `alerts` CLI mutates the daemon's `state_snapshots`.
- **Three different Situation clocks:** `Situation.updated_at` (last assignment), the UI's `last_changed` (max of
  member `last_updated_at`) and dormancy (`updated_at`).
- **Classification** triggers on `last_updated_at > classified_at`, so reprocessing re-runs the classifier (and
  the LLM, if enabled).
- **Recompute windows** are inconsistent: principals 3 d, ranking 7 d, situations 7 d, corroboration all,
  clustering 48 h.
- **Duplicate evidence.** `url#0`/`url#1` BBC duplicates pass dedup and inflate event size; 13 pairs observed.
- **Migration numbering.** `feat/localhost-demo` also defines migration 4. `data/demo/osint-demo.db` records v4
  with the demo's semantics, so merged main would skip the entity migration on that file.

---

## Deterministic assistant-action readiness

| Action | Status | Why |
|---|---|---|
| `get_changes_since` | **BLOCKED BY SEMANTICS** | no membership time, change log or run ledger; "change" is undefined for overwritten fields |
| `get_situation_state` | **BLOCKED BY SEMANTICS** | a Situation has no state model; status is a staleness clock |
| `get_development_evidence` | NEEDS READ MODEL | `event_items`, `raw_items` and per-item provenance exist (`situation_views` computes them). Needs duplicate/overlap handling and persisted evidence roles to be trustworthy |
| `get_actor_activity` | NEEDS READ MODEL | principals per event exist, but are recomputed only in-window and reduced to the top parent in consumers. Needs an actor-level read model over `is_principal` + `actor_role` with the institution chain |
| `get_primary_sources` | NEEDS READ MODEL | provenance evidence type is computed at read time; primary roles are in `provenance.yaml`. Dedup-dropped carriers are lost |
| `search_developments` | NEEDS READ MODEL | no full-text index; frozen summaries; mixed events |
| `follow_situation` | NEEDS DATA MODEL | no user-state table; also gated on Situation semantics (above) |
| `mute_situation` | NEEDS DATA MODEL | same |

None is READY. These verdicts are **conditional on S1-S4**. Even the "NEEDS READ MODEL" actions return drifting
referents until S1 is resolved.

---

## Observability gaps

(GOOD / PARTIAL / BLIND per stage and signal.)

| Stage | Last run | Last success | Last failure | In / out | Reject reasons | Duration | Exceptions | Version |
|---|---|---|---|---|---|---|---|---|
| collectors | BLIND | PARTIAL (`inspect sources`) | PARTIAL / BLIND (stdout, DEBUG) | PARTIAL | BLIND | PARTIAL (> 60 s only) | PARTIAL (no traceback) | BLIND |
| dedup | BLIND | BLIND | BLIND | PARTIAL | BLIND | BLIND | PARTIAL | BLIND (embedding model not stamped) |
| NLP / entities | BLIND | BLIND | PARTIAL | PARTIAL | GOOD (`resolution_method/evidence`) | BLIND | PARTIAL | PARTIAL (`ner_status`, not stamped) |
| clustering / segmentation | PARTIAL (proxy) | BLIND | PARTIAL | PARTIAL (INFO) | PARTIAL (log only) | BLIND | PARTIAL | BLIND |
| principals | PARTIAL | BLIND | PARTIAL | PARTIAL | BLIND | BLIND | PARTIAL | BLIND |
| classification | GOOD | GOOD | PARTIAL | PARTIAL | PARTIAL | BLIND | PARTIAL | GOOD (`classification_source`) |
| corroboration | BLIND | BLIND | PARTIAL (silent fallback) | PARTIAL | PARTIAL | BLIND | PARTIAL | BLIND |
| situations | PARTIAL | BLIND | PARTIAL | PARTIAL | BLIND (reasons discarded) | BLIND | PARTIAL | BLIND |
| ranking | GOOD | GOOD | PARTIAL | PARTIAL | GOOD (`rank_reasons`) | BLIND | PARTIAL | BLIND |
| I&W / fusion | BLIND | BLIND | PARTIAL | PARTIAL | BLIND | BLIND | PARTIAL | BLIND |
| alerts / delivery | PARTIAL / BLIND | BLIND | PARTIAL | PARTIAL / BLIND | BLIND (suppression at DEBUG) | BLIND | PARTIAL | n/a |
| briefings / LLM | GOOD | GOOD | PARTIAL | PARTIAL | n/a | BLIND | PARTIAL | BLIND (`model_used` wrong) |
| daemon / tiers | BLIND out of process | BLIND | PARTIAL | PARTIAL | n/a | BLIND | PARTIAL (no `exc_info`) | n/a |

**Structural gaps:**
- no log file handler;
- `status` and `/api/daemon/status` read in-process state, so they always show no jobs;
- restarts and crashes leave no gap record (`scheduler.py:57,84-87`);
- a hang inside the write lock blocks every tier while the gap check stays silent.

---

## Evaluation gaps

| Area | Coverage |
|---|---|
| Development identity across incremental runs | **none** (the replay is one-shot) |
| Situation identity / membership stability | **none** (idempotence test only) |
| Situation grouping quality | one 1-day review, no gold |
| Corroboration / source independence | unit tests only, no benchmark |
| Cross-language clustering | **none** (windows are English) |
| Temporal / change correctness | a few unit tests, no benchmark |
| Ranking | unit tests, no gold |
| Alerts, fusion, briefing, fulltext, relations, ingest/webhook, SSE | **no tests** |
| Dedup | 3 hash tests |
| Entity / roles | owner-reviewed gold (25 Devs, it/es tiny), no hold-out |
| Clustering / segmentation | 9 frozen windows; LLM-labelled, not human; hold-out re-run more than once |

---

## Stable contracts (safe to build against)

1. **`raw_items`** as append-only evidence with unique (source_id, external_id); `fetched_at` as ingestion time.
2. **Entity layer:** resolver trust model (no durable fuzzy truth), `item_entities.resolution_method/evidence`,
   institution registry with parents, `development_actors` as a pure function, the frozen owner-reviewed gold and
   audit, and NER status diagnostics.
3. **Provenance origin grouping** as a pure, tested function (`provenance/resolve.py`, `confidence.py`), used at
   read time.
4. **Structured/narrative partition** (`event_grouping.partition`): sensors are never text-clustered with news.
5. **The migration runner:** versioned, per-migration transactions, pre-migration backup.
6. **Frozen benchmark harnesses** (clustering windows, entity gold) and the separate-commit convention.
7. **`segment()`** as a pure function over a batch, whose compatibility logic is benchmarked.

## Contracts that must change first

1. **Development persistence:**
   - a deterministic reconciliation of new clusters to existing events, with no `.first()` and no silent double
     membership;
   - UNIQUE(event, item);
   - membership `added_at` / `run_id`;
   - lineage records if an event is ever split or merged.
2. **Time:** earliest-publication / occurred time per Development, separate from creation time;
   `published_at` semantics per source class.
3. **The run ledger** and version stamps (code SHA, config hash, model names) on derived outputs.
4. **The Situation assignment record** (reasons, candidates, rule version, `assigned_at`), status history, and a
   single Situation activity clock.
5. **An append-only change log** for Development and Situation fields.
6. **Identity anchors:**
   - future user state and assistant references key on `situations.id` / `events.id`, never on slug, title or
     `canonical_name`;
   - Source identity gets a stable key (the `sources.yaml` identity) separate from the feed display name;
   - principal links join by entity id, not surface name, before follows depend on actor sets.

---

## Recommended engineering sequence

Constraints on every phase:
- the frozen clustering benchmark, entity gold and segmentation benchmark must stay unchanged unless a change is
  the phase's stated purpose;
- the Situation holdout (`feat/situation-coverage`) stays untouched until its window closes on
  2026-10-03 12:00 UTC;
- every migration after 4 must account for `feat/localhost-demo`'s colliding migration 4.

### Phase 0: foundation blockers (correctness, no semantic change)
- **Prerequisite:** none.
- **Scope:**
  - persist JSON mutations (aliases, relation evidence);
  - alert dispatch within a live session, plus persisting `delivered_via`;
  - quiet hours must not advance state without recording the suppressed transition;
  - collector failures must never emit signals (OpenSky / BGP / DNS HTTP-only paths), and must surface in a
    per-collector status;
  - a log file handler, with `log_level` honoured;
  - traceback on tier failure;
  - a gap record across daemon restarts (persisted last tick).
- **Gate:** new unit tests for each bug; entity, clustering and segmentation benchmarks identical; smoke passes.
- **Must remain unchanged:** clustering, segmentation, entity outputs, ranking.

### Phase 1: run ledger and temporal primitives
- **Prerequisite:** Phase 0.
- **Scope:** migration 5 adds:
  - `pipeline_runs` (tier, start/end, stage status and counts, code SHA, config hash, model names);
  - `event_items.added_at` + `run_id` + UNIQUE(event, item);
  - Development `earliest_published_at` (derived) next to the existing creation time. Keep the column name
    change for later, or alias it in the read model.

  It also documents `published_at` semantics per source class. Nothing reads these fields for decisions yet.
- **Gate:**
  - a replay of two frozen windows as two incremental runs distinguishes new-evidence from re-clustered
    memberships;
  - benchmarks identical;
  - the migration round-trips on a copy of `data/osint.db` (copy only).
- **Must remain unchanged:** all derived outputs.

### Phase 2: Development identity contract
- **Prerequisite:** Phase 1 (membership time and runs make the change measurable).
- **Scope:**
  - define and implement cluster→event reconciliation: deterministic best-overlap, no double membership, and an
    explicit lineage row when a segmented event splits;
  - decide single-source policy (hold back vs flag);
  - exclude roundup/rolling items from corroboration and from summary selection (the diagnosis rule);
  - use a summary refresh policy.
- **Gate:**
  - a new frozen **incremental Development-identity benchmark** (replay windows tick by tick; measure ID stability
    and mixed-event rate) with human-checked labels;
  - the clustering benchmark SAME recall no worse, and UNRELATED/RELATED links no worse;
  - entity gold unchanged.
- **Must remain unchanged:** the entity layer, the Situation grouper.

### Phase 3: Situation state semantics
- **Prerequisite:** Phase 2, plus the holdout closed and reported.
- **Scope:**
  - decide what a Situation *is* (a state with defined variables vs a curated bucket);
  - persist assignment decisions (`situation_memberships` with reasons, candidates, rule version, run);
  - status history;
  - one activity clock;
  - close and rename operations for auto-created Situations;
  - contextual actor reduction (institution → state only where the Situation is state-level);
  - leader coverage via `represents` or entity links, not surface forms;
  - fix the missing-signal score inflation.
- **Gate:**
  - a Situation gold set (membership plus non-membership, owner-reviewed);
  - membership explainable for 100% of assignments;
  - the holdout protocol respected;
  - entity gold unchanged.
- **Must remain unchanged:** Development identity (Phase 2 contract), entity layer.

### Phase 4: change history
- **Prerequisite:** Phases 1-3.
- **Scope:**
  - an append-only change log for Development fields (membership, corroboration level, principals,
    classification) and Situation fields (membership, status, title);
  - `get_changes_since(T)` as a read model over the log, never over logs or heuristics.
- **Gate:** a scripted scenario suite (new Development, new evidence, new primary source, corroboration upgrade,
  principal change, status change, pure reprocessing ⇒ no change) passes on replayed windows.
- **Must remain unchanged:** derived decision logic.

### Phase 5: user follow / last-seen state
- **Prerequisite:** Phase 4.
- **Scope:**
  - `user_observations` (object, last_seen_at) and follows/mutes on Situation IDs;
  - writes serialised with the daemon (defined API-process write path).
- **Gate:**
  - "since last seen" equals `get_changes_since(last_seen)` on the scenario suite;
  - concurrency test with daemon + API writing.
- **Must remain unchanged:** pipeline outputs.

### Phase 6: deterministic action API
- **Prerequisite:** Phases 4-5.
- **Scope:** the eight actions above as typed, read-only (except follow/mute) functions over read models, each
  returning evidence ids.
- **Gate:** per-action contract tests on frozen fixtures; results reproducible with the same data and version
  stamps.
- **Must remain unchanged:** read models only; no new inference.

### Phase 7: command palette
- **Prerequisite:** Phase 6.
- **Scope:** a UI over the action API only.
- **Gate:** every palette command maps to one action and cites evidence ids.
- **Must remain unchanged:** actions.

### Phase 8: LLM orchestration
- **Prerequisite:** Phases 6-7.
- **Scope:**
  - the LLM calls deterministic actions only;
  - every persisted LLM output goes to an `llm_outputs` table with model, prompt version, input ids and run;
  - generated text is labelled and never written into canonical fields;
  - the existing LLM classifier `change_summary` and arbiter paths are brought under the same rule.
- **Gate:**
  - no canonical field is writable by an LLM (test);
  - outputs are reproducible from the stored inputs.
- **Must remain unchanged:** canonical Development, Situation and entity contracts.

---

## Build / no-build gate

**Situation state + change history (Phases 3-4): NO-BUILD yet.**
- It is **not** safe to start them immediately after this audit.
- Both would persist history *about* Developments whose referent is not pinned (S1) and whose times are
  processing times (S3).
- They would build on Situation memberships that carry no decision record (S2), in a DB that silently loses some
  writes (S4).
- A change log built now would record reprocessing as change, and would have to be migrated or discarded once
  the Development contract is fixed.

**What must land first, in order:**
1. **Phase 0 (S4 + visibility):** the lost-write fixes (JSON mutation, alert session, `delivered_via`, quiet
   hours) and the collector false-signal and visibility fixes. These change no Development or Situation behaviour.
2. **Phase 1 (S3):** run ledger, membership `added_at`/`run_id` with UNIQUE(event, item), and Development
   publication-time fields.
3. **Phase 2 (S1):** the Development reconciliation contract, gated by a new incremental identity benchmark.

**When the gate opens.** Phases 3-4 may begin when Phase 2's gate has passed and the Situation holdout (closes
2026-10-03 12:00 UTC) has been reported. Phase 3 then resolves S2 itself (persisted assignment decisions) before
Phase 4 records history on top of it.

**Allowed now, in parallel.** Phases 0 and 1 may start immediately after this audit. Phase 1's migration 5 must
account for `feat/localhost-demo`'s colliding migration 4.

## Source count and modality summary

- **Code:** osint_monitor/ at f7b01d5, traced by five read-only passes plus my own spot checks.
- **Data:** two 2026-09-30 snapshot copies (schema v3, 1895 items, 107 events, 12 situations; news, institutional,
  multilingual it/es, sanctions, ADS-B, seismic, OONI, NVD), sampled with seed 20261001 (`lineage/`).
- **Evaluations read:** clustering (diagnosis, segmentation compatibility, phase C, recall), situations
  2026-09-25, and entities (foundation final, owner rescore).
- **Not covered:** the live daemon DB and `data/osint.db`, which were not opened; a run of the daemon, API or
  alert delivery. Items marked *(inferred)* are from code only.
