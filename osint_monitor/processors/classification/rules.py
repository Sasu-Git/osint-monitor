"""Deterministic, keyword-based development classifier.

Free, offline and reproducible. It is the default backend, the fallback when the
LLM classifier fails, and the reference implementation for tests. It reads
headlines first (they are compact and factual) and only falls back to full text
when no headline matches.

It does not judge significance or write assessments: significance_class stays
None and why_it_matters stays empty.
"""

from __future__ import annotations

import re

from osint_monitor.core.config import DevelopmentTypeDefaults, load_development_types
from osint_monitor.core.models import (
    ClusterContext,
    Concreteness,
    DevelopmentClassification,
    EventType,
    InteractionMode,
    UncertaintyFlag,
)
from osint_monitor.processors.classification.base import context_flags, entities_by_kind


def _rx(pattern: str) -> re.Pattern:
    return re.compile(pattern, re.IGNORECASE)


# Headlines that are opinion/analysis/spokesperson remarks, whatever their topic.
COMMENTARY_TITLE = _rx(
    r"\b(?:analysis|opinion|op-ed|editorial|commentary|explainer|"
    r"spokes(?:person|man|woman)|told reporters|reiterat\w*|"
    r"analysts? (?:say|said|warn)|experts? (?:say|said))\b|^what\b"
)

# Clauses naming a topic of discussion ("meets X to discuss sanctions") are removed
# before type matching, so the topic does not become the event type.
DISCUSSION_CLAUSE = _rx(r"\b(?:to discuss|discuss(?:es|ed|ing)?|over|about|regarding|ahead of)\b[^.,;:]*")

# Ordered: the first matching rule wins. Decisive, verb-anchored actions come first,
# then meetings, then policy, then rhetoric.
TYPE_RULES: list[tuple[EventType, re.Pattern]] = [
    (EventType.CEASEFIRE, _rx(r"\b(?:ceasefire|cease-fire|truce|cessation of hostilities|armistice)\b")),
    (EventType.TREATY, _rx(r"\btreaty\b")),
    (EventType.ARMS_TRANSFER, _rx(
        r"\b(?:arms|weapons) (?:sale|deal|package|deliver\w*|shipment)s?\b|\bmilitary aid\b")),
    (EventType.AGREEMENT, _rx(
        r"\b(?:sign(?:s|ed)?|agree(?:s|d)?|reach(?:es|ed)?|seal(?:s|ed)?|conclude[sd]?|strike[sd]?|struck)\b"
        r"[^.;]{0,40}\b(?:agreement|deal|accord|memorandum|mou|pact)\b"
        r"|\bagree(?:s|d)? (?:to|on)\b|\b(?:agreement|deal|accord|pact) (?:signed|reached|agreed)\b")),
    (EventType.ELECTION, _rx(
        r"\b(?:elections?|re-elected|referendum|(?:wins?|won) (?:the )?(?:vote|presidency|election))\b")),
    (EventType.RESIGNATION, _rx(
        r"\b(?:resign(?:s|ed|ation)?|steps? down|stepped down|sack(?:s|ed)|ousted|removed from (?:office|post))\b"
        r"|\bdismiss(?:es|ed)\b(?! (?:the )?(?:reports?|claims?|allegations?))")),
    (EventType.APPOINTMENT, _rx(r"\b(?:appoint(?:s|ed|ment)?|sworn in|nominat(?:es|ed|ion)|named (?:as )?(?:the )?new)\b")),
    (EventType.SANCTIONS, _rx(r"\bsanction(?:s|ed|ing)?\b|\bdesignat(?:es|ed|ion)\b|\basset freezes?\b|\bblacklist(?:s|ed)?\b")),
    (EventType.ECONOMIC_ACTION, _rx(
        r"\b(?:tariffs?|export controls?|export ban|import ban|embargo|aid package|trade restrictions?)\b")),
    (EventType.MILITARY_EXERCISE, _rx(r"\b(?:military|naval|joint) exercises?\b|\bdrills?\b|\bwar ?games\b")),
    (EventType.MILITARY_ACTION, _rx(
        r"\b(?:air ?strikes?|strikes? (?:on|against)|struck|shell(?:ing|ed)|bombard\w*|bomb(?:ing|ed|s)|"
        r"(?:missile|drone|rocket) (?:attack|strike)s?|attack(?:s|ed)?|offensive|invade[sd]?|invasion|"
        r"launche[sd] (?:missiles|rockets|drones))\b")),
    (EventType.DEPLOYMENT, _rx(
        r"\b(?:re)?deploy(?:s|ed|ment|ing)?\b|\b(?:sends?|sent) (?:troops|warships|forces|jets)\b"
        r"|\bdispatch(?:es|ed)\b|\bcarrier strike group\b")),
    (EventType.SUMMIT, _rx(r"\bsummit\b")),
    (EventType.NEGOTIATION, _rx(
        r"\bnegotiat\w*|\bround of talks\b|\b(?:peace|nuclear|trade|ceasefire|indirect|direct) talks\b"
        r"|\btalks (?:resume|resumed|continue|stall\w*|collapse\w*)\b")),
    (EventType.DIPLOMATIC_VISIT, _rx(
        r"\b(?:state visit|official visit|visits|visited|visit to|arrive[sd]? in|trip to|tour of)\b")),
    (EventType.BILATERAL_MEETING, _rx(
        r"\b(?:met|meets?|meeting|h(?:o|e)lds? (?:[\w-]+ )?talks|talks with|hosted|hosts|"
        r"welcomed|phone call|phoned|spoke by phone|by phone|call with|video ?call|videoconference|"
        r"spoke (?:with|to))\b")),
    (EventType.NEGOTIATION, _rx(r"\btalks\b")),
    (EventType.POLICY_CHANGE, _rx(
        r"\b(?:executive order|decree|new law|signed into law|bill|legislation|new (?:policy|rules?)|"
        r"policy change|regulations?|reform|bans?|banned|to ban|takes? effect|took effect|"
        r"(?:comes?|came|enters?|entered) into force)\b")),
    (EventType.THREAT, _rx(
        r"\bthreaten(?:s|ed)?\b|\bvow(?:s|ed)? to (?:retaliate|respond|strike)\b|\bwill (?:retaliate|respond)\b")),
    (EventType.WARNING, _rx(r"\bwarn(?:s|ed|ing)?\b|\bcaution(?:s|ed)?\b")),
]
# Only matched against headlines: "said" appears in almost every article body.
STATEMENT_TITLE = _rx(r"\b(?:said|says|stated|declare[sd]|announce[sd]|statement|addresse[sd])\b")

