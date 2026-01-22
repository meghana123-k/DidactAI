import uuid
from sqlalchemy import (
    Column, String, Numeric, Integer,
    JSON, TIMESTAMP, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .base import Base


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    student_id = Column(String(100), nullable=False)
    topic = Column(String(200), nullable=False)

    best_accuracy = Column(Numeric(5, 2), nullable=False)
    certificate_version = Column(Integer, default=1)

    certificate_data = Column(JSON, nullable=False)

    issued_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(TIMESTAMP(timezone=True))

    __table_args__ = (
        UniqueConstraint("student_id", "topic", name="uq_student_topic"),
    )
