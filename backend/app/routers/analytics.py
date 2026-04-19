from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"]
)

@router.post("/", response_model=schemas.Analytics, status_code=status.HTTP_201_CREATED)
def create_report(report: schemas.AnalyticsCreate, db: Session = Depends(get_db)):
    # .dict() is for Pydantic v1, .model_dump() for Pydantic v2. 
    # ** ensures every key in the JSON goes to the right column in the DB.
    new_report = models.Analytics(**report.dict())
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report