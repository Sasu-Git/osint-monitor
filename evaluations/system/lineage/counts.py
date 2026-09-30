import sqlite3, sys, json
from collections import Counter
db = sys.argv[1]
c = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
q = lambda s, *a: c.execute(s, a).fetchall()
print("sources:"); 
for r in q("select s.id,s.name,s.type,s.category,s.credibility_score,count(r.id),min(r.published_at),max(r.published_at),sum(r.published_at is null),min(r.fetched_at),max(r.fetched_at) from sources s left join raw_items r on r.source_id=s.id group by s.id order by count(r.id) desc"): print(' ',r)
print("items with source_id not in sources:", q("select count(*) from raw_items where source_id not in (select id from sources)"))
print("null published_at:", q("select count(*) from raw_items where published_at is null"))
print("published_at > fetched_at (+1h):", q("select count(*) from raw_items where published_at > datetime(fetched_at,'+1 hour')"))
print("published_at in future vs max fetched:", q("select id,title,published_at,fetched_at from raw_items where published_at > (select max(fetched_at) from raw_items)"))
print("null/empty url:", q("select count(*) from raw_items where url is null or url=''"))
print("dup content_hash groups:", q("select count(*),sum(n) from (select content_hash,count(*) n from raw_items group by content_hash having n>1)"))
print("dup url groups:", q("select count(*),sum(n) from (select url,count(*) n from raw_items where url is not null and url<>'' group by url having n>1)"))
print("dup lower(title) groups:", q("select count(*),sum(n) from (select lower(trim(title)) t,count(*) n from raw_items group by t having n>1)"))
print("items in >1 event:", q("select count(*) from (select item_id from event_items group by item_id having count(distinct event_id)>1)"))
print("dup event_items rows:", q("select count(*) from (select event_id,item_id from event_items group by 1,2 having count(*)>1)"))
print("items processed:", q("select count(*),sum(processed_at is not null),sum(embedding is not null) from raw_items"))
print("items in any event:", q("select count(distinct item_id) from event_items"))
ev = q("select e.id,count(ei.item_id),count(distinct r.source_id),e.source_count from events e left join event_items ei on ei.event_id=e.id left join raw_items r on r.id=ei.item_id group by e.id")
print("events:", len(ev))
print("by n_items:", sorted(Counter(r[1] for r in ev).items()))
print("by n_distinct_sources:", sorted(Counter(r[2] for r in ev).items()))
print("source_count != distinct sources:", [(r[0],r[2],r[3]) for r in ev if r[2]!=r[3]][:30], sum(r[2]!=r[3] for r in ev))
pr = q("select count(distinct event_id) from event_entities where is_principal=1")[0][0]
print("events with principals:", pr, f"{100*pr/len(ev):.1f}%")
st = q("select count(*) from events where situation_id is not null")[0][0]
print("events with situation:", st, f"{100*st/len(ev):.1f}%")
print("corroboration_level:", q("select corroboration_level,count(*) from events group by 1"))
print("admiralty:", q("select admiralty_rating,count(*) from events group by 1"))
print("confidence_class:", q("select confidence_class,count(*) from events group by 1"))
print("significance_class:", q("select significance_class,count(*) from events group by 1"))
print("event_domain:", q("select event_domain,count(*) from events group by 1"))
print("classification_source:", q("select classification_source,count(*) from events group by 1"))
print("ranked:", q("select count(*),sum(rank_score is not null),min(ranked_at),max(ranked_at) from events"))
print("first>last:", q("select id,first_reported_at,last_updated_at from events where first_reported_at>last_updated_at"))
# compare event timestamps with member item timestamps
bad=[]
for eid,fr,lu in q("select id,first_reported_at,last_updated_at from events"):
    mn,mx,mf = q("select min(coalesce(r.published_at,r.fetched_at)),max(coalesce(r.published_at,r.fetched_at)),max(r.fetched_at) from event_items ei join raw_items r on r.id=ei.item_id where ei.event_id=?",eid)[0]
    if mn and (fr[:16]!=mn[:16] or lu[:16] not in (mx[:16], (mf or '')[:16])):
        bad.append((eid,fr,mn,lu,mx,mf))
print("event ts vs items mismatches:",len(bad)); [print('  ',b) for b in bad[:25]]
print("situations:"); [print(' ',r) for r in q("select s.id,s.slug,s.title,s.status,s.region,s.primary_actors,s.created_at,s.updated_at,(select count(*) from events e where e.situation_id=s.id) from situations s")]
print("alerts types:", q("select alert_type,count(*),sum(event_id is not null),sum(item_id is not null) from alerts group by 1"))
print("claims with event:", q("select count(*),sum(event_id is not null) from claims"))
print("item_entities roles:", q("select role,count(*) from item_entities group by 1"))
print("event_entities roles:", q("select role,count(*),sum(is_principal) from event_entities group by 1"))
print("entity types:", q("select entity_type,count(*) from entities group by 1 order by 2 desc"))
