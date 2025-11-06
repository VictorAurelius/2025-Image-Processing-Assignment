# Cân Bằng Histogram (Histogram Equalization)

## Giới Thiệu

Histogram Equalization là kỹ thuật tăng cường tương phản (contrast enhancement) bằng cách **phân bố lại cường độ pixel** để histogram trở nên đồng đều hơn.

## Khái Niệm Cơ Bản

### Histogram
Histogram h(r) của một ảnh là biểu đồ tần số xuất hiện của mỗi mức xám:

```
h(rk) = nk
```
- rk: Mức xám thứ k (0 đến L-1)
- nk: Số pixel có giá trị rk
- L: Tổng số mức xám (thường là 256 cho 8-bit)

### Normalized Histogram
```
p(rk) = nk / n
```
- n: Tổng số pixel trong ảnh
- p(rk): Xác suất của mức xám rk (tổng = 1)

## Mục Đích

### Vấn đề:
- Ảnh có tương phản thấp
- Histogram tập trung ở một vùng nhỏ
- Sử dụng không hiệu quả dải cường độ

### Giải pháp:
- Spread out histogram để cover toàn bộ range [0, L-1]
- Tăng global contrast
- Làm rõ details

## Thuật Toán Histogram Equalization

### Bước 1: Tính Histogram
```
h(rk) = số pixel có giá trị rk
```

### Bước 2: Tính CDF (Cumulative Distribution Function)
```
CDF(rk) = Σ(i=0 to k) h(ri)
```
Hoặc normalized:
```
CDF(rk) = Σ(i=0 to k) p(ri)
```

### Bước 3: Normalize CDF
```
CDF_normalized(rk) = (CDF(rk) - CDF_min) / (total_pixels - CDF_min) × (L - 1)
```

Hoặc đơn giản hơn:
```
s_k = ((L-1) / n) × CDF(r_k)
```

### Bước 4: Mapping
Map mỗi pixel cũ sang giá trị mới:
```
new_pixel = round(CDF_normalized(old_pixel))
```

## Ví Dụ Chi Tiết

### Input Image (3×3):
```
1  2  5
6  7  7
1  1  0
```

### Bước 1: Tính Histogram
```
Gray Level | Count | Pixels
    0      |   1   | (2,2)
    1      |   3   | (0,0), (1,0), (1,1)
    2      |   1   | (0,1)
    5      |   1   | (0,2)
    6      |   1   | (1,2)
    7      |   2   | (2,2), (2,1)
```

Total pixels: n = 9

### Bước 2: Tính CDF
```
Gray Level | Count | CDF
    0      |   1   |  1
    1      |   3   |  4
    2      |   1   |  5
    5      |   1   |  6
    6      |   1   |  7
    7      |   2   |  9
```

### Bước 3: Histogram Equalization với L = 8 levels (0-7)

Formula: `new_value = round((CDF - CDF_min) / (n - CDF_min) × (L - 1))`

Với CDF_min = 1 (min non-zero CDF), n = 9, L = 8:

```
Old | CDF | Calculation               | New
----|-----|---------------------------|----
 0  |  1  | (1-1)/(9-1) × 7 = 0.0    |  0
 1  |  4  | (4-1)/(9-1) × 7 = 2.625  |  3
 2  |  5  | (5-1)/(9-1) × 7 = 3.5    |  4
 5  |  6  | (6-1)/(9-1) × 7 = 4.375  |  4
 6  |  7  | (7-1)/(9-1) × 7 = 5.25   |  5
 7  |  9  | (9-1)/(9-1) × 7 = 7.0    |  7
```

### Output Image:
```
Original:      Equalized:
1  2  5        3  4  4
6  7  7   →    5  7  7
1  1  0        3  3  0
```

## Phương Pháp Đơn Giản Hơn (Thường Dùng)

### Formula:
```
new_value = round((L-1) / n × CDF(old_value))
```

### Với ví dụ trên (L=8, n=9):
```
Old | CDF | (7/9) × CDF | Rounded
----|-----|-------------|--------
 0  |  1  |    0.78     |   1
 1  |  4  |    3.11     |   3
 2  |  5  |    3.89     |   4
 5  |  6  |    4.67     |   5
 6  |  7  |    5.44     |   5
 7  |  9  |    7.00     |   7
```

## Đặc Điểm & Tính Chất

### Ưu Điểm:
1. **Automatic**: Không cần parameters
2. **Effective**: Tăng contrast đáng kể
3. **Full Range**: Sử dụng toàn bộ [0, L-1]
4. **Simple**: Dễ implement

### Nhược Điểm:
1. **Over-enhancement**: Có thể tăng quá mức
2. **Noise Amplification**: Nhiễu cũng được tăng cường
3. **Histogram Gaps**: Có thể tạo gaps trong histogram mới
4. **Global**: Không phù hợp với ảnh có lighting không đồng đều

### Khi Nào Hiệu Quả:
- Ảnh có tương phản thấp
- Histogram tập trung một chỗ
- Cần tăng global contrast
- Ảnh y tế, X-ray
- Preprocessing cho các thuật toán khác

