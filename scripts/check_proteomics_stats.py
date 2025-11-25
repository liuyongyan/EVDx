import pandas as pd

META_FILE = "analysis_results/proteomics/merged_metadata.csv"

def check_counts():
    df = pd.read_csv(META_FILE)
    print("--- Sample Counts by Refined Condition ---")
    print(df['Refined_Condition'].value_counts())
    
    print("\n--- Sample Counts by Batch (Study) ---")
    print(df['Batch'].value_counts())

if __name__ == "__main__":
    check_counts()

