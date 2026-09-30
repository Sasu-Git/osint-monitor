"""Stage-by-stage tables for evaluations/entities/entity-resolution.md from the saved benchmark runs."""
import json
import sys
from pathlib import Path

from osint_monitor.benchmark import entities as eb

RUNS = Path("evaluations/entities/runs")
STAGES = [("00-baseline", "baseline (main)"), ("01-fuzzy-safety", "1 fuzzy-alias safety"),
          ("02-normalisation", "2 text/name normalisation"), ("03-multilingual", "3 multilingual NER"),
          ("04-institutions", "4 institutional hierarchy"), ("05-roles", "5 actor roles"),
          ("06-principals-from-roles", "6 principals from roles"), ("07-roundups", "7 round-up safeguards")]
LANGS = ["all", "en", "it", "es", "es+it"]
out = []
runs = {k: json.loads((RUNS / f"{k}.json").read_text(encoding="utf-8")) for k, _ in STAGES}


def cell(t):
    return f"{t['hit'] / t['total']:.0%} ({t['hit']}/{t['total']})" if t and t["total"] else "-"


for metric, label in eb.METRICS:
    out += [f"### {label}", "", "| Stage | " + " | ".join(LANGS) + " |", "|---|" + "---:|" * len(LANGS)]
    for k, name in STAGES:
        s = runs[k]["summary"].get(metric, {})
        out.append(f"| {name} | " + " | ".join(cell(s.get(l)) for l in LANGS) + " |")
    out.append("")

out += ["## Errors fixed and introduced per stage", ""]
for (prev, _), (cur, name) in zip(STAGES, STAGES[1:]):
    d = eb.diff(runs[prev], runs[cur])
    out += [f"### {name}", ""]
    rows = []
    for metric, label in eb.METRICS:
        f, i = d[metric]["fixed"], d[metric]["introduced"]
        if f or i:
            devs = sorted({x.split()[0] for x in f + i})
            rows.append(f"| {label} | {len(f)} | {len(i)} | {', '.join(devs)} |")
    if rows:
        out += ["| Metric | fixed | introduced | Developments |", "|---|---:|---:|---|"] + rows
        intro = [(label, x) for metric, label in eb.METRICS for x in d[metric]["introduced"]]
        if intro:
            out += ["", "Introduced:"] + [f"- {label}: {x}" for label, x in intro]
    else:
        out.append("No unit changed.")
    out.append("")
Path(sys.argv[1]).write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"wrote {sys.argv[1]}")
