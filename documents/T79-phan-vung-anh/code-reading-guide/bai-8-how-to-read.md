# Hướng Dẫn Đọc Code: Bài 8 - K-means Clustering

## Tổng Quan
Phân vùng ảnh vệ tinh bằng K-means clustering trên không gian màu RGB/HSV.

## Input/Output
**Input:** Ảnh vệ tinh | **Output:** K vùng màu đồng nhất

## Thuật Toán Chính

### `kmeans_segmentation()` (dòng 53-79)

**Pipeline:**
```python
# 1. Reshape (H×W×3) → (N×3)
pixels = img.reshape((-1, 3)).astype(np.float32)

# 2. K-means
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iter, 1.0)
_, labels, centers = cv2.kmeans(pixels, K, None, criteria, 10,
                                 cv2.KMEANS_PP_CENTERS)

# 3. Tạo ảnh phân vùng
seg = centers[labels.flatten()].reshape(img.shape).astype(np.uint8)
```

## Code Quan Trọng

### K-means OpenCV (dòng 74)
```python
_, labels, centers = cv2.kmeans(
    pixels,              # Data (N×3)
    K,                   # Số cụm
    None,                # Best labels (output)
    criteria,            # Điều kiện dừng
    10,                  # Số attempts (chọn best)
    cv2.KMEANS_PP_CENTERS  # K-means++ initialization
)
```

**Return:**
- `labels`: Nhãn của mỗi pixel (N×1)
- `centers`: Tâm các cụm (K×3)

### Thống kê cụm (dòng 115-119)
```python
unique_labels, counts = np.unique(labels, return_counts=True)
for label, count in zip(unique_labels, counts):
    center = centers[label]
    percentage = 100 * count / labels.size
    print(f"Cụm {label}: RGB({center[0]:.0f}, {center[1]:.0f}, {center[2]:.0f}) - {percentage:.1f}%")
```

## Tham Số

| Tham số | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `K` | 4 | Số cụm |
| `max_iter` | 20 | Số iterations tối đa |
| `attempts` | 10 | Số lần chạy K-means (chọn best) |

## Lỗi Thường Gặp

### Chọn K không phù hợp
**Fix:** Elbow method
```python
from sklearn.cluster import KMeans

inertias = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)
    inertias.append(kmeans.inertia_)

plt.plot(range(2, 11), inertias)
plt.xlabel('K')
plt.ylabel('Inertia')
plt.show()
```

## Mở Rộng

### K-means trên HSV
```python
img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
seg_hsv, labels_hsv, centers_hsv = kmeans_segmentation(img_hsv, K=4)
seg_rgb = cv2.cvtColor(seg_hsv, cv2.COLOR_HSV2RGB)
```

### Kết hợp spatial information
```python
# Feature: [R, G, B, x×w, y×w]
H, W, _ = img.shape
y_coords, x_coords = np.mgrid[0:H, 0:W]
features = np.dstack([img, x_coords*0.1, y_coords*0.1])
```

---
**File:** `bai-8-kmeans/cluster.py` (228 dòng)
