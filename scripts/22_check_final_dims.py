import pandas as pd

PROT_FILE = "analysis_results/proteomics/merged_protein_matrix_log2.csv"
MIRNA_FILE = "analysis_results/mirna/merged_mirna_matrix_log2.csv"

def check_dims():
    print("Checking dimensions...")
    
    # Proteomics
    try:
        df_p = pd.read_csv(PROT_FILE, index_col=0)
        print(f"Proteomics: {df_p.shape[0]} Features, {df_p.shape[1]} Samples")
    except:
        print("Proteomics file not found/readable.")

    # miRNA
    try:
        df_m = pd.read_csv(MIRNA_FILE, index_col=0)
        print(f"miRNA: {df_m.shape[0]} Features, {df_m.shape[1]} Samples")
    except:
        print("miRNA file not found/readable.")

if __name__ == "__main__":
    check_dims()
