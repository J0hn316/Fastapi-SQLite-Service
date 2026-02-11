from __future__ import annotations

import json
from typing import Any

from sqlalchemy.orm import Session

from app.audit.models import AuditEvent


def log_audit_event(
    db: Session,
    *,
    action: str,
    resource: str,
    resource_id: int | None,
    actor: str,
    client_ip: str | None = None,
    user_agent: str | None = None,
    meta: dict[str, Any] | None = None,
) -> AuditEvent:
    """
    Insert an audit event row. Caller controls transaction boundaries (commit happens elsewhere).
    """
    event = AuditEvent(
        action=action,
        resource=resource,
        resource_id=resource_id,
        actor=actor,
        client_ip=client_ip,
        user_agent=user_agent,
        meta_json=json.dumps(meta, ensure_ascii=False) if meta else None,
    )

    db.add(event)
    return event
