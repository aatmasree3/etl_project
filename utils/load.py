import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from datetime import datetime
import json

# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# You may import these from your existing pipeline
from utils.transform import transformation_steps
from utils.extract import get_data_from_source

def load_to_mysql(df, table_name="cleaned_data"):
    try:
        # 1️⃣ Check if DataFrame has data and columns
        if df.empty or df.shape[1] == 0:
            print("❗ Error: DataFrame is empty or has no columns. Skipping load.")
            return

        # 2️⃣ MySQL connection string
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}")

        # 3️⃣ Write DataFrame to MySQL
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        print(f"✅ Data loaded successfully into '{table_name}' table.")

    except Exception as e:
        print(f"❌ Failed to load data: {e}")

def log_metadata(source_info, transformation_steps, destination_table):
    metadata = {
        "timestamp": str(datetime.now()),
        "source": source_info,
        "transformations": transformation_steps,
        "destination": f"MySQL → {destination_table}"
    }

    # Save lineage log to a JSON file
    os.makedirs("logs", exist_ok=True)  # Make sure 'logs/' exists
    with open("logs/lineage_log.json", "w") as f:
        json.dump(metadata, f, indent=4)
    print("📝 Metadata and lineage log saved to logs/lineage_log.json")

if __name__ == "__main__":
    # Extract raw data and source info
    data, source_info = get_data_from_source()

    # Transform data
    from transform import transform_data
    df_transformed = transform_data(data)

    # ✅ Load to MySQL if data is valid
    load_to_mysql(df_transformed, table_name="cleaned_data")

    # 📝 Save metadata
    log_metadata(source_info, transformation_steps, "cleaned_data")
