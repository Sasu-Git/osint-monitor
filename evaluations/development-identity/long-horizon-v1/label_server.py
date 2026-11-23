"""Blind labelling page for the long-horizon Development-identity gold (spec frozen 2026-11-23, see SPEC.md and SPEC-FREEZE.md).

    python label_server.py [--port 8795]   then open http://127.0.0.1:8795/
    python label_server.py --validate      every case labelled, codes well-formed
    python label_server.py --freeze        validate, then write labels-freeze.json (sha256 of labels + history)

Reads cases.json only (cases.json holds no Development id, item id, cosine, stratum, gap band or system decision; key.json
is never opened by this file). Each case shows two sides, an earlier set of reports and a later set, with outlet,
publication time, headline and lead. Bound to 127.0.0.1. Writes labels.yaml and label-history.jsonl next to cases.json.
Every save is appended to the history (the first answer per case is the blind primary basis). After --freeze the server
refuses edits.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import yaml

HERE = Path(__file__).resolve().parent
LABELS = ["SAME_EPISODE", "FOLLOW_UP_SAME_STORYLINE", "RECURRING_SEPARATE_OCCURRENCE", "DIFFERENT", "CANNOT_TELL"]
CONFIDENCE = ["high", "medium", "low"]

CSS = """body{font:15px/1.45 system-ui,sans-serif;max-width:960px;margin:0 auto;padding:16px;color:#1d1d1f;background:#fff}
a{color:#0b57d0}h1{font-size:20px}h2{font-size:16px;margin:14px 0 4px}.muted{color:#666}.box{border:1px solid #ddd;
border-radius:6px;padding:10px 14px;margin:10px 0}table{border-collapse:collapse;width:100%}td,th{padding:4px 6px;
border-bottom:1px solid #eee;text-align:left;vertical-align:top}textarea,select{width:100%;box-sizing:border-box}
.done{color:#137333}.todo{color:#b3261e}button{padding:6px 14px;margin-top:8px}.draft{background:#fff8e1}
.side{border-left:4px solid #bbb;padding-left:10px}"""

HELP = """<b>Definitions (frozen 2026-11-23).</b> A Development is one occurrence or tightly bounded event
episode. Longer-running storylines belong at the Situation layer. There is no fixed maximum duration: judge each case. Compare the <b>earlier reports</b> with the <b>later
reports</b> and choose one:<ul>
<li><b>SAME_EPISODE</b>: the later reports are about the same occurrence or tightly bounded episode as the earlier
ones (same event, further detail, casualty updates, official documents, direct aftermath inside that episode).</li>
<li><b>FOLLOW_UP_SAME_STORYLINE</b>: a different, later occurrence that follows from the earlier one (a reaction,
consequence, response or next step) in the same storyline.</li>
<li><b>RECURRING_SEPARATE_OCCURRENCE</b>: another instance of a repeating kind of event with the same actors or place,
not caused by the earlier one (another strike, another meeting, another match).</li>
<li><b>DIFFERENT</b>: unrelated, or sharing only a broad topic, theme, country or actor.</li>
<li><b>CANNOT_TELL</b>: the reports do not give enough to decide. Not for complicated cases.</li></ul>
Judge only what the reports say. Do not use outside knowledge of what happened later."""


def esc(x) -> str:
    return html.escape("" if x is None else str(x))


def page(title: str, body: str) -> bytes:
    return (f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width'>"
            f"<title>{esc(title)}</title><style>{CSS}</style></head><body>{body}</body></html>").encode("utf-8")


class App:
    def __init__(self, directory: Path):
        self.dir = Path(directory)
        self.labels_path = self.dir / "labels.yaml"
        self.history_path = self.dir / "label-history.jsonl"
        self.freeze_path = self.dir / "labels-freeze.json"
        self.cases = {c["case_id"]: c for c in json.loads((self.dir / "cases.json").read_text(encoding="utf-8"))["cases"]}
        self.ids = sorted(self.cases)

    @property
    def frozen(self) -> bool:
        return self.freeze_path.exists()

    def load(self) -> dict:
        if not self.labels_path.exists():
            return {}
        return yaml.safe_load(self.labels_path.read_text(encoding="utf-8")) or {}

    def save(self, data: dict) -> None:
        tmp = self.labels_path.with_suffix(".yaml.tmp")
        tmp.write_text(yaml.safe_dump({k: data[k] for k in sorted(data)}, sort_keys=False, allow_unicode=True, width=120)
                       if data else "{}\n", encoding="utf-8", newline="\n")
        os.replace(tmp, self.labels_path)

    def log_save(self, cid: str, label: dict) -> None:
        rec = {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "case": cid, **label}
        with open(self.history_path, "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def label_problems(self, cid: str, v: dict) -> list[str]:
        out = []
        if v.get("label") not in LABELS:
            out.append(f"{cid}: label {v.get('label')!r} not in the label set")
        if v.get("confidence") not in CONFIDENCE + [None]:
            out.append(f"{cid}: confidence {v.get('confidence')!r} not high/medium/low")
        return out

    def problems(self, data: dict) -> list[str]:
        out = [f"{i}: not labelled" for i in self.ids if i not in data]
        out += [f"{i}: not in the sample" for i in data if i not in self.cases]
        for i, v in data.items():
            out += self.label_problems(i, v)
        return out

    # ---- pages
    def index(self) -> bytes:
        data = self.load()
        rows = "".join(
            f"<tr><td><a href='/case/{i}'>{i}</a></td><td>{esc(self.cases[i]['a']['items'][0]['title'])}</td>"
            f"<td class='{'done' if i in data else 'todo'}'>{esc(data[i]['label']) if i in data else 'todo'}</td></tr>"
            for i in self.ids)
        frozen = "<p class='done'>Labels frozen; editing is closed.</p>" if self.frozen else ""
        return page("Long-horizon identity labels",
                    f"<h1>Long-horizon Development identity: labels</h1>{frozen}"
                    f"<p class='muted'>{sum(i in data for i in self.ids)} / {len(self.ids)} labelled.</p>"
                    f"<div class='box draft'>{HELP}</div><table><tr><th>Case</th><th>First earlier headline</th>"
                    f"<th>Label</th></tr>{rows}</table>")

    def case(self, cid: str) -> bytes:
        c, data = self.cases[cid], self.load()
        cur = data.get(cid, {})
        nxt = next((j for j in self.ids if j > cid and j not in data), next((j for j in self.ids if j not in data), None))
        d = " disabled" if self.frozen else ""

        def side(name: str, s: dict) -> str:
            items = "".join(
                f"<div class='box'><div class='muted'>{esc(it['source'])} · {esc(it['published_at'])} UTC</div>"
                f"<b>{esc(it['title'])}</b><div>{esc(it['text'])}</div></div>" for it in s["items"])
            return f"<div class='side'><h2>{name}</h2>{items}</div>"
        opts = "<option value=''>-- choose --</option>" + "".join(
            f"<option value='{o}'{' selected' if o == cur.get('label') else ''}>{o}</option>" for o in LABELS)
        conf = "<option value=''>-- optional --</option>" + "".join(
            f"<option value='{o}'{' selected' if o == cur.get('confidence') else ''}>{o}</option>" for o in CONFIDENCE)
        form = (f"<form method='post' action='/case/{esc(cid)}'><div class='box'>"
                f"<p><label>Are the later reports part of the same occurrence or episode as the earlier reports?"
                f"<select name='label'{d}>{opts}</select></label></p>"
                f"<p><label>confidence <select name='confidence'{d}>{conf}</select></label></p>"
                f"<p><label>note (optional)<textarea name='note' rows='2'{d}>{esc(cur.get('note'))}</textarea></label></p>"
                f"<input type='hidden' name='next' value='{esc(nxt or '')}'><button{d}>Save</button></div></form>")
        return page(cid, f"<p><a href='/'>All cases</a></p><h1>{esc(cid)}</h1>"
                    f"<details class='box draft'><summary>Definitions</summary>{HELP}</details>"
                    f"{side('Earlier reports', c['a'])}{side('Later reports', c['b'])}{form}")


def make_handler(app: App):
    class Handler(BaseHTTPRequestHandler):
        def _send(self, body: bytes, status: int = 200, location: str | None = None):
            self.send_response(status)
            if location:
                self.send_header("Location", location)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = urlparse(self.path).path
            if path == "/":
                return self._send(app.index())
            m = re.fullmatch(r"/case/(LH\d+)", path)
            if m and m.group(1) in app.cases:
                return self._send(app.case(m.group(1)))
            self._send(page("Not found", "<p>Not found</p>"), 404)

        def do_POST(self):
            m = re.fullmatch(r"/case/(LH\d+)", urlparse(self.path).path)
            if not m or m.group(1) not in app.cases or app.frozen:
                return self._send(page("Refused", "<p>Refused (unknown case, or labels frozen).</p>"), 403)
            cid = m.group(1)
            form = parse_qs(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode("utf-8"))

            def one(k: str) -> str:
                return form.get(k, [""])[0].strip()
            label = {"label": one("label"), "confidence": one("confidence") or None, "note": one("note") or None}
            bad = app.label_problems(cid, label)
            if bad:
                return self._send(page("Invalid", f"<p>{esc('; '.join(bad))} <a href='/case/{esc(cid)}'>Back</a></p>"), 400)
            data = app.load()
            data[cid] = label
            app.save(data)
            app.log_save(cid, label)
            nxt = one("next")
            self._send(b"", 303, f"/case/{nxt}" if re.fullmatch(r"LH\d+", nxt) else "/")

        def log_message(self, *args):
            pass
    return Handler


def freeze(app: App) -> int:
    bad = app.problems(app.load())
    print("\n".join(bad) if bad else f"OK: {len(app.ids)} cases labelled")
    if bad:
        return 1
    if app.frozen:
        print("already frozen:", app.freeze_path.name)
        return 1
    rec = {"frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "labels_sha256": hashlib.sha256(app.labels_path.read_bytes()).hexdigest(),
           "history_sha256": hashlib.sha256(app.history_path.read_bytes()).hexdigest() if app.history_path.exists() else None,
           "cases": len(app.ids)}
    app.freeze_path.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8", newline="\n")
    print("frozen:", app.freeze_path.name)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8795)
    ap.add_argument("--dir", default=str(HERE))
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--freeze", action="store_true")
    a = ap.parse_args()
    app = App(Path(a.dir))
    if a.freeze:
        sys.exit(freeze(app))
    if a.validate:
        bad = app.problems(app.load())
        print("\n".join(bad) if bad else f"OK: {len(app.ids)} cases labelled")
        sys.exit(1 if bad else 0)
    print(f"http://127.0.0.1:{a.port}/")
    ThreadingHTTPServer(("127.0.0.1", a.port), make_handler(app)).serve_forever()


if __name__ == "__main__":
    main()
