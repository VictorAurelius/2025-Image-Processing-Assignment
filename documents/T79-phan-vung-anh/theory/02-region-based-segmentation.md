# Lý Thuyết: Phân Vùng Dựa Trên Vùng (Region-Based Segmentation)

## Tổng Quan

Phân vùng dựa trên vùng (region-based segmentation) là phương pháp nhóm các pixel liền kề có thuộc tính tương đồng (màu sắc, độ sáng, texture) thành các vùng đồng nhất. Khác với phương pháp dựa trên biên (edge-based), region-based tập trung vào sự tương đồng bên trong vùng thay vì sự khác biệt giữa các vùng.

Hai kỹ thuật chính trong nhóm này là **Region Growing** (lan tỏa vùng từ các điểm giống) và **Split-and-Merge** (tách và hợp vùng theo cây tứ phân). Region Growing bắt đầu từ seed points và mở rộng dần theo tiêu chí tương đồng, trong khi Split-and-Merge chia nhỏ ảnh thành các vùng rồi hợp những vùng tương đồng.

Phương pháp region-based đặc biệt hiệu quả với ảnh y tế (tách tổn thương, u), ảnh viễn thám (phân loại đất), và các ứng dụng cần phân vùng chính xác vùng có thuộc tính đồng nhất.

## Ứng Dụng

- **Bài 6**: Region Growing - Tách tổn thương trên ảnh siêu âm/CT
- **Bài 7**: Split-Merge - Phân đoạn phong cảnh (trời/biển/đất)

## Nguyên Lý Toán Học

### 1. Region Growing (Lan Tỏa Vùng)

**Ý tưởng:** Bắt đầu từ seed points, lan tỏa sang các pixel láng giềng thỏa mãn tiêu chí tương đồng.

**Thuật toán:**

```
Input: Ảnh I, seeds S = {s₁, s₂, ..., sₙ}, ngưỡng τ
Output: Vùng R

1. Khởi tạo R = S, Q = S (queue)
2. While Q không rỗng:
   a. Lấy pixel p từ Q
   b. For each láng giềng n của p:
      - Nếu n chưa được xét và |I(n) - I(p)| ≤ τ:
        * Thêm n vào R
        * Thêm n vào Q
3. Return R
```

**Tiêu chí tương đồng phổ biến:**

1. **Sai khác cục bộ:**
   ```
   |I(p) - I(seed)| ≤ τ
   ```

2. **Sai khác với láng giềng:**
   ```
   |I(p) - I(n)| ≤ τ
   ```

3. **Sai khác với trung bình vùng:**
   ```
   |I(p) - μᴿ| ≤ τ, với μᴿ = mean(I(r)) ∀r ∈ R
   ```

4. **Tiêu chí kết hợp:**
   ```
   |I(p) - μᴿ| ≤ τ₁ AND σᴿ ≤ τ₂
   ```
   với σᴿ là độ lệch chuẩn vùng R

**Độ phức tạp:**
- Thời gian: O(n) với n là số pixel trong vùng
- Không gian: O(n) cho queue và visited array

**Láng giềng:**
- 4-connected: {(0,1), (1,0), (0,-1), (-1,0)}
- 8-connected: thêm {(1,1), (1,-1), (-1,1), (-1,-1)}

### 2. Split-and-Merge (Tách và Hợp)

**Ý tưởng:** Chia đệ quy ảnh thành các vùng nhỏ (quadtree), sau đó hợp những vùng tương đồng.

**Thuật toán Split:**

```
Split(Region R):
1. Nếu R đồng nhất (homogeneous):
   - Dừng
2. Ngược lại:
   - Chia R thành 4 vùng con (quadrants)
   - Đệ quy Split(R₁), Split(R₂), Split(R₃), Split(R₄)
```

**Tiêu chí đồng nhất:**

1. **Độ lệch chuẩn:**
   ```
   H(R) = True nếu σ(R) ≤ σ_max
   ```

2. **Range:**
   ```
   H(R) = True nếu max(R) - min(R) ≤ threshold
   ```

3. **Variance:**
   ```
   H(R) = True nếu Var(R) ≤ τ
   ```

**Thuật toán Merge:**

