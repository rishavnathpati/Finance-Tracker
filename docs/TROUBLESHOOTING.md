# Troubleshooting Guide - Finance Tracker

This guide helps you resolve common issues you might encounter while using Finance Tracker.

## Common Issues and Solutions

### 1. Installation Issues

#### "Command not found" Error
```
finance-tracker: command not found
```

**Solutions:**
1. Use the full Python command:
```bash
python3 -m finance_tracker
```

2. Verify Python installation:
```bash
python3 --version
```

3. Reinstall the package:
```bash
python3 -m pip install -e .
```

#### Python Not Found
```
'python' is not recognized as an internal or external command
```

**Solutions:**
1. Make sure Python is installed:
   - Windows: Download from https://www.python.org/downloads/
   - Mac: Run `brew install python`

2. Add Python to PATH (Windows):
   - Reinstall Python and check "Add Python to PATH"

### 2. Database Issues

#### Database Error on Startup
```
Error: Unable to connect to database
```

**Solutions:**
1. Reset the database:
```bash
finance-tracker --reset
```

2. Reinitialize the application:
```bash
finance-tracker --init
```

3. Check data directory permissions:
   - Ensure the `data` directory exists
   - Verify you have write permissions

#### Lost or Corrupted Data
```
Error: Database is corrupted
```

**Solutions:**
1. Check for backups in `data/backups`
2. Reset and reinitialize:
```bash
finance-tracker --reset
finance-tracker --init
```

### 3. Transaction Issues

#### Invalid Amount Format
```
Error: Invalid amount format
```

**Solutions:**
- Use decimal points: `50.00` instead of `50`
- Don't use currency symbols: `50.00` instead of `$50.00`
- Don't use commas: `1000.00` instead of `1,000.00`

Correct examples:
```bash
finance-tracker transaction add expense 50.00 1 5
finance-tracker transaction add income 1000.00 1 1
```

#### Category Not Found
```
Error: Category not found
```

**Solutions:**
1. List available categories:
```bash
finance-tracker category list
```

2. Use correct category IDs:
   - Income categories: 1-4
   - Expense categories: 5-10

### 4. Account Issues

#### Account Not Found
```
Error: Account with ID X not found
```

**Solutions:**
1. List your accounts:
```bash
finance-tracker account list
```

2. Use the correct account ID in transactions:
```bash
finance-tracker transaction add expense 50.00 1 5  # '1' is the account ID
```

#### Insufficient Funds
```
Error: Insufficient funds in account
```

**Solutions:**
1. Check account balance:
```bash
finance-tracker account list
```

2. Verify transaction amount
3. Use correct account ID

### 5. Report Issues

#### No Data in Reports
```
No transactions found for this period
```

**Solutions:**
1. Check date range:
```bash
finance-tracker transaction list --start-date 2024-01-01 --end-date 2024-12-31
```

2. Verify transactions were recorded:
```bash
finance-tracker transaction list
```

### 6. Performance Issues

#### Slow Operation
**Solutions:**
1. Check database size:
   - Look in `data/finance_tracker.db`
   - Consider archiving old data

2. Clean up old logs:
   - Check `logs` directory
   - Delete old log files

### 7. Debug Mode

If you're experiencing issues, run in debug mode:
```bash
finance-tracker --debug
```

This will:
- Show detailed error messages
- Log additional information
- Help identify the source of problems

### 8. Complete Reset

If nothing else works:

1. Backup your data:
```bash
finance-tracker export transactions data/backup_transactions.csv
finance-tracker export accounts data/backup_accounts.csv
```

2. Reset the application:
```bash
finance-tracker --reset
```

3. Initialize fresh:
```bash
finance-tracker --init
```

4. Import your data:
```bash
finance-tracker import transactions data/backup_transactions.csv
finance-tracker import accounts data/backup_accounts.csv
```

### 9. Getting Help

If you still have issues:

1. Run the test script:
```bash
python test_installation.py
```

2. Check the logs:
   - Look in the `logs` directory
   - Check `finance_tracker.log`

3. Enable debug mode:
```bash
finance-tracker --debug
```

### 10. Preventive Measures

To avoid issues:

1. Regular backups:
```bash
finance-tracker export transactions backup_$(date +%Y%m%d).csv
```

2. Regular maintenance:
   - Check logs regularly
   - Keep software updated
   - Monitor database size

3. Best practices:
   - Record transactions daily
   - Use clear descriptions
   - Double-check account and category IDs
   - Review monthly summaries
