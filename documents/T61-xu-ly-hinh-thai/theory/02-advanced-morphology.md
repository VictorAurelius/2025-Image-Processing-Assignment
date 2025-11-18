# 02 - Phép Toán Morphology Nâng Cao

## Tổng Quan

Ngoài bốn phép toán cơ bản (Erosion, Dilation, Opening, Closing), xử lý hình thái còn cung cấp các phép toán nâng cao như **Morphological Gradient**, **Top-hat Transform**, **Black-hat Transform**, và **Hit-or-Miss Transform**. Các phép toán này được xây dựng từ các phép toán cơ bản nhưng giải quyết những vấn đề đặc thù hơn.

Morphological Gradient giúp phát hiện biên bằng cách tính hiệu giữa Dilation và Erosion. Top-hat và Black-hat Transform được sử dụng để tách foreground/background và khử nền không đồng đều. Hit-or-Miss Transform cho phép phát hiện các mẫu hình dạng cụ thể trong ảnh.

Các phép toán này đặc biệt hữu ích trong preprocessing cho OCR, phân tích ảnh y tế, kiểm tra chất lượng công nghiệp, và phát hiện khuyết tật.

## Ứng Dụng

- **Bài 3 (Gradient)**: Trích biên bằng Morphological Gradient (Dilation - Erosion)
- **Bài 7 (Pruning)**: Sử dụng Hit-or-Miss để xóa pixel thừa ở cạnh (spurs)
- **Bài 8 (Foreground Extraction)**: Sử dụng Erosion để tách core và rim
- **Bài 9 (Background Removal)**: Sử dụng Top-hat và Black-hat để khử nền không đồng đều

## Nguyên Lý Toán Học

### 1. Morphological Gradient

Gradient hình thái phát hiện biên bằng cách tính sự khác biệt giữa Dilation và Erosion.

**Công thức:**
```
grad(A) = (A ⊕ B) - (A ⊖ B)
```

Trong đó:
- `A ⊕ B`: Dilation của A với SE B
- `A ⊖ B`: Erosion của A với SE B
- Kết quả là đường biên có độ dày phụ thuộc vào kích thước B

**Các Biến Thể:**

1. **External Gradient (Gradient Ngoài):**
   ```
   grad_ext(A) = (A ⊕ B) - A
   ```
   - Chỉ lấy pixel được thêm vào bởi Dilation
   - Biên nằm bên ngoài vật thể

2. **Internal Gradient (Gradient Trong):**
   ```
   grad_int(A) = A - (A ⊖ B)
   ```
   - Chỉ lấy pixel bị loại bỏ bởi Erosion
   - Biên nằm bên trong vật thể

3. **Morphological Gradient (Gradient Chuẩn):**
   ```
   grad(A) = (A ⊕ B) - (A ⊖ B)
   ```
   - Biên nằm cả trong và ngoài vật thể
   - Độ dày biên = 2 × kích thước SE

**Tính chất:**
- Độ dày biên tỷ lệ với kích thước SE
- Ít nhạy với nhiễu hơn Canny, Sobel
- Kết quả là biên liên tục, ít đứt đoạn

### 2. Top-hat Transform

Top-hat Transform trích xuất các vật thể sáng hơn nền cục bộ.

**Công thức (White Top-hat):**
```
T_white(A) = A - (A ∘ B)
```

Trong đó:
- `A ∘ B`: Opening của A
- Kết quả: Các chi tiết sáng nhỏ hơn SE

**Ý Nghĩa:**
- Opening loại bỏ các vật thể nhỏ hơn SE
- Top-hat = Gốc - Opening = Các vật thể đã bị loại bỏ
- Trích xuất các chi tiết sáng trên nền tối hoặc không đồng đều

**Ứng Dụng:**
- Khử nền không đồng đều (Bài 9)
- Tách foreground từ background
- Phát hiện các đốm sáng nhỏ (khuyết tật, tế bào)

### 3. Black-hat Transform

Black-hat Transform trích xuất các vật thể tối hơn nền cục bộ.

