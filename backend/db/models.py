import uuid

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Integer,
    Float,
    Boolean
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    mode = Column(String, nullable=False)
    summary_source = Column(String)
    quiz_payload = Column(JSONB, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    attempt_number = Column(Integer, nullable=False)
    mode = Column(String, nullable=False)

    total_score = Column(Integer)
    max_score = Column(Integer)
    accuracy = Column(Float)
    passed = Column(Boolean)

    analytics_snapshot = Column(JSONB)
    difficulty_progress = Column(JSONB)
    concept_progress = Column(JSONB)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class QuestionResponse(Base):
    __tablename__ = "question_responses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    attempt_id = Column(
        UUID(as_uuid=True),
        ForeignKey("quiz_attempts.id"),
        nullable=False
    )

    question_id = Column(String, nullable=False)
    concept = Column(String)
    difficulty = Column(String)

    selected_option = Column(String)
    correct_option = Column(String)
    is_correct = Column(Boolean)

    time_taken = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
