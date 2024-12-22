"""Database utility functions for the Finance Tracker application."""

import os
from pathlib import Path
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from ..models.base import Base
from ..models.models import Category
from .logger import FinanceLogger

# Initialize logger
logger = FinanceLogger(name="finance_tracker.db", log_file="logs/db.log")


def get_database_url() -> str:
    """Get the database URL from environment or use default SQLite database."""
    return os.getenv("DATABASE_URL", "sqlite:///data/finance_tracker.db")


def create_database_engine(database_url: Optional[str] = None):
    """Create and return a database engine."""
    if database_url is None:
        database_url = get_database_url()

    # Ensure the data directory exists
    db_path = Path("data")
    db_path.mkdir(exist_ok=True)

    return create_engine(database_url, echo=False)  # Disable SQL echo


def get_db_session() -> Session:
    """Create and return a new database session."""
    engine = create_database_engine()
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def init_database():
    """Initialize the database with tables and default data."""
    engine = create_database_engine()

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create a session
    session = get_db_session()

    try:
        # Only add default categories if they don't exist
        if session.query(Category).count() == 0:
            # Default income categories
            income_categories = [
                ("Salary", "income"),
                ("Investments", "income"),
                ("Freelance", "income"),
                ("Other Income", "income"),
            ]

            # Default expense categories
            expense_categories = [
                ("Housing", "expense"),
                ("Transportation", "expense"),
                ("Food", "expense"),
                ("Utilities", "expense"),
                ("Healthcare", "expense"),
                ("Entertainment", "expense"),
                ("Shopping", "expense"),
                ("Education", "expense"),
                ("Savings", "expense"),
                ("Other Expenses", "expense"),
            ]

            # Housing subcategories
            housing_subcategories = [
                ("Rent", "expense"),
                ("Mortgage", "expense"),
                ("Maintenance", "expense"),
                ("Insurance", "expense"),
            ]

            # Transportation subcategories
            transportation_subcategories = [
                ("Public Transit", "expense"),
                ("Fuel", "expense"),
                ("Car Maintenance", "expense"),
                ("Parking", "expense"),
            ]

            # Food subcategories
            food_subcategories = [
                ("Groceries", "expense"),
                ("Restaurants", "expense"),
                ("Take-out", "expense"),
            ]

            # Create main categories and store their IDs
            category_map = {}

            # Add income categories
            for name, type_ in income_categories:
                category = Category(name=name, type=type_)
                session.add(category)
                session.flush()  # Flush to get the ID
                category_map[name] = category.id

            # Add expense categories
            for name, type_ in expense_categories:
                category = Category(name=name, type=type_)
                session.add(category)
                session.flush()  # Flush to get the ID
                category_map[name] = category.id

            # Add subcategories
            for name, type_ in housing_subcategories:
                session.add(
                    Category(name=name, type=type_, parent_id=category_map["Housing"])
                )

            for name, type_ in transportation_subcategories:
                session.add(
                    Category(
                        name=name, type=type_, parent_id=category_map["Transportation"]
                    )
                )

            for name, type_ in food_subcategories:
                session.add(
                    Category(name=name, type=type_, parent_id=category_map["Food"])
                )

            session.commit()
            print("Default categories created successfully.")
            logger.info("Default categories created successfully")
        else:
            print("Categories already exist, skipping initialization.")
            logger.info("Categories already exist, skipping initialization")

    except Exception as e:
        error_msg = f"Error initializing database: {e}"
        print(error_msg)
        logger.error(error_msg)
        session.rollback()
        raise
    finally:
        session.close()


def reset_database():
    """Reset the database by dropping all tables and reinitializing."""
    engine = create_database_engine()

    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    logger.info("All tables dropped")

    # Reinitialize the database
    init_database()
    logger.info("Database reinitialized")

    print("Database reset successfully.")
