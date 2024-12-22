GUI Components Reference
=====================

This section documents the graphical user interface components of Finance Tracker.

Main Window
----------

.. automodule:: src.gui.main_window
   :members:
   :undoc-members:
   :show-inheritance:

Dashboard Components
-----------------

Dashboard Widget
~~~~~~~~~~~~~~

.. automodule:: src.gui.widgets.dashboard
   :members:
   :undoc-members:
   :show-inheritance:

Summary Card
~~~~~~~~~~

.. automodule:: src.gui.widgets.summary_card
   :members:
   :undoc-members:
   :show-inheritance:

Transaction Components
-------------------

Transactions Widget
~~~~~~~~~~~~~~~~

.. automodule:: src.gui.widgets.transactions
   :members:
   :undoc-members:
   :show-inheritance:

Transaction Dialog
~~~~~~~~~~~~~~~

.. automodule:: src.gui.dialogs.transaction_dialog
   :members:
   :undoc-members:
   :show-inheritance:

Reports Components
---------------

Reports Widget
~~~~~~~~~~~

.. automodule:: src.gui.widgets.reports
   :members:
   :undoc-members:
   :show-inheritance:

Account Components
---------------

Accounts Widget
~~~~~~~~~~~~

.. automodule:: src.gui.widgets.accounts
   :members:
   :undoc-members:
   :show-inheritance:

Category Components
----------------

Categories Widget
~~~~~~~~~~~~~~

.. automodule:: src.gui.widgets.categories
   :members:
   :undoc-members:
   :show-inheritance:

Dialogs
------

Settings Dialog
~~~~~~~~~~~~

.. automodule:: src.gui.dialogs.settings_dialog
   :members:
   :undoc-members:
   :show-inheritance:

Styling
------

.. automodule:: src.gui.style
   :members:
   :undoc-members:
   :show-inheritance:

Example Usage
-----------

Creating Custom Widgets
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from PyQt6.QtWidgets import QWidget, QVBoxLayout
    from src.gui.style import CARD_STYLE
    from src.gui.widgets.summary_card import SummaryCard

    class CustomDashboardWidget(QWidget):
        def __init__(self, finance_manager):
            super().__init__()
            self.finance_manager = finance_manager
            self.init_ui()

        def init_ui(self):
            layout = QVBoxLayout(self)
            
            # Create summary cards
            self.balance_card = SummaryCard("Balance", "$0.00", "💰")
            self.income_card = SummaryCard("Income", "$0.00", "📈")
            
            # Add to layout
            layout.addWidget(self.balance_card)
            layout.addWidget(self.income_card)
            
            # Apply styling
            self.setStyleSheet(CARD_STYLE)

Adding Custom Dialogs
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton
    from src.gui.style import DIALOG_STYLE, ACTION_BUTTON_STYLE

    class CustomDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.init_ui()

        def init_ui(self):
            layout = QVBoxLayout(self)
            
            # Add widgets
            button = QPushButton("Save")
            button.setStyleSheet(ACTION_BUTTON_STYLE)
            layout.addWidget(button)
            
            # Apply styling
            self.setStyleSheet(DIALOG_STYLE)

Using Charts
~~~~~~~~~~

.. code-block:: python

    from PyQt6.QtCharts import QChart, QPieSeries
    from src.gui.widgets.dashboard import DashboardWidget

    class CustomChartWidget(DashboardWidget):
        def create_chart(self):
            # Create pie chart
            series = QPieSeries()
            series.append("Category 1", 30.0)
            series.append("Category 2", 70.0)
            
            chart = QChart()
            chart.addSeries(series)
            chart.setTitle("Custom Chart")
            
            return chart

Widget Styling
~~~~~~~~~~~~

.. code-block:: python

    # Apply card style
    widget.setStyleSheet(CARD_STYLE)

    # Apply button styles
    save_button.setStyleSheet(ACTION_BUTTON_STYLE)
    delete_button.setStyleSheet(DELETE_BUTTON_STYLE)

    # Apply input styles
    input_field.setStyleSheet(INPUT_STYLE)

See Also
--------

* :doc:`/guides/user-manual` - User interface guide
* :doc:`/dev/architecture` - GUI architecture
* :doc:`/api/core` - Core functionality
