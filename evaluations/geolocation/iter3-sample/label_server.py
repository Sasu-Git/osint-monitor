"""Local blind labelling page for the iteration-3 fresh sample. Writes only owner-labels.yaml (next to this file).

    python label_server.py [--port 8792]      then open http://127.0.0.1:8792/
    python label_server.py --validate         every case labelled, codes well-formed
    python label_server.py --freeze           validate, then write labels-freeze.json (sha256 of the labels file)

Reads label-cases.json and countries-iso3.json only (no stored place, map decision, stratum or rule output).
Bound to 127.0.0.1. After --freeze the server refuses edits.

Second opinion (owner request 2026-11-10): when claude-verdicts.json exists (a blind second labeller's verdicts, hash
in claude-verdicts-freeze.json), a case shows Claude's verdict only after the owner has saved a label for it. Every
save is appended to owner-label-history.jsonl with ``after_reveal`` true when that case's verdict had already been
shown, so labels changed after seeing the second opinion stay identifiable. The labels file format is unchanged.
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
LABELS_PATH = HERE / "owner-labels.yaml"
FREEZE_PATH = HERE / "labels-freeze.json"
CASES = {c["development_id"]: c for c in json.loads((HERE / "label-cases.json").read_text(encoding="utf-8"))["cases"]}
IDS = sorted(CASES)
COUNTRIES = json.loads((HERE / "countries-iso3.json").read_text(encoding="utf-8"))
CODE = re.compile(r"^([A-Z]{3}|NONE)$")
VERDICTS_PATH = HERE / "claude-verdicts.json"
HISTORY_PATH = HERE / "owner-label-history.jsonl"
VERDICTS = ({int(k): v for k, v in json.loads(VERDICTS_PATH.read_text(encoding="utf-8"))["verdicts"].items()}
            if VERDICTS_PATH.exists() else {})

CSS = """body{font:15px/1.45 system-ui,sans-serif;max-width:900px;margin:0 auto;padding:16px;color:#1d1d1f;background:#fff}
a{color:#0b57d0}h1{font-size:20px}.muted{color:#666}.box{border:1px solid #ddd;border-radius:6px;padding:10px 14px;
margin:10px 0}table{border-collapse:collapse;width:100%}td,th{padding:4px 6px;border-bottom:1px solid #eee;text-align:left;
vertical-align:top}input[type=text],textarea{width:100%;box-sizing:border-box}.done{color:#137333}.todo{color:#b3261e}
button{padding:6px 14px;margin-top:8px}"""

HELP = """<b>event_country</b>: ISO 3166-1 alpha-3 of the country where the reported event takes place (where it happened,
not who acted or who reported it). <b>NONE</b> when there is no single event country: several countries equally, at sea,
global, or not determinable from these reports. <b>event_place</b> (optional): a more specific place, as written."""


def load() -> dict:
    if not LABELS_PATH.exists():
        return {}
    return {int(k): v for k, v in (yaml.safe_load(LABELS_PATH.read_text(encoding="utf-8")) or {}).items()}


def save(data: dict) -> None:
    tmp = LABELS_PATH.with_suffix(".yaml.tmp")
    tmp.write_text(yaml.safe_dump({k: data[k] for k in sorted(data)}, sort_keys=False, allow_unicode=True, width=120),
                   encoding="utf-8", newline="\n")
    os.replace(tmp, LABELS_PATH)


def history() -> list[dict]:
    if not HISTORY_PATH.exists():
        return []
    return [json.loads(x) for x in HISTORY_PATH.read_text(encoding="utf-8").splitlines() if x.strip()]


def log_save(i: int, label: dict, after_reveal: bool) -> None:
    rec = {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "case": i, **label,
           "after_reveal": after_reveal}
    with open(HISTORY_PATH, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def baseline_history(data: dict) -> None:
    """Record labels saved before the second opinion existed, once, as the pre-reveal answers."""
    if VERDICTS and not HISTORY_PATH.exists():
        HISTORY_PATH.write_text("", encoding="utf-8")
        for i in sorted(data):
            log_save(i, {**data[i], "baseline": True}, False)


def agrees(i: int, data: dict) -> bool | None:
    if i not in data or i not in VERDICTS:
        return None
    return data[i]["event_country"] == VERDICTS[i]["event_country"]


def verdict_box(i: int, data: dict) -> str:
    if i not in VERDICTS or i not in data:
        return ""
    v, ok = VERDICTS[i], agrees(i, data)
    first = next((h for h in history() if h["case"] == i), None)
    changed = (f"<p class='muted'>Your first answer was <b>{esc(first['event_country'])}</b>; you changed it after "
               f"seeing this verdict (logged).</p>" if first and first["event_country"] != data[i]["event_country"]
               and any(h["case"] == i and h["after_reveal"] for h in history()) else "")
    mark = "<span class='done'>agrees with you</span>" if ok else "<span class='todo'>differs from you</span>"
    return (f"<div class='box' style='background:#f6f8fc'><b>Claude's verdict</b> (blind, made before seeing yours; "
            f"shown only after you save): <b>{esc(v['event_country'])}</b>"
            f"{' · ' + esc(v['event_place']) if v.get('event_place') else ''} · {esc(v.get('confidence'))} confidence · "
            f"{mark}<div>{esc(v.get('reason'))}</div>{changed}</div>")


def problems(data: dict) -> list[str]:
    out = [f"D{i}: not labelled" for i in IDS if i not in data]
    out += [f"D{i}: event_country {v.get('event_country')!r} is not ISO3 or NONE" for i, v in data.items()
            if not CODE.match(str(v.get("event_country", "")))]
    out += [f"D{i}: not in the sample" for i in data if i not in CASES]
    return out


def esc(x) -> str:
    return html.escape("" if x is None else str(x))


def page(title: str, body: str) -> bytes:
    return (f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width'>"
            f"<title>{esc(title)}</title><style>{CSS}</style></head><body>{body}</body></html>").encode("utf-8")


def index() -> bytes:
    data = load()
    marks = {None: "", True: "<span class='done'>agrees</span>", False: "<span class='todo'>differs</span>"}
    rows = "".join(
        f"<tr><td><a href='/case/{i}'>D{i}</a></td><td>{esc(CASES[i]['headline'])}</td>"
        f"<td class='{'done' if i in data else 'todo'}'>{esc(data[i]['event_country']) if i in data else 'todo'}</td>"
        + (f"<td>{marks[agrees(i, data)]}</td>" if VERDICTS else "") + "</tr>"
        for i in IDS)
    frozen = "<p class='done'>Labels frozen; editing is closed.</p>" if FREEZE_PATH.exists() else ""
    ag = [agrees(i, data) for i in IDS if agrees(i, data) is not None]
    second = (f" Claude agrees on {sum(ag)} of {len(ag)} you have labelled; its verdict on a case appears after you "
              f"save yours." if VERDICTS else "")
    return page("Geolocation labels", f"<h1>Geolocation iteration 3: event country labels</h1>{frozen}"
                f"<p class='muted'>{sum(i in data for i in IDS)} / {len(IDS)} labelled.{second}</p>"
                f"<div class='box'>{HELP}</div><table><tr><th>Case</th><th>Headline</th><th>Label</th>"
                + ("<th>Claude</th>" if VERDICTS else "") + f"</tr>{rows}</table>")


def case(i: int) -> bytes:
    c, data = CASES[i], load()
    cur = data.get(i, {})
    nxt = next((j for j in IDS if j > i and j not in data), next((j for j in IDS if j not in data), None))
    items = "".join(
        f"<div class='box'><div class='muted'>{esc(it['source'])} · {esc(it['published_at'])}</div>"
        f"<b>{esc(it['title'])}</b><div>{esc(it['text'])}</div></div>" for it in c["items"])
    more = (f"<p class='muted'>Showing {len(c['items'])} of {c['members']} reports.</p>"
            if c["members"] > len(c["items"]) else "")
    opts = "".join(f"<option value='{esc(x['id'])}'>{esc(x['name'])}</option>" for x in COUNTRIES)
    disabled = " disabled" if FREEZE_PATH.exists() else ""
    form = (f"<form method='post' action='/case/{i}'><div class='box'>{HELP}<p><label>event_country "
            f"<input type='text' name='event_country' list='iso' required value='{esc(cur.get('event_country'))}'"
            f" placeholder='e.g. UKR or NONE'{disabled}></label></p><datalist id='iso'><option value='NONE'>{opts}"
            f"</datalist><p><label>event_place (optional) <input type='text' name='event_place' "
            f"value='{esc(cur.get('event_place'))}'{disabled}></label></p><p><label>note (optional) <textarea "
            f"name='note' rows='2'{disabled}>{esc(cur.get('note'))}</textarea></label></p>"
            f"<input type='hidden' name='next' value='{nxt or ''}'><button{disabled}>Save</button></div></form>")
    go = f"<p><a href='/case/{nxt}'>Next unlabelled case →</a></p>" if (VERDICTS and i in data and nxt) else ""
    return page(f"D{i}", f"<p><a href='/'>All cases</a></p><h1>D{i}: {esc(c['headline'])}</h1>"
                f"{verdict_box(i, data)}{go}{form}{more}{items}")


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
            return self._send(index())
        m = re.fullmatch(r"/case/(\d+)", path)
        if m and int(m.group(1)) in CASES:
            return self._send(case(int(m.group(1))))
        self._send(page("Not found", "<p>Not found</p>"), 404)

    def do_POST(self):
        m = re.fullmatch(r"/case/(\d+)", urlparse(self.path).path)
        if not m or int(m.group(1)) not in CASES or FREEZE_PATH.exists():
            return self._send(page("Refused", "<p>Refused (unknown case, or labels frozen).</p>"), 403)
        form = parse_qs(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode("utf-8"))
        code = form.get("event_country", [""])[0].strip().upper()
        if not CODE.match(code):
            return self._send(page("Invalid", f"<p>'{esc(code)}' is not an ISO3 code or NONE. "
                                              f"<a href='/case/{m.group(1)}'>Back</a></p>"), 400)
        data = load()
        i = int(m.group(1))
        revealed = bool(VERDICTS) and i in data and i in VERDICTS
        data[i] = {"event_country": code,
                   "event_place": form.get("event_place", [""])[0].strip() or None,
                   "note": form.get("note", [""])[0].strip() or None}
        save(data)
        if VERDICTS:
            log_save(i, data[i], revealed)
            return self._send(b"", 303, f"/case/{i}")  # stay: show the second opinion next to the saved label
        nxt = form.get("next", [""])[0]
        self._send(b"", 303, f"/case/{nxt}" if nxt else "/")

    def log_message(self, *args):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8792)
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--freeze", action="store_true")
    a = ap.parse_args()
    if a.validate or a.freeze:
        bad = problems(load())
        print("\n".join(bad) if bad else f"OK: {len(IDS)} cases labelled")
        if bad:
            sys.exit(1)
        if a.freeze:
            rec = {"frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                   "labels_sha256": hashlib.sha256(LABELS_PATH.read_bytes()).hexdigest(), "cases": len(IDS)}
            if HISTORY_PATH.exists():
                hist = history()
                rec["history_sha256"] = hashlib.sha256(HISTORY_PATH.read_bytes()).hexdigest()
                rec["changed_after_reveal"] = sorted({h["case"] for h in hist if h["after_reveal"]})
            FREEZE_PATH.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8", newline="\n")
            print("frozen:", FREEZE_PATH.name)
        return
    baseline_history(load())
    print(f"http://127.0.0.1:{a.port}/")
    ThreadingHTTPServer(("127.0.0.1", a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
