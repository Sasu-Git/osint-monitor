"""Owner review sheet for the relation gold.

    python evaluations/relations/scripts/build_review_sheet.py
      -> review/relation-review-sheet.md
      -> review/owner-verdicts.yaml (created once; existing verdicts are never overwritten)

The sheet shows each case with its evidence, the system context (system Development, production Situation) and
the blind draft label. The candidate rule that selected a case is not shown (review/candidate-rules.json).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review"
VERDICT_FIELDS = ("label", "direction", "identity_flag", "note")


def side(o, tag):
    sysdev = ", ".join(f"D{d}" for d in o["system_developments"]) or "none (not surfaced: single source)"
    rows = [f"**{tag}** `{o['id']}`",
            "",
            f"- **Members:** {len(o['members'])} item(s)",
            f"- **Sources:** {', '.join(o['sources'])}",
            f"- **Times:** {str(o['first'])[:16]} to {str(o['last'])[:16]} UTC",
            f"- **Actors:** {', '.join(o['actors'][:12]) or 'none extracted'}",
            f"- **Places:** {', '.join(o['places'][:10]) or 'none extracted'}",
            f"- **System Development:** {sysdev}",
            f"- **Situation (production, `actor_set`):** {', '.join(o['situations']) or 'none'}",
            "- **Evidence:**"]
    for e in o["evidence"]:
        rows.append(f"  - {str(e['published_at'])[:16]} [{e['source']}] **{e['title']}**")
        if e["excerpt"]:
            rows.append(f"    > {e['excerpt'][:280]}")
    return rows


def main():
    data = json.loads((REVIEW / "cases.json").read_text(encoding="utf-8"))
    drafts = json.loads((REVIEW / "draft-labels.json").read_text(encoding="utf-8"))
    cases = sorted(data["cases"], key=lambda c: c["case"])
    counts = {}
    for d in drafts.values():
        counts[d["label"]] = counts.get(d["label"], 0) + 1
    lines = [
        "# Development relation review sheet (Phase 3 gold, development split)", "",
        "One case is one pair of **distinct** Developments. Side A is the earlier Development.",
        "",
        "**Definitions.** They are in `../taxonomy.md`. Labels:",
        "",
        "- the relation types `same_calamity_lifecycle`, `same_visit_or_summit`, `same_attack_wave`,",
        "  `reaction_to`, `follow_up_to`, `caused_by` and `co_caused_with`;",
        "- `NO_RELATION`;",
        "- `AMBIGUOUS`.",
        "",
        "**Direction.** For a directed type, write it as source -> target. For example, `B->A` with",
        "`reaction_to` means B reacts to A. Use `none` for symmetric types.",
        "",
        "**How to review.** Fill in your verdict in `owner-verdicts.yaml`. You may correct the type, the",
        "direction or both. Notes are kept verbatim. Set `identity_flag: SAME_DEVELOPMENT_SUSPECTED` when the two",
        "sides look like one occurrence: that is an identity question, not a relation.",
        "",
        "**About the draft labels.** A separate annotator wrote them, seeing only the evidence text and the",
        "taxonomy. How a case was selected is deliberately not shown.",
        "",
        f"**Cases:** {len(cases)}. Draft labels: "
        + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) + ".", "",
        "| Case | A | B | Draft label | Direction | Confidence |", "|---|---|---|---|---|---|"]
    for c in cases:
        d = drafts[c["case"]]
        lines.append(f"| [{c['case']}](#{c['case'].lower()}) | {c['a']['evidence'][0]['title'][:60]} | "
                     f"{c['b']['evidence'][0]['title'][:60]} | {d['label']} | {d['direction']} | {d['confidence']} |")
    lines.append("")
    for c in cases:
        d = drafts[c["case"]]
        lines += ["---", "", f"## {c['case']}", ""]
        lines += side(c["a"], "Development A") + [""] + side(c["b"], "Development B") + [""]
        lines += [
            "| Proposed relation | Direction | Confidence | Flags |",
            "|---|---|---|---|",
            f"| `{d['label']}` | {d['direction']} | {d['confidence']} | "
            f"{', '.join(x for x in (d.get('identity_flag'), d.get('flag')) if x) or 'none'} |",
            "",
            f"**Rationale:** {d['rationale']}",
            "",
            "**Owner verdict:** ______  ·  **Direction:** ______  ·  **Note:** ______", ""]
    (REVIEW / "relation-review-sheet.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    vpath = REVIEW / "owner-verdicts.yaml"
    if not vpath.exists():
        header = ("# Owner verdicts for the relation gold, one entry per case. `label: ACCEPT` accepts the draft label\n"
                  "# and direction; otherwise write the label (and direction for directed types). Notes are kept verbatim.\n")
        body = "".join(f"{c['case']}: {{label: null, direction: null, identity_flag: null, note: null}}\n"
                       for c in cases)
        vpath.write_text(header + body, encoding="utf-8", newline="\n")
    print(len(cases), "cases -> review/relation-review-sheet.md")


if __name__ == "__main__":
    main()
