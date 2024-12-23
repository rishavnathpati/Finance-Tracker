"""Utility module for generating sample data for the Finance Tracker application."""

from datetime import datetime, timedelta
from decimal import Decimal
import random

from src.core.finance_manager import FinanceManager
from src.models.models import TransactionType, AccountType


def add_dummy_data(finance_manager: FinanceManager) -> None:
    """Add sample data to the database.

    This function creates sample accounts, categories, and transactions that
    represent typical Indian financial data including salaries, expenses,
    and investments.

    Args:
        finance_manager (FinanceManager): The finance manager instance to use.
    """
    # Create accounts with Indian currency amounts
    finance_manager.add_account(
        name="Savings Account",
        account_type=AccountType.SAVINGS,
        balance=Decimal("150000.00"),  # ₹1.5L
    )

    salary_account = finance_manager.add_account(
        name="Salary Account",
        account_type=AccountType.CHECKING,
        balance=Decimal("50000.00"),  # ₹50K
    )

    credit_account = finance_manager.add_account(
        name="Credit Card",
        account_type=AccountType.CREDIT_CARD,
        balance=Decimal("0.00"),
    )

    investment_account = finance_manager.add_account(
        name="Investment Account",
        account_type=AccountType.INVESTMENT,
        balance=Decimal("500000.00"),  # ₹5L
    )

    # Create categories with colors
    categories = [
        ("Salary", TransactionType.INCOME, "#28a745"),
        ("Bonus", TransactionType.INCOME, "#20c997"),
        ("Investment Returns", TransactionType.INCOME, "#007bff"),
        ("Rent", TransactionType.EXPENSE, "#dc3545"),
        ("Groceries", TransactionType.EXPENSE, "#ffc107"),
        ("Utilities", TransactionType.EXPENSE, "#17a2b8"),
        ("Internet & DTH", TransactionType.EXPENSE, "#6610f2"),
        ("Mobile Recharge", TransactionType.EXPENSE, "#e83e8c"),
        ("Transportation", TransactionType.EXPENSE, "#fd7e14"),
        ("Entertainment", TransactionType.EXPENSE, "#6f42c1"),
        ("Food Delivery", TransactionType.EXPENSE, "#d63384"),
        ("Shopping", TransactionType.EXPENSE, "#0dcaf0"),
        ("Healthcare", TransactionType.EXPENSE, "#198754"),
        ("Insurance", TransactionType.EXPENSE, "#6c757d"),
        ("Education", TransactionType.EXPENSE, "#495057"),
        ("House Maintenance", TransactionType.EXPENSE, "#343a40"),
        ("Personal Care", TransactionType.EXPENSE, "#7952b3"),
        ("Gifts & Donations", TransactionType.EXPENSE, "#e83e8c"),
        ("LIC", TransactionType.EXPENSE, "#20c997"),
        ("Mutual Funds SIP", TransactionType.EXPENSE, "#0dcaf0"),
    ]

    category_ids = {}
    for name, trans_type, color in categories:
        category = finance_manager.add_category(
            name=name, type=trans_type, color_code=color
        )
        category_ids[name] = category.id

    # Add transactions for the last 3 months
    start_date = datetime.now() - timedelta(days=90)
    current_date = start_date

    while current_date <= datetime.now():
        _add_daily_transactions(
            finance_manager,
            current_date,
            salary_account.id,
            credit_account.id,
            investment_account.id,
            investment_account.balance,
            category_ids,
        )
        current_date += timedelta(days=1)


