"""Pluggable providers for the four upstream inputs of the Situation v2 engine.

Roles: ``topic`` (family of the Development), ``location`` (specific places and the event country), ``principals``
(canonical parties), ``components`` (report-component evidence; the owner's V4 condition is derived on read and is
never stored as a field).

Two origins per role:
* ``stored``: values read from the snapshot copy, exactly what the deployed pipeline stored.
* ``model``: values read from a frozen predictions file (JSONL keyed by ``development_id`` plus a ``.meta.json``
  sidecar naming the model id, the predictions hash and the acceptance-evaluation record). The real upstream models
  plug in by producing such a file; no code change is needed. Model providers never compute anything.

Every ``get`` returns ``Provided(value, provenance)``; the driver writes both into the step trace.
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .util import sha256_file

ROLES = ("topic", "location", "principals", "components")
USABLE_CONFIDENCE = ("high", "medium")     # owner ruling T3 (2026-11-23): downstream may consume high + medium
V2_FAMILIES = ("armed_conflict", "security", "diplomacy", "economic", "politics", "hazard")


@dataclass(frozen=True)
class Provided:
    value: dict
    provenance: dict


class Provider:
    role: str = ""
    origin: str = ""                         # "stored" | "model"
    provider_id: str = ""

    def describe(self) -> dict:
        return {"role": self.role, "origin": self.origin, "provider_id": self.provider_id}

    def get(self, dev_id: int) -> Provided:  # pragma: no cover - interface
        raise NotImplementedError


# -- in-memory (tests, and any caller that already holds the values) -------------------------------------------

class DictProvider(Provider):
    def __init__(self, role: str, values: dict[int, dict], provider_id: str | None = None, origin: str = "stored"):
        self.role, self.origin = role, origin
        self.provider_id = provider_id or f"dict-{role}"
        self._values = values

    def get(self, dev_id: int) -> Provided:
        v = self._values.get(dev_id)
        return Provided(dict(v) if v is not None else {},
                        {"provider_id": self.provider_id, "origin": self.origin,
                         "source": "in-memory", "present": v is not None})


# -- stored values from the snapshot copy -----------------------------------------------------------------------

class StoredTopicProvider(Provider):
    """Family from ``events.event_type`` through the frozen v2 family mapping (contract section 1.1)."""
    role, origin = "topic", "stored"

    def __init__(self, conn: sqlite3.Connection, family_of: Callable[[str | None], str | None]):
        self.provider_id = "stored-topic:events.event_type"
        self._types = dict(conn.execute("SELECT id, event_type FROM events"))
        self._family_of = family_of

    def get(self, dev_id: int) -> Provided:
        t = self._types.get(dev_id)
        return Provided({"family": self._family_of(t), "label": t, "confidence": None},
                        {"provider_id": self.provider_id, "origin": "stored", "source": "events.event_type"})


class StoredLocationProvider(Provider):
    """Specific places of the Development's items (same selection as ``situations.store._specific_places``) and the
    interim event country: the single country of those places, else None. Containment comes from the gazetteer."""
    role, origin = "location", "stored"

    def __init__(self, conn: sqlite3.Connection, geo, normalizer, normalise: Callable[[str], str],
                 location_types: tuple[str, ...], geography_sha256: str):
        self.provider_id = "stored-location:item_entities+gazetteer"
        self._geo, self._geo_sha = geo, geography_sha256
        rows = conn.execute(
            "SELECT DISTINCT ei.event_id, e.canonical_name FROM event_items ei "
            "JOIN item_entities ie ON ie.item_id = ei.item_id JOIN entities e ON e.id = ie.entity_id "
            f"WHERE e.entity_type IN ({','.join('?' * len(location_types))}) AND e.canonical_name IS NOT NULL "
            "ORDER BY ei.event_id, e.canonical_name", location_types)
        self._places: dict[int, dict[str, str | None]] = {}
        for eid, name in rows:
            place = geo.canonical(normalise(name))
            surface = normalizer.surface(name) or ""
            if place and not geo.is_country(place) and normalizer.represents(surface) == surface:
                self._places.setdefault(eid, {})[place] = self._country(place)

    def _country(self, p: str):
        geo = self._geo
        anc = set(geo.ancestors(p)) & set(geo.countries)
        if geo.canonical(p) in geo.countries:
            return geo.canonical(p)
        return sorted(anc)[0] if len(anc) == 1 else None

    def get(self, dev_id: int) -> Provided:
        places = dict(sorted(self._places.get(dev_id, {}).items()))
        countries = {c for c in places.values() if c}
        return Provided({"places": places, "event_country": next(iter(countries)) if len(countries) == 1 else None,
                         "confidence": None},
                        {"provider_id": self.provider_id, "origin": "stored",
                         "source": "item_entities(GPE/LOC/FAC)+gazetteer", "geography_sha256": self._geo_sha[:12]})

    def describe(self) -> dict:
        return {**super().describe(), "geography_sha256": self._geo_sha}


class StoredPrincipalsProvider(Provider):
    """Principal actors as stored on ``event_entities.is_principal``, collapsed to canonical parties."""
    role, origin = "principals", "stored"

    def __init__(self, conn: sqlite3.Connection, canonical_keys: Callable[[list[str]], frozenset[str]]):
        self.provider_id = "stored-principals:event_entities.is_principal"
        self._names: dict[int, list[str]] = {}
        for eid, name in conn.execute(
                "SELECT ee.event_id, e.canonical_name FROM event_entities ee JOIN entities e ON e.id = ee.entity_id "
                "WHERE ee.is_principal = 1 ORDER BY ee.event_id, e.canonical_name"):
            self._names.setdefault(eid, []).append(name)
        self._keys = canonical_keys

    def get(self, dev_id: int) -> Provided:
        names = self._names.get(dev_id, [])
        return Provided({"names": names, "parties": sorted(self._keys(names)), "has_principals": bool(names)},
                        {"provider_id": self.provider_id, "origin": "stored", "source": "event_entities.is_principal"})


# -- component evidence (read-only JSONL, report-components-v1) ---------------------------------------------------

def derive_v4(component_sizes: list[int]) -> bool:
    """The owner's V4 condition: at least two report-item components, each with at least two items. Derived on read."""
    return sum(1 for s in component_sizes if s >= 2) >= 2


