from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, database

router = APIRouter()

@router.get("/summary")
def get_analytics_summary(db: Session = Depends(database.get_db)):
    # Query the 'lessons' table for the 136-136-136 split
    curriculum_stats = db.query(
        models.Lesson.language, 
        func.count(models.Lesson.id)
    ).group_by(models.Lesson.language).all()

    # Transform list of tuples into a dictionary
    stats_dict = {lang: count for lang, count in curriculum_stats}

    return {
        "metrics": {
            "total_lessons": sum(stats_dict.values()),
            "active_users": 0,
            "lesson_requests": 0
        },
        "language_stats": stats_dict,
        "event_breakdown": {},
        "trends": []
    }
