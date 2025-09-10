from sqlalchemy import Column, String, TIMESTAMP, UUID, Enum
import uuid
import enum
from sqlalchemy.dialects.postgresql import JSONB

from licitabot.infrastructure.database.base import Base
from datetime import datetime, timezone


class ExecutionStatus(str, enum.Enum):
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Execution(Base):
    __tablename__ = "executions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_name = Column(String, nullable=False)
    status = Column(
        Enum(ExecutionStatus), nullable=False, default=ExecutionStatus.RUNNING
    )
    meta = Column(JSONB, nullable=True)
    result = Column(JSONB, nullable=True)
    error = Column(JSONB, nullable=True)

    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    ended_at = Column(TIMESTAMP(timezone=True), nullable=True)

    def mark_success(self, result: dict | None = None):
        self.status = ExecutionStatus.SUCCESS
        self.ended_at = datetime.now(timezone.utc)
        if result:
            self.result = result

    def mark_failed(self, error: dict | None = None):
        self.status = ExecutionStatus.FAILED
        self.ended_at = datetime.now(timezone.utc)
        if error:
            self.error = error

    def mark_cancelled(self):
        self.status = ExecutionStatus.CANCELLED
        self.ended_at = datetime.now(timezone.utc)
