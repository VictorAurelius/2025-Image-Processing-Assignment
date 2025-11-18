# 04 - Morphology Mức Xám (Grayscale Morphology)

## Tổng Quan

Grayscale Morphology mở rộng các phép toán morphology từ ảnh nhị phân sang ảnh mức xám, trong đó các phép toán min/max thay thế cho set operations. Thay vì chỉ xử lý 2 giá trị (0 và 1), grayscale morphology xử lý toàn bộ dải giá trị từ 0-255.

Các phép toán cơ bản (Erosion, Dilation, Opening, Closing) vẫn giữ nguyên ý nghĩa hình học nhưng được điều chỉnh cho ảnh mức xám. Top-hat và Black-hat Transform đặc biệt hữu ích trong grayscale morphology để khử nền không đồng đều và tách foreground/background.

## Ứng Dụng

- **Bài 8 (Foreground Extraction)**: Sử dụng Erosion mức xám để tách core và rim
- **Bài 9 (Background Removal)**: Sử dụng Top-hat và Black-hat để khử nền không đồng đều trên ảnh mức xám

## Nguyên Lý Toán Học

### 1. Erosion Mức Xám

**Công thức:**
```
(f ⊖ b)(x,y) = min{f(x+s, y+t) - b(s,t) | (s,t) ∈ D_b}
```

Trong đó:
- `f`: Ảnh đầu vào (grayscale)
- `b`: Structuring element (grayscale hoặc binary)
- `D_b`: Domain của SE

**Ý nghĩa:**
- Thay thế pixel bằng giá trị min trong vùng SE
- "Thu nhỏ" các vùng sáng
- "Phồng to" các vùng tối

**Flat SE (SE phẳng):**
```
(f ⊖ B)(x,y) = min{f(x+s, y+t) | (s,t) ∈ B}
```
- SE chỉ là hình dạng, không có giá trị
- Đơn giản hơn, thường dùng hơn

### 2. Dilation Mức Xám

**Công thức:**
```
(f ⊕ b)(x,y) = max{f(x-s, y-t) + b(s,t) | (s,t) ∈ D_b}
```

**Flat SE:**
```
(f ⊕ B)(x,y) = max{f(x-s, y-t) | (s,t) ∈ B}
```

**Ý nghĩa:**
- Thay thế pixel bằng giá trị max trong vùng SE
- "Phồng to" các vùng sáng
- "Thu nhỏ" các vùng tối

### 3. Opening và Closing Mức Xám

**Opening:**
```
f ∘ b = (f ⊖ b) ⊕ b
```
- Loại bỏ các đỉnh sáng (peaks) nhỏ hơn SE
- Làm phẳng nền

**Closing:**
```
f • b = (f ⊕ b) ⊖ b
```
- Lấp các thung lũng tối (valleys) nhỏ hơn SE
- Làm phẳng nền

### 4. Top-hat và Black-hat

**White Top-hat:**
```
T_white(f) = f - (f ∘ b)
```
- Trích xuất các đỉnh sáng
- Bài 9 dòng 107

**Black Top-hat:**
```
T_black(f) = (f • b) - f
```
- Trích xuất các thung lũng tối
- Bài 9 dòng 117

### 5. Morphological Gradient Mức Xám

**Gradient:**
```
grad(f) = (f ⊕ b) - (f ⊖ b)
```
- Phát hiện biên trên ảnh mức xám
- Bài 3 có thể áp dụng cho grayscale

## Code Examples (OpenCV)

### Example 1: Erosion và Dilation Mức Xám

```python
import cv2
import numpy as np

# Ảnh mức xám (KHÔNG nhị phân hóa)
img = cv2.imread('input.jpg', 0)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# Erosion mức xám
eroded = cv2.erode(img, kernel)
print(f"Erosion làm tối ảnh: {img.mean():.2f} → {eroded.mean():.2f}")

# Dilation mức xám
dilated = cv2.dilate(img, kernel)
print(f"Dilation làm sáng ảnh: {img.mean():.2f} → {dilated.mean():.2f}")

cv2.imwrite('eroded_gray.png', eroded)
cv2.imwrite('dilated_gray.png', dilated)
```

**Từ Bài 8 Code (extract.py):**
- Dòng 114: `core = cv2.erode(A, B)` - Erosion để tạo core
- Input A đã nhị phân nhưng có thể áp dụng cho grayscale

### Example 2: Top-hat Transform (Khử Nền)

