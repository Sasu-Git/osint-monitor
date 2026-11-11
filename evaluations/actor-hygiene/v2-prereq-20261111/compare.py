"""Gates G1, G5, G6 of DEFECTS.md: diff two replay_actors.py outputs (baseline, candidate).

    python compare.py BASE.json CAND.json OUT.json
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

A_NAMES = r"milei|musk|pike|machado|bukele|macron|vance|donald j\.? trump"
B_NAMES = r"emmanuel macron|nayib bukele|j\.?d\.? vance|donald j\.? trump"
C_NAMES = r"^(democrats?|democratic|republicans?|democratici|english|chinas long march|china's long march|long march|rachel|simon|sim[oó]n)$"
EXPECTED_SITUATIONS = {
    "javier-milei-milei": ["javier milei"], "elon-musk-musk": ["elon musk"], "christa-pike-pike": ["christa pike"],
    "machado-maria-corina-machado": ["maria corina machado"], "bukele-el-salvador-nayib-bukele": ["el salvador"],
    "emmanuel-macron-france-macron": ["france"], "donald-j-trump-united-states": ["united states"],
    "democrat-united-states": ["united states"], "china-chinas-long-march": ["china"], "rachel-simon": [],
}


def carries(names, pattern) -> bool:
    return any(re.search(pattern, n.lower()) for n in names)


def main(base_p, cand_p, out_p) -> int:
    base, cand = (json.loads(Path(p).read_text(encoding="utf-8")) for p in (base_p, cand_p))
    out = {}

    # G1: defect expectations
    sit = {v["slug"]: v for v in cand["situations"].values()}
    g1_sit = {slug: {"expected": exp, "got": sit[slug]["situation_keys"] if slug in sit else None,
                     "ok": slug in sit and sit[slug]["situation_keys"] == exp}
              for slug, exp in EXPECTED_SITUATIONS.items()}
    d402 = cand["developments"].get("402", {})
    probes = cand["probe_sets"]
    guards_ok = (probes["guard-bolsonaro"]["situation_keys"] == ["flávio bolsonaro", "jair bolsonaro"]
                 and probes["guard-lone-surname"]["situation_keys"] == ["germany", "musk"])
    other_sit_changed = {v["slug"]: {"base": base["situations"][k]["situation_keys"], "cand": v["situation_keys"]}
                         for k, v in cand["situations"].items()
                         if v["slug"] not in EXPECTED_SITUATIONS and v["situation_keys"] != base["situations"][k]["situation_keys"]}
    out["G1"] = {"situations": g1_sit, "D402_principals": d402.get("principals"), "guards_ok": guards_ok,
                 "other_situations_changed": other_sit_changed,
                 "pass": all(x["ok"] for x in g1_sit.values()) and not d402.get("principals") and guards_ok
                 and not other_sit_changed}

    # G5: actor-type distribution
    def dist(r):
        types = Counter(t for d in r["developments"].values() for t in d["principal_types"])
        nkeys = Counter(min(len(d["situation_keys"]), 4) for d in r["developments"].values())
        share = sum(1 for d in r["developments"].values() if d["situation_keys"]) / len(r["developments"])
        return types, nkeys, share
    (bt, bn, bs), (ct, cn, cs) = dist(base), dist(cand)
    changed = {}
    for eid, b in base["developments"].items():
        c = cand["developments"][eid]
        if (b["principals"], b["principal_types"], b["situation_keys"]) != (c["principals"], c["principal_types"], c["situation_keys"]):
            names = set(b["principals"]) | set(c["principals"])
            changed[eid] = {"base": b["principals"], "cand": c["principals"],
                            "base_keys": b["situation_keys"], "cand_keys": c["situation_keys"],
                            "explained": carries(names, A_NAMES) or carries(names, B_NAMES) or carries(names, C_NAMES)}
    out["G5"] = {"principal_types": {"base": dict(bt), "cand": dict(ct)},
                 "situation_key_count_per_development": {"base": dict(bn), "cand": dict(cn)},
                 "share_with_keys": {"base": round(bs, 4), "cand": round(cs, 4)},
                 "changed_developments": len(changed),
                 "unexplained": {k: v for k, v in changed.items() if not v["explained"]},
                 "changes": changed,
                 "pass": (bs - cs) < 0.01 and all(v["explained"] for v in changed.values())}

    # G6: topic keys (Development identity input)
    topic = {}
    for eid, b in base["developments"].items():
        c = cand["developments"][eid]
        if b["topic_keys"] != c["topic_keys"]:
            names = set(b["principals"]) | set(c["principals"])
            topic[eid] = {"base": b["topic_keys"], "cand": c["topic_keys"],
                          "explained": carries(names, B_NAMES) or carries(names, C_NAMES)}
    out["G6"] = {"changed": len(topic), "unexplained": {k: v for k, v in topic.items() if not v["explained"]},
                 "changes": topic, "pass": all(v["explained"] for v in topic.values())}
    Path(out_p).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    for g in ("G1", "G5", "G6"):
        print(g, "PASS" if out[g]["pass"] else "FAIL")
    print("G1 situations:", {k: v["got"] for k, v in g1_sit.items() if not v["ok"]} or "all as expected",
          "| D402:", d402.get("principals"), "| guards:", guards_ok, "| other Situations changed:", other_sit_changed)
    print("G5 share with keys:", out["G5"]["share_with_keys"], "| changed Developments:", len(changed),
          "| unexplained:", len(out["G5"]["unexplained"]))
    print("G6 topic-key changes:", len(topic), "| unexplained:", len(out["G6"]["unexplained"]))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(*sys.argv[1:4]))
