"""Core module for managing financial data and operations."""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple, Union

from sqlalchemy import and_, case, desc, extract, func, or_
from sqlalchemy.orm import Session, joinedload

from src.models.models import (
    Account,
    AccountType,
    Category,
    Transaction,
    TransactionType,
)


class FinanceManager:
    """Main class for managing financial operations and data."""

    def __init__(self, db: Session) -> None:
        """Initialize the finance manager.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db

    # Account Management Methods
    def get_accounts(self) -> List[Account]:
        """Get all accounts.

        Returns:
            List[Account]: List of all accounts.
        """
        return self.db.query(Account).all()

    def get_account(self, account_id: int) -> Optional[Account]:
        """Get an account by its ID.

        Args:
            account_id (int): The account ID to look up.

        Returns:
            Optional[Account]: The account if found, None otherwise.
        """
        return self.db.get(Account, account_id)

    def add_account(
        self, name: str, account_type: AccountType, balance: float = 0.0
    ) -> Account:
        """Add a new account.

        Args:
            name (str): Account name.
            account_type (AccountType): Type of account.
            balance (float, optional): Initial balance. Defaults to 0.0.

        Returns:
            Account: The created account.
        """
        account = Account(
            name=name, type=account_type, balance=Decimal(str(balance))
        )
        self.db.add(account)
        self.db.commit()
        return account

    def update_account_balance(
        self, account_id: int, new_balance: float
    ) -> Optional[Account]:
        """Update an account's balance.

        Args:
            account_id (int): The account ID to update.
            new_balance (float): The new balance amount.

        Returns:
            Optional[Account]: The updated account if found, None otherwise.
        """
        account = self.get_account(account_id)
        if account:
            account.balance = Decimal(str(new_balance))
            self.db.commit()
        return account

    # Category Management Methods
    def get_categories(self) -> List[Category]:
        """Get all categories.

        Returns:
            List[Category]: List of all categories.
        """
        return self.db.query(Category).all()

    def get_category(self, category_id: int) -> Optional[Category]:
        """Get a category by its ID.

        Args:
            category_id (int): The category ID to look up.

        Returns:
            Optional[Category]: The category if found, None otherwise.
        """
        return self.db.get(Category, category_id)

    def add_category(
        self,
        name: str,
        type: TransactionType,
        color_code: Optional[str] = None,
    ) -> Category:
        """Add a new category.

        Args:
            name (str): Category name.
            type (TransactionType): Type of transactions in this category.
            color_code (Optional[str], optional): Color for UI. Defaults to None.

        Returns:
            Category: The created category.
        """
        category = Category(name=name, type=type, color_code=color_code)
        self.db.add(category)
        self.db.commit()
        return category

    def update_category(
        self,
        category_id: int,
        name: Optional[str] = None,
        type: Optional[TransactionType] = None,
        color_code: Optional[str] = None,
    ) -> Optional[Category]:
        """Update a category.

        Args:
            category_id (int): The category ID to update.
            name (Optional[str], optional): New name. Defaults to None.
            type (Optional[TransactionType], optional): New type. Defaults to None.
            color_code (Optional[str], optional): New color. Defaults to None.

        Returns:
            Optional[Category]: The updated category if found, None otherwise.
        """
        category = self.get_category(category_id)
        if category:
            if name is not None:
                category.name = name
            if type is not None:
                category.type = type
            if color_code is not None:
                category.color_code = color_code
            self.db.commit()
        return category

    def delete_category(self, category_id: int) -> bool:
        """Delete a category.

        Args:
            category_id (int): The category ID to delete.

        Returns:
            bool: True if deleted, False if not found.
        """
        category = self.get_category(category_id)
        if category:
            self.db.delete(category)
            self.db.commit()
            return True
        return False

    # Transaction Management Methods
    def get_transaction(self, transaction_id: int) -> Optional[Transaction]:
        """Get a transaction by its ID.

        Args:
            transaction_id (int): The transaction ID to look up.

        Returns:
            Optional[Transaction]: The transaction if found, None otherwise.
        """
        return (
            self.db.query(Transaction)
            .options(
                joinedload(Transaction.from_account),
                joinedload(Transaction.to_account),
                joinedload(Transaction.category),
            )
            .filter(Transaction.id == transaction_id)
            .first()
        )

    def get_transactions(
        self, limit: Optional[int] = None
    ) -> List[Transaction]:
        """Get all transactions, optionally limited.

        Args:
            limit (Optional[int], optional): Max number to return. Defaults to None.

        Returns:
            List[Transaction]: List of transactions.
        """
        query = self.db.query(Transaction).order_by(desc(Transaction.date))
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_recent_transactions(self, limit: int = 5) -> List[Transaction]:
        """Get recent transactions.

        Args:
            limit (int, optional): Max number to return. Defaults to 5.

        Returns:
            List[Transaction]: List of recent transactions.
        """
        return (
            self.db.query(Transaction)
            .options(
                joinedload(Transaction.from_account),
                joinedload(Transaction.to_account),
                joinedload(Transaction.category),
            )
            .order_by(desc(Transaction.date))
            .limit(limit)
            .all()
        )

    def search_transactions(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        transaction_type: Optional[str] = None,
        account_id: Optional[int] = None,
    ) -> List[Transaction]:
        """Search transactions with filters.

        Args:
            start_date (Optional[datetime], optional): Start date. Defaults to None.
            end_date (Optional[datetime], optional): End date. Defaults to None.
            transaction_type (Optional[str], optional): Type filter. Defaults to None.
            account_id (Optional[int], optional): Account filter. Defaults to None.

        Returns:
            List[Transaction]: List of matching transactions.
        """
        query = self.db.query(Transaction).options(
            joinedload(Transaction.from_account),
            joinedload(Transaction.to_account),
            joinedload(Transaction.category),
        )

        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        if transaction_type:
            query = query.filter(Transaction.type == transaction_type)
        if account_id:
            query = query.filter(
                or_(
                    Transaction.from_account_id == account_id,
                    Transaction.to_account_id == account_id,
                )
            )

        return query.order_by(desc(Transaction.date)).all()

    def create_transaction(self, **data: Any) -> Transaction:
        """Create a new transaction.

        Args:
            **data: Transaction data fields.

        Returns:
            Transaction: The created transaction.
        """
        if "amount" in data:
            data["amount"] = Decimal(str(data["amount"]))
        transaction = Transaction(**data)
        self.db.add(transaction)
        self.db.commit()
        return transaction

    def update_transaction(
        self, transaction_id: int, **data: Any
    ) -> Optional[Transaction]:
        """Update an existing transaction.

        Args:
            transaction_id (int): The transaction ID to update.
            **data: Transaction data fields to update.

        Returns:
            Optional[Transaction]: The updated transaction if found, None otherwise.
        """
        transaction = self.get_transaction(transaction_id)
        if transaction:
            if "amount" in data:
                data["amount"] = Decimal(str(data["amount"]))
            for key, value in data.items():
                setattr(transaction, key, value)
            self.db.commit()
        return transaction

    def delete_transaction(self, transaction_id: int) -> bool:
        """Delete a transaction.

        Args:
            transaction_id (int): The transaction ID to delete.

        Returns:
            bool: True if deleted, False if not found.
        """
        transaction = self.get_transaction(transaction_id)
        if transaction:
            self.db.delete(transaction)
            self.db.commit()
            return True
        return False

    def add_transaction(
        self,
        amount: float,
        transaction_type: TransactionType,
        account_id: int,
        category_id: int,
        description: str = "",
        date: Optional[datetime] = None,
    ) -> Transaction:
        """Add a new transaction.

        Args:
            amount (float): Transaction amount.
            transaction_type (TransactionType): Type of transaction.
            account_id (int): Account ID.
            category_id (int): Category ID.
            description (str, optional): Description. Defaults to "".
            date (Optional[datetime], optional): Transaction date. Defaults to None.

        Returns:
            Transaction: The created transaction.
        """
        if date is None:
            date = datetime.now()

        amount_decimal = Decimal(str(amount))
        transaction = Transaction(
            amount=amount_decimal,
            type=transaction_type,
            from_account_id=account_id,
            category_id=category_id,
            description=description,
            date=date,
        )

        # Update account balance
        account = self.get_account(account_id)
        if account:
            if transaction_type == TransactionType.INCOME:
                account.balance += amount_decimal
            else:
                account.balance -= amount_decimal

        self.db.add(transaction)
        self.db.commit()
        return transaction

    def get_daily_balances(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[datetime, Decimal]:
        """Get daily balance totals between two dates.

        Args:
            start_date (datetime): Start date.
            end_date (datetime): End date.

        Returns:
            Dict[datetime, Decimal]: Daily balances.
        """
        daily_balances = {}
        current_date = start_date

        # Get initial balance before start date
        initial_balance = sum(
            account.balance for account in self.get_accounts()
        )
        previous_transactions_sum = self.db.query(
            func.sum(
                case(
                    (
                        Transaction.type == TransactionType.INCOME,
                        Transaction.amount,
                    ),
                    (
                        Transaction.type == TransactionType.EXPENSE,
                        -Transaction.amount,
                    ),
                    else_=0,
                )
            )
        ).filter(Transaction.date > end_date).scalar() or Decimal("0")

        running_balance = initial_balance - previous_transactions_sum

        while current_date <= end_date:
            # Get transactions for current date
            daily_transactions = self.db.query(
                func.sum(
                    case(
                        (
                            Transaction.type == TransactionType.INCOME,
                            Transaction.amount,
                        ),
                        (
                            Transaction.type == TransactionType.EXPENSE,
                            -Transaction.amount,
                        ),
                        else_=0,
                    )
                )
            ).filter(
                and_(
                    func.date(Transaction.date) == current_date.date(),
                )
            ).scalar() or Decimal(
                "0"
            )

            running_balance += daily_transactions
            daily_balances[current_date] = running_balance
            current_date += timedelta(days=1)

        return daily_balances

    def get_monthly_comparison(
        self, year: int
    ) -> List[Tuple[str, Decimal, Decimal]]:
        """Get monthly comparison of income vs expenses.

        Args:
            year (int): Year to get data for.

        Returns:
            List[Tuple[str, Decimal, Decimal]]: Monthly income/expense pairs.
        """
        months = []
        for month in range(1, 13):
            summary = self.get_monthly_summary(year, month)
            month_name = datetime(year, month, 1).strftime("%b")
            months.append(
                (
                    month_name,
                    summary["total_income"],
                    summary["total_expenses"],
                )
            )
        return months

    def get_trends(
        self, months: int = 12
    ) -> List[Tuple[datetime, Decimal, Decimal, float]]:
        """Get trend data for the last N months.

        Args:
            months (int, optional): Number of months. Defaults to 12.

        Returns:
            List[Tuple[datetime, Decimal, Decimal, float]]: Monthly trend data.
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)  # Approximate

        trend_data = []
        current_date = start_date

        while current_date <= end_date:
            year = current_date.year
            month = current_date.month
            summary = self.get_monthly_summary(year, month)

            # Calculate savings rate
            savings_rate = 0.0
            if summary["total_income"] > 0:
                savings_rate = float(
                    summary["net_savings"] / summary["total_income"] * 100
                )

            trend_data.append(
                (
                    current_date,
                    summary["total_income"],
                    summary["total_expenses"],
                    savings_rate,
                )
            )

            # Move to next month
            if month == 12:
                current_date = datetime(year + 1, 1, 1)
            else:
                current_date = datetime(year, month + 1, 1)

        return trend_data

    def get_monthly_summary(
        self, year: int, month: int
    ) -> Dict[str, Union[Decimal, int, Dict[str, Decimal]]]:
        """Get summary of transactions for a specific month.

        Args:
            year (int): Year to get data for.
            month (int): Month to get data for.

        Returns:
            Dict[str, Union[Decimal, int, Dict[str, Decimal]]]: Monthly summary.
        """
        # Query for income
        total_income = self.db.query(func.sum(Transaction.amount)).filter(
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month,
            Transaction.type == TransactionType.INCOME,
        ).scalar() or Decimal("0")

        # Query for expenses
        total_expenses = self.db.query(func.sum(Transaction.amount)).filter(
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month,
            Transaction.type == TransactionType.EXPENSE,
        ).scalar() or Decimal("0")

        # Calculate net income (income - expenses)
        net_income = total_income - total_expenses

        # For this implementation, net savings is the same as net income
        net_savings = net_income

        # Get expenses by category
        expenses_by_category = (
            self.db.query(
                Category.name, func.sum(Transaction.amount).label("total")
            )
            .join(Transaction, Transaction.category_id == Category.id)
            .filter(
                extract("year", Transaction.date) == year,
                extract("month", Transaction.date) == month,
                Transaction.type == TransactionType.EXPENSE,
            )
            .group_by(Category.name)
            .all()
        )

        expense_by_category = {}
        for category_name, total in expenses_by_category:
            expense_by_category[category_name] = total

        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_income": net_income,
            "net_savings": net_savings,
            "year": year,
            "month": month,
            "expense_by_category": expense_by_category,
        }
