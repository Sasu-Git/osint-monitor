"""E1 feasibility gate (EXPERIMENT-PLAN.md, procedure step 1 and amendment 1). No pipeline change; read-only.

    python feasibility.py --identity-wt ../osint-monitor-identity --actors-wt ../osint-monitor-actors \
        --code-wt ../osint-monitor-timing --out feasibility-results.json

For every development pair it computes the headline main action and its action class (frozen lexicon
``action_classes.yaml``), then:
  F1 = share of cross-day OVERMERGE pairs on which the guard would cut every link (gate: >= 40%);
  F2 = number of cross-day SAME pairs on which the guard would cut at least one link (gate: <= 1).
Holdout data is never read: gold entries with split != development and defect cases in the holdout window are dropped
before any other field is used.
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import html
import json
import sys
from datetime import datetime
from itertools import product
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
HOLDOUT_WINDOW = "2026-08-31"
MODELS = {"en": "en_core_web_lg", "es": "es_core_news_md", "it": "it_core_news_md"}
WINDOW_FILES = {
    "2026-08-21": "evaluations/clustering/windows/2026-08-21.items.jsonl",
    "2026-09-25": "evaluations/clustering/windows/2026-09-25.items.jsonl",
    "2026-09-30-multilingual": "evaluations/identity/windows/2026-09-30-multilingual.items.jsonl",
    "2026-10-03-live": "evaluations/identity/windows/2026-10-03-live.items.jsonl",
    "2026-10-05-live": "evaluations/identity/windows/2026-10-05-live.items.jsonl",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def when(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("T", " ")[:19])


class Actions:
    def __init__(self, lexicon: dict):
        import spacy
        self.nlp = {lang: spacy.load(name) for lang, name in MODELS.items()}
        self.generic = {lang: set(v) for lang, v in lexicon["generic"].items()}
        self.cls = {lang: {} for lang in MODELS}
        for name, langs in lexicon["classes"].items():
            for lang, lemmas in langs.items():
                for lemma in lemmas:
                    self.cls[lang][lemma] = name
        self.cache: dict[tuple[str, str], dict] = {}

    def __call__(self, title: str, lang: str) -> dict:
        key = (title, lang)
        if key not in self.cache:
            self.cache[key] = self._action(title, lang)
        return self.cache[key]

    def _action(self, title: str, lang: str) -> dict:
        if lang not in self.nlp:
            return {"lemma": None, "class": None, "why": f"no model for {lang}"}
        doc = self.nlp[lang](html.unescape(title))
        for sent in doc.sents:
            root = sent.root
            if root.pos_ in ("VERB", "NOUN", "PROPN"):
                lemma = root.lemma_.lower()
                if lemma in self.generic[lang]:
                    return {"lemma": lemma, "class": None, "why": "generic"}
                cls = self.cls[lang].get(lemma)
                return {"lemma": lemma, "class": cls, "why": None if cls else "out of lexicon"}
        return {"lemma": None, "class": None, "why": "no verbal or nominal root"}


def fires(x: dict, y: dict, actions: Actions, headline_kind, report: str) -> tuple[bool, str]:
    """The guard on one item link: (fires, reason it does or does not)."""
    hours = abs((when(x["published_at"]) - when(y["published_at"])).total_seconds()) / 3600
    if hours <= 24:
        return False, "within 24 h"
    if headline_kind(x["title"]) != report or headline_kind(y["title"]) != report:
        return False, "not both report headlines"
    ax, ay = actions(x["title"], x["lang"]), actions(y["title"], y["lang"])
    if not ax["class"] or not ay["class"]:
        return False, "main action not classed"
    if ax["class"] == ay["class"]:
        return False, "same class"
    return True, "classes differ"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--identity-wt", type=Path, required=True, help="worktree of fix/identity-defects (e98a0fe or later)")
    p.add_argument("--actors-wt", type=Path, required=True, help="worktree of fix/actor-hygiene (Phase 2 dev run)")
    p.add_argument("--code-wt", type=Path, required=True, help="worktree whose segmentation code defines headline_kind")
    p.add_argument("--out", type=Path, default=HERE / "feasibility-results.json")
    a = p.parse_args()
    if sys.platform == "win32":
        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)

    sys.path.insert(0, str(a.code_wt.resolve()))
    from osint_monitor.processors.development_segmentation import REPORT, headline_kind

    lexicon_path = HERE / "action_classes.yaml"
    inputs = {
        "lexicon": lexicon_path,
        "gold_rev2": a.identity_wt / "evaluations/identity/gold/identity-gold.yaml",
        "gold_rev3_additions": a.identity_wt / "evaluations/identity/gold/identity-gold-rev3-additions.yaml",
        "defect_set": a.identity_wt / "evaluations/identity/defects/defect-cases.json",
        "phase2_dev_run": a.actors_wt / "evaluations/identity/runs/phase2-dev-actor-hygiene.json",
        **{f"window {w}": a.identity_wt / f for w, f in WINDOW_FILES.items()},
    }
    hashes = {k: sha256(v) for k, v in inputs.items()}

    items = {}
    for w, f in WINDOW_FILES.items():
        for line in (a.identity_wt / f).read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            # the wayback clustering windows carry no lang field: they are English-only benchmark windows
            items[r["id"]] = {"item": r["id"], "title": r["title"], "lang": r.get("lang") or "en",
                              "published_at": r["published_at"]}

    cases: dict[tuple, dict] = {}

    def add(side_a, side_b, label, source, overmerge):
        key = tuple(sorted([tuple(sorted(i["item"] for i in side_a)), tuple(sorted(i["item"] for i in side_b))]))
        c = cases.setdefault(key, {"a": side_a, "b": side_b, "labels": set(), "sources": [], "overmerge": False})
        c["labels"].add(label)
        c["sources"].append(source)
        c["overmerge"] |= overmerge

    gold = {}
    for name in ("gold_rev2", "gold_rev3_additions"):
        for cid, e in yaml.safe_load(inputs[name].read_text(encoding="utf-8")).items():
            if e["split"] != "development":
                continue
            gold[cid] = e

    kept = set()
    for w in json.loads(inputs["phase2_dev_run"].read_text(encoding="utf-8"))["windows"]:
        if w["window"] == HOLDOUT_WINDOW:
            continue
        for row in w["ledger"]:
            if row["gold"] == "DIFFERENT_DEVELOPMENT" and row["current"] == "kept together":
                kept.add(row["case"])

    for cid, e in gold.items():
        if e["label"] == "AMBIGUOUS":
            continue
        add([items[e["a"]]], [items[e["b"]]], e["label"], f"gold {cid}", cid in kept)

    for c in json.loads(inputs["defect_set"].read_text(encoding="utf-8"))["cases"]:
        if c["window"] == HOLDOUT_WINDOW or c["expected"] == "AMBIGUOUS":
            continue
        side = lambda s: [{k: i[k] for k in ("item", "title", "lang", "published_at")} for i in c[s]["items"]]  # noqa: E731
        add(side("a"), side("b"), c["expected"], f"defect {c['case']} {c['class']}", c["class"] == "OVERMERGE")

    actions = Actions(yaml.safe_load(lexicon_path.read_text(encoding="utf-8")))
    rows, conflicts = [], []
    for key, c in cases.items():
        if len(c["labels"]) > 1:
            conflicts.append({"sources": c["sources"], "labels": sorted(c["labels"])})
            continue
        label = next(iter(c["labels"]))
        links = []
        for x, y in product(c["a"], c["b"]):
            if x["item"] == y["item"]:
                continue
            hours = abs((when(x["published_at"]) - when(y["published_at"])).total_seconds()) / 3600
            fired, why = fires(x, y, actions, headline_kind, REPORT)
            links.append({"a": x["item"], "b": y["item"], "hours": round(hours, 1), "fires": fired, "why": why})
        if not links:
            continue
        cross_day = all(l["hours"] > 24 for l in links) if label == "DIFFERENT_DEVELOPMENT" \
            else any(l["hours"] > 24 for l in links)
        if not cross_day:
            continue
        single = len(c["a"]) == 1 and len(c["b"]) == 1
        detail = None
        if single:
            x, y = c["a"][0], c["b"][0]
            detail = {"a": {"title": x["title"], "lang": x["lang"], **actions(x["title"], x["lang"])},
                      "b": {"title": y["title"], "lang": y["lang"], **actions(y["title"], y["lang"])}}
        rows.append({
            "sources": c["sources"], "label": label, "overmerge": c["overmerge"],
            "links": len(links), "links_fired": sum(l["fires"] for l in links),
            "cuts_all": all(l["fires"] for l in links), "cuts_any": any(l["fires"] for l in links),
            "why_not": sorted({l["why"] for l in links if not l["fires"]}),
            "hours_min": min(l["hours"] for l in links), "hours_max": max(l["hours"] for l in links),
            "single": detail,
        })

    om = [r for r in rows if r["label"] == "DIFFERENT_DEVELOPMENT" and r["overmerge"]]
    diff = [r for r in rows if r["label"] == "DIFFERENT_DEVELOPMENT"]
    same = [r for r in rows if r["label"] == "SAME_DEVELOPMENT"]
    f1 = sum(r["cuts_all"] for r in om)
    f2 = sum(r["cuts_any"] for r in same)
    summary = {
        "F1": {"cut": f1, "of": len(om), "rate": round(f1 / len(om), 3) if om else None, "gate": ">= 0.40",
               "pass": bool(om) and f1 / len(om) >= 0.40},
        "F2": {"cut": f2, "of": len(same), "gate": "<= 1", "pass": f2 <= 1},
        "secondary": {
            "F1_any_link": sum(r["cuts_any"] for r in om),
            "all_cross_day_different_cut_all": [sum(r["cuts_all"] for r in diff), len(diff)],
        },
        "conflicts": conflicts,
    }
    summary["gate"] = "PASS" if summary["F1"]["pass"] and summary["F2"]["pass"] else "FAIL"
    a.out.write_text(json.dumps({"inputs": {k: str(v) for k, v in inputs.items()}, "sha256": hashes,
                                 "summary": summary, "rows": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
