import pandas as pd
import numpy as np
import os
import gzip

# Configuration
RAW_DIR = "raw_data/geo_downloads"
METADATA_FILE = "geo_mirna_candidates_enriched.csv"
OUTPUT_DIR = "analysis_results/mirna"

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_study_metadata():
    if os.path.exists(METADATA_FILE):
        return pd.read_csv(METADATA_FILE).set_index("GEO_ID")["Inferred_Disease"].to_dict()
    return {}

def load_count_matrix(file_path):
    """
    Load a count matrix from various formats (csv, tsv, txt, xlsx, gz).
    """
    try:
        lower_path = file_path.lower()
        
        if lower_path.endswith('.xlsx') or lower_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        elif lower_path.endswith('.csv') or lower_path.endswith('.csv.gz'):
            df = pd.read_csv(file_path)
        else:
            # Try tab then whitespace for txt/tsv
            try:
                df = pd.read_csv(file_path, sep='\t')
                if df.shape[1] < 2: # If only 1 col, maybe whitespace
                    df = pd.read_csv(file_path, sep=r'\s+')
            except:
                df = pd.read_csv(file_path, sep=r'\s+')
                
        return df
    except Exception as e:
        print(f"  Error loading {os.path.basename(file_path)}: {e}")
        return None

def clean_mirna_id(id_str):
    """
    Standardize miRNA ID to 'hsa-mir-X'.
    - Handle pipe-separated IDs (e.g. "seq|let-7a|...") by extracting the name.
    - Lowercase
    - Remove 'hsa-', 'mir-', 'miR-' prefix variations
    - Re-add standard 'hsa-mir-' prefix
    """
    s = str(id_str).lower()
    
    # Handle pipes (isomiR annotations)
    if "|" in s:
        parts = s.split("|")
        found_name = None
        # Look for the part that is the name (has 'let' or 'mir' but isn't just the prefix)
        for p in parts:
            if ("let" in p or "mir" in p) and not (p == "hsa" or p == "mir"):
                found_name = p
                break
        if found_name:
            s = found_name
            
    # Remove existing prefixes
    s = s.replace('hsa-', '').replace('mir-', '').replace('mirna-', '')
    return f"hsa-mir-{s}"

def standardize_mirna_matrix(df, gse_id, disease_label):
    """
    Standardize a raw count matrix:
    1. Identify miRNA column (rows)
    2. Identify Sample columns
    3. Log2 transform (pseudo-count + 1)
    """
    # 1. Find miRNA ID column
    # Look for 'miRNA', 'ID', 'Name', or first column if string
    id_col = None
    for col in df.columns:
        if any(kw in str(col).lower() for kw in ['mirna', 'id', 'name', 'feature']):
            id_col = col
            break
    
    if not id_col:
        # Assume first column is ID
        id_col = df.columns[0]
        
    # --- FILTERING STEP ---
    # Remove GO terms, KEGG, etc. (rows with ':')
    # Check if column contains strings first
    if df[id_col].dtype == object:
        df = df[~df[id_col].str.contains(':', na=False)]
    # ----------------------
    
    # Set ID as index
    df = df.set_index(id_col)
    
    # --- HARMONIZATION STEP ---
    # Clean index values
    df.index = df.index.map(clean_mirna_id)
    # --------------------------
    
    # 2. Filter non-numeric columns (metadata)
    # Keep only numeric columns (counts)
    numeric_df = df.select_dtypes(include=[np.number])
    
    if numeric_df.shape[1] == 0:
        print(f"  No numeric columns found in {gse_id}")
        return None, None
        
    # Aggregate duplicates (Sum counts for same miRNA ID)
    if not numeric_df.index.is_unique:
        print(f"  Aggregating duplicate IDs in {gse_id}")
        numeric_df = numeric_df.groupby(level=0).sum()
        
    # 3. Normalize (Log2 CPM-ish)
    # Simple normalization: log2(x + 1)
    # ideally we should do TMM/DESeq2 size factors, but for a first pass log2 is okay
    # Check if already normalized (presence of floats or log-like values)
    is_integers = (numeric_df.fillna(0) % 1  == 0).all().all()
    max_val = numeric_df.max().max()
    
    norm_df = numeric_df.copy()
    
    if is_integers and max_val > 100: # Likely Raw Counts
        # Convert to CPM (Counts Per Million) first to handle library size diffs
        library_sizes = numeric_df.sum()
        norm_df = (numeric_df.div(library_sizes) * 1e6)
        norm_df = np.log2(norm_df + 1)
    elif max_val < 50: # Likely already Log2
        pass # Keep as is
    else: # Likely TPM/FPKM (Floats > 50)
        norm_df = np.log2(norm_df + 1)
        
    # 4. Create Metadata
    metadata = []
    for sample in norm_df.columns:
        global_id = f"{gse_id}_{sample}"
        
        # Infer Control vs Case
        cond = "Case"
        if any(x in str(sample).lower() for x in ['control', 'ctrl', 'healthy', 'norm', 'hc']):
            cond = "Healthy Control"
        elif disease_label:
            cond = disease_label
            
        metadata.append({
            "Global_ID": global_id,
            "Accession": gse_id,
            "Original_Sample_ID": sample,
            "Condition": cond,
            "Biofluid": "Serum/Plasma (inferred)"
        })
        
    # Rename columns to Global ID
    norm_df.columns = [f"{gse_id}_{c}" for c in norm_df.columns]
    
    return norm_df, metadata

