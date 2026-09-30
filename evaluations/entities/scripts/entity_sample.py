"""Entity review sample: real Developments, current main NER / resolution / principal logic,
recomputed on working copies of evaluation data. Read-only with respect to entity logic."""
import hashlib, json, re, sqlite3, sys
from collections import Counter, defaultdict

from rapidfuzz import fuzz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload

from osint_monitor.core.config import load_entities_config, load_event_grouping_config, load_sources_config
from osint_monitor.core.database import Entity, Event, EventEntity, EventItem, ItemEntity, RawItem
from osint_monitor.processors.actors import ActorNormalizer
from osint_monitor.processors.entity_resolver import (
    FUZZY_THRESHOLD_CROSS_TYPE, FUZZY_THRESHOLD_SAME_TYPE, correct_entity_type, normalise,
)
from osint_monitor.processors.event_grouping import NARRATIVE, source_class
from osint_monitor.processors.geography import Gazetteer
from osint_monitor.processors.nlp import SPACY_LABEL_MAP, get_nlp
from osint_monitor.processors.principals import _lead, item_candidates, item_evidence, select_principals
from osint_monitor.core.models import EntityType

SEED = "entity-review-2026-09-30"
DBS = {"en": "data/eval/entity-review-en.db", "ml": "data/eval/entity-review-ml.db"}
DOMAINS = ["diplomacy", "military", "security", "political", "economic", "humanitarian", "institutional"]
# Classifier never assigns these two in the data: sampled from domain "unknown" by source role / headline words
FALLBACK = {
    "humanitarian": (re.compile(r"refugee|displac|famine|humanitarian|aid\b|relief|hunger|migrant|evacuat|"
                                r"rifugiat|profughi|desplazad|ayuda", re.I), {"UN News", "UN Press"}),
    "institutional": (re.compile(r"court|tribunal|\bUN\b|United Nations|Security Council|General Assembly|NATO|"
                                 r"\bEU\b|Commission|Council|Parliament|central bank|ECB|IMF|WTO|Corte|Tribunal", re.I),
                      {"ECB Press", "European Commission Press", "Council of the EU Press", "European Parliament Press",
                       "BIS Press", "Federal Reserve Press", "UN Press"}),
}
LOCATION_TYPES = {"GPE", "LOC", "FAC", "FACILITY"}
ACTOR_NER = {"PERSON", "ORG", "NORP", "GPE"}

feeds = {f.name: f for f in load_sources_config().rss_feeds}
grouping = load_event_grouping_config()
seeded = {normalise(e.canonical_name) for e in load_entities_config()} | {
    normalise(a) for e in load_entities_config() for a in e.aliases}
nlp = get_nlp()
normalizer = ActorNormalizer.load()
geo = Gazetteer.load()


def lang_of(source):
    return feeds[source].language if source in feeds and feeds[source].language else "en (assumed)"


def order_key(db, eid):
    return hashlib.sha1(f"{SEED}:{db}:{eid}".encode()).hexdigest()


def explain_resolution(session, mention, etype, linked):
    """Replay EntityResolver.resolve steps read-only, against the entity table of the copy."""
    try:
        corrected = correct_entity_type(mention, EntityType(etype)).value
    except ValueError:
        corrected = etype
    low, norm = mention.strip().lower(), normalise(mention)
    ent = linked
    names = [ent.canonical_name, *(ent.aliases or [])] if ent else []
    if ent and normalise(ent.canonical_name) == norm and norm not in seeded and len(names) <= 2:
        return "new entity", "no existing match: the mention created this entity"
    if ent and any(n.lower() == low for n in names):
        how = "seeded (entities.yaml)" if norm in seeded else "exact alias"
        return how, f"'{mention}' is a recorded name of '{ent.canonical_name}'"
    if ent and any(normalise(n) == norm for n in names):
        return "normalised alias", f"normalised '{norm}' matches '{ent.canonical_name}'"
    best = max(((fuzz.ratio(norm, normalise(n)), n) for n in names), default=(0, ""))
    thr = FUZZY_THRESHOLD_SAME_TYPE if ent and ent.entity_type == corrected else FUZZY_THRESHOLD_CROSS_TYPE
    return "fuzzy", f"best alias '{best[1]}' scored {best[0]:.0f} (threshold {thr})"


