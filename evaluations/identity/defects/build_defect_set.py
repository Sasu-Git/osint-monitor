"""Build the Development-identity defect review set (2026-10-09): identity failures that block or distort Phase 3.

    python evaluations/identity/defects/build_defect_set.py   # -> defect-cases.json, defect-review.md, manifest.yaml

Baseline: the accepted identity code (fix/cross-language-identity 0eff3ea: Phase 2 identity, GDELT headline-only
rule; the rejected cross-language stage disabled). No identity logic is changed. Current Developments come from the
existing replays of that code (deterministic; identical across replay sets):
- evaluations/relations/runtime/runs/ for 2026-10-03-live, 2026-10-05-live, 2026-10-08-live;
- evaluations/relations/runs-rev2/ for the other development windows.

Case sources (each with an owner-approved expected identity):
- RB: the 22 scored BLOCKED_BY_IDENTITY relation gold pairs (relation gold revision 2: two distinct occurrences);
- RT: SAME_DEVELOPMENT_SUSPECTED verdicts of the runtime benchmark and the targeted batch (owner: one occurrence);
- IG: identity gold (revision 2 development cases, revision 4 additions) the baseline gets wrong;
- CT: correct-behaviour controls: seeded identity gold cases the baseline gets right, plus the owner-confirmed
  correct merges among the blocked relation pairs (T008, T034, T041).
Pairs naming the same two item sets are merged into one case that lists every reference. Development holdouts and
sealed holdouts are not read (the identity gold's holdout split is excluded).

Classes (mechanical, from the expected identity and the current Developments):
- OVERMERGE: expected different, currently in one Development;
- CROSS_LANGUAGE_MISS: expected same, apart, the two sides share no language;
- LATE_ATTACHMENT_MISS: expected same, apart, same language, the sides arrive in different ticks and the earlier one
  is in a Development;
- SPLIT: expected same, apart, same language, both sides in (different) Developments;
- SAME_LANGUAGE_RECALL_MISS: expected same, apart, same language, otherwise (a side in no Development);
- CORRECT_BEHAVIOR: the baseline matches the expected identity;
- AMBIGUOUS: the expected identity is AMBIGUOUS.
"""
import hashlib
import json
import random
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
EVAL = HERE.parents[1]
REL, IDN = EVAL / "relations", EVAL / "identity"
sys.stdout.reconfigure(encoding="utf-8")
SEED = 20261009
RUNTIME_WINDOWS = {"2026-10-03-live", "2026-10-05-live", "2026-10-08-live"}


def when(v):
    return datetime.fromisoformat(str(v).replace("Z", "")) if v else None


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_windows():
    """window id -> {items: id -> item row, start, tick_hours, trace, trace_path}"""
    out = {}
    specs = []
    for w in yaml.safe_load((IDN / "manifest.yaml").read_text(encoding="utf-8"))["windows"]:
        if w["split"] == "development":
            specs.append((w["id"], (IDN / w["items_file"]).resolve(), w["start"]))
    for w in yaml.safe_load((REL / "manifest.yaml").read_text(encoding="utf-8"))["windows"]:
        if w["split"] == "development":
            specs.append((w["id"], (REL / w["items_file"]).resolve(), w["start"]))
    for w in yaml.safe_load((REL / "runtime" / "manifest.yaml").read_text(encoding="utf-8"))["windows"]:
        specs.append((w["id"], (REL / "runtime" / w["items_file"]).resolve(), w["start"]))
    for wid, items_file, start in specs:
        if wid in out:
            continue
        tpath = (REL / "runtime" / "runs" / f"{wid}.json") if wid in RUNTIME_WINDOWS else (REL / "runs-rev2" / f"{wid}.json")
        trace = json.loads(tpath.read_text(encoding="utf-8"))
        items = {}
        for line in items_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                items[r["id"]] = r
        out[wid] = {"items": items, "start": when(start), "trace": trace, "trace_path": tpath, "items_file": items_file}
    return out


def tick(w, item_id):
    r = w["items"][item_id]
    t = when(r.get("published_at") or r.get("fetched_at"))
    if not t or t < w["start"]:
        return 1
    return int((t - w["start"]) / timedelta(hours=12)) + 1


