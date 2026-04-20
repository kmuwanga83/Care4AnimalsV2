from sqlalchemy import func
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter()

@router.get("/summary")
def get_summary(db: Session = Depends(database.get_db)):
    results = db.query(models.Lesson.language, func.count(models.Lesson.id))\
                .group_by(models.Lesson.language).all()
    # Returns: {"en": 136, "lg": 136, "sw": 136}
    return {lang: count for lang, count in results}