# Situational-awareness workspace

Frontend milestone, branch `feat/sa-workspace` (base `adacb83`). UI and presentation only. It reads the
accepted backend state and adds personal-priority state; it does not change how Developments, Situations,
clustering, segmentation, entity resolution, cross-language identity, relations, alerting or collectors behave.

Screenshots (live-database snapshot of 2026-10-27, demo priorities: China and Ukraine HIGH, Russia LOW,
Military HIGH, Economic MUTED) are in [`screenshots/`](screenshots/):

| | |
|---|---|
| Main workspace (Today) | `01-main-workspace.png` |
| World map with a country filter and a Development preview | `02-world-map.png` |
| Priority panel | `03-priority-panel.png` |
| Development detail and evidence | `04-development-detail.png` |
| Situation view | `05-situation-view.png` |
| Phone width (390 px) | `06-narrow-phone.png` |

## Information architecture

`Situation → Development → Evidence`, with four entries in the top navigation:

| Nav | Route | What it is |
|---|---|---|
| Today | `/` | The workspace: filter and priority rail, map, Development feed, context rail |
| Map | `/map` | The same workspace with a taller map. One page, not a second screen |
| Situations | `/situations`, `/situations/{slug}` | Situation list; a Situation's timeline, latest Development, map and status |
| Priorities | `/priorities` | The priority panel on its own page, with the rules explained |

A Development opens at `/developments/{id}` (Development, then Evidence). A map marker opens a preview in the
context rail (`/developments/{id}/preview`), which links to the full page.

The workspace answers, per card: what changed (title, summary, New / Updated), where (location),
why it is relevant to me (priority reason, "Involves …"), what supports it (confidence, independent sources,
ranking reasons) and which Situation it belongs to.

| Column (desktop) | Width | Content |
|---|---|---|
| Left rail | 280 px (about 17%) | Filters (period, country, topic, Development type, confidence, lifecycle, Situation, show muted); My priorities |
| Centre | the rest (about 60%) | Map (44% of the viewport height, 68% on `/map`), then the feed |
| Right rail | 320 px (about 20%) | Preview of a clicked marker; the selected Situation or country; "In this period" counts; Situations that changed |

## One selection, three views

The feed, the map and the context rail are built from one selection (`api/workspace_views.select`):
Today's corroborated Developments updated in the window (at least two independent sources, unchanged rule),
in the pipeline's ranking order, filtered, then ordered by personal priority. The filter form in the left
rail is the single source of truth:

- changing a filter swaps the feed with HTMX (`hx-get`, URL pushed) and the context rail out of band;
- after every feed swap the map reloads its GeoJSON from the same form;
- clicking a country on the map sets the form's country field and fires the same change;
- changing a priority returns the updated panel with `HX-Trigger: priorities-changed`, which re-runs the form,
  so the feed reorders and the map recolours at once;
- hovering a feed card outlines its marker; hovering a Situation in the context rail outlines that Situation's markers.

Periods: 24 h, 72 h, 7 d, ending at the newest collected Development (as Today did), not the wall clock.

## Map semantics

MapLibre GL JS 4.7.1 (unpkg), no tile service: the basemap is Natural Earth 1:110m country outlines served
from `/static/geo/countries.geojson`; cluster labels use the MapLibre demo glyphs.

- **Markers** are Developments whose stored coordinates pass the placement check (below). Low zoom clusters them;
  clicking a cluster zooms in; a cluster holding a HIGH item has an amber outline.
- **Marker style**: HIGH large amber, NORMAL blue, LOW small grey, MUTED (only with "Show muted") dark.
  A hollow ring means the stored location is a whole country (the point is a country centroid, not a place).
- **Hover** shows title, time, place, principal actors, Situation and independent-source count.
- **Click a marker** opens the preview in the context rail. **Click a country** filters to Developments that concern
  it; click it again (or the × in the rail) to clear.

**Event geography and actor relevance are separate.** Each card shows:

- *Location*: where it happened, from the stored coordinates and place name. "Genève, Switzerland".
- *Involves*: the states its principal actors act for, from the existing actor normaliser (`Xi → China`).
  "Involves China, United States".

A US–China meeting in Geneva is placed in Switzerland and concerns Switzerland (location), the US and China
(actors). The country filter and country priorities match either role, and the reason says which:
`HIGH country: China (actor)`.

