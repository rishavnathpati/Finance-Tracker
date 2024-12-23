import random
from datetime import datetime, timedelta
from decimal import Decimal

from ..core.finance_manager import FinanceManager
from ..models.models import AccountType, TransactionType


def add_dummy_data(finance_manager: FinanceManager):
    """Add dummy data to the database."""

    # Create accounts
    savings = finance_manager.add_account(
        name="Savings Account",
        account_type=AccountType.SAVINGS,
        balance=Decimal("150000.00"),  # ₹1.5L
    )

    salary = finance_manager.add_account(
        name="Salary Account",
        account_type=AccountType.CHECKING,
        balance=Decimal("50000.00"),  # ₹50K
    )

    credit = finance_manager.add_account(
        name="Credit Card",
        account_type=AccountType.CREDIT_CARD,
        balance=Decimal("0.00"),
    )

    investment = finance_manager.add_account(
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
    for name, type, color in categories:
        category = finance_manager.add_category(name=name, type=type, color_code=color)
        category_ids[name] = category.id

    # Add transactions for the last 3 months
    start_date = datetime.now() - timedelta(days=90)
    current_date = start_date

    while current_date <= datetime.now():
        # Monthly salary (1st of month)
        if current_date.day == 1:
            base_salary = 85000  # ₹85K base
            bonus = random.randint(0, 15000)  # Up to ₹15K bonus
            salary_amount = Decimal(str(base_salary + bonus))
            finance_manager.add_transaction(
                amount=salary_amount,
                transaction_type=TransactionType.INCOME,
                account_id=salary.id,
                category_id=category_ids["Salary"],
                description="Monthly salary",
                date=current_date,
            )

        # Quarterly bonus (every 3 months)
        if current_date.day == 15 and current_date.month % 3 == 0:
            bonus_amount = Decimal(str(random.randint(20000, 50000)))  # ₹20K-50K
            finance_manager.add_transaction(
                amount=bonus_amount,
                transaction_type=TransactionType.INCOME,
                account_id=salary.id,
                category_id=category_ids["Bonus"],
                description="Quarterly performance bonus",
                date=current_date,
            )

        # Monthly rent (5th of month)
        if current_date.day == 5:
            finance_manager.add_transaction(
                amount=Decimal("25000.00"),  # ₹25K rent
                transaction_type=TransactionType.EXPENSE,
                account_id=salary.id,
                category_id=category_ids["Rent"],
                description="Monthly rent",
                date=current_date,
            )

        # Utilities (10th of month)
        if current_date.day == 10:
            # Electricity
            amount = Decimal(str(random.randint(1500, 3000)))  # ₹1.5K-3K
            finance_manager.add_transaction(
                amount=amount,
                transaction_type=TransactionType.EXPENSE,
                account_id=credit.id,
                category_id=category_ids["Utilities"],
                description="Electricity bill",
                date=current_date,
            )

            # Water
            finance_manager.add_transaction(
                amount=Decimal("500.00"),  # ₹500
                transaction_type=TransactionType.EXPENSE,
                account_id=credit.id,
                category_id=category_ids["Utilities"],
                description="Water bill",
                date=current_date,
            )

        # Internet & Mobile (15th of month)
        if current_date.day == 15:
            finance_manager.add_transaction(
                amount=Decimal("1199.00"),  # ₹1,199
                transaction_type=TransactionType.EXPENSE,
                account_id=credit.id,
                category_id=category_ids["Internet & DTH"],
                description="Broadband + DTH",
                date=current_date,
            )
            finance_manager.add_transaction(
                amount=Decimal("699.00"),  # ₹699
                transaction_type=TransactionType.EXPENSE,
                account_id=credit.id,
                category_id=category_ids["Mobile Recharge"],
                description="Mobile recharge",
                date=current_date,
            )

        # Groceries (weekly)
        if current_date.weekday() == 5:  # Saturday
            amount = Decimal(str(random.randint(2000, 4000)))  # ₹2K-4K
            finance_manager.add_transaction(
                amount=amount,
                transaction_type=TransactionType.EXPENSE,
                account_id=credit.id,
                category_id=category_ids["Groceries"],
                description="Weekly groceries",
                date=current_date,
            )

        # Food Delivery (2-3 times per week)
        if random.random() < 0.4:  # 40% chance each day
            amount = Decimal(str(random.randint(200, 800)))  # ₹200-800
            finance_manager.add_transaction(
                amount=amount,
                transaction_type=TransactionType.EXPENSE,
                account_id=credit.id,
                category_id=category_ids["Food Delivery"],
                description="Food delivery",
                date=current_date,
            )

        # Transportation
        if current_date.weekday() < 5:  # Weekdays
            amount = Decimal(str(random.randint(100, 300)))  # ₹100-300
            finance_manager.add_transaction(
                amount=amount,
                transaction_type=TransactionType.EXPENSE,
                account_id=credit.id,
                category_id=category_ids["Transportation"],
                description="Daily commute",
                date=current_date,
            )

        # Monthly SIP (3rd of month)
        if current_date.day == 3:
            finance_manager.add_transaction(
                amount=Decimal("10000.00"),  # ₹10K
                transaction_type=TransactionType.EXPENSE,
                account_id=salary.id,
                category_id=category_ids["Mutual Funds SIP"],
                description="Monthly SIP investment",
                date=current_date,
            )

        # LIC Premium (20th of month)
        if current_date.day == 20:
            finance_manager.add_transaction(
                amount=Decimal("5000.00"),  # ₹5K
                transaction_type=TransactionType.EXPENSE,
                account_id=salary.id,
                category_id=category_ids["LIC"],
                description="LIC premium",
                date=current_date,
            )

        # Investment returns (monthly)
        if current_date.day == 1:
            return_rate = random.uniform(0.008, 0.012)  # 0.8% to 1.2% monthly return
            investment_return = Decimal(str(float(investment.balance) * return_rate))
            finance_manager.add_transaction(
                amount=investment_return,
                transaction_type=TransactionType.INCOME,
                account_id=investment.id,
                category_id=category_ids["Investment Returns"],
                description="Investment returns",
                date=current_date,
            )

        # Shopping (weekends)
        if current_date.weekday() >= 5 and random.random() < 0.4:
            amount = Decimal(str(random.randint(1000, 5000)))  # ₹1K-5K
            finance_manager.add_transaction(
                amount=amount,
                transaction_type=TransactionType.EXPENSE,
                account_id=credit.id,
                category_id=category_ids["Shopping"],
                description="Weekend shopping",
                date=current_date,
            )

        # Healthcare (random)
        if random.random() < 0.05:  # 5% chance each day
            amount = Decimal(str(random.randint(500, 2000)))  # ₹500-2K
            finance_manager.add_transaction(
                amount=amount,
                transaction_type=TransactionType.EXPENSE,
                account_id=credit.id,
                category_id=category_ids["Healthcare"],
                description="Healthcare expense",
                date=current_date,
            )

        current_date += timedelta(days=1)
