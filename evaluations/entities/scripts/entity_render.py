"""Render the entity review JSON into a Markdown review document with empty review fields."""
import json, re, sys
from collections import Counter, OrderedDict, defaultdict

from osint_monitor.processors.actors import ActorNormalizer
from osint_monitor.processors.entity_resolver import normalise
from osint_monitor.processors.geography import Gazetteer

data = json.load(open(sys.argv[1], encoding="utf-8"))
out_path = sys.argv[2]
normalizer, geo = ActorNormalizer.load(), Gazetteer.load()
DOMAINS = ["diplomacy", "military", "security", "political", "economic", "humanitarian", "institutional"]
PLACE = {"GPE", "LOC", "FAC", "FACILITY"}
ABBREV = re.compile(r"^(?:[A-Z]\.){2,}$|^[A-Z][a-z]{0,3}\.$")
INSTITUTION_NOUNS = {"navy", "army", "air force", "defense", "defence", "pentagon", "military", "ministry", "government",
                     "department", "police", "court", "parliament", "congress", "senate", "treasury", "state department"}
CLASSES = ["NER detection", "entity typing", "alias resolution", "person -> state/institution mapping",
           "location/actor confusion", "contextual organisation", "duplicate canonical identity",
           "multilingual failure", "principal-selection failure"]


def esc(s, n=None):
    s = " ".join(str(s if s is not None else "").split())
    if n and len(s) > n:
        s = s[: n - 1] + "…"
    return s.replace("|", "\\|")


def fold(name):
    return normalise(re.sub(r"^(the|a|an)\s+", "", name or "", flags=re.I).rstrip("’'s").strip())


def flags(ev):
    f = OrderedDict()
    add = lambda cls, text, principal=False: f.setdefault((cls, text), principal)   # noqa: E731
    res = ev["resolution"]
    langs = {i["lang"] for i in ev["items"]}
    for r in res:
        m = r["mention"]
        if ABBREV.match(m.strip()):
            pass
        elif re.match(r"^the\s", m, re.I) or re.search(r"['’]s?$", m):
            add("NER detection", f"article/possessive kept in span: '{esc(m, 60)}'")
        elif ("\n" in m or "&#" in m or len(m.split()) > 7 or re.search(r"[a-z][A-Z]", m)
              or (m[:1].islower() and not re.match(r"^(al|el|la|de|van|von|bin|anti|north|south|east|west)\b", m))):
            add("NER detection", f"malformed span '{esc(m, 70)}' ({r['type']})")
        if r["method"] == "fuzzy":
            add("alias resolution", f"fuzzy: '{esc(m, 50)}' -> '{esc(r['canonical'], 50)}' ({r['reason']})")
        if r["type"] in ("PERSON", "ORG") and (geo.is_country(m) or geo.is_subnational(m)):
            add("entity typing", f"'{m}' typed {r['type']} but is a known place")
        if r["type"] in PLACE and normalizer.is_media(m):
            add("entity typing", f"'{m}' typed {r['type']} but is a media outlet")
    by_fold = defaultdict(set)
    for r in res:
        if r["canonical"]:
            by_fold[(r["type"], fold(r["canonical"]))].add(r["canonical"])
    for (t, k), names in by_fold.items():
        if len(names) > 1:
            add("duplicate canonical identity", f"{t} entities {sorted(names)} are one name")
    finals = ev["principals"]["final"]
    for k in finals:
        rows = [r for r in res if r["canonical"] and (normalizer.surface(r["mention"]) == k
                                                     or normalizer.surface(r["canonical"]) == k or fold(r["canonical"]) == k)]
        types = {r["type"] for r in rows}
        surfaces = ev["principals"]["surfaces"].get(k, [])
        if not geo.is_country(k) and types and types <= PLACE:
            add("location/actor confusion", f"principal '{k}' comes from place mentions ({', '.join(sorted(types))})", True)
        elif geo.is_subnational(k):
            add("location/actor confusion", f"principal '{k}' is a sub-national place", True)
        if types & {"EVENT", "PRODUCT"}:
            add("entity typing", f"principal '{k}' is typed {', '.join(sorted(types & {'EVENT', 'PRODUCT'}))}", True)
        if any(normalizer.is_media(s) for s in surfaces) or re.search(r"\bnews\b", k):
            add("contextual organisation", f"principal '{k}' is a media outlet / programme name", True)
        if re.search(r",\s*[a-z]{2}$", k):
            add("location/actor confusion", f"principal '{k}' is a 'Place, ST' address"
                                            + (f" typed {', '.join(sorted(types))}" if types else ""), True)
        if k in INSTITUTION_NOUNS:
            add("person -> state/institution mapping", f"principal '{k}' is a generic institution name, not mapped to its state", True)
        if "PERSON" in types and normalizer.key(k) == k and not geo.is_country(k):
            add("person -> state/institution mapping", f"principal person '{k}' has no state/body mapping (fine for private persons)", True)
        if types and types <= {"ORG"} and re.search(r",|\binc\b|\bllc\b|\bltd\b|\bcorp", k):
            add("contextual organisation", f"principal '{k}' is a company in an administrative notice", True)
        if langs & {"it", "es"} and len(k.split()) > 3:
            add("multilingual failure", f"principal '{esc(k, 60)}' is a clause, not a name", True)
        for s in surfaces:
            if geo.is_subnational(s) and normalizer.key(s) not in (None, s):
                add("location/actor confusion", f"capital/city '{s}' stands for '{normalizer.key(s)}'", True)
    if langs & {"it", "es"}:
        bad = sum(1 for r in res if len(r["mention"].split()) > 5 or "\n" in r["mention"])
        add("multilingual failure", f"{'/'.join(sorted(langs & {'it', 'es'}))} text parsed by the English NER model"
                                    + (f"; {bad} clause-length spans" if bad else ""))
    if not finals:
        add("principal-selection failure", "no principal actor selected", True)
    elif not any(geo.is_country(k) for k in finals):
        add("principal-selection failure", f"no state among the principals ({', '.join(finals)}); check they are actors", True)
    return f


