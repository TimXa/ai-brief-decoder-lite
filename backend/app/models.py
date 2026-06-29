import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RunStatus(str, enum.Enum):
    completed = "completed"
    failed = "failed"


class DecodeRun(Base):
    __tablename__ = "decode_runs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), nullable=False)
    input_text: Mapped[str] = mapped_column(Text, nullable=False)
    structured_result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    raw_provider_output: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_code: Mapped[str | None] = mapped_column(nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
