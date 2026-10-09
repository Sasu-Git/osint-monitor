"""Run one pre-registered acceptance-guard experiment (evaluations/identity/xlang-guard-tuning-plan.md).

    python evaluations/identity/scripts/run_guard_experiments.py --exp OFF|E0|E1|E2a|E2b|E3|E4|E5|E6|E7 [--k K]
    python evaluations/identity/scripts/run_guard_experiments.py --summary

One replay of every development window per experiment (config changed in memory only; the config file is not
touched). From the same replay it scores the identity gold revision 4 additions and the Phase 2 identity gold
(revision 2 development cases). Results: runs/xlang-guard/NAME.json. ``--summary`` compares every experiment with
the stage-off run (OFF) and applies the plan's qualification and selection rule. Holdouts are never replayed.
"""
import json
import os
import sys
from collections import Counter
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")

import yaml  # noqa: E402

OUT = ROOT / "runs" / "xlang-guard"
REGRESSION = {"G12": "RAF Fairford (SCMP en / El Pais es)", "G13": "RAF Fairford (BBC en / Clarin es)",
              "G14": "Siberian plague (Al Jazeera en / Europa Press es)", "G02": "R138 AI luncheon (it / en)",
              "G03": "R138 America.gov (es / en)", "C006": "GDELT recall case (es / en)"}
MANDATORY = ("G12", "G13", "G14")


def experiments(k: int | None) -> dict[str, dict]:
    return {
        "OFF": {"enabled": False},
        "E0": {"enabled": True},
        "E1": {"enabled": True, "require_anchor_classes": 2},
        "E2a": {"enabled": True, "broad_anchor_units": 3},
        "E2b": {"enabled": True, "broad_anchor_units": 5},
        "E3": {"enabled": True, "direct_links_only": True},
        "E4": {"enabled": True, "exact_places": True},
        "E5": {"enabled": True, "broad_anchor_units": k, "direct_links_only": True, "exact_places": True},
        "E6": {"enabled": True, "require_anchor_classes": 2, "direct_links_only": True, "exact_places": True},
        "E7": {"enabled": True, "require_anchor_classes": 2, "broad_anchor_units": k, "direct_links_only": True,
               "exact_places": True},
    }


def run(name: str, overrides: dict) -> dict:
    import replay_current
    from phase2_baseline import score
    from osint_monitor.core import config as C
    import osint_monitor.processors.clustering as CL
    from osint_monitor.processors import cross_language as X
    from osint_monitor.core.database import RawItem, get_session

    base_loader = C.load_event_grouping_config

    def loader(*a, **kw):
        cfg = base_loader(*a, **kw)
        for key, value in overrides.items():
            setattr(cfg.cross_language, key, value)
        return cfg
    C.load_event_grouping_config = CL.load_event_grouping_config = loader
    base_merge, state, links_out = X.merge_units, {}, []

    def recording(units, links, direct_only=False):
        out = base_merge(units, links, direct_only)
        kept = [l for l in links if l.accepted]
        if direct_only:
            kept = X.direct_links(units, kept)
        s = get_session()
        ids = [i for l in kept for i in l.a.items + l.b.items]
        ext = dict(s.query(RawItem.id, RawItem.external_id).filter(RawItem.id.in_(ids))) if ids else {}
        s.close()
        for l in kept:
            links_out.append({"window": state["w"], "a": [ext[i] for i in l.a.items], "b": [ext[i] for i in l.b.items],
                              "cosine": round(l.cosine, 3), "evidence": l.evidence})
        state["dropped_by_g3"] = state.get("dropped_by_g3", 0) + sum(1 for l in links if l.accepted) - len(kept)
        return out
    X.merge_units = recording

    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    adds = yaml.safe_load((ROOT / "gold" / "identity-gold-rev3-additions.yaml").read_text(encoding="utf-8"))
    gold2 = {k: v for k, v in yaml.safe_load((ROOT / "gold" / "identity-gold.yaml").read_text(encoding="utf-8")).items()
             if v["split"] == "development"}
    members, phase2 = {}, []
    for w in manifest["windows"]:
        if w["split"] != "development":
            continue
        state["w"] = w["id"]
        t = replay_current.replay(w)
        members[w["id"]] = {i: sorted(r["developments"]) for i, r in t["items"].items()}
        phase2.append(score(t, gold2))
        print(name, w["id"], len(t["developments"]), "Developments", flush=True)

    def together(e):
        m = members[e["window"]]
        return bool(set(m.get(e["a"], [])) & set(m.get(e["b"], [])))
    from score_identity import totals
    tot = totals(phase2)
    return {"experiment": name, "overrides": overrides,
            "rev4": {cid: {"label": e["label"], "together": together(e)} for cid, e in sorted(adds.items())},
            "phase2": {cid: {"label": e["label"], "together": together(e)} for cid, e in sorted(gold2.items())},
            "phase2_totals": {k: v for k, v in tot.items() if k != "error_classes"},
            "accepted_links": links_out, "accepted_link_count": len(links_out),
            "links_dropped_by_g3": state.get("dropped_by_g3", 0)}


