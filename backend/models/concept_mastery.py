from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class ConceptMastery(Base):
    __tablename__ = "concept_mastery"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    concept = Column(String, index=True)
    attempts = Column(Integer, default=0)
    correct = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)
    last_seen = Column(DateTime, default=datetime.utcnow)
