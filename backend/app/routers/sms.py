import json
import logging

from fastapi import APIRouter, Depends, Form, Header, HTTPException, Request
from sqlalchemy.orm import Session

from .. import models
from ..config import settings
from ..database import get_db
from ..services.keyword_parser import (
    normalize_incoming_text,
    parse_keyword,
    parse_language_command,
)
from ..services.lesson_service import lesson_service
from ..services.sms_service import normalize_phone_e164, sms_service
from ..services.webhook_security import validate_at_webhook_request

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/sms", tags=["sms"])

MAX_INCOMING_SMS_LEN = 2000


@router.get("/logs")
def get_sms_logs(db: Session = Depends(get_db), limit: int = 20):
    return db.query(models.SMSLog).order_by(models.SMSLog.id.desc()).limit(limit).all()


@router.post("/callback")
def sms_callback(
    request: Request,
    from_: str = Form(..., alias="from"),
    to: str = Form(default=""),
    text: str = Form(...),
    date: str | None = Form(default=None),
    id_: str | None = Form(default=None, alias="id"),
    link_id: str | None = Form(default=None, alias="linkId"),
    at_webhook_token: str | None = Header(default=None, alias="X-AT-Webhook-Token"),
    db: Session = Depends(get_db),
):
    ok, err = validate_at_webhook_request(
        request.client.host if request.client else None,
        settings.at_webhook_allowed_ips,
        at_webhook_token,
        settings.at_webhook_token,
    )
    if not ok:
        raise HTTPException(status_code=403, detail=err or "Forbidden")

    try:
        sender = normalize_phone_e164(from_)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    normalized_text = normalize_incoming_text(text)[:MAX_INCOMING_SMS_LEN]
    lang_cmd = parse_language_command(normalized_text)
    keyword = parse_keyword(normalized_text)

    user = db.query(models.UserProfile).filter(models.UserProfile.phone_number == sender).first()
    if not user:
        user = models.UserProfile(phone_number=sender, preferred_language="en", notify_sms=True)
        db.add(user)
        db.commit()
        db.refresh(user)

    log_event(
        db,
        "incoming_sms",
        {
            "from": sender,
            "to": to,
            "text": normalized_text,
            "date": date,
            "provider_id": id_,
            "link_id": link_id,
        },
    )

    if lang_cmd:
        user.preferred_language = lang_cmd
        db.commit()
        replies = {"lg": "Okyusiddwa okukozesa Oluganda.", "sw": "Umebadilisha lugha kuwa Kiswahili.", "en": "Language changed to English."}
        sms_service.send_sms(db=db, user_id=user.id, to=sender, message=replies[lang_cmd])
        log_event(db, "language_change", {"sender": sender, "to": lang_cmd})
        return {"status": "success", "action": "language_change"}

    if not keyword:
        help_text = "Invalid keyword. Reply with lesson code like L91."
        sms_service.send_sms(db=db, user_id=user.id, to=sender, message=help_text)
        return {"status": "error", "message": "Invalid keyword"}

    lesson = lesson_service.get_by_code(db=db, code=keyword, language=user.preferred_language)
    if not lesson:
        help_text = f"Keyword {keyword} not found. Reply with a valid code like L91."
        sms_service.send_sms(db=db, user_id=user.id, to=sender, message=help_text)
        log_event(db, "keyword_error", {"sender": sender, "keyword": keyword})
        return {"status": "error", "message": "Keyword not found", "keyword": keyword}

    sms_logs = sms_service.send_sms(db=db, user_id=user.id, to=sender, message=lesson.content)
    first_log = sms_logs[0]
    log_event(db, "lesson_request", {"sender": sender, "keyword": keyword, "language": user.preferred_language})
    logger.info("Inbound SMS processed sender=%s keyword=%s status=%s", sender, keyword, first_log.status)
    return {"status": first_log.status, "recipient": sender, "keyword": keyword}


def log_event(db: Session, event_type: str, metadata: dict):
    db.add(models.Analytics(event_type=event_type, metadata_json=json.dumps(metadata)))
    db.commit()