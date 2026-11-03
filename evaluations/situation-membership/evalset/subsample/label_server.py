"""Local labelling page for the subsample. Writes only owner-labels-subsample.yaml (next to this file).

    python label_server.py [--port 8791]        then open http://127.0.0.1:8791/

Blind: it reads ../cases.json (the same fields a reviewer sees in the full set), ../scopes.json (founder evidence for
the automatic Situations), manifest.json and the labels file. It never reads ../key.json. Bound to 127.0.0.1 only.
When done: python labels_subsample.py validate, then python labels_subsample.py freeze.
"""

from __future__ import annotations

import argparse
import html
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import yaml

HERE = Path(__file__).resolve().parent
EVALSET = HERE.parent
LABELS_PATH = HERE / "owner-labels-subsample.yaml"
LABELS = ("MEMBER", "CONTEXT", "SPILLOVER", "OTHER_SITUATION", "NOT_MEMBER", "AMBIGUOUS")
LABEL_HELP = {
    "MEMBER": "belongs to this Situation",
    "CONTEXT": "commentary or analysis about it: linked context, not a member",
    "SPILLOVER": "a consequence that belongs to its own Situation",
    "OTHER_SITUATION": "belongs to a different Situation",
    "NOT_MEMBER": "off scope",
    "AMBIGUOUS": "cannot be decided from what is shown",
}

IDS = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))["case_ids"]
CASES = {c["case_id"]: c for c in json.loads((EVALSET / "cases.json").read_text(encoding="utf-8"))["cases"]
         if c["case_id"] in set(IDS)}
SCOPES = {a["slug"]: a for a in json.loads((EVALSET / "scopes.json").read_text(encoding="utf-8"))["automatic"]}

CSS = """body{font:15px/1.45 system-ui,sans-serif;max-width:900px;margin:0 auto;padding:16px;color:#1d1d1f;background:#fff}
a{color:#0b57d0}h1{font-size:20px}h2{font-size:17px;margin-top:22px}.muted{color:#666}.box{border:1px solid #ddd;
border-radius:6px;padding:10px 14px;margin:10px 0}table{border-collapse:collapse;width:100%}td,th{padding:4px 6px;
border-bottom:1px solid #eee;text-align:left;vertical-align:top}input[type=text],textarea{width:100%;box-sizing:border-box}
label.opt{display:block;margin:3px 0}.done{color:#137333}.todo{color:#b3261e}button{padding:6px 14px;margin-top:8px}"""


def load() -> dict:
    return yaml.safe_load(LABELS_PATH.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    tmp = LABELS_PATH.with_suffix(".yaml.tmp")
    tmp.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8",
                   newline="\n")
    os.replace(tmp, LABELS_PATH)


def esc(x) -> str:
    return html.escape("" if x is None else str(x))


def page(title: str, body: str) -> bytes:
    return (f"<!doctype html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width,"
            f"initial-scale=1'><title>{esc(title)}</title><style>{CSS}</style></head><body>{body}</body></html>"
            ).encode("utf-8")


def last_reviewer(data: dict) -> str:
    for e in reversed(data["cases"]):
        if e.get("reviewer"):
            return e["reviewer"]
    for s in data["situation_scopes"]:
        if s.get("reviewer"):
            return s["reviewer"]
    return ""


