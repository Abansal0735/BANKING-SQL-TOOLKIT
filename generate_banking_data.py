"""
Synthetic Banking Dataset Generator
------------------------------------
Generates fully synthetic data for: customers, accounts, transactions,
loans, branches. No real data used. Safe to distribute publicly.

Run: python3 generate_banking_data.py
Output: 5 CSV files in ./output/
"""

import random
import csv
import os
from datetime import date, timedelta

random.seed(42)  # reproducible output

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------- Reference lists ----------
FIRST_NAMES = ["James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda",
               "David","Elizabeth","William","Barbara","Richard","Susan","Joseph","Jessica",
               "Thomas","Sarah","Charles","Karen","Ravi","Priya","Wei","Mei","Carlos","Sofia",
               "Ahmed","Fatima","Liam","Olivia"]
LAST_NAMES = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis",
              "Rodriguez","Martinez","Kumar","Sharma","Chen","Wang","Khan","Ali",
              "Silva","Costa","Müller","Schmidt"]
REGIONS = ["North", "South", "East", "West", "Central"]
SEGMENTS = ["Retail", "SME", "Corporate"]
RISK_RATINGS = ["Low", "Medium", "High"]
ACCOUNT_TYPES = ["Savings", "Current", "Loan"]
ACCOUNT_STATUS = ["Active", "Dormant", "Closed"]
TXN_TYPES = ["Deposit", "Withdrawal", "Transfer"]
CHANNELS = ["ATM", "Branch", "Online", "Mobile"]
LOAN_PRODUCTS = ["Personal", "Home", "Auto", "SME"]
LOAN_STATUS = ["Active", "Closed", "Default"]
BRANCH_NAMES = ["Downtown","Uptown","Riverside","Hillview","Lakeside","Central Plaza",
                "Eastgate","Westend","Northpark","Southbridge","Harborview","Old Town",
                "Greenfield","Metro Square","Sunset"]

def random_date(start_year=2021, end_year=2025):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

# ---------- 1. BRANCHES ----------
NUM_BRANCHES = 15
branches = []
for i in range(1, NUM_BRANCHES + 1):
    branches.append({
        "branch_id": i,
        "branch_name": f"{BRANCH_NAMES[i-1]} Branch",
        "region": random.choice(REGIONS)
    })

