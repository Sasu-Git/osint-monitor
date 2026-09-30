"""Source expansion (docs/source-acquisition.md): canonical identities, languages kept as published,
provenance roles of the new sources, licensed feeds disabled, and the collector fixes found by the
source-health audit. Payloads in tests/fixtures/sources/ are trimmed real provider responses."""

import builtins
from datetime import datetime
from pathlib import Path

import feedparser
import pytest

from osint_monitor.collectors import inventory as inv
from osint_monitor.core.config import load_sources_config
from osint_monitor.processors.provenance.confidence import EvidenceItem, assess_confidence
from osint_monitor.processors.provenance.resolve import ProvenanceResolver

FIXTURES = Path(__file__).parent / "fixtures" / "sources"
T = datetime(2026, 9, 30, 9, 0)


def feed(name):
    return next(f for f in load_sources_config().rss_feeds if f.name == name)


def item(n, source, title, text=""):
    category = next((f.category for f in load_sources_config().rss_feeds if f.name == source), None)
    return EvidenceItem(item_id=n, source_name=source, source_category=category, title=title, text=text,
                        published_at=T.replace(minute=n))


# --- identities and endpoints --------------------------------------------------------------------

def test_every_feed_declares_identity_language_and_a_known_role():
    resolver = ProvenanceResolver()
    for f in load_sources_config().rss_feeds:
        assert f.language in {"en", "it", "es"}, f.name
        role = resolver.source_role(item(1, f.name, "t")).value
        assert role in {"primary_official", "wire", "independent_reporting", "specialist_reporting", "analysis"}, f.name


def test_several_endpoints_of_one_organisation_are_one_identity_and_one_origin():
    eps = inv.configured_endpoints()
    by_identity = {}
    for e in eps:
        by_identity.setdefault(e.identity, set()).add(e.source_name)
    assert by_identity["ANSA"] == {"ANSA Mondo", "ANSA English"}
    assert by_identity["BBC"] == {"BBC World", "BBC Mundo"}
    assert by_identity["Federal Reserve"] == {"Federal Reserve Press", "Federal Reserve Speeches"}
    assert by_identity["United Nations"] == {"UN News", "UN Press"}
    names = [e.key for e in eps]
    assert len(names) == len(set(names))                          # no duplicate endpoint identity
    a = assess_confidence([item(1, "ANSA Mondo", "Scontri a Gaza"), item(2, "ANSA English", "Clashes in Gaza")])
    assert a.independent_origins == 1                             # two ANSA feeds, one origin


def test_documents_are_stored_under_one_name_per_publisher():
    from osint_monitor.processors.documents import DocumentCollector
    assert DocumentCollector.FEDERAL_REGISTER_SOURCE == "Federal Register"
    assert DocumentCollector.CRS_SOURCE == "Congressional Research Service"
    eps = {e.endpoint: e for e in inv.configured_endpoints() if e.collector == "DocumentCollector"}
    assert {e.source_name for e in eps.values()} == {"Federal Register", "Congressional Research Service"}


# --- languages -----------------------------------------------------------------------------------

@pytest.mark.parametrize("fixture, source, lang", [("ansa_mondo.xml", "ANSA Mondo", "it"),
                                                   ("elpais_internacional.xml", "El País Internacional", "es")])
def test_original_language_title_body_and_url_are_kept(fixture, source, lang):
    from osint_monitor.collectors.rss import RSSCollector
    from osint_monitor.processors.language import process_multilingual_item
    parsed = feedparser.parse((FIXTURES / fixture).read_bytes())
    items = RSSCollector.entries_to_items(parsed.entries, source)
    assert items and feed(source).language == lang
    first, entry = items[0], parsed.entries[0]
    assert first.title == entry.title and first.url == entry.link and first.published_at is not None
    assert first.source_name == source
    assert process_multilingual_item(first) == first              # Latin-script text is never translated


# --- provenance of the new sources ---------------------------------------------------------------

