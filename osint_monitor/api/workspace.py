"""Situational-awareness workspace: Today / Map (one synchronised page), Priorities, the Development
preview, the map's GeoJSON and the personal-priority routes.

Reads the intelligence database read-only (api/workspace_views.py). Writes only personal priorities, to
the separate user-state database (core/user_state.py). Mutations take stable ids: a country id
(ISO 3166-1 alpha-3 or Natural Earth code) or an EventDomain value; anything else is rejected.
"""

from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse

from osint_monitor.api.pages import CONFIDENCE_LABELS, _read, _Unavailable, _unavailable, templates
from osint_monitor.core.user_state import Level, PriorityStore, Scope

router = APIRouter()
RANGE_LABELS = {"24h": "24 h", "3d": "72 h", "7d": "7 d"}


def store() -> PriorityStore:
    return PriorityStore()


def _filters(request: Request):
    from osint_monitor.api.workspace_views import Filters
    q = request.query_params
    return Filters(range=q.get("range", "24h"), domain=q.get("domain", ""), situation=q.get("situation", ""),
                   confidence=q.get("confidence", ""), lifecycle=q.get("lifecycle", ""), type=q.get("type", ""),
                   country=q.get("country", ""), show_muted=q.get("show_muted", "") in ("1", "true", "on"))


def _validate(scope: str, key: str) -> Scope:
    from osint_monitor.api.geo import CountryIndex
    from osint_monitor.api.workspace_views import DOMAINS
    try:
        s = Scope(scope)
    except ValueError:
        raise HTTPException(404, f"unknown priority scope {scope!r}; use one of {[x.value for x in Scope]}")
    if s is Scope.COUNTRY and key not in CountryIndex.load().countries:
        raise HTTPException(404, f"unknown country id {key!r} (use an ISO 3166-1 alpha-3 code)")
    if s is Scope.DOMAIN and key not in DOMAINS:
        raise HTTPException(404, f"unknown topic {key!r}; use one of {DOMAINS}")
    return s


def _level(value: str) -> Level:
    try:
        return Level(str(value).upper())
    except ValueError:
        raise HTTPException(422, f"level must be one of {[x.value for x in Level]}")


def priorities_context() -> dict:
    from osint_monitor.api.geo import CountryIndex
    from osint_monitor.api.workspace_views import DOMAINS
    index, st = CountryIndex.load(), store()
    countries = st.levels(Scope.COUNTRY)
    order = {Level.HIGH: 0, Level.LOW: 1, Level.MUTED: 2}
    return {
        "domain_levels": {d: st.levels(Scope.DOMAIN).get(d, Level.NORMAL).value for d in DOMAINS},
        "country_levels": sorted(((c, index.name(c), lv.value) for c, lv in countries.items()),
                                 key=lambda x: (order.get(Level(x[2]), 3), x[1])),
        "levels": [lv.value for lv in Level],
    }


def _workspace_context(request: Request, view: str) -> dict:
    from osint_monitor.api.workspace_views import LIFECYCLES, workspace
    from osint_monitor.core.database import Situation
    from osint_monitor.core.models import EventType
    f = _filters(request)
    page = _read(lambda s: workspace(s, f, store()))
    situations = _read(lambda s: sorted(((x.slug, x.title) for x in s.query(Situation)), key=lambda x: x[1]))
    return {"page": page, "view": view, "ranges": RANGE_LABELS, "confidences": list(CONFIDENCE_LABELS),
            "lifecycles": LIFECYCLES, "event_types": [t.value for t in EventType if t.value != "unknown"],
            "all_situations": situations, **priorities_context()}


async def _workspace(request: Request, view: str):
    try:
        context = _workspace_context(request, view)
    except _Unavailable as e:
        return _unavailable(request, "Today", e)
    template = "_feed.html" if request.headers.get("HX-Request") else "workspace.html"
    return templates.TemplateResponse(request, template, context)


@router.get("/", response_class=HTMLResponse)
async def today_page(request: Request):
    return await _workspace(request, "today")


@router.get("/map", response_class=HTMLResponse)
async def map_page(request: Request):
    return await _workspace(request, "map")


@router.get("/priorities", response_class=HTMLResponse)
async def priorities_page(request: Request):
    return templates.TemplateResponse(request, "priorities.html", priorities_context())


