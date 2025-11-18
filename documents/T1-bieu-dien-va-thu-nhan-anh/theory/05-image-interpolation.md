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

## 14. Code Examples Chi tiết

### 14.1. Custom Bilinear Interpolation từ Scratch
```python
import numpy as np
import cv2

def bilinear_resize(img, new_height, new_width):
    """
    Custom bilinear interpolation implementation

    Args:
        img: Input image (grayscale)
        new_height, new_width: Target dimensions

    Returns:
        Resized image
    """
    old_height, old_width = img.shape
    new_img = np.zeros((new_height, new_width), dtype=img.dtype)

    # Scaling factors
    row_scale = old_height / new_height
    col_scale = old_width / new_width

    for i in range(new_height):
        for j in range(new_width):
            # Map to old coordinates
            old_i = i * row_scale
            old_j = j * col_scale

            # Get integer parts
            i0 = int(np.floor(old_i))
            j0 = int(np.floor(old_j))

            # Get fractional parts
            di = old_i - i0
            dj = old_j - j0

            # Clamp to image boundaries
            i0 = min(i0, old_height - 2)
            j0 = min(j0, old_width - 2)
            i1 = i0 + 1
            j1 = j0 + 1

            # Bilinear interpolation
            # f(x,y) = (1-dx)(1-dy)f00 + dx(1-dy)f10 + (1-dx)dy*f01 + dx*dy*f11
            val = (1 - dj) * (1 - di) * img[i0, j0] + \
                  dj * (1 - di) * img[i0, j1] + \
                  (1 - dj) * di * img[i1, j0] + \
                  dj * di * img[i1, j1]

            new_img[i, j] = int(val)

    return new_img

# Test
img = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)
resized_custom = bilinear_resize(img, 300, 300)
resized_cv2 = cv2.resize(img, (300, 300), interpolation=cv2.INTER_LINEAR)

# Compare
diff = np.abs(resized_custom.astype(float) - resized_cv2.astype(float))
print(f"Max difference: {diff.max()}")  # Should be small (~0-2)
print(f"Mean difference: {diff.mean():.2f}")
```

### 14.2. Comparison Dashboard
```python
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def compare_all_interpolations(img_path, scale_down=4):
    """
    So sánh tất cả interpolation methods

    Args:
        img_path: Path to image
        scale_down: Downsampling factor
    """
    # Load original
    img_original = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    H, W = img_original.shape

    # Downsample
    small_size = (W // scale_down, H // scale_down)
    img_small = cv2.resize(img_original, small_size, interpolation=cv2.INTER_AREA)

    # Upsample với different methods
    methods = {
        'NEAREST': cv2.INTER_NEAREST,
        'LINEAR': cv2.INTER_LINEAR,
        'CUBIC': cv2.INTER_CUBIC,
        'LANCZOS': cv2.INTER_LANCZOS4
    }

    results = {}
    for name, method in methods.items():
        upsampled = cv2.resize(img_small, (W, H), interpolation=method)
        psnr_val = psnr(img_original, upsampled, data_range=255)
        ssim_val = ssim(img_original, upsampled, data_range=255)

        results[name] = {
            'image': upsampled,
            'psnr': psnr_val,
            'ssim': ssim_val
        }

    # Visualize
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))

    axes[0, 0].imshow(img_original, cmap='gray')
    axes[0, 0].set_title('Original')
    axes[0, 0].axis('off')

    axes[0, 1].imshow(img_small, cmap='gray')
    axes[0, 1].set_title(f'Downsampled (1/{scale_down})')
    axes[0, 1].axis('off')

    axes[0, 2].axis('off')

    for idx, (name, data) in enumerate(results.items()):
        row = (idx + 3) // 3
        col = (idx + 3) % 3
        axes[row, col].imshow(data['image'], cmap='gray')
        axes[row, col].set_title(f"{name}\nPSNR: {data['psnr']:.2f} dB\nSSIM: {data['ssim']:.4f}")
        axes[row, col].axis('off')

    plt.tight_layout()
    plt.savefig('interpolation_comparison.png', dpi=150)
    print("Saved: interpolation_comparison.png")

    # Print results table
    print("\nInterpolation Method Comparison:")
    print(f"{'Method':<12} {'PSNR (dB)':<12} {'SSIM':<8}")
    print("-" * 35)
    for name, data in sorted(results.items(), key=lambda x: x[1]['ssim'], reverse=True):
        print(f"{name:<12} {data['psnr']:<12.2f} {data['ssim']:<8.4f}")

    return results

# compare_all_interpolations('lena.png', scale_down=4)
```