def test_institutions_are_primary_and_newspapers_independent():
    resolver = ProvenanceResolver()
    got = {p.source_name: p.evidence_type.value for p in resolver.resolve([
        item(1, "ECB Press", "Monetary policy decisions"), item(2, "European Commission Press", "Daily News"),
        item(3, "El País Internacional", "Choques en Gaza"), item(4, "Rai News Esteri", "Scontri a Gaza"),
        item(5, "Kyiv Independent", "Russia strikes Kyiv energy infrastructure")])}
    assert got == {"ECB Press": "primary", "European Commission Press": "primary",
                   "El País Internacional": "independent", "Rai News Esteri": "independent",
                   "Kyiv Independent": "independent"}


def test_think_tank_analysis_never_counts_as_corroboration():
    a = assess_confidence([item(1, "Crisis Group", "Gaza: what the clashes mean"),
                           item(2, "SIPRI", "Arms transfers to the region"),
                           item(3, "Bruegel", "The economics of the Gaza war"),
                           item(4, "Rai News Esteri", "Scontri a Gaza")])
    assert a.independent_origins == 1
    roles = {p.source_name: p.evidence_type.value for p in ProvenanceResolver().resolve(
        [item(1, "Crisis Group", "t"), item(2, "SIPRI", "t"), item(3, "Congressional Research Service", "t")])}
    assert set(roles.values()) == {"commentary"}


def test_spanish_and_italian_wire_attributions_are_derivative():
    resolver = ProvenanceResolver()
    got = {p.source_name: p.derived_from for p in resolver.resolve([
        item(1, "El País Internacional", "Choques en Gaza", "Según informó la agencia EFE, los choques..."),
        item(2, "Il Sole 24 Ore Mondo", "Scontri a Gaza", "Secondo l'ANSA gli scontri sono proseguiti"),
        item(3, "Clarín Mundo", "Choques en Gaza", "GAZA (Europa Press) - Los choques..."),
        item(4, "ANSA Mondo", "Scontri a Gaza (ANSA)", "ROMA - (ANSA) - Scontri")])}
    assert got == {"El País Internacional": "EFE", "Il Sole 24 Ore Mondo": "ANSA", "Clarín Mundo": "Europa Press",
                   "ANSA Mondo": None}                            # ANSA citing itself is its own reporting
    a = assess_confidence([item(1, "ANSA Mondo", "Scontri a Gaza"),
                           item(2, "Il Sole 24 Ore Mondo", "Scontri a Gaza", "Secondo l'ANSA gli scontri...")])
    assert a.independent_origins == 1                             # a copy of ANSA is not a second origin


# --- licensed / credential-gated -----------------------------------------------------------------

def test_licensed_feeds_are_configured_but_disabled_with_the_reason():
    rows = {r.endpoint.source_name: r for r in inv.build_inventory(inv.configured_endpoints(), env={})}
    for name, needle in (("Reuters World", "licensed"), ("EFE", "licensed")):
        assert not rows[name].enabled and needle in rows[name].disabled_reason
        assert rows[name].state == inv.DISABLED
    assert rows["ANSA Mondo"].enabled and rows["ECB Press"].role == "primary_official"


def test_every_new_feed_is_visible_in_the_inventory_with_role_and_language():
    rows = {r.endpoint.source_name: r for r in inv.build_inventory(inv.configured_endpoints(), env={})}
    for f in load_sources_config().rss_feeds:
        r = rows[f.name]
        assert r.endpoint.identity == (f.identity or f.name) and r.endpoint.language == f.language and r.role
    s = inv.summarize(list(rows.values()), None)
    assert set(s["enabled_endpoints_by_language"]) >= {"en", "it", "es"}
    assert s["enabled_identities_by_role"]["analysis"] >= 3


# --- collector fixes -----------------------------------------------------------------------------

