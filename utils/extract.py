import json
import xmltodict
import pymongo
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

def get_data_from_source():
    choice = input("Select source type (csv/excel/sql/parquet): ").strip().lower()
    source_info = {}

    if choice == "csv":
        path = input("Enter the path to the CSV file: ").strip()
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ File not found: {path}")
        
        data = pd.read_csv(path)
        source_info = {"source": f"local file: {path}", "type": "CSV"}

    elif choice == "excel":
        path = input("Enter the path to the Excel file: ").strip()
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ File not found: {path}")
        
        excel_file = pd.ExcelFile(path)
        print(f"📄 Available sheets: {excel_file.sheet_names}")
        sheet_name = input("Enter sheet name (or press Enter for first sheet): ").strip()
        
        if not sheet_name:
            sheet_name = excel_file.sheet_names[0]
        
        data = pd.read_excel(path, sheet_name=sheet_name)
        source_info = {"source": f"local file: {path}, sheet: {sheet_name}", "type": "Excel"}

    elif choice == "sql":
        try:
            source_db = input("Enter source database name: ").strip()
            engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@localhost/{source_db}")
            
            tables = pd.read_sql("SHOW TABLES", engine)
            print("📦 Available tables:")
            for i, table in enumerate(tables.iloc[:, 0]):
                print(f"{i + 1}. {table}")
            
            table_index = int(input("Select a table by number: ")) - 1
            table_name = tables.iloc[table_index, 0]

            use_query = input("Use custom SQL query? (y/n): ").strip().lower()
            if use_query == 'y':
                query = input("Enter your SQL query: ").strip()
                data = pd.read_sql(query, engine)
            else:
                data = pd.read_sql(f"SELECT * FROM {table_name}", engine)
            
            source_info = {"source": f"MySQL: {source_db}.{table_name}", "type": "SQL"}

        except Exception as e:
            raise Exception(f"❌ Database error: {e}")

    elif choice == "parquet":
        path = input("Enter the path to the Parquet file: ").strip()
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ File not found: {path}")
        
        data = pd.read_parquet(path)
        source_info = {"source": f"local file: {path}", "type": "Parquet"}

    else:
        raise ValueError("❌ Invalid input. Please choose from: csv, excel, sql, parquet")

    # Add ingestion timestamp
    source_info["timestamp"] = str(datetime.now())

    # ✅ Extra validation and preview
    if data.empty or data.shape[1] == 0:
        print("⚠️ Warning: Extracted DataFrame is empty or has no columns.")
    else:
        print(f"✅ Data extracted successfully. Shape: {data.shape}")
        print("🔍 Sample data:")
        print(data.head())

    return data, source_info
