# CHECKLIST - T79 PHÂN VÙNG ẢNH

## ✅ Cài đặt ban đầu

- [ ] Đã cài Python 3.8+
- [ ] Đã cài pip
- [ ] Đã chạy `pip install -r requirements.txt`
- [ ] Đã test import: `python3 -c "import cv2, numpy, matplotlib, scipy, skimage"`

## ✅ Chạy từng bài tập

### Nhóm 1: Phân ngưỡng cơ bản (Bài 1-4)

- [ ] **Bài 1: Global Thresholding**
  - File: `bai-1-global-thresholding/threshold.py`
  - Mục tiêu: Hiểu thuật toán iterative thresholding
  - Kết quả: Thấy ngưỡng hội tụ và mask nhị phân

- [ ] **Bài 2: Otsu**
  - File: `bai-2-otsu/threshold.py`
  - Mục tiêu: Hiểu Otsu's method
  - Kết quả: Histogram và số linh kiện đếm được

- [ ] **Bài 3: Adaptive Thresholding** ⭐⭐⭐⭐⭐ CRITICAL
  - File: `bai-3-adaptive-thresholding/threshold.py`
  - Mục tiêu: Xử lý độ sáng không đều
  - Kết quả: So sánh MEAN vs GAUSSIAN
  - **LƯU Ý:** Bài này rất quan trọng cho OCR/document processing

- [ ] **Bài 4: Bayes-ML**
  - File: `bai-4-bayes-ml/threshold.py`
  - Mục tiêu: Hiểu Bayes decision theory
  - Kết quả: Ngưỡng ML và phân bố Gaussian

### Nhóm 2: Phân vùng dựa biên (Bài 5)

- [ ] **Bài 5: Edge + Hough**
  - File: `bai-5-edge-hough/detect.py`
  - Mục tiêu: Phát hiện đường thẳng
  - Kết quả: Canny edges và HoughLines

### Nhóm 3: Phân vùng dựa vùng (Bài 6-7)

- [ ] **Bài 6: Region Growing** ⭐⭐⭐⭐⭐ CRITICAL
  - File: `bai-6-region-growing/grow.py`
  - Mục tiêu: Thuật toán lan tỏa vùng
  - Kết quả: Vùng lan từ seed points
  - **LƯU Ý:** Quan trọng cho medical imaging

- [ ] **Bài 7: Split-Merge**
  - File: `bai-7-split-merge/segment.py`
  - Mục tiêu: Phân đoạn theo vùng đồng nhất
  - Kết quả: Các vùng với boundaries

### Nhóm 4: Phân vùng dựa clustering (Bài 8)

- [ ] **Bài 8: K-means**
  - File: `bai-8-kmeans/cluster.py`
  - Mục tiêu: Gom cụm theo màu
  - Kết quả: K clusters và labels

### Nhóm 5: Phân vùng nâng cao (Bài 9-10)

- [ ] **Bài 9: Motion Segmentation** ⭐⭐⭐⭐⭐ CRITICAL
  - File: `bai-9-motion-segmentation/segment.py`
  - Mục tiêu: Phát hiện chuyển động trong video
  - Kết quả: Frame diff vs MOG2, bounding boxes
  - **LƯU Ý:** Quan trọng cho video processing

- [ ] **Bài 10: Watershed**
  - File: `bai-10-watershed/segment.py`
  - Mục tiêu: Tách vật thể chạm nhau
  - Kết quả: Labels và đếm đồng xu

## ✅ Kiểm tra kết quả

### Mỗi bài cần kiểm tra:

