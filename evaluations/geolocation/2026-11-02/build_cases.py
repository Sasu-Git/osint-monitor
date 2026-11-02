"""Join audit-all.json (audit.py) with the hand labels (labels.py) into the frozen case set and summary stats.

    python build_cases.py <audit-all.json>   -> cases.json, stats.json (this folder)
"""
import json, random, sys
from collections import Counter

from labels import SHOWN_SAMPLE_DEFECTS, SHOWN_SAMPLE_IDS, SUPPRESSED

rows = {r["development_id"]: r for r in json.load(open(sys.argv[1], encoding="utf-8"))}
cases = []
for eid, (cause, verdict, note) in sorted(SUPPRESSED.items()):
    cases.append({**rows[eid], "set": "suppressed", "root_cause": cause, "stored_verdict": verdict,
                  "defect_side": "frontend" if verdict == "C" else "stored", "expected_interpretation": note})
for eid in SHOWN_SAMPLE_IDS:
    cause, verdict, note = SHOWN_SAMPLE_DEFECTS.get(eid, ("CORRECT_LOCATION", "C", "right country"))
    cases.append({**rows[eid], "set": "shown_sample", "root_cause": cause, "stored_verdict": verdict,
                  "defect_side": "none" if verdict == "C" else "stored (shown anyway)", "expected_interpretation": note})
for c in cases:
    c.pop("summary_full", None)
json.dump(cases, open("cases.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

allr = list(rows.values())
located = [r for r in allr if r["valid_point"] or r["stored_place"]]
shown = [r for r in allr if r["shown"]]
supp = [c for c in cases if c["set"] == "suppressed"]
sample = [c for c in cases if c["set"] == "shown_sample"]
unlabelled = [r["development_id"] for r in located if not r["shown"] and r["development_id"] not in SUPPRESSED]
country_level = sum(1 for r in shown if r["stored_place"] and "," not in r["stored_place"])
stats = {
    "developments": len(allr), "with_stored_location": len(located), "no_stored_location": len(allr) - len(located),
    "shown": len(shown), "shown_country_level_point": country_level, "suppressed": len(located) - len(shown),
    "suppressed_unlabelled": unlabelled,
    "suppressed_stored_verdict": dict(Counter(c["stored_verdict"] for c in supp)),
    "suppressed_root_cause": dict(Counter(c["root_cause"] for c in supp).most_common()),
    "suppressed_wrong_root_cause": dict(Counter(c["root_cause"] for c in supp if c["stored_verdict"] == "W").most_common()),
    "suppressed_correct_root_cause": dict(Counter(c["root_cause"] for c in supp if c["stored_verdict"] == "C").most_common()),
    "shown_sample_verdict": dict(Counter(c["stored_verdict"] for c in sample)),
    "gaza_mozambique": sum(1 for r in allr if (r["stored_place"] or "").startswith("Gaza, Zona Sul")),
    "west_bank_minneapolis": sum(1 for r in allr if (r["stored_place"] or "").startswith("West Bank, Washington Avenue")),
}
lang = Counter(); lang_bad = Counter()
for c in supp:
    main = max(c["languages"], key=c["languages"].get) if c["languages"] else "?"
    lang[main] += 1
    if c["stored_verdict"] == "W":
        lang_bad[main] += 1
lang_all = Counter(max(r["languages"], key=r["languages"].get) if r["languages"] else "?" for r in located)
stats["dominant_language_located"] = dict(lang_all.most_common())
stats["dominant_language_suppressed"] = dict(lang.most_common())
stats["dominant_language_suppressed_wrong"] = dict(lang_bad.most_common())
json.dump(stats, open("stats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(stats, ensure_ascii=False, indent=1))
