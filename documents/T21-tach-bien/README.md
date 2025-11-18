# Tài Liệu T21-40: Tách Biên (Edge Detection)

## 📋 Tổng Quan

Folder này chứa **tài liệu lý thuyết** và **hướng dẫn đọc code** cho các bài tập về **Tách Biên** (T21-40).

**Nội dung**:
- 7 bài lý thuyết chuyên sâu
- 10 hướng dẫn đọc code chi tiết
- 100% Tiếng Việt (trừ technical terms)

**Nguồn**: Dựa trên PDF T21-40 Tách Biên từ giáo trình Image Processing

## 📁 Cấu Trúc Thư Mục

```
documents/T21-tach-bien/
├── README.md                          (File này)
│
├── theory/                            (7 files lý thuyết)
│   ├── 01-edge-detection-fundamentals.md
│   ├── 02-canny-edge-detection.md
│   ├── 03-hough-transform.md
│   ├── 04-contour-detection.md
│   ├── 05-perspective-transform.md
│   ├── 06-morphological-edge-processing.md
│   └── 07-measurement-and-calibration.md
│
└── code-reading-guide/                (10 files hướng dẫn)
    ├── bai-1-how-to-read.md  → Edge detectors comparison
    ├── bai-2-how-to-read.md  → Document scanning
    ├── bai-3-how-to-read.md  → Lane detection
    ├── bai-4-how-to-read.md  → Scratch detection
    ├── bai-5-how-to-read.md  → Coin counting
    ├── bai-6-how-to-read.md  → Product cropping
    ├── bai-7-how-to-read.md  → Crack detection
    ├── bai-8-how-to-read.md  → Leaf measurement
    ├── bai-9-how-to-read.md  → Object measurement
    └── bai-10-how-to-read.md → Document deskew
```

## 📚 Theory Files - Lý Thuyết

### 1. [Edge Detection Fundamentals](theory/01-edge-detection-fundamentals.md)

**Nội dung**: Roberts, Prewitt, Sobel, Scharr operators
- Nguyên lý gradient 2D
- So sánh các toán tử
- Gaussian smoothing
- Thresholding techniques

**Áp dụng**: Bài 1, Bài 4

---

### 2. [Canny Edge Detection](theory/02-canny-edge-detection.md)

**Nội dung**: Thuật toán Canny 5 bước
- Non-maximum suppression
- Double thresholding
- Hysteresis edge tracking
- Auto Canny

**Áp dụng**: Bài 2, Bài 3, Bài 6

---

### 3. [Hough Transform](theory/03-hough-transform.md)

**Nội dung**: Phát hiện đường thẳng và đường tròn
- Hough Lines (Standard & Probabilistic)
- Hough Circles
- Parameter tuning
- Lane detection workflow

**Áp dụng**: Bài 3 (Lines), Bài 5 (Circles)

---

### 4. [Contour Detection](theory/04-contour-detection.md)

**Nội dụng**: Tìm và phân tích contours
- findContours() modes
- Contour properties (area, perimeter, moments)
- Bounding rectangles
- Shape features

**Áp dụng**: Bài 6, Bài 8

---

### 5. [Perspective Transform](theory/05-perspective-transform.md)

**Nội dung**: Sửa góc nhìn và xoay ảnh
- 4-point perspective transform
- Document scanning
- Rotation correction (deskew)
- Homography matrix

**Áp dụng**: Bài 2, Bài 10

---

### 6. [Morphological Edge Processing](theory/06-morphological-edge-processing.md)

**Nội dung**: Xử lý biên với morphology
- Morphological gradient
- Top-hat & Black-hat transforms
- Structuring elements
- Directional morphology

**Áp dụng**: Bài 4 (Scratch), Bài 7 (Crack)

---

### 7. [Measurement and Calibration](theory/07-measurement-and-calibration.md)

**Nội dung**: Đo đạc vật thể trong ảnh
- Pixels per metric calibration
- Reference object methods
- Distance & area measurement
- Accuracy & error sources

**Áp dụng**: Bài 9

---

## 🔍 Code-Reading-Guides - Hướng Dẫn Đọc Code

### Cấu Trúc Mỗi Guide

