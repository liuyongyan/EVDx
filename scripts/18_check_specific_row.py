import pandas as pd

FILE = "analysis_results/mirna/merged_mirna_matrix_log2.csv"
TARGET_ROW = "hsa-mir-1"

def check_specific_row():
    print(f"Loading {FILE}...")
    df = pd.read_csv(FILE, index_col=0)
    
    if TARGET_ROW not in df.index:
        print(f"{TARGET_ROW} not found.")
        return
        
    row_data = df.loc[TARGET_ROW]
    
    # Count non-nulls
    non_null_count = row_data.notna().sum()
    total_cols = len(df.columns)
    
    print(f"\nRow: {TARGET_ROW}")
    print(f"Non-null values: {non_null_count} / {total_cols} ({non_null_count/total_cols:.1%})")
    
    # Which datasets have it?
    # We assume column names are GSE_Sample
    datasets = set([c.split('_')[0] for c in row_data.dropna().index])
    
    print("\nDatasets containing this miRNA:")
    print(", ".join(sorted(list(datasets))))

if __name__ == "__main__":
    check_specific_row()
