-- ============================================================
-- QUERY 4: Structuring Pattern Detection (AML Red Flag)
-- ============================================================
-- BUSINESS CONTEXT:
-- "Structuring" (aka "smurfing") is a money-laundering technique
-- where someone deposits multiple amounts just under a reporting
-- threshold (commonly $1,000 or $10,000 depending on jurisdiction)
-- to avoid triggering mandatory currency transaction reports.
--
-- Classic red flag pattern: multiple deposits on the SAME DAY,
-- to the SAME account, each just under a round threshold.
--
-- This query flags accounts with 5+ deposits in a single day where
-- the average deposit amount sits suspiciously just under $1,000 —
-- a textbook structuring signature that AML/compliance analysts
-- are trained to look for.
--
-- INTERVIEW RELEVANCE: AML/fraud detection logic is increasingly
-- asked about in fintech and bank SQL interviews, especially for
-- compliance-adjacent analyst roles.
-- ============================================================

SELECT
    account_id,
    txn_date,
    COUNT(*) AS deposit_count,
    SUM(amount) AS total_deposited,
    ROUND(AVG(amount), 2) AS avg_deposit_amount
FROM transactions
WHERE txn_type = 'Deposit'
GROUP BY account_id, txn_date
HAVING COUNT(*) >= 5
   AND AVG(amount) BETWEEN 800 AND 999   -- adjust threshold to your jurisdiction's reporting limit
ORDER BY total_deposited DESC;

-- ============================================================
-- VARIANT: Join back to customer info for an investigator's view
-- (this is the version a compliance analyst would actually use —
-- raw account_id isn't actionable, they need the customer context)
-- ============================================================

SELECT
    c.customer_id,
    c.full_name,
    c.risk_rating,
    flagged.account_id,
    flagged.txn_date,
    flagged.deposit_count,
    flagged.total_deposited
FROM (
    SELECT
        account_id,
        txn_date,
        COUNT(*) AS deposit_count,
        SUM(amount) AS total_deposited,
        AVG(amount) AS avg_amount
    FROM transactions
    WHERE txn_type = 'Deposit'
    GROUP BY account_id, txn_date
    HAVING COUNT(*) >= 5 AND AVG(amount) BETWEEN 800 AND 999
) flagged
JOIN accounts a ON flagged.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
ORDER BY flagged.total_deposited DESC;

-- NOTE: Real AML systems also check patterns ACROSS multiple days
-- and ACROSS linked accounts (same customer, joint accounts, etc.),
-- which requires more advanced window functions. This query covers
-- the foundational single-day, single-account case.
