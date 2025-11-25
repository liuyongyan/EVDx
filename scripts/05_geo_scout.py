import requests
import pandas as pd
import time
import xml.etree.ElementTree as ET

# Configuration
GEO_API_SEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
GEO_API_SUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
OUTPUT_FILE = "geo_mirna_candidates.csv"

# Search Strategy
# Looking for: (Plasma OR Serum) AND (Exosome OR EV) AND (miRNA OR non-coding) AND (High throughput sequencing)
QUERY = '("plasma"[Sample Source] OR "serum"[Sample Source]) AND ("exosome"[Description] OR "extracellular vesicle"[Description]) AND ("microRNA"[Description] OR "miRNA"[Description]) AND "non coding rna profiling by high throughput sequencing"[DataSet Type] AND "Homo sapiens"[Organism]'

def search_geo(query, retmax=500):
    """Search GEO for datasets matching the query."""
    params = {
        "db": "gds", # GEO DataSets
        "term": query,
        "retmax": retmax,
        "retmode": "json"
    }
    
    try:
        print(f"Searching GEO with query: {query}")
        response = requests.get(GEO_API_SEARCH, params=params)
        response.raise_for_status()
        data = response.json()
        id_list = data.get("esearchresult", {}).get("idlist", [])
        return id_list
    except Exception as e:
        print(f"Error searching GEO: {e}")
        return []

def get_geo_summaries(id_list):
    """Fetch summaries for a list of GEO IDs."""
    if not id_list:
        return []
    
    # GEO API allows comma-separated IDs
    ids_str = ",".join(id_list)
    params = {
        "db": "gds",
        "id": ids_str,
        "retmode": "json"
    }
    
    try:
        print(f"Fetching summaries for {len(id_list)} datasets...")
        response = requests.get(GEO_API_SUMMARY, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("result", {})
    except Exception as e:
        print(f"Error fetching summaries: {e}")
        return {}

def analyze_geo_entry(gds_id, summary):
    """Extract relevant info from a GEO Summary."""
    # Note: 'summary' is a dict from the JSON response
    
    accession = summary.get("accession", "")
    title = summary.get("title", "")
    summary_text = summary.get("summary", "")
    gse_id = ""
    
    # Extract GSE ID (Series ID) which is what we actually download
    # The 'accession' in GDS search often points to GDSxxx, but we want GSExxx
    # Looking at 'entrytype' or 'ext_relations' might help, but title often has it or we find it via ELink
    # Actually, for GDS db, 'accession' starts with GDS or GSE.
    
    # Let's store the GDS ID and try to find the GSE
    
    return {
        "GEO_ID": accession,
        "Title": title,
        "Summary": summary_text[:300] + "...", # Truncate
        "Date": summary.get("pdat", ""),
        "Taxon": summary.get("taxon", ""),
        "n_samples": summary.get("n_samples", "Unknown"),
        "GDS_ID": gds_id
    }

def main():
    print("Starting GEO miRNA Scout...")
    
    # 1. Search
    ids = search_geo(QUERY)
    print(f"Found {len(ids)} datasets.")
    
    if not ids:
        return

    # 2. Get Details
    # Process in chunks if too many (GEO has limits)
    chunk_size = 50
    all_candidates = []
    
    for i in range(0, len(ids), chunk_size):
        chunk = ids[i:i+chunk_size]
        summaries = get_geo_summaries(chunk)
        
        for gds_id in chunk:
            if gds_id in summaries:
                info = analyze_geo_entry(gds_id, summaries[gds_id])
                all_candidates.append(info)
        
        time.sleep(1) # Rate limit
        
    # 3. Filter and Save
    df = pd.DataFrame(all_candidates)
    
    # Filter: Ensure n_samples > 10 for ML utility
    # Note: n_samples might be int or str
    def parse_n(n):
        try: return int(n)
        except: return 0
        
    df['Sample_Count'] = df['n_samples'].apply(parse_n)
    filtered_df = df[df['Sample_Count'] > 10].copy()
    
    # Sort by date
    filtered_df.sort_values(by='Date', ascending=False, inplace=True)
    
    print(f"\nSummary:")
    print(f"Total Found: {len(df)}")
    print(f"Qualified (>10 samples): {len(filtered_df)}")
    
    # Add empty columns for manual review
    filtered_df['Review_Decision'] = "Pending"
    filtered_df['Disease_Label'] = ""
    
    filtered_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved candidate list to {OUTPUT_FILE}")
    
    print("\nTop Candidates:")
    print(filtered_df[['GEO_ID', 'Title', 'Sample_Count']].head(10).to_markdown(index=False))

if __name__ == "__main__":
    main()
