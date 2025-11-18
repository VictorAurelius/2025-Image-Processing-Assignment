# 05 - Thuật Toán Watershed Segmentation

## Tổng Quan

Watershed là một thuật toán segmentation mạnh mẽ, dựa trên ẩn dụ địa hình học: ảnh được xem như bề mặt địa hình, trong đó giá trị pixel là độ cao. Thuật toán "ngập nước" từ các minima (vùng thấp), tạo ra các "vùng nước" (catchment basins) và "đập ngăn nước" (watershed lines) chính là biên phân đoạn.

Watershed đặc biệt hiệu quả cho bài toán tách các vật thể chạm nhau hoặc chồng lên nhau, như đồng xu dính nhau, tế bào chạm nhau, hoặc các sản phẩm trên băng chuyền. Thuật toán này thường được kết hợp với Distance Transform và Morphology để xác định markers (điểm xuất phát).

## Ứng Dụng

- **Bài 4 (Watershed)**: Tách và đếm đồng xu/viên nén dính nhau bằng Watershed + Distance Transform

## Nguyên Lý Toán Học

### 1. Ẩn Dụ Địa Hình

**Mô hình:**
- Ảnh grayscale = Bề mặt địa hình 3D
- Pixel sáng = Vùng cao (đỉnh núi)
- Pixel tối = Vùng thấp (thung lũng)
- Gradient lớn = Độ dốc lớn

**Quá trình "ngập nước":**
1. Khoan lỗ tại tất cả local minima
2. Ngập nước từ dưới lên
3. Khi hai vùng nước gặp nhau, xây đập ngăn
4. Các đập = Watershed lines

### 2. Thuật Toán Watershed Cơ Bản

**Input:**
- Ảnh gradient (hoặc distance transform)

**Steps:**
```
1. Tìm tất cả local minima
2. Gán label cho từng minimum (marker)
3. Lặp theo thứ tự tăng dần của độ cao:
   for h from min to max:
       for pixel p at height h:
           if p có hàng xóm đã label:
               assign p to same label
           if p có nhiều labels khác nhau ở hàng xóm:
               mark p as watershed line (-1)
```

**Vấn đề Over-segmentation:**
- Watershed thường tạo ra quá nhiều vùng do nhiễu
- Giải pháp: Dùng markers để hướng dẫn segmentation

### 3. Marker-based Watershed

**Marker:**
- Sure foreground: Chắc chắn là vật thể
- Sure background: Chắc chắn là nền
- Unknown region: Vùng cần phân đoạn

**Quy trình (từ Bài 4):**
```
1. Nhị phân hóa: threshold → binary image
2. Opening: Khử nhiễu
3. Dilate → Sure background
4. Distance Transform
5. Threshold distance → Sure foreground
6. Unknown = Sure BG - Sure FG
7. Connected Components → Label markers
8. Watershed với markers
```

**Công thức:**
```python
# Từ Bài 4 code (separate.py)
_, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # Dòng 80
opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=2)  # Dòng 90
sure_bg = cv2.dilate(opening, kernel, iterations=3)  # Dòng 94
dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)  # Dòng 103
_, sure_fg = cv2.threshold(dist, 0.5 * dist.max(), 255, 0)  # Dòng 113
unknown = cv2.subtract(sure_bg, sure_fg)  # Dòng 119
_, markers = cv2.connectedComponents(sure_fg)  # Dòng 127
markers = markers + 1  # Dòng 131
markers[unknown == 255] = 0  # Dòng 133
markers = cv2.watershed(img, markers)  # Dòng 141
```

### 4. Distance Transform

Distance Transform tính khoảng cách từ mỗi pixel foreground đến pixel background gần nhất.

**Công thức Euclidean:**
```
D(p) = min{||p - q|| | q ∈ background}
```

**Ứng dụng trong Watershed:**
- Pixels có distance lớn = Tâm vật thể
- Threshold distance → Sure foreground
- Peaks của distance map = Markers tốt

**Từ Bài 4 (dòng 103-106):**
```python
dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
print(f"Khoảng cách max: {dist.max():.2f}")
_, sure_fg = cv2.threshold(dist, 0.5 * dist.max(), 255, 0)
```

## Code Examples (OpenCV)

### Example 1: Watershed Cơ Bản (từ Bài 4)

```python
import cv2
import numpy as np

# Đọc ảnh
img = cv2.imread('coins.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold
_, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Khử nhiễu bằng Opening
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=2)

# Sure background (Dilate)
sure_bg = cv2.dilate(opening, kernel, iterations=3)

# Distance transform → Sure foreground
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)
sure_fg = np.uint8(sure_fg)

# Unknown region
unknown = cv2.subtract(sure_bg, sure_fg)

# Markers
_, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1  # Nền = 1
markers[unknown == 255] = 0  # Unknown = 0

# Watershed
markers = cv2.watershed(img, markers)

# Vẽ biên (markers == -1)
img[markers == -1] = [0, 0, 255]

# Đếm số vật thể
n_objects = len(np.unique(markers)) - 2  # Trừ nền và biên
print(f"Số vật thể: {n_objects}")

cv2.imwrite('watershed_result.png', img)
```

