"""Configuration management utilities."""

import json
import os
from typing import Dict, Any

from .logger import FinanceLogger

# Initialize logger
logger = FinanceLogger(name="finance_tracker.config", log_file="logs/config.log")

DEFAULT_CONFIG = {
    "database": {"type": "sqlite", "path": "data/finance_tracker.db"},
    "logging": {
        "level": "INFO",
        "file": "logs/finance_tracker.log",
        "max_size": 5242880,  # 5MB
        "backup_count": 5,
    },
    "currency": {"default": "USD", "display_symbol": "$"},
    "date_format": "%Y-%m-%d",
    "export": {"default_format": "csv", "path": "data/exports"},
    "receipts": {
        "path": "data/receipts",
        "allowed_extensions": [".jpg", ".jpeg", ".png", ".pdf"],
    },
}

CONFIG_FILE = "config/config.json"


def load_config() -> Dict[str, Any]:
    """Load configuration from file."""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return create_default_config()
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        return DEFAULT_CONFIG


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file."""
    try:
        # Ensure config directory exists
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

        logger.info("Configuration saved successfully")
    except Exception as e:
        logger.error(f"Error saving config: {str(e)}")
        raise


def create_default_config() -> Dict[str, Any]:
    """Create and save default configuration."""
    try:
        save_config(DEFAULT_CONFIG)
        logger.info("Default configuration created")
        return DEFAULT_CONFIG
    except Exception as e:
        logger.error(f"Error creating default config: {str(e)}")
        raise


def get_config_value(key: str, default: Any = None) -> Any:
    """Get a configuration value by key."""
    config = load_config()
    keys = key.split(".")

    try:
        value = config
        for k in keys:
            value = value[k]
        return value
    except (KeyError, TypeError):
        logger.warning(f"Config key '{key}' not found, using default: {default}")
        return default


def update_config_value(key: str, value: Any) -> None:
    """Update a configuration value."""
    config = load_config()
    keys = key.split(".")

    # Navigate to the correct level
    current = config
    for k in keys[:-1]:
        if k not in current:
            current[k] = {}
        current = current[k]

    # Update the value
    current[keys[-1]] = value
    save_config(config)
    logger.info(f"Updated config key '{key}' to '{value}'")


def reset_config() -> None:
    """Reset configuration to defaults."""
    try:
        create_default_config()
        logger.info("Configuration reset to defaults")
    except Exception as e:
        logger.error(f"Error resetting config: {str(e)}")
        raise
