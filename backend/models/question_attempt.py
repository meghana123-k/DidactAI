from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class QuestionAttempt(Base):
    __tablename__ = "question_attempts"

    id = Column(Integer, primary_key=True)
    quiz_attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"))
    concept = Column(String)
    difficulty = Column(String)
    selected_option = Column(String)
    correct_answer = Column(String)
    is_correct = Column(Boolean)