### Placement check: no fabricated or contradicted coordinates

The pipeline geocodes a Development's most-mentioned place name through Nominatim and stores the first result.
On the live snapshot that result is sometimes another place of the same name: "Gaza" in Mozambique
(14 Developments), "West Bank" in Minneapolis, a Washington story stored in China. The workspace never invents a
coordinate and never moves one. It shows a stored point only when it agrees with the Development's own reports
(`api/geo.placement`):

1. The country the point lies in (Natural Earth 1:50m outlines; a coastal point within about 15 km of exactly one
   country takes that country) must be the country of the most-mentioned place, as the existing gazetteer
   (`config/geography.yaml`) resolves it (Gaza → Palestine).
2. If the gazetteer knows none of the most-mentioned places, the country of any mentioned place it knows will do.
3. A whole-country point of an archipelago that falls at sea (Indonesia, Philippines) is kept when it lies within
   that one country's extent.
4. Otherwise there is no marker: the Development stays in the feed with "No confirmed location" (or the mentioned
   country, "not on map"), and the detail page says why ("stored point lies in Mozambique, the reports mention Palestine").

On the 2026-10-27 snapshot: 992 corroborated Developments, 821 mapped (83%), 111 contradicted, 29 unconfirmed,
22 without coordinates, 9 at sea. Stored coordinates are not changed; the check runs at read time.

## Priority semantics

Personal priority is presentation state, not an intelligence score.

| Level | Effect |
|---|---|
| HIGH | Listed before everything else; amber edge on the card and amber marker; reason shown |
| NORMAL | Default (no stored row). The pipeline's ranking order |
| LOW | Listed after NORMAL; quieter card and marker; reason shown |
| MUTED | Hidden from the feed and map unless "Show muted"; counted ("9 muted") |

Combination (deterministic, `workspace_views.priority_for`). A Development's countries are its location
country plus the states its principal actors act for.

1. **MUTED**: its topic is muted, or it concerns countries and every one of them is muted. A US–Russia meeting with
   Russia muted is still shown, because the US is not muted.
2. **HIGH**: its topic or any (unmuted) country it concerns is HIGH.
3. **LOW**: its topic is LOW, or every (unmuted) country it concerns is LOW.
4. **NORMAL** otherwise.

Within a level, the pipeline's ranking order is kept. Priority changes ordering, emphasis and default
visibility only. It does not touch Development creation, Situation membership, confidence, evidence or any stored
field; the test `test_priorities_never_change_developments_situations_or_evidence` compares the intelligence
database before and after a sequence of priority changes and page loads.

The feed explains every reordering in words ("Surfaced first because: HIGH country: Ukraine (location) + HIGH
topic: Military"). There is no relevance number. Event significance (the pipeline's significance class and
ranking reasons) stays a separate line on the card.

Topics are the existing `EventDomain` taxonomy (diplomacy, military, security, political, economic,
humanitarian, institutional). Development type (`EventType`) is a secondary filter. No new ontology.

## Persistence model

Personal priorities live in their own SQLite file, never in the intelligence database:

- path `OSINT_USER_STATE_DB`, default `data/user_state.db` (created on first use; `data/*.db` is git-ignored);
- table `preferences(profile, scope, key, level, updated_at)`, primary key `(profile, scope, key)`;
  `user_state_meta(schema_version = 1)`;
- `profile` is `"default"` (no accounts); `scope` is `country` (key: ISO 3166-1 alpha-3, or Natural Earth's code
  where there is none: KOS, CYN, SOL) or `domain` (key: an `EventDomain` value); `level` is HIGH / LOW / MUTED
  (NORMAL deletes the row).

The same row shape takes later scopes without a schema change: `situation` (follow or mute by slug),
`requirement`, `last_seen`. None is implemented.

**No migration of the intelligence database.** Schema version stays 6. The pipeline never reads the user-state file.

Routes (all take stable ids; names are rejected with 404, unknown levels with 422):