Mỗi hướng dẫn bao gồm 8 phần:

1. **Tổng Quan** - Mục tiêu bài tập (2-3 dòng)
2. **Input/Output** - Files và format
3. **Thuật Toán Chính** - Các bước với số dòng code
4. **Code Quan Trọng** - 5 đoạn code quan trọng nhất + giải thích
5. **Tham Số Quan Trọng** - Bảng tham số có thể điều chỉnh
6. **Kết Quả Mong Đợi** - Output trông như thế nào
7. **Lỗi Thường Gặp** - 3 lỗi phổ biến + cách fix
8. **Mở Rộng** - 5 gợi ý cải tiến

### Danh Sách Guides

| Guide | Bài Tập | Kỹ Thuật Chính | Độ Khó |
|-------|---------|----------------|--------|
| [bai-1-how-to-read.md](code-reading-guide/bai-1-how-to-read.md) | Edge Detectors Comparison | Roberts, Prewitt, Sobel, Scharr | ⭐⭐ |
| [bai-2-how-to-read.md](code-reading-guide/bai-2-how-to-read.md) | Document Scanning | Perspective Transform | ⭐⭐⭐⭐ |
| [bai-3-how-to-read.md](code-reading-guide/bai-3-how-to-read.md) | Lane Detection | Sobel + Hough Lines | ⭐⭐⭐⭐ |
| [bai-4-how-to-read.md](code-reading-guide/bai-4-how-to-read.md) | Scratch Detection | Morphological Gradient | ⭐⭐⭐ |
| [bai-5-how-to-read.md](code-reading-guide/bai-5-how-to-read.md) | Coin Counting | Hough Circles | ⭐⭐⭐ |
| [bai-6-how-to-read.md](code-reading-guide/bai-6-how-to-read.md) | Product Cropping | Canny + Contours | ⭐⭐⭐⭐ |
| [bai-7-how-to-read.md](code-reading-guide/bai-7-how-to-read.md) | Crack Detection | Top-hat Transform | ⭐⭐⭐ |
| [bai-8-how-to-read.md](code-reading-guide/bai-8-how-to-read.md) | Leaf Measurement | Contour Area | ⭐⭐ |
| [bai-9-how-to-read.md](code-reading-guide/bai-9-how-to-read.md) | Object Measurement | Reference Calibration | ⭐⭐⭐⭐ |
| [bai-10-how-to-read.md](code-reading-guide/bai-10-how-to-read.md) | Document Deskew | Rotation Correction | ⭐⭐⭐ |

---

## 🎯 Lộ Trình Học Tập Đề Xuất

### Cấp Độ 1: Cơ Bản (Tuần 1-2)

1. **Đọc lý thuyết**:
   - 01-edge-detection-fundamentals.md
   - 04-contour-detection.md

2. **Thực hành**:
   - Bài 1: Edge Detectors Comparison (⭐⭐)
   - Bài 8: Leaf Measurement (⭐⭐)

**Mục tiêu**: Hiểu gradient, Sobel, contours cơ bản

---

### Cấp Độ 2: Trung Bình (Tuần 3-4)

1. **Đọc lý thuyết**:
   - 02-canny-edge-detection.md
   - 03-hough-transform.md
   - 06-morphological-edge-processing.md

2. **Thực hành**:
   - Bài 4: Scratch Detection (⭐⭐⭐)
   - Bài 5: Coin Counting (⭐⭐⭐)
   - Bài 7: Crack Detection (⭐⭐⭐)

**Mục tiêu**: Canny, Hough, Morphology

---

### Cấp Độ 3: Nâng Cao (Tuần 5-6) ⭐ QUAN TRỌNG CHO ĐỒ ÁN

1. **Đọc lý thuyết**:
   - 05-perspective-transform.md
   - 07-measurement-and-calibration.md

2. **Thực hành**:
   - Bài 2: Document Scanning (⭐⭐⭐⭐)
   - Bài 3: Lane Detection (⭐⭐⭐⭐)
   - Bài 6: Product Cropping (⭐⭐⭐⭐)
   - Bài 9: Object Measurement (⭐⭐⭐⭐)

**Mục tiêu**: Hoàn chỉnh pipeline phức tạp

---

