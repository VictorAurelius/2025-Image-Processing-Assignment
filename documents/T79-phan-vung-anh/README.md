# Tài Liệu T79-99: Phân Vùng Ảnh (Image Segmentation)

## 📋 Tổng Quan

Folder này chứa **tài liệu lý thuyết** và **hướng dẫn đọc code** cho các bài tập về **Phân Vùng Ảnh** (T79-99).

**Nội dung**:
- 6 bài lý thuyết chuyên sâu
- 10 hướng dẫn đọc code chi tiết
- 100% Tiếng Việt (trừ technical terms)

**Nguồn**: Dựa trên PDF T79-99 Phân Vùng Ảnh từ giáo trình Image Processing

## 📁 Cấu Trúc Thư Mục

```
documents/T79-phan-vung-anh/
├── README.md                          (File này)
│
├── theory/                            (6 files lý thuyết)
│   ├── 01-thresholding-methods.md
│   ├── 02-region-based-segmentation.md
│   ├── 03-clustering-segmentation.md
│   ├── 04-edge-based-segmentation.md
│   ├── 05-motion-segmentation.md
│   └── 06-segmentation-evaluation.md
│
└── code-reading-guide/                (10 files hướng dẫn)
    ├── bai-1-how-to-read.md  → Global thresholding
    ├── bai-2-how-to-read.md  → Otsu thresholding
    ├── bai-3-how-to-read.md  → Adaptive thresholding
    ├── bai-4-how-to-read.md  → Bayes-ML thresholding
    ├── bai-5-how-to-read.md  → Edge + Hough
    ├── bai-6-how-to-read.md  → Region growing
    ├── bai-7-how-to-read.md  → Split-merge
    ├── bai-8-how-to-read.md  → K-means clustering
    ├── bai-9-how-to-read.md  → Motion segmentation
    └── bai-10-how-to-read.md → Watershed markers
```

## 📚 Theory Files - Lý Thuyết

### 1. [Thresholding Methods](theory/01-thresholding-methods.md)

**Nội dung**: Các phương pháp ngưỡng
- Global thresholding
- Otsu's method (optimal threshold)
- Adaptive thresholding (Mean, Gaussian)
- Bayes-ML thresholding

**Áp dụng**: Bài 1, 2, 3, 4

---

### 2. [Region-Based Segmentation](theory/02-region-based-segmentation.md)

**Nội dung**: Phân vùng dựa trên vùng
- Region growing
- Split-and-merge
- Felzenszwalb's algorithm
- Watershed segmentation

**Áp dụng**: Bài 6, 7, 10

---

### 3. [Clustering Segmentation](theory/03-clustering-segmentation.md)

**Nội dung**: Phân cụm ảnh
- K-means clustering
- Mean-shift
- Gaussian Mixture Models (GMM)
- DBSCAN

**Áp dụng**: Bài 8

---

### 4. [Edge-Based Segmentation](theory/04-edge-based-segmentation.md)

**Nội dung**: Phân vùng dựa biên
- Watershed from edges
- Active contours (Snakes)
- Level sets
- Graph cuts

**Áp dụng**: Bài 5, 10

---

### 5. [Motion Segmentation](theory/05-motion-segmentation.md)

**Nội dung**: Phân vùng chuyển động
- Frame differencing
- Background subtraction (MOG2, KNN)
- Optical flow
- Motion history image

**Áp dụng**: Bài 9

---

### 6. [Segmentation Evaluation](theory/06-segmentation-evaluation.md)

**Nội dung**: Đánh giá chất lượng phân vùng
- IoU (Intersection over Union)
- Dice coefficient
- F1 score, Precision, Recall
- Boundary metrics

