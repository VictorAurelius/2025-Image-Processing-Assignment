# Bài 4: Đếm Đồng Xu Dính Nhau - Watershed - How to Read

## Tổng Quan

File `separate.py` (245 dòng) sử dụng Watershed Segmentation kết hợp Distance Transform để tách và đếm các đồng xu/viên nén chạm nhau.

## Input/Output

**Input**: `../input/coins/touching.jpg`
**Output**: `segmented.png` (biên đỏ), `distance_transform.png`, `result.png` (8 subplots)

## Thuật Toán Chính (7 bước)

1. **Chuyển Grayscale & Threshold INV** (dòng 77-82) → Đối tượng = trắng
2. **Opening** (dòng 85-91) → Khử nhiễu
3. **Dilate → Sure Background** (dòng 94-96)
4. **Distance Transform** (dòng 103-106) → Tìm tâm vật thể
5. **Threshold Distance → Sure Foreground** (dòng 113-116)
6. **Sure BG - Sure FG = Unknown** (dòng 119-120)
7. **Connected Components → Markers** (dòng 127-134)
8. **Watershed** (dòng 141-146) → Phân đoạn

## Code Quan Trọng

### 1. Distance Transform (Dòng 103-106)

```python
dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
print(f"[+] Khoảng cách max: {dist.max():.2f}")
```

**Giải thích**: Tính khoảng cách từ mỗi pixel đến biên gần nhất. Pixels ở tâm có distance lớn.

### 2. Sure Foreground (Dòng 113-116)

```python
_, sure_fg = cv2.threshold(dist, 0.5 * dist.max(), 255, 0)
```

**Giải thích**: Chỉ giữ pixels có distance > 50% max = chắc chắn là tâm vật thể.

### 3. Markers Preparation (Dòng 127-134)

```python
_, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1  # Nền = 1
markers[unknown == 255] = 0  # Unknown = 0
```

**Giải thích**:
- Label từng sure foreground component (1, 2, 3, ...)
- +1 để nền = 1 (Watershed cần nền > 0)
- Unknown = 0 để Watershed phân đoạn

### 4. Watershed (Dòng 141-146)

```python
markers = cv2.watershed(img, markers)
# markers == -1: Biên
# markers == 1: Nền
# markers >= 2: Vật thể
count = len(np.unique(markers)) - 2
```

### 5. Hiển thị 8 Bước (Dòng 159-199)

```python
plt.subplot(2, 4, 1): Ảnh gốc
plt.subplot(2, 4, 2): Nhị phân INV
plt.subplot(2, 4, 3): Opening
plt.subplot(2, 4, 4): Sure BG
plt.subplot(2, 4, 5): Distance Transform (colormap 'jet')
plt.subplot(2, 4, 6): Sure FG
plt.subplot(2, 4, 7): Unknown
plt.subplot(2, 4, 8): Kết quả (biên đỏ)
```

## Tham Số Quan Trọng

| Tham Số | Giá Trị | Ý Nghĩa | Ảnh Hưởng |
|---------|---------|---------|-----------|
| **Opening Iterations** | 2 | Số lần Opening | Nhiều → khử nhiễu tốt, mất chi tiết |
| **Dilate Iterations** | 3 | Số lần Dilate (Sure BG) | Nhiều → Sure BG lớn hơn |
| **Distance Threshold** | 0.5 × max | Tỷ lệ threshold distance | Thấp → nhiều markers, Cao → ít markers |
| **Distance Type** | DIST_L2 | Loại distance | L2 = Euclidean (chính xác) |
| **Mask Size** | 5 | Kích thước mask cho distance | Lớn → chính xác hơn, chậm hơn |

## Kết Quả Mong Đợi

**Input**: 9 đồng xu chạm nhau
**Output**: 
- Phát hiện 9 vật thể riêng biệt
- Biên đỏ phân cách rõ ràng
- Không over-segmentation (nhờ markers tốt)

**Phân tích**:
- Sure FG: 9 vùng nhỏ ở tâm
- Unknown: Vùng giữa các đồng xu
- Watershed phân Unknown thành 9 vùng

## Lỗi Thường Gặp

### Lỗi 1: Over-segmentation (Quá Nhiều Vùng)

**Triệu chứng**: Watershed tạo hàng trăm vùng nhỏ

**Nguyên nhân**: Distance threshold quá thấp → quá nhiều markers

**Fix**:
```python
# BAD: Threshold quá thấp
_, sure_fg = cv2.threshold(dist, 0.2 * dist.max(), 255, 0)

# GOOD: Threshold cao hơn
_, sure_fg = cv2.threshold(dist, 0.6 * dist.max(), 255, 0)
```

### Lỗi 2: Under-segmentation (Quá Ít Vùng)

**Triệu chứng**: Nhiều vật thể bị gộp thành 1

**Nguyên nhân**: Distance threshold quá cao → quá ít markers

**Fix**: Giảm threshold xuống 0.4-0.5

### Lỗi 3: Biên Không Chính Xác

**Nguyên nhân**: Opening quá mạnh

**Fix**: Giảm iterations hoặc kernel size

## Mở Rộng

### 1. Interactive Threshold

```python
def watershed_trackbar(threshold_percent):
    dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist, threshold_percent/100 * dist.max(), 255, 0)
    # ... tiếp tục watershed
    # Hiển thị kết quả với số đối tượng

cv2.createTrackbar('Threshold %', 'Watershed', 50, 100, watershed_trackbar)
```

### 2. Gradient-based Watershed

```python
# Thay vì distance, dùng gradient
sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
gradient = np.sqrt(sobel_x**2 + sobel_y**2)
markers = cv2.watershed(cv2.cvtColor(gradient.astype(np.uint8), cv2.COLOR_GRAY2BGR), markers)
```

### 3. Post-processing Merge

```python
# Gộp các vùng quá nhỏ hoặc quá gần nhau
min_area = 100
for label in range(2, markers.max() + 1):
    if np.sum(markers == label) < min_area:
        markers[markers == label] = 1  # Gộp vào nền
```

### 4. Contour-based Markers

```python
# Thay vì distance, dùng contours để tạo markers
contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
markers = np.zeros(opening.shape, dtype=np.int32)
for i, cnt in enumerate(contours, start=2):
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(markers, (cx, cy), 5, i, -1)
```

### 5. H-minima Suppression

```python
from skimage.morphology import reconstruction

def h_minima(image, h):
    shifted = image + h
    reconstructed = reconstruction(shifted - h, image, method='erosion')
    return reconstructed

# Giảm số minima bằng h-minima
dist_hmin = h_minima(dist, 0.3 * dist.max())
_, sure_fg = cv2.threshold(dist_hmin, 0, 255, cv2.THRESH_BINARY)
```

---

**Tổng Dòng Code**: 245 dòng
**Độ Phức Tạp**: Khó (★★★★☆)
**File**: `bai-4-watershed/separate.py`
**Theory**: [05-watershed-algorithm.md](../theory/05-watershed-algorithm.md), [06-distance-transform.md](../theory/06-distance-transform.md)
