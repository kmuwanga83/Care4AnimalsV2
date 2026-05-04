import logging
import re
import time
from collections.abc import Iterable

import africastalking
from sqlalchemy.orm import Session

from app.config import settings
from app.models import SMSLog

logger = logging.getLogger(__name__)

PHONE_RE = re.compile(r"^\+[1-9]\d{6,14}$")
_DIGITS_ONLY = re.compile(r"^\d{8,15}$")


def normalize_phone_e164(raw: str) -> str:
    """
    Normalize to E.164 for storage and provider calls. AT may send +256... or 256...
    """
    s = (raw or "").strip().replace(" ", "")
    if not s:
        raise ValueError("Phone number is empty")
    if s.startswith("+"):
        if PHONE_RE.match(s):
            return s
        raise ValueError(f"Invalid international phone number: {raw!r}")
    if _DIGITS_ONLY.match(s):
        return f"+{s}"
    raise ValueError(f"Phone must be international E.164 (e.g. +2567...) got {raw!r}")


def _normalize_recipients(to: str | Iterable[str]) -> list[str]:
    recipients = [to] if isinstance(to, str) else list(to)
    cleaned = [recipient.strip() for recipient in recipients if recipient and recipient.strip()]
    invalid = [recipient for recipient in cleaned if not PHONE_RE.match(recipient)]
    if invalid:
        raise ValueError(f"Invalid international phone numbers: {', '.join(invalid)}")
    if not cleaned:
        raise ValueError("At least one recipient is required")
    return cleaned


class SMSService:
    def __init__(self) -> None:
        africastalking.initialize(settings.at_username, settings.at_api_key)
        self._client = africastalking.SMS

    def _send_with_retry(self, recipients: list[str], message: str) -> dict:
        last_error: Exception | None = None
        for attempt in range(1, settings.sms_max_retries + 1):
            try:
                if settings.at_sender_id:
                    return self._client.send(message, recipients, sender_id=settings.at_sender_id)
                return self._client.send(message, recipients)
            except Exception as exc:  # pragma: no cover - provider/network failures vary
                last_error = exc
                logger.warning("SMS send attempt %s/%s failed: %s", attempt, settings.sms_max_retries, exc)
                if attempt < settings.sms_max_retries:
                    time.sleep(settings.sms_retry_backoff_seconds * attempt)
        raise RuntimeError(f"SMS provider failed after {settings.sms_max_retries} attempts: {last_error}")

    def send_sms(self, db: Session, user_id: int, to: str | Iterable[str], message: str) -> list[SMSLog]:
        recipients = _normalize_recipients(to)
        logs: list[SMSLog] = []
        for phone in recipients:
            log_entry = SMSLog(user_id=user_id, phone_number=phone, message_body=message, status="pending")
            db.add(log_entry)
            logs.append(log_entry)
        db.commit()
        for log_entry in logs:
            db.refresh(log_entry)

        def _match_provider_row(phone: str, idx: int, rows: list[dict]) -> dict:
            if idx < len(rows) and not rows[idx].get("number"):
                return rows[idx]
            for row in rows:
                num = (row.get("number") or "").strip().replace(" ", "")
                if num == phone or num.lstrip("+") == phone.lstrip("+"):
                    return row
            if idx < len(rows):
                return rows[idx]
            return {}

        try:
            response = self._send_with_retry(recipients, message)
            provider_recipients = response.get("SMSMessageData", {}).get("Recipients", [])

            for idx, log_entry in enumerate(logs):
                provider_data = _match_provider_row(log_entry.phone_number, idx, provider_recipients)
                status = str(provider_data.get("status", "sent")).lower()
                log_entry.status = status
                log_entry.provider_message_id = provider_data.get("messageId")
                if "fail" in status or "invalid" in status:
                    log_entry.error_log = provider_data.get("status", "Provider failed to send message")
        except Exception as exc:
            logger.exception("SMS send failed for recipients=%s", recipients)
            for log_entry in logs:
                log_entry.status = "failed"
                log_entry.error_log = str(exc)

        db.commit()
        for log_entry in logs:
            db.refresh(log_entry)
            logger.info("SMS log id=%s phone=%s status=%s", log_entry.id, log_entry.phone_number, log_entry.status)
        return logs


sms_service = SMSService()