**Áp dụng**: Tất cả các bài

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
| [bai-1-how-to-read.md](code-reading-guide/bai-1-how-to-read.md) | Global Thresholding | Fixed threshold | ⭐ |
| [bai-2-how-to-read.md](code-reading-guide/bai-2-how-to-read.md) | Otsu Thresholding | Otsu's method | ⭐⭐ |
| [bai-3-how-to-read.md](code-reading-guide/bai-3-how-to-read.md) | Adaptive Thresholding | Local thresholding | ⭐⭐⭐⭐ |
| [bai-4-how-to-read.md](code-reading-guide/bai-4-how-to-read.md) | Bayes-ML Threshold | Statistical methods | ⭐⭐⭐ |
| [bai-5-how-to-read.md](code-reading-guide/bai-5-how-to-read.md) | Edge + Hough | Canny + Hough | ⭐⭐⭐ |
| [bai-6-how-to-read.md](code-reading-guide/bai-6-how-to-read.md) | Region Growing | Seed-based growing | ⭐⭐⭐⭐ |
| [bai-7-how-to-read.md](code-reading-guide/bai-7-how-to-read.md) | Split-Merge | Quad-tree | ⭐⭐⭐ |
| [bai-8-how-to-read.md](code-reading-guide/bai-8-how-to-read.md) | K-means Clustering | K-means algorithm | ⭐⭐⭐ |
| [bai-9-how-to-read.md](code-reading-guide/bai-9-how-to-read.md) | Motion Segmentation | MOG2, Frame diff | ⭐⭐⭐⭐ |
| [bai-10-how-to-read.md](code-reading-guide/bai-10-how-to-read.md) | Watershed Markers | Marker-based watershed | ⭐⭐⭐ |

---

## 🎯 Lộ Trình Học Tập Đề Xuất

### Cấp Độ 1: Cơ Bản - Thresholding (Tuần 1-2)

1. **Đọc lý thuyết**:
   - 01-thresholding-methods.md

2. **Thực hành**:
   - Bài 1: Global Thresholding (⭐)
   - Bài 2: Otsu Thresholding (⭐⭐)
   - Bài 4: Bayes-ML Thresholding (⭐⭐⭐)

**Mục tiêu**: Hiểu các phương pháp ngưỡng cơ bản và nâng cao

---

### Cấp Độ 2: Trung Bình - Region & Clustering (Tuần 3-4)

1. **Đọc lý thuyết**:
   - 02-region-based-segmentation.md
   - 03-clustering-segmentation.md

2. **Thực hành**:
   - Bài 7: Split-Merge (⭐⭐⭐)
   - Bài 8: K-means Clustering (⭐⭐⭐)
   - Bài 10: Watershed Markers (⭐⭐⭐)

**Mục tiêu**: Region growing, clustering, watershed

---

### Cấp Độ 3: Nâng Cao (Tuần 5-6) ⭐ QUAN TRỌNG CHO ĐỒ ÁN

1. **Đọc lý thuyết**:
   - 04-edge-based-segmentation.md
   - 05-motion-segmentation.md
   - 06-segmentation-evaluation.md

2. **Thực hành**:
   - Bài 3: Adaptive Thresholding (⭐⭐⭐⭐) ← **CRITICAL**
   - Bài 6: Region Growing (⭐⭐⭐⭐) ← **CRITICAL**
   - Bài 9: Motion Segmentation (⭐⭐⭐⭐) ← **CRITICAL**

**Mục tiêu**: Hoàn chỉnh pipeline phức tạp, real-time segmentation

---

## 📊 Thống Kê

### Theory Files
- **Số lượng**: 6 files
- **Tổng dòng**: ~2,029 dòng
- **Kích thước**: ~96 KB
- **Nội dung**: 30+ code examples, 20+ công thức toán, 18+ bảng so sánh

### Code-Reading-Guides
- **Số lượng**: 10 files
- **Tổng dòng**: ~2,384 dòng
- **Kích thước**: ~60 KB
- **Nội dung**: 50+ code segments, 30+ lỗi + fix, 50+ gợi ý mở rộng

### Tổng Cộng
- **16 files** tài liệu
- **~4,413 dòng** nội dung
- **~156 KB** kích thước
- **100% Tiếng Việt** (trừ technical terms)

---

## 🔑 Khái Niệm Quan Trọng

### Phân Vùng Ảnh Là Gì?

