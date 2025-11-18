# 03 - Morphology Nhị Phân (Binary Morphology)

## Tổng Quan

Binary Morphology là nền tảng của xử lý hình thái, tập trung vào xử lý ảnh nhị phân (chỉ có 2 giá trị: 0 và 1, đen và trắng). Các kỹ thuật này đặc biệt hiệu quả cho việc phân tích các vật thể rời rạc như văn bản, linh kiện điện tử, tế bào y học, và các sản phẩm công nghiệp.

Hai kỹ thuật quan trọng trong Binary Morphology là **Connected Components Analysis** (phân tích thành phần liên thông) và **Hole Filling** (lấp lỗ). Connected Components giúp tách và đếm các vật thể riêng biệt, còn Hole Filling giúp phục hồi các vật thể bị khuyết.

Các kỹ thuật này được ứng dụng rộng rãi trong OCR (nhận dạng ký tự), phân đoạn ảnh y tế, kiểm tra chất lượng sản xuất, và robot vision.

## Ứng Dụng

- **Bài 2 (Closing)**: Sử dụng Closing để lấp lỗ trong vật thể
- **Bài 4 (Watershed)**: Sử dụng Connected Components để đánh nhãn vùng
- **Bài 5 (Character Segmentation)**: Sử dụng Connected Components để tách từng ký tự
- **Bài 6 (Particle Measurement)**: Phân tích từng component, tính diện tích, chu vi

## Nguyên Lý Toán Học

### 1. Connected Components Analysis

Connected Components là các tập hợp pixel liên thông với nhau (có thể đi được từ pixel này sang pixel khác mà không đi qua background).

**Định nghĩa Liên Thông:**

1. **4-connectivity (Liên thông 4 hướng):**
   - Hai pixel là hàng xóm nếu cạnh chung
   - Mỗi pixel có tối đa 4 hàng xóm: trên, dưới, trái, phải
   ```
     | p1 |
   --|----|-
   p2| p |p3
   --|----|-
     | p4 |
   ```

2. **8-connectivity (Liên thông 8 hướng):**
   - Hai pixel là hàng xóm nếu cạnh hoặc góc chung
   - Mỗi pixel có tối đa 8 hàng xóm
   ```
   p1| p2 |p3
   --|----|-
   p4| p |p5
   --|----|-
   p6| p7 |p8
   ```

**Thuật Toán Two-Pass Labeling:**

**Pass 1 (Quét xuống):**
```
for each pixel p in image:
    if p is foreground:
        neighbors = get_labeled_neighbors(p)
        if neighbors is empty:
            assign new label to p
        else:
            assign min(neighbors) to p
            record equivalences
```

**Pass 2 (Gộp nhãn):**
```
for each pixel p:
    if p is labeled:
        p.label = find_root(p.label)
```

**OpenCV Implementation:**
```python
n_components, labels = cv2.connectedComponents(binary_image)
```
- `n_components`: Số lượng component (kể cả background = 0)
- `labels`: Ma trận nhãn (mỗi pixel thuộc component nào)

**Tính chất:**
- Component 0 luôn là background
- Các component từ 1 trở đi là foreground
- Số component thực = `n_components - 1`

### 2. Hole Filling

Hole (lỗ) là vùng background được bao quanh hoàn toàn bởi foreground.

**Định nghĩa:**
```
H = {h | h thuộc background và không thể đi được đến biên ảnh mà không đi qua foreground}
```

**Thuật Toán (Morphological Reconstruction):**

**Phương pháp 1: Flood Fill từ Biên**
```
1. Tạo marker = 1 ở biên, 0 ở bên trong
2. Marker AND (NOT image) = background ngoài lỗ
3. Lấp lỗ = image OR (NOT marker)
```

**Phương pháp 2: Morphological Closing**
```
filled = closing(image, large_kernel)
```
- Kernel phải lớn hơn lỗ cần lấp
- Đơn giản nhưng có thể lấp cả lỗ lớn không mong muốn

**Phương pháp 3: Morphological Reconstruction**
```
1. marker = 1 - image (invert)
2. Set biên của marker = 0
3. Reconstruct marker under (1 - image)
4. filled = 1 - reconstructed
```

**Từ Bài 2 Code:**
```python
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
# Closing tự động lấp lỗ nhỏ hơn kernel
```

### 3. Component Properties (Đặc Tính Component)

Mỗi component có thể được đặc trưng bởi nhiều thuộc tính:

**Geometric Properties:**
1. **Area (Diện tích):**
   ```
   Area = Số pixel thuộc component
   ```

