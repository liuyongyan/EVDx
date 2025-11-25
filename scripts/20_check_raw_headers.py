import pandas as pd
import os

FILES = [
    "raw_data/pride_downloads/PXD036491/proteinGroups.txt"
]

def check_headers():
    for f in FILES:
        print(f"\n--- {f} ---")
        try:
            # Read only header
            df = pd.read_csv(f, sep='\t', nrows=0)
            cols = [c for c in df.columns if "Intensity" in c or "LFQ" in c]
            print(cols) # Show ALL columns
        except Exception as e:
            print(e)

if __name__ == "__main__":
    check_headers()

