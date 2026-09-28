"""Canonical actor names and situation slugs.

Automatically created situations are named and keyed only from canonical actor
sets, so "USA / Iran", "Iran / United States" and "Tehran / Washington" all map to
the same slug and cannot become duplicate situations.
"""

from __future__ import annotations

import re
from typing import Iterable

from osint_monitor.processors.entity_resolver import normalise

_NON_SLUG = re.compile(r"[^a-z0-9]+")


class ActorCanonicalizer:
    def __init__(self, aliases: dict[str, str] | None = None, represents: dict[str, str] | None = None):
        self._aliases = {normalise(k): normalise(v) for k, v in (aliases or {}).items()}
        # situations are country-level: a head of state or ministry stands for its state
        self._represents = {normalise(k): normalise(v) for k, v in (represents or {}).items()}
        self._display: dict[str, str] = {}

    def key(self, name: str) -> str:
        """Lowercase canonical key for an actor name."""
        k = normalise(name)
        k = self._aliases.get(k, k)
        return self._represents.get(k, k)

    def keys(self, names: Iterable[str]) -> frozenset[str]:
        return frozenset(k for k in (self.key(n) for n in names) if k)

    def remember(self, name: str) -> None:
        """Record a preferred display spelling (seed names win because they are loaded first)."""
        self._display.setdefault(self.key(name), name.strip())

    def display(self, key: str) -> str:
        return self._display.get(key) or " ".join(w if w.isupper() else w.capitalize() for w in key.split())

    def slug(self, keys: Iterable[str]) -> str:
        return "-".join(_NON_SLUG.sub("-", k).strip("-") for k in sorted(keys))

    def title(self, keys: Iterable[str]) -> str:
        return " – ".join(sorted(self.display(k) for k in keys))
