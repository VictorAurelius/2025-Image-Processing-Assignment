# Lý Thuyết: Phân Vùng Dựa Trên Biên (Edge-Based Segmentation)

## Tổng Quan

Phân vùng dựa trên biên (edge-based segmentation) tập trung vào việc phát hiện các biên (edges) - nơi có sự thay đổi đột ngột về độ sáng hoặc màu sắc - để phân tách các vùng khác nhau trong ảnh. Phương pháp này bổ sung cho region-based segmentation bằng cách tập trung vào ranh giới thay vì nội dung vùng.

Watershed là thuật toán quan trọng nhất trong nhóm này, mô phỏng quá trình ngập nước của địa hình để tách các vật thể chạm nhau. Active Contours (Snakes) sử dụng đường cong biến dạng dưới tác động của energy function để bám sát biên vật thể.

Các phương pháp edge-based đặc biệt hiệu quả trong phân tích ảnh y tế (tách tế bào chạm nhau), đếm vật thể công nghiệp, và các ứng dụng cần ranh giới chính xác.

## Ứng Dụng

- **Bài 5**: Edge Detection + Hough Transform - Phát hiện đường thẳng
- **Bài 10**: Watershed Segmentation - Đếm đồng xu/hạt bi dính nhau

## Nguyên Lý Toán Học

### 1. Watershed Segmentation

**Ý tưởng:** Coi ảnh như địa hình 3D với độ cao = độ sáng, ngập nước từ các minima (markers) cho đến khi gặp watershed lines.

**Thuật toán (Vincent-Soille):**

```
Input: Distance transform D, markers M
Output: Labels L

1. Sắp xếp pixels theo độ cao tăng dần
2. For each mức h từ thấp đến cao:
   a. For each pixel p có D(p) = h:
      - Nếu p láng giềng với label đã có:
        * Gán p vào label đó
      - Nếu p láng giềng với nhiều labels khác nhau:
        * Đánh dấu p là watershed (biên)
3. Return L
```

**Distance Transform:**

```
DT(p) = min{d(p, q) | q ∈ background}
```

Với d là khoảng cách Euclidean hoặc Manhattan.

**Pipeline đầy đủ:**

```
1. Preprocessing: Denoise (Gaussian blur)
2. Thresholding: Otsu/Adaptive
3. Morphology: Opening (loại nhiễu)
4. Distance Transform: cv2.distanceTransform()
5. Find Markers: peak_local_max() hoặc threshold DT
6. Label Markers: ndi.label()
7. Watershed: watershed(-DT, markers, mask)
```

**Độ phức tạp:** O(n log n) với n là số pixels

### 2. Canny Edge Detection

**Bước 1: Gaussian smoothing**

```
G(x,y) = (1/(2πσ²)) × exp(-(x²+y²)/(2σ²))
I_smooth = I ⊗ G
```

**Bước 2: Gradient magnitude và direction**

```
Gₓ = ∂I/∂x (Sobel x)
Gᵧ = ∂I/∂y (Sobel y)

Magnitude: M = √(Gₓ² + Gᵧ²)
Direction: θ = arctan(Gᵧ/Gₓ)
```

**Bước 3: Non-maximum suppression**

Giữ lại pixel nếu M(p) là maximum theo hướng gradient.

**Bước 4: Hysteresis thresholding**

```
- Strong edge: M ≥ T_high
- Weak edge: T_low ≤ M < T_high
- Giữ weak edge nếu kết nối với strong edge
```

**Độ phức tạp:** O(n)

### 3. Hough Transform (Line Detection)

**Hough Space:** Mỗi đường thẳng trong image space tương ứng với một điểm trong Hough space (ρ, θ).

**Phương trình đường thẳng:**

```
ρ = x cos θ + y sin θ
```

Với:
- ρ: Khoảng cách từ gốc tọa độ đến đường thẳng
- θ: Góc của pháp tuyến

**Thuật toán:**

```
1. Khởi tạo accumulator H[ρ, θ] = 0
2. For each edge pixel (x, y):
   a. For θ = 0° to 180°:
      - Tính ρ = x cos θ + y sin θ
      - H[ρ, θ] += 1
3. Tìm local maxima trong H
4. Each maximum → một đường thẳng
```

