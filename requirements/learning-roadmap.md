# LỘ TRÌNH HỌC IMAGE PROCESSING ĐỂ THỰC HIỆN FINAL PROJECT

## 🎯 Mục Tiêu Final Project
**Đề tài 43: Phân Vùng Người & Phát Hiện Xâm Nhập Khu Vực Cấm**

### Các kỹ thuật cần thiết:
1. **Frame differencing** - Phân vùng dựa trên chuyển động
2. **Adaptive thresholding** - Ngưỡng thích nghi xử lý ánh sáng thay đổi
3. **Edge detection** (Sobel/Canny) - Phát hiện biên
4. **Region growing** - Tăng trưởng vùng để xác định hình người
5. **Morphological operations** - Xử lý hình thái để loại nhiễu và tách đối tượng
6. **Background subtraction** (MOG2) - Tách nền động

---

## 📋 PHÂN TÍCH CÁC FILE BÀI TẬP

### 1. T1-20: Biểu Diễn và Thu Nhận Ảnh (5 Labs)
**Mức độ**: Cơ bản - Nền tảng
**Mục tiêu**: Hiểu cách biểu diễn, lưu trữ và xử lý ảnh số

- **Lab 1**: Quantization (8→6→4→2 bit) + Quality metrics
- **Lab 2**: Zooming & Shrinking với interpolation
- **Lab 3**: Đo đạc góc, cung tròn, diện tích
- **Lab 4**: 4/8/m-connectivity và tìm đường đi
- **Lab 5**: Đánh giá chất lượng ảnh (MAE, MSE, PSNR, SSIM)

**Liên quan đến Final Project**: ⭐⭐ (Trung bình)
- Lab 5 quan trọng để đánh giá độ chính xác phân vùng

---

### 2. T21-40: Tách Biên (10 Bài)
**Mức độ**: Trung bình - Quan trọng
**Mục tiêu**: Nắm vững các phương pháp phát hiện biên

#### 🔴 **BÀI QUAN TRỌNG CHO FINAL PROJECT**:

- **Bài 1**: So sánh edge detectors (Roberts, Prewitt, **Sobel**, Scharr) + xử lý nhiễu
  - ⭐⭐⭐⭐⭐ **CRITICAL** - Sobel là yêu cầu bắt buộc

- **Bài 3**: Lane detection với **Canny** + Hough Lines
  - ⭐⭐⭐⭐⭐ **CRITICAL** - Canny là yêu cầu bắt buộc
  - Học cách kết hợp edge detection với các phương pháp khác

- **Bài 5**: Đếm xu với Canny + HoughCircles
  - ⭐⭐⭐ - Hiểu cách áp dụng edge detection vào bài toán thực tế

- **Bài 6**: Cắt sản phẩm với contour detection
  - ⭐⭐⭐⭐ - Quan trọng để xác định đối tượng sau edge detection

#### Các bài khác (tham khảo thêm):
- Bài 2: Document scanning - perspective transform
- Bài 4: Surface defect detection - Laplacian
- Bài 7: Crack detection - LoG + skeleton
- Bài 8: Leaf measurement
- Bài 9: Object measurement với calibration
- Bài 10: Document deskewing

**Liên quan đến Final Project**: ⭐⭐⭐⭐⭐ (Rất cao)

---

### 3. T61-78: Xử Lý Hình Thái (9 Bài)
**Mức độ**: Trung bình - Rất quan trọng
**Mục tiêu**: Làm sạch ảnh, tách đối tượng, loại nhiễu

#### 🔴 **BÀI QUAN TRỌNG CHO FINAL PROJECT**:

- **Bài 1**: Opening để loại nhiễu salt-and-pepper
  - ⭐⭐⭐⭐⭐ **CRITICAL** - Cần thiết để loại nhiễu từ frame differencing

- **Bài 2**: Closing để lấp lỗ và nối biên
  - ⭐⭐⭐⭐⭐ **CRITICAL** - Cần thiết để hoàn thiện contour người

- **Bài 3**: Morphological gradient cho edge extraction
  - ⭐⭐⭐⭐ - Phương pháp bổ sung cho Sobel/Canny

