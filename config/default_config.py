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
DEFAULT_CURRENCY = "INR"
SUPPORTED_CURRENCIES = [
    "INR",  # Indian Rupee
    "USD",  # US Dollar
    "EUR",  # Euro
    "GBP",  # British Pound
]

# Indian Tax Brackets (FY 2023-24)
TAX_BRACKETS = {
    "OLD_REGIME": [
        (250000, 0),  # Up to 2.5L: 0%
        (500000, 0.05),  # 2.5L to 5L: 5%
        (750000, 0.10),  # 5L to 7.5L: 10%
        (1000000, 0.15),  # 7.5L to 10L: 15%
        (1250000, 0.20),  # 10L to 12.5L: 20%
        (1500000, 0.25),  # 12.5L to 15L: 25%
        (float("inf"), 0.30),  # Above 15L: 30%
    ],
    "NEW_REGIME": [
        (300000, 0),  # Up to 3L: 0%
        (600000, 0.05),  # 3L to 6L: 5%
        (900000, 0.10),  # 6L to 9L: 10%
        (1200000, 0.15),  # 9L to 12L: 15%
        (1500000, 0.20),  # 12L to 15L: 20%
        (float("inf"), 0.30),  # Above 15L: 30%
    ],
}

# UPI Settings
UPI_SETTINGS = {
    "ENABLED": True,
    "PROVIDERS": ["Google Pay", "PhonePe", "Paytm", "BHIM", "Amazon Pay"],
}

# Date format settings
DATE_FORMAT = "%d-%m-%Y"  # Indian format
DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"

# Category color schemes
CATEGORY_COLORS = {
    "income": "#28a745",  # Green
    "expense": "#dc3545",  # Red
    "transfer": "#17a2b8",  # Blue
    "investment": "#ffc107",  # Yellow
    "tax": "#6c757d",  # Grey
}

# Budget notification thresholds (percentage of budget)
BUDGET_WARNING_THRESHOLD = 80
BUDGET_DANGER_THRESHOLD = 95

# Bill reminder settings
REMINDER_SETTINGS = {
    "ENABLED": True,
    "DAYS_BEFORE": 3,
    "NOTIFICATION_METHODS": ["app", "email"],
    "RECURRING_BILLS": [
        "Electricity",
        "Water",
        "Internet",
        "Phone",
        "DTH",
        "Gas",
        "Rent",
        "Insurance",
    ],
}

# File storage settings
RECEIPT_STORAGE_PATH = os.path.join(BASE_DIR, "data", "receipts")
EXPORT_PATH = os.path.join(BASE_DIR, "data", "exports")

# Receipt scanning settings
RECEIPT_SCAN_SETTINGS = {
    "ENABLED": True,
    "OCR_ENGINE": "tesseract",
    "SUPPORTED_FORMATS": ["jpg", "jpeg", "png", "pdf"],
    "AUTO_CATEGORIZE": True,
}

# Expense splitting settings
SPLIT_SETTINGS = {
    "ENABLED": True,
    "METHODS": ["EQUAL", "PERCENTAGE", "EXACT", "SHARES"],
    "SETTLEMENT_METHODS": ["UPI", "CASH", "BANK_TRANSFER"],
}

# Budget templates
BUDGET_TEMPLATES = {
    "CONSERVATIVE": {
        "Housing": 30,  # Rent/EMI
        "Transportation": 10,  # Fuel, maintenance
        "Utilities": 10,  # Electricity, water, internet
        "Groceries": 15,  # Food, household items
        "Healthcare": 10,  # Medical expenses
        "Entertainment": 5,  # Movies, dining out
        "Savings": 20,  # Investments, emergency fund
    },
    "AGGRESSIVE_SAVING": {
        "Housing": 25,
        "Transportation": 8,
        "Utilities": 8,
        "Groceries": 12,
        "Healthcare": 7,
        "Entertainment": 5,
        "Savings": 35,
    },
}

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
    "BACKEND": "simple",
    "TIMEOUT": 300,
    "OPTIONS": {
        "MAX_ENTRIES": 1000,
    },
}

# Security settings
SECURITY = {
    "PASSWORD_HASH_ALGORITHM": "bcrypt",
    "SALT_ROUNDS": 12,
    "SESSION_TIMEOUT": 3600,
    "MAX_LOGIN_ATTEMPTS": 3,
    "LOCKOUT_DURATION": 300,
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
    "ENABLE_UPI": True,
    "ENABLE_TAX_CALCULATION": True,
    "ENABLE_BILL_REMINDERS": True,
    "ENABLE_RECEIPT_SCANNING": True,
    "ENABLE_EXPENSE_SPLITTING": True,
    "ENABLE_BUDGET_TEMPLATES": True,
}
