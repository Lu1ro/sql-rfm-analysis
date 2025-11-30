import pandas as pd
import sqlite3
import os

# --- Configuration: Define File Paths ---
# 'base_dir' ensures the script runs correctly regardless of where it is executed
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, 'data', 'ecommerce.db')
file1 = os.path.join(base_dir, 'data', 'retail_2009.csv')
file2 = os.path.join(base_dir, 'data', 'retail_2010.csv')

def create_database():
    """
    ETL Function: Extracts data from CSVs, Transforms it, and Loads it into SQLite.
    """
    print("[INFO] Starting ETL Pipeline...")
    
    # --- Step 1: Extraction ---
    if not os.path.exists(file1) or not os.path.exists(file2):
        print("[ERROR] Source files not found. Please check 'data/' directory.")
        return

    print("[INFO] Loading raw data files...")
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    print("[INFO] Merging datasets (2009-2011)...")
    df = pd.concat([df1, df2], ignore_index=True)

    # --- Step 2: Transformation ---
    # Standardize column names to snake_case for easier SQL querying
    df.columns = [c.strip().replace(' ', '_').lower() for c in df.columns]
    
    print(f"[INFO] Original Row Count: {len(df)}")
    
    # Remove records without Customer ID (essential for RFM analysis)
    df = df.dropna(subset=['customer_id'])
    
    # Normalize 'invoicedate' column name if needed
    if 'invoicedate' in df.columns:
        df.rename(columns={'invoicedate': 'invoice_date'}, inplace=True)

    # Convert data types for performance optimization
    df['customer_id'] = df['customer_id'].astype(int)
    df['invoice_date'] = pd.to_datetime(df['invoice_date'])
    
    print(f"[INFO] Cleaned Row Count: {len(df)}")

    # --- Step 3: Loading ---
    print(f"[INFO] Saving data to SQLite database: {db_path}")
    conn = sqlite3.connect(db_path)
    
    # Write DataFrame to SQL table 'transactions'
    df.to_sql('transactions', conn, if_exists='replace', index=False)
    
    conn.close()
    print("[SUCCESS] Database 'ecommerce.db' created successfully.")

if __name__ == "__main__":
    create_database()
