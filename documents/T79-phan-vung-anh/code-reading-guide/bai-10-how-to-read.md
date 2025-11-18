# Hướng Dẫn Đọc Code: Bài 10 - Watershed Segmentation

## Tổng Quan
Watershed segmentation để tách và đếm đồng xu/hạt bi dính nhau.

## Input/Output
**Input:** Ảnh đồng xu dính nhau | **Output:** Labels, số vật thể, biên vùng

## Thuật Toán Chính

### Pipeline Watershed (dòng 78-110)

**Bước 1: Otsu Thresholding (dòng 79-83)**
```python
_, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, np.ones((3,3)), iterations=1)
```

**Bước 2: Distance Transform (dòng 92)**
```python
dist = cv2.distanceTransform(bw, cv2.DIST_L2, 5)
```
**Giải thích:** Mỗi pixel = khoảng cách đến background gần nhất.

**Bước 3: Tìm Local Maxima làm Markers (dòng 97-103)**
```python
from skimage.feature import peak_local_max
coords = peak_local_max(dist, footprint=np.ones((3,3)), labels=bw)

mask = np.zeros(dist.shape, dtype=bool)
mask[tuple(coords.T)] = True
markers, num_markers = ndi.label(mask)
```

**Bước 4: Watershed (dòng 107)**
```python
from skimage.segmentation import watershed
labels = watershed(-dist, markers, mask=bw.astype(bool))
```
**Giải thích:** Dùng `-dist` vì watershed "ngập nước" từ minima.

## Code Quan Trọng

### Distance Transform visualization (dòng 173-176)
```python
plt.imshow(dist, cmap='jet')
plt.colorbar(fraction=0.046, pad=0.04)
```
**Giải thích:** Màu nóng (đỏ/vàng) = xa background (tâm vật thể).

### Vẽ markers (dòng 150-152)
```python
img_markers = img.copy()
for coord in coords:
    cv2.circle(img_markers, (coord[1], coord[0]), 3, (255,0,0), -1)
```

### Vẽ biên + đánh số (dòng 135-147)
```python
for i in range(1, num_objects + 1):
    mask = (labels == i).astype(np.uint8)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img_with_boundaries, contours, -1, (0, 255, 0), 2)
    
    # Đánh số
    M = cv2.moments(contours[0])
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        cv2.putText(img_with_boundaries, str(i), (cx-10, cy+5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 2)
```

### Báo cáo chi tiết (dòng 223-239)
```python
print(f"{'ID':<5} {'Diện tích':<12} {'Tọa độ tâm':<20} {'Tỷ lệ %'}")
for i in range(1, num_objects + 1):
    mask = (labels == i).astype(np.uint8)
    area = np.sum(mask)
    M = cv2.moments(mask)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    percentage = 100 * area / obj_pixels
    print(f"{i:<5} {area:<12} ({cx:>3}, {cy:>3}) {percentage:>5.1f}%")
```

## Tham Số Quan Trọng

| Tham số | Vị trí | Giá trị | Ý nghĩa |
|---------|--------|---------|---------|
| `morphology iterations` | Dòng 83 | 1 | Số lần opening (loại nhiễu) |
| `distance type` | Dòng 92 | `cv2.DIST_L2` | Euclidean distance |
| `peak footprint` | Dòng 97 | (3,3) | Kích thước vùng tìm peak |

## Kết Quả Mong Đợi
- Với 12 đồng xu trong ảnh mẫu
- Phát hiện: 12 markers
- Số vật thể sau watershed: 12
- Diện tích trung bình: ~5000-6000 pixels (tùy radius)

## Lỗi Thường Gặp

### 1. Oversegmentation (quá nhiều vùng)
**Nguyên nhân:** Nhiễu tạo ra nhiều local maxima
**Fix:**
```python
# Tăng footprint size
coords = peak_local_max(dist, footprint=np.ones((5,5)), labels=bw)

# Hoặc threshold distance transform
coords = peak_local_max(dist, footprint=np.ones((3,3)), 
                        labels=bw, threshold_abs=0.5*dist.max())
```

### 2. Undersegmentation (ít vùng)
**Nguyên nhân:** footprint quá lớn, hoặc vật thể dính quá chặt
**Fix:**
```python
# Giảm footprint
coords = peak_local_max(dist, footprint=np.ones((2,2)), labels=bw)

# Erosion trước distance transform
bw_eroded = cv2.erode(bw, np.ones((3,3)), iterations=2)
dist = cv2.distanceTransform(bw_eroded, cv2.DIST_L2, 5)
```

### 3. Vật thể bị "nuốt" biên
**Nguyên nhân:** Morphology opening quá mạnh
**Fix:** Giảm iterations hoặc kernel size
```python
kernel = np.ones((2,2), np.uint8)
bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel, iterations=1)
```

## Mở Rộng

### 1. Watershed trên gradient magnitude
```python
# Thay vì distance transform, dùng gradient
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
gradient = np.sqrt(sobelx**2 + sobely**2)

labels = watershed(gradient, markers, mask=bw)
```

### 2. Interactive watershed (user click seeds)
```python
seeds = []

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        seeds.append((y, x))
        cv2.circle(img_display, (x, y), 3, (0, 0, 255), -1)
        cv2.imshow('Image', img_display)

cv2.setMouseCallback('Image', mouse_callback)
# User clicks seeds, then apply watershed
```

### 3. Watershed với multiple classes
```python
# Markers với nhiều labels
markers = np.zeros_like(gray, dtype=np.int32)
markers[bg_sure] = 1  # Background
markers[fg_sure] = 2  # Foreground class 1
markers[fg2_sure] = 3  # Foreground class 2

labels = cv2.watershed(img, markers)
```

### 4. Morphological reconstruction
```python
# Tạo markers bằng h-minima transform
from skimage.morphology import reconstruction

h = 10
seed = dist - h
mask = dist
reconstructed = reconstruction(seed, mask, method='dilation')
regional_max = (dist - reconstructed) > 0
```

### 5. Đánh giá kết quả
```python
# So sánh với ground truth
from sklearn.metrics import adjusted_rand_score

gt_labels = cv2.imread('ground_truth_labels.png', 0)
score = adjusted_rand_score(labels.ravel(), gt_labels.ravel())
print(f"Adjusted Rand Index: {score:.4f}")
```

---
**File:** `bai-10-watershed/segment.py` (249 dòng)
**Lý thuyết:** [04-edge-based-segmentation.md](../theory/04-edge-based-segmentation.md)