def describe(w, members):
    tr = w["trace"]
    rows = []
    for m in members:
        it, tri = w["items"].get(m, {}), tr["items"].get(m, {})
        rows.append({"item": m, "source": it.get("source"), "lang": tri.get("lang") or it.get("lang"),
                     "published_at": str(it.get("published_at") or it.get("fetched_at") or "")[:16],
                     "tick": tick(w, m), "title": it.get("title"),
                     "developments": sorted(tri.get("developments") or [])})
    devs = sorted({d for r in rows for d in r["developments"]})
    principals = sorted({p for d in devs for p in (tr["developments"][str(d)].get("principals") or [])})
    places = sorted({p for m in members for p in (tr["items"].get(m, {}).get("places") or [])})
    return {"items": rows, "developments": devs, "langs": sorted({r["lang"] for r in rows if r["lang"]}),
            "actors": principals[:12], "places": places[:12],
            "development_sizes": {str(d): len(tr["developments"][str(d)]["members"]) for d in devs}}


def classify(expected, a, b):
    together = bool(set(a["developments"]) & set(b["developments"]))
    if expected == "AMBIGUOUS":
        return "AMBIGUOUS"
    if expected == "DIFFERENT_DEVELOPMENT":
        return "OVERMERGE" if together else "CORRECT_BEHAVIOR"
    if together:
        return "CORRECT_BEHAVIOR"
    if not set(a["langs"]) & set(b["langs"]):
        return "CROSS_LANGUAGE_MISS"
    ta, tb = min(r["tick"] for r in a["items"]), min(r["tick"] for r in b["items"])
    earlier = a if ta <= tb else b
    if ta != tb and earlier["developments"]:
        return "LATE_ATTACHMENT_MISS"
    if a["developments"] and b["developments"]:
        return "SPLIT"
    return "SAME_LANGUAGE_RECALL_MISS"


