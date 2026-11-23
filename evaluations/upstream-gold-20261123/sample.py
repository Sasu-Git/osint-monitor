"""Draw the two blind upstream gold samples (topic/event A, location B) from the 2026-11-23 VM snapshot.

    PYTHONPATH=<worktree> HF_HUB_OFFLINE=1 <main .venv python> sample.py --snapshot gold-snap.db \
        --situation-key key.json --iter3-manifest manifest.json --out-dir <this dir>

Writes topic/manifest.json, topic/cases.json, location/manifest.json, location/cases.json. Labels nothing, scores nothing.
Snapshot sha256 is verified, the file is opened read-only and copied with the sqlite backup API into a temp dir.
"""
import argparse, hashlib, json, random, re, shutil, sqlite3, tempfile
from pathlib import Path

from osint_monitor.processors.development_segmentation import REPORT, headline_kind
from osint_monitor.processors.language import item_language

SNAP_SHA = "7463859a4f3537eb29447a755f252dbebc80cc01a1d855739c57b10489964c3c"
FIRST_ID = 1342                      # id > 1341
SEED_A, SEED_B, SEED_SUBSET = 20261123, 20261124, 20261125
SIZE_A = {"en": 70, "es": 40, "it": 40}
SIZE_B = {"en": 80, "es": 35, "it": 35}
STRIKE_SHARE = 0.40
SUBSET_SIZE = 50
LEAD_SHOWN, ITEMS_SHOWN = 600, 25

# Stratification only; never shown to the labeller.
STRIKE_WORDS = {
    "en": r"attack\w*|strike\w*|struck|airstrike\w*|bomb\w*|shell(?:ing|ed)|raid\w*",
    "es": r"ataque\w*|atac(?:a|an|ar|ó|aron|ando)|bombardeo\w*|bombardea\w*|bombardeó|bombardearon",
    "it": r"attacc\w*|attacca\w*|raid\w*|bombardament\w*|bombarda\w*|colpisc\w*|colpit\w*",
}
STRIKE_RE = {k: re.compile(r"\b(?:%s)\b" % v, re.I) for k, v in STRIKE_WORDS.items()}


def is_unknown(t):
    return t is None or str(t).strip().lower() in ("", "unknown")


