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
import unicodedata
from typing import Iterable

from osint_monitor.core.config import ActorsConfig, load_actors_config
from osint_monitor.processors.entity_resolver import normalise

_QUOTES = "\"'“”‘’`«»"
_POSSESSIVE = re.compile(r"['’]s?$")
_EDGE = re.compile(r"^[\s\-–—:;,.!?()\[\]" + _QUOTES + r"]+|[\s\-–—:;,.!?()\[\]" + _QUOTES + r"]+$")
_SPACES = re.compile(r"\s+")


def fold(text: str) -> str:
    """Accent-insensitive form ("Irán" -> "iran", "israelí" -> "israeli"), as the gazetteer matches places."""
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))


def clean(text: str) -> str:
    """Strip surrounding quotes/punctuation and a trailing possessive: "Air Force’s" -> "Air Force"."""
    t = _EDGE.sub("", text or "")
    t = _POSSESSIVE.sub("", t)
    return _SPACES.sub(" ", _EDGE.sub("", t)).strip()


class ActorNormalizer:
    def __init__(self, config: ActorsConfig | None = None,
                 extra_aliases: dict[str, str] | None = None, extra_represents: dict[str, str] | None = None,
                 place_aliases: dict[str, str] | None = None):
        config = config or ActorsConfig()
        key = lambda x: normalise(clean(x))                                # noqa: E731  same cleanup as mentions
        n = lambda d: {key(k): key(v) for k, v in d.items()}                # noqa: E731
        self._non_actors = {key(x) for x in config.non_actors}
        self._ambiguous = {fold(key(x)) for x in config.ambiguous_names}
        self._demonyms = n(config.demonyms)
        self._aliases = {**n(config.aliases), **n(extra_aliases or {})}
        # accent-folded lookups, and the gazetteer's place names in other languages ("Estados Unidos",
        # "Stati Uniti", "Moscú"): a place alias is used only for a mention that is not already an actor name
        self._demonyms_folded = {fold(k): v for k, v in self._demonyms.items()}
        self._aliases_folded = {fold(k): v for k, v in self._aliases.items()}
        self._places = {fold(key(k)): key(v) for k, v in (place_aliases or {}).items()}
        self._represents = {**n(config.represents), **n(extra_represents or {})}
        self._known = (set(self._demonyms) | set(self._demonyms.values()) | set(self._aliases)
                       | set(self._aliases.values()) | set(self._represents) | set(self._represents.values()))
        self._known_folded = {fold(x): x for x in self._known}
        titles = sorted({key(t) for t in config.titles if key(t)}, key=len, reverse=True)
        self._title = re.compile(r"^(?:" + "|".join(re.escape(t) for t in titles) + r")\s+") if titles else None
        self.media = {key(m) for m in config.media_outlets}

    @classmethod
    def load(cls, extra_aliases: dict[str, str] | None = None,
             extra_represents: dict[str, str] | None = None) -> "ActorNormalizer":
        """Actor config plus the institution registry (config/institutions.yaml): every name of an
        institution is an alias of its canonical name, and an institution represents its top parent
        (the U.S. Navy acts for the United States). Two-letter acronyms (UN, EU) stay out: here names are
        compared lower-case, and "un" is also an article."""
        from osint_monitor.processors.institutions import registry
        reg = registry()
        aliases, represents = {}, {}
        for inst in reg.by_name.values():
            for alias in inst.aliases:
                if len(re.sub(r"[^A-Za-z]", "", alias)) > 2:
                    aliases[alias] = inst.canonical
            top = reg.top(inst.canonical)
            if top != inst.canonical:
                represents[inst.canonical] = top
        from osint_monitor.processors.geography import CONFIG_DIR
        import yaml
        geo = CONFIG_DIR / "geography.yaml"
        places = (yaml.safe_load(geo.read_text(encoding="utf-8")) or {}).get("aliases") if geo.exists() else None
        return cls(load_actors_config(), {**aliases, **(extra_aliases or {})}, {**represents, **(extra_represents or {})},
                   place_aliases=places)

    def _demonym(self, k: str) -> str | None:
        for table, word in ((self._demonyms, k), (self._demonyms_folded, fold(k))):
            if word in table:
                return table[word]
            if word.endswith("s") and word[:-1] in table:     # "Russians", "Aussies", "rusos"
                return table[word[:-1]]
        return None

    def _alias(self, k: str) -> str:
        if k in self._aliases:
            return self._aliases[k]
        f = fold(k)
        if f in self._aliases_folded:
            return self._aliases_folded[f]
        if k not in self._known and f in self._places:          # "estados unidos" -> "united states"
            p = self._places[f]
            return self._aliases.get(p, p)                      # gazetteer "turkiye" -> actor "turkey"
        if k not in self._known:
            return self._known_folded.get(f, k)                 # "irán" -> "iran"
        return k

    def surface(self, name: str) -> str | None:
        """Canonical name of the mentioned actor, or None if it is not an actor."""
        k = normalise(clean(name))
        if self._title and k not in self._known:
            k = self._title.sub("", k)                    # "FM Araghchi" -> "araghchi"
        if not k or k in self._non_actors or fold(k) in self._ambiguous:
            return None
        k = self._demonym(k) or k
        k = self._alias(k)
        return None if k in self._non_actors else k

    def key(self, name: str) -> str | None:
        """The state or body the mentioned actor stands for."""
        k = self.surface(name)
        return self._represents.get(k, k) if k else None

    def represents(self, surface_key: str) -> str:
        return self._represents.get(surface_key, surface_key)

    def keys(self, names: Iterable[str]) -> frozenset[str]:
        return frozenset(k for k in (self.key(n) for n in names) if k)

    def is_media(self, name: str) -> bool:
        return normalise(clean(name)) in self.media

    def is_known(self, name: str) -> bool:
        """Whether the configuration names this actor (used to rescue NER misses such as "Xi-Trump")."""
        k = self.surface(name)
        return bool(k) and (k in self._known or normalise(clean(name)) in self._known)
