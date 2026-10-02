"""Institutional items sample (read-only). python inst.py <db>"""
import sqlite3, sys, random, numpy as np
random.seed(20261001)
c = sqlite3.connect(f"file:{sys.argv[1]}?mode=ro", uri=True)
q = lambda s, *a: c.execute(s, a).fetchall()
inst = ["White House","State Department","Defense.gov","European Commission Press","Council of the EU Press","European Parliament Press","UN News","UN Press","Federal Register","ECB Press","Federal Reserve Press"]
for s in inst:
    rows = q("select r.id, r.published_at, r.title, (select group_concat(event_id) from event_items where item_id=r.id) from raw_items r join sources so on so.id=r.source_id where so.name=? order by r.id", s)
    pick = sorted(random.sample(rows, min(3, len(rows))))
    print(s, len(rows), "in events:", sum(1 for r in rows if r[3]))
    for r in pick: print("   ", r[0], r[1][:16] if r[1] else None, r[3], r[2][:100])
emb = lambda i: (lambda v: v / np.linalg.norm(v))(np.frombuffer(q("select embedding from raw_items where id=?", i)[0][0], dtype=np.float32))
for a, bs in [(23, [48, 57, 238, 267]), (167, [48, 238, 176]), (4, [488, 510])]:
    print(a, q("select title from raw_items where id=?", a)[0][0][:60], [(b, round(float(emb(a) @ emb(b)), 3)) for b in bs])
