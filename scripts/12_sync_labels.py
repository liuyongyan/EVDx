import pandas as pd
import os

# Files
PROT_META = "analysis_results/proteomics/merged_metadata.csv"
MIRNA_META = "analysis_results/mirna/merged_mirna_metadata.csv"

PROT_LABELS = "candidate_papers_final.csv"
MIRNA_LABELS = "geo_mirna_candidates_final.csv"

def update_metadata(meta_path, label_path, id_col, label_col):
    if not os.path.exists(meta_path) or not os.path.exists(label_path):
        print(f"Skipping {meta_path} (Files missing)")
        return

    print(f"Updating {meta_path}...")
    meta_df = pd.read_csv(meta_path)
    label_df = pd.read_csv(label_path)
    
    # Create map: Accession -> Final Label
    label_map = label_df.set_index(id_col)[label_col].to_dict()
    
    # Update 'Condition' where it is generic or unknown
    # Logic: If we have a better label in label_map, use it.
    # But respect 'Healthy Control' labels from the sample level.
    
    new_conditions = []
    for index, row in meta_df.iterrows():
        acc = row['Accession']
        current_cond = row['Condition']
        
        better_label = label_map.get(acc, "")
        
        if str(current_cond).lower() in ["case", "case (unknown disease)", "cancer (unspecified)", "unknown"]:
            if pd.notna(better_label) and better_label:
                new_conditions.append(better_label)
            else:
                new_conditions.append(current_cond)
        elif "control" in str(current_cond).lower():
            new_conditions.append("Healthy Control")
        else:
            # Keep existing specific label
            new_conditions.append(current_cond)
            
    meta_df['Refined_Condition'] = new_conditions
    
    # Overwrite
    meta_df.to_csv(meta_path, index=False)
    print(f"Updated {len(meta_df)} rows.")
    print(meta_df['Refined_Condition'].value_counts().head().to_markdown())

def main():
    # Proteomics
    update_metadata(PROT_META, PROT_LABELS, "Accession", "Final_Disease_Label")
    
    # miRNA
    update_metadata(MIRNA_META, MIRNA_LABELS, "GEO_ID", "Final_Disease_Label")

if __name__ == "__main__":
    main()
