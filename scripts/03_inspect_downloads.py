import pandas as pd
import os

DOWNLOAD_DIR = "raw_data/pride_downloads"

def inspect_file(file_path):
    print(f"\n--- Inspecting {os.path.basename(os.path.dirname(file_path))} ---")
    try:
        # Read only header first to save memory
        df = pd.read_csv(file_path, sep='\t', nrows=5)
        print(f"Columns ({len(df.columns)}):")
        
        # Print interesting columns (Intensity, LFQ)
        intensity_cols = [c for c in df.columns if "Intensity" in c or "LFQ" in c]
        print(f"Intensity Columns found: {len(intensity_cols)}")
        print(intensity_cols) # Show ALL columns
        
        # Check for Gene names
        if "Gene names" in df.columns:
            print("Gene names column: Present")
        else:
            print("Gene names column: MISSING")
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def main():
    for project in os.listdir(DOWNLOAD_DIR):
        proj_dir = os.path.join(DOWNLOAD_DIR, project)
        if os.path.isdir(proj_dir):
            pg_file = os.path.join(proj_dir, "proteinGroups.txt")
            if os.path.exists(pg_file):
                inspect_file(pg_file)

if __name__ == "__main__":
    main()

