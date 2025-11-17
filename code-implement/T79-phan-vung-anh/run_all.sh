#!/bin/bash

# Script chạy tất cả 10 bài tập T79 - Phân vùng ảnh

echo "============================================================"
echo "CHẠY TẤT CẢ BÀI TẬP T79 - PHÂN VÙNG ẢNH"
echo "============================================================"
echo ""

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "Lỗi: Không tìm thấy Python3"
    exit 1
fi

# Kiểm tra và cài đặt dependencies
echo "Kiểm tra dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies đã sẵn sàng"
echo ""

# Danh sách các bài tập
exercises=(
    "bai-1-global-thresholding/threshold.py"
    "bai-2-otsu/threshold.py"
    "bai-3-adaptive-thresholding/threshold.py"
    "bai-4-bayes-ml/threshold.py"
    "bai-5-edge-hough/detect.py"
    "bai-6-region-growing/grow.py"
    "bai-7-split-merge/segment.py"
    "bai-8-kmeans/cluster.py"
    "bai-9-motion-segmentation/segment.py"
    "bai-10-watershed/segment.py"
)

# Chạy từng bài
for i in "${!exercises[@]}"; do
    exercise="${exercises[$i]}"
    num=$((i + 1))

    echo "------------------------------------------------------------"
    echo "BÀI $num: $exercise"
    echo "------------------------------------------------------------"

    if [ -f "$exercise" ]; then
        python3 "$exercise"

        if [ $? -eq 0 ]; then
            echo "✓ Hoàn thành bài $num"
        else
            echo "✗ Lỗi khi chạy bài $num"
        fi
    else
        echo "✗ Không tìm thấy file: $exercise"
    fi

    echo ""
done

echo "============================================================"
echo "HOÀN THÀNH TẤT CẢ!"
echo "============================================================"
