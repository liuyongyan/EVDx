import pandas as pd
import os

FILE = "analysis_results/mirna/merged_mirna_matrix_log2.csv"

def check_junk():
    print(f"Loading {FILE}...")
    # Load just the first column to filter, then load specific rows if needed
    # Actually, loading the whole thing is fast enough (~100MB)
    df = pd.read_csv(FILE, index_col=0)
    
    print(f"Total Rows: {len(df)}")
    
    # Identify Junk Rows
    # Criteria: Long strings, pipes, non-standard prefixes
    junk_rows = []
    for idx in df.index:
        s = str(idx)
        if "|" in s or len(s) > 30 or "val" in s or "tyr" in s:
            junk_rows.append(idx)
            
    print(f"Potential Junk Rows: {len(junk_rows)}")
    
    if not junk_rows:
        return

    # Check Sparsity
    # Count non-NaN values for these rows
    junk_df = df.loc[junk_rows]
    non_null_counts = junk_df.notna().sum(axis=1)
    
    print("\n--- Junk Analysis (Top 20 by Sample Count) ---")
    print("Row ID | Samples with Data | % of Total Samples")
    print("-" * 60)
    
    sorted_junk = non_null_counts.sort_values(ascending=False).head(20)
    
    for idx, count in sorted_junk.items():
        pct = (count / df.shape[1]) * 100
        print(f"{idx[:40]}... | {count} | {pct:.2f}%")

if __name__ == "__main__":
    check_junk()
