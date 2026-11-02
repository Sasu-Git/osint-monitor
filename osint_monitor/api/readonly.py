"""Read-only web deployment (OSINT_DB_READONLY=1): which requests the web server refuses.

The intelligence DB is already opened with SQLite mode=ro (core/database.py), so a write would fail anyway. This
gate refuses those requests up front with a deliberate 403, and also refuses what mode=ro cannot stop:

- every POST / PUT / PATCH / DELETE, except personal priorities, which live in the separate user-state DB
  (core/user_state.py): alert acknowledge, ingest, webhook, briefing generation, ACH, IMINT, pause / resume / toggle;
- GET routes that call a language model (CIR report, ACH markdown, LLM-scored indicators);
- the daemon control API, including its status: in a separate web worktree its pause flag is not the daemon's.
"""

from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse

READ_METHODS = {"GET", "HEAD", "OPTIONS"}
# Personal priorities: written to the user-state DB only (OSINT_USER_STATE_DB)
USER_STATE_PREFIXES = ("/api/priorities", "/ui/priorities")
BLOCKED_GET_PREFIXES = ("/api/daemon", "/api/intel/report/cir/", "/api/intel/ach/")


def refusal(method: str, path: str, query: dict) -> str | None:
    """Why a request is refused in read-only mode, or None when it is allowed."""
    if method.upper() not in READ_METHODS:
        if path.startswith(USER_STATE_PREFIXES):
            return None
        return "writes to the intelligence database and operational controls are disabled"
    if path.startswith(BLOCKED_GET_PREFIXES):
        return "operational and language-model routes are disabled"
    if path.startswith("/api/intel/indicators") and str(query.get("use_llm", "")).lower() in {"1", "true", "yes"}:
        return "language-model scoring is disabled"
    return None


async def readonly_gate(request: Request, call_next):
    """HTTP middleware: 403 for refused requests when OSINT_DB_READONLY is set."""
    from osint_monitor.core.database import db_readonly

    if db_readonly():
        reason = refusal(request.method, request.url.path, dict(request.query_params))
        if reason:
            return JSONResponse({"error": f"Read-only deployment: {reason}.", "read_only": True}, status_code=403)
    return await call_next(request)