| Route | |
|---|---|
| `GET /api/priorities` | `{"country": {"CHN": "HIGH"}, "domain": {"economic": "MUTED"}}` |
| `PUT /api/priorities/{scope}/{key}` | body `{"level": "HIGH"}` |
| `DELETE /api/priorities/{scope}/{key}` | back to NORMAL |
| `DELETE /api/priorities[?scope=]` | reset |
| `POST /ui/priorities/{scope}/{key}`, `POST /ui/priorities/reset` | HTMX forms; return the panel and `HX-Trigger: priorities-changed` |
| `GET /ui/countries?q=` | country search for the panel |
| `GET /api/workspace/developments.geojson` | mapped Developments of the current selection (same query parameters as `/`); `scope=situation&situation=<slug>` for every Development of a Situation; `unmapped` count |

## Responsive behaviour

- At or above 1201 px: three columns. The left rail collapses (« button), giving its width to the map and feed.
- 801–1200 px: the context rail becomes a drawer from the right ("What changed" button); a marker click opens it.
- At or below 800 px: one column. The map is 52% of the viewport height, the feed follows, and both rails are
  drawers ("Filters & priorities", "What changed"). The map keeps zoom, pan, cluster expansion and country click.

## Known backend limitations

- **Geocoding quality** (above): about 17% of corroborated Developments have no confirmed map position, mostly
  because the stored point contradicts the reports. Fixing that belongs to geocoding, not the UI.
- **Many locations are whole countries.** Nominatim returns a country centroid when the most-mentioned place is a
  country, and place names arrive in the local script ("Олешки", "中国"). The UI marks these and shows the
  country name for them.
- **No primary-evidence flag is stored per Development.** Provenance is computed on demand (`assess_event`, about
  2 s or more per Development on the live snapshot), so feed cards show confidence and independent-source count,
  and the evidence grouping (official / independent / derivative / commentary) appears on the detail page only.
  An evidence-role filter was left out for the same reason.
- **Item language is not stored**, so evidence rows show source, time, excerpt, role and link, but not language.
- **Development lifecycle is not stored.** "New" / "Updated" is derived from stored timestamps (first reported inside
  or before the period). Situation status (active / dormant / closed) is the backend's.
- **The Situation detail page is slow on the live data** (about 25 s for a large Situation): the existing view
  computes provenance for every Development in the timeline. Unchanged here; worth a cached provenance field later.
- Classification errors show through (a campaign speech classified `military` surfaces under a HIGH Military
  priority). The UI shows the backend's classification as stored.

## Owner review (2026-10-27)

Architecture, visual direction and interaction model approved; commit and push, deploy later (web server only,
after Candidate A's C2, on separate approval).

Non-blocking follow-ups for the next frontend pass:

1. Make the `H / N / L / M` controls self-explanatory with tooltips and accessible labels (High, Normal, Low,
   Muted) on hover and focus, without making them larger.
2. Temporal grouping in long feeds and timelines (subtle Today / Yesterday / Earlier or date separators).
3. An analyst-facing warning for unusually heterogeneous evidence, **only** once future semantic work defines it.
   No frontend heuristic.
4. Lighter card metadata at phone width.

The review also showed upstream identity problems the UI now makes visible: a ceasefire Development with 593 items
of mixed occurrences, and a broad Russia–Ukraine Situation. They are recorded as evaluation evidence on
`eval/phase2-followup` (`evaluations/phase2-followup/diagnostics/ui-review-2026-10-27/`), not handled in the UI.

## Deliberately deferred

LLM chat, predictive or relevance scoring, natural-language intelligence requirements, relation graph
exploration, ontology changes, cross-language merging, user accounts, a native mobile app; also followed or muted
Situations, last-seen state, a custom time range, and an evidence-role filter (see limitations). Relation data is
not used by any page.

## Deployment boundary

This milestone can deploy independently of the parked Phase 2 work:

- no change to Development identity, Situation creation or membership, clustering, segmentation, entity resolution,
  cross-language identity (still disabled), relations, alerting, collectors or the supervisor;
- no intelligence-database migration (schema stays 6); personal priorities are a separate file;
- personal priorities affect presentation only (tested);
- the backend semantic test suite stays green.

It changes the web server only (`main.py serve`); the daemon does not import the new modules. The old Leaflet
`/map` page and the old Today templates are replaced by the workspace; the classic dashboard pages are unchanged.

Regenerate the country geometry with `python scripts/build_country_geo.py NE_110M.geojson NE_50M.geojson`
(Natural Earth v5.1.2, public domain).
