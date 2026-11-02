"""Near-boundary pairs across the whole snapshot (read-only).

For every Development, every pair of items the matcher could compare (both prefixes >= syndication_min_chars, the
later item not primary/commentary, different origins; no early stop), compute the P2 bound and SequenceMatcher's
quick_ratio(); compute the full ratio() only when the bound is >= 0.80. Records every pair with ratio >= 0.80 or
bound >= 0.95 and checks, on all of them: bound == quick_ratio(), ratio() <= bound.

    python boundary.py --db <snapshot> --out boundary_pairs.csv
"""
import argparse, csv, sqlite3
from collections import Counter
from datetime import datetime
from difflib import SequenceMatcher

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.core.models import EvidenceType
from osint_monitor.processors.provenance import resolve as R
from osint_monitor.processors.provenance.context import build_evidence

ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()

captured = {}
def capture(self, items, resolved):                  # keep the pre-syndication provenance, do no matching
    captured["items"], captured["resolved"] = items, list(resolved)
R.ProvenanceResolver._mark_syndicated_copies = capture

resolver = R.ProvenanceResolver()
cfg = resolver.config
n, thr = cfg.syndication_min_chars, cfg.syndication_similarity
session = sessionmaker(bind=create_engine(f"sqlite:///file:{a.db}?mode=ro&uri=true"))()
ids = [r[0] for r in sqlite3.connect(f"file:{a.db}?mode=ro", uri=True).execute("select id from events order by id")]
stats = Counter()
with open(a.out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["event_id", "item_i", "item_j", "bound", "quick_ratio", "ratio"])
    for eid in ids:
        items = build_evidence(session, eid)
        resolver.resolve(items)
        items, resolved = captured["items"], captured["resolved"]
        order = sorted(range(len(items)), key=lambda i: (items[i].published_at or datetime.min, i))
        earlier = []
        for i in order:
            body = R._normalize(items[i].text)
            if len(body) < n:
                continue
            prefix = body[: n * 2]
            counts = Counter(prefix)
            if resolved[i].evidence_type not in (EvidenceType.PRIMARY, EvidenceType.COMMENTARY):
                for other, j, oc in earlier:
                    if resolved[j].origin == resolved[i].origin:
                        continue
                    stats["pairs"] += 1
                    bound = 2.0 * sum((counts & oc).values()) / (len(prefix) + len(other))
                    if bound < 0.80:
                        continue
                    sm = SequenceMatcher(None, prefix, other, autojunk=False)
                    q, r = sm.quick_ratio(), sm.ratio()
                    stats["bound_ge_0.80"] += 1
                    stats["bound_ne_quick"] += bound != q
                    stats["ratio_gt_bound"] += r > bound
                    if r >= 0.80 or bound >= thr:
                        w.writerow([eid, items[i].item_id, items[j].item_id, repr(bound), repr(q), repr(r)])
                        stats["recorded"] += 1
                        stats["ratio_0.90_0.95"] += 0.90 <= r < thr
                        stats["ratio_ge_thr"] += r >= thr
                        stats["bound_ge_thr_ratio_lt_thr"] += bound >= thr > r
            earlier.append((prefix, i, counts))
print(dict(stats))