**Image Segmentation** là quá trình chia ảnh thành các vùng (regions) có ý nghĩa:
- Mỗi vùng có tính chất tương tự (màu sắc, texture, cường độ)
- Các vùng khác nhau có tính chất khác biệt
- Mục đích: Tách foreground/background, phân loại vật thể

### Các Nhóm Phương Pháp

1. **Threshold-Based** (Dựa trên ngưỡng)
   - Đơn giản, nhanh
   - Phù hợp: Nền đơn giản, contrast cao
   - Bài 1, 2, 3, 4

2. **Region-Based** (Dựa trên vùng)
   - Xét tính chất vùng (similarity)
   - Phù hợp: Vùng đồng nhất
   - Bài 6, 7, 10

3. **Clustering** (Phân cụm)
   - Không cần seed/threshold
   - Phù hợp: Nhiều vùng, không biết trước
   - Bài 8

4. **Edge-Based** (Dựa trên biên)
   - Kết hợp edge detection
   - Phù hợp: Biên rõ ràng
   - Bài 5, 10

5. **Motion-Based** (Dựa trên chuyển động)
   - Cho video
   - Phù hợp: Tách vật động/tĩnh
   - Bài 9

---

## 🆚 So Sánh Các Phương Pháp

| Phương Pháp | Tốc Độ | Độ Chính Xác | Tự Động | Ứng Dụng |
|-------------|--------|--------------|---------|----------|
| **Global Threshold** | Rất nhanh ⭐⭐⭐ | Thấp | Không | Document scan |
| **Otsu** | Nhanh ⭐⭐⭐ | Trung bình ⭐⭐ | Có ⭐⭐⭐ | QC, OCR |
| **Adaptive** | Chậm | Cao ⭐⭐⭐ | Có ⭐⭐⭐ | Ánh sáng không đều |
| **Region Growing** | Chậm | Cao ⭐⭐⭐ | Bán tự động | Medical imaging |
| **K-means** | Trung bình ⭐⭐ | Trung bình ⭐⭐ | Có ⭐⭐⭐ | Color segmentation |
| **Watershed** | Chậm | Cao ⭐⭐⭐ | Bán tự động | Overlapping objects |
| **MOG2** | Nhanh ⭐⭐⭐ | Cao ⭐⭐⭐ | Có ⭐⭐⭐ | Video surveillance |

---

## 🔗 Liên Kết

### Code Implementation
**Folder code**: [/code-implement/T79-phan-vung-anh/](/code-implement/T79-phan-vung-anh/)

Mỗi bài tập có:
- Script Python với Vietnamese comments
- Auto-generate sample images
- Detailed console output
- Visualization kết quả
- So sánh nhiều phương pháp

### PDF Gốc
**Nguồn lý thuyết**: `T79-99 Phân vùng ảnh.pdf`

### Tài Liệu Khác
- [T1 - Biểu Diễn và Thu Nhận Ảnh](/documents/T1-bieu-dien-va-thu-nhan-anh/)
- [T21 - Tách Biên](/documents/T21-tach-bien/)
- [T61 - Xử Lý Hình Thái](/documents/T61-xu-ly-hinh-thai/)

---

## 💡 Mẹo Sử Dụng

### Khi Đọc Lý Thuyết
1. Đọc **Tổng Quan** để nắm ý tưởng
2. Hiểu **Nguyên Lý Toán Học** (quan trọng!)
3. Xem **Code Examples** để biết cách implement
4. So sánh **Ưu Nhược Điểm** để chọn phương pháp phù hợp
5. Thử **Kỹ Thuật Nâng Cao** khi đã hiểu cơ bản

### Khi Đọc Code
1. Đọc **Tổng Quan** + **Thuật Toán Chính** trước
2. Mở code song song, tìm đến số dòng được dẫn
3. Đọc kỹ **Code Quan Trọng** (5 đoạn)
4. Chạy code, so sánh với **Kết Quả Mong Đợi**
5. Gặp lỗi → Xem **Lỗi Thường Gặp**
6. Muốn cải tiến → Xem **Mở Rộng**

