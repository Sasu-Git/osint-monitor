# Collector cleanup: work packages (2026-11-02). Plan only; nothing enabled, disabled or deployed

**Source.**
- **Decisions:** `TRIAGE-2026-11-02.md` (`eval/soak-safe-20261102` `508e38c`), from the collector status read
  2026-11-02 ~14:40Z.
- **Code and config references:** `main` `19b8754` (collector code unchanged since `44e0357`).
- **Evidence labels:** **[repo]** = code or config here; **[status]** = the collector's recorded error;
  **UNVERIFIED** = an external cause not tested. Endpoint probes were declined in this session, so no external cause is
  upgraded to fact.

**Every package is a runtime change** (collector set, config or alerting). It ships as its own candidate through the
deploy runbook, never bundled with the pair-matcher soak or with another package unless listed together below.
⚠️ Packages WP5 and WP-opt involve API keys or credentials. Coordinate with the Data & AI Team before storing or
deploying any key; no key is stored here.

## FIX

### WP1. Wikipedia edit monitor: identify the client
| | |
|---|---|
| Problem | Every MediaWiki API call returns `403 Forbidden` [status]. `WikipediaEditMonitor` calls `requests.get(self.API_URL, params=…)` with **no User-Agent** (`osint_monitor/collectors/spectrum.py`, the `WikipediaEditMonitor` revisions fetch) [repo]. Cause: Wikimedia's API policy asks for a descriptive client User-Agent with a contact — **UNVERIFIED** as the reason for these 403s |
| Change | Send `User-Agent: OSINT-Monitor/<version> (<project URL or contact>)` on the collector's requests (one header dict); keep the existing rate (cold tier, hourly) |
| Prerequisite | A contact string the owner is willing to send (an email or project URL) |
| Expected after | `state: ok` or `partial` on the next cold tick, with revisions for the watched pages; consecutive failures reset |
| Test | Unit test: the request carries the header (mocked `requests.get`). Operational: one manual cold-tier run against a scratch DB, or C1 of its deploy, showing the collector healthy. If it is still 403 with the header, the cause was something else: stop, and re-triage as REPLACE or DISABLE |
| Risk | Low: one collector, header only; it ingests only edit metadata of watched pages |
| Credentials | None (no key); the contact string is public by design |

### WP2. Defense Stock Monitor: no false "Source resumed" alerts
| | |
|---|---|
| Problem | The monitor emits an item only when a ticker moves past its threshold (`collectors/financial.py`), and markets close at weekends [repo]. The silence-break rule (`alerting/engine.py: _tier2_source_silence_break`) therefore fired "Source resumed: Defense Stock Monitor (silent 62–66 h)" after weekends: 5 alerts, 09-28 to 10-21 [snapshot]. `_operational_silence` excuses only our own outages [repo] |
| Change | A per-source flag for **event-driven sources** (emit only on a condition), set for Defense Stock Monitor (and any other threshold-triggered source the owner names), exempting them from silence-break alerts. Config-level list, for example `alerts.yaml: silence_break_exempt: [...]` |
| Prerequisite | Owner confirms which sources are event-driven (proposed: Defense Stock Monitor, Commodity SIGINT) |
| Expected after | No `source_silence_break` alert for exempt sources; the other sources unchanged |
| Test | Unit: exempt source silent for 66 h then posting gives no alert; non-exempt source gives an alert (the existing behaviour). Replay of the alert engine on the snapshot: only the 5 Defense Stock alerts would disappear |
| Risk | Low: alerting only; no collection change |
| Credentials | None |

## REPLACE (or DISABLE if no replacement path is chosen)

### WP3. Nitter accounts (9)
| | |
|---|---|
| Problem | AuroraIntel, CENTCOM, COUPSURE, NATO, NavyLookout, RALee85, TheIntelFrog, bellingcat, detresfa_: "all instances failed". `nitter.poast.org` does not resolve and `nitter.net` fails; never succeeded; about 1,030 consecutive failures each [status]. Instances are `nitter_instances` in `config/sources.yaml` [repo]. That public Nitter instances have largely shut down is **UNVERIFIED** |
| Options | (a) **Disable now**: remove or comment the 9 `twitter_accounts` entries, or empty `nitter_instances`; about 10,000 failing calls a day stop. (b) **Replace** through official channels where the account's owner publishes elsewhere (for example the NATO and CENTCOM press-release RSS, the bellingcat site RSS): add those as `rss_feeds` with `identity` set so provenance treats them as the same organisation. (c) Self-hosted Nitter or the X API: needs X session tokens or a paid key, and is not recommended without an owner decision |
| Proposed | (a) now, plus (b) for the official accounts whose site feeds exist. Each feed URL is to be verified when the package is built (**UNVERIFIED** until then) |
| Expected after | No Nitter failures in collector status. For (b), new RSS endpoints healthy |
| Test | `main.py inspect sources` shows the accounts disabled or absent and the replacement feeds configured; one warm tick on a scratch DB; C1 of the deploy |
| Risk | Low for (a): the collector never produced an item, so nothing is lost. Low to medium for (b): new sources add items, so provenance roles must be set (official → `primary_official`) |
| Credentials | None for (a) and (b) |

