import sys
import logging
from PyQt6.QtWidgets import QApplication

from src.gui import MainWindow
from src.models.base import SessionLocal, init_db
from src.utils.dummy_data import add_dummy_data
from src.core.finance_manager import FinanceManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the application."""
    try:
        # Initialize database
        logger.info("Initializing database...")
        init_db()

        # Create database session
        logger.info("Creating database session...")
        db = SessionLocal()

        # Create finance manager
        logger.info("Creating finance manager...")
        finance_manager = FinanceManager(db)

        # Add dummy data if no transactions exist
        transactions = finance_manager.get_recent_transactions()
        logger.info(f"Found {len(transactions)} existing transactions")
        if not transactions:
            logger.info("Adding dummy data...")
            try:
                add_dummy_data(finance_manager)
                logger.info("Dummy data added successfully")
            except Exception as e:
                logger.error(f"Error adding dummy data: {e}", exc_info=True)

        # Create and run GUI application
        logger.info("Starting GUI application...")
        app = QApplication(sys.argv)
        app.setStyle("Fusion")

        window = MainWindow(finance_manager)
        window.show()

        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
