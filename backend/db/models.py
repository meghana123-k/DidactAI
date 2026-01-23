import uuid
from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric,
    Boolean,
    Float,
    DateTime,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    JSON
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

from .base import Base


# ============================================================
# USER
# ============================================================
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ============================================================
# QUIZ (SNAPSHOT)
# ============================================================
class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    summary_mode = Column(
        String(20),
        CheckConstraint("summary_mode IN ('basic', 'conceptual', 'detailed')"),
        nullable=False
    )

    summary_source = Column(String)
    quiz_payload = Column(JSONB, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ============================================================
# QUIZ ATTEMPT (PRE / POST)
# ============================================================
class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    topic = Column(String(200), nullable=False)

    assessment_phase = Column(
        String(10),
        CheckConstraint("assessment_phase IN ('pre', 'post')"),
        nullable=False
    )

    summary_mode = Column(
        String(20),
        CheckConstraint("summary_mode IN ('basic', 'conceptual', 'detailed')"),
        nullable=False
    )

    accuracy = Column(Numeric(5, 2), nullable=False)
    total_score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)

    difficulty_analysis = Column(JSON, nullable=False)
    concept_analysis = Column(JSON, nullable=False)

    attempt_metadata = Column(JSON)
    integrity_score = Column(Numeric(5, 2))

    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ============================================================
# QUESTION RESPONSE (OPTIONAL – FUTURE ANALYTICS)
# ============================================================
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


# ============================================================
# CERTIFICATE (HIGHEST SCORE POLICY)
# ============================================================
class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    topic = Column(String(200), nullable=False)

    best_accuracy = Column(Numeric(5, 2), nullable=False)
    certificate_version = Column(Integer, default=1)

    certificate_data = Column(JSON, nullable=False)

    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("user_id", "topic", name="uq_user_topic"),
    )
