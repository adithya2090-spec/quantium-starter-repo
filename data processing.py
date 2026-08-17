import os
import glob
import pandas as pd

# Path to the folder containing the CSV files
DATA_DIR = "data"
OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "formatted_sales_data.csv")

def process_files():
    # Find all CSV files in the data directory
    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    
    if not csv_files:
        print(f"Error: No CSV files found in the '{DATA_DIR}' directory.")
        return

    print(f"Found {len(csv_files)} CSV files: {csv_files}")

    all_data = []

    for file in csv_files:
        try:
            df = pd.read_csv(file)
            
            # Standardize column names to lowercase and strip whitespace
            df.columns = df.columns.str.strip().str.lower()

            # Step 1: Keep only Pink Morsel rows (case-insensitive and stripping whitespace)
            df = df[df["product"].astype(str).str.strip().str.lower() == "pink morsel"]

            # Step 2: Clean price field (remove '$', commas, etc.) and compute sales
            df["price"] = (
                df["price"]
                .astype(str)
                .str.replace(r"[\$,]", "", regex=True)
                .astype(float)
            )
            df["quantity"] = df["quantity"].astype(float)
            df["sales"] = df["quantity"] * df["price"]

            # Step 3 & 4: Select required columns
            df = df[["sales", "date", "region"]]

            all_data.append(df)
            print(f"Successfully processed: {file}")
            
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    if not all_data:
        print("No matching 'Pink Morsel' data found across any files.")
        return

    # Combine all dataframes into one
    combined = pd.concat(all_data, ignore_index=True)

    # Convert date to datetime and sort chronologically
    combined["date"] = pd.to_datetime(combined["date"])
    combined = combined.sort_values("date").reset_index(drop=True)
    
    # Format date back to standard string format (YYYY-MM-DD)
    combined["date"] = combined["date"].dt.strftime("%Y-%m-%d")

    # Ensure output folder exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Save combined output
    combined.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved combined output to {OUTPUT_FILE}")
    print("\nPreview of combined data:")
    print(combined.head())

if __name__ == "__main__":
    process_files()