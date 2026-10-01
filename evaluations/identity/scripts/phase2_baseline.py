"""Phase 2 baseline: what the CURRENT runtime does with Development identity, scored on gold revision 2.

No runtime change. The development windows only are replayed tick by tick (``replay_current.replay``) twice, each
time in a clean temporary database; the holdout window is neither replayed nor scored.

Per pair of a gold case (AMBIGUOUS excluded): the pair is *kept together* when, after the later item's tick, both
items share a Development ID. Development IDs are never deleted, split or merged by the current code, so final
membership (with the tick each membership was added) is the full history.

Writes runs/phase2-baseline.json (metrics, ledger, findings, determinism) for phase2-baseline.md.

Usage: python evaluations/identity/scripts/phase2_baseline.py
"""
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402

import replay_current  # noqa: E402

SCORED = ("SAME_DEVELOPMENT", "DIFFERENT_DEVELOPMENT")


def comparable(trace: dict) -> dict:
    """Everything identity-relevant in a replay, without wall-clock-dependent fields."""
    return {
        "developments": {d: {k: v[k] for k in ("summary", "created_tick", "members", "principals", "sources")}
                         for d, v in trace["developments"].items()},
        "item_developments": {i: r["developments"] for i, r in trace["items"].items()},
        "ticks": [{k: t[k] for k in ("tick", "items_in", "items_stored", "clusters_before_segmentation",
                                     "segmentation_cuts")} for t in trace["ticks"]],
    }


def diff_traces(a: dict, b: dict) -> list[str]:
    out = []
    for key in ("developments", "item_developments"):
        for k in sorted(set(a[key]) | set(b[key])):
            if a[key].get(k) != b[key].get(k):
                out.append(f"{key}[{k}]: {a[key].get(k)} != {b[key].get(k)}")
    for ta, tb in zip(a["ticks"], b["ticks"]):
        for k in ta:
            if ta[k] != tb[k]:
                out.append(f"tick {ta['tick']} {k} differs")
    return out


def classify_split(t, case, devs_shared, a, b):
    ia, ib = t["items"][a], t["items"][b]
    dev = t["developments"][str(devs_shared[0])]
    ta, tb = dev["members"].get(a), dev["members"].get(b)
    if ia["roundup"] or ib["roundup"]:
        return "roundup contamination", "a roundup item shares the Development, so its mixed headline links distinct occurrences"
    if len(dev["sources"]) == 1:
        return "single-source promotion", "one outlet's near-identical headlines form the Development on their own"
    if len(ia["developments"]) > 1 or len(ib["developments"]) > 1:
        return "duplicate membership", "an item belongs to two Developments, so a cluster spanning both joins the first by unordered overlap"
    if ta != tb:
        return "late attachment", "a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge)"
    return ("whole-storyline overmerge", "distinct occurrences of one storyline linked above the similarity threshold "
            f"in one cluster ({len(dev['members'])}-item Development); segmentation did not cut them")


def classify_merge(t, case, a, b, cuts):
    ia, ib = t["items"][a], t["items"][b]
    multilingual = ia["lang"] != ib["lang"]
    lang_note = " (cross-language: the embedding model is English-only)" if multilingual else ""
    if frozenset((a, b)) in cuts:
        return "segmentation interaction", "segmentation cut the link between them (guard: " + cuts[frozenset((a, b))] + ")" + lang_note
    if ia["developments"] and ib["developments"]:
        return "missed continuation", "both are in Developments, but different ones: the same occurrence exists twice" + lang_note
    if ia["tick"] != ib["tick"]:
        return "missed continuation", "the later item did not join the earlier item's Development (or neither was clustered)" + lang_note
    if ia["developments"] or ib["developments"]:
        return "missed continuation", "one item is in a Development, the other was left out of it" + lang_note
    return "other", "same-tick items of one occurrence not grouped (below the link threshold or left as noise)" + lang_note