**Kết quả:** Tách được các đồng xu dính nhau

### Example 2: Watershed với Custom Markers

```python
import cv2
import numpy as np

img = cv2.imread('cells.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Tạo markers thủ công (ví dụ: từ user clicks)
markers = np.zeros(binary.shape, dtype=np.int32)

# Marker 1: Background (vẽ ở biên)
markers[0:5, :] = 1
markers[-5:, :] = 1
markers[:, 0:5] = 1
markers[:, -5:] = 1

# Marker 2, 3, 4, ...: Foreground objects (vẽ ở tâm các vật thể)
# Ví dụ: User click tại (100, 100), (200, 150), ...
click_points = [(100, 100), (200, 150), (300, 200)]
for i, (x, y) in enumerate(click_points, start=2):
    cv2.circle(markers, (x, y), 5, i, -1)

# Watershed
markers = cv2.watershed(img, markers)

# Tô màu
img[markers == -1] = [0, 0, 255]  # Biên = đỏ
for i in range(2, markers.max() + 1):
    img[markers == i] = np.random.randint(0, 255, 3).tolist()

cv2.imwrite('custom_markers.png', img)
```

### Example 3: Watershed với Gradient Image

```python
import cv2
import numpy as np

img = cv2.imread('objects.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Tính gradient (thay vì distance transform)
sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
gradient = np.sqrt(sobel_x**2 + sobel_y**2)
gradient = cv2.normalize(gradient, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# Markers từ thresholding
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
_, markers = cv2.connectedComponents(binary)

# Watershed trên gradient
markers = cv2.watershed(cv2.cvtColor(gradient, cv2.COLOR_GRAY2BGR), markers)

# Hiển thị
img[markers == -1] = [255, 0, 0]
cv2.imwrite('gradient_watershed.png', img)
```

### Example 4: Interactive Watershed (với Trackbar)

```python
import cv2
import numpy as np

def watershed_with_threshold(threshold_value):
    # Distance transform
    dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)

    # Threshold distance
    _, sure_fg = cv2.threshold(dist, threshold_value/100 * dist.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)

    # Unknown
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Markers
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    # Watershed
    img_copy = img.copy()
    markers_ws = cv2.watershed(img_copy, markers)

    img_copy[markers_ws == -1] = [0, 0, 255]

    # Đếm
    n_objects = len(np.unique(markers_ws)) - 2

    # Hiển thị
    cv2.putText(img_copy, f"Objects: {n_objects}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Watershed', img_copy)

# Setup
img = cv2.imread('coins.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=2)
sure_bg = cv2.dilate(opening, kernel, iterations=3)

# Trackbar
cv2.namedWindow('Watershed')
cv2.createTrackbar('Threshold', 'Watershed', 50, 100, watershed_with_threshold)

watershed_with_threshold(50)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Example 5: Watershed Post-processing

```python
import cv2
import numpy as np

# ... (watershed code như Example 1)

# Sau watershed, lọc các vùng quá nhỏ
min_area = 100
for label in range(2, markers.max() + 1):
    region_mask = (markers == label).astype(np.uint8) * 255
    area = np.sum(region_mask == 255)

    if area < min_area:
        # Xóa region nhỏ, gộp vào background
        markers[region_mask == 255] = 1

# Gộp các vùng gần nhau (dựa trên centroid distance)
from scipy.spatial import distance_matrix

centroids = []
labels_list = []
for label in range(2, markers.max() + 1):
    region_mask = (markers == label)
    if np.sum(region_mask) > 0:
        y_coords, x_coords = np.where(region_mask)
        cx = np.mean(x_coords)
        cy = np.mean(y_coords)
        centroids.append([cx, cy])
        labels_list.append(label)

if len(centroids) > 1:
    centroids = np.array(centroids)
    distances = distance_matrix(centroids, centroids)

    # Gộp nếu khoảng cách < threshold
    merge_threshold = 50
    label_map = {label: label for label in labels_list}

    for i in range(len(labels_list)):
        for j in range(i+1, len(labels_list)):
            if distances[i, j] < merge_threshold:
                old_label = labels_list[j]
                new_label = label_map[labels_list[i]]
                markers[markers == old_label] = new_label
                label_map[old_label] = new_label

