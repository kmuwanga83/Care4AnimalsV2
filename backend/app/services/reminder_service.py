from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.services.notification_service import notification_service


class ReminderService:
    def send_lesson_reminder(self, db: Session, user_id: int, message: str) -> dict:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        reminder = f"[Reminder {timestamp}] {message}"
        return notification_service.send(db=db, user_id=user_id, message=reminder, channels=["sms", "email", "push"])


reminder_service = ReminderService()
