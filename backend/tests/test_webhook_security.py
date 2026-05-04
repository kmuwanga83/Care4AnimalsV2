from app.services.webhook_security import validate_at_webhook_request


def test_validate_webhook_token_required_when_configured():
    ok, err = validate_at_webhook_request("41.203.0.0", "", None, "secret")
    assert ok is False
    assert err == "invalid webhook token"

    ok, err = validate_at_webhook_request("41.203.0.0", "", "secret", "secret")
    assert ok is True and err is None


def test_validate_webhook_ip_allowlist_when_no_token():
    ok, err = validate_at_webhook_request("41.203.210.30", "41.203.210.30", None, None)
    assert ok is True

    ok, err = validate_at_webhook_request("8.8.8.8", "41.203.210.30", None, None)
    assert ok is False
