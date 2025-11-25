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
        sample_id = row['Original_Sample_ID']
        
        # Check for sample-level inferred metadata
        inferred_meta_path = f"analysis_results/{acc}/inferred_metadata.csv"
        if os.path.exists(inferred_meta_path):
            try:
                # Load on demand (or cache it for performance if list is huge)
                sample_map = pd.read_csv(inferred_meta_path).set_index('SampleID')['Group'].to_dict()
                
                mapped_group = None
                if sample_id in sample_map:
                    mapped_group = sample_map[sample_id]
                elif "_" in sample_id:
                    # Try stripping suffix (e.g. EV1_1 -> EV1)
                    base_id = sample_id.rsplit('_', 1)[0]
                    if base_id in sample_map:
                        mapped_group = sample_map[base_id]
                        
                if mapped_group:
                    # Map "Disease" to the specific label, "Control" to "Healthy Control"
                    if mapped_group.lower() == "disease":
                        current_cond = "Case" # Let downstream logic pick the specific disease name
                    elif mapped_group.lower() == "control":
                        current_cond = "Healthy Control"
            except Exception as e:
                # print(f"Error reading {inferred_meta_path}: {e}")
                pass
        
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
