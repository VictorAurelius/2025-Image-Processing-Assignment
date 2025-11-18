# 01 - Cơ Bản Xử Lý Hình Thái (Morphology Fundamentals)

## Tổng Quan

Xử lý hình thái (Morphological Image Processing) là một tập hợp các kỹ thuật xử lý ảnh dựa trên hình dạng, sử dụng các phép toán tập hợp. Được phát triển bởi Georges Matheron và Jean Serra vào những năm 1960, xử lý hình thái ban đầu được thiết kế cho ảnh nhị phân nhưng sau đó được mở rộng cho ảnh mức xám.

Bốn phép toán cơ bản trong xử lý hình thái là **Erosion** (xói mòn), **Dilation** (giãn nở), **Opening** (mở), và **Closing** (đóng). Các phép toán này sử dụng một **Structuring Element** (SE) - một mẫu hình dạng nhỏ - để khám phá và sửa đổi cấu trúc của ảnh.

Xử lý hình thái đặc biệt hiệu quả trong các tác vụ như khử nhiễu, phân đoạn ảnh, phát hiện biên, và trích xuất đặc trưng hình dạng. Khác với các phương pháp dựa trên convolution (như Gaussian blur), xử lý hình thái bảo toàn cấu trúc hình học và biên của vật thể.

## Ứng Dụng

Các phép toán morphology cơ bản được ứng dụng rộng rãi trong các bài tập thực tế:

- **Bài 1 (Opening)**: Làm sạch văn bản quét - sử dụng Opening để khử nhiễu muối tiêu trên tài liệu
- **Bài 2 (Closing)**: Lấp lỗ và nối nét - sử dụng Closing để phục hồi vật thể bị khuyết
- **Bài 3 (Gradient)**: Trích biên bằng morphological gradient (Dilation - Erosion)
- **Bài 4 (Watershed)**: Sử dụng Erosion/Dilation kết hợp với Distance Transform để tách đối tượng dính nhau
- **Bài 5 (Character Segmentation)**: Kết hợp Opening và Closing để phân đoạn ký tự

## Nguyên Lý Toán Học

### 1. Erosion (Xói Mòn)

Erosion là phép toán "thu nhỏ" vật thể bằng cách loại bỏ các pixel ở biên.

**Công thức (Ảnh nhị phân):**
```
A ⊖ B = {z | (B)z ⊆ A}
```

Trong đó:
- `A` là ảnh đầu vào
- `B` là structuring element
- `(B)z` là B được tịnh tiến đến vị trí z
- Erosion chỉ giữ lại các pixel z mà khi đặt SE tại đó, toàn bộ SE nằm trong vật thể A

**Công thức (Ảnh mức xám):**
```
(A ⊖ B)(x,y) = min{A(x+s, y+t) - B(s,t) | (s,t) ∈ D_B}
```

**Tính chất:**
- Erosion là phép đối ngẫu với Dilation
- Erosion(A ∪ B) ⊇ Erosion(A) ∪ Erosion(B)
- Giảm kích thước vật thể
- Loại bỏ các thành phần nhỏ hơn SE

### 2. Dilation (Giãn Nở)

Dilation là phép toán "phồng lên" vật thể bằng cách thêm pixel vào biên.

**Công thức (Ảnh nhị phân):**
```
A ⊕ B = {z | (B̂)z ∩ A ≠ ∅}
```

Trong đó:
- `B̂` là phản chiếu của B
- Dilation giữ lại pixel z nếu SE (đã phản chiếu) tại z giao với A không rỗng

**Công thức (Ảnh mức xám):**
```
(A ⊕ B)(x,y) = max{A(x-s, y-t) + B(s,t) | (s,t) ∈ D_B}
```

**Tính chất:**
- Dilation(A ∪ B) = Dilation(A) ∪ Dilation(B)
- Tăng kích thước vật thể
- Lấp các lỗ nhỏ
- Nối các thành phần gần nhau

### 3. Opening (Mở)

