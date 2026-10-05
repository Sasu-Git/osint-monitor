"""Localhost-only owner review UI for the Phase 3 Development relation gold (an annotation tool, not runtime logic).

Cases come from evaluations/relations/review/cases.json, the structured source the review sheet
(relation-review-sheet.md) is rendered from. Owner decisions are written to owner-verdicts.yaml, one case at a time,
atomically. Draft labels (draft-labels.json) are shown only for cases the owner has already decided. Nothing under
evaluations/relations/holdout/ is ever read, and no database is opened.

Run standalone (no database, no daemon):
    python -m uvicorn osint_monitor.api.relation_review:standalone_app --host 127.0.0.1 --port 8012
It is also mounted at /eval/relations in the main app (``python main.py serve``).
"""

from __future__ import annotations

import json
import os
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

import yaml
from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

REPO = Path(__file__).resolve().parents[2]
RELATIONS_DIR = REPO / "evaluations" / "relations"
REVIEW_DIR = RELATIONS_DIR / "review"
HOLDOUT_DIR = RELATIONS_DIR / "holdout"
TEMPLATES = Jinja2Templates(directory=str(REPO / "web" / "templates"))

DIRECTED = ("reaction_to", "follow_up_to", "caused_by")
SYMMETRIC = ("same_calamity_lifecycle", "same_visit_or_summit", "same_attack_wave", "co_caused_with")
RELATIONS = SYMMETRIC[:3] + DIRECTED + SYMMETRIC[3:]
IDENTITY = "SAME_DEVELOPMENT_SUSPECTED"
VERDICTS = ("NO_RELATION",) + RELATIONS + ("AMBIGUOUS", IDENTITY)
DIRECTIONS = ("A->B", "B->A")
FILTERS = ("all", "unreviewed", "reviewed", "ambiguous", "identity", "disagree")
# keyboard shortcuts, shown on the page
SHORTCUTS = {"NO_RELATION": "n", "same_calamity_lifecycle": "1", "same_visit_or_summit": "2", "same_attack_wave": "3",
             "reaction_to": "4", "follow_up_to": "5", "caused_by": "6", "co_caused_with": "7", "AMBIGUOUS": "a",
             IDENTITY: "i"}
HEADER = ("# Owner verdicts for the Phase 3 relation gold, one entry per case (written by the review UI,\n"
          "# /eval/relations). label: NO_RELATION | a relation type | AMBIGUOUS | SAME_DEVELOPMENT_SUSPECTED.\n"
          "# direction (A->B | B->A, source -> target) only for reaction_to, follow_up_to, caused_by.\n"
          "# Notes are kept verbatim. Regenerating the review sheet never overwrites this file.\n")

_lock = threading.Lock()


def _commentary_rule():
    from osint_monitor.processors.classification.rules import COMMENTARY_TITLE
    return COMMENTARY_TITLE


# --- data ------------------------------------------------------------------------------------------------------------

