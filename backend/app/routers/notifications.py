from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..services.lesson_service import lesson_service
from ..services.notification_service import notification_service
from ..services.reminder_service import reminder_service

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])


@router.post("/send")
def send_notification(payload: schemas.NotificationRequest, db: Session = Depends(get_db)):
    try:
        return notification_service.send(
            db=db,
            user_id=payload.user_id,
            message=payload.message,
            channels=payload.channels,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/reminders")
def send_reminder(payload: schemas.ReminderRequest, db: Session = Depends(get_db)):
    if payload.reminder_type == "lesson" and payload.lesson_code:
        lesson = lesson_service.get_by_code(db=db, code=payload.lesson_code)
        if lesson:
            reminder_message = f"Lesson reminder: {lesson.content}"
        else:
            reminder_message = f"Lesson reminder: code {payload.lesson_code} was not found."
    else:
        reminder_message = f"System reminder: {payload.reminder_type}"

    return reminder_service.send_lesson_reminder(db=db, user_id=payload.user_id, message=reminder_message)
