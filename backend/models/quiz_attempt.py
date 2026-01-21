from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from database import Base

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    mode = Column(String)                  # conceptual / basic / detailed
    total_score = Column(Float)
    accuracy = Column(Float)
    passed = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
