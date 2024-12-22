"""Error handling utilities for the Finance Tracker application."""

from typing import Optional, Dict, Any, Type
from types import TracebackType
from datetime import datetime
import traceback

from .logger import error_logger


class FinanceError(Exception):
    """Base exception class for Finance Tracker application."""

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the error."""
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.details = details or {}
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary format."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
        }


class DatabaseError(FinanceError):
    """Database-related errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "DATABASE_ERROR", details)


class ValidationError(FinanceError):
    """Data validation errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "VALIDATION_ERROR", details)


class AuthenticationError(FinanceError):
    """Authentication-related errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "AUTH_ERROR", details)


class ConfigurationError(FinanceError):
    """Configuration-related errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "CONFIG_ERROR", details)


class DataImportError(FinanceError):
    """Data import-related errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "IMPORT_ERROR", details)


class DataExportError(FinanceError):
    """Data export-related errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "EXPORT_ERROR", details)


class TransactionError(FinanceError):
    """Transaction-related errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "TRANSACTION_ERROR", details)


class ErrorHandler:
    """Class for handling and managing errors in the application."""

    def __init__(self):
        """Initialize error handler."""
        self.error_mappings = {
            "DB_CONNECTION": DatabaseError,
            "VALIDATION": ValidationError,
            "AUTH": AuthenticationError,
            "CONFIG": ConfigurationError,
            "IMPORT": DataImportError,
            "EXPORT": DataExportError,
            "TRANSACTION": TransactionError,
        }

    def handle_error(
        self,
        error: Exception,
        error_type: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> FinanceError:
        """Handle and transform errors into application-specific errors."""
        context = context or {}

        # If it's already a FinanceError, just log it and return
        if isinstance(error, FinanceError):
            self._log_error(error, context)
            return error

        # Map the error to an application-specific error
        if error_type and error_type in self.error_mappings:
            mapped_error = self.error_mappings[error_type](
                str(error), details={"original_error": str(error), **context}
            )
        else:
            # Default to base FinanceError if no mapping exists
            mapped_error = FinanceError(
                str(error),
                "UNKNOWN_ERROR",
                details={"original_error": str(error), **context},
            )

        self._log_error(mapped_error, context)
        return mapped_error

    def _log_error(self, error: FinanceError, context: Dict[str, Any]):
        """Log the error with context."""
        error_logger.error(
            f"Error occurred: {error.error_code} - {error.message}",
            extra={
                "error_details": error.details,
                "context": context,
                "traceback": traceback.format_exc(),
            },
        )


class ErrorContext:
    """Context manager for handling errors in a specific context."""

    def __init__(
        self,
        context_name: str,
        error_handler: Optional[ErrorHandler] = None,
        error_type: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize error context."""
        self.context_name = context_name
        self.error_handler = error_handler or ErrorHandler()
        self.error_type = error_type
        self.context = context or {}
        self.context["context_name"] = context_name

    def __enter__(self):
        """Enter the context."""
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[Exception]],
        exc_val: Optional[Exception],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        """Exit the context and handle any errors."""
        if exc_val is not None:
            mapped_error = self.error_handler.handle_error(
                exc_val, self.error_type, self.context
            )
            raise mapped_error from exc_val
        return False


def handle_errors(
    error_type: Optional[str] = None, context: Optional[Dict[str, Any]] = None
):
    """Decorator for handling errors in functions."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            error_handler = ErrorHandler()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                mapped_error = error_handler.handle_error(
                    e,
                    error_type,
                    {
                        "function": func.__name__,
                        "args": args,
                        "kwargs": kwargs,
                        **(context or {}),
                    },
                )
                raise mapped_error from e

        return wrapper

    return decorator
