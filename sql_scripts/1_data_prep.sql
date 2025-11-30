/* SQL Pipeline for E-commerce RFM Analysis (Steps 1, 2, 3) */

-- STEP 1: Data Preparation & Cleaning (Creates clean_transactions VIEW)
DROP VIEW IF EXISTS clean_transactions;

CREATE VIEW clean_transactions AS
SELECT 
    customer_id,
    invoice_date,
    invoice,
    quantity,
    price,
    (quantity * price) AS total_amount
FROM transactions
WHERE quantity > 0 
  AND price > 0
  AND customer_id IS NOT NULL;


-- STEP 2: RFM Metrics Calculation (Creates rfm_metrics TABLE)
DROP TABLE IF EXISTS rfm_metrics;

CREATE TABLE rfm_metrics AS
WITH reference_date AS (
    -- Establish a reference point for Recency calculation
    SELECT DATE(MAX(invoice_date), '+1 day') AS max_date 
    FROM clean_transactions
),
customer_agg AS (
    -- Aggregate transaction data by Customer ID
    SELECT
        t.customer_id,
        (SELECT max_date FROM reference_date) AS ref_d,
        MAX(t.invoice_date) AS last_purchase_date,
        COUNT(DISTINCT t.invoice) AS frequency,
        SUM(t.total_amount) AS monetary
    FROM clean_transactions t
    GROUP BY t.customer_id
)
SELECT
    customer_id,
    CAST(julianday(ref_d) - julianday(last_purchase_date) AS INTEGER) AS recency,
    frequency,
    monetary,
    -- Assign scores (1=low, 5=high)
    NTILE(5) OVER (ORDER BY CAST(julianday(ref_d) - julianday(last_purchase_date) AS INTEGER) DESC) AS r_score,
    NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
    NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
FROM customer_agg;


-- STEP 3: Customer Segmentation (Final Report)
SELECT 
    customer_id,
    recency,
    frequency,
    monetary,
    r_score || f_score || m_score AS rfm_score,
    CASE 
        -- Assign human-readable labels based on RFM scores
        WHEN (r_score = 5 AND f_score = 5 AND m_score = 5) THEN 'Champions'
        WHEN (f_score >= 4 AND m_score >= 4) THEN 'Loyal Customers'
        WHEN (r_score = 5 AND m_score = 1) THEN 'New Customers'
        WHEN (r_score = 1 AND f_score = 1) THEN 'Lost Customers'
        WHEN (r_score <= 2 AND f_score >= 4 AND m_score >= 4) THEN 'At Risk'
        ELSE 'Regular'
    END AS customer_segment
FROM rfm_metrics
ORDER BY monetary DESC;