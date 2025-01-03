"""Reports widget for displaying financial analytics and reports."""

import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Tuple

from PyQt6.QtCharts import (
    QBarCategoryAxis,
    QBarSeries,
    QBarSet,
    QChart,
    QChartView,
    QDateTimeAxis,
    QLineSeries,
    QPieSeries,
    QValueAxis,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QPainter
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.core.finance_manager import FinanceManager
from src.gui.style import (
    ACTION_BUTTON_STYLE,
    CARD_STYLE,
    CARD_TITLE_STYLE,
    INPUT_STYLE,
    TAB_STYLE,
)
from src.gui.widgets.summary_card import SummaryCard
from src.utils.config_manager import get_config
from src.utils.formatting import format_currency

logger = logging.getLogger(__name__)


class ReportsWidget(QWidget):
    """Widget for viewing financial reports and analytics."""

    def __init__(self, finance_manager: FinanceManager):
        """Initialize the reports widget.

        Args:
            finance_manager: The finance manager instance
        """
        logger.debug("Initializing ReportsWidget")
        super().__init__()
        self.finance_manager = finance_manager
        self.config = get_config()
        self.currency_symbol = self.config.get("currency", {}).get(
            "display_symbol", "₹"
        )
        logger.debug("Calling init_ui")
        self.init_ui()
        logger.debug("ReportsWidget initialization complete")

    def init_ui(self):
        """Initialize the user interface with charts and reports."""
        logger.debug("Setting up ReportsWidget UI")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        title = QLabel("Reports & Analytics")
        title.setStyleSheet(
            "font-size: 24px; color: white; font-weight: bold;"
        )
        layout.addWidget(title)

        # Time period selector
        period_layout = QHBoxLayout()

        self.year_spin = QSpinBox()
        self.year_spin.setStyleSheet(INPUT_STYLE)
        self.year_spin.setRange(2000, 2100)
        self.year_spin.setValue(datetime.now().year)

        self.month_combo = QComboBox()
        self.month_combo.setStyleSheet(INPUT_STYLE)
        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        self.month_combo.addItems(months)
        self.month_combo.setCurrentIndex(datetime.now().month - 1)

        refresh_button = QPushButton("Refresh")
        refresh_button.setStyleSheet(ACTION_BUTTON_STYLE)
        refresh_button.clicked.connect(self.refresh_data)

        period_layout.addWidget(QLabel("Year:"))
        period_layout.addWidget(self.year_spin)
        period_layout.addWidget(QLabel("Month:"))
        period_layout.addWidget(self.month_combo)
        period_layout.addWidget(refresh_button)
        period_layout.addStretch()

        layout.addLayout(period_layout)

        # Tab widget for different reports
        tabs = QTabWidget()
        tabs.setStyleSheet(TAB_STYLE)

        # Monthly Overview Tab
        overview_tab = QScrollArea()
        overview_tab.setWidgetResizable(True)
        overview_content = QWidget()
        overview_layout = QVBoxLayout(overview_content)
        overview_layout.setSpacing(20)

        # Summary cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        self.income_card = SummaryCard(
            "Total Income", f"{self.currency_symbol}0.00", "📈"
        )
        self.expenses_card = SummaryCard(
            "Total Expenses", f"{self.currency_symbol}0.00", "📉"
        )
        self.savings_card = SummaryCard(
            "Net Savings", f"{self.currency_symbol}0.00", "💰"
        )
        self.savings_rate_card = SummaryCard("Savings Rate", "0%", "📊")

        cards_layout.addWidget(self.income_card)
        cards_layout.addWidget(self.expenses_card)
        cards_layout.addWidget(self.savings_card)
        cards_layout.addWidget(self.savings_rate_card)

        overview_layout.addLayout(cards_layout)

        # Charts
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)

        # Expense by Category Chart
        expense_chart_container = QFrame()
        expense_chart_container.setStyleSheet(CARD_STYLE)
        expense_chart_layout = QVBoxLayout(expense_chart_container)
        expense_chart_layout.setContentsMargins(15, 15, 15, 15)

        expense_chart_title = QLabel("Expenses by Category")
        expense_chart_title.setStyleSheet(CARD_TITLE_STYLE)
        expense_chart_layout.addWidget(expense_chart_title)

        self.expense_chart = self.create_pie_chart()
        expense_chart_layout.addWidget(self.expense_chart)

        charts_layout.addWidget(expense_chart_container)

        # Daily Balance Chart
        balance_chart_container = QFrame()
        balance_chart_container.setStyleSheet(CARD_STYLE)
        balance_chart_layout = QVBoxLayout(balance_chart_container)
        balance_chart_layout.setContentsMargins(15, 15, 15, 15)

        balance_chart_title = QLabel("Daily Balance")
        balance_chart_title.setStyleSheet(CARD_TITLE_STYLE)
        balance_chart_layout.addWidget(balance_chart_title)

        self.balance_chart = self.create_line_chart("Balance")
        balance_chart_layout.addWidget(self.balance_chart)

        charts_layout.addWidget(balance_chart_container)

        overview_layout.addLayout(charts_layout)

        # Income vs Expenses Bar Chart
        comparison_chart_container = QFrame()
        comparison_chart_container.setStyleSheet(CARD_STYLE)
        comparison_chart_layout = QVBoxLayout(comparison_chart_container)
        comparison_chart_layout.setContentsMargins(15, 15, 15, 15)

        comparison_chart_title = QLabel("Income vs Expenses")
        comparison_chart_title.setStyleSheet(CARD_TITLE_STYLE)
        comparison_chart_layout.addWidget(comparison_chart_title)

        self.comparison_chart = self.create_bar_chart()
        comparison_chart_layout.addWidget(self.comparison_chart)

        overview_layout.addWidget(comparison_chart_container)

        overview_tab.setWidget(overview_content)
        tabs.addTab(overview_tab, "Monthly Overview")

        # Trends Tab
        trends_tab = QScrollArea()
        trends_tab.setWidgetResizable(True)
        trends_content = QWidget()
        trends_layout = QVBoxLayout(trends_content)
        trends_layout.setSpacing(20)

        # Income Trend Chart
        income_trend_container = QFrame()
        income_trend_container.setStyleSheet(CARD_STYLE)
        income_trend_layout = QVBoxLayout(income_trend_container)
        income_trend_layout.setContentsMargins(15, 15, 15, 15)

        income_trend_title = QLabel("Income Trend")
        income_trend_title.setStyleSheet(CARD_TITLE_STYLE)
        income_trend_layout.addWidget(income_trend_title)

        self.income_trend_chart = self.create_line_chart("Income")
        income_trend_layout.addWidget(self.income_trend_chart)

        trends_layout.addWidget(income_trend_container)

        # Expense Trend Chart
        expense_trend_container = QFrame()
        expense_trend_container.setStyleSheet(CARD_STYLE)
        expense_trend_layout = QVBoxLayout(expense_trend_container)
        expense_trend_layout.setContentsMargins(15, 15, 15, 15)

        expense_trend_title = QLabel("Expense Trend")
        expense_trend_title.setStyleSheet(CARD_TITLE_STYLE)
        expense_trend_layout.addWidget(expense_trend_title)

        self.expense_trend_chart = self.create_line_chart("Expenses")
        expense_trend_layout.addWidget(self.expense_trend_chart)

        trends_layout.addWidget(expense_trend_container)

        # Savings Rate Trend Chart
        savings_trend_container = QFrame()
        savings_trend_container.setStyleSheet(CARD_STYLE)
        savings_trend_layout = QVBoxLayout(savings_trend_container)
        savings_trend_layout.setContentsMargins(15, 15, 15, 15)

        savings_trend_title = QLabel("Savings Rate Trend")
        savings_trend_title.setStyleSheet(CARD_TITLE_STYLE)
        savings_trend_layout.addWidget(savings_trend_title)

        self.savings_trend_chart = self.create_line_chart("Savings Rate (%)")
        savings_trend_layout.addWidget(self.savings_trend_chart)

        trends_layout.addWidget(savings_trend_container)

        trends_tab.setWidget(trends_content)
        tabs.addTab(trends_tab, "Trends")

        layout.addWidget(tabs)

        # Initial data load
        self.refresh_data()

        logger.debug("ReportsWidget UI setup complete")

    def create_pie_chart(self) -> QChartView:
        """Create a pie chart."""
        series = QPieSeries()

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setBackgroundVisible(True)
        chart.setBackgroundBrush(QBrush(QColor("#2d2d2d")))
        chart.legend().setVisible(True)
        chart.legend().setLabelColor(QColor("#ffffff"))
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setMinimumHeight(300)

        return chart_view

    def create_line_chart(self, value_title: str) -> QChartView:
        """Create a line chart."""
        series = QLineSeries()
        series.setColor(QColor("#007acc"))  # Set line color
        pen = series.pen()
        pen.setWidth(2)
        series.setPen(pen)

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setBackgroundVisible(True)
        chart.setBackgroundBrush(QBrush(QColor("#2d2d2d")))
        chart.legend().setVisible(False)

        date_axis = QDateTimeAxis()
        date_axis.setFormat("dd-MM-yyyy")  # Indian date format
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
        value_axis.setTitleText(f"{value_title} ({self.currency_symbol})")
        value_axis.setTitleBrush(QColor("#ffffff"))
        chart.addAxis(value_axis, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(value_axis)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setMinimumHeight(300)

        return chart_view

    def create_bar_chart(self) -> QChartView:
        """Create a bar chart."""
        series = QBarSeries()

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setBackgroundVisible(True)
        chart.setBackgroundBrush(QBrush(QColor("#2d2d2d")))
        chart.legend().setVisible(True)
        chart.legend().setLabelColor(QColor("#ffffff"))
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignTop)

        categories_axis = QBarCategoryAxis()
        categories_axis.setLabelsColor(QColor("#ffffff"))
        categories_axis.setGridLineColor(QColor("#404040"))
        categories_axis.setMinorGridLineColor(QColor("#353535"))
        categories_axis.setTitleText("Month")
        categories_axis.setTitleBrush(QColor("#ffffff"))
        chart.addAxis(categories_axis, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(categories_axis)

        value_axis = QValueAxis()
        value_axis.setLabelsColor(QColor("#ffffff"))
        value_axis.setGridLineColor(QColor("#404040"))
        value_axis.setMinorGridLineColor(QColor("#353535"))
        value_axis.setTitleText(f"Amount ({self.currency_symbol})")
        value_axis.setTitleBrush(QColor("#ffffff"))
        chart.addAxis(value_axis, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(value_axis)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setMinimumHeight(300)

        return chart_view

    def update_summary_cards(self, monthly_summary: Dict):
        """Update the summary cards with current data."""
        self.income_card.set_value(
            format_currency(monthly_summary["total_income"], self.config)
        )
        self.expenses_card.set_value(
            format_currency(monthly_summary["total_expenses"], self.config)
        )
        self.savings_card.set_value(
            format_currency(monthly_summary["net_savings"], self.config)
        )

        if monthly_summary["total_income"] > 0:
            savings_rate = (
                monthly_summary["net_savings"]
                / monthly_summary["total_income"]
            ) * 100
            self.savings_rate_card.set_value(f"{savings_rate:.1f}%")
        else:
            self.savings_rate_card.set_value("0.0%")

    def update_expense_chart(self, expense_data: Dict[str, Decimal]):
        """Update the expense breakdown pie chart."""
        series = QPieSeries()
        colors = [
            "#28a745",
            "#dc3545",
            "#ffc107",
            "#17a2b8",
            "#6610f2",
            "#e83e8c",
        ]
        for i, (category, amount) in enumerate(expense_data.items()):
            slice = series.append(
                f"{category}\n({format_currency(amount, self.config)})",
                float(amount),
            )
            slice.setLabelVisible(True)
            slice.setLabelColor(QColor("#ffffff"))
            slice.setColor(QColor(colors[i % len(colors)]))

        chart = self.expense_chart.chart()
        chart.removeAllSeries()
        chart.addSeries(series)

    def update_balance_chart(self, daily_balances: Dict[datetime, Decimal]):
        """Update the daily balance line chart."""
        series = QLineSeries()
        series.setColor(QColor("#007acc"))  # Set line color
        pen = series.pen()
        pen.setWidth(2)
        series.setPen(pen)

        for date, balance in daily_balances.items():
            series.append(date.timestamp() * 1000, float(balance))

        chart = self.balance_chart.chart()
        chart.removeAllSeries()
        chart.addSeries(series)

        if daily_balances:
            dates = list(daily_balances.keys())
            balances = list(daily_balances.values())

            # Create new axes
            date_axis = QDateTimeAxis()
            date_axis.setFormat("dd-MM-yyyy")  # Indian date format
            date_axis.setLabelsColor(QColor("#ffffff"))
            date_axis.setGridLineColor(QColor("#404040"))
            date_axis.setMinorGridLineColor(QColor("#353535"))
            date_axis.setTitleText("Date")
            date_axis.setTitleBrush(QColor("#ffffff"))
            date_axis.setRange(dates[0], dates[-1])

            value_axis = QValueAxis()
            value_axis.setLabelsColor(QColor("#ffffff"))
            value_axis.setGridLineColor(QColor("#404040"))
            value_axis.setMinorGridLineColor(QColor("#353535"))
            value_axis.setTitleText(f"Balance ({self.currency_symbol})")
            value_axis.setTitleBrush(QColor("#ffffff"))
            value_axis.setRange(
                float(min(balances)), float(max(balances)) * 1.1
            )

            # Remove old axes and add new ones
            for old_axis in chart.axes():
                chart.removeAxis(old_axis)

            chart.addAxis(date_axis, Qt.AlignmentFlag.AlignBottom)
            chart.addAxis(value_axis, Qt.AlignmentFlag.AlignLeft)
            series.attachAxis(date_axis)
            series.attachAxis(value_axis)

    def update_comparison_chart(
        self, monthly_data: List[Tuple[str, Decimal, Decimal]]
    ):
        """Update the income vs expenses bar chart."""
        income_set = QBarSet("Income")
        income_set.setColor(QColor("#28a745"))  # Green for income
        expense_set = QBarSet("Expenses")
        expense_set.setColor(QColor("#dc3545"))  # Red for expenses
        categories = []

        for month, income, expense in monthly_data:
            categories.append(month)
            income_set.append(float(income))
            expense_set.append(float(expense))

        series = QBarSeries()
        series.append(income_set)
        series.append(expense_set)

        chart = self.comparison_chart.chart()
        chart.removeAllSeries()
        chart.addSeries(series)

        # Create new axes
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setLabelsColor(QColor("#ffffff"))
        axis_x.setGridLineColor(QColor("#404040"))
        axis_x.setMinorGridLineColor(QColor("#353535"))
        axis_x.setTitleText("Month")
        axis_x.setTitleBrush(QColor("#ffffff"))

        axis_y = QValueAxis()
        axis_y.setLabelsColor(QColor("#ffffff"))
        axis_y.setGridLineColor(QColor("#404040"))
        axis_y.setMinorGridLineColor(QColor("#353535"))
        axis_y.setTitleText(f"Amount ({self.currency_symbol})")
        axis_y.setTitleBrush(QColor("#ffffff"))

        if monthly_data:
            max_value = max(max(income_set), max(expense_set))
            axis_y.setRange(0, max_value * 1.1)

        # Remove old axes and add new ones
        for old_axis in chart.axes():
            chart.removeAxis(old_axis)

        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

    def update_trend_charts(
        self, trend_data: List[Tuple[datetime, Decimal, Decimal, Decimal]]
    ):
        """Update all trend charts."""
        income_series = QLineSeries()
        income_series.setColor(QColor("#28a745"))  # Green for income
        pen = income_series.pen()
        pen.setWidth(2)
        income_series.setPen(pen)

        expense_series = QLineSeries()
        expense_series.setColor(QColor("#dc3545"))  # Red for expenses
        pen = expense_series.pen()
        pen.setWidth(2)
        expense_series.setPen(pen)

        savings_rate_series = QLineSeries()
        savings_rate_series.setColor(
            QColor("#007acc")
        )  # Blue for savings rate
        pen = savings_rate_series.pen()
        pen.setWidth(2)
        savings_rate_series.setPen(pen)

        for date, income, expense, savings_rate in trend_data:
            timestamp = date.timestamp() * 1000
            income_series.append(timestamp, float(income))
            expense_series.append(timestamp, float(expense))
            savings_rate_series.append(timestamp, float(savings_rate))

        # Update Income Trend Chart
        chart = self.income_trend_chart.chart()
        chart.removeAllSeries()
        chart.addSeries(income_series)

        if trend_data:
            dates = [d[0] for d in trend_data]
            incomes = [d[1] for d in trend_data]

            # Create new axes
            date_axis = QDateTimeAxis()
            date_axis.setFormat("dd-MM-yyyy")  # Indian date format
            date_axis.setLabelsColor(QColor("#ffffff"))
            date_axis.setGridLineColor(QColor("#404040"))
            date_axis.setMinorGridLineColor(QColor("#353535"))
            date_axis.setTitleText("Date")
            date_axis.setTitleBrush(QColor("#ffffff"))
            date_axis.setRange(dates[0], dates[-1])

            value_axis = QValueAxis()
            value_axis.setLabelsColor(QColor("#ffffff"))
            value_axis.setGridLineColor(QColor("#404040"))
            value_axis.setMinorGridLineColor(QColor("#353535"))
            value_axis.setTitleText(f"Income ({self.currency_symbol})")
            value_axis.setTitleBrush(QColor("#ffffff"))
            value_axis.setRange(0, float(max(incomes)) * 1.1)

            # Remove old axes and add new ones
            for old_axis in chart.axes():
                chart.removeAxis(old_axis)

            chart.addAxis(date_axis, Qt.AlignmentFlag.AlignBottom)
            chart.addAxis(value_axis, Qt.AlignmentFlag.AlignLeft)
            income_series.attachAxis(date_axis)
            income_series.attachAxis(value_axis)

        # Update Expense Trend Chart
        chart = self.expense_trend_chart.chart()
        chart.removeAllSeries()
        chart.addSeries(expense_series)

        if trend_data:
            expenses = [d[2] for d in trend_data]

            # Create new axes
            date_axis = QDateTimeAxis()
            date_axis.setFormat("dd-MM-yyyy")  # Indian date format
            date_axis.setLabelsColor(QColor("#ffffff"))
            date_axis.setGridLineColor(QColor("#404040"))
            date_axis.setMinorGridLineColor(QColor("#353535"))
            date_axis.setTitleText("Date")
            date_axis.setTitleBrush(QColor("#ffffff"))
            date_axis.setRange(dates[0], dates[-1])

            value_axis = QValueAxis()
            value_axis.setLabelsColor(QColor("#ffffff"))
            value_axis.setGridLineColor(QColor("#404040"))
            value_axis.setMinorGridLineColor(QColor("#353535"))
            value_axis.setTitleText(f"Expenses ({self.currency_symbol})")
            value_axis.setTitleBrush(QColor("#ffffff"))
            value_axis.setRange(0, float(max(expenses)) * 1.1)

            # Remove old axes and add new ones
            for old_axis in chart.axes():
                chart.removeAxis(old_axis)

            chart.addAxis(date_axis, Qt.AlignmentFlag.AlignBottom)
            chart.addAxis(value_axis, Qt.AlignmentFlag.AlignLeft)
            expense_series.attachAxis(date_axis)
            expense_series.attachAxis(value_axis)

        # Update Savings Rate Trend Chart
        chart = self.savings_trend_chart.chart()
        chart.removeAllSeries()
        chart.addSeries(savings_rate_series)

        if trend_data:
            savings_rates = [d[3] for d in trend_data]

            # Create new axes
            date_axis = QDateTimeAxis()
            date_axis.setFormat("dd-MM-yyyy")  # Indian date format
            date_axis.setLabelsColor(QColor("#ffffff"))
            date_axis.setGridLineColor(QColor("#404040"))
            date_axis.setMinorGridLineColor(QColor("#353535"))
            date_axis.setTitleText("Date")
            date_axis.setTitleBrush(QColor("#ffffff"))
            date_axis.setRange(dates[0], dates[-1])

            value_axis = QValueAxis()
            value_axis.setLabelsColor(QColor("#ffffff"))
            value_axis.setGridLineColor(QColor("#404040"))
            value_axis.setMinorGridLineColor(QColor("#353535"))
            value_axis.setTitleText("Savings Rate (%)")
            value_axis.setTitleBrush(QColor("#ffffff"))
            value_axis.setRange(0, float(max(savings_rates)) * 1.1)

            # Remove old axes and add new ones
            for old_axis in chart.axes():
                chart.removeAxis(old_axis)

            chart.addAxis(date_axis, Qt.AlignmentFlag.AlignBottom)
            chart.addAxis(value_axis, Qt.AlignmentFlag.AlignLeft)
            savings_rate_series.attachAxis(date_axis)
            savings_rate_series.attachAxis(value_axis)

    def refresh_data(self):
        """Refresh all report data."""
        year = self.year_spin.value()
        month = self.month_combo.currentIndex() + 1

        # Get monthly summary
        monthly_summary = self.finance_manager.get_monthly_summary(year, month)
        self.update_summary_cards(monthly_summary)

        # Update expense breakdown chart
        self.update_expense_chart(monthly_summary["expense_by_category"])

        # Get and update daily balances
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        daily_balances = self.finance_manager.get_daily_balances(
            start_date, end_date
        )
        self.update_balance_chart(daily_balances)

        # Get and update monthly comparison data
        monthly_data = self.finance_manager.get_monthly_comparison(year)
        self.update_comparison_chart(monthly_data)

        # Get and update trend data
        trend_data = self.finance_manager.get_trends(months=12)
        self.update_trend_charts(trend_data)
