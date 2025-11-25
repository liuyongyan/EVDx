import pandas as pd
import requests
import time
import re
import os

# Configuration
INPUT_FILE = "candidate_papers_for_review.csv"
OUTPUT_FILE = "candidate_papers_enriched.csv"
PRIDE_API_PROJECT = "https://www.ebi.ac.uk/pride/ws/archive/v2/projects"

def get_pride_metadata(accession):
    """Fetch detailed project metadata from PRIDE."""
    url = f"{PRIDE_API_PROJECT}/{accession}"
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return {}
        return r.json()
    except:
        return {}

def extract_disease_from_pride_json(data):
    """Extract disease from PRIDE JSON tags, keywords, or description."""
    
    # 1. Check explicit 'diseases' field
    diseases = data.get("diseases", [])
    disease_names = [d.get("name", "") for d in diseases]
    
    # Filter out "Disease" (too generic) or "Homo sapiens"
    valid_diseases = [d for d in disease_names if d.lower() not in ["disease", "homo sapiens"]]
    
    if valid_diseases:
        return "; ".join(valid_diseases)
        
    # 2. Check Keywords
    keywords = data.get("keywords", [])
    
    # 3. Check Description
    desc = data.get("projectDescription", "")
    title = data.get("title", "")
    
    full_text = f"{' '.join(keywords)} {title} {desc}".lower()
    
    if "alzheimer" in full_text: return "Alzheimer's Disease"
    if "ovarian" in full_text and "cancer" in full_text: return "Ovarian Cancer"
    if "parkinson" in full_text: return "Parkinson's Disease"
    if "lung" in full_text and "cancer" in full_text: return "Lung Cancer"
    if "liver" in full_text and "cancer" in full_text: return "Liver Cancer"
    if "hcc" in full_text: return "Liver Cancer"
    if "pancreatic" in full_text: return "Pancreatic Cancer"
    if "covid" in full_text or "sars-cov-2" in full_text: return "COVID-19"
    if "als" in full_text or "amyotrophic" in full_text: return "ALS"
    if "rheumatoid" in full_text: return "Rheumatoid Arthritis"
    if "sepsis" in full_text: return "Sepsis"
    if "breast" in full_text and "cancer" in full_text: return "Breast Cancer"
    
    return ""

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"{INPUT_FILE} not found.")
        return

    df = pd.read_csv(INPUT_FILE)
    print(f"Enriching {len(df)} PRIDE datasets...")
    
    enriched_labels = []
    
    for index, row in df.iterrows():
        acc = row['Accession']
        # Skip if we already have a good label (optional, but good to double check)
        
        print(f"Checking {acc}...")
        meta = get_pride_metadata(acc)
        disease = extract_disease_from_pride_json(meta)
        
        # Fallback to existing label if new one is empty
        if not disease and 'Proposed_Disease_Label' in row and "Unknown" not in str(row['Proposed_Disease_Label']):
             disease = row['Proposed_Disease_Label']
             
        enriched_labels.append(disease)
        time.sleep(0.2)
        
    df['Enriched_Disease'] = enriched_labels
    
    # Save
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved enriched list to {OUTPUT_FILE}")
    print(df[['Accession', 'Enriched_Disease']].head(15).to_markdown(index=False))

if __name__ == "__main__":
    main()
