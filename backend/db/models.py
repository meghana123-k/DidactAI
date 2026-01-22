import uuid
from sqlalchemy import Column, String, Numeric, TIMESTAMP, UniqueConstraint, JSON
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

    student_id = Column(String(100), nullable=False)
    topic = Column(String(200), nullable=False)

    mode = Column(String(20), nullable=False)  # pre / post

    accuracy = Column(Numeric(5, 2), nullable=False)
    total_score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)

    difficulty_analysis = Column(JSON, nullable=False)
    concept_analysis = Column(JSON, nullable=False)

    attempt_metadata = Column(JSON)
    integrity_score = Column(Numeric(5, 2))

    created_at = Column(TIMESTAMP, server_default=func.now())


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



class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    student_id = Column(String(100), nullable=False)
    topic = Column(String(200), nullable=False)

    best_accuracy = Column(Numeric(5, 2), nullable=False)
    issued_at = Column(TIMESTAMP, server_default=func.now())

    certificate_data = Column(JSON, nullable=False)

    __table_args__ = (
        UniqueConstraint("student_id", "topic", name="uq_student_topic"),
    )