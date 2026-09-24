"""Per-item provenance: who published it, who actually reported it, what kind of evidence it is.

Pragmatic on purpose -- no citation graph. Derivative reporting is inferred only from
explicit attribution to a configured origin ("(Reuters)", "according to AP") or from a
near-identical copy of an earlier item's body text. Anything else is treated as the
outlet's own reporting.
"""

from __future__ import annotations

import re
from datetime import datetime
from difflib import SequenceMatcher
from typing import Sequence

from osint_monitor.core.config import ProvenanceConfig, load_provenance_config
from osint_monitor.core.models import (
    EvidenceItem, EvidenceType, ItemProvenance, ItemStance, SourceRole,
)

_SPACE = re.compile(r"\s+")


def _alias_regex(alias: str) -> str:
    """Short all-caps aliases (AP, AFP) match case-sensitively to avoid ordinary words."""
    escaped = re.escape(alias)
    return f"(?-i:{escaped})" if alias.isupper() and len(alias) <= 4 else escaped


def _normalize(text: str) -> str:
    return _SPACE.sub(" ", text.lower()).strip()


class ProvenanceResolver:
    """Resolves EvidenceItems into ItemProvenance using config/provenance.yaml."""

    def __init__(self, config: ProvenanceConfig | None = None):
        self.config = config or load_provenance_config()
        cfg = self.config
        self._sources = {name.lower(): profile for name, profile in cfg.sources.items()}
        self._attribution: list[tuple[str, re.Pattern]] = []
        for origin, profile in cfg.origins.items():
            aliases = profile.aliases or [origin]
            alias_group = "(?:" + "|".join(_alias_regex(a) for a in aliases) + ")"
            for template in cfg.attribution_patterns:
                self._attribution.append(
                    (origin, re.compile(template.replace("{alias}", alias_group), re.IGNORECASE | re.MULTILINE)))
        self._firsthand = [re.compile(p, re.IGNORECASE) for p in cfg.firsthand_patterns]
        self._retraction = [re.compile(p, re.IGNORECASE | re.MULTILINE) for p in cfg.retraction_patterns]

    # -- source level ---------------------------------------------------------------

    def source_role(self, item: EvidenceItem) -> SourceRole:
        cfg = self.config
        profile = self._sources.get(item.source_name.lower())
        if profile and profile.role:
            return profile.role
        if item.source_category and item.source_category in cfg.category_roles:
            return cfg.category_roles[item.source_category]
        if item.collector_type and item.collector_type in cfg.collector_roles:
            return cfg.collector_roles[item.collector_type]
        return SourceRole.UNKNOWN

    def source_origin(self, item: EvidenceItem) -> str:
        profile = self._sources.get(item.source_name.lower())
        return profile.origin if profile and profile.origin else item.source_name

    def origin_role(self, origin: str) -> SourceRole | None:
        profile = self.config.origins.get(origin)
        return profile.role if profile else None

    # -- item level -----------------------------------------------------------------

    def attributed_origin(self, item: EvidenceItem, own_origin: str) -> str | None:
        """Earliest-mentioned configured origin the item attributes its report to."""
        text = f"{item.title}\n{item.text}"
        best: tuple[int, str] | None = None
        for origin, pattern in self._attribution:
            if origin == own_origin:
                continue
            m = pattern.search(text)
            if m and (best is None or m.start() < best[0]):
                best = (m.start(), origin)
        return best[1] if best else None

    def is_retraction(self, item: EvidenceItem) -> bool:
        text = f"{item.title}\n{item.text}"
        return any(p.search(text) for p in self._retraction)

    def is_firsthand(self, item: EvidenceItem) -> bool:
        text = f"{item.title}\n{item.text}"
        return any(p.search(text) for p in self._firsthand)

    def resolve(self, items: Sequence[EvidenceItem]) -> list[ItemProvenance]:
        """Provenance for every item, in input order."""
        cfg = self.config
        resolved: list[ItemProvenance] = []
        for item in items:
            role = self.source_role(item)
            own_origin = self.source_origin(item)
            stance = item.stance
            if stance == ItemStance.SUPPORTS and self.is_retraction(item):
                stance = ItemStance.RETRACTS
            derived = None if role == SourceRole.PRIMARY_OFFICIAL else self.attributed_origin(item, own_origin)

            if role in cfg.commentary_roles:
                etype, note = EvidenceType.COMMENTARY, f"{role.value} source"
            elif derived:
                etype, note = EvidenceType.DERIVATIVE, f"attributes report to {derived}"
            elif role == SourceRole.PRIMARY_OFFICIAL:
                etype, note = EvidenceType.PRIMARY, "official source"
            elif self.is_firsthand(item):
                etype, note = EvidenceType.FIRSTHAND, "direct observation"
            else:
                etype, note = EvidenceType.INDEPENDENT, "own reporting, origin not traced further"
            if role == SourceRole.UNKNOWN:
                note += "; source role unknown"

            resolved.append(ItemProvenance(
                item_id=item.item_id, source_name=item.source_name, source_role=role,
                evidence_type=etype, origin=derived or own_origin, stance=stance,
                derived_from=derived, note=note,
            ))
        self._mark_syndicated_copies(items, resolved)
        return resolved

    def _mark_syndicated_copies(self, items: Sequence[EvidenceItem], resolved: list[ItemProvenance]) -> None:
        """A later item whose body text starts like an earlier item from another origin is a copy."""
        cfg = self.config
        n = cfg.syndication_min_chars
        order = sorted(range(len(items)), key=lambda i: (items[i].published_at or datetime.min, i))
        earlier: list[tuple[str, int]] = []   # (normalized prefix, index)
        for i in order:
            body = _normalize(items[i].text)
            if len(body) < n:
                continue
            prefix = body[: n * 2]
            prov = resolved[i]
            if prov.evidence_type not in (EvidenceType.PRIMARY, EvidenceType.COMMENTARY):
                for other_prefix, j in earlier:
                    if resolved[j].origin == prov.origin:
                        continue
                    if SequenceMatcher(None, prefix, other_prefix, autojunk=False).ratio() >= cfg.syndication_similarity:
                        origin = resolved[j].origin
                        resolved[i] = prov.model_copy(update={
                            "evidence_type": EvidenceType.DERIVATIVE, "origin": origin, "derived_from": origin,
                            "note": f"near-identical copy of {resolved[j].source_name}",
                        })
                        break
            earlier.append((prefix, i))
