"""Source inventory (collectors/inventory.py, `python main.py inspect sources`): configured
identities and endpoints follow build_collectors() and config; enabled follows credentials;
observations come from a database opened read-only."""

import hashlib
import json
import sys
from datetime import datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.collectors import inventory as inv
from osint_monitor.core.config import SourceConfig, SourcesFileConfig, TwitterAccountConfig, load_sources_config
from osint_monitor.core.database import Base, RawItem, Source

GATED_ENV = {"FAA_NOTAM_KEY": "x", "COMTRADE_API_KEY": "x", "SAM_GOV_API_KEY": "x", "SPACETRACK_USER": "x",
             "SPACETRACK_PASS": "x", "RIPE_ATLAS_KEY": "x"}
NOW = datetime(2026, 9, 29, 12, 0)


def test_inventory_covers_every_collector_build_collectors_can_build(monkeypatch):
    from osint_monitor.processors.pipeline import build_collectors
    for k, v in GATED_ENV.items():
        monkeypatch.setenv(k, v)
    built = {type(c).__name__ for c in build_collectors()}
    listed = {e.collector for e in inv.configured_endpoints()}
    assert built == listed - {"ADSBCollector"}            # the OpenSky fallback is built only if adsb_tracks fails
    assert not built & {u.collector for u in inv.UNWIRED}


def test_rss_and_nitter_endpoints_follow_the_sources_config():
    config = load_sources_config()
    eps = inv.configured_endpoints(config)
    assert [e.source_name for e in eps if e.collector == "RSSCollector"] == [f.name for f in config.rss_feeds]
    assert {e.source_name for e in eps if e.collector == "NitterCollector"} == {
        "@" + a.username.lstrip("@") for a in config.twitter_accounts}


def test_one_identity_with_several_feeds_is_one_identity_and_several_endpoints():
    config = SourcesFileConfig(rss_feeds=[
        SourceConfig(name="BBC World", identity="BBC", url="https://feeds.bbci.co.uk/news/world/rss.xml"),
        SourceConfig(name="BBC Business", identity="BBC", url="https://feeds.bbci.co.uk/news/business/rss.xml"),
        SourceConfig(name="BBC Politics", identity="BBC", url="https://feeds.bbci.co.uk/news/politics/rss.xml",
                     enabled=False),
    ], twitter_accounts=[TwitterAccountConfig(username="@bellingcat")])
    rows = inv.build_inventory([e for e in inv.configured_endpoints(config) if e.family == "rss"], env={})
    s = inv.summarize(rows, None)
    assert s["identities_configured"] == 1 and s["endpoints_configured"] == 3
    assert s["endpoints_enabled"] == 2 and s["endpoints_disabled"] == 1
    assert [r.disabled_reason for r in rows if not r.enabled] == ["disabled in config/sources.yaml"]
    assert "@bellingcat" in {e.source_name for e in inv.configured_endpoints(config)}   # leading @ not doubled


def test_credentials_decide_enabled_and_alternative_modes_switch():
    eps = inv.configured_endpoints()
    firms = [e for e in eps if e.collector == "NASAFIRMSCollector"]
    no_key = {e.endpoint: inv.gate_status(e.gate, {})[0] for e in firms}
    with_key = {e.endpoint: inv.gate_status(e.gate, {"NASA_FIRMS_KEY": "k"})[0] for e in firms}
    assert no_key == {"area API": False, "global VIIRS 24h CSV (no key)": True}
    assert with_key == {"area API": True, "global VIIRS 24h CSV (no key)": False}
    acled = next(e for e in eps if e.collector == "ACLEDCollector")
    assert inv.gate_status(acled.gate, {"ACLED_EMAIL": "a"}) == (False, "ACLED_PASSWORD not set")
    congress = next(e for e in eps if e.collector == "CongressCollector")
    assert inv.gate_status(congress.gate, {})[0] is False      # built, but returns nothing without the key


def make_db(path, rows):
    engine = create_engine(f"sqlite:///{path}")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    sources = {}
    for n, (name, type_, url, title, hours_ago) in enumerate(rows):
        if name not in sources:
            sources[name] = Source(name=name, type=type_, url=url)
            session.add(sources[name])
            session.flush()
        session.add(RawItem(source_id=sources[name].id, title=title, url=url, content_hash=f"h{n}",
                            fetched_at=NOW - timedelta(hours=hours_ago)))
    session.commit()
    session.close()
    engine.dispose()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


ROWS = [
    ("BBC World", "rss", "https://www.bbc.co.uk/news/1", "Story one", 1),
    ("BBC World", "rss", "https://www.bbc.co.uk/news/2", "Story two", 50),
    ("DNS Health Monitor", "infrastructure", "https://kremlin.ru", "Domain OK: kremlin.ru", 2),
    ("DNS Health Monitor", "infrastructure", "https://president.ir", "DOMAIN DOWN: president.ir", 100),
    ("NASA FIRMS", "structured_api", "https://firms.modaps.eosdis.nasa.gov/map/", "Thermal anomaly (ukraine)", 3),
    ("bbc world", "rss", "https://www.bbc.co.uk/news/3", "Old alias", 4),
]


