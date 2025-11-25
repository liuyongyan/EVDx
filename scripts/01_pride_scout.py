import requests
import json
import pandas as pd
import time
import os

# Configuration
PRIDE_API_BASE = "https://www.ebi.ac.uk/pride/ws/archive/v2"
OUTPUT_FILE = "pride_scout_results.csv"

# Keywords - Search one by one to ensure hits
SEARCH_TERMS = ["exosome", "extracellular vesicle", "microvesicle", "plasma proteomics", "serum proteomics"]

REQUIRED_SOFTWARE = ["MaxQuant", "maxquant"]
BLOOD_KEYWORDS = ["plasma", "serum", "blood", "circulating"]
CELL_KEYWORDS = ["cell line", "cell culture", "supernatant", "in vitro", "conditioned media"]

def search_pride_projects(keyword, page_size=100):
    """Search PRIDE projects with a single keyword."""
    url = f"{PRIDE_API_BASE}/search/projects"
    params = {
        "keyword": keyword,
        "pageSize": page_size,
        "page": 0
    }
    
    all_projects = []
    while True:
        print(f"Fetching page {params['page']} for keyword '{keyword}'...")
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # The API returns a direct list of projects
            projects = data
            
            if not projects:
                break
                
            all_projects.extend(projects)
            
            # Pagination check
            if len(projects) < page_size:
                break
                
            params["page"] += 1
            time.sleep(0.5) # Respect API rate limits
            
        except Exception as e:
            print(f"Error fetching projects: {e}")
            break
            
    return all_projects

def check_project_files(project_accession):
    """Check if project has processed result files (proteinGroups, Excel, CSV)."""
    url = f"{PRIDE_API_BASE}/projects/{project_accession}/files"
    
    try:
        response = requests.get(url)
        # response.raise_for_status() # PRIDE sometimes returns 200 even if empty or 404 if no files
        if response.status_code != 200:
             return False, []
             
        files = response.json()
        
        has_results = False
        file_names = []
        
        for f in files:
            fname = f.get("fileName", "")
            file_names.append(fname)
            lower_name = fname.lower()
            
            # Skip raw files
            if lower_name.endswith(".raw"):
                continue
                
            # Strict check for MaxQuant first
            if "proteingroups.txt" in lower_name:
                has_results = True
            # Broader check for other result tables
            elif lower_name.endswith(".xlsx") or lower_name.endswith(".xls") or lower_name.endswith(".csv") or lower_name.endswith(".tsv"):
                 # Avoid metadata/methods files if possible
                 if "metadata" not in lower_name and "method" not in lower_name:
                     has_results = True
            elif lower_name.endswith(".txt") and ("result" in lower_name or "quant" in lower_name or "protein" in lower_name):
                 has_results = True
                
        return has_results, file_names
    except Exception as e:
        print(f"Error checking files for {project_accession}: {e}")
        return False, []

def analyze_project(project):
    """Analyze a project to see if it meets our criteria."""
    accession = project.get("accession")
    title = project.get("title", "").lower()
    description = project.get("projectDescription", "").lower()
    sample_protocol = project.get("sampleProcessingProtocol", "").lower()
    data_protocol = project.get("dataProcessingProtocol", "").lower()
    
    # Organism check
    organisms = project.get("organisms", [])
    is_human = False
    for org in organisms:
        if isinstance(org, dict):
            if "Homo sapiens" in org.get("name", "") or "9606" in str(org.get("accession", "")):
                is_human = True
                break
        elif isinstance(org, str):
             if "Homo sapiens" in org or "9606" in org:
                 is_human = True
                 break
            
    if not is_human:
        return {"Status": "Non-Human", "Accession": accession}

    full_text = f"{title} {description} {sample_protocol} {data_protocol}"
    
    # Check for MaxQuant
    is_maxquant = any(kw.lower() in full_text for kw in REQUIRED_SOFTWARE)
    
    # Check for Blood source
    is_blood = any(kw in full_text for kw in BLOOD_KEYWORDS)
    
    # Check for Cell line (for exclusion or flagging)
    is_cell_line = any(kw in full_text for kw in CELL_KEYWORDS)
    
    # Determination
    status = "Skip"
    if is_maxquant:
        if is_blood and not is_cell_line:
            status = "High Priority (Blood)"
        elif is_blood and is_cell_line:
            status = "Mixed/Unsure"
        elif not is_blood and is_cell_line:
            status = "Cell Line"
        else:
            status = "MaxQuant (Other)"
            
    return {
        "Accession": accession,
        "Title": project.get("title"),
        "SubmissionDate": project.get("submissionDate"),
        "Status": status,
        "Is_MaxQuant": is_maxquant,
        "Is_Blood": is_blood,
        "Is_CellLine": is_cell_line,
        "Description": project.get("projectDescription", "")[:200] + "..."
    }

def main():
    print("Starting PRIDE Scout (Broad Results Search)...")
    
    all_projects_dict = {} 
    
    # 1. Search for projects
    for term in SEARCH_TERMS:
        projects = search_pride_projects(term)
        for p in projects:
            all_projects_dict[p.get("accession")] = p
            
    unique_projects = list(all_projects_dict.values())
    print(f"Found {len(unique_projects)} unique candidate projects.")
    
    results = []
    
    # 2. Analyze each project
    print("Analyzing metadata...")
    for i, proj in enumerate(unique_projects):
        analysis = analyze_project(proj)
        
        if analysis["Status"] == "Non-Human":
            continue
            
        # Filter: Keep Blood projects that use MaxQuant
        if analysis["Is_MaxQuant"] and analysis["Is_Blood"]:
             print(f"Checking files for candidate: {analysis['Accession']} - {analysis['Status']}")
             has_res, files = check_project_files(analysis["Accession"])
             analysis["Has_Results"] = has_res
             results.append(analysis)
        elif analysis["Is_MaxQuant"]:
            # Keep it but mark as not checked for files
            analysis["Has_Results"] = "Not Checked"
            results.append(analysis)

        if i % 50 == 0:
            print(f"Processed {i}/{len(unique_projects)}...")

    # 3. Save results
    if results:
        df = pd.DataFrame(results)
        # Reorder columns
        cols = ["Accession", "Status", "Has_Results", "SubmissionDate", "Title", "Is_Blood", "Is_CellLine"]
        # Handle missing cols if any
        available_cols = [c for c in cols if c in df.columns]
        df = df[available_cols]
        
        # Filter for high priority
        high_priority = df[ (df["Status"] == "High Priority (Blood)") & (df["Has_Results"] == True) ]
        
        print(f"\nSummary:")
        print(f"Total Human MaxQuant Projects Found: {len(df)}")
        print(f"Blood-derived MaxQuant Projects: {len(df[df['Is_Blood'] == True])}")
        
        if 'Has_Results' in df.columns:
             print(f"Projects with Results (txt/xlsx/csv): {len(df[df['Has_Results'] == True])}")
        
        print("\nTop High Priority Candidates (Blood + Results):")
        if not high_priority.empty:
            print(high_priority[["Accession", "Title"]].head(10))
        else:
            print("None found.")
        
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\nFull results saved to {OUTPUT_FILE}")
    else:
        print("No matching projects found.")

if __name__ == "__main__":
    main()