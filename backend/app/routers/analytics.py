from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, database

router = APIRouter()

@router.get("/summary")
def get_analytics_summary(db: Session = Depends(database.get_db)):
    # 1. Achievement: Query the 'lessons' table for the language split (EN, LG, SW)
    curriculum_stats = db.query(
        models.Lesson.language, 
        func.count(models.Lesson.id)
    ).group_by(models.Lesson.language).all()

    # 2. Achievement: Query the 'lessons' table for the Topic distribution
    # This identifies the focus areas like 'Vaccination', 'Safety', etc.
    topic_query = db.query(
        models.Lesson.topic, 
        func.count(models.Lesson.id)
    ).group_by(models.Lesson.topic).all()

    # Transform list of tuples into dictionaries
    stats_dict = {lang: count for lang, count in curriculum_stats}
    topic_dict = {topic: count for topic, count in topic_query}

    return {
        "metrics": {
            "total_lessons": sum(stats_dict.values()),
            "active_users": 0,
            "lesson_requests": 0
        },
        "language_stats": stats_dict,
        "topic_stats": topic_dict,  # <-- Milestone 3: Now properly exposed
        "event_breakdown": {},
        "trends": []
    }