# REQ-5: Tạo Code và Documents cho Các Bài Lab Image Processing

## 📋 Mục Tiêu

Tạo đầy đủ code implementation và documents cho các bài thực hành Image Processing theo cấu trúc mẫu của `T1-bieu-dien-va-thu-nhan-anh`, bao gồm:
- **T21-40**: Tách biên (10 Bài)
- **T61-78**: Xử lý hình thái (9 Bài)
- **T79-99**: Phân vùng ảnh (10 Bài)

## 🎯 Yêu Cầu Chi Tiết

### 1. Ngôn Ngữ
- ✅ **Document & Comment**: Tiếng Việt (trừ các thuật ngữ chuyên ngành)
- ✅ **Tên biến/hàm trong code**: Tiếng Anh
- ✅ **Console output**: Tiếng Việt

### 2. Cấu Trúc Folder
```
code-implement/
├── T21-tach-bien/              # T21-40 Tách biên.pdf
├── T61-xu-ly-hinh-thai/        # T61-78 Xử lý hình thái.pdf
└── T79-phan-vung-anh/          # T79-99 Phân vùng ảnh.pdf

documents/
├── T21-tach-bien/
├── T61-xu-ly-hinh-thai/
└── T79-phan-vung-anh/
```

### 3. Cấu Trúc Mỗi Folder Code (ví dụ: T21-tach-bien/)
```
T21-tach-bien/
├── bai-1-edge-detectors/       # Bài 1
│   └── compare.py
├── bai-2-document-scanning/    # Bài 2
│   └── scan.py
├── ...                         # Các bài khác
├── input/
│   ├── sample-images/
│   ├── README.md               # Hướng dẫn chuẩn bị input
│   └── generate_samples.py     # Script tạo ảnh mẫu tự động
├── output/                     # Tự tạo khi chạy
├── README.md                   # Hướng dẫn tổng quan
├── requirements.txt            # Dependencies
├── run_all.sh                  # Script chạy tất cả (Linux/Mac)
└── run_all.bat                 # Script chạy tất cả (Windows)
```

### 4. Cấu Trúc Mỗi Folder Documents (ví dụ: T21-tach-bien/)
```
T21-tach-bien/
├── theory/                     # Lý thuyết nền tảng
│   ├── 01-edge-detection-fundamentals.md
│   ├── 02-gradient-operators.md
│   ├── 03-canny-edge-detection.md
│   └── ...
├── exercises/                  # Giải thích từng bài (optional)
│   ├── bai-1-edge-detectors.md
│   └── ...
├── code-reading-guide/         # 🔥 MỚI: Hướng dẫn đọc code
│   ├── bai-1-how-to-read.md
│   ├── bai-2-how-to-read.md
│   └── ...
└── README.md                   # Tổng quan
```

### 5. Nội Dung Code Mỗi Bài

#### 5.1 Header Comment (Tiếng Việt)
```python
"""
Bài X — Tên Bài

Mục tiêu:
- Mục tiêu 1
- Mục tiêu 2

Kỹ thuật sử dụng:
- Kỹ thuật 1
- Kỹ thuật 2

Input:
- Ảnh gì, format gì
- Yêu cầu về ảnh

Output:
- Kết quả gì
- Lưu ở đâu

Tác giả đề bài: TS. Phan Thanh Toàn
"""
```

#### 5.2 Code Structure
```python
# Import libraries
import cv2
import numpy as np
import os

# Định nghĩa hàm xử lý (nếu cần)
def process_function():
    """Giải thích hàm bằng tiếng Việt"""
    pass

# Main execution
if __name__ == "__main__":
    # 1. Thiết lập đường dẫn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "...")
    output_dir = os.path.join(script_dir, "..", "output")

    # 2. Tạo output folder
    os.makedirs(output_dir, exist_ok=True)

    # 3. Kiểm tra input, tự tạo nếu không có
    if not os.path.exists(input_path):
        print(f"WARNING: {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")
        # Code tạo ảnh mẫu

    # 4. Đọc ảnh
    img = cv2.imread(input_path)

    # 5. Xử lý
    # ...

    # 6. Hiển thị kết quả
    print("="*70)
    print("BÀI X: TÊN BÀI")
    print("="*70)
    # In metrics, kết quả

    # 7. Lưu output
    cv2.imwrite(output_path, result)
    print(f"\nĐã lưu kết quả tại: {output_path}")
```

#### 5.3 Code Phải Tự Động Tạo Ảnh Mẫu
- Nếu không tìm thấy ảnh input → tự tạo ảnh mẫu phù hợp
- Đảm bảo code chạy được ngay mà không cần chuẩn bị ảnh thủ công

