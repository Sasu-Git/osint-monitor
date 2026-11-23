"""Follow-up facts: items with no compatible link to earlier members, near-duplicate-path items, gold manifests.
Usage: python d398_followup.py <snapshot.db> <results dir>   (reads d398_attach_rows.json; snapshot opened read-only)"""
import json, sqlite3, subprocess, sys
from collections import Counter
snap, d = sys.argv[1], sys.argv[2]
rows = json.load(open(f"{d}/d398_attach_rows.json"))
c = sqlite3.connect(f"file:{snap}?mode=ro", uri=True)
sim = {i: (s, a) for i, s, a in c.execute("select item_id, similarity_score, added_at from event_items where event_id=398")}
out = {}
zero = [r for r in rows if r["n_compat_prior"] == 0]
out["zero_link_items"] = [{"id": r["id"], "similarity_score": sim[r["id"]][0], "added_at": sim[r["id"]][1],
                           "max_cos_prior": round(r["max_cos_prior"], 3),
                           "title": c.execute("select title from raw_items where id=?", (r["id"],)).fetchone()[0]} for r in zero]
nd = [r for r in rows if sim[r["id"]][0] != 1.0]
out["near_dup_path_items"] = {"n": len(nd), "n_compat_prior_quantiles": sorted(r["n_compat_prior"] for r in nd)[::max(1, len(nd)//10)],
                              "zero_compat": sum(1 for r in nd if r["n_compat_prior"] == 0),
                              "similarity_range": [min(sim[r["id"]][0] for r in nd), max(sim[r["id"]][0] for r in nd)]}
out["same_run_items_note"] = "links to same-run members not counted (only earlier runs)"
# gold manifests
ref = "origin/eval/upstream-gold-20261123"
for k in ("topic", "location"):
    txt = subprocess.run(["git", "show", f"{ref}:evaluations/upstream-gold-20261123/{k}/manifest.json"], capture_output=True, text=True, encoding="utf-8").stdout
    m = json.loads(txt)
    flat = json.dumps(m)
    ids = set()
    def walk(o, key=None):
        if isinstance(o, dict):
            for kk, v in o.items():
                if kk in ("event_id", "development_id", "id", "dev_id") and isinstance(v, int):
                    ids.add(v)
                walk(v, kk)
        elif isinstance(o, list):
            for v in o:
                if isinstance(v, int) and key and "id" in key:
                    ids.add(v)
                walk(v, key)
    walk(m)
    out[f"gold_{k}"] = {"top_keys": list(m.keys()), "first_id": m.get("first_id"), "ids_found": len(ids),
                        "min_id": min(ids) if ids else None, "contains_398": 398 in ids,
                        "literal_398_token_present": any(t in flat for t in ("[398,", " 398,", " 398]", ":398", '"D398"', '"398"'))}
json.dump(out, open(f"{d}/followup.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False)[:5000])
