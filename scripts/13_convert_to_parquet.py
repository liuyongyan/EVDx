import pandas as pd
import os

# Configuration
ANALYSIS_DIR = "analysis_results"

def convert_to_parquet(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv") and "matrix" in file:
                csv_path = os.path.join(root, file)
                parquet_path = csv_path.replace(".csv", ".parquet")
                
                print(f"Converting {csv_path}...")
                try:
                    df = pd.read_csv(csv_path, index_col=0)
                    
                    # Ensure index name is string (Parquet requirement sometimes)
                    df.index = df.index.map(str)
                    
                    # Save as Parquet (Snappy compression is default and good)
                    df.to_parquet(parquet_path)
                    
                    # Check size
                    csv_size = os.path.getsize(csv_path) / (1024*1024)
                    pq_size = os.path.getsize(parquet_path) / (1024*1024)
                    
                    print(f"  Done. CSV: {csv_size:.2f} MB -> Parquet: {pq_size:.2f} MB")
                    
                    # Remove CSV if successful
                    os.remove(csv_path)
                    print(f"  Removed original CSV.")
                    
                except Exception as e:
                    print(f"  Error converting {file}: {e}")

if __name__ == "__main__":
    convert_to_parquet(ANALYSIS_DIR)
