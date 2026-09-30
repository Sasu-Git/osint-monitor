"""Text and name normalisation before NER and entity resolution.

``clean_text`` prepares an item's text for NER: HTML entities decoded (also double-escaped ones), invisible
characters and non-breaking spaces removed, and feed text glued across a sentence or word boundary split
where that is safely detectable ("Thursday.Macron said", "strikesRussian"). Stored item text is never changed.

``clean_name`` turns a raw NER span into a canonical name: entities, invisible characters, quote and dash variants
unified, a leading English article (unless it is part of the name: The Hague, The Gambia), a possessive and stray
punctuation removed. Quotes and dashes are left as written in the NER text, where the model reads them.
Raw mentions stay available separately (``ItemEntity.span_text``).
"""

from __future__ import annotations

import html
import re

_INVISIBLE = re.compile("[​‌‍⁠﻿­]")
_QUOTES = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', " ": " ", " ": " "})
_SPACE_VARIANTS = str.maketrans({" ": " ", " ": " "})
_DASHES = str.maketrans({"–": "-", "—": "-", "‑": "-"})     # names only: in text a dash separates
# "Thursday.Macron", "system.The": a sentence end glued to the next sentence
_GLUED_SENTENCE = re.compile(r"(?<=[a-z]{2}[.!?])(?=[A-Z][a-z])")
# "strikesRussian": a lower-case word glued to a capitalised one (not McKinsey, iPhone, AnthropicAI)
_GLUED_WORD = re.compile(r"\b([a-z]{4,})([A-Z][a-z]{2,})\b")
_SPACES = re.compile(r"[ \t]+")

IDENTITY_ARTICLES = {"the hague", "the gambia", "the bahamas", "the netherlands antilles"}
_ARTICLE = re.compile(r"^the\s+", re.I)
_POSSESSIVE = re.compile(r"(?<=\w)'s?$|(?<=s)'$")
_EDGE = re.compile(r"^[\s\"'(\[{,;:.\-]+|[\s\"')\]},;:\-]+$")


def unescape(text: str) -> str:
    for _ in range(3):
        decoded = html.unescape(text)
        if decoded == text:
            break
        text = decoded
    return text


def clean_text(text: str | None) -> str:
    t = unescape(text or "")
    t = _INVISIBLE.sub("", t).translate(_SPACE_VARIANTS)
    t = _GLUED_SENTENCE.sub(" ", t)
    t = _GLUED_WORD.sub(r"\1 \2", t)
    return _SPACES.sub(" ", t)


def clean_name(name: str | None) -> str:
    t = clean_text(name).translate(_QUOTES).translate(_DASHES).strip()      # names only: NER reads the text as written
    t = " ".join(t.split())
    for _ in range(2):
        t = _EDGE.sub("", t)
        t = _POSSESSIVE.sub("", t)
    if _ARTICLE.match(t) and t.lower() not in IDENTITY_ARTICLES:
        t = _ARTICLE.sub("", t)
    return t.strip()
