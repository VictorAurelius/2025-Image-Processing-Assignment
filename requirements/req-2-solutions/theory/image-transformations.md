# Biến Đổi Cường Độ Ảnh (Image Intensity Transformations)

## Giới Thiệu

Intensity transformations là các phép biến đổi point-wise (từng pixel độc lập) để điều chỉnh brightness, contrast, hoặc enhance features trong ảnh.

**General Form**: `s = T(r)`
- r: Input intensity (0 to L-1)
- s: Output intensity (0 to L-1)
- T: Transformation function

## Các Phép Biến Đổi Cơ Bản

### 1. Negative Transformation
```
s = L - 1 - r
```
**Hiệu ứng**: Đảo ngược màu (photographic negative)

**Ứng dụng**:
- Medical imaging (dễ nhìn vùng tối)
- Enhance white/gray details trong dark background

---

### 2. Log Transformation

#### Công Thức:
```
s = c × log(1 + r)
```
- c: Constant để scale output
- Thường: c = (L-1) / log(1 + r_max)

#### Đặc Điểm:
- **Expands dark regions** (vùng tối)
- **Compresses bright regions** (vùng sáng)
- Maps narrow range of low intensities → wide range of output
- Maps wide range of high intensities → narrow range of output

#### Curve:

```
Output
  │     ╱────
  │    ╱
  │   ╱
  │  ╱
  │ ╱
  │╱
  └──────────── Input
```

Steep tại input thấp, flatten tại input cao

#### Khi Nào Sử Dụng:
- Ảnh có **dynamic range lớn**
- Cần **brighten dark regions**
- Fourier spectrum visualization
- Ảnh có histogram **tập trung ở vùng thấp (0-70)**

#### Ví Dụ:
**Input**: Fourier spectrum (range 0-10⁶)
**After Log**: Range 0-255, dễ nhìn

#### Đối với Histogram Tập Trung 0-70:
**Câu hỏi trong đề**: "Một ảnh 8-bit có histogram tập trung ở vùng cường độ thấp (0-70). Nếu áp dụng log transform, điều gì xảy ra?"

**Đáp án**:
- **Độ tương phản ở vùng tối TĂNG**
- **Độ tương phản ở vùng sáng GIẢM**
- Log transform "stretches" dark values, "compresses" bright values

#### Inverse Log:
```
s = c × exp(r/c) - 1
```
Opposite effect: Compresses dark, expands bright

---

### 3. Power-Law (Gamma) Transformation

#### Công Thức:
```
s = c × r^γ
```
- c: Constant (thường = 1)
- γ (gamma): Exponent parameter

#### Normalize về [0, 1]:
```
s = ((r / (L-1))^γ) × (L-1)
```

#### Đặc Điểm theo γ:

##### γ < 1 (e.g., γ = 0.4, 0.5):
- **Brightens image** (làm sáng)
- **Expands dark values** → more separation
- **Compresses bright values** → less separation
- Curve bends upward
- Giống log transform nhưng có control hơn

```
Output
  │      ╱─────
  │     ╱
  │    ╱
  │   ╱
  │  ╱
  │ ╱
  └──────────── Input
```

**Use case**:
- Brighten underexposed images
- Enhance dark details
- Display images on monitors (gamma correction)

##### γ = 1:
- **No change** (identity)
- s = r

##### γ > 1 (e.g., γ = 2, 2.5):
- **Darkens image** (làm tối)
- **Compresses dark values** → less separation
- **Expands bright values** → more separation
- Curve bends downward

```
Output
  │        ╱
  │       ╱
  │      ╱
  │     ╱
  │    ╱
  │  ╱─
  └──────────── Input
```

**Use case**:
- Darken overexposed images
- Reduce dark noise
- Enhance bright details

#### Ví Dụ Câu Hỏi Đề Thi:
**"Cho γ = 0.4, kết quả mô tả ảnh sau biến đổi?"**

**Đáp án**: **B. Ảnh sáng hơn ảnh gốc**

**Giải thích**:
- γ = 0.4 < 1
- r^0.4 > r for r < 1 (normalized)
- Majority of pixels become brighter
- Histogram shifts right

#### So Sánh γ Values:

| γ | Effect | Dark Regions | Bright Regions | Use Case |
|---|--------|--------------|----------------|----------|
| 0.4 | Very bright | Expand greatly | Compress | Very dark images |
| 0.5 | Bright | Expand | Compress | Dark images |
| 1.0 | No change | No change | No change | Already good |
| 2.0 | Dark | Compress | Expand | Bright images |
| 2.5 | Very dark | Compress greatly | Expand | Very bright images |

#### Gamma Correction:
Monitors có inherent gamma ≈ 2.5

**Correction**: Apply γ = 1/2.5 ≈ 0.4 để display correctly

---

### 4. Piecewise-Linear Transformation

#### Contrast Stretching:
```
        s_max  ────────╱
               ╱
             ╱
           ╱
  s_min ╱────
        r_min    r_max
```

