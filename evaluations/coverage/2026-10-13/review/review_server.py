"""Local-only blind review for the coverage-recoverability sample (evaluation tool; no pipeline code is imported).

Serves review.html and a small JSON API on 127.0.0.1:
  GET  /api/state          blind cases (review-cases.json) + current owner labels
  POST /api/label          {"case", "label", "partners", "note"}: validated, then saved at once to owner-labels.yaml
  GET  /api/reveal?case=ID the stratum and bucket reason from key.json, only once that case has a saved label

Labels: SHOULD_JOIN (the item belongs in one Development with at least one shown partner; name which), SHOULD_NOT_JOIN,
AMBIGUOUS. The frozen files (sample-manifest.json, review-cases.json, key.json) are never written.

Usage: python review_server.py [--port 8766]   then open http://127.0.0.1:8766/
"""
from __future__ import annotations

import json
import os
import sys
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import yaml

HERE = Path(__file__).resolve().parent
LABELS_FILE = HERE / "owner-labels.yaml"
LABELS = ("SHOULD_JOIN", "SHOULD_NOT_JOIN", "AMBIGUOUS")
HEADER = ("# Owner labels for the coverage-recoverability sample (see review_server.py for the fields).\n"
          "# The sample, partners and key are frozen in sample-manifest.json / FREEZE.md.\n")
_lock = threading.Lock()


def load_labels(case_ids):
    try:
        raw = yaml.safe_load(LABELS_FILE.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        raw = {}
    return {c: {f: (raw.get(c) or {}).get(f) for f in ("label", "partners", "note", "labelled_at")} for c in case_ids}


def save_labels(labels):
    with _lock:
        tmp = LABELS_FILE.with_suffix(".tmp")
        tmp.write_text(HEADER + yaml.safe_dump(dict(sorted(labels.items())), allow_unicode=True, sort_keys=True),
                       encoding="utf-8")
        os.replace(tmp, LABELS_FILE)


class Handler(BaseHTTPRequestHandler):
    cases: dict = {}
    key: dict = {}
    labels: dict = {}

    def _send(self, status, body, ctype):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status, obj):
        self._send(status, json.dumps(obj, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        url = urlparse(self.path)
        if url.path in ("/", "/index.html"):
            self._send(200, (HERE / "review.html").read_bytes(), "text/html; charset=utf-8")
        elif url.path == "/api/state":
            self._json(200, {"cases": list(self.cases.values()), "labels": self.labels, "options": LABELS})
        elif url.path == "/api/reveal":
            cid = (parse_qs(url.query).get("case") or [""])[0]
            if cid not in self.cases:
                return self._json(404, {"error": "unknown case"})
            if not self.labels[cid]["label"]:
                return self._json(403, {"error": "label the case first"})
            self._json(200, self.key[cid])
        else:
            self._send(404, b"not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/label":
            return self._send(404, b"not found", "text/plain")
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
            cid, label = body.get("case"), body.get("label")
            if cid not in self.cases:
                raise ValueError(f"unknown case {cid!r}")
            if label not in LABELS:
                raise ValueError(f"label must be one of {LABELS}")
            shown = [p["id"] for p in self.cases[cid]["partners"]]
            partners = [int(p) for p in body.get("partners") or []]
            if any(p not in shown for p in partners):
                raise ValueError("partners must be among the shown partner ids")
            if label == "SHOULD_JOIN" and not partners:
                raise ValueError("SHOULD_JOIN needs at least one partner")
            if label != "SHOULD_JOIN":
                partners = []
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            return self._json(400, {"error": str(e)})
        self.labels[cid] = {"label": label, "partners": partners or None, "note": (body.get("note") or "").strip() or None,
                            "labelled_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        save_labels(self.labels)
        print(f"saved {cid}: {label}", flush=True)
        self._json(200, {"case": cid, "entry": self.labels[cid]})


def main() -> int:
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8766
    cases = json.loads((HERE / "review-cases.json").read_text(encoding="utf-8"))
    Handler.cases = {c["case"]: c for c in cases}
    Handler.key = json.loads((HERE / "key.json").read_text(encoding="utf-8"))
    Handler.labels = load_labels(list(Handler.cases))
    print(f"{len(cases)} cases, {sum(1 for v in Handler.labels.values() if v['label'])} labelled; "
          f"http://127.0.0.1:{port}/", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
