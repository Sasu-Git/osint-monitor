"""Build the frozen, blind L1-L3 labelling packet from the frozen dataset selection (no measurement, no DA rule).

    python build_labelling.py --db data/eval/snapshot-20261027-forensic.db --code-wt ../osint-monitor-timing \
        --dataset ../dataset --out .

Reads the snapshot read-only (sqlite3, mode=ro) and imports only presentation helpers from the production code
(headline kind, roundup detection, the pipeline's item-language function). Writes:
- review-cases.json  what the reviewer sees: per case a reference report and one candidate (pair), or a reference
                     and the sampled members (set). No Development id, no label set, no source of the case, no
                     score, no threshold, no expected answer. Cases are shuffled with a fixed seed.
- key.json           per case: label set (L1, L2, L2b, L3a, L3b), Development id, stratum, item ids. Never served.
- FREEZE-LABELLING.json  hashes of inputs, outputs, scripts; code and snapshot identity; counts.
Reference report (EXPERIMENT-PLAN.md amendment 1): the earliest-published founder whose headline kind is REPORT and
which is not a roundup (ties: lowest id); if no founder qualifies, the earliest founder, recorded as a fallback.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import random
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

SEED = 20261028
EXCERPT = 420
ACTOR_TYPES = ("PERSON", "ORG", "NORP")
PLACE_TYPES = ("GPE", "LOC", "FAC")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", type=Path, required=True)
    ap.add_argument("--code-wt", type=Path, required=True)
    ap.add_argument("--dataset", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    sys.path.insert(0, str(a.code_wt.resolve()))
    from osint_monitor.processors.actor_roles import is_roundup
    from osint_monitor.processors.development_segmentation import REPORT, headline_kind
    from osint_monitor.processors.language import item_language

    db = sqlite3.connect(f"file:{a.db.resolve().as_posix()}?mode=ro", uri=True)
    giants = json.loads((a.dataset / "giant-label-sample.json").read_text(encoding="utf-8"))
    large = json.loads((a.dataset / "large-occurrence-candidates.json").read_text(encoding="utf-8"))

    def item(i: int) -> dict:
        title, content, url, pub, src = db.execute(
            "select ri.title, ri.content, ri.url, ri.published_at, so.name from raw_items ri "
            "join sources so on so.id = ri.source_id where ri.id = ?", (i,)).fetchone()
        text = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", content or "")).split())
        if text.lower().startswith((title or "").lower()):
            text = text[len(title or ""):].strip(" .-:")
        ents = db.execute("select e.canonical_name, e.entity_type from item_entities ie join entities e "
                          "on e.id = ie.entity_id where ie.item_id = ?", (i,)).fetchall()
        actors = sorted({n for n, t in ents if t in ACTOR_TYPES})[:8]
        places = sorted({n for n, t in ents if t in PLACE_TYPES})[:8]
        return {"title": title or "", "source": src, "published": (pub or "")[:16],
                "language": item_language(src, f"{title or ''}. {(content or '')[:500]}"),
                "excerpt": (text[:EXCERPT] + (" …" if len(text) > EXCERPT else "")) if text else "",
                "actors": actors, "places": places,
                "url": url if url and url.startswith(("http://", "https://")) else ""}

    def reference(founders: list[dict]) -> tuple[int, bool]:
        ok = [f for f in founders if headline_kind(f["title"] or "") == REPORT and not is_roundup(f["title"] or "")]
        pool, fallback = (ok, False) if ok else (founders, True)
        best = min(pool, key=lambda f: (f["published_at"] or "9999", f["item_id"]))
        return best["item_id"], fallback

    cases, key, fallbacks = [], {}, []

    def add(kind, lset, eid, ref, cand=None, members=None, stratum=None):
        cases.append({"kind": kind, "reference": ref, "candidate": cand, "members": members})
        key[len(cases) - 1] = {"set": lset, "event_id": eid, "stratum": stratum}

    for g in giants:
        ref_id, fb = reference(g["founders"])
        if fb:
            fallbacks.append(g["event_id"])
        ref = item(ref_id)
        for f in g["founders"]:
            if f["item_id"] != ref_id:
                add("pair", "L1", g["event_id"], (ref_id, ref), (f["item_id"], item(f["item_id"])), stratum="founder")
        for m in g["sample"]:
            add("pair", "L2", g["event_id"], (ref_id, ref), (m["item_id"], item(m["item_id"])), stratum=m["stratum"])
        add("set", "L2b", g["event_id"], (ref_id, ref), members=[(m["item_id"], item(m["item_id"])) for m in g["sample"][::2]])
    for d in large:
        founders = db.execute("select ei.item_id, ri.title, ri.published_at, ei.added_run_id from event_items ei "
                              "join raw_items ri on ri.id = ei.item_id where ei.event_id = ? order by ei.added_at, ei.item_id",
                              (d["event_id"],)).fetchall()
        first_run = founders[0][3]
        fs = [{"item_id": i, "title": t, "published_at": p} for i, t, p, r in founders if r == first_run]
        ref_id, fb = reference(fs)
        if fb:
            fallbacks.append(d["event_id"])
        ref = item(ref_id)
        sample = [m for m in d["sample"] if m["item_id"] != ref_id]
        for m in sample:
            add("pair", "L3a", d["event_id"], (ref_id, ref), (m["item_id"], item(m["item_id"])), stratum="large")
        add("set", "L3b", d["event_id"], (ref_id, ref), members=[(m["item_id"], item(m["item_id"])) for m in sample])

    order = list(range(len(cases)))
    random.Random(SEED).shuffle(order)
    review, key_out = [], {}
    for n, k in enumerate(order, start=1):
        c, cid = cases[k], f"R{n:03d}"
        review.append({"case": cid, "kind": c["kind"], "reference": c["reference"][1],
                       "candidate": c["candidate"][1] if c["candidate"] else None,
                       "members": [m[1] for m in c["members"]] if c["members"] else None})
        key_out[cid] = {**key[k], "reference_item": c["reference"][0],
                        "candidate_item": c["candidate"][0] if c["candidate"] else None,
                        "member_items": [m[0] for m in c["members"]] if c["members"] else None}
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "review-cases.json").write_text(json.dumps(review, ensure_ascii=False, indent=1), encoding="utf-8")
    (a.out / "key.json").write_text(json.dumps(key_out, ensure_ascii=False, indent=1), encoding="utf-8")

    def git(*args):
        return subprocess.run(["git", "-C", str(a.code_wt), *args], capture_output=True, text=True).stdout.strip()
    counts = {}
    for v in key_out.values():
        counts[v["set"]] = counts.get(v["set"], 0) + 1
    freeze = {
        "seed": SEED, "cases": len(review), "by_set": counts, "reference_fallbacks": fallbacks,
        "code": {"worktree": str(a.code_wt), "sha": git("rev-parse", "HEAD"), "dirty": bool(git("status", "--porcelain"))},
        "snapshot": {"path": str(a.db), "sha256": hashlib.sha256(a.db.read_bytes()).hexdigest()},
        "dataset_freeze_sha256": sha(a.dataset / "FREEZE.json"),
        "inputs": {n: sha(a.dataset / n) for n in ("giant-label-sample.json", "large-occurrence-candidates.json")},
        "outputs": {n: sha(a.out / n) for n in ("review-cases.json", "key.json")},
        "scripts": {n: sha(a.out / n) for n in ("build_labelling.py", "review_server.py", "review.html", "labels_tool.py")
                    if (a.out / n).exists()},
        "plan": {n: sha(a.out.resolve().parent / n) for n in ("EXPERIMENT-PLAN.md", "ACCEPTANCE-GATE.md", "ARCHITECTURE.md",
                                                     "DATASET-MANIFEST.md")},
    }
    (a.out / "FREEZE-LABELLING.json").write_text(json.dumps(freeze, indent=1), encoding="utf-8")
    print(json.dumps({k: freeze[k] for k in ("cases", "by_set", "reference_fallbacks")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
