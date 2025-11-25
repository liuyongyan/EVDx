import pandas as pd
import requests
import time
import re
import os

# Configuration
INPUT_FILE = "geo_mirna_candidates.csv"
OUTPUT_FILE = "geo_mirna_candidates_enriched.csv"
GEO_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
GEO_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def get_samples_for_series(gse_id):
    """Find GSM (Sample) IDs for a GSE Series."""
    params = {
        "db": "gds",
        "term": f"{gse_id}[Accession] AND gse_gsm[Filter]",
        "retmax": 5, # We only need a few to check metadata
        "retmode": "json"
    }
    try:
        r = requests.get(GEO_ESEARCH, params=params)
        data = r.json()
        return data.get("esearchresult", {}).get("idlist", [])
    except:
        return []

def get_sample_metadata(gsm_db_ids):
    """Fetch metadata for sample IDs (internal GDS IDs)."""
    if not gsm_db_ids:
        return ""
        
    params = {
        "db": "gds",
        "id": ",".join(gsm_db_ids),
        "retmode": "json"
    }
    try:
        r = requests.get(GEO_ESUMMARY, params=params)
        data = r.json()
        result_dict = data.get("result", {})
        
        # Extract characteristics
        all_chars = set()
        for uid in gsm_db_ids:
            if uid in result_dict:
                summary = result_dict[uid].get("summary", "")
                title = result_dict[uid].get("title", "")
                
                # Try to find "diagnosis: ... " or "disease: ..."
                # GEO often puts this in the 'summary' text for samples
                all_chars.add(title)
                all_chars.add(summary)
                
        return "; ".join(list(all_chars))[:500] # Truncate
    except:
        return ""

def infer_disease_from_text(text):
    text = str(text).lower()
    if "healthy" in text or "control" in text or "normal" in text:
        if "cancer" in text or "tumor" in text or "carcinoma" in text:
            # Check for specific cancers
            if "ovarian" in text: return "Ovarian Cancer"
            if "lung" in text: return "Lung Cancer"
            if "liver" in text or "hcc" in text: return "Liver Cancer"
            if "gastric" in text: return "Gastric Cancer"
            if "breast" in text: return "Breast Cancer"
            if "pancreatic" in text: return "Pancreatic Cancer"
            if "parkinson" in text: return "Parkinson's Disease"
            return "Cancer (Unspecified)"
    
    if "parkinson" in text: return "Parkinson's Disease"
    if "alzheimer" in text: return "Alzheimer's Disease"
    if "sepsis" in text: return "Sepsis"
    if "covid" in text or "sars" in text: return "COVID-19"
    
    return ""

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"{INPUT_FILE} not found.")
        return

    df = pd.read_csv(INPUT_FILE)
    print(f"Enriching {len(df)} GEO datasets...")
    
    enriched_labels = []
    metadata_snippets = []
    
    for index, row in df.iterrows():
        gse_id = row['GEO_ID']
        print(f"Checking {gse_id}...")
        
        # 1. Get Samples
        gsm_ids = get_samples_for_series(gse_id)
        
        # 2. Get Metadata
        meta = get_sample_metadata(gsm_ids)
        metadata_snippets.append(meta)
        
        # 3. Infer
        # Combine Title and Metadata for inference
        full_text = f"{row['Title']} {meta}"
        disease = infer_disease_from_text(full_text)
        enriched_labels.append(disease)
        
        time.sleep(0.5) # Rate limit
        
    df['Inferred_Disease'] = enriched_labels
    df['Sample_Metadata_Snippet'] = metadata_snippets
    
    # Move Inferred Disease to front
    cols = ['GEO_ID', 'Inferred_Disease', 'Title', 'Sample_Count', 'Sample_Metadata_Snippet']
    df = df[cols]
    
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved enriched list to {OUTPUT_FILE}")
    print(df[['GEO_ID', 'Inferred_Disease']].head(15).to_markdown(index=False))

if __name__ == "__main__":
    main()
