from datetime import datetime, timedelta
from decimal import Decimal

from PyQt6.QtCharts import (
    QChart,
    QChartView,
    QDateTimeAxis,
    QLineSeries,
    QPieSeries,
    QValueAxis,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ...core.finance_manager import FinanceManager
from ...utils.config_manager import get_config
from ..style import CARD_CONTENT_STYLE, CARD_STYLE, CARD_TITLE_STYLE
from .summary_card import SummaryCard


class DashboardWidget(QWidget):
    """Dashboard widget showing financial overview."""

    def __init__(self, finance_manager: FinanceManager):
        super().__init__()
        self.finance_manager = finance_manager
        self.config = get_config()
        self.currency_symbol = "₹" if self.config["DEFAULT_CURRENCY"] == "INR" else "$"
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Add title
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 24px; color: white; font-weight: bold;")
        main_layout.addWidget(title)

        # Create scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        # Create content widget
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(20)

        # Add summary cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        self.balance_card = SummaryCard(
            "Total Balance", f"{self.currency_symbol}0.00", "💰"
        )
        self.income_card = SummaryCard(
            "Monthly Income", f"{self.currency_symbol}0.00", "📈"
        )
        self.expenses_card = SummaryCard(
            "Monthly Expenses", f"{self.currency_symbol}0.00", "📉"
        )
        self.savings_card = SummaryCard(
            "Monthly Savings", f"{self.currency_symbol}0.00", "💎"
        )

        cards_layout.addWidget(self.balance_card)
        cards_layout.addWidget(self.income_card)
        cards_layout.addWidget(self.expenses_card)
        cards_layout.addWidget(self.savings_card)

        content_layout.addLayout(cards_layout)

        # Add charts
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)

        # Expense breakdown chart
        expense_chart_container = QFrame()
        expense_chart_container.setStyleSheet(CARD_STYLE)
        expense_chart_layout = QVBoxLayout(expense_chart_container)
        expense_chart_layout.setContentsMargins(15, 15, 15, 15)

        expense_chart_title = QLabel("Expense Breakdown")
        expense_chart_title.setStyleSheet(CARD_TITLE_STYLE)
        expense_chart_layout.addWidget(expense_chart_title)

        self.expense_chart = self.create_expense_chart()
        expense_chart_layout.addWidget(self.expense_chart)

        # Balance trend chart
        trend_chart_container = QFrame()
        trend_chart_container.setStyleSheet(CARD_STYLE)
        trend_chart_layout = QVBoxLayout(trend_chart_container)
        trend_chart_layout.setContentsMargins(15, 15, 15, 15)

        trend_chart_title = QLabel("Balance Trend")
        trend_chart_title.setStyleSheet(CARD_TITLE_STYLE)
        trend_chart_layout.addWidget(trend_chart_title)

        self.trend_chart = self.create_trend_chart()
        trend_chart_layout.addWidget(self.trend_chart)

        charts_layout.addWidget(expense_chart_container)
        charts_layout.addWidget(trend_chart_container)

        content_layout.addLayout(charts_layout)

        # Add recent transactions
        transactions_container = QFrame()
        transactions_container.setStyleSheet(CARD_STYLE)
        transactions_layout = QVBoxLayout(transactions_container)
        transactions_layout.setContentsMargins(15, 15, 15, 15)

        transactions_title = QLabel("Recent Transactions")
        transactions_title.setStyleSheet(CARD_TITLE_STYLE)
        transactions_layout.addWidget(transactions_title)

        self.transactions_content = QLabel("No recent transactions")
        self.transactions_content.setStyleSheet(CARD_CONTENT_STYLE)
        transactions_layout.addWidget(self.transactions_content)

        content_layout.addWidget(transactions_container)

        # Set scroll area widget
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # Initial data refresh
        self.refresh_data()

    def create_expense_chart(self) -> QChartView:
        """Create the expense breakdown pie chart."""
        series = QPieSeries()

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setBackgroundVisible(True)
        chart.setBackgroundBrush(QColor("#2d2d2d"))
        chart.legend().setVisible(True)
        chart.legend().setLabelColor(QColor("#ffffff"))
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setMinimumHeight(300)

        return chart_view

    def create_trend_chart(self) -> QChartView:
        """Create the balance trend line chart."""
        series = QLineSeries()
        series.setColor(QColor("#007acc"))  # Set line color
        pen = series.pen()
        pen.setWidth(2)
        series.setPen(pen)

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setBackgroundVisible(True)
        chart.setBackgroundBrush(QColor("#2d2d2d"))
        chart.legend().setVisible(False)

        # Create axes
        date_axis = QDateTimeAxis()
        date_axis.setFormat("MMM dd")
        date_axis.setLabelsColor(QColor("#ffffff"))
        date_axis.setGridLineColor(QColor("#404040"))
        date_axis.setMinorGridLineColor(QColor("#353535"))
        date_axis.setTitleText("Date")
        date_axis.setTitleBrush(QColor("#ffffff"))
        chart.addAxis(date_axis, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(date_axis)

        value_axis = QValueAxis()
        value_axis.setLabelsColor(QColor("#ffffff"))
        value_axis.setGridLineColor(QColor("#404040"))
        value_axis.setMinorGridLineColor(QColor("#353535"))
        value_axis.setTitleText(f"Balance ({self.currency_symbol})")
        value_axis.setTitleBrush(QColor("#ffffff"))
        chart.addAxis(value_axis, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(value_axis)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setMinimumHeight(300)

        return chart_view

    def format_currency(self, amount: Decimal) -> str:
        """Format decimal amount as currency string."""
        if self.config["DEFAULT_CURRENCY"] == "INR":
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
                        result = (
                            s[-2:] + "," + result if len(s) > 2 else s + "," + result
                        )
                        s = s[:-2]
                    return f"₹{result}"

            return format_indian(amount)
        else:
            return f"${amount:,.2f}"

    def update_summary_cards(self):
        """Update the summary cards with current data."""
        # Get current month's data
        now = datetime.now()
        year = now.year
        month = now.month

        monthly_summary = self.finance_manager.get_monthly_summary(year, month)
        total_balance = sum(
            account.balance for account in self.finance_manager.get_accounts()
        )

        # Update card values
        self.balance_card.set_value(self.format_currency(total_balance))
        self.income_card.set_value(
            self.format_currency(monthly_summary["total_income"])
        )
        self.expenses_card.set_value(
            self.format_currency(monthly_summary["total_expenses"])
        )
        self.savings_card.set_value(
            self.format_currency(monthly_summary["net_savings"])
        )

    def update_expense_chart(self):
        """Update the expense breakdown chart."""
        # Get current month's expenses by category
        now = datetime.now()
        monthly_summary = self.finance_manager.get_monthly_summary(now.year, now.month)

        series = QPieSeries()
        colors = ["#28a745", "#dc3545", "#ffc107", "#17a2b8", "#6610f2", "#e83e8c"]
        for i, (category, amount) in enumerate(
            monthly_summary["expense_by_category"].items()
        ):
            slice = series.append(category, float(amount))
            slice.setLabelVisible(True)
            slice.setLabelColor(QColor("#ffffff"))
            slice.setColor(QColor(colors[i % len(colors)]))

        chart = self.expense_chart.chart()
        chart.removeAllSeries()
        chart.addSeries(series)

    def update_trend_chart(self):
        """Update the balance trend chart."""
        # Get daily balances for the last 30 days
        series = QLineSeries()
        series.setColor(QColor("#007acc"))  # Set line color
        pen = series.pen()
        pen.setWidth(2)
        series.setPen(pen)

        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        daily_balances = self.finance_manager.get_daily_balances(start_date, end_date)
        for date, balance in daily_balances.items():
            series.append(date.timestamp() * 1000, float(balance))

        chart = self.trend_chart.chart()
        chart.removeAllSeries()
        chart.addSeries(series)

        # Create new axes
        date_axis = QDateTimeAxis()
        date_axis.setFormat("MMM dd")
        date_axis.setLabelsColor(QColor("#ffffff"))
        date_axis.setGridLineColor(QColor("#404040"))
        date_axis.setMinorGridLineColor(QColor("#353535"))
        date_axis.setTitleText("Date")
        date_axis.setTitleBrush(QColor("#ffffff"))
        date_axis.setRange(start_date, end_date)

        value_axis = QValueAxis()
        value_axis.setLabelsColor(QColor("#ffffff"))
        value_axis.setGridLineColor(QColor("#404040"))
        value_axis.setMinorGridLineColor(QColor("#353535"))
        value_axis.setTitleText(f"Balance ({self.currency_symbol})")
        value_axis.setTitleBrush(QColor("#ffffff"))

        if daily_balances:
            balances = list(daily_balances.values())
            value_axis.setRange(float(min(balances)), float(max(balances)) * 1.1)
        else:
            value_axis.setRange(0, 100)  # Default range if no data

        # Remove old axes and add new ones
        for old_axis in chart.axes():
            chart.removeAxis(old_axis)

        chart.addAxis(date_axis, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(value_axis, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(date_axis)
        series.attachAxis(value_axis)

    def update_recent_transactions(self):
        """Update the recent transactions list."""
        transactions = self.finance_manager.get_recent_transactions(limit=5)

        if not transactions:
            self.transactions_content.setText("No recent transactions")
            return

        text = ""
        for t in transactions:
            date = t.date.strftime("%d-%m-%Y")  # Indian date format
            amount = self.format_currency(t.amount)
            text += f"{date} - {t.type} - {amount} - {t.description or 'N/A'}\n"

        self.transactions_content.setText(text.strip())

    def refresh_data(self):
        """Refresh all dashboard data."""
        self.update_summary_cards()
        self.update_expense_chart()
        self.update_trend_chart()
        self.update_recent_transactions()