def flags_for(ev):
    """Automatic suspicion flags (for review only)."""
    out = []
    keys = ev["principals"]["final"]
    for k in keys:
        if geo.is_subnational(k):
            out.append(("location/actor confusion", f"principal '{k}' is a sub-national place"))
    surfaces = {s for k in keys for s in ev["principals"]["surfaces"].get(k, [])}
    for s in surfaces:
        if normalizer.is_media(s):
            out.append(("contextual organisation", f"principal surface '{s}' is a media outlet"))
        if geo.is_subnational(s) and normalizer.key(s) not in (None, s):
            out.append(("capital -> state mapping", f"'{s}' (a place) stands for '{normalizer.key(s)}'"))
    canon = defaultdict(set)
    for r in ev["resolution"]:
        k = normalizer.surface(r["canonical"] or "") or normalise(r["canonical"] or "")
        canon[k].add(r["canonical"])
        m = r["mention"]
        if m != m.strip() or re.match(r"^(the|a|an)\s", m, re.I) or re.search(r"['’]s$|[\"“”:;,.]$", m) or len(m.split()) > 5:
            out.append(("malformed NER span", f"'{m}'"))
        if r["method"] == "fuzzy":
            out.append(("alias resolution", f"'{m}' -> '{r['canonical']}' by fuzzy match ({r['reason']})"))
        if r["type"] in ("PERSON", "ORG") and (geo.is_country(m) or geo.is_subnational(m)):
            out.append(("entity typing", f"'{m}' typed {r['type']} but is a known place"))
        if r["type"] in LOCATION_TYPES and normalizer.is_media(m):
            out.append(("entity typing", f"'{m}' typed {r['type']} but is a media outlet"))
    for k, names in canon.items():
        if len({n for n in names if n}) > 1:
            out.append(("duplicate canonical identity", f"{sorted(names)} fold to '{k}'"))
    for k in keys:
        for s in ev["principals"]["surfaces"].get(k, []):
            if s == k and not geo.is_country(k) and any(r["canonical"] and normalise(r["canonical"]) == s and
                                                        r["type"] == "PERSON" for r in ev["resolution"]):
                out.append(("person -> state/institution mapping", f"person '{s}' is not mapped to a state or body"))
    if any(i["lang"] in ("it", "es") for i in ev["items"]):
        missed = [n for n in ev["ner"] if n["label"] not in SPACY_LABEL_MAP]
        weird = [n for n in ev["ner"] if n["label"] in ("PERSON", "ORG") and len(n["text"]) <= 3]
        out.append(("multilingual", f"{', '.join(sorted({i['lang'] for i in ev['items']}))} text parsed by the English NER model"
                                    + (f"; short {len(weird)} PERSON/ORG spans" if weird else "")))
    rej = [c for c in ev["principals"]["candidates"] if c["rejected"]]
    if not keys:
        out.append(("principal-selection failure", "no principal actor selected"))
    return out


def build(db, event_id, session):
    e = session.get(Event, event_id)
    rows = (session.query(RawItem).options(joinedload(RawItem.source)).join(EventItem, EventItem.item_id == RawItem.id)
            .filter(EventItem.event_id == event_id).order_by(RawItem.published_at).all())
    ev = {"db": db, "id": event_id, "domain": e.event_domain, "type": e.event_type, "headline": e.summary,
          "items": [], "ner": [], "resolution": [], "principals": {}, "geography": [], "downstream": []}
    evidence, candidates = [], []
    for r in rows:
        src = r.source.name if r.source else "?"
        lead = _lead(r.content)
        ev["items"].append({"id": r.id, "source": src, "lang": lang_of(src), "published": str(r.published_at or r.fetched_at)[:16],
                            "title": r.title, "lead": lead})
        text = f"{r.title or ''}\n{(r.content or '')[:600]}"
        doc = nlp(text)
        for ent in doc.ents:
            ev["ner"].append({"item": r.id, "text": ent.text, "label": ent.label_, "kept": ent.label_ in SPACY_LABEL_MAP,
                              "sentence": " ".join(ent.sent.text.split())[:160]})
        cands = item_candidates(nlp, r.title or "", lead, normalizer)
        for c in cands:
            surface = normalizer.surface(c.text)
            candidates.append({"item": r.id, "text": c.text, "field": c.field, "participant": c.participant,
                               "rejected": c.rejected or ("" if c.participant else "topic / not a participant"),
                               "surface": surface, "key": normalizer.represents(surface) if surface else None,
                               "non_actor": surface is None})
        evidence.append(item_evidence(cands, normalizer))
        for ie in session.query(ItemEntity).options(joinedload(ItemEntity.entity)).filter(ItemEntity.item_id == r.id):
            ent = ie.entity
            method, reason = explain_resolution(session, ie.span_text or ent.canonical_name, ent.entity_type, ent)
            ev["resolution"].append({"item": r.id, "mention": ie.span_text or ent.canonical_name, "type": ent.entity_type,
                                     "canonical": ent.canonical_name, "entity_id": ent.id, "method": method,
                                     "reason": reason})
        stored = {normalise(x["mention"]) for x in ev["resolution"] if x["item"] == r.id}
        for n in ev["ner"]:
            if n["item"] == r.id and n["kept"] and normalise(n["text"]) not in stored:
                ev["resolution"].append({"item": r.id, "mention": n["text"], "type": SPACY_LABEL_MAP[n["label"]].value,
                                         "canonical": None, "entity_id": None, "method": "unresolved",
                                         "reason": "detected now but no stored entity link for this item"})
    sel = select_principals(evidence)
    principal_links = {ee.entity_id for ee in session.query(EventEntity).filter(EventEntity.event_id == event_id,
                                                                                EventEntity.is_principal.is_(True))}
    ev["principals"] = {"candidates": candidates, "support": {k: round(v, 2) for k, v in sel.support.items()},
                        "required": sel.required, "final": sorted(sel.keys),
                        "surfaces": {k: sorted(v) for k, v in sel.surfaces.items()},
                        "principal_entities": sorted({x["canonical"] for x in ev["resolution"]
                                                      if x["entity_id"] in principal_links})}
    participant_keys = {c["key"] for c in candidates if c["participant"] and c["key"]}
    seen = set()
    for x in ev["resolution"]:
        if x["type"] in LOCATION_TYPES and x["mention"] not in seen:
            seen.add(x["mention"])
            canon = geo.canonical(x["mention"])
            ev["geography"].append({"mention": x["mention"], "canonical": canon,
                                    "level": "country" if geo.is_country(canon) else "sub-national" if geo.is_subnational(canon)
                                    else "not in gazetteer",
                                    "contained_in": sorted(geo.ancestors(canon) - {canon}),
                                    "as_actor": (normalizer.key(x["mention"]) in participant_keys) if normalizer.key(x["mention"]) else False})
    no_principals = not principal_links
    for x in {r["canonical"]: r for r in ev["resolution"] if r["canonical"]}.values():
        is_p = x["entity_id"] in principal_links
        is_actor = x["type"] in ACTOR_NER
        ev["downstream"].append({"entity": x["canonical"], "type": x["type"], "principal": is_p,
                                 "clustering": x["type"] in LOCATION_TYPES,
                                 "situation": is_p or (no_principals and is_actor),
                                 "ranking": is_p, "provenance": False,
                                 "ui": is_p or (no_principals and is_actor)})
    ev["flags"] = flags_for(ev)
    return ev