def main():
    ensure_dir(OUTPUT_DIR)
    study_map = load_study_metadata()
    
    all_dfs = []
    all_metadata = []
    
    projects = [d for d in os.listdir(RAW_DIR) if os.path.isdir(os.path.join(RAW_DIR, d))]
    print(f"Found {len(projects)} GEO datasets.")
    
    for proj in projects:
        print(f"Processing {proj}...")
        proj_dir = os.path.join(RAW_DIR, proj)
        files = [f for f in os.listdir(proj_dir) if not f.startswith('.')]
        
        # Find the best file (prefer "normalized" or "counts" or "matrix")
        # Priority: *matrix* > *count* > *normalized*
        target_file = None
        
        # Filter for count/matrix files
        candidates = [f for f in files if "count" in f.lower() or "matrix" in f.lower() or "raw" in f.lower()]
        
        if not candidates:
            # Fallback to any text/csv file
            candidates = [f for f in files if f.endswith('txt.gz') or f.endswith('csv.gz') or f.endswith('.xlsx')]
            
        if candidates:
            # Pick the largest file (likely the full matrix)
            # Just pick the first one for now
            target_file = candidates[0]
            
        if target_file:
            fpath = os.path.join(proj_dir, target_file)
            print(f"  Using {target_file}")
            disease = study_map.get(proj, "Unknown")
            
            raw_df = load_count_matrix(fpath)
            if raw_df is not None:
                norm_df, meta = standardize_mirna_matrix(raw_df, proj, disease)
                if norm_df is not None:
                    all_dfs.append(norm_df)
                    all_metadata.extend(meta)
        else:
            print(f"  No suitable data file found in {proj}")

    if not all_dfs:
        print("No valid miRNA data processed.")
        return

    print("\nMerging all miRNA datasets...")
    # Outer join on index (miRNA IDs)
    # Warning: miRNA IDs might be mismatched (hsa-miR-21 vs hsa-miR-21-5p)
    # This simple merge assumes exact string match. Ideally we'd map to miRBase.
    master_matrix = pd.concat(all_dfs, axis=1, join='outer')
    
    # Save Matrix
    matrix_path = os.path.join(OUTPUT_DIR, "merged_mirna_matrix_log2.csv")
    master_matrix.to_csv(matrix_path)
    print(f"Saved Matrix: {matrix_path}")
    print(f"  Dimensions: {master_matrix.shape}")
    
    # Save Metadata
    meta_df = pd.DataFrame(all_metadata)
    meta_path = os.path.join(OUTPUT_DIR, "merged_mirna_metadata.csv")
    meta_df.to_csv(meta_path, index=False)
    print(f"Saved Metadata: {meta_path}")
    print(f"  Samples: {len(meta_df)}")
    print("\nSample Counts by Condition:")
    print(meta_df['Condition'].value_counts().to_markdown())

if __name__ == "__main__":
    main()