class ReviewStore:
    """Cases, blind drafts and owner verdicts. Reads only the review directory."""

    def __init__(self, review_dir: Path = REVIEW_DIR):
        self.dir = Path(review_dir).resolve()
        if HOLDOUT_DIR.resolve() in (self.dir, *self.dir.parents):
            raise ValueError("the sealed holdout is never loaded by the review UI")
        data = json.loads((self.dir / "cases.json").read_text(encoding="utf-8"))
        self.cases = {c["case"]: c for c in sorted(data["cases"], key=lambda c: c["case"])}
        if len(self.cases) != len(data["cases"]):
            raise ValueError("duplicate case IDs in cases.json")
        self.order = list(self.cases)
        self._drafts = json.loads((self.dir / "draft-labels.json").read_text(encoding="utf-8"))
        self.verdicts_path = self.dir / "owner-verdicts.yaml"

    # verdicts
    def load_verdicts(self) -> dict:
        if not self.verdicts_path.exists():
            return {}
        raw = yaml.safe_load(self.verdicts_path.read_text(encoding="utf-8")) or {}
        return {k: v for k, v in raw.items() if isinstance(v, dict)}

    def verdict(self, cid: str) -> dict | None:
        v = self.load_verdicts().get(cid)
        return v if v and v.get("label") else None

    def save(self, cid: str, label: str, direction: str | None, note: str | None) -> dict:
        if cid not in self.cases:
            raise KeyError(cid)
        entry = validate(label, direction, note)
        with _lock:
            current = self.load_verdicts()
            current[cid] = entry
            text = HEADER + yaml.safe_dump({k: current[k] for k in sorted(current)}, sort_keys=False,
                                           allow_unicode=True, width=10_000, default_flow_style=None)
            fd, tmp = tempfile.mkstemp(dir=self.dir, prefix=".owner-verdicts.", suffix=".tmp")
            try:
                with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
                    f.write(text)
                os.replace(tmp, self.verdicts_path)
            finally:
                if os.path.exists(tmp):
                    os.remove(tmp)
        return entry

    # drafts: only after the owner has decided
    def draft_after_verdict(self, cid: str) -> dict | None:
        return self._drafts.get(cid) if self.verdict(cid) else None

    def agrees(self, cid: str, verdicts: dict | None = None) -> bool | None:
        v = (verdicts if verdicts is not None else self.load_verdicts()).get(cid)
        if not v or not v.get("label"):
            return None
        d = self._drafts[cid]
        draft_label = IDENTITY if d.get("identity_flag") == IDENTITY else d["label"]
        draft_dir = d["direction"] if d["direction"] in DIRECTIONS else None
        return v["label"] == draft_label and v.get("direction") == draft_dir

    # navigation
    def filtered(self, flt: str, rel: str | None = None) -> list[str]:
        vs = self.load_verdicts()
        done = lambda c: bool(vs.get(c, {}).get("label"))
        keep = {
            "all": lambda c: True,
            "unreviewed": lambda c: not done(c),
            "reviewed": done,
            "ambiguous": lambda c: vs.get(c, {}).get("label") == "AMBIGUOUS",
            "identity": lambda c: vs.get(c, {}).get("label") == IDENTITY,
            "disagree": lambda c: self.agrees(c, vs) is False,
        }.get(flt, lambda c: True)
        out = [c for c in self.order if keep(c)]
        if rel:
            out = [c for c in out if vs.get(c, {}).get("label") == rel]
        return out

    def summary(self) -> dict:
        vs = {c: v for c, v in self.load_verdicts().items() if v.get("label") and c in self.cases}
        counts = {k: sum(1 for v in vs.values() if v["label"] == k) for k in VERDICTS}
        disagreements = [c for c in sorted(vs) if self.agrees(c, vs) is False]
        return {"total": len(self.cases), "reviewed": len(vs), "remaining": len(self.cases) - len(vs),
                "counts": counts, "identity": counts[IDENTITY], "ambiguous": counts["AMBIGUOUS"],
                "disagreements": disagreements,
                "positives": {r: counts[r] for r in RELATIONS}}


