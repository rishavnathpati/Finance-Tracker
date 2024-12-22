# Quick Start Guide - Finance Tracker

This guide will help you get started with Finance Tracker in just 5 minutes.

## Step 1: Installation

### Windows Users
1. Download Python from https://www.python.org/downloads/
2. Run the installer
   - ✅ CHECK "Add Python to PATH"
   - Click "Install Now"

### Mac Users
1. Open Terminal (Press Command + Space, type "Terminal", press Enter)
2. Install Python:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
```

## Step 2: Test Installation

1. Open Terminal (Mac) or Command Prompt (Windows)
2. Run:
```bash
python test_installation.py
```

You should see a series of successful test messages.

## Step 3: Quick Examples

### Add Your First Account
```bash
finance-tracker account add "My Checking" checking --balance 1000.00
```

This creates a checking account with $1,000 balance.

### Record Your First Expense
```bash
finance-tracker transaction add expense 50.00 1 5 --description "Grocery shopping"
```

This records a $50 grocery expense from your checking account.

### View Your Transactions
```bash
finance-tracker transaction list
```

### Check Monthly Summary
```bash
finance-tracker summary monthly 2024 3
```

## Common Commands Reference Card

### Account Management
```bash
# Add account
finance-tracker account add "Account Name" account_type --balance amount

# List accounts
finance-tracker account list
```

### Transaction Management
```bash
# Add expense
finance-tracker transaction add expense amount account_id category_id --description "description"

# Add income
finance-tracker transaction add income amount account_id category_id --description "description"

# List transactions
finance-tracker transaction list
```

### Reports
```bash
# Monthly summary
finance-tracker summary monthly YEAR MONTH
```

## Quick Category Reference

### Income Categories (ID: Name)
- 1: Salary
- 2: Investments
- 3: Freelance
- 4: Other Income

### Expense Categories (ID: Name)
- 5: Food/Groceries
- 6: Entertainment
- 7: Transportation
- 8: Housing
- 9: Utilities
- 10: Healthcare

## 5-Minute Getting Started Example

Copy and paste these commands to try out the basic features:

```bash
# 1. Add accounts
finance-tracker account add "Checking" checking --balance 1000.00
finance-tracker account add "Savings" savings --balance 5000.00

# 2. Record income
finance-tracker transaction add income 2000.00 1 1 --description "Monthly salary"

# 3. Record some expenses
finance-tracker transaction add expense 50.00 1 5 --description "Groceries"
finance-tracker transaction add expense 30.00 1 6 --description "Movie ticket"
finance-tracker transaction add expense 25.00 1 7 --description "Gas"

# 4. View your transactions
finance-tracker transaction list

# 5. Check your monthly summary
finance-tracker summary monthly 2024 3
```

## Need Help?

1. Check the detailed [User Manual](USER_MANUAL.md)
2. Run the test script:
```bash
python test_installation.py
```
3. Enable debug mode:
```bash
finance-tracker --debug
```

## Daily Usage Tips

1. **Record transactions daily** - Don't wait to record expenses
2. **Use clear descriptions** - Help your future self understand the transactions
3. **Check monthly summaries** - Review your finances at least monthly
4. **Categorize correctly** - Use appropriate categories for better tracking
5. **Keep receipts** - Cross-reference with your records

Remember: The key to successful financial tracking is consistency in recording your transactions!
