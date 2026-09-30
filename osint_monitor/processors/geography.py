"""Geographic compatibility: are two place mentions the same place, or one inside the other?

Deterministic, from config/geography.yaml (aliases, containment, directional prefixes).
"Northern Cyprus" and "Cyprus" are compatible (the first is part of the second); so are
"California" and "United States". Two different places in one country are not: Kyiv and
Odesa are different places even though both are in Ukraine. Unknown names only match
themselves after normalisation.

    gazetteer = Gazetteer.load()
    gazetteer.compatible({"northern cyprus"}, {"cyprus"})       # True
    gazetteer.compatible({"kyiv"}, {"khartoum"})                # False
"""

from __future__ import annotations

import html
import unicodedata
import re
from functools import lru_cache
from pathlib import Path

import yaml

from osint_monitor.core.config import CONFIG_DIR

_POSSESSIVE = re.compile(r"(?:'|’)s?$")
_SPACE = re.compile(r"\s+")
_ARTICLE = re.compile(r"^(the|a|an)\s+")


def clean(name: str) -> str:
    """Lower-case, unescape HTML, drop possessives, leading articles and stray punctuation."""
    t = html.unescape(name or "").replace("‌", "").replace(" ", " ")
    t = _SPACE.sub(" ", t.strip().lower())
    t = "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))   # Irán = iran
    t = _POSSESSIVE.sub("", t).strip(" .,;:\"“”'’")
    return _ARTICLE.sub("", t)


class Gazetteer:
    def __init__(self, aliases: dict | None = None, places: dict | None = None, countries: list | None = None,
                 directional_prefixes: list | None = None, region_members: dict | None = None,
                 regions: dict | None = None, use_regions: bool = False):
        self.aliases = {clean(k): clean(v) for k, v in (aliases or {}).items()}
        self.parent = {clean(k): clean(v) for k, v in (places or {}).items()}
        self.prefixes = sorted((clean(p) for p in directional_prefixes or []), key=len, reverse=True)
        self.members: dict[str, set[str]] = {}          # place -> the regions it belongs to
        groups = dict(region_members or {})
        if use_regions:
            groups.update(regions or {})
        for region, members in groups.items():
            for m in members:
                self.members.setdefault(clean(m), set()).add(clean(region))
        self.countries = {clean(c) for c in countries or []}
        self.known = (self.countries | set(self.parent) | set(self.parent.values())
                      | set(self.aliases.values()) | {r for rs in self.members.values() for r in rs})
        self._ancestors = lru_cache(maxsize=None)(self._compute_ancestors)

    @classmethod
    def load(cls, path: Path | None = None, use_regions: bool = False) -> "Gazetteer":
        path = path or CONFIG_DIR / "geography.yaml"
        if not path.exists():
            return cls(use_regions=use_regions)
        with open(path, encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
        return cls(raw.get("aliases"), raw.get("places"), raw.get("countries"), raw.get("directional_prefixes"),
                   raw.get("region_members"), raw.get("regions"), use_regions=use_regions)

    def canonical(self, name: str) -> str:
        """The canonical place for a mention. "northern cyprus" -> "cyprus" when "northern
        cyprus" is not itself listed but "cyprus" is: the mention names a part of Cyprus."""
        t = self.aliases.get(clean(name), clean(name))
        if t in self.known:
            return t
        for p in self.prefixes:
            if t.startswith(p + " "):
                rest = self.aliases.get(t[len(p) + 1:], t[len(p) + 1:])
                if rest in self.known:
                    return rest
        return t

    def _compute_ancestors(self, place: str) -> frozenset[str]:
        out: set[str] = set()
        frontier = [place]
        while frontier:
            p = frontier.pop()
            for up in [self.parent.get(p), *self.members.get(p, ())]:
                if up and up not in out and up != place:
                    out.add(up)
                    frontier.append(up)
        return frozenset(out)

    def ancestors(self, name: str) -> frozenset[str]:
        return self._ancestors(self.canonical(name))

    def same_or_contains(self, a: str, b: str) -> bool:
        a, b = self.canonical(a), self.canonical(b)
        return a == b or a in self._ancestors(b) or b in self._ancestors(a)

    def is_country(self, name: str) -> bool:
        return self.canonical(name) in self.countries

    def is_subnational(self, name: str) -> bool:
        """A known place inside a country (a city, region or territory), not a country."""
        c = self.canonical(name)
        return c not in self.countries and bool(self._ancestors(c) & self.countries)

    def compatible(self, a: set[str], b: set[str]) -> bool:
        """Some place in ``a`` is the same as, contains, or lies inside some place in ``b``."""
        return any(self.same_or_contains(x, y) for x in a for y in b)