**Công thức (Black Top-hat):**
```
T_black(A) = (A • B) - A
```

Trong đó:
- `A • B`: Closing của A
- Kết quả: Các chi tiết tối (lỗ) đã bị lấp bởi Closing

**Ý Nghĩa:**
- Closing lấp các lỗ nhỏ hơn SE
- Black-hat = Closing - Gốc = Các lỗ đã bị lấp
- Trích xuất các chi tiết tối trên nền sáng hoặc không đồng đều

**Ứng Dụng:**
- Phát hiện lỗ nhỏ, vết nứt
- Tách văn bản tối trên nền sáng
- Phát hiện khuyết tật bề mặt

### 4. Hit-or-Miss Transform

Hit-or-Miss Transform phát hiện các mẫu hình dạng cụ thể.

**Công thức:**
```
A ⊛ (B1, B2) = (A ⊖ B1) ∩ (A^c ⊖ B2)
```

Trong đó:
- `B1`: SE cho foreground (phải khớp)
- `B2`: SE cho background (phải khớp)
- `A^c`: Phần bù của A
- `∩`: Giao

**Cách Hoạt Động:**
1. Tìm các vị trí mà B1 khớp với foreground
2. Tìm các vị trí mà B2 khớp với background
3. Giao của hai tập hợp trên