2. **Perimeter (Chu vi):**
   ```
   Perimeter = cv2.arcLength(contour, True)
   ```

3. **Bounding Box:**
   ```
   x, y, w, h = cv2.boundingRect(contour)
   ```

4. **Centroid (Tâm):**
   ```
   M = cv2.moments(contour)
   cx = M['m10'] / M['m00']
   cy = M['m01'] / M['m00']
   ```

5. **Circularity (Độ tròn):**
   ```
   Circularity = 4π × Area / Perimeter²
   ```
   - = 1 cho hình tròn hoàn hảo
   - < 1 cho hình khác

6. **Aspect Ratio:**
   ```
   Aspect Ratio = width / height
   ```

**Từ Bài 6 Code (measure.py):**
```python
# Dòng 106: contours, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Dòng 110: areas = sorted([cv2.contourArea(c) for c in contours])
# Dòng 159-163: Tính moments và centroid
```

### 4. Labeling và Filtering

**Filtering Components theo Thuộc Tính:**

```python
# Lọc theo diện tích
min_area = 100
max_area = 10000
valid_components = [c for c in components if min_area < c.area < max_area]

# Lọc theo aspect ratio
min_aspect = 0.5
max_aspect = 2.0
valid_components = [c for c in components if min_aspect < c.aspect < max_aspect]

# Lọc theo circularity (phát hiện hình tròn)
min_circularity = 0.8
circles = [c for c in components if c.circularity > min_circularity]
```

**Từ Bài 5 Code (segment.py):**
```python
# Dòng 140-142: Lọc component theo area
min_area = 100
max_area = img.shape[0] * img.shape[1] * 0.5
valid_components = [c for c in components_info if min_area < c['area'] < max_area]
```

## Code Examples (OpenCV)

### Example 1: Connected Components Basic

```python
import cv2
import numpy as np

# Ảnh nhị phân
img = cv2.imread('objects.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Connected Components
n_components, labels = cv2.connectedComponents(binary)

print(f"Số components (kể cả nền): {n_components}")
print(f"Số vật thể: {n_components - 1}")

# Tô màu từng component
colored = np.zeros((*binary.shape, 3), dtype=np.uint8)
colors = np.random.randint(0, 255, size=(n_components, 3), dtype=np.uint8)
colors[0] = [0, 0, 0]  # Background = đen

for label in range(n_components):
    colored[labels == label] = colors[label]

cv2.imwrite('labeled.png', colored)
```

**Từ Bài 5 Code (segment.py):**
- Dòng 110: `n, labels = cv2.connectedComponents(bw)`

### Example 2: Component Analysis với contourArea

```python
import cv2
import numpy as np

img = cv2.imread('particles.png', 0)
_, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Tìm contours (cách khác để tìm components)
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print(f"Số contours: {len(contours)}")

# Phân tích từng contour
for idx, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)
    x, y, w, h = cv2.boundingRect(cnt)

    # Moments
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # Circularity
        circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0

        print(f"Component {idx+1}:")
        print(f"  Area: {area:.2f}")
        print(f"  Perimeter: {perimeter:.2f}")
        print(f"  Centroid: ({cx}, {cy})")
        print(f"  BBox: ({x}, {y}, {w}, {h})")
        print(f"  Circularity: {circularity:.3f}")
```

**Từ Bài 6 Code (measure.py):**
- Dòng 104-108: findContours và tính area
- Dòng 159-167: Tính moments, centroid, circularity

### Example 3: Hole Filling với Closing

```python
import cv2
import numpy as np

# Ảnh có lỗ
img = cv2.imread('object_with_holes.png', 0)
_, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Lấp lỗ bằng Closing
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
filled = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

# Tính số lỗ đã lấp
holes = cv2.subtract(filled, binary)
print(f"Pixels đã lấp: {np.sum(holes == 255)}")

cv2.imwrite('filled.png', filled)
cv2.imwrite('holes_only.png', holes)
```

**Từ Bài 2 Code (fill_holes.py):**
- Dòng 90-95: Sử dụng Closing để lấp lỗ
- Dòng 98-102: Đếm pixels đã lấp

### Example 4: Component Filtering

