"""Source inventory: every source identity and endpoint the pipeline is configured to query,
whether each is enabled here, and what a database and a daemon log show it produced.

Read-only. Nothing is collected, no network call is made, the database is opened read-only
and never migrated. ``python main.py inspect sources`` prints it.

Terms
    source identity  the organisation, outlet or account whose content an endpoint returns
                     (BBC, USGS, RIPE NCC, @bellingcat). Counted once however many endpoints.
    endpoint         one independently issued query per collection cycle: a feed URL, or an
                     API queried for one target (a ticker, an ASN, a domain, a page).
                     Authentication calls, mirrors and fallback URLs for the same query are
                     not separate endpoints.
    configured       wired into ``pipeline.build_collectors()``, including endpoints built only
                     when a credential is set and alternative modes of one collector.
                     Collector classes that nothing builds are listed separately (UNWIRED).
    enabled          built in this environment and able to return data: required credentials
                     and local prerequisites present. Whether the remote side answers is not
                     checked (no network).
    observed         stored items whose ``Source.name`` is the endpoint's source name. Items
                     are stored per collector, so an endpoint of a multi-target collector is
                     attributed only when its target is visible on the item (URL or title);
                     otherwise its observation is "unknown".

The endpoint list is derived from the collectors' own target constants and
config/sources.yaml, so it follows them; tests check it against ``build_collectors()``.
"""

from __future__ import annotations

import importlib.util
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

# Collector families, in report order.
FAMILIES = ["rss", "social", "government", "documents", "sanctions", "structured", "sigint",
            "infrastructure", "spectrum", "financial", "adsb"]

ACTIVE, NO_OBSERVATIONS, DISABLED, ERRORS, UNKNOWN = (
    "active", "enabled / no observations", "disabled", "recurrent errors observed", "unknown")

# Landing countries SubmarineCableMonitor.collect() queries (its local priority_countries).
CABLE_PRIORITY_COUNTRIES = {"IR", "AE", "SA", "OM", "EG", "UA", "RU"}


@dataclass(frozen=True)
class Gate:
    """When build_collectors() builds the endpoint and when it can return data."""
    env: tuple[str, ...] = ()            # all must be set
    unless_env: tuple[str, ...] = ()     # alternative mode used only while these are unset
    prerequisite: str | None = None      # key into PREREQUISITES
    fallback_only: bool = False          # built only if another collector cannot be imported
    config_enabled: bool = True          # sources.yaml ``enabled``
    access: str | None = None            # sources.yaml ``access``: why it is off / what it needs


@dataclass(frozen=True)
class Endpoint:
    family: str
    collector: str                       # collector class
    identity: str                        # organisation / outlet / account
    source_name: str                     # Source.name its items are stored under
    endpoint: str                        # what is queried
    url: str
    target: str | None = None
    match: tuple[str, str] | None = None  # ("url" | "title", token): attributes items to this target
    gate: Gate = field(default_factory=Gate)
    note: str = ""
    language: str | None = None          # ISO 639-1, from sources.yaml (content is stored untranslated)
    category: str | None = None          # sources.yaml category (-> provenance category_roles)

    @property
    def key(self) -> str:
        return f"{self.source_name} :: {self.endpoint}" + (f" [{self.target}]" if self.target else "")


@dataclass(frozen=True)
class Unwired:
    collector: str
    module: str
    source_name: str
    note: str


UNWIRED = [
    Unwired("AISCollector", "collectors/ais.py", "ais_{region}", "stub: collect() always returns []"),
    Unwired("TelegramCollector", "collectors/telegram.py", "tg:{channel}", "needs TELEGRAM_API_ID/HASH; no channels configured"),
    Unwired("TwitterAPICollector", "collectors/twitter.py", "@{username}", "needs TWITTER_BEARER_TOKEN"),
    Unwired("CustomWebCollector", "collectors/custom.py", "{name}", "CSS-selector scraper; no targets configured"),
    Unwired("SentinelCollector", "collectors/sigint.py", "Sentinel Imagery", "needs SENTINEL_CLIENT_ID/SECRET; 5 AOIs defined"),
]


