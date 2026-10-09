"""Score the identity follow-up on the frozen defect set and the identity gold, against the baseline replays.

    python evaluations/identity/defects/score_followup.py --label NAME   # -> runs-NAME/, score-NAME.json

Replays every window the defect set uses with the current code (fixed replay clock) into runs-NAME/, then compares,
case by case, the baseline (the frozen defect set's replays) with the new replays:
- defect set: correct / wrong per case, before and after, with every transition listed;
- identity gold (revision 2 development cases and revision 4 additions): every case whose outcome changed.
The sealed holdouts are never read.
"""
import json
import os
import sys
from collections import Counter
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
HERE = Path(__file__).resolve().parent
EVAL = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(EVAL / "identity" / "scripts"))
sys.path.insert(0, str(EVAL / "relations" / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

import yaml  # noqa: E402


def specs():
    from replay_windows import windows as relation_windows
    import build_runtime_cases
    out = {}
    for w in yaml.safe_load((EVAL / "identity" / "manifest.yaml").read_text(encoding="utf-8"))["windows"]:
        if w["split"] == "development":
            out[w["id"]] = {**w, "items_file": str((EVAL / "identity" / w["items_file"]).resolve())}
    for w in relation_windows("development"):
        out.setdefault(w["id"], w)
    rt = yaml.safe_load((EVAL / "relations" / "runtime" / "manifest.yaml").read_text(encoding="utf-8"))
    for w in build_runtime_cases.windows(rt):
        out.setdefault(w["id"], w)
    return out


def replay_all(label):
    import replay_current
    d = HERE / f"runs-{label}"
    d.mkdir(exist_ok=True)
    out = {}
    for wid, w in sorted(specs().items()):
        p = d / f"{wid}.json"
        if not p.exists():
            t = replay_current.replay(w)
            keep = {"window": wid,
                    "developments": {k: {"members": sorted(v["members"]), "principals": v["principals"],
                                         "summary": v["summary"]} for k, v in t["developments"].items()},
                    "items": {i: {"developments": r["developments"], "lang": r["lang"], "places": r["places"]}
                              for i, r in t["items"].items()}}
            p.write_text(json.dumps(keep, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8",
                         newline="\n")
            print(wid, len(keep["developments"]), "Developments", flush=True)
        out[wid] = json.loads(p.read_text(encoding="utf-8"))
    return out


def together(trace, a_members, b_members):
    devs = lambda ms: {d for m in ms for d in (trace["items"].get(m, {}).get("developments") or [])}  # noqa: E731
    return bool(devs(a_members) & devs(b_members))


def correct(expected, tog):
    return {"SAME_DEVELOPMENT": tog, "DIFFERENT_DEVELOPMENT": not tog}.get(expected)


def main() -> int:
    from build_defect_set import load_windows
    label = sys.argv[sys.argv.index("--label") + 1]
    base = {wid: w["trace"] for wid, w in load_windows().items()}
    new = replay_all(label)
    cases = json.loads((HERE / "defect-cases.json").read_text(encoding="utf-8"))["cases"]
    rows, trans = [], Counter()
    for c in cases:
        a = [r["item"] for r in c["a"]["items"]]
        b = [r["item"] for r in c["b"]["items"]]
        before, after = correct(c["expected"], together(base[c["window"]], a, b)), \
            correct(c["expected"], together(new[c["window"]], a, b))
        rows.append({"case": c["case"], "class": c["class"], "refs": c["refs"], "before": before, "after": after})
        trans[(c["class"], before, after)] += 1
    gold = {k: v for k, v in yaml.safe_load((EVAL / "identity" / "gold" / "identity-gold.yaml").read_text(
        encoding="utf-8")).items() if v["split"] == "development"}
    gold.update(yaml.safe_load((EVAL / "identity" / "gold" / "identity-gold-rev3-additions.yaml").read_text(
        encoding="utf-8")))
    gold_changed, gold_tally = [], Counter()
    for cid, e in sorted(gold.items()):
        if e["label"] == "AMBIGUOUS":
            continue
        bf = correct(e["label"], together(base[e["window"]], [e["a"]], [e["b"]]))
        af = correct(e["label"], together(new[e["window"]], [e["a"]], [e["b"]]))
        gold_tally[("before", bf)] += 1
        gold_tally[("after", af)] += 1
        if bf != af:
            gold_changed.append({"case": cid, "label": e["label"], "window": e["window"], "before": bf, "after": af})
    out = {"label": label, "defect_transitions": {f"{k[0]} {k[1]}->{k[2]}": v for k, v in sorted(trans.items())},
           "defect_rows": rows, "gold_correct": {"before": gold_tally[("before", True)],
                                                 "after": gold_tally[("after", True)],
                                                 "scored": gold_tally[("before", True)] + gold_tally[("before", False)]},
           "gold_changed": gold_changed}
    (HERE / f"score-{label}.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
                                              newline="\n")
    by = Counter()
    for r in rows:
        by[(r["class"], "fixed" if (not r["before"] and r["after"]) else "broken" if (r["before"] and not r["after"])
            else "same")] += 1
    print("defect set:", dict(sorted(by.items())))
    print("defect correct before", sum(1 for r in rows if r["before"]), "after", sum(1 for r in rows if r["after"]),
          "of", len(rows))
    print("gold correct:", out["gold_correct"])
    for g in gold_changed:
        print("  gold changed:", g)
    for r in rows:
        if r["before"] != r["after"]:
            print("  defect changed:", r["case"], r["class"], r["refs"][0], r["before"], "->", r["after"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
