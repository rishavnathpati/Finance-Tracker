# Finance Tracker

A modern desktop application for personal finance management built with Python and PyQt6.

## Features

- **Dashboard**
  - Overview of financial status
  - Monthly income and expense summaries
  - Balance trend visualization
  - Expense breakdown by category
  - Recent transactions list

- **Transaction Management**
  - Add, edit, and delete transactions
  - Filter transactions by date, type, and account
  - Support for income, expenses, and transfers
  - Categorize transactions
  - Add descriptions and tags

- **Reports & Analytics**
  - Monthly comparison of income vs expenses
  - Expense breakdown by category
  - Income and expense trends
  - Savings rate tracking
  - Customizable date ranges

- **Account Management**
  - Support for multiple accounts
  - Different account types (checking, savings, credit card, etc.)
  - Real-time balance tracking
  - Transfer between accounts

## Requirements

- Python 3.9 or higher
- PyQt6
- SQLAlchemy
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/finance-tracker.git
cd finance-tracker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the application:
```bash
python -m finance_tracker --init
```

## Usage

1. Start the application:
```bash
python src/main.py
```

2. The main window will open with several tabs:
   - **Dashboard**: View financial overview and summaries
   - **Transactions**: Manage your transactions
   - **Reports**: View detailed financial reports and analytics

3. To add a transaction:
   - Click "+ Add Transaction" button
   - Fill in the transaction details
   - Click "Save"

4. To view reports:
   - Go to the Reports tab
   - Select the desired time period
   - View various charts and analytics

## Project Structure

```
finance-tracker/
├── src/
│   ├── cli/            # Command-line interface
│   ├── core/           # Core business logic
│   ├── gui/            # GUI components
│   │   ├── dialogs/    # Dialog windows
│   │   └── widgets/    # Reusable widgets
│   ├── models/         # Database models
│   └── utils/          # Utility functions
├── tests/              # Test files
├── data/               # Data storage
└── logs/               # Application logs
```

## Development

- The application uses SQLAlchemy for database management
- PyQt6 for the graphical interface
- Follows a modular architecture for easy maintenance
- Includes comprehensive logging for debugging

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
