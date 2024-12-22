"""Application initialization utilities."""

from pathlib import Path
import sys

from .logger import FinanceLogger
from .db_utils import init_database
from .config_manager import create_default_config

# Initialize logger
logger = FinanceLogger(
    name="finance_tracker.initializer", log_file="logs/initializer.log"
)


def create_directories():
    """Create required directories."""
    directories = ["data", "data/exports", "data/receipts", "logs"]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def create_files():
    """Create required files."""
    files = ["data/.gitkeep", "data/exports/.gitkeep", "data/receipts/.gitkeep"]

    for file in files:
        Path(file).touch(exist_ok=True)


def initialize_application():
    """Initialize the application."""
    try:
        print("Starting application initialization...")

        # Create required directories
        print("Creating required directories...")
        create_directories()

        # Create required files
        print("Creating required files...")
        create_files()

        # Initialize configuration
        print("Initializing configuration...")
        create_default_config()

        # Initialize database
        print("Initializing database...")
        init_database()
        print("Database initialized successfully")

        print("Application initialization completed successfully.")

    except Exception as e:
        logger.error(f"Error during initialization: {str(e)}")
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def reset_application():
    """Reset the application to its initial state."""
    try:
        print("Resetting application - all data will be lost!")
        response = input("Are you sure you want to reset the application? (y/N): ")

        if response.lower() != "y":
            print("Reset cancelled.")
            return

        # Initialize database (this will drop and recreate all tables)
        init_database()

        # Re-initialize the application
        initialize_application()

        print("Application reset successfully")

    except Exception as e:
        logger.error(f"Error during reset: {str(e)}")
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
