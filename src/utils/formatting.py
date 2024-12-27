"""Utility functions for formatting data in the Finance Tracker application."""

from decimal import Decimal
from typing import Dict, Any


def format_currency(
    amount: Decimal, config: Dict[str, Any]
) -> str:
    """Format a decimal amount as currency string.

    Args:
        amount: The decimal amount to format
        config: Configuration dictionary containing currency settings

    Returns:
        str: The formatted currency string
    """
    symbol = config.get("currency", {}).get("display_symbol", "₹")
    return f"{symbol}{amount:,.2f}"