### 6. File `README.md` Trong Code Folder

Nội dung bắt buộc:
- ✅ Tổng quan topic
- ✅ Cấu trúc thư mục
- ✅ Hướng dẫn cài đặt (Python, dependencies)
- ✅ Hướng dẫn chuẩn bị input (3 cách: tạo tự động, tự chuẩn bị, để code tự tạo)
- ✅ Cách chạy (chạy tất cả, chạy từng bài)
- ✅ Mô tả chi tiết từng bài (mục tiêu, kỹ năng, output)
- ✅ Troubleshooting
- ✅ Link tới documents

### 7. File `requirements.txt`
Danh sách thư viện cần thiết:
```
opencv-python>=4.8.0
numpy>=1.24.0
scikit-image>=0.21.0
matplotlib>=3.7.0
scipy>=1.11.0
```

### 8. Script `run_all.sh` và `run_all.bat`
- Chạy tất cả bài tập theo thứ tự
- Hiển thị progress
- Báo lỗi nếu có

### 9. File `code-reading-guide/` - Hướng Dẫn Đọc Code

🔥 **QUAN TRỌNG**: Tạo hướng dẫn đọc code cho từng bài để hiểu nhanh nhất

**Template: `bai-X-how-to-read.md`**
```markdown
# Hướng Dẫn Đọc Code: Bài X - Tên Bài

## 📖 Mục Tiêu Bài Tập
- [Tóm tắt mục tiêu]

## 🎯 Kỹ Thuật Chính
- Kỹ thuật 1: [Giải thích ngắn gọn]
- Kỹ thuật 2: [Giải thích ngắn gọn]

## 📂 File Code
`bai-X-tenbai/script.py`

## 🗺️ Sơ Đồ Luồng Xử Lý
[Flowchart bằng text hoặc mermaid]

## 📝 Đọc Code Theo Thứ Tự

### Bước 1: Import và Setup
- **Dòng XX-YY**: Import thư viện
- **Giải thích**: Tại sao cần thư viện này

### Bước 2: Hàm Xử Lý Chính
- **Dòng XX-YY**: Hàm `function_name()`
- **Input**: [Mô tả input]
- **Output**: [Mô tả output]
- **Thuật toán**:
  1. Bước 1
  2. Bước 2
- **Tại sao làm vậy**: [Giải thích lý do]

### Bước 3: Main Execution
- **Dòng XX-YY**: Đọc ảnh
- **Dòng XX-YY**: Xử lý
- **Dòng XX-YY**: Lưu kết quả

## 🔍 Các Đoạn Code Quan Trọng

### 1. Thuật toán core (dòng XX-YY)
```python
[Code snippet]
```
**Giải thích chi tiết**:
[Giải thích từng dòng]

### 2. Xử lý edge case (dòng XX-YY)
[...]

## 💡 Hiểu Sâu Hơn

### Câu hỏi 1: Tại sao dùng [kỹ thuật X]?
**Trả lời**: [Giải thích]

### Câu hỏi 2: Parameters ảnh hưởng như thế nào?
**Trả lời**: [Giải thích]

## 🧪 Thử Nghiệm

Để hiểu rõ hơn, thử:
1. Thay đổi parameter X → Quan sát kết quả
2. Thử với ảnh khác nhau → So sánh
3. Comment dòng Y → Xem ảnh hưởng

## 📚 Tham Khảo
- Theory: `documents/TX-topic/theory/YY-theory-file.md`
- OpenCV docs: [Link]
```

### 10. Documents - Theory Files

Mỗi file lý thuyết cần có:
- ✅ Khái niệm cơ bản (tiếng Việt)
- ✅ Công thức toán học (nếu có)
- ✅ Ưu/nhược điểm
- ✅ Khi nào sử dụng
- ✅ Ví dụ minh họa (nếu có)
- ✅ Code snippet (nếu cần)
- ✅ Tham khảo

### 11. Documents - README.md

Tổng quan về topic, danh sách lý thuyết, link tới code

---

## 📦 DANH SÁCH BÀI CẦN TẠO

### Topic 1: T21-40 Tách Biên (10 Bài)

Folder: `T21-tach-bien/`

**Bài tập:**
1. ⭐⭐⭐⭐⭐ **Bài 1**: So sánh edge detectors (Roberts, Prewitt, Sobel, Scharr) + noise
   - File: `bai-1-edge-detectors/compare.py`

2. **Bài 2**: Document scanning với perspective transform
   - File: `bai-2-document-scanning/scan.py`

3. ⭐⭐⭐⭐⭐ **Bài 3**: Lane detection (Canny + Hough Lines)
   - File: `bai-3-lane-detection/detect.py`

