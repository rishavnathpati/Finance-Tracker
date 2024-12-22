"""Visualization utilities for the Finance Tracker application."""

from typing import Dict, List, Any
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta

from ..models.models import Transaction


class FinanceVisualizer:
    """Class for generating financial visualizations."""

    @staticmethod
    def create_expense_pie_chart(
        expenses_by_category: Dict[str, float], title: str = "Expenses by Category"
    ) -> plt.Figure:
        """Create a pie chart showing expense distribution by category."""
        fig, ax = plt.subplots(figsize=(10, 8))

        # Sort categories by amount
        categories = sorted(
            expenses_by_category.items(), key=lambda x: x[1], reverse=True
        )
        labels = [cat[0] for cat in categories]
        values = [cat[1] for cat in categories]

        # Create pie chart
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        ax.set_title(title)

        return fig

    @staticmethod
    def create_income_expense_bar_chart(
        monthly_data: List[Dict[str, Any]]
    ) -> plt.Figure:
        """Create a bar chart comparing income and expenses over time."""
        fig, ax = plt.subplots(figsize=(12, 6))

        # Extract data
        months = [item["month"] for item in monthly_data]
        income = [item["income"] for item in monthly_data]
        expenses = [item["expenses"] for item in monthly_data]

        # Set up bar positions
        x = range(len(months))
        width = 0.35

        # Create bars
        ax.bar([i - width / 2 for i in x], income, width, label="Income")
        ax.bar([i + width / 2 for i in x], expenses, width, label="Expenses")

        # Customize chart
        ax.set_ylabel("Amount")
        ax.set_title("Monthly Income vs Expenses")
        ax.set_xticks(x)
        ax.set_xticklabels(months)
        ax.legend()

        return fig

    @staticmethod
    def create_spending_trend_line(
        transactions: List[Transaction], days: int = 30
    ) -> plt.Figure:
        """Create a line chart showing spending trends over time."""
        fig, ax = plt.subplots(figsize=(12, 6))

        # Convert transactions to DataFrame
        df = pd.DataFrame(
            [
                {"date": t.date, "amount": float(t.amount), "type": t.type.value}
                for t in transactions
            ]
        )

        # Group by date and calculate daily totals
        daily_totals = df.groupby("date")["amount"].sum()

        # Create date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        date_range = pd.date_range(start=start_date, end=end_date)

        # Reindex to include all dates and fill missing values with 0
        daily_totals = daily_totals.reindex(date_range, fill_value=0)

        # Calculate cumulative sum
        cumulative_spending = daily_totals.cumsum()

        # Create line plot
        ax.plot(cumulative_spending.index, cumulative_spending.values)
        ax.set_xlabel("Date")
        ax.set_ylabel("Cumulative Spending")
        ax.set_title(f"Spending Trend (Last {days} Days)")

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)

        return fig

    @staticmethod
    def create_interactive_dashboard(transactions: List[Transaction]) -> go.Figure:
        """Create an interactive dashboard using Plotly."""
        # Create figure with subplots
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "Expenses by Category",
                "Monthly Income vs Expenses",
                "Daily Spending",
                "Category Distribution",
            ),
        )

        # Convert transactions to DataFrame
        df = pd.DataFrame(
            [
                {
                    "date": t.date,
                    "amount": float(t.amount),
                    "type": t.type.value,
                    "category": t.category.name,
                }
                for t in transactions
            ]
        )

        # 1. Expenses by Category (Pie Chart)
        expenses = df[df["type"] == "expense"].groupby("category")["amount"].sum()
        fig.add_trace(
            go.Pie(labels=expenses.index, values=expenses.values), row=1, col=1
        )

        # 2. Monthly Income vs Expenses (Bar Chart)
        monthly = df.set_index("date").resample("M").sum()
        fig.add_trace(
            go.Bar(x=monthly.index, y=monthly["amount"], name="Monthly Total"),
            row=1,
            col=2,
        )

        # 3. Daily Spending (Line Chart)
        daily = df[df["type"] == "expense"].groupby("date")["amount"].sum()
        fig.add_trace(
            go.Scatter(
                x=daily.index, y=daily.values, mode="lines", name="Daily Spending"
            ),
            row=2,
            col=1,
        )

        # 4. Category Distribution (Bar Chart)
        category_dist = df.groupby("category")["amount"].sum()
        fig.add_trace(
            go.Bar(
                x=category_dist.index, y=category_dist.values, name="Category Total"
            ),
            row=2,
            col=2,
        )

        # Update layout
        fig.update_layout(
            height=800, showlegend=False, title_text="Financial Dashboard"
        )

        return fig

    @staticmethod
    def save_visualization(fig: plt.Figure, filename: str):
        """Save a visualization to file."""
        fig.savefig(filename, bbox_inches="tight")
        plt.close(fig)

    @staticmethod
    def save_interactive_dashboard(fig: go.Figure, filename: str):
        """Save an interactive dashboard to HTML file."""
        fig.write_html(filename)