```python
import cv2
import numpy as np

img = cv2.imread('license_plate.png', 0)
_, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Tìm components
n, labels = cv2.connectedComponents(binary)

# Phân tích và lọc
valid_labels = []
for label in range(1, n):  # Bỏ qua background (0)
    mask = (labels == label).astype(np.uint8) * 255
    area = np.sum(mask == 255)

    # Lọc theo diện tích
    if 100 < area < 5000:
        # Lọc theo aspect ratio
        y_coords, x_coords = np.where(labels == label)
        x_min, x_max = x_coords.min(), x_coords.max()
        y_min, y_max = y_coords.min(), y_coords.max()
        width = x_max - x_min
        height = y_max - y_min
        aspect = width / height if height > 0 else 0

        if 0.2 < aspect < 1.5:
            valid_labels.append(label)

print(f"Valid components: {len(valid_labels)} / {n-1}")

# Tạo ảnh chỉ có valid components
filtered = np.zeros_like(binary)
for label in valid_labels:
    filtered[labels == label] = 255

cv2.imwrite('filtered_components.png', filtered)
```

**Từ Bài 5 Code (segment.py):**
- Dòng 114-137: Phân tích chi tiết từng component
- Dòng 140-143: Lọc component theo kích thước

### Example 5: Hierarchical Connected Components

```python
import cv2
import numpy as np

# Ảnh có objects lồng nhau (như chữ O, P, B)
img = cv2.imread('text.png', 0)
_, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Tìm contours với hierarchy
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# hierarchy[i] = [Next, Previous, First_Child, Parent]
print(f"Số contours: {len(contours)}")

# Phân loại
external = []
holes = []

for idx, h in enumerate(hierarchy[0]):
    if h[3] == -1:  # Không có parent = external contour
        external.append(idx)
    else:  # Có parent = hole
        holes.append(idx)

print(f"External contours: {len(external)}")
print(f"Holes: {len(holes)}")

# Vẽ
img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
cv2.drawContours(img_color, contours, -1, (0, 255, 0), 2)
cv2.imwrite('hierarchical.png', img_color)
```

## So Sánh Các Phương Pháp

### Connected Components vs Contours

| Đặc Điểm | Connected Components | findContours |
|----------|---------------------|--------------|
| **Output** | Ma trận labels | Danh sách điểm biên |
| **Thông tin** | Label mỗi pixel | Chỉ biên |
| **Tốc độ** | Nhanh hơn | Chậm hơn |
| **Memory** | Cần ma trận labels | Ít hơn |
| **Hierarchy** | Không | Có (RETR_TREE) |
| **Ứng dụng** | Labeling, statistics | Shape analysis, drawing |

### Hole Filling Methods

| Phương Pháp | Công Thức | Ưu Điểm | Nhược Điểm |
|-------------|-----------|---------|------------|
| **Morphological Closing** | (A ⊕ B) ⊖ B | Đơn giản, nhanh | Có thể lấp cả lỗ lớn |
| **Flood Fill** | Fill từ biên | Chính xác | Phức tạp hơn |
| **Reconstruction** | Iterate dilation | Lấp chính xác mọi lỗ | Chậm |

## Ưu Nhược Điểm

### Connected Components Analysis

**Ưu điểm:**
- Tách và đếm vật thể tự động
- Tính toán nhanh (thuật toán tối ưu)
- Cung cấp thông tin chi tiết về từng component
- Hỗ trợ filtering linh hoạt

**Nhược điểm:**
- Chỉ hoạt động với ảnh nhị phân rõ ràng
- Nhạy với nhiễu (nhiễu tạo thêm component)
- Vật thể dính nhau được coi là 1 component
- Cần preprocessing tốt (thresholding, morphology)

### Hole Filling

**Ưu điểm:**
- Phục hồi vật thể bị khuyết
- Đơn giản với Morphological Closing
- Hiệu quả cho lỗ nhỏ

**Nhược điểm:**
- Closing có thể lấp cả lỗ lớn không mong muốn
- Kernel size khó chọn
- Có thể nối nhầm các vật thể gần nhau

## Kỹ Thuật Nâng Cao

### 1. Component Statistics với connectedComponentsWithStats

```python
import cv2
import numpy as np

img = cv2.imread('objects.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Connected Components với statistics
n, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)

# stats[i] = [left, top, width, height, area]
# centroids[i] = [cx, cy]

print(f"Số components: {n - 1}")
for i in range(1, n):  # Bỏ qua background
    x, y, w, h, area = stats[i]
    cx, cy = centroids[i]
    print(f"Component {i}:")
    print(f"  BBox: ({x}, {y}, {w}, {h})")
    print(f"  Area: {area}")
    print(f"  Centroid: ({cx:.2f}, {cy:.2f})")
```

