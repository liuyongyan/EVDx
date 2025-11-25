import pandas as pd
import requests
import gzip
import io
import os
import re

# Configuration
INPUT_META = "analysis_results/mirna/merged_mirna_metadata.csv"
OUTPUT_FILE = "analysis_results/mirna/sample_level_ground_truth.csv"
GEO_MATRIX_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series"

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_series_matrix_url(gse_id):
    stub = gse_id[:-3] + "nnn"
    return f"{GEO_MATRIX_URL}/{stub}/{gse_id}/matrix/{gse_id}_series_matrix.txt.gz"

def parse_series_matrix(gse_id):
    url = get_series_matrix_url(gse_id)
    print(f"Fetching metadata for {gse_id}...")
    
    try:
        r = requests.get(url)
        if r.status_code != 200:
            print(f"  Failed to fetch matrix: {r.status_code}")
            return {}
            
        # Decompress in memory
        with gzip.open(io.BytesIO(r.content), 'rt', encoding='latin-1') as f:
            lines = f.readlines()
            
        # Parse Sample Info
        sample_titles = []
        sample_geo_accessions = []
        sample_characteristics = [] # List of lists (ch1, ch2...)
        
        for line in lines:
            if line.startswith("!Sample_title"):
                sample_titles = line.strip().split('\t')[1:]
            elif line.startswith("!Sample_geo_accession"):
                sample_geo_accessions = line.strip().split('\t')[1:]
            elif line.startswith("!Sample_characteristics"):
                chars = line.strip().split('\t')[1:]
                sample_characteristics.append(chars)
                
        # Combine into a dictionary: {Sample_Title : "Char1; Char2..."}
        # Note: The column names in our CSV might match Sample_Title OR Sample_Geo_Accession
        # We need to support both map directions.
        
        meta_map = {}
        for i, title in enumerate(sample_titles):
            # Combine all characteristics lines for this sample
            char_text = "; ".join([row[i].strip('"') for row in sample_characteristics if i < len(row)])
            
            # Clean title (remove quotes)
            clean_title = title.strip('"')
            geo_acc = sample_geo_accessions[i].strip('"') if i < len(sample_geo_accessions) else ""
            
            # Store mapping for both Title and GSM ID
            full_text = f"{clean_title} {char_text}"
            meta_map[clean_title] = full_text
            if geo_acc:
                meta_map[geo_acc] = full_text
                
        return meta_map
        
    except Exception as e:
        print(f"  Error parsing matrix: {e}")
        return {}

def infer_condition(text):
    t = str(text).lower()
    
    # Control Logic
    if any(x in t for x in ['healthy', 'control', 'normal', 'non-tumor', 'non-cancer', 'volunteer', 'h.c.']):
        return "Healthy Control"
        
    # Disease Logic
    if "gastric cancer" in t: return "Gastric Cancer"
    if "lung cancer" in t or "nsclc" in t: return "Lung Cancer"
    if "breast cancer" in t: return "Breast Cancer"
    if "ovarian cancer" in t: return "Ovarian Cancer"
    if "parkinson" in t or "pd patient" in t: return "Parkinson's Disease"
    if "alzheimer" in t or "ad patient" in t: return "Alzheimer's Disease"
    if "multiple sclerosis" in t or "ms patient" in t: return "Multiple Sclerosis"
    if "sepsis" in t or "septic" in t: return "Sepsis"
    if "covid" in t or "sars-cov-2" in t: return "COVID-19"
    if "depression" in t or "mdd" in t: return "Depression"
    if "preterm" in t: return "Preterm Birth"
    if "diabetes" in t: return "Diabetes"
    
    # Generic Case
    if "patient" in t or "case" in t or "tumor" in t or "cancer" in t:
        return "Case (Unspecified)"
        
    return "Unknown"

def main():
    if not os.path.exists(INPUT_META):
        print("Metadata file not found.")
        return
        
    df = pd.read_csv(INPUT_META)
    gse_ids = df['Accession'].unique()
    
    print(f"Processing {len(gse_ids)} studies...")
    
    # 1. Build Master Map {Study -> {SampleName -> MetadataText}}
    study_maps = {}
    for gse in gse_ids:
        if gse.startswith("GSE"):
            study_maps[gse] = parse_series_matrix(gse)
            
    # 2. Apply to DataFrame
    new_conditions = []
    metadata_texts = []
    
    for index, row in df.iterrows():
        acc = row['Accession']
        sample_id = row['Original_Sample_ID'] # e.g. "Sample_1" or "GSM12345" or "GSE123_Sample1"
        
        # Clean sample_id to match keys (remove GSE prefix if added during normalization)
        # In 10_normalize_mirna.py we kept original name, but column was GSE_Sample.
        # Original_Sample_ID should be the raw name.
        
        # Attempt to find key
        meta_text = ""
        
        # Extract GSM ID from filename if present
        gsm_match = re.search(r"(GSM\d+)", sample_id)
        gsm_key = gsm_match.group(1) if gsm_match else None
        
        if acc in study_maps:
            mapping = study_maps[acc]
            
            # Priority 1: Exact Match
            if sample_id in mapping:
                meta_text = mapping[sample_id]
            # Priority 2: GSM ID Match (Most reliable)
            elif gsm_key and gsm_key in mapping:
                meta_text = mapping[gsm_key]
            # Priority 3: Partial match (Fallback)
            else:
                for key in mapping:
                    if key in sample_id or sample_id in key:
                        meta_text = mapping[key]
                        break
        
        metadata_texts.append(meta_text)
        
        # Infer
        if meta_text:
            cond = infer_condition(meta_text)
        else:
            cond = row['Condition'] # Fallback to previous logic
            
        new_conditions.append(cond)
        
    df['Sample_Metadata_Raw'] = metadata_texts
    df['Refined_Condition'] = new_conditions
    
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved Ground Truth to {OUTPUT_FILE}")
    print(df['Refined_Condition'].value_counts().head(20).to_markdown())

if __name__ == "__main__":
    main()
