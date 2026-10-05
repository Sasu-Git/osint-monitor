"""Server-rendered reading pages: Today, Development detail, Situations, Situation detail.

Read-only. View models come from api/development_views.py and api/situation_views.py; the
templates only format what those return. Filters on Today work as a plain GET form and are
enhanced with HTMX (the list is swapped in place when the request carries HX-Request).
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

logger = logging.getLogger(__name__)
router = APIRouter()
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "web" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

UNCLASSIFIED = {None, "", "unknown"}
CONFIDENCE_LABELS = {"confirmed": "Confirmed", "probable": "Probable", "possible": "Possible",
                     "disputed": "Disputed", "unverified": "Unverified"}
SOURCE_ROLE_LABELS = {"primary_official": "Official source", "wire": "Wire agency",
                      "independent_reporting": "Independent reporting", "specialist_reporting": "Specialist outlet",
                      "analysis": "Analysis", "osint": "OSINT account", "social": "Social media", "unknown": None}
GROUP_LABELS = {"official": "Official / primary", "independent": "Independent reporting",
                "derivative": "Derivative and syndicated coverage", "commentary": "Commentary and analysis",
                "undetermined": "Provenance not determined"}
SUMMARY_METHOD_LABELS = {"extractive-leads-v1": "Summary: lead sentences selected verbatim from independent reports",
                         "llm": "Summary: written by a language model from these reports only"}
EVIDENCE_LABELS = {"primary": "Primary", "firsthand": "First-hand", "independent": "Independent report",
                   "derivative": "Derivative", "commentary": "Commentary"}


def type_label(value: str | None) -> str:
    return "Unclassified" if value in UNCLASSIFIED else value.replace("_", " ").capitalize()


def domain_label(value: str | None) -> str | None:
    return None if value in UNCLASSIFIED else value.replace("_", " ").capitalize()


def when(value: datetime | None, with_date: bool = True) -> str:
    if value is None:
        return "time unknown"
    return value.strftime("%d %b %Y, %H:%M UTC" if with_date else "%H:%M UTC").lstrip("0")


templates.env.filters.update(
    type_label=type_label, domain_label=domain_label, when=when,
    conf_label=lambda v: CONFIDENCE_LABELS.get(v or "", "Not assessed"),
    role_label=lambda v: SOURCE_ROLE_LABELS.get(v or "unknown"),
    evidence_label=lambda v: EVIDENCE_LABELS.get(v or ""),
    humanize=lambda v: (v or "").replace("_", " ").capitalize(),
    group_label=lambda k: GROUP_LABELS.get(k, k),
    summary_method=lambda m: SUMMARY_METHOD_LABELS.get(m or "", f"Summary method: {m}"),
)


def _session():
    from osint_monitor.core.database import get_session
    return get_session()


def _unavailable(request: Request, page: str, error: Exception) -> HTMLResponse:
    logger.error(f"{page} page: database unavailable: {error}")
    return templates.TemplateResponse(request, "unavailable.html", {"page": page}, status_code=503)


class _Unavailable(Exception):
    pass


def _read(fn):
    """Run a read-only view builder in its own session; any database failure (missing file,
    lock, corrupt schema, even opening the session) becomes _Unavailable."""
    try:
        session = _session()
    except Exception as e:
        raise _Unavailable(e) from e
    try:
        return fn(session)
    except Exception as e:
        raise _Unavailable(e) from e
    finally:
        session.close()


@router.get("/", response_class=HTMLResponse)
async def today_page(request: Request, range: str = "24h", domain: str = "", situation: str = "",
                     confidence: str = ""):
    from osint_monitor.api.development_views import TIME_RANGES, today
    try:
        page = _read(lambda s: today(s, range_key=range, domain=domain, situation=situation, confidence=confidence))
    except _Unavailable as e:
        return _unavailable(request, "Today", e)
    context = {"page": page, "ranges": list(TIME_RANGES), "confidences": list(CONFIDENCE_LABELS)}
    template = "_today_results.html" if request.headers.get("HX-Request") else "today.html"
    return templates.TemplateResponse(request, template, context)


@router.get("/developments/{event_id}", response_class=HTMLResponse)
async def development_detail_page(request: Request, event_id: int):
    from osint_monitor.api.development_views import MIN_INDEPENDENT_SOURCES, development_page
    try:
        page = _read(lambda s: development_page(s, event_id))
    except _Unavailable as e:
        return _unavailable(request, "Development", e)
    if page is None:
        return templates.TemplateResponse(request, "development_detail.html", {"page": None, "event_id": event_id},
                                          status_code=404)
    return templates.TemplateResponse(request, "development_detail.html",
                                      {"page": page, "event_id": event_id, "min_sources": MIN_INDEPENDENT_SOURCES})


@router.get("/situations", response_class=HTMLResponse)
async def situations_page(request: Request):
    from osint_monitor.api.situation_views import list_situations
    try:
        situations = _read(list_situations)
    except _Unavailable as e:
        return _unavailable(request, "Situations", e)
    return templates.TemplateResponse(request, "situations.html", {"situations": situations})


@router.get("/situations/{slug}", response_class=HTMLResponse)
async def situation_detail_page(request: Request, slug: str):
    from osint_monitor.api.situation_views import situation_detail
    try:
        detail = _read(lambda s: situation_detail(s, slug))
    except _Unavailable as e:
        return _unavailable(request, "Situation", e)
    status = 404 if detail is None else 200
    return templates.TemplateResponse(request, "situation_detail.html", {"situation": detail, "slug": slug},
                                      status_code=status)
