import requests
import os
# import gzip # No longer needed for uncompressed file

# Configuration
MIRBASE_URL = "https://raw.githubusercontent.com/mikelove/miRBase/master/mature.fa"
REF_DIR = "raw_data/references"
OUTPUT_FILE = "raw_data/references/mirbase_seq_map.csv"

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_mirbase():
    ensure_dir(REF_DIR)
    local_path = os.path.join(REF_DIR, "mature.fa")
    
    if os.path.exists(local_path):
        print("miRBase mature.fa already exists.")
        return local_path
        
    print(f"Downloading {MIRBASE_URL}...")
    try:
        r = requests.get(MIRBASE_URL, stream=True)
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download complete.")
        return local_path
    except Exception as e:
        print(f"Error downloading miRBase: {e}")
        return None

def parse_fasta_to_map(fasta_path):
    """
    Parse FASTA and build Sequence -> Name map.
    Only keeps 'hsa-' (Human) entries to keep it small and relevant.
    """
    print("Parsing miRBase FASTA...")
    seq_map = {}
    
    try:
        with open(fasta_path, 'r') as f:
            current_name = ""
            current_seq = []
            
            for line in f:
                line = line.strip()
                if line.startswith(">"):
                    # Process previous entry
                    if current_name and current_seq:
                        seq = "".join(current_seq).upper()
                        # Only keep human
                        if "hsa-" in current_name:
                            if seq not in seq_map:
                                seq_map[seq] = current_name
                                
                    # Start new entry
                    # Header: >hsa-let-7a-5p MIMAT0000062 Homo sapiens let-7a-5p
                    # Extract "hsa-let-7a-5p"
                    parts = line.split()
                    current_name = parts[0][1:] # Remove >
                    current_seq = []
                else:
                    current_seq.append(line)
            
            # Process last entry
            if current_name and current_seq and "hsa-" in current_name:
                seq = "".join(current_seq).upper()
                if seq not in seq_map:
                    seq_map[seq] = current_name
                    
        print(f"Loaded {len(seq_map)} unique human miRNA sequences.")
        return seq_map
        
    except Exception as e:
        print(f"Error parsing FASTA: {e}")
        return {}

def save_map(seq_map):
    with open(OUTPUT_FILE, 'w') as f:
        f.write("Sequence,miRNA_ID\n")
        for seq, name in seq_map.items():
            f.write(f"{seq},{name}\n")
    print(f"Saved map to {OUTPUT_FILE}")

def main():
    fasta_path = download_mirbase()
    if fasta_path:
        seq_map = parse_fasta_to_map(fasta_path)
        if seq_map:
            save_map(seq_map)

if __name__ == "__main__":
    main()
