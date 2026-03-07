from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.security import require_api_key
from app.db.session import get_db
from app.schemas.audit import AuditListOut
from app.services.audit_service import list_audit_events

router = APIRouter(
    prefix="/audit", tags=["audit"], dependencies=[Depends(require_api_key)]
)


@router.get("", response_model=AuditListOut)
def list_audit_route(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    action: str | None = Query(default=None),
    resource: str | None = Query(default=None),
    resource_id: int | None = Query(default=None),
) -> AuditListOut:
    items, total = list_audit_events(
        db,
        limit=limit,
        offset=offset,
        action=action,
        resource=resource,
        resource_id=resource_id,
    )
    return {"items": items, "total": total, "limit": limit, "offset": offset}
