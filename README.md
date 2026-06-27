# 🏦 SecureBank — Full-Stack Banking Portal Simulation

A complete, interactive banking application built with **Python, SQLite, and
Streamlit** — simulating a real bank's customer and admin experience on top
of a fully synthetic dataset. Built as a hands-on project to demonstrate
SQL, data modeling, and full-stack development skills using only Python.

> ⚠️ **This is a portfolio/demo project.** All data is synthetic. No real
> customers, accounts, or financial information are involved anywhere in
> this project.

---

## 🎯 What This Project Demonstrates

- Relational database design (5+ interlinked tables)
- Writing and optimizing SQL queries (CTEs, window functions, statistical
  calculations, conditional aggregation)
- Building a role-based, multi-page web application entirely in Python
- Session-state management, form handling, and data validation
- Realistic application features: authentication, money transfers,
  loan workflows, search/filtering, CSV export

---

## ✨ Features

### 👤 Customer Portal
| Feature | Description |
|---|---|
| **Login** | Customer ID + password (default: date of birth in `DDMMYYYY` format, or a custom password) |
| **Overview** | Real-time account balances (computed from full transaction history, not a stale stored value) and account list |
| **Transfer Money** | Send money to any account by **account number**, with an optional description and a confirmation step before anything is finalized |
| **Transactions** | Filterable by date range, with CSV export |
| **Loans** | View existing loans, repayment status, and EMI details |
| **Apply for a Loan** | Submit a loan request (amount, type, purpose) and track its approval status |
| **Change Password** | Self-service password update |

### 🛠️ Admin Portal
| Feature | Description |
|---|---|
| **Portfolio Overview** | Customer/account breakdowns by type (Individual/Company/NGO × Savings/Current/Fixed Deposit/Recurring Deposit/Loan) |
| **Customer Search** | Filter by name, customer type, region, or risk rating; export results |
| **Loan Applications** | Review pending requests; Approve (auto-creates a real loan account) or Reject with notes |
| **Fraud Detection** | Flags AML "structuring" patterns (multiple deposits just under a reporting threshold) |
| **Risk Scoring** | Composite, multi-factor customer risk score (base rating + behavioral flags) |
| **Loan Delinquency** | DPD (Days Past Due) bucket analysis, with an **editable snapshot date** |
| **Branch Performance** | Monthly transaction volume trends per branch |
| **Anomaly Detection** | Statistical (z-score) outlier transaction detection, relative to each account's own history |
| **Add New Customer** | Create a customer + their first account directly from the admin panel |

---

## 🏗️ Tech Stack

- **Python 3.10+**
- **Streamlit** — the entire front-end (no HTML/CSS/JS framework needed)
- **SQLite** — the database engine
- **pandas** — data manipulation between SQL and the UI

---

## 📂 Project Structure

```
BANKING-SQL-TOOLKIT/
├── bank_portal.py              # Main Streamlit application (this is what you run)
├── generate_banking_data.py    # Synthetic dataset generator
├── load_data.py                # Loads generated CSVs into banking.db
├── banking.db                  # SQLite database (generated, not hand-written)
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml             # Forces a consistent light theme
├── dataset/                    # Generated CSVs (branches, customers, accounts, transactions, loans)
├── queries/                    # 11 standalone SQL queries with business-context documentation
└── docs/
    └── README.md                # This file
```

---

## 🚀 Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate the synthetic dataset
```bash
python generate_banking_data.py
```
This creates an `output/` folder with 5 CSV files. Copy them into `dataset/`.

### 3. Load the data into SQLite
```bash
python load_data.py
```
This creates `banking.db` with all tables populated.

### 4. Run the app
```bash
streamlit run bank_portal.py
```
Your browser will open automatically to `http://localhost:8501`.

---

## 🔑 Demo Credentials

**Customer login:** Use any `customer_id` from the dataset (e.g. `1`), with
the password being that customer's `date_of_birth` in `DDMMYYYY` format
(look it up directly in the `customers` table if needed).

**Admin login:**
- Username: `admin`
- Password: `admin123`

---

## 🗃️ Database Schema

6 tables: `branches`, `customers`, `accounts`, `transactions`, `loans`,
`loan_applications`. See [`ERD.md`](ERD.md) for the full entity-relationship
diagram.

Key design choices:
- **Account numbers encode metadata**: format is `{type_code}{branch:02d}{sequence:06d}`
  (e.g. `2008000001` = a Current account at branch 08)
- **Balances are computed, not stored**: `current_balance = opening_balance + all credits − all debits`,
  calculated live from the transaction ledger — this is closer to how real
  banking systems work (append-only transaction logs) than storing a
  mutable balance field
- **Money transfers are double-entry**: every transfer inserts two linked
  transaction rows (a withdrawal + a deposit), not a single magic balance update

---

## ⚠️ Known Limitations (intentional, for a demo)

- **Passwords are stored in plain text.** A real system would hash and
  salt passwords (e.g. bcrypt). This is a deliberate simplification for
  a demo project, not a production practice.
- **Data resets if you re-run `load_data.py`.** It rebuilds the entire
  database from the CSVs, which will erase anything entered through the
  live app (new customers, transfers, loan applications). Only re-run it
  when you actually want a fresh dataset.
- **Deployed (cloud) versions reset on restart.** If hosted on Streamlit
  Community Cloud, the filesystem is ephemeral — any in-session changes
  won't persist across app restarts/redeploys.
- **Single shared SQLite file, no concurrency handling.** Fine for a demo
  with one user at a time; a production system would use a proper
  client-server database.

---

## 📊 The SQL Query Library

This project is paired with a standalone library of 11 documented SQL
queries (in `/queries`), covering everything from basic duplicate
detection to statistical anomaly scoring. Each query includes business
context explaining why a real bank would need it. See the main project
README for the full list.

---

## 🙋 About This Project

Built by [Your Name] as a hands-on project to practice SQL and
full-stack development using real-world banking data patterns. I work
in banking software professionally, which inspired the realistic feature
set, but all data, logic, and code here is original and entirely
synthetic — no proprietary or confidential information is used anywhere.

Feedback and suggestions welcome — feel free to connect on
[LinkedIn](#) or open an issue.