**Structuring Element:**
SE có 3 giá trị:
- `1`: Phải là foreground
- `0`: Phải là background
- `-1` (don't care): Không quan tâm

**Ứng Dụng:**
- Pruning (xóa pixel thừa) - Bài 7
- Thinning (làm mỏng)
- Thickening (làm dày)
- Corner detection
- Pattern matching

## Code Examples (OpenCV)

### Example 1: Morphological Gradient

```python
import cv2
import numpy as np

# Đọc ảnh
img = cv2.imread('input.png', 0)
_, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Tạo SE
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# Morphological Gradient
gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)

# Hoặc tính thủ công
dilated = cv2.dilate(binary, kernel)
eroded = cv2.erode(binary, kernel)
gradient_manual = cv2.subtract(dilated, eroded)

# So sánh với Canny
edges_canny = cv2.Canny(img, 50, 150)

print(f"Morph gradient pixels: {np.sum(gradient > 0)}")
print(f"Canny edge pixels: {np.sum(edges_canny > 0)}")

cv2.imwrite('gradient.png', gradient)
cv2.imwrite('canny.png', edges_canny)
```

**Từ Bài 3 Code (extract_edges.py):**
- Dòng 85: `grad = cv2.morphologyEx(bw, cv2.MORPH_GRADIENT, kernel)`
- Dòng 94: `edges = cv2.Canny(img, 50, 150)` - So sánh với Canny

### Example 2: Top-hat Transform

```python
import cv2
import numpy as np

# Ảnh có chiếu sáng không đều
img = cv2.imread('uneven_lighting.jpg', 0)

# Kernel lớn để ước lượng nền
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))

# Top-hat: Trích xuất vật thể sáng
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

# Hoặc tính thủ công
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
tophat_manual = cv2.subtract(img, opening)

# Tăng cường bằng cách cộng Top-hat vào ảnh gốc
enhanced = cv2.add(img, tophat)

cv2.imwrite('tophat.png', tophat)
cv2.imwrite('enhanced.png', enhanced)
```

**Từ Bài 9 Code (remove.py):**
- Dòng 107: `tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)`
- Dòng 117: `blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)`
- Dòng 128: `corrected = cv2.normalize(img + tophat - blackhat, None, 0, 255, cv2.NORM_MINMAX)`

### Example 3: Black-hat Transform

```python
import cv2
import numpy as np

# Ảnh tài liệu với văn bản tối
img = cv2.imread('document.jpg', 0)

# Kernel
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))

# Black-hat: Trích xuất vật thể tối
blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)

# Hoặc tính thủ công
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
blackhat_manual = cv2.subtract(closing, img)

# Làm rõ văn bản bằng cách trừ Black-hat
enhanced = cv2.subtract(img, blackhat)

cv2.imwrite('blackhat.png', blackhat)
cv2.imwrite('enhanced_text.png', enhanced)
```

### Example 4: Hit-or-Miss Transform (Pruning)

```python
import cv2
import numpy as np

# Ảnh nhị phân với gai (spurs)
img = cv2.imread('skeleton.png', 0)
_, binary = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# SE để phát hiện pixel đơn lẻ ở cạnh
# 0 = must be 0, 1 = must be 1, -1 = don't care
se = np.array([[0, 0, 0],
               [-1, 1, -1],
               [1, 1, 1]], dtype=np.int8)

# Hit-or-Miss
hit_miss = cv2.morphologyEx(binary.astype(np.uint8), cv2.MORPH_HITMISS, se)

# Xóa các pixel được phát hiện
pruned = np.where(hit_miss == 1, 0, binary)

# Lặp lại cho đến khi hội tụ
for i in range(10):
    hit_miss = cv2.morphologyEx(pruned.astype(np.uint8), cv2.MORPH_HITMISS, se)
    if np.sum(hit_miss) == 0:
        break
    pruned = np.where(hit_miss == 1, 0, pruned)

print(f"Pruned after {i+1} iterations")
cv2.imwrite('pruned.png', (pruned * 255).astype(np.uint8))
```

**Từ Bài 7 Code (prune.py):**
- Dòng 98-105: Định nghĩa base SE với 0, 1, -1
- Dòng 109-117: Tạo 8 SE bằng cách xoay
- Dòng 141: `hm = cv2.morphologyEx(bw.astype(np.uint8), cv2.MORPH_HITMISS, se)`
- Dòng 146: `bw = np.where(hm == 1, 0, bw)` - Xóa pixel được hit

### Example 5: Kết Hợp Top-hat và Black-hat

```python
import cv2
import numpy as np

# Ảnh PCB hoặc tài liệu với chiếu sáng không đều
img = cv2.imread('pcb.jpg', 0)

# Kernel
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))

# Top-hat và Black-hat
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)

# Điều chỉnh: Img + Top-hat - Black-hat
corrected = cv2.normalize(img.astype(np.float32) + tophat - blackhat,
                          None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# Tính histogram để kiểm tra độ đồng đều
hist_orig = cv2.calcHist([img], [0], None, [256], [0, 256])
hist_corr = cv2.calcHist([corrected], [0], None, [256], [0, 256])

import matplotlib.pyplot as plt
plt.plot(hist_orig, label='Original', alpha=0.7)
plt.plot(hist_corr, label='Corrected', alpha=0.7)
plt.legend()
plt.show()

cv2.imwrite('corrected.png', corrected)
```

## So Sánh Các Phương Pháp

| Phép Toán | Công Thức | Input | Output | Ứng Dụng Chính |
|-----------|-----------|-------|--------|----------------|
| **Gradient** | (A ⊕ B) - (A ⊖ B) | Nhị phân | Biên | Phát hiện biên dày, liên tục |
| **Top-hat** | A - (A ∘ B) | Mức xám | Vật thể sáng | Khử nền tối, trích foreground sáng |
| **Black-hat** | (A • B) - A | Mức xám | Vật thể tối | Khử nền sáng, trích foreground tối |
| **Hit-or-Miss** | (A ⊖ B1) ∩ (A^c ⊖ B2) | Nhị phân | Pattern match | Pruning, thinning, pattern detection |

### So Sánh Gradient Methods

| Phương Pháp | Độ Dày Biên | Độ Chính Xác | Tốc Độ | Nhiễu | Liên Tục |
|-------------|-------------|--------------|--------|-------|----------|
| **Morph Gradient** | Dày | Trung bình | Nhanh | Ít nhạy | Cao |
| **Sobel** | Mỏng | Cao | Nhanh | Nhạy | Trung bình |
| **Canny** | Rất mỏng | Rất cao | Chậm | Nhạy | Cao |
| **Laplacian** | Mỏng | Trung bình | Nhanh | Rất nhạy | Thấp |

**Khi Nào Dùng Morph Gradient:**
- Ảnh nhị phân hoặc có cấu trúc rõ ràng
- Cần biên liên tục, ít đứt đoạn
- Ảnh có nhiễu nhưng không cần biên mỏng chính xác
- Real-time processing

**Khi Nào Dùng Canny:**
- Ảnh mức xám phức tạp
- Cần biên mỏng, chính xác
- Không bị ràng buộc về tốc độ
- Ảnh chất lượng tốt, ít nhiễu

### So Sánh Top-hat vs Black-hat

| Đặc Điểm | Top-hat | Black-hat |
|----------|---------|-----------|
| **Công thức** | A - Opening(A) | Closing(A) - A |
| **Trích xuất** | Vật thể sáng | Vật thể tối |
| **Nền gốc** | Tối/không đều | Sáng/không đều |
| **Output** | Các đỉnh (peaks) | Các thung lũng (valleys) |
| **Ứng dụng** | Văn bản sáng, đốm sáng | Văn bản tối, lỗ, vết nứt |

## Ưu Nhược Điểm

### Morphological Gradient

**Ưu điểm:**
- Biên liên tục, ít đứt đoạn
- Ít nhạy với nhiễu
- Tính toán đơn giản, nhanh
- Độ dày biên có thể điều chỉnh bằng kernel size

**Nhược điểm:**
- Biên dày hơn Canny, kém chính xác
- Không tốt cho ảnh có texture phức tạp
- Không có non-maximum suppression như Canny

### Top-hat / Black-hat Transform

**Ưu điểm:**
- Khử nền không đồng đều hiệu quả
- Trích xuất foreground mà không cần thresholding phức tạp
- Hoạt động tốt với chiếu sáng không đều
- Có thể kết hợp để tăng cường tương phản

**Nhược điểm:**
- Kernel size phải chọn cẩn thận (lớn hơn vật thể cần trích xuất)
- Có thể loại bỏ cả vật thể lớn nếu kernel quá lớn
- Không hiệu quả với nền có texture phức tạp

### Hit-or-Miss Transform

**Ưu điểm:**
- Phát hiện pattern chính xác
- Linh hoạt với SE tùy chỉnh
- Hiệu quả cho pruning, thinning

**Nhược điểm:**
- Chỉ hoạt động với ảnh nhị phân
- Nhạy với nhiễu
- Cần định nghĩa SE cẩn thận
- Cần lặp nhiều lần cho kết quả tốt

## Kỹ Thuật Nâng Cao

### 1. Multi-direction Hit-or-Miss (Pruning 8 Hướng)

```python
import cv2
import numpy as np

# Base SE
base = np.array([[0, 0, 0],
                 [-1, 1, -1],
                 [1, 1, 1]], dtype=np.int8)

# Tạo 8 SE bằng cách xoay
SEs = []
for k in range(4):
    SEs.append(np.rot90(base, k))
    SEs.append(np.rot90(np.fliplr(base), k))

# Áp dụng tất cả SE
img = cv2.imread('skeleton.png', 0)
_, binary = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

for iteration in range(10):
    changed = False
    for se in SEs:
        hm = cv2.morphologyEx(binary.astype(np.uint8), cv2.MORPH_HITMISS, se)
        if np.sum(hm) > 0:
            binary = np.where(hm == 1, 0, binary)
            changed = True
    if not changed:
        break

print(f"Converged after {iteration+1} iterations")
```

**Từ Bài 7:** Pruning sử dụng 8 SE (dòng 109-117)

### 2. Adaptive Top-hat với Multi-scale

```python
import cv2
import numpy as np

img = cv2.imread('uneven.jpg', 0)

# Multi-scale top-hat
scales = [7, 15, 31]
tophats = []

for size in scales:
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    tophats.append(tophat)

# Kết hợp bằng weighted sum
weights = [0.5, 0.3, 0.2]  # Ưu tiên scale nhỏ
combined = np.zeros_like(img, dtype=np.float32)
for tophat, weight in zip(tophats, weights):
    combined += tophat.astype(np.float32) * weight

combined = cv2.normalize(combined, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
cv2.imwrite('multi_scale_tophat.png', combined)
```

### 3. Directional Gradient (Gradient Theo Hướng)

```python
import cv2
import numpy as np

img = cv2.imread('input.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# SE hướng ngang
se_horizontal = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
grad_h = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, se_horizontal)

# SE hướng dọc
se_vertical = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
grad_v = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, se_vertical)

# Kết hợp
grad_total = np.sqrt(grad_h**2 + grad_v**2).astype(np.uint8)

cv2.imwrite('directional_gradient.png', grad_total)
```

### 4. Morphological Smoothing

Kết hợp Opening và Closing để làm mịn:

```python
import cv2

img = cv2.imread('noisy.png', 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# Alternate Sequential Filter (ASF)
smoothed = binary.copy()
for _ in range(3):
    smoothed = cv2.morphologyEx(smoothed, cv2.MORPH_OPEN, kernel)
    smoothed = cv2.morphologyEx(smoothed, cv2.MORPH_CLOSE, kernel)

cv2.imwrite('smoothed.png', smoothed)
```

### 5. Conditional Top-hat (Adaptive Background Removal)

```python
import cv2
import numpy as np

img = cv2.imread('variable_background.jpg', 0)

# Ước lượng kernel size cục bộ dựa trên local statistics
def estimate_local_kernel_size(image, window_size=50):
    h, w = image.shape
    kernel_map = np.zeros((h, w), dtype=np.int32)

    for i in range(0, h, window_size):
        for j in range(0, w, window_size):
            window = image[i:min(i+window_size, h), j:min(j+window_size, w)]
            # Kernel size tỷ lệ với std deviation của vùng
            std = window.std()
            kernel_size = max(7, min(31, int(std / 2)))
            kernel_map[i:i+window_size, j:j+window_size] = kernel_size

    return kernel_map

# Áp dụng top-hat adaptive
kernel_map = estimate_local_kernel_size(img)
result = np.zeros_like(img)

unique_sizes = np.unique(kernel_map)
for size in unique_sizes:
    mask = (kernel_map == size)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    result = np.where(mask, tophat, result)

cv2.imwrite('adaptive_tophat.png', result)
```

## Tài Liệu Tham Khảo

### Papers

1. **Maragos, P. & Schafer, R. (1987)**
   - "Morphological Filters - Part I: Their Set-Theoretic Analysis and Relations to Linear Shift-Invariant Filters"
   - IEEE Transactions on Acoustics, Speech, and Signal Processing

2. **Meyer, F. & Beucher, S. (1990)**
   - "Morphological Segmentation"
   - Journal of Visual Communication and Image Representation

3. **Soille, P. (1999)**
   - "Morphological Image Analysis: Principles and Applications"
   - Springer

### Online Resources

- **OpenCV Morphological Transformations**: https://docs.opencv.org/4.x/d3/dbe/tutorial_opening_closing_hats.html
- **MATLAB Top-hat Filtering**: https://www.mathworks.com/help/images/ref/imtophat.html

## Liên Kết

### Bài Tập Liên Quan

- [Bài 3: Trích Biên với Gradient](../code-reading-guide/bai-3-how-to-read.md)
- [Bài 7: Pruning với Hit-or-Miss](../code-reading-guide/bai-7-how-to-read.md)
- [Bài 9: Khử Nền với Top-hat/Black-hat](../code-reading-guide/bai-9-how-to-read.md)

### Theory Liên Quan

- [01 - Morphology Fundamentals](./01-morphology-fundamentals.md)
- [03 - Binary Morphology](./03-binary-morphology.md)
- [04 - Grayscale Morphology](./04-grayscale-morphology.md)

---

**Nguồn**: T61-78 Xử lý hình thái - Ph.D Phan Thanh Toàn
