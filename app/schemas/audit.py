from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AuditEventOut(BaseModel):
    id: int
    event_time: datetime
    action: str
    resource: str
    resource_id: int | None
    actor: str
    client_ip: str | None
    user_agent: str | None
    meta_json: str | None

    model_config = {"from_attributes": True}


class AuditListOut(BaseModel):
    items: list[AuditEventOut]
    total: int
    limit: int
    offset: int
