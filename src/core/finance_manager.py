from typing import List, Optional, Dict, Tuple
from datetime import datetime, timedelta
from sqlalchemy import desc, func, extract, and_, case, or_
from sqlalchemy.orm import joinedload
from ..models.models import Transaction, Account, Category


class FinanceManager:
    def __init__(self, db):
        self.db = db

    # Account Management Methods
    def get_accounts(self) -> List[Account]:
        """Get all accounts."""
        return self.db.query(Account).all()

    def get_account(self, account_id: int) -> Optional[Account]:
        """Get an account by its ID."""
        return self.db.get(Account, account_id)

    def add_account(
        self, name: str, account_type: str, balance: float = 0.0
    ) -> Account:
        """Add a new account."""
        account = Account(name=name, type=account_type, balance=balance)
        self.db.add(account)
        self.db.commit()
        return account

    def update_account_balance(
        self, account_id: int, new_balance: float
    ) -> Optional[Account]:
        """Update an account's balance."""
        account = self.get_account(account_id)
        if account:
            account.balance = new_balance
            self.db.commit()
        return account

    # Transaction Management Methods
    def get_transaction(self, transaction_id: int) -> Optional[Transaction]:
        """Get a transaction by its ID."""
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

    def get_transactions(self, limit: Optional[int] = None) -> List[Transaction]:
        """Get all transactions, optionally limited to a specific number."""
        query = self.db.query(Transaction).order_by(desc(Transaction.date))
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_recent_transactions(self, limit: int = 5) -> List[Transaction]:
        """Get recent transactions."""
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

    def get_categories(self) -> List[Category]:
        """Get all categories."""
        return self.db.query(Category).all()

    def search_transactions(
        self,
        start_date: datetime = None,
        end_date: datetime = None,
        transaction_type: str = None,
        account_id: int = None,
    ) -> List[Transaction]:
        """Search transactions with filters."""
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

    def create_transaction(self, **data) -> Transaction:
        """Create a new transaction."""
        transaction = Transaction(**data)
        self.db.add(transaction)
        self.db.commit()
        return transaction

    def update_transaction(self, transaction_id: int, **data) -> Optional[Transaction]:
        """Update an existing transaction."""
        transaction = self.get_transaction(transaction_id)
        if transaction:
            for key, value in data.items():
                setattr(transaction, key, value)
            self.db.commit()
        return transaction

    def delete_transaction(self, transaction_id: int) -> bool:
        """Delete a transaction."""
        transaction = self.get_transaction(transaction_id)
        if transaction:
            self.db.delete(transaction)
            self.db.commit()
            return True
        return False

    def add_transaction(
        self,
        amount: float,
        transaction_type: str,
        account_id: int,
        category_id: int,
        description: str = "",
        date: datetime = None,
    ) -> Transaction:
        """Add a new transaction."""
        if date is None:
            date = datetime.now()

        transaction = Transaction(
            amount=amount,
            type=transaction_type,
            account_id=account_id,
            category_id=category_id,
            description=description,
            date=date,
        )

        # Update account balance
        account = self.get_account(account_id)
        if account:
            if transaction_type == "income":
                account.balance += amount
            else:
                account.balance -= amount

        self.db.add(transaction)
        self.db.commit()
        return transaction

    def get_daily_balances(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[datetime, float]:
        """Get daily balance totals between two dates."""
        daily_balances = {}
        current_date = start_date

        # Get initial balance before start date
        initial_balance = sum(account.balance for account in self.get_accounts())
        previous_transactions_sum = (
            self.db.query(
                func.sum(
                    case(
                        (Transaction.type == "income", Transaction.amount),
                        (Transaction.type == "expense", -Transaction.amount),
                        else_=0,
                    )
                )
            )
            .filter(Transaction.date > end_date)
            .scalar()
            or 0
        )

        running_balance = initial_balance - previous_transactions_sum

        while current_date <= end_date:
            # Get transactions for current date
            daily_transactions = (
                self.db.query(
                    func.sum(
                        case(
                            (Transaction.type == "income", Transaction.amount),
                            (Transaction.type == "expense", -Transaction.amount),
                            else_=0,
                        )
                    )
                )
                .filter(
                    and_(
                        func.date(Transaction.date) == current_date.date(),
                    )
                )
                .scalar()
                or 0
            )

            running_balance += daily_transactions
            daily_balances[current_date] = running_balance
            current_date += timedelta(days=1)

        return daily_balances

    def get_monthly_comparison(self, year: int) -> List[Tuple[str, float, float]]:
        """Get monthly comparison of income vs expenses for a year."""
        months = []
        for month in range(1, 13):
            summary = self.get_monthly_summary(year, month)
            month_name = datetime(year, month, 1).strftime("%b")
            months.append(
                (month_name, summary["total_income"], summary["total_expenses"])
            )
        return months

    def get_trends(
        self, months: int = 12
    ) -> List[Tuple[datetime, float, float, float]]:
        """Get trend data for the last N months."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)  # Approximate

        trend_data = []
        current_date = start_date

        while current_date <= end_date:
            year = current_date.year
            month = current_date.month
            summary = self.get_monthly_summary(year, month)

            # Calculate savings rate
            savings_rate = 0
            if summary["total_income"] > 0:
                savings_rate = (summary["net_savings"] / summary["total_income"]) * 100

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

    def get_monthly_summary(self, year: int, month: int) -> Dict:
        """Get summary of transactions for a specific month."""
        # Query for income
        total_income = (
            self.db.query(func.sum(Transaction.amount))
            .filter(
                extract("year", Transaction.date) == year,
                extract("month", Transaction.date) == month,
                Transaction.type == "income",
            )
            .scalar()
            or 0.0
        )

        # Query for expenses
        total_expenses = (
            self.db.query(func.sum(Transaction.amount))
            .filter(
                extract("year", Transaction.date) == year,
                extract("month", Transaction.date) == month,
                Transaction.type == "expense",
            )
            .scalar()
            or 0.0
        )

        # Calculate net income (income - expenses)
        net_income = total_income - total_expenses

        # For this implementation, net savings is the same as net income
        # In a more complex implementation, you might want to track savings transactions separately
        net_savings = net_income

        # Get expenses by category
        expenses_by_category = (
            self.db.query(
                Transaction.category_id, func.sum(Transaction.amount).label("total")
            )
            .filter(
                extract("year", Transaction.date) == year,
                extract("month", Transaction.date) == month,
                Transaction.type == "expense",
            )
            .group_by(Transaction.category_id)
            .all()
        )

        expense_by_category = {}
        for category_id, total in expenses_by_category:
            # For now using category_id as name since we don't have category names
            expense_by_category[f"Category {category_id}"] = float(total)

        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_income": net_income,
            "net_savings": net_savings,
            "year": year,
            "month": month,
            "expense_by_category": expense_by_category,
        }
