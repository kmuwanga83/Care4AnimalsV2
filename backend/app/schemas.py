from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# --- SMS Schemas (RESTORED) ---
class SmsWebhookIn(BaseModel):
    # Adjust these fields if your SMS provider sends different data
    from_number: str
    to_number: str
    body: str

# --- Analytics Schemas ---
class AnalyticsBase(BaseModel):
    farmer_id: Optional[int] = None
    event_type: str
    metadata_json: Optional[str] = None

class AnalyticsCreate(AnalyticsBase):
    pass

class Analytics(AnalyticsBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# --- Topic/Lesson Schemas (Optional, but good to have) ---
class TopicBase(BaseModel):
    title: str

class LessonBase(BaseModel):
    title: str
    topic_id: int