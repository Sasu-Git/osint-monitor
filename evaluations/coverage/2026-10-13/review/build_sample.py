"""Freeze the coverage-recoverability sample (read-only on the snapshot; run with the deployed code on PYTHONPATH).

    python build_sample.py SNAPSHOT_DB ../coverage.json

Draws a fixed-seed sample of unsurfaced items from four review strata of the 2026-10-13 coverage diagnosis, finds the
partner items that put each one in its bucket (the same rules as coverage_diag.py), and writes:

  sample-manifest.json  seed, code SHA, snapshot sha256, strata pool sizes, sample membership, partner ids per case
  review-cases.json     blind review cases: item + up to 3 partners, in a seeded shuffled order, with no bucket,
                        score or rule (what the owner sees before labelling)
  key.json              per case: stratum and the reason it entered the bucket (revealed only after a label is saved)

Partners per stratum:
  below_threshold        the 3 cross-source items within 48 h with the highest production cosine (all below 0.53)
  segmentation_es / _it  the linked partners (production link rule) whose link a segmentation guard cut, by cosine
  cross_language         the 3 other-language items within 24 h with the highest multilingual cosine
"""
import hashlib
import json
import random
import subprocess
import sys
from datetime import timedelta
from pathlib import Path

import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload, sessionmaker