# Completed vs planned. Headlines use the present tense for completed events.
COMPLETION = _rx(
    r"\b(?:met|meets|held|holds|hosted|hosts|signed|signs|agreed|agrees|reached|reaches|imposed|imposes|"
    r"designated|designates|struck|strikes|launched|launches|deployed|deploys|arrived|arrives|visited|visits|"
    r"took effect|takes effect|(?:came|comes|entered|enters) into force|enacted|passed|approved|adopted|won|"
    r"wins|resigned|resigns|appointed|appoints|sworn in|spoke|speaks|phoned|killed|seized|froze|freezes|"
    r"issued|issues)\b"
)
FUTURE = _rx(
    r"\b(?:will|to (?:meet|visit|sign|impose|hold|travel|introduce|ban)|plans? to|planning to|intends? to|"
    r"expected to|set to|scheduled to|poised to|propose[sd]?|proposal|considering|considers|could|mulls?|"
    r"weighs?|upcoming|next week|threaten\w*|announce[sd]? (?:a )?plans?)\b"
)
AGREED = _rx(
    r"\b(?:sign(?:s|ed)?|agree(?:s|d)?|reach(?:es|ed)?|seal(?:s|ed)?|conclude[sd]?|announce[sd]?|"
    r"takes? effect|took effect|in effect|into force|holds|holding|ratif\w+|brokered|struck)\b"
)
TALKS = _rx(r"\b(?:talks|negotiat\w*|proposal|propose[sd]?|push(?:es)? for|seek(?:s|ing)?|mediat\w*)\b")
CALLS_FOR = _rx(r"\b(?:call(?:s|ed)? for|urge[sd]?|demand(?:s|ed)?|appeal(?:s|ed)? for)\b")
SANCTION_IMPOSED = _rx(
    r"\b(?:impose[sd]?|imposing|slap(?:s|ped)?|announce[sd]? (?:new |fresh |further )?sanctions|"
    r"sanctions? (?:on|against)|designat(?:es|ed)|blacklist(?:s|ed)|froze|freezes|extend(?:s|ed)|"
    r"expand(?:s|ed)|adds?|added)\b"
)
POLICY_IMPLEMENTED = _rx(
    r"\b(?:takes? effect|took effect|into force|enacted|signed into law|signs?|signed|passe[sd]|"
    r"approve[sd]|adopt(?:s|ed)|issue[sd]|implement(?:s|ed)|introduce[sd]|bans|banned)\b"
)

