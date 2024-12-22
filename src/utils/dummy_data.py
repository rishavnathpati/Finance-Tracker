from decimal import Decimal
from datetime import datetime, timedelta
import random

from ..models.models import TransactionType, AccountType
from ..core.finance_manager import FinanceManager


def add_dummy_data(finance_manager: FinanceManager):
    """Add dummy data to the database."""

    # Create accounts
    checking = finance_manager.create_account(
        name="Checking Account",
        account_type=AccountType.CHECKING,
        initial_balance=Decimal("8000.00"),
        description="Main checking account",
    )

    savings = finance_manager.create_account(
        name="Savings Account",
        account_type=AccountType.SAVINGS,
        initial_balance=Decimal("25000.00"),
        description="Emergency fund and savings",
    )

    credit = finance_manager.create_account(
        name="Credit Card",
        account_type=AccountType.CREDIT_CARD,
        initial_balance=Decimal("0.00"),
        description="Main credit card",
    )

    investment = finance_manager.create_account(
        name="Investment Account",
        account_type=AccountType.INVESTMENT,
        initial_balance=Decimal("50000.00"),
        description="Long-term investments",
    )

    # Create categories with colors
    categories = [
        ("Salary", TransactionType.INCOME, "#28a745"),
        ("Freelance", TransactionType.INCOME, "#20c997"),
        ("Investment Returns", TransactionType.INCOME, "#007bff"),
        ("Rent", TransactionType.EXPENSE, "#dc3545"),
        ("Groceries", TransactionType.EXPENSE, "#ffc107"),
        ("Utilities", TransactionType.EXPENSE, "#17a2b8"),
        ("Internet", TransactionType.EXPENSE, "#6610f2"),
        ("Phone", TransactionType.EXPENSE, "#e83e8c"),
        ("Transportation", TransactionType.EXPENSE, "#fd7e14"),
        ("Entertainment", TransactionType.EXPENSE, "#6f42c1"),
        ("Dining Out", TransactionType.EXPENSE, "#d63384"),
        ("Shopping", TransactionType.EXPENSE, "#0dcaf0"),
        ("Healthcare", TransactionType.EXPENSE, "#198754"),
        ("Insurance", TransactionType.EXPENSE, "#6c757d"),
    ]

    category_ids = {}
    for name, type, color in categories:
        category = finance_manager.create_category(
            name=name, type=type, color_code=color
        )
        category_ids[name] = category.id

    # Add transactions for the last 3 months
    start_date = datetime.now() - timedelta(days=90)
    current_date = start_date

    while current_date <= datetime.now():
        # Monthly salary (around 15th)
        if current_date.day == 15:
            base_salary = 7500
            bonus = random.randint(0, 1000)
            salary = Decimal(str(base_salary + bonus))
            finance_manager.create_transaction(
                type=TransactionType.INCOME,
                amount=salary,
                from_account_id=checking.id,
                category_id=category_ids["Salary"],
                description="Monthly salary",
                date=current_date,
                tags="salary,regular",
            )

        # Freelance income (random days, 2-3 times per month)
        if random.random() < 0.1:  # 10% chance each day
            amount = Decimal(str(random.randint(500, 2000)))
            finance_manager.create_transaction(
                type=TransactionType.INCOME,
                amount=amount,
                from_account_id=checking.id,
                category_id=category_ids["Freelance"],
                description="Freelance project",
                date=current_date,
                tags="freelance",
            )

        # Monthly rent (1st of month)
        if current_date.day == 1:
            finance_manager.create_transaction(
                type=TransactionType.EXPENSE,
                amount=Decimal("2000.00"),
                from_account_id=checking.id,
                category_id=category_ids["Rent"],
                description="Monthly rent",
                date=current_date,
                tags="housing,regular",
            )

        # Utilities (5th of month)
        if current_date.day == 5:
            amount = Decimal(str(random.randint(100, 150)))
            finance_manager.create_transaction(
                type=TransactionType.EXPENSE,
                amount=amount,
                from_account_id=checking.id,
                category_id=category_ids["Utilities"],
                description="Monthly utilities",
                date=current_date,
                tags="utilities,regular",
            )

        # Internet and Phone (10th of month)
        if current_date.day == 10:
            finance_manager.create_transaction(
                type=TransactionType.EXPENSE,
                amount=Decimal("80.00"),
                from_account_id=credit.id,
                category_id=category_ids["Internet"],
                description="Internet bill",
                date=current_date,
                tags="utilities,regular",
            )
            finance_manager.create_transaction(
                type=TransactionType.EXPENSE,
                amount=Decimal("65.00"),
                from_account_id=credit.id,
                category_id=category_ids["Phone"],
                description="Phone bill",
                date=current_date,
                tags="utilities,regular",
            )

        # Groceries (2-3 times per week)
        if random.random() < 0.4:  # 40% chance each day
            amount = Decimal(str(random.randint(50, 150)))
            finance_manager.create_transaction(
                type=TransactionType.EXPENSE,
                amount=amount,
                from_account_id=credit.id,
                category_id=category_ids["Groceries"],
                description="Grocery shopping",
                date=current_date,
                tags="food,regular",
            )

        # Dining Out (2-3 times per week)
        if random.random() < 0.3:  # 30% chance each day
            amount = Decimal(str(random.randint(20, 80)))
            finance_manager.create_transaction(
                type=TransactionType.EXPENSE,
                amount=amount,
                from_account_id=credit.id,
                category_id=category_ids["Dining Out"],
                description="Restaurant",
                date=current_date,
                tags="food,entertainment",
            )

        # Entertainment (weekends)
        if (
            current_date.weekday() >= 5 and random.random() < 0.5
        ):  # 50% chance on weekends
            amount = Decimal(str(random.randint(30, 100)))
            finance_manager.create_transaction(
                type=TransactionType.EXPENSE,
                amount=amount,
                from_account_id=credit.id,
                category_id=category_ids["Entertainment"],
                description="Entertainment",
                date=current_date,
                tags="entertainment,leisure",
            )

        # Shopping (random)
        if random.random() < 0.15:  # 15% chance each day
            amount = Decimal(str(random.randint(50, 200)))
            finance_manager.create_transaction(
                type=TransactionType.EXPENSE,
                amount=amount,
                from_account_id=credit.id,
                category_id=category_ids["Shopping"],
                description="Shopping",
                date=current_date,
                tags="shopping",
            )

        # Transportation
        if random.random() < 0.7:  # 70% chance each day (work days)
            amount = Decimal(str(random.randint(5, 20)))
            finance_manager.create_transaction(
                type=TransactionType.EXPENSE,
                amount=amount,
                from_account_id=credit.id,
                category_id=category_ids["Transportation"],
                description="Transportation",
                date=current_date,
                tags="transport,regular",
            )

        # Healthcare (random)
        if random.random() < 0.05:  # 5% chance each day
            amount = Decimal(str(random.randint(50, 300)))
            finance_manager.create_transaction(
                type=TransactionType.EXPENSE,
                amount=amount,
                from_account_id=credit.id,
                category_id=category_ids["Healthcare"],
                description="Healthcare",
                date=current_date,
                tags="health",
            )

        # Insurance (20th of month)
        if current_date.day == 20:
            finance_manager.create_transaction(
                type=TransactionType.EXPENSE,
                amount=Decimal("150.00"),
                from_account_id=checking.id,
                category_id=category_ids["Insurance"],
                description="Insurance premium",
                date=current_date,
                tags="insurance,regular",
            )

        # Investment returns (monthly)
        if current_date.day == 1:
            return_rate = random.uniform(0.005, 0.015)  # 0.5% to 1.5% monthly return
            investment_return = Decimal(str(float(investment.balance) * return_rate))
            finance_manager.create_transaction(
                type=TransactionType.INCOME,
                amount=investment_return,
                from_account_id=investment.id,
                category_id=category_ids["Investment Returns"],
                description="Investment returns",
                date=current_date,
                tags="investment,returns",
            )

        current_date += timedelta(days=1)
