import pandas as pd
import os

# Configuration
ANALYSIS_DIR = "analysis_results"

def revert_to_csv(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".parquet"):
                parquet_path = os.path.join(root, file)
                csv_path = parquet_path.replace(".parquet", ".csv")
                
                print(f"Reverting {parquet_path}...")
                try:
                    df = pd.read_parquet(parquet_path)
                    
                    # Save as CSV
                    df.to_csv(csv_path)
                    
                    print(f"  Done. Saved to {csv_path}")
                    
                    # Remove Parquet
                    os.remove(parquet_path)
                    print(f"  Removed Parquet file.")
                    
                except Exception as e:
                    print(f"  Error converting {file}: {e}")

if __name__ == "__main__":
    revert_to_csv(ANALYSIS_DIR)
