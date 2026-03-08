"""Centralized error handling utilities"""

from typing import Dict, Any, Optional
from enum import Enum


class ErrorCode(str, Enum):
    """Standard error codes"""
    # Client errors (4xx)
    BAD_REQUEST = "BAD_REQUEST"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    
    # Server errors (5xx)
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    AI_SERVICE_ERROR = "AI_SERVICE_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"


class AppError(Exception):
    """Base application error"""
    
    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.INTERNAL_ERROR,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for API response"""
        return {
            "success": False,
            "error": {
                "code": self.code.value,
                "message": self.message,
                "details": self.details
            }
        }


class ValidationError(AppError):
    """Validation error (400)"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code=ErrorCode.VALIDATION_ERROR,
            status_code=400,
            details=details
        )


class UnauthorizedError(AppError):
    """Unauthorized error (401)"""
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            message=message,
            code=ErrorCode.UNAUTHORIZED,
            status_code=401
        )


class ForbiddenError(AppError):
    """Forbidden error (403)"""
    def __init__(self, message: str = "Access denied"):
        super().__init__(
            message=message,
            code=ErrorCode.FORBIDDEN,
            status_code=403
        )


class NotFoundError(AppError):
    """Not found error (404)"""
    def __init__(self, resource: str, resource_id: Optional[str] = None):
        message = f"{resource} not found"
        if resource_id:
            message = f"{resource} with ID '{resource_id}' not found"
        super().__init__(
            message=message,
            code=ErrorCode.NOT_FOUND,
            status_code=404
        )


class ConflictError(AppError):
    """Conflict error (409)"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code=ErrorCode.CONFLICT,
            status_code=409,
            details=details
        )


class ServiceUnavailableError(AppError):
    """Service unavailable error (503)"""
    def __init__(self, service: str, message: Optional[str] = None):
        msg = message or f"{service} is temporarily unavailable"
        super().__init__(
            message=msg,
            code=ErrorCode.SERVICE_UNAVAILABLE,
            status_code=503,
            details={"service": service}
        )


class AIServiceError(AppError):
    """AI service error (503)"""
    def __init__(self, message: str = "AI service error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code=ErrorCode.AI_SERVICE_ERROR,
            status_code=503,
            details=details
        )


class DatabaseError(AppError):
    """Database error (500)"""
    def __init__(self, message: str = "Database operation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code=ErrorCode.DATABASE_ERROR,
            status_code=500,
            details=details
        )


def error_response(
    message: str,
    code: ErrorCode = ErrorCode.INTERNAL_ERROR,
    status_code: int = 500,
    details: Optional[Dict[str, Any]] = None
) -> tuple[Dict[str, Any], int]:
    """
    Create standardized error response
    
    Returns:
        Tuple of (response_dict, status_code)
    """
    return {
        "success": False,
        "error": {
            "code": code.value,
            "message": message,
            "details": details or {}
        }
    }, status_code


def success_response(data: Any, status_code: int = 200) -> tuple[Dict[str, Any], int]:
    """
    Create standardized success response
    
    Returns:
        Tuple of (response_dict, status_code)
    """
    return {
        "success": True,
        "data": data
    }, status_code