- **Bài 4**: Watershed để tách đối tượng chồng lấn
  - ⭐⭐⭐ - Hữu ích khi có nhiều người trong frame

- **Bài 8**: Foreground extraction bằng erosion
  - ⭐⭐⭐⭐ - Quan trọng để tách người khỏi nền

#### Các bài khác (tham khảo thêm):
- Bài 5: Character segmentation
- Bài 6: Đo kích thước particles
- Bài 7: Pruning với hit-or-miss
- Bài 9: Background removal với top-hat/black-hat

**Liên quan đến Final Project**: ⭐⭐⭐⭐⭐ (Rất cao)

---

### 4. T79-99: Phân Vùng Ảnh (10 Bài)
**Mức độ**: Nâng cao - CỰC KỲ QUAN TRỌNG
**Mục tiêu**: Kỹ thuật phân vùng - CORE của Final Project

#### 🔴 **BÀI QUAN TRỌNG CHO FINAL PROJECT**:

- **Bài 3**: Adaptive Thresholding (Mean/Gaussian)
  - ⭐⭐⭐⭐⭐ **CRITICAL - YÊU CẦU BẮT BUỘC**
  - Xử lý điều kiện ánh sáng thay đổi

- **Bài 6**: Region Growing từ seed points
  - ⭐⭐⭐⭐⭐ **CRITICAL - YÊU CẦU BẮT BUỘC**
  - Xác định hình người sau edge detection

- **Bài 9**: Motion Segmentation (Frame Differencing + MOG2)
  - ⭐⭐⭐⭐⭐ **CRITICAL - YÊU CẦU BẮT BUỘC**
  - Phân vùng dựa trên chuyển động
  - Background subtraction MOG2

#### Các bài nên học:

- **Bài 1**: Global thresholding (iterative method)
  - ⭐⭐⭐ - Nền tảng để hiểu adaptive thresholding

- **Bài 2**: Otsu's method
  - ⭐⭐⭐⭐ - Phương pháp tự động tìm ngưỡng phổ biến

- **Bài 5**: Edge detection + Hough Lines
  - ⭐⭐⭐ - Kết hợp edge detection với line detection

- **Bài 10**: Watershed
  - ⭐⭐⭐ - Tách đối tượng chồng lấn

#### Các bài khác (tham khảo):
- Bài 4: Bayes/ML thresholding
- Bài 7: Split-merge segmentation
- Bài 8: K-means clustering

**Liên quan đến Final Project**: ⭐⭐⭐⭐⭐ (CỰC KỲ CAO - CORE)

---

## 🎓 LỘ TRÌNH HỌC ĐỀ XUẤT

### GIAI ĐOẠN 1: NỀN TẢNG CƠ BẢN (1-2 tuần)
**Mục tiêu**: Hiểu cách ảnh được biểu diễn và xử lý cơ bản

📚 **Học theo thứ tự**:
1. **T1-20 Lab 1** - Quantization và quality metrics
   - Hiểu cách lưu trữ ảnh
   - Học các metrics đánh giá (PSNR, SSIM) - cần cho báo cáo

2. **T1-20 Lab 5** - Quality metrics evaluation
   - Thực hành đánh giá chất lượng
   - Chuẩn bị cho việc đánh giá độ chính xác phân vùng

**Thời gian**: 2-3 ngày

---

### GIAI ĐOẠN 2: EDGE DETECTION (1-2 tuần)
**Mục tiêu**: Nắm vững Sobel và Canny - YÊU CẦU BẮT BUỘC

📚 **Học theo thứ tự**:

1. 🔴 **T21-40 Bài 1** - So sánh edge detectors + noise handling
   - **QUAN TRỌNG NHẤT**
   - Hiểu Sobel, Prewitt, Roberts, Scharr
   - Học cách xử lý nhiễu (Gaussian blur)
   - **Thời gian**: 3-4 ngày

2. 🔴 **T21-40 Bài 3** - Lane detection với Canny
   - **QUAN TRỌNG NHẤT**
   - Nắm vững Canny edge detector
   - Học kết hợp với Hough Lines
   - **Thời gian**: 2-3 ngày

