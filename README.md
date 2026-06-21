# Banking & Fintech SQL Toolkit (Sample)

A small collection of SQL queries modeled on real-world problems that
banking and fintech risk, operations, and compliance teams solve every
day — built on a fully synthetic dataset so anyone can practice safely.

I work in banking software, and over time I noticed that most SQL
tutorials use generic e-commerce datasets (customers/orders/products).
This project is my attempt to give SQL learners something closer to
what banking/fintech data analysts actually work with.

## What's in This Repo (Free Sample)

This is a sample of a larger toolkit. Included here:

- **`generate_banking_data.py`** — generates a fully synthetic dataset:
  ~2,000 customers, ~2,500 accounts, ~80,000 transactions, 270 loans,
  across 15 branches. No real data, no PII, safe to use anywhere.
- **`00_schema.sql`** — table definitions for the dataset
- **3 sample queries:**
  - `01_duplicate_transactions.sql` — detecting operational duplicate transactions
  - `03_daily_reconciliation.sql` — daily account balance reconciliation using window functions
  - `04_structuring_detection.sql` — flagging AML "structuring" fraud patterns

## How to Use This

### 1. Generate the dataset
```bash
python generate_banking_data.py
```
This creates an `output/` folder with 5 CSV files: `branches.csv`,
`customers.csv`, `accounts.csv`, `transactions.csv`, `loans.csv`.

### 2. Load it into a database
Use `00_schema.sql` to create the tables in Postgres, MySQL, or SQLite,
then import the CSVs into the matching tables.

**Quickest option (SQLite, no extra installs):**
```python
import sqlite3, csv

conn = sqlite3.connect("banking.db")
cur = conn.cursor()
# Run the contents of 00_schema.sql here, then load each CSV
# (see generate_banking_data.py for the table structure)
```

### 3. Run the queries
Each `.sql` file includes:
- The query itself
- A comment block explaining the business problem it solves
- Notes on why this matters in a real banking/fintech context

Open any `.sql` file, copy the query, and run it against your loaded
database.

## The Full Toolkit

This repo includes 3 of 8 total queries. The complete toolkit includes:

- Loan delinquency bucketing (DPD aging) — core risk reporting metric
- Transaction velocity monitoring — fraud/risk account flagging
- Loan default rate analysis by region/product
- Customer lifetime value calculation
- Branch performance trending with month-over-month growth

👉 **Get the full 8-query toolkit here: [your Gumroad link]**

## A Note on the Data

This dataset is entirely synthetic, generated with Python's built-in
`random` module using a fixed seed for reproducibility. It does not
represent real customers, accounts, or transactions of any kind.

## License

This sample is shared for educational/portfolio purposes. See `LICENSE`
for terms. The full toolkit (sold separately) has its own license terms
included with purchase.

## About

Built by Abhishek Bansal — I work in banking software and enjoy writing
about practical SQL patterns from the industry. Feel free to connect
me at bansal0735@gmail.com.
