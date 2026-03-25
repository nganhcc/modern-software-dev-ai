from __future__ import annotations

import logging
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from .. import db
from ..exceptions import ValidationError, DatabaseError, ResourceNotFoundError
from ..schemas import CreateNoteRequest, NoteResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get(
    "",
    response_model=List[NoteResponse],
    summary="List all notes",
)
def list_all_notes() -> List[NoteResponse]:
    """Retrieve all notes ordered by creation date (newest first)."""
    try:
        rows = db.list_notes()
        logger.info(f"Retrieved {len(rows)} notes")
        return [
            NoteResponse(
                id=row["id"],
                content=row["content"],
                created_at=row["created_at"],
            )
            for row in rows
        ]
    except DatabaseError as exc:
        logger.error(f"Database error listing notes: {exc.message}")
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
    except Exception as exc:
        logger.error(f"Unexpected error listing notes: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to list notes")


@router.post(
    "",
    response_model=NoteResponse,
    summary="Create a new note",
)
def create_note(payload: CreateNoteRequest) -> NoteResponse:
    """Create and store a new note."""
    try:
        content = payload.content.strip()
        if not content:
            raise ValidationError("Content cannot be empty")

        note_id = db.insert_note(content)
        logger.info(f"Created note with id {note_id}")

        note = db.get_note(note_id)
        if note is None:
            raise ResourceNotFoundError("note", note_id)

        return NoteResponse(
            id=note["id"],
            content=note["content"],
            created_at=note["created_at"],
        )
    except ValidationError as exc:
        logger.warning(f"Validation error: {exc.message}")
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
    except ResourceNotFoundError as exc:
        logger.error(f"Resource error: {exc.message}")
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
    except DatabaseError as exc:
        logger.error(f"Database error creating note: {exc.message}")
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
    except Exception as exc:
        logger.error(f"Unexpected error creating note: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create note")


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Get a single note",
)
def get_single_note(note_id: int) -> NoteResponse:
    """Retrieve a specific note by id."""
    try:
        row = db.get_note(note_id)
        if row is None:
            logger.warning(f"Note not found: {note_id}")
            raise ResourceNotFoundError("note", note_id)

        logger.info(f"Retrieved note {note_id}")
        return NoteResponse(
            id=row["id"],
            content=row["content"],
            created_at=row["created_at"],
        )
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
    except DatabaseError as exc:
        logger.error(f"Database error getting note: {exc.message}")
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
    except Exception as exc:
        logger.error(f"Unexpected error getting note: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve note")