Opening là phép Erosion tiếp theo Dilation với cùng SE.

**Công thức:**
```
A ∘ B = (A ⊖ B) ⊕ B
```

**Tính chất:**
- Opening ≤ Original (luôn nhỏ hơn hoặc bằng ảnh gốc)
- Loại bỏ các vật thể nhỏ hơn SE
- Làm mịn đường biên phía ngoài
- Tách các vật thể nối nhau bởi cầu nối mỏng
- Opening(Opening(A)) = Opening(A) (idempotent)

**Ứng dụng:**
- Khử nhiễu muối tiêu (Bài 1)
- Loại bỏ chi tiết nhỏ không mong muốn

### 4. Closing (Đóng)

Closing là phép Dilation tiếp theo Erosion với cùng SE.

**Công thức:**
```
A • B = (A ⊕ B) ⊖ B
```

**Tính chất:**
- Closing ≥ Original (luôn lớn hơn hoặc bằng ảnh gốc)
- Lấp các lỗ nhỏ hơn SE
- Làm mịn đường biên phía trong
- Nối các khe hở nhỏ
- Closing(Closing(A)) = Closing(A) (idempotent)

**Ứng dụng:**
- Lấp lỗ trong vật thể (Bài 2)
- Nối các nét gần nhau

## Code Examples (OpenCV)

### Example 1: Erosion và Dilation Cơ Bản

```python
import cv2
import numpy as np

# Đọc ảnh và nhị phân hóa
img = cv2.imread('input.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Tạo Structuring Element
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# Erosion
eroded = cv2.erode(binary, kernel, iterations=1)

# Dilation
dilated = cv2.dilate(binary, kernel, iterations=1)

# Lưu kết quả
cv2.imwrite('eroded.png', eroded)
cv2.imwrite('dilated.png', dilated)
```

**Giải thích:**
- `cv2.getStructuringElement()`: Tạo SE với hình dạng RECT, ELLIPSE, hoặc CROSS
- `iterations`: Số lần lặp lại phép toán (tăng hiệu ứng)

### Example 2: Opening để Khử Nhiễu

```python
import cv2
import numpy as np

# Tạo ảnh nhiễu muối tiêu
img = cv2.imread('noisy_document.png', 0)
_, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Opening với kernel nhỏ
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

# So sánh trước/sau
removed_noise = np.sum(binary != opened)
print(f"Số pixel nhiễu đã loại: {removed_noise}")

cv2.imwrite('cleaned.png', opened)
```

**Kết quả mong đợi:**
- Nhiễu muối tiêu (hạt đen/trắng rời rạc) bị loại bỏ
- Nét chữ chính được bảo toàn
- Ảnh sạch hơn, dễ đọc hơn

### Example 3: Closing để Lấp Lỗ

```python
import cv2
import numpy as np

# Ảnh có lỗ nhỏ
img = cv2.imread('object_with_holes.png', 0)
_, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Closing để lấp lỗ
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

# Tính diện tích trước/sau
area_before = np.sum(binary == 255)
area_after = np.sum(closed == 255)
filled = area_after - area_before

print(f"Diện tích lấp thêm: {filled} pixels ({filled/area_before*100:.2f}%)")
```

**Kết quả mong đợi:**
- Lỗ nhỏ bên trong vật thể được lấp đầy
- Khe hở giữa các phần gần nhau được nối lại
- Diện tích vật thể tăng lên

### Example 4: So Sánh Các Loại Structuring Element

```python
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('input.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Tạo các SE khác nhau
se_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
se_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
se_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))

# Áp dụng Opening
open_rect = cv2.morphologyEx(binary, cv2.MORPH_OPEN, se_rect)
open_ellipse = cv2.morphologyEx(binary, cv2.MORPH_OPEN, se_ellipse)
open_cross = cv2.morphologyEx(binary, cv2.MORPH_OPEN, se_cross)

# Hiển thị
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
axes[0].imshow(binary, 'gray'); axes[0].set_title('Gốc')
axes[1].imshow(open_rect, 'gray'); axes[1].set_title('RECT')
axes[2].imshow(open_ellipse, 'gray'); axes[2].set_title('ELLIPSE')
axes[3].imshow(open_cross, 'gray'); axes[3].set_title('CROSS')
plt.show()
```

