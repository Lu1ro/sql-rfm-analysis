import pandas as pd
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
excel_path = os.path.join(base_dir, 'data', 'online_retail_II.xlsx')
csv_path_2009 = os.path.join(base_dir, 'data', 'retail_2009.csv')
csv_path_2010 = os.path.join(base_dir, 'data', 'retail_2010.csv')

def convert_excel_to_csv():
    print(f"🔄 Reading Excel file: {excel_path}...")
    
    if not os.path.exists(excel_path):
        print("❌ ERROR: File 'online_retail_II.xlsx' not found in 'data' folder.")
        return

    try:
        xls = pd.ExcelFile(excel_path)
        print(f"✅ Found sheets: {xls.sheet_names}")
    except Exception as e:
        print(f"❌ Error opening Excel file: {e}")
        return

    print("💾 Saving 2009-2010 data to CSV...")
    df1 = pd.read_excel(xls, sheet_name=0) 
    df1.to_csv(csv_path_2009, index=False)
    print(f"✅ Created: {csv_path_2009}")

    print("💾 Saving 2010-2011 data to CSV...")
    df2 = pd.read_excel(xls, sheet_name=1)
    df2.to_csv(csv_path_2010, index=False)
    print(f"✅ Created: {csv_path_2010}")
    
    print("🎉 Done! Now you can run setup_db.py")

if __name__ == "__main__":
    convert_excel_to_csv()
