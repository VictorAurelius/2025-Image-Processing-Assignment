# CHỈ MỤC TẤT CẢ FILES - T79 PHÂN VÙNG ẢNH

## Tổng quan
- **Tổng số files Python:** 11 files
- **Tổng số bài tập:** 10 bài
- **Tài liệu:** 5 files markdown
- **Scripts:** 2 files (sh + bat)

---

## Files chính

### 📚 Tài liệu
| File | Mô tả |
|------|-------|
| `README.md` | Tài liệu chính, hướng dẫn đầy đủ |
| `QUICK_START.md` | Hướng dẫn nhanh 3 bước |
| `INSTALL.md` | Hướng dẫn cài đặt chi tiết |
| `INDEX.md` | File này - chỉ mục tổng hợp |
| `requirements.txt` | Danh sách thư viện cần thiết |

### 🚀 Scripts chạy
| File | Hệ điều hành | Mô tả |
|------|--------------|-------|
| `run_all.sh` | Linux/Mac | Script chạy tất cả 10 bài |
| `run_all.bat` | Windows | Script chạy tất cả 10 bài |

---

## 10 Bài tập chính

### Bài 1: Global Thresholding
**File:** `bai-1-global-thresholding/threshold.py`
- **Dòng code:** ~120 dòng
- **Input:** `input/conveyor.jpg` (tự động tạo)
- **Output:** `bai-1-global-thresholding/output/global_threshold_result.png`
- **Thuật toán:** Iterative thresholding T=(m₁+m₂)/2
- **Độ khó:** ⭐⭐

### Bài 2: Otsu
**File:** `bai-2-otsu/threshold.py`
- **Dòng code:** ~135 dòng
- **Input:** `input/parts.jpg` (tự động tạo)
- **Output:** `bai-2-otsu/output/otsu_threshold_result.png`
- **Thuật toán:** Otsu's between-class variance
- **Độ khó:** ⭐⭐

### Bài 3: Adaptive Thresholding ⭐ CRITICAL
**File:** `bai-3-adaptive-thresholding/threshold.py`
- **Dòng code:** ~145 dòng
- **Input:** `input/receipt.jpg` (tự động tạo)
- **Output:** `bai-3-adaptive-thresholding/output/adaptive_threshold_result.png`
- **Thuật toán:** Adaptive MEAN_C / GAUSSIAN_C
- **Độ khó:** ⭐⭐⭐⭐⭐

### Bài 4: Bayes-ML Thresholding
**File:** `bai-4-bayes-ml/threshold.py`
- **Dòng code:** ~165 dòng
- **Input:** `input/steel_rust.jpg` (tự động tạo)
- **Output:** `bai-4-bayes-ml/output/bayes_ml_result.png`
- **Thuật toán:** Bayes decision theory, Gaussian model
- **Độ khó:** ⭐⭐⭐

### Bài 5: Edge Detection + Hough
**File:** `bai-5-edge-hough/detect.py`
- **Dòng code:** ~170 dòng
- **Input:** `input/lanes.jpg` (tự động tạo)
- **Output:** `bai-5-edge-hough/output/edge_hough_result.png`
- **Thuật toán:** Canny + HoughLinesP
- **Độ khó:** ⭐⭐⭐

### Bài 6: Region Growing ⭐ CRITICAL
**File:** `bai-6-region-growing/grow.py`
- **Dòng code:** ~200 dòng
- **Input:** `input/ultrasound.png` (tự động tạo)
- **Output:** `bai-6-region-growing/output/region_growing_result.png`
- **Thuật toán:** BFS 8-neighbor, |I(p)-I(seed)| < τ
- **Độ khó:** ⭐⭐⭐⭐⭐

### Bài 7: Split-Merge Segmentation
**File:** `bai-7-split-merge/segment.py`
- **Dòng code:** ~155 dòng
- **Input:** `input/landscape.jpg` (tự động tạo)
- **Output:** `bai-7-split-merge/output/split_merge_result.png`
- **Thuật toán:** Felzenszwalb (quadtree split-merge)
- **Độ khó:** ⭐⭐⭐⭐

### Bài 8: K-means Clustering
**File:** `bai-8-kmeans/cluster.py`
- **Dòng code:** ~175 dòng
- **Input:** `input/satellite.jpg` (tự động tạo)
- **Output:** `bai-8-kmeans/output/kmeans_result.png`
- **Thuật toán:** K-means clustering RGB/HSV
- **Độ khó:** ⭐⭐⭐

### Bài 9: Motion Segmentation ⭐ CRITICAL
**File:** `bai-9-motion-segmentation/segment.py`
- **Dòng code:** ~210 dòng
- **Input:** `input/gate.mp4` (tự động tạo video 50 frames)
- **Output:**
  - `bai-9-motion-segmentation/output/motion_statistics.png`
  - `bai-9-motion-segmentation/output/frames/*.jpg`
- **Thuật toán:** Frame differencing + MOG2 background subtraction
- **Độ khó:** ⭐⭐⭐⭐⭐

### Bài 10: Watershed Segmentation
**File:** `bai-10-watershed/segment.py`
- **Dòng code:** ~205 dòng
- **Input:** `input/coins.png` (tự động tạo)
- **Output:** `bai-10-watershed/output/watershed_result.png`
- **Thuật toán:** Distance transform + Watershed
- **Độ khó:** ⭐⭐⭐⭐

