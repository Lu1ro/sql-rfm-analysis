/*
   Step 3: Customer Segmentation
   Objective: Map RFM scores to human-readable business segments.
   
   Segments Logic:
   - Champions: Bought recently, buy often, and spend the most (555).
   - Loyal Customers: High frequency and monetary value.
   - New Customers: High Recency (bought recently) but low Frequency.
   - At Risk: Big spenders who haven't purchased in a while.
   - Lost Customers: Lowest scores across all metrics.
*/

SELECT 
    customer_id,
    recency,
    frequency,
    monetary,
    r_score || f_score || m_score AS rfm_score,
    CASE 
        WHEN (r_score = 5 AND f_score = 5 AND m_score = 5) THEN 'Champions'
        WHEN (f_score >= 4 AND m_score >= 4) THEN 'Loyal Customers'
        WHEN (r_score = 5 AND m_score = 1) THEN 'New Customers'
        WHEN (r_score = 1 AND f_score = 1) THEN 'Lost Customers'
        WHEN (r_score <= 2 AND f_score >= 4 AND m_score >= 4) THEN 'At Risk'
        ELSE 'Regular'
    END AS customer_segment
FROM rfm_metrics
ORDER BY monetary DESC;