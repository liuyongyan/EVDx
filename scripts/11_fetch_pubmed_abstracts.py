import pandas as pd
import requests
import time
import os
import re

# Configuration
PRIDE_CSV = "candidate_papers_enriched.csv"
GEO_CSV = "geo_mirna_candidates_enriched.csv"
OUTPUT_PRIDE = "candidate_papers_final.csv"
OUTPUT_GEO = "geo_mirna_candidates_final.csv"

NCBI_API_KEY = "" # Leave empty or add if available
EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def search_pubmed_id(title):
    """Search PubMed for a paper title to get the PMID."""
    url = f"{EUTILS_BASE}/esearch.fcgi"
    clean_title = re.sub(r'[^\w\s]', '', title) # Remove punctuation
    params = {
        "db": "pubmed",
        "term": f"{clean_title}[Title]",
        "retmode": "json",
        "api_key": NCBI_API_KEY
    }
    try:
        r = requests.get(url, params=params)
        data = r.json()
        ids = data.get("esearchresult", {}).get("idlist", [])
        if ids:
            return ids[0]
    except:
        pass
    return None

def fetch_abstract(pmid):
    """Fetch abstract text for a PMID."""
    if not pmid: return ""
    
    url = f"{EUTILS_BASE}/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml",
        "api_key": NCBI_API_KEY
    }
    try:
        r = requests.get(url, params=params)
        text = r.text
        # Simple regex extract for AbstractText
        # <AbstractText>...</AbstractText>
        matches = re.findall(r'<AbstractText.*?>(.*?)</AbstractText>', text, re.DOTALL)
        if matches:
            return " ".join(matches)
    except:
        pass
    return ""

def infer_disease_from_text(text):
    """Expanded disease inference logic."""
    t = str(text).lower()
    
    # Mapping rules (Priority order)
    rules = [
        ("Alzheimer", "Alzheimer's Disease"),
        ("Parkinson", "Parkinson's Disease"),
        ("Amyotrophic lateral sclerosis", "ALS"),
        ("ALS", "ALS"),
        ("Multiple Sclerosis", "Multiple Sclerosis"),
        ("Schizophrenia", "Schizophrenia"),
        ("Glioblastoma", "Glioblastoma"),
        ("Ovarian Cancer", "Ovarian Cancer"),
        ("Ovarian carcinoma", "Ovarian Cancer"),
        ("Pancreatic Cancer", "Pancreatic Cancer"),
        ("Pancreatic ductal adenocarcinoma", "Pancreatic Cancer"),
        ("Breast Cancer", "Breast Cancer"),
        ("Triple-negative breast cancer", "Breast Cancer (TNBC)"),
        ("Lung Cancer", "Lung Cancer"),
        ("NSCLC", "Lung Cancer"),
        ("Lung adenocarcinoma", "Lung Cancer"),
        ("Liver Cancer", "Liver Cancer"),
        ("Hepatocellular carcinoma", "Liver Cancer"),
        ("HCC", "Liver Cancer"),
        ("Gastric Cancer", "Gastric Cancer"),
        ("Colorectal Cancer", "Colorectal Cancer"),
        ("Prostate Cancer", "Prostate Cancer"),
        ("Melanoma", "Melanoma"),
        ("COVID-19", "COVID-19"),
        ("SARS-CoV-2", "COVID-19"),
        ("Sepsis", "Sepsis"),
        ("Myocardial infarction", "Heart Disease"),
        ("Thrombocytopenia", "Thrombocytopenia"),
        ("Eosinophilic esophagitis", "Eosinophilic Esophagitis"),
        ("Tuberculosis", "Tuberculosis"),
        ("Diabetes", "Diabetes"),
        ("Rheumatoid Arthritis", "Rheumatoid Arthritis")
    ]
    
    for keyword, label in rules:
        if keyword.lower() in t:
            return label
            
    if "cancer" in t or "tumor" in t or "carcinoma" in t:
        return "Cancer (Unspecified)"
        
    return ""

def process_csv(input_file, output_file, id_col):
    if not os.path.exists(input_file):
        print(f"Skipping {input_file} (Not found)")
        return

    df = pd.read_csv(input_file)
    print(f"\nProcessing {input_file} ({len(df)} rows)...")
    
    abstracts = []
    new_labels = []
    
    for index, row in df.iterrows():
        title = row.get('Title', '')
        existing_label = row.get('Inferred_Disease', '') if 'Inferred_Disease' in row else row.get('Enriched_Disease', '')
        
        # Skip if we already have a specific label (not just "Cancer (Unspecified)" or empty)
        if existing_label and "Unspecified" not in str(existing_label) and "Unknown" not in str(existing_label):
            abstracts.append("Skipped (Label exists)")
            new_labels.append(existing_label)
            continue
            
        print(f"  Fetching info for: {title[:30]}...")
        pmid = search_pubmed_id(title)
        abstract = fetch_abstract(pmid)
        
        # Infer from Abstract
        inferred = infer_disease_from_text(abstract)
        
        # If abstract inference fails, try title again with stricter rules
        if not inferred:
            inferred = infer_disease_from_text(title)
            
        abstracts.append(abstract[:100] + "..." if abstract else "")
        new_labels.append(inferred if inferred else existing_label)
        
        time.sleep(0.5) # Rate limit
        
    df['Abstract_Snippet'] = abstracts
    df['Final_Disease_Label'] = new_labels
    
    # Save
    df.to_csv(output_file, index=False)
    print(f"Saved updated list to {output_file}")
    print(df[[id_col, 'Final_Disease_Label']].head(10).to_markdown(index=False))

def main():
    # Process PRIDE (Proteins)
    process_csv(PRIDE_CSV, OUTPUT_PRIDE, "Accession")
    
    # Process GEO (miRNA)
    process_csv(GEO_CSV, OUTPUT_GEO, "GEO_ID")

if __name__ == "__main__":
    main()
