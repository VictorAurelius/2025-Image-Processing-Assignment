# 06 - Distance Transform Applications

## Tổng Quan

Distance Transform tính khoảng cách từ mỗi pixel foreground đến pixel background gần nhất. Kết quả là một distance map, trong đó giá trị mỗi pixel thể hiện "độ sâu" của nó vào trong vật thể. Pixels gần biên có distance nhỏ, pixels ở tâm vật thể có distance lớn.

Distance Transform là công cụ quan trọng trong watershed segmentation (Bài 4), tìm skeleton của vật thể, và phân tích hình dạng. Nó giúp xác định tâm vật thể một cách tự động và chính xác.

## Ứng Dụng

- **Bài 4 (Watershed)**: Sử dụng Distance Transform để tìm sure foreground (tâm vật thể)
- Tìm skeleton (xương)
- Phân tích độ dày vật thể
- Tìm medial axis

## Nguyên Lý Toán Học

### 1. Định Nghĩa

**Distance Transform:**
```
D(p) = min{d(p, q) | q ∈ background}
```

Trong đó:
- `p`: Pixel foreground
- `q`: Pixel background
- `d(p, q)`: Khoảng cách giữa p và q

### 2. Các Loại Distance Metrics

**Euclidean Distance (L2):**
```
d_L2(p1, p2) = √[(x1-x2)² + (y1-y2)²]
```
- Khoảng cách thực tế
- Sử dụng trong Bài 4 (dòng 103)

**Manhattan Distance (L1):**
```
d_L1(p1, p2) = |x1-x2| + |y1-y2|
```
- Nhanh hơn
- Kém chính xác hơn

**Chessboard Distance (L∞):**
```
d_L∞(p1, p2) = max(|x1-x2|, |y1-y2|)
```
- Nhanh nhất
- Sử dụng cho ứng dụng real-time

### 3. Từ Bài 4 Code

```python
# Dòng 103-106
dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
print(f"[+] Tính Distance Transform (L2, mask size 5)")
print(f"[+] Khoảng cách max: {dist.max():.2f}")
print(f"[+] Khoảng cách min: {dist.min():.2f}")
```

**Ý nghĩa:**
- `cv2.DIST_L2`: Euclidean distance
- `5`: Mask size (kernel size cho tính toán)
- `dist.max()`: Tâm vật thể (xa biên nhất)

## Code Examples (OpenCV)

### Example 1: Basic Distance Transform

```python
import cv2
import numpy as np

img = cv2.imread('objects.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Distance Transform
dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)

# Normalize để visualize
dist_vis = cv2.normalize(dist, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

print(f"Max distance: {dist.max():.2f}")
print(f"Mean distance: {dist.mean():.2f}")

cv2.imwrite('distance_map.png', dist_vis)
```

### Example 2: Find Object Centers

```python
import cv2
import numpy as np

img = cv2.imread('coins.jpg', 0)
_, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Distance Transform
dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)

# Threshold để tìm tâm
_, centers = cv2.threshold(dist, 0.6 * dist.max(), 255, 0)

# Tìm vị trí tâm
centers_uint8 = centers.astype(np.uint8)
contours, _ = cv2.findContours(centers_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
for cnt in contours:
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(img_color, (cx, cy), 5, (0, 0, 255), -1)

cv2.imwrite('centers.png', img_color)
```

### Example 3: Skeleton with Distance Transform

```python
import cv2
import numpy as np

img = cv2.imread('shape.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Distance Transform
dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)

# Skeleton = Local maxima của distance map
# Sử dụng morphological reconstruction
from skimage.morphology import reconstruction

seed = dist - 1
skeleton = reconstruction(seed, dist, method='erosion')
skeleton = (skeleton == dist).astype(np.uint8) * 255

cv2.imwrite('skeleton.png', skeleton)
```