# --- prerequisites (local only, never the network) -----------------------------------------------

def _finance_agent() -> tuple[bool, str]:
    from osint_monitor.collectors.finance_bridge import _DEFAULT_FINANCE_AGENT_PATH
    run = Path(_DEFAULT_FINANCE_AGENT_PATH) / "run.py"
    return run.exists(), f"finance_agent not found at {run.parent}"


def _playwright() -> tuple[bool, str]:
    return importlib.util.find_spec("playwright") is not None, "playwright is not installed (and a Chrome CDP session is required)"


PREREQUISITES = {"finance_agent": _finance_agent, "playwright": _playwright}


def gate_status(gate: Gate, env=None) -> tuple[bool, str | None]:
    """(enabled, reason it is not)."""
    env = os.environ if env is None else env
    if not gate.config_enabled:
        return False, "disabled in config/sources.yaml" + (f": {gate.access}" if gate.access else "")
    if gate.fallback_only:
        return False, "fallback only: built when adsb_tracks cannot be imported"
    missing = [v for v in gate.env if not env.get(v)]
    if missing:
        return False, f"{', '.join(missing)} not set"
    present = [v for v in gate.unless_env if env.get(v)]
    if present:
        return False, f"alternative mode: not used while {', '.join(present)} is set"
    if gate.prerequisite:
        ok, reason = PREREQUISITES[gate.prerequisite]()
        if not ok:
            return False, reason
    return True, None


# --- the configured endpoints ---------------------------------------------------------------------

