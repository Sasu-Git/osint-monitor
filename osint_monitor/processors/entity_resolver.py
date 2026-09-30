"""Entity resolution: normalisation, coreference, type-correction, then
alias-based + fuzzy matching."""

from __future__ import annotations

import html
import logging
import re
import unicodedata
from datetime import datetime

from rapidfuzz import fuzz
from sqlalchemy.orm import Session

from osint_monitor.core.config import load_entities_config
from osint_monitor.core.database import Entity
from osint_monitor.core.models import EntityType, ExtractedEntity

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------
FUZZY_THRESHOLD_SAME_TYPE = 80   # same entity-type comparison
FUZZY_THRESHOLD_CROSS_TYPE = 85  # cross-type comparison

# ---------------------------------------------------------------------------
# 1. Abbreviation expansion (applied *before* fuzzy matching)
# ---------------------------------------------------------------------------
ABBREVIATION_MAP: dict[str, str] = {
    "u.s.":   "united states",
    "u.s":    "united states",
    "us":     "united states",
    "usa":    "united states",
    "uk":     "united kingdom",
    "eu":     "european union",
    "uae":    "united arab emirates",
    "dprk":   "north korea",
    "prc":    "china",
    "roc":    "taiwan",
}

# ---------------------------------------------------------------------------
# 2. Coreference map – known geopolitical / org synonyms
#    Maps every variant (lowercased) to a single canonical form.
# ---------------------------------------------------------------------------
_COREFERENCE_GROUPS: list[tuple[str, list[str]]] = [
    # Capitals are places with their own identity (a capital acting for its state is a role, see
    # config/actors.yaml `represents`); institutions are in config/institutions.yaml.
    ("United States", [
        "united states", "u.s.", "u.s", "us", "usa",
        "america", "united states of america",
    ]),
    ("Russia", [
        "russia", "russian federation",
    ]),
    ("China", [
        "china", "people's republic of china", "prc",
    ]),
    ("Iran", [
        "iran", "islamic republic of iran",
    ]),
    ("Israel", [
        "israel",
    ]),
    ("Ukraine", [
        "ukraine",
    ]),
    ("North Korea", [
        "north korea", "dprk",
    ]),
]

COREFERENCE_MAP: dict[str, str] = {}
for _canonical, _variants in _COREFERENCE_GROUPS:
    for _v in _variants:
        COREFERENCE_MAP[_v] = _canonical.lower()

# ---------------------------------------------------------------------------
# 3. Type-correction table – spaCy mis-tags these as ORG
# ---------------------------------------------------------------------------
KNOWN_PERSONS: set[str] = {
    "trump", "donald trump",
    "putin", "vladimir putin",
    "xi jinping", "xi",
    "zelenskyy", "zelensky", "volodymyr zelenskyy",
    "netanyahu", "benjamin netanyahu",
    "khamenei", "ali khamenei",
    "hegseth", "pete hegseth",
}

# ---------------------------------------------------------------------------
# Leading-article regex
# ---------------------------------------------------------------------------
_ARTICLE_RE = re.compile(r"^(the|a|an)\s+", re.IGNORECASE)
_TWITTER_RE = re.compile(r"^@")


# ---------------------------------------------------------------------------
# Normalisation helper
# ---------------------------------------------------------------------------

def normalise(text: str) -> str:
    """Return a normalised form used for comparison / lookup.

    Steps:
      1. Strip & lowercase
      2. Strip leading articles ("the ", "a ", "an ")
      3. Strip @ prefix (Twitter handles)
      4. Expand known abbreviations
      5. Apply coreference map
    """
    t = text.strip().lower()
    t = _ARTICLE_RE.sub("", t).strip()
    t = _TWITTER_RE.sub("", t).strip()

    # Full-text abbreviation replacement (if the *entire* normalised string
    # matches an abbreviation key, expand it).
    if t in ABBREVIATION_MAP:
        t = ABBREVIATION_MAP[t]

    # Coreference collapse
    if t in COREFERENCE_MAP:
        t = COREFERENCE_MAP[t]

    return t


