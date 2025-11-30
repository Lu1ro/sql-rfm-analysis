import pandas as pd
import sqlite3
import os

# Define file paths relative to the script location
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, 'data', 'ecommerce.db')
file1 = os.path.join(base_dir, 'data', 'retail_2009.csv')
file2 = os.path.join(base_dir, 'data', 'retail_2010.csv')


def create_database():
    print("🚀 Starting ETL Pipeline...")

    # 1. Validation: Ensure source files exist
    if not os.path.exists(file1) or not os.path.exists(file2):
        print("❌ Error: Source CSV files not found in 'data/' directory.")
        return

    # 2. Extraction: Load raw datasets
    print("   [Extract] Loading raw CSV files...")
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    print("   [Extract] Merging datasets...")
    df = pd.concat([df1, df2], ignore_index=True)

    # 3. Transformation: Clean and standardize data
    # Standardize column names to snake_case for SQL compatibility
    df.columns = [c.strip().replace(' ', '_').lower() for c in df.columns]

    print(f"   [Transform] Original Rows: {len(df)}")

    # Remove records with missing Customer IDs (cannot perform RFM on anonymous users)
    df = df.dropna(subset=['customer_id'])

    # Rename 'invoicedate' to 'invoice_date' if necessary for consistency
    if 'invoicedate' in df.columns:
        df.rename(columns={'invoicedate': 'invoice_date'}, inplace=True)

    # Type Casting
    df['customer_id'] = df['customer_id'].astype(int)
    df['invoice_date'] = pd.to_datetime(df['invoice_date'])

    print(f"   [Transform] Cleaned Rows: {len(df)}")

    # 4. Loading: Save to SQLite database
    print(f"   [Load] Saving to SQLite database at {db_path}...")
    conn = sqlite3.connect(db_path)
    df.to_sql('transactions', conn, if_exists='replace', index=False)
    conn.close()
    print("✅ Success: Database created and populated.")


if __name__ == "__main__":
    create_database()