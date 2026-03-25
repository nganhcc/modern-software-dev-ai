from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exception_handlers import http_exception_handler

from . import db
from .db import init_db
from .exceptions import AppException
from .routers import action_items, notes

# ============================================================================
# Logging Configuration
# ============================================================================

logger = logging.getLogger(__name__)


# ============================================================================
# App Factory and Configuration
# ============================================================================


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Action Item Extractor",
        description="Extract action items from notes using rules-based or LLM methods",
        version="1.0.0",
    )

    # ========================================================================
    # Lifecycle Events
    # ========================================================================

    @app.on_event("startup")
    async def startup_event() -> None:
        """Initialize database and app state on startup."""
        try:
            logger.info("Initializing database...")
            init_db()
            logger.info("Database initialized successfully")
        except Exception as exc:
            logger.error(f"Failed to initialize database: {exc}", exc_info=True)
            raise

    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        """Clean up resources on shutdown."""
        logger.info("Application shutting down")

    # ========================================================================
    # Exception Handlers
    # ========================================================================

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Any, exc: AppException) -> Dict[str, Any]:
        """Handle custom application exceptions."""
        logger.warning(f"Application error: {exc.message}")
        return {
            "detail": exc.message,
            "status_code": exc.status_code,
        }

    @app.exception_handler(HTTPException)
    async def http_exception_handler_custom(request: Any, exc: HTTPException) -> Dict[str, Any]:
        """Handle HTTP exceptions."""
        logger.warning(f"HTTP error {exc.status_code}: {exc.detail}")
        return await http_exception_handler(request, exc)

    # ========================================================================
    # Routes
    # ========================================================================

    @app.get("/", response_class=HTMLResponse, tags=["UI"])
    def index() -> str:
        """Serve the main UI."""
        html_path = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
        return html_path.read_text(encoding="utf-8")

    @app.get("/health", tags=["Health"])
    def health_check() -> Dict[str, str]:
        """Health check endpoint."""
        return {"status": "healthy"}

    # Include routers
    app.include_router(notes.router)
    app.include_router(action_items.router)

    # Mount static files
    static_dir = Path(__file__).resolve().parents[1] / "frontend"
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    return app


# ============================================================================
# App Instance
# ============================================================================

app = create_app()