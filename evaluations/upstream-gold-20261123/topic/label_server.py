"""Blind labelling page for the topic/event gold (event-topic-model SPEC, frozen 2026-11-23).

    python label_server.py [--port 8793]   then open http://127.0.0.1:8793/
    python label_server.py --validate      every case labelled, codes well-formed
    python label_server.py --freeze        validate, then write labels-freeze.json (sha256 of labels + history)

Reads cases.json and taxonomy.json only: member headlines, leads and source names. No stored event_type, principals,
situation, map point or any system output is ever shown. Bound to 127.0.0.1. Writes labels.yaml and
label-history.jsonl next to this file. Every save is appended to the history (the first answer per case is the blind
primary basis). After --freeze the server refuses edits.
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
LABELS_PATH = HERE / "labels.yaml"
HISTORY_PATH = HERE / "label-history.jsonl"
FREEZE_PATH = HERE / "labels-freeze.json"
CASES = {c["development_id"]: c for c in json.loads((HERE / "cases.json").read_text(encoding="utf-8"))["cases"]}
IDS = sorted(CASES)
TAX = json.loads((HERE / "taxonomy.json").read_text(encoding="utf-8"))
ACTION_TYPES = TAX["action_types"] + TAX["extra"]
INTENTS = ["occurred", "announced_planned", "threatened", "called_for", "hypothetical", "denied", "reported_allegation"]
POLITICAL = ["yes", "no", "n.a."]

CSS = """body{font:15px/1.45 system-ui,sans-serif;max-width:900px;margin:0 auto;padding:16px;color:#1d1d1f;background:#fff}
a{color:#0b57d0}h1{font-size:20px}.muted{color:#666}.box{border:1px solid #ddd;border-radius:6px;padding:10px 14px;
margin:10px 0}table{border-collapse:collapse;width:100%}td,th{padding:4px 6px;border-bottom:1px solid #eee;text-align:left;
vertical-align:top}input[type=text],textarea,select{width:100%;box-sizing:border-box}.done{color:#137333}.todo{color:#b3261e}
button{padding:6px 14px;margin-top:8px}"""

HELP = """<b>action_type</b>: what happened (the type of the main action in the reports), from the list;
<b>out_of_scope</b> for sport, markets, culture, crime, health, obituaries; <b>unknown</b> when you cannot tell.
<b>intent</b>: modality of that action (occurred, announced_planned, threatened, called_for, hypothetical, denied,
reported_allegation); not needed for out_of_scope. <b>agent</b>: who performs the action (doer of the main verb);
<b>target</b>: whom it is directed at; <b>speaker</b>: who says it, for statements and claims (not the agent unless they
also act). One actor per line, or several separated by semicolons. A place is never an agent. <b>speaker_is_political</b>:
the speaker is a state, government, party, international organisation or armed actor (yes), or a celebrity, company or
analyst (no), or there is no speaker (n.a.)."""


def esc(x) -> str:
    return html.escape("" if x is None else str(x))


def load() -> dict:
    if not LABELS_PATH.exists():
        return {}
    return {int(k): v for k, v in (yaml.safe_load(LABELS_PATH.read_text(encoding="utf-8")) or {}).items()}


def save(data: dict) -> None:
    tmp = LABELS_PATH.with_suffix(".yaml.tmp")
    tmp.write_text(yaml.safe_dump({k: data[k] for k in sorted(data)}, sort_keys=False, allow_unicode=True, width=120)
                   if data else "{}\n", encoding="utf-8", newline="\n")
    os.replace(tmp, LABELS_PATH)


def history() -> list[dict]:
    if not HISTORY_PATH.exists():
        return []
    return [json.loads(x) for x in HISTORY_PATH.read_text(encoding="utf-8").splitlines() if x.strip()]


def log_save(i: int, label: dict) -> None:
    rec = {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "case": i, **label}
    with open(HISTORY_PATH, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def actors(raw: str) -> list[str]:
    return [a.strip() for a in re.split(r"[\n;]", raw or "") if a.strip()]


def label_problems(i: int, v: dict) -> list[str]:
    out = []
    if v.get("action_type") not in ACTION_TYPES:
        out.append(f"D{i}: action_type {v.get('action_type')!r} not in taxonomy")
    if v.get("action_type") != "out_of_scope" and v.get("intent") not in INTENTS:
        out.append(f"D{i}: intent {v.get('intent')!r} not in enum")
    if v.get("intent") not in INTENTS + [None]:
        out.append(f"D{i}: intent {v.get('intent')!r} not in enum")
    if v.get("speaker_is_political") not in POLITICAL:
        out.append(f"D{i}: speaker_is_political {v.get('speaker_is_political')!r} not yes/no/n.a.")
    for k in ("agent", "target", "speaker"):
        if not isinstance(v.get(k), list):
            out.append(f"D{i}: {k} must be a list")
    return out


def problems(data: dict) -> list[str]:
    out = [f"D{i}: not labelled" for i in IDS if i not in data]
    out += [f"D{i}: not in the sample" for i in data if i not in CASES]
    for i, v in data.items():
        out += label_problems(i, v)
    return out


def page(title: str, body: str) -> bytes:
    return (f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width'>"
            f"<title>{esc(title)}</title><style>{CSS}</style></head><body>{body}</body></html>").encode("utf-8")


def index() -> bytes:
    data = load()
    rows = "".join(
        f"<tr><td><a href='/case/{i}'>D{i}</a></td><td>{esc(CASES[i]['items'][0]['title'])}</td>"
        f"<td class='{'done' if i in data else 'todo'}'>{esc(data[i]['action_type']) if i in data else 'todo'}</td></tr>"
        for i in IDS)
    frozen = "<p class='done'>Labels frozen; editing is closed.</p>" if FREEZE_PATH.exists() else ""
    return page("Topic labels", f"<h1>Topic / event gold: labels</h1>{frozen}"
                f"<p class='muted'>{sum(i in data for i in IDS)} / {len(IDS)} labelled.</p>"
                f"<div class='box'>{HELP}</div><table><tr><th>Case</th><th>First headline</th><th>action_type</th></tr>"
                f"{rows}</table>")


def select(name: str, options: list[str], cur, disabled: str, blank: bool = True) -> str:
    opts = ("<option value=''>-- choose --</option>" if blank else "") + "".join(
        f"<option value='{esc(o)}'{' selected' if o == cur else ''}>{esc(o)}</option>" for o in options)
    return f"<select name='{name}'{disabled}>{opts}</select>"


def case(i: int) -> bytes:
    c, data = CASES[i], load()
    cur = data.get(i, {})
    nxt = next((j for j in IDS if j > i and j not in data), next((j for j in IDS if j not in data), None))
    items = "".join(
        f"<div class='box'><div class='muted'>{esc(it['source'])} · {esc(it['published_at'])}</div>"
        f"<b>{esc(it['title'])}</b><div>{esc(it['text'])}</div></div>" for it in c["items"])
    more = (f"<p class='muted'>Showing {len(c['items'])} of {c['members']} reports.</p>"
            if c["members"] > len(c["items"]) else "")
    d = " disabled" if FREEZE_PATH.exists() else ""

    def ta(name: str) -> str:
        return (f"<p><label>{name} (one per line)<textarea name='{name}' rows='2'{d}>"
                f"{esc(chr(10).join(cur.get(name) or []))}</textarea></label></p>")
    form = (f"<form method='post' action='/case/{i}'><div class='box'>{HELP}"
            f"<p><label>action_type {select('action_type', ACTION_TYPES, cur.get('action_type'), d)}</label></p>"
            f"<p><label>intent {select('intent', INTENTS, cur.get('intent'), d)}</label></p>"
            f"{ta('agent')}{ta('target')}{ta('speaker')}"
            f"<p><label>speaker_is_political {select('speaker_is_political', POLITICAL, cur.get('speaker_is_political'), d)}"
            f"</label></p><p><label>note (optional) <textarea name='note' rows='2'{d}>{esc(cur.get('note'))}</textarea>"
            f"</label></p><input type='hidden' name='next' value='{nxt or ''}'><button{d}>Save</button></div></form>")
    return page(f"D{i}", f"<p><a href='/'>All cases</a></p><h1>D{i}</h1>{form}{more}{items}")


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
        i = int(m.group(1))
        form = parse_qs(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode("utf-8"))

        def one(k: str) -> str:
            return form.get(k, [""])[0].strip()
        label = {"action_type": one("action_type"), "intent": one("intent") or None,
                 "agent": actors(one("agent")), "target": actors(one("target")), "speaker": actors(one("speaker")),
                 "speaker_is_political": one("speaker_is_political"), "note": one("note") or None}
        bad = label_problems(i, label)
        if bad:
            return self._send(page("Invalid", f"<p>{esc('; '.join(bad))} <a href='/case/{i}'>Back</a></p>"), 400)
        data = load()
        data[i] = label
        save(data)
        log_save(i, label)
        nxt = one("next")
        self._send(b"", 303, f"/case/{nxt}" if nxt else "/")

    def log_message(self, *args):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8793)
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--freeze", action="store_true")
    a = ap.parse_args()
    if a.validate or a.freeze:
        bad = problems(load())
        print("\n".join(bad) if bad else f"OK: {len(IDS)} cases labelled")
        if bad:
            sys.exit(1)
        if a.freeze:
            if FREEZE_PATH.exists():
                print("already frozen:", FREEZE_PATH.name)
                sys.exit(1)
            rec = {"frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                   "labels_sha256": hashlib.sha256(LABELS_PATH.read_bytes()).hexdigest(),
                   "history_sha256": hashlib.sha256(HISTORY_PATH.read_bytes()).hexdigest() if HISTORY_PATH.exists() else None,
                   "cases": len(IDS)}
            FREEZE_PATH.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8", newline="\n")
            print("frozen:", FREEZE_PATH.name)
        return
    print(f"http://127.0.0.1:{a.port}/")
    ThreadingHTTPServer(("127.0.0.1", a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