def score(trace: dict, gold: dict) -> dict:
    t = trace
    cases = {k: v for k, v in gold.items() if v["window"] == t["window"]}
    cuts = {}
    for tk in t["ticks"]:
        for x, y, guard in tk["segmentation_cuts"]:
            if x and y:
                cuts[frozenset((x, y))] = guard
    tally = Counter()
    ledger = []
    for cid, g in sorted(cases.items()):
        a, b = g["a"], g["b"]
        ia, ib = t["items"][a], t["items"][b]
        shared = sorted(set(ia["developments"]) & set(ib["developments"]))
        together = bool(shared)
        label = g["label"]
        if label not in SCORED:
            tally["ambiguous"] += 1
            continue
        same = label == "SAME_DEVELOPMENT"
        tally["pairs"] += 1
        tally["together"] += together
        tally["gold_same"] += same
        tally["together_and_same"] += together and same
        if same and ia["tick"] != ib["tick"]:
            tally["cross_tick_same"] += 1
            tally["cross_tick_same_retained"] += together
        if together and not same:
            cls, why = classify_split(t, cid, shared, a, b)
        elif same and not together:
            cls, why = classify_merge(t, cid, a, b, cuts)
        else:
            continue
        ledger.append({
            "case": cid, "gold": label,
            "current": "kept together" if together else ("different Developments" if ia["developments"] and ib["developments"]
                                                         else "not grouped"),
            "developments": [ia["developments"], ib["developments"]], "ticks": [ia["tick"], ib["tick"]],
            "items": [{"id": i["id"], "source": i["source"], "lang": i["lang"], "title": i["title"]} for i in (ia, ib)],
            "error_class": cls, "root_cause": why,
            "failure": "split failure (DIFFERENT kept together)" if together else "merge failure (SAME kept apart)",
        })

    # Developments: mixed, duplicates, single-source, roundups
    member_items = defaultdict(list)
    for d, dv in t["developments"].items():
        for m in dv["members"]:
            member_items[m].append(d)
    gold_pairs = [(g["a"], g["b"], g["label"]) for g in cases.values()]
    mixed, labelled = [], []
    for d, dv in t["developments"].items():
        mem = set(dv["members"])
        inside = [lab for a, b, lab in gold_pairs if a in mem and b in mem]
        if inside:
            labelled.append(d)
        if "DIFFERENT_DEVELOPMENT" in inside:
            mixed.append(d)
    multi = [d for d, dv in t["developments"].items() if len(dv["members"]) >= 2]
    dup = {i: ds for i, ds in member_items.items() if len(ds) > 1}
    single = [{"development": d, "source": dv["sources"][0], "items": len(dv["members"]), "summary": dv["summary"]}
              for d, dv in t["developments"].items() if len(dv["sources"]) == 1]
    roundup = []
    for d, dv in t["developments"].items():
        r = [m for m in dv["members"] if t["items"][m]["roundup"]]
        if not r:
            continue
        others = [m for m in dv["members"] if m not in r]
        src_all = {t["items"][m]["source"] for m in dv["members"]}
        src_wo = {t["items"][m]["source"] for m in others}
        summary_is_roundup = any(t["items"][m]["title"] == dv["summary"] for m in r) and bool(others)
        mem = set(others)
        diff_among_others = [c for c, g in cases.items() if g["label"] == "DIFFERENT_DEVELOPMENT"
                             and g["a"] in mem and g["b"] in mem]
        roundup.append({"development": d, "summary": dv["summary"], "roundup_items": r, "members": len(dv["members"]),
                        "sources_with": len(src_all), "sources_without": len(src_wo),
                        "source_count_inflated": len(src_all) > len(src_wo), "corroboration": dv.get("corroboration"),
                        "summary_is_roundup_with_reports_present": summary_is_roundup,
                        "gold_different_pairs_among_non_roundup_members": diff_among_others})
    late = sum(1 for dv in t["developments"].values() for m, tk in dv["members"].items()
               if tk and dv["created_tick"] and tk > dv["created_tick"])
    return {"window": t["window"], "tally": dict(tally), "ledger": ledger,
            "developments": len(t["developments"]), "multi_item": len(multi),
            "mixed": mixed, "labelled_developments": labelled,
            "duplicate_memberships": dup, "items_in_developments": len(member_items),
            "single_source": single, "roundups": roundup, "late_memberships": late,
            "overlap_extensions": sum(1 for dv in t["developments"].values()
                                      if len({tk for tk in dv["members"].values()}) > 1)}


def main() -> int:
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    gold = yaml.safe_load((ROOT / "gold" / "identity-gold.yaml").read_text(encoding="utf-8"))
    gm = yaml.safe_load((ROOT / "gold" / "manifest.yaml").read_text(encoding="utf-8"))
    assert gm["revision"] == 2, "baseline is defined on gold revision 2"
    gold = {k: v for k, v in gold.items() if v["split"] == "development"}      # the holdout stays sealed
    results, determinism = [], []
    for w in manifest["windows"]:
        if w["split"] != "development":
            continue
        runs = [replay_current.replay(w) for _ in range(2)]
        diffs = diff_traces(comparable(runs[0]), comparable(runs[1]))
        committed = ROOT / "review" / "system-trace" / f"{w['id']}.json"
        diffs_committed = diff_traces(comparable(runs[0]), comparable(json.loads(committed.read_text(encoding="utf-8"))))
        determinism.append({"window": w["id"], "run1_vs_run2": diffs[:20], "run1_vs_review_trace": diffs_committed[:20],
                            "identical": not diffs, "identical_to_review_trace": not diffs_committed})
        results.append(score(runs[0], gold))
        traces = ROOT / "runs" / "phase2-baseline-traces"
        traces.mkdir(parents=True, exist_ok=True)
        (traces / f"{w['id']}.json").write_text(json.dumps(comparable(runs[0]), indent=1, ensure_ascii=False) + "\n",
                                                encoding="utf-8", newline="\n")
        print(w["id"], "replayed twice; identical:", not diffs, "| vs review trace:", not diffs_committed, flush=True)
    out = ROOT / "runs" / "phase2-baseline.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"gold_revision": gm["revision"], "gold_sha256": gm["sha256"]["gold/identity-gold.yaml"],
                               "windows": results, "determinism": determinism}, indent=1, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")
    print("written", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
