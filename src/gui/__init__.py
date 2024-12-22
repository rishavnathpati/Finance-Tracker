"""GUI package for the Finance Tracker application."""

from .main_window import MainWindow
from .widgets.dashboard import DashboardWidget
from .widgets.accounts import AccountsWidget
from .widgets.transactions import TransactionsWidget
from .widgets.categories import CategoriesWidget
from .widgets.reports import ReportsWidget

__all__ = [
    "MainWindow",
    "DashboardWidget",
    "AccountsWidget",
    "TransactionsWidget",
    "CategoriesWidget",
    "ReportsWidget",
]
