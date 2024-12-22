"""GUI widgets package for the Finance Tracker application."""

from .dashboard import DashboardWidget
from .accounts import AccountsWidget
from .transactions import TransactionsWidget
from .categories import CategoriesWidget
from .reports import ReportsWidget

__all__ = [
    "DashboardWidget",
    "AccountsWidget",
    "TransactionsWidget",
    "CategoriesWidget",
    "ReportsWidget",
]
