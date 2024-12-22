from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QDialog,
    QLineEdit,
    QComboBox,
    QFormLayout,
    QMessageBox,
    QColorDialog,
)
from PyQt6.QtCore import Qt

from ...core.finance_manager import FinanceManager
from ...models.models import Category
from ..style import (
    INPUT_STYLE,
    ACTION_BUTTON_STYLE,
    DELETE_BUTTON_STYLE,
    DIALOG_STYLE,
)


class CategoryDialog(QDialog):
    """Dialog for adding/editing categories."""

    def __init__(
        self,
        finance_manager: FinanceManager,
        parent=None,
        category=None,
        parent_category=None,
    ):
        super().__init__(parent)
        self.finance_manager = finance_manager
        self.category = category
        self.parent_category = parent_category
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Add Category" if not self.category else "Edit Category")
        self.setStyleSheet(DIALOG_STYLE)
        self.setMinimumWidth(400)

        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Name field
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(INPUT_STYLE)
        if self.category:
            self.name_input.setText(self.category.name)
        layout.addRow("Name:", self.name_input)

        # Type field
        self.type_combo = QComboBox()
        self.type_combo.setStyleSheet(INPUT_STYLE)
        self.type_combo.addItems(["income", "expense"])
        if self.category:
            self.type_combo.setCurrentText(self.category.type)
        elif self.parent_category:
            self.type_combo.setCurrentText(self.parent_category.type)
            self.type_combo.setEnabled(False)
        layout.addRow("Type:", self.type_combo)

        # Parent category field
        self.parent_combo = QComboBox()
        self.parent_combo.setStyleSheet(INPUT_STYLE)
        self.parent_combo.addItem("None", None)

        categories = self.finance_manager.get_categories()
        for cat in categories:
            if not cat.parent_id:  # Only show top-level categories
                if (
                    self.category and cat.id != self.category.id
                ):  # Don't allow setting self as parent
                    self.parent_combo.addItem(cat.name, cat.id)

        if self.category and self.category.parent_id:
            index = self.parent_combo.findData(self.category.parent_id)
            self.parent_combo.setCurrentIndex(index)
        elif self.parent_category:
            index = self.parent_combo.findData(self.parent_category.id)
            self.parent_combo.setCurrentIndex(index)

        layout.addRow("Parent Category:", self.parent_combo)

        # Color field
        color_layout = QHBoxLayout()

        self.color_input = QLineEdit()
        self.color_input.setStyleSheet(INPUT_STYLE)
        self.color_input.setReadOnly(True)
        if self.category and self.category.color_code:
            self.color_input.setText(self.category.color_code)
            self.color_input.setStyleSheet(
                f"{INPUT_STYLE} background-color: {self.category.color_code};"
            )

        color_button = QPushButton("Choose Color")
        color_button.setStyleSheet(ACTION_BUTTON_STYLE)
        color_button.clicked.connect(self.choose_color)

        color_layout.addWidget(self.color_input)
        color_layout.addWidget(color_button)

        layout.addRow("Color:", color_layout)

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

    def choose_color(self):
        """Show color picker dialog."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_input.setText(color.name())
            self.color_input.setStyleSheet(
                f"{INPUT_STYLE} background-color: {color.name()};"
            )

    def get_data(self):
        """Get the category data from the form."""
        try:
            return {
                "name": self.name_input.text().strip(),
                "type": self.type_combo.currentText(),
                "parent_id": self.parent_combo.currentData(),
                "color_code": self.color_input.text() or None,
            }
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
            return None


class CategoriesWidget(QWidget):
    """Widget for managing categories."""

    def __init__(self, finance_manager: FinanceManager):
        super().__init__()
        self.finance_manager = finance_manager
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("Categories")
        title.setStyleSheet("font-size: 24px; color: white; font-weight: bold;")
        header_layout.addWidget(title)

        add_button = QPushButton("+ Add Category")
        add_button.setStyleSheet(ACTION_BUTTON_STYLE)
        add_button.clicked.connect(lambda: self.add_category())
        header_layout.addWidget(add_button, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(header_layout)

        # Category tree
        self.tree = QTreeWidget()
        self.tree.setStyleSheet(
            """
            QTreeWidget {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 5px;
            }
            QTreeWidget::item {
                color: #ffffff;
                padding: 5px;
            }
            QTreeWidget::item:selected {
                background-color: #37373d;
            }
        """
        )
        self.tree.setHeaderLabels(["Name", "Type", "Color"])
        self.tree.setColumnWidth(0, 300)
        self.tree.setColumnWidth(1, 100)

        layout.addWidget(self.tree)

        # Action buttons
        button_layout = QHBoxLayout()

        add_subcategory_button = QPushButton("Add Subcategory")
        add_subcategory_button.setStyleSheet(ACTION_BUTTON_STYLE)
        add_subcategory_button.clicked.connect(self.add_subcategory)

        edit_button = QPushButton("Edit")
        edit_button.setStyleSheet(ACTION_BUTTON_STYLE)
        edit_button.clicked.connect(self.edit_category)

        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet(DELETE_BUTTON_STYLE)
        delete_button.clicked.connect(self.delete_category)

        button_layout.addWidget(add_subcategory_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # Initial data load
        self.refresh_data()

    def create_tree_item(self, category: Category) -> QTreeWidgetItem:
        """Create a tree widget item for a category."""
        item = QTreeWidgetItem([category.name, category.type])
        item.setData(0, Qt.ItemDataRole.UserRole, category.id)

        if category.color_code:
            color_label = QLabel()
            color_label.setStyleSheet(
                f"background-color: {category.color_code}; border: 1px solid #555555;"
            )
            color_label.setFixedSize(20, 20)
            self.tree.setItemWidget(item, 2, color_label)

        # Add subcategories recursively
        for subcategory in category.subcategories:
            item.addChild(self.create_tree_item(subcategory))

        return item

    def refresh_data(self):
        """Refresh the category tree."""
        self.tree.clear()

        # Get all top-level categories
        categories = self.finance_manager.get_categories()
        top_level_categories = [c for c in categories if not c.parent_id]

        # Add categories to tree
        for category in top_level_categories:
            self.tree.addTopLevelItem(self.create_tree_item(category))

        self.tree.expandAll()

    def get_selected_category(self) -> tuple[Category, QTreeWidgetItem]:
        """Get the currently selected category and its tree item."""
        selected_items = self.tree.selectedItems()
        if not selected_items:
            return None, None

        item = selected_items[0]
        category_id = item.data(0, Qt.ItemDataRole.UserRole)
        category = self.finance_manager.get_category(category_id)

        return category, item

    def add_category(self, parent_category=None):
        """Show dialog to add a new category."""
        dialog = CategoryDialog(
            self.finance_manager, self, parent_category=parent_category
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data:
                try:
                    self.finance_manager.create_category(**data)
                    self.refresh_data()
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))

    def add_subcategory(self):
        """Show dialog to add a subcategory to the selected category."""
        category, _ = self.get_selected_category()
        if not category:
            QMessageBox.warning(
                self, "No Selection", "Please select a parent category."
            )
            return

        self.add_category(parent_category=category)

    def edit_category(self):
        """Show dialog to edit the selected category."""
        category, _ = self.get_selected_category()
        if not category:
            QMessageBox.warning(
                self, "No Selection", "Please select a category to edit."
            )
            return

        dialog = CategoryDialog(self.finance_manager, self, category=category)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data:
                try:
                    self.finance_manager.update_category(category.id, **data)
                    self.refresh_data()
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))

    def delete_category(self):
        """Delete the selected category."""
        category, _ = self.get_selected_category()
        if not category:
            QMessageBox.warning(
                self, "No Selection", "Please select a category to delete."
            )
            return

        if category.subcategories:
            QMessageBox.warning(
                self,
                "Cannot Delete",
                "This category has subcategories. Please delete or move them first.",
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this category? This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.finance_manager.delete_category(category.id)
                self.refresh_data()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))