def collect_ids(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("development_id", "event_id") and isinstance(v, int):
                out.add(v)
            collect_ids(v, out)
    elif isinstance(obj, list):
        for v in obj:
            collect_ids(v, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--situation-key", required=True)
    ap.add_argument("--iter3-manifest", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    snap = Path(a.snapshot)
    sha = hashlib.sha256(snap.read_bytes()).hexdigest()
    if sha != SNAP_SHA:
        raise SystemExit(f"snapshot sha256 mismatch: {sha}")

    excl = set()
    for p in (a.situation_key, a.iter3_manifest):
        collect_ids(json.loads(Path(p).read_text(encoding="utf-8")), excl)

    tmp = Path(tempfile.mkdtemp(prefix="gold-"))
    src = sqlite3.connect(f"file:{snap.as_posix()}?mode=ro", uri=True)
    db = sqlite3.connect(tmp / "copy.db")
    src.backup(db)
    src.close()

    rows = db.execute("select id, summary, event_type from events where id >= ? order by id", (FIRST_ID,)).fetchall()
    frame = len(rows)
    dev = {}
    n_excl = n_noreport = 0
    for i, summary, et in rows:
        if i in excl:
            n_excl += 1
            continue
        items = db.execute(
            "select r.id, s.name, r.published_at, r.title, r.content from event_items ei"
            " join raw_items r on r.id = ei.item_id left join sources s on s.id = r.source_id"
            " where ei.event_id = ? order by r.id", (i,)).fetchall()
        if not any(headline_kind(t[3]) == REPORT for t in items):
            n_noreport += 1
            continue
        langs = {}
        for it in items:
            l = item_language(it[1], it[3] or "")
            langs[l] = langs.get(l, 0) + 1
        dom = sorted(langs.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        dev[i] = {"items": items, "lang": dom, "unknown": is_unknown(et),
                  "strike": bool(STRIKE_RE.get(dom) and any(STRIKE_RE[dom].search(t[3] or "") for t in items))}
    elig = sorted(dev)
    report = {"frame_developments_id_gt_1341": frame, "excluded_by_key_or_manifest": n_excl,
              "excluded_no_report_headline": n_noreport, "eligible": len(elig),
              "eligible_by_language": {l: sum(1 for d in dev.values() if d["lang"] == l)
                                       for l in sorted({d["lang"] for d in dev.values()})},
              "eligible_unknown_by_language": {l: sum(1 for d in dev.values() if d["lang"] == l and d["unknown"])
                                               for l in sorted({d["lang"] for d in dev.values()})},
              "eligible_strike_by_language": {l: sum(1 for d in dev.values() if d["lang"] == l and d["strike"])
                                              for l in sorted({d["lang"] for d in dev.values()})}}

    shortfalls = []
    # ---- Sample A
    rng = random.Random(SEED_A)
    A, A_strata = [], {}
    for l in ("en", "es", "it"):
        want_unk = SIZE_A[l] // 2
        for kind, n in (("unknown", want_unk), ("typed", SIZE_A[l] - want_unk)):
            pool = [i for i in elig if dev[i]["lang"] == l and dev[i]["unknown"] == (kind == "unknown")]
            take = rng.sample(pool, min(n, len(pool)))
            if len(pool) < n:
                shortfalls.append({"sample": "A", "stratum": f"{l}/{kind}", "wanted": n, "available": len(pool)})
            A_strata[f"{l}/{kind}"] = {"wanted": n, "pool": len(pool), "drawn": len(take)}
            A += [(i, f"{l}/{kind}") for i in sorted(take)]
    a_ids = {i for i, _ in A}
    # ---- Sample B (disjoint from A). Strike strata first, then random from the rest of the language.
    rng = random.Random(SEED_B)
    B, B_strata = [], {}
    for l in ("en", "es", "it"):
        n_strike = round(SIZE_B[l] * STRIKE_SHARE)
        for kind, n in (("strike", n_strike), ("random", SIZE_B[l] - n_strike)):
            taken = {i for i, _ in B}
            pool = [i for i in elig if dev[i]["lang"] == l and i not in a_ids and i not in taken
                    and (kind == "random" or dev[i]["strike"])]
            take = rng.sample(pool, min(n, len(pool)))
            if len(pool) < n:
                shortfalls.append({"sample": "B", "stratum": f"{l}/{kind}", "wanted": n, "available": len(pool)})
            B_strata[f"{l}/{kind}"] = {"wanted": n, "pool": len(pool), "drawn": len(take)}
            B += [(i, f"{l}/{kind}") for i in sorted(take)]
    b_ids = sorted(i for i, _ in B)
    assert not (a_ids & set(b_ids)) and len(set(b_ids)) == len(b_ids)
    subset = sorted(random.Random(SEED_SUBSET).sample(b_ids, min(SUBSET_SIZE, len(b_ids))))

    def case(i):
        d = dev[i]
        return {"development_id": i, "members": len(d["items"]),
                "items": [{"item_id": t[0], "source": t[1], "published_at": t[2], "title": t[3],
                           "text": re.sub(r"\s+", " ", t[4] or "").strip()[:LEAD_SHOWN]} for t in d["items"][:ITEMS_SHOWN]]}

    out = Path(a.out_dir)
    common = {"snapshot": "gold-snap.db", "snapshot_sha256": sha, "first_id": FIRST_ID,
              "eligibility": "id > 1341; not in situation-membership key.json or iter3 manifest; >= 1 report headline "
                             "(headline_kind == report); dominant language = most common item_language(source, title)",
              "frame": report, "shortfalls": shortfalls}
    sa = dict(common, sample="A topic/event", seed=SEED_A, target=SIZE_A, strata=A_strata,
              unknown_definition="stored event_type NULL, '' or 'unknown'; every other value (incl. 'other') is typed",
              cases=[{"development_id": i, "stratum": s} for i, s in A])
    sb = dict(common, sample="B location", seed=SEED_B, role_subset_seed=SEED_SUBSET, target=SIZE_B,
              strike_share=STRIKE_SHARE, strike_words=STRIKE_WORDS, strata=B_strata,
              disjoint_from="topic/manifest.json", role_subset=subset,
              cases=[{"development_id": i, "stratum": s, "role_labels": i in subset} for i, s in B])
    for d, m, ids in (("topic", sa, sorted(a_ids)), ("location", sb, b_ids)):
        (out / d / "manifest.json").write_text(json.dumps(m, indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
        cs = {"cases": [dict(case(i), **({"role_labels": i in subset} if d == "location" else {})) for i in ids]}
        (out / d / "cases.json").write_text(json.dumps(cs, indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(json.dumps(report), "\nA", json.dumps(A_strata), "\nB", json.dumps(B_strata), "\nshortfalls", shortfalls)
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
