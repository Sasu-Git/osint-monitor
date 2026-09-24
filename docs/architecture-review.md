# Architecture Review — Personal Situational-Awareness Fork

**Date:** 2026-09-24
**Scope:** Prompt 1 of the fork development chain. Review only; no code changed.
**Baseline commit:** `168abd7`

Target information hierarchy: **Situation → Development → Evidence / Source Items**.
Target output per development: **FACT / ASSESSMENT / WATCH** (prediction optional).

---

## 1. Summary

The storage layer, deduplication, embeddings, spaCy NER, entity resolution, LLM provider abstraction, collector base class, alert channels, and pause mechanism are a good foundation and should be reused.

Four things conflict with the new product:

1. **Development identity is unstable.** `cluster_recent_items` re-runs HDBSCAN over a 48h window every tick; `_find_overlapping_event` merges each cluster into the first existing event sharing any item. Events chain-merge and never split. `event_type` is always `None`. The unused `extract_event_triples` / `EVENT_VERB_MAP` in `processors/nlp.py` is a ready seed for a rule-based classifier.
2. **Ranking is a fake-precision weighted score.** `processors/scoring.py` combines keyword/entity/credibility/novelty with arbitrary weights (0.30/0.20/0.25/0.25). It is computed and discarded in `pipeline.py` (`_process_single_item`), then recomputed per item in clustering — reloading `sources.yaml` on every call.
3. **Source reliability is effectively broken.** `ensure_source` never sets `Source.category`, and YAML categories (`us_gov`, `news`, `analysis`) do not match the keys corroboration expects (`official_gov`, `wire_service`, …). Result: every RSS source grades **C** — Defense.gov equals a blog. "Independent" means distinct `source_id`, so syndicated wire copies count as independent confirmation.
4. **No Situation layer.** Only a keyword-derived `region` string exists.

Everything else is extension, disabling, or separating mixed concerns.

**Documentation conflict:** `CLAUDE.md` and `AGENTS.md` define the project as a *predictive* system with mandatory report archiving. The new intent (situational awareness, prediction optional) conflicts. Both should be rewritten early in the chain.

---

## 2. Retain unchanged

| Area | Files | Reason |
|---|---|---|
| DB engine/session, SQLite WAL | `core/database.py` (engine section) | Simple, works |
| `Source`, `RawItem`, `Entity`, `ItemEntity`, `Claim`, `Alert`, `Briefing`, `StateSnapshot` tables | `core/database.py` | Map directly to the evidence layer |
| Deduplication (exact hash → semantic → source-aware) | `processors/dedup.py` | Correct idea: near-duplicate from a different source is kept as evidence |
| Embeddings | `processors/embeddings.py` | Small, swappable |
| NER | `processors/nlp.py` (`extract_entities`) | Adequate |
| LLM provider ABC + OpenAI/Anthropic/Ollama/Gemini | `analysis/llm.py` | ABC justified: four real implementations |
| `BaseCollector`, RSS, sanctions | `collectors/base.py`, `rss.py`, `sanctions.py` | ABC justified: ~30 implementations |
| Alert channels, fatigue, state tracker | `alerting/channels.py`, `fatigue.py`, `state.py` | Clean and small |
| Pause flag + APScheduler tiers | `core/scheduler.py` | Works; relocate into the serve process (see §8) |
| Geocoding, SSE stream, CLI skeleton | `processors/geocoding.py`, `api/websocket.py`, `cli.py` | Fine |

---

## 3. Extend

| Module | Extension |
|---|---|
| `Event` model | Keep table/class name `events`/`Event`; call it **Development** in UI/API (avoid rename migration). Add: `development_type`, `is_action`, `classification_reason`, `rank_tier` (major/notable/routine), `rank_reasons` (JSON list of plain-language strings), `situation_id`, `headline`, `fact_md`, `assessment_md`, `watch_md`, `llm_model`, `status` (active/merged/dismissed), `merged_into_id`. |
| `EventItem` | Add unique constraint `(event_id, item_id)` (currently missing). Add `evidence_role` (primary / independent / derivative / commentary). |
| `Source` | Add `reliability` (explicit A–F in YAML), `origin_group` (syndicated copies count once), `role` (official / wire / media / analysis / social). Sync from YAML on every start — today credibility is only set at creation. |
| `SourceConfig` / `sources.yaml` | Fields above, plus a generic `collectors:` list (`class`, `tier`, `enabled`, `params`). |
| `EntityResolver` | Move hardcoded `_COREFERENCE_GROUPS` and `KNOWN_PERSONS` to `entities.yaml`. Cache `normalise(alias)` — the fuzzy loop re-normalises every alias for every mention. |
| `LLMProvider` | Per-task provider/model from config (`llm.tasks.classify`, `.summarize`, `.briefing`). Remove hardcoded model names in constructors. Add timeout + one retry. Record the actual model in `model_used` (currently stores provider name). |
| `processors/language.py` | Remove hardcoded `provider="openai"`. Disable translation by default (one LLM call per non-English item). |
| Corroboration | Grades from `SourceEvaluator`; independence by `origin_group`; recompute only events touched this tick (currently rescans all events every tick). |
| Briefing | Build context from ranked developments grouped by situation, not 200 raw items with severity numbers. FACT / ASSESSMENT / WATCH output. Prompts moved to `config/prompts/*.md`. |
| `init_db` migrations | Replace swallow-all-exceptions `ALTER` list with ordered migrations keyed on `PRAGMA user_version`. Alembic is a declared but unused dependency — adopt or drop (recommend drop). |

