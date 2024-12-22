from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    ForeignKey,
    Boolean,
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import relationship
import enum

from .base import Base


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class AccountType(str, enum.Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT_CARD = "credit_card"
    CASH = "cash"
    INVESTMENT = "investment"


class Category(Base):
    """Model for transaction categories."""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # income/expense
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    color_code = Column(String(7), nullable=True)  # Hex color code
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    transactions = relationship("Transaction", back_populates="category")


class Account(Base):
    """Model for financial accounts."""

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(
        SQLAlchemyEnum(AccountType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
    )
    balance = Column(Numeric(precision=10, scale=2), nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="USD")
    is_active = Column(Boolean, default=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    transactions_from = relationship(
        "Transaction",
        foreign_keys="Transaction.from_account_id",
        back_populates="from_account",
    )
    transactions_to = relationship(
        "Transaction",
        foreign_keys="Transaction.to_account_id",
        back_populates="to_account",
    )


class Transaction(Base):
    """Model for financial transactions."""

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    type = Column(
        SQLAlchemyEnum(
            TransactionType, values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False,
    )
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    description = Column(String(255), nullable=True)

    # Foreign Keys
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    to_account_id = Column(
        Integer, ForeignKey("accounts.id"), nullable=True
    )  # For transfers

    # Tags stored as comma-separated string
    tags = Column(String(255), nullable=True)

    # Receipt image path
    receipt_path = Column(String(255), nullable=True)

    # Recurring transaction fields
    is_recurring = Column(Boolean, default=False)
    recurring_interval = Column(
        String(50), nullable=True
    )  # daily, weekly, monthly, etc.
    recurring_end_date = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = relationship("Category", back_populates="transactions")
    from_account = relationship(
        "Account", foreign_keys=[from_account_id], back_populates="transactions_from"
    )
    to_account = relationship(
        "Account", foreign_keys=[to_account_id], back_populates="transactions_to"
    )


class Budget(Base):
    """Model for budget settings."""

    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = relationship("Category")
