"""Blind input for the identity labeller: candidate pairs with item text only.

Each case shows, for both items: headline, excerpt, outlet, original publication time and language. It does NOT
show which rule proposed the pair, the similarity score, the tick, or how the current system grouped the items.
Cases are shuffled (seeded) and numbered per window; the case -> candidate mapping stays in cases.json.

Usage: python evaluations/identity/scripts/make_labeller_input.py
Writes review/labeller-input.md (for the labeller) and review/cases.json (mapping, not given to the labeller).
"""
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "review" / "system-trace"
SEED = 20261001
SHORT = {"2026-08-21": "A", "2026-09-25": "B", "2026-09-30-multilingual": "C", "2026-08-31": "H"}

DEFINITION = """Two source items describe the same Development when they report the same concrete occurrence (an
action, interaction, decision, statement or incident), with compatible actors, place and time, such that one
could be a rewrite or an update of the other. Updates to the same occurrence (rising death toll, later details)
stay in it. A reaction to it, a response or policy decision following it, a repeated occurrence of the same kind
on another day, a preview before it, and analysis or explainers about it are different Developments, or
commentary, in the same storyline or Situation, however similar the language or the actors.

Analysis, explainers, opinion and live blogs / daily roundups are not evidence of a Development: an analysis
piece and a report are never the same Development (label DIFFERENT_DEVELOPMENT, note "commentary"). A roundup
is the same Development as a report only if its headline is that single concrete occurrence."""


def main() -> int:
    rng = random.Random(SEED)
    cases, lines = [], ["# Development identity: blind labelling input", "",
                        "## Definition (label only from this and the item text)", "", DEFINITION, "",
                        "## Labels", "",
                        "- `SAME_DEVELOPMENT`, `DIFFERENT_DEVELOPMENT` or `AMBIGUOUS`",
                        "- optional relation note: update | rewrite | reaction | follow-up | repeat | commentary | "
                        "preview | unrelated",
                        "- confidence: high | medium | low; rationale: one sentence", ""]
    for trace_file in sorted(TRACE.glob("*.json")):
        t = json.loads(trace_file.read_text(encoding="utf-8"))
        pairs = list(t["candidates"])
        rng.shuffle(pairs)
        prefix = SHORT[t["window"]]
        lines += [f"## Window {prefix}", ""]
        for n, c in enumerate(pairs, 1):
            cid = f"{prefix}{n:03d}"
            a, b = t["items"][c["a"]], t["items"][c["b"]]
            if rng.random() < 0.5:                      # no positional hint
                a, b = b, a
            cases.append({"case": cid, "window": t["window"], "split": t["split"], "a": a["id"], "b": b["id"]})
            lines.append(f"### {cid}")
            for tag, it in (("1", a), ("2", b)):
                lines.append(f"- **{tag}** [{it['source']}, {it['lang']}, published {it['published_at'] or 'unknown'}] "
                             f"{it['title']}")
                if it["excerpt"]:
                    lines.append(f"  - {it['excerpt'][:300].strip()}")
            lines.append("")
    (ROOT / "review" / "labeller-input.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    (ROOT / "review" / "cases.json").write_text(json.dumps(cases, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(len(cases), "cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
