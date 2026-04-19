from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base  # <--- THIS IS THE MISSING PIECE

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    preferred_language = Column(String, default="en")
    last_interaction = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    title = Column(String)
    content = Column(Text)
    language = Column(String, index=True)
    theme = Column(String, nullable=True)
    sms_text = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# ... Keep your Analytics and other models below ...
# backend/app/models.py

class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String)  # e.g., 'lesson_request'
    metadata_json = Column(Text) # To store JSON data
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

# ... keep UserProfile and Lesson models below ...