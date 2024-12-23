from decimal import Decimal

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ...core.finance_manager import FinanceManager
from ...models.models import AccountType
from ...utils.config_manager import get_config
from ..style import (
    ACTION_BUTTON_STYLE,
    CARD_STYLE,
    CARD_TITLE_STYLE,
    DELETE_BUTTON_STYLE,
    DIALOG_STYLE,
    INPUT_STYLE,
    TABLE_STYLE,
)


def format_currency(amount: Decimal, config) -> str:
    """Format decimal amount as currency string."""
    if config["DEFAULT_CURRENCY"] == "INR":
        # Format with Indian number system (lakhs and crores)
        def format_indian(num):
            num = float(num)
            if num >= 10000000:  # Crore
                return f"₹{num/10000000:.2f}Cr"
            elif num >= 100000:  # Lakh
                return f"₹{num/100000:.2f}L"
            else:
                s = str(int(num))
                result = s[-3:]
                s = s[:-3]
                while s:
                    result = s[-2:] + "," + result if len(s) > 2 else s + "," + result
                    s = s[:-2]
                return f"₹{result}"

        return format_indian(amount)
    else:
        return f"${amount:,.2f}"


class AccountDialog(QDialog):
    """Dialog for adding/editing accounts."""

    def __init__(self, parent=None, account=None):
        super().__init__(parent)
        self.account = account
        self.config = get_config()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Add Account" if not self.account else "Edit Account")
        self.setStyleSheet(DIALOG_STYLE)
        self.setMinimumWidth(400)

        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Name field
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(INPUT_STYLE)
        if self.account:
            self.name_input.setText(self.account.name)
        layout.addRow("Name:", self.name_input)

        # Type field
        self.type_combo = QComboBox()
        self.type_combo.setStyleSheet(INPUT_STYLE)
        for account_type in AccountType:
            self.type_combo.addItem(account_type.value)
        if self.account:
            self.type_combo.setCurrentText(self.account.type.value)
        layout.addRow("Type:", self.type_combo)

        # Balance field
        self.balance_input = QLineEdit()
        self.balance_input.setStyleSheet(INPUT_STYLE)
        if self.account:
            self.balance_input.setText(str(self.account.balance))
        layout.addRow("Balance:", self.balance_input)

        # Currency field
        self.currency_input = QLineEdit()
        self.currency_input.setStyleSheet(INPUT_STYLE)
        self.currency_input.setText(
            self.account.currency if self.account else self.config["DEFAULT_CURRENCY"]
        )
        layout.addRow("Currency:", self.currency_input)

        # Description field
        self.description_input = QLineEdit()
        self.description_input.setStyleSheet(INPUT_STYLE)
        if self.account:
            self.description_input.setText(self.account.description or "")
        layout.addRow("Description:", self.description_input)

        # Buttons
        button_layout = QHBoxLayout()

        save_button = QPushButton("Save")
        save_button.setStyleSheet(ACTION_BUTTON_STYLE)
        save_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet(DELETE_BUTTON_STYLE)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addRow("", button_layout)

    def get_data(self):
        """Get the account data from the form."""
        try:
            return {
                "name": self.name_input.text().strip(),
                "account_type": AccountType(self.type_combo.currentText()),
                "initial_balance": Decimal(self.balance_input.text()),
                "currency": self.currency_input.text().strip(),
                "description": self.description_input.text().strip() or None,
            }
        except (ValueError, TypeError) as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
            return None


class AccountsWidget(QWidget):
    """Widget for managing accounts."""

    def __init__(self, finance_manager: FinanceManager):
        super().__init__()
        self.finance_manager = finance_manager
        self.config = get_config()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("Accounts")
        title.setStyleSheet("font-size: 24px; color: white; font-weight: bold;")
        header_layout.addWidget(title)

        add_button = QPushButton("+ Add Account")
        add_button.setStyleSheet(ACTION_BUTTON_STYLE)
        add_button.clicked.connect(self.add_account)
        header_layout.addWidget(add_button, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(header_layout)

        # Accounts table
        self.table = QTableWidget()
        self.table.setStyleSheet(TABLE_STYLE)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Type", "Balance", "Currency", "Description"]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            5, QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self.table)

        # Action buttons
        button_layout = QHBoxLayout()

        edit_button = QPushButton("Edit")
        edit_button.setStyleSheet(ACTION_BUTTON_STYLE)
        edit_button.clicked.connect(self.edit_account)

        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet(DELETE_BUTTON_STYLE)
        delete_button.clicked.connect(self.delete_account)

        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # Initial data load
        self.refresh_data()

    def refresh_data(self):
        """Refresh the accounts table."""
        accounts = self.finance_manager.get_accounts()

        self.table.setRowCount(len(accounts))
        for i, account in enumerate(accounts):
            self.table.setItem(i, 0, QTableWidgetItem(str(account.id)))
            self.table.setItem(i, 1, QTableWidgetItem(account.name))
            self.table.setItem(i, 2, QTableWidgetItem(account.type.value))
            self.table.setItem(
                i, 3, QTableWidgetItem(format_currency(account.balance, self.config))
            )
            self.table.setItem(i, 4, QTableWidgetItem(account.currency))
            self.table.setItem(i, 5, QTableWidgetItem(account.description or ""))

    def add_account(self):
        """Show dialog to add a new account."""
        dialog = AccountDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data:
                try:
                    self.finance_manager.create_account(**data)
                    self.refresh_data()
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))

    def edit_account(self):
        """Show dialog to edit the selected account."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self, "No Selection", "Please select an account to edit."
            )
            return

        account_id = int(self.table.item(selected_items[0].row(), 0).text())
        account = self.finance_manager.get_account(account_id)

        dialog = AccountDialog(self, account)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data:
                try:
                    self.finance_manager.update_account(account_id, **data)
                    self.refresh_data()
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))

    def delete_account(self):
        """Delete the selected account."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self, "No Selection", "Please select an account to delete."
            )
            return

        account_id = int(self.table.item(selected_items[0].row(), 0).text())

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this account? This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.finance_manager.delete_account(account_id)
                self.refresh_data()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))
