from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SmsWebhookIn(BaseModel):
    from_number: str
    text: str

class AnalyticsCreate(BaseModel):
    farmer_id: Optional[int] = None
    event_type: str
    metadata: Optional[str] = None

    class Config:
        from_attributes = True