**Probabilistic Hough Transform (HoughLinesP):**

Nhanh hơn bằng cách sample ngẫu nhiên thay vì kiểm tra tất cả pixels.

**Độ phức tạp:**
- Standard: O(n × θ_bins)
- Probabilistic: O(n) average case

### 4. Active Contours (Snakes)

**Energy Function:**

```
E = ∫₀¹ [E_internal(v(s)) + E_external(v(s))] ds
```

Với v(s) = [x(s), y(s)] là đường cong parametric.

**Internal Energy (smoothness):**

```
E_internal = α|v'(s)|² + β|v''(s)|²
```

- α: Tension (căng)
- β: Rigidity (cứng)

**External Energy (image features):**

```
E_external = -|∇I|²  (gradient magnitude)
```

hoặc:

```
E_external = -∇[Gσ ⊗ I]²  (GVF - Gradient Vector Flow)
```

**Iterative Update:**

```
v^(t+1) = v^(t) - γ × (∂E/∂v)
```

**Độ phức tạp:** O(i × n) với i iterations, n points trên contour

## Code Examples (OpenCV)

### 1. Canny Edge Detection

```python
import cv2
import numpy as np

def canny_edge_detection(gray, low=50, high=150):
    """
    Canny edge detection.

    Args:
        gray: Ảnh xám
        low: Low threshold
        high: High threshold (thường = 2×low hoặc 3×low)

    Returns:
        edges: Ảnh biên nhị phân
    """
    # Denoise
    blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)

    # Canny
    edges = cv2.Canny(blurred, low, high)

    return edges

# Sử dụng
gray = cv2.imread('input.jpg', 0)
edges = canny_edge_detection(gray, low=80, high=160)

cv2.imshow('Edges', edges)
cv2.waitKey(0)
```

### 2. Hough Line Transform

```python
def detect_lines(edges, threshold=80, min_length=60, max_gap=10):
    """
    Phát hiện đường thẳng bằng Hough Transform.

    Args:
        edges: Ảnh biên (từ Canny)
        threshold: Số votes tối thiểu trong Hough space
        min_length: Độ dài tối thiểu của đường thẳng
        max_gap: Khoảng cách tối đa để nối 2 đoạn

    Returns:
        lines: List các đường thẳng [[x1, y1, x2, y2], ...]
    """
    lines = cv2.HoughLinesP(
        edges,
        rho=1,                    # Độ phân giải ρ (pixels)
        theta=np.pi/180,          # Độ phân giải θ (radians)
        threshold=threshold,
        minLineLength=min_length,
        maxLineGap=max_gap
    )

    return lines

# Sử dụng
img = cv2.imread('lanes.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 80, 160)
lines = detect_lines(edges)

# Vẽ đường thẳng
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow('Lines', img)
cv2.waitKey(0)
```

### 3. Watershed Segmentation

```python
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage.segmentation import watershed

def watershed_segmentation(gray):
    """
    Watershed segmentation để tách vật thể chạm nhau.

    Pipeline:
    1. Otsu thresholding
    2. Morphology opening
    3. Distance transform
    4. Find markers (peaks)
    5. Watershed

    Returns:
        labels: Ảnh labels
        num_objects: Số vật thể
    """
    # Bước 1: Otsu
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Bước 2: Opening để loại nhiễu
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)

    # Bước 3: Distance Transform
    dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)

    # Bước 4: Tìm local maxima làm markers
    coords = peak_local_max(dist, footprint=np.ones((3, 3)), labels=binary)

    # Tạo markers
    mask = np.zeros(dist.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, num_markers = ndi.label(mask)

    # Bước 5: Watershed
    labels = watershed(-dist, markers, mask=binary.astype(bool))

    return labels, num_markers

# Sử dụng
gray = cv2.imread('coins.png', 0)
labels, num_objects = watershed_segmentation(gray)
print(f"Phát hiện {num_objects} vật thể")

# Vẽ kết quả
import matplotlib.pyplot as plt
plt.imshow(labels, cmap='nipy_spectral')
plt.title(f'{num_objects} objects')
plt.show()
```

### 4. Active Contours (scikit-image)

