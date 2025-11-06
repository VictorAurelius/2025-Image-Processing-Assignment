# Phương Pháp Nội Suy Ảnh (Image Interpolation Methods)

## Giới Thiệu

Image interpolation là kỹ thuật ước tính giá trị pixel tại vị trí không nguyên (non-integer positions) dựa trên các pixel lân cận đã biết.

**Khi nào cần interpolation**:
- **Zooming/Upsampling**: Phóng to ảnh (e.g., 3×3 → 7×7)
- **Shrinking/Downsampling**: Thu nhỏ ảnh
- **Rotation**: Xoay ảnh
- **Geometric transformations**: Affine, perspective transforms
- **Image warping**: Biến dạng ảnh

## Khái Niệm Cơ Bản

### Problem:
```
Original: 3×3        Target: 7×7
  0  1  2             0    1    2    3    4    5    6
0 A  B  C          0  A   ?    ?    B    ?    ?    C
1 D  E  F    →     1  ?   ?    ?    ?    ?    ?    ?
2 G  H  I          2  ?   ?    ?    ?    ?    ?    ?
                   3  D   ?    ?    E    ?    ?    F
                   4  ?   ?    ?    ?    ?    ?    ?
                   5  ?   ?    ?    ?    ?    ?    ?
                   6  G   ?    ?    H    ?    ?    I
```

Cần estimate giá trị tại các vị trí "?" từ các giá trị đã biết A-I.

### Mapping:
```
target_coord = source_coord × scale_factor
```

Example: 3×3 → 7×7
```
scale = 7/3 ≈ 2.33
target_x = source_x × 2.33
```

Sau mapping, thường không rơi đúng vào grid → cần interpolation

---

## 1. Nearest Neighbor Interpolation

### Định Nghĩa:
Chọn giá trị pixel **gần nhất** (nearest) trong ảnh gốc.

### Công Thức:
```
f(x, y) = f(round(x), round(y))
```

### Thuật Toán:
1. Map coordinate từ target → source
2. Round to nearest integer
3. Copy giá trị

### Ví Dụ:
```
Source (3×3):         Target (7×7) - Nearest Neighbor:
1  2  3               1  1  2  2  2  3  3
4  5  6      →        1  1  2  2  2  3  3
7  8  9               4  4  5  5  5  6  6
                      4  4  5  5  5  6  6
                      7  7  8  8  8  9  9
                      7  7  8  8  8  9  9
                      7  7  8  8  8  9  9
```

**Pattern**: Mỗi pixel gốc được replicate thành một block

### Đặc Điểm:

#### Ưu Điểm:
- **Fastest** - O(1) per pixel
- **Simple** to implement
- **No new values** created (preserve original values)
- Good cho ảnh **categorical/labeled** (e.g., segmentation masks)

#### Nhược Điểm:
- **Blocky/pixelated** results
- **Jagged edges** (aliasing)
- **Discontinuities** visible
- Not smooth

#### Khi Nào Dùng:
- Speed critical
- Categorical data (labels, masks)
- Small magnification
- Pixel art (preserve sharp edges)

### Trong Đề Thi:
**"Nếu sử dụng nearest neighbor để tạo 7×7 thì ảnh mới là gì?"**

**Cách giải**:
1. Xác định scale factor: 7/original_size
2. For each target pixel:
   - Map back to source: source_pos = target_pos / scale
   - Round source_pos
   - Copy value
3. Kết quả sẽ có **block pattern** rõ ràng

---

## 2. Bilinear Interpolation

### Định Nghĩa:
Interpolation tuyến tính theo **2 directions** (x và y) sử dụng **4 nearest neighbors**.

### Công Thức:

Cho position (x, y) với:
- x = floor(x) + dx, where 0 ≤ dx < 1
- y = floor(y) + dy, where 0 ≤ dy < 1

```
f(x, y) = (1-dx)(1-dy) × f(x₀, y₀)     [top-left]
        + dx(1-dy) × f(x₁, y₀)         [top-right]
        + (1-dx)dy × f(x₀, y₁)         [bottom-left]
        + dx × dy × f(x₁, y₁)          [bottom-right]
```

Với:
- (x₀, y₀) = (floor(x), floor(y))
- (x₁, y₁) = (ceil(x), ceil(y))

### Visualize:

