from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTabWidget,
    QWidget,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QCheckBox,
    QFormLayout,
)

from ..style import DIALOG_STYLE, INPUT_STYLE, ACTION_BUTTON_STYLE, TAB_STYLE


class SettingsDialog(QDialog):
    """Settings dialog for configuring the application."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setStyleSheet(DIALOG_STYLE)
        self.setMinimumWidth(600)
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Create tab widget
        tabs = QTabWidget()
        tabs.setStyleSheet(TAB_STYLE)

        # General settings tab
        general_tab = QWidget()
        general_layout = QFormLayout(general_tab)
        general_layout.setContentsMargins(20, 20, 20, 20)
        general_layout.setSpacing(15)

        # Currency settings
        currency_combo = QComboBox()
        currency_combo.setStyleSheet(INPUT_STYLE)
        currency_combo.addItems(["USD ($)", "EUR (€)", "GBP (£)", "JPY (¥)"])
        general_layout.addRow("Default Currency:", currency_combo)

        # Date format settings
        date_format_combo = QComboBox()
        date_format_combo.setStyleSheet(INPUT_STYLE)
        date_format_combo.addItems(["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
        general_layout.addRow("Date Format:", date_format_combo)

        # Theme settings
        theme_combo = QComboBox()
        theme_combo.setStyleSheet(INPUT_STYLE)
        theme_combo.addItems(["Dark Theme", "Light Theme"])
        general_layout.addRow("Theme:", theme_combo)

        # Add general tab
        tabs.addTab(general_tab, "General")

        # Notifications tab
        notifications_tab = QWidget()
        notifications_layout = QFormLayout(notifications_tab)
        notifications_layout.setContentsMargins(20, 20, 20, 20)
        notifications_layout.setSpacing(15)

        # Email notifications
        email_check = QCheckBox("Enable Email Notifications")
        email_check.setStyleSheet("QCheckBox { color: white; }")
        notifications_layout.addRow(email_check)

        email_input = QLineEdit()
        email_input.setStyleSheet(INPUT_STYLE)
        email_input.setPlaceholderText("Enter your email address")
        notifications_layout.addRow("Email Address:", email_input)

        # Budget alerts
        budget_check = QCheckBox("Enable Budget Alerts")
        budget_check.setStyleSheet("QCheckBox { color: white; }")
        notifications_layout.addRow(budget_check)

        threshold_spin = QSpinBox()
        threshold_spin.setStyleSheet(INPUT_STYLE)
        threshold_spin.setRange(50, 100)
        threshold_spin.setValue(80)
        threshold_spin.setSuffix("%")
        notifications_layout.addRow("Alert Threshold:", threshold_spin)

        # Add notifications tab
        tabs.addTab(notifications_tab, "Notifications")

        # Add tabs to layout
        layout.addWidget(tabs)

        # Add buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        save_button = QPushButton("Save")
        save_button.setStyleSheet(ACTION_BUTTON_STYLE)
        save_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4d4d4d;
                border: none;
                border-radius: 5px;
                color: #ffffff;
                font-size: 14px;
                padding: 8px 16px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5d5d5d;
            }
        """
        )
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)

        layout.addLayout(button_layout)
