# Lý thuyết: Nội suy Ảnh (Image Interpolation)

## 1. Giới thiệu

Nội suy ảnh là quá trình ước tính giá trị pixel tại các vị trí không nguyên trong ảnh gốc, cần thiết khi:
- **Zooming (phóng to)**: Tăng kích thước ảnh
- **Shrinking (thu nhỏ)**: Giảm kích thước ảnh
- **Rotation**: Xoay ảnh
- **Geometric transformation**: Biến đổi hình học

## 2. Nearest Neighbor Interpolation

### 2.1. Nguyên lý
Lấy giá trị pixel gần nhất:
```
f(x, y) = f(round(x), round(y))
```

### 2.2. Thuật toán
```python
def nearest_neighbor(img, new_size):
    H_old, W_old = img.shape
    H_new, W_new = new_size

    result = np.zeros((H_new, W_new))

    for i in range(H_new):
        for j in range(W_new):
            # Map new coordinate to old coordinate
            i_old = round(i * H_old / H_new)
            j_old = round(j * W_old / W_new)

            # Clamp to valid range
            i_old = min(i_old, H_old - 1)
            j_old = min(j_old, W_old - 1)

            result[i, j] = img[i_old, j_old]

    return result
```

### 2.3. Ưu nhược điểm

**Ưu điểm**:
- **Rất nhanh**: O(1) per pixel
- **Đơn giản**: Dễ implement
- **Giữ nguyên giá trị**: Không tạo giá trị mới

**Nhược điểm**:
- **Blocky effect**: Hiệu ứng răng cưa
- **Discontinuities**: Không mượt
- **Chất lượng thấp**: Khi zoom lớn

**Ứng dụng**: Real-time processing, preview, pixel art

### 2.4. OpenCV
```python
resized = cv2.resize(img, new_size, interpolation=cv2.INTER_NEAREST)
```

## 3. Bilinear Interpolation

### 3.1. Nguyên lý
Nội suy tuyến tính theo 2 chiều (x và y):
```
f(x, y) = weighted average of 4 nearest pixels
```

### 3.2. Công thức
Cho điểm (x, y) với x ∈ [x₁, x₂], y ∈ [y₁, y₂]:

**Bước 1**: Nội suy theo x
```
f(x, y₁) = ((x₂ - x) × f(x₁, y₁) + (x - x₁) × f(x₂, y₁)) / (x₂ - x₁)
f(x, y₂) = ((x₂ - x) × f(x₁, y₂) + (x - x₁) × f(x₂, y₂)) / (x₂ - x₁)
```

**Bước 2**: Nội suy theo y
```
f(x, y) = ((y₂ - y) × f(x, y₁) + (y - y₁) × f(x, y₂)) / (y₂ - y₁)
```

### 3.3. Dạng đơn giản hóa
Với fractional parts α = x - floor(x), β = y - floor(y):
```
f(x, y) = (1-α)(1-β)×f₀₀ + α(1-β)×f₁₀ + (1-α)β×f₀₁ + αβ×f₁₁
```

Trong đó f_ij là giá trị tại 4 góc.

### 3.4. Ưu nhược điểm

**Ưu điểm**:
- **Mượt mà**: Không có discontinuities
- **Chất lượng tốt**: Tốt hơn nearest neighbor
- **Vẫn nhanh**: O(1) với lookup 4 pixels

**Nhược điểm**:
- **Blur nhẹ**: Mất một chút chi tiết
- **Không giữ giá trị gốc**: Tạo giá trị trung gian

**Ứng dụng**: Zooming images, texture mapping, general purpose

### 3.5. OpenCV
```python
resized = cv2.resize(img, new_size, interpolation=cv2.INTER_LINEAR)
```

## 4. Bicubic Interpolation

### 4.1. Nguyên lý
Sử dụng đa thức bậc 3 để nội suy từ 16 pixel láng giềng (4×4):
```
f(x, y) = Σᵢ Σⱼ aᵢⱼ xⁱ yʲ  (i, j = 0..3)
```

### 4.2. Đặc điểm
- **16 neighbors**: Xét lưới 4×4
- **Smooth**: C¹ continuous (đạo hàm liên tục)
- **Better than bilinear**: Ít blur hơn, sắc nét hơn

