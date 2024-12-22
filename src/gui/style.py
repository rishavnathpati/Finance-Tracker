"""Style definitions for the Finance Tracker GUI."""

# Main application style
MAIN_STYLE = """
QMainWindow {
    background-color: #1e1e1e;
}
"""

# Sidebar style
SIDEBAR_STYLE = """
QWidget {
    background-color: #252526;
    border-right: 1px solid #333333;
}
"""

# Content area style
CONTENT_STYLE = """
QWidget {
    background-color: #1e1e1e;
}
"""

# Navigation button style
BUTTON_STYLE = """
QPushButton {
    background-color: transparent;
    border: none;
    border-radius: 5px;
    color: #cccccc;
    font-size: 14px;
    text-align: left;
    padding: 10px 15px;
}

QPushButton:hover {
    background-color: #2d2d2d;
    color: #ffffff;
}
"""

# Active navigation button style
ACTIVE_BUTTON_STYLE = """
QPushButton {
    background-color: #37373d;
    border: none;
    border-radius: 5px;
    color: #ffffff;
    font-size: 14px;
    text-align: left;
    padding: 10px 15px;
}
"""

# Title style
TITLE_STYLE = """
QLabel {
    color: #ffffff;
    font-size: 24px;
    font-weight: bold;
    padding: 20px;
}
"""

# Card widget style
CARD_STYLE = """
QFrame {
    background-color: #2d2d2d;
    border-radius: 10px;
    padding: 15px;
}

QFrame > QLabel {
    background: none;
    border: none;
}
"""

# Card title style
CARD_TITLE_STYLE = """
QLabel {
    color: #ffffff;
    font-size: 16px;
    font-weight: bold;
    background: none;
    border: none;
}
"""

# Card content style
CARD_CONTENT_STYLE = """
QLabel {
    color: #cccccc;
    font-size: 14px;
    line-height: 1.4;
    background: none;
    border: none;
}
"""

# Table style
TABLE_STYLE = """
QTableWidget {
    background-color: #1e1e1e;
    border: 1px solid #333333;
    border-radius: 5px;
    gridline-color: #333333;
}

QTableWidget::item {
    padding: 5px;
    color: #cccccc;
}

QTableWidget::item:selected {
    background-color: #37373d;
    color: #ffffff;
}

QHeaderView::section {
    background-color: #252526;
    color: #ffffff;
    padding: 5px;
    border: 1px solid #333333;
}
"""

# Input field style
INPUT_STYLE = """
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
    background-color: #3c3c3c;
    border: 1px solid #555555;
    border-radius: 5px;
    color: #ffffff;
    padding: 5px 10px;
    min-height: 25px;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {
    border: 1px solid #007acc;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: url(:/icons/down_arrow.png);
}

QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    background-color: #4d4d4d;
    border: none;
    border-radius: 2px;
    width: 16px;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #5d5d5d;
}

QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {
    image: url(:/icons/up_arrow.png);
}

QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {
    image: url(:/icons/down_arrow.png);
}
"""

# Action button style
ACTION_BUTTON_STYLE = """
QPushButton {
    background-color: #007acc;
    border: none;
    border-radius: 5px;
    color: #ffffff;
    font-size: 14px;
    padding: 8px 16px;
    min-width: 100px;
}

QPushButton:hover {
    background-color: #1c97ea;
}

QPushButton:pressed {
    background-color: #0062a3;
}

QPushButton:disabled {
    background-color: #4d4d4d;
    color: #999999;
}
"""

# Delete button style
DELETE_BUTTON_STYLE = """
QPushButton {
    background-color: #c42b1c;
    border: none;
    border-radius: 5px;
    color: #ffffff;
    font-size: 14px;
    padding: 8px 16px;
    min-width: 100px;
}

QPushButton:hover {
    background-color: #e81123;
}

QPushButton:pressed {
    background-color: #a01616;
}
"""

# Dialog style
DIALOG_STYLE = """
QDialog {
    background-color: #1e1e1e;
}

QDialog QLabel {
    color: #ffffff;
}
"""

# Message box style
MESSAGE_BOX_STYLE = """
QMessageBox {
    background-color: #1e1e1e;
}

QMessageBox QLabel {
    color: #ffffff;
}

QMessageBox QPushButton {
    background-color: #007acc;
    border: none;
    border-radius: 5px;
    color: #ffffff;
    font-size: 14px;
    padding: 8px 16px;
    min-width: 100px;
}

QMessageBox QPushButton:hover {
    background-color: #1c97ea;
}
"""

# Scroll bar style
SCROLLBAR_STYLE = """
QScrollBar:vertical {
    border: none;
    background-color: #1e1e1e;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #424242;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background-color: #686868;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
    background: none;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
"""

# Tab widget style
TAB_STYLE = """
QTabWidget::pane {
    border: 1px solid #333333;
    background-color: #1e1e1e;
}

QTabBar::tab {
    background-color: #252526;
    color: #cccccc;
    padding: 8px 16px;
    border: 1px solid #333333;
    border-bottom: none;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

QTabBar::tab:selected {
    background-color: #1e1e1e;
    color: #ffffff;
}

QTabBar::tab:hover:!selected {
    background-color: #2d2d2d;
}
"""

# Progress bar style
PROGRESS_BAR_STYLE = """
QProgressBar {
    border: 1px solid #333333;
    border-radius: 5px;
    text-align: center;
    color: #ffffff;
    background-color: #1e1e1e;
}

QProgressBar::chunk {
    background-color: #007acc;
    border-radius: 5px;
}
"""