def main() -> int:
    windows = load_windows()
    cases: dict = {}

    def add(window, a_members, b_members, expected, approval, ref, note=None, root=None):
        key = (window, frozenset(a_members), frozenset(b_members))
        alt = (window, frozenset(b_members), frozenset(a_members))
        if alt in cases:
            key = alt
        c = cases.setdefault(key, {"window": window, "a_members": list(a_members), "b_members": list(b_members),
                                   "expected": expected, "approval": approval, "refs": [], "notes": [],
                                   "root_hints": []})
        c["refs"].append(ref)
        if note:
            c["notes"].append(note)
        if root:
            c["root_hints"].append(root)
        if c["expected"] != expected:
            c["notes"].append(f"conflicting expected identity from {ref}: {expected}")

    # RB: blocked relation pairs (scored)
    elig = yaml.safe_load((REL / "runtime-eligibility-rev2.yaml").read_text(encoding="utf-8"))["cases"]
    rgold = yaml.safe_load((REL / "gold" / "relation-gold-rev2.yaml").read_text(encoding="utf-8"))
    sides = yaml.safe_load((REL / "gold" / "relation-sides-rev2.yaml").read_text(encoding="utf-8"))
    for cid, e in elig.items():
        if e["status"] != "BLOCKED_BY_IDENTITY":
            continue
        g = rgold[cid]
        a, b = sides[g["a"]], sides[g["b"]]
        if e["scored"]:
            add(a["window"], a["members"], b["members"], "DIFFERENT_DEVELOPMENT",
                f"relation gold rev 2 {cid} = {g['label']} (owner verdict: two distinct occurrences)",
                f"RB {cid} ({g['label']})", root="relation pair inside one Development")
        elif g.get("identity_verdict") == "SAME_DEVELOPMENT":
            add(a["window"], a["members"], b["members"], "SAME_DEVELOPMENT",
                f"owner identity verdict 2026-10-07b ({cid})", f"CT {cid} (blocked relation pair, correct merge)")
    # RT: runtime benchmark and targeted batch identity suspects
    for gpath, key in ((REL / "runtime" / "gold" / "runtime-gold.yaml", "runtime benchmark"),
                       (REL / "runtime-targeted" / "gold" / "targeted-gold.yaml", "targeted batch")):
        for cid, e in yaml.safe_load(gpath.read_text(encoding="utf-8")).items():
            if e["label"] == "SAME_DEVELOPMENT_SUSPECTED":
                add(e["window"], e["a"]["members"], e["b"]["members"], "SAME_DEVELOPMENT",
                    f"owner verdict 2026-10-09 ({key} {cid}: SAME_DEVELOPMENT_SUSPECTED)", f"RT {cid}",
                    note="both sides are system Developments the owner judged one occurrence")
    # IG: identity gold the baseline gets wrong (and the control pool)
    gold2 = {k: v for k, v in yaml.safe_load((IDN / "gold" / "identity-gold.yaml").read_text(encoding="utf-8")).items()
             if v["split"] == "development"}
    adds = yaml.safe_load((IDN / "gold" / "identity-gold-rev3-additions.yaml").read_text(encoding="utf-8"))
    ledger = {}
    for w in json.loads((IDN / "runs" / "phase2-dev-xlang-off-clock.json").read_text(encoding="utf-8"))["windows"]:
        for e in w["ledger"]:
            ledger[e["case"]] = e
    pool = []
    for cid, e in sorted({**gold2, **adds}.items()):
        w = windows[e["window"]]
        a, b = describe(w, [e["a"]]), describe(w, [e["b"]])
        cls = classify(e["label"], a, b)
        approval = (f"identity gold rev 2 {cid} ({e.get('source')})" if cid in gold2
                    else f"identity gold rev 4 {cid} ({e.get('source')})")
        if cls == "CORRECT_BEHAVIOR":
            pool.append((cid, e, approval))
            continue
        le = ledger.get(cid, {})
        add(e["window"], [e["a"]], [e["b"]], e["label"], approval, f"IG {cid}",
            note=e.get("note") or e.get("boundary_reason"),
            root=le.get("root_cause") or le.get("error_class"))
    # CT: seeded controls (10 SAME kept together, 10 DIFFERENT kept apart), revision 2 development cases
    rng = random.Random(SEED)
    for label in ("SAME_DEVELOPMENT", "DIFFERENT_DEVELOPMENT"):
        cand = [p for p in pool if p[1]["label"] == label and p[0] in gold2]
        for cid, e, approval in rng.sample(cand, min(10, len(cand))):
            add(e["window"], [e["a"]], [e["b"]], e["label"], approval, f"CT {cid} (control)")

    out = []
    for n, (key, c) in enumerate(sorted(cases.items(), key=lambda kv: (kv[1]["window"], kv[1]["refs"][0])), 1):
        w = windows[c["window"]]
        a, b = describe(w, c["a_members"]), describe(w, c["b_members"])
        cls = classify(c["expected"], a, b)
        if cls == "OVERMERGE":
            dev = sorted(set(a["developments"]) & set(b["developments"]))
            root = (c["root_hints"][0] if c["root_hints"] else "whole-storyline overmerge") + \
                f" (shared Development {dev}, {a['development_sizes'].get(str(dev[0]))} items)"
            blocks = "yes: the two occurrences have no distinct Development endpoints"
        elif cls == "CROSS_LANGUAGE_MISS":
            root = "English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)"
            blocks = "distorts: one occurrence has a Development per language (duplicate endpoints)"
        elif cls in ("SPLIT", "LATE_ATTACHMENT_MISS", "SAME_LANGUAGE_RECALL_MISS"):
            root = c["root_hints"][0] if c["root_hints"] else {
                "SPLIT": "two same-language clusters not linked (below the link threshold or cut by segmentation)",
                "LATE_ATTACHMENT_MISS": "a later report did not attach to the existing Development",
                "SAME_LANGUAGE_RECALL_MISS": "a report not clustered (no Development)"}[cls]
            blocks = ("distorts: duplicate endpoints for one occurrence" if a["developments"] and b["developments"]
                      else "yes: a side has no Development (NOT_SURFACED)")
        elif cls == "CORRECT_BEHAVIOR":
            root, blocks = "-", "no"
        else:
            root, blocks = "expected identity is AMBIGUOUS", "unknown"
        out.append({"case": f"D{n:03d}", "class": cls, "window": c["window"], "expected": c["expected"],
                    "approval": c["approval"], "refs": c["refs"], "notes": [x for x in c["notes"] if x],
                    "root_cause": root, "blocks_phase3_endpoint": blocks, "a": a, "b": b})

    (HERE / "defect-cases.json").write_text(json.dumps({"baseline": "0eff3ea (identity code; cross-language stage disabled)",
                                                        "cases": out}, indent=1, ensure_ascii=False) + "\n",
                                            encoding="utf-8", newline="\n")
    write_sheet(out)
    counts = Counter(c["class"] for c in out)
    sources = defaultdict(Counter)
    for c in out:
        for r in c["refs"]:
            sources[r.split(" ")[0]][c["class"]] += 1
    inputs = {str(p.relative_to(EVAL)): sha256(p) for p in sorted(
        {w["trace_path"] for w in windows.values()} | {w["items_file"] for w in windows.values()} |
        {REL / "runtime-eligibility-rev2.yaml", REL / "gold" / "relation-gold-rev2.yaml",
         REL / "gold" / "relation-sides-rev2.yaml", REL / "runtime" / "gold" / "runtime-gold.yaml",
         REL / "runtime-targeted" / "gold" / "targeted-gold.yaml", IDN / "gold" / "identity-gold.yaml",
         IDN / "gold" / "identity-gold-rev3-additions.yaml", IDN / "runs" / "phase2-dev-xlang-off-clock.json"})}
    manifest = {"frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "state": "FROZEN candidate manifest: identity defect review set (no identity logic changed)",
                "baseline": "identity code 0eff3ea; cross-language stage disabled", "seed": SEED,
                "cases": len(out), "by_class": dict(sorted(counts.items())),
                "by_source": {k: dict(v) for k, v in sorted(sources.items())},
                "outputs": {f: sha256(HERE / f) for f in ("defect-cases.json", "defect-review.md")},
                "inputs": inputs,
                "script": sha256(Path(__file__))}
    (HERE / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, width=120),
                                        encoding="utf-8", newline="\n")
    vpath = HERE / "owner-verdicts.yaml"
    if not vpath.exists():
        vpath.write_text("# Owner verdicts on the identity defect set: per case, class (ACCEPT or a corrected class),\n"
                         "# expected (ACCEPT or a corrected identity), note. Never overwritten by the builder.\n"
                         + yaml.safe_dump({c["case"]: {"class": None, "expected": None, "note": None} for c in out},
                                          sort_keys=True, width=120), encoding="utf-8", newline="\n")
    print(dict(sorted(counts.items())))
    print({k: dict(v) for k, v in sorted(sources.items())})
    return 0