```python
from skimage.segmentation import active_contour
from skimage.filters import gaussian

def snake_segmentation(img, init_contour, alpha=0.015, beta=10, gamma=0.001):
    """
    Active contour (snake) segmentation.

    Args:
        img: Ảnh xám
        init_contour: Đường cong khởi tạo (n×2 array)
        alpha: Snake length weight
        beta: Snake smoothness weight
        gamma: Explicit time stepping parameter

    Returns:
        snake: Đường cong hội tụ
    """
    # Smooth image
    img_smooth = gaussian(img, sigma=3, preserve_range=False)

    # Active contour
    snake = active_contour(
        img_smooth,
        init_contour,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
        max_iterations=2500
    )

    return snake

# Sử dụng
img = cv2.imread('object.jpg', 0)

# Khởi tạo circle
s = np.linspace(0, 2*np.pi, 400)
r = 100 + 30*np.sin(s)
c = 220 + 50*np.cos(s)
init = np.array([r, c]).T

# Snake
snake = snake_segmentation(img, init, alpha=0.01, beta=10)

# Vẽ kết quả
import matplotlib.pyplot as plt
plt.imshow(img, cmap='gray')
plt.plot(init[:, 0], init[:, 1], 'r--', label='Initial')
plt.plot(snake[:, 0], snake[:, 1], 'b-', linewidth=2, label='Snake')
plt.legend()
plt.show()
```

## So Sánh Các Phương Pháp

| Phương pháp | Độ phức tạp | Tự động? | Ưu điểm | Nhược điểm |
|------------|-------------|----------|---------|------------|
| **Canny** | O(n) | Bán tự động | Nhanh, chính xác | Cần chọn thresholds |
| **Hough Lines** | O(n×θ) | Tự động | Robust với nhiễu | Chỉ phát hiện hình dạng đặc biệt |
| **Watershed** | O(n log n) | Cần markers | Tách vật chạm nhau tốt | Oversegmentation |
| **Active Contours** | O(i×n) | Cần init | Biên mượt, chính xác | Chậm, nhạy với init |

## Ưu Nhược Điểm

### Watershed

**Ưu điểm:**
- Tách tốt vật thể chạm/dính nhau
- Biên liên tục, đóng kín
- Phù hợp đếm vật thể (cells, coins, etc.)

**Nhược điểm:**
- Oversegmentation với nhiễu
- Cần markers chính xác
- Phụ thuộc distance transform

### Canny + Hough

**Ưu điểm:**
- Nhanh, hiệu quả
- Robust với nhiễu (Canny)
- Phát hiện hình dạng parametric (Hough)

**Nhược điểm:**
- Edges có thể không liên tục
- Cần post-processing để tạo vùng
- Hough chỉ cho hình đơn giản

### Active Contours

**Ưu điểm:**
- Biên mượt, chính xác
- Có thể kết hợp prior knowledge
- Sub-pixel accuracy

**Nhược điểm:**
- Chậm (iterative)
- Nhạy với khởi tạo
- Có thể bị stuck ở local minima

## Tài Liệu Tham Khảo

1. **Canny, J.** (1986). "A computational approach to edge detection." IEEE Transactions on Pattern Analysis and Machine Intelligence, 8(6), 679-698.

2. **Hough, P. V.** (1962). "Method and means for recognizing complex patterns." U.S. Patent 3,069,654.

3. **Vincent, L., & Soille, P.** (1991). "Watersheds in digital spaces: an efficient algorithm based on immersion simulations." IEEE PAMI, 13(6), 583-598.

4. **Kass, M., Witkin, A., & Terzopoulos, D.** (1988). "Snakes: Active contour models." International Journal of Computer Vision, 1(4), 321-331.

## Liên Kết

- **Code:**
  - [Bài 5: Edge + Hough](/code-implement/T79-phan-vung-anh/bai-5-edge-hough/)
  - [Bài 10: Watershed](/code-implement/T79-phan-vung-anh/bai-10-watershed/)

- **Lý thuyết liên quan:**
  - [02: Region-based](02-region-based-segmentation.md)
  - [06: Evaluation](06-segmentation-evaluation.md)

---

**Tác giả:** Ph.D Phan Thanh Toàn | **Cập nhật:** 2025-11-17