VIDEO = _rx(r"\b(?:video ?call|videoconference|video conference|video link|virtual (?:meeting|summit|talks)|online meeting|by video)\b")
PHONE = _rx(r"\b(?:phone ?call|telephone|spoke by phone|by phone|phoned|over the phone|call with|calls? between)\b")
PHYSICAL = _rx(
    r"\b(?:in-person|face-to-face|face to face|hosted|hosts|arrive[sd]? in|visit(?:ed|s)?|welcomed|"
    r"shook hands|on the sidelines)\b"
)
# Case-sensitive: "met ... in Muscat" (a capitalised place after "in").
MET_IN_PLACE = re.compile(r"\b(?:[Mm]et|[Mm]eets?|[Mm]eeting|[Tt]alks|[Ss]ummit)\b[^.;]{0,60}\bin [A-Z]")
MULTILATERAL = _rx(
    r"\b(?:g7|g20|brics|asean|(?:foreign|defen[cs]e|finance) ministers|ministerial|multilateral|trilateral|leaders of)\b"
)
DENIAL = _rx(
    r"\b(?:den(?:y|ies|ied)|rejects? (?:the )?reports?|dismiss(?:es|ed) (?:the )?reports?|false reports?|"
    r"did not take place|never happened|no such (?:meeting|talks|agreement|deal))\b"
)

MEETING_TYPES = {
    EventType.BILATERAL_MEETING, EventType.MULTILATERAL_MEETING, EventType.SUMMIT,
    EventType.NEGOTIATION, EventType.DIPLOMATIC_VISIT,
}
RHETORIC_TYPES = {
    EventType.SIGNIFICANT_STATEMENT, EventType.THREAT, EventType.WARNING,
    EventType.COMMENTARY, EventType.OTHER, EventType.UNKNOWN,
}
AGREEMENT_TYPES = {EventType.AGREEMENT, EventType.TREATY, EventType.CEASEFIRE}