3. **T21-40 Bài 6** - Contour detection
   - Học cách tìm và xử lý contours
   - Chuẩn bị cho việc xác định hình người
   - **Thời gian**: 2 ngày

**Thời gian giai đoạn**: 7-9 ngày

---

### GIAI ĐOẠN 3: MORPHOLOGICAL OPERATIONS (1 tuần)
**Mục tiêu**: Làm sạch kết quả, tách đối tượng

📚 **Học theo thứ tự**:

1. 🔴 **T61-78 Bài 1** - Opening (loại nhiễu)
   - **CRITICAL** - Loại nhiễu từ frame differencing
   - Hiểu erosion và dilation
   - **Thời gian**: 2-3 ngày

2. 🔴 **T61-78 Bài 2** - Closing (lấp lỗ)
   - **CRITICAL** - Hoàn thiện contour
   - **Thời gian**: 2 ngày

3. **T61-78 Bài 3** - Morphological gradient
   - Phương pháp bổ sung cho edge detection
   - **Thời gian**: 1-2 ngày

4. **T61-78 Bài 8** - Foreground extraction
   - Tách foreground/background
   - **Thời gian**: 1-2 ngày

**Thời gian giai đoạn**: 6-9 ngày

---

### GIAI ĐOẠN 4: SEGMENTATION - CORE (2-3 tuần)
**Mục tiêu**: Làm chủ các kỹ thuật phân vùng - TRỌNG TÂM

📚 **Học theo thứ tự**:

1. **T79-99 Bài 1** - Global thresholding
   - Nền tảng cho adaptive thresholding
   - **Thời gian**: 2 ngày

2. **T79-99 Bài 2** - Otsu's method
   - Automatic thresholding
   - **Thời gian**: 2 ngày

3. 🔴 **T79-99 Bài 3** - Adaptive Thresholding
   - **CRITICAL - YÊU CẦU BẮT BUỘC**
   - Mean vs Gaussian adaptive
   - Xử lý ánh sáng không đều
   - **Thời gian**: 4-5 ngày

4. 🔴 **T79-99 Bài 9** - Motion Segmentation
   - **CRITICAL - YÊU CẦU BẮT BUỘC**
   - Frame differencing
   - Background subtraction (MOG2, KNN)
   - **Thời gian**: 5-6 ngày

5. 🔴 **T79-99 Bài 6** - Region Growing
   - **CRITICAL - YÊU CẦU BẮT BUỘC**
   - Seed selection
   - Homogeneity criteria
   - **Thời gian**: 4-5 ngày

6. **T79-99 Bài 10** - Watershed
   - Tách đối tượng chồng lấn
   - **Thời gian**: 2-3 ngày

**Thời gian giai đoạn**: 19-23 ngày

---

### GIAI ĐOẠN 5: TÍCH HỢP & FINAL PROJECT (2-3 tuần)
**Mục tiêu**: Kết hợp tất cả kỹ thuật đã học

📚 **Pipeline Final Project**:

```
Input Video
    ↓
[1] Frame Differencing / MOG2  ← Bài T79-99.9
    ↓ (Binary mask)
[2] Morphological Operations   ← Bài T61-78.1, T61-78.2
    (Opening → Closing)
    ↓ (Cleaned mask)
[3] Adaptive Thresholding      ← Bài T79-99.3
    (Handle lighting changes)
    ↓
[4] Edge Detection             ← Bài T21-40.1, T21-40.3
    (Sobel/Canny)
    ↓ (Edges)
[5] Contour Detection          ← Bài T21-40.6
    ↓ (Candidate regions)
[6] Region Growing             ← Bài T79-99.6
    (Refine person shape)
    ↓
[7] ROI Zone Check
    ↓
Output: Bounding box + Alert
```

**Các bước thực hiện**:
1. Thiết lập môi trường và dataset (2-3 ngày)
2. Implement từng module theo pipeline (7-10 ngày)
3. Tích hợp và testing (3-4 ngày)
4. Optimization và evaluation (3-4 ngày)
5. Viết báo cáo (3-4 ngày)

