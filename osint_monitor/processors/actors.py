"""Actor normalisation: entity mentions -> canonical actors.

One service, used by principal-actor extraction, situation grouping and ranking, so
"Aussie", "Australian" and "Australia's" are the same actor everywhere and "AI" is
never an actor anywhere. Rules live in config/actors.yaml; see its header for the order.

Two levels of identity:

- ``surface(name)``: the canonical name of what was mentioned ("Trump", "australia").
  Used to decide which linked entities to flag as principal.
- ``key(name)``: the state or body that actor stands for ("united states"). Principal
  support is counted and situations are matched at this level, so Trump, the White
  House and "US" in three headlines are one participant with three mentions.
"""

from __future__ import annotations

import re
from typing import Iterable

from osint_monitor.core.config import ActorsConfig, load_actors_config
from osint_monitor.processors.entity_resolver import normalise

_QUOTES = "\"'“”‘’`«»"
_POSSESSIVE = re.compile(r"['’]s?$")
_EDGE = re.compile(r"^[\s\-–—:;,.!?()\[\]" + _QUOTES + r"]+|[\s\-–—:;,.!?()\[\]" + _QUOTES + r"]+$")
_SPACES = re.compile(r"\s+")


def clean(text: str) -> str:
    """Strip surrounding quotes/punctuation and a trailing possessive: "Air Force’s" -> "Air Force"."""
    t = _EDGE.sub("", text or "")
    t = _POSSESSIVE.sub("", t)
    return _SPACES.sub(" ", _EDGE.sub("", t)).strip()


class ActorNormalizer:
    def __init__(self, config: ActorsConfig | None = None,
                 extra_aliases: dict[str, str] | None = None, extra_represents: dict[str, str] | None = None):
        config = config or ActorsConfig()
        key = lambda x: normalise(clean(x))                                # noqa: E731  same cleanup as mentions
        n = lambda d: {key(k): key(v) for k, v in d.items()}                # noqa: E731
        self._non_actors = {key(x) for x in config.non_actors}
        self._demonyms = n(config.demonyms)
        self._aliases = {**n(config.aliases), **n(extra_aliases or {})}
        self._represents = {**n(config.represents), **n(extra_represents or {})}
        self._known = (set(self._demonyms) | set(self._demonyms.values()) | set(self._aliases)
                       | set(self._aliases.values()) | set(self._represents) | set(self._represents.values()))

    @classmethod
    def load(cls, extra_aliases: dict[str, str] | None = None,
             extra_represents: dict[str, str] | None = None) -> "ActorNormalizer":
        return cls(load_actors_config(), extra_aliases, extra_represents)

    def _demonym(self, k: str) -> str | None:
        if k in self._demonyms:
            return self._demonyms[k]
        if k.endswith("s") and k[:-1] in self._demonyms:       # "Russians", "Aussies"
            return self._demonyms[k[:-1]]
        return None

    def surface(self, name: str) -> str | None:
        """Canonical name of the mentioned actor, or None if it is not an actor."""
        k = normalise(clean(name))
        if not k or k in self._non_actors:
            return None
        k = self._demonym(k) or k
        k = self._aliases.get(k, k)
        return None if k in self._non_actors else k

    def key(self, name: str) -> str | None:
        """The state or body the mentioned actor stands for."""
        k = self.surface(name)
        return self._represents.get(k, k) if k else None

    def represents(self, surface_key: str) -> str:
        return self._represents.get(surface_key, surface_key)

    def keys(self, names: Iterable[str]) -> frozenset[str]:
        return frozenset(k for k in (self.key(n) for n in names) if k)

    def is_known(self, name: str) -> bool:
        """Whether the configuration names this actor (used to rescue NER misses such as "Xi-Trump")."""
        k = self.surface(name)
        return bool(k) and (k in self._known or normalise(clean(name)) in self._known)
