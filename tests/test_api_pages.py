"""Every dashboard page renders (guards against template API drift in Starlette).

TestClient is used without its context manager, so the startup hook (init_db)
does not run and no database is touched; the pages load their data via /api.
"""

import pytest
from fastapi.testclient import TestClient

from osint_monitor.api.app import app

PAGES = ["/", "/events", "/events/1", "/entities", "/entities/1", "/map", "/graph", "/briefings",
         "/alerts", "/indicators", "/claims", "/timeline", "/stix"]


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.mark.parametrize("path", PAGES)
def test_page_renders(client, path):
    r = client.get(path)
    assert r.status_code == 200
    assert "<html" in r.text.lower()