samples = []
pools = defaultdict(list)
for db, path in DBS.items():
    engine = create_engine(f"sqlite:///{path}")
    session = sessionmaker(bind=engine)()
    for e in session.query(Event).all():
        items = (session.query(RawItem).options(joinedload(RawItem.source)).join(EventItem, EventItem.item_id == RawItem.id)
                 .filter(EventItem.event_id == e.id).all())
        if not items or any(source_class(i.source.name, i.source.type, grouping) != NARRATIVE for i in items):
            continue
        srcs = sorted({i.source.name for i in items})
        dom = e.event_domain or "unknown"
        if dom == "unknown":
            text = " ".join(i.title or "" for i in items)
            for fb, (rx, fb_sources) in FALLBACK.items():
                if set(srcs) & fb_sources or rx.search(text):
                    pools[fb].append((db, e.id, srcs, True))
        else:
            pools[dom].append((db, e.id, srcs, False))
    session.close()

sessions = {db: sessionmaker(bind=create_engine(f"sqlite:///{p}"))() for db, p in DBS.items()}
for dom in sorted(DOMAINS, key=lambda d: len(pools[d])):      # scarcest domain first: a shared event goes there
    taken = {(x["db"], x["id"]) for x in samples}
    pool = sorted((p for p in pools[dom] if (p[0], p[1]) not in taken), key=lambda x: order_key(x[0], x[1]))
    built = {}
    def ev_of(p):
        if (p[0], p[1]) not in built:
            built[(p[0], p[1])] = build(p[0], p[1], sessions[p[0]])
        return built[(p[0], p[1])]
    chosen, seen_sources = [], set()
    ml_first = [p for p in pool if p[0] == "ml"]
    if ml_first:
        chosen.append(ml_first[0]); seen_sources |= set(ml_first[0][2])
    while len(chosen) < min(3, len(pool)):
        rest = [p for p in pool if p not in chosen]
        best = max(rest, key=lambda p: (len(set(p[2]) - seen_sources), -rest.index(p)))
        chosen.append(best); seen_sources |= set(best[2])
    flagged = [p for p in pool if p not in chosen and any(f[0] not in ("multilingual",) for f in ev_of(p)["flags"])]
    if len(pool) > len(chosen) and not any(any(f[0] != "multilingual" for f in ev_of(p)["flags"]) for p in chosen) and flagged:
        chosen.append(flagged[0])
    elif len(pool) > len(chosen):
        rest = [p for p in pool if p not in chosen]
        chosen.append(max(rest, key=lambda p: (len(set(p[2]) - seen_sources), -rest.index(p))))
    for p in chosen:
        ev = ev_of(p)
        ev["sampled_as"] = dom
        ev["sampled_by_fallback"] = p[3]
        samples.append(ev)
    print(dom, "pool", len(pool), "chosen", [(p[0], p[1]) for p in chosen])
json.dump(samples, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)
