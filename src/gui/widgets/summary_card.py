from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt


class SummaryCard(QWidget):
    """A custom widget for displaying summary information."""

    def __init__(self, title: str, value: str, icon: str, parent=None):
        super().__init__(parent)
        self.title = title
        self.value = value
        self.icon = icon
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        # Set up the main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Create header with icon and title
        header = QWidget()
        header.setStyleSheet("background: transparent;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        # Icon
        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet(
            """
            QLabel {
                color: #ffffff;
                font-size: 16px;
                background: transparent;
            }
        """
        )

        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet(
            """
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }
        """
        )

        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Value
        self.value_label = QLabel(self.value)
        self.value_label.setObjectName("value_label")
        self.value_label.setStyleSheet(
            """
            QLabel {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            }
        """
        )
        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        # Add widgets to layout
        layout.addWidget(header)
        layout.addWidget(self.value_label)
        layout.addStretch()

        # Set widget style
        self.setStyleSheet(
            """
            SummaryCard {
                background-color: #2d2d2d;
                border-radius: 10px;
            }
        """
        )

        # Set fixed height
        self.setFixedHeight(120)

    def set_value(self, value: str):
        """Update the displayed value."""
        self.value_label.setText(value)
