# Lý Thuyết: Phương Pháp Phân Ngưỡng (Thresholding Methods)

## Tổng Quan

Phân ngưỡng (thresholding) là kỹ thuật cơ bản và quan trọng nhất trong phân vùng ảnh, cho phép tách vật thể khỏi nền dựa trên giá trị độ sáng của pixel. Phương pháp này chuyển đổi ảnh xám thành ảnh nhị phân bằng cách so sánh mỗi pixel với một hoặc nhiều ngưỡng.

Phân ngưỡng là bước đầu tiên trong nhiều ứng dụng xử lý ảnh như nhận dạng ký tự quang học (OCR), phát hiện vật thể, kiểm tra chất lượng công nghiệp, và phân tích ảnh y tế. Hiệu quả của phương pháp phụ thuộc vào việc lựa chọn ngưỡng phù hợp với đặc điểm của ảnh.

Có ba nhóm phương pháp phân ngưỡng chính: **Global Thresholding** (ngưỡng toàn cục - một giá trị cho toàn ảnh), **Otsu Thresholding** (tự động tìm ngưỡng tối ưu), và **Adaptive Thresholding** (ngưỡng cục bộ thích nghi với từng vùng ảnh).

## Ứng Dụng

- **Bài 1**: Global Thresholding - Tách sản phẩm trên băng chuyền
- **Bài 2**: Otsu Thresholding - Đếm linh kiện điện tử
- **Bài 3**: Adaptive Thresholding - Tách chữ trên hóa đơn bị bóng
- **Bài 4**: Bayes-ML Thresholding - Phát hiện rỉ sét trên kim loại

## Nguyên Lý Toán Học

### 1. Global Thresholding

Phương pháp đơn giản nhất: chọn một giá trị ngưỡng T cho toàn bộ ảnh.

**Công thức cơ bản:**

```
g(x,y) = { 255  nếu f(x,y) ≥ T
         { 0    nếu f(x,y) < T
```

**Thuật toán lặp tìm T (Heuristic Iterative):**

1. Khởi tạo T₀ = mean(I)
2. Chia ảnh thành 2 nhóm: G₁ = {pixels ≥ T}, G₂ = {pixels < T}
3. Tính m₁ = mean(G₁), m₂ = mean(G₂)
4. Tính T_new = (m₁ + m₂) / 2
5. Nếu |T_new - T| < ε thì dừng, ngược lại T = T_new, quay lại bước 2

**Độ phức tạp:** O(n × k) với n là số pixel, k là số lần lặp (thường < 10)

### 2. Otsu Thresholding

Tìm ngưỡng T tối ưu bằng cách **tối đa hóa phương sai giữa các lớp** (between-class variance).

**Công thức:**

Giả sử có 2 lớp C₀ và C₁, với xác suất:
- P₀(T) = Σ(i=0 to T) p(i)
- P₁(T) = Σ(i=T+1 to 255) p(i) = 1 - P₀(T)

Độ sáng trung bình mỗi lớp:
- μ₀(T) = Σ(i=0 to T) i·p(i) / P₀(T)
- μ₁(T) = Σ(i=T+1 to 255) i·p(i) / P₁(T)

**Between-class variance:**

```
σ²_B(T) = P₀(T) × P₁(T) × [μ₀(T) - μ₁(T)]²
```

**Ngưỡng tối ưu:**

```
T* = argmax(σ²_B(T))  với T ∈ [0, 255]
```

**Độ phức tạp:** O(256 × n) ≈ O(n)

### 3. Adaptive Thresholding

Ngưỡng thay đổi theo từng vùng cục bộ, phù hợp với ảnh có độ sáng không đều.

**Công thức:**

```
T(x,y) = mean(N(x,y)) - C
```

hoặc:

```
T(x,y) = gaussian_weighted_mean(N(x,y)) - C
```

Trong đó:
- N(x,y): Vùng láng giềng blockSize × blockSize quanh pixel (x,y)
- C: Hằng số điều chỉnh (thường 2-10)

**Hai phương pháp:**

1. **ADAPTIVE_THRESH_MEAN_C**: Trung bình đơn giản
   ```
   T(x,y) = (1/n) × Σ I(i,j) - C
   ```

2. **ADAPTIVE_THRESH_GAUSSIAN_C**: Trung bình Gaussian có trọng số
   ```
   T(x,y) = Σ G(i,j) × I(i,j) - C
   ```
   với G là kernel Gaussian 2D

