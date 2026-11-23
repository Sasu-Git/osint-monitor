"""Derive the owner's V4 condition at read time from the JSONL; never stored as a field.

V4 = at least two report-item components, each with at least two items.
Usage: python derive_v4.py [snap-*.jsonl]
"""
import json, sys
from pathlib import Path

p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("snap-7463859a.jsonl")
n = v4 = 0
for line in p.read_text(encoding="utf-8").splitlines():
    r = json.loads(line)
    n += 1
    if sum(1 for s in r["component_sizes"] if s >= 2) >= 2:
        v4 += 1
print(f"developments={n} v4_derived={v4}")
