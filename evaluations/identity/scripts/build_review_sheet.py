"""Build the owner review sheet from the blind draft labels and the current-system trace.

Inputs: review/cases.json (case -> item pair), review/draft-labels.json (blind labeller output:
case -> label, note, confidence, rationale), review/system-trace/*.json (current main replay).
Outputs: review/identity-review-sheet.md and review/owner-verdicts.yaml (blank verdicts to fill in).

Structural flags are computed from the DRAFT label against the current grouping, so they change if the owner
corrects a label; they describe cases, not any future algorithm.
"""
import json
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review"
FLAGS = {
    "grows_same_id": "cluster grows over time and should keep the same ID",
    "should_split": "one Development should split into two",
    "should_merge": "two candidate Developments (or an unattached item) should merge",
    "same_story_new_action": "same story, materially new action",
    "roundup_contamination": "roundup contaminating identity",
    "single_source_below_development": "single-source evidence that must stay below the Development layer",
    "late_attach": "item attached late to an existing Development",
}


def main() -> int:
    cases = json.loads((REVIEW / "cases.json").read_text(encoding="utf-8"))
    labels = json.loads((REVIEW / "draft-labels.json").read_text(encoding="utf-8"))
    traces = {json.loads(p.read_text(encoding="utf-8"))["window"]: json.loads(p.read_text(encoding="utf-8"))
              for p in (REVIEW / "system-trace").glob("*.json")}
    cand = {w: {(c["a"], c["b"]): c for c in t["candidates"]} for w, t in traces.items()}

    rows, flagged = [], defaultdict(list)
    for case in cases:
        t = traces[case["window"]]
        a, b = t["items"][case["a"]], t["items"][case["b"]]
        c = cand[case["window"]].get(tuple(sorted((a["id"], b["id"]))), {"rules": [], "why": [], "cosine": None})
        lab = labels.get(case["case"], {})
        label, note = lab.get("label", "MISSING"), (lab.get("note") or "")
        same_dev = sorted(set(a["developments"]) & set(b["developments"]))
        devs = {d: t["developments"][str(d)] for d in set(a["developments"]) | set(b["developments"])}
        flags = []
        if same_dev and label == "DIFFERENT_DEVELOPMENT":
            flags.append("should_split")
            if note in ("reaction", "follow-up", "repeat", "preview"):
                flags.append("same_story_new_action")
        if not same_dev and label == "SAME_DEVELOPMENT":
            flags.append("should_merge")
        if same_dev and label == "SAME_DEVELOPMENT" and a["tick"] != b["tick"]:
            flags.append("grows_same_id")
        if label == "SAME_DEVELOPMENT" and ("late_attach" in c["rules"] or "near_miss" in c["rules"]):
            flags.append("late_attach")
        if same_dev and (a["roundup"] or b["roundup"]) and label != "SAME_DEVELOPMENT":
            flags.append("roundup_contamination")
        if same_dev and any(len(devs[d]["sources"]) == 1 for d in same_dev):
            flags.append("single_source_below_development")
        for f in flags:
            flagged[f].append(case["case"])
        rows.append((case, a, b, c, lab, same_dev, devs, flags))

    out = ["# Development identity: owner review sheet", "",
           "Draft labels were written blind: the labeller saw only the item text, outlet, publication time, "
           "language and the Development definition. It did not see the current grouping, similarity scores or "
           "the rule that proposed a case. The current-system columns are here for your review only.", "",
           "Fill in `owner-verdicts.yaml` (or the verdict line under each case): `ACCEPT`, or the corrected "
           "label `SAME_DEVELOPMENT` / `DIFFERENT_DEVELOPMENT` / `AMBIGUOUS`, with an optional note. Nothing is "
           "frozen or hashed until your verdicts are applied.", "",
           "## Structural cases (computed from the draft label)", "",
           "| Flag | Meaning | Cases |", "|---|---|---|"]
    for key, meaning in FLAGS.items():
        ids = flagged.get(key, [])
        out.append(f"| `{key}` | {meaning} | {len(ids)}: {', '.join(ids) if ids else '-'} |")
    out += ["", "## Totals", ""]
    counts = defaultdict(lambda: defaultdict(int))
    for row in rows:
        case, lab = row[0], row[4]
        counts[case["window"]][lab.get("label", "MISSING")] += 1
    out += ["| Window | Split | Cases | SAME | DIFFERENT | AMBIGUOUS |", "|---|---|---:|---:|---:|---:|"]
    for w, cnt in counts.items():
        out.append(f"| {w} | {traces[w]['split']} | {sum(cnt.values())} | {cnt['SAME_DEVELOPMENT']} | "
                   f"{cnt['DIFFERENT_DEVELOPMENT']} | {cnt['AMBIGUOUS']} |")
    current_window = None
    for case, a, b, c, lab, same_dev, devs, flags in rows:
        if case["window"] != current_window:
            current_window = case["window"]
            out += ["", f"## Window {current_window} ({case['split']})", ""]
        cos = f"{c['cosine']:.2f}" if c.get("cosine") is not None else "n/a"
        rel = (f"same Development D{', D'.join(map(str, same_dev))}" if same_dev else
               "different Developments" if a["developments"] and b["developments"] else
               "one item not in any Development" if a["developments"] or b["developments"] else
               "neither in a Development")
        out += [f"### {case['case']}" + (f"  · flags: {', '.join(flags)}" if flags else ""), "",
                "| | Item 1 | Item 2 |", "|---|---|---|",
                f"| id · tick | `{a['id']}` · t{a['tick']} | `{b['id']}` · t{b['tick']} |",
                f"| published | {a['published_at'] or 'unknown'} | {b['published_at'] or 'unknown'} |",
                f"| source · lang | {a['source']} · {a['lang']}{' · ROUNDUP' if a['roundup'] else ''} | "
                f"{b['source']} · {b['lang']}{' · ROUNDUP' if b['roundup'] else ''} |",
                f"| headline | {a['title']} | {b['title']} |",
                f"| current Development | {', '.join('D' + str(d) for d in a['developments']) or '-'} | "
                f"{', '.join('D' + str(d) for d in b['developments']) or '-'} |",
                f"| places | {', '.join(a['places'][:5]) or '-'} | {', '.join(b['places'][:5]) or '-'} |", ""]
        for d, dv in sorted(devs.items()):
            out.append(f"- D{d}: \"{dv['summary'][:90]}\" · {len(dv['members'])} items · sources "
                       f"{', '.join(dv['sources'])} · principals {', '.join(dv['principals'][:5]) or '-'}")
        out += [f"- current system: {rel}; cosine {cos}; " + "; ".join(c.get("why") or []),
                f"- **proposed:** `{lab.get('label', 'MISSING')}`" + (f" ({lab['note']})" if lab.get("note") else "")
                + f" · confidence {lab.get('confidence', '-')} · {lab.get('rationale', '')}",
                "- **owner verdict:** ____", ""]
    (REVIEW / "identity-review-sheet.md").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    verdicts = {case["case"]: {"proposed": lab.get("label"), "verdict": None, "note": None}
                for case, a, b, c, lab, *_ in rows}
    (REVIEW / "owner-verdicts.yaml").write_text(
        "# Owner verdicts: set verdict to ACCEPT or to SAME_DEVELOPMENT / DIFFERENT_DEVELOPMENT / AMBIGUOUS.\n"
        + yaml.safe_dump(verdicts, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")
    print(len(rows), "cases;", {k: len(v) for k, v in flagged.items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