**Độ phức tạp:** O(n × blockSize²)

### 4. Bayes-ML Thresholding

Dựa trên lý thuyết xác suất Bayes và Maximum Likelihood, giả định phân bố Gaussian.

**Mô hình:**
- Lớp 0 (nền): N(μ₀, σ₀²)
- Lớp 1 (vật thể): N(μ₁, σ₁²)
- Prior: P₀, P₁ (P₀ + P₁ = 1)

**Likelihood:**

```
p(x|C₀) = (1/(σ₀√(2π))) × exp(-(x-μ₀)²/(2σ₀²))
p(x|C₁) = (1/(σ₁√(2π))) × exp(-(x-μ₁)²/(2σ₁²))
```

**Bayes decision:**

```
p(x|C₀)P₀ = p(x|C₁)P₁
```

**Ngưỡng tối ưu (σ₀ ≠ σ₁):**

```
T* = (μ₀σ₁² - μ₁σ₀² + σ₀σ₁√[(μ₁-μ₀)² + 2(σ₁²-σ₀²)ln(σ₁P₀/σ₀P₁)]) / (σ₁² - σ₀²)
```

**Trường hợp đặc biệt (σ₀ = σ₁ = σ):**

```
T* = (μ₀ + μ₁)/2 + (σ²/(μ₁-μ₀)) × ln(P₀/P₁)
```

## Code Examples (OpenCV)

### 1. Global Thresholding

```python
import cv2
import numpy as np

def global_threshold_iterative(gray, eps=1e-3, max_iter=100):
    """Thuật toán phân ngưỡng toàn cục lặp."""
    T = float(np.mean(gray))

    for iteration in range(max_iter):
        G1 = gray[gray >= T]  # Nhóm sáng
        G2 = gray[gray < T]   # Nhóm tối

        if len(G1) == 0 or len(G2) == 0:
            break

        m1 = float(np.mean(G1))
        m2 = float(np.mean(G2))
        newT = 0.5 * (m1 + m2)

        if abs(newT - T) <= eps:
            T = newT
            break
        T = newT

    _, binary = cv2.threshold(gray, T, 255, cv2.THRESH_BINARY)
    return binary, T

# Sử dụng
img = cv2.imread('input.jpg', 0)
binary, threshold_value = global_threshold_iterative(img)
print(f"Ngưỡng hội tụ: {threshold_value:.2f}")
```

### 2. Otsu Thresholding

```python
import cv2

# Otsu tự động tìm ngưỡng tối ưu
gray = cv2.imread('input.jpg', 0)

# Otsu thresholding
T_otsu, binary_otsu = cv2.threshold(gray, 0, 255,
                                     cv2.THRESH_BINARY + cv2.THRESH_OTSU)

print(f"Ngưỡng Otsu tối ưu: {T_otsu:.2f}")

# Hiển thị histogram với ngưỡng
import matplotlib.pyplot as plt
plt.hist(gray.ravel(), 256, [0,256])
plt.axvline(x=T_otsu, color='r', linestyle='--', label=f'Otsu T={T_otsu:.0f}')
plt.legend()
plt.show()
```

### 3. Adaptive Thresholding

```python
import cv2

gray = cv2.imread('receipt.jpg', 0)

# Tham số
block_size = 35  # Phải là số lẻ
C = 7

# Adaptive MEAN
adaptive_mean = cv2.adaptiveThreshold(
    gray, 255,
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY,
    block_size, C
)

# Adaptive GAUSSIAN
adaptive_gaussian = cv2.adaptiveThreshold(
    gray, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    block_size, C
)

# So sánh
cv2.imshow('MEAN', adaptive_mean)
cv2.imshow('GAUSSIAN', adaptive_gaussian)
cv2.waitKey(0)
```

### 4. Bayes-ML Thresholding

