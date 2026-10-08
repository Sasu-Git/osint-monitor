"""Benchmark the (disabled) cross-language stage on Development-identity gold revision 3.

    python evaluations/identity/scripts/score_rev3_xlang.py   # -> runs/rev3-xlang.json

Replays the development windows holding revision 3 cases twice with the current code:
- off: the stage as configured (disabled), the production baseline;
- on: the stage switched on in memory only; the config file is not changed.

A gold pair is *together* when, at the end of the replay, both items share a Development ID. On the revision 3
additions it reports:
- SAME pairs together (true merges), DIFFERENT pairs together (false merges), SAME pairs apart (missed);
- precision, recall and F1 of "together" for SAME, off and on;
- what the stage itself changed (pairs together only when on);
- all of the above by candidate cosine band and by language pair, with and without the four contract-conflict
  cases.

It also records every accepted cross-language link with its evidence, and the regression cases (RAF Fairford,
Siberian plague, R138). The identity holdout is never replayed.
"""
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402

REGRESSION = {"G12": "RAF Fairford (SCMP en / El Pais es)", "G13": "RAF Fairford (BBC en / Clarin es)",
              "G14": "Siberian plague (Al Jazeera en / Europa Press es)", "G02": "R138 AI luncheon (it / en)",
              "G03": "R138 America.gov (es / en)"}


def replay_windows(enabled: bool, wanted: list[str], links_out: list):
    import replay_current
    from osint_monitor.core import config as C
    import osint_monitor.processors.clustering as CL
    from osint_monitor.processors import cross_language as X
    from osint_monitor.core.database import RawItem, get_session
    base_loader = getattr(C, "_orig_loader", C.load_event_grouping_config)
    C._orig_loader = base_loader

    def loader(*a, **k):
        cfg = base_loader(*a, **k)
        cfg.cross_language.enabled = enabled
        return cfg
    C.load_event_grouping_config = loader
    CL.load_event_grouping_config = loader
    base_propose = getattr(X, "_orig_propose", X.propose)
    X._orig_propose = base_propose
    state = {}

    def recording(units, config, geo):
        links = base_propose(units, config, geo)
        s = get_session()
        ids = [i for l in links for i in l.a.items + l.b.items]
        ext = dict(s.query(RawItem.id, RawItem.external_id).filter(RawItem.id.in_(ids))) if ids else {}
        s.close()
        for l in links:
            if l.accepted:
                links_out.append({"window": state["w"], "a": [ext[i] for i in l.a.items], "b": [ext[i] for i in l.b.items],
                                  "langs": [sorted(l.a.langs), sorted(l.b.langs)], "cosine": round(l.cosine, 3),
                                  "evidence": l.evidence})
        return links
    X.propose = recording
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    out = {}
    for w in manifest["windows"]:
        if w["id"] in wanted:
            assert w["split"] == "development"
            state["w"] = w["id"]
            t = replay_current.replay(w)
            out[w["id"]] = {i: set(r["developments"]) for i, r in t["items"].items()}
            print(("ON " if enabled else "OFF"), w["id"], len(t["developments"]), "Developments", flush=True)
    return out


def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else None
    r = tp / (tp + fn) if tp + fn else None
    f = 2 * p * r / (p + r) if p and r else None
    return {"tp": tp, "fp": fp, "fn": fn, "precision": p, "recall": r, "f1": f}


def main() -> int:
    adds = yaml.safe_load((ROOT / "gold" / "identity-gold-rev3-additions.yaml").read_text(encoding="utf-8"))
    strata = json.loads((ROOT / "review-rev3" / "strata.json").read_text(encoding="utf-8"))["strata"]
    wanted = sorted({e["window"] for e in adds.values()})
    links: list = []
    off = replay_windows(False, wanted, [])
    on = replay_windows(True, wanted, links)

    def together(state, e):
        return bool(state[e["window"]].get(e["a"], set()) & state[e["window"]].get(e["b"], set()))

    rows = []
    for cid, e in sorted(adds.items()):
        s = strata.get(cid, {})
        band = ("<0.65" if s.get("cosine", 1) < 0.65 else "0.65-0.75" if s.get("cosine", 1) < 0.75 else ">=0.75") \
            if s else "given"
        rows.append({"case": cid, "label": e["label"], "langs": "-".join(e["languages"]), "band": band,
                     "conflict": bool(e.get("contract_conflict")), "off": together(off, e), "on": together(on, e)})

    def score(sel, key):
        same = [r for r in sel if r["label"] == "SAME_DEVELOPMENT"]
        diff = [r for r in sel if r["label"] == "DIFFERENT_DEVELOPMENT"]
        return prf(sum(r[key] for r in same), sum(r[key] for r in diff), sum(not r[key] for r in same))

    def block(sel):
        return {"off": score(sel, "off"), "on": score(sel, "on"),
                "stage_added_true": sorted(r["case"] for r in sel if r["on"] and not r["off"] and r["label"] == "SAME_DEVELOPMENT"),
                "stage_added_false": sorted(r["case"] for r in sel if r["on"] and not r["off"] and r["label"] == "DIFFERENT_DEVELOPMENT"),
                "false_merges_on": sorted(r["case"] for r in sel if r["on"] and r["label"] == "DIFFERENT_DEVELOPMENT"),
                "missed_same_on": sorted(r["case"] for r in sel if not r["on"] and r["label"] == "SAME_DEVELOPMENT")}

    report = {"all": block(rows), "without_conflicts": block([r for r in rows if not r["conflict"]]),
              "by_band": {b: block([r for r in rows if r["band"] == b]) for b in sorted({r["band"] for r in rows})},
              "by_languages": {l: block([r for r in rows if r["langs"] == l]) for l in sorted({r["langs"] for r in rows})},
              "regression": {cid: {"case": REGRESSION[cid], "off": next(r["off"] for r in rows if r["case"] == cid),
                                   "on": next(r["on"] for r in rows if r["case"] == cid)} for cid in REGRESSION},
              "accepted_links": links, "accepted_link_count": len(links), "rows": rows}
    out = ROOT / "runs" / "rev3-xlang.json"
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    a, wc = report["all"], report["without_conflicts"]
    print("OFF", a["off"])
    print("ON ", a["on"])
    print("ON without conflicts", wc["on"])
    print("stage added true", a["stage_added_true"], "false", a["stage_added_false"])
    print("regression", report["regression"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
