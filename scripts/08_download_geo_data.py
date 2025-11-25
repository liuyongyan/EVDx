import pandas as pd
import requests
import os
import time
import re
import urllib.request
from bs4 import BeautifulSoup

# Configuration
INPUT_CSV = "geo_mirna_candidates_enriched.csv"
DOWNLOAD_DIR = "raw_data/geo_downloads"
GEO_FILE_URL_BASE = "https://ftp.ncbi.nlm.nih.gov/geo/series"

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_supp_files(gse_id):
    """
    Constructs the likely FTP URL for the supplementary files.
    GEO structure: /geo/series/GSEnnn/GSE12345/suppl/
    """
    # GSE12345 -> GSE12nnn
    # GSE123 -> GSE1nnn
    stub = gse_id[:-3] + "nnn"
    url = f"{GEO_FILE_URL_BASE}/{stub}/{gse_id}/suppl/"
    return url

def download_supp_files(gse_id):
    """
    Download supplementary files by constructing the URL directly.
    Uses BeautifulSoup to parse the directory listing.
    """
    print(f"\nProcessing {gse_id}...")
    project_dir = os.path.join(DOWNLOAD_DIR, gse_id)
    ensure_dir(project_dir)
    
    # Construct URL directly
    supp_url = get_supp_files(gse_id)
    http_url = supp_url.replace("ftp://", "https://")
    
    try:
        print(f"Checking: {http_url}")
        response = requests.get(http_url)
        if response.status_code != 200:
            print(f"Error: Status code {response.status_code} for {http_url}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all links
        links = soup.find_all('a')
        file_names = [link.get('href') for link in links if link.get('href')]
            
        # Filter for relevant files (counts, raw, txt, csv, xls)
        # Common GEO extensions: .txt.gz, .csv.gz, .tsv.gz, .xlsx, .xls, .tar
        # We want count matrices.
        target_files = []
        for f in file_names:
            lower_f = f.lower()
            # Skip parent directory links
            if f.startswith('/') or f.startswith('?') or f.startswith('http'):
                continue
                
            # Criteria:
            # 1. Must be a file (has extension)
            # 2. Must contain 'count', 'raw', 'matrix', 'fpkm', 'tpm', 'rpkm' OR be a clear table (.csv/.tsv/.xlsx)
            is_interesting = False
            if any(kw in lower_f for kw in ['count', 'raw', 'matrix', 'quant', 'expression', 'fpkm', 'tpm', 'rpkm']):
                is_interesting = True
            elif lower_f.endswith('.csv.gz') or lower_f.endswith('.tsv.gz') or lower_f.endswith('.txt.gz') or lower_f.endswith('.xlsx'):
                is_interesting = True
            
            if is_interesting and not lower_f.endswith('/'):
                target_files.append(f)
        
        if not target_files:
            print(f"No relevant supplementary files found in {http_url}")
            return
            
        for fname in target_files:
            # Download
            file_url = f"{http_url}{fname}"
            local_path = os.path.join(project_dir, fname)
            
            if os.path.exists(local_path):
                # print(f"Skipping existing: {fname}")
                continue
                
            print(f"Downloading {fname}...")
            urllib.request.urlretrieve(file_url, local_path)
            
    except Exception as e:
        print(f"Error accessing {http_url}: {e}")

def main():
    ensure_dir(DOWNLOAD_DIR)
    
    if not os.path.exists(INPUT_CSV):
        print(f"{INPUT_CSV} not found.")
        return
        
    df = pd.read_csv(INPUT_CSV)
    gse_ids = df['GEO_ID'].unique().tolist()
    print(f"Found {len(gse_ids)} GEO datasets to process.")
    
    for gse in gse_ids:
        download_supp_files(gse)
        time.sleep(1)

if __name__ == "__main__":
    main()
