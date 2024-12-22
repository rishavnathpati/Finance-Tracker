"""Logging utilities for the Finance Tracker application."""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Union, Any
from logging.handlers import RotatingFileHandler


class FinanceLogger:
    """Custom logger for the Finance Tracker application."""

    def __init__(
        self,
        name: str = "finance_tracker",
        log_file: Optional[str] = "logs/finance_tracker.log",
        level: Union[str, int] = logging.INFO,
        max_bytes: int = 5 * 1024 * 1024,  # 5 MB
        backup_count: int = 5,
        format_string: Optional[str] = None,
    ):
        """Initialize the logger."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Clear any existing handlers
        self.logger.handlers = []

        # Default format string
        if format_string is None:
            format_string = "%(asctime)s - %(levelname)s - %(message)s"

        formatter = logging.Formatter(format_string)

        # Console handler - only for ERROR and above
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.ERROR)
        console_formatter = logging.Formatter("Error: %(message)s")
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler (if log_file is specified)
        if log_file:
            # Ensure log directory exists
            log_dir = Path(log_file).parent
            log_dir.mkdir(parents=True, exist_ok=True)

            file_handler = RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            self.logger.addHandler(file_handler)

    def setLevel(self, level: Union[str, int]):
        """Set the logging level."""
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        self.logger.setLevel(level)

    def debug(self, message: str, *args, **kwargs):
        """Log debug message."""
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Log info message."""
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """Log warning message."""
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """Log error message."""
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """Log critical message."""
        self.logger.critical(message, *args, **kwargs)

    def exception(self, message: str, *args, **kwargs):
        """Log exception message."""
        self.logger.exception(message, *args, **kwargs)


class TransactionLogger(FinanceLogger):
    """Logger specifically for transaction-related events."""

    def __init__(self, *args, **kwargs):
        """Initialize transaction logger."""
        super().__init__(name="finance_tracker.transactions", *args, **kwargs)

    def log_transaction(
        self,
        transaction_type: str,
        amount: float,
        from_account: str,
        category: str,
        to_account: Optional[str] = None,
    ):
        """Log a transaction event."""
        message = (
            f"Transaction: {transaction_type} - Amount: {amount} - "
            f"From: {from_account} - Category: {category}"
        )
        if to_account:
            message += f" - To: {to_account}"

        self.info(message)


class SecurityLogger(FinanceLogger):
    """Logger specifically for security-related events."""

    def __init__(self, *args, **kwargs):
        """Initialize security logger."""
        super().__init__(name="finance_tracker.security", *args, **kwargs)

    def log_login_attempt(
        self, username: str, success: bool, ip_address: Optional[str] = None
    ):
        """Log a login attempt."""
        status = "successful" if success else "failed"
        message = f"Login {status} for user: {username}"
        if ip_address:
            message += f" from IP: {ip_address}"

        if success:
            self.info(message)
        else:
            self.warning(message)

    def log_security_event(self, event_type: str, details: str):
        """Log a security event."""
        self.warning(f"Security Event - {event_type}: {details}")


class ErrorLogger(FinanceLogger):
    """Logger specifically for error tracking and debugging."""

    def __init__(self, *args, **kwargs):
        """Initialize error logger."""
        super().__init__(name="finance_tracker.errors", *args, **kwargs)

    def log_error(self, error: Exception, context: Optional[dict] = None):
        """Log an error with context."""
        message = f"Error: {str(error)}"
        if context:
            message += f" - Context: {context}"

        self.error(message, exc_info=True)


class AuditLogger(FinanceLogger):
    """Logger for audit trail of important system events."""

    def __init__(self, *args, **kwargs):
        """Initialize audit logger."""
        super().__init__(name="finance_tracker.audit", *args, **kwargs)

    def log_data_modification(
        self, entity_type: str, entity_id: str, action: str, user: str
    ):
        """Log data modification events."""
        timestamp = datetime.now().isoformat()
        self.info(
            f"Data Modification - Time: {timestamp} - "
            f"Entity: {entity_type} - ID: {entity_id} - "
            f"Action: {action} - User: {user}"
        )

    def log_config_change(
        self, setting: str, old_value: Any, new_value: Any, user: str
    ):
        """Log configuration changes."""
        timestamp = datetime.now().isoformat()
        self.info(
            f"Config Change - Time: {timestamp} - "
            f"Setting: {setting} - Old: {old_value} - "
            f"New: {new_value} - User: {user}"
        )


class PerformanceLogger(FinanceLogger):
    """Logger for performance monitoring."""

    def __init__(self, *args, **kwargs):
        """Initialize performance logger."""
        super().__init__(name="finance_tracker.performance", *args, **kwargs)

    def log_operation_time(self, operation: str, duration_ms: float):
        """Log operation execution time."""
        self.debug(f"Operation Time - {operation}: {duration_ms}ms")

    def log_database_query(self, query: str, duration_ms: float):
        """Log database query execution time."""
        self.debug(f"Query Time - Duration: {duration_ms}ms - Query: {query}")


# Create default loggers
default_logger = FinanceLogger()
transaction_logger = TransactionLogger()
security_logger = SecurityLogger()
error_logger = ErrorLogger()
audit_logger = AuditLogger()
performance_logger = PerformanceLogger()

# Prevent propagation of logs to root logger
for logger in [
    default_logger,
    transaction_logger,
    security_logger,
    error_logger,
    audit_logger,
    performance_logger,
]:
    logger.logger.propagate = False
