import requests
import os
import sys
import pandas as pd
import urllib.request

# Configuration
PRIDE_API_BASE = "https://www.ebi.ac.uk/pride/ws/archive/v2"
DOWNLOAD_DIR = "raw_data/pride_downloads"
INPUT_CSV = "candidate_papers_enriched.csv"

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_project_files(accession):
    """Get list of files for a project."""
    url = f"{PRIDE_API_BASE}/projects/{accession}/files"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return []
        return response.json()
    except Exception as e:
        print(f"Error getting files for {accession}: {e}")
        return []

def download_file(url, local_path):
    """Download a file with progress tracking using urllib."""
    try:
        # Convert FTP to HTTP if possible for better stability
        if url.startswith("ftp://ftp.pride.ebi.ac.uk"):
            url = url.replace("ftp://", "https://")

        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, local_path)
        print(f"Downloaded: {local_path}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def process_project(accession):
    """Find and download proteinGroups.txt and metadata for a project."""
    print(f"\nProcessing {accession}...")
    project_dir = os.path.join(DOWNLOAD_DIR, accession)
    ensure_dir(project_dir)
    
    files = get_project_files(accession)
    
    # Look for interesting files
    target_files = []
    for f in files:
        fname = f.get("fileName", "")
        lower_name = fname.lower()
        
        # Skip raw files
        if lower_name.endswith(".raw"):
            continue

        is_target = False
        if "proteingroups.txt" in lower_name:
            is_target = True
        elif lower_name.endswith(".xlsx") or lower_name.endswith(".xls") or lower_name.endswith(".csv"):
             # Avoid obvious non-results
             if "metadata" not in lower_name and "method" not in lower_name:
                 is_target = True
        elif "sdrf" in lower_name or "experimentaldesign" in lower_name or "summary.txt" in lower_name:
            is_target = True
            
        if is_target:
            target_files.append(f)
            
    if not target_files:
        print(f"No relevant files found for {accession}")
        return

    for tf in target_files:
        fname = tf.get("fileName")
        locations = tf.get("publicFileLocations", [])
        download_url = None
        
        for loc in locations:
            val = loc.get("value", "")
            if val.startswith("http"):
                download_url = val
                break
        
        if not download_url:
            for loc in locations:
                val = loc.get("value", "")
                if val.startswith("ftp"):
                    download_url = val
                    break
        
        if download_url:
            local_path = os.path.join(project_dir, fname)
            if os.path.exists(local_path):
                # Optional: Skip if exists
                # print(f"File already exists: {local_path}")
                pass
            else:
                download_file(download_url, local_path)

def main():
    ensure_dir(DOWNLOAD_DIR)
    
    if not os.path.exists(INPUT_CSV):
        print(f"{INPUT_CSV} not found.")
        return
        
    df = pd.read_csv(INPUT_CSV)
    accessions = df['Accession'].unique().tolist()
    print(f"Found {len(accessions)} projects to process.")
    
    for acc in accessions:
        process_project(acc)

if __name__ == "__main__":
    main()
