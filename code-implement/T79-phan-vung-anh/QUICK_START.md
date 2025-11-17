# HƯỚNG DẪN NHANH - T79 PHÂN VÙNG ẢNH

## Cài đặt nhanh (3 bước)

### Bước 1: Cài thư viện
```bash
pip install opencv-python numpy matplotlib scipy scikit-image
```

### Bước 2: Chạy thử 1 bài
```bash
cd bai-1-global-thresholding
python threshold.py
```

### Bước 3: Chạy tất cả
```bash
# Linux/Mac
./run_all.sh

# Windows
run_all.bat
```

## Danh sách bài tập

| # | Tên | File | Độ khó |
|---|-----|------|--------|
| 1 | Global Thresholding | `bai-1-global-thresholding/threshold.py` | ⭐⭐ |
| 2 | Otsu | `bai-2-otsu/threshold.py` | ⭐⭐ |
| 3 | Adaptive Thresholding | `bai-3-adaptive-thresholding/threshold.py` | ⭐⭐⭐⭐⭐ |
| 4 | Bayes-ML | `bai-4-bayes-ml/threshold.py` | ⭐⭐⭐ |
| 5 | Edge + Hough | `bai-5-edge-hough/detect.py` | ⭐⭐⭐ |
| 6 | Region Growing | `bai-6-region-growing/grow.py` | ⭐⭐⭐⭐⭐ |
| 7 | Split-Merge | `bai-7-split-merge/segment.py` | ⭐⭐⭐⭐ |
| 8 | K-means | `bai-8-kmeans/cluster.py` | ⭐⭐⭐ |
| 9 | Motion Segmentation | `bai-9-motion-segmentation/segment.py` | ⭐⭐⭐⭐⭐ |
| 10 | Watershed | `bai-10-watershed/segment.py` | ⭐⭐⭐⭐ |

## Ảnh input

**KHÔNG CẦN CHUẨN BỊ!** Code sẽ tự động tạo ảnh mẫu.

Hoặc tạo thủ công:
```bash
cd input
python generate_samples.py
```

## Kết quả

Mỗi bài tạo folder `output/` với:
- Ảnh kết quả (.png)
- Biểu đồ matplotlib
- Console log chi tiết

## Lỗi thường gặp

**Lỗi: No module named 'cv2'**
```bash
pip install opencv-python
```

**Lỗi: No module named 'skimage'**
```bash
pip install scikit-image
```

**Video không chạy (Bài 9):**
- Để code tự tạo video mẫu
- Hoặc cài codec: `pip install opencv-python-headless`

## 3 bài quan trọng nhất

1. **Bài 3** - Adaptive Thresholding (độ sáng không đều)
2. **Bài 6** - Region Growing (lan tỏa vùng)
3. **Bài 9** - Motion Segmentation (video)

---

**Chạy ngay và xem kết quả!** 🚀
