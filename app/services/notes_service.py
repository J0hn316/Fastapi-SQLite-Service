from __future__ import annotations
from fastapi import Request

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.db.models import Note
from app.audit.logger import log_audit_event
from app.schemas.notes_schemas import NoteCreate, NoteUpdate


def create_note(db: Session, data: NoteCreate, *, actor: str, request: Request) -> Note:
    note = Note(
        title=data.title,
        content=data.content,
        tags=data.tags,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    log_audit_event(
        db,
        action="notes.create",
        resource="notes",
        resource_id=note.id,
        actor=actor,
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        meta={"title": note.title, "tags": note.tags},
    )

    db.commit()
    return note


def get_note(db: Session, note_id: int) -> Note | None:
    return db.get(Note, note_id)


def list_notes(
    db: Session, *, limit: int, offset: int, q: str | None = None
) -> tuple[list[Note], int]:
    stmt: Select = select(Note)

    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            or_(
                Note.title.ilike(like),
                Note.content.ilike(like),
                Note.tags.ilike(like),
            )
        )

    total_stmt = select(func.count()).select_from(stmt.subquery())

    stmt = stmt.order_by(Note.updated_at.desc()).limit(limit).offset(offset)

    items = list(db.execute(stmt).scalars().all())
    total = int(db.execute(total_stmt).scalar_one())

    return items, total


def update_note(
    db: Session, note: Note, data: NoteUpdate, *, actor: str, request: Request
) -> Note:
    before = {"title": note.title, "content": note.content, "tags": note.tags}

    if data.title is not None:
        note.title = data.title
    if data.content is not None:
        note.content = data.content
    if data.tags is not None:
        note.tags = data.tags

    db.commit()
    db.refresh(note)

    after = {"title": note.title, "content": note.content, "tags": note.tags}

    log_audit_event(
        db,
        action="notes.update",
        resource="notes",
        resource_id=note.id,
        actor=actor,
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        meta={"before": before, "after": after},
    )

    db.commit()
    return note


def delete_note(db: Session, note: Note, *, actor: str, request: Request) -> None:
    note_id = note.id
    meta = {"title": note.title, "tags": note.tags}

    db.delete(note)
    db.commit()

    log_audit_event(
        db,
        action="notes.delete",
        resource="notes",
        resource_id=note_id,
        actor=actor,
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        meta=meta,
    )

    db.commit()