def index() -> bytes:
    data = load()
    done = sum(1 for e in data["cases"] if e.get("label"))
    sdone = sum(1 for s in data["situation_scopes"] if s.get("domains_or_types") is not None)
    rows = []
    for e in data["cases"]:
        c = CASES[e["case_id"]]
        st = f"<span class=done>{esc(e['label'])}</span>" if e.get("label") else "<span class=todo>open</span>"
        rows.append(f"<tr><td><a href='/case/{esc(e['case_id'])}'>{esc(e['case_id'])}</a></td>"
                    f"<td>{esc(c['situation']['slug'])}</td><td>{esc(c['development']['headline'])}</td><td>{st}</td></tr>")
    first_open = next((e["case_id"] for e in data["cases"] if not e.get("label")), None)
    nxt = f"<a href='/case/{esc(first_open)}'>next open case</a>" if first_open else "all cases labelled"
    body = (f"<h1>Situation membership: labelling subsample</h1>"
            f"<p class=muted>Blind set: no scores, membership or origin are shown. Do not open key.json or the live "
            f"Situation pages. Labels are saved to {esc(LABELS_PATH.name)}.</p>"
            f"<p>1. <a href='/scopes'>Intended scopes of the automatic Situations</a>: {sdone}/{len(data['situation_scopes'])}"
            f" filled (do these first).<br>2. Cases: {done}/{len(data['cases'])} labelled; {nxt}.<br>3. When done: "
            f"<code>python labels_subsample.py validate</code>, then <code>python labels_subsample.py freeze</code>.</p>"
            f"<table><tr><th>Case</th><th>Situation</th><th>Development</th><th>Label</th></tr>{''.join(rows)}</table>")
    return page("Membership labelling", body)


def scopes_page() -> bytes:
    data = load()
    rev = last_reviewer(data)
    parts = []
    for s in data["situation_scopes"]:
        a = SCOPES[s["slug"]]
        der = a.get("derived") or {}
        founders = "".join(f"<li>D{esc(f['development_id'])}: {esc(f['headline'])} <span class=muted>({esc(f.get('domain'))}"
                           f" / {esc(f.get('event_type'))})</span></li>" for f in a.get("founders", []))
        dv = ", ".join(s["domains_or_types"]) if s.get("domains_or_types") is not None else ""
        pv = ", ".join(s["places"]) if s.get("places") is not None else ""
        parts.append(
            f"<div class=box><h2>{esc(a['title'])} <span class=muted>({esc(s['slug'])})</span></h2>"
            f"<p class=muted>Primary actors: {esc(', '.join(a.get('primary_actors', [])))}. Derived from founders: domains "
            f"{esc(', '.join(der.get('domains', [])))}; event types {esc(', '.join(der.get('event_types', [])))}. Evidence, "
            f"not the answer.</p><details><summary>Founders</summary><ul>{founders}</ul></details>"
            f"<p>Domains or event types (comma-separated; empty = none)<input type=text name='d__{esc(s['slug'])}' value='{esc(dv)}'></p>"
            f"<p>Places (comma-separated; empty = none)<input type=text name='p__{esc(s['slug'])}' value='{esc(pv)}'></p>"
            f"<p>Note<input type=text name='n__{esc(s['slug'])}' value='{esc(s.get('note'))}'></p>"
            f"<input type=hidden name='f__{esc(s['slug'])}' value='1'></div>")
    body = (f"<p><a href='/'>back</a></p><h1>Intended scope of each automatic Situation</h1>"
            f"<form method=post action='/scopes'><p>Reviewer<input type=text name=reviewer value='{esc(rev)}' required></p>"
            f"{''.join(parts)}<button>Save all scopes</button></form>")
    return page("Scopes", body)