def _add_daily_transactions(
    finance_manager: FinanceManager,
    date: datetime,
    salary_account_id: int,
    credit_account_id: int,
    investment_account_id: int,
    investment_balance: Decimal,
    category_ids: dict,
) -> None:
    """Add transactions for a specific date.

    Args:
        finance_manager (FinanceManager): The finance manager instance.
        date (datetime): The date to add transactions for.
        salary_account_id (int): ID of the salary account.
        credit_account_id (int): ID of the credit card account.
        investment_account_id (int): ID of the investment account.
        investment_balance (Decimal): Current balance of investment account.
        category_ids (dict): Dictionary mapping category names to IDs.
    """
    # Monthly salary (1st of month)
    if date.day == 1:
        base_salary = 85000  # ₹85K base
        bonus = random.randint(0, 15000)  # Up to ₹15K bonus
        salary_amount = Decimal(str(base_salary + bonus))
        finance_manager.add_transaction(
            amount=salary_amount,
            transaction_type=TransactionType.INCOME,
            account_id=salary_account_id,
            category_id=category_ids["Salary"],
            description="Monthly salary",
            date=date,
        )

    # Quarterly bonus (every 3 months)
    if date.day == 15 and date.month % 3 == 0:
        bonus_amount = Decimal(str(random.randint(20000, 50000)))  # ₹20K-50K
        finance_manager.add_transaction(
            amount=bonus_amount,
            transaction_type=TransactionType.INCOME,
            account_id=salary_account_id,
            category_id=category_ids["Bonus"],
            description="Quarterly performance bonus",
            date=date,
        )

    # Monthly rent (5th of month)
    if date.day == 5:
        finance_manager.add_transaction(
            amount=Decimal("25000.00"),  # ₹25K rent
            transaction_type=TransactionType.EXPENSE,
            account_id=salary_account_id,
            category_id=category_ids["Rent"],
            description="Monthly rent",
            date=date,
        )

    # Utilities (10th of month)
    if date.day == 10:
        # Electricity
        amount = Decimal(str(random.randint(1500, 3000)))  # ₹1.5K-3K
        finance_manager.add_transaction(
            amount=amount,
            transaction_type=TransactionType.EXPENSE,
            account_id=credit_account_id,
            category_id=category_ids["Utilities"],
            description="Electricity bill",
            date=date,
        )

        # Water
        finance_manager.add_transaction(
            amount=Decimal("500.00"),  # ₹500
            transaction_type=TransactionType.EXPENSE,
            account_id=credit_account_id,
            category_id=category_ids["Utilities"],
            description="Water bill",
            date=date,
        )

    # Internet & Mobile (15th of month)
    if date.day == 15:
        finance_manager.add_transaction(
            amount=Decimal("1199.00"),  # ₹1,199
            transaction_type=TransactionType.EXPENSE,
            account_id=credit_account_id,
            category_id=category_ids["Internet & DTH"],
            description="Broadband + DTH",
            date=date,
        )
        finance_manager.add_transaction(
            amount=Decimal("699.00"),  # ₹699
            transaction_type=TransactionType.EXPENSE,
            account_id=credit_account_id,
            category_id=category_ids["Mobile Recharge"],
            description="Mobile recharge",
            date=date,
        )

    # Groceries (weekly)
    if date.weekday() == 5:  # Saturday
        amount = Decimal(str(random.randint(2000, 4000)))  # ₹2K-4K
        finance_manager.add_transaction(
            amount=amount,
            transaction_type=TransactionType.EXPENSE,
            account_id=credit_account_id,
            category_id=category_ids["Groceries"],
            description="Weekly groceries",
            date=date,
        )

    # Food Delivery (2-3 times per week)
    if random.random() < 0.4:  # 40% chance each day
        amount = Decimal(str(random.randint(200, 800)))  # ₹200-800
        finance_manager.add_transaction(
            amount=amount,
            transaction_type=TransactionType.EXPENSE,
            account_id=credit_account_id,
            category_id=category_ids["Food Delivery"],
            description="Food delivery",
            date=date,
        )

    # Transportation
    if date.weekday() < 5:  # Weekdays
        amount = Decimal(str(random.randint(100, 300)))  # ₹100-300
        finance_manager.add_transaction(
            amount=amount,
            transaction_type=TransactionType.EXPENSE,
            account_id=credit_account_id,
            category_id=category_ids["Transportation"],
            description="Daily commute",
            date=date,
        )

    # Monthly SIP (3rd of month)
    if date.day == 3:
        finance_manager.add_transaction(
            amount=Decimal("10000.00"),  # ₹10K
            transaction_type=TransactionType.EXPENSE,
            account_id=salary_account_id,
            category_id=category_ids["Mutual Funds SIP"],
            description="Monthly SIP investment",
            date=date,
        )

    # LIC Premium (20th of month)
    if date.day == 20:
        finance_manager.add_transaction(
            amount=Decimal("5000.00"),  # ₹5K
            transaction_type=TransactionType.EXPENSE,
            account_id=salary_account_id,
            category_id=category_ids["LIC"],
            description="LIC premium",
            date=date,
        )

    # Investment returns (monthly)
    if date.day == 1:
        # 0.8% to 1.2% monthly return
        return_rate = random.uniform(0.008, 0.012)
        investment_return = Decimal(str(float(investment_balance) * return_rate))
        finance_manager.add_transaction(
            amount=investment_return,
            transaction_type=TransactionType.INCOME,
            account_id=investment_account_id,
            category_id=category_ids["Investment Returns"],
            description="Investment returns",
            date=date,
        )

    # Shopping (weekends)
    if date.weekday() >= 5 and random.random() < 0.4:
        amount = Decimal(str(random.randint(1000, 5000)))  # ₹1K-5K
        finance_manager.add_transaction(
            amount=amount,
            transaction_type=TransactionType.EXPENSE,
            account_id=credit_account_id,
            category_id=category_ids["Shopping"],
            description="Weekend shopping",
            date=date,
        )

    # Healthcare (random)
    if random.random() < 0.05:  # 5% chance each day
        amount = Decimal(str(random.randint(500, 2000)))  # ₹500-2K
        finance_manager.add_transaction(
            amount=amount,
            transaction_type=TransactionType.EXPENSE,
            account_id=credit_account_id,
            category_id=category_ids["Healthcare"],
            description="Healthcare expense",
            date=date,
        )