def test_ofac_namespaced_xml_is_parsed():
    from osint_monitor.collectors.sanctions import SanctionsCollector
    items = SanctionsCollector(feed_name="OFAC SDN")._parse_ofac((FIXTURES / "ofac_sdn.xml").read_bytes())
    assert [i.title for i in items] == ["OFAC SDN: AEROCARIBBEAN AIRLINES", items[1].title] and len(items) == 2
    assert "Program: CUBA" in items[0].content and items[0].external_id == "ofac_36"


def test_federal_register_and_gdelt_queries_use_the_api_syntax():
    from osint_monitor.collectors.structured import GDELTCollector
    from osint_monitor.processors.documents import DocumentCollector
    assert DocumentCollector.DOCUMENT_TYPES == ("PRESDOCU", "RULE", "PRORULE", "NOTICE")
    q = GDELTCollector().query
    assert q.startswith("(") and q.endswith(")") and " OR " in q


def test_rss_http_refusal_is_an_error_not_zero_items(monkeypatch, capsys):
    from osint_monitor.collectors import rss
    import requests

    def refuse(*a, **k):
        raise requests.HTTPError("403 Client Error: Forbidden")
    monkeypatch.setattr(rss._requests, "get", refuse)
    monkeypatch.setattr(rss.feedparser, "parse", lambda url: feedparser.FeedParserDict(entries=[], status=403))
    assert rss.RSSCollector(name="Lawfare", url="https://example.org/feed").collect() == []
    assert "[err] Lawfare: 403" in capsys.readouterr().out
    ecb = (FIXTURES / "ecb_press.xml").read_bytes()
    monkeypatch.setattr(rss._requests, "get", lambda *a, **k: type("R", (), {
        "text": ecb.decode("utf-8"), "raise_for_status": lambda self: None})())
    monkeypatch.setattr(rss.feedparser, "parse", feedparser.api.parse if hasattr(feedparser, "api") else feedparser.parse)
    got = rss.RSSCollector(name="ECB Press", url="https://www.ecb.europa.eu/rss/press.html").collect()
    assert len(got) == 2 and "[ok] ECB Press: 2 items" in capsys.readouterr().out


def test_ripe_atlas_content_keeps_every_field(monkeypatch):
    from osint_monitor.collectors import spectrum
    m = spectrum.RIPEAtlasMonitor(targets=[{"target": "185.143.232.0/22", "name": "Iran DCI core", "country": "IR",
                                            "type": "telecom"}])
    monkeypatch.setattr(m, "_get_existing_measurements", lambda target: [{"id": 7}])
    monkeypatch.setattr(m, "_get_measurement_results", lambda msm_id: [{"avg": 600.0}, {"avg": 650.0}])
    monkeypatch.setattr(spectrum.time, "sleep", lambda s: None)
    [it] = m.collect()
    for part in ("Target: 185.143.232.0/22", "Name: Iran DCI core", "Measurement ID: 7", "Probes reporting: 2",
                 "Avg RTT: 625.0ms", "Max RTT: 650.0ms"):
        assert part in it.content


@pytest.mark.parametrize("vix, level", [(27, "ELEVATED FEAR"), (35, "HIGH FEAR"), (45, "EXTREME FEAR")])
def test_vix_ladder_reaches_every_level(vix, level):
    from osint_monitor.collectors.finance_bridge import FinanceBridgeCollector
    c = FinanceBridgeCollector(agent_path="/nonexistent")
    items = c._extract_volatility_signals({"macro_data": [{"series_id": "VIXCLS", "current_value": vix,
                                                           "trend": "Increasing"}]}, "2026-09-30")
    assert items and items[0].title.startswith(f"VIX {level}")


def test_build_collectors_survives_a_failing_optional_import(monkeypatch):
    from osint_monitor.processors.pipeline import build_collectors
    real_import = builtins.__import__

    def failing(name, *a, **k):
        if name == "osint_monitor.collectors.govint":
            raise ImportError("simulated")
        return real_import(name, *a, **k)
    monkeypatch.setattr(builtins, "__import__", failing)
    names = {type(c).__name__ for c in build_collectors()}
    assert "CongressCollector" not in names and "IAEACollector" in names and "RSSCollector" in names