```
Merge(Regions):
1. For each cặp vùng láng giềng Rᵢ, Rⱼ:
   a. Nếu |μ(Rᵢ) - μ(Rⱼ)| ≤ τ:
      - Hợp Rᵢ và Rⱼ thành R_new
      - Cập nhật danh sách vùng
2. Lặp cho đến khi không hợp được nữa
```

**Độ phức tạp:**
- Split: O(n log n) với n là số pixel
- Merge: O(m²) với m là số vùng sau split
- Tổng: O(n log n + m²)

### 3. Felzenszwalb's Efficient Graph-Based Segmentation

Phương pháp hiện đại kết hợp split-merge trên graph.

**Ý tưởng:** Mô hình ảnh như đồ thị G = (V, E) với:
- V: pixels
- E: edges với trọng số w(eᵢⱼ) = |I(i) - I(j)|

**Tiêu chí hợp vùng:**

```
Int(C) = max(w(e)) với e ∈ MST(C)  (internal difference)
Diff(C₁, C₂) = min(w(eᵢⱼ)) với i ∈ C₁, j ∈ C₂  (external difference)

Merge nếu: Diff(C₁, C₂) ≤ min(Int(C₁) + τ(C₁), Int(C₂) + τ(C₂))
với τ(C) = k/|C|  (threshold function)
```

**Tham số:**
- k (scale): Độ ưu tiên vùng lớn (↑k → ít vùng hơn)
- σ (sigma): Gaussian smoothing trước khi phân vùng
- min_size: Diện tích tối thiểu vùng

**Độ phức tạp:** O(n log n) với Kruskal's MST

## Code Examples (OpenCV)

### 1. Region Growing cơ bản

```python
import cv2
import numpy as np
from collections import deque

def region_growing(gray, seeds, tau=5):
    """
    Region Growing với 8-láng giềng.

    Args:
        gray: Ảnh xám (H×W)
        seeds: List các seed points [(y1, x1), (y2, x2), ...]
        tau: Ngưỡng sai khác cho phép

    Returns:
        mask: Ảnh nhị phân vùng đã lan tỏa
    """
    H, W = gray.shape
    visited = np.zeros_like(gray, dtype=np.uint8)
    mask = np.zeros_like(gray, dtype=np.uint8)

    # 8 hướng láng giềng
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    # BFS queue
    queue = deque()

    # Khởi tạo với seeds
    for sy, sx in seeds:
        if 0 <= sy < H and 0 <= sx < W:
            queue.append((sy, sx))
            visited[sy, sx] = 1
            mask[sy, sx] = 255

    # BFS lan tỏa
    while queue:
        y, x = queue.popleft()

        for dy, dx in directions:
            ny, nx = y + dy, x + dx

            # Kiểm tra biên và đã thăm
            if 0 <= ny < H and 0 <= nx < W and not visited[ny, nx]:
                # Tiêu chí tương đồng
                if abs(int(gray[ny, nx]) - int(gray[y, x])) <= tau:
                    visited[ny, nx] = 1
                    mask[ny, nx] = 255
                    queue.append((ny, nx))

    return mask
```

### 2. Region Growing cải tiến với tiêu chí động

```python
def region_growing_dynamic(gray, seeds, tau_local=5, tau_global=10):
    """
    Region Growing với tiêu chí kết hợp local và global.

    Tiêu chí:
    1. |I(p) - I(neighbor)| ≤ tau_local
    2. |I(p) - mean(Region)| ≤ tau_global
    """
    H, W = gray.shape
    visited = np.zeros_like(gray, dtype=np.uint8)
    mask = np.zeros_like(gray, dtype=np.uint8)
    directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

    queue = deque()
    region_pixels = []

    # Khởi tạo
    for sy, sx in seeds:
        if 0 <= sy < H and 0 <= sx < W:
            queue.append((sy, sx))
            visited[sy, sx] = 1
            mask[sy, sx] = 255
            region_pixels.append(gray[sy, sx])

    # Lan tỏa
    while queue:
        y, x = queue.popleft()
        region_mean = np.mean(region_pixels)  # Cập nhật mean động

        for dy, dx in directions:
            ny, nx = y + dy, x + dx

            if 0 <= ny < H and 0 <= nx < W and not visited[ny, nx]:
                pixel_val = gray[ny, nx]

                # Tiêu chí kết hợp
                local_diff = abs(int(pixel_val) - int(gray[y, x]))
                global_diff = abs(int(pixel_val) - region_mean)

                if local_diff <= tau_local and global_diff <= tau_global:
                    visited[ny, nx] = 1
                    mask[ny, nx] = 255
                    queue.append((ny, nx))
                    region_pixels.append(pixel_val)

    return mask, region_mean
```

