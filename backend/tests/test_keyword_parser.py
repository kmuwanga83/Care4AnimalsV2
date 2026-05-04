from app.services.keyword_parser import (
    normalize_incoming_text,
    parse_keyword,
    parse_language_command,
)


def test_parse_language_command():
    assert parse_language_command("lg") == "lg"
    assert parse_language_command("  ENGLISH  ") == "en"


def test_parse_keyword_extracts_code():
    assert parse_keyword(" Please send L91 lesson ") == "L91"


def test_parse_keyword_returns_none_for_invalid_input():
    assert parse_keyword("hello there") is None


def test_normalize_incoming_text_collapses_spaces():
    assert normalize_incoming_text("  hi   there  ") == "hi there"
