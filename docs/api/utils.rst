Utilities Reference
==================

This section documents the utility modules that provide supporting functionality.

Configuration Management
---------------------

.. automodule:: src.utils.config_manager
   :members:
   :undoc-members:
   :show-inheritance:

Data Management
-------------

.. automodule:: src.utils.data_manager
   :members:
   :undoc-members:
   :show-inheritance:

Database Utilities
---------------

.. automodule:: src.utils.db_utils
   :members:
   :undoc-members:
   :show-inheritance:

Error Handling
------------

.. automodule:: src.utils.error_handler
   :members:
   :undoc-members:
   :show-inheritance:

Logging
------

.. automodule:: src.utils.logger
   :members:
   :undoc-members:
   :show-inheritance:

Visualization
-----------

.. automodule:: src.utils.visualization
   :members:
   :undoc-members:
   :show-inheritance:

Example Usage
-----------

Configuration Management
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from src.utils.config_manager import ConfigManager

    # Load configuration
    config = ConfigManager()
    
    # Get configuration values
    db_url = config.get("database", "url")
    log_level = config.get("logging", "level")
    
    # Update configuration
    config.set("database", "url", "sqlite:///new_db.sqlite")
    config.save()

Data Import/Export
~~~~~~~~~~~~~~~

.. code-block:: python

    from src.utils.data_manager import DataManager
    from src.models.base import SessionLocal

    # Initialize data manager
    db = SessionLocal()
    data_manager = DataManager(db)
    
    # Export data
    data_manager.export_transactions("transactions.csv")
    
    # Import data
    data_manager.import_transactions("new_transactions.csv")
    
    # Backup database
    data_manager.create_backup()

Database Operations
~~~~~~~~~~~~~~~~

.. code-block:: python

    from src.utils.db_utils import initialize_database, reset_database
    
    # Initialize new database
    initialize_database()
    
    # Reset database (warning: deletes all data)
    reset_database()
    
    # Check database health
    check_database_integrity()

Error Handling
~~~~~~~~~~~~

.. code-block:: python

    from src.utils.error_handler import handle_error, log_error
    
    try:
        # Some operation that might fail
        perform_operation()
    except Exception as e:
        # Handle and log error
        handle_error(e)
        log_error("Operation failed", e)

Logging
~~~~~~

.. code-block:: python

    from src.utils.logger import get_logger
    
    # Get module logger
    logger = get_logger(__name__)
    
    # Log messages
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")

Data Visualization
~~~~~~~~~~~~~~~

.. code-block:: python

    from src.utils.visualization import (
        create_pie_chart,
        create_line_chart,
        create_bar_chart
    )
    
    # Create charts
    pie_chart = create_pie_chart(data, title="Expenses by Category")
    line_chart = create_line_chart(x_data, y_data, title="Balance Trend")
    bar_chart = create_bar_chart(categories, values, title="Monthly Summary")

Best Practices
------------

Error Handling
~~~~~~~~~~~~

1. Always use the error handler for consistency:

.. code-block:: python

    from src.utils.error_handler import handle_error

    try:
        # Risky operation
        result = perform_operation()
    except Exception as e:
        handle_error(e)
        raise

Logging
~~~~~~

1. Use the logger instead of print statements:

.. code-block:: python

    # Bad
    print("Operation completed")

    # Good
    logger = get_logger(__name__)
    logger.info("Operation completed")

2. Include relevant context in log messages:

.. code-block:: python

    logger.error(
        "Database operation failed",
        extra={
            "operation": "insert",
            "table": "transactions",
            "error_code": e.code
        }
    )

Configuration
~~~~~~~~~~~

1. Use configuration manager for all settings:

.. code-block:: python

    # Bad
    DB_URL = "sqlite:///finance.db"

    # Good
    config = ConfigManager()
    db_url = config.get("database", "url")

2. Handle missing configuration gracefully:

.. code-block:: python

    try:
        value = config.get("section", "key")
    except KeyError:
        value = default_value

See Also
--------

* :doc:`/guides/installation` - Installation and setup
* :doc:`/dev/architecture` - System architecture
* :doc:`/api/core` - Core functionality
