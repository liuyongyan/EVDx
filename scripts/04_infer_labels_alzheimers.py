import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Configuration
FILE_PATH = "raw_data/pride_downloads/PXD024216/proteinGroups.txt"
OUTPUT_DIR = "analysis_results/PXD024216"
MARKERS = ["ORM2", "RBP4", "HYDIN", "FXIIIA1", "FXIIIB"] # Markers mentioned in description

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    ensure_dir(OUTPUT_DIR)
    print(f"Loading {FILE_PATH}...")
    
    # Load data
    df = pd.read_csv(FILE_PATH, sep='\t')
    
    # Filter for markers
    # Gene names are often separated by semicolon
    marker_rows = df[df['Gene names'].apply(lambda x: any(m in str(x).split(';') for m in MARKERS) if pd.notnull(x) else False)]
    
    if marker_rows.empty:
        print("No marker proteins found!")
        return

    print(f"Found {len(marker_rows)} marker rows.")
    
    # Extract LFQ intensities
    lfq_cols = [c for c in df.columns if "LFQ intensity EV" in c]
    print(f"Found {len(lfq_cols)} sample columns.")
    
    # Create a small matrix for markers
    marker_data = marker_rows[['Gene names'] + lfq_cols].copy()
    marker_data.set_index('Gene names', inplace=True)
    
    # Transpose: Samples as rows, Proteins as columns
    X = marker_data.T
    
    # Clean sample names (LFQ intensity EV1_1 -> EV1)
    # Since we have replicates (_1, _2), we should average them or treat them separately
    # Let's average technical replicates first
    
    sample_ids = sorted(list(set([c.split('_')[0].replace('LFQ intensity ', '') for c in lfq_cols])))
    print(f"Unique Subjects: {len(sample_ids)}") # Should be 29 or 30
    
    X_averaged = pd.DataFrame(index=sample_ids, columns=marker_data.index)
    
    for subject in sample_ids:
        # Find cols for this subject
        subj_cols = [c for c in lfq_cols if f"LFQ intensity {subject}_" in c]
        if not subj_cols: 
            continue
            
        # Average
        vals = marker_data[subj_cols].replace(0, np.nan).mean(axis=1)
        X_averaged.loc[subject] = vals
        
    # Log transform (important for proteomics)
    X_log = np.log2(X_averaged.astype(float).fillna(0) + 1)
    
    print("\nMarker Intensities (Log2):")
    print(X_log)
    
    # Clustering
    # We expect 3 groups: AD (10), MCI (10), Control (9) = 29 total
    # Or just AD vs Control.
    # The description says ORM2/RBP4 are elevated in AD.
    
    # Let's try K-Means with k=2 (AD vs Non-AD) or k=3
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(X_log)
    
    X_log['Cluster'] = clusters
    
    # Sort by ORM2 intensity to see which cluster is high
    # ORM2 gene name might be "ORM2" or "ORM2;ORM1"
    orm2_col = [c for c in X_log.columns if "ORM2" in c][0]
    
    X_log_sorted = X_log.sort_values(by=orm2_col, ascending=False)
    
    print("\nSamples sorted by ORM2 intensity (High = Probable AD):")
    print(X_log_sorted[[orm2_col, 'Cluster']])
    
    # Save inference
    X_log_sorted.to_csv(f"{OUTPUT_DIR}/inferred_labels.csv")
    print(f"\nInferred labels saved to {OUTPUT_DIR}/inferred_labels.csv")

if __name__ == "__main__":
    main()