### Example 5: Custom Structuring Element

```python
import cv2
import numpy as np

# Tạo SE tùy chỉnh (horizontal line)
se_horizontal = np.array([[0, 0, 0],
                          [1, 1, 1],
                          [0, 0, 0]], dtype=np.uint8)

# Tạo SE tùy chỉnh (vertical line)
se_vertical = np.array([[0, 1, 0],
                        [0, 1, 0],
                        [0, 1, 0]], dtype=np.uint8)

img = cv2.imread('lines.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Trích xuất đường ngang
horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, se_horizontal)

# Trích xuất đường dọc
vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, se_vertical)

cv2.imwrite('horizontal.png', horizontal_lines)
cv2.imwrite('vertical.png', vertical_lines)
```

## So Sánh Các Phương Pháp

| Phép Toán | Công Thức | Hiệu Ứng | Ứng Dụng Chính | Kernel Phù Hợp |
|-----------|-----------|----------|----------------|----------------|
| **Erosion** | A ⊖ B | Thu nhỏ vật thể, loại bỏ pixel biên | Tách vật thể, làm mỏng | RECT cho ảnh kỹ thuật, ELLIPSE cho vật thể tự nhiên |
| **Dilation** | A ⊕ B | Phồng to vật thể, thêm pixel biên | Nối khe hở, lấp lỗ nhỏ | ELLIPSE cho mịn màng, RECT cho góc cạnh |
| **Opening** | (A ⊖ B) ⊕ B | Loại bỏ vật thể nhỏ, làm mịn biên ngoài | Khử nhiễu, tách vật thể | 3x3 hoặc 5x5 cho nhiễu nhỏ |
| **Closing** | (A ⊕ B) ⊖ B | Lấp lỗ, làm mịn biên trong | Phục hồi vật thể, nối nét | 5x5 hoặc 7x7 cho lỗ vừa |

### So Sánh Opening vs Closing

| Đặc Điểm | Opening | Closing |
|----------|---------|---------|
| **Thứ tự** | Erosion → Dilation | Dilation → Erosion |
| **Kết quả vs Gốc** | Nhỏ hơn hoặc bằng | Lớn hơn hoặc bằng |
| **Loại bỏ** | Vật thể nhỏ bên ngoài | Lỗ nhỏ bên trong |
| **Biên** | Làm mịn biên ngoài | Làm mịn biên trong |
| **Ứng dụng** | Khử nhiễu, tách vật thể | Lấp lỗ, nối nét |

### So Sánh với Phương Pháp Khác

| Phương Pháp | Ưu Điểm | Nhược Điểm | Khi Nào Dùng |
|-------------|---------|------------|--------------|
| **Morphology** | Bảo toàn hình dạng, nhanh, đơn giản | Chỉ hiệu quả với ảnh nhị phân/có cấu trúc rõ | Ảnh nhị phân, tài liệu, linh kiện |
| **Gaussian Blur** | Làm mịn đều, tốt cho ảnh tự nhiên | Mất biên, không bảo toàn hình dạng | Ảnh tự nhiên, khử nhiễu Gaussian |
| **Median Filter** | Tốt cho nhiễu muối tiêu | Chậm hơn morphology | Ảnh có nhiễu impulse |
| **Bilateral Filter** | Bảo toàn biên, làm mịn vùng phẳng | Rất chậm | Ảnh tự nhiên cần giữ biên |

## Ưu Nhược Điểm

### Ưu Điểm

1. **Đơn Giản và Trực Quan**
   - Dễ hiểu về mặt hình học
   - Kết quả có thể dự đoán được
   - Ít tham số cần điều chỉnh