```
Known pixels:
  f(0,0)  ────  f(1,0)
    │             │
    │      ×(x,y) │  ← target position
    │             │
  f(0,1)  ────  f(1,1)

Weights based on distance:
  Closer → Higher weight
```

### Thuật Toán (Step-by-step):

1. **Map coordinate**: target → source
2. **Get 4 neighbors**:
   - Top-left: (floor(x), floor(y))
   - Top-right: (ceil(x), floor(y))
   - Bottom-left: (floor(x), ceil(y))
   - Bottom-right: (ceil(x), ceil(y))
3. **Interpolate horizontally** (2 times):
   - f_top = lerp(f_top_left, f_top_right, dx)
   - f_bottom = lerp(f_bottom_left, f_bottom_right, dx)
4. **Interpolate vertically**:
   - f(x,y) = lerp(f_top, f_bottom, dy)

### Ví Dụ Chi Tiết:

**Source (2×2):**
```
10  20
30  40
```

**Target position (0.5, 0.5)**:

```
Neighbors:
  f(0,0)=10   f(1,0)=20
  f(0,1)=30   f(1,1)=40

Calculation:
dx = 0.5, dy = 0.5

f(0.5, 0.5) = (1-0.5)(1-0.5) × 10    [weight 0.25]
            + 0.5(1-0.5) × 20         [weight 0.25]
            + (1-0.5)×0.5 × 30        [weight 0.25]
            + 0.5×0.5 × 40            [weight 0.25]
            = 0.25×10 + 0.25×20 + 0.25×30 + 0.25×40
            = 2.5 + 5 + 7.5 + 10
            = 25
```

**Result**: Exactly the average (center position)

### Ví Dụ Scaling:

**Source (3×3):**
```
1  2  3
4  5  6
7  8  9
```

**Target (7×7) - Bilinear**:
```
1.0  1.3  1.7  2.0  2.3  2.7  3.0
2.0  2.3  2.7  3.0  3.3  3.7  4.0
3.3  3.7  4.0  4.3  4.7  5.0  5.3
4.0  4.3  4.7  5.0  5.3  5.7  6.0
5.3  5.7  6.0  6.3  6.7  7.0  7.3
6.0  6.3  6.7  7.0  7.3  7.7  8.0
7.0  7.3  7.7  8.0  8.3  8.7  9.0
```

**Pattern**: Smooth transitions, no blocks

### Đặc Điểm:

#### Ưu Điểm:
- **Smooth results** (mượt hơn nhiều)
- **No blocky artifacts**
- **Continuous** output
- **Good quality/speed trade-off**
- Most commonly used

#### Nhược Điểm:
- **Blurs edges** slightly
- **New values** created (average of neighbors)
- Slower than nearest neighbor
- Not as sharp as bicubic

#### Khi Nào Dùng:
- General purpose resizing
- Real-time applications (games, video)
- Good balance between quality and speed
- Continuous data (photos, natural images)

### Trong Đề Thi:

**"Nếu dùng bilinear để tạo 7×7 thì ảnh mới là gì?"**

**Cách giải**:
1. Calculate scale factor
2. For each target pixel:
   - Map to source (will be fractional)
   - Find 4 neighbors
   - Calculate weights based on distance
   - Weighted average
3. Kết quả: **Smooth gradients**, không có blocks

**"Nếu dùng bilinear để tạo 3×3 thì ảnh mới là gì?"**

**Với downsampling nhỏ**:
- May vẫn có some aliasing
- But smoother than nearest neighbor

---

## 3. Bicubic Interpolation

### Định Nghĩa:
Uses **16 nearest neighbors** (4×4 grid) với cubic polynomial.

### Công Thức:
Phức tạp hơn, sử dụng cubic convolution kernel.

### Đặc Điểm:

#### Ưu Điểm:
- **Highest quality** của 3 methods cơ bản
- **Sharpest edges**
- **Smoother than bilinear**
- Professional standard

#### Nhược Điểm:
- **Slowest** - 16 pixels per calculation
- More complex
- May introduce slight ringing
- Overkill for some applications

#### Khi Nào Dùng:
- High-quality required
- Photography, professional editing
- Slow is acceptable
- Upsampling >2x

---

## 4. Area Interpolation (INTER_AREA)

### Định Nghĩa:
Resampling using pixel area relation. Tốt cho **downsampling**.

