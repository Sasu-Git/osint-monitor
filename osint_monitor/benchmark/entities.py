"""Entity benchmark on the frozen gold set (evaluations/entities/gold/).

Measures, separately and per language (en / it / es):

- NER detection precision / recall   -- mentions the pipeline extracts from each item's headline and lead;
- entity typing accuracy             -- detected mentions whose type is one the gold allows;
- canonical resolution accuracy      -- detected mentions the resolver maps to the gold identity, against a
                                        temporary copy of the frozen entity tables (their learned aliases
                                        included), plus canonical-name hygiene;
- principal-actor precision / recall -- per Development;
- actor-role accuracy                -- per gold role entry.

No composite score. Every unit outcome is kept so two runs can be diffed (errors fixed / introduced, with the
Developments affected). Production entry points are called, never re-implemented here: NER through
``nlp.extract_mentions``, resolution through ``EntityResolver``, principals and roles through
``principals.development_actors``.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import yaml

GOLD_DIR = Path(__file__).resolve().parents[2] / "evaluations" / "entities" / "gold"
LANGS = ("en", "it", "es")
ROLES = ("actor", "participant", "target", "affected", "institutional_context", "subject", "location")


# --- gold ------------------------------------------------------------------------------------------

@dataclass
class GoldMention:
    surface: str
    types: tuple[str, ...]
    canonical: str
    optional: bool


@dataclass
class GoldDevelopment:
    key: str
    ref: str
    db: str
    items: list[dict]                               # id, source, lang, title, lead
    mentions: dict[int, list[GoldMention]]
    roles: dict[str, str]
    principals: list[tuple[str, ...]]               # alternatives per principal

    @property
    def lang(self) -> str:
        langs = {_lang(i["lang"]) for i in self.items}
        return langs.pop() if len(langs) == 1 else "+".join(sorted(langs))


def _lang(value: str) -> str:
    return (value or "en").split()[0]


def verify(root: Path = GOLD_DIR) -> dict:
    manifest = yaml.safe_load((root / "manifest.yaml").read_text(encoding="utf-8"))
    for name, digest in manifest["sha256"].items():
        actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
        if actual != digest:
            raise ValueError(f"{root / name} changed since it was frozen ({actual} != {digest})")
    return manifest


def load_gold(root: Path = GOLD_DIR) -> tuple[list[GoldDevelopment], dict[str, set[str]]]:
    verify(root)
    gold = yaml.safe_load((root / "gold.yaml").read_text(encoding="utf-8"))
    items = json.loads((root / "items.json").read_text(encoding="utf-8"))
    names = {c: {norm(n) for n in [c, *aliases]} for c, aliases in gold["canonical_names"].items()}
    out = []
    for key, g in gold["developments"].items():
        mentions = {}
        for item_id, text in g["items"].items():
            parsed = []
            for entry in text.split("; "):
                optional = entry.startswith("? ")
                surface, types, canonical = (x.strip() for x in entry.removeprefix("? ").split(" | "))
                parsed.append(GoldMention(surface, tuple(types.split("/")), canonical, optional))
            mentions[int(item_id)] = parsed
        out.append(GoldDevelopment(key, g["ref"], items[key]["db"], items[key]["items"], mentions, g.get("roles") or {},
                                   [tuple(p.split("|")) for p in g.get("principals") or []]))
    return out, names


# --- comparison helpers ---------------------------------------------------------------------------

_SPACE = re.compile(r"\s+")


def norm(text: str) -> str:
    """Comparison form of a surface: HTML entities, quotes/dashes, articles, possessives, case, spaces."""
    t = html.unescape(text or "").replace("⁠", "").replace("​", "")
    t = t.replace("’", "'").replace("‘", "'").replace("–", "-").replace("—", "-")
    t = re.sub(r"'s?$", "", t.strip())
    t = re.sub(r"^(the|a|an|la|el|il|lo|los|las|le|gli|i)\s+", "", t.strip(), flags=re.I)
    return _SPACE.sub(" ", t).strip(" .,:;\"'").lower()


def same_identity(predicted: str | None, canonical: str, names: dict[str, set[str]]) -> bool:
    if not predicted:
        return False
    accepted = names.get(canonical, {norm(canonical)})
    return norm(predicted) in accepted


def clean_canonical(name: str) -> bool:
    """Canonical-name hygiene: no HTML entity, leading article, possessive, glued text or stray punctuation."""
    return not (re.search(r"&#?\w+;", name) or re.match(r"^(the|a|an)\s", name, re.I) or re.search(r"['’]s?$", name)
                or re.search(r"[a-z][A-Z][a-z]", name) or re.search(r"[\s,;:]$|^\W", name) or "\n" in name)


def _match(gold: list[GoldMention], predicted: list[tuple[str, str]]) -> tuple[dict[int, int], list[int]]:
    """Gold index -> predicted index (one-to-one), and unmatched predicted indexes. Exact comparison form
    first, then containment on word boundaries with at most two extra words ("north Gaza" / "Gaza"), so a
    clause-length span does not count as detecting a name inside it."""
    pairs: dict[int, int] = {}
    free = set(range(len(predicted)))
    for exact in (True, False):
        for gi, g in enumerate(gold):
            if gi in pairs:
                continue
            gn = norm(g.surface)
            for pi in sorted(free):
                pn = norm(predicted[pi][0])
                if exact:
                    ok = pn == gn
                else:
                    ok = bool(pn and gn and abs(len(pn.split()) - len(gn.split())) <= 2
                              and (re.search(rf"\b{re.escape(gn)}\b", pn) or re.search(rf"\b{re.escape(pn)}\b", gn)))
                if ok:
                    pairs[gi] = pi
                    free.discard(pi)
                    break
    return pairs, sorted(free)


# --- the run --------------------------------------------------------------------------------------

@dataclass
class Tally:
    hit: int = 0
    total: int = 0

    def add(self, ok: bool) -> None:
        self.total += 1
        self.hit += bool(ok)

    def rate(self) -> float | None:
        return self.hit / self.total if self.total else None


@dataclass
class RunResult:
    units: dict[str, dict] = field(default_factory=dict)     # unit id -> {metric, lang, dev, ok, detail}
    tallies: dict[str, dict[str, Tally]] = field(default_factory=lambda: defaultdict(lambda: defaultdict(Tally)))
    predictions: dict = field(default_factory=dict)

    def record(self, metric: str, unit: str, lang: str, dev: str, ok: bool, detail: str) -> None:
        self.units[f"{metric}:{unit}"] = {"metric": metric, "lang": lang, "dev": dev, "ok": bool(ok), "detail": detail}
        for key in (lang, "all"):
            self.tallies[metric][key].add(ok)


def _resolver_sessions(tmp: Path, root: Path):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from osint_monitor.core.database import Base, Entity
    sessions = {}
    for db in ("en", "ml"):
        engine = create_engine(f"sqlite:///{tmp / f'entities-{db}.db'}")
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)()
        for row in json.loads((root / f"entities-{db}.json").read_text(encoding="utf-8")):
            session.add(Entity(id=row["id"], canonical_name=row["canonical_name"], entity_type=row["entity_type"],
                               aliases=row["aliases"]))
        session.commit()
        sessions[db] = session
    return sessions


def predict(root: Path = GOLD_DIR) -> dict:
    """Run the production entry points on the frozen items. Returns every prediction (no scoring)."""
    from osint_monitor.core.models import EntityType, ExtractedEntity
    from osint_monitor.processors import principals as P
    from osint_monitor.processors.entity_resolver import EntityResolver
    from osint_monitor.processors.nlp import extract_mentions

    devs, _ = load_gold(root)
    out: dict = {}
    with tempfile.TemporaryDirectory(prefix="osint-entity-bench-") as tmp:
        sessions = _resolver_sessions(Path(tmp), root)
        resolvers = {db: EntityResolver(s) for db, s in sessions.items()}
        for dev in devs:
            resolver = resolvers[dev.db]
            items = {}
            for item in dev.items:
                lang = _lang(item["lang"])
                mentions = []
                for field_name in ("title", "lead"):
                    for m in extract_mentions(item[field_name] or "", lang):
                        try:
                            etype = EntityType(m.entity_type.value)
                        except ValueError:
                            etype = EntityType.ORG
                        entity = resolver.resolve(ExtractedEntity(text=m.text, entity_type=etype,
                                                                  canonical_name=m.canonical_name))
                        mentions.append({"field": field_name, "text": m.text, "type": m.entity_type.value,
                                         "canonical": entity.canonical_name if entity else None,
                                         "method": getattr(resolver, "last_method", None),
                                         "evidence": getattr(resolver, "last_evidence", None)})
                items[str(item["id"])] = mentions
            sessions[dev.db].commit()
            actors = P.development_actors([{"title": i["title"] or "", "lead": i["lead"] or "", "lang": _lang(i["lang"]),
                                            "source": i["source"]} for i in dev.items])
            out[dev.key] = {"items": items, "principals": sorted(actors.principals), "roles": dict(actors.roles)}
        for s in sessions.values():
            engine = s.get_bind()
            s.close()
            engine.dispose()
    return out


def score(predictions: dict, root: Path = GOLD_DIR) -> RunResult:
    devs, names = load_gold(root)
    result = RunResult(predictions=predictions)
    for dev in devs:
        p = predictions[dev.key]
        for item in dev.items:
            lang = _lang(item["lang"])
            mentions = p["items"][str(item["id"])]
            predicted = [(m["text"], m["type"]) for m in mentions]
            gold = dev.mentions[item["id"]]
            pairs, _ = _match(gold, predicted)
            for gi, g in enumerate(gold):
                if g.optional:
                    continue
                unit = f"{dev.key}:{item['id']}:{gi}:{g.surface}"
                pi = pairs.get(gi)
                result.record("ner_recall", unit, lang, dev.key, pi is not None,
                              f"'{g.surface}'" + (f" <- '{predicted[pi][0]}'" if pi is not None else " missed"))
                if pi is None:
                    continue
                m = mentions[pi]
                result.record("typing", unit, lang, dev.key, m["type"] in g.types,
                              f"'{g.surface}' {m['type']} (gold {'/'.join(g.types)})")
                result.record("resolution", unit, lang, dev.key, same_identity(m["canonical"], g.canonical, names),
                              f"'{m['text']}' -> '{m['canonical']}' [{m['method'] or '-'}] (gold {g.canonical})")
                if m["canonical"]:
                    result.record("canonical_hygiene", unit, lang, dev.key, clean_canonical(m["canonical"]),
                                  f"canonical '{m['canonical']}'")
            matched = set(pairs.values())
            optional = {pi for gi, pi in pairs.items() if gold[gi].optional}
            for pi, (surface, ptype) in enumerate(predicted):
                if pi in optional:
                    continue
                result.record("ner_precision", f"{dev.key}:{item['id']}:p{pi}:{surface}", lang, dev.key, pi in matched,
                              f"'{surface}' {ptype}" + ("" if pi in matched else " (not in gold)"))
        matched_gold = set()
        for name in p["principals"]:
            hit = next((n for n, alts in enumerate(dev.principals) if n not in matched_gold
                        and any(same_identity(name, a, names) for a in alts)), None)
            if hit is not None:
                matched_gold.add(hit)
            result.record("principal_precision", f"{dev.key}:{name}", dev.lang, dev.key, hit is not None,
                          f"predicted '{name}'" + ("" if hit is not None else " (not a gold principal)"))
        for n, alts in enumerate(dev.principals):
            result.record("principal_recall", f"{dev.key}:{alts[0]}", dev.lang, dev.key, n in matched_gold,
                          f"gold '{'|'.join(alts)}'" + ("" if n in matched_gold else f" missed (predicted {p['principals']})"))
        for canonical, role in dev.roles.items():
            got = next((r for name, r in p["roles"].items() if same_identity(name, canonical, names)), None)
            result.record("actor_role", f"{dev.key}:{canonical}", dev.lang, dev.key, got == role,
                          f"{canonical}: {got} (gold {role})")
    return result


def run(root: Path = GOLD_DIR) -> RunResult:
    return score(predict(root), root)


# --- reporting ------------------------------------------------------------------------------------

METRICS = [("ner_precision", "NER detection precision"), ("ner_recall", "NER detection recall"),
           ("typing", "Entity typing accuracy"), ("resolution", "Canonical resolution accuracy"),
           ("canonical_hygiene", "Canonical-name hygiene"), ("principal_precision", "Principal-actor precision"),
           ("principal_recall", "Principal-actor recall"), ("actor_role", "Actor-role accuracy")]


def summary(result: RunResult) -> dict:
    out = {}
    for metric, _ in METRICS:
        t = result.tallies.get(metric, {})
        out[metric] = {k: {"hit": v.hit, "total": v.total} for k, v in sorted(t.items())}
    return out


def _fmt(t: dict | None) -> str:
    if not t or not t["total"]:
        return "-"
    return f"{t['hit'] / t['total']:.0%} ({t['hit']}/{t['total']})"


def format_summary(s: dict) -> str:
    langs = sorted({k for m in s.values() for k in m if k != "all"}, key=lambda x: (x not in LANGS, x))
    lines = ["| Metric | all | " + " | ".join(langs) + " |", "|---|---:|" + "---:|" * len(langs)]
    for metric, label in METRICS:
        row = s.get(metric, {})
        lines.append(f"| {label} | {_fmt(row.get('all'))} | " + " | ".join(_fmt(row.get(l)) for l in langs) + " |")
    return "\n".join(lines)


def to_json(result: RunResult) -> dict:
    return {"summary": summary(result), "units": result.units, "predictions": result.predictions}


def diff(before: dict, after: dict) -> dict:
    """Per metric: units that went wrong -> right (fixed) and right -> wrong (introduced), with Developments.
    Precision units are predictions: a false positive that disappears is fixed, a new one is introduced."""
    out = {}
    for metric, _ in METRICS:
        fixed, introduced = [], []
        precision = metric in ("ner_precision", "principal_precision")
        for k in sorted(set(before["units"]) | set(after["units"])):
            b, a = before["units"].get(k), after["units"].get(k)
            if (b or a)["metric"] != metric:
                continue
            if b and a:
                if not b["ok"] and a["ok"]:
                    fixed.append(f"{a['dev']} {b['detail']} => {a['detail']}")
                elif b["ok"] and not a["ok"]:
                    introduced.append(f"{a['dev']} {b['detail']} => {a['detail']}")
            elif precision and b and not b["ok"]:
                fixed.append(f"{b['dev']} {b['detail']} (prediction removed)")
            elif precision and a and not a["ok"]:
                introduced.append(f"{a['dev']} {a['detail']} (new prediction)")
        out[metric] = {"fixed": fixed, "introduced": introduced}
    return out


def format_diff(d: dict) -> str:
    lines = []
    for metric, label in METRICS:
        f, i = d[metric]["fixed"], d[metric]["introduced"]
        if not (f or i):
            continue
        devs = sorted({x.split()[0] for x in f + i})
        lines.append(f"**{label}**: {len(f)} fixed, {len(i)} introduced — Developments {', '.join(devs)}")
        lines += [f"  - fixed: {x}" for x in f] + [f"  - introduced: {x}" for x in i]
    return "\n".join(lines) or "no unit changed"