## 📊 Thống Kê

### Theory Files
- **Số lượng**: 7 files
- **Tổng dòng**: ~5,500 dòng
- **Kích thước**: ~180 KB
- **Nội dung**: 40+ code examples, 30+ công thức toán, 25+ bảng so sánh

### Code-Reading-Guides
- **Số lượng**: 10 files
- **Tổng dòng**: ~2,650 dòng
- **Kích thước**: ~86 KB
- **Nội dung**: 50+ code segments, 30+ lỗi + fix, 50+ gợi ý mở rộng

### Tổng Cộng
- **17 files** tài liệu
- **~8,150 dòng** nội dung
- **~266 KB** kích thước
- **100% Tiếng Việt** (trừ technical terms)

---

## 🔗 Liên Kết

### Code Implementation
**Folder code**: [/code-implement/T21-tach-bien/](/code-implement/T21-tach-bien/)

Mỗi bài tập có:
- Script Python với Vietnamese comments
- Auto-generate sample images
- Detailed console output
- Visualization kết quả

### PDF Gốc
**Nguồn lý thuyết**: `T21-40 Tách biên.pdf`

### Tài Liệu Khác
- [T1 - Biểu Diễn và Thu Nhận Ảnh](/documents/T1-bieu-dien-va-thu-nhan-anh/)
- [T61 - Xử Lý Hình Thái](/documents/T61-xu-ly-hinh-thai/)
- [T79 - Phân Vùng Ảnh](/documents/T79-phan-vung-anh/)

---

## 💡 Mẹo Sử Dụng

### Khi Đọc Lý Thuyết
1. Đọc **Tổng Quan** để nắm ý tưởng
2. Tập trung vào **Code Examples** để hiểu cách dùng
3. Xem **So Sánh** để biết khi nào dùng phương pháp nào
4. Thử **Kỹ Thuật Nâng Cao** khi đã hiểu cơ bản

### Khi Đọc Code
1. Đọc **Tổng Quan** + **Thuật Toán Chính** trước
2. Mở code song song, tìm đến số dòng được dẫn
3. Đọc kỹ **Code Quan Trọng** (5 đoạn)
4. Chạy code, so sánh với **Kết Quả Mong Đợi**
5. Gặp lỗi → Xem **Lỗi Thường Gặp**
6. Muốn cải tiến → Xem **Mở Rộng**

### Tips
- ⭐⭐⭐⭐ = Quan trọng cho đồ án cuối kỳ
- Làm theo thứ tự từ dễ → khó
- Mỗi bài nên chạy code + đọc guide + đọc theory liên quan

---

## 🆘 Hỗ Trợ

### Tài Liệu Tham Khảo Thêm

**Sách**:
- Digital Image Processing (Gonzalez & Woods) - Chapter 10
- Computer Vision: Algorithms and Applications (Szeliski) - Chapter 4
- Learning OpenCV 4 (Kaehler & Bradski) - Chapter 5-7

**Online**:
- [OpenCV Documentation](https://docs.opencv.org/4.x/)
- [PyImageSearch Blog](https://pyimagesearch.com/)
- [Mất Khởi Edge Detection](https://en.wikipedia.org/wiki/Edge_detection)

**Papers Quan Trọng**:
- Canny, J. (1986). A Computational Approach to Edge Detection
- Duda & Hart (1972). Use of the Hough Transformation
- Sobel, I. (1968). An Isotropic 3×3 Image Gradient Operator

---

## ✅ Checklist Hoàn Thành

Sau khi học xong T21, bạn nên:

- [ ] Hiểu được 4 toán tử gradient cơ bản
- [ ] Biết cách dùng Canny edge detector
- [ ] Thực hiện được Hough Lines và Circles
- [ ] Tìm và phân tích được contours
- [ ] Làm được perspective transform
- [ ] Áp dụng được morphological operations
- [ ] Đo được kích thước vật thể trong ảnh
- [ ] Hoàn thành 10/10 bài tập

**Mục tiêu cuối**: Tự tin làm đồ án liên quan đến edge detection!

---

**Tác giả**: Dựa trên PDF T21-40 Tách Biên
**Cập nhật**: 2025
**Phiên bản**: 1.0
