import pytest
from decimal import Decimal
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.base import Base
from src.models.models import Account, Category, TransactionType, AccountType
from src.core.finance_manager import FinanceManager

# Test database configuration
TEST_DATABASE_URL = "sqlite:///test_finance.db"


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def finance_manager(db_session):
    """Create a FinanceManager instance with test database session."""
    return FinanceManager(db_session)


@pytest.fixture
def sample_category(db_session):
    """Create a sample expense category."""
    category = Category(name="Test Category", type="expense")
    db_session.add(category)
    db_session.commit()
    return category


@pytest.fixture
def sample_account(db_session):
    """Create a sample checking account."""
    account = Account(
        name="Test Account",
        type=AccountType.CHECKING,
        balance=Decimal("1000.00"),
        currency="USD",
    )
    db_session.add(account)
    db_session.commit()
    return account


def test_create_account(finance_manager):
    """Test creating a new account."""
    account = finance_manager.create_account(
        name="Test Account",
        account_type=AccountType.CHECKING,
        initial_balance=Decimal("1000.00"),
        currency="USD",
        description="Test account description",
    )

    assert account.id is not None
    assert account.name == "Test Account"
    assert account.type == AccountType.CHECKING
    assert account.balance == Decimal("1000.00")
    assert account.currency == "USD"
    assert account.description == "Test account description"


def test_create_transaction(finance_manager, sample_account, sample_category):
    """Test creating a new transaction."""
    initial_balance = sample_account.balance
    transaction_amount = Decimal("50.00")

    transaction = finance_manager.create_transaction(
        type=TransactionType.EXPENSE,
        amount=transaction_amount,
        from_account_id=sample_account.id,
        category_id=sample_category.id,
        description="Test transaction",
    )

    assert transaction.id is not None
    assert transaction.amount == transaction_amount
    assert transaction.type == TransactionType.EXPENSE
    assert transaction.from_account_id == sample_account.id
    assert transaction.category_id == sample_category.id
    assert transaction.description == "Test transaction"

    # Check that account balance was updated
    assert sample_account.balance == initial_balance - transaction_amount


def test_get_monthly_summary(finance_manager, sample_account, sample_category):
    """Test getting monthly financial summary."""
    # Create test transactions
    finance_manager.create_transaction(
        type=TransactionType.INCOME,
        amount=Decimal("1000.00"),
        from_account_id=sample_account.id,
        category_id=sample_category.id,
        date=datetime(2023, 10, 1),
    )

    finance_manager.create_transaction(
        type=TransactionType.EXPENSE,
        amount=Decimal("500.00"),
        from_account_id=sample_account.id,
        category_id=sample_category.id,
        date=datetime(2023, 10, 15),
    )

    summary = finance_manager.get_monthly_summary(2023, 10)

    assert summary["total_income"] == Decimal("1000.00")
    assert summary["total_expenses"] == Decimal("500.00")
    assert summary["net_savings"] == Decimal("500.00")
    assert sample_category.name in summary["expense_by_category"]
    assert summary["expense_by_category"][sample_category.name] == Decimal("500.00")


def test_search_transactions(finance_manager, sample_account, sample_category):
    """Test searching transactions with various filters."""
    # Create test transactions
    transaction1 = finance_manager.create_transaction(
        type=TransactionType.EXPENSE,
        amount=Decimal("50.00"),
        from_account_id=sample_account.id,
        category_id=sample_category.id,
        date=datetime(2023, 10, 1),
        tags="food,groceries",
    )

    transaction2 = finance_manager.create_transaction(
        type=TransactionType.EXPENSE,
        amount=Decimal("100.00"),
        from_account_id=sample_account.id,
        category_id=sample_category.id,
        date=datetime(2023, 10, 15),
        tags="entertainment",
    )

    # Test date range filter
    transactions = finance_manager.search_transactions(
        start_date=datetime(2023, 10, 1), end_date=datetime(2023, 10, 31)
    )
    assert len(transactions) == 2

    # Test amount filter
    transactions = finance_manager.search_transactions(min_amount=Decimal("75.00"))
    assert len(transactions) == 1
    assert transactions[0].amount == Decimal("100.00")

    # Test category filter
    transactions = finance_manager.search_transactions(category_id=sample_category.id)
    assert len(transactions) == 2

    # Test account filter
    transactions = finance_manager.search_transactions(account_id=sample_account.id)
    assert len(transactions) == 2

    # Test transaction type filter
    transactions = finance_manager.search_transactions(
        transaction_type=TransactionType.EXPENSE
    )
    assert len(transactions) == 2


def test_get_account_balance(finance_manager, sample_account):
    """Test getting account balance."""
    balance = finance_manager.get_account_balance(sample_account.id)
    assert balance == sample_account.balance


def test_transfer_between_accounts(finance_manager, sample_account):
    """Test transferring money between accounts."""
    # Create second account
    second_account = finance_manager.create_account(
        name="Second Account",
        account_type=AccountType.SAVINGS,
        initial_balance=Decimal("500.00"),
    )

    initial_balance_1 = sample_account.balance
    initial_balance_2 = second_account.balance
    transfer_amount = Decimal("200.00")

    # Create transfer transaction
    finance_manager.create_transaction(
        type=TransactionType.TRANSFER,
        amount=transfer_amount,
        from_account_id=sample_account.id,
        to_account_id=second_account.id,
        category_id=1,  # Assuming a transfer category exists
    )

    # Check balances were updated correctly
    assert sample_account.balance == initial_balance_1 - transfer_amount
    assert second_account.balance == initial_balance_2 + transfer_amount