---

## 4. Replace

Only two replacements are warranted:

1. **Batch HDBSCAN + overlap-merge → incremental assignment.** A new item joins the nearest active development within a time window if similarity ≥ τ **and** at least one shared entity; otherwise it forms a candidate development. Development IDs become stable across ticks. Keep HDBSCAN as an optional periodic re-seed / merge-suggestion pass, switched from the `hdbscan` package to `sklearn.cluster.HDBSCAN` (scikit-learn is already pulled in by sentence-transformers; `hdbscan` is a build problem on Windows / Python 3.14).
2. **`scoring.py` weighted severity → policy-driven ranker** producing an ordinal tier plus explicit reasons. Keep writing the `severity` column during transition for API compatibility; remove it from the UI.

---

## 5. Abstractions — which are justified

| Candidate | Verdict | Rationale |
|---|---|---|
| **Collector** | Keep ABC; add config-driven registry | Many implementations. Replace the `COLLECTOR_TIERS` dict and the try/except import wall in `build_collectors` with loading from config (`class` path, `tier`, `enabled`). |
| **LLMProvider** | Keep ABC | Four implementations exist. |
| **DevelopmentClassifier** | Protocol | Two real implementations from day one: rule-based (verb map + YAML patterns; default, free) and LLM-based (optional). Prime experimentation point. |
| **DevelopmentRanker** | Protocol, one implementation (`PolicyRanker` reading `config/ranking.yaml`) | Explicit goal to experiment with ranking policies; LLM re-ranker is a likely second implementation. Most variation lives in YAML. |
| **SituationGrouper** | Light Protocol, ship one implementation | Start with configured grouping (YAML watchlist of situations: entities + keywords). Automatic entity co-occurrence grouping is a likely second. |
| **SourceEvaluator** | No base class | Variation is data, not code. One concrete module extracted from `corroboration.py`. |
| **BriefingGenerator** | No base class | One function: developments + prompt template + LLM. A no-LLM markdown digest is a separate function, not a subclass. |
| **Pipeline stage** | No class hierarchy | Plain functions `(session, ctx) -> stats` in a dict registry; order and enablement in YAML. Replaces the hardcoded sequence in `run_post_processing` and makes disabling I&W/fusion trivial. |

---

## 6. Mixed responsibilities

- **`processors/pipeline.py`** — collector construction, tier table, source upsert, per-item processing, post-processing orchestration, console printing. Split into `collectors/registry.py`, `processors/ingest.py` (store + NLP), and `processors/pipeline.py` (stage runner only). Latent bug: `import os` sits inside the govint `try` block but `os` is used in later blocks.
- **Duplicated ingestion** — `api/routes/ingest.py` and the `/api/intel/webhook` route each re-implement part of `_process_single_item`. Both should call `processors/ingest.py`.
- **`processors/clustering.py`** — clustering + severity scoring + region assignment + persistence + entity propagation + claim linking.
- **`processors/corroboration.py`** — hardcoded reliability policy + event scoring + claim grouping + embedding-based disagreement.
- **`analysis/briefing.py`** — querying + context formatting + prompts + persistence + an ACH function duplicating `analysis/ach.py`.
- **`analysis/export.py`** — CSV export + LLM-written CIR/IIR reports + webhook model.
- **`api/routes/intelligence.py`** — ~30 endpoints across ~10 unrelated features in one router.
- **Templates** — HTMX is loaded but pages use `fetch()` + `innerHTML`. Presentation logic (`severityBadge`, `statusBadgeFromCorroboration`) lives in `base.html` JS. All libraries load from unpkg/jsdelivr CDNs (no offline use).
- **Config drift** — `openai_model` defaults to `gpt-4o-mini` while docs say gpt-5-mini; keyword lists duplicated between `scoring.py` and `sources.yaml: alert_keywords`.
- **Scheduler + SSE** — `broadcast()` is an in-process bus; when the daemon runs as a separate process, pushes never reach `serve`.