4. **Bài 4**: Surface defect detection (Laplacian)
   - File: `bai-4-defect-detection/detect.py`

5. **Bài 5**: Coin counting (Canny + HoughCircles)
   - File: `bai-5-coin-counting/count.py`

6. ⭐⭐⭐⭐⭐ **Bài 6**: Product cropping (Contour detection)
   - File: `bai-6-product-cropping/crop.py`

7. **Bài 7**: Crack detection (LoG + skeleton)
   - File: `bai-7-crack-detection/detect.py`

8. **Bài 8**: Leaf measurement (perimeter, area, serration)
   - File: `bai-8-leaf-measurement/measure.py`

9. **Bài 9**: Object measurement with calibration
   - File: `bai-9-object-measurement/measure.py`

10. **Bài 10**: Document deskewing (Hough Lines)
    - File: `bai-10-deskewing/deskew.py`

**Theory files cần tạo:**
- `01-edge-detection-fundamentals.md` - Khái niệm cơ bản về edge detection
- `02-gradient-operators.md` - Roberts, Prewitt, Sobel, Scharr
- `03-canny-edge-detection.md` - Canny algorithm chi tiết
- `04-laplacian-log.md` - Laplacian và LoG
- `05-hough-transform.md` - Hough Lines và Circles
- `06-contour-detection.md` - Contours và hierarchy
- `07-perspective-transform.md` - Perspective correction

---

### Topic 2: T61-78 Xử Lý Hình Thái (9 Bài)

Folder: `T61-xu-ly-hinh-thai/`

**Bài tập:**
1. ⭐⭐⭐⭐⭐ **Bài 1**: Opening (loại nhiễu salt-and-pepper)
   - File: `bai-1-opening/denoise.py`

2. ⭐⭐⭐⭐⭐ **Bài 2**: Closing (lấp lỗ, nối biên)
   - File: `bai-2-closing/fill_holes.py`

3. ⭐⭐⭐⭐ **Bài 3**: Morphological gradient (edge extraction)
   - File: `bai-3-gradient/extract_edges.py`

4. **Bài 4**: Watershed (tách đối tượng chồng lấn)
   - File: `bai-4-watershed/separate.py`

5. **Bài 5**: Character segmentation
   - File: `bai-5-character-segmentation/segment.py`

6. **Bài 6**: Measuring particle sizes
   - File: `bai-6-particle-measurement/measure.py`

7. **Bài 7**: Pruning (hit-or-miss transform)
   - File: `bai-7-pruning/prune.py`

8. ⭐⭐⭐⭐ **Bài 8**: Foreground extraction
   - File: `bai-8-foreground-extraction/extract.py`

9. **Bài 9**: Background removal (top-hat/black-hat)
   - File: `bai-9-background-removal/remove.py`

**Theory files cần tạo:**
- `01-morphology-fundamentals.md` - Khái niệm cơ bản
- `02-structuring-elements.md` - Structuring elements
- `03-erosion-dilation.md` - Erosion và Dilation
- `04-opening-closing.md` - Opening và Closing
- `05-morphological-gradient.md` - Gradient, top-hat, black-hat
- `06-hit-or-miss.md` - Hit-or-miss transform
- `07-watershed-algorithm.md` - Watershed algorithm

---

### Topic 3: T79-99 Phân Vùng Ảnh (10 Bài)

Folder: `T79-phan-vung-anh/`

**Bài tập:**
1. **Bài 1**: Global thresholding (iterative method)
   - File: `bai-1-global-thresholding/threshold.py`

2. ⭐⭐⭐⭐ **Bài 2**: Otsu's method
   - File: `bai-2-otsu/threshold.py`

3. ⭐⭐⭐⭐⭐ **Bài 3**: Adaptive thresholding (Mean/Gaussian)
   - File: `bai-3-adaptive-thresholding/threshold.py`

4. **Bài 4**: Bayes/Maximum Likelihood thresholding
   - File: `bai-4-bayes-ml/threshold.py`

5. **Bài 5**: Edge detection + Hough Lines
   - File: `bai-5-edge-hough/detect.py`

6. ⭐⭐⭐⭐⭐ **Bài 6**: Region growing
   - File: `bai-6-region-growing/grow.py`

7. **Bài 7**: Split-merge segmentation
   - File: `bai-7-split-merge/segment.py`

8. **Bài 8**: K-means clustering
   - File: `bai-8-kmeans/cluster.py`

9. ⭐⭐⭐⭐⭐ **Bài 9**: Motion segmentation (Frame differencing + MOG2)
   - File: `bai-9-motion-segmentation/segment.py`

10. **Bài 10**: Watershed segmentation
    - File: `bai-10-watershed/segment.py`

