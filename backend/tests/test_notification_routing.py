from unittest.mock import MagicMock, patch

from app.services.notification_service import NotificationService


def test_fallback_to_email_when_sms_fails():
    db = MagicMock()
    user = MagicMock()
    user.id = 1
    user.phone_number = "+256700000001"
    user.email = "farmer@example.com"
    user.push_token = None
    user.notify_sms = True
    user.notify_email = True
    user.notify_push = False

    db.query.return_value.filter.return_value.first.return_value = user

    failed_sms = MagicMock()
    failed_sms.status = "failed"
    failed_sms.error_log = "gateway down"
    failed_sms.provider_message_id = None

    with patch(
        "app.services.notification_service.sms_service.send_sms",
        return_value=[failed_sms],
    ):
        with patch(
            "app.services.notification_service.email_service.send_email",
            return_value="email-sent",
        ):
            svc = NotificationService()
            result = svc.send(db, 1, "Hello", ["sms", "email"])

    assert result["status"] == "sent"
    assert result["channel"] == "email"