def case_page(cid: str, msg: str = "") -> bytes:
    data = load()
    e = next(x for x in data["cases"] if x["case_id"] == cid)
    c = CASES[cid]
    s, d = c["situation"], c["development"]
    reports = "".join(f"<li>{esc(r['headline'])} <span class=muted>({esc(r['source'])}, {esc(r['published_at'])})</span></li>"
                      for r in d.get("reports", []))
    opts = "".join(f"<label class=opt><input type=radio name=label value={l} {'checked' if e.get('label') == l else ''}"
                   f" required> <b>{l}</b> <span class=muted>{esc(LABEL_HELP[l])}</span></label>" for l in LABELS)
    i = IDS.index(cid)
    prev_l = f"<a href='/case/{IDS[i - 1]}'>previous</a>" if i else ""
    next_l = f"<a href='/case/{IDS[i + 1]}'>next</a>" if i + 1 < len(IDS) else ""
    body = (f"<p><a href='/'>index</a> · {prev_l} · {next_l} · case {i + 1}/{len(IDS)}</p>{msg}"
            f"<h1>{esc(cid)}</h1>"
            f"<div class=box><h2>Situation: {esc(s['title'])}</h2><p class=muted>{esc(s['slug'])} · {esc(s['kind'])} · region "
            f"{esc(s.get('region'))}</p><p>Primary actors: {esc(', '.join(s.get('primary_actors', [])))}</p>"
            f"<p>{esc(s.get('description'))}</p></div>"
            f"<div class=box><h2>Development D{esc(d['development_id'])}: {esc(d['headline'])}</h2>"
            f"<p>{esc(d.get('summary') or '')}</p><table>"
            f"<tr><td>First reported</td><td>{esc(d.get('first_reported_at'))}</td></tr>"
            f"<tr><td>Principal actors</td><td>{esc(', '.join(d.get('principal_actors') or []))}</td></tr>"
            f"<tr><td>Other actors</td><td>{esc(', '.join(d.get('other_mentioned_actors') or []))}</td></tr>"
            f"<tr><td>Domain / type</td><td>{esc(d.get('domain'))} / {esc(d.get('event_type'))}</td></tr>"
            f"<tr><td>Region</td><td>{esc(d.get('region'))}</td></tr>"
            f"<tr><td>Reports</td><td>{esc(d.get('report_count'))}</td></tr></table><ul>{reports}</ul></div>"
            f"<form method=post action='/case/{esc(cid)}'>{opts}"
            f"<p>Reason (one line)<input type=text name=reason value='{esc(e.get('reason'))}' required></p>"
            f"<p>Reviewer<input type=text name=reviewer value='{esc(e.get('reviewer') or last_reviewer(data))}' required></p>"
            f"<button>Save and next</button></form>")
    return page(cid, body)


class Handler(BaseHTTPRequestHandler):
    def _send(self, body: bytes, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _redirect(self, to: str) -> None:
        self.send_response(303)
        self.send_header("Location", to)
        self.end_headers()

    def _form(self) -> dict[str, str]:
        n = int(self.headers.get("Content-Length") or 0)
        q = parse_qs(self.rfile.read(n).decode("utf-8"), keep_blank_values=True)
        return {k: v[0] for k, v in q.items()}

    def do_GET(self):
        p = urlparse(self.path).path
        if p == "/":
            return self._send(index())
        if p == "/scopes":
            return self._send(scopes_page())
        if p.startswith("/case/") and p[6:] in CASES:
            return self._send(case_page(p[6:]))
        self._send(page("Not found", "<p>Not found. <a href='/'>index</a></p>"), 404)

    def do_POST(self):
        p = urlparse(self.path).path
        f = self._form()
        data = load()
        if p == "/scopes":
            rev = f.get("reviewer", "").strip()
            for s in data["situation_scopes"]:
                if f"f__{s['slug']}" not in f:
                    continue
                split = lambda v: [x.strip() for x in v.split(",") if x.strip()]  # noqa: E731
                s["domains_or_types"] = split(f.get(f"d__{s['slug']}", ""))
                s["places"] = split(f.get(f"p__{s['slug']}", ""))
                s["note"] = f.get(f"n__{s['slug']}", "").strip() or None
                s["reviewer"] = rev or None
            save(data)
            return self._redirect("/")
        cid = p[6:] if p.startswith("/case/") else None
        if cid in CASES:
            label = f.get("label")
            if label not in LABELS:
                return self._send(case_page(cid, "<p class=todo>Choose one label.</p>"), 400)
            e = next(x for x in data["cases"] if x["case_id"] == cid)
            e["label"], e["reason"] = label, f.get("reason", "").strip() or None
            e["reviewer"] = f.get("reviewer", "").strip() or None
            save(data)
            i = IDS.index(cid)
            return self._redirect(f"/case/{IDS[i + 1]}" if i + 1 < len(IDS) else "/")
        self._send(page("Not found", "<p>Not found.</p>"), 404)

    def log_message(self, *args):
        pass


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8791)
    a = ap.parse_args()
    print(f"labelling page: http://127.0.0.1:{a.port}/  (labels -> {LABELS_PATH}; Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
