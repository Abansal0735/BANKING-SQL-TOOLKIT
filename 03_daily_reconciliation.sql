-- ============================================================
-- QUERY 3: Daily Account Reconciliation (Running Balance Check)
-- ============================================================
-- BUSINESS CONTEXT:
-- Every bank's operations team reconciles account balances daily:
-- opening_balance + (credits - debits) should equal the system's
-- recorded closing balance. Mismatches indicate missed transactions,
-- system sync issues, or potential fraud — this is one of the
-- highest-priority daily checks in bank operations.
--
-- This query builds a running computed balance per account per day
-- using a window function, which is the standard pattern for this
-- problem and a very common SQL interview topic (cumulative sums).
-- ============================================================

WITH daily_movement AS (
    SELECT
        account_id,
        txn_date,
        SUM(CASE WHEN txn_type IN ('Deposit', 'Transfer') THEN amount ELSE 0 END) AS total_credits,
        SUM(CASE WHEN txn_type = 'Withdrawal' THEN amount ELSE 0 END) AS total_debits
    FROM transactions
    GROUP BY account_id, txn_date
)
SELECT
    a.account_id,
    a.opening_balance,
    dm.txn_date,
    dm.total_credits,
    dm.total_debits,
    a.opening_balance + SUM(dm.total_credits - dm.total_debits)
        OVER (PARTITION BY a.account_id ORDER BY dm.txn_date) AS computed_running_balance
FROM accounts a
JOIN daily_movement dm ON a.account_id = dm.account_id
ORDER BY a.account_id, dm.txn_date;

-- ============================================================
-- VARIANT: Reconciliation MISMATCH check
-- If your dataset has a separate "recorded_balance" snapshot table
-- (not included in this base pack, but common in real systems),
-- you'd compare against it like this:
--
-- SELECT
--     r.account_id, r.txn_date, r.computed_running_balance,
--     s.recorded_closing_balance,
--     r.computed_running_balance - s.recorded_closing_balance AS variance
-- FROM running_balance r
-- JOIN balance_snapshots s
--   ON r.account_id = s.account_id AND r.txn_date = s.snapshot_date
-- WHERE ABS(r.computed_running_balance - s.recorded_closing_balance) > 0.01
-- ORDER BY ABS(variance) DESC;
--
-- This pattern — "compute expected, compare to recorded, flag variance" —
-- is the core logic behind almost ALL reconciliation systems in banking,
-- not just account balances (also used for card settlements, nostro/vostro
-- accounts, and interbank clearing).
-- ============================================================
