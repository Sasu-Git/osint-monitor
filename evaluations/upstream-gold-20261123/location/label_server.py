"""Blind labelling page for the location gold (event-location-model SPEC, frozen 2026-11-23, amendment 1).

    python label_server.py [--port 8794]   then open http://127.0.0.1:8794/
    python label_server.py --validate      every case labelled, codes well-formed, role subset complete
    python label_server.py --freeze        validate, then write labels-freeze.json (sha256 of labels + history)

Reads cases.json and countries-iso3.json only: member headlines, leads and source names. No stored place, map point,
principals, event_type or any system output is ever shown. Bound to 127.0.0.1. Writes labels.yaml and
label-history.jsonl next to this file. Every save is appended to the history (the first answer per case is the blind
primary basis). After --freeze the server refuses edits.

Cases flagged role_labels (the 50-Development subset) also ask, per shown report, for its place mentions with a role.
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
COUNTRIES = json.loads((HERE / "countries-iso3.json").read_text(encoding="utf-8"))
SPECIAL = ["NONE", "MULTI", "SEA_OR_REGION", "DISPUTED"]
CODE = re.compile(r"^([A-Z]{3}|NONE|MULTI|SEA_OR_REGION|DISPUTED)$")
ROLES = ["event", "target", "origin", "actor_location", "venue", "reporting", "mentioned"]

CSS = """body{font:15px/1.45 system-ui,sans-serif;max-width:900px;margin:0 auto;padding:16px;color:#1d1d1f;background:#fff}
a{color:#0b57d0}h1{font-size:20px}.muted{color:#666}.box{border:1px solid #ddd;border-radius:6px;padding:10px 14px;
margin:10px 0}table{border-collapse:collapse;width:100%}td,th{padding:4px 6px;border-bottom:1px solid #eee;text-align:left;
vertical-align:top}input[type=text],textarea{width:100%;box-sizing:border-box}.done{color:#137333}.todo{color:#b3261e}
button{padding:6px 14px;margin-top:8px}"""

HELP = """<b>event_country</b>: ISO 3166-1 alpha-3 of the country where the reported event takes place (where it
happened, or where an attack lands; not who acted, who reported it or where an actor is based). Special values:
<b>NONE</b> (no occurrence place, e.g. a statement with no venue, or not determinable), <b>MULTI</b> (occurrence places
in several countries), <b>SEA_OR_REGION</b> (the location is a sea, strait or multi-country region, no country),
<b>DISPUTED</b> (a disputed territory). <b>event_place</b> (optional): the specific place, as written."""
ROLE_HELP = """<b>Place mentions</b> (this case only): for each report below, list its place mentions, one per line, as
<code>place | role</code>. Roles: <b>event</b> (where it happened), <b>target</b> (where an attack or measure lands),
<b>origin</b> (launch or departure), <b>actor_location</b> (where an actor is based, as in "Tehran says"),
<b>venue</b> (location of a meeting or statement), <b>reporting</b> (dateline, "reports from"), <b>mentioned</b>
(anything else). Write <code>none</code> if the report names no place."""


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


def parse_places(raw: str) -> tuple[list[dict], list[str]]:
    """Lines 'place | role' -> mentions; 'none' -> []. Returns (mentions, errors)."""
    text = (raw or "").strip()
    if not text:
        return [], ["empty (write 'none' if no place)"]
    if text.lower() == "none":
        return [], []
    out, errs = [], []
    for line in text.splitlines():
        if not line.strip():
            continue
        place, sep, role = line.rpartition("|")
        place, role = place.strip(), role.strip().lower()
        if not sep or not place or role not in ROLES:
            errs.append(f"bad line {line.strip()!r}")
        else:
            out.append({"place": place, "role": role})
    return out, errs


def label_problems(i: int, v: dict) -> list[str]:
    out = []
    if not CODE.match(str(v.get("event_country", ""))):
        out.append(f"D{i}: event_country {v.get('event_country')!r} is not ISO3 or NONE/MULTI/SEA_OR_REGION/DISPUTED")
    if i in CASES and CASES[i].get("role_labels"):
        pm = v.get("place_mentions") or {}
        for it in CASES[i]["items"]:
            key = str(it["item_id"])
            if key not in pm:
                out.append(f"D{i}: item {key}: place mentions missing")
            else:
                for m in pm[key]:
                    if m.get("role") not in ROLES or not m.get("place"):
                        out.append(f"D{i}: item {key}: bad mention {m!r}")
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
        f"<td>{'roles' if CASES[i].get('role_labels') else ''}</td>"
        f"<td class='{'done' if i in data else 'todo'}'>{esc(data[i]['event_country']) if i in data else 'todo'}</td></tr>"
        for i in IDS)
    frozen = "<p class='done'>Labels frozen; editing is closed.</p>" if FREEZE_PATH.exists() else ""
    return page("Location labels", f"<h1>Location gold: labels</h1>{frozen}"
                f"<p class='muted'>{sum(i in data for i in IDS)} / {len(IDS)} labelled. Cases marked 'roles' also ask "
                f"for per-report place roles.</p><div class='box'>{HELP}</div><table><tr><th>Case</th>"
                f"<th>First headline</th><th></th><th>Label</th></tr>{rows}</table>")


def case(i: int) -> bytes:
    c, data = CASES[i], load()
    cur = data.get(i, {})
    pm = cur.get("place_mentions") or {}
    nxt = next((j for j in IDS if j > i and j not in data), next((j for j in IDS if j not in data), None))
    d = " disabled" if FREEZE_PATH.exists() else ""
    roles = bool(c.get("role_labels"))

    def mentions_box(it) -> str:
        if not roles:
            return ""
        key = str(it["item_id"])
        val = ("none" if key in pm and not pm[key] else
               "\n".join(f"{m['place']} | {m['role']}" for m in pm.get(key, [])))
        return (f"<label>place mentions of this report (place | role)<textarea name='places_{key}' rows='3'{d}>"
                f"{esc(val)}</textarea></label>")
    items = "".join(
        f"<div class='box'><div class='muted'>{esc(it['source'])} · {esc(it['published_at'])}</div>"
        f"<b>{esc(it['title'])}</b><div>{esc(it['text'])}</div>{mentions_box(it)}</div>" for it in c["items"])
    more = (f"<p class='muted'>Showing {len(c['items'])} of {c['members']} reports.</p>"
            if c["members"] > len(c["items"]) else "")
    opts = "".join(f"<option value='{esc(x['id'])}'>{esc(x['name'])}</option>" for x in COUNTRIES)
    special = "".join(f"<option value='{s}'>" for s in SPECIAL)
    top = (f"<div class='box'>{HELP}<p><label>event_country <input type='text' name='event_country' list='iso' "
           f"required value='{esc(cur.get('event_country'))}' placeholder='e.g. UKR, NONE, MULTI'{d}></label></p>"
           f"<datalist id='iso'>{special}{opts}</datalist><p><label>event_place (optional) <input type='text' "
           f"name='event_place' value='{esc(cur.get('event_place'))}'{d}></label></p>"
           f"<p><label>note (optional) <textarea name='note' rows='2'{d}>{esc(cur.get('note'))}</textarea></label></p>"
           f"{('<div>' + ROLE_HELP + '</div>') if roles else ''}</div>")
    form = (f"<form method='post' action='/case/{i}'>{top}{items}<input type='hidden' name='next' "
            f"value='{nxt or ''}'><button{d}>Save</button></form>")
    return page(f"D{i}", f"<p><a href='/'>All cases</a></p><h1>D{i}</h1>{form}{more}")


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
        label = {"event_country": one("event_country").upper(), "event_place": one("event_place") or None,
                 "note": one("note") or None}
        errs = []
        if CASES[i].get("role_labels"):
            label["place_mentions"] = {}
            for it in CASES[i]["items"]:
                key = str(it["item_id"])
                mentions, e = parse_places(one(f"places_{key}"))
                label["place_mentions"][key] = mentions
                errs += [f"item {key}: {x}" for x in e]
        errs += [p for p in label_problems(i, label) if "place mentions" not in p and "bad mention" not in p]
        if errs:
            return self._send(page("Invalid", f"<p>{esc('; '.join(errs))} <a href='/case/{i}'>Back</a></p>"), 400)
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
    ap.add_argument("--port", type=int, default=8794)
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
                   "cases": len(IDS), "role_subset_cases": sum(1 for c in CASES.values() if c.get("role_labels"))}
            FREEZE_PATH.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8", newline="\n")
            print("frozen:", FREEZE_PATH.name)
        return
    print(f"http://127.0.0.1:{a.port}/")
    ThreadingHTTPServer(("127.0.0.1", a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