**Output mẫu**:
```
Interpolation Method Comparison:
Method       PSNR (dB)    SSIM
-----------------------------------
LANCZOS      32.45        0.9234
CUBIC        31.89        0.9187
LINEAR       29.67        0.8956
NEAREST      24.12        0.8123
```

### 14.3. Rotation với Different Interpolations
```python
def compare_rotation_interpolation(img_path, angle=45):
    """So sánh interpolation cho rotation"""
    img = cv2.imread(img_path)
    H, W = img.shape[:2]
    center = (W // 2, H // 2)

    methods = {
        'NEAREST': cv2.INTER_NEAREST,
        'LINEAR': cv2.INTER_LINEAR,
        'CUBIC': cv2.INTER_CUBIC
    }

    fig, axes = plt.subplots(2, 2, figsize=(12, 12))

    axes[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Original')
    axes[0, 0].axis('off')

    for idx, (name, method) in enumerate(methods.items()):
        # Get rotation matrix
        M = cv2.getRotationMatrix2D(center, angle, scale=1.0)

        # Rotate
        rotated = cv2.warpAffine(img, M, (W, H), flags=method)

        # Display
        row = (idx + 1) // 2
        col = (idx + 1) % 2
        axes[row, col].imshow(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))
        axes[row, col].set_title(f'{name}\nRotation {angle}°')
        axes[row, col].axis('off')

    plt.tight_layout()
    plt.savefig('rotation_interpolation.png', dpi=150)
    print("Saved: rotation_interpolation.png")

# compare_rotation_interpolation('photo.jpg', angle=45)
```

### 14.4. Smart Multi-step Resize
```python
def smart_resize(img, target_size, max_step_ratio=0.5):
    """
    Multi-step resize để giảm aliasing khi shrink nhiều

    Args:
        img: Input image
        target_size: (width, height) target
        max_step_ratio: Tỉ lệ tối đa giảm mỗi bước (0.5 = giảm 50%)

    Returns:
        Resized image
    """
    current = img.copy()
    current_size = (img.shape[1], img.shape[0])  # (W, H)

    steps = []

    # Calculate intermediate steps
    while (current_size[0] > target_size[0] * (1 / max_step_ratio)) or \
          (current_size[1] > target_size[1] * (1 / max_step_ratio)):

        new_w = max(int(current_size[0] * max_step_ratio), target_size[0])
        new_h = max(int(current_size[1] * max_step_ratio), target_size[1])
        steps.append((new_w, new_h))
        current_size = (new_w, new_h)

    steps.append(target_size)

    print(f"Resize plan: {img.shape[1]}x{img.shape[0]} → {' → '.join([f'{w}x{h}' for w,h in steps])}")

    # Resize step by step
    for step_size in steps:
        # Blur before downsampling
        kernel_size = 5
        current = cv2.GaussianBlur(current, (kernel_size, kernel_size), 0)

        # Downsample
        current = cv2.resize(current, step_size, interpolation=cv2.INTER_AREA)

    return current

# Example
img_large = cv2.imread('4k_image.jpg')
img_small_naive = cv2.resize(img_large, (640, 480), cv2.INTER_AREA)
img_small_smart = smart_resize(img_large, (640, 480))

# Compare quality
# img_small_smart should have better quality (less aliasing)
```

## 15. Best Practices

### ✅ Nên làm

1. **Chọn interpolation theo direction**
   ```python
   def auto_interpolation(img, new_size):
       old_size = (img.shape[1], img.shape[0])
       is_upscaling = new_size[0] > old_size[0] or new_size[1] > old_size[1]

       if is_upscaling:
           # Upscaling: Quality matters
           method = cv2.INTER_CUBIC
       else:
           # Downscaling: Anti-aliasing matters
           method = cv2.INTER_AREA

       return cv2.resize(img, new_size, interpolation=method)
   ```

2. **Anti-aliasing khi downsample**
   ```python
   def safe_downsample(img, scale_factor):
       # Gaussian blur trước
       sigma = scale_factor / 2
       kernel_size = int(2 * sigma * 2 + 1)
       blurred = cv2.GaussianBlur(img, (kernel_size, kernel_size), sigma)

       # Sau đó downsample
       new_size = (img.shape[1] // scale_factor, img.shape[0] // scale_factor)
       return cv2.resize(blurred, new_size, cv2.INTER_AREA)
   ```