---

## 7. Disable by default (keep, behind `features:` flags)

| Group | Modules |
|---|---|
| Tracking sensors | `adsb.py`, `adsb_tracks.py`, `ais.py` (not currently wired) |
| Infrastructure / cyber | `infrastructure.py` (BGP, DNS, flight routes, seismic explosion), `spectrum.py` (Wikipedia edits, cables, satellites, RIPE), NVD in `sigint.py`, OONI |
| Environmental / US-centric | FIRMS, USGS, SEC, SAM, COMTRADE, Congress, NOTAM, `DocumentCollector` (Federal Register) |
| Finance | `financial.py`, `finance_bridge.py` (depends on sibling repo), `CurrencyCollector` |
| Social scraping | Nitter (instances largely dead), `browser.py` X collector (Playwright + Chrome profile), telegram / twitter |
| Heavy enrichment | Playwright fallback in `fulltext.py`, stance NLI cross-encoder, `imint.py` (CLIP), LLM relation extraction, LLM translation |
| Analytics | ACH; I&W and `estimate_escalation_probability` (sigmoid "probability" — exactly the fake precision to avoid); fusion + signal gaps; coordination detection; graph analytics; STIX; temporal "historical parallels"; trend-anomaly alerts |
| Infrastructure | `core/tasks.py` (Celery), `docker-compose.yml` (Postgres/Redis), pgvector path |

**Default on:** RSS (expanded with primary sources: foreign-ministry/government press releases, UN, EU, NATO), OFAC/UN sanctions, travel advisories, GDELT (optional), UNHCR/IAEA (optional), full-text enrichment without Playwright, desktop alerts limited to new major-tier developments.

---

## 8. Smallest viable architecture

```
collectors/registry.py       build from sources.yaml (class, tier, enabled, params)
        │  RawItemModel
        ▼
processors/ingest.py         dedup → store RawItem → Source sync (sources.py) → language detect
        ▼
nlp.py + entity_resolver.py  entities (unchanged; coreference data → entities.yaml)
        ▼
processors/clustering.py     incremental assign → Development (Event) + EventItem.evidence_role
        ▼
processors/classify.py       DevelopmentClassifier: RuleClassifier (default) | LLMClassifier
                             → development_type, is_action, classification_reason
        ▼
processors/corroboration.py  via sources.py → independent count (origin_group), Admiralty, level
        ▼
processors/ranking.py        PolicyRanker(config/ranking.yaml) → rank_tier + rank_reasons
        ▼
processors/situations.py     ConfiguredSituationGrouper(config/situations.yaml) → situation_id
        ▼
analysis/summarize.py        LLM FACT/ASSESSMENT/WATCH for major/notable tiers only, cached on Event
analysis/briefing.py         situations → top developments → FACT/ASSESSMENT/WATCH
api/ + web/templates         Situation → Development → Evidence (HTMX partials)
```

### Example `config/ranking.yaml` (ordinal, no user-facing numbers)

```yaml
type_priority:
  military_action: major
  agreement: major
  sanctions: major
  meeting: notable
  policy_change: notable
  statement: routine
  commentary: routine
promote:
  - when: {independent_sources_gte: 3}
    reason: "Reported by 3+ independent outlets"
  - when: {has_primary_source: true}
    reason: "Confirmed by an official/primary source"
  - when: {senior_actor: true, type: meeting}
    reason: "In-person meeting of senior representatives"
demote:
  - when: {role_only: [commentary, analysis]}
    reason: "Commentary only, no reported action"
```

This makes "meeting outranks statement" the default without making it a hard rule: ceasefires (`agreement`) and sanctions packages start at `major`.

### Pipeline stages

```yaml
pipeline:
  stages: [cluster, classify, corroborate, rank, group, geocode]
  optional_stages: [iw, fusion, relations]   # run only if the matching features.* flag is on
```

### Operations

- `python main.py run` — FastAPI with embedded scheduler (single process; fixes SSE gap). Keep `daemon` / `serve` for power use.
- `python main.py backup` — SQLite online-backup API to `data/backups/`.
- `python main.py doctor` — checks spaCy model, embedder, API keys, feed reachability.
- `pyproject.toml` as the single dependency source, with extras `[browser]`, `[anthropic]`, `[gemini]`, `[advanced]`, `[dev]`. `requirements.txt` currently duplicates it.
- Replace bash-only `run.sh` with CLI subcommands (Windows-friendly).

