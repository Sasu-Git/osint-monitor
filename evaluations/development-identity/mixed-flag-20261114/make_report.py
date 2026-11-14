import json
d = json.load(open("results.json", encoding="utf-8"))
s = d["summary"]
L = ["# Mixed-flag diagnostic (read-only, numbers only, no verdicts)", "",
     f"Input: `{d['input']}`  sha256 `{d['sha256']}` (verified before use). Seed for samples: {d['seed']}.",
     "Code: `compatible_link` / `segment_items` from osint_monitor/processors/development_segmentation.py at origin/main b92acc6, "
     "config = load_event_grouping_config().development_segmentation. Components = connected components over pairs where compatible_link is true.",
     f"Developments with >=1 item: {d['developments_total']}; with >=2 items: {d['developments_ge2']}; scored (>=2 members with embeddings): {d['scored']}; skipped: {d['skipped_lt2_embedded']}.",
     "", "Definitions: V1 >=2 components; V2 >=2 components each >=2 items; V3 = V1 on report-headline items only; V4 = V2 on report-headline items only.",
     "Dominant language = most common `item_language(source, title+lead)` among members. Size band uses stored member count.", "",
     "## Counts (flagged / n, share)", "", "| group | n | V1 | V2 | V3 | V4 |", "|---|---|---|---|---|---|"]
def row(name, t):
    c = [f"{t[v]} ({100*t[v]/t['n']:.1f}%)" if t["n"] else "-" for v in ("V1", "V2", "V3", "V4")]
    return f"| {name} | {t['n']} | " + " | ".join(c) + " |"
L.append(row("all", s["overall"]))
for k, t in s["by_size"].items(): L.append(row(f"size {k}", t))
for k, t in s["by_language"].items(): L.append(row(f"lang {k}", t))
L += ["", "## Known merged Developments (check only, not used to tune)", "",
      "| Development | size | components (all) | components (report only) | V1 | V2 | V3 | V4 |", "|---|---|---|---|---|---|---|---|"]
for k, r in d["known"].items():
    L.append(f"| {k} | {r['size']} | {r['components']} | {r['report_components']} | " + " | ".join(str(r[v]) for v in ("V1","V2","V3","V4")) + " |")
L += ["", "Note: V3/V4 drop analysis/rolling items, which can act as bridges in the all-items graph, so V3 can flag a Development V1 does not (e.g. D439).",
      "", "## Read-only confirmation", "",
      "The snapshot was opened `mode=ro`, copied with the sqlite backup API to a temp dir, and the copy was opened with `PRAGMA query_only=ON` (SQLAlchemy engine, no commit). "
      f"A sha256 over events(id, summary, situation_id) and event_items(event_id, item_id) was identical before and after: {d['read_only']['unchanged']} (`{d['read_only']['membership_fingerprint_before']}`). No Development membership or identity was written.", ""]
def sample(title, key, pool):
    L.extend([f"## {title}", "", f"Pool size {pool}; 15 drawn with random.Random({d['seed']}) from the sorted id list. Items grouped by component (`c<k>`); kind = headline_kind.", ""])
    for dev in d[key]:
        L.append(f"### D{dev['id']} (size {dev['size']}; components {dev['components']}; report-only {dev['report_components']})")
        for it in sorted(dev["items"], key=lambda x: x["comp"]):
            L.append(f"- c{it['comp']} [{it['kind']}] {it['title']} ({it['source']})")
        L.append("")
sample("Sample: flagged by V1 but not V2", "sample_V1_not_V2", d["pool_sizes"]["V1_not_V2"])
sample("Sample: flagged by V4", "sample_V4", d["pool_sizes"]["V4"])
open("REPORT.md", "w", encoding="utf-8").write("\n".join(L))
