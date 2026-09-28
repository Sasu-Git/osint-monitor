"""Collectors cannot hold a tier indefinitely: DNS lookups have a deadline, HTTP calls have
(connect, read) timeouts, and a per-collector time budget stops long target loops.
No network: resolvers and HTTP are replaced."""

import logging
import socket
import time

import pytest

from osint_monitor.collectors import infrastructure as infra
from osint_monitor.core.config import load_sources_config
from osint_monitor.processors.pipeline import COLLECTOR_TIERS, _run_single_collector


def test_hung_resolver_returns_none_within_the_deadline(monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", lambda *a, **k: time.sleep(5))
    started = time.monotonic()
    assert infra.resolve_with_deadline("kcna.kp", deadline=0.2) is None
    assert time.monotonic() - started < 1.0


def test_resolver_distinguishes_no_such_domain_from_an_answer(monkeypatch):
    def fake(host, *a, **k):
        if host == "gone.example":
            raise socket.gaierror("no such host")
        return [(None, None, None, None, ("10.0.0.1", 443)), (None, None, None, None, ("10.0.0.1", 443))]
    monkeypatch.setattr(socket, "getaddrinfo", fake)
    assert infra.resolve_with_deadline("gone.example") == []
    assert infra.resolve_with_deadline("up.example") == ["10.0.0.1"]


def dns_monitor(monkeypatch, domains, budget=None):
    monkeypatch.setattr(infra.time, "sleep", lambda s: None)          # skip the politeness pause
    info = {"desc": "portal", "country": "IR", "type": "government"}
    return infra.DNSHealthMonitor(domains={d: info for d in domains}, time_budget_seconds=budget)


def test_resolver_timeout_is_not_reported_as_a_down_domain(monkeypatch):
    mon = dns_monitor(monkeypatch, ["slow.ir", "ok.ir"])
    monkeypatch.setattr(infra.DNSHealthMonitor, "_check_dns",
                        staticmethod(lambda d: {"resolves": False, "ips": [], "timed_out": True} if d == "slow.ir"
                                     else {"resolves": True, "ips": ["10.0.0.1"]}))
    monkeypatch.setattr(infra.DNSHealthMonitor, "_check_http", staticmethod(
        lambda d: {"reachable": True, "status_code": 200, "response_time_ms": 5, "scheme": "https"}))
    titles = [i.title for i in mon.collect()]
    assert titles == ["Domain OK: ok.ir (portal, IR)"]
    assert not any("DOWN" in t for t in titles)


def test_dns_monitor_stops_when_its_budget_is_spent(monkeypatch):
    mon = dns_monitor(monkeypatch, [f"d{n}.ir" for n in range(10)], budget=0.25)
    checked = []

    def slow_dns(domain):
        checked.append(domain)
        end = time.monotonic() + 0.1              # time.sleep is stubbed out by dns_monitor
        while time.monotonic() < end:
            pass
        return {"resolves": True, "ips": ["10.0.0.1"]}
    monkeypatch.setattr(infra.DNSHealthMonitor, "_check_dns", staticmethod(slow_dns))
    monkeypatch.setattr(infra.DNSHealthMonitor, "_check_http", staticmethod(
        lambda d: {"reachable": True, "status_code": 200, "response_time_ms": 5, "scheme": "https"}))
    mon.start_budget()
    items = mon.collect()
    assert mon.budget_exceeded and 1 <= len(checked) < 10 and len(items) == len(checked)


def test_bgp_monitor_uses_bounded_timeouts_and_stops_on_budget(monkeypatch):
    calls = []

    class Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return {"data": {}}

    def fake_get(url, params=None, timeout=None):
        calls.append(timeout)
        time.sleep(0.05)
        return Resp()
    monkeypatch.setattr(infra.requests, "get", fake_get)
    mon = infra.BGPMonitor(time_budget_seconds=0.12)
    mon.start_budget()
    mon.collect()
    assert calls and all(t == infra._HTTP_TIMEOUT for t in calls)
    assert mon.budget_exceeded and len(calls) < 2 * len(mon.watched_asns)
    assert mon.current_target.startswith("AS") and not mon.current_target.startswith("ASAS")


def test_bgp_runs_in_the_warm_tier_and_budgets_fit_their_tiers():
    tiers = load_sources_config().tiers
    assert COLLECTOR_TIERS["BGPMonitor"] == "warm" and COLLECTOR_TIERS["DNSHealthMonitor"] == "hot"
    assert tiers.collector_budgets["DNSHealthMonitor"] < tiers.hot_interval_seconds
    assert tiers.collector_budgets["BGPMonitor"] < tiers.warm_interval_seconds


def test_runner_starts_the_clock_and_reports_a_partial_collection(monkeypatch, caplog):
    mon = dns_monitor(monkeypatch, [f"d{n}.ir" for n in range(5)], budget=0.0)
    monkeypatch.setattr(infra.DNSHealthMonitor, "_check_dns", staticmethod(lambda d: {"resolves": True, "ips": []}))
    with caplog.at_level(logging.WARNING, logger="osint_monitor.processors.pipeline"):
        items = _run_single_collector(mon)
    assert items == [] and "stopped early" in caplog.text


@pytest.mark.parametrize("budget", [None])
def test_collectors_without_a_budget_are_unbounded(monkeypatch, budget):
    mon = dns_monitor(monkeypatch, ["a.ir", "b.ir"], budget=budget)
    monkeypatch.setattr(infra.DNSHealthMonitor, "_check_dns", staticmethod(lambda d: {"resolves": True, "ips": []}))
    monkeypatch.setattr(infra.DNSHealthMonitor, "_check_http", staticmethod(
        lambda d: {"reachable": True, "status_code": 200, "response_time_ms": 5, "scheme": "https"}))
    mon.start_budget()
    assert len(mon.collect()) == 2 and not mon.budget_exceeded