def configured_endpoints(config=None) -> list[Endpoint]:
    from osint_monitor.collectors import (
        adsb, adsb_tracks, financial, govint, infrastructure as infra, sanctions, sigint, spectrum, structured,
    )
    from osint_monitor.core.config import load_sources_config
    from osint_monitor.processors.documents import DocumentCollector

    config = config or load_sources_config()
    out: list[Endpoint] = []
    add = out.append

    for feed in config.rss_feeds:
        add(Endpoint("rss", "RSSCollector", feed.identity or feed.name, feed.name, "RSS feed", feed.url,
                     gate=Gate(config_enabled=feed.enabled, access=feed.access),
                     language=feed.language, category=feed.category))
    instances = config.nitter_instances or ["https://nitter.net"]
    for account in config.twitter_accounts:
        user = account.username.lstrip("@")
        add(Endpoint("social", "NitterCollector", f"@{user}", f"@{user}", "Nitter RSS",
                     f"{instances[0]}/{user}/rss", note=f"mirrors tried in order: {', '.join(instances)}"))
    add(Endpoint("social", "XForYouCollector", "X (For You feed of the logged-in account)", "X-ForYou",
                 "x.com/home via Chrome CDP", "https://x.com/home", gate=Gate(prerequisite="playwright")))

    for name, feed in sanctions.SANCTIONS_FEEDS.items():
        identity = "US Treasury OFAC" if name.startswith("OFAC") else "UN Security Council"
        add(Endpoint("sanctions", "SanctionsCollector", identity, name, "sanctions list XML", feed["url"]))

    add(Endpoint("structured", "ACLEDCollector", "ACLED", "ACLED", "events API (OAuth token first)",
                 structured.ACLEDCollector.BASE_URL, gate=Gate(env=("ACLED_EMAIL", "ACLED_PASSWORD"))))
    add(Endpoint("structured", "GDELTCollector", "GDELT Project", "GDELT", "article search",
                 structured.GDELTCollector.CONTEXT_API, note=f"falls back to {structured.GDELTCollector.DOC_API}"))
    add(Endpoint("structured", "USGSSeismicCollector", "USGS", "USGS Seismic", "FDSN event query (7 days, M2+)",
                 structured.USGSSeismicCollector.BASE_URL))
    firms = structured.NASAFIRMSCollector
    for zone in firms.CONFLICT_ZONES:
        add(Endpoint("structured", "NASAFIRMSCollector", "NASA FIRMS", "NASA FIRMS", "area API", firms.AREA_API,
                     target=zone, match=("title", f"({zone})"), gate=Gate(env=("NASA_FIRMS_KEY",))))
    add(Endpoint("structured", "NASAFIRMSCollector", "NASA FIRMS", "NASA FIRMS", "global VIIRS 24h CSV (no key)",
                 firms.FALLBACK_CSV, gate=Gate(unless_env=("NASA_FIRMS_KEY",))))

    add(Endpoint("government", "CongressCollector", "US Congress (congress.gov)", "US Congress", "bills API",
                 govint.CongressCollector.API_URL, gate=Gate(env=("CONGRESS_API_KEY",))))
    add(Endpoint("government", "TravelAdvisoryCollector", "US State Department", "Travel Advisories",
                 "travel advisories RSS", govint.TravelAdvisoryCollector.RSS_URL))
    ooni = govint.OONICollector
    add(Endpoint("government", "OONICollector", "OONI", "OONI Internet Monitor", "incidents", ooni.INCIDENTS_URL,
                 match=("url", "/incidents")))
    add(Endpoint("government", "OONICollector", "OONI", "OONI Internet Monitor", "anomalous measurements",
                 ooni.MEASUREMENTS_URL, match=("url", "explorer.ooni.org/search")))
    for fir in govint.NOTAMCollector.FIRS_OF_INTEREST:
        add(Endpoint("government", "NOTAMCollector", "US FAA", "NOTAMs", "NOTAM API", govint.NOTAMCollector.FAA_API_URL,
                     target=fir, match=("title", fir), gate=Gate(env=("FAA_NOTAM_KEY",))))
    add(Endpoint("documents", "DocumentCollector", "US Federal Register", DocumentCollector.FEDERAL_REGISTER_SOURCE,
                 "documents API", DocumentCollector.FEDERAL_REGISTER_URL, language="en"))
    add(Endpoint("documents", "DocumentCollector", "Congressional Research Service", DocumentCollector.CRS_SOURCE,
                 "CRS products RSS", DocumentCollector.CRS_RSS_URL, language="en"))

    add(Endpoint("sigint", "IAEACollector", "IAEA", "IAEA Nuclear Safeguards", "top news feed", sigint.IAEACollector.FEED_URL))
    add(Endpoint("sigint", "NVDCollector", "NIST NVD", "NVD CVE Intelligence", "CVE API (7 days)", sigint.NVDCollector.BASE_URL,
                 note=f"CVEs are cross-checked against the CISA KEV catalogue ({sigint.NVDCollector.CISA_KEV_URL}), "
                      "which yields no items of its own"))
    add(Endpoint("sigint", "CurrencyCollector", "ExchangeRate-API (open.er-api.com)", "Currency SIGINT",
                 "USD rates (9 watched currencies)", sigint.CurrencyCollector.BASE_URL))
    add(Endpoint("sigint", "UNHCRCollector", "UNHCR", "UNHCR Displacement", "population demographics API",
                 sigint.UNHCRCollector.BASE_URL))
    for hs in sigint._DUAL_USE_HS_CODES:
        add(Endpoint("sigint", "COMTRADECollector", "UN Comtrade", "UN COMTRADE", "HS import flows",
                     "https://comtradeapi.un.org/data/v1/get/C/A/HS", target=hs, match=("url", f"CommodityCodes={hs}"),
                     gate=Gate(env=("COMTRADE_API_KEY",))))

    for asn in infra.WATCHED_ASNS:
        add(Endpoint("infrastructure", "BGPMonitor", "RIPE NCC", "BGP Infrastructure Monitor",
                     "RIPEstat routing status + BGP updates", infra.RIPE_ROUTING_STATUS, target=asn,
                     match=("url", f"/{asn}"), note=f"two calls per ASN, one observation: also {infra.RIPE_RIS_API}"))
    for domain in infra.WATCHED_DOMAINS:
        add(Endpoint("infrastructure", "DNSHealthMonitor", "OSINT Monitor (own DNS + HTTPS probe)", "DNS Health Monitor",
                     "DNS lookup + HEAD", f"https://{domain}", target=domain, match=("url", f"//{domain}")))
    for zone, cfg in infra.FlightRouteMonitor.WATCH_ZONES.items():
        add(Endpoint("infrastructure", "FlightRouteMonitor", "OpenSky Network", "Flight Route Monitor", "state vectors (bbox)",
                     infra.FlightRouteMonitor.OPENSKY_URL, target=zone, match=("title", cfg["desc"].split(" / ")[0])))
    add(Endpoint("infrastructure", "SeismicExplosionDetector", "USGS", "Seismic Explosion Detector",
                 "FDSN event query (24 h, shallow)", infra.SeismicExplosionDetector.BASE_URL))

    for page in spectrum.WATCHED_PAGES:
        add(Endpoint("spectrum", "WikipediaEditMonitor", "Wikimedia (English Wikipedia)", "Wikipedia Edit Monitor",
                     "page revisions", spectrum.WikipediaEditMonitor.API_URL, target=page["title"],
                     match=("title", page["title"])))
    countries = sorted({c for cable in spectrum.WATCHED_CABLES for c in cable["landing_countries"]} & CABLE_PRIORITY_COUNTRIES)
    for cc in countries:
        add(Endpoint("spectrum", "SubmarineCableMonitor", "RIPE NCC", "Submarine Cable Monitor", "RIPEstat country resources",
                     spectrum.SubmarineCableMonitor.RIPE_COUNTRY_ROUTING, target=cc, match=("url", f"stat.ripe.net/{cc}")))
    for norad in spectrum.RECON_SATELLITES:
        add(Endpoint("spectrum", "SatelliteTracker", "Space-Track.org", "Satellite Orbital Tracker", "GP elements",
                     spectrum.SatelliteTracker.TLE_URL, target=norad, match=("title", norad),
                     gate=Gate(env=("SPACETRACK_USER", "SPACETRACK_PASS"))))
    for t in spectrum.LATENCY_TARGETS:
        add(Endpoint("spectrum", "RIPEAtlasMonitor", "RIPE NCC", "RIPE Atlas Probes", "Atlas ping measurements",
                     f"{spectrum.RIPEAtlasMonitor.API_URL}/measurements/", target=t["target"], match=("title", t["target"]),
                     gate=Gate(env=("RIPE_ATLAS_KEY",)), note="the key only gates construction; it is never sent"))

    for symbol in financial.CommodityMonitor.COMMODITIES:
        add(Endpoint("financial", "CommodityMonitor", "Yahoo Finance", "Commodity SIGINT", "chart API",
                     financial.CommodityMonitor.YAHOO_QUOTE_URL, target=symbol, match=("url", f"/quote/{symbol}")))
    for symbol in financial.DefenseStockMonitor.DEFENSE_TICKERS:
        add(Endpoint("financial", "DefenseStockMonitor", "Yahoo Finance", "Defense Stock Monitor", "chart API",
                     financial.DefenseStockMonitor.YAHOO_QUOTE_URL, target=symbol, match=("title", f"({symbol})")))
    for cik, company in financial.SECDefenseMonitor.DEFENSE_CIKS.items():
        add(Endpoint("financial", "SECDefenseMonitor", "SEC EDGAR", "SEC Defense Filings", "submissions API",
                     financial.SECDefenseMonitor.EDGAR_SUBMISSIONS, target=cik, match=("title", str(company))))
    for kw in financial.SAMContractMonitor.DEFENSE_KEYWORDS[:5]:
        add(Endpoint("financial", "SAMContractMonitor", "SAM.gov (GSA)", "SAM.gov Procurement", "opportunities search",
                     financial.SAMContractMonitor.API_URL, target=kw, gate=Gate(env=("SAM_GOV_API_KEY",))))
    add(Endpoint("financial", "FinanceBridgeCollector", "finance_agent (sibling repository)", "Financial Intelligence (Quant)",
                 "local subprocess run.py", "local", gate=Gate(prerequisite="finance_agent")))

    add(Endpoint("adsb", "ADSBTrackCollector", "ADSB.lol", "ADSB Military Tracks", "global military aircraft",
                 adsb_tracks.ADSB_LOL_MIL, note=f"filtered locally to {len(adsb_tracks.WATCH_REGIONS)} regions"))
    for region in ("persian_gulf", "black_sea", "taiwan_strait"):
        add(Endpoint("adsb", "ADSBCollector", "OpenSky Network", f"adsb_{region}", "state vectors (bbox)",
                     adsb.OPENSKY_API_URL, target=region, gate=Gate(fallback_only=True)))
    return out


