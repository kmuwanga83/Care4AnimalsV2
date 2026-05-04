from sqlalchemy.orm import Session

from app import models


class LessonService:
    @staticmethod
    def get_by_code(db: Session, code: str, language: str = "en") -> models.Lesson | None:
        lesson = (
            db.query(models.Lesson)
            .filter(models.Lesson.code == code.upper(), models.Lesson.language == language)
            .first()
        )
        if lesson:
            return lesson
        return (
            db.query(models.Lesson)
            .filter(models.Lesson.code == code.upper(), models.Lesson.language == "en")
            .first()
        )


lesson_service = LessonService()