```python
import numpy as np
import cv2

def bayes_threshold(mu0, sigma0, mu1, sigma1, P0, P1):
    """Tính ngưỡng Bayes-ML cho 2 lớp Gaussian."""

    # Trường hợp sigma khác nhau
    numerator = mu0 * sigma1**2 - mu1 * sigma0**2 + \
                sigma0 * sigma1 * np.sqrt(
                    (mu1 - mu0)**2 +
                    2 * (sigma1**2 - sigma0**2) * np.log((sigma1 * P0) / (sigma0 * P1))
                )
    denominator = sigma1**2 - sigma0**2

    if abs(denominator) < 1e-6:
        # Trường hợp sigma bằng nhau
        T = (mu0 + mu1) / 2
    else:
        T = numerator / denominator

    return T

# Ước lượng tham số từ dữ liệu
mu0, sigma0 = 120, 12  # Nền
mu1, sigma1 = 165, 15  # Vật thể
P0, P1 = 0.7, 0.3      # Prior

T = bayes_threshold(mu0, sigma0, mu1, sigma1, P0, P1)
print(f"Ngưỡng Bayes-ML: {T:.2f}")

# Áp dụng
gray = cv2.imread('steel_rust.jpg', 0)
_, binary = cv2.threshold(gray, T, 255, cv2.THRESH_BINARY)
```

## So Sánh Các Phương Pháp

| Phương pháp | Độ phức tạp | Tốc độ | Điều kiện áp dụng | Độ chính xác |
|------------|-------------|--------|------------------|--------------|
| **Global Iterative** | O(n×k) | Nhanh | Độ sáng đồng đều, histogram bimodal | Tốt nếu đúng điều kiện |
| **Otsu** | O(n) | Rất nhanh | Histogram bimodal rõ ràng | Cao với histogram tốt |
| **Adaptive MEAN** | O(n×b²) | Trung bình | Độ sáng không đều | Tốt cho văn bản |
| **Adaptive GAUSSIAN** | O(n×b²) | Trung bình | Độ sáng không đều, nhiễu | Rất tốt, mượt |
| **Bayes-ML** | O(n) | Nhanh | Biết prior và phân bố | Tối ưu lý thuyết |

Chú thích:
- n: số pixel
- k: số lần lặp (thường < 10)
- b: blockSize

## Ưu Nhược Điểm

### Global Thresholding

**Ưu điểm:**
- Đơn giản, dễ hiểu và cài đặt
- Rất nhanh, O(n×k)
- Hiệu quả cao với ảnh có độ sáng đồng đều
- Ít tham số (chỉ cần epsilon)

**Nhược điểm:**
- Thất bại với ảnh có độ sáng không đều
- Nhạy cảm với nhiễu
- Không phù hợp với histogram multimodal
- Kết quả phụ thuộc vào khởi tạo T₀

### Otsu Thresholding

**Ưu điểm:**
- Tự động, không cần tham số
- Tối ưu toán học (tối đa hóa variance)
- Rất nhanh O(n)
- Hiệu quả cao với histogram bimodal rõ ràng

**Nhược điểm:**
- Chỉ tối ưu với 2 lớp
- Thất bại khi histogram không bimodal
- Nhạy với tỷ lệ diện tích vật thể/nền
- Không xử lý được độ sáng không đều

### Adaptive Thresholding

**Ưu điểm:**
- Xử lý tốt độ sáng không đều
- GAUSSIAN xử lý nhiễu tốt hơn MEAN
- Phù hợp cho OCR, document scanning
- Robust với gradient ánh sáng

**Nhược điểm:**
- Chậm hơn global (O(n×b²))
- Cần điều chỉnh 2 tham số (blockSize, C)
- Có thể tạo nhiễu ở vùng đồng nhất
- Kết quả phụ thuộc nhiều vào tham số

### Bayes-ML Thresholding

**Ưu điểm:**
- Tối ưu lý thuyết (Bayes decision)
- Kết hợp prior knowledge
- Hiệu quả với dữ liệu có phân bố Gaussian
- Cho phép điều chỉnh cost function

**Nhược điểm:**
- Cần ước lượng tham số (μ, σ, P)
- Giả định phân bố Gaussian không luôn đúng
- Phức tạp hơn về mặt toán học
- Nhạy với sai số ước lượng tham số

## Kỹ Thuật Nâng Cao

### 1. Multi-Otsu Thresholding

Mở rộng Otsu cho nhiều lớp (k > 2):

```python
from skimage.filters import threshold_multiotsu

# Tìm k-1 ngưỡng cho k lớp
thresholds = threshold_multiotsu(gray, classes=3)
regions = np.digitize(gray, bins=thresholds)
```

**Ứng dụng:** Phân đoạn ảnh y tế (xương-mô-nền), ảnh vệ tinh