def write_sheet(cases):
    order = ["OVERMERGE", "CROSS_LANGUAGE_MISS", "SPLIT", "LATE_ATTACHMENT_MISS", "SAME_LANGUAGE_RECALL_MISS",
             "AMBIGUOUS", "CORRECT_BEHAVIOR"]
    counts = Counter(c["class"] for c in cases)
    lines = ["# Development identity defect set: owner review", "",
             "Baseline: identity code `0eff3ea` (Phase 2 identity, GDELT headline-only rule; cross-language stage "
             "disabled). Nothing in identity logic has changed. Each case is a pair of item sets with the owner-approved "
             "expected identity, the Developments the baseline forms today, the class and the suspected root cause. "
             "Record verdicts in `owner-verdicts.yaml` (class / expected: ACCEPT or a correction; note).", "",
             "| class | cases |", "|---|---|"] + [f"| {k} | {counts.get(k, 0)} |" for k in order] + [""]

    def side(tag, s):
        out = [f"**{tag}** Developments {', '.join(f'D{d} ({s['development_sizes'][str(d)]} items)' for d in s['developments']) or 'none (not surfaced)'}"
               f" · langs {', '.join(s['langs'])}",
               f"  actors: {', '.join(s['actors']) or '-'} · places: {', '.join(s['places']) or '-'}"]
        for r in s["items"]:
            devs = ",".join(f"D{d}" for d in r["developments"]) or "-"
            out.append(f"- `{r['item']}` {r['published_at']} (tick {r['tick']}) [{r['source']}, {r['lang']}] [{devs}] "
                       f"{(r['title'] or '')[:150]}")
        return out
    for cls in order:
        sel = [c for c in cases if c["class"] == cls]
        if not sel:
            continue
        lines += [f"## {cls} ({len(sel)})", ""]
        for c in sel:
            lines += [f"### {c['case']} · {c['window']}", "",
                      f"- **Expected:** {c['expected']} ({c['approval']})",
                      f"- **References:** {'; '.join(c['refs'])}",
                      f"- **Root cause (suspected):** {c['root_cause']}",
                      f"- **Blocks a Phase 3 endpoint:** {c['blocks_phase3_endpoint']}"]
            if c["notes"]:
                lines.append(f"- **Notes:** {'; '.join(str(n) for n in c['notes'])}")
            lines += [""] + side("A", c["a"]) + [""] + side("B", c["b"]) + ["", "---", ""]
    (HERE / "defect-review.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    sys.exit(main())
