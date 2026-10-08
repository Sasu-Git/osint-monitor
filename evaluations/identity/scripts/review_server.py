"""Local-only review page for the Development-identity gold (evaluation tool; no pipeline code is imported).

Serves review/review.html and a small JSON API on 127.0.0.1:
  GET  /api/state    cases (review/review-cases.json) + current owner verdicts
  POST /api/verdict  {"case", "verdict", "confidence", "boundary_reason", "note"}: validated, then saved at once to
                     review/owner-verdicts.yaml (atomic, deterministic; draft labels are never touched)

Usage: python evaluations/identity/scripts/review_server.py [--port 8765] [--verdicts PATH]
Then open http://127.0.0.1:8765/ . Nothing is frozen or hashed by this tool.
"""
from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verdicts as V  # noqa: E402

REVIEW = V.REVIEW
CASES_FILE = REVIEW / "review-cases.json"
PAGE = REVIEW / "review.html"


def load_cases() -> list[dict]:
    return json.loads(CASES_FILE.read_text(encoding="utf-8"))


class Handler(BaseHTTPRequestHandler):
    cases: list[dict] = []
    verdicts: dict[str, dict] = {}
    verdicts_path: Path = V.VERDICTS_FILE

    def _send(self, status: int, body: bytes, ctype: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, obj) -> None:
        self._send(status, json.dumps(obj, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def log_message(self, fmt, *args):          # quiet: one line per verdict only
        pass

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE.read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/state":
            self._json(200, {"cases": self.cases, "verdicts": self.verdicts,
                             "options": {"verdict": V.VERDICTS, "confidence": V.CONFIDENCE,
                                         "boundary_reason": V.BOUNDARY}})
        else:
            self._send(404, b"not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/verdict":
            return self._send(404, b"not found", "text/plain")
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
            cid = body.get("case")
            if cid not in self.verdicts:
                raise ValueError(f"unknown case id {cid!r}")
            entry = V.validate(body)
        except (ValueError, json.JSONDecodeError) as e:
            return self._json(400, {"error": str(e)})
        self.verdicts[cid] = entry
        V.save(self.verdicts, self.verdicts_path)
        print(f"saved {cid}: {entry['verdict']}", flush=True)
        self._json(200, {"case": cid, "entry": entry})


def main() -> int:
    global CASES_FILE, PAGE
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8765
    if "--dir" in sys.argv:                     # another review set, e.g. review-rev3 (gold revision 3)
        review = Path(__file__).resolve().parents[1] / sys.argv[sys.argv.index("--dir") + 1]
        CASES_FILE, PAGE = review / "review-cases.json", review / "review.html"
        Handler.verdicts_path = review / "owner-verdicts.yaml"
    Handler.cases = load_cases()
    ids = [c["case"] for c in Handler.cases]
    assert len(ids) == len(set(ids)), "duplicate case ids"
    if "--verdicts" in sys.argv:
        Handler.verdicts_path = Path(sys.argv[sys.argv.index("--verdicts") + 1])
    Handler.verdicts = V.load(ids, Handler.verdicts_path)
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    done = sum(1 for v in Handler.verdicts.values() if v["verdict"])
    print(f"Identity review: http://127.0.0.1:{port}/  ({done}/{len(ids)} reviewed; saving to {Handler.verdicts_path})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
