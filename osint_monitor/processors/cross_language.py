"""Cross-language Development links (owner decision, 2026-10-07).

The narrative clusterer embeds with an English-only model, so one occurrence reported in English and in Spanish or
Italian ends up as two Developments (RAF Fairford, the Siberian plague case, the White House AI luncheon). This
stage runs after development segmentation and proposes links between narrative units that share no language. It
uses a multilingual model (``CrossLanguageConfig.model``) **for candidate generation only**:

- A candidate pair is two units with disjoint languages, first reported at most ``max_hours`` apart, whose
  multilingual centroid cosine is at least ``min_cosine``.
- A candidate is **accepted only on explicit anchors** (owner rule P7, applied across languages):
  - no place conflict (the specific places they name are compatible);
  - and at least one of: a shared specific named entity (``development_segmentation._occurrence_anchors``: not a
    state, a leader, an outlet or a generic label); a specific (non-country) place equal to, containing, or
    contained in one on the other side (gazetteer); or a shared number that is not a year.
- **Cosine alone never merges.**

Accepted pairs are returned as item-id links. Clusters carry them (``cluster["xlang_links"]``), so
``development_identity.reconcile`` treats them as links: an item can extend, or help found, a Development in another
language. The independent-origins rule still applies. The model name and revision are recorded in the run ledger
(``core.runs.model_versions``) and in every accepted link's evidence.
"""

from __future__ import annotations

import logging
import re
import threading
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from itertools import combinations
from pathlib import Path

import numpy as np

logger = logging.getLogger(__name__)
_model = None
_model_lock = threading.Lock()
_YEAR = re.compile(r"^(19|20)\d\d$")
_NUMBER = re.compile(r"(?<![\w.,])(\d{1,3}(?:[.,\s]\d{3})+|\d{3,})(?![\w])")


def model_and_revision(name: str):
    """The multilingual SentenceTransformer (offline cache) and its pinned revision (the cache's commit hash)."""
    global _model
    with _model_lock:
        if _model is None:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer(name)
    return _model, revision_of(name)


def revision_of(name: str) -> str | None:
    """The cached model's revision (huggingface hub refs/main), or None when unknown."""
    import os
    hub = Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface")) / "hub"
    ref = hub / ("models--" + name.replace("/", "--")) / "refs" / "main"
    try:
        return ref.read_text(encoding="utf-8").strip()
    except OSError:
        return None


def numbers(text: str) -> set[str]:
    """Numbers of three or more digits, thousands separators removed, years excluded ("16,000" == "16.000"). Shorter
    numbers (ages, counts under 100) recur by coincidence and are not evidence of one occurrence."""
    out = set()
    for m in _NUMBER.finditer(text or ""):
        n = re.sub(r"[.,\s]", "", m.group(1))
        if not _YEAR.match(n):
            out.add(n.lstrip("0") or "0")
    return out


@dataclass
class Unit:
    items: list[int]
    langs: set[str]
    first: datetime | None
    vector: np.ndarray | None = None
    anchors: set[str] = field(default_factory=set)
    places: set[str] = field(default_factory=set)       # specific (non-country) canonical places, gazetteer-known
    numbers: set[str] = field(default_factory=set)


@dataclass
class XLink:
    a: Unit
    b: Unit
    cosine: float
    accepted: bool
    evidence: list[str]


def specific_places_compatible(a: set[str], b: set[str], geo) -> list[str]:
    """Pairs (x, y) of specific places where x is y, contains y or lies inside y."""
    return [f"{x}~{y}" for x in sorted(a) for y in sorted(b) if geo.same_or_contains(x, y)]


@dataclass(frozen=True)
class Guard:
    """Acceptance guard switches (CrossLanguageConfig; the defaults are the original stage) and, for G2, the anchors
    and places that are broad in this run."""
    require_anchor_classes: int = 1
    exact_places: bool = False
    broad_anchors: frozenset = frozenset()
    broad_places: frozenset = frozenset()

    @classmethod
    def of(cls, cl, units: list[Unit] | None = None) -> "Guard":
        broad_a, broad_p = broad_terms(units or [], cl.broad_anchor_units)
        return cls(cl.require_anchor_classes, cl.exact_places, broad_a, broad_p)


def broad_terms(units: list[Unit], k: int | None) -> tuple[frozenset, frozenset]:
    """G2: anchors and places that occur in more than ``k`` units of the run (a storyline, not one occurrence)."""
    if k is None:
        return frozenset(), frozenset()
    anchors, places = Counter(), Counter()
    for u in units:
        anchors.update(u.anchors)
        places.update(u.places)
    return (frozenset(x for x, n in anchors.items() if n > k), frozenset(x for x, n in places.items() if n > k))


