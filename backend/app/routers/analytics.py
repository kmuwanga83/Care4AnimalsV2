from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    # 1. Total count of all recorded events
    total_interactions = db.query(models.Analytics).count()

    # 2. Group events by type (e.g., how many 'lesson_request' vs 'keyword_error')
    type_counts = db.query(
        models.Analytics.event_type, 
        func.count(models.Analytics.event_type)
    ).group_by(models.Analytics.event_type).all()

    # 3. Total unique farmers/users in the system
    total_users = db.query(models.UserProfile).count()

    # 4. Break down of users by language preference
    lang_counts = db.query(
        models.UserProfile.preferred_language,
        func.count(models.UserProfile.preferred_language)
    ).group_by(models.UserProfile.preferred_language).all()

    # Final structured response for the dashboard
    return {
        "metrics": {
            "total_interactions": total_interactions,
            "active_users": total_users
        },
        "event_breakdown": {t: c for t, c in type_counts},
        "language_stats": {l: c for l, c in lang_counts}
    }