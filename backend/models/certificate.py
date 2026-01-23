import uuid
from sqlalchemy import (
    Column,
    String,
    Numeric,
    Integer,
    JSON,
    TIMESTAMP,
    UniqueConstraint,
    CheckConstraint,
    Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .base import Base


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(String(100), nullable=False)
    topic = Column(String(200), nullable=False)

    best_accuracy = Column(
        Numeric(5, 2),
        nullable=False
    )

    certificate_version = Column(Integer, default=1, nullable=False)

    certificate_data = Column(JSON, nullable=False)

    issued_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        onupdate=func.now()
    )

    __table_args__ = (
        # Enforce highest-score-per-topic-per-student
        UniqueConstraint("user_id", "topic", name="uq_student_topic"),

        # Accuracy must be valid percentage
        CheckConstraint(
            "best_accuracy >= 0 AND best_accuracy <= 100",
            name="ck_certificate_accuracy_range"
        ),

        # Performance index (very important)
        Index("idx_certificate_student_topic", "user_id", "topic"),
    )
