"""Default configuration settings for the Finance Tracker application."""

import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Database settings
DATABASE = {
    "default": {
        "ENGINE": "sqlite",
        "NAME": os.path.join(BASE_DIR, "data", "finance_tracker.db"),
    }
}

# Currency settings
DEFAULT_CURRENCY = "USD"
SUPPORTED_CURRENCIES = [
    "USD",  # US Dollar
    "EUR",  # Euro
    "GBP",  # British Pound
    "JPY",  # Japanese Yen
    "AUD",  # Australian Dollar
    "CAD",  # Canadian Dollar
    "CHF",  # Swiss Franc
    "CNY",  # Chinese Yuan
    "INR",  # Indian Rupee
]

# Date format settings
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Category color schemes
CATEGORY_COLORS = {
    "income": "#28a745",  # Green
    "expense": "#dc3545",  # Red
    "transfer": "#17a2b8",  # Blue
}

# Budget notification thresholds (percentage of budget)
BUDGET_WARNING_THRESHOLD = 80
BUDGET_DANGER_THRESHOLD = 95

# File storage settings
RECEIPT_STORAGE_PATH = os.path.join(BASE_DIR, "data", "receipts")
EXPORT_PATH = os.path.join(BASE_DIR, "data", "exports")

# Logging settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "data", "finance_tracker.log"),
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "finance_tracker": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# Report generation settings
REPORT_SETTINGS = {
    "page_size": "A4",
    "charts_per_page": 2,
    "default_chart_type": "bar",
    "chart_colors": [
        "#FF6B6B",  # Red
        "#4ECDC4",  # Turquoise
        "#45B7D1",  # Blue
        "#96CEB4",  # Green
        "#FFEEAD",  # Yellow
        "#D4A5A5",  # Pink
        "#9FA8DA",  # Purple
        "#FFE0B2",  # Orange
    ],
}

# Cache settings
CACHE_SETTINGS = {
    "BACKEND": "simple",  # Options: 'simple', 'redis', 'memcached'
    "TIMEOUT": 300,  # 5 minutes
    "OPTIONS": {
        "MAX_ENTRIES": 1000,
    },
}

# Security settings
SECURITY = {
    "PASSWORD_HASH_ALGORITHM": "bcrypt",
    "SALT_ROUNDS": 12,
    "SESSION_TIMEOUT": 3600,  # 1 hour
    "MAX_LOGIN_ATTEMPTS": 3,
    "LOCKOUT_DURATION": 300,  # 5 minutes
}

# Feature flags
FEATURES = {
    "ENABLE_CATEGORIES": True,
    "ENABLE_BUDGETS": True,
    "ENABLE_REPORTS": True,
    "ENABLE_RECEIPTS": True,
    "ENABLE_EXPORT": True,
    "ENABLE_IMPORT": True,
    "ENABLE_RECURRING": True,
    "ENABLE_NOTIFICATIONS": True,
}
