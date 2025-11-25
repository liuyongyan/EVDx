import pandas as pd
import os

# Configuration
PRIDE_CSV = "candidate_papers_final.csv"
GEO_CSV = "geo_mirna_candidates_final.csv"
OUTPUT_MD = "documentation/05_Selected_Papers.md"

def generate_markdown():
    print("Generating documentation/05_Selected_Papers.md...")
    
    md_content = "# Selected Papers\n\n"
    md_content += "This document lists all the datasets that passed our strict quality filters (Human Blood, Standardized Pipelines, Results Available) and were included in the final EVDx database.\n\n"
    
    # --- Proteomics ---
    md_content += "## 1. Proteomics (PRIDE / MaxQuant)\n"
    md_content += "**Total:** 23 Studies\n\n"
    
    if os.path.exists(PRIDE_CSV):
        df_pride = pd.read_csv(PRIDE_CSV)
        # Columns to show: Accession, Final_Disease_Label, Title, SubmissionDate
        # Rename for display
        df_pride = df_pride[['Accession', 'Final_Disease_Label', 'Title', 'SubmissionDate']]
        df_pride.columns = ['Accession', 'Disease Cohort', 'Study Title', 'Date']
        
        # Format as markdown table
        md_content += df_pride.to_markdown(index=False)
        md_content += "\n\n"
    else:
        md_content += "*Error: Proteomics list not found.*\n\n"

    # --- miRNA ---
    md_content += "## 2. miRNA (GEO / RNA-seq)\n"
    md_content += "**Total:** 34 Studies\n\n"
    
    if os.path.exists(GEO_CSV):
        df_geo = pd.read_csv(GEO_CSV)
        # Columns: GEO_ID, Final_Disease_Label, Title, Sample_Count
        # Rename
        df_geo = df_geo[['GEO_ID', 'Final_Disease_Label', 'Sample_Count', 'Title']]
        df_geo.columns = ['GEO ID', 'Disease Cohort', 'Samples', 'Study Title']
        
        md_content += df_geo.to_markdown(index=False)
        md_content += "\n\n"
    else:
        md_content += "*Error: miRNA list not found.*\n\n"
        
    # Write file
    with open(OUTPUT_MD, 'w') as f:
        f.write(md_content)
    
    print(f"Successfully created {OUTPUT_MD}")

if __name__ == "__main__":
    generate_markdown()