def validate(label: str, direction: str | None, note: str | None) -> dict:
    if label not in VERDICTS:
        raise ValueError(f"unknown verdict {label!r}")
    direction = direction or None
    if label in DIRECTED:
        if direction not in DIRECTIONS:
            raise ValueError(f"{label} needs a direction (A->B or B->A)")
    elif direction is not None:
        raise ValueError(f"{label} takes no direction")
    return {"label": label, "direction": direction, "identity_flag": IDENTITY if label == IDENTITY else None,
            "note": note if note not in (None, "") else None,
            "reviewed_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}


# --- presentation ----------------------------------------------------------------------------------------------------

def side_view(o: dict) -> dict:
    rule = _commentary_rule()
    surfaced = bool(o["system_developments"])
    return {
        "id": o["id"], "first": str(o["first"] or "")[:16], "last": str(o["last"] or "")[:16],
        "actors": o["actors"], "places": o["places"], "situations": o["situations"],
        "sources": o["sources"], "members": len(o["members"]), "langs": o.get("langs") or [],
        "system": ", ".join(f"D{d}" for d in o["system_developments"]) if surfaced else None,
        "single_source": len(o["sources"]) == 1, "roundup_only": o.get("roundup_only"),
        "evidence": [{**e, "published_at": str(e["published_at"] or "")[:16],
                      "commentary": bool(rule.search(e["title"]))} for e in o["evidence"]],
    }


# --- routes ----------------------------------------------------------------------------------------------------------

def localhost_only(request: Request) -> None:
    host = request.client.host if request.client else ""
    if host not in ("127.0.0.1", "::1", "localhost", "testclient"):
        raise HTTPException(status_code=403, detail="the relation review UI is localhost-only")


router = APIRouter(dependencies=[Depends(localhost_only)])
_store: ReviewStore | None = None


def get_store() -> ReviewStore:
    global _store
    if _store is None:
        _store = ReviewStore()
    return _store


def _q(flt: str, rel: str | None) -> str:
    return urlencode({k: v for k, v in (("filter", flt), ("rel", rel)) if v and v != "all"})


def _nav(store: ReviewStore, cid: str, flt: str, rel: str | None) -> dict:
    ids = store.filtered(flt, rel)
    if cid in ids:
        i = ids.index(cid)
        prev_id, next_id = (ids[i - 1] if i > 0 else None), (ids[i + 1] if i + 1 < len(ids) else None)
    else:                                   # the case left the filter (e.g. just reviewed under "unreviewed")
        later = [c for c in ids if c > cid]
        earlier = [c for c in ids if c < cid]
        prev_id, next_id = (earlier[-1] if earlier else None), (later[0] if later else None)
    return {"prev": prev_id, "next": next_id, "position": (ids.index(cid) + 1) if cid in ids else None,
            "in_filter": len(ids)}


def _case_context(store: ReviewStore, cid: str, flt: str, rel: str | None, error: str | None = None) -> dict:
    c = store.cases[cid]
    verdict = store.verdict(cid)
    s = store.summary()
    return {"cid": cid, "a": side_view(c["a"]), "b": side_view(c["b"]), "verdict": verdict,
            "verdicts": VERDICTS, "directed": DIRECTED, "shortcuts": SHORTCUTS, "filters": FILTERS,
            "relations": RELATIONS, "flt": flt, "rel": rel, "q": _q(flt, rel), "nav": _nav(store, cid, flt, rel),
            "reviewed": s["reviewed"], "total": s["total"], "remaining": s["remaining"], "error": error}


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
def start(request: Request, filter: str = "unreviewed", rel: str | None = None):
    store = get_store()
    ids = store.filtered(filter, rel)
    if not ids:
        return RedirectResponse("/eval/relations/summary", status_code=303)
    return RedirectResponse(f"/eval/relations/case/{ids[0]}?{_q(filter, rel)}", status_code=303)


@router.get("/summary", response_class=HTMLResponse)
def summary(request: Request):
    store = get_store()
    return TEMPLATES.TemplateResponse(request, "relation_review_summary.html",
                                      {"s": store.summary(), "relations": RELATIONS, "verdicts": VERDICTS})


@router.get("/case/{cid}", response_class=HTMLResponse)
def case_page(request: Request, cid: str, filter: str = "all", rel: str | None = None):
    store = get_store()
    if cid not in store.cases:
        raise HTTPException(status_code=404, detail=f"no case {cid}")
    return TEMPLATES.TemplateResponse(request, "relation_review.html", _case_context(store, cid, filter, rel))


@router.post("/case/{cid}", response_class=HTMLResponse)
def save_case(request: Request, cid: str, label: str = Form(...), direction: str = Form(""),
              note: str = Form(""), filter: str = Form("all"), rel: str = Form("")):
    store = get_store()
    if cid not in store.cases:
        raise HTTPException(status_code=404, detail=f"no case {cid}")
    rel = rel or None
    try:
        store.save(cid, label, direction or None, note)
    except ValueError as exc:
        ctx = _case_context(store, cid, filter, rel, error=str(exc))
        return TEMPLATES.TemplateResponse(request, "relation_review_panel.html", ctx, status_code=422)
    if request.headers.get("HX-Request"):
        return TEMPLATES.TemplateResponse(request, "relation_review_panel.html", _case_context(store, cid, filter, rel))
    return RedirectResponse(f"/eval/relations/case/{cid}?{_q(filter, rel)}", status_code=303)


@router.get("/case/{cid}/draft", response_class=HTMLResponse)
def reveal_draft(request: Request, cid: str):
    store = get_store()
    if cid not in store.cases:
        raise HTTPException(status_code=404, detail=f"no case {cid}")
    draft = store.draft_after_verdict(cid)
    if draft is None:
        raise HTTPException(status_code=403, detail="the draft is shown only after your verdict")
    return TEMPLATES.TemplateResponse(request, "relation_review_draft.html",
                                      {"cid": cid, "draft": draft, "agrees": store.agrees(cid)})


standalone_app = FastAPI(title="Relation gold review (localhost)")
standalone_app.include_router(router, prefix="/eval/relations")


@standalone_app.get("/")
def _root():
    return RedirectResponse("/eval/relations", status_code=303)
