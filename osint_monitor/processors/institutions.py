"""Institutional hierarchy (config/institutions.yaml): institutions, multilateral organisations and forums
as first-class entities with parents, and context resolution of generic labels ("the Navy", "the Council").

``InstitutionRegistry.lookup(name)`` -> the institution a name denotes (short all-capital aliases match
case-sensitively). ``resolve_generic(label, qualifiers)`` -> the institution a generic label denotes given
the states / organisations the item names or its publisher is (``item_qualifiers``); None when the context
does not identify one. ``parents(canonical)`` -> the chain up to the state or organisation it belongs to.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import yaml

from osint_monitor.core.config import CONFIG_DIR


def _key(name: str) -> str:
    t = "".join(c for c in unicodedata.normalize("NFKD", name or "") if not unicodedata.combining(c))
    t = re.sub(r"^the\s+", "", t.strip(), flags=re.I).replace("’", "'")
    return " ".join(t.lower().split()).strip(" .,")


def _case_sensitive(alias: str) -> bool:
    letters = re.sub(r"[^A-Za-z]", "", alias)
    return len(letters) <= 5 and letters.isupper()


@dataclass(frozen=True)
class Institution:
    canonical: str
    kind: str
    parent: str | None = None
    aliases: tuple[str, ...] = field(default_factory=tuple)


class InstitutionRegistry:
    def __init__(self, institutions: list[Institution], generic: dict[str, dict[str, str]]):
        self.by_name = {i.canonical: i for i in institutions}
        self._exact: dict[str, Institution] = {}          # case-sensitive acronyms
        self._folded: dict[str, Institution] = {}
        for inst in institutions:
            self._folded[_key(inst.canonical)] = inst
            for alias in inst.aliases:
                if _case_sensitive(alias):
                    self._exact[alias.replace(".", "")] = inst
                else:
                    self._folded[_key(alias)] = inst
        self.generic = {_key(label): {_key(q): target for q, target in (m or {}).items()}
                        for label, m in generic.items()}

    @classmethod
    def load(cls, path: Path | None = None) -> "InstitutionRegistry":
        path = path or CONFIG_DIR / "institutions.yaml"
        if not path.exists():
            return cls([], {})
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        items = [Institution(i["canonical"], i.get("kind", "OTHER_ORGANIZATION"), i.get("parent"),
                             tuple(i.get("aliases") or [])) for i in raw.get("institutions", [])]
        return cls(items, raw.get("generic_labels") or {})

    def lookup(self, name: str) -> Institution | None:
        if not name:
            return None
        exact = self._exact.get(name.strip().replace(".", ""))
        if exact:
            return exact
        folded = _key(name)
        if _case_sensitive(name.strip()) and folded not in {_key(i.canonical) for i in self.by_name.values()}:
            return None                                   # "UN" matched above or not at all; never "un"
        return self._folded.get(folded)

    def is_generic(self, name: str) -> bool:
        return _key(name) in self.generic

    def resolve_generic(self, label: str, qualifiers: set[str]) -> Institution | None:
        """The institution a generic label denotes given the item's qualifiers (canonical state or
        organisation names), when exactly one candidate fits."""
        options = self.generic.get(_key(label), {})
        hits = {target for q, target in options.items() if q in {_key(x) for x in qualifiers}}
        return self.by_name.get(hits.pop()) if len(hits) == 1 else None

    def parents(self, canonical: str) -> list[str]:
        out, seen = [], set()
        inst = self.by_name.get(canonical)
        while inst and inst.parent and inst.parent not in seen:
            out.append(inst.parent)
            seen.add(inst.parent)
            inst = self.by_name.get(inst.parent)
        return out

    def top(self, canonical: str) -> str:
        chain = self.parents(canonical)
        return chain[-1] if chain else canonical


@lru_cache(maxsize=1)
def registry() -> InstitutionRegistry:
    return InstitutionRegistry.load()


def item_qualifiers(mentions: list[tuple[str, str]], source_name: str | None = None) -> set[str]:
    """States and organisations an item names (canonical names), plus its publisher's identity and that
    identity's parents: the context a generic label is resolved in. ``mentions``: (text, entity type)."""
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.geography import Gazetteer
    reg = registry()
    geo, actors = _geo_actors()
    out: set[str] = set()
    for text, etype in mentions:
        inst = reg.lookup(text)
        if inst:
            out.add(inst.canonical)
            out.update(reg.parents(inst.canonical))
            continue
        if etype in ("GPE", "NORP", "PERSON", "ORG"):
            key = actors.key(text)                        # "American" -> united states, "Trump" -> united states
            if key and geo.is_country(key):
                out.add(key)
    identity = _source_identity(source_name)
    if identity:
        out.add(identity)
        out.update(reg.parents(identity))
    return out


@lru_cache(maxsize=1)
def _geo_actors():
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.geography import Gazetteer
    return Gazetteer.load(), ActorNormalizer.load()


@lru_cache(maxsize=256)
def _source_identity(source_name: str | None) -> str | None:
    if not source_name:
        return None
    from osint_monitor.core.config import load_sources_config
    feed = next((f for f in load_sources_config().rss_feeds if f.name == source_name), None)
    return (feed.identity or feed.name) if feed else None
