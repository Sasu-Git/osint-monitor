"""Actor roles: what each entity does in a Development (Core Entity Resolution Principle).

Roles: ``actor`` (performs / owns the action), ``participant`` (takes part without owning it: counterpart,
recipient, meeting guest), ``target`` (the action is directed against it), ``affected`` (the action happens
to it: moved, protected, deported), ``institutional_context`` (the forum or organisation it happens in),
``location`` and ``subject`` (mentioned, discussed).

Per item, each actor-capable mention gets a role from its place in the dependency parse of the headline or
lead sentence, for the English model (ClearNLP labels) and the Italian/Spanish models (Universal
Dependencies). Modifiers take their head's role ("Israeli forces kill ..." -> Israel is the actor), a
capital or seat of government acting stands for its state (config/actors.yaml ``represents``), generic
institution labels count only when the item's context resolves them (config/institutions.yaml). Per
Development, a holder's role is the one with the most weight (headline 1.0, lead 0.5).
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

ROLE_PRIORITY = ["actor", "target", "participant", "affected", "institutional_context", "location", "subject"]
HEADLINE, LEAD = 1.0, 0.5

COERCIVE_VERBS = {"kill", "strike", "attack", "hit", "target", "sanction", "bomb", "shell", "blame", "accuse",
                  "threaten", "condemn", "arrest", "revoke", "ban", "punish", "invade", "raid", "seize", "fine",
                  "sue", "blacklist", "expel", "defeat", "shoot", "destroy", "sink", "block", "reject", "warn",
                  # it / es
                  "uccidere", "colpire", "attaccare", "sanzionare", "accusare", "minacciare", "condannare",
                  "matar", "atacar", "sancionar", "acusar", "amenazar", "condenar", "bombardear", "rechazar"}
AFFECTING_VERBS = {"send", "deploy", "dispatch", "station", "deport", "repatriate", "evict", "return", "relocate", "protect", "defend", "help",
                   "support", "aid", "rescue", "evacuate", "free", "release", "compensate", "shelter",
                   "rimpatriare", "espellere", "proteggere", "difendere", "aiutare", "enviar", "deportar",
                   "repatriar", "proteger", "defender", "ayudar"}
# the addressee of a request is its target: "Poland asks NATO for more forces"
REQUEST_VERBS = {"ask", "request", "urge", "press", "appeal", "demand", "petition", "implore", "chiedere", "sollecitare",
                 "pedir", "solicitar", "instar", "exigir"}
MEETING_VERBS = {"meet", "visit", "host", "call", "talk", "negotiate", "incontrare", "visitare", "reunirse",
                 "visitar", "hablar"}
# the parties to a meeting or negotiation are co-actors: "Trump meets Xi", "talks between Trump and Xi"
MEETING_NOUNS = {"summit", "talk", "talks", "meeting", "visit", "call", "dinner", "negotiation", "dialogue", "deal",
                 "pact", "accord", "agreement", "treaty", "truce", "vertice", "incontro", "cumbre", "reunión",
                 "acuerdo", "accordo", "colloquio", "negociación", "trattativa"}
TOPIC_VERBS = {"discuss", "debate", "address", "raise", "focus", "consider", "examine", "review", "weigh", "mull",
               "cite", "mention", "eye", "discutere", "discutir"}
TOPIC_SUBJECT_VERBS = {"top", "dominate", "overshadow", "headline", "loom", "feature"}
TOPIC_HEADS = {"crisis", "war", "conflict", "issue", "tension", "question", "debate", "concern", "fear", "row",
               "dispute", "future", "role", "link", "relation", "tie"}

PARTICIPANT_PREPS = {"with", "between", "con", "tra", "fra", "entre", "among"}
TARGET_PREPS = {"against", "contro", "contra"}
ON_PREPS = {"on", "upon", "sobre", "su", "sul", "sulla", "sui", "sugli", "sulle"}
AGENT_PREPS = {"by", "da", "dal", "dalla", "dai", "dagli", "por"}
TO_PREPS = {"to", "a", "al", "alla", "ai", "agli", "alle", "hacia", "into"}
FOR_PREPS = {"for", "per", "para"}
PLACE_PREPS = {"in", "at", "across", "near", "over", "from", "throughout", "inside", "outside", "around", "off",
               "en", "nel", "nella", "nei", "negli", "nelle", "desde", "cerca", "vicino", "presso", "within"}
OF_PREPS = {"of", "de", "di", "del", "della", "dei", "degli", "delle", "dello"}
# nouns whose modifier or genitive is the one acting: "Houthi attacks", "US sanctions", "the Pentagon's
# blacklisting", "respuesta oficial de EEUU", "decision of the court"
ACTION_NOUNS = {"attack", "strike", "airstrike", "sanction", "raid", "offensive", "bombardment", "invasion", "blockade",
                "crackdown", "decision", "plan", "proposal", "offer", "order", "decree", "response", "reply", "deal",
                "exercise", "drill", "operation", "ban", "blacklisting", "veto", "ruling", "statement", "warning",
                "demand", "threat", "request", "announcement", "move", "push", "campaign", "deployment",
                "ataque", "sanción", "decisión", "propuesta", "oferta", "orden", "decreto", "respuesta", "plan",
                "attacco", "sanzione", "decisione", "proposta", "offerta", "ordine", "risposta", "piano", "annuncio"}
COERCIVE_NOUNS = {"sanction", "strike", "attack", "tariff", "embargo", "ban", "blockade", "raid", "crackdown",
                  "pressure", "assault", "offensive", "bombardment", "restriction", "curb", "war", "measure",
                  "levy", "penalty", "duty", "sanzione", "attacco", "sanción", "ataque", "complaint"}

SUBJECT_DEPS = {"nsubj", "csubj", "expl"}
PASSIVE_DEPS = {"nsubjpass", "csubjpass", "nsubj:pass", "csubj:pass"}
OBJECT_DEPS = {"dobj", "obj", "attr", "oprd"}
INDIRECT_DEPS = {"iobj", "dative"}
CLIMB_DEPS = {"compound", "amod", "poss", "nmod:poss", "appos", "flat", "flat:name", "nummod", "conj", "det"}
PREP_OBJECT_DEPS = {"pobj"}                 # English: token under a preposition
OBLIQUE_DEPS = {"obl", "nmod", "obl:agent", "obl:arg"}  # UD: token with a "case" child


@dataclass
class Mention:
    text: str
    holder: str                # canonical actor key this mention stands for (lower case)
    role: str
    field: str
    reason: str = ""
    fallback: bool = False     # role inferred from no grammatical evidence (headline fragment, unknown relation)


@dataclass
class ItemRoles:
    mentions: list[Mention] = field(default_factory=list)


def _lemma(tok) -> str:
    return (tok.lemma_ or tok.text).lower()


def _case_word(tok) -> str | None:
    for child in tok.children:
        if child.dep_ in ("case", "mark") or (child.dep_ == "fixed" and child.pos_ == "ADP"):
            return child.lower_
    return None


def _phrase_head(tok):
    """The head of the noun phrase a token modifies ("G7" -> "sanctions" -> "proposal")."""
    for _ in range(6):
        if tok.dep_ in ("compound", "amod", "nmod", "flat", "flat:name") and tok.head is not tok:
            tok = tok.head
        else:
            break
    return tok


def clause_role(span, is_place: bool, is_forum: bool) -> tuple[str, str]:
    """(role, reason) of a mention from its position in the parse."""
    tok = span.root
    for _ in range(14):
        dep, head = tok.dep_, tok.head
        if dep in CLIMB_DEPS and head is not tok:
            if dep == "conj":
                tok = head
                continue
            if dep in ("compound", "amod", "nmod") and is_forum and _phrase_head(head).dep_ not in SUBJECT_DEPS | {"ROOT"}:
                return "institutional_context", f"frames '{head.text}'"   # "G7 agreement", "push G7 sanctions proposal"
            if dep in ("compound", "amod", "poss", "nmod:poss") and _lemma(head) in ACTION_NOUNS:
                return "actor", f"agent of '{head.text}'"      # "Houthi attacks", "US sanctions"
            tok = head                          # "Israeli forces", "Saudi Arabia's minister", "US Navy officials"
            continue
        if dep in PREP_OBJECT_DEPS or (dep in OBLIQUE_DEPS and _case_word(tok)):
            prep_tok = head if dep in PREP_OBJECT_DEPS else None
            word = (prep_tok.lower_ if prep_tok is not None else _case_word(tok)) or ""
            gov = (prep_tok.head if prep_tok is not None else head)
            gov_lemma = _lemma(gov)
            if dep == "obl:agent" or (word in AGENT_PREPS and any(c.dep_ in ("auxpass", "aux:pass") for c in gov.children)):
                return "actor", f"agent ('{word}') of '{gov.text}'"
            if word in OF_PREPS and gov is not tok and gov.pos_ in ("NOUN", "PROPN"):
                if _lemma(gov) in ACTION_NOUNS:
                    return "actor", f"agent of '{gov.text}'"    # "respuesta oficial de EEUU"
                tok = gov                        # "head of Hamas" -> the noun's role
                continue
            if word in PARTICIPANT_PREPS:
                if gov_lemma in TOPIC_VERBS:
                    return "subject", f"'{word}' after topic verb"
                if gov_lemma in MEETING_VERBS or gov_lemma in MEETING_NOUNS:
                    return "actor", f"party to '{gov.text}' ('{word}')"
                return "participant", f"'{word}' {gov.text}"
            if word in TARGET_PREPS:
                return "target", f"'{word}' {gov.text}"
            if word in ON_PREPS and (gov_lemma in COERCIVE_NOUNS or gov_lemma in COERCIVE_VERBS):
                return "target", f"'{word}' after '{gov.text}'"
            if is_forum and word in PLACE_PREPS | TO_PREPS | {"at", "before", "ante", "davanti"}:
                return "institutional_context", f"'{word}' {tok.text}"
            if word in TO_PREPS and gov_lemma in AFFECTING_VERBS:
                return "affected", f"'{word}' after '{gov.text}'"
            if word in FOR_PREPS:
                return "affected", f"'{word}' {tok.text}"
            if word in PLACE_PREPS or is_place:
                return "location", f"'{word}' {tok.text}"
            return "subject", f"'{word}' {tok.text}"
        if dep in SUBJECT_DEPS or dep in PASSIVE_DEPS:
            gov_lemma = _lemma(head)
            if dep in PASSIVE_DEPS:
                return ("target" if gov_lemma in COERCIVE_VERBS else "affected"), f"passive subject of '{head.text}'"
            if gov_lemma in TOPIC_SUBJECT_VERBS:
                return "subject", f"subject of agenda verb '{head.text}'"
            if head.pos_ in ("NOUN", "PROPN") and _lemma(head) in TOPIC_HEADS:
                return "subject", f"subject of '{head.text}'"
            return "actor", f"subject of '{head.text}'"
        if dep in OBJECT_DEPS:
            gov_lemma = _lemma(head)
            if gov_lemma in TOPIC_VERBS:
                return "subject", f"object of topic verb '{head.text}'"
            if gov_lemma in COERCIVE_VERBS or gov_lemma in REQUEST_VERBS:
                return "target", f"object of '{head.text}'"
            if gov_lemma in AFFECTING_VERBS:
                return "affected", f"object of '{head.text}'"
            if is_place and gov_lemma not in MEETING_VERBS:
                return "location", f"place object of '{head.text}'"
            if gov_lemma in MEETING_VERBS:
                return "actor", f"party to '{head.text}'"
            return "participant", f"object of '{head.text}'"
        if dep in INDIRECT_DEPS:
            return ("institutional_context" if is_forum else "participant"), f"indirect object of '{head.text}'"
        if dep == "agent":
            return "actor", "passive agent"
        if dep == "ROOT":
            if tok.pos_ in ("NOUN", "PROPN") and any(c.dep_ in ("compound", "amod", "nmod") for c in tok.children):
                return "actor", "headline subject without a verb"
            return ("location" if is_place else "subject"), FALLBACK + "headline fragment"
        if dep in ("prep", "case"):
            tok = head
            continue
        break
    return ("location" if is_place else "subject"), FALLBACK + f"'{tok.dep_}' of '{tok.head.text}'"


FALLBACK = "fallback: "
FALLBACK_WEIGHT = 0.25                      # a role with no grammatical evidence counts a quarter
_GOVERNMENT_OF = __import__("re").compile(r"^(?:the\s+)?(?:government|gobierno|governo|administration)\s+(?:of|de|di|del)\s+(.+)$", 2)


def item_roles(nlp, title: str, lead: str, lang: str, normalizer, geo, source: str | None = None) -> ItemRoles:
    """Roles of the actor-capable mentions of one item's headline and lead sentence."""
    from osint_monitor.processors.institutions import item_qualifiers, registry
    from osint_monitor.processors.nlp import entity_type_of, mention_span
    from osint_monitor.processors.principals import rejection
    from osint_monitor.processors.text_normalize import clean_name, clean_text
    reg = registry()
    out = ItemRoles()
    for fld, text in (("title", title), ("lead", lead)):
        if not text:
            continue
        doc = nlp(clean_text(text)[:500])
        spans = []
        for ent in doc.ents:
            span = mention_span(ent)
            if span is None:
                continue
            etype = entity_type_of(ent.label_, span.text, lang)
            label = etype.value if etype else ("ORG" if reg.lookup(span.text) or reg.is_generic(span.text) else None)
            if label in ("PERSON", "NORP", "GPE", "ORG", "LOC", "FAC"):
                spans.append((span, label))
        qualifiers = item_qualifiers([(s.text, lab) for s, lab in spans], source)
        for span, label in spans:
            name = clean_name(span.text)
            why = rejection(span, normalizer, geo, label=label) if label in ("PERSON", "NORP", "GPE", "ORG") else None
            if why in ("reporting_outlet", "weather_system", "common_noun", "not_a_people", "affiliation"):
                continue                                   # not an actor candidate in this sentence
            inst = reg.lookup(name) or (reg.resolve_generic(name, qualifiers) if reg.is_generic(name) else None)
            if reg.is_generic(name) and inst is None:
                continue                                   # generic label the context does not resolve
            is_forum = bool(inst and inst.kind in ("MULTILATERAL_ORGANIZATION", "MULTILATERAL_FORUM", "INSTITUTIONAL_BODY"))
            gov_of = _GOVERNMENT_OF.match(name)
            if gov_of:
                name, label = gov_of.group(1), "GPE"           # "Gobierno de Irán" acts as Iran
            # countries are polities that act; only other places default to location
            is_place = label in ("LOC", "FAC") or (label == "GPE" and not inst and not geo.is_country(name))
            role, reason = clause_role(span, is_place, is_forum)
            if normalizer.is_media(name):
                role, reason = "subject", "media outlet: reports, does not act"   # publisher != actor
            multilateral = bool(inst and inst.kind in ("MULTILATERAL_ORGANIZATION", "MULTILATERAL_FORUM"))
            if multilateral and role in ("participant", "affected", "location", "subject"):
                role, reason = "institutional_context", reason + "; the organisation frames, does not act"
            if inst is not None:
                holder = inst.canonical.lower()
            elif label in ("GPE", "LOC", "FAC"):
                place = geo.canonical(name)
                acts_for = normalizer.key(name)
                state = geo.canonical(acts_for) if acts_for else None
                if role in ("actor", "target", "participant") and not geo.is_country(place):
                    if state and geo.is_country(state) and state != place:
                        holder = state                     # a capital acting stands for its state ("Tallinn accuses")
                    else:
                        holder, role, reason = place, "location", reason + "; a place does not act"
                else:
                    holder = place                          # countries: the gazetteer's canonical name
            else:
                holder = normalizer.surface(name) or name.lower()
                key = normalizer.key(name)
                if label == "NORP" and key:
                    holder = geo.canonical(key) if geo.is_country(key) else key   # "Israeli" -> israel
            out.mentions.append(Mention(span.text, holder, role, fld, reason, reason.startswith(FALLBACK)))
    return out


