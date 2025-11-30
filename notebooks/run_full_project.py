import sqlite3
import pandas as pd
import os

# --- Configuration ---
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, 'data', 'ecommerce.db')

def execute_sql_file(cursor, filename):
    """
    Helper function to read and execute a SQL script file.
    """
    file_path = os.path.join(base_dir, 'sql_scripts', filename)
    print(f"[INFO] Executing SQL script: {filename}...")
    
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return False
        
    with open(file_path, 'r') as f:
        sql_script = f.read()
        try:
            cursor.executescript(sql_script)
            print(f"[SUCCESS] executed {filename}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to execute {filename}: {e}")
            return False

def main():
    # Ensure the database exists
    if not os.path.exists(db_path):
        print("[ERROR] Database not found. Please run 'setup_db.py' first.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("[START] Running Full SQL Pipeline...")

    # Execute SQL scripts in the correct order to maintain dependency
    # Step 1: Data Cleaning
    if not execute_sql_file(cursor, '1_data_prep.sql'): return
    
    # Step 2: Metrics Calculation
    if not execute_sql_file(cursor, '2_rfm_calculation.sql'): return
    
    # Step 3: Segmentation (Final Report)
    print("\n[REPORT] Top 10 High-Value Customers:")
    try:
        # We read the 3rd script again just to fetch the SELECT query for display
        with open(os.path.join(base_dir, 'sql_scripts', '3_segmentation.sql'), 'r') as f:
            query = f.read()
            df = pd.read_sql_query(query, conn)
            print(df.head(10))
            
            # Optional: Export results to CSV for sharing
            output_csv = os.path.join(base_dir, 'rfm_results.csv')
            df.to_csv(output_csv, index=False)
            print(f"\n[INFO] Full results exported to: {output_csv}")
            
    except Exception as e:
        print(f"[ERROR] Failed to fetch results: {e}")

    conn.close()
    print("[DONE] Pipeline finished.")

if __name__ == "__main__":
    main()
