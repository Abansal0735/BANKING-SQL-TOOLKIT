-- ============================================================
-- Banking SQL Toolkit — Schema
-- Run this FIRST to create the tables before loading CSV data.
-- Compatible with SQLite, Postgres, and MySQL (minor tweaks noted).
-- ============================================================

CREATE TABLE branches (
    branch_id     INTEGER PRIMARY KEY,
    branch_name   VARCHAR(50),
    region        VARCHAR(50)
);

CREATE TABLE customers (
    customer_id     INTEGER PRIMARY KEY,
    full_name       VARCHAR(100),
    segment         VARCHAR(20),
    region          VARCHAR(50),
    onboarding_date DATE,
    risk_rating     VARCHAR(10)
);

CREATE TABLE accounts (
    account_id      INTEGER PRIMARY KEY,
    customer_id     INTEGER,
    account_type    VARCHAR(20),
    branch_id       INTEGER,
    open_date       DATE,
    status          VARCHAR(10),
    opening_balance DECIMAL(14,2)
);

CREATE TABLE transactions (
    transaction_id   BIGINT PRIMARY KEY,
    account_id       INTEGER,
    txn_date         DATE,
    txn_time         VARCHAR(8),
    txn_type         VARCHAR(20),
    amount           DECIMAL(14,2),
    channel          VARCHAR(20),
    counterparty_id  INTEGER
);

CREATE TABLE loans (
    loan_id            INTEGER PRIMARY KEY,
    account_id         INTEGER,
    loan_amount        DECIMAL(14,2),
    disbursement_date  DATE,
    emi_amount         DECIMAL(10,2),
    due_date           DATE,
    last_payment_date  DATE,
    loan_status        VARCHAR(15),
    product_type       VARCHAR(20)
);

-- NOTE: Foreign key constraints (e.g. accounts.customer_id -> customers.customer_id)
-- are intentionally left out here to keep CSV loading simple and avoid
-- load-order errors. Add them later with ALTER TABLE if you want strict
-- referential integrity for a production-style demo.