_COLLECTOR_TYPES = {"sanctions": "sanctions", "social": "twitter"}     # provenance collector_roles keys


def provenance_role(ep: Endpoint, resolver=None) -> str:
    """The source role provenance assigns to the endpoint's items (config/provenance.yaml)."""
    from osint_monitor.processors.provenance.confidence import EvidenceItem
    from osint_monitor.processors.provenance.resolve import ProvenanceResolver
    resolver = resolver or ProvenanceResolver()
    return resolver.source_role(EvidenceItem(source_name=ep.source_name, source_category=ep.category,
                                             collector_type=_COLLECTOR_TYPES.get(ep.family))).value


# --- observations ---------------------------------------------------------------------------------

@dataclass
class SourceObservation:
    items: int = 0
    last: datetime | None = None
    last_24h: int = 0
    last_7d: int = 0
    rows: list[tuple[str, str, datetime]] = field(default_factory=list)   # (url, title, fetched_at)


@dataclass
class Observations:
    db: str
    coverage: tuple[datetime | None, datetime | None]
    now: datetime | None
    sources: dict[str, SourceObservation]
    source_types: dict[str, str]


def _parse_time(value) -> datetime | None:
    if value is None or isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value).replace("Z", ""))


def read_observations(db_path: str, now: datetime | None = None) -> Observations:
    """Stored items per source, from a SQLite file opened read-only (never migrated)."""
    import sqlite3
    path = Path(db_path)
    if not path.exists():
        raise FileNotFoundError(db_path)
    # Read-only even at the file level: without pending WAL content, open immutable so SQLite does
    # not create -wal/-shm side files next to the database; with it, read through the WAL.
    wal = path.with_name(path.name + "-wal")
    flags = "mode=ro" if wal.exists() and wal.stat().st_size else "mode=ro&immutable=1"
    conn = sqlite3.connect(f"file:{path.as_posix()}?{flags}", uri=True)
    try:
        types = {n: t for n, t in conn.execute("SELECT name, type FROM sources")}
        rows = conn.execute("SELECT s.name, r.url, r.title, r.fetched_at FROM raw_items r "
                            "JOIN sources s ON s.id = r.source_id").fetchall()
    finally:
        conn.close()
    times = [_parse_time(r[3]) for r in rows if r[3]]
    start, end = (min(times), max(times)) if times else (None, None)
    now = now or end
    sources: dict[str, SourceObservation] = defaultdict(SourceObservation)
    for name in types:
        sources[name]                                           # a source row with no items still exists
    for name, url, title, fetched in rows:
        t = _parse_time(fetched)
        o = sources[name]
        o.items += 1
        o.rows.append((url or "", title or "", t))
        if t and (o.last is None or t > o.last):
            o.last = t
        if t and now:
            o.last_24h += t >= now - timedelta(hours=24)
            o.last_7d += t >= now - timedelta(days=7)
    return Observations(db=str(path), coverage=(start, end), now=now, sources=dict(sources), source_types=types)