### 4.3. Ưu nhược điểm

**Ưu điểm**:
- **Chất lượng cao**: Sắc nét, mượt mà
- **Tốt cho zooming**: Giữ chi tiết tốt
- **Smooth gradients**: Gradient đẹp

**Nhược điểm**:
- **Chậm hơn**: O(16) lookups per pixel
- **Có thể overshoot**: Tạo giá trị nằm ngoài [min, max] của 16 neighbors

**Ứng dụng**: High-quality image scaling, professional image editing

### 4.4. OpenCV
```python
resized = cv2.resize(img, new_size, interpolation=cv2.INTER_CUBIC)
```

## 5. Area Interpolation

### 5.1. Nguyên lý
Lấy trung bình của vùng pixel tương ứng:
```
f(x, y) = average of all pixels mapping to (x, y)
```

### 5.2. Đặc điểm
- **Best for shrinking**: Giảm aliasing
- **Resampling**: Lấy mẫu lại đúng cách
- **Slower**: Phải xét nhiều pixels

### 5.3. Ứng dụng
Tối ưu cho **downsampling** (thu nhỏ ảnh):
```python
small = cv2.resize(large, smaller_size, interpolation=cv2.INTER_AREA)
```

## 6. Lanczos Interpolation

### 6.1. Nguyên lý
Sử dụng sinc function với windowing:
```
L(x) = sinc(x) × sinc(x/a)  for |x| < a
```

Thường a = 3 (Lanczos-3)

### 6.2. Đặc điểm
- **High quality**: Chất lượng rất cao
- **Sharp**: Sắc nét nhất
- **Slow**: Chậm nhất
- **8×8 neighbors**: Xét lưới 8×8

### 6.3. OpenCV
```python
resized = cv2.resize(img, new_size, interpolation=cv2.INTER_LANCZOS4)
```

## 7. Pixel Replication

### 7.1. Nguyên lý
Nhân bản pixel theo tỷ lệ nguyên:
```python
# Zoom ×k
zoomed = np.repeat(np.repeat(img, k, axis=0), k, axis=1)
```

### 7.2. Đặc điểm
- **Simplest**: Đơn giản nhất
- **Blocky**: Hiệu ứng block rõ ràng
- **Fast**: Rất nhanh cho tỷ lệ nguyên
- **Pixel art style**: Giữ pixel art aesthetic

### 7.3. Ứng dụng
- Pixel art games
- Retro graphics
- Quick preview

## 8. So sánh các phương pháp

| Method | Speed | Quality | Blur | Aliasing | Best for |
|--------|-------|---------|------|----------|----------|
| Nearest | ⭐⭐⭐⭐⭐ | ⭐ | None | High | Real-time, pixel art |
| Bilinear | ⭐⭐⭐⭐ | ⭐⭐⭐ | Medium | Low | General purpose |
| Bicubic | ⭐⭐⭐ | ⭐⭐⭐⭐ | Low | Very low | High quality zoom |
| Area | ⭐⭐⭐ | ⭐⭐⭐⭐ | Low | Minimal | Shrinking |
| Lanczos | ⭐⭐ | ⭐⭐⭐⭐⭐ | Minimal | Minimal | Professional |
| Replication | ⭐⭐⭐⭐⭐ | ⭐ | None | High | Pixel art |

## 9. Lựa chọn phương pháp

### 9.1. Theo tác vụ
```
Zooming (Enlarge):
  - Real-time → Nearest or Bilinear
  - Quality → Bicubic or Lanczos
  - Pixel art → Nearest or Replication

Shrinking (Reduce):
  - Always → INTER_AREA
  - Or → Bicubic/Lanczos

Rotation:
  - Bilinear or Bicubic

Arbitrary transform:
  - Bilinear (fast) or Bicubic (quality)
```

### 9.2. Theo chất lượng/tốc độ
```
Need speed: Nearest > Bilinear > Bicubic > Lanczos
Need quality: Lanczos > Bicubic > Area > Bilinear > Nearest
```

## 10. Anti-aliasing

### 10.1. Vấn đề Aliasing
Khi shrinking, chi tiết cao tần bị méo (aliasing)

