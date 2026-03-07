from __future__ import annotations

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.audit.models import AuditEvent


def list_audit_events(
    db: Session,
    *,
    limit: int,
    offset: int,
    action: str | None = None,
    resource: str | None = None,
    resource_id: int | None = None,
) -> tuple[list[AuditEvent], int]:
    stmt: Select = select(AuditEvent)

    if action:
        stmt = stmt.where(AuditEvent.action == action)

    if resource:
        stmt = stmt.where(AuditEvent.resource == resource)

    if resource_id:
        stmt = stmt.where(AuditEvent.resource_id == resource_id)

    total_stmt = select(func.count()).select_from(stmt.subquery())

    stmt = stmt.order_by(AuditEvent.id.desc()).limit(limit).offset(offset)

    items = list(db.execute(stmt).scalars().all())
    total = int(db.execute(total_stmt).scalar_one())
    return items, total