def _merge_person_names(weights: dict[str, dict[str, float]]) -> dict[str, dict[str, float]]:
    """One holder per identity: surface variants ("houthi" / "houthis", "irán" / "iran") merge under the
    longest name, and "hegseth" folds into "pete hegseth"."""
    from osint_monitor.processors.entity_resolver import variant_key
    names = sorted(weights, key=len, reverse=True)
    target = {}
    by_variant: dict[str, str] = {}
    for n in names:
        v = variant_key(n)
        if v in by_variant:
            target[n] = by_variant[v]
        else:
            by_variant[v] = n
    for short in names:
        if " " in short or short in target:
            continue
        full = next((n for n in names if n != short and n.split()[-1] == short and " " in n), None)
        if full:
            target[short] = full
    merged: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for name, roles in weights.items():
        for role, w in roles.items():
            merged[target.get(name, name)][role] += w
    return merged


# Multi-story documents: rolling coverage and news round-ups report several Developments in one item. Their
# mentions are not evidence of who acted in this Development (and the programme name is no actor). The
# segmentation headline forms (live, day N, round-up, briefing) plus in-brief / latest / key-developments.
_ROUNDUP = __import__("re").compile(r"\bin brief\b|\bnews in brief\b|\b(?:war|crisis) latest\b|\blatest:|"
                                    r"\bkey developments\b|\bwhat we know\b|\bnotizie in breve\b|\ben directo\b|"
                                    r"\bin diretta\b|\bminuto a minuto\b", 2)