def test_observations_are_read_only_and_attributed_per_endpoint(tmp_path):
    db = tmp_path / "copy.db"
    make_db(db, ROWS)
    before = digest(db)
    obs = inv.read_observations(str(db))
    assert digest(db) == before and not (tmp_path / "copy.db-wal").exists()
    assert obs.now == NOW - timedelta(hours=1) and obs.sources["BBC World"].items == 2
    rows = {r.endpoint.key: r for r in inv.build_inventory(inv.configured_endpoints(), obs, env={})}
    assert rows["BBC World :: RSS feed"].items == 2 and rows["BBC World :: RSS feed"].state == inv.ACTIVE
    assert rows["BBC World :: RSS feed"].last_24h == 1
    assert rows["DNS Health Monitor :: DNS lookup + HEAD [kremlin.ru]"].items == 1
    assert rows["DNS Health Monitor :: DNS lookup + HEAD [tass.com]"].state == inv.NO_OBSERVATIONS
    # FIRMS without a key: the fallback CSV is the only enabled mode and gets the items;
    # the disabled area API is not credited with them
    assert rows["NASA FIRMS :: global VIIRS 24h CSV (no key)"].items == 1
    assert rows["NASA FIRMS :: area API [ukraine]"].state == inv.DISABLED
    assert rows["NASA FIRMS :: area API [ukraine]"].items is None
    s = inv.summarize(list(rows.values()), obs)
    assert s["unconfigured_source_names"] == ["bbc world"]
    assert s["coverage_days"] < 7


def test_reading_a_wal_database_creates_no_side_files(tmp_path):
    import sqlite3
    db = tmp_path / "wal.db"
    make_db(db, ROWS)
    conn = sqlite3.connect(db)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.close()                                         # last connection: WAL checkpointed and removed
    assert not (tmp_path / "wal.db-wal").exists()
    before = digest(db)
    assert inv.read_observations(str(db)).sources["BBC World"].items == 2
    assert digest(db) == before
    assert not (tmp_path / "wal.db-wal").exists() and not (tmp_path / "wal.db-shm").exists()


def test_log_evidence_marks_recurrent_errors_without_judging_silence(tmp_path):
    log = tmp_path / "daemon.out.log"
    log.write_text("\n".join(["  [err] @NATO: all Nitter instances failed (last: timeout)"] * 4
                             + ["  [ok] Lawfare: 0 items"] * 4
                             + ["  [ok] UN Consolidated: 50 entries", "  [skip] X-ForYou: Chrome CDP not available"]),
                   encoding="utf-8")
    evidence = inv.read_log(str(log))
    assert evidence["@NATO"].err == 4 and evidence["Lawfare"].returned == 0
    assert evidence["UN Consolidated"].returned == 50 and evidence["X-ForYou"].skip == 1
    db = tmp_path / "copy.db"
    make_db(db, ROWS)
    rows = {r.endpoint.source_name: r for r in inv.build_inventory(
        inv.configured_endpoints(), inv.read_observations(str(db)), evidence, env={})}
    assert rows["@NATO"].state == inv.ERRORS and "all Nitter instances failed" in rows["@NATO"].evidence
    assert rows["Lawfare"].state == inv.NO_OBSERVATIONS           # silent, not declared broken
    assert "0 items returned" in rows["Lawfare"].evidence


def test_naming_issues_are_reported_not_merged(tmp_path):
    db = tmp_path / "copy.db"
    make_db(db, ROWS)
    eps = inv.configured_endpoints()
    issues = inv.naming_issues(eps, inv.read_observations(str(db)))
    assert not any("government_documents" in i for i in issues)          # one stored name per publisher now
    assert any("US State Department is stored under 2 source names by different collectors" in i for i in issues)
    assert not any(i.startswith("ANSA is stored") for i in issues)                  # declared feeds of one identity
    assert any("spelling variants" in i and "'bbc world'" in i and "'BBC World'" in i for i in issues)
    assert any("database sources names 'bbc world'" in i for i in issues)


def test_inspect_sources_cli_is_read_only(tmp_path, monkeypatch, capsys):
    from osint_monitor import cli
    db = tmp_path / "copy.db"
    make_db(db, ROWS)
    before = digest(db)
    monkeypatch.setattr(sys, "argv", ["main.py", "inspect", "sources", "--db", str(db), "--json"])
    cli.main()
    data = json.loads(capsys.readouterr().out)
    assert digest(db) == before
    s = data["summary"]
    assert s["endpoints_configured"] == len(data["endpoints"]) and s["endpoints_enabled"] + s["endpoints_disabled"] == \
        s["endpoints_configured"]
    assert s["identities_observed"] >= 2 and data["unwired"]
    monkeypatch.setattr(sys, "argv", ["main.py", "inspect", "sources", "--db", str(db)])
    cli.main()
    text = capsys.readouterr().out
    assert text.startswith("Source identities") and "Endpoints" in text and "[rss]" in text
    monkeypatch.setattr(sys, "argv", ["main.py", "inspect", "sources", "--db", str(db), "--since", "7d", "--active-only"])
    cli.main()
    assert "Reuters World" not in capsys.readouterr().out.split("Present in code")[0]
    assert digest(db) == before


def test_since_parser_rejects_nonsense():
    from osint_monitor.cli import _parse_since
    assert _parse_since("24h") == timedelta(hours=24) and _parse_since("7d") == timedelta(days=7)
    with pytest.raises(SystemExit):
        _parse_since("soon")
