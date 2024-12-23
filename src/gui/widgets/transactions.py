from decimal import Decimal

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDoubleSpinBox,
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
from ...models.models import TransactionType
from ...utils.config_manager import get_config
from ..style import (
    ACTION_BUTTON_STYLE,
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


class TransactionDialog(QDialog):
    """Dialog for adding/editing transactions."""

    def __init__(self, finance_manager: FinanceManager, parent=None, transaction=None):
        super().__init__(parent)
        self.finance_manager = finance_manager
        self.transaction = transaction
        self.config = get_config()
        self.currency_symbol = "₹" if self.config["DEFAULT_CURRENCY"] == "INR" else "$"
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(
            "Add Transaction" if not self.transaction else "Edit Transaction"
        )
        self.setStyleSheet(DIALOG_STYLE)
        self.setMinimumWidth(500)

        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Type field
        self.type_combo = QComboBox()
        self.type_combo.setStyleSheet(INPUT_STYLE)
        for trans_type in TransactionType:
            self.type_combo.addItem(trans_type.value)
        if self.transaction:
            self.type_combo.setCurrentText(self.transaction.type.value)
        layout.addRow("Type:", self.type_combo)

        # Amount field
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setStyleSheet(INPUT_STYLE)
        self.amount_input.setRange(0, 1000000000)
        self.amount_input.setDecimals(2)
        self.amount_input.setPrefix(self.currency_symbol)
        if self.transaction:
            self.amount_input.setValue(float(self.transaction.amount))
        layout.addRow("Amount:", self.amount_input)

        # Date field
        self.date_input = QDateEdit()
        self.date_input.setStyleSheet(INPUT_STYLE)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd-MM-yyyy")  # Indian date format
        if self.transaction:
            self.date_input.setDate(
                QDate(
                    self.transaction.date.year,
                    self.transaction.date.month,
                    self.transaction.date.day,
                )
            )
        else:
            self.date_input.setDate(QDate.currentDate())
        layout.addRow("Date:", self.date_input)

        # From Account field
        self.from_account_combo = QComboBox()
        self.from_account_combo.setStyleSheet(INPUT_STYLE)
        accounts = self.finance_manager.get_accounts()
        for account in accounts:
            self.from_account_combo.addItem(
                f"{account.name} ({account.currency})", account.id
            )
        if self.transaction:
            index = self.from_account_combo.findData(self.transaction.from_account_id)
            self.from_account_combo.setCurrentIndex(index)
        layout.addRow("From Account:", self.from_account_combo)

        # To Account field (for transfers)
        self.to_account_combo = QComboBox()
        self.to_account_combo.setStyleSheet(INPUT_STYLE)
        self.to_account_combo.addItem("N/A", None)
        for account in accounts:
            self.to_account_combo.addItem(
                f"{account.name} ({account.currency})", account.id
            )
        if self.transaction and self.transaction.to_account_id:
            index = self.to_account_combo.findData(self.transaction.to_account_id)
            self.to_account_combo.setCurrentIndex(index)
        layout.addRow("To Account:", self.to_account_combo)

        # Category field
        self.category_combo = QComboBox()
        self.category_combo.setStyleSheet(INPUT_STYLE)
        categories = self.finance_manager.get_categories()
        for category in categories:
            self.category_combo.addItem(category.name, category.id)
        if self.transaction:
            index = self.category_combo.findData(self.transaction.category_id)
            self.category_combo.setCurrentIndex(index)
        layout.addRow("Category:", self.category_combo)

        # Description field
        self.description_input = QLineEdit()
        self.description_input.setStyleSheet(INPUT_STYLE)
        if self.transaction:
            self.description_input.setText(self.transaction.description or "")
        layout.addRow("Description:", self.description_input)

        # Tags field
        self.tags_input = QLineEdit()
        self.tags_input.setStyleSheet(INPUT_STYLE)
        if self.transaction and self.transaction.tags:
            self.tags_input.setText(self.transaction.tags)
        layout.addRow("Tags:", self.tags_input)

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

        # Connect signals
        self.type_combo.currentTextChanged.connect(self.on_type_changed)

        # Initial state
        self.on_type_changed(self.type_combo.currentText())

    def on_type_changed(self, transaction_type):
        """Handle transaction type changes."""
        is_transfer = transaction_type == TransactionType.TRANSFER.value
        self.to_account_combo.setEnabled(is_transfer)
        if not is_transfer:
            self.to_account_combo.setCurrentIndex(0)

    def get_data(self):
        """Get the transaction data from the form."""
        try:
            return {
                "type": TransactionType(self.type_combo.currentText()),
                "amount": Decimal(str(self.amount_input.value())),
                "date": self.date_input.date().toPyDate(),
                "from_account_id": self.from_account_combo.currentData(),
                "to_account_id": self.to_account_combo.currentData(),
                "category_id": self.category_combo.currentData(),
                "description": self.description_input.text().strip() or None,
                "tags": self.tags_input.text().strip() or None,
            }
        except (ValueError, TypeError) as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
            return None


class TransactionsWidget(QWidget):
    """Widget for managing transactions."""

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

        title = QLabel("Transactions")
        title.setStyleSheet("font-size: 24px; color: white; font-weight: bold;")
        header_layout.addWidget(title)

        add_button = QPushButton("+ Add Transaction")
        add_button.setStyleSheet(ACTION_BUTTON_STYLE)
        add_button.clicked.connect(self.add_transaction)
        header_layout.addWidget(add_button, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(header_layout)

        # Filters
        filter_layout = QHBoxLayout()

        # Date range filter
        self.start_date = QDateEdit()
        self.start_date.setStyleSheet(INPUT_STYLE)
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("dd-MM-yyyy")  # Indian date format
        self.start_date.setDate(QDate.currentDate().addMonths(-1))

        self.end_date = QDateEdit()
        self.end_date.setStyleSheet(INPUT_STYLE)
        self.end_date.setCalendarPopup(True)
        self.end_date.setDisplayFormat("dd-MM-yyyy")  # Indian date format
        self.end_date.setDate(QDate.currentDate())

        filter_layout.addWidget(QLabel("From:"))
        filter_layout.addWidget(self.start_date)
        filter_layout.addWidget(QLabel("To:"))
        filter_layout.addWidget(self.end_date)

        # Type filter
        self.type_filter = QComboBox()
        self.type_filter.setStyleSheet(INPUT_STYLE)
        self.type_filter.addItem("All Types", None)
        for trans_type in TransactionType:
            self.type_filter.addItem(trans_type.value, trans_type)

        filter_layout.addWidget(QLabel("Type:"))
        filter_layout.addWidget(self.type_filter)

        # Account filter
        self.account_filter = QComboBox()
        self.account_filter.setStyleSheet(INPUT_STYLE)
        self.account_filter.addItem("All Accounts", None)
        accounts = self.finance_manager.get_accounts()
        for account in accounts:
            self.account_filter.addItem(account.name, account.id)

        filter_layout.addWidget(QLabel("Account:"))
        filter_layout.addWidget(self.account_filter)

        # Apply filters button
        apply_button = QPushButton("Apply Filters")
        apply_button.setStyleSheet(ACTION_BUTTON_STYLE)
        apply_button.clicked.connect(self.refresh_data)
        filter_layout.addWidget(apply_button)

        layout.addLayout(filter_layout)

        # Transactions table
        self.table = QTableWidget()
        self.table.setStyleSheet(TABLE_STYLE)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Date",
                "Type",
                "Amount",
                "From Account",
                "To Account",
                "Category",
                "Description",
            ]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            7, QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self.table)

        # Action buttons
        button_layout = QHBoxLayout()

        edit_button = QPushButton("Edit")
        edit_button.setStyleSheet(ACTION_BUTTON_STYLE)
        edit_button.clicked.connect(self.edit_transaction)

        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet(DELETE_BUTTON_STYLE)
        delete_button.clicked.connect(self.delete_transaction)

        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # Initial data load
        self.refresh_data()

    def refresh_data(self):
        """Refresh the transactions table."""
        start_date = self.start_date.date().toPyDate()
        end_date = self.end_date.date().toPyDate()
        transaction_type = self.type_filter.currentData()
        account_id = self.account_filter.currentData()

        transactions = self.finance_manager.search_transactions(
            start_date=start_date,
            end_date=end_date,
            transaction_type=transaction_type,
            account_id=account_id,
        )

        self.table.setRowCount(len(transactions))
        for i, transaction in enumerate(transactions):
            self.table.setItem(i, 0, QTableWidgetItem(str(transaction.id)))
            self.table.setItem(
                i,
                1,
                QTableWidgetItem(
                    transaction.date.strftime("%d-%m-%Y")
                ),  # Indian date format
            )
            self.table.setItem(i, 2, QTableWidgetItem(transaction.type.value))
            self.table.setItem(
                i, 3, QTableWidgetItem(format_currency(transaction.amount, self.config))
            )
            self.table.setItem(i, 4, QTableWidgetItem(transaction.from_account.name))
            self.table.setItem(
                i,
                5,
                QTableWidgetItem(
                    transaction.to_account.name if transaction.to_account else "N/A"
                ),
            )
            self.table.setItem(i, 6, QTableWidgetItem(transaction.category.name))
            self.table.setItem(i, 7, QTableWidgetItem(transaction.description or ""))

    def add_transaction(self):
        """Show dialog to add a new transaction."""
        dialog = TransactionDialog(self.finance_manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data:
                try:
                    self.finance_manager.create_transaction(**data)
                    self.refresh_data()
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))

    def edit_transaction(self):
        """Show dialog to edit the selected transaction."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self, "No Selection", "Please select a transaction to edit."
            )
            return

        transaction_id = int(self.table.item(selected_items[0].row(), 0).text())
        transaction = self.finance_manager.get_transaction(transaction_id)

        dialog = TransactionDialog(self.finance_manager, self, transaction)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data:
                try:
                    self.finance_manager.update_transaction(transaction_id, **data)
                    self.refresh_data()
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))

    def delete_transaction(self):
        """Delete the selected transaction."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self, "No Selection", "Please select a transaction to delete."
            )
            return

        transaction_id = int(self.table.item(selected_items[0].row(), 0).text())

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this transaction? This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.finance_manager.delete_transaction(transaction_id)
                self.refresh_data()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))