---

## 9. Dependency rules

```
core (config, database, models)    ← imported by everything; imports nothing internal
collectors/*                       → core.models only
processors/sources.py              → core.config
processors/ingest.py               → dedup, embeddings, nlp, entity_resolver, sources
processors/{clustering, classify, corroboration, ranking, situations}
                                   → core + sources; classify may use analysis.llm
processors/pipeline.py             → stage registry only
analysis/{summarize, briefing}     → analysis.llm, core
analysis/{ach, indicators, fusion, coordination, graph, stix_export, temporal}   [optional]
                                   → core; never imported by the core pipeline except
                                     through the stage registry when features.* is enabled
api/routes/*                       → read-side queries + pipeline triggers
web/templates                      → API HTML partials only
```

---

## 10. Migration risks

1. **Development identity changes.** Incremental clustering will not reproduce existing HDBSCAN events. Provide `rebuild-developments --days N` or start with a fresh DB.
2. **Admiralty ratings shift** once the source-category bug is fixed. Correct behaviour, but it will look like a regression.
3. **Silent migration failures.** Current `init_db` swallows every exception. Fix before adding columns.
4. **Alert engine depends on I&W/fusion state.** Disabling them silences tier-1/tier-3 alerts. Replace with "new major-tier development" and "development promoted" alerts.
5. **Severity ordering is everywhere** — dashboard, briefing, CSV export, CLI `export`. Switch together.
6. **LLM cost.** Gate classification/summaries to top tiers and cache results.
7. **Environment.** Under Python 3.14, pytest in the user site is broken (`ImportError: cannot import name '__version__' from '_pytest'`); hdbscan/spaCy wheels may be missing. Pin a 3.11/3.12 venv.
8. **Docs contradict the product** — `CLAUDE.md`, `AGENTS.md`, `README.md`.
9. **Two-process SQLite** is fine under WAL, but single-process `run` avoids the SSE gap.

---

## 11. Tests

**Delete / trim:** `tests/test_models.py` (Pydantic defaults); most of `tests/test_scoring.py` (tests weights being removed); keep `tests/test_vessel_parser.py` only while AIS exists.
**Keep:** dedup, entity resolver, geocoding, stance.
**Add (behavioural; deterministic fake embedder, stubbed NER):**

- Ingest: 3 items from 2 outlets → 1 development with 2 independent sources.
- Clustering stability: an item arriving next tick joins the same development ID.
- Syndication: two items sharing an `origin_group` count as 1 source.
- Classifier: "X met Y in Z" → `meeting`; "OFAC designates…" → `sanctions`.
- Ranker: meeting > statement; ceasefire > meeting; commentary-only demoted.
- Situation grouping from YAML.
- One API smoke test per primary page.

Make embedder and NER injectable as function parameters with defaults — no DI framework.

---

## 12. Files likely to change

**Modify**
`osint_monitor/core/database.py`, `core/config.py`, `core/scheduler.py`, `processors/pipeline.py`, `processors/clustering.py`, `processors/corroboration.py`, `processors/entity_resolver.py`, `processors/language.py`, `analysis/llm.py`, `analysis/briefing.py`, `alerting/engine.py`, `api/app.py`, `api/routes/events.py`, `api/routes/ingest.py`, `api/routes/intelligence.py` (split), `api/routes/briefings.py`, `cli.py`, `web/templates/base.html`, `dashboard.html`, `events.html`, `event_detail.html`, `briefings.html`, `config/sources.yaml`, `config/entities.yaml`, `pyproject.toml`, `requirements.txt`, `README.md`, `CLAUDE.md`, `AGENTS.md`, `tests/conftest.py`, `tests/test_scoring.py`

**New**
`collectors/registry.py`, `processors/ingest.py`, `processors/sources.py`, `processors/classify.py`, `processors/ranking.py`, `processors/situations.py`, `analysis/summarize.py`, `core/migrations.py`, `api/routes/situations.py`, `web/templates/situations.html`, `web/templates/situation_detail.html`, `web/templates/partials/*`, `config/ranking.yaml`, `config/situations.yaml`, `config/development_types.yaml`, `config/features.yaml` (or a block in `sources.yaml`), `config/prompts/*.md`, tests for ingest / clustering / classify / rank / situations

**Deprecate (keep behind flags)**
`processors/scoring.py`, `core/tasks.py`, `docker-compose.yml`, `run.sh`, `analysis/indicators.py` (escalation probability), `analysis/fusion.py`, `analysis/stix_export.py`
