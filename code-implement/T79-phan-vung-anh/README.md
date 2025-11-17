# T79-99: PHÂN VÙNG ẢNH (IMAGE SEGMENTATION)

Code hoàn chỉnh cho 10 bài thực hành về Phân vùng ảnh - Image Segmentation

**Tác giả gốc:** Ph.D Phan Thanh Toàn
**Nguồn:** T79-99 Phân vùng ảnh.pdf

---

## Tổng quan

Bộ code này bao gồm **10 bài tập thực hành** về các kỹ thuật phân vùng ảnh cơ bản đến nâng cao, được triển khai bằng Python với OpenCV, NumPy và Scikit-image.

### Danh sách 10 bài tập:

| Bài | Tên bài | Kỹ thuật | Mức độ | Trang PDF |
|-----|---------|----------|--------|-----------|
| 1 | **Global Thresholding** | Phân ngưỡng toàn cục lặp | ⭐⭐ | 1-2 |
| 2 | **Otsu** | Phân ngưỡng Otsu tối ưu | ⭐⭐ | 3-4 |
| 3 | **Adaptive Thresholding** | Phân ngưỡng thích nghi | ⭐⭐⭐⭐⭐ | 5-6 |
| 4 | **Bayes-ML** | Phân ngưỡng Bayes/ML | ⭐⭐⭐ | 7-8 |
| 5 | **Edge + Hough** | Dò biên + Hough Transform | ⭐⭐⭐ | 9-10 |
| 6 | **Region Growing** | Lan tỏa vùng từ hạt giống | ⭐⭐⭐⭐⭐ | 11-12 |
| 7 | **Split-Merge** | Phân đoạn tứ phân | ⭐⭐⭐⭐ | 13-14 |
| 8 | **K-means** | Gom cụm màu K-means | ⭐⭐⭐ | 15-16 |
| 9 | **Motion Segmentation** | Phân vùng chuyển động | ⭐⭐⭐⭐⭐ | 17-18 |
| 10 | **Watershed** | Watershed cho vật thể chạm nhau | ⭐⭐⭐⭐ | 19-20 |

---

## Cấu trúc thư mục

```
T79-phan-vung-anh/
│
├── bai-1-global-thresholding/
│   ├── threshold.py          # Code chính
│   └── output/               # Kết quả (tự động tạo)
│
├── bai-2-otsu/
│   ├── threshold.py
│   └── output/
│
├── bai-3-adaptive-thresholding/
│   ├── threshold.py
│   └── output/
│
├── bai-4-bayes-ml/
│   ├── threshold.py
│   └── output/
│
├── bai-5-edge-hough/
│   ├── detect.py
│   └── output/
│
├── bai-6-region-growing/
│   ├── grow.py
│   └── output/
│
├── bai-7-split-merge/
│   ├── segment.py
│   └── output/
│
├── bai-8-kmeans/
│   ├── cluster.py
│   └── output/
│
├── bai-9-motion-segmentation/
│   ├── segment.py
│   └── output/
│       └── frames/           # Video frames
│
├── bai-10-watershed/
│   ├── segment.py
│   └── output/
│
├── input/
│   ├── README.md
│   ├── generate_samples.py   # Tạo ảnh mẫu
│   └── *.jpg, *.png, *.mp4   # Ảnh/video input (tự động tạo)
│
├── requirements.txt
├── run_all.sh                # Script chạy tất cả (Linux/Mac)
├── run_all.bat               # Script chạy tất cả (Windows)
└── README.md                 # File này
```

---

## Cài đặt

### Yêu cầu hệ thống

- Python 3.8+
- pip

### Cài đặt thư viện

```bash
pip install -r requirements.txt
```

**Thư viện cần thiết:**
- opencv-python >= 4.8.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- scipy >= 1.10.0
- scikit-image >= 0.21.0

---

## Cách sử dụng

### 1. Chạy từng bài riêng lẻ

```bash
# Chạy bài 1
cd bai-1-global-thresholding
python threshold.py

# Chạy bài 3
cd bai-3-adaptive-thresholding
python threshold.py

# Chạy bài 6
cd bai-6-region-growing
python grow.py
```

### 2. Chạy tất cả bài tập

**Linux/Mac:**
```bash
chmod +x run_all.sh
./run_all.sh
```

**Windows:**
```cmd
run_all.bat
```

### 3. Tạo ảnh mẫu

Nếu không có ảnh input, mỗi bài sẽ **TỰ ĐỘNG TẠO** ảnh mẫu khi chạy.

Hoặc tạo tất cả ảnh mẫu trước:

```bash
cd input
python generate_samples.py
```

---

## Chi tiết từng bài tập

### Bài 1: Global Thresholding (Phân ngưỡng toàn cục)
- **Đề bài:** Tách sản phẩm khỏi nền trên băng chuyền
- **Thuật toán:** Iterative thresholding T = (m₁+m₂)/2
- **Input:** `conveyor.jpg`
- **Output:** Ảnh nhị phân, giá trị ngưỡng T

### Bài 2: Otsu (Phân ngưỡng Otsu)
- **Đề bài:** Đếm số linh kiện điện tử
- **Thuật toán:** Otsu's method (between-class variance)
- **Input:** `parts.jpg`
- **Output:** Histogram, mask, số lượng linh kiện

### Bài 3: Adaptive Thresholding ⭐⭐⭐⭐⭐
- **Đề bài:** Tách chữ trên hóa đơn có độ sáng không đều
- **Thuật toán:** Adaptive Mean/Gaussian thresholding
- **Input:** `receipt.jpg`
- **Output:** So sánh MEAN vs GAUSSIAN vs Otsu

