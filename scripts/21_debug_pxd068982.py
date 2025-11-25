import requests
import json

ACCESSION = "PXD068982"
URL = f"https://www.ebi.ac.uk/pride/ws/archive/v2/projects/{ACCESSION}/files"

def list_all_files():
    print(f"Checking files for {ACCESSION}...")
    r = requests.get(URL)
    files = r.json()
    for f in files:
        print(f"- {f.get('fileName')} ({f.get('fileCategory', {}).get('value')})")

if __name__ == "__main__":
    list_all_files()