### 3. Felzenszwalb Segmentation (scikit-image)

```python
from skimage.segmentation import felzenszwalb
from skimage.segmentation import mark_boundaries
import matplotlib.pyplot as plt

# Đọc ảnh
img = cv2.imread('landscape.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Tham số
scale = 100      # Độ ưu tiên vùng lớn
sigma = 0.8      # Gaussian smoothing
min_size = 150   # Diện tích tối thiểu

# Phân vùng
segments = felzenszwalb(img_rgb, scale=scale, sigma=sigma, min_size=min_size)

print(f"Số vùng: {len(np.unique(segments))}")

# Vẽ biên vùng
boundaries = mark_boundaries(img_rgb, segments, color=(1, 1, 0))

# Hiển thị
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(img_rgb)
axes[0].set_title('Original')
axes[1].imshow(segments, cmap='nipy_spectral')
axes[1].set_title(f'Segments ({len(np.unique(segments))} regions)')
axes[2].imshow(boundaries)
axes[2].set_title('Boundaries')
plt.show()
```

### 4. Morphological Watershed (OpenCV implementation)

```python
import cv2
import numpy as np
from scipy import ndimage

def watershed_segmentation(gray):
    """Watershed segmentation cho vật thể chạm nhau."""

    # Bước 1: Otsu thresholding
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Bước 2: Morphology opening
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)

    # Bước 3: Distance Transform
    dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)

    # Bước 4: Tìm local maxima làm markers
    from skimage.feature import peak_local_max
    coords = peak_local_max(dist, footprint=np.ones((3, 3)), labels=binary)

    mask = np.zeros(dist.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, num_markers = ndimage.label(mask)

    # Bước 5: Watershed
    from skimage.segmentation import watershed
    labels = watershed(-dist, markers, mask=binary.astype(bool))

    return labels, num_markers

# Sử dụng
gray = cv2.imread('coins.png', 0)
labels, num_objects = watershed_segmentation(gray)
print(f"Phát hiện {num_objects} vật thể")
```

## So Sánh Các Phương Pháp

| Phương pháp | Độ phức tạp | Cần seeds? | Ưu điểm chính | Nhược điểm chính |
|------------|-------------|------------|---------------|------------------|
| **Region Growing** | O(n) | Có | Đơn giản, chính xác với seed tốt | Nhạy với seed và τ |
| **Split-Merge** | O(n log n) | Không | Tự động, phân cấp | Chậm, nhiều tham số |
| **Felzenszwalb** | O(n log n) | Không | Nhanh, robust | Cần điều chỉnh scale |
| **Watershed** | O(n log n) | Có (markers) | Tách vật chạm nhau tốt | Oversegmentation |

## Ưu Nhược Điểm

### Region Growing

**Ưu điểm:**
- Đơn giản, trực quan, dễ cài đặt
- Hiệu quả O(n) rất nhanh
- Kết quả chính xác nếu seed và τ phù hợp
- Cho phép kiểm soát vùng từ seed

**Nhược điểm:**
- Cần chọn seed manually (hoặc tự động không chính xác)
- Rất nhạy với τ (quá nhỏ → vùng nhỏ, quá lớn → tràn)
- Nhạy với nhiễu
- Không tách được vật thể chạm nhau

### Split-Merge

**Ưu điểm:**
- Tự động, không cần seed
- Cấu trúc phân cấp (quadtree) hữu ích
- Xử lý tốt vùng có kích thước khác nhau
- Có thể merge ở nhiều mức

**Nhược điểm:**
- Chậm O(n log n + m²)
- Nhiều tham số (σ_max, min_area, merge_threshold)
- Block artifacts (vùng vuông góc)
- Merge có thể không optimal

### Felzenszwalb

**Ưu điểm:**
- Nhanh O(n log n), hiệu quả
- Tự động, robust
- Tham số scale trực quan
- Ít oversegmentation

**Nhược điểm:**
- Không phù hợp cho mọi loại ảnh
- Scale cần điều chỉnh theo ảnh
- Vùng không quá chính xác
- Khó kiểm soát số vùng chính xác

### Watershed

