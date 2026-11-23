"""Approved laptop<->VM reproducibility gate (2026-11-23): cosine distance <= 1e-4 decides; bitwise is informational."""
import base64
import importlib.util
import json
from pathlib import Path

import numpy as np

PKG = Path(__file__).resolve().parents[1] / "deploy" / "multilingual-model"
spec = importlib.util.spec_from_file_location("compare_repro", PKG / "compare_repro.py")
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)


def _write(tmp, name, ref, emb):
    d = dict(ref)
    d["_full_embedding_b64"] = base64.b64encode(emb.astype(np.float32).tobytes()).decode()
    d["embeddings_sha256_bitwise"] = __import__("hashlib").sha256(emb.astype(np.float32).tobytes()).hexdigest()
    p = tmp / name
    p.write_text(json.dumps(d), encoding="utf-8")
    return p


def _ref():
    d = json.loads((PKG / "repro-laptop.json").read_text(encoding="utf-8"))
    e = np.frombuffer(base64.b64decode(d["_full_embedding_b64"]), dtype=np.float32).reshape(d["shape"]).copy()
    return d, e


def test_gate_constant_is_approved_value():
    assert cr.COSINE_DISTANCE_MAX == 1e-4


def test_identical_passes_and_reports_bitwise(tmp_path):
    d, e = _ref()
    a = _write(tmp_path, "a.json", d, e)
    assert cr.main([str(a), str(a)]) == 0


def test_tiny_float_noise_passes_but_not_bitwise(tmp_path):
    d, e = _ref()
    a = _write(tmp_path, "a.json", d, e)
    b = _write(tmp_path, "b.json", d, e + np.float32(1e-6))
    out = tmp_path / "r.json"
    assert cr.main([str(a), str(b), "--out", str(out)]) == 0
    r = json.loads(out.read_text(encoding="utf-8"))
    assert r["pass"] and r["informational"]["bitwise_identical"] is False


def test_drift_over_gate_fails(tmp_path):
    d, e = _ref()
    a = _write(tmp_path, "a.json", d, e)
    e2 = e.copy()
    e2[3] = np.roll(e2[3], 1)          # one sentence clearly different
    b = _write(tmp_path, "b.json", d, e2)
    out = tmp_path / "r.json"
    assert cr.main([str(a), str(b), "--out", str(out)]) == 1
    assert json.loads(out.read_text(encoding="utf-8"))["sentences_over_gate"] == [3]


def test_different_revision_not_comparable(tmp_path):
    d, e = _ref()
    a = _write(tmp_path, "a.json", d, e)
    b = _write(tmp_path, "b.json", dict(d, revision="0" * 40), e)
    assert cr.main([str(a), str(b)]) == 2
