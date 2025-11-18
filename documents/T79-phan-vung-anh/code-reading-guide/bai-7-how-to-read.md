# Hướng Dẫn Đọc Code: Bài 7 - Split-Merge (Felzenszwalb)

## Tổng Quan
Phân đoạn ảnh phong cảnh bằng Felzenszwalb's Efficient Graph-Based Segmentation.

## Input/Output
**Input:** Ảnh phong cảnh (trời/biển/đất) | **Output:** Segmented regions

## Thuật Toán Chính

### `felzenszwalb()` từ scikit-image (dòng 89)
```python
seg = felzenszwalb(img_rgb, scale=100, sigma=0.8, min_size=150)
```

**Tham số:**
- `scale=100`: Độ ưu tiên vùng lớn (↑scale → ít vùng)
- `sigma=0.8`: Gaussian smoothing
- `min_size=150`: Diện tích tối thiểu vùng (pixels)

### Tạo ảnh màu trung bình (dòng 106-111)
```python
seg_mean = np.zeros_like(img_rgb)
for i in np.unique(seg):
    mask = (seg == i)
    if np.sum(mask) > 0:
        mean_color = np.mean(img_rgb[mask], axis=0)
        seg_mean[mask] = mean_color
```

## Code Quan Trọng

### Thống kê vùng (dòng 98-103)
```python
for i in range(min(5, num_segments)):
    mask = (seg == i)
    area = np.sum(mask)
    mean_color = np.mean(img_rgb[mask], axis=0)
    print(f"Vùng {i}: {area} pixels, màu TB: RGB({mean_color[0]:.0f}, ...)")
```

### Vẽ biên vùng (dòng 115)
```python
from skimage.segmentation import mark_boundaries
boundaries = mark_boundaries(img_rgb, seg, color=(1,1,0), mode='thick')
```

## Tham Số

| Tham số | Default | Ý nghĩa | Điều chỉnh |
|---------|---------|---------|------------|
| `scale` | 100 | Preference vùng lớn | ↑ → ít vùng, ↓ → nhiều vùng |
| `sigma` | 0.8 | Gaussian blur | ↑ → mượt hơn |
| `min_size` | 150 | Min pixels/vùng | ↑ → merge vùng nhỏ |

## Kết Quả Mong Đợi
- Phân đoạn mịn (scale=50): ~15-20 vùng
- Phân đoạn vừa (scale=100): ~8-12 vùng
- Phân đoạn thô (scale=200): ~3-5 vùng

## Mở Rộng

### So sánh với SLIC superpixels
```python
from skimage.segmentation import slic

seg_slic = slic(img_rgb, n_segments=100, compactness=10)
```

### Merge vùng theo màu
```python
threshold_merge = 20
for i in np.unique(seg):
    for j in np.unique(seg):
        if i < j:
            mean_i = np.mean(img_rgb[seg == i], axis=0)
            mean_j = np.mean(img_rgb[seg == j], axis=0)
            if np.linalg.norm(mean_i - mean_j) < threshold_merge:
                seg[seg == j] = i
```

---
**File:** `bai-7-split-merge/segment.py` (215 dòng)
