"""repair_situations.invalid_reason validates actor sets through the Situation canonicaliser (2026-11-23)."""
import importlib.util
from pathlib import Path

import pytest

from osint_monitor.processors.actors import ActorNormalizer

_spec = importlib.util.spec_from_file_location("repair_situations",
                                               Path(__file__).resolve().parents[1] / "scripts" / "repair_situations.py")
repair = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(repair)


@pytest.fixture(scope="module")
def norm():
    return ActorNormalizer.load()


@pytest.mark.parametrize("actors", [["Elon Musk", "Musk"], ["Christa Pike", "Pike"], ["Javier Milei", "Milei"],
                                    ["Machado", "Maria Corina Machado"]])
def test_name_variant_pairs_are_invalid(norm, actors):
    assert repair.invalid_reason(actors, norm, 2) is not None


@pytest.mark.parametrize("actors", [["China", "United States"], ["Israel", "Palestine"], ["Rachel", "Simon"],
                                    ["Jair Bolsonaro", "Flávio Bolsonaro"]])
def test_valid_or_unchanged_sets_pass(norm, actors):
    assert repair.invalid_reason(actors, norm, 2) is None


def test_previous_findings_still_found(norm):
    assert "collapse" in repair.invalid_reason(["Donald J. Trump", "United States"], norm, 2)
    assert "no longer actors" in repair.invalid_reason(["Democrat", "United States"], norm, 2)