## DISABLE

### WP4. Lawfare
| | |
|---|---|
| Problem | `403 Forbidden` on `https://www.lawfaremedia.org/feed`, fallback also 403; never succeeded [status]. The collector already sends a descriptive User-Agent (`collectors/rss.py`, `_RSS_HEADERS`) [repo]. Anti-bot protection is the likely cause (**UNVERIFIED**). Getting past it is not an option |
| Change | `enabled: false` with `access: "feed answers 403 to automated clients (2026-11)"` on the Lawfare entry (`config/sources.yaml`), the existing mechanism (as for Reuters) |
| Prerequisite | None |
| Expected after | Shown as `disabled` in collector status, not `failed` |
| Test | `inspect sources` lists it disabled; status after one warm tick |
| Risk | Very low: never produced an item; it was commentary anyway (analysis role in provenance) |
| Credentials | None |

## KEEP_OPTIONAL (registered only when their prerequisite exists; mirrors the existing `SPACETRACK_USER` / `RIPE_ATLAS_KEY` pattern in `processors/pipeline.py`)

### WP5. US Congress
| | |
|---|---|
| Problem | `CONGRESS_API_KEY not set – skipping`, recorded as `failed` on every cold tick [status]. `CongressCollector()` is registered unconditionally (`pipeline.py`, government intelligence block) [repo] |
| Change | Register `CongressCollector` only when `CONGRESS_API_KEY` is set. Without it, nothing is registered: no failure entry. Adding the key later (a separate decision) enables it |
| Prerequisite | None for the guard. For collection, a free api.congress.gov key ⚠️ (coordinate with the Data & AI Team before storing it; it belongs in `.env`, never in git) |
| Expected after | No `US Congress` failure; with a key, legislative items (cold tier) |
| Test | Unit: registration with and without the env var |
| Risk | Very low |
| Credentials | Only to enable collection: an API key ⚠️ |

### WP6. finance_agent bridge
| | |
|---|---|
| Problem | `finance_agent not found at C:\Users\EugenioVardiero\finance_agent` (`FINANCE_AGENT_PATH` default) [status/repo]. The sibling repo is not on this host |
| Change | Register `FinanceBridgeCollector` only when the path exists (or `FINANCE_AGENT_PATH` is set and exists) |
| Prerequisite | None for the guard. To enable it, the owner installs the `finance_agent` checkout and its setup (size **UNVERIFIED**) |
| Expected after | No failure entry; the financial modality in fusion relies on the commodity and defense-stock collectors meanwhile |
| Test | Unit: registration with an existing and a missing path |
| Risk | Very low |
| Credentials | Possibly the finance_agent's own (**UNVERIFIED**) |

### WP7. X-ForYou
| | |
|---|---|
| Problem | `Chrome CDP not available` on every warm tick [status]. It is a manual, browser-driven collector (the `x-collect` skill) that needs a logged-in Chrome with `--remote-debugging-port=9222` or `CHROME_CDP_URL` [repo] |
| Change | Remove it from the daemon's warm tier (`COLLECTOR_TIERS["XForYouCollector"]` and its registration), or register it only when an explicit opt-in env var is set. Manual use through the skill is unchanged |
| Prerequisite | None |
| Expected after | No failure entry from the daemon; manual collection still works |
| Test | Unit: not registered by default; the skill path still constructs it |
| Risk | Very low |
| Credentials | The owner's X session in a local browser, only for manual use |

## KEEP (no package)
- **BGP Monitor:** partial; RIPE Stat read time-outs on single ASNs, last success today [status]. An optional later
  tweak would be a longer timeout or one retry for slow ASNs.
- **NVD:** one transient 503, succeeded the same day [status].

## Suggested grouping for deploys (each a separate candidate)

| Order | Content | Why grouped |
|---|---|---|
| 1 | WP4 + WP3(a) | config-only disables of never-working sources |
| 2 | WP5 + WP6 + WP7 | registration guards, same code area and test pattern |
| 3 | WP1 | one collector, needs a contact string |
| 4 | WP2 | alerting rule; needs the owner's event-driven source list |
| 5 | WP3(b) | new sources: provenance roles and their own C1 |

**Outcome after 1–3:** the recurring "14 failed collectors" warning reduces to genuine, transient failures.

**Owner inputs needed:**
- the WP1 contact string;
- the WP2 event-driven list;
- whether WP3 is (a) only or (a) + (b);
- whether to obtain the Congress key (⚠️ via the Data & AI Team).
