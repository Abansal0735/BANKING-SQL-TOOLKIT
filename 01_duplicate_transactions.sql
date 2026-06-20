-- ============================================================
-- QUERY 1: Duplicate Transaction Detection
-- ============================================================
-- BUSINESS CONTEXT:
-- Banks must catch duplicate transactions caused by system retries,
-- batch reprocessing errors, or double-submission from a channel
-- (e.g., a customer double-tapping "Submit" on mobile, or a batch
-- job re-running after a timeout). Undetected duplicates lead to
-- double-billing, reconciliation breaks, and customer complaints.
--
-- This query flags transactions on the SAME account, SAME date,
-- SAME amount, and SAME type appearing more than once — a strong
-- signal of an operational duplicate (not a coincidence, since the
-- combination of all four matching is statistically rare).
--
-- INTERVIEW RELEVANCE: This is a very common take-home/interview
-- question for bank data analyst roles ("how would you detect
-- duplicate transactions in a ledger table?").
-- ============================================================

SELECT
    account_id,
    txn_date,
    amount,
    txn_type,
    COUNT(*) AS occurrence_count
FROM transactions
GROUP BY account_id, txn_date, amount, txn_type
HAVING COUNT(*) > 1
ORDER BY occurrence_count DESC, txn_date DESC;

-- VARIANT: To also see the individual duplicate transaction_ids
-- (useful for an ops team to actually action/reverse them):

SELECT
    t.transaction_id,
    t.account_id,
    t.txn_date,
    t.txn_time,
    t.amount,
    t.txn_type,
    t.channel
FROM transactions t
JOIN (
    SELECT account_id, txn_date, amount, txn_type
    FROM transactions
    GROUP BY account_id, txn_date, amount, txn_type
    HAVING COUNT(*) > 1
) dup
  ON t.account_id = dup.account_id
 AND t.txn_date = dup.txn_date
 AND t.amount = dup.amount
 AND t.txn_type = dup.txn_type
ORDER BY t.account_id, t.txn_date, t.txn_time;

-- NOTE: This catches exact duplicates. A more advanced version
-- (not covered in this pack) would use a time-window self-join
-- to catch near-duplicates within, say, a 5-minute window even
-- if the amount differs slightly due to fees.
