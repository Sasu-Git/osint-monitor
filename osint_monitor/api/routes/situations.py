"""Situations API: read-only evidence view (see api/situation_views.py for the contract)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from osint_monitor.api.situation_views import SituationDetail, SituationSummary, list_situations, situation_detail
from osint_monitor.core.database import get_session

router = APIRouter()


@router.get("", response_model=list[SituationSummary])
def get_situations():
    session = get_session()
    try:
        return list_situations(session)
    finally:
        session.close()


@router.get("/{slug}", response_model=SituationDetail)
def get_situation(slug: str):
    session = get_session()
    try:
        detail = situation_detail(session, slug)
    finally:
        session.close()
    if detail is None:
        raise HTTPException(status_code=404, detail=f"No situation {slug!r}")
    return detail