class RuleBasedClassifier:
    """Keyword/regex classifier. Deterministic: same context, same result."""

    name = "rules"

    def __init__(self, type_defaults: dict[EventType, DevelopmentTypeDefaults] | None = None):
        self._defaults = type_defaults or load_development_types()

    def classify(self, context: ClusterContext) -> DevelopmentClassification:
        titles = " \n".join(i.title for i in context.items)
        full_text = " \n".join(f"{i.title} {i.excerpt}" for i in context.items)
        notes: list[str] = []
        flags = context_flags(context)

        event_type, matched = self._match_type(titles, full_text)
        notes.append(f"matched '{matched}'" if matched else "no rule matched")

        planned = bool(FUTURE.search(titles)) and not COMPLETION.search(titles)
        event_type, concreteness = self._concreteness(event_type, titles, full_text, planned, flags, notes)

        defaults = self._defaults.get(event_type) or self._defaults[EventType.UNKNOWN]
        mode = defaults.interaction_mode
        if event_type in MEETING_TYPES:
            if event_type == EventType.BILATERAL_MEETING and MULTILATERAL.search(full_text):
                event_type = EventType.MULTILATERAL_MEETING
            mode = self._interaction_mode(event_type, titles, full_text)
            if mode == InteractionMode.UNKNOWN:
                flags.append(UncertaintyFlag.INTERACTION_MODE_UNCLEAR)

        if any(DENIAL.search(f"{i.title} {i.excerpt}") for i in context.items):
            flags.append(UncertaintyFlag.CONTRADICTORY_REPORTS)
            notes.append("an item denies the report")

        actors, countries, orgs = entities_by_kind(context)
        if event_type in MEETING_TYPES and not actors and len(countries) < 2:
            flags.append(UncertaintyFlag.ACTORS_UNCLEAR)
        if event_type == EventType.UNKNOWN:
            flags.append(UncertaintyFlag.INSUFFICIENT_CONTEXT)

        return DevelopmentClassification(
            event_type=event_type,
            event_domain=defaults.domain,
            interaction_mode=mode,
            concreteness=concreteness,
            significance_class=None,
            actors=actors,
            countries=countries,
            organizations=orgs,
            location=context.location_name,
            material_change=context.items[0].title if context.items else "",
            why_it_matters="",
            is_routine_commentary=event_type == EventType.COMMENTARY,
            classification_notes="Rules: " + "; ".join(notes),
            uncertainty_flags=flags,
            classifier=self.name,
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _match_type(titles: str, full_text: str) -> tuple[EventType, str]:
        commentary = COMMENTARY_TITLE.search(titles)
        if commentary:
            return EventType.COMMENTARY, commentary.group(0)

        stripped_titles = DISCUSSION_CLAUSE.sub(" ", titles)
        for event_type, pattern in TYPE_RULES:
            m = pattern.search(stripped_titles)
            if m:
                return event_type, m.group(0)
        statement = STATEMENT_TITLE.search(stripped_titles)
        if statement:
            return EventType.SIGNIFICANT_STATEMENT, statement.group(0)

        stripped_text = DISCUSSION_CLAUSE.sub(" ", full_text)
        for event_type, pattern in TYPE_RULES:
            m = pattern.search(stripped_text)
            if m:
                return event_type, m.group(0)
        return EventType.UNKNOWN, ""

    def _concreteness(
        self,
        event_type: EventType,
        titles: str,
        full_text: str,
        planned: bool,
        flags: list[UncertaintyFlag],
        notes: list[str],
    ) -> tuple[EventType, Concreteness]:
        defaults = self._defaults.get(event_type) or self._defaults[EventType.UNKNOWN]

        if event_type in RHETORIC_TYPES:
            return event_type, defaults.concreteness

        if planned:
            flags.append(UncertaintyFlag.UNCONFIRMED_COMPLETION)
            notes.append("reported as planned, not completed")
            return event_type, Concreteness.DECLARATION

        if event_type in AGREEMENT_TYPES:
            if AGREED.search(titles):
                return event_type, Concreteness.AGREEMENT
            if TALKS.search(full_text):
                notes.append("talks without a reported outcome")
                return EventType.NEGOTIATION, Concreteness.NEGOTIATION
            if CALLS_FOR.search(titles):
                notes.append("call for, not an agreement")
                return EventType.SIGNIFICANT_STATEMENT, Concreteness.DECLARATION
            flags.append(UncertaintyFlag.INSUFFICIENT_CONTEXT)
            return event_type, Concreteness.UNKNOWN

        if event_type == EventType.SANCTIONS and not SANCTION_IMPOSED.search(titles):
            flags.append(UncertaintyFlag.UNCONFIRMED_COMPLETION)
            notes.append("sanctions mentioned but not reported as imposed")
            return event_type, Concreteness.DECLARATION

        if event_type == EventType.POLICY_CHANGE and not POLICY_IMPLEMENTED.search(titles):
            flags.append(UncertaintyFlag.UNCONFIRMED_COMPLETION)
            notes.append("policy announced, implementation not reported")
            return event_type, Concreteness.DECLARATION

        return event_type, defaults.concreteness

    @staticmethod
    def _interaction_mode(event_type: EventType, titles: str, full_text: str) -> InteractionMode:
        if VIDEO.search(full_text):
            return InteractionMode.VIDEO
        if PHONE.search(full_text):
            return InteractionMode.TELEPHONE
        if PHYSICAL.search(full_text) or MET_IN_PLACE.search(full_text):
            return InteractionMode.PHYSICAL
        if event_type in (EventType.DIPLOMATIC_VISIT, EventType.SUMMIT):
            return InteractionMode.PHYSICAL
        return InteractionMode.UNKNOWN
