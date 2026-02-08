from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine
from app.core.config import settings
from app.api.notes_api import router as notes_router

app = FastAPI(title=settings.app_name)

app.include_router(notes_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    # Basic DB connectivity check
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}