# --- daemon log evidence ---------------------------------------------------------------------------

_LOG_LINE = re.compile(r"^\s*\[(ok|err|skip)\] ([^:]+?): ?(.*)$")
_RETURNED = re.compile(r"^(\d+) (?:items?|entries)\b")


@dataclass
class LogEvidence:
    ok: int = 0
    err: int = 0
    skip: int = 0
    returned: int | None = None          # summed "N items" / "N entries", when the collector prints it
    last_error: str | None = None

    @property
    def runs(self) -> int:
        return self.ok + self.err + self.skip


def read_log(path: str) -> dict[str, LogEvidence]:
    """Per collector name: the [ok] / [err] / [skip] lines collectors print each run."""
    out: dict[str, LogEvidence] = defaultdict(LogEvidence)
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = _LOG_LINE.match(line)
            if not m:
                continue
            status, name, rest = m.groups()
            e = out[name]
            setattr(e, status, getattr(e, status) + 1)
            if status == "ok" and (r := _RETURNED.match(rest)):
                e.returned = (e.returned or 0) + int(r.group(1))
            if status == "err":
                e.last_error = rest.strip()[:160]
    return dict(out)


# --- the inventory ---------------------------------------------------------------------------------

@dataclass
class EndpointRow:
    endpoint: Endpoint
    enabled: bool
    disabled_reason: str | None
    items: int | None                    # None: not attributable to this endpoint
    last_observed: datetime | None
    last_24h: int | None
    state: str
    evidence: str = ""
    role: str = ""                       # provenance source role of its items