@router.get("/developments/{event_id}/preview", response_class=HTMLResponse)
async def development_preview(request: Request, event_id: int):
    from osint_monitor.api.development_views import development_page
    from osint_monitor.api.workspace_views import describe
    from osint_monitor.core.database import Event

    def build(s):
        page = development_page(s, event_id)
        if page is None:
            return None, None
        return page, describe(s, [s.get(Event, event_id)], store(), None)[event_id]
    try:
        page, item = _read(build)
    except _Unavailable as e:
        return _unavailable(request, "Development", e)
    status = 404 if page is None else 200
    return templates.TemplateResponse(request, "_dev_preview.html", {"page": page, "item": item, "event_id": event_id},
                                      status_code=status)


@router.get("/api/workspace/developments.geojson")
async def developments_geojson(request: Request, scope: str = ""):
    """Mapped Developments of the current selection. ``scope=situation`` with ``situation=<slug>`` returns every
    Development of that Situation regardless of age. Developments without a confirmed placement are left out
    and counted in ``unmapped``."""
    from osint_monitor.api.workspace_views import geojson
    f = _filters(request)
    try:
        data = _read(lambda s: geojson(s, f, store(), situation_window=scope == "situation"))
    except _Unavailable:
        return JSONResponse({"error": "database unavailable"}, status_code=503)
    return JSONResponse(data, media_type="application/geo+json")


# --- personal priorities (JSON) --------------------------------------------------------------------

@router.get("/api/priorities")
async def get_priorities():
    st = store()
    return {scope.value: {k: v.value for k, v in st.levels(scope).items()} for scope in Scope}


@router.put("/api/priorities/{scope}/{key}")
async def put_priority(scope: str, key: str, body: dict = Body(...)):
    s = _validate(scope, key)
    level = _level(body.get("level", ""))
    store().set(s, key, level)
    return {"scope": s.value, "key": key, "level": level.value}


@router.delete("/api/priorities/{scope}/{key}")
async def delete_priority(scope: str, key: str):
    s = _validate(scope, key)
    store().set(s, key, Level.NORMAL)
    return {"scope": s.value, "key": key, "level": Level.NORMAL.value}


@router.delete("/api/priorities")
async def reset_priorities(scope: str = ""):
    st = store()
    if scope:
        try:
            st.reset(Scope(scope))
        except ValueError:
            raise HTTPException(404, f"unknown priority scope {scope!r}")
    else:
        st.reset()
    return await get_priorities()


# --- personal priorities (HTMX forms; respond with the panel and tell the page to refresh) -------------

def _panel(request: Request) -> HTMLResponse:
    response = templates.TemplateResponse(request, "_priorities.html", priorities_context())
    response.headers["HX-Trigger"] = "priorities-changed"
    return response


@router.get("/ui/countries", response_class=HTMLResponse)
async def country_search(request: Request, q: str = ""):
    """Up to 12 countries whose name starts with, then contains, the query (or whose id is it)."""
    from osint_monitor.api.geo import CountryIndex
    index, levels = CountryIndex.load(), store().levels(Scope.COUNTRY)
    needle = q.strip().lower()
    hits = []
    if len(needle) >= 2:
        names = index.all()
        hits = ([c for c in names if c[0].lower() == needle or c[1].lower().startswith(needle)]
                + [c for c in names if needle in c[1].lower() and not c[1].lower().startswith(needle)
                   and c[0].lower() != needle])[:12]
    return templates.TemplateResponse(request, "_country_results.html", {
        "q": q, "levels": [lv.value for lv in Level],
        "results": [(cid, name, levels.get(cid, Level.NORMAL).value) for cid, name in hits]})


@router.post("/ui/priorities/reset", response_class=HTMLResponse)
async def reset_priorities_form(request: Request):
    form = await request.form()
    scope = form.get("scope", "")
    store().reset(Scope(scope) if scope in [s.value for s in Scope] else None)
    return _panel(request)


@router.post("/ui/priorities/{scope}/{key}", response_class=HTMLResponse)
async def set_priority_form(request: Request, scope: str, key: str):
    s = _validate(scope, key)
    form = await request.form()
    store().set(s, key, _level(form.get("level", "")))
    return _panel(request)
