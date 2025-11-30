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
ORDER BY monetary DESC
LIMIT 20;