**Theory files cần tạo:**
- `01-segmentation-fundamentals.md` - Khái niệm cơ bản
- `02-thresholding-methods.md` - Global, Otsu, Adaptive
- `03-region-based-methods.md` - Region growing, split-merge
- `04-clustering-methods.md` - K-means, Mean-shift
- `05-motion-detection.md` - Frame differencing, background subtraction
- `06-background-subtraction.md` - MOG2, KNN algorithms

---

## 🔄 QUY TRÌNH THỰC HIỆN

### Giai đoạn 1: T21-tach-bien (Ưu tiên cao)
1. ✅ Tạo cấu trúc folder
2. ✅ Đọc PDF `T21-40 Tách biên.pdf` để lấy code
3. ✅ Tạo 10 bài tập (code y nguyên từ PDF, comment tiếng Việt)
4. ✅ Tạo `input/README.md` + `generate_samples.py`
5. ✅ Tạo `requirements.txt`
6. ✅ Tạo `run_all.sh` và `run_all.bat`
7. ✅ Tạo `README.md` tổng quan
8. ✅ Tạo 7 theory files trong `documents/T21-tach-bien/theory/`
9. ✅ Tạo 10 code-reading-guide files
10. ✅ Tạo `documents/T21-tach-bien/README.md`

### Giai đoạn 2: T61-xu-ly-hinh-thai (Ưu tiên cao)
[Lặp lại quy trình trên]

### Giai đoạn 3: T79-phan-vung-anh (Ưu tiên cao)
[Lặp lại quy trình trên]

---

## ✅ CHECKLIST HOÀN THÀNH MỖI TOPIC

### Code Implementation
- [ ] Tạo folder structure đúng
- [ ] 10 (hoặc 9) bài tập với code đầy đủ
- [ ] Mỗi code có header comment tiếng Việt
- [ ] Code tự tạo ảnh mẫu nếu thiếu input
- [ ] `input/README.md` hướng dẫn chuẩn bị ảnh
- [ ] `input/generate_samples.py` tạo ảnh mẫu
- [ ] `requirements.txt` đầy đủ
- [ ] `run_all.sh` và `run_all.bat` chạy được
- [ ] `README.md` đầy đủ theo template
- [ ] Test chạy tất cả code thành công

### Documents
- [ ] Theory files đầy đủ (tiếng Việt)
- [ ] Code reading guide cho từng bài
- [ ] `README.md` tổng quan
- [ ] Link giữa code và documents đúng

---

## 📝 LƯU Ý QUAN TRỌNG

### 1. Về Code
- ⚠️ **Code y nguyên từ PDF**, chỉ thêm comment tiếng Việt
- ⚠️ Phải tự động tạo ảnh mẫu nếu thiếu input
- ⚠️ Console output phải rõ ràng, dễ hiểu
- ⚠️ Xử lý error gracefully (file not found, wrong format, etc.)

### 2. Về Documents
- ⚠️ Tiếng Việt rõ ràng, dễ hiểu
- ⚠️ Code reading guide phải giúp người đọc hiểu nhanh
- ⚠️ Theory phải liên kết với code implementation
- ⚠️ Có ví dụ minh họa khi cần

### 3. Về Input
- ⚠️ Hướng dẫn 3 cách chuẩn bị input:
  1. Tạo tự động bằng `generate_samples.py`
  2. Tự chuẩn bị ảnh theo hướng dẫn
  3. Để code tự tạo khi chạy (fallback)

### 4. Về Thứ Tự Ưu Tiên
- 🔥 Ưu tiên **BÀI QUAN TRỌNG** (⭐⭐⭐⭐⭐) trước
- 🔥 Tạo theo thứ tự: T21 → T61 → T79 (theo độ quan trọng cho final project)

---

## 🎯 KẾT QUẢ MONG ĐỢI

Sau khi hoàn thành req-5:

✅ Có 3 folder code-implement hoàn chỉnh
✅ Có 3 folder documents đầy đủ
✅ Tất cả code chạy được ngay (không cần chuẩn bị thủ công)
✅ Có hướng dẫn đọc code chi tiết cho từng bài
✅ Có đủ tài liệu lý thuyết để hiểu rõ

→ **Người dùng có thể học từng bài một cách hiệu quả nhất để chuẩn bị cho final project**

---

## 📚 THAM KHẢO

- Mẫu: `code-implement/T1-bieu-dien-va-thu-nhan-anh/`
- Mẫu: `documents/T1-bieu-dien-va-thu-nhan-anh/`
- Learning roadmap: `requirements/learning-roadmap.md`
- Final project: `requirements/req-4.md`