**Thời gian giai đoạn**: 18-25 ngày

---

## 📊 TỔNG KẾT: BÀI TẬP THEO ĐỘ ƯU TIÊN

### 🔴 MỨC ĐỘ 5/5 - BẮT BUỘC PHẢI HỌC (10 bài)

| Bài | Tên | Kỹ thuật | Thời gian |
|-----|-----|----------|-----------|
| T21-40.1 | Edge Detectors Comparison | **Sobel** (required) | 3-4 ngày |
| T21-40.3 | Lane Detection | **Canny** (required) | 2-3 ngày |
| T21-40.6 | Product Cropping | Contour detection | 2 ngày |
| T61-78.1 | Opening | Noise removal | 2-3 ngày |
| T61-78.2 | Closing | Hole filling | 2 ngày |
| T79-99.3 | Adaptive Thresholding | **Required** | 4-5 ngày |
| T79-99.6 | Region Growing | **Required** | 4-5 ngày |
| T79-99.9 | Motion Segmentation | **Frame diff + MOG2** | 5-6 ngày |

**Tổng thời gian**: ~25-33 ngày

---

### ⭐ MỨC ĐỘ 4/5 - NÊN HỌC (6 bài)

| Bài | Tên | Lý do | Thời gian |
|-----|-----|-------|-----------|
| T79-99.2 | Otsu's Method | Automatic thresholding | 2 ngày |
| T61-78.3 | Morphological Gradient | Alternative edge method | 1-2 ngày |
| T61-78.8 | Foreground Extraction | Foreground/background | 1-2 ngày |
| T79-99.1 | Global Thresholding | Foundation | 2 ngày |
| T79-99.5 | Edge + Hough Lines | Combined methods | 2 ngày |
| T1-20.5 | Quality Metrics | Evaluation | 1 ngày |

**Tổng thời gian**: ~9-11 ngày

---

### 📘 MỨC ĐỘ 3/5 - THAM KHẢO THÊM (6 bài)

| Bài | Tên | Lý do |
|-----|-----|-------|
| T21-40.5 | Coin Counting | Canny + HoughCircles |
| T61-78.4 | Watershed | Separate overlapping |
| T79-99.10 | Watershed Segmentation | Separate people |
| T1-20.1 | Quantization | Image representation |
| T21-40.2 | Document Scanning | Perspective transform |
| T79-99.8 | K-means Clustering | Alternative method |

---

## 🗓️ LỊCH TRÌNH HỌC ĐỀ XUẤT

### Lộ trình NHANH (6-8 tuần)
- **Tuần 1-2**: Edge Detection (T21-40.1, T21-40.3, T21-40.6)
- **Tuần 3**: Morphological Ops (T61-78.1, T61-78.2, T61-78.8)
- **Tuần 4-6**: Segmentation (T79-99.1→3, T79-99.9, T79-99.6)
- **Tuần 7-8**: Final Project implementation

### Lộ trình CHUẨN (8-10 tuần)
- **Tuần 1**: Nền tảng (T1-20.1, T1-20.5)
- **Tuần 2-3**: Edge Detection + bài tập bổ sung
- **Tuần 4**: Morphological Operations đầy đủ
- **Tuần 5-7**: Segmentation + bài tập bổ sung
- **Tuần 8-10**: Final Project + optimization

### Lộ trình CHI TIẾT (10-12 tuần)
- Học tất cả bài MỨC ĐỘ 5/5 và 4/5
- Tham khảo thêm các bài MỨC ĐỘ 3/5
- Thời gian dư để research và debugging

---

## 💡 LỜI KHUYÊN

### Cách học hiệu quả:
1. **Đọc đề bài** → Hiểu yêu cầu
2. **Nghiên cứu lý thuyết** → Xem trong knowledge-base của final-project
3. **Code từng bước** → Debug và test
4. **So sánh kết quả** → Với expected output
5. **Note lại** → Ghi chú các vấn đề gặp phải

