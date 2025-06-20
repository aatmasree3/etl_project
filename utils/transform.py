import pandas as pd
from datetime import datetime

transformation_steps = []

def infer_schema(data):
    """Infer schema from pandas DataFrame"""
    if isinstance(data, pd.DataFrame):
        return {col: str(data[col].dtype) for col in data.columns}
    else:
        # Fallback for non-DataFrame data
        sample = data[0] if isinstance(data, list) else data
        return {k: type(v).__name__ for k, v in sample.items()}

def transform_data(data):
    print("🔧 Received raw data in transform:")
    print(data.head())
    print("Data type:", type(data))
    print("Shape:", data.shape)
    
    global transformation_steps
    
    # If data is already a DataFrame, use it directly
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        # Convert to DataFrame if it's not already
        df = pd.json_normalize(data)
    
    print("\n📋 Available columns:", list(df.columns))

    while True:
        print("\n🔧 Choose a transformation:")
        print("1. Convert column type (int, float, str)")
        print("2. Rename a column")
        print("3. Drop missing, blank, or null rows")
        print("4. Remove duplicate rows")
        print("5. Fill missing values (default, mean, min, max)")
        print("6. Convert string column to datetime with format")
        print("7. Remove selected columns")
        print("8. Done")

        choice = input("Enter choice number: ").strip()

        # 1. Type Conversion
        if choice == '1':
            col = input("Enter column name: ")
            if col not in df.columns:
                print("⚠️ Column not found.")
                continue
            dtype = input("Convert to (int/float/str): ").strip()
            try:
                if dtype == 'int':
                    df[col] = df[col].astype(int)
                elif dtype == 'float':
                    df[col] = df[col].astype(float)
                elif dtype == 'str':
                    df[col] = df[col].astype(str)
                else:
                    print("⚠️ Unsupported type.")
                    continue
                transformation_steps.append(f"{col} → {dtype}")
                print(f"✅ Converted {col} to {dtype}.")
            except Exception as e:
                print("❌ Conversion failed:", e)

        # 2. Rename column
        elif choice == '2':
            old_col = input("Enter current column name: ")
            new_col = input("Enter new column name: ")
            if old_col in df.columns:
                df.rename(columns={old_col: new_col}, inplace=True)
                transformation_steps.append(f"{old_col} → {new_col}")
                print(f"✅ Renamed {old_col} to {new_col}.")
            else:
                print("⚠️ Column not found.")

        # 3. Drop missing or blank
        elif choice == '3':
            df.replace('', pd.NA, inplace=True)
            df.dropna(inplace=True)
            transformation_steps.append("drop missing/blank/null rows")
            print("✅ Dropped rows with missing/blank/null values.")

        # 4. Remove duplicates
        elif choice == '4':
            before = len(df)
            df.drop_duplicates(inplace=True)
            after = len(df)
            transformation_steps.append("remove duplicate rows")
            print(f"✅ Removed {before - after} duplicate rows.")

        # 5. Fill missing values
        elif choice == '5':
            col = input("Enter column to fill missing values in: ")
            if col not in df.columns:
                print("⚠️ Column not found.")
                continue
            method = input("Method (default/mean/min/max): ").lower()
            if method == "default":
                val = input("Enter default value: ")
                df[col].fillna(val, inplace=True)
                transformation_steps.append(f"{col} → fillna('{val}')")
            elif method == "mean":
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col].fillna(df[col].mean(), inplace=True)
                transformation_steps.append(f"{col} → fillna(mean)")
            elif method == "min":
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col].fillna(df[col].min(), inplace=True)
                transformation_steps.append(f"{col} → fillna(min)")
            elif method == "max":
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col].fillna(df[col].max(), inplace=True)
                transformation_steps.append(f"{col} → fillna(max)")
            else:
                print("⚠️ Invalid method.")
                continue
            print(f"✅ Filled missing values in {col} using {method}.")

        # 6. Convert string to datetime
        elif choice == '6':
            col = input("Enter column to convert to datetime: ")
            fmt = input("Enter date format (e.g., %Y-%m-%d): ")
            try:
                df[col] = pd.to_datetime(df[col], format=fmt, errors='coerce')
                transformation_steps.append(f"{col} → datetime('{fmt}')")
                print(f"✅ Converted {col} to datetime using format {fmt}.")
            except Exception as e:
                print("❌ Date conversion failed:", e)

        # 7. Remove columns
        elif choice == '7':
            cols = input("Enter column names to remove (comma-separated): ").split(',')
            cols = [c.strip() for c in cols if c.strip() in df.columns]
            df.drop(columns=cols, inplace=True)
            transformation_steps.append(f"Removed columns: {', '.join(cols)}")
            print(f"✅ Removed columns: {cols}")

        elif choice == '8':
            print("🛑 Transformation complete.")
            break

        else:
            print("❌ Invalid option. Try again.")

    print("✅ Transformed data:")
    print(df.head())
    print("Final shape:", df.shape)

    return df