def _attributed(ep: Endpoint, obs: SourceObservation, now: datetime | None) -> tuple[int, datetime | None, int]:
    kind, token = ep.match
    hits = [t for url, title, t in obs.rows if token.lower() in (url if kind == "url" else title).lower()]
    last = max((t for t in hits if t), default=None)
    day = sum(1 for t in hits if t and now and t >= now - timedelta(hours=24))
    return len(hits), last, day


def build_inventory(endpoints: list[Endpoint], observations: Observations | None = None,
                    log: dict[str, LogEvidence] | None = None, env=None) -> list[EndpointRow]:
    from osint_monitor.processors.provenance.resolve import ProvenanceResolver
    resolver = ProvenanceResolver()
    gates = {ep.key: gate_status(ep.gate, env) for ep in endpoints}
    # Items are attributed among the endpoints enabled here: a disabled alternative mode (FIRMS area
    # API without its key) must not be credited with what the enabled mode stored.
    per_source = Counter(e.source_name for e in endpoints if gates[e.key][0])
    rows = []
    for ep in endpoints:
        enabled, reason = gates[ep.key]
        items = last = day = None
        if observations is not None:
            obs = observations.sources.get(ep.source_name, SourceObservation())
            if not obs.items:
                items = 0
            elif not enabled:
                items = None
            elif per_source[ep.source_name] == 1:
                items, last, day = obs.items, obs.last, obs.last_24h
            elif ep.match is not None:
                items, last, day = _attributed(ep, obs, observations.now)
        ev = (log or {}).get(ep.source_name)
        evidence = ""
        if ev:
            evidence = f"log: {ev.ok} ok / {ev.err} err / {ev.skip} skip runs"
            if ev.returned is not None:
                evidence += f", {ev.returned} items returned"
            if ev.err and ev.last_error:
                evidence += f"; last error: {ev.last_error}"
        if not enabled:
            state = DISABLED
        elif ev and ev.err >= 3 and ev.err * 2 >= ev.runs:
            state = ERRORS
        elif items:
            state = ACTIVE
        elif items == 0:
            state = NO_OBSERVATIONS
        else:
            state = UNKNOWN
        rows.append(EndpointRow(ep, enabled, reason, items, last, day, state, evidence, provenance_role(ep, resolver)))
    return rows


def summarize(rows: list[EndpointRow], observations: Observations | None) -> dict:
    identities = {r.endpoint.identity for r in rows}
    enabled = [r for r in rows if r.enabled]
    out = {
        "identities_configured": len(identities),
        "identities_enabled": len({r.endpoint.identity for r in enabled}),
        "source_names_configured": len({r.endpoint.source_name for r in rows}),
        "endpoints_configured": len(rows),
        "endpoints_enabled": len(enabled),
        "endpoints_disabled": len(rows) - len(enabled),
        "api_urls_configured": len({r.endpoint.url for r in rows}),
        # enabled identities by the provenance role of their items, and content languages
        "enabled_identities_by_role": dict(Counter(role for _, role in {(r.endpoint.identity, r.role) for r in enabled})),
        "enabled_endpoints_by_language": dict(Counter(r.endpoint.language or "unspecified" for r in enabled)),
    }
    if observations is not None:
        configured_names = {r.endpoint.source_name for r in rows}
        stored = {n for n, o in observations.sources.items() if o.items}
        observed_rows = [r for r in rows if r.items]
        out.update({
            "db": observations.db,
            "coverage": [observations.coverage[0], observations.coverage[1]],
            "coverage_days": ((observations.coverage[1] - observations.coverage[0]).total_seconds() / 86400
                              if observations.coverage[0] else 0.0),
            "identities_observed": len({r.endpoint.identity for r in observed_rows}),
            "source_names_observed": len(stored & configured_names),
            "endpoints_observed": len(observed_rows),
            "endpoints_unattributable": sum(1 for r in rows if r.items is None and r.enabled and
                                            observations.sources.get(r.endpoint.source_name, SourceObservation()).items),
            "endpoints_active_24h": sum(1 for r in rows if r.last_24h),
            "endpoints_active_7d": sum(1 for r in rows if r.items and r.last_observed
                                       and r.last_observed >= observations.now - timedelta(days=7)),
            "endpoints_never_observed": sum(1 for r in rows if r.items == 0),
            "enabled_never_observed": sum(1 for r in rows if r.enabled and r.items == 0),
            "unconfigured_source_names": sorted(stored - configured_names),
        })
    return out


