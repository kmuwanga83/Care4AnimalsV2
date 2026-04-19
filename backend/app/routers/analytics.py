from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    # 1. Core Metrics (Existing)
    total_interactions = db.query(models.Analytics).count()
    total_users = db.query(models.UserProfile).count()

    # 2. Event Breakdown (Existing)
    type_counts = db.query(
        models.Analytics.event_type, 
        func.count(models.Analytics.event_type)
    ).group_by(models.Analytics.event_type).all()

    # 3. Language Statistics (Existing)
    lang_counts = db.query(
        models.UserProfile.preferred_language,
        func.count(models.UserProfile.preferred_language)
    ).group_by(models.UserProfile.preferred_language).all()

    # 4. NEW: Interaction Trends (Last 7 Days)
    # This identifies how many SMS hits you get per day
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    daily_trends = db.query(
        func.date(models.Analytics.timestamp).label("date"),
        func.count(models.Analytics.id).label("count")
    ).filter(models.Analytics.timestamp >= seven_days_ago)\
     .group_by(func.date(models.Analytics.timestamp))\
     .order_by("date").all()

    # 5. NEW: Top Requested Lessons
    # Since we store 'keyword' in metadata_json, we can extract common requests
    # For now, we'll return a placeholder or simplified logic if metadata is complex
    # A simple count of 'lesson_request' events:
    lesson_requests = db.query(models.Analytics).filter(
        models.Analytics.event_type == "lesson_request"
    ).count()

    return {
        "metrics": {
            "total_interactions": total_interactions,
            "active_users": total_users,
            "lesson_requests": lesson_requests
        },
        "event_breakdown": {t: c for t, c in type_counts},
        "language_stats": {l: c for l, c in lang_counts},
        "trends": [
            {"date": str(d.date), "count": d.count} for d in daily_trends
        ]
    }