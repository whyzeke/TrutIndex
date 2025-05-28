import pandas as pd
import sqlite3
import os

def excel_to_sqlite(excel_file, sqlite_db):
    # Load the Excel file
    xls = pd.ExcelFile(excel_file)
    
    # Connect to SQLite database
    conn = sqlite3.connect(sqlite_db)
    
    for sheet_name in xls.sheet_names:
        print(f"Processing sheet: {sheet_name}")
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Clean table name
        table_name = sheet_name.replace(' ', '_').replace('-', '_')
        
        # Write dataframe to SQLite table
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Created table '{table_name}' with {len(df)} records.\n")
    
    # Verification: print tables and their contents
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Database tables and contents:")
    for (table_name,) in tables:
        print(f"\nTable: {table_name}")
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")  # Show up to 10 rows
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        # Print columns as header
        print("\t".join(columns))
        # Print rows
        for row in rows:
            print("\t".join(str(cell) for cell in row))
    
    conn.close()
    print(f"\nExcel file '{excel_file}' has been converted to SQLite database '{sqlite_db}'.")

if __name__ == "__main__":
    excel_file = "Country.xlsx"  # Replace with your Excel file path
    sqlite_db = "output_database.db"     # Desired SQLite DB filename
    
    if not os.path.exists(excel_file):
        print(f"Error: Excel file '{excel_file}' does not exist.")
    else:
        excel_to_sqlite(excel_file, sqlite_db)
