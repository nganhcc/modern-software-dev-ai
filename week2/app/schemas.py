"""
Pydantic schemas for request/response validation and API documentation.
All API contracts are defined here for type safety and OpenAPI spec generation.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ============================================================================
# Request Schemas
# ============================================================================


class ExtractActionItemsRequest(BaseModel):
    """Request payload for extracting action items using rules-based method."""

    text: str = Field(..., min_length=1, description="Notes or text to extract action items from")
    save_note: bool = Field(default=False, description="Whether to save the text as a note")


class ExtractActionItemsLLMRequest(BaseModel):
    """Request payload for extracting action items using LLM method."""

    text: str = Field(..., min_length=1, description="Notes or text to extract action items from")
    save_note: bool = Field(default=False, description="Whether to save the text as a note")


class MarkActionItemDoneRequest(BaseModel):
    """Request payload for marking an action item as done/undone."""

    done: bool = Field(default=True, description="Whether the action item is completed")


class CreateNoteRequest(BaseModel):
    """Request payload for creating a note."""

    content: str = Field(..., min_length=1, description="Note content")


# ============================================================================
# Response Schemas
# ============================================================================


class ActionItemResponse(BaseModel):
    """Response representation of an action item."""

    id: int
    note_id: Optional[int] = None
    text: str
    done: bool
    created_at: str

    class Config:
        from_attributes = True


class ExtractedActionItemResponse(BaseModel):
    """Simplified action item response during extraction (id + text only)."""

    id: int
    text: str


class NoteResponse(BaseModel):
    """Response representation of a note."""

    id: int
    content: str
    created_at: str

    class Config:
        from_attributes = True


class ExtractActionItemsResponse(BaseModel):
    """Response payload for rule-based action item extraction."""

    note_id: Optional[int] = None
    items: list[ExtractedActionItemResponse]


class ExtractActionItemsLLMResponse(BaseModel):
    """Response payload for LLM-based action item extraction with metadata."""

    note_id: Optional[int] = None
    extraction_method: str = Field(..., description="Method used: 'llm' or 'rules'")
    fallback_reason: Optional[str] = Field(None, description="Reason for fallback if applicable")
    items: list[ExtractedActionItemResponse]


class MarkActionItemDoneResponse(BaseModel):
    """Response payload for marking an action item done."""

    id: int
    done: bool


class ErrorResponse(BaseModel):
    """Standard error response format."""

    detail: str
    status_code: int
