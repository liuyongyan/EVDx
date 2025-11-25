import pandas as pd

META_FILE = "analysis_results/mirna/merged_mirna_metadata.csv"
LABEL_FILE = "geo_mirna_candidates_final.csv"

def check_unknowns():
    # Load Metadata
    meta = pd.read_csv(META_FILE)
    
    # Load Titles
    labels = pd.read_csv(LABEL_FILE).set_index("GEO_ID")["Title"].to_dict()
    
    # Filter for Unknown
    unknowns = meta[meta['Refined_Condition'] == 'Unknown']
    
    if unknowns.empty:
        print("No Unknown samples found.")
        return

    print(f"Found {len(unknowns)} Unknown samples.")
    
    # Group by Accession (Study)
    grouped = unknowns.groupby('Accession').size().reset_index(name='Count')
    grouped['Title'] = grouped['Accession'].map(labels)
    
    # Sort
    grouped.sort_values('Count', ascending=False, inplace=True)
    
    print("\n--- Unknown Studies ---")
    print(grouped.to_markdown(index=False))

if __name__ == "__main__":
    check_unknowns()