def judge(a: Unit, b: Unit, cosine: float, geo, model_tag: str, guard: Guard | None = None) -> XLink:
    g = guard or Guard()
    evidence = [f"multilingual cosine {cosine:.2f} ({model_tag})"]
    # only gazetteer-known places can conflict: multilingual NER emits noisy LOC spans ("gobierno", "regno")
    if a.places and b.places and not specific_places_compatible(a.places, b.places, geo):
        return XLink(a, b, cosine, False, evidence + [f"place conflict {sorted(a.places)} / {sorted(b.places)}"])
    shared_anchor = sorted(a.anchors & b.anchors)
    if g.exact_places:
        shared_place = [f"{x}~{x}" for x in sorted(a.places & b.places)]
    else:
        shared_place = specific_places_compatible(a.places, b.places, geo)
    shared_number = sorted(a.numbers & b.numbers)
    broad = [x for x in shared_anchor if x in g.broad_anchors] + \
            [p for p in shared_place if set(p.split("~")) & g.broad_places]
    shared_anchor = [x for x in shared_anchor if x not in g.broad_anchors]
    shared_place = [p for p in shared_place if not set(p.split("~")) & g.broad_places]
    if shared_anchor:
        evidence.append(f"shared anchors {shared_anchor[:4]}")
    if shared_place:
        evidence.append(f"shared specific places {shared_place[:4]}")
    if shared_number:
        evidence.append(f"shared numbers {shared_number[:4]}")
    if broad:
        evidence.append(f"broad, not decisive {broad[:4]}")
    classes = sum(1 for c in (shared_anchor, shared_place, shared_number) if c)
    if classes and classes < g.require_anchor_classes:
        evidence.append(f"{classes} anchor class(es), {g.require_anchor_classes} required")
    return XLink(a, b, cosine, classes >= max(1, g.require_anchor_classes), evidence)


def build_units(session, groups: list[list[int]], singles: list[int], config) -> list[Unit]:
    """One unit per narrative group and per unclustered narrative item, with its languages, first time, multilingual
    centroid, explicit anchors, specific places and numbers."""
    from osint_monitor.core.database import Entity, ItemEntity, RawItem
    from osint_monitor.processors.development_segmentation import LOCATION_TYPES, _occurrence_anchors, gazetteer
    from osint_monitor.processors.embeddings import headline_only
    from osint_monitor.processors.entity_resolver import normalise
    from osint_monitor.processors.language import item_language

    ids = sorted({i for g in groups for i in g} | set(singles))
    rows = {r.id: r for r in session.query(RawItem).filter(RawItem.id.in_(ids))}
    geo = gazetteer(False)
    anchors, _ = _occurrence_anchors(session, rows, config.development_segmentation) \
        if config.development_segmentation.occurrence_match else ({}, {})
    from osint_monitor.processors.actors import ActorNormalizer
    actors = ActorNormalizer.load()
    places: dict[int, set[str]] = {}
    for item_id, name, etype in (session.query(ItemEntity.item_id, Entity.canonical_name, Entity.entity_type)
                                 .join(Entity, Entity.id == ItemEntity.entity_id)
                                 .filter(ItemEntity.item_id.in_(ids))):
        if etype not in LOCATION_TYPES or not name:
            continue
        place = geo.canonical(normalise(name))
        # specific, known places only: not a country, not unknown to the gazetteer, and not a capital or seat of
        # government that stands for its state ("Brussels", "Tehran", "Kyiv": actors.yaml represents)
        if geo.is_country(place) or place not in geo.known or actors.represents(actors.surface(name) or "") != (actors.surface(name) or ""):
            continue
        places.setdefault(item_id, set()).add(place)
    model, rev = model_and_revision(config.cross_language.model)
    texts = {i: (r.title or "") if headline_only(r.content) else f"{r.title or ''}. {(r.content or '')[:300]}"
             for i, r in rows.items()}
    order = [i for i in ids if i in rows]
    vecs = dict(zip(order, model.encode([texts[i] for i in order], normalize_embeddings=True))) if order else {}
    units = []
    for members in [list(g) for g in groups] + [[i] for i in singles]:
        members = [i for i in members if i in rows]
        if not members:
            continue
        v = np.mean([vecs[i] for i in members], axis=0)
        times = [rows[i].published_at or rows[i].fetched_at for i in members if rows[i].published_at or rows[i].fetched_at]
        units.append(Unit(
            items=members,
            langs={item_language(rows[i].source.name if rows[i].source else "", rows[i].title or "") or "en"
                   for i in members},
            first=min(times) if times else None, vector=v / (np.linalg.norm(v) + 1e-9),
            anchors=set().union(*(anchors.get(i, set()) for i in members)),
            places=set().union(*(places.get(i, set()) for i in members)),
            numbers=set().union(*(numbers(f"{rows[i].title} {(rows[i].content or '')[:300]}") for i in members))))
    return units


