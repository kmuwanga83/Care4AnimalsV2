from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database  # Using relative imports based on your structure

router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["analytics"]
)

@router.post("/events")
async def create_event(
    event_type: str, 
    platform: str, 
    lesson_id: str = None, 
    db: Session = Depends(database.get_db)
):
    new_event = models.AnalyticsEvent(
        event_type=event_type,
        platform=platform,
        lesson_id=lesson_id
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return {"status": "success", "event_id": new_event.id}