"""Extra read-only checks. python extra.py <db-copy>"""
import sqlite3, sys, json, random, re
import numpy as np
from collections import Counter, defaultdict
from datetime import datetime
random.seed(20261001)
db = sys.argv[1]; THR = float(sys.argv[2]) if len(sys.argv) > 2 else 0.80
c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
q = lambda s, *a: c.execute(s, a).fetchall()
print("== BBC-style same-URL pairs and their events")
for url, ids in q("select url, group_concat(id) from raw_items where source_id in (select id from sources where type='rss') group by url having count(*)>1"):
    ids = [int(x) for x in ids.split(",")]
    evs = [sorted(e for (e,) in q("select event_id from event_items where item_id=?", i)) for i in ids]
    ext = [q("select external_id,title,published_at from raw_items where id=?", i)[0] for i in ids]
    print(ids, evs, [(e[0][-25:] if e[0] else None, e[1][:60], e[2][:16]) for e in ext])
print("== rank_reasons combos")
rr = Counter()
both = []
for eid, r in q("select id, rank_reasons from events"):
    r = json.loads(r or "[]"); rr.update(r)
    if "stale" in r and "new_development" in r: both.append(eid)
print(rr); print("stale+new_development:", len(both))
print("== confidence_class vs corroboration_level mismatch")
m = {"CONFIRMED": "confirmed", "PROBABLE": "probable", "POSSIBLE": "possible", "DOUBTFUL": "doubtful"}
for r in q("select id, confidence_class, corroboration_level, admiralty_rating, source_count from events"):
    if m.get(r[2]) != r[1]: print("  ", r)
print("== seismic: USGS vs explosion detector id overlap")
u = {x[0].replace("usgs_", ""): x[1] for x in q("select external_id, published_at from raw_items r join sources s on s.id=r.source_id where s.name='USGS Seismic'")}
sx = {x[0].replace("seis_exp_", ""): x[1] for x in q("select external_id, published_at from raw_items r join sources s on s.id=r.source_id where s.name='Seismic Explosion Detector'")}
print("usgs", len(u), "explosion", len(sx), "shared ids", len(set(u) & set(sx)))
print("== alerts with item_id / events, sample")
for r in q("select id, alert_type, event_id, item_id, title, created_at from alerts where alert_type in ('source_silence_break','new_event_cluster','iw_threshold','fusion_convergence') order by id limit 12"): print("  ", r)
print("== embedding near-duplicates across sources among unclustered narrative items (cos>=0.80, <=72h)")
rows = q("select r.id, s.name, s.type, r.title, r.published_at, r.fetched_at, r.embedding from raw_items r join sources s on s.id=r.source_id where r.id not in (select item_id from event_items) and r.embedding is not null")
struct_types = {"infrastructure","adsb","ais","aviation","financial","spectrum","sanctions","sigint_vuln","sigint_econ","sigint_displacement","sigint_nuclear","sigint_imint","sigint_trade"}
rows = [r for r in rows if r[2] not in struct_types and r[1] not in ("USGS Seismic","NASA FIRMS","Travel Advisories")]
V = np.stack([np.frombuffer(r[6], dtype=np.float32) for r in rows]); V = V / np.linalg.norm(V, axis=1, keepdims=True)
S = V @ V.T
def ts(r): return datetime.fromisoformat((r[4] or r[5])[:19])
pairs = []
for i in range(len(rows)):
    for j in range(i+1, len(rows)):
        if S[i, j] >= THR and rows[i][1] != rows[j][1] and abs((ts(rows[i]) - ts(rows[j])).total_seconds()) <= 72*3600:
            pairs.append((round(float(S[i, j]), 3), rows[i][0], rows[i][1], rows[i][3][:70], rows[j][0], rows[j][1], rows[j][3][:70]))
pairs.sort(reverse=True)
print(len(pairs), "pairs")
for p in pairs[:25]: print("  ", p)
print("== unclustered items similar (>=0.80) to an item in an event (missed attachments)")
ev_rows = q("select r.id, s.name, r.title, r.embedding, ei.event_id from raw_items r join sources s on s.id=r.source_id join event_items ei on ei.item_id=r.id")
E = np.stack([np.frombuffer(r[3], dtype=np.float32) for r in ev_rows]); E = E / np.linalg.norm(E, axis=1, keepdims=True)
T = V @ E.T
miss = []
for i in range(len(rows)):
    j = int(T[i].argmax())
    if T[i, j] >= THR: miss.append((round(float(T[i, j]), 3), rows[i][0], rows[i][1], rows[i][3][:70], "E%d" % ev_rows[j][4], ev_rows[j][2][:60]))
miss.sort(reverse=True); print(len(miss))
for m_ in miss[:20]: print("  ", m_)
