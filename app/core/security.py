from __future__ import annotations

from fastapi import Header, HTTPException, status

from app.core.config import settings


def require_api_key(x_api_key: str | None = Header(default=None)) -> str:
    """
    Simple API key auth.
    Client must send: X-API-Key: <key>
    Returns the actor string.
    """

    if not x_api_key or x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )

    return "api_key"
