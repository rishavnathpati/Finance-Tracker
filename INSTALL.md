# Installation and Usage Guide for Finance Tracker

## Step 1: Install Python
First, you need to install Python on your computer if you haven't already.

1. Go to https://www.python.org/downloads/
2. Download the latest version for your operating system (Windows/Mac/Linux)
3. Run the installer
   - On Windows: Make sure to check "Add Python to PATH" during installation
   - On Mac/Linux: Python might already be installed. Open Terminal and type `python3 --version` to check

## Step 2: Install Finance Tracker

1. Open Terminal (Mac/Linux) or Command Prompt (Windows)

2. Install the required tools:
```bash
python3 -m pip install --upgrade pip
```

3. Navigate to the Finance Tracker directory:
```bash
cd path/to/finance-tracker
```

4. Install the application:
```bash
python3 -m pip install -e .
```

## Step 3: Initialize the Application

1. Initialize the application:
```bash
python3 -m finance_tracker --init
```

## Step 4: Using the Application

Here's a step-by-step guide to test the basic features:

1. Start the application:
```bash
python3 -m finance_tracker
```

2. Add an Account:
```bash
finance-tracker account add "My Checking" checking --balance 1000.00
```

3. View your accounts:
```bash
finance-tracker account list
```

4. Add a transaction:
```bash
finance-tracker transaction add expense 50.00 1 5 --description "Grocery shopping"
```
(Where 1 is your account ID and 5 is the category ID for Food/Groceries)

5. View your transactions:
```bash
finance-tracker transaction list
```

6. View monthly summary:
```bash
finance-tracker summary monthly 2024 3
```

## Common Operations

### Managing Accounts
- Add new account:
```bash
finance-tracker account add "Account Name" account_type --balance initial_balance
```
Example: 
```bash
finance-tracker account add "Savings" savings --balance 5000.00
```

### Managing Transactions
- Add expense:
```bash
finance-tracker transaction add expense amount account_id category_id --description "description"
```
Example:
```bash
finance-tracker transaction add expense 25.50 1 5 --description "Lunch"
```

- Add income:
```bash
finance-tracker transaction add income amount account_id category_id --description "description"
```
Example:
```bash
finance-tracker transaction add income 2000.00 1 1 --description "Salary"
```

### Viewing Reports
- Monthly summary:
```bash
finance-tracker summary monthly YEAR MONTH
```
Example:
```bash
finance-tracker summary monthly 2024 3
```

## Troubleshooting

1. If you see "command not found":
   - Make sure Python is installed correctly
   - Try using `python3 -m finance_tracker` instead

2. If you see database errors:
   - Try resetting the application:
   ```bash
   python3 -m finance_tracker --reset
   ```

3. For any other issues:
   - Run in debug mode:
   ```bash
   python3 -m finance_tracker --debug
   ```

## Example Session

Here's a complete example session to test the application:

1. Initialize the application:
```bash
python3 -m finance_tracker --init
```

2. Add a checking account:
```bash
finance-tracker account add "Main Checking" checking --balance 1000.00
```

3. Add a savings account:
```bash
finance-tracker account add "Savings" savings --balance 5000.00
```

4. Add some transactions:
```bash
# Add salary income
finance-tracker transaction add income 2000.00 1 1 --description "Monthly Salary"

# Add some expenses
finance-tracker transaction add expense 50.00 1 5 --description "Groceries"
finance-tracker transaction add expense 30.00 1 6 --description "Movie Night"
finance-tracker transaction add expense 100.00 1 2 --description "Gas"
```

5. View your monthly summary:
```bash
finance-tracker summary monthly 2024 3
```

This will give you a good overview of the application's basic functionality. The application will show you your total income, expenses, and current balances.
