from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models import Base


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    action: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # e.g. "notes.create"

    resource: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g. "notes"
    resource_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    actor: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. "api_key"
    client_ip: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(300), nullable=True)

    meta_json: Mapped[str | None] = mapped_column(Text, nullable=True)