### Khi học mỗi bài:
- ✅ Hiểu **TẠI SAO** dùng kỹ thuật này
- ✅ Hiểu **KHI NÀO** áp dụng
- ✅ Hiểu **CÁCH** parameters ảnh hưởng đến kết quả
- ✅ Thử nghiệm với **NHIỀU** ảnh khác nhau
- ✅ Note lại **ƯU/NHƯỢC ĐIỂM**

### Chuẩn bị cho Final Project:
- 📝 Tạo notebook riêng cho mỗi kỹ thuật
- 📊 So sánh performance của các methods
- 📸 Lưu lại kết quả tốt để làm example
- 🔧 Tối ưu parameters cho từng điều kiện ánh sáng

---

## 🎯 CHECKLIST TRƯỚC KHI LÀM FINAL PROJECT

### Kiến thức Edge Detection:
- [ ] Hiểu cách Sobel hoạt động
- [ ] Hiểu cách Canny hoạt động
- [ ] Biết khi nào dùng Sobel vs Canny
- [ ] Biết cách xử lý nhiễu trước edge detection
- [ ] Biết cách tìm và xử lý contours

### Kiến thức Morphological Operations:
- [ ] Hiểu erosion và dilation
- [ ] Biết khi nào dùng opening vs closing
- [ ] Biết cách chọn structuring element size
- [ ] Biết cách loại nhiễu từ binary mask

### Kiến thức Segmentation:
- [ ] Hiểu frame differencing
- [ ] Hiểu background subtraction (MOG2)
- [ ] Hiểu adaptive thresholding (Mean vs Gaussian)
- [ ] Hiểu region growing algorithm
- [ ] Biết cách kết hợp nhiều kỹ thuật

### Kỹ năng Implementation:
- [ ] Thành thạo OpenCV Python
- [ ] Biết cách đọc/ghi video
- [ ] Biết cách visualize kết quả
- [ ] Biết cách measure performance
- [ ] Biết cách tune parameters

---

## 📚 TÀI LIỆU THAM KHẢO

Khi học, tham khảo các tài liệu trong `final-project/knowledge-base/`:
- `01-fundamentals.md` - Khái niệm cơ bản
- `02-edge-detection.md` - Edge detection chi tiết
- `03-morphological-operations.md` - Morphological operations
- `04-segmentation.md` - Segmentation techniques
- `05-motion-detection.md` - Motion detection
- `06-opencv-reference.md` - OpenCV APIs

---

## ✅ KẾT LUẬN

### Con đường học tối ưu:
```
Nền tảng → Edge Detection → Morphology → Segmentation → Integration
(1 tuần)   (2 tuần)         (1 tuần)    (3 tuần)        (3 tuần)
```

### Bài tập CORE (10 bài - BẮT BUỘC):
1. T21-40.1 - Sobel ⭐⭐⭐⭐⭐
2. T21-40.3 - Canny ⭐⭐⭐⭐⭐
3. T21-40.6 - Contours ⭐⭐⭐⭐⭐
4. T61-78.1 - Opening ⭐⭐⭐⭐⭐
5. T61-78.2 - Closing ⭐⭐⭐⭐⭐
6. T79-99.3 - Adaptive Thresholding ⭐⭐⭐⭐⭐
7. T79-99.6 - Region Growing ⭐⭐⭐⭐⭐
8. T79-99.9 - Motion Segmentation ⭐⭐⭐⭐⭐

**Tổng thời gian học 10 bài CORE**: 25-33 ngày
**Tổng thời gian cả project**: 8-12 tuần

### Lưu ý quan trọng:
- 🔴 Tập trung vào 10 bài CORE trước
- 🔴 Mỗi bài phải code và test kỹ
- 🔴 Hiểu **TẠI SAO** và **KHI NÀO** dùng mỗi kỹ thuật
- 🔴 Note lại parameters tốt nhất cho từng kỹ thuật
- 🔴 Chuẩn bị dataset test đa dạng (sáng/tối, trong/ngoài, nhiều người/1 người)

---

**Chúc bạn học tốt và hoàn thành xuất sắc Final Project! 🎓**