### Tips Quan Trọng
- **Adaptive Thresholding** (Bài 3): Quan trọng nhất cho đồ án ⭐⭐⭐⭐
- **Region Growing** (Bài 6): Hiểu rõ để custom cho bài toán riêng
- **Motion Segmentation** (Bài 9): Cần cho ứng dụng video real-time
- Làm theo thứ tự: Threshold → Region → Clustering → Motion
- Mỗi phương pháp có use case riêng, KHÔNG có phương pháp "tốt nhất"

---

## 🧪 Thực Hành

### Workflow Chuẩn

**Bước 1: Xác Định Bài Toán**
- Ảnh tĩnh hay video?
- Nền đơn giản hay phức tạp?
- Ánh sáng đều hay không đều?
- Cần real-time không?

**Bước 2: Chọn Phương Pháp**
- Nền đơn giản + contrast cao → **Global/Otsu**
- Ánh sáng không đều → **Adaptive**
- Nhiều vùng, không biết trước → **K-means**
- Vật thể chồng lấn → **Watershed**
- Video, tách foreground/background → **MOG2**

**Bước 3: Tiền Xử Lý**
- Gaussian blur (giảm nhiễu)
- Morphology (loại nhiễu, đóng khe hở)
- Color space conversion (nếu cần)

**Bước 4: Segmentation**
- Áp dụng phương pháp đã chọn
- Điều chỉnh tham số

**Bước 5: Hậu Xử Lý**
- Remove small regions (area < threshold)
- Morphology cleanup
- Contour filtering

**Bước 6: Đánh Giá**
- Visual inspection
- IoU, Dice score (nếu có ground truth)

---

## 🆘 Hỗ Trợ

### Tài Liệu Tham Khảo Thêm

**Sách**:
- Digital Image Processing (Gonzalez & Woods) - Chapter 10
- Computer Vision: Algorithms and Applications (Szeliski) - Chapter 5
- Learning OpenCV 4 (Kaehler & Bradski) - Chapter 9

**Online**:
- [OpenCV Documentation](https://docs.opencv.org/4.x/)
- [PyImageSearch: Segmentation](https://pyimagesearch.com/category/segmentation/)
- [Wikipedia: Image Segmentation](https://en.wikipedia.org/wiki/Image_segmentation)

**Papers Quan Trọng**:
- Otsu, N. (1979). A threshold selection method from gray-level histograms
- Felzenszwalb & Huttenlocher (2004). Efficient Graph-Based Image Segmentation
- Zivkovic, Z. (2004). Improved adaptive Gaussian mixture model (MOG2)

---

## ✅ Checklist Hoàn Thành

Sau khi học xong T79, bạn nên:

- [ ] Hiểu và implement được Global, Otsu, Adaptive thresholding
- [ ] Biết khi nào dùng phương pháp nào
- [ ] Implement được Region Growing
- [ ] Sử dụng được K-means cho color segmentation
- [ ] Hiểu và dùng được Watershed
- [ ] Implement motion segmentation với MOG2
- [ ] Đánh giá được chất lượng segmentation (IoU, Dice)
- [ ] Hoàn thành 10/10 bài tập
- [ ] Tự tin kết hợp nhiều phương pháp

**Mục tiêu cuối**: Tự tin làm đồ án liên quan đến segmentation!

---

## 🎓 Kết Hợp Với Các Topic Khác

### T21 (Edge Detection) + T79 (Segmentation)
- Watershed from edges (Bài 10)
- Edge + Hough (Bài 5)
- Contour-based segmentation

### T61 (Morphology) + T79 (Segmentation)
- Post-processing sau threshold
- Watershed markers với morphology
- Hole filling, noise removal

### T1 (Biểu Diễn) + T79 (Segmentation)
- Color space conversion (HSV, Lab)
- Histogram analysis
- Multi-channel segmentation

**Đồ án lớn**: Kết hợp T21 + T61 + T79 để tạo pipeline hoàn chỉnh!

---

**Tác giả**: Dựa trên PDF T79-99 Phân Vùng Ảnh
**Cập nhật**: 2025
**Phiên bản**: 1.0
