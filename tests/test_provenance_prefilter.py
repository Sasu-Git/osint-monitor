"""The syndicated-copy pre-check is a pure shortcut: same pairs accepted, same provenance, same order.

The reference below is the matcher as it was before the pre-check (main 44e0357), kept verbatim so the new code is
compared against it on random and near-threshold inputs (evaluations/performance/pair-matcher/EQUIVALENCE.md).
"""

import random
import string
from collections import Counter
from datetime import datetime, timedelta
from difflib import SequenceMatcher

import pytest

from osint_monitor.core.models import EvidenceItem, EvidenceType
from osint_monitor.processors.provenance import ProvenanceResolver, assess_confidence
from osint_monitor.processors.provenance.resolve import _normalize, quick_ratio_bound

T0 = datetime(2026, 9, 24, 8, 0)
ALPHABET = string.ascii_lowercase + " " * 6 + ".,'"


def reference_mark(self, items, resolved):
    """ProvenanceResolver._mark_syndicated_copies before the pre-check (verbatim)."""
    cfg = self.config
    n = cfg.syndication_min_chars
    order = sorted(range(len(items)), key=lambda i: (items[i].published_at or datetime.min, i))
    earlier = []
    for i in order:
        body = _normalize(items[i].text)
        if len(body) < n:
            continue
        prefix = body[: n * 2]
        prov = resolved[i]
        if prov.evidence_type not in (EvidenceType.PRIMARY, EvidenceType.COMMENTARY):
            for other_prefix, j in earlier:
                if resolved[j].origin == prov.origin:
                    continue
                if SequenceMatcher(None, prefix, other_prefix, autojunk=False).ratio() >= cfg.syndication_similarity:
                    origin = resolved[j].origin
                    resolved[i] = prov.model_copy(update={
                        "evidence_type": EvidenceType.DERIVATIVE, "origin": origin, "derived_from": origin,
                        "note": f"near-identical copy of {resolved[j].source_name}",
                    })
                    break
        earlier.append((prefix, i))


def text(rnd, length=420):
    return "".join(rnd.choice(ALPHABET) for _ in range(length))


def edit(rnd, s, k):
    """k random single-character substitutions, insertions or deletions."""
    s = list(s)
    for _ in range(k):
        pos = rnd.randrange(len(s))
        op = rnd.random()
        if op < 0.4:
            s[pos] = rnd.choice(ALPHABET)
        elif op < 0.7:
            s.insert(pos, rnd.choice(ALPHABET))
        else:
            del s[pos]
    return "".join(s)


# --- the bound --------------------------------------------------------------------------------------

def test_bound_equals_quick_ratio_and_never_below_ratio():
    rnd = random.Random(1)
    near = 0
    for _ in range(1500):
        a = text(rnd, rnd.randint(150, 400))
        b = edit(rnd, a, rnd.randint(0, 40)) if rnd.random() < 0.7 else text(rnd, rnd.randint(150, 400))
        sm = SequenceMatcher(None, a, b, autojunk=False)
        bound = quick_ratio_bound(Counter(a), Counter(b), len(a) + len(b))
        assert bound == sm.quick_ratio()                        # exactly difflib's own value
        r = sm.ratio()
        assert r <= bound
        near += 0.90 <= r < 0.99
    assert near > 50                                           # plenty of pairs around the 0.95 threshold


def test_bound_handles_empty_strings_like_difflib():
    assert quick_ratio_bound(Counter(), Counter(), 0) == SequenceMatcher(None, "", "").quick_ratio() == 1.0


# --- the matcher, end to end ------------------------------------------------------------------------

def corpus(rnd, n_items, copy_share):
    """Items from several outlets; some are near-copies of earlier ones at distances that straddle the threshold."""
    bases, items = [], []
    for k in range(n_items):
        if bases and rnd.random() < copy_share:
            body = edit(rnd, rnd.choice(bases), rnd.choice([0, 1, 3, 6, 9, 12, 15, 20, 30]))
        else:
            body = text(rnd, rnd.randint(150, 600))
            bases.append(body)
        items.append(EvidenceItem(item_id=k, source_name=rnd.choice(["Reuters", "BBC World", "Al Jazeera", "AP",
                                                                      "Le Monde", "DW", "Kyiv Independent"]),
                                  source_category="news", collector_type="rss",
                                  title=f"Report {k}", text=body,
                                  published_at=T0 + timedelta(minutes=rnd.randint(0, 600))))
    return items


@pytest.mark.parametrize("seed,n_items,copy_share", [(s, 8, 0.5) for s in range(4)] + [(s, 60, 0.4) for s in range(3)]
                         + [(0, 120, 0.3)])
def test_resolve_identical_to_reference(monkeypatch, seed, n_items, copy_share):
    items = corpus(random.Random(seed), n_items, copy_share)
    new = ProvenanceResolver()
    got = [p.model_dump() for p in new.resolve(items)]
    got_conf = assess_confidence(items, new).model_dump()
    monkeypatch.setattr(ProvenanceResolver, "_mark_syndicated_copies", reference_mark)
    ref = ProvenanceResolver()
    want = [p.model_dump() for p in ref.resolve(items)]
    assert got == want
    assert got_conf == assess_confidence(items, ref).model_dump()
    assert any(p["evidence_type"] == EvidenceType.DERIVATIVE for p in want if "copy" in p["note"])  # copies exercised


def test_first_match_order_is_kept(monkeypatch):
    """An item similar to two earlier items from different outlets is attributed to the first one in time order."""
    rnd = random.Random(7)
    base = text(rnd, 420)
    items = [EvidenceItem(item_id=1, source_name="Reuters", source_category="news", text=base, published_at=T0),
             EvidenceItem(item_id=2, source_name="AP", source_category="news", text=edit(rnd, base, 2),
                          published_at=T0 + timedelta(minutes=1)),
             EvidenceItem(item_id=3, source_name="DW", source_category="news", text=edit(rnd, base, 1),
                          published_at=T0 + timedelta(minutes=2))]
    got = [p.model_dump() for p in ProvenanceResolver().resolve(items)]
    monkeypatch.setattr(ProvenanceResolver, "_mark_syndicated_copies", reference_mark)
    assert got == [p.model_dump() for p in ProvenanceResolver().resolve(items)]
