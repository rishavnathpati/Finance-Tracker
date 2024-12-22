"""Data import/export utilities for the Finance Tracker application."""

import csv
import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

from sqlalchemy.orm import Session
from ..models.models import Account, Category, TransactionType


class DataManager:
    """Class for handling data import and export operations."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def export_to_csv(self, data: List[Any], filename: str, data_type: str):
        """Export data to CSV file."""
        if data_type == "transactions":
            fieldnames = [
                "date",
                "type",
                "amount",
                "category",
                "from_account",
                "to_account",
                "description",
                "tags",
            ]
            rows = [
                {
                    "date": t.date.strftime("%Y-%m-%d"),
                    "type": t.type.value,
                    "amount": str(t.amount),
                    "category": t.category.name,
                    "from_account": t.from_account.name,
                    "to_account": t.to_account.name if t.to_account else "",
                    "description": t.description or "",
                    "tags": t.tags or "",
                }
                for t in data
            ]
        elif data_type == "accounts":
            fieldnames = ["name", "type", "balance", "currency", "description"]
            rows = [
                {
                    "name": a.name,
                    "type": a.type.value,
                    "balance": str(a.balance),
                    "currency": a.currency,
                    "description": a.description or "",
                }
                for a in data
            ]
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def import_from_csv(self, filename: str, data_type: str) -> List[Dict[str, Any]]:
        """Import data from CSV file."""
        if not Path(filename).exists():
            raise FileNotFoundError(f"File not found: {filename}")

        with open(filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)

        if data_type == "transactions":
            return self._process_transaction_import(data)
        elif data_type == "accounts":
            return self._process_account_import(data)
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

    def _process_transaction_import(
        self, data: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """Process imported transaction data."""
        processed_data = []

        for row in data:
            # Get or create category
            category = self._get_or_create_category(row["category"])

            # Get accounts
            from_account = self._get_account_by_name(row["from_account"])
            to_account = (
                self._get_account_by_name(row["to_account"])
                if row["to_account"]
                else None
            )

            if not from_account:
                raise ValueError(f"Account not found: {row['from_account']}")

            processed_data.append(
                {
                    "date": datetime.strptime(row["date"], "%Y-%m-%d"),
                    "type": TransactionType(row["type"]),
                    "amount": Decimal(row["amount"]),
                    "category_id": category.id,
                    "from_account_id": from_account.id,
                    "to_account_id": to_account.id if to_account else None,
                    "description": row["description"],
                    "tags": row["tags"],
                }
            )

        return processed_data

    def _process_account_import(
        self, data: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """Process imported account data."""
        return [
            {
                "name": row["name"],
                "type": row["type"],
                "balance": Decimal(row["balance"]),
                "currency": row["currency"],
                "description": row["description"],
            }
            for row in data
        ]

    def _get_or_create_category(self, category_name: str) -> Category:
        """Get existing category or create new one."""
        category = self.db_session.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(
                name=category_name, type="expense"
            )  # Default to expense
            self.db_session.add(category)
            self.db_session.commit()
        return category

    def _get_account_by_name(self, account_name: str) -> Optional[Account]:
        """Get account by name."""
        return self.db_session.query(Account).filter_by(name=account_name).first()

    def export_to_json(self, data: List[Any], filename: str, data_type: str):
        """Export data to JSON file."""
        if data_type == "transactions":
            json_data = [
                {
                    "date": t.date.strftime("%Y-%m-%d"),
                    "type": t.type.value,
                    "amount": str(t.amount),
                    "category": t.category.name,
                    "from_account": t.from_account.name,
                    "to_account": t.to_account.name if t.to_account else None,
                    "description": t.description,
                    "tags": t.tags,
                }
                for t in data
            ]
        elif data_type == "accounts":
            json_data = [
                {
                    "name": a.name,
                    "type": a.type.value,
                    "balance": str(a.balance),
                    "currency": a.currency,
                    "description": a.description,
                }
                for a in data
            ]
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

        with open(filename, "w") as jsonfile:
            json.dump(json_data, jsonfile, indent=2)

    def import_from_json(self, filename: str, data_type: str) -> List[Dict[str, Any]]:
        """Import data from JSON file."""
        if not Path(filename).exists():
            raise FileNotFoundError(f"File not found: {filename}")

        with open(filename, "r") as jsonfile:
            data = json.load(jsonfile)

        if data_type == "transactions":
            return self._process_transaction_import(data)
        elif data_type == "accounts":
            return self._process_account_import(data)
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

    def import_from_excel(self, filename: str, data_type: str) -> List[Dict[str, Any]]:
        """Import data from Excel file."""
        if not Path(filename).exists():
            raise FileNotFoundError(f"File not found: {filename}")

        df = pd.read_excel(filename)
        data = df.to_dict("records")

        if data_type == "transactions":
            return self._process_transaction_import(data)
        elif data_type == "accounts":
            return self._process_account_import(data)
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

    def export_to_excel(self, data: List[Any], filename: str, data_type: str):
        """Export data to Excel file."""
        if data_type == "transactions":
            df_data = [
                {
                    "date": t.date,
                    "type": t.type.value,
                    "amount": float(t.amount),
                    "category": t.category.name,
                    "from_account": t.from_account.name,
                    "to_account": t.to_account.name if t.to_account else None,
                    "description": t.description,
                    "tags": t.tags,
                }
                for t in data
            ]
        elif data_type == "accounts":
            df_data = [
                {
                    "name": a.name,
                    "type": a.type.value,
                    "balance": float(a.balance),
                    "currency": a.currency,
                    "description": a.description,
                }
                for a in data
            ]
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

        df = pd.DataFrame(df_data)
        df.to_excel(filename, index=False)