---

## Input folder

### Files trong input/
| File | Mô tả |
|------|-------|
| `input/README.md` | Hướng dẫn về ảnh input |
| `input/generate_samples.py` | Script tạo tất cả ảnh mẫu |
| `input/*.jpg, *.png, *.mp4` | Ảnh/video input (tự động tạo) |

### Danh sách ảnh input cần thiết:
1. `conveyor.jpg` - Băng chuyền (Bài 1)
2. `parts.jpg` - Linh kiện (Bài 2)
3. `receipt.jpg` - Hóa đơn (Bài 3)
4. `steel_rust.jpg` - Kim loại rỉ (Bài 4)
5. `lanes.jpg` - Vạch kẻ đường (Bài 5)
6. `ultrasound.png` - Siêu âm (Bài 6)
7. `landscape.jpg` - Phong cảnh (Bài 7)
8. `satellite.jpg` - Vệ tinh (Bài 8)
9. `gate.mp4` - Video cổng (Bài 9)
10. `coins.png` - Đồng xu (Bài 10)

---

## Output folders

Mỗi bài tạo thư mục `output/` với kết quả:

```
bai-X-ten-bai/
└── output/
    ├── *.png           # Ảnh kết quả
    └── frames/         # Video frames (chỉ Bài 9)
```

---

## Thống kê code

### Tổng số dòng code (ước tính)
- **Bài 1:** ~120 dòng
- **Bài 2:** ~135 dòng
- **Bài 3:** ~145 dòng
- **Bài 4:** ~165 dòng
- **Bài 5:** ~170 dòng
- **Bài 6:** ~200 dòng
- **Bài 7:** ~155 dòng
- **Bài 8:** ~175 dòng
- **Bài 9:** ~210 dòng
- **Bài 10:** ~205 dòng
- **Tổng:** ~1,680 dòng code Python

### Đặc điểm code
✅ Header comment tiếng Việt chi tiết
✅ Docstrings cho tất cả functions
✅ Console output tiếng Việt
✅ Tự động tạo ảnh mẫu
✅ Xử lý lỗi
✅ Lưu kết quả chất lượng cao
✅ Biểu đồ matplotlib
✅ Thống kê chi tiết

---

## Thư viện sử dụng

Từ `requirements.txt`:
```
opencv-python >= 4.8.0
numpy >= 1.24.0
matplotlib >= 3.7.0
scipy >= 1.10.0
scikit-image >= 0.21.0
```

---

## Cách sử dụng nhanh

### 1. Cài đặt
```bash
pip install -r requirements.txt
```

### 2. Chạy 1 bài
```bash
cd bai-1-global-thresholding
python3 threshold.py
```

### 3. Chạy tất cả
```bash
./run_all.sh          # Linux/Mac
run_all.bat           # Windows
```

---

## Map đường dẫn nhanh

```
T79-phan-vung-anh/
│
├── 📖 README.md                    ← Đọc đầu tiên
├── 🚀 QUICK_START.md              ← Hướng dẫn nhanh
├── 💾 INSTALL.md                   ← Cài đặt
├── 📋 INDEX.md                     ← File này
│
├── 📦 requirements.txt
├── ▶️ run_all.sh
├── ▶️ run_all.bat
│
├── 🖼️ input/
│   ├── README.md
│   ├── generate_samples.py
│   └── (ảnh tự động tạo)
│
├── 1️⃣ bai-1-global-thresholding/
│   └── threshold.py
│
├── 2️⃣ bai-2-otsu/
│   └── threshold.py
│
├── 3️⃣ bai-3-adaptive-thresholding/  ⭐ CRITICAL
│   └── threshold.py
│
├── 4️⃣ bai-4-bayes-ml/
│   └── threshold.py
│
├── 5️⃣ bai-5-edge-hough/
│   └── detect.py
│
├── 6️⃣ bai-6-region-growing/         ⭐ CRITICAL
│   └── grow.py
│
├── 7️⃣ bai-7-split-merge/
│   └── segment.py
│
├── 8️⃣ bai-8-kmeans/
│   └── cluster.py
│
├── 9️⃣ bai-9-motion-segmentation/    ⭐ CRITICAL
│   └── segment.py
│
└── 🔟 bai-10-watershed/
    └── segment.py
```

---

## Bài tập quan trọng (CRITICAL)

⭐⭐⭐⭐⭐ **TOP 3 BÀI PHẢI HỌC:**

1. **Bài 3 - Adaptive Thresholding**
   - Xử lý độ sáng không đều
   - Ứng dụng OCR, document scanning

2. **Bài 6 - Region Growing**
   - Thuật toán lan tỏa vùng
   - Medical image segmentation

3. **Bài 9 - Motion Segmentation**
   - Xử lý video
   - Phát hiện chuyển động
   - Surveillance, tracking

---

## Tham khảo

- **PDF gốc:** T79-99 Phân vùng ảnh.pdf
- **Tác giả:** Ph.D Phan Thanh Toàn
- **OpenCV:** https://docs.opencv.org/
- **Scikit-image:** https://scikit-image.org/

---

**Tất cả code đã sẵn sàng chạy 100%!** 🎉
