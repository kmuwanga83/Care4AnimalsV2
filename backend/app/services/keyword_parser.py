import re

KEYWORD_RE = re.compile(r"\b([A-Z]{1,4}\d{1,4})\b")

LANGUAGE_ALIASES: dict[str, str] = {
    "LG": "lg",
    "LUGANDA": "lg",
    "SW": "sw",
    "SWAHILI": "sw",
    "EN": "en",
    "ENGLISH": "en",
}


def normalize_incoming_text(text: str) -> str:
    return " ".join((text or "").strip().split())


def parse_keyword(text: str) -> str | None:
    normalized = normalize_incoming_text(text).upper()
    match = KEYWORD_RE.search(normalized)
    return match.group(1) if match else None


def parse_language_command(text: str) -> str | None:
    """If the message is only a language switch keyword, return preferred lang code (lg/sw/en)."""
    normalized = normalize_incoming_text(text).upper()
    return LANGUAGE_ALIASES.get(normalized)
