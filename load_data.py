"""
Load Banking CSVs into a SQLite Database
------------------------------------------
Run this AFTER generate_banking_data.py has created your CSVs
and you've moved them into the 'dataset' folder.

Folder structure expected:
  banking-sql-toolkit/
    load_data.py          <- this file
    dataset/
      branches.csv
      customers.csv
      accounts.csv
      transactions.csv
      loans.csv

Run: python load_data.py
Output: banking.db (a SQLite database file) in the same folder
"""

import sqlite3
import csv
import os

DATASET_DIR = "dataset"
DB_NAME = "banking.db"

# Remove old DB if it exists, so re-running this script is always clean
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

print("Creating tables...")
cur.executescript("""
CREATE TABLE branches (
    branch_id INTEGER PRIMARY KEY,
    branch_name TEXT,
    region TEXT
);

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    full_name TEXT,
    segment TEXT,
    region TEXT,
    onboarding_date DATE,
    risk_rating TEXT
);

CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    account_type TEXT,
    branch_id INTEGER,
    open_date DATE,
    status TEXT,
    opening_balance REAL
);

CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY,
    account_id INTEGER,
    txn_date DATE,
    txn_time TEXT,
    txn_type TEXT,
    amount REAL,
    channel TEXT,
    counterparty_id INTEGER
);

CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    loan_amount REAL,
    disbursement_date DATE,
    emi_amount REAL,
    due_date DATE,
    last_payment_date DATE,
    loan_status TEXT,
    product_type TEXT
);
""")

def load_csv(table, filename, columns):
    path = os.path.join(DATASET_DIR, filename)
    if not os.path.exists(path):
        print(f"  WARNING: {path} not found — skipping {table}")
        return 0

    with open(path, newline="", encoding="cp1252") as f:
        reader = csv.DictReader(f)
        rows = []
        for r in reader:
            row = tuple(r[c] if r[c] != "" else None for c in columns)
            rows.append(row)

    placeholders = ",".join(["?"] * len(columns))
    cur.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)
    conn.commit()
    return len(rows)

print("Loading CSVs...")

counts = {}
counts["branches"] = load_csv(
    "branches", "branches.csv",
    ["branch_id", "branch_name", "region"]
)
counts["customers"] = load_csv(
    "customers", "customers.csv",
    ["customer_id", "full_name", "segment", "region", "onboarding_date", "risk_rating"]
)
counts["accounts"] = load_csv(
    "accounts", "accounts.csv",
    ["account_id", "customer_id", "account_type", "branch_id", "open_date", "status", "opening_balance"]
)
counts["transactions"] = load_csv(
    "transactions", "transactions.csv",
    ["transaction_id", "account_id", "txn_date", "txn_time", "txn_type", "amount", "channel", "counterparty_id"]
)
counts["loans"] = load_csv(
    "loans", "loans.csv",
    ["loan_id", "account_id", "loan_amount", "disbursement_date", "emi_amount", "due_date", "last_payment_date", "loan_status", "product_type"]
)

print("\nDone! Loaded into banking.db:")
for table, count in counts.items():
    print(f"  {table}: {count} rows")

conn.close()
print(f"\nDatabase file created at: {os.path.abspath(DB_NAME)}")
print("You can now run the query files (01, 02, 03, 04...) against this database.")