### 2. Hysteresis Thresholding

Sử dụng 2 ngưỡng (high, low) như Canny edge detector:

```python
def hysteresis_threshold(gray, T_low, T_high):
    """Hysteresis thresholding với 2 ngưỡng."""
    strong = (gray >= T_high).astype(np.uint8) * 255
    weak = ((gray >= T_low) & (gray < T_high)).astype(np.uint8) * 255

    # Kết nối weak edges với strong edges
    # (cần flood fill hoặc morphology operations)
    result = strong.copy()
    # ... (logic kết nối)

    return result
```

**Ưu điểm:** Giảm false positive, tăng connectivity

### 3. Locally Adaptive Threshold với Niblack/Sauvola

**Niblack method:**

```python
def niblack_threshold(gray, window_size=15, k=0.2):
    """Niblack local thresholding."""
    mean = cv2.blur(gray, (window_size, window_size))
    mean_sq = cv2.blur(gray**2, (window_size, window_size))
    std = np.sqrt(mean_sq - mean**2)

    threshold = mean + k * std
    binary = (gray > threshold).astype(np.uint8) * 255

    return binary
```

**Sauvola method (cải tiến Niblack):**

```python
def sauvola_threshold(gray, window_size=15, k=0.2, R=128):
    """Sauvola local thresholding."""
    mean = cv2.blur(gray, (window_size, window_size))
    mean_sq = cv2.blur(gray**2, (window_size, window_size))
    std = np.sqrt(mean_sq - mean**2)

    threshold = mean * (1 + k * (std / R - 1))
    binary = (gray > threshold).astype(np.uint8) * 255

    return binary
```

**Ứng dụng:** OCR văn bản cổ, degraded documents

### 4. Histogram Equalization trước Thresholding

Cải thiện contrast trước khi phân ngưỡng:

```python
# CLAHE (Contrast Limited Adaptive Histogram Equalization)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
enhanced = clahe.apply(gray)

# Sau đó áp dụng Otsu
T, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

### 5. Morphological Post-processing

Làm sạch kết quả thresholding:

```python
# Opening: loại bỏ nhiễu nhỏ
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

# Closing: lấp các lỗ nhỏ
filled = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)

# Kết hợp
final = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
final = cv2.morphologyEx(final, cv2.MORPH_CLOSE, kernel)
```

## Tài Liệu Tham Khảo

1. **Otsu, N.** (1979). "A threshold selection method from gray-level histograms." IEEE Transactions on Systems, Man, and Cybernetics, 9(1), 62-66.

2. **Sezgin, M., & Sankur, B.** (2004). "Survey over image thresholding techniques and quantitative performance evaluation." Journal of Electronic Imaging, 13(1), 146-168.

3. **Bradski, G., & Kaehler, A.** (2008). "Learning OpenCV: Computer Vision with the OpenCV Library." O'Reilly Media.

4. **Gonzalez, R. C., & Woods, R. E.** (2018). "Digital Image Processing" (4th ed.). Pearson.

5. **Niblack, W.** (1986). "An Introduction to Digital Image Processing." Prentice-Hall.

6. **Sauvola, J., & Pietikäinen, M.** (2000). "Adaptive document image binarization." Pattern Recognition, 33(2), 225-236.

## Liên Kết

- **Code thực hành:**
  - [Bài 1: Global Thresholding](/code-implement/T79-phan-vung-anh/bai-1-global-thresholding/)
  - [Bài 2: Otsu Thresholding](/code-implement/T79-phan-vung-anh/bai-2-otsu/)
  - [Bài 3: Adaptive Thresholding](/code-implement/T79-phan-vung-anh/bai-3-adaptive-thresholding/)
  - [Bài 4: Bayes-ML Thresholding](/code-implement/T79-phan-vung-anh/bai-4-bayes-ml/)

- **Lý thuyết liên quan:**
  - [02: Region-based Segmentation](02-region-based-segmentation.md)
  - [03: Clustering Segmentation](03-clustering-segmentation.md)
  - [06: Segmentation Evaluation](06-segmentation-evaluation.md)

- **Tài liệu gốc:** T79-99 Phân vùng ảnh (trang 1-8)

---

**Tác giả:** Ph.D Phan Thanh Toàn
**Cập nhật:** 2025-11-17
**Phiên bản:** 1.0
