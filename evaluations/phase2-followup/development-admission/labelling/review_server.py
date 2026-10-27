"""Local-only blind review for the Development-admission labels L1-L3 (evaluation tool; no pipeline code imported).

    python review_server.py [--port 8781] [--reviewer owner]     then open http://127.0.0.1:8781/

Serves review.html and a JSON API on 127.0.0.1 only:
  GET  /api/state   the blind cases (review-cases.json) and the current labels
  POST /api/label   {"case", "label", "note"}: validated, then saved at once to owner-labels.yaml

Labels (identity contract): SAME_OCCURRENCE, DIFFERENT_OCCURRENCE, AMBIGUOUS. The key (key.json: label set,
Development, stratum) is never loaded or served, so nothing about why a case was sampled reaches the page.

Provenance: each entry records reviewer and time; changing a verdict keeps the previous one in the entry's history.
One reviewer per case: a label from a different reviewer on an already-labelled case is refused. The frozen files
(review-cases.json, key.json, FREEZE-LABELLING.json) are never written.
"""
from __future__ import annotations

import json
import os
import sys
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import yaml

HERE = Path(__file__).resolve().parent
LABELS = ("SAME_OCCURRENCE", "DIFFERENT_OCCURRENCE", "AMBIGUOUS")
HEADER = ("# Owner labels for the Development-admission review (see review_server.py for the fields).\n"
          "# Cases and key are frozen in FREEZE-LABELLING.json.\n")
FIELDS = ("label", "note", "reviewer", "labelled_at", "history")
_lock = threading.Lock()


def load_labels(path: Path, case_ids):
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        raw = {}
    return {c: {f: (raw.get(c) or {}).get(f) for f in FIELDS} for c in case_ids}


def save_labels(path: Path, labels):
    with _lock:
        tmp = path.with_suffix(".tmp")
        done = {c: v for c, v in labels.items() if v.get("label")}
        tmp.write_text(HEADER + yaml.safe_dump(dict(sorted(done.items())), allow_unicode=True, sort_keys=True),
                       encoding="utf-8")
        os.replace(tmp, path)


class Handler(BaseHTTPRequestHandler):
    cases: dict = {}
    labels: dict = {}
    reviewer: str = "owner"
    labels_file: Path = HERE / "owner-labels.yaml"

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
            self._json(200, {"cases": list(self.cases.values()), "labels": self.labels, "options": LABELS,
                             "reviewer": self.reviewer})
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
            prior = self.labels[cid]
            if prior.get("label") and prior.get("reviewer") and prior["reviewer"] != self.reviewer:
                raise ValueError(f"{cid} is already labelled by {prior['reviewer']}; not overwritten")
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            return self._json(400, {"error": str(e)})
        history = list(prior.get("history") or [])
        if prior.get("label"):
            history.append({k: prior[k] for k in ("label", "note", "reviewer", "labelled_at")})
        self.labels[cid] = {"label": label, "note": (body.get("note") or "").strip() or None, "reviewer": self.reviewer,
                            "labelled_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                            "history": history or None}
        save_labels(self.labels_file, self.labels)
        print(f"saved {cid}: {label}", flush=True)
        self._json(200, {"case": cid, "entry": self.labels[cid]})


def main() -> int:
    args = sys.argv
    port = int(args[args.index("--port") + 1]) if "--port" in args else 8781
    Handler.reviewer = (args[args.index("--reviewer") + 1] if "--reviewer" in args else "owner").strip()
    if not Handler.reviewer:
        raise SystemExit("--reviewer must not be empty")
    if "--labels" in args:                       # test runs write elsewhere, never to owner-labels.yaml
        Handler.labels_file = Path(args[args.index("--labels") + 1])
    cases = json.loads((HERE / "review-cases.json").read_text(encoding="utf-8"))
    Handler.cases = {c["case"]: c for c in cases}
    Handler.labels = load_labels(Handler.labels_file, list(Handler.cases))
    print(f"{len(cases)} cases, {sum(1 for v in Handler.labels.values() if v['label'])} labelled; "
          f"labels -> {Handler.labels_file}; http://127.0.0.1:{port}/", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