```python
import cv2
import numpy as np

# Ảnh có chiếu sáng không đều
img = cv2.imread('uneven_lighting.jpg', 0)

# Kernel lớn để ước lượng nền
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))

# Top-hat: Trích xuất vật thể sáng hơn nền
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

# Black-hat: Trích xuất vật thể tối hơn nền
blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)

# Điều chỉnh: img + tophat - blackhat
corrected = cv2.normalize(img.astype(np.float32) + tophat - blackhat,
                          None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# So sánh histogram
import matplotlib.pyplot as plt
plt.hist(img.ravel(), bins=256, alpha=0.5, label='Original')
plt.hist(corrected.ravel(), bins=256, alpha=0.5, label='Corrected')
plt.legend()
plt.show()

cv2.imwrite('corrected.png', corrected)
```

**Từ Bài 9 Code (remove.py):**
- Dòng 98-100: Tạo kernel RECT 15x15
- Dòng 107: Top-hat transform
- Dòng 117: Black-hat transform
- Dòng 128: Kết hợp để điều chỉnh

### Example 3: Morphological Smoothing

```python
import cv2
import numpy as np

img = cv2.imread('noisy_grayscale.jpg', 0)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# Opening smooths bright peaks
opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# Closing smooths dark valleys
closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

# Combine: (Open + Close) / 2
smoothed = cv2.addWeighted(opened, 0.5, closed, 0.5, 0)

cv2.imwrite('smoothed.png', smoothed)
```

### Example 4: Multi-scale Top-hat

```python
import cv2
import numpy as np

img = cv2.imread('document.jpg', 0)

# Top-hat ở nhiều scales
scales = [7, 15, 31]
tophats = []

for size in scales:
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    tophats.append(tophat)

# Kết hợp (max hoặc weighted sum)
combined = np.maximum.reduce(tophats)  # Lấy max

# Hoặc weighted sum
# combined = tophats[0] * 0.5 + tophats[1] * 0.3 + tophats[2] * 0.2

cv2.imwrite('multi_scale_tophat.png', combined)
```

**Từ Bài 9 Code (remove.py):**
- Dòng 150-171: So sánh nhiều kernel sizes

### Example 5: Contrast Enhancement

```python
import cv2
import numpy as np

img = cv2.imread('low_contrast.jpg', 0)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))

# Top-hat và Black-hat
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)

# Tăng cường tương phản
enhanced = cv2.add(img, tophat)
enhanced = cv2.subtract(enhanced, blackhat)

# So sánh histogram
print(f"Original std: {img.std():.2f}")
print(f"Enhanced std: {enhanced.std():.2f}")

cv2.imwrite('enhanced.png', enhanced)
```

## So Sánh Các Phương Pháp

### Grayscale vs Binary Morphology

| Đặc Điểm | Binary Morphology | Grayscale Morphology |
|----------|------------------|---------------------|
| **Input** | 2 giá trị (0, 1) | 0-255 |
| **Erosion** | Set erosion (AND) | min operation |
| **Dilation** | Set dilation (OR) | max operation |
| **Tốc độ** | Nhanh hơn | Chậm hơn |
| **Ứng dụng** | Phân đoạn, đếm vật thể | Khử nền, tăng cường |

### Top-hat vs Histogram Equalization

| Phương Pháp | Nguyên Lý | Ưu Điểm | Nhược Điểm |
|-------------|-----------|---------|------------|
| **Top-hat** | Morphological, local | Bảo toàn cấu trúc, khử nền tốt | Cần chọn kernel size |
| **Histogram Eq** | Statistical, global | Đơn giản, tự động | Có thể tăng nhiễu |
| **CLAHE** | Adaptive histogram | Tốt cho ảnh y tế | Phức tạp hơn |

## Ưu Nhược Điểm

### Grayscale Morphology

**Ưu điểm:**
- Xử lý trực tiếp ảnh mức xám, không cần thresholding
- Bảo toàn thông tin gradient
- Top-hat/Black-hat hiệu quả cho khử nền
- Tăng cường tương phản cục bộ

**Nhược điểm:**
- Chậm hơn binary morphology
- Nhạy cảm với kernel size
- Có thể tạo artifacts nếu kernel không phù hợp
- Khó visualize kết quả hơn binary

## Kỹ Thuật Nâng Cao

### 1. Adaptive Morphological Filtering

```python
import cv2
import numpy as np

def adaptive_tophat(image, min_size=7, max_size=31):
    # Ước lượng kernel size dựa trên local variance
    local_var = cv2.GaussianBlur(image**2, (15, 15), 0) - \
                cv2.GaussianBlur(image, (15, 15), 0)**2

    # Normalize variance to kernel size range
    kernel_size_map = cv2.normalize(local_var, None,
                                     min_size, max_size,
                                     cv2.NORM_MINMAX).astype(int)

    # Làm cho kernel size là số lẻ
    kernel_size_map = kernel_size_map // 2 * 2 + 1

    result = np.zeros_like(image)

    # Áp dụng top-hat với kernel size khác nhau
    unique_sizes = np.unique(kernel_size_map)
    for size in unique_sizes:
        mask = (kernel_size_map == size)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
        tophat = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)
        result[mask] = tophat[mask]

    return result

img = cv2.imread('variable_background.jpg', 0)
adaptive_result = adaptive_tophat(img)
cv2.imwrite('adaptive_tophat.png', adaptive_result)
```

### 2. Rolling Ball Background Subtraction

```python
import cv2
import numpy as np

def rolling_ball_background(image, radius=50):
    # Tạo structuring element hình cầu
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (radius*2, radius*2))

    # Opening xấp xỉ rolling ball
    background = cv2.morphologyEx(image, cv2.MORPH_OPEN, se)

    # Subtract background
    foreground = cv2.subtract(image, background)

    return foreground, background

img = cv2.imread('fluorescence.tif', 0)
fg, bg = rolling_ball_background(img, radius=30)

cv2.imwrite('foreground.png', fg)
cv2.imwrite('background.png', bg)
```

**Ứng dụng:** Phổ biến trong ảnh y tế (fluorescence microscopy)

### 3. Morphological Gradient Mức Xám với Sobel

```python
import cv2
import numpy as np

img = cv2.imread('input.jpg', 0)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# Morphological gradient
morph_grad = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

# Sobel gradient
sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
sobel_grad = np.sqrt(sobel_x**2 + sobel_y**2)
sobel_grad = cv2.normalize(sobel_grad, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# So sánh
print(f"Morph gradient mean: {morph_grad.mean():.2f}")
print(f"Sobel gradient mean: {sobel_grad.mean():.2f}")

cv2.imwrite('morph_gradient.png', morph_grad)
cv2.imwrite('sobel_gradient.png', sobel_grad)
```

### 4. Toggle Mapping (Contrast Enhancement)

```python
import cv2
import numpy as np

img = cv2.imread('low_contrast.jpg', 0)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# Dilation và Erosion
dilated = cv2.dilate(img, kernel)
eroded = cv2.erode(img, kernel)

# Toggle: Chọn giá trị gần với original nhất
diff_dilation = np.abs(img.astype(np.int16) - dilated.astype(np.int16))
diff_erosion = np.abs(img.astype(np.int16) - eroded.astype(np.int16))

result = np.where(diff_dilation < diff_erosion, dilated, eroded)

cv2.imwrite('toggle_mapped.png', result.astype(np.uint8))
```

**Ứng dụng:** Khử nhiễu mạnh hơn median filter

### 5. Shade Correction (Khử Bóng)

```python
import cv2
import numpy as np

img = cv2.imread('document_shadow.jpg', 0)

# Kernel lớn để ước lượng background
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (51, 51))

# Opening ước lượng background
background = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# Subtract và normalize
corrected = cv2.divide(img, background, scale=255)

# Hoặc dùng top-hat
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
corrected_tophat = cv2.normalize(img.astype(np.float32) + tophat,
                                  None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

cv2.imwrite('shade_corrected.png', corrected)
cv2.imwrite('shade_corrected_tophat.png', corrected_tophat)
```

**Từ Bài 9:** Tương tự shade correction

## Tài Liệu Tham Khảo

### Papers

1. **Sternberg, S. R. (1986)**
   - "Grayscale Morphology"
   - Computer Vision, Graphics, and Image Processing

2. **Soille, P. (2003)**
   - "Morphological Image Analysis"
   - Springer (Chương về Grayscale Morphology)

### Online

- **OpenCV Morphological Transformations**: https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html
- **ImageJ Rolling Ball**: https://imagej.net/plugins/rolling-ball-background-subtraction

## Liên Kết

- [Bài 8: Tách Tiền Cảnh](../code-reading-guide/bai-8-how-to-read.md)
- [Bài 9: Khử Nền](../code-reading-guide/bai-9-how-to-read.md)
- [02 - Advanced Morphology](./02-advanced-morphology.md)

---

**Nguồn**: T61-78 - Ph.D Phan Thanh Toàn