**Ưu điểm:**
- Tách tốt vật thể chạm nhau
- Kết quả chính xác với markers tốt
- Ứng dụng rộng (y tế, đếm vật thể)
- Biên vùng liên tục

**Nhược điểm:**
- Cần tìm markers (phức tạp)
- Dễ oversegmentation với nhiễu
- Phụ thuộc vào distance transform
- Chậm hơn region growing đơn giản

## Kỹ Thuật Nâng Cao

### 1. Seeded Region Growing với Multiple Criteria

```python
def advanced_region_growing(gray, seeds, criteria_func):
    """
    Region Growing với hàm tiêu chí custom.

    criteria_func(pixel, neighbor, region) -> bool
    """
    H, W = gray.shape
    visited = np.zeros_like(gray, dtype=np.uint8)
    mask = np.zeros_like(gray, dtype=np.uint8)
    directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

    queue = deque()
    region_info = {'pixels': [], 'mean': 0, 'std': 0}

    # Khởi tạo
    for sy, sx in seeds:
        if 0 <= sy < H and 0 <= sx < W:
            queue.append((sy, sx))
            visited[sy, sx] = 1
            mask[sy, sx] = 255
            region_info['pixels'].append(gray[sy, sx])

    # Cập nhật thống kê vùng
    def update_region_stats():
        region_info['mean'] = np.mean(region_info['pixels'])
        region_info['std'] = np.std(region_info['pixels'])

    # Lan tỏa
    while queue:
        update_region_stats()
        y, x = queue.popleft()

        for dy, dx in directions:
            ny, nx = y + dy, x + dx

            if 0 <= ny < H and 0 <= nx < W and not visited[ny, nx]:
                # Sử dụng hàm tiêu chí custom
                if criteria_func(gray[ny, nx], gray[y, x], region_info):
                    visited[ny, nx] = 1
                    mask[ny, nx] = 255
                    queue.append((ny, nx))
                    region_info['pixels'].append(gray[ny, nx])

    return mask, region_info

# Ví dụ sử dụng
def my_criteria(pixel, neighbor, region):
    """Tiêu chí kết hợp nhiều điều kiện."""
    local_diff = abs(int(pixel) - int(neighbor))
    global_diff = abs(int(pixel) - region['mean'])

    return (local_diff <= 5 and
            global_diff <= 10 and
            region['std'] <= 15)

mask, info = advanced_region_growing(gray, seeds, my_criteria)
```

### 2. Confidence-Connected Region Growing

```python
def confidence_connected(gray, seeds, multiplier=2.5, initial_radius=1):
    """
    Confidence-Connected Region Growing (ITK-style).

    Tiêu chí: |I(p) - μᴿ| ≤ multiplier × σᴿ
    """
    H, W = gray.shape
    visited = np.zeros_like(gray, dtype=np.uint8)
    mask = np.zeros_like(gray, dtype=np.uint8)
    directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

    # Thu thập pixels xung quanh seeds để ước lượng ban đầu
    initial_pixels = []
    for sy, sx in seeds:
        for dy in range(-initial_radius, initial_radius+1):
            for dx in range(-initial_radius, initial_radius+1):
                ny, nx = sy + dy, sx + dx
                if 0 <= ny < H and 0 <= nx < W:
                    initial_pixels.append(gray[ny, nx])

    # Ước lượng mean và std ban đầu
    mean = np.mean(initial_pixels)
    std = np.std(initial_pixels)

    queue = deque()
    region_pixels = initial_pixels.copy()

    # Khởi tạo seeds
    for sy, sx in seeds:
        queue.append((sy, sx))
        visited[sy, sx] = 1
        mask[sy, sx] = 255

    # Lan tỏa với confidence interval
    iterations = 0
    while queue:
        iterations += 1

        # Cập nhật thống kê mỗi 100 iterations
        if iterations % 100 == 0:
            mean = np.mean(region_pixels)
            std = np.std(region_pixels)

        y, x = queue.popleft()
        threshold = multiplier * std

        for dy, dx in directions:
            ny, nx = y + dy, x + dx

            if 0 <= ny < H and 0 <= nx < W and not visited[ny, nx]:
                pixel_val = gray[ny, nx]

                if abs(int(pixel_val) - mean) <= threshold:
                    visited[ny, nx] = 1
                    mask[ny, nx] = 255
                    queue.append((ny, nx))
                    region_pixels.append(pixel_val)

    return mask, mean, std
```