### Example 4: Compare Distance Metrics

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('circle.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Các distance metrics
dist_l1 = cv2.distanceTransform(binary, cv2.DIST_L1, 3)
dist_l2 = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
dist_c = cv2.distanceTransform(binary, cv2.DIST_C, 5)

# Visualize
fig, axes = plt.subplots(1, 4, figsize=(16, 4))

axes[0].imshow(binary, 'gray')
axes[0].set_title('Original')

axes[1].imshow(dist_l1, 'jet')
axes[1].set_title(f'L1 (max={dist_l1.max():.2f})')

axes[2].imshow(dist_l2, 'jet')
axes[2].set_title(f'L2 (max={dist_l2.max():.2f})')

axes[3].imshow(dist_c, 'jet')
axes[3].set_title(f'Chessboard (max={dist_c.max():.2f})')

plt.tight_layout()
plt.savefig('distance_comparison.png', dpi=150)
plt.show()
```

### Example 5: Thickness Analysis

```python
import cv2
import numpy as np

# Ảnh vật thể có độ dày thay đổi (ví dụ: mạch máu, đường ống)
img = cv2.imread('vessel.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Distance Transform
dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)

# Độ dày tại mỗi điểm = 2 × distance
thickness = dist * 2

# Thống kê
print(f"Độ dày min: {thickness[thickness > 0].min():.2f}")
print(f"Độ dày max: {thickness.max():.2f}")
print(f"Độ dày trung bình: {thickness[thickness > 0].mean():.2f}")

# Color-coded thickness
thickness_colored = cv2.applyColorMap(
    cv2.normalize(thickness, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8),
    cv2.COLORMAP_JET
)
cv2.imwrite('thickness_map.png', thickness_colored)
```

## So Sánh Các Phương Pháp

### Distance Metrics Comparison

| Metric | Công Thức | Tốc Độ | Chính Xác | Ứng Dụng |
|--------|-----------|--------|-----------|----------|
| **L1** | ‖x1-x2‖ + ‖y1-y2‖ | Nhanh nhất | Thấp | Ước lượng nhanh |
| **L2** | √[(x1-x2)² + (y1-y2)²] | Trung bình | Cao | Watershed, skeleton |
| **Chessboard** | max(‖x1-x2‖, ‖y1-y2‖) | Nhanh | Trung bình | Grid-based apps |

### Distance Transform vs Erosion

| Đặc Điểm | Distance Transform | Erosion |
|----------|-------------------|---------|
| **Output** | Distance map (float) | Binary image |
| **Thông tin** | Khoảng cách chính xác | Chỉ có/không |
| **Ứng dụng** | Watershed, skeleton, thickness | Morphology operations |
| **Tốc độ** | Chậm hơn | Nhanh hơn |

## Ưu Nhược Điểm

**Ưu điểm:**
- Tìm tâm vật thể chính xác
- Hỗ trợ watershed hiệu quả
- Phân tích độ dày vật thể
- Tìm medial axis/skeleton

**Nhược điểm:**
- Chậm hơn morphology operations
- Nhạy cảm với nhiễu ở biên
- Không tốt cho vật thể không đều

## Kỹ Thuật Nâng Cao

### 1. Adaptive Threshold Distance (từ Bài 4)

```python
# Bài 4 dòng 113-116
_, sure_fg = cv2.threshold(dist, 0.5 * dist.max(), 255, 0)
sure_fg = np.uint8(sure_fg)
print(f"[+] Threshold tại 50% khoảng cách max: {0.5 * dist.max():.2f}")
```

**Giải thích:**
- Threshold = 50% × max distance
- Adaptive: Tự động điều chỉnh theo kích thước vật thể

### 2. Medial Axis Transform

```python
import cv2
import numpy as np
from scipy import ndimage

def medial_axis(binary_image):
    dist = cv2.distanceTransform(binary_image, cv2.DIST_L2, 5)

    # Tìm local maxima
    local_max = (dist == ndimage.maximum_filter(dist, size=3))

    # Kết hợp với threshold
    medial = (local_max & (dist > 2)).astype(np.uint8) * 255

    return medial, dist

img = cv2.imread('shape.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

medial, dist = medial_axis(binary)
cv2.imwrite('medial_axis.png', medial)
```

### 3. Voronoi Diagram với Distance Transform

```python
import cv2
import numpy as np

# Ảnh với nhiều seeds (markers)
seeds = np.zeros((500, 500), dtype=np.uint8)
seeds[100, 100] = 255
seeds[400, 100] = 255
seeds[250, 400] = 255
seeds[100, 400] = 255

# Distance Transform từ seeds
dist = cv2.distanceTransform(cv2.bitwise_not(seeds), cv2.DIST_L2, 5)

# Watershed để tạo Voronoi
n, labels = cv2.connectedComponents(seeds)
labels = labels + 1
labels[seeds == 0] = 0

voronoi = cv2.watershed(cv2.cvtColor(dist.astype(np.uint8), cv2.COLOR_GRAY2BGR), labels)

# Visualize
voronoi_colored = np.zeros((500, 500, 3), dtype=np.uint8)
colors = np.random.randint(0, 255, (n+1, 3))
for i in range(1, n+1):
    voronoi_colored[voronoi == i] = colors[i]

cv2.imwrite('voronoi.png', voronoi_colored)
```

## Tài Liệu Tham Khảo

- **OpenCV Distance Transform**: https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html
- **Digital Image Processing** - Gonzalez & Woods, Chương 9

## Liên Kết

- [Bài 4: Watershed](../code-reading-guide/bai-4-how-to-read.md)
- [05 - Watershed Algorithm](./05-watershed-algorithm.md)

---

**Nguồn**: T61-78 - Ph.D Phan Thanh Toàn