# --- naming consistency ----------------------------------------------------------------------------

def _norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def naming_issues(endpoints: list[Endpoint], observations: Observations | None = None) -> list[str]:
    """Places where one source is named differently, or different sources share a name."""
    from osint_monitor.core.config import CONFIG_DIR, load_event_grouping_config
    import yaml

    issues = []
    configured = {e.source_name for e in endpoints}
    by_norm = defaultdict(set)
    names = set(configured)
    prov = yaml.safe_load((CONFIG_DIR / "provenance.yaml").read_text(encoding="utf-8")) or {}
    grouping = load_event_grouping_config()
    referenced = {"config/provenance.yaml sources": set(prov.get("sources", {})),
                  "config/event_grouping.yaml": set(grouping.structured.sources) | set(grouping.narrative_sources)
                  | set(grouping.strategies)}
    if observations is not None:
        referenced["database sources"] = set(observations.sources)
    for where, found in referenced.items():
        names |= found
        for n in sorted(found - configured):
            issues.append(f"{where} names {n!r}, which no configured endpoint produces")
    for n in names:
        by_norm[_norm(n)].add(n)
    for variants in by_norm.values():
        if len(variants) > 1:
            issues.append(f"spelling variants of one name: {sorted(variants)}")
    per_name = defaultdict(set)
    for e in endpoints:
        per_name[e.source_name].add(e.identity)
    for name, ids in sorted(per_name.items()):
        if len(ids) > 1:
            issues.append(f"{name!r} is the stored name for {len(ids)} publishers: {sorted(ids)}")
    per_identity = defaultdict(set)
    for e in endpoints:
        per_identity[e.identity].add(e.source_name)
    collectors_of = defaultdict(set)
    for e in endpoints:
        collectors_of[e.identity].add(e.collector)
    for identity, ns in sorted(per_identity.items()):
        # several feeds of one organisation declared in sources.yaml (`identity`) are the design;
        # one organisation split across different collectors is not
        if len(ns) > 1 and collectors_of[identity] != {"RSSCollector"}:
            issues.append(f"{identity} is stored under {len(ns)} source names by different collectors: {sorted(ns)}")
    identity_of = {e.source_name: e.identity for e in endpoints}
    for name, spec in sorted((prov.get("sources") or {}).items()):
        if not (isinstance(spec, dict) and spec.get("origin")):
            continue
        declared = identity_of.get(name)
        if declared is None or declared == name:
            if spec["origin"] != name:
                issues.append(f"{name!r} has provenance origin {spec['origin']!r} but no declared identity")
        elif spec["origin"] != declared:
            issues.append(f"{name!r}: identity {declared!r} in sources.yaml, origin {spec['origin']!r} in provenance.yaml")
    if observations is not None:
        rss_named = {e.source_name for e in endpoints if e.collector == "NitterCollector"}
        typed_rss = sorted(n for n in rss_named if observations.source_types.get(n) == "rss")
        if typed_rss:
            issues.append(f"Nitter accounts stored with Source.type 'rss': {typed_rss}")
    return issues


# --- report ----------------------------------------------------------------------------------------

def _when(t: datetime | None) -> str:
    return t.strftime("%Y-%m-%d %H:%M") if t else "-"


