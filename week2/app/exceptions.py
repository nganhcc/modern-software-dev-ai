"""
Custom exception classes for the application.
Provides structured error handling with appropriate HTTP status codes.
"""
from __future__ import annotations


class AppException(Exception):
    """Base exception class for application-specific errors."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(AppException):
    """Raised when input validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=400)


class ResourceNotFoundError(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource_type: str, resource_id: int) -> None:
        message = f"{resource_type} with id {resource_id} not found"
        super().__init__(message, status_code=404)


class DatabaseError(AppException):
    """Raised when a database operation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=500)