### Bài 4: Bayes-ML Thresholding
- **Đề bài:** Phân tách vùng rỉ sét trên kim loại
- **Thuật toán:** Bayes decision theory, Gaussian model
- **Input:** `steel_rust.jpg`
- **Output:** Ngưỡng ML/Bayes, phân bố Gaussian

### Bài 5: Edge Detection + Hough Transform
- **Đề bài:** Phát hiện vạch kẻ đường
- **Thuật toán:** Canny + HoughLinesP
- **Input:** `lanes.jpg`
- **Output:** Edges, đường thẳng, thống kê góc/độ dài

### Bài 6: Region Growing ⭐⭐⭐⭐⭐
- **Đề bài:** Tách tổn thương trên ảnh siêu âm
- **Thuật toán:** BFS 8-neighbor, |I(p)-I(seed)| < τ
- **Input:** `ultrasound.png`
- **Output:** Vùng lan tỏa, contours

### Bài 7: Split-Merge Segmentation
- **Đề bài:** Phân đoạn ảnh phong cảnh (trời/biển/đất)
- **Thuật toán:** Quadtree split-merge (Felzenszwalb)
- **Input:** `landscape.jpg`
- **Output:** Các vùng, boundaries, thống kê

### Bài 8: K-means Clustering
- **Đề bài:** Phân vùng ảnh vệ tinh theo màu
- **Thuật toán:** K-means clustering (RGB/HSV)
- **Input:** `satellite.jpg`
- **Output:** K cụm màu, labels, centers

### Bài 9: Motion Segmentation (Video) ⭐⭐⭐⭐⭐
- **Đề bài:** Đếm người/xe qua cổng
- **Thuật toán:** Frame differencing + MOG2
- **Input:** `gate.mp4`
- **Output:** Foreground masks, bounding boxes, thống kê

### Bài 10: Watershed Segmentation
- **Đề bài:** Đếm đồng xu dính nhau
- **Thuật toán:** Distance transform + Watershed
- **Input:** `coins.png`
- **Output:** Labels, contours, đếm vật thể

---

## Đặc điểm code

### ✅ Tính năng
- ✅ Code y nguyên từ PDF T79-99
- ✅ Header comment TIẾNG VIỆT chi tiết
- ✅ Tự động tạo ảnh mẫu nếu thiếu input
- ✅ Console output tiếng Việt với phân tích kỹ thuật
- ✅ Lưu kết quả ra file PNG chất lượng cao
- ✅ Hiển thị biểu đồ matplotlib
- ✅ Xử lý lỗi và thông báo rõ ràng

### 📊 Output mỗi bài
- Ảnh/video kết quả
- Biểu đồ phân tích
- Thống kê số liệu
- Console log chi tiết

---

## Ghi chú quan trọng

### 🔥 Bài quan trọng nhất (CRITICAL)
1. **Bài 3 - Adaptive Thresholding:** Xử lý độ sáng không đều
2. **Bài 6 - Region Growing:** Thuật toán lan tỏa vùng
3. **Bài 9 - Motion Segmentation:** Xử lý video, phát hiện chuyển động

### 💡 Tips
- Với Bài 9, video mẫu sẽ được tạo tự động (50 frames)
- Có thể thay đổi tham số trong code để test
- Kết quả lưu trong thư mục `output/` của mỗi bài

### ⚠️ Lưu ý
- Đảm bảo đủ RAM cho Bài 9 (xử lý video)
- Bài 10 cần scikit-image và scipy
- Một số bài có thể chạy chậm trên máy yếu

---

## Kết quả mẫu

Mỗi bài sẽ tạo:
- File ảnh kết quả trong `output/`
- Biểu đồ matplotlib (tự động hiển thị)
- Log console với thống kê

Ví dụ output console Bài 1:
```
============================================================
PHÂN NGƯỠNG TOÀN CỤC - GLOBAL THRESHOLDING
============================================================

Giá trị ngưỡng hội tụ: T = 142.35
Kích thước ảnh: (400, 600)

Thống kê phân vùng:
  - Pixel nền (đen): 168523 (70.2%)
  - Pixel vật thể (trắng): 71477 (29.8%)

Độ sáng trung bình:
  - Vùng nền: 181.45
  - Vùng vật thể: 62.18
  - Chênh lệch: 119.27

Đã lưu kết quả tại: output/global_threshold_result.png

============================================================
HOÀN THÀNH!
============================================================
```

---

## Xử lý lỗi thường gặp

### Lỗi: Module not found
```bash
pip install -r requirements.txt
```

### Lỗi: Cannot open video (Bài 9)
- Đảm bảo có codec H.264
- Hoặc để code tự tạo video mẫu

### Lỗi: Matplotlib không hiển thị
```bash
# Linux
export DISPLAY=:0

# hoặc chạy trong Jupyter
%matplotlib inline
```

---

## Tham khảo

- **Tài liệu gốc:** T79-99 Phân vùng ảnh.pdf
- **OpenCV Docs:** https://docs.opencv.org/
- **Scikit-image:** https://scikit-image.org/

---

## Tác giả

**Code implementation:**
- Dựa trên giáo trình của Ph.D Phan Thanh Toàn
- Code Python: Claude Code Assistant

**Liên hệ:**
- Email: support@example.com
- GitHub: https://github.com/yourrepo

---

## License

Educational purposes only. Code mẫu cho học tập và nghiên cứu.

---

**Chúc bạn học tốt! 🎓**

Nếu gặp vấn đề, vui lòng tạo Issue hoặc liên hệ.
