# 🛒 E-Commerce RFM Analysis & Customer Segmentation

## 📌 Business Goal
The objective of this project is to segment customers of a UK-based online retailer using **RFM (Recency, Frequency, Monetary)** analysis. This segmentation allows the marketing team to target specific user groups (e.g., "Champions", "At Risk") with personalized campaigns.

**Dataset:** 2 Years of transactional data (2009-2011).

## 📊 Final Result (Segmentation)
The SQL analysis successfully categorized customers based on their purchasing behavior.
* **Champions:** High spenders who buy often and recently.
* **Loyal Customers:** Frequent buyers.
* **At Risk:** Big spenders who haven't purchased in a while.

![RFM Result](images/rfm_result.png)

## 🛠️ Tech Stack
* **Python (Pandas):** ETL process (Extract, Transform, Load) to merge and clean 2 years of Excel data into a SQLite database.
* **SQL (SQLite):**
    * Data Cleaning (Views).
    * RFM Calculation (Window Functions `NTILE`).
    * Segmentation Logic (`CASE` statements).

## 🚀 How to Replicate
1.  Run the ETL script:
    ```bash
    python notebooks/setup_db.py
    ```
2.  Execute SQL scripts in DBeaver/VS Code:
    * `1_data_prep.sql`
    * `2_rfm_calculation.sql`
    * `3_segmentation.sql`