2. **Hiệu Quả Tính Toán**
   - Thuật toán đơn giản, chạy nhanh
   - Có thể tối ưu hóa phần cứng
   - Phù hợp cho real-time processing

3. **Bảo Toàn Cấu Trúc**
   - Giữ nguyên hình dạng cơ bản
   - Không làm mờ biên như convolution
   - Hiệu quả cho ảnh nhị phân và có cấu trúc rõ ràng

4. **Linh Hoạt**
   - Có thể tùy chỉnh SE theo nhu cầu
   - Kết hợp các phép toán để tạo hiệu ứng phức tạp
   - Mở rộng được cho ảnh mức xám

### Nhược Điểm

1. **Nhạy Cảm với Structuring Element**
   - Kích thước SE ảnh hưởng lớn đến kết quả
   - Cần thử nghiệm để chọn SE phù hợp
   - SE không phù hợp có thể làm hỏng ảnh

2. **Giới Hạn với Ảnh Phức Tạp**
   - Hiệu quả giảm với ảnh có nhiều noise hoặc texture phức tạp
   - Khó xử lý các vật thể có hình dạng không đồng nhất
   - Không tốt cho ảnh tự nhiên có gradient mềm

3. **Mất Thông Tin**
   - Opening có thể loại bỏ chi tiết quan trọng
   - Erosion làm nhỏ vật thể, có thể mất đi hoàn toàn
   - Closing có thể nối nhầm các vật thể gần nhau

4. **Thiếu Tính Adaptive**
   - Cùng một SE được áp dụng trên toàn ảnh
   - Không thích nghi với từng vùng cục bộ
   - Khó xử lý ảnh có chiếu sáng không đồng đều

## Kỹ Thuật Nâng Cao

### 1. Multi-Scale Morphology

Sử dụng nhiều kernel size khác nhau để phát hiện cấu trúc ở các tỷ lệ khác nhau:

```python
import cv2
import numpy as np

img = cv2.imread('input.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Multi-scale opening
results = []
for size in [3, 5, 7, 9]:
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    results.append(opened)

# Kết hợp kết quả (ví dụ: lấy max)
combined = np.maximum.reduce(results)
```

### 2. Conditional Morphology

Áp dụng morphology có điều kiện dựa trên đặc tính cục bộ:

```python
import cv2
import numpy as np

img = cv2.imread('input.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Tính mật độ cục bộ
kernel_density = np.ones((15, 15), np.float32) / 225
density = cv2.filter2D(binary.astype(np.float32), -1, kernel_density)

# Áp dụng morphology mạnh hơn ở vùng mật độ cao
kernel_small = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
kernel_large = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))

opened_small = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_small)
opened_large = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_large)

# Kết hợp dựa trên mật độ
result = np.where(density > 0.5, opened_large, opened_small)
```

### 3. Sequential Morphology

Kết hợp nhiều phép toán morphology theo trình tự:

```python
import cv2

img = cv2.imread('noisy_holes.png', 0)
_, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Pipeline: Opening → Closing → Opening
kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

step1 = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel1)   # Khử nhiễu
step2 = cv2.morphologyEx(step1, cv2.MORPH_CLOSE, kernel2)   # Lấp lỗ
step3 = cv2.morphologyEx(step2, cv2.MORPH_OPEN, kernel1)    # Làm mịn lại

cv2.imwrite('cleaned.png', step3)
```

### 4. Anisotropic Morphology

Sử dụng SE có hướng để xử lý cấu trúc có phương:

```python
import cv2
import numpy as np

img = cv2.imread('lines.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# SE cho đường ngang (dài theo chiều ngang)
se_horizontal = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))

# SE cho đường dọc (dài theo chiều dọc)
se_vertical = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))

# Trích xuất đường ngang
horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, se_horizontal)

# Trích xuất đường dọc
vertical = cv2.morphologyEx(binary, cv2.MORPH_OPEN, se_vertical)

# Kết hợp
grid = cv2.bitwise_or(horizontal, vertical)
```

### 5. Morphological Reconstruction

