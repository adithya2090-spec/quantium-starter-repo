import os
import glob
import pandas as pd

DATA_DIR = "data"
OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "formatted_sales_data.csv")

def process_files():
    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    
    if not csv_files:
        print(f"Error: No CSV files found in the '{DATA_DIR}' directory.")
        return

    all_data = []

    for file in csv_files:
        try:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip().str.lower()

            # Keep only Pink Morsel rows
            df = df[df["product"].astype(str).str.strip().str.lower() == "pink morsel"]

            # Clean price and calculate sales
            df["price"] = (
                df["price"]
                .astype(str)
                .str.replace(r"[\$,]", "", regex=True)
                .astype(float)
            )
            df["quantity"] = df["quantity"].astype(float)
            df["sales"] = df["quantity"] * df["price"]

            df = df[["sales", "date", "region"]]
            all_data.append(df)
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    if not all_data:
        print("No matching 'Pink Morsel' data found.")
        return

    combined = pd.concat(all_data, ignore_index=True)
    combined["date"] = pd.to_datetime(combined["date"])
    combined = combined.sort_values("date").reset_index(drop=True)
    combined["date"] = combined["date"].dt.strftime("%Y-%m-%d")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    combined.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved combined output to {OUTPUT_FILE}")

if __name__ == "__main__":
    process_files()