from app.services.notification_service import NotificationService


class DummyUser:
    def __init__(self):
        self.id = 1
        self.phone_number = "+256700000001"
        self.email = "user@example.com"
        self.push_token = "push-token"
        self.notify_sms = True
        self.notify_email = True
        self.notify_push = True


def test_channel_enabled_respects_preferences():
    user = DummyUser()
    service = NotificationService()
    assert service._channel_enabled(user, "sms") is True
    assert service._channel_enabled(user, "email") is True
    assert service._channel_enabled(user, "push") is True

    user.notify_sms = False
    user.notify_email = False
    user.notify_push = False
    assert service._channel_enabled(user, "sms") is False
    assert service._channel_enabled(user, "email") is False
    assert service._channel_enabled(user, "push") is False