def is_roundup(title: str) -> bool:
    from osint_monitor.processors.development_segmentation import ROLLING, headline_kind
    return headline_kind(title or "") == ROLLING or bool(_ROUNDUP.search(title or ""))


@dataclass
class DevelopmentRoles:
    roles: dict[str, str]                       # holder -> role
    weights: dict[str, dict[str, float]]        # holder -> role -> weight
    items: list[ItemRoles]
    headline_actors: set[str] = field(default_factory=set)   # holders acting in at least one headline


def development_roles(items: list[dict], normalizer=None, geo=None) -> DevelopmentRoles:
    """Roles across a Development's items. ``items``: dicts with title, lead, lang, source (and optionally
    ``roundup``: True excludes the item's mentions)."""
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.geography import Gazetteer
    from osint_monitor.processors.nlp import get_language_nlp
    normalizer = normalizer or ActorNormalizer.load()
    geo = geo or Gazetteer.load()
    weights: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    parsed = []
    for i in items:
        if i.get("roundup", is_roundup(i.get("title") or "")):
            continue                                        # a round-up is not evidence of who acted here
        lang = (i.get("lang") or "en").split()[0]
        nlp = get_language_nlp(lang)
        if nlp is None:
            continue
        r = item_roles(nlp, i.get("title") or "", i.get("lead") or "", lang, normalizer, geo, i.get("source"))
        parsed.append(r)
        seen = {}
        for m in r.mentions:
            w = (HEADLINE if m.field == "title" else LEAD) * (FALLBACK_WEIGHT if m.fallback else 1.0)
            key = (m.holder, m.role)
            seen[key] = max(seen.get(key, 0.0), w)          # an item counts once per holder and role
        for (holder, role), w in seen.items():
            weights[holder][role] += w
    headline = {m.holder for r in parsed for m in r.mentions if m.field == "title" and m.role == "actor" and not m.fallback}
    merged = _merge_person_names({**{h: dict(rs) for h, rs in weights.items()}})
    names = {h: next((m for m in merged if m == h or h in m.split()), h) for h in headline}
    roles = {h: max(rs, key=lambda r: (rs[r], -ROLE_PRIORITY.index(r))) for h, rs in merged.items()}
    return DevelopmentRoles(roles, {h: dict(r) for h, r in merged.items()}, parsed,
                            {names[h] for h in headline} & set(merged))
