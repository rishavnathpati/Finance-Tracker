"""Test script to verify Finance Tracker installation and basic functionality."""

import os
import sys
from decimal import Decimal
from datetime import datetime

def print_step(step_number, description):
    """Print a step in the test process."""
    print(f"\n{'='*80}")
    print(f"Step {step_number}: {description}")
    print(f"{'='*80}\n")

def run_command(command):
    """Run a command and print its output."""
    print(f"Running command: {command}")
    result = os.system(command)
    if result != 0:
        print(f"Command failed with exit code: {result}")
        return False
    return True

def main():
    """Run the installation test."""
    
    print("\nFinance Tracker Installation Test")
    print("================================\n")

    # Step 1: Check Python installation
    print_step(1, "Checking Python installation")
    print(f"Python version: {sys.version}")

    # Step 2: Install the package
    print_step(2, "Installing Finance Tracker")
    if not run_command("python3 -m pip install -e ."):
        print("Failed to install Finance Tracker")
        return False

    # Step 3: Initialize the application
    print_step(3, "Initializing Finance Tracker")
    if not run_command("python3 -m finance_tracker --init"):
        print("Failed to initialize Finance Tracker")
        return False

    # Step 4: Create test accounts
    print_step(4, "Creating test accounts")
    commands = [
        "python3 -m finance_tracker account add 'Test Checking' checking --balance 1000.00",
        "python3 -m finance_tracker account add 'Test Savings' savings --balance 5000.00"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            print("Failed to create test accounts")
            return False

    # Step 5: List accounts
    print_step(5, "Listing accounts")
    if not run_command("python3 -m finance_tracker account list"):
        print("Failed to list accounts")
        return False

    # Step 6: Create test transactions
    print_step(6, "Creating test transactions")
    commands = [
        "python3 -m finance_tracker transaction add income 2000.00 1 1 --description 'Test Salary'",
        "python3 -m finance_tracker transaction add expense 50.00 1 5 --description 'Test Groceries'",
        "python3 -m finance_tracker transaction add expense 30.00 1 6 --description 'Test Entertainment'"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            print("Failed to create test transactions")
            return False

    # Step 7: List transactions
    print_step(7, "Listing transactions")
    if not run_command("python3 -m finance_tracker transaction list"):
        print("Failed to list transactions")
        return False

    # Step 8: View monthly summary
    print_step(8, "Viewing monthly summary")
    current_date = datetime.now()
    if not run_command(f"python3 -m finance_tracker summary monthly {current_date.year} {current_date.month}"):
        print("Failed to view monthly summary")
        return False

    print("\nInstallation Test Complete!")
    print("All steps completed successfully.")
    print("\nYou can now start using Finance Tracker with the following command:")
    print("python3 -m finance_tracker")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        sys.exit(1)