print(f"Số vùng sau post-processing: {len(np.unique(markers)) - 2}")
```

## So Sánh Các Phương Pháp

### Watershed vs Thresholding

| Đặc Điểm | Thresholding | Watershed |
|----------|--------------|-----------|
| **Nguyên lý** | Phân ngưỡng giá trị pixel | Phân vùng dựa trên gradient |
| **Tách vật thể dính nhau** | Không | Có |
| **Độ phức tạp** | Đơn giản | Phức tạp hơn |
| **Over-segmentation** | Không | Có (cần markers) |
| **Ứng dụng** | Ảnh có contrast rõ | Vật thể dính nhau |

### Watershed vs GrabCut

| Phương Pháp | Input | Output | Ưu Điểm | Nhược Điểm |
|-------------|-------|--------|---------|------------|
| **Watershed** | Markers + Gradient | Segmentation | Nhanh, tách vật thể dính | Over-segmentation |
| **GrabCut** | Bounding box | Foreground/Background | Chính xác hơn | Chậm, cần user input |

### Distance Transform Methods

| Loại | Công Thức | Tốc Độ | Chính Xác | Ứng Dụng |
|------|-----------|--------|-----------|----------|
| **DIST_L1** | Manhattan | Nhanh nhất | Thấp | Ước lượng nhanh |
| **DIST_L2** | Euclidean | Trung bình | Cao | Watershed (Bài 4) |
| **DIST_C** | Chessboard | Nhanh | Trung bình | Grid-based |

## Ưu Nhược Điểm

### Watershed

**Ưu điểm:**
- Tách vật thể dính nhau hiệu quả
- Tạo biên đóng (closed boundaries)
- Không cần biết trước số lượng vật thể
- Hoạt động tốt với vật thể hình tròn/ellipse

**Nhược điểm:**
- Over-segmentation (tạo quá nhiều vùng)
- Cần markers tốt (preprocessing phức tạp)
- Nhạy với nhiễu
- Không tốt cho vật thể hình dạng không đều

### Distance Transform

**Ưu điểm:**
- Tìm tâm vật thể chính xác
- Tạo markers tốt cho watershed
- Đơn giản, nhanh

**Nhược điểm:**
- Chỉ tốt cho vật thể tròn/ellipse
- Không tốt cho vật thể dài/mỏng
- Threshold distance phải điều chỉnh thủ công

## Kỹ Thuật Nâng Cao

### 1. H-minima Transform (Giảm Over-segmentation)

```python
import cv2
import numpy as np
from skimage.morphology import reconstruction

def h_minima(image, h):
    # Suppress minima shallower than h
    shifted = image + h
    reconstructed = reconstruction(shifted - h, image, method='erosion')
    return reconstructed

# Áp dụng
img = cv2.imread('noisy_coins.jpg', 0)
_, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)

# H-minima để giảm số markers
h_value = 0.3 * dist.max()
dist_hmin = h_minima(dist, h_value)

# Tiếp tục watershed như bình thường
```

### 2. Marker-controlled Watershed với Contour

```python
import cv2
import numpy as np

img = cv2.imread('cells.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Tìm contours để tạo markers
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

markers = np.zeros(binary.shape, dtype=np.int32)
markers[binary == 0] = 1  # Background

# Vẽ markers tại tâm mỗi contour
for i, cnt in enumerate(contours, start=2):
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(markers, (cx, cy), 5, i, -1)

# Watershed
markers = cv2.watershed(img, markers)
img[markers == -1] = [255, 0, 0]

cv2.imwrite('contour_markers_watershed.png', img)
```

### 3. Iterative Watershed (Phân cấp)

```python
import cv2
import numpy as np

def iterative_watershed(image, max_iterations=3):
    results = []

    for i in range(max_iterations):
        # Distance transform
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)

        # Threshold giảm dần
        threshold_ratio = 0.7 - i * 0.1
        _, sure_fg = cv2.threshold(dist, threshold_ratio * dist.max(), 255, 0)

        # Watershed
        kernel = np.ones((3, 3), np.uint8)
        sure_bg = cv2.dilate(binary, kernel, iterations=3)
        unknown = cv2.subtract(sure_bg, sure_fg.astype(np.uint8))

        _, markers = cv2.connectedComponents(sure_fg.astype(np.uint8))
        markers = markers + 1
        markers[unknown == 255] = 0

        markers = cv2.watershed(image, markers)

        results.append(markers.copy())

    return results

img = cv2.imread('complex_objects.jpg')
results = iterative_watershed(img, max_iterations=3)

# Hiển thị kết quả các iterations
for i, markers in enumerate(results):
    img_copy = img.copy()
    img_copy[markers == -1] = [0, 0, 255]
    cv2.imwrite(f'iteration_{i+1}.png', img_copy)
```

## Tài Liệu Tham Khảo

### Papers

1. **Vincent, L. & Soille, P. (1991)**
   - "Watersheds in Digital Spaces: An Efficient Algorithm Based on Immersion Simulations"
   - IEEE PAMI, Vol. 13, No. 6

2. **Meyer, F. & Beucher, S. (1990)**
   - "Morphological Segmentation"
   - Journal of Visual Communication

3. **Beucher, S. & Meyer, F. (1993)**
   - "The Morphological Approach to Segmentation: The Watershed Transformation"
   - Mathematical Morphology in Image Processing

### Online

- **OpenCV Watershed**: https://docs.opencv.org/4.x/d3/db4/tutorial_py_watershed.html
- **scikit-image Watershed**: https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_watershed.html

## Liên Kết

- [Bài 4: Watershed Segmentation](../code-reading-guide/bai-4-how-to-read.md)
- [06 - Distance Transform](./06-distance-transform.md)
- [03 - Binary Morphology](./03-binary-morphology.md)

---

**Nguồn**: T61-78 - Ph.D Phan Thanh Toàn
