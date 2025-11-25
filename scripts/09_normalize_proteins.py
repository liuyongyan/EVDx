import pandas as pd
import numpy as np
import os
import re

# Configuration
RAW_DIR = "raw_data/pride_downloads"
METADATA_FILE = "candidate_papers_enriched.csv"
OUTPUT_DIR = "analysis_results/proteomics"
MIN_PROTEINS = 100 # Minimum proteins detected to keep a sample

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_study_metadata():
    """Load the enriched study-level metadata."""
    if os.path.exists(METADATA_FILE):
        return pd.read_csv(METADATA_FILE).set_index("Accession")["Enriched_Disease"].to_dict()
    return {}

def infer_sample_type(sample_name, study_disease):
    """
    Infer if a sample is Case or Control based on its name.
    sample_name: e.g., "EV_Control_01", "Cancer_02"
    study_disease: e.g., "Ovarian Cancer"
    """
    s = sample_name.lower()
    
    # Control keywords
    if any(x in s for x in ['control', 'ctrl', 'healthy', 'norm', 'hc_', '_hc', 'non-disease']):
        return "Healthy Control"
    
    # If not control, assume it's the study disease
    # (Unless it's a technical replicate pool, standard, etc.)
    if any(x in s for x in ['pool', 'standard', 'ref']):
        return "Technical Control"
        
    if pd.isna(study_disease) or study_disease == "":
        return "Case (Unknown Disease)"
        
    return study_disease

def process_maxquant_file(accession, folder_path, study_disease):
    """Process a single proteinGroups.txt file."""
    file_path = os.path.join(folder_path, "proteinGroups.txt")
    if not os.path.exists(file_path):
        return None, None

    print(f"Processing {accession}...")
    
    try:
        # Load data (only necessary columns to save memory)
        # We need: Protein names, Gene names, Potential contaminant, Reverse, LFQ intensity *
        df = pd.read_csv(file_path, sep='\t', low_memory=False)
    except Exception as e:
        print(f"  Error reading file: {e}")
        return None, None

    # 1. Standard Filtering (MaxQuant)
    # Remove Contaminants, Reverse, Only identified by site
    if 'Potential contaminant' in df.columns:
        df = df[df['Potential contaminant'] != '+']
    if 'Reverse' in df.columns:
        df = df[df['Reverse'] != '+']
    if 'Only identified by site' in df.columns:
        df = df[df['Only identified by site'] != '+']

    # 2. Feature Selection (Gene Names)
    # Handle variations in column naming
    gene_col = None
    for col in df.columns:
        if col.lower() in ['gene names', 'genenames', 'gene_names', 'genes']:
            gene_col = col
            break
            
    protein_col = None
    for col in df.columns:
        if col.lower() in ['majority protein ids', 'majority protein id', 'protein ids']:
            protein_col = col
            break
            
    if gene_col:
        df['Feature_ID'] = df[gene_col]
        if protein_col:
            df['Feature_ID'] = df['Feature_ID'].fillna(df[protein_col])
    elif protein_col:
        print(f"  Warning: No Gene Name column found. Using {protein_col}.")
        df['Feature_ID'] = df[protein_col]
    else:
        print("  Error: No ID column found (Gene names/Protein IDs). Skipping.")
        return None, None
        
    df['Feature_ID'] = df['Feature_ID'].fillna('Unknown')
    
    # Handle duplicates: Group by Feature_ID and take the one with highest total intensity, or sum?
    # Standard approach: Take entry with most peptides, or sum intensities. 
    # Let's keep it simple: Group by Feature_ID and sum.
    
    # 3. Extract LFQ Columns
    lfq_cols = [c for c in df.columns if c.startswith("LFQ intensity ")]
    if not lfq_cols:
        print(f"  No LFQ columns found in {accession}. Checking 'Intensity' columns...")
        lfq_cols = [c for c in df.columns if c.startswith("Intensity ") and c != "Intensity"]
        
    if not lfq_cols:
        print(f"  Skipping {accession}: No intensity data found.")
        return None, None

    # Create metadata for these samples
    metadata_rows = []
    cleaned_data = {} # {SampleID: {Gene: Intensity}}
    
    # Aggregate duplicates first
    # We only care about Feature_ID and lfq_cols
    subset = df[['Feature_ID'] + lfq_cols].copy()
    # Convert to numeric, force errors to NaN
    for c in lfq_cols:
        subset[c] = pd.to_numeric(subset[c], errors='coerce')
        
    # Group by Gene and Sum (handling isoforms mapped to same gene)
    grouped = subset.groupby('Feature_ID').sum()
    
    # Log2 Transform (x+1)
    grouped = np.log2(grouped + 1)
    
    # Filter low quality samples (columns)
    valid_samples = []
    for col in grouped.columns:
        # clean column name: "LFQ intensity Sample1" -> "Sample1"
        original_sample_name = col.replace("LFQ intensity ", "").replace("Intensity ", "")
        
        # Check non-zero count
        n_proteins = (grouped[col] > 0).sum()
        if n_proteins < MIN_PROTEINS:
            continue
            
        global_id = f"{accession}_{original_sample_name}"
        
        # Infer Label
        label = infer_sample_type(original_sample_name, study_disease)
        
        metadata_rows.append({
            "Global_ID": global_id,
            "Accession": accession,
            "Original_Sample_ID": original_sample_name,
            "Condition": label,
            "Proteins_Detected": n_proteins,
            "Batch": accession # Study ID as Batch
        })
        
        # Store data with Global ID
        cleaned_data[global_id] = grouped[col]
        valid_samples.append(global_id)

    if not cleaned_data:
        return None, None

    # Convert to DataFrame
    final_df = pd.DataFrame(cleaned_data)
    return final_df, metadata_rows

def main():
    ensure_dir(OUTPUT_DIR)
    study_map = load_study_metadata()
    
    all_dfs = []
    all_metadata = []
    
    projects = [d for d in os.listdir(RAW_DIR) if os.path.isdir(os.path.join(RAW_DIR, d))]
    print(f"Found {len(projects)} datasets to process.")
    
    for proj in projects:
        disease = study_map.get(proj, "Unknown")
        df, meta = process_maxquant_file(proj, os.path.join(RAW_DIR, proj), disease)
        
        if df is not None and not df.empty:
            all_dfs.append(df)
            all_metadata.extend(meta)
            
    if not all_dfs:
        print("No valid data processed.")
        return

    print("\nMerging all datasets...")
    # Outer join on index (Gene Names)
    master_matrix = pd.concat(all_dfs, axis=1, join='outer')
    
    # Save Matrix
    matrix_path = os.path.join(OUTPUT_DIR, "merged_protein_matrix_log2.csv")
    master_matrix.to_csv(matrix_path)
    print(f"Saved Matrix: {matrix_path}")
    print(f"  Dimensions: {master_matrix.shape}")
    
    # Save Metadata
    meta_df = pd.DataFrame(all_metadata)
    meta_path = os.path.join(OUTPUT_DIR, "merged_metadata.csv")
    meta_df.to_csv(meta_path, index=False)
    print(f"Saved Metadata: {meta_path}")
    print(f"  Samples: {len(meta_df)}")
    print("\nSample Counts by Condition:")
    print(meta_df['Condition'].value_counts().to_markdown())

if __name__ == "__main__":
    main()
