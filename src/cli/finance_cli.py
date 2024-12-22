import argparse
from datetime import datetime
from decimal import Decimal
import sys

from ..core.finance_manager import FinanceManager
from ..models.models import TransactionType, AccountType, Account, Category
from ..models.base import SessionLocal
from ..utils.logger import FinanceLogger
from src.models.models import TransactionType, AccountType, Account, Category
from src.models.base import SessionLocal
from src.utils.logger import FinanceLogger

# Initialize logger
logger = FinanceLogger(name="finance_cli", log_file="logs/cli.log")


class FinanceCLI:
    """Command Line Interface for Finance Tracker"""

    def __init__(self):
        self.db = SessionLocal()
        self.finance_manager = FinanceManager(self.db)

    def setup_parser(self) -> argparse.ArgumentParser:
        """Set up command line argument parser."""
        parser = argparse.ArgumentParser(description="Personal Finance Tracker CLI")
        parser.add_argument(
            "--init", action="store_true", help="Initialize the database"
        )
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Account commands
        account_parser = subparsers.add_parser("account", help="Account management")
        account_subparsers = account_parser.add_subparsers(dest="account_command")

        # Add account
        add_account = account_subparsers.add_parser("add", help="Add new account")
        add_account.add_argument("name", help="Account name")
        add_account.add_argument(
            "type", choices=[t.value for t in AccountType], help="Account type"
        )
        add_account.add_argument(
            "--balance", type=float, default=0.0, help="Initial balance"
        )
        add_account.add_argument("--currency", default="USD", help="Account currency")
        add_account.add_argument("--description", help="Account description")

        # List accounts
        account_subparsers.add_parser("list", help="List all accounts")

        # Category commands
        category_parser = subparsers.add_parser("category", help="Category management")
        category_subparsers = category_parser.add_subparsers(dest="category_command")

        # List categories
        category_subparsers.add_parser("list", help="List all categories")

        # Transaction commands
        transaction_parser = subparsers.add_parser(
            "transaction", help="Transaction management"
        )
        transaction_subparsers = transaction_parser.add_subparsers(
            dest="transaction_command"
        )

        # Add transaction
        add_transaction = transaction_subparsers.add_parser(
            "add", help="Add new transaction"
        )
        add_transaction.add_argument(
            "type", choices=[t.value for t in TransactionType], help="Transaction type"
        )
        add_transaction.add_argument("amount", type=float, help="Transaction amount")
        add_transaction.add_argument("from_account", type=int, help="Source account ID")
        add_transaction.add_argument("category", type=int, help="Category ID")
        add_transaction.add_argument(
            "--to_account", type=int, help="Destination account ID (for transfers)"
        )
        add_transaction.add_argument("--description", help="Transaction description")
        add_transaction.add_argument("--date", help="Transaction date (YYYY-MM-DD)")
        add_transaction.add_argument("--tags", help="Comma-separated tags")

        # List transactions
        list_transactions = transaction_subparsers.add_parser(
            "list", help="List transactions"
        )
        list_transactions.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
        list_transactions.add_argument("--end-date", help="End date (YYYY-MM-DD)")
        list_transactions.add_argument(
            "--category", type=int, help="Filter by category ID"
        )
        list_transactions.add_argument(
            "--account", type=int, help="Filter by account ID"
        )
        list_transactions.add_argument(
            "--type",
            choices=[t.value for t in TransactionType],
            help="Filter by transaction type",
        )

        # Summary commands
        summary_parser = subparsers.add_parser("summary", help="Financial summaries")
        summary_subparsers = summary_parser.add_subparsers(dest="summary_command")

        # Monthly summary
        monthly_summary = summary_subparsers.add_parser(
            "monthly", help="Monthly financial summary"
        )
        monthly_summary.add_argument("year", type=int, help="Year")
        monthly_summary.add_argument("month", type=int, help="Month")

        return parser

    def handle_account_command(self, args):
        """Handle account-related commands."""
        if args.account_command == "add":
            account = self.finance_manager.create_account(
                name=args.name,
                account_type=AccountType(args.type),
                initial_balance=Decimal(str(args.balance)),
                currency=args.currency,
                description=args.description,
            )
            print(f"Account created successfully. ID: {account.id}")
            logger.info(f"Created account '{args.name}' with ID {account.id}")

        elif args.account_command == "list":
            accounts = self.db.query(Account).all()
            if not accounts:
                print("\nNo accounts found.")
                return

            print("\nAccounts:")
            print("ID | Name | Type | Balance | Currency")
            print("-" * 50)
            for account in accounts:
                print(
                    f"{account.id} | {account.name} | {account.type.value} | {account.balance:.2f} | {account.currency}"
                )

    def handle_category_command(self, args):
        """Handle category-related commands."""
        if args.category_command == "list":
            categories = self.db.query(Category).all()
            if not categories:
                print("\nNo categories found.")
                return

            print("\nCategories:")
            print("ID | Name | Type | Parent")
            print("-" * 50)
            for category in categories:
                parent_name = category.parent.name if category.parent else "None"
                print(
                    f"{category.id} | {category.name} | {category.type} | {parent_name}"
                )

    def handle_transaction_command(self, args):
        """Handle transaction-related commands."""
        if args.transaction_command == "add":
            try:
                date = datetime.strptime(args.date, "%Y-%m-%d") if args.date else None
                tags = args.tags.split(",") if args.tags else None

                # Get account currency
                account = (
                    self.db.query(Account)
                    .filter(Account.id == args.from_account)
                    .first()
                )
                if not account:
                    raise ValueError(f"Account with ID {args.from_account} not found")

                transaction = self.finance_manager.create_transaction(
                    type=TransactionType(args.type),
                    amount=Decimal(str(args.amount)),
                    from_account_id=args.from_account,
                    category_id=args.category,
                    to_account_id=args.to_account,
                    description=args.description,
                    date=date,
                    tags=",".join(tags) if tags else None,
                )
                print(f"Transaction created successfully. ID: {transaction.id}")
                logger.info(
                    f"Created {args.type} transaction for {args.amount} {account.currency}. ID: {transaction.id}"
                )

            except Exception as e:
                print(f"Error: {str(e)}")
                logger.error(f"Error creating transaction: {str(e)}")

        elif args.transaction_command == "list":
            start_date = (
                datetime.strptime(args.start_date, "%Y-%m-%d")
                if args.start_date
                else None
            )
            end_date = (
                datetime.strptime(args.end_date, "%Y-%m-%d") if args.end_date else None
            )
            transaction_type = TransactionType(args.type) if args.type else None

            transactions = self.finance_manager.search_transactions(
                start_date=start_date,
                end_date=end_date,
                category_id=args.category,
                account_id=args.account,
                transaction_type=transaction_type,
            )

            if not transactions:
                print("\nNo transactions found.")
                return

            print("\nTransactions:")
            print(
                "ID | Date | Type | Amount | From Account | To Account | Category | Description"
            )
            print("-" * 80)
            for t in transactions:
                print(
                    f"{t.id} | {t.date.date()} | {t.type.value} | {t.amount:.2f} | "
                    f"{t.from_account.name} | {t.to_account.name if t.to_account else 'N/A'} | "
                    f"{t.category.name} | {t.description or 'N/A'}"
                )

    def handle_summary_command(self, args):
        """Handle summary-related commands."""
        if args.summary_command == "monthly":
            summary = self.finance_manager.get_monthly_summary(args.year, args.month)

            print(f"\nMonthly Summary for {args.year}-{args.month:02d}")
            print("-" * 40)
            print(f"Total Income: ${summary['total_income']:,.2f}")
            print(f"Total Expenses: ${summary['total_expenses']:,.2f}")
            print(f"Net Savings: ${summary['net_savings']:,.2f}")

            if summary["expense_by_category"]:
                print("\nExpenses by Category:")
                print("-" * 40)
                for category, amount in summary["expense_by_category"].items():
                    print(f"{category}: ${amount:,.2f}")
            else:
                print("\nNo expenses recorded for this period.")

    def run(self):
        """Run the CLI application."""
        parser = self.setup_parser()
        args = parser.parse_args()

        try:
            if args.command == "account":
                self.handle_account_command(args)
            elif args.command == "category":
                self.handle_category_command(args)
            elif args.command == "transaction":
                self.handle_transaction_command(args)
            elif args.command == "summary":
                self.handle_summary_command(args)
            else:
                parser.print_help()
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            logger.error(f"Error in CLI: {str(e)}")
        finally:
            self.db.close()


def main():
    """Entry point for the CLI application."""
    cli = FinanceCLI()
    cli.run()


if __name__ == "__main__":
    main()
