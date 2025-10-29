#!/bin/bash
# Run all exercises for T1: Biểu diễn và Thu nhận Ảnh

echo "=========================================="
echo "T1: BIỂU DIỄN VÀ THU NHẬN ẢNH"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Working directory: $SCRIPT_DIR"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "Virtual environment created and dependencies installed."
    echo ""
else
    source venv/bin/activate
    echo "Virtual environment activated."
    echo ""
fi

# Function to run a script
run_script() {
    local script_path=$1
    local script_name=$(basename $(dirname $script_path))

    echo "=========================================="
    echo "Running: $script_name"
    echo "=========================================="
    python3 "$script_path"
    echo ""
    echo "Completed: $script_name"
    echo ""
}

# Run all exercises
echo "Starting all exercises..."
echo ""

run_script "bai-tap-1-camera-storage/calculator.py"
run_script "bai-tap-2-quantization/quantize_scan.py"
run_script "bai-tap-3-bitplane-slicing/bitplane.py"
run_script "bai-tap-4-connectivity/robot_path.py"
run_script "bai-tap-5-color-space/skin_detection.py"

run_script "lab-1-quantization-eval/evaluate.py"
run_script "lab-2-zooming-shrinking/resize.py"
run_script "lab-3-measure-circle/measure.py"
run_script "lab-4-connected-components/labeling.py"
run_script "lab-5-image-quality/assess.py"

echo "=========================================="
echo "ALL EXERCISES COMPLETED!"
echo "=========================================="
echo ""
echo "Output files are saved in the 'output' folder."
echo ""
