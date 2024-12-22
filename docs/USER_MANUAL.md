# Finance Tracker User Manual

## Table of Contents
1. [Getting Started](#getting-started)
2. [Managing Accounts](#managing-accounts)
3. [Recording Transactions](#recording-transactions)
4. [Viewing Reports](#viewing-reports)
5. [Tips and Best Practices](#tips-and-best-practices)

## Getting Started

### First Time Setup

1. Open Terminal (Mac) or Command Prompt (Windows)
2. Navigate to the Finance Tracker folder
3. Run the test installation:
```bash
python test_installation.py
```

### Daily Usage

1. Open Terminal/Command Prompt
2. Start Finance Tracker:
```bash
finance-tracker
```

## Managing Accounts

### Adding a New Account

1. Basic Format:
```bash
finance-tracker account add "Account Name" account_type --balance amount
```

2. Examples:
```bash
# Add checking account
finance-tracker account add "Main Checking" checking --balance 1000.00

# Add savings account
finance-tracker account add "Emergency Fund" savings --balance 5000.00

# Add credit card
finance-tracker account add "Credit Card" credit_card --balance 0.00
```

### Viewing Accounts

```bash
finance-tracker account list
```

This will show:
- Account ID
- Account Name
- Type
- Current Balance
- Currency

## Recording Transactions

### Recording Expenses

1. Basic Format:
```bash
finance-tracker transaction add expense amount account_id category_id --description "description"
```

2. Examples:
```bash
# Record grocery shopping
finance-tracker transaction add expense 50.00 1 5 --description "Weekly groceries"

# Record utility bill
finance-tracker transaction add expense 100.00 1 4 --description "Electricity bill"
```

### Recording Income

1. Basic Format:
```bash
finance-tracker transaction add income amount account_id category_id --description "description"
```

2. Examples:
```bash
# Record salary
finance-tracker transaction add income 2000.00 1 1 --description "Monthly salary"

# Record investment return
finance-tracker transaction add income 100.00 2 2 --description "Stock dividend"
```

### Common Category IDs

Income Categories:
- 1: Salary
- 2: Investments
- 3: Freelance
- 4: Other Income

Expense Categories:
- 5: Food/Groceries
- 6: Entertainment
- 7: Transportation
- 8: Housing
- 9: Utilities
- 10: Healthcare

### Viewing Transactions

1. View all transactions:
```bash
finance-tracker transaction list
```

2. Filter by date range:
```bash
finance-tracker transaction list --start-date 2024-01-01 --end-date 2024-03-31
```

## Viewing Reports

### Monthly Summary

1. Basic Format:
```bash
finance-tracker summary monthly YEAR MONTH
```

2. Example:
```bash
finance-tracker summary monthly 2024 3
```

This shows:
- Total Income
- Total Expenses
- Net Savings
- Breakdown by Category

## Tips and Best Practices

### 1. Regular Transaction Recording

Record transactions daily to maintain accurate records:
```bash
# Morning coffee
finance-tracker transaction add expense 3.50 1 6 --description "Coffee"

# Lunch
finance-tracker transaction add expense 12.00 1 5 --description "Lunch"
```

### 2. Monthly Review Process

1. View monthly summary:
```bash
finance-tracker summary monthly 2024 3
```

2. Check account balances:
```bash
finance-tracker account list
```

3. Review transactions:
```bash
finance-tracker transaction list --start-date 2024-03-01 --end-date 2024-03-31
```

### 3. Organizing Transactions

Use clear descriptions and categories:
```bash
# Good examples:
finance-tracker transaction add expense 50.00 1 5 --description "Grocery shopping at Walmart"
finance-tracker transaction add expense 30.00 1 6 --description "Movie ticket - Avatar"

# Not as helpful:
finance-tracker transaction add expense 50.00 1 5 --description "Shopping"
finance-tracker transaction add expense 30.00 1 6 --description "Entertainment"
```

### 4. Common Tasks Reference

#### Adding Regular Income
```bash
# Monthly salary
finance-tracker transaction add income 2000.00 1 1 --description "Monthly salary"
```

#### Recording Bills
```bash
# Rent
finance-tracker transaction add expense 1000.00 1 8 --description "Monthly rent"

# Utilities
finance-tracker transaction add expense 100.00 1 9 --description "Electricity bill"
finance-tracker transaction add expense 50.00 1 9 --description "Water bill"
```

#### Recording Daily Expenses
```bash
# Transportation
finance-tracker transaction add expense 25.00 1 7 --description "Gas"

# Food
finance-tracker transaction add expense 15.00 1 5 --description "Lunch at cafe"
```

### 5. Troubleshooting

If you encounter issues:

1. Check your command format:
```bash
# Correct format
finance-tracker transaction add expense 50.00 1 5 --description "Groceries"

# Common mistakes
finance-tracker transaction add expense 50 1 5 # Missing .00 for amount
finance-tracker transaction add expense 50.00 1 # Missing category_id
```

2. Enable debug mode:
```bash
finance-tracker --debug
```

3. Reset if needed:
```bash
finance-tracker --reset
```

Remember: Always keep your receipts and cross-reference with your bank statements regularly.