def format_inventory(rows: list[EndpointRow], summary: dict, issues: list[str], active_only: bool = False) -> str:
    s = summary
    lines = ["Source identities",
             f"  configured:        {s['identities_configured']}",
             f"  enabled:           {s['identities_enabled']}"]
    if "identities_observed" in s:
        lines.append(f"  observed:          {s['identities_observed']}")
    lines += ["", "Endpoints",
              f"  configured:        {s['endpoints_configured']}   ({s['api_urls_configured']} distinct feed/API URLs, "
              f"{s['source_names_configured']} stored source names)",
              f"  enabled:           {s['endpoints_enabled']}",
              f"  disabled:          {s['endpoints_disabled']}",
              "  enabled identities by provenance role: "
              + ", ".join(f"{k} {v}" for k, v in sorted(s["enabled_identities_by_role"].items())),
              "  enabled endpoints by language: "
              + ", ".join(f"{k} {v}" for k, v in sorted(s["enabled_endpoints_by_language"].items()))]
    if "endpoints_observed" in s:
        c0, c1 = s["coverage"]
        lines += [f"  observed:          {s['endpoints_observed']}"
                  + (f"   (+{s['endpoints_unattributable']} of multi-target collectors with items not attributable)"
                     if s["endpoints_unattributable"] else ""),
                  f"  active last 24h:   {s['endpoints_active_24h']}",
                  f"  active last 7d:    {s['endpoints_active_7d']}"
                  + (f"   (database covers only {s['coverage_days']:.1f} days)" if s["coverage_days"] < 7 else ""),
                  f"  no observations:   {s['endpoints_never_observed']}   ({s['enabled_never_observed']} of them enabled)",
                  "", f"Database: {s['db']} (read-only), items fetched {_when(c0)} .. {_when(c1)} UTC"]
        if s["unconfigured_source_names"]:
            lines.append(f"  stored names no configured endpoint produces: {s['unconfigured_source_names']}")
    by_family = defaultdict(list)
    for r in rows:
        if active_only and r.state != ACTIVE:
            continue
        by_family[r.endpoint.family].append(r)
    for family in FAMILIES:
        if not by_family.get(family):
            continue
        lines += ["", f"[{family}]"]
        for r in by_family[family]:
            e = r.endpoint
            target = f" [{e.target}]" if e.target else ""
            items = "?" if r.items is None else str(r.items)
            meta = ", ".join(x for x in (e.identity if e.identity != e.source_name else "", r.role, e.language or "") if x)
            lines.append(f"  {e.source_name}{target} -- {e.endpoint}" + (f"   ({meta})" if meta else ""))
            lines.append(f"      {r.state}; items {items}, last {_when(r.last_observed)}"
                         + (f"; {r.disabled_reason}" if r.disabled_reason else ""))
            if r.evidence:
                lines.append(f"      {r.evidence}")
    lines += ["", "Present in code, not wired into build_collectors():"]
    lines += [f"  {u.collector} ({u.module}): {u.note}" for u in UNWIRED]
    if issues:
        lines += ["", "Naming / canonicalisation (reported, not merged):"] + [f"  - {i}" for i in issues]
    return "\n".join(lines)


def inventory_json(rows: list[EndpointRow], summary: dict, issues: list[str]) -> dict:
    def row(r: EndpointRow) -> dict:
        e = r.endpoint
        return {"family": e.family, "collector": e.collector, "identity": e.identity, "source_name": e.source_name,
                "endpoint": e.endpoint, "url": e.url, "target": e.target, "enabled": r.enabled,
                "disabled_reason": r.disabled_reason, "items": r.items,
                "last_observed": r.last_observed.isoformat() if r.last_observed else None,
                "last_24h": r.last_24h, "state": r.state, "evidence": r.evidence, "note": e.note,
                "language": e.language, "category": e.category, "role": r.role}
    s = dict(summary)
    if "coverage" in s:
        s["coverage"] = [t.isoformat() if t else None for t in s["coverage"]]
    return {"summary": s, "endpoints": [row(r) for r in rows],
            "unwired": [u.__dict__ for u in UNWIRED], "naming_issues": issues}
