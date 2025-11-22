#!/bin/bash

# EVmiRNA2.0 Complete Bulk Downloader
# Downloads ALL 3 CSV files for each project:
# 1. Metadata
# 2. Expression
# 3. Expression Count

set -e  # Exit on error

# Configuration
OUTPUT_DIR="evmirna_data"
API_BASE="https://guolab.wchscu.cn/EVmiRNA2.0_api/api"
PROJECT_IDS_FILE="project_ids.txt"
DELAY=0.5  # Delay between requests in seconds

# API endpoints and suffixes (bash 3.2 compatible)
# Format: file_type|endpoint|suffix
FILE_TYPES="
metadata|download_metadata|_metadata.csv
expression|download_expression|_expression.csv
expression_count|download_expression_Count|_expression_count.csv
"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "========================================"
echo "EVmiRNA2.0 Complete Bulk Downloader"
echo "Downloads ALL 3 CSV files per project:"
echo "  1. Metadata"
echo "  2. Expression"
echo "  3. Expression Count"
echo "========================================"

# Check if project IDs file exists
if [ ! -f "$PROJECT_IDS_FILE" ]; then
    echo -e "${RED}Error: $PROJECT_IDS_FILE not found${NC}"
    echo ""
    echo "Please create this file first:"
    echo "1. Open https://guolab.wchscu.cn/EVmiRNA2.0/#/download"
    echo "2. Run get_project_ids.js in browser console"
    echo "3. Save the downloaded project_ids.txt file here"
    exit 1
fi

# Count total projects
TOTAL_PROJECTS=$(wc -l < "$PROJECT_IDS_FILE" | tr -d ' ')
TOTAL_FILES=$((TOTAL_PROJECTS * 3))
echo "Projects: $TOTAL_PROJECTS"
echo "Total files to download: $TOTAL_FILES (3 per project)"
echo "Output directory: $OUTPUT_DIR"
echo "========================================"
echo ""

# Read confirmation
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Statistics
CURRENT_PROJECT=0
TOTAL_SUCCESS=0
TOTAL_FAILED=0
FAILED_DOWNLOADS=()

# Function to download a single file
download_file() {
    local PROJECT_ID=$1
    local FILE_TYPE=$2
    local ENDPOINT=$3
    local SUFFIX=$4
    local OUTPUT_FILE="$OUTPUT_DIR/${PROJECT_ID}${SUFFIX}"

    # Skip if already downloaded
    if [ -f "$OUTPUT_FILE" ]; then
        echo -e "    ${BLUE}⏭️  $FILE_TYPE: Already exists${NC}"
        return 0
    fi

    # Download the file
    HTTP_CODE=$(curl -w "%{http_code}" -s -o "$OUTPUT_FILE" \
        -H 'Accept: application/json' \
        -H 'Referer: https://guolab.wchscu.cn/EVmiRNA2.0/' \
        "${API_BASE}/${ENDPOINT}/${PROJECT_ID}")

    # Check if successful
    if [ "$HTTP_CODE" -eq 200 ]; then
        # Check if file has content and is not an error page
        if [ -s "$OUTPUT_FILE" ] && ! grep -q "<!doctype html" "$OUTPUT_FILE"; then
            FILE_SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
            echo -e "    ${GREEN}✓ $FILE_TYPE: Downloaded ($FILE_SIZE)${NC}"
            return 0
        else
            echo -e "    ${RED}✗ $FILE_TYPE: Empty or invalid response${NC}"
            rm -f "$OUTPUT_FILE"
            return 1
        fi
    else
        echo -e "    ${RED}✗ $FILE_TYPE: HTTP Error $HTTP_CODE${NC}"
        rm -f "$OUTPUT_FILE"
        return 1
    fi
}

# Download all projects
while IFS= read -r PROJECT_ID; do
    # Skip empty lines
    [ -z "$PROJECT_ID" ] && continue

    ((CURRENT_PROJECT++))

    echo -e "${YELLOW}[$CURRENT_PROJECT/$TOTAL_PROJECTS]${NC} ${PROJECT_ID}"

    PROJECT_SUCCESS=0
    PROJECT_FAILED=0

    # Download all 3 file types
    echo "$FILE_TYPES" | while IFS='|' read -r FILE_TYPE ENDPOINT SUFFIX; do
        # Skip empty lines
        [ -z "$FILE_TYPE" ] && continue

        if download_file "$PROJECT_ID" "$FILE_TYPE" "$ENDPOINT" "$SUFFIX"; then
            ((PROJECT_SUCCESS++))
            ((TOTAL_SUCCESS++))
        else
            ((PROJECT_FAILED++))
            ((TOTAL_FAILED++))
            FAILED_DOWNLOADS+=("${PROJECT_ID} - ${FILE_TYPE}")
        fi

        # Small delay between file downloads
        sleep $DELAY
    done

    # Summary for this project
    if [ $PROJECT_FAILED -eq 0 ]; then
        echo -e "  ${GREEN}Complete: 3/3 files${NC}"
    else
        echo -e "  ${YELLOW}Partial: $PROJECT_SUCCESS/3 files${NC}"
    fi

    echo ""

done < "$PROJECT_IDS_FILE"

# Final Summary
echo "========================================"
echo "Download Complete!"
echo "========================================"
echo -e "${GREEN}Successful downloads: $TOTAL_SUCCESS${NC}"
echo -e "${RED}Failed downloads: $TOTAL_FAILED${NC}"
echo "Total attempted: $TOTAL_FILES"
echo ""
echo "Success rate: $(awk "BEGIN {printf \"%.1f\", ($TOTAL_SUCCESS/$TOTAL_FILES)*100}")%"
echo "Output directory: $(pwd)/$OUTPUT_DIR"

# List failed downloads
if [ $TOTAL_FAILED -gt 0 ]; then
    echo ""
    echo "========================================"
    echo "Failed Downloads:"
    echo "========================================"
    for ITEM in "${FAILED_DOWNLOADS[@]}"; do
        echo "  - $ITEM"
    done

    # Save failed downloads to file
    printf "%s\n" "${FAILED_DOWNLOADS[@]}" > failed_downloads.txt
    echo ""
    echo "Failed downloads saved to: failed_downloads.txt"
fi

# Count files by type
echo ""
echo "========================================"
echo "Files by Type:"
echo "========================================"
METADATA_COUNT=$(ls -1 "$OUTPUT_DIR"/*_metadata.csv 2>/dev/null | wc -l | tr -d ' ')
EXPRESSION_COUNT=$(ls -1 "$OUTPUT_DIR"/*_expression.csv 2>/dev/null | wc -l | tr -d ' ')
EXPRESSION_COUNT_COUNT=$(ls -1 "$OUTPUT_DIR"/*_expression_count.csv 2>/dev/null | wc -l | tr -d ' ')

echo "Metadata files:        $METADATA_COUNT"
echo "Expression files:      $EXPRESSION_COUNT"
echo "Expression count files: $EXPRESSION_COUNT_COUNT"

echo ""
echo "Done!"
