import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Configuration & Setup ---
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, 'data', 'ecommerce.db')
img_dir = os.path.join(base_dir, 'images')

if not os.path.exists(img_dir):
    os.makedirs(img_dir)

# --- Data Extraction ---
print("[INFO] Connecting to database...")
conn = sqlite3.connect(db_path)

sql_query = """
SELECT 
    recency,
    frequency,
    monetary,
    CASE 
        WHEN (r_score = 5 AND f_score = 5 AND m_score = 5) THEN 'Champions'
        WHEN (f_score >= 4 AND m_score >= 4) THEN 'Loyal Customers'
        WHEN (r_score = 5 AND m_score = 1) THEN 'New Customers'
        WHEN (r_score = 1 AND f_score = 1) THEN 'Lost Customers'
        WHEN (r_score <= 2 AND f_score >= 4 AND m_score >= 4) THEN 'At Risk'
        ELSE 'Regular'
    END AS segment
FROM rfm_metrics
"""

print("[INFO] Extracting data...")
df = pd.read_sql_query(sql_query, conn)
conn.close()

# --- Visualization ---
sns.set_theme(style="whitegrid")

# Chart 1: Customer Segment Distribution
plt.figure(figsize=(10, 6))
segment_order = df['segment'].value_counts().index
sns.countplot(y='segment', data=df, order=segment_order, palette='viridis')

plt.title('Distribution of Customer Segments', fontsize=14)
plt.xlabel('Number of Customers')
plt.ylabel('Segment')
plt.tight_layout()

dist_path = os.path.join(img_dir, 'rfm_distribution.png')
plt.savefig(dist_path)
print(f"[SUCCESS] Saved Chart 1: {dist_path}")

# Chart 2: Recency vs. Frequency Scatter Plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='recency', y='frequency', hue='segment', alpha=0.6, palette='deep')

plt.yscale('log')
plt.title('Customer Segments: Recency vs. Frequency', fontsize=14)
plt.xlabel('Recency (Days since last purchase)')
plt.ylabel('Frequency (Log Scale)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

scatter_path = os.path.join(img_dir, 'rfm_scatter.png')
plt.savefig(scatter_path)
print(f"[SUCCESS] Saved Chart 2: {scatter_path}")

print("[DONE] Visualization pipeline completed successfully.")