import pandas as pd
import os

# Configuration
PRIDE_RESULTS_FILE = "pride_scout_results.csv"
OUTPUT_CANDIDATE_FILE = "candidate_papers_for_review.csv"

def generate_list():
    if not os.path.exists(PRIDE_RESULTS_FILE):
        print(f"Error: {PRIDE_RESULTS_FILE} not found. Run pride_scout.py first.")
        return

    df = pd.read_csv(PRIDE_RESULTS_FILE)
    
    # Filter for our strict criteria
    # 1. Blood (Plasma/Serum)
    # 2. MaxQuant used
    # 3. Results found (Has_Results == True)
    
    # Ensure string conversion for filtering
    if 'Has_Results' in df.columns:
        df['Has_Results'] = df['Has_Results'].astype(str)
        
        candidates = df[
            (df['Is_Blood'] == True) & 
            (df['Has_Results'] == 'True') & 
            (df['Status'].str.contains("Blood", case=False))
        ].copy()
    else:
        print("Error: 'Has_Results' column not found in CSV.")
        return
    
    # Select relevant columns for the user
    # Note: 'Description' might be missing if not saved in scout, checking availability
    available_cols = df.columns.tolist()
    target_cols = ['Accession', 'Title', 'SubmissionDate']
    cols = [c for c in target_cols if c in available_cols]
    
    review_list = candidates[cols].copy()
    
    # Add columns for manual review
    review_list['Proposed_Disease_Label'] = ""
    review_list['Sample_Type'] = "Plasma/Serum" 
    review_list['Review_Decision'] = "Pending" 
    
    # Try to infer disease from title for convenience
    def infer_disease(title):
        t = str(title).lower()
        if "alzheimer" in t: return "Alzheimer's Disease"
        if "ovarian" in t: return "Ovarian Cancer"
        if "liver" in t or "hepatocellular" in t or "hcc" in t: return "Liver Cancer"
        if "lung" in t: return "Lung Cancer"
        if "covid" in t or "sars-cov-2" in t: return "COVID-19"
        if "als" in t or "amyotrophic" in t: return "ALS"
        if "parkinson" in t: return "Parkinson's Disease"
        if "sepsis" in t or "septic" in t: return "Sepsis"
        if "melanoma" in t: return "Melanoma"
        if "gastric" in t: return "Gastric Cancer"
        if "rheumatoid" in t: return "Rheumatoid Arthritis"
        if "hiv" in t: return "HIV"
        if "pancreatic" in t: return "Pancreatic Cancer"
        return "Unknown (Check Title)"

    review_list['Proposed_Disease_Label'] = review_list['Title'].apply(infer_disease)
    
    # Sort by Date (Newest first)
    if 'SubmissionDate' in review_list.columns:
        review_list.sort_values(by='SubmissionDate', ascending=False, inplace=True)
    
    # Save
    review_list.to_csv(OUTPUT_CANDIDATE_FILE, index=False)
    print(f"Generated {OUTPUT_CANDIDATE_FILE} with {len(review_list)} candidates.")
    
    # Print a preview for the CLI
    print("\n--- Candidate Preview (Top 15) ---")
    print(review_list[['Accession', 'Proposed_Disease_Label', 'Title']].head(15).to_markdown(index=False))

if __name__ == "__main__":
    generate_list()