### Khi Nào Không Hiệu Quả:
- Ảnh đã có contrast tốt
- Ảnh có nhiễu cao
- Cần preserve specific intensity relationships
- Ảnh màu (cần xử lý đặc biệt)

## Adaptive Histogram Equalization (AHE)

### Vấn Đề của Global HE:
- Không xử lý tốt lighting không đồng đều
- Over-enhancement ở vùng đồng nhất

### Giải Pháp: CLAHE
**CLAHE (Contrast Limited Adaptive Histogram Equalization)**

#### Cách hoạt động:
1. Chia ảnh thành tiles (e.g., 8×8)
2. Equalize histogram của mỗi tile
3. **Clip histogram** để tránh over-amplification
4. Bilinear interpolation giữa các tiles

#### Ưu điểm:
- Local contrast enhancement
- Giảm over-enhancement
- Tốt cho ảnh medical imaging

## Histogram Matching (Specification)

### Mục đích:
Transform histogram của ảnh để match một histogram mục tiêu cụ thể

### Thuật toán:
1. Equalize ảnh input → CDF₁
2. Equalize histogram target → CDF₂
3. For each pixel: Find s sao cho CDF₂(s) ≈ CDF₁(r)

### Ứng dụng:
- Normalize ảnh từ nhiều nguồn khác nhau
- Match lighting conditions
- Style transfer

## Histogram Equalization cho Ảnh Màu

### Vấn Đề:
Không thể equalize trực tiếp RGB vì thay đổi color balance

### Giải pháp:

#### 1. Equalize từng channel RGB riêng:
```
R' = HE(R)
G' = HE(G)
B' = HE(B)
```
**Nhược điểm**: Thay đổi màu sắc

#### 2. Equalize trong HSV/HSI:
```
H, S, V = RGB_to_HSV(image)
V' = HE(V)  # Chỉ equalize Value/Intensity
RGB' = HSV_to_RGB(H, S, V')
```
**Ưu điểm**: Preserve hue và saturation

#### 3. Equalize trong YCbCr:
```
Y, Cb, Cr = RGB_to_YCbCr(image)
Y' = HE(Y)  # Chỉ equalize luminance
RGB' = YCbCr_to_RGB(Y', Cb, Cr)
```
**Ưu điểm**: Giữ thông tin màu, tốt nhất

## Ví Dụ Thực Tế

### Case 1: Medical X-ray
**Input**: X-ray image tối, low contrast
**After HE**: Details rõ ràng hơn, dễ chẩn đoán

### Case 2: Underexposed Photo
**Input**: Ảnh chụp thiếu sáng
**After HE**: Brightness tăng, details visible

### Case 3: Foggy Image
**Input**: Ảnh sương mù, low contrast
**After HE**: Clearer, nhưng có thể over-enhance noise

## So Sánh với Các Phương Pháp Khác

| Method | Pros | Cons | Use Case |
|--------|------|------|----------|
| **Histogram Equalization** | Automatic, simple | Over-enhancement, global | General contrast enhancement |
| **CLAHE** | Local adaptation | Slower, parameters | Medical images, varied lighting |
| **Histogram Matching** | Control output distribution | Need target histogram | Normalization across images |
| **Gamma Correction** | Preserve relationships | Need parameter | Brightening/darkening |
| **Contrast Stretching** | Simple, fast | Linear transformation | Basic contrast |

## Implementation Tips

### 1. Preprocessing:
- Remove extreme outliers trước khi equalize
- Consider noise reduction

### 2. Postprocessing:
- Clip extreme values nếu cần
- Smooth transitions

### 3. Parameter Tuning:
- Số levels L: Thường 256, nhưng có thể giảm
- Clip limit cho CLAHE: 2-4 thường tốt
- Tile size cho CLAHE: 8×8 hoặc 16×16

## Code Patterns

### Python (NumPy):
```python
import numpy as np

def histogram_equalization(image):
    # Flatten image
    flat = image.flatten()

    # Calculate histogram
    hist, bins = np.histogram(flat, bins=256, range=[0,256])

    # Calculate CDF
    cdf = hist.cumsum()

    # Normalize CDF
    cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())

    # Map old values to new
    equalized = np.interp(flat, bins[:-1], cdf_normalized)

    return equalized.reshape(image.shape).astype('uint8')
```

### OpenCV:
```python
import cv2

# Grayscale
equalized = cv2.equalizeHist(image)

# Color (YCrCb)
ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
ycrcb[:,:,0] = cv2.equalizeHist(ycrcb[:,:,0])
equalized = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

# CLAHE
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
equalized = clahe.apply(image)
```

## Tham Khảo

- Digital Image Processing (Gonzalez & Woods) - Chapter 3
- OpenCV Documentation: `cv2.equalizeHist()`, `cv2.createCLAHE()`
- scikit-image: `exposure.equalize_hist()`, `exposure.equalize_adapthist()`
- "Adaptive Histogram Equalization and Its Variations" (Pizer et al., 1987)
