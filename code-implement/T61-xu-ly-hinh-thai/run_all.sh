#!/bin/bash

################################################################################
# Script chạy tất cả bài tập T61 - Xử lý hình thái
################################################################################

echo "================================================================================"
echo "CHẠY TẤT CẢ BÀI TẬP T61 - XỬ LÝ HÌNH THÁI"
echo "================================================================================"

# Màu sắc
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 chưa được cài đặt!"
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Python 3: $(python3 --version)"

# Kiểm tra requirements
echo ""
echo "Kiểm tra dependencies..."
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}[WARNING]${NC} Virtual environment chưa tồn tại. Tạo mới..."
    python3 -m venv venv
fi

source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

echo "Cài đặt requirements..."
pip install -q -r requirements.txt

echo ""
echo "================================================================================"
echo "BẮT ĐẦU CHẠY CÁC BÀI TẬP"
echo "================================================================================"

# Danh sách bài tập
exercises=(
    "bai-1-opening:denoise.py:Làm sạch văn bản quét"
    "bai-2-closing:fill_holes.py:Lấp lỗ và nối nét"
    "bai-3-gradient:extract_edges.py:Trích biên bằng gradient"
    "bai-4-watershed:separate.py:Đếm đồng xu dính nhau"
    "bai-5-character-segmentation:segment.py:Phân đoạn ký tự"
    "bai-6-particle-measurement:measure.py:Đo đường kính hạt"
    "bai-7-pruning:prune.py:Xóa pixel thừa"
    "bai-8-foreground-extraction:extract.py:Tách tiền cảnh"
    "bai-9-background-removal:remove.py:Khử nền không đều"
)

success_count=0
fail_count=0
total=${#exercises[@]}

for exercise in "${exercises[@]}"; do
    IFS=':' read -r folder script title <<< "$exercise"

    echo ""
    echo "--------------------------------------------------------------------------------"
    echo -e "${BLUE}Đang chạy:${NC} $title ($folder/$script)"
    echo "--------------------------------------------------------------------------------"

    cd "$folder" || { echo -e "${RED}[ERROR]${NC} Không tìm thấy thư mục $folder"; ((fail_count++)); continue; }

    if python3 "$script"; then
        echo -e "${GREEN}[✓]${NC} $title: Thành công"
        ((success_count++))
    else
        echo -e "${RED}[✗]${NC} $title: Thất bại"
        ((fail_count++))
    fi

    cd ..
done

# Tổng kết
echo ""
echo "================================================================================"
echo "KẾT QUẢ TỔNG HỢP"
echo "================================================================================"
echo -e "Tổng số bài tập: ${BLUE}$total${NC}"
echo -e "Thành công: ${GREEN}$success_count${NC}"
echo -e "Thất bại: ${RED}$fail_count${NC}"

if [ $fail_count -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ TẤT CẢ BÀI TẬP ĐÃ CHẠY THÀNH CÔNG!${NC}"
    echo "================================================================================"
    exit 0
else
    echo ""
    echo -e "${YELLOW}⚠ CÓ $fail_count BÀI TẬP THẤT BẠI. VUI LÒNG KIỂM TRA LẠI!${NC}"
    echo "================================================================================"
    exit 1
fi
