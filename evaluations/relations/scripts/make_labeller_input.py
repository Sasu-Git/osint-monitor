"""Blind labeller input: per case only the item text, outlet, publication time and language of each side, plus the
taxonomy. No candidate rule, similarity, actors, places, Situation, system Development or owner note.

    python evaluations/relations/scripts/make_labeller_input.py   # -> review/labeller-input.md
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    import sys
    review = ROOT / (sys.argv[sys.argv.index("--dir") + 1] if "--dir" in sys.argv else "review")
    cases = json.loads((review / "cases.json").read_text(encoding="utf-8"))["cases"]
    out = ["# Relation labelling input (blind)", "",
           "Label every case using the definitions in `taxonomy.md` (included below).",
           "",
           "- Side A is the earlier Development, side B the later one.",
           "- Each side is one Development: one occurrence, possibly reported by several outlets.",
           "",
           "Return, per case:",
           "",
           "- `label`: one relation type, `NO_RELATION` or `AMBIGUOUS`;",
           "- `direction`: for a directed type, which side holds the first role: `A->B` means A is the reaction /",
           "  follow-up / effect / commentary and B the trigger / original / cause / subject; `B->A` the reverse; else",
           "  `none`;",
           "- `identity_flag`: `SAME_DEVELOPMENT_SUSPECTED` or null;",
           "- `flag`: for example `commentary`, or null;",
           "- `rationale`: one sentence that cites the evidence;",
           "- `confidence`: high, medium or low.",
           "", "---", "", (ROOT / "taxonomy.md").read_text(encoding="utf-8"), "", "---", ""]
    for c in cases:
        out.append(f"## {c['case']}")
        for side in ("a", "b"):
            o = c[side]
            out.append(f"**{side.upper()}** ({len(o['members'])} item(s))")
            for e in o["evidence"]:
                out.append(f"- {str(e['published_at'])[:16]} [{e['source']}] {e['title']}")
                if e["excerpt"]:
                    out.append(f"  > {e['excerpt'][:300]}")
        out.append("")
    (review / "labeller-input.md").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print(len(cases), "cases -> review/labeller-input.md")


if __name__ == "__main__":
    main()