Tái tạo vật thể từ marker và mask:

```python
import cv2
import numpy as np

# Marker: Phần chắc chắn là vật thể (ví dụ: sau erosion mạnh)
# Mask: Ranh giới tối đa (ảnh gốc)

img = cv2.imread('input.png', 0)
_, mask = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Tạo marker bằng erosion mạnh
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
marker = cv2.erode(mask, kernel, iterations=3)

# Reconstruction: Dilation lặp cho đến khi không thay đổi, giới hạn bởi mask
reconstructed = marker.copy()
kernel_small = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

while True:
    dilated = cv2.dilate(reconstructed, kernel_small)
    dilated = cv2.min(dilated, mask)  # Giới hạn bởi mask

    if np.array_equal(dilated, reconstructed):
        break
    reconstructed = dilated

cv2.imwrite('reconstructed.png', reconstructed)
```

## Tài Liệu Tham Khảo

### Sách Giáo Khoa

1. **Digital Image Processing** - Rafael C. Gonzalez & Richard E. Woods
   - Chương 9: Morphological Image Processing
   - Trang 645-710 (Phiên bản thứ 4)

2. **Morphological Image Analysis** - Pierre Soille
   - Toàn bộ sách chuyên sâu về morphology
   - Springer, 2003

3. **Computer Vision: Algorithms and Applications** - Richard Szeliski
   - Chương 3.3: Morphological Operations

### Paper Quan Trọng

1. Serra, J. (1982). "Image Analysis and Mathematical Morphology"
   - Nền tảng lý thuyết về morphology

2. Haralick, R. M., et al. (1987). "Image Analysis Using Mathematical Morphology"
   - IEEE PAMI, Vol. 9, No. 4

3. Soille, P., & Talbot, H. (2001). "Directional Morphological Filtering"
   - IEEE PAMI, Vol. 23, No. 11

### Tài Liệu Trực Tuyến

1. **OpenCV Documentation**
   - https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html
   - Tutorial đầy đủ với code examples

2. **scikit-image Documentation**
   - https://scikit-image.org/docs/stable/api/skimage.morphology.html
   - Thư viện Python cho morphology

3. **HIPR2 (Hypermedia Image Processing Reference)**
   - https://homepages.inf.ed.ac.uk/rbf/HIPR2/morops.htm
   - Giải thích trực quan với hình ảnh

### Video Tutorials

1. **First Principles of Computer Vision** - Shree Nayar (Columbia University)
   - Playlist về Mathematical Morphology trên YouTube

2. **Digital Image Processing** - NPTEL Course
   - Lectures 28-30: Morphological Operations

## Liên Kết

### Liên Kết Nội Bộ

- **Bài Tập Thực Hành**:
  - [Bài 1: Làm Sạch Văn Bản (Opening)](../code-reading-guide/bai-1-how-to-read.md)
  - [Bài 2: Lấp Lỗ (Closing)](../code-reading-guide/bai-2-how-to-read.md)
  - [Bài 3: Trích Biên (Gradient)](../code-reading-guide/bai-3-how-to-read.md)

- **Theory Liên Quan**:
  - [02 - Advanced Morphology](./02-advanced-morphology.md): Gradient, Top-hat, Black-hat
  - [03 - Binary Morphology](./03-binary-morphology.md): Connected Components, Holes Filling
  - [04 - Grayscale Morphology](./04-grayscale-morphology.md): Morphology cho ảnh mức xám

### Liên Kết Bên Ngoài

- **OpenCV Morphology Tutorial**: https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html
- **MATLAB Morphology**: https://www.mathworks.com/help/images/morphological-filtering.html
- **Interactive Morphology Demo**: http://www.dai.ed.ac.uk/HIPR2/morops.htm

---

**Tác giả**: Dựa trên giáo trình T61-78 của Ph.D Phan Thanh Toàn
**Cập nhật**: 2025
**Code Repository**: `/code-implement/T61-xu-ly-hinh-thai/`
