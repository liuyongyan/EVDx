import pandas as pd

PROT_META = "analysis_results/proteomics/merged_metadata.csv"
MIRNA_META = "analysis_results/mirna/merged_mirna_metadata.csv"

def check_balance(file_path, name):
    print(f"\n=== {name} Balance Check ===")
    try:
        df = pd.read_csv(file_path)
        
        # Group by Study (Batch/Accession) and Condition
        # Using 'Accession' as batch
        counts = df.groupby(['Accession', 'Refined_Condition']).size().unstack(fill_value=0)
        
        # Calculate Control %
        if 'Healthy Control' in counts.columns:
            counts['Control_Pct'] = (counts['Healthy Control'] / counts.sum(axis=1)) * 100
        else:
            counts['Healthy Control'] = 0
            counts['Control_Pct'] = 0.0
            
        # Sort by Total Samples
        counts['Total'] = counts.sum(axis=1)
        counts.sort_values('Total', ascending=False, inplace=True)
        
        print(counts[['Healthy Control', 'Control_Pct']].to_markdown())
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_balance(PROT_META, "Proteomics")
    check_balance(MIRNA_META, "miRNA")