class ComponentEvidenceProvider(Provider):
    role, origin = "components", "stored"

    def __init__(self, path: Path, algorithm_version: str = "report-components-v1"):
        self.path = Path(path)
        self.sha256 = sha256_file(self.path)
        self.provider_id = f"{algorithm_version}:{self.sha256[:12]}"
        self._rows: dict[int, dict] = {}
        for line in self.path.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            if r.get("algorithm_version") != algorithm_version:
                raise SystemExit(f"STOP: component evidence algorithm_version {r.get('algorithm_version')!r} != "
                                 f"{algorithm_version!r}")
            self._rows[int(r["development_id"])] = r

    def describe(self) -> dict:
        return {**super().describe(), "path": self.path.name, "sha256": self.sha256, "rows": len(self._rows)}

    def get(self, dev_id: int) -> Provided:
        r = self._rows.get(dev_id)
        prov = {"provider_id": self.provider_id, "origin": "stored", "source": self.path.name,
                "sha256": self.sha256[:12], "present": r is not None}
        if r is None:
            return Provided({}, prov)
        return Provided({"component_sizes": list(r["component_sizes"]), "report_item_count": r["report_item_count"]},
                        prov)


# -- frozen model predictions ---------------------------------------------------------------------------------------

class FrozenPredictions:
    """A frozen predictions JSONL (one object per line, key ``development_id``) with its ``.meta.json`` sidecar.

    Sidecar fields: ``model_id``, ``predictions_sha256``, ``spec_ref``, ``acceptance_eval`` =
    {``record_path`` (relative to the sidecar), ``record_sha256``}. The eval record is a JSON file whose
    ``acceptance.scored`` is true and whose ``model_id`` and ``predictions_sha256`` match (checked by the guard)."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.meta_path = self.path.with_suffix(self.path.suffix + ".meta.json")
        if not self.path.exists():
            raise SystemExit(f"STOP: predictions file missing: {self.path}")
        if not self.meta_path.exists():
            raise SystemExit(f"STOP: predictions sidecar missing: {self.meta_path}")
        self.meta = json.loads(self.meta_path.read_text(encoding="utf-8"))
        self.sha256 = sha256_file(self.path)
        if self.meta.get("predictions_sha256") != self.sha256:
            raise SystemExit(f"STOP: predictions hash mismatch for {self.path}: sidecar "
                             f"{self.meta.get('predictions_sha256')}, file {self.sha256}")
        if not self.meta.get("model_id"):
            raise SystemExit(f"STOP: sidecar of {self.path} has no model_id")
        self.model_id = self.meta["model_id"]
        self.rows: dict[int, dict] = {}
        for n, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            r = json.loads(line)
            did = int(r["development_id"])
            if did in self.rows:
                raise SystemExit(f"STOP: duplicate development_id {did} in {self.path} (line {n})")
            self.rows[did] = r

    def acceptance_record(self) -> tuple[Path, dict] | None:
        ev = self.meta.get("acceptance_eval") or {}
        rel = ev.get("record_path")
        if not rel:
            return None
        p = (self.meta_path.parent / rel).resolve()
        if not p.exists() or sha256_file(p) != ev.get("record_sha256"):
            return None
        return p, json.loads(p.read_text(encoding="utf-8"))

    def prov(self, dev_id: int) -> dict:
        return {"provider_id": f"model:{self.model_id}", "origin": "model", "model_id": self.model_id,
                "source": self.path.name, "predictions_sha256": self.sha256[:12], "present": dev_id in self.rows}


class _ModelProvider(Provider):
    origin = "model"

    def __init__(self, predictions: FrozenPredictions):
        self.pred = predictions
        self.provider_id = f"model:{predictions.model_id}"

    def describe(self) -> dict:
        return {**super().describe(), "model_id": self.pred.model_id, "predictions_file": self.pred.path.name,
                "predictions_sha256": self.pred.sha256, "predictions_rows": len(self.pred.rows),
                "meta_sha256": sha256_file(self.pred.meta_path)}


class ModelTopicProvider(_ModelProvider):
    """Record: ``topic_family`` (v2 family, ``out_of_scope`` or null), ``confidence``, ``abstain_reason`` (topic SPEC
    section 1). Consumed only when the family is a v2 family and confidence is high or medium (T3); otherwise the
    family is None, the same as ``unknown`` today. The unconsumed raw record stays visible in the trace."""
    role = "topic"

    def get(self, dev_id: int) -> Provided:
        r = self.pred.rows.get(dev_id)
        prov = self.pred.prov(dev_id)
        if r is None:
            return Provided({"family": None, "label": None, "confidence": None, "used": False}, prov)
        fam, conf = r.get("topic_family"), r.get("confidence")
        used = fam in V2_FAMILIES and conf in USABLE_CONFIDENCE
        return Provided({"family": fam if used else None, "label": fam, "confidence": conf,
                         "abstain_reason": r.get("abstain_reason"), "used": used}, prov)


class ModelLocationProvider(_ModelProvider):
    """Record (location SPEC section 1): ``event_location``, ``event_country``, ``target_location`` (optional
    ``target_country``), ``places`` [{place, country, role}], ``confidence``, ``abstain_reason``. Consumed when
    confidence is high or medium: ``places`` = the event and target places with their countries (roles event and
    target only, never origin, actor_location, venue or reporting); ``event_country`` as given (null for seas,
    regions, disputed). Otherwise no places and no event country."""
    role = "location"

    def get(self, dev_id: int) -> Provided:
        r = self.pred.rows.get(dev_id)
        prov = self.pred.prov(dev_id)
        if r is None:
            return Provided({"places": {}, "event_country": None, "confidence": None, "used": False}, prov)
        conf = r.get("confidence")
        used = conf in USABLE_CONFIDENCE
        places: dict[str, str | None] = {}
        if used:
            for p in r.get("places") or []:
                if p.get("role") in ("event", "target") and p.get("place"):
                    places[p["place"]] = p.get("country")
            for key, ckey in (("event_location", "event_country"), ("target_location", "target_country")):
                if r.get(key) and r[key] not in places:
                    places[r[key]] = r.get(ckey)
        return Provided({"places": dict(sorted(places.items())),
                         "event_country": r.get("event_country") if used else None,
                         "confidence": conf, "abstain_reason": r.get("abstain_reason"), "used": used}, prov)


class ModelPrincipalsProvider(_ModelProvider):
    """Record: ``principal_parties`` (canonical party names or surfaces), mapped through the same canonicaliser as
    the stored path so that representatives collapse to their states in the engine's keys."""
    role = "principals"

    def __init__(self, predictions: FrozenPredictions, canonical_keys: Callable[[list[str]], frozenset[str]]):
        super().__init__(predictions)
        self._keys = canonical_keys

    def get(self, dev_id: int) -> Provided:
        r = self.pred.rows.get(dev_id)
        prov = self.pred.prov(dev_id)
        names = list((r or {}).get("principal_parties") or [])
        return Provided({"names": names, "parties": sorted(self._keys(names)), "has_principals": bool(names)}, prov)
