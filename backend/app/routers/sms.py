from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
import json # New: Required for metadata logging

router = APIRouter(prefix="/sms", tags=["sms"])

@router.post("/incoming", response_model=schemas.SMSResponse)
def handle_incoming_sms(payload: schemas.SMSRequest, db: Session = Depends(get_db)):
    keyword = payload.message.strip().upper()
    sender = payload.sender

    # 1. Manage User Profile (Get or Create)
    user = db.query(models.UserProfile).filter(models.UserProfile.phone_number == sender).first()
    if not user:
        user = models.UserProfile(phone_number=sender, preferred_language="en")
        db.add(user)
        db.commit()
        db.refresh(user)

    # 2. Handle Language Switch Commands
    if keyword in ["LG", "LUGANDA"]:
        user.preferred_language = "lg"
        db.commit()
        log_event(db, "language_change", {"sender": sender, "to": "lg"})
        return {"recipient": sender, "message": "Okyusiddwa okukozesa Oluganda.", "language_detected": "lg"}
    
    if keyword in ["SW", "SWAHILI"]:
        user.preferred_language = "sw"
        db.commit()
        log_event(db, "language_change", {"sender": sender, "to": "sw"})
        return {"recipient": sender, "message": "Umebadilisha lugha kuwa Kiswahili.", "language_detected": "sw"}

    if keyword in ["EN", "ENGLISH"]:
        user.preferred_language = "en"
        db.commit()
        log_event(db, "language_change", {"sender": sender, "to": "en"})
        return {"recipient": sender, "message": "Language changed to English.", "language_detected": "en"}

    # 3. Lookup Lesson
    lesson = db.query(models.Lesson).filter(
        models.Lesson.code == keyword,
        models.Lesson.language == user.preferred_language
    ).first()

    # Fallback to English
    if not lesson:
        lesson = db.query(models.Lesson).filter(
            models.Lesson.code == keyword,
            models.Lesson.language == "en"
        ).first()

    # 4. Final Processing & Logging
    if not lesson:
        log_event(db, "keyword_error", {"sender": sender, "keyword": keyword})
        return {
            "recipient": sender, 
            "message": "Keyword not found. Text LG for Luganda, SW for Swahili.", 
            "language_detected": user.preferred_language,
            "status": "error"
        }

    # Log successful lesson request
    log_event(db, "lesson_request", {
        "sender": sender, 
        "keyword": keyword, 
        "language": user.preferred_language
    })

    return {
        "recipient": sender,
        "message": lesson.sms_text or lesson.content,
        "language_detected": user.preferred_language
    }

def log_event(db: Session, event_type: str, metadata: dict):
    """Helper function to record analytics events"""
    new_event = models.Analytics(
        event_type=event_type,
        metadata_json=json.dumps(metadata)
    )
    db.add(new_event)
    db.commit()