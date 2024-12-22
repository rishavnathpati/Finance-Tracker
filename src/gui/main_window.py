from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtCore import Qt
import qdarktheme

from ..core.finance_manager import FinanceManager
from ..utils.logger import FinanceLogger
from .widgets.dashboard import DashboardWidget
from .widgets.accounts import AccountsWidget
from .widgets.transactions import TransactionsWidget
from .widgets.categories import CategoriesWidget
from .widgets.reports import ReportsWidget
from .dialogs.settings_dialog import SettingsDialog
from .style import (
    SIDEBAR_STYLE,
    CONTENT_STYLE,
    BUTTON_STYLE,
    ACTIVE_BUTTON_STYLE,
    TITLE_STYLE,
)

# Initialize logger
logger = FinanceLogger(name="finance_gui", log_file="logs/gui.log")


class MainWindow(QMainWindow):
    """Main window of the Finance Tracker application."""

    def __init__(self, finance_manager: FinanceManager):
        super().__init__()
        self.finance_manager = finance_manager
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Finance Tracker")
        self.setMinimumSize(1200, 800)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # Create stacked widget for main content
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet(CONTENT_STYLE)

        # Create and add pages
        self.dashboard = DashboardWidget(self.finance_manager)
        self.accounts = AccountsWidget(self.finance_manager)
        self.transactions = TransactionsWidget(self.finance_manager)
        self.categories = CategoriesWidget(self.finance_manager)
        self.reports = ReportsWidget(self.finance_manager)

        self.stacked_widget.addWidget(self.dashboard)
        self.stacked_widget.addWidget(self.accounts)
        self.stacked_widget.addWidget(self.transactions)
        self.stacked_widget.addWidget(self.categories)
        self.stacked_widget.addWidget(self.reports)

        main_layout.addWidget(self.stacked_widget)

        # Set dark theme
        self.set_theme()

        # Show dashboard by default
        self.show_dashboard()

    def create_sidebar(self):
        """Create the sidebar with navigation buttons."""
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet(SIDEBAR_STYLE)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Add logo/title
        title = QLabel("Finance\nTracker")
        title.setStyleSheet(TITLE_STYLE)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Add navigation buttons
        self.nav_buttons = []

        dashboard_btn = self.create_nav_button("Dashboard", "📊", self.show_dashboard)
        accounts_btn = self.create_nav_button("Accounts", "💰", self.show_accounts)
        transactions_btn = self.create_nav_button(
            "Transactions", "💸", self.show_transactions
        )
        categories_btn = self.create_nav_button("Categories", "🏷️", self.show_categories)
        reports_btn = self.create_nav_button("Reports", "📈", self.show_reports)

        layout.addWidget(dashboard_btn)
        layout.addWidget(accounts_btn)
        layout.addWidget(transactions_btn)
        layout.addWidget(categories_btn)
        layout.addWidget(reports_btn)

        # Add spacer
        layout.addSpacerItem(
            QSpacerItem(
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        # Add settings button at bottom
        settings_btn = self.create_nav_button("Settings", "⚙️", self.show_settings)
        layout.addWidget(settings_btn)

        return sidebar

    def create_nav_button(self, text, icon, callback):
        """Create a navigation button with icon and text."""
        button = QPushButton(f"{icon} {text}")
        button.setStyleSheet(BUTTON_STYLE)
        button.setFixedHeight(50)
        button.clicked.connect(callback)
        self.nav_buttons.append(button)
        return button

    def update_nav_buttons(self, active_button):
        """Update navigation button styles."""
        for button in self.nav_buttons:
            if button == active_button:
                button.setStyleSheet(ACTIVE_BUTTON_STYLE)
            else:
                button.setStyleSheet(BUTTON_STYLE)

    def show_dashboard(self):
        """Show the dashboard page."""
        self.stacked_widget.setCurrentWidget(self.dashboard)
        self.update_nav_buttons(self.nav_buttons[0])
        self.dashboard.refresh_data()

    def show_accounts(self):
        """Show the accounts page."""
        self.stacked_widget.setCurrentWidget(self.accounts)
        self.update_nav_buttons(self.nav_buttons[1])
        self.accounts.refresh_data()

    def show_transactions(self):
        """Show the transactions page."""
        self.stacked_widget.setCurrentWidget(self.transactions)
        self.update_nav_buttons(self.nav_buttons[2])
        self.transactions.refresh_data()

    def show_categories(self):
        """Show the categories page."""
        self.stacked_widget.setCurrentWidget(self.categories)
        self.update_nav_buttons(self.nav_buttons[3])
        self.categories.refresh_data()

    def show_reports(self):
        """Show the reports page."""
        self.stacked_widget.setCurrentWidget(self.reports)
        self.update_nav_buttons(self.nav_buttons[4])
        self.reports.refresh_data()

    def show_settings(self):
        """Show the settings dialog."""
        dialog = SettingsDialog(self)
        if dialog.exec():
            # TODO: Save settings
            logger.info("Settings saved")
        else:
            logger.info("Settings cancelled")

    def set_theme(self):
        """Set the application theme."""
        qdarktheme.setup_theme("dark")

    def closeEvent(self, event):
        """Handle application close event."""
        event.accept()
