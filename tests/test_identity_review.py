"""Identity-gold review tooling (evaluations/identity/): verdicts are validated, stored apart from the draft labels,
written deterministically, and never overwritten by regenerating the review sheet."""

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "evaluations" / "identity" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import verdicts as V  # noqa: E402


def test_invalid_verdict_values_are_rejected():
    for bad in ({"verdict": "SAME"}, {"verdict": "AMBIGUOUS", "confidence": "certain"},
                {"verdict": "AMBIGUOUS", "boundary_reason": "vibes"}):
        with pytest.raises(ValueError):
            V.validate(bad)
    ok = V.validate({"verdict": "SAME_DEVELOPMENT", "confidence": "low", "boundary_reason": "same_occurrence",
                     "note": "  x  "})
    assert ok["verdict"] == "SAME_DEVELOPMENT" and ok["note"] == "x" and ok["reviewed_at"]
    assert V.validate({"verdict": None})["reviewed_at"] is None      # clearing a verdict


def test_verdicts_are_deterministic_sorted_and_never_carry_the_draft_label(tmp_path):
    path = tmp_path / "v.yaml"
    path.write_text("B002: {proposed: SAME_DEVELOPMENT, verdict: null, note: null}\n", encoding="utf-8")
    loaded = V.load(["B002", "A001"], path)
    assert "proposed" not in loaded["B002"] and loaded["A001"] == V.blank()
    loaded["B002"] = V.validate({"verdict": "DIFFERENT_DEVELOPMENT"}) | {"reviewed_at": "2026-10-01T00:00:00Z"}
    V.save(loaded, path)
    text = path.read_text(encoding="utf-8")
    assert text.index("A001:") < text.index("B002:") and "proposed" not in text
    assert V.dump(V.load(["A001", "B002"], path)) == text           # round trip is byte-identical


def test_regenerating_the_sheet_never_overwrites_owner_verdicts(tmp_path, monkeypatch):
    import build_review_sheet as B
    path = tmp_path / "owner-verdicts.yaml"
    path.write_text("A001: {verdict: SAME_DEVELOPMENT}\n", encoding="utf-8")
    monkeypatch.setattr(V, "VERDICTS_FILE", path)
    monkeypatch.setattr(B, "REVIEW", tmp_path)
    for name in ("cases.json", "draft-labels.json"):
        (tmp_path / name).write_text((B.ROOT / "review" / name).read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "system-trace").mkdir()
    for f in (B.ROOT / "review" / "system-trace").glob("*.json"):
        (tmp_path / "system-trace" / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
    B.main()
    assert path.read_text(encoding="utf-8") == "A001: {verdict: SAME_DEVELOPMENT}\n"
    assert (tmp_path / "review-cases.json").exists()
