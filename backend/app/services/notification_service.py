import logging

from sqlalchemy.orm import Session

from app import models
from app.services.email_service import email_service
from app.services.push_service import push_service
from app.services.sms_service import sms_service

logger = logging.getLogger(__name__)


def _sms_delivery_failed(status: str | None) -> bool:
    s = (status or "").lower()
    return s == "failed" or "fail" in s or "invalid" in s


class NotificationService:
    CHANNEL_ORDER = ["sms", "email", "push"]

    def send(self, db: Session, user_id: int, message: str, channels: list[str] | None = None) -> dict:
        user = db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()
        if not user:
            raise ValueError(f"User id={user_id} not found")

        requested = channels or self.CHANNEL_ORDER
        unique_ordered_channels = [channel for channel in self.CHANNEL_ORDER if channel in requested]
        attempts: list[dict] = []

        for channel in unique_ordered_channels:
            if not self._channel_enabled(user, channel):
                attempts.append({"channel": channel, "status": "skipped_preferences"})
                continue

            try:
                provider_message_id = self._dispatch_channel(db, user, channel, message)
                attempts.append({"channel": channel, "status": "sent", "provider_message_id": provider_message_id})
                return {"status": "sent", "channel": channel, "attempts": attempts}
            except Exception as exc:
                logger.warning("Notification channel failure user_id=%s channel=%s error=%s", user_id, channel, exc)
                self._log_notification(db, user.id, channel, message, "failed", str(exc), None)
                attempts.append({"channel": channel, "status": "failed", "error": str(exc)})

        return {"status": "failed", "attempts": attempts}

    @staticmethod
    def _channel_enabled(user: models.UserProfile, channel: str) -> bool:
        return {
            "sms": bool(user.notify_sms and user.phone_number),
            "email": bool(user.notify_email and user.email),
            "push": bool(user.notify_push and user.push_token),
        }.get(channel, False)

    def _dispatch_channel(self, db: Session, user: models.UserProfile, channel: str, message: str) -> str | None:
        if channel == "sms":
            sms_logs = sms_service.send_sms(db=db, user_id=user.id, to=user.phone_number, message=message)
            first = sms_logs[0]
            if _sms_delivery_failed(first.status):
                raise RuntimeError(first.error_log or "SMS failed")
            self._log_notification(db, user.id, channel, message, "sent", None, first.provider_message_id)
            return first.provider_message_id

        if channel == "email":
            provider_message_id = email_service.send_email(
                to=user.email,
                subject="Care4Animals Notification",
                body=message,
            )
            self._log_notification(db, user.id, channel, message, "sent", None, provider_message_id)
            return provider_message_id

        if channel == "push":
            provider_message_id = push_service.send(user.id, message)
            self._log_notification(db, user.id, channel, message, "sent", None, provider_message_id)
            return provider_message_id

        raise ValueError(f"Unsupported channel: {channel}")

    @staticmethod
    def _log_notification(
        db: Session,
        user_id: int,
        channel: str,
        message: str,
        status: str,
        error_log: str | None,
        provider_message_id: str | None,
    ) -> None:
        db.add(
            models.NotificationLog(
                user_id=user_id,
                channel=channel,
                message_body=message,
                status=status,
                error_log=error_log,
                provider_message_id=provider_message_id,
            )
        )
        db.commit()


notification_service = NotificationService()