def correct_entity_type(text: str, entity_type: EntityType) -> EntityType:
    """Fix known mis-classifications (e.g. 'Trump' tagged ORG -> PERSON)."""
    if normalise(text) in KNOWN_PERSONS or text.strip().lower() in KNOWN_PERSONS:
        if entity_type != EntityType.PERSON:
            logger.debug(
                "Type-corrected '%s' from %s -> PERSON", text, entity_type
            )
            return EntityType.PERSON
    return entity_type


# ---------------------------------------------------------------------------
# Main resolver
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Resolution safety (fuzzy matches never create durable truth)
# ---------------------------------------------------------------------------

_VARIANT_PUNCT = re.compile(r"[.’'`´,\-–—/]")
_ORDINAL_WORDS = {"first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"}
_NUMBER = re.compile(r"\d+")


def variant_key(text: str) -> str:
    """Surface form without case, article, possessive, punctuation or a plural 's': "the U.S. Navy",
    "US Navy" and "U.S. Navy’s" share a key; "American" and "Mexican" do not."""
    t = html.unescape(text or "").lower().strip()
    t = "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))   # Teherán = Teheran
    t = re.sub(r"['’]s?$", "", t)
    t = _ARTICLE_RE.sub("", t)
    t = _VARIANT_PUNCT.sub("", t)
    t = " ".join(t.split())
    return t[:-1] if len(t) > 3 and t.endswith("s") and not t.endswith("ss") else t


def _numbers(text: str) -> set[str]:
    words = set(re.findall(r"[a-z]+", text.lower()))
    return set(_NUMBER.findall(text)) | (words & _ORDINAL_WORDS)


def _acronym(text: str) -> str | None:
    letters = re.sub(r"[^A-Za-z]", "", text)
    return letters if len(letters) >= 2 and letters.isupper() else None


_GEO = None
_ACTORS = None


def _country_or_nationality(text: str) -> str | None:
    """The country a whole mention names ("Canada", "American", "U.S."), else None."""
    global _GEO, _ACTORS
    if _GEO is None:
        from osint_monitor.processors.actors import ActorNormalizer
        from osint_monitor.processors.geography import Gazetteer
        _GEO, _ACTORS = Gazetteer.load(), ActorNormalizer.load()
    if _GEO.is_country(text):
        return _GEO.canonical(text)
    key = _ACTORS.surface(text)
    return key if key and _GEO.is_country(key) else None


def _known_place(text: str) -> str | None:
    _country_or_nationality("")            # load
    canon = _GEO.canonical(text)
    return canon if (_GEO.is_country(canon) or _GEO.is_subnational(canon)) else None


def identity_conflict(mention: str, candidate: str) -> str | None:
    """Why ``mention`` must not be taken for ``candidate`` by similarity alone, or None.
    Identity-critical tokens must agree: numbers and ordinals, country/nationality words (never fuzzy),
    known places, acronym letters, and the proper-noun tokens two multi-word names do not share."""
    if variant_key(mention) == variant_key(candidate):
        return None
    if _numbers(mention) != _numbers(candidate):
        return "numbers differ"
    if _country_or_nationality(mention) or _country_or_nationality(candidate):
        return "country or nationality word"
    pm, pc = _known_place(mention), _known_place(candidate)
    if (pm or pc) and pm != pc:
        return "different places"
    vm, vc = variant_key(mention).split(), variant_key(candidate).split()
    if len(vm) == 1 and len(vc) == 1:
        return "single-word names differ"          # Zou / Zhou, Eastern / Western: the one token is the identity
    am, ac = _acronym(mention), _acronym(candidate)
    if (am or ac) and am != ac:
        return "acronym letters differ"
    tm = {w for w in re.findall(r"[A-Za-z][\w\-]*", mention) if w[0].isupper()}
    tc = {w for w in re.findall(r"[A-Za-z][\w\-]*", candidate) if w[0].isupper()}
    if len(tm) > 1 and len(tc) > 1 and {variant_key(w) for w in tm} ^ {variant_key(w) for w in tc}:
        only_m = {variant_key(w) for w in tm} - {variant_key(w) for w in tc}
        only_c = {variant_key(w) for w in tc} - {variant_key(w) for w in tm}
        if only_m and only_c:
            return "different name tokens"
    return None


