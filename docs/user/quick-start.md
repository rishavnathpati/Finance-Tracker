# Quick Start Guide

This guide will help you get started with Finance Tracker quickly.

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

### Installation Steps

1. Get the application:
```bash
# Option 1: Clone with git
git clone https://github.com/yourusername/finance-tracker.git
cd finance-tracker

# Option 2: Download and extract zip file
# Download from GitHub and extract
```

2. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

## First Launch

1. Start the application:
```bash
python src/main.py
```

2. The main window will open with three tabs:
   - Dashboard: Overview of your finances
   - Transactions: Manage your transactions
   - Reports: View financial reports and analytics

## Basic Usage

### Setting Up Accounts

1. Click "+ Add Account" in the Accounts section
2. Fill in the account details:
   - Name (e.g., "Main Checking")
   - Type (Checking, Savings, Credit Card, etc.)
   - Initial Balance
   - Currency (default: USD)

### Recording Transactions

1. Click "+ Add Transaction" in the Transactions tab
2. Enter transaction details:
   - Type (Income/Expense/Transfer)
   - Amount
   - Date
   - Category
   - Description (optional)
   - Tags (optional)

### Viewing Reports

1. Go to the Reports tab
2. Select the desired time period
3. View various reports:
   - Income vs Expenses
   - Expense Breakdown
   - Savings Rate
   - Balance Trend

## Common Tasks

### Managing Categories

1. Go to Settings → Categories
2. Add, edit, or delete categories
3. Organize categories with parent/child relationships

### Importing Data

1. Go to File → Import
2. Select file format (CSV, QIF, OFX)
3. Map columns to transaction fields
4. Review and confirm import

### Exporting Data

1. Go to File → Export
2. Choose export format
3. Select date range
4. Choose destination file

## Tips & Tricks

1. **Quick Entry**:
   - Use keyboard shortcuts for faster data entry
   - Tab between fields
   - Enter to save

2. **Filtering**:
   - Use search box to filter transactions
   - Filter by date range, category, or account
   - Save common filters

3. **Dashboard Customization**:
   - Rearrange widgets
   - Show/hide sections
   - Customize chart types

4. **Regular Backups**:
   - Enable automatic backups
   - Export data regularly
   - Keep backup copies secure

## Troubleshooting

### Common Issues

1. **Application won't start**:
   - Verify Python installation
   - Check dependencies
   - Look for error messages in logs/

2. **Database errors**:
   - Reset database: `python -m src.utils.db_utils --reset`
   - Check file permissions
   - Verify database file exists

3. **Import failures**:
   - Check file format
   - Verify column mappings
   - Look for error messages

### Getting Help

1. Check documentation in docs/
2. Search GitHub issues
3. Create a new issue with:
   - Error message
   - Steps to reproduce
   - System information

## Next Steps

1. Read the full [User Manual](manual.md)
2. Set up [Categories](manual.md#categories)
3. Configure [Automatic Backups](manual.md#backups)
4. Explore [Advanced Features](manual.md#advanced-features)
