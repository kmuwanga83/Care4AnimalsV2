import pytest

from app.services.sms_service import _normalize_recipients, normalize_phone_e164


def test_normalize_phone_e164_accepts_plus_prefix():
    assert normalize_phone_e164("+256700000001") == "+256700000001"


def test_normalize_phone_e164_adds_plus_for_digits():
    assert normalize_phone_e164("256700000001") == "+256700000001"


def test_normalize_phone_e164_rejects_invalid():
    with pytest.raises(ValueError):
        normalize_phone_e164("0700000001")


def test_normalize_recipients_accepts_single_number():
    assert _normalize_recipients("+256700000001") == ["+256700000001"]


def test_normalize_recipients_accepts_bulk():
    assert _normalize_recipients(["+256700000001", " +256700000002 "]) == [
        "+256700000001",
        "+256700000002",
    ]


def test_normalize_recipients_rejects_invalid_numbers():
    with pytest.raises(ValueError):
        _normalize_recipients(["0700000001"])
