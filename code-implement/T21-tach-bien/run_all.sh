#!/bin/bash

# Run All Edge Detection Assignments
# This script executes all 10 edge detection assignments sequentially

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Print header
echo "================================================================="
echo -e "${BLUE}Edge Detection Assignment - Running All Tests${NC}"
echo "================================================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed${NC}"
    exit 1
fi

# Check if sample images exist, if not generate them
if [ ! -d "input/sample-images" ]; then
    echo -e "${YELLOW}Sample images not found. Generating them...${NC}"
    python3 input/generate_samples.py
    echo ""
fi

# Counter for success/failure
total=10
success=0
failed=0

# Array of assignments
declare -a assignments=(
    "bai-1-edge-detectors:compare.py:building.jpg"
    "bai-2-document-scanning:scan.py:doc.jpg"
    "bai-3-lane-detection:detect.py:road.jpg"
    "bai-4-defect-detection:detect.py:surface.jpg"
    "bai-5-coin-counting:count.py:coins.jpg"
    "bai-6-product-cropping:crop.py:product.jpg"
    "bai-7-crack-detection:detect.py:surface_crack.jpg"
    "bai-8-leaf-measurement:measure.py:leaf.jpg"
    "bai-9-object-measurement:measure.py:measure.jpg"
    "bai-10-deskewing:deskew.py:receipt.jpg"
)

# Run each assignment
for i in "${!assignments[@]}"; do
    IFS=':' read -r folder script image <<< "${assignments[$i]}"
    num=$((i + 1))

    echo "-----------------------------------------------------------------"
    echo -e "${BLUE}[$num/$total] Running: $folder${NC}"
    echo "-----------------------------------------------------------------"

    # Check if folder exists
    if [ ! -d "$folder" ]; then
        echo -e "${RED}Error: Folder $folder not found${NC}"
        ((failed++))
        continue
    fi

    # Check if script exists
    if [ ! -f "$folder/$script" ]; then
        echo -e "${RED}Error: Script $script not found in $folder${NC}"
        ((failed++))
        continue
    fi

    # Check if input image exists
    input_path="input/sample-images/$image"
    if [ ! -f "$input_path" ]; then
        echo -e "${RED}Error: Input image $image not found${NC}"
        ((failed++))
        continue
    fi

    # Run the script
    if python3 "$folder/$script" "$input_path"; then
        echo -e "${GREEN}✓ Success${NC}"
        ((success++))
    else
        echo -e "${RED}✗ Failed${NC}"
        ((failed++))
    fi

    echo ""
done

# Print summary
echo "================================================================="
echo -e "${BLUE}Summary${NC}"
echo "================================================================="
echo -e "Total:   $total"
echo -e "${GREEN}Success: $success${NC}"
if [ $failed -gt 0 ]; then
    echo -e "${RED}Failed:  $failed${NC}"
else
    echo -e "Failed:  $failed"
fi
echo "================================================================="

# Exit with error if any test failed
if [ $failed -gt 0 ]; then
    exit 1
fi

echo ""
echo -e "${GREEN}All assignments completed successfully!${NC}"
echo "Check the 'output' directory for results."