3. **Benchmark khi chọn method**
   ```python
   import time

   methods = [cv2.INTER_NEAREST, cv2.INTER_LINEAR, cv2.INTER_CUBIC]
   for method in methods:
       start = time.time()
       for _ in range(100):
           resized = cv2.resize(img, (800, 600), interpolation=method)
       elapsed = time.time() - start
       print(f"{method}: {elapsed:.3f}s")
   ```

### ❌ Không nên làm

1. **Không dùng NEAREST cho photo downsampling**
   ```python
   # ❌ SAI - Severe aliasing
   small = cv2.resize(large_photo, (small_w, small_h), cv2.INTER_NEAREST)

   # ✅ ĐÚNG
   small = cv2.resize(large_photo, (small_w, small_h), cv2.INTER_AREA)
   ```

2. **Không dùng AREA cho upsampling**
   ```python
   # ❌ SAI - Blur
   big = cv2.resize(small, (big_w, big_h), cv2.INTER_AREA)

   # ✅ ĐÚNG
   big = cv2.resize(small, (big_w, big_h), cv2.INTER_CUBIC)
   ```

3. **Không resize ảnh nhiều lần liên tiếp**
   ```python
   # ❌ SAI - Quality degradation
   img = cv2.resize(img, (200, 200))
   img = cv2.resize(img, (300, 300))
   img = cv2.resize(img, (150, 150))

   # ✅ ĐÚNG - Resize 1 lần
   img = cv2.resize(original, (150, 150))
   ```

### 💡 Tips

1. **Interpolation selection cheat sheet**
   ```
   Task: Photo zoom             → CUBIC hoặc LANCZOS
   Task: Photo shrink           → AREA
   Task: Real-time video        → LINEAR
   Task: Pixel art              → NEAREST
   Task: Rotation/warp          → LINEAR hoặc CUBIC
   Task: Professional work      → LANCZOS
   ```

2. **Aspect ratio preservation**
   ```python
   def resize_keep_aspect(img, max_w, max_h):
       h, w = img.shape[:2]
       scale = min(max_w / w, max_h / h)
       new_w, new_h = int(w * scale), int(h * scale)
       return cv2.resize(img, (new_w, new_h), cv2.INTER_AREA)
   ```

## 16. Common Pitfalls

### Lỗi 1: Aspect ratio distortion
**Vấn đề**:
```python
img = cv2.resize(img, (300, 300))  # Bị méo nếu không vuông!
```

**Giải pháp**:
```python
# Preserve aspect ratio
h, w = img.shape[:2]
aspect = w / h
new_w = 300
new_h = int(new_w / aspect)
img_resized = cv2.resize(img, (new_w, new_h))
```

### Lỗi 2: Multiple resize degradation
**Vấn đề**: Resize nhiều lần → quality loss tích lũy.

**Giải pháp**: Lưu original, resize từ original mỗi lần cần.

### Lỗi 3: Quên anti-aliasing
**Vấn đề**: Downsample 4K → 480p trực tiếp → severe aliasing.

**Giải pháp**: Progressive downsample hoặc blur trước.

## 17. Bài tập Thực hành

### Bài 1: Implement Nearest Neighbor
**Đề bài**: Viết hàm `nearest_resize(img, new_size)` từ scratch.

**Gợi ý**: Map coordinates, round, clamp.

### Bài 2: Benchmark Interpolations
**Đề bài**: So sánh speed và quality của 5 methods.

**Yêu cầu**:
- Resize 1920×1080 → 640×480
- Measure time (100 iterations)
- Compute PSNR/SSIM vs ideal (high-res original)

### Bài 3: Smart Thumbnail Generator
**Đề bài**: Tạo thumbnail với aspect ratio preserved và quality tối ưu.

**Yêu cầu**:
- Input: Ảnh bất kỳ
- Output: 200×200 thumbnail (centered crop nếu cần)
- Sử dụng best interpolation method

## 18. Tóm tắt

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

**Key Takeaways**:
1. **INTER_AREA for downsampling** - prevents aliasing
2. **INTER_CUBIC for upsampling** - good quality/speed balance
3. **INTER_LANCZOS4 for professional** - best quality
4. **INTER_NEAREST for pixel art** - preserves sharp edges
5. **Anti-alias before downsample** - blur first with Gaussian

---

**References**:
- Gonzalez & Woods - Digital Image Processing (Chapter 2.4)
- OpenCV Documentation - Geometric Transformations
- "Keys, Robert G. - Cubic convolution interpolation for digital image processing" (1981)