def agg(rows, key):
    c, first = Counter(), {}
    for r in rows:
        k = key(r)
        c[k] += 1
        first.setdefault(k, r)
    return [(first[k], n) for k, n in c.items()]


lines = []
w = lines.append
w("# Entity review sample — 2026-09-30")
w("")
w("Real Developments from a read-only copy of the daemon database (2026-09-25 → 09-30, English feeds) and the")
w("source-expansion evaluation collection (2026-09-30, Italian/Spanish feeds). Classification and principal actors were")
w("recomputed on working copies with current `main` (ee93a3e); NER was re-run with the pipeline's spaCy model on each item's")
w("headline + first 600 characters. Entity logic was not changed.")
w("")
w("**Selection** (made before any flag was read, except as noted): per domain, a seeded order (`sha1(seed:db:id)`), first an")
w("item from the multilingual collection when the domain has one, then the Developments adding the most unseen sources; a")
w("4th is taken from auto-flagged Developments only if none of the first three is flagged. No embedding scores, Situation")
w("decisions or ranking were used. The rules classifier assigns no Development to **humanitarian** or **institutional** in")
w("this data: those are sampled from domain `unknown` by source (UN / EU / central-bank feeds) or headline words, and marked")
w("*fallback*. Only 2 humanitarian candidates exist; economic has 3 in total.")
w("")
w("**Columns.** *Method* replays the resolver read-only: `new entity` = no existing match, the mention created the")
w("entity; `exact alias` / `normalised alias` / `seeded` = matched a recorded name; `fuzzy` = rapidfuzz ratio above the")
w("threshold (80 same type, 85 cross type); `unresolved` = detected by NER now but not linked to the item. *Downstream*:")
w("principal → ranking, Situation matching, UI actors; places (GPE/LOC/FAC) → clustering (segmentation's place check);")
w("provenance never uses entities; when a Development has no principal, Situation matching and the UI fall back to all")
w("mentioned actors. ⚑ marks automatic flags (heuristics, for your review — not conclusions).")
w("")
w("Review codes: `Y` / `N` / `?` (unsure).")
w("")
summary = []
failures = Counter()
ordered = sorted(data, key=lambda e: (DOMAINS.index(e["sampled_as"]), e["db"], e["id"]))
w("## Contents")
w("")
for n, ev in enumerate(ordered, 1):
    w(f"{n}. [{ev['sampled_as']}] {esc(ev['headline'], 90)} — `{ev['db']}#{ev['id']}`")
