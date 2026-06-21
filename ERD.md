# Database Schema — Entity Relationship Diagram

This diagram shows how the 5 tables in this dataset relate to each other.
GitHub renders this automatically — no image needed.

```mermaid
erDiagram
    BRANCHES ||--o{ ACCOUNTS : "has"
    CUSTOMERS ||--o{ ACCOUNTS : "owns"
    ACCOUNTS ||--o{ TRANSACTIONS : "records"
    ACCOUNTS ||--o| LOANS : "may have"
    ACCOUNTS ||--o{ TRANSACTIONS : "counterparty (transfers)"

    BRANCHES {
        int branch_id PK
        string branch_name
        string region
    }

    CUSTOMERS {
        int customer_id PK
        string full_name
        string segment
        string region
        date onboarding_date
        string risk_rating
    }

    ACCOUNTS {
        int account_id PK
        int customer_id FK
        string account_type
        int branch_id FK
        date open_date
        string status
        decimal opening_balance
    }

    TRANSACTIONS {
        bigint transaction_id PK
        int account_id FK
        date txn_date
        string txn_time
        string txn_type
        decimal amount
        string channel
        int counterparty_id FK
    }

    LOANS {
        int loan_id PK
        int account_id FK
        decimal loan_amount
        date disbursement_date
        decimal emi_amount
        date due_date
        date last_payment_date
        string loan_status
        string product_type
    }
```

## Relationship Notes

- **One branch → many accounts.** Each account is opened at exactly one
  branch.
- **One customer → many accounts.** A customer can hold multiple
  accounts (e.g., a Savings account and a Loan account).
- **One account → many transactions.** All deposits, withdrawals, and
  transfers are tied to a single account.
- **One account → at most one loan.** Only accounts with
  `account_type = 'Loan'` have a corresponding row in the loans table.
- **Transactions can reference another account as a counterparty**
  (used for `Transfer` type transactions) — this is a self-referencing
  relationship back into `accounts`.

## Why This Structure

This mirrors a simplified version of a real core banking data model:
customer and account are separated (since one customer can have
multiple accounts), transactions are append-only event records (never
updated, only inserted — which is how real ledgers work), and loans
are modeled as a one-to-one extension of an account rather than a
separate customer-level entity, since a loan is fundamentally an
account-level product.
