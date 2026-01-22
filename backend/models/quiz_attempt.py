import uuid
from sqlalchemy import (
    Column, String, Integer, Numeric,
    JSON, TIMESTAMP, CheckConstraint, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .base import Base


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    student_id = Column(String(100), nullable=False, index=True)
    topic = Column(String(200), nullable=False, index=True)

    assessment_phase = Column(
        String(10),
        CheckConstraint("assessment_phase IN ('pre', 'post')"),
        nullable=False,
        index=True
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

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        index=True
    )

    __table_args__ = (
        # Common query accelerator:
        Index(
            "idx_student_topic_phase_time",
            "student_id",
            "topic",
            "assessment_phase",
            "created_at"
        ),
    )
