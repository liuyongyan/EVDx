#!/bin/bash
# ===========================================
# EVDx - Download Large Data Files
# ===========================================
# Run this script after cloning the repo to download
# large data files that are excluded from GitHub.
#
# Usage: ./scripts/download_large_files.sh
# ===========================================

set -e  # Exit on error

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "============================================"
echo "EVDx - Downloading Large Data Files"
echo "============================================"
echo ""

# ---------------------------------------------
# Hoshino 2020 Data (123 MB)
# ---------------------------------------------
echo ">>> Downloading Hoshino 2020 data..."
cd "$PROJECT_ROOT/hoshino2020_data"

if [ -f "Human512Reports.xlsx" ]; then
    echo "    Human512Reports.xlsx already exists, skipping..."
else
    echo "    Downloading Human512Reports.xlsx (108 MB)..."
    curl -# -O ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2020/08/PXD018301/Human512Reports.xlsx
fi

if [ -f "Mouse74Reports.xlsx" ]; then
    echo "    Mouse74Reports.xlsx already exists, skipping..."
else
    echo "    Downloading Mouse74Reports.xlsx (15 MB)..."
    curl -# -O ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2020/08/PXD018301/Mouse74Reports.xlsx
fi

echo "    Hoshino 2020 download complete!"
echo ""

# ---------------------------------------------
# Kugeratski 2021 Data (3.2 GB)
# ---------------------------------------------
echo ">>> Downloading Kugeratski 2021 data..."
cd "$PROJECT_ROOT/kugeratski2021_data"

ZIP1="txtfolderMaxQuant-MS14celllinesderivedexosomesfiles.zip"
ZIP2="txtfolderMaxQuant-MSisolationmethodscomparisonfiles.zip"

if [ -f "$ZIP1" ]; then
    echo "    $ZIP1 already exists, skipping..."
else
    echo "    Downloading 14 cell lines data (2.0 GB)..."
    curl -# -O "ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2021/06/PXD020260/$ZIP1"
fi

if [ -f "$ZIP2" ]; then
    echo "    $ZIP2 already exists, skipping..."
else
    echo "    Downloading isolation methods data (1.2 GB)..."
    curl -# -O "ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2021/06/PXD020260/$ZIP2"
fi

# Extract if not already extracted
DIR1="14_cell_lines_maxquant"
DIR2="isolation_methods_maxquant"

if [ -d "$DIR1" ]; then
    echo "    $DIR1 already extracted, skipping..."
else
    echo "    Extracting 14 cell lines data..."
    unzip -q "$ZIP1"
    # Rename to cleaner directory name
    mv "txt folder MaxQuant - MS 14 cell lines derived exosomes files" "$DIR1"
fi

if [ -d "$DIR2" ]; then
    echo "    $DIR2 already extracted, skipping..."
else
    echo "    Extracting isolation methods data..."
    unzip -q "$ZIP2"
    # Rename to cleaner directory name
    mv "txt folder MaxQuant - MS isolation methods comparison files" "$DIR2"
fi

echo "    Kugeratski 2021 download complete!"
echo ""

# ---------------------------------------------
# Summary
# ---------------------------------------------
echo "============================================"
echo "Download Complete!"
echo "============================================"
echo ""
echo "Downloaded files:"
echo "  - hoshino2020_data/Human512Reports.xlsx (108 MB)"
echo "  - hoshino2020_data/Mouse74Reports.xlsx (15 MB)"
echo "  - kugeratski2021_data/$ZIP1 (2.0 GB)"
echo "  - kugeratski2021_data/$ZIP2 (1.2 GB)"
echo ""
echo "Total: ~3.3 GB"
echo ""
echo "You can now use all datasets. See README.md for usage."