### 2. Selective Hole Filling

```python
import cv2
import numpy as np

img = cv2.imread('object.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Tìm holes
inverted = cv2.bitwise_not(binary)
n, labels = cv2.connectedComponents(inverted)

# Lọc holes theo kích thước
filled = binary.copy()
for label in range(1, n):
    hole_mask = (labels == label).astype(np.uint8) * 255
    area = np.sum(hole_mask == 255)

    # Chỉ lấp holes nhỏ hơn threshold
    if area < 500:
        filled[hole_mask == 255] = 255

cv2.imwrite('selective_filled.png', filled)
```

### 3. Component Merging (Gộp Components Gần Nhau)

```python
import cv2
import numpy as np
from scipy.spatial import distance_matrix

img = cv2.imread('objects.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

n, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)

# Tính khoảng cách giữa các centroids
distances = distance_matrix(centroids[1:], centroids[1:])

# Gộp components gần nhau
merge_threshold = 50
merged_labels = labels.copy()
label_map = {i: i for i in range(n)}

for i in range(1, n):
    for j in range(i+1, n):
        if distances[i-1, j-1] < merge_threshold:
            # Gộp j vào i
            old_label = label_map[j]
            new_label = label_map[i]
            merged_labels[labels == old_label] = new_label
            label_map[j] = new_label

# Đếm số components sau gộp
unique_labels = len(np.unique(merged_labels)) - 1
print(f"Components sau gộp: {unique_labels}")
```

### 4. Shape-based Component Classification

```python
import cv2
import numpy as np

img = cv2.imread('shapes.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def classify_shape(contour):
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0

    # Approximate polygon
    epsilon = 0.04 * perimeter
    approx = cv2.approxPolyDP(contour, epsilon, True)
    vertices = len(approx)

    if circularity > 0.85:
        return "Circle"
    elif vertices == 3:
        return "Triangle"
    elif vertices == 4:
        x, y, w, h = cv2.boundingRect(contour)
        aspect = w / h
        if 0.95 <= aspect <= 1.05:
            return "Square"
        else:
            return "Rectangle"
    else:
        return f"Polygon-{vertices}"

# Phân loại
for idx, cnt in enumerate(contours):
    shape = classify_shape(cnt)
    print(f"Component {idx+1}: {shape}")
```

### 5. Component Tracking (Theo Dõi Components Qua Nhiều Frame)

```python
import cv2
import numpy as np

def get_components(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    n, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)
    return centroids[1:], stats[1:]  # Bỏ qua background

# Giả sử có video
cap = cv2.VideoCapture('objects.mp4')
prev_centroids = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    centroids, stats = get_components(frame)

    if prev_centroids is not None:
        # Matching components giữa frames
        from scipy.spatial import distance_matrix
        distances = distance_matrix(prev_centroids, centroids)

        # Tìm best match (Hungarian algorithm hoặc đơn giản min distance)
        for i, prev_c in enumerate(prev_centroids):
            if len(centroids) > 0:
                nearest_idx = np.argmin(distances[i])
                nearest_dist = distances[i, nearest_idx]
                if nearest_dist < 50:  # Threshold
                    # Match found
                    cv2.line(frame,
                             tuple(prev_c.astype(int)),
                             tuple(centroids[nearest_idx].astype(int)),
                             (0, 255, 0), 2)

    prev_centroids = centroids
    cv2.imshow('Tracking', frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## Tài Liệu Tham Khảo

### Sách

1. **Digital Image Processing** - Gonzalez & Woods
   - Chương 9.5: Component Labeling

2. **Computer Vision: Algorithms and Applications** - Szeliski
   - Chương 3.3.3: Connected Components

### Papers

1. **He, L., et al. (2017)**
   - "A Run-Based Two-Scan Labeling Algorithm"
   - IEEE Transactions on Image Processing

2. **Rosenfeld, A. & Pfaltz, J. L. (1966)**
   - "Sequential Operations in Digital Picture Processing"
   - Journal of the ACM

### Online

- **OpenCV Connected Components**: https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html
- **scikit-image Label**: https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.label

## Liên Kết

- [Bài 2: Lấp Lỗ](../code-reading-guide/bai-2-how-to-read.md)
- [Bài 5: Phân Đoạn Ký Tự](../code-reading-guide/bai-5-how-to-read.md)
- [Bài 6: Đo Đạc Hạt](../code-reading-guide/bai-6-how-to-read.md)

---

**Nguồn**: T61-78 - Ph.D Phan Thanh Toàn
