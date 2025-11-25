import pandas as pd
import re

FILE = "analysis_results/mirna/merged_mirna_matrix_log2.csv"

def check_sequences():
    print(f"Loading {FILE}...")
    df = pd.read_csv(FILE, index_col=0)
    
    # Check for Sequence-like IDs
    # (Only A, C, G, T, U, length > 15)
    seq_pattern = re.compile(r'^[ACGTUacgtu]{15,}$')
    
    seq_rows = []
    for idx in df.index:
        s = str(idx)
        # Skip if it has 'mir' or 'let' (already named)
        if "mir" in s or "let" in s:
            continue
            
        if seq_pattern.match(s):
            seq_rows.append(idx)
            
    print(f"Found {len(seq_rows)} rows that look like raw sequences.")
    
    if seq_rows:
        # Check sparsity
        seq_df = df.loc[seq_rows]
        counts = seq_df.notna().sum(axis=1).sort_values(ascending=False)
        
        print("\n--- Top Sequence Features ---")
        print(counts.head(10))

if __name__ == "__main__":
    check_sequences()