### 3. Hierarchical Split-Merge

```python
def hierarchical_split_merge(gray, min_std=5, min_size=16):
    """
    Hierarchical Split-Merge với quadtree.

    Args:
        gray: Ảnh xám
        min_std: Ngưỡng std cho vùng đồng nhất
        min_size: Kích thước tối thiểu vùng
    """
    H, W = gray.shape
    segments = np.zeros((H, W), dtype=np.int32)
    label_id = [1]  # Mutable counter

    def is_homogeneous(region):
        """Kiểm tra vùng có đồng nhất không."""
        return np.std(region) <= min_std

    def split(y1, x1, y2, x2):
        """Chia đệ quy vùng thành quadrants."""
        region = gray[y1:y2, x1:x2]
        h, w = region.shape

        # Điều kiện dừng
        if h < min_size or w < min_size or is_homogeneous(region):
            segments[y1:y2, x1:x2] = label_id[0]
            label_id[0] += 1
            return

        # Chia thành 4 quadrants
        mid_y = (y1 + y2) // 2
        mid_x = (x1 + x2) // 2

        split(y1, x1, mid_y, mid_x)      # Top-left
        split(y1, mid_x, mid_y, x2)      # Top-right
        split(mid_y, x1, y2, mid_x)      # Bottom-left
        split(mid_y, mid_x, y2, x2)      # Bottom-right

    # Bước 1: Split
    split(0, 0, H, W)

    # Bước 2: Merge các vùng láng giềng tương đồng
    def merge_neighbors(segments, gray, threshold=10):
        """Merge các vùng láng giềng có mean gần nhau."""
        changed = True
        while changed:
            changed = False
            labels = np.unique(segments)

            for label in labels:
                if label == 0:
                    continue

                mask = (segments == label)
                mean_val = np.mean(gray[mask])

                # Tìm láng giềng
                dilated = cv2.dilate(mask.astype(np.uint8), np.ones((3, 3)))
                neighbors = np.unique(segments[dilated > 0])

                for neighbor in neighbors:
                    if neighbor != label and neighbor != 0:
                        neighbor_mask = (segments == neighbor)
                        neighbor_mean = np.mean(gray[neighbor_mask])

                        if abs(mean_val - neighbor_mean) <= threshold:
                            segments[neighbor_mask] = label
                            changed = True

        return segments

    segments = merge_neighbors(segments, gray)

    return segments
```

## Tài Liệu Tham Khảo

1. **Adams, R., & Bischof, L.** (1994). "Seeded region growing." IEEE Transactions on Pattern Analysis and Machine Intelligence, 16(6), 641-647.

2. **Felzenszwalb, P. F., & Huttenlocher, D. P.** (2004). "Efficient graph-based image segmentation." International Journal of Computer Vision, 59(2), 167-181.

3. **Horowitz, S. L., & Pavlidis, T.** (1976). "Picture segmentation by a tree traversal algorithm." Journal of the ACM, 23(2), 368-388.

4. **Vincent, L., & Soille, P.** (1991). "Watersheds in digital spaces: an efficient algorithm based on immersion simulations." IEEE Transactions on Pattern Analysis and Machine Intelligence, 13(6), 583-598.

5. **Yoo, T. S., et al.** (2002). "Engineering and algorithm design for an image processing API: A technical report on ITK–the insight toolkit." Studies in Health Technology and Informatics, 586-592.

## Liên Kết

- **Code thực hành:**
  - [Bài 6: Region Growing](/code-implement/T79-phan-vung-anh/bai-6-region-growing/)
  - [Bài 7: Split-Merge](/code-implement/T79-phan-vung-anh/bai-7-split-merge/)
  - [Bài 10: Watershed](/code-implement/T79-phan-vung-anh/bai-10-watershed/)

- **Lý thuyết liên quan:**
  - [01: Thresholding Methods](01-thresholding-methods.md)
  - [03: Clustering Segmentation](03-clustering-segmentation.md)
  - [04: Edge-based Segmentation](04-edge-based-segmentation.md)

- **Tài liệu gốc:** T79-99 Phân vùng ảnh (trang 11-14)

---

**Tác giả:** Ph.D Phan Thanh Toàn
**Cập nhật:** 2025-11-17
**Phiên bản:** 1.0