sys.stdout.reconfigure(encoding="utf-8")
SEED = 20261013
PER_STRATUM = 30
TOP = 3
LINK = 0.53
HERE = Path(__file__).resolve().parent
STRATA = {
    "below_threshold": lambda r: r["reason"] == "below_link_threshold",
    "segmentation_es": lambda r: r["reason"] == "segmentation_rejected" and r["lang"] == "es",
    "segmentation_it": lambda r: r["reason"] == "segmentation_rejected" and r["lang"] == "it",
    "cross_language": lambda r: r["reason"] == "cross_language_candidate",
}


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(db: str, coverage: str) -> int:
    from osint_monitor.core.config import load_event_grouping_config
    from osint_monitor.processors import lexical
    from osint_monitor.core.database import RawItem
    from osint_monitor.processors.development_segmentation import incompatibility, segment_items
    from osint_monitor.processors.embeddings import blob_to_embedding
    from osint_monitor.processors.language import item_language
    import osint_monitor

    rows = json.load(open(coverage, encoding="utf-8"))["rows"]
    rng = random.Random(SEED)
    pools = {k: sorted(r["id"] for r in rows if f(r)) for k, f in STRATA.items()}
    sample = {k: sorted(rng.sample(ids, min(PER_STRATUM, len(ids)))) for k, ids in pools.items()}

    s = sessionmaker(bind=create_engine(f"sqlite:///file:{db}?mode=ro&uri=true", connect_args={"uri": True}))()
    cfg = load_event_grouping_config()
    items = s.query(RawItem).options(joinedload(RawItem.source)).filter(RawItem.embedding.isnot(None)).all()
    by_id = {r.id: r for r in items}
    ids = [r.id for r in items]
    pos = {i: k for k, i in enumerate(ids)}
    X = np.array([blob_to_embedding(r.embedding) for r in items], dtype=np.float32)
    X /= np.linalg.norm(X, axis=1, keepdims=True) + 1e-9
    t = np.array([(r.published_at or r.fetched_at).timestamp() for r in items])
    src = np.array([r.source_id for r in items])
    lang = {r.id: item_language(r.source.name if r.source else None, r.title or "") for r in items}

    def near(i, hours):
        k = pos[i]
        n = np.where(np.abs(t - t[k]) <= hours * 3600)[0]
        return n[n != k]

    partners, reasons = {}, {}
    # below threshold: top cross-source production cosine within 48 h
    for i in sample["below_threshold"]:
        n = near(i, 48)
        n = n[src[n] != by_id[i].source_id]
        cos = X[n] @ X[pos[i]]
        top = np.argsort(-cos)[:TOP]
        partners[i] = [ids[n[j]] for j in top]
        reasons[i] = {"rule": "best cross-source cosine within 48 h is in [0.45, 0.53): below the 0.53 link threshold",
                      "scores": [round(float(cos[j]), 3) for j in top]}
    # segmentation-rejected: linked partners whose links a guard cut
    seg_items = sample["segmentation_es"] + sample["segmentation_it"]
    linked = {}
    for i in seg_items:
        n = near(i, 48)
        cos = X[n] @ X[pos[i]]
        out = []
        for j, c in zip(n, cos):
            other = by_id[ids[j]]
            if other.source_id != by_id[i].source_id and c >= LINK:
                out.append((ids[j], float(c)))
            elif other.source_id == by_id[i].source_id and c >= 0.5 and lexical.same_source_update(
                    by_id[i].title or "", other.title or ""):
                out.append((ids[j], float(c)))
        linked[i] = sorted(out, key=lambda x: -x[1])
    seg = segment_items(s, set(seg_items) | {j for i in seg_items for j, _ in linked[i]}, cfg.development_segmentation)
    for i in seg_items:
        cut = [(j, c, incompatibility(seg[i], seg[j], cfg.development_segmentation)) for j, c in linked[i]
               if i in seg and j in seg]
        cut = [x for x in cut if x[2]][:TOP]
        partners[i] = [j for j, _, _ in cut]
        reasons[i] = {"rule": "linked by the production rule (cosine >= 0.53 cross-source, or a same-source update), "
                              "but a segmentation guard cut every link",
                      "scores": [round(c, 3) for _, c, _ in cut], "guards": [g for _, _, g in cut]}
    # cross-language: multilingual cosine to other-language items within 24 h
    from sentence_transformers import SentenceTransformer
    ml = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    import re
    meta = re.compile(r"^\s*Domain:\s*\S+\s*\|\s*Language:[^|]*\|\s*Source country:[^|]*$", re.I)

    def text(r):
        return (r.title or "") if meta.match(r.content or "") else f"{r.title or ''}. {(r.content or '')[:300]}"
    for i in sample["cross_language"]:
        n = [ids[j] for j in near(i, 24) if lang[ids[j]] != lang[i]]
        M = ml.encode([text(by_id[i])] + [text(by_id[j]) for j in n], normalize_embeddings=True,
                      batch_size=64, show_progress_bar=False)
        cos = M[1:] @ M[0]
        top = np.argsort(-cos)[:TOP]
        partners[i] = [n[j] for j in top]
        reasons[i] = {"rule": "no same-language link; another-language report within 24 h scores >= 0.60 with the "
                              "multilingual model", "scores": [round(float(cos[j]), 3) for j in top]}

    def show(r):
        return {"id": r.id, "source": r.source.name if r.source else None, "lang": lang[r.id],
                "published": (r.published_at or r.fetched_at).isoformat(timespec="minutes"), "title": r.title,
                "excerpt": "" if meta.match(r.content or "") else (r.content or "")[:400], "url": r.url}

    order = [(k, i) for k in STRATA for i in sample[k]]
    random.Random(SEED + 1).shuffle(order)
    cases, key = [], {}
    for n, (k, i) in enumerate(order, 1):
        cid = f"C{n:03d}"
        cases.append({"case": cid, "item": show(by_id[i]), "partners": [show(by_id[j]) for j in partners[i]]})
        key[cid] = {"stratum": k, "item": i, "partners": partners[i], **reasons[i]}

    code = subprocess.run(["git", "-C", str(Path(osint_monitor.__file__).parent), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    manifest = {"seed": SEED, "shuffle_seed": SEED + 1, "per_stratum": PER_STRATUM, "top_partners": TOP,
                "code_sha": code, "snapshot": Path(db).name, "snapshot_sha256": sha256(db),
                "coverage_json_sha256": sha256(coverage), "pool_sizes": {k: len(v) for k, v in pools.items()},
                "sample": sample, "cases": {cid: {"item": v["item"], "partners": v["partners"]} for cid, v in key.items()}}
    for name, obj in (("sample-manifest.json", manifest), ("review-cases.json", cases), ("key.json", key)):
        (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print({k: len(v) for k, v in sample.items()}, "cases", len(cases),
          "without partners:", [c for c, v in key.items() if not v["partners"]])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
