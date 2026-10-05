# Source health and collection observability

This page is for operators. It answers three questions:

- **Is our collection working?** That is *execution health*.
- **Is each source's data fresh?** That is *source freshness*.
- **When were we not collecting?** That is *collection gaps*.

None of these is a statement about the world. **A collector failure, a stale source or a collection gap is never
a geopolitical finding.** The fusion signal-gap detector and the alert engine consult collector health, and do not
report an outage as a finding.

## Data model

`data/logs/collector_status.json` has the shape `{"schema": 2, "collectors": {<stable key>: entry}}`. It is
written after every collector run (`collectors/status.py`).

| Field | Meaning |
|---|---|
| `key` | **Stable operational identity**: `<CollectorClass>:<configured URL>`, or `NitterCollector:<account>`, or `<CollectorClass>:<code-defined name>` for singleton collectors. It never depends on an editable display name. |
| `name` | Current display name (a label; it may change without orphaning the record) |
| `collector_type`, `source_type`, `tier`, `endpoint` | Collector class, item source type, scheduling tier, queried URL (credentials redacted) |
| `last_attempt` / `last_run` | Last time it ran |
| `last_success`, `last_failure` | Last run in state ok/partial; last failed run |
| `state` | Last run's state. `ok`: no warning or error logged. `partial`: errors logged, but items returned. `failed`: an exception, or errors with no items. |
| `failure_scope` | `whole_collector` (failed) or `some_endpoints_or_entries` (partial) |
| `consecutive_failures` | Failed runs in a row; reset to 0 by any ok or partial run |
| `last_error`, `last_error_class`, `errors` | Redacted error text (at most 5); the exception class, or `LoggedError` |
| `items`, `duration_s` | Items returned by the last run; its duration |
| `http_status` | Last HTTP status, where the collector exposes it (RSS, Nitter); otherwise null, never guessed |
| `fallback_used` | The collector used its fallback path (RSS: feedparser's own fetcher; Nitter: an instance other than the first) |

**Derived health** is computed when the file is read (`health_of`):

| State | Condition |
|---|---|
| `disabled` | the feed is off in `config/sources.yaml` |
| `not_run` | configured, never recorded |
| `failed` | the last run failed |
| `stale` | no success within the freshness window: max(3 × tier interval, 30 min). This catches a stopped daemon even though the last run was ok. |
| `partial` | the last run was partial and is fresh |
| `healthy` | the last run was ok and is fresh |

**Transitions.** Every change of run state (ok → failed, failed → ok, …) is appended to
`data/logs/collector_events.jsonl`. This makes collector-level and endpoint-level outages reconstructible without
a per-run log.

**Alert delivery.** `data/logs/alert_delivery.json` holds, per channel, the last attempt, last success and last
failure, the consecutive failure count, and the last error (redacted). A channel whose `send()` returns False is a
failure too.

**File robustness.**
- A **missing** file means no runs yet.
- A **malformed** file raises `StatusFileError` for readers. `main.py status` prints `MALFORMED`. On the next run,
  the writer moves it aside as `collector_status.corrupt-<time>.json` and starts clean, logging an ERROR.
- A pre-schema-2 file (keyed by display name) is read as legacy entries. Each is adopted into its stable key on
  that collector's next run.

## Source identity audit

Where operational state is keyed today (2026-10-05):

| Place | Key | Stable? | Status |
|---|---|---|---|
| `collector_status.json` | display name (schema 1) | no | **Fixed here**: collector class + configured URL / account |
| `Source` rows (`pipeline.ensure_source`, `api/routes/intelligence.py`) | `Source.name` = display name | no | Renaming a feed in `sources.yaml` creates a new `Source` row. Older items stay on the old row. Not changed here: it is the source model, and a redesign is out of scope. |
| `collectors/inventory.py` `Endpoint.key` | `source_name :: endpoint` | no (contains the display name) | Report-only. Observation counts follow `Source.name`. |
| Alert state `source_last_seen` | `Source.id` | stable per row, but rows are created by name | follows `Source` |
| `processors/scoring.py`, `processors/institutions.py` | feed lookup by `feed.name` | no | config lookups. A rename changes credibility and institution role until both sides are updated. |
| `SourceConfig.identity` | organisation identity | stable, but **not unique per endpoint** (one outlet can have several feeds) | right for counting independent origins, wrong as a health key |

**Minimal fix used.** The health record uses the configured URL, which is the feed's actual endpoint. Changing a
feed's URL is a new endpoint, so it gets a new record by design. Changing its name keeps the record.

## Collection gaps

`python main.py gaps --start <UTC> --end <UTC> [--tier warm] [--db URL | --log daemon.err.log --log-utc-offset 2]`
is read-only. It reports:

- **Expected cadence**: the tier interval from `config/sources.yaml`.
- **Actual runs**: from the run ledger (`pipeline_runs`, schema 5 and later). For an older daemon, from its log's
  `Running job "<Tier> tier` lines, with the log's UTC offset.
- **Coverage**: the fraction of the window covered by runs, each run covering one interval.
- **Tier gaps**: more than max(3 × interval, 15 min) without a run.
  - **Cause `daemon_not_running`** only when a `daemon_down` gap record exists. Why the process stopped is still
    unknown.
  - **Otherwise `unknown`**: host suspend, a blocked scheduler and a stopped process cannot be told apart, and no
    cause is inferred.
- **Collector-level outages** (`failed`) and **endpoint-level outages** (`partial`): from
  `collector_events.jsonl`, with the error class as the stated cause.

Validated on the old daemon's log for the Situation hold-out window (2026-09-29 12:00 → 10-03 12:00 UTC): warm
coverage 39.8% (38.2 of 96 h, 229 runs), with the same 19 gaps measured by hand in the hold-out report.

## Status

`python main.py status` is read-only and works with no daemon and no database. It shows:

- **Daemon:** the pause flag, and a heartbeat per tier from `tier_ticks.json`. `SILENT` means the tier has not
  ticked within its gap threshold; the cause is unknown.
- **Pipeline runs:** the latest run per tier from the run ledger (status, counts, failed stages, code SHA). For a
  schema-3 database it says the run ledger is missing.
- **Collectors:** counts per health state, then failed, stale and partial collectors with last attempt, last
  success, consecutive failures, fallback and error. Not-run collectors are summarised on one line.
- **Collection, last 24 h:** warm coverage and gaps from the run ledger, plus recorded gap events.
- **Entity extraction:** the NER model per language (available / DEGRADED / MISSING).
- **Alert delivery:** failing channels.

## Logging

| Event | Level |
|---|---|
| Collector failed | WARNING `Collector X FAILED (n consecutive): …` (and ERROR with the exception for a raised error; traceback at DEBUG) |
| Partial run | WARNING `Collector X partial: n items, m errors (…)` |
| Recovery | INFO `Collector X recovered` |
| Steady ok run | DEBUG (no per-run INFO noise) |
| Fallback used | INFO (RSS) |
| Post-processing stage failure | ERROR (unchanged; also `failed: …` in the run's `stages`) |
| Database write failure | ERROR, items not stored (unchanged) |
| Alert delivery failure | ERROR on exception; WARNING when `send()` returns False |
| Outage not alerted | INFO `Signal gap not alerted (collection outage)`; INFO `Source X resumed …, not alerted: <why>` |

**Redaction.** Every log record (console and `daemon.log`) and every stored error is redacted (`status.redact`).
That covers URL query tokens (`api_key`, `token`, …), `key=value` secrets, `Authorization` and other auth headers,
and `user:pass@` in URLs.
