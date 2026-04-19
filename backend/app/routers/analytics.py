from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_report(report: schemas.AnalyticsCreate, db: Session = Depends(get_db)):
    new_report = models.Analytics(**report.dict())
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report
