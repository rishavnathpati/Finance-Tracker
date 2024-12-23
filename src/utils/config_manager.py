"""Configuration management utilities for the Finance Tracker application."""

import json
import os
from typing import Any, Dict, Optional

from .logger import FinanceLogger

# Initialize logger
logger = FinanceLogger(
    name="finance_tracker.config", log_file="logs/config.log"
)

DEFAULT_CONFIG: Dict[str, Any] = {
    "DEFAULT_CURRENCY": "INR",
    "database": {"type": "sqlite", "path": "data/finance_tracker.db"},
    "logging": {
        "level": "INFO",
        "file": "logs/finance_tracker.log",
        "max_size": 5242880,  # 5MB
        "backup_count": 5,
    },
    "currency": {"default": "INR", "display_symbol": "₹"},
    "date_format": "%d-%m-%Y",  # Indian date format
    "export": {"default_format": "csv", "path": "data/exports"},
    "receipts": {
        "path": "data/receipts",
        "allowed_extensions": [".jpg", ".jpeg", ".png", ".pdf"],
    },
}

CONFIG_FILE = "config/config.json"


def get_config() -> Dict[str, Any]:
    """Get the current configuration.

    Returns:
        Dict[str, Any]: The current configuration dictionary.
    """
    return load_config()


def load_config() -> Dict[str, Any]:
    """Load configuration from file.

    Returns:
        Dict[str, Any]: The loaded configuration dictionary.
    """
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return create_default_config()
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        return DEFAULT_CONFIG


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file.

    Args:
        config (Dict[str, Any]): The configuration to save.

    Raises:
        Exception: If there is an error saving the configuration.
    """
    try:
        # Ensure config directory exists
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

        logger.info("Configuration saved successfully")
    except Exception as e:
        logger.error(f"Error saving config: {str(e)}")
        raise


def create_default_config() -> Dict[str, Any]:
    """Create and save default configuration.

    Returns:
        Dict[str, Any]: The default configuration dictionary.

    Raises:
        Exception: If there is an error creating the default configuration.
    """
    try:
        save_config(DEFAULT_CONFIG)
        logger.info("Default configuration created")
        return DEFAULT_CONFIG
    except Exception as e:
        logger.error(f"Error creating default config: {str(e)}")
        raise


def get_config_value(key: str, default: Optional[Any] = None) -> Any:
    """Get a configuration value by key.

    Args:
        key (str): The configuration key to look up.
        default (Optional[Any], optional): Default value if key not found.
            Defaults to None.

    Returns:
        Any: The configuration value or default if not found.
    """
    config = load_config()
    keys = key.split(".")

    try:
        value = config
        for k in keys:
            value = value[k]
        return value
    except (KeyError, TypeError):
        logger.warning(
            f"Config key '{key}' not found, using default: {default}"
        )
        return default


def update_config_value(key: str, value: Any) -> None:
    """Update a configuration value.

    Args:
        key (str): The configuration key to update.
        value (Any): The new value to set.
    """
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