- [ ] Console log hiển thị đầy đủ thông tin
- [ ] Matplotlib hiển thị biểu đồ
- [ ] File output/*.png được tạo thành công
- [ ] Kết quả hợp lý (số liệu, vùng phân đoạn)

### Kết quả mẫu cần thấy:

**Bài 1:**
- [ ] Giá trị ngưỡng T (ví dụ: T=142.35)
- [ ] Mask nhị phân rõ ràng
- [ ] Tỷ lệ pixel nền/vật thể

**Bài 2:**
- [ ] Histogram với ngưỡng Otsu
- [ ] Số linh kiện đếm được
- [ ] So sánh với ngưỡng thủ công

**Bài 3:**
- [ ] 3 ảnh: Adaptive MEAN, GAUSSIAN, Otsu
- [ ] MEAN/GAUSSIAN tách chữ tốt hơn Otsu

**Bài 4:**
- [ ] Phân bố Gaussian của 2 lớp
- [ ] Ngưỡng ML tính được
- [ ] Vùng rỉ sét được tô màu

**Bài 5:**
- [ ] Canny edges rõ nét
- [ ] Đường thẳng được vẽ (màu xanh)
- [ ] Thống kê góc/độ dài

**Bài 6:**
- [ ] Vùng lan tỏa từ seeds
- [ ] Contours rõ ràng
- [ ] Test với tau khác nhau

**Bài 7:**
- [ ] Nhiều vùng với màu khác nhau
- [ ] Boundaries rõ ràng
- [ ] So sánh scale khác nhau

**Bài 8:**
- [ ] K clusters với màu đặc trưng
- [ ] Labels rõ ràng
- [ ] So sánh RGB vs HSV

**Bài 9:**
- [ ] Video frames trong output/frames/
- [ ] Bounding boxes trên vật thể chuyển động
- [ ] Biểu đồ thống kê
- [ ] So sánh MOG2 vs Frame Diff

**Bài 10:**
- [ ] Distance transform (ảnh nhiệt)
- [ ] Markers (điểm đỏ)
- [ ] Labels với màu khác nhau
- [ ] Đếm chính xác số đồng xu

## ✅ Nâng cao (Optional)

- [ ] Thử thay đổi tham số mỗi bài
- [ ] Thử với ảnh thực tế của bạn
- [ ] So sánh kết quả các phương pháp
- [ ] Đo thời gian chạy mỗi thuật toán

## ✅ Tài liệu

- [ ] Đã đọc README.md
- [ ] Đã đọc QUICK_START.md
- [ ] Hiểu cấu trúc thư mục (INDEX.md)
- [ ] Biết cách debug lỗi (INSTALL.md)

## ✅ Tổng kết

### Mục tiêu học tập đã đạt:

- [ ] Hiểu 4 nhóm kỹ thuật phân vùng:
  - [ ] Phân ngưỡng (Thresholding)
  - [ ] Dựa biên (Edge-based)
  - [ ] Dựa vùng (Region-based)
  - [ ] Clustering

- [ ] Biết khi nào dùng kỹ thuật nào:
  - [ ] Otsu: Ảnh có 2 đỉnh histogram rõ
  - [ ] Adaptive: Độ sáng không đều
  - [ ] Region Growing: Vùng đồng nhất
  - [ ] Watershed: Vật thể chạm nhau
  - [ ] K-means: Phân loại theo màu
  - [ ] Motion: Phát hiện chuyển động

- [ ] Có thể áp dụng vào project thực tế:
  - [ ] OCR / Document processing
  - [ ] Medical imaging
  - [ ] Industrial inspection
  - [ ] Video surveillance
  - [ ] Satellite image analysis

## ✅ Hoàn thành

- [ ] **ĐÃ CHẠY THÀNH CÔNG TẤT CẢ 10 BÀI**
- [ ] **HIỂU RÕ TỪNG THUẬT TOÁN**
- [ ] **SẴN SÀNG ÁP DỤNG VÀO DỰ ÁN THỰC TẾ**

---

## 📊 Tiến độ của bạn

Tổng bài đã hoàn thành: __ / 10

**Nhóm 1 (Thresholding):** __ / 4
**Nhóm 2 (Edge):** __ / 1
**Nhóm 3 (Region):** __ / 2
**Nhóm 4 (Clustering):** __ / 1
**Nhóm 5 (Advanced):** __ / 2

---

**Chúc bạn học tốt!** 🎓

Đánh dấu ✓ vào checkbox khi hoàn thành mỗi mục!