class EntityResolver:
    """Resolves extracted entity mentions to canonical entities in the DB.

    Resolution order:
      0. Normalise text, correct entity type
      1. Exact match against *trusted* names: canonical names, seeded aliases (config/entities.yaml) and
         aliases that are surface variants of the canonical name ("US Navy" / "the U.S. Navy")
      2. Normalised match (abbreviations, coreference groups)
      3. Fuzzy match (rapidfuzz, type-aware thresholds) -- *provisional*: accepted only when no
         identity-critical token disagrees (``identity_conflict``) and never stored as an alias
      4. Create new entity if no match

    Aliases learned by earlier fuzzy matches (not seeded, not a surface variant) are no longer trusted
    for exact matches; they are fuzzy evidence checked against the entity's canonical name. Every call
    leaves ``last_method`` and ``last_evidence`` for the caller to store.
    """

    def __init__(self, session: Session):
        self.session = session
        self._alias_map: dict[str, int] | None = None
        # Secondary map: normalised-form -> entity_id (for normalisation hits)
        self._norm_map: dict[str, int] | None = None
        self._untrusted: dict[str, int] = {}          # learned alias (lower) -> entity id
        self._canonical: dict[int, str] = {}
        self.last_method: str | None = None
        self.last_evidence: str | None = None

    # ------------------------------------------------------------------
    # Alias / normalisation caches
    # ------------------------------------------------------------------

    @staticmethod
    def _seeded_aliases() -> dict[str, set[str]]:
        out: dict[str, set[str]] = {}
        for seed in load_entities_config():
            out.setdefault(variant_key(seed.canonical_name), set()).update(variant_key(a) for a in seed.aliases)
        return out

    def _build_alias_map(self) -> dict[str, int]:
        """Build lowercase trusted name -> entity_id lookup (and the untrusted learned aliases)."""
        if self._alias_map is not None:
            return self._alias_map

        self._alias_map = {}
        self._norm_map = {}
        self._untrusted = {}
        seeded = self._seeded_aliases()
        entities = self.session.query(Entity).all()
        for ent in entities:
            self._canonical[ent.id] = ent.canonical_name
            key = ent.canonical_name.lower()
            self._alias_map[key] = ent.id
            self._norm_map[normalise(ent.canonical_name)] = ent.id
            trusted = {variant_key(ent.canonical_name)} | seeded.get(variant_key(ent.canonical_name), set())
            for alias in ent.aliases or []:
                if variant_key(alias) in trusted:
                    self._alias_map.setdefault(alias.lower(), ent.id)
                    self._norm_map.setdefault(normalise(alias), ent.id)
                else:
                    self._untrusted.setdefault(alias.lower(), ent.id)
        return self._alias_map

    def _get_norm_map(self) -> dict[str, int]:
        if self._norm_map is None:
            self._build_alias_map()
        assert self._norm_map is not None
        return self._norm_map

    def _entity_type_for_id(self, eid: int) -> str | None:
        """Return the entity_type string for a given entity id (cheap)."""
        ent = self.session.get(Entity, eid)
        return ent.entity_type if ent else None

    # ------------------------------------------------------------------
    # Core resolution
    # ------------------------------------------------------------------

    def _done(self, entity: Entity, method: str, evidence: str) -> Entity:
        self.last_method, self.last_evidence = method, evidence
        entity.last_seen_at = datetime.utcnow()
        return entity

    def _institution_entity(self, canonical: str) -> Entity:
        return self._institution_entity_typed(canonical, EntityType.ORG)

    def _institution_entity_typed(self, canonical: str, etype: EntityType) -> Entity:
        entity = self.session.query(Entity).filter_by(canonical_name=canonical).first()
        if entity is None:
            entity = Entity(canonical_name=canonical, entity_type=etype.value, aliases=[],
                            first_seen_at=datetime.utcnow(), last_seen_at=datetime.utcnow())
            self.session.add(entity)
            self.session.flush()
            if self._alias_map is not None:
                self._alias_map[canonical.lower()] = entity.id
                self._norm_map[normalise(canonical)] = entity.id
        return entity

    def resolve(self, extracted: ExtractedEntity, context: set[str] | None = None) -> Entity:
        """Resolve an extracted entity to a database Entity (see the class docstring).

        ``context``: the states / organisations the mention's item names or its publisher is
        (``institutions.item_qualifiers``); a generic label ("the Navy") resolves only through it."""
        # --- Step 0: normalise & type-correct --------------------------------
        corrected_type = correct_entity_type(
            extracted.text, extracted.entity_type
        )
        extracted = extracted.model_copy(
            update={"entity_type": corrected_type}
        )

        from osint_monitor.processors.text_normalize import clean_name
        clean = clean_name(extracted.text) or extracted.text.strip()
        text_lower = extracted.text.strip().lower()
        text_norm = normalise(clean)

        alias_map = self._build_alias_map()
        norm_map = self._get_norm_map()

        # --- Step 0b: institutions, organisations and forums (config/institutions.yaml) --------
        from osint_monitor.processors.institutions import registry
        reg = registry()
        inst = reg.lookup(clean) or reg.lookup(extracted.text.strip())
        if inst is not None:
            return self._done(self._institution_entity(inst.canonical), "registry",
                              f"'{extracted.text}' is a name of {inst.canonical} ({inst.kind})")
        generic = reg.is_generic(clean)
        if generic:
            inst = reg.resolve_generic(clean, context or set())
            if inst is not None:
                return self._done(self._institution_entity(inst.canonical), "registry-context",
                                  f"generic '{clean}' with {sorted(context or [])} -> {inst.canonical}")

        # --- Step 0c: nationality words name their country, deterministically ("Canadian", "American");
        # never by similarity ("American" is not "Mexican")
        if corrected_type == EntityType.NORP or extracted.entity_type == EntityType.NORP:
            country = _country_or_nationality(clean)
            if country:
                eid = alias_map.get(country) or norm_map.get(normalise(country))
                entity = self.session.get(Entity, eid) if eid else None
                if entity is None:
                    entity = self._institution_entity_typed(country.title(), EntityType.GPE)
                return self._done(entity, "demonym", f"'{extracted.text}' names {entity.canonical_name}")

        # --- Step 1: Exact match against trusted names ----------------------
        exact_key = text_lower if text_lower in alias_map else clean.lower()
        if exact_key in alias_map:
            entity = self.session.get(Entity, alias_map[exact_key])
            if entity:
                return self._done(entity, "exact", f"'{extracted.text}' is a trusted name of '{entity.canonical_name}'")

        # --- Step 1b: Exact match (normalised form) -------------------------
        if text_norm in norm_map:
            entity = self.session.get(Entity, norm_map[text_norm])
            if entity:
                # a pure surface variant becomes an alias; a match through the abbreviation /
                # coreference tables is resolution evidence only
                if variant_key(extracted.text) in {variant_key(entity.canonical_name),
                                                    *(variant_key(a) for a in entity.aliases or [])}:
                    self._register_alias(entity, extracted.text)
                return self._done(entity, "normalised", f"normalised '{text_norm}' matches '{entity.canonical_name}'")

        # --- Step 2: Fuzzy match -- provisional, never stored as an alias --
        best_score = 0.0
        best_id: int | None = None
        best_alias = ""
        # a generic label whose context names no owner is not matched to a look-alike either
        candidates = [] if generic else list(alias_map.items()) + list(self._untrusted.items())
        for alias, eid in candidates:
            # Compare normalised forms for better fuzzy performance
            alias_norm = normalise(alias)
            score = fuzz.ratio(text_norm, alias_norm)
            if score > best_score:
                best_score, best_id, best_alias = score, eid, alias

        if best_id is not None:
            target_type = self._entity_type_for_id(best_id)
            threshold = (
                FUZZY_THRESHOLD_SAME_TYPE
                if target_type == corrected_type.value
                else FUZZY_THRESHOLD_CROSS_TYPE
            )

            if best_score >= threshold:
                entity = self.session.get(Entity, best_id)
                conflict = entity and (identity_conflict(extracted.text, entity.canonical_name)
                                       or identity_conflict(extracted.text, best_alias))
                if entity and not conflict:
                    logger.debug("Fuzzy matched '%s' -> '%s' (%.0f%%, threshold=%d)",
                                 extracted.text, entity.canonical_name, best_score, threshold)
                    return self._done(entity, "fuzzy-provisional",
                                      f"'{best_alias}' scored {best_score:.0f} (threshold {threshold}); not stored as an alias")
                if entity:
                    logger.debug("Fuzzy candidate '%s' for '%s' refused: %s", entity.canonical_name, extracted.text, conflict)
                    refused = f"fuzzy candidate '{entity.canonical_name}' ({best_score:.0f}) refused: {conflict}"
                else:
                    refused = ""
            else:
                refused = ""
        else:
            refused = ""

        # --- Step 3: Create new entity --------------------------------------
        canonical = clean_name(extracted.canonical_name or extracted.text) or extracted.text.strip()
        entity = Entity(
            canonical_name=canonical,
            entity_type=corrected_type.value,
            aliases=[extracted.text] if extracted.text != canonical else [],
            first_seen_at=datetime.utcnow(),
            last_seen_at=datetime.utcnow(),
        )
        self.session.add(entity)
        self.session.flush()  # get the ID

        # Update caches
        self._alias_map[canonical.lower()] = entity.id
        self._norm_map[normalise(canonical)] = entity.id
        self._canonical[entity.id] = canonical
        if extracted.text.lower() != canonical.lower():
            self._alias_map[extracted.text.lower()] = entity.id
            self._norm_map[normalise(extracted.text)] = entity.id

        logger.debug(
            "Created new entity: %s (%s)", canonical, corrected_type.value
        )
        self.last_method = "new"
        self.last_evidence = ("generic label: the context names no owning institution" if generic
                              else refused or "no trusted match")
        return entity

    # ------------------------------------------------------------------
    # Alias management
    # ------------------------------------------------------------------

    def _register_alias(self, entity: Entity, raw_text: str) -> None:
        """Add *raw_text* as an alias of *entity* (if not already present)."""
        aliases = entity.aliases or []
        if raw_text.lower() not in [a.lower() for a in aliases]:
            aliases.append(raw_text)
            entity.aliases = aliases

        # Keep caches warm
        self._alias_map[raw_text.lower()] = entity.id
        norm = normalise(raw_text)
        if self._norm_map is not None:
            self._norm_map[norm] = entity.id

    # ------------------------------------------------------------------
    # Seeding from config
    # ------------------------------------------------------------------

    def seed_from_config(self):
        """Seed entities from entities.yaml into the database."""
        seeds = load_entities_config()
        count = 0
        for seed in seeds:
            existing = self.session.query(Entity).filter_by(
                canonical_name=seed.canonical_name
            ).first()
            if existing:
                # Update aliases
                existing_aliases = set(existing.aliases or [])
                existing_aliases.update(seed.aliases)
                existing.aliases = list(existing_aliases)
                if seed.wikidata_id:
                    existing.wikidata_id = seed.wikidata_id
                continue

            entity = Entity(
                canonical_name=seed.canonical_name,
                entity_type=seed.entity_type,
                aliases=seed.aliases,
                wikidata_id=seed.wikidata_id,
            )
            self.session.add(entity)
            count += 1

        self.session.commit()
        if count:
            logger.info("Seeded %d new entities from config", count)
        self._alias_map = None  # invalidate cache
        self._norm_map = None
