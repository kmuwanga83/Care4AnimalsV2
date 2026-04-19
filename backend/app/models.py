from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))

class Analytics(Base):
    __tablename__ = "analytics"
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, nullable=True)
    event_type = Column(String, index=True)
    metadata_json = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)