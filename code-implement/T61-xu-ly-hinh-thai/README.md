# T61 - XỬ LÝ HÌNH THÁI (MORPHOLOGICAL OPERATIONS)

Bộ 9 bài tập thực hành về xử lý hình thái từ giáo trình **T61-78 Xử lý hình thái** của Ph.D Phan Thanh Toàn.

## Mục lục

1. [Làm sạch văn bản quét - Opening](#bài-1-làm-sạch-văn-bản-quét)
2. [Lấp lỗ và nối nét - Closing](#bài-2-lấp-lỗ-và-nối-nét)
3. [Trích biên - Morphological Gradient](#bài-3-trích-biên)
4. [Đếm đồng xu dính nhau - Watershed](#bài-4-đếm-đồng-xu)
5. [Phân đoạn ký tự - Connected Components](#bài-5-phân-đoạn-ký-tự)
6. [Đo đường kính hạt - Particle Measurement](#bài-6-đo-đường-kính-hạt)
7. [Xóa pixel thừa - Pruning](#bài-7-xóa-pixel-thừa)
8. [Tách tiền cảnh - Foreground Extraction](#bài-8-tách-tiền-cảnh)
9. [Khử nền không đều - Top-hat/Black-hat](#bài-9-khử-nền-không-đều)

## Cài đặt

### 1. Clone hoặc tải về repository

```bash
cd /mnt/e/person/xly/2025-Image-Processing-Assignment/code-implement/T61-xu-ly-hinh-thai
```

### 2. Tạo virtual environment (khuyến nghị)

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## Cấu trúc thư mục

```
T61-xu-ly-hinh-thai/
├── bai-1-opening/                  # Bài 1: Opening để khử nhiễu
│   └── denoise.py
├── bai-2-closing/                  # Bài 2: Closing để lấp lỗ
│   └── fill_holes.py
├── bai-3-gradient/                 # Bài 3: Morphological Gradient
│   └── extract_edges.py
├── bai-4-watershed/                # Bài 4: Watershed Segmentation
│   └── separate.py
├── bai-5-character-segmentation/   # Bài 5: Character Segmentation
│   └── segment.py
├── bai-6-particle-measurement/     # Bài 6: Particle Measurement
│   └── measure.py
├── bai-7-pruning/                  # Bài 7: Pruning bằng Hit-or-Miss
│   └── prune.py
├── bai-8-foreground-extraction/    # Bài 8: Foreground Extraction
│   └── extract.py
├── bai-9-background-removal/       # Bài 9: Top-hat/Black-hat
│   └── remove.py
├── input/                          # Ảnh đầu vào
│   ├── docs/
│   ├── parts/
│   ├── objects/
│   ├── coins/
│   ├── plates/
│   ├── surface/
│   ├── edges/
│   ├── conveyor/
│   ├── README.md
│   └── generate_samples.py
├── output/                         # Kết quả output (tự động tạo)
├── requirements.txt
├── run_all.sh                      # Script chạy tất cả (Linux/Mac)
├── run_all.bat                     # Script chạy tất cả (Windows)
└── README.md
```

## Chạy bài tập

### Chạy từng bài

```bash
# Bài 1: Làm sạch văn bản
cd bai-1-opening
python denoise.py

# Bài 2: Lấp lỗ và nối nét
cd bai-2-closing
python fill_holes.py

# ... tương tự cho các bài khác
```

### Chạy tất cả

```bash
# Linux/Mac
chmod +x run_all.sh
./run_all.sh

# Windows
run_all.bat
```

## Mô tả chi tiết các bài tập

### Bài 1: Làm sạch văn bản quét

**Mục tiêu**: Khử nhiễu muối tiêu trên ảnh tài liệu bằng phép Opening.

**Kỹ thuật**:
- Nhị phân hóa Otsu
- Opening = Erosion → Dilation
- So sánh kernel 3×3 vs 5×5

**Input**: `input/docs/noisy_scan.png`
**Output**: `output/bai-1-opening/`

### Bài 2: Lấp lỗ và nối nét

**Mục tiêu**: Lấp lỗ nhỏ và nối các nét gần nhau bằng phép Closing.

**Kỹ thuật**:
- Closing = Dilation → Erosion
- So sánh kernel RECT/ELLIPSE/CROSS
- Đo diện tích trước/sau

**Input**: `input/parts/gapped.png`
**Output**: `output/bai-2-closing/`

### Bài 3: Trích biên

**Mục tiêu**: Trích xuất đường biên bằng Morphological Gradient.

**Kỹ thuật**:
- Gradient = Dilation - Erosion
- So sánh với Canny Edge
- Phân tích độ dày biên

**Input**: `input/objects/sample.png`
**Output**: `output/bai-3-gradient/`

### Bài 4: Đếm đồng xu

**Mục tiêu**: Tách và đếm các đồng xu chạm nhau bằng Watershed.

**Kỹ thuật**:
- Opening khử nhiễu
- Distance Transform
- Watershed Segmentation
- Sure Foreground/Background

**Input**: `input/coins/touching.jpg`
**Output**: `output/bai-4-watershed/`

### Bài 5: Phân đoạn ký tự

**Mục tiêu**: Tách từng ký tự trên biển số để chuẩn bị OCR.

**Kỹ thuật**:
- Opening loại nhiễu nhỏ
- Closing nối nét đứt
- Connected Components
- Lọc theo kích thước

**Input**: `input/plates/plate.jpg`
**Output**: `output/bai-5-character-segmentation/`

### Bài 6: Đo đường kính hạt

**Mục tiêu**: Phân loại hạt/lỗ theo kích thước (nhỏ/vừa/lớn).

**Kỹ thuật**:
- Closing làm tròn
- Find Contours
- Tính diện tích
- Phân cụm theo percentile (33%, 66%)

**Input**: `input/surface/holes.png`
**Output**: `output/bai-6-particle-measurement/`

### Bài 7: Xóa pixel thừa

**Mục tiêu**: Pruning biên/skeleton bằng Hit-or-Miss Transform.

**Kỹ thuật**:
- Structuring Elements 8 hướng
- Hit-or-Miss Transform
- Lặp đến hội tụ
- Xóa spurs (gai)

**Input**: `input/edges/jagged.png`
**Output**: `output/bai-7-pruning/`

### Bài 8: Tách tiền cảnh

**Mục tiêu**: Tách Core và Rim của vật thể.

**Kỹ thuật**:
- Core = Erosion(A, B)
- Rim = A - Core
- Phân tích với kernel khác nhau
- Overlay màu sắc

**Input**: `input/conveyor/items.png`
**Output**: `output/bai-8-foreground-extraction/`

### Bài 9: Khử nền không đều

**Mục tiêu**: Loại bỏ chiếu sáng không đồng đều.

**Kỹ thuật**:
- Top-hat = Img - Opening
- Black-hat = Closing - Img
- Corrected = Img + Top-hat - Black-hat
- So sánh histogram

**Input**: `input/docs/uneven.jpg`
**Output**: `output/bai-9-background-removal/`

## Tính năng chính

### 1. Tự động tạo ảnh mẫu

Nếu thiếu ảnh input, mỗi bài tập sẽ **TỰ ĐỘNG TẠO** ảnh mẫu phù hợp.

```bash
# Hoặc tạo tất cả ảnh mẫu cùng lúc
cd input
python generate_samples.py
```

### 2. Console output chi tiết

Mỗi bài tập hiển thị:
- Tiến trình từng bước
- Thông số kỹ thuật
- Thống kê kết quả
- Phân tích chi tiết

### 3. Visualization đầy đủ

- So sánh trước/sau
- Các bước trung gian
- Biểu đồ thống kê
- Zoom chi tiết

### 4. Lưu kết quả

Tất cả kết quả được lưu vào `output/`:
- Ảnh xử lý
- Biểu đồ phân tích
- File thống kê (nếu có)

## Requirements

```
opencv-python>=4.8.0
numpy>=1.24.0
scikit-image>=0.21.0
scipy>=1.11.0
matplotlib>=3.7.0
```

## Kiến thức áp dụng

### Các phép toán cơ bản

1. **Erosion (Xói mòn)**: Thu nhỏ vật thể
2. **Dilation (Giãn nở)**: Mở rộng vật thể
3. **Opening**: Erosion → Dilation (khử nhiễu)
4. **Closing**: Dilation → Erosion (lấp lỗ)
5. **Gradient**: Dilation - Erosion (trích biên)
6. **Top-hat**: Img - Opening (vật thể sáng)
7. **Black-hat**: Closing - Img (vật thể tối)

### Ứng dụng thực tế

- OCR (Optical Character Recognition)
- Kiểm tra chất lượng công nghiệp
- Phân tích y sinh (tế bào, mô)
- Xử lý ảnh vệ tinh
- Nhận dạng biển số
- Phân đoạn ảnh y tế

## Tác giả

**Ph.D Phan Thanh Toàn**
Giáo trình: T61-78 Xử lý hình thái

## License

Tài liệu học tập - Chỉ sử dụng cho mục đích giáo dục.

## Tham khảo

- OpenCV Documentation: https://docs.opencv.org/
- Digital Image Processing - Gonzalez & Woods
- Morphological Image Processing - Pierre Soille

---

**Lưu ý**: Đảm bảo đã cài đặt Python 3.8+ và tất cả dependencies trước khi chạy.

Chúc bạn học tốt!