def compare(exp: dict, off: dict) -> dict:
    def added(part, label):
        return sorted(c for c, r in exp[part].items()
                      if r["label"] == label and r["together"] and not off[part][c]["together"])

    def lost(part):
        return sorted(c for c, r in exp[part].items()
                      if r["label"] == "SAME_DEVELOPMENT" and not r["together"] and off[part][c]["together"])
    rows = exp["rev4"]
    tp = sum(1 for r in rows.values() if r["label"] == "SAME_DEVELOPMENT" and r["together"])
    fp = sum(1 for r in rows.values() if r["label"] == "DIFFERENT_DEVELOPMENT" and r["together"])
    fn = sum(1 for r in rows.values() if r["label"] == "SAME_DEVELOPMENT" and not r["together"])
    out = {"tp": tp, "fp": fp, "fn": fn,
           "precision": tp / (tp + fp) if tp + fp else None, "recall": tp / (tp + fn) if tp + fn else None,
           "stage_added_true": added("rev4", "SAME_DEVELOPMENT"),
           "stage_added_false": added("rev4", "DIFFERENT_DEVELOPMENT"),
           "phase2_new_false": added("phase2", "DIFFERENT_DEVELOPMENT"),
           "phase2_new_true": added("phase2", "SAME_DEVELOPMENT"),
           "lost_true": lost("phase2") + lost("rev4"),
           "regression": {c: (exp["rev4"].get(c) or exp["phase2"].get(c))["together"] for c in REGRESSION},
           "accepted_links": exp["accepted_link_count"], "links_dropped_by_g3": exp["links_dropped_by_g3"]}
    out["qualifies"] = (len(out["stage_added_false"]) <= 2 and not out["phase2_new_false"]
                        and all(out["regression"][c] for c in MANDATORY) and len(out["stage_added_true"]) >= 8)
    return out


def choose_k(results: dict) -> int:
    """Plan section 4 / amendment 2: k for E5 and E7."""
    def key(name):
        r = results[name]
        return (not r["qualifies"], len(r["stage_added_false"]) + len(r["phase2_new_false"]),
                -len(r["stage_added_true"]), 0 if name == "E2a" else 1)
    return 3 if min(("E2a", "E2b"), key=key) == "E2a" else 5


def summary() -> int:
    data = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(OUT.glob("*.json")) if p.stem != "summary"}
    off = data["OFF"]
    results = {n: compare(d, off) for n, d in data.items() if n != "OFF"}
    k = choose_k(results) if {"E2a", "E2b"} <= set(results) else None
    components = {"E0": 0, "E1": 1, "E2a": 1, "E2b": 1, "E3": 1, "E4": 1, "E5": 3, "E6": 3, "E7": 4}
    qualifying = [n for n, r in results.items() if r["qualifies"] and n != "E0"]
    winner = min(qualifying, key=lambda n: (-len(results[n]["stage_added_true"]), components[n], n)) if qualifying else None
    near = any(len(r["stage_added_false"]) < 5 and len(r["stage_added_true"]) >= 8      # plan section 6
               for n, r in results.items() if n != "E0")
    decision = ("ENABLE CROSS-LANGUAGE STAGE (for holdout evaluation): " + winner) if winner else \
        ("KEEP DISABLED" if near else "REJECT CURRENT APPROACH")
    print(f"k for E5/E7: {k}")
    print(f"{'exp':5s} {'TP/FP/FN':>10s} {'P':>5s} {'R':>5s}  added T/F  P2 newF  mand  R138  C006  links  qualifies")
    for n, r in results.items():
        reg = r["regression"]
        print(f"{n:5s} {r['tp']:>3d}/{r['fp']:>2d}/{r['fn']:>2d} {r['precision'] or 0:5.2f} {r['recall'] or 0:5.2f}  "
              f"{len(r['stage_added_true']):>4d}/{len(r['stage_added_false']):<4d} {len(r['phase2_new_false']):>6d}  "
              f"{'ok' if all(reg[c] for c in MANDATORY) else 'FAIL':>4s}  {int(reg['G02'])}{int(reg['G03'])}    "
              f"{int(reg['C006'])}   {r['accepted_links']:>5d}  {r['qualifies']}")
    print("decision:", decision)
    (OUT / "summary.json").write_text(json.dumps({"k": k, "results": results, "qualifying": qualifying,
                                                  "winner": winner, "decision": decision}, indent=1) + "\n",
                                      encoding="utf-8", newline="\n")
    return 0


def main() -> int:
    if "--summary" in sys.argv:
        return summary()
    name = sys.argv[sys.argv.index("--exp") + 1]
    k = int(sys.argv[sys.argv.index("--k") + 1]) if "--k" in sys.argv else None
    exps = experiments(k)
    if name in ("E5", "E7") and k is None:
        print("E5 and E7 need --k (chosen from E2a/E2b by the plan's rule; see --summary)")
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{name}.json"
    if out.exists():
        print(f"refusing: {out.name} exists (each experiment runs once)")
        return 1
    result = run(name, exps[name])
    out.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(name, "done:", result["accepted_link_count"], "accepted links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
