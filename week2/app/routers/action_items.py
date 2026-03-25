from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException

from .. import db
from ..exceptions import ValidationError, DatabaseError, ResourceNotFoundError
from ..schemas import (
    ExtractActionItemsRequest,
    ExtractActionItemsLLMRequest,
    ExtractActionItemsResponse,
    ExtractActionItemsLLMResponse,
    ActionItemResponse,
    MarkActionItemDoneRequest,
    MarkActionItemDoneResponse,
)
from ..services.extract import extract_action_items, extract_action_items_llm_with_meta

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/action-items", tags=["action-items"])


# ============================================================================
# Action Items Extraction
# ============================================================================


@router.post(
    "/extract",
    response_model=ExtractActionItemsResponse,
    summary="Extract action items using rule-based method",
)
def extract(payload: ExtractActionItemsRequest) -> ExtractActionItemsResponse:
    """Extract action items from text using rule-based heuristics."""
    try:
        text = payload.text.strip()
        if not text:
            raise ValidationError("Text cannot be empty")

        note_id: Optional[int] = None
        if payload.save_note:
            note_id = db.insert_note(text)
            logger.info(f"Created note with id {note_id}")

        items = extract_action_items(text)
        logger.info(f"Extracted {len(items)} action items")

        ids = db.insert_action_items(items, note_id=note_id)
        logger.info(f"Inserted {len(ids)} action items into database")

        return ExtractActionItemsResponse(
            note_id=note_id,
            items=[{"id": i, "text": t} for i, t in zip(ids, items)],
        )
    except ValidationError as exc:
        logger.warning(f"Validation error: {exc.message}")
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
    except DatabaseError as exc:
        logger.error(f"Database error during extraction: {exc.message}")
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
    except Exception as exc:
        logger.error(f"Unexpected error during extraction: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to extract action items")


@router.post(
    "/extract-llm",
    response_model=ExtractActionItemsLLMResponse,
    summary="Extract action items using LLM method",
)
def extract_llm(payload: ExtractActionItemsLLMRequest) -> ExtractActionItemsLLMResponse:
    """Extract action items from text using LLM with fallback to rules."""
    try:
        text = payload.text.strip()
        if not text:
            raise ValidationError("Text cannot be empty")

        note_id: Optional[int] = None
        if payload.save_note:
            note_id = db.insert_note(text)
            logger.info(f"Created note with id {note_id}")

        extraction_result = extract_action_items_llm_with_meta(text)
        items = extraction_result["items"]
        method = extraction_result["extraction_method"]
        reason = extraction_result["fallback_reason"]

        logger.info(
            f"LLM extraction completed with method={method}, "
            f"items_count={len(items)}, fallback_reason={reason}"
        )

        ids = db.insert_action_items(items, note_id=note_id)
        logger.info(f"Inserted {len(ids)} action items into database")

        return ExtractActionItemsLLMResponse(
            note_id=note_id,
            extraction_method=method,
            fallback_reason=reason,
            items=[{"id": i, "text": t} for i, t in zip(ids, items)],
        )
    except ValidationError as exc:
        logger.warning(f"Validation error: {exc.message}")
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
    except DatabaseError as exc:
        logger.error(f"Database error during LLM extraction: {exc.message}")
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
    except Exception as exc:
        logger.error(f"Unexpected error during LLM extraction: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to extract action items using LLM")


# ============================================================================
# Action Items List and Management
# ============================================================================


@router.get(
    "",
    response_model=list[ActionItemResponse],
    summary="List all action items",
)
def list_all(note_id: Optional[int] = None) -> list[ActionItemResponse]:
    """Retrieve action items, optionally filtered by note_id."""
    try:
        rows = db.list_action_items(note_id=note_id)
        logger.info(f"Retrieved {len(rows)} action items")
        return [
            ActionItemResponse(
                id=r["id"],
                note_id=r["note_id"],
                text=r["text"],
                done=bool(r["done"]),
                created_at=r["created_at"],
            )
            for r in rows
        ]
    except DatabaseError as exc:
        logger.error(f"Database error listing action items: {exc.message}")
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
    except Exception as exc:
        logger.error(f"Unexpected error listing action items: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to list action items")


@router.post(
    "/{action_item_id}/done",
    response_model=MarkActionItemDoneResponse,
    summary="Mark action item as done",
)
def mark_done(
    action_item_id: int, payload: MarkActionItemDoneRequest
) -> MarkActionItemDoneResponse:
    """Mark an action item as done or undone."""
    try:
        db.mark_action_item_done(action_item_id, payload.done)
        logger.info(f"Marked action item {action_item_id} as done={payload.done}")
        return MarkActionItemDoneResponse(id=action_item_id, done=payload.done)
    except DatabaseError as exc:
        logger.error(f"Database error marking item done: {exc.message}")
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
    except Exception as exc:
        logger.error(f"Unexpected error marking item done: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to mark action item")