Maps [r_min, r_max] → [s_min, s_max]

#### Thresholding:
```
s = {
  L-1  if r > threshold
  0    if r ≤ threshold
}
```

#### Gray-level Slicing:
Highlight specific range of gray levels

---

## So Sánh Các Phép Biến Đổi

### Log vs Power-Law (γ < 1):

| Đặc điểm | Log | Power-Law (γ < 1) |
|----------|-----|-------------------|
| **Control** | Fixed curve | Adjustable γ |
| **Flexibility** | One shape | Many shapes |
| **Brightening** | Strong | Adjustable |
| **Use case** | Large dynamic range | General brightening |

**Common**: Both expand dark, compress bright

### Effect on Histogram:

#### Log Transform:
- **Histogram tập trung 0-70**:
  - → Spreads out toward right
  - More even distribution
  - Better contrast in dark regions

#### Gamma (γ < 1):
- **Histogram shifts right** (brighter)
- Amount depends on γ value
- Distribution shape changes

#### Gamma (γ > 1):
- **Histogram shifts left** (darker)
- Compresses into lower values

---

## Contrast & Brightness

### Brightness:
- Overall intensity level
- Shift histogram left/right
- Linear: `s = r + b`

### Contrast:
- Difference between intensities
- Spread histogram wider/narrower
- Linear: `s = a × r`

### Combined:
```
s = a × r + b
```
- a: Contrast factor
- b: Brightness offset

---

## Histogram-Based Transformations

### Histogram Equalization:
- Automatic contrast enhancement
- Spreads histogram evenly
- Detail trong phần lý thuyết riêng

### Histogram Matching:
- Transform to specific target distribution
- More control than equalization

---

## Ứng Dụng Thực Tế

### 1. Medical Imaging:
- **Log transform**: Enhance X-ray details
- **Gamma correction**: Adjust monitor display

### 2. Photography:
- **Gamma < 1**: Brighten underexposed photos
- **Gamma > 1**: Darken overexposed areas

### 3. Computer Vision:
- **Normalization**: Preprocessing for algorithms
- **Enhancement**: Improve feature detection

### 4. Display Technology:
- **Gamma correction**: Compensate for monitor gamma
- CRT displays: γ ≈ 2.5
- LCD displays: γ ≈ 2.2

---

## Đặc Điểm của Histogram sau Transform

### Ảnh với Histogram Tập Trung Vùng Thấp:

#### Trước Transform:
```
Count
  │  ███
  │  ███
  │  ███
  │  ███
  └──────────── Gray Level
    0   70  255
    ↑ concentrated
```

#### Sau Log Transform:
```
Count
  │    ┌─┐
  │   ┌┘ └┐
  │  ┌┘   └┐
  └──────────── Gray Level
    0       255
    ↑ spread out
```

**Hiệu ứng**:
- Vùng 0-70 được "stretched" → nhiều levels hơn
- Contrast trong vùng tối tăng
- Vùng sáng compressed → ít levels hơn

---

## Tips & Best Practices

### 1. Chọn Phép Transform:
- **Dark image**: Log hoặc γ < 1
- **Bright image**: γ > 1
- **Large dynamic range**: Log
- **Fine control needed**: Power-law

### 2. Parameter Tuning:
- Start với γ = 0.5 cho brightening
- Start với γ = 2.0 cho darkening
- Adjust dựa trên visual inspection

### 3. Preprocessing:
- Normalize input to [0, 1]
- Handle overflow/underflow

### 4. Postprocessing:
- Clip values to valid range
- Convert back to appropriate data type

### 5. Combine Transformations:
- Log → then contrast stretching
- Gamma → then histogram equalization

---

## Code Examples

### Log Transform:
```python
import numpy as np

def log_transform(image, c=None):
    if c is None:
        c = 255 / np.log(1 + np.max(image))

    log_image = c * np.log(1 + image.astype(float))
    return np.uint8(log_image)
```

### Power-Law Transform:
```python
def power_law_transform(image, gamma=1.0):
    # Normalize to [0, 1]
    normalized = image / 255.0

    # Apply gamma
    transformed = np.power(normalized, gamma)

    # Scale back to [0, 255]
    return np.uint8(transformed * 255)
```

### Combined:
```python
def adjust_brightness_contrast(image, alpha=1.0, beta=0):
    """
    alpha: contrast (1.0 = no change)
    beta: brightness (0 = no change)
    """
    return np.clip(alpha * image + beta, 0, 255).astype(np.uint8)
```

---

## Tham Khảo

- Digital Image Processing (Gonzalez & Woods) - Chapter 3
- Computer Vision: Algorithms and Applications (Szeliski) - Chapter 3.1
- "Gamma Correction" - Charles Poynton
- OpenCV Documentation: `cv2.LUT()`, `cv2.pow()`
- NumPy: `np.log()`, `np.power()`