**Giải pháp**: Blur trước khi shrink
```python
# Blur first
blurred = cv2.GaussianBlur(img, (5, 5), 0)

# Then shrink
small = cv2.resize(blurred, smaller_size, cv2.INTER_AREA)
```

### 10.2. Mipmap
Chuỗi ảnh với resolution giảm dần (×1, ×0.5, ×0.25, ...):
- Pre-computed for speed
- Select appropriate level
- Used in texture mapping

## 11. Round-trip Quality

**Thí nghiệm**: Original → Shrink → Enlarge back

```python
original = img  # 1000×1000
small = cv2.resize(original, (500, 500), cv2.INTER_AREA)
back = cv2.resize(small, (1000, 1000), cv2.INTER_CUBIC)

psnr = cv2.PSNR(original, back)
```

**Kết quả thường thấy**:
- INTER_NEAREST: PSNR ~20-25 dB (kém)
- INTER_LINEAR: PSNR ~25-30 dB (tốt)
- INTER_CUBIC: PSNR ~30-35 dB (rất tốt)
- INTER_LANCZOS4: PSNR ~32-37 dB (xuất sắc)

## 12. Code Examples

### 12.1. So sánh tất cả methods
```python
methods = [
    ('Nearest', cv2.INTER_NEAREST),
    ('Linear', cv2.INTER_LINEAR),
    ('Cubic', cv2.INTER_CUBIC),
    ('Area', cv2.INTER_AREA),
    ('Lanczos', cv2.INTER_LANCZOS4)
]

for name, method in methods:
    resized = cv2.resize(img, new_size, interpolation=method)
    cv2.imwrite(f'resized_{name}.png', resized)
```

### 12.2. Custom bilinear
```python
def bilinear_interpolate(img, x, y):
    x1, y1 = int(np.floor(x)), int(np.floor(y))
    x2, y2 = x1 + 1, y1 + 1

    # Clamp
    x1 = np.clip(x1, 0, img.shape[1]-1)
    x2 = np.clip(x2, 0, img.shape[1]-1)
    y1 = np.clip(y1, 0, img.shape[0]-1)
    y2 = np.clip(y2, 0, img.shape[0]-1)

    # Fractional parts
    alpha = x - x1
    beta = y - y1

    # Interpolate
    return (1-alpha)*(1-beta)*img[y1,x1] + \
           alpha*(1-beta)*img[y1,x2] + \
           (1-alpha)*beta*img[y2,x1] + \
           alpha*beta*img[y2,x2]
```

## 13. Best Practices

### 13.1. General guidelines
- **Zooming**: INTER_CUBIC or INTER_LANCZOS4
- **Shrinking**: INTER_AREA always
- **Real-time**: INTER_NEAREST or INTER_LINEAR
- **Quality priority**: INTER_LANCZOS4
- **Speed priority**: INTER_NEAREST

### 13.2. Avoid
- Don't use INTER_NEAREST for shrinking (aliasing)
- Don't use INTER_AREA for zooming (blur)
- Don't shrink too much at once (shrink in steps)

### 13.3. Multi-step resize
```python
# Better quality for large shrinking
def smart_resize(img, target_size):
    current = img.copy()
    current_size = img.shape[:2]

    while current_size[0] > target_size[0] * 2:
        new_size = (current_size[0] // 2, current_size[1] // 2)
        current = cv2.resize(current, new_size, cv2.INTER_AREA)
        current_size = new_size

    return cv2.resize(current, target_size, cv2.INTER_AREA)
```

## 14. Tóm tắt

**Interpolation methods hierarchy**:
```
Quality:  Lanczos > Bicubic > Bilinear > Nearest
Speed:    Nearest > Bilinear > Bicubic > Lanczos
Aliasing: Area/Lanczos > Bicubic > Bilinear > Nearest
```

**Quick decision tree**:
```
Is it zooming?
  ├─ Yes: Need quality? → Bicubic/Lanczos : Bilinear
  └─ No (shrinking): Always use INTER_AREA
```

---

**References**:
- Gonzalez & Woods - Digital Image Processing (Chapter 2.4)
- OpenCV Documentation - Geometric Transformations
- "Keys, Robert G. - Cubic convolution interpolation for digital image processing" (1981)