def propose(units: list[Unit], config, geo) -> list[XLink]:
    cl = config.cross_language
    tag = f"{cl.model}@{(revision_of(cl.model) or '?')[:8]}"
    guard = Guard.of(cl, units)
    out = []
    for a, b in combinations(units, 2):
        if a.langs & b.langs or a.vector is None or b.vector is None:
            continue
        if a.first and b.first and abs((a.first - b.first).total_seconds()) > cl.max_hours * 3600:
            continue
        cos = float(a.vector @ b.vector)
        if cos >= cl.min_cosine:
            out.append(judge(a, b, cos, geo, tag, guard))
    return out


def link_groups(session, groups: list[list[int]], singles: list[int], config) -> tuple[list[list[int]], dict[int, list]]:
    """Merge units joined by accepted cross-language links. Returns (groups, xlang) where xlang maps an index into
    the returned groups to the accepted item-id link pairs inside it, with their evidence."""
    from osint_monitor.processors.development_segmentation import gazetteer
    units = build_units(session, groups, singles, config)
    links = propose(units, config, gazetteer(False))
    for l in links:
        logger.info("Cross-language %s: %s <-> %s; %s", "LINK" if l.accepted else "candidate rejected",
                    l.a.items[:3], l.b.items[:3], "; ".join(l.evidence))
    return merge_units(units, links, config.cross_language.direct_links_only)


def _cross(a: Unit, b: Unit) -> bool:
    return not (a.langs & b.langs)


def direct_links(units: list[Unit], accepted: list[XLink]) -> list[XLink]:
    """G3: the accepted links that merge units only through direct support. A component of three or more units is
    kept whole when every cross-language unit pair in it has an accepted link; otherwise its links are reconsidered
    in descending cosine order and a link is kept only if every cross-language pair of the component it creates is
    still directly linked (plan amendment 1)."""
    index = {id(u): n for n, u in enumerate(units)}
    linked = {frozenset((index[id(l.a)], index[id(l.b)])) for l in accepted}

    def clique(members: set[int]) -> bool:
        return all(frozenset((x, y)) in linked for x, y in combinations(sorted(members), 2)
                   if _cross(units[x], units[y]))

    comp_of: dict[int, set[int]] = {}
    for l in accepted:                                      # components of the accepted links
        x, y = index[id(l.a)], index[id(l.b)]
        merged = comp_of.get(x, {x}) | comp_of.get(y, {y})
        for m in merged:
            comp_of[m] = merged
    kept: list[XLink] = []
    whole = {frozenset(c) for c in comp_of.values() if clique(c)}
    current: dict[int, set[int]] = {}
    for l in sorted(accepted, key=lambda l: (-l.cosine, index[id(l.a)], index[id(l.b)])):
        x, y = index[id(l.a)], index[id(l.b)]
        if frozenset(comp_of[x]) in whole:
            kept.append(l)
            continue
        merged = current.get(x, {x}) | current.get(y, {y})
        if clique(merged):
            for m in merged:
                current[m] = merged
            kept.append(l)
    order = {id(l): n for n, l in enumerate(accepted)}
    return sorted(kept, key=lambda l: order[id(l)])


def merge_units(units: list[Unit], links: list[XLink], direct_only: bool = False
                ) -> tuple[list[list[int]], dict[int, list]]:
    """Merge units joined by accepted links (G3: direct links only). Returns (groups, xlang) as ``link_groups``."""
    parent = list(range(len(units)))
    index = {id(u): n for n, u in enumerate(units)}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    accepted = [l for l in links if l.accepted]
    if direct_only:
        accepted = direct_links(units, accepted)
    for l in accepted:
        parent[find(index[id(l.a)])] = find(index[id(l.b)])
    merged: dict[int, list[int]] = {}
    for n, u in enumerate(units):
        merged.setdefault(find(n), []).extend(u.items)
    out_groups, xlang = [], {}
    pairs_by_root: dict[int, list] = {}
    for l in accepted:
        pairs_by_root.setdefault(find(index[id(l.a)]), []).append(
            {"a": l.a.items, "b": l.b.items, "evidence": l.evidence})
    for root, items in merged.items():
        if len(items) < 2 and root not in pairs_by_root:
            continue                                    # a lone unclustered item stays unclustered
        out_groups.append(sorted(set(items)))
        if root in pairs_by_root:
            xlang[len(out_groups) - 1] = pairs_by_root[root]
    return out_groups, xlang


def linked_pairs(xlang_entries: list[dict]) -> set[tuple[int, int]]:
    """Every item pair across an accepted cross-language link (a < b)."""
    out = set()
    for e in xlang_entries or []:
        for i in e["a"]:
            for j in e["b"]:
                out.add((min(i, j), max(i, j)))
    return out
