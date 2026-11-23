"""Compare two repro_check outputs (reference, candidate) under the approved reproducibility gate.

Gate (owner approval 2026-11-23): every sentence's cosine distance between reference and candidate embeddings is
<= 1e-4. Bitwise equality of the float32 embeddings is reported separately and never decides PASS/FAIL.

    python compare_repro.py repro-laptop.json repro-vm.json [--out result.json]

Exit 0 = PASS, 1 = FAIL (gate), 2 = inputs not comparable (different sentences, shape or model revision).
"""
import argparse, base64, json, sys
import numpy as np

COSINE_DISTANCE_MAX = 1e-4  # owner-approved gate, 2026-11-23


def load(p):
    d = json.load(open(p, encoding="utf-8"))
    e = np.frombuffer(base64.b64decode(d["_full_embedding_b64"]), dtype=np.float32).reshape(d["shape"])
    return d, e


def compare(a, ea, b, eb):
    problems = [f"{k} differs" for k in ("model", "revision", "shape", "sentences")
                if k in a and k in b and a[k] != b[k]]
    if problems:
        return {"comparable": False, "problems": problems}
    cos = (ea * eb).sum(1) / (np.linalg.norm(ea, axis=1) * np.linalg.norm(eb, axis=1))
    dist = (1.0 - cos).astype(float)
    return {"comparable": True,
            "gate": f"per-sentence cosine distance <= {COSINE_DISTANCE_MAX:g}",
            "max_cosine_distance": float(dist.max()),
            "sentences_over_gate": [int(i) for i in np.nonzero(dist > COSINE_DISTANCE_MAX)[0]],
            "pass": bool(dist.max() <= COSINE_DISTANCE_MAX),
            "informational": {"bitwise_identical": a["embeddings_sha256_bitwise"] == b["embeddings_sha256_bitwise"],
                              "max_abs_diff": float(np.abs(ea - eb).max())}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("reference"); ap.add_argument("candidate"); ap.add_argument("--out")
    x = ap.parse_args(argv)
    (a, ea), (b, eb) = load(x.reference), load(x.candidate)
    r = compare(a, ea, b, eb)
    r.update(reference=x.reference, candidate=x.candidate)
    if x.out:
        json.dump(r, open(x.out, "w", encoding="utf-8"), indent=1)
    if not r["comparable"]:
        print("NOT COMPARABLE:", "; ".join(r["problems"])); return 2
    print(f"gate ({r['gate']}): {'PASS' if r['pass'] else 'FAIL'}  max distance {r['max_cosine_distance']:.3g}"
          + (f"  over gate: {r['sentences_over_gate']}" if r["sentences_over_gate"] else ""))
    print(f"informational: bitwise identical {r['informational']['bitwise_identical']}, "
          f"max abs diff {r['informational']['max_abs_diff']:.3g}")
    return 0 if r["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