w("")
current = None
for n, ev in enumerate(ordered, 1):
    if ev["sampled_as"] != current:
        current = ev["sampled_as"]
        w(f"---\n\n# {current.capitalize()}\n")
    fl = flags(ev)
    for (cls, _), _p in fl.items():
        failures[cls] += 1
    w(f"## {n}. {esc(ev['headline'])}")
    w("")
    w(f"- **Development:** `{ev['db']}#{ev['id']}` (db `{'entity-review-en' if ev['db'] == 'en' else 'entity-review-ml'}`)")
    w(f"- **Domain / type:** {ev['domain']} / {ev['type']}" + (f" — sampled as **{ev['sampled_as']}** (fallback)" if ev["sampled_by_fallback"] else ""))
    w(f"- **Items:** {len(ev['items'])}; **sources:** {', '.join(sorted({i['source'] for i in ev['items']}))}; "
      f"**languages:** {', '.join(sorted({i['lang'] for i in ev['items']}))}")
    w("")
    w("### Source text")
    w("")
    w("| Item | Source | Lang | Published (UTC) | Headline | Lead |")
    w("|---|---|---|---|---|---|")
    for i in ev["items"]:
        w(f"| {i['id']} | {esc(i['source'])} | {i['lang']} | {i['published']} | {esc(i['title'], 140)} | {esc(i['lead'], 200)} |")
    w("")
    w("### Raw NER output")
    w("")
    w("| Text span | NER type | Kept by pipeline | × | Source sentence (first) |")
    w("|---|---|---|---:|---|")
    for r, k in agg(ev["ner"], lambda r: (r["text"], r["label"])):
        w(f"| {esc(r['text'], 60)} | {r['label']} | {'yes' if r['kept'] else 'no (label not stored)'} | {k} | {esc(r['sentence'], 150)} |")
    w("")
    w("### Resolution output + review")
    w("")
    w("| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |")
    w("|---|---|---|---|---|---:|---|---|---|---|---|---|")
    res_rows = agg(ev["resolution"], lambda r: (r["mention"], r["type"], r["canonical"], r["method"]))
    for r, k in sorted(res_rows, key=lambda x: (x[0]["method"] == "unresolved", x[0]["type"], x[0]["mention"])):
        w(f"| {esc(r['mention'], 60)} | {r['type']} | {esc(r['canonical'] or '—', 60)} | {r['method']} | {esc(r['reason'], 90)} | {k} | | | | | | |")
    w("")
    p = ev["principals"]
    w("### Principal actors")
    w("")
    w("| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |")
    w("|---|---|---|---|---|")
    for c, k in agg(p["candidates"], lambda c: (c["text"], c["field"], c["participant"], c["rejected"])):
        norm = "non-actor (dropped)" if c["non_actor"] else f"{c['surface']} → {c['key']}"
        w(f"| {c['field']} ×{k} | {esc(c['text'], 60)} | {'yes' if c['participant'] else 'no'} | {esc(c['rejected'] or '—')} | {esc(norm, 70)} |")
    w("")
    sup = ", ".join(f"{k} {v}" for k, v in sorted(p["support"].items(), key=lambda x: -x[1])) or "—"
    w(f"- **Support per actor** (headline 1.0, lead 0.5; needed {p['required']}): {esc(sup)}")
    w(f"- **Final principal actors:** {', '.join(p['final']) or '—'}")
    w(f"- **Entities flagged principal on the Development:** {', '.join(p['principal_entities']) or '—'}")
    w("")
    w("### Geography")
    w("")
    if ev["geography"]:
        w("| Place mention | Canonical place | Level | Contained in | Treated as actor? |")
        w("|---|---|---|---|---|")
        for g in ev["geography"]:
            w(f"| {esc(g['mention'], 50)} | {esc(g['canonical'], 40)} | {g['level']} | {esc(', '.join(g['contained_in']) or '—', 60)} | {'yes' if g['as_actor'] else 'no'} |")
    else:
        w("No place entities.")
    w("")
    w("### Current downstream effect")
    w("")
    w("| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |")
    w("|---|---|---|---|---|---|---|---|")
    yn = lambda b: "yes" if b else "—"   # noqa: E731
    for d in sorted(ev["downstream"], key=lambda d: (not d["principal"], d["type"], d["entity"])):
        w(f"| {esc(d['entity'], 60)} | {d['type']} | {yn(d['principal'])} | {yn(d['clustering'])} | {yn(d['situation'])} | "
          f"{yn(d['ranking'])} | — | {yn(d['ui'])} |")
    w("")
    if fl:
        w("### ⚑ Automatic flags")
        w("")
        for (cls, text), principal in fl.items():
            w(f"- **{cls}**{' (principal)' if principal else ''}: {esc(text)}")
        w("")
    w("### Development review")
    w("")
    w("```text")
    w("Overall actors correct? YES / NO / PARTIAL")
    w("Missing important actor:")
    w("Spurious actor:")
    w("Notes:")
    w("```")
    w("")
    mentions = len(ev["resolution"])
    suspect_entities = sum(1 for (c, _), pr in fl.items() if not pr and c != "multilingual failure")
    suspect_principals = sum(1 for (_, _), pr in fl.items() if pr and _ != "no principal actor selected")
    unresolved = sum(1 for r in ev["resolution"] if r["method"] == "unresolved")
    summary.append((ev["sampled_as"], mentions, suspect_entities, suspect_principals, unresolved))

w("---")
w("")
w("# Summary")
w("")
w("| Domain | Examples | Entity mentions | Suspect entities | Suspect principals | Unresolved |")
w("|---|---:|---:|---:|---:|---:|")
tot = [0, 0, 0, 0, 0]
for d in DOMAINS:
    rows = [s for s in summary if s[0] == d]
    vals = [len(rows)] + [sum(r[i] for r in rows) for i in range(1, 5)]
    tot = [a + b for a, b in zip(tot, vals)]
    w(f"| {d} | {' | '.join(str(v) for v in vals)} |")
w(f"| **total** | {' | '.join(f'**{v}**' for v in tot)} |")
w("")
w("Suspect counts are automatic flags (deduplicated per Development), not confirmed errors.")
w("")
w("## Suspected failures by class")
w("")
w("| Class | Flags |")
w("|---|---:|")
for c in CLASSES:
    w(f"| {c} | {failures.get(c, 0)} |")
w("")
open(out_path, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print(dict(failures)); print(tot)