### Đặc Điểm:
- **Best for shrinking** images
- Reduces aliasing when downsampling
- Essentially averages regions
- OpenCV default for decimation

### Khi Dùng:
- **Shrinking images** (e.g., 1024×1024 → 512×512)
- Creating thumbnails
- Preventing aliasing in downsampling

---

## So Sánh Methods

| Method | Speed | Quality | Use Case | Neighbors Used |
|--------|-------|---------|----------|----------------|
| **Nearest Neighbor** | Fastest | Lowest - Blocky | Categorical data, speed | 1 |
| **Bilinear** | Fast | Good - Smooth | General purpose | 4 |
| **Bicubic** | Slow | Best - Sharpest | High quality | 16 |
| **Area** | Medium | Good for downsample | Shrinking images | Variable |

---

## Hiệu Ứng Trên Edges

### Nearest Neighbor:
```
Original edge:     Enlarged:
  0 0 1 1           0 0 0 1 1 1
                    0 0 0 1 1 1
                    0 0 0 1 1 1
```
Sharp, blocky edge

### Bilinear:
```
Original edge:     Enlarged:
  0 0 1 1           0 0 0.3 0.7 1 1
                    0 0 0.3 0.7 1 1
```
Smooth transition, slight blur

### Bicubic:
```
Original edge:     Enlarged:
  0 0 1 1           0 0 0.4 0.9 1 1
                    0 0 0.4 0.9 1 1
```
Sharper than bilinear, still smooth

---

## Connected Components và Connectivity

### Trong Binary Images:

#### Nearest Neighbor:
- **Preserves topology** better
- **4-connectivity** và **8-connectivity** maintained
- Sharp boundaries

#### Bilinear:
- **Grayscale values** created at boundaries
- Need re-threshold if binary output required
- May change connectivity counts

**Implication**:
- For binary images needing connectivity analysis → Nearest Neighbor preferred
- For display → Bilinear better

---

## Practical Considerations

### 1. Upsampling (Zooming):
- **2x or less**: Bilinear sufficient
- **More than 2x**: Consider bicubic
- **Pixel art**: Nearest neighbor

### 2. Downsampling (Shrinking):
- **Prefer Area or Bilinear**
- Avoid nearest neighbor (aliasing)
- Consider anti-aliasing filter first

### 3. Rotation:
- Usually **Bilinear** or **Bicubic**
- Nearest causes stepping artifacts

### 4. Real-time:
- **Nearest Neighbor** for speed
- Bilinear if GPU available

---

## Implementation Tips

### Boundary Handling:
```python
# Clamp coordinates
x = max(0, min(x, width-1))
y = max(0, min(y, height-1))
```

### Optimization:
- **Pre-calculate** scale factors
- **Lookup tables** for weights
- **SIMD** instructions for parallel processing
- **GPU** for large images

### Precision:
- Use **float** for calculations
- Round only at final step
- Avoid accumulating errors

---

## Code Examples

### OpenCV:
```python
import cv2

# Nearest Neighbor
nearest = cv2.resize(img, (new_width, new_height),
                     interpolation=cv2.INTER_NEAREST)

# Bilinear
bilinear = cv2.resize(img, (new_width, new_height),
                      interpolation=cv2.INTER_LINEAR)

# Bicubic
bicubic = cv2.resize(img, (new_width, new_height),
                     interpolation=cv2.INTER_CUBIC)

# Area (for downsampling)
area = cv2.resize(img, (new_width, new_height),
                  interpolation=cv2.INTER_AREA)
```

### Manual Bilinear:
```python
def bilinear_interpolate(img, x, y):
    x0, y0 = int(x), int(y)
    x1, y1 = min(x0 + 1, img.shape[1]-1), min(y0 + 1, img.shape[0]-1)

    dx, dy = x - x0, y - y0

    value = (1-dx)*(1-dy) * img[y0, x0] + \
            dx*(1-dy) * img[y0, x1] + \
            (1-dx)*dy * img[y1, x0] + \
            dx*dy * img[y1, x1]

    return value
```

---

## Tham Khảo

- Digital Image Processing (Gonzalez & Woods) - Chapter 2
- "Interpolation Methods" - Keys (1981)
- OpenCV Documentation: `cv2.resize()`
- PIL/Pillow Documentation: `Image.resize()`
- scikit-image: `skimage.transform.resize()`
