Core API Reference
=================

This section covers the core functionality of Finance Tracker.

Finance Manager
-------------

.. automodule:: src.core.finance_manager
   :members:
   :undoc-members:
   :show-inheritance:

Models
------

Account Model
~~~~~~~~~~~~

.. automodule:: src.models.models
   :members: Account
   :undoc-members:
   :show-inheritance:

Transaction Model
~~~~~~~~~~~~~~~

.. automodule:: src.models.models
   :members: Transaction
   :undoc-members:
   :show-inheritance:

Category Model
~~~~~~~~~~~~

.. automodule:: src.models.models
   :members: Category
   :undoc-members:
   :show-inheritance:

Enums
-----

.. automodule:: src.models.models
   :members: TransactionType, AccountType
   :undoc-members:
   :show-inheritance:

Database Base
-----------

.. automodule:: src.models.base
   :members:
   :undoc-members:
   :show-inheritance:

Example Usage
-----------

Finance Manager
~~~~~~~~~~~~~

.. code-block:: python

    from src.core.finance_manager import FinanceManager
    from src.models.base import SessionLocal

    # Create database session
    db = SessionLocal()
    
    # Initialize finance manager
    manager = FinanceManager(db)
    
    # Add an account
    account = manager.add_account(
        name="Checking Account",
        account_type="checking",
        balance=1000.00
    )
    
    # Add a transaction
    transaction = manager.add_transaction(
        amount=50.00,
        transaction_type="expense",
        account_id=account.id,
        category_id=1,
        description="Groceries"
    )
    
    # Get monthly summary
    summary = manager.get_monthly_summary(2024, 1)

Models
~~~~~

.. code-block:: python

    from src.models.models import Account, Transaction, Category
    from src.models.base import SessionLocal
    
    # Create database session
    db = SessionLocal()
    
    # Create an account
    account = Account(
        name="Savings",
        type="savings",
        balance=5000.00,
        currency="USD"
    )
    db.add(account)
    
    # Create a category
    category = Category(
        name="Food",
        type="expense"
    )
    db.add(category)
    
    # Create a transaction
    transaction = Transaction(
        amount=25.50,
        type="expense",
        account_id=account.id,
        category_id=category.id,
        description="Lunch"
    )
    db.add(transaction)
    
    # Commit changes
    db.commit()

Error Handling
------------

The core modules use SQLAlchemy's session management for database operations. Transactions are automatically rolled back on error:

.. code-block:: python

    try:
        # Perform database operations
        manager.add_transaction(...)
        manager.update_account_balance(...)
    except Exception as e:
        # Transaction is automatically rolled back
        logger.error(f"Error: {e}")
        raise
    finally:
        # Close session
        db.close()

See Also
--------

* :doc:`/guides/installation` - Installation instructions
* :doc:`/dev/architecture` - Architecture overview
* :doc:`/api/models` - Detailed model documentation