with open(f"{OUTPUT_DIR}/branches.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=branches[0].keys())
    w.writeheader()
    w.writerows(branches)

# ---------- 2. CUSTOMERS ----------
NUM_CUSTOMERS = 2000
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    onboarding = random_date(2018, 2025)
    customers.append({
        "customer_id": i,
        "full_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
        "segment": random.choices(SEGMENTS, weights=[70, 22, 8])[0],
        "region": random.choice(REGIONS),
        "onboarding_date": onboarding.isoformat(),
        "risk_rating": random.choices(RISK_RATINGS, weights=[70, 22, 8])[0]
    })

with open(f"{OUTPUT_DIR}/customers.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=customers[0].keys())
    w.writeheader()
    w.writerows(customers)

# ---------- 3. ACCOUNTS ----------
# Each customer gets 1-2 accounts
accounts = []
account_id_counter = 1
customer_accounts_map = {}  # customer_id -> list of account_ids

for cust in customers:
    num_accounts = random.choices([1, 2], weights=[70, 30])[0]
    customer_accounts_map[cust["customer_id"]] = []
    for _ in range(num_accounts):
        open_date = random_date(
            int(cust["onboarding_date"][:4]), 2025
        )
        status = random.choices(ACCOUNT_STATUS, weights=[78, 15, 7])[0]
        accounts.append({
            "account_id": account_id_counter,
            "customer_id": cust["customer_id"],
            "account_type": random.choices(ACCOUNT_TYPES, weights=[55, 35, 10])[0],
            "branch_id": random.randint(1, NUM_BRANCHES),
            "open_date": open_date.isoformat(),
            "status": status,
            "opening_balance": round(random.uniform(500, 50000), 2)
        })
        customer_accounts_map[cust["customer_id"]].append(account_id_counter)
        account_id_counter += 1

with open(f"{OUTPUT_DIR}/accounts.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=accounts[0].keys())
    w.writeheader()
    w.writerows(accounts)

# ---------- 4. TRANSACTIONS ----------
# Generate transactions per active/dormant account
transactions = []
txn_id_counter = 1000000

active_accounts = [a for a in accounts if a["status"] != "Closed"]

for acct in active_accounts:
    num_txns = random.randint(5, 60)
    open_dt = date.fromisoformat(acct["open_date"])
    for _ in range(num_txns):
        txn_date = random_date(max(open_dt.year, 2023), 2025)
        if txn_date < open_dt:
            txn_date = open_dt

        txn_type = random.choices(TXN_TYPES, weights=[35, 35, 30])[0]
        amount = round(random.uniform(10, 9500), 2)

        # Inject occasional duplicate transactions (same account, same amount, same/near date)
        is_duplicate_pair = random.random() < 0.015  # ~1.5% chance to create a duplicate

        counterparty = None
        if txn_type == "Transfer":
            counterparty = random.choice(accounts)["account_id"]

        txn = {
            "transaction_id": txn_id_counter,
            "account_id": acct["account_id"],
            "txn_date": txn_date.isoformat(),
            "txn_time": f"{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}",
            "txn_type": txn_type,
            "amount": amount,
            "channel": random.choice(CHANNELS),
            "counterparty_id": counterparty if counterparty else ""
        }
        transactions.append(txn)
        txn_id_counter += 1

        if is_duplicate_pair:
            # create a near-duplicate transaction (same account, same amount, same day, different time/channel)
            dup = txn.copy()
            dup["transaction_id"] = txn_id_counter
            dup["txn_time"] = f"{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"
            dup["channel"] = random.choice(CHANNELS)
            transactions.append(dup)
            txn_id_counter += 1

# Inject structuring pattern: a handful of accounts get many small transactions
# (e.g., 5-9 deposits just under round thresholds, same day) to simulate AML-flag scenarios
structuring_accounts = random.sample(active_accounts, k=min(15, len(active_accounts)))
for acct in structuring_accounts:
    burst_date = random_date(2024, 2025)
    num_small_txns = random.randint(5, 9)
    for _ in range(num_small_txns):
        transactions.append({
            "transaction_id": txn_id_counter,
            "account_id": acct["account_id"],
            "txn_date": burst_date.isoformat(),
            "txn_time": f"{random.randint(8,18):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}",
            "txn_type": "Deposit",
            "amount": round(random.uniform(900, 995), 2),  # just under a 1000 threshold
            "channel": random.choice(["Branch", "ATM"]),
            "counterparty_id": ""
        })
        txn_id_counter += 1

with open(f"{OUTPUT_DIR}/transactions.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=transactions[0].keys())
    w.writeheader()
    w.writerows(transactions)

# ---------- 5. LOANS ----------
loan_accounts = [a for a in accounts if a["account_type"] == "Loan"]
loans = []
loan_id_counter = 1

for acct in loan_accounts:
    disb_date = date.fromisoformat(acct["open_date"])
    loan_amount = round(random.uniform(5000, 500000), 2)
    emi = round(loan_amount / random.randint(12, 60), 2)
    due_date = disb_date + timedelta(days=30)

    status = random.choices(LOAN_STATUS, weights=[65, 25, 10])[0]

    if status == "Closed":
        last_payment = due_date + timedelta(days=random.randint(0, 5))
    elif status == "Default":
        # last payment was long ago, simulating 90+ days past due
        last_payment = due_date - timedelta(days=random.randint(0, 10))
        due_date = due_date  # due date stays in the past relative to "today" (assume today = 2025-12-31)
    else:  # Active
        last_payment = due_date - timedelta(days=random.randint(-5, 5))

    loans.append({
        "loan_id": loan_id_counter,
        "account_id": acct["account_id"],
        "loan_amount": loan_amount,
        "disbursement_date": disb_date.isoformat(),
        "emi_amount": emi,
        "due_date": due_date.isoformat(),
        "last_payment_date": last_payment.isoformat(),
        "loan_status": status,
        "product_type": random.choice(LOAN_PRODUCTS)
    })
    loan_id_counter += 1

with open(f"{OUTPUT_DIR}/loans.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=loans[0].keys())
    w.writeheader()
    w.writerows(loans)

print(f"Done. Generated:")
print(f"  {len(branches)} branches")
print(f"  {len(customers)} customers")
print(f"  {len(accounts)} accounts")
print(f"  {len(transactions)} transactions")
print(f"  {len(loans)} loans")
print(f"Files written to ./{OUTPUT_DIR}/")
