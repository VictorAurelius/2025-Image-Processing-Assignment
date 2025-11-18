# Lý thuyết: Lấy Mẫu và Lượng Tử Hóa (Sampling & Quantization)

## 1. Giới thiệu

Ảnh số (digital image) được tạo ra từ ảnh tương tự (analog image) thông qua hai quá trình:
1. **Lấy mẫu (Sampling)**: Rời rạc hóa tọa độ không gian
2. **Lượng tử hóa (Quantization)**: Rời rạc hóa giá trị mức xám

## 2. Lấy Mẫu (Sampling)

### 2.1. Định nghĩa
Lấy mẫu là quá trình chia ảnh liên tục thành một lưới các pixel rời rạc.

**Ảnh liên tục**: f(x, y) với x, y ∈ ℝ
**Ảnh rời rạc**: f[i, j] với i, j ∈ ℤ

### 2.2. Độ phân giải không gian (Spatial Resolution)
- Số lượng pixel trong ảnh: M × N
  - M: số hàng (height)
  - N: số cột (width)
- Mật độ pixel: DPI (Dots Per Inch) hoặc PPI (Pixels Per Inch)

**Ví dụ**:
- 720p: 1280 × 720 pixels
- 1080p (Full HD): 1920 × 1080 pixels
- 4K (UHD): 3840 × 2160 pixels

### 2.3. Định lý Nyquist-Shannon
Để tránh hiện tượng aliasing khi lấy mẫu:

```
f_sampling >= 2 × f_max
```

Trong đó:
- f_sampling: Tần số lấy mẫu
- f_max: Tần số cao nhất trong tín hiệu gốc

**Ý nghĩa**: Cần lấy mẫu ít nhất 2 lần tần số cao nhất để tái tạo lại tín hiệu.

### 2.4. Aliasing
**Hiện tượng**: Khi lấy mẫu không đủ dày, chi tiết cao tần bị méo thành chi tiết thấp tần.

**Ví dụ**:
- Bánh xe quay trong phim có vẻ quay ngược
- Đường kẻ chéo bị răng cưa (jagged edges)

**Giải pháp**:
- Tăng tần số lấy mẫu
- Dùng anti-aliasing filter trước khi lấy mẫu

## 3. Lượng Tử Hóa (Quantization)

### 3.1. Định nghĩa
Lượng tử hóa là quá trình chuyển giá trị liên tục của mức xám thành các giá trị rời rạc.

**Ảnh liên tục**: I(x, y) ∈ [0, ∞)
**Ảnh lượng tử hóa**: I_q(x, y) ∈ {0, 1, 2, ..., L-1}

### 3.2. Độ phân giải mức xám (Gray-level Resolution)
Số lượng mức xám có thể biểu diễn:

```
L = 2^k
```

Trong đó:
- L: Số mức xám
- k: Số bit dùng để biểu diễn (bit-depth)

**Ví dụ**:
- k = 1 bit: L = 2 (nhị phân: 0, 1)
- k = 4 bit: L = 16 (0-15)
- k = 8 bit: L = 256 (0-255) - Tiêu chuẩn
- k = 10 bit: L = 1024 (0-1023)
- k = 12 bit: L = 4096 (0-4095)
- k = 16 bit: L = 65536 (0-65535)

### 3.3. Lượng tử hóa đều (Uniform Quantization)
Chia khoảng giá trị thành L khoảng bằng nhau:

```
Δ = (I_max - I_min) / L
```

**Thuật toán**:
```python
# Normalize to [0, 1]
normalized = (img - img.min()) / (img.max() - img.min())

# Quantize
quantized_index = round(normalized * (L - 1))

# Reconstruct
reconstructed = quantized_index / (L - 1) * (img.max() - img.min()) + img.min()
```

### 3.4. Sai số lượng tử hóa (Quantization Error)
```
e(i, j) = I_q(i, j) - I(i, j)
```

**Đặc điểm**:
- Sai số tối đa: ±Δ/2
- Giảm k → tăng Δ → tăng sai số
- Xuất hiện hiệu ứng "false contour" (đường viền giả)

### 3.5. Hiệu ứng Posterization
Khi k quá nhỏ, ảnh có vẻ như poster với các vùng màu phẳng rõ ràng.

**Nguyên nhân**: Không đủ mức xám để biểu diễn gradient mượt

## 4. Trade-off giữa Sampling và Quantization

### 4.1. Kích thước file
```
Size = M × N × k (bits)
     = M × N × k / 8 (bytes)
```

**Ví dụ**: Ảnh 1920×1080, 8-bit:
```
Size = 1920 × 1080 × 8 / 8 = 2,073,600 bytes ≈ 2 MB
```

### 4.2. So sánh

| Yếu tố | Ảnh hưởng | Trade-off |
|--------|-----------|-----------|
| M × N ↑ | Tăng chi tiết không gian | Tăng dung lượng theo O(MN) |
| k ↑ | Tăng chi tiết mức xám | Tăng dung lượng tuyến tính |
| M × N ↓ | Mất chi tiết, blur, blocky | Giảm dung lượng |
| k ↓ | False contour, posterization | Giảm dung lượng |

### 4.3. Quy tắc thumb
- **Spatial**: Tăng resolution quan trọng hơn nếu cần chi tiết hình học
- **Quantization**: Tăng bit-depth quan trọng hơn nếu cần gradient mượt
- **Cân bằng**: 8-bit thường đủ cho mắt người; resolution tùy ứng dụng

## 5. Ứng dụng thực tế

### 5.1. Photography
- **JPEG**: 8-bit per channel (24-bit RGB)
- **RAW**: 12-14 bit per channel
- **Lý do**: RAW cần dynamic range cao cho post-processing

### 5.2. Medical Imaging
- **X-ray**: 10-16 bit
- **CT/MRI**: 12-16 bit
- **Lý do**: Cần chi tiết mức xám cao để phân biệt mô

### 5.3. Video Streaming
- **SD**: 480p, 8-bit
- **HD**: 720p/1080p, 8-bit
- **4K HDR**: 3840×2160, 10-bit
- **Lý do**: Trade-off giữa chất lượng và băng thông

### 5.4. Surveillance
- **Resolution**: 720p-4K tùy yêu cầu
- **Bit-depth**: 8-bit thường đủ
- **FPS**: 15-30 fps
- **Lý do**: Cân bằng giữa chi tiết, storage, băng thông

## 6. Công thức quan trọng

### 6.1. Kích thước ảnh
```
Total pixels = M × N
Total bits = M × N × k
Total bytes = M × N × k / 8
```

### 6.2. Số mức xám
```
L = 2^k
k = log₂(L)
```

### 6.3. Bandwidth (video)
```
Bandwidth (bps) = M × N × k × fps
Bandwidth (Mbps) = M × N × k × fps / (1024 × 1024)
```

### 6.4. Storage (video)
```
Storage (bytes) = M × N × k × fps × duration / 8
```

## 7. Code Examples Chi Tiết

### 7.1. Demo Sampling với độ phân giải khác nhau
```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

def demonstrate_sampling(image_path):
    """Demo hiệu ứng của sampling với các độ phân giải khác nhau"""
    # Đọc ảnh gốc
    img_original = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    H, W = img_original.shape

    # Các độ phân giải khác nhau (giảm dần)
    resolutions = [
        (H, W),           # Original
        (H//2, W//2),     # 50%
        (H//4, W//4),     # 25%
        (H//8, W//8),     # 12.5%
        (64, 64),         # Fixed low resolution
        (32, 32)          # Very low
    ]

    results = []
    for new_size in resolutions:
        # Downsample
        downsampled = cv2.resize(img_original, (new_size[1], new_size[0]))
        # Upsample back to original size for comparison
        upsampled = cv2.resize(downsampled, (W, H), interpolation=cv2.INTER_NEAREST)
        results.append(upsampled)

    # Hiển thị kết quả
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    titles = ['Original', '50%', '25%', '12.5%', '64x64', '32x32']

    for i, (ax, img, title) in enumerate(zip(axes.flatten(), results, titles)):
        ax.imshow(img, cmap='gray')
        ax.set_title(f'{title}\n{resolutions[i][0]}x{resolutions[i][1]}')
        ax.axis('off')

    plt.tight_layout()
    plt.savefig('sampling_demo.png', dpi=150)
    print("Saved: sampling_demo.png")

    return results

# Sử dụng
# demonstrate_sampling('lena.png')
```

**Output**: Sẽ thấy rõ hiệu ứng blocky và mất chi tiết khi giảm resolution.

### 7.2. Demo Quantization với bit-depth khác nhau
```python
def demonstrate_quantization(image_path):
    """Demo hiệu ứng của quantization với các bit-depth khác nhau"""
    img_original = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Các bit-depth khác nhau
    bit_depths = [8, 7, 6, 5, 4, 3, 2, 1]

    results = {}
    for k in bit_depths:
        L = 2 ** k  # Số mức xám

        # Uniform quantization
        # Normalize to [0, L-1]
        quantized_index = np.floor(img_original.astype(np.float32) / 256 * L)
        quantized_index = np.clip(quantized_index, 0, L - 1)

        # Reconstruct to [0, 255]
        reconstructed = (quantized_index / (L - 1) * 255).astype(np.uint8)

        results[k] = reconstructed

    # Hiển thị
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))

    for i, (ax, k) in enumerate(zip(axes.flatten(), bit_depths)):
        ax.imshow(results[k], cmap='gray', vmin=0, vmax=255)
        ax.set_title(f'{k}-bit ({2**k} levels)')
        ax.axis('off')

    plt.tight_layout()
    plt.savefig('quantization_demo.png', dpi=150)
    print("Saved: quantization_demo.png")

    # In thống kê
    print("\nQuantization Statistics:")
    print(f"{'Bits':<6} {'Levels':<8} {'Unique Values':<15} {'File Size (approx)'}")
    for k in bit_depths:
        unique = len(np.unique(results[k]))
        size = img_original.size * k / 8 / 1024  # KB
        print(f"{k:<6} {2**k:<8} {unique:<15} {size:.2f} KB")

    return results

# Sử dụng
# demonstrate_quantization('lena.png')
```

**Output mẫu**:
```
Quantization Statistics:
Bits   Levels   Unique Values   File Size (approx)
8      256      256             256.00 KB
7      128      128             224.00 KB
6      64       64              192.00 KB
5      32       32              160.00 KB
4      16       16              128.00 KB
3      8        8               96.00 KB
2      4        4               64.00 KB
1      2        2               32.00 KB
```

### 7.3. So sánh Sampling vs Quantization
```python
def compare_sampling_vs_quantization(image_path):
    """So sánh hiệu ứng của giảm sampling vs giảm quantization"""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    H, W = img.shape

    # Scenario 1: Giảm spatial resolution, giữ 8-bit
    spatial_reduced = cv2.resize(img, (W//4, H//4))
    spatial_back = cv2.resize(spatial_reduced, (W, H), cv2.INTER_NEAREST)

    # Scenario 2: Giảm bit-depth, giữ spatial resolution
    L = 16  # 4-bit
    quantized = np.floor(img.astype(np.float32) / 256 * L)
    quantized = (quantized / (L - 1) * 255).astype(np.uint8)

    # Scenario 3: Giảm cả hai
    both_reduced = cv2.resize(img, (W//4, H//4))
    both_quant = np.floor(both_reduced.astype(np.float32) / 256 * L)
    both_quant = (both_quant / (L - 1) * 255).astype(np.uint8)
    both_back = cv2.resize(both_quant, (W, H), cv2.INTER_NEAREST)

    # Tính PSNR
    from skimage.metrics import peak_signal_noise_ratio as psnr

    psnr_spatial = psnr(img, spatial_back, data_range=255)
    psnr_quant = psnr(img, quantized, data_range=255)
    psnr_both = psnr(img, both_back, data_range=255)

    # Hiển thị
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))

    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('Original\n(Full resolution, 8-bit)')

    axes[0, 1].imshow(spatial_back, cmap='gray')
    axes[0, 1].set_title(f'Reduced Spatial (25%, 8-bit)\nPSNR: {psnr_spatial:.2f} dB')

    axes[1, 0].imshow(quantized, cmap='gray')
    axes[1, 0].set_title(f'Reduced Quantization (100%, 4-bit)\nPSNR: {psnr_quant:.2f} dB')

    axes[1, 1].imshow(both_back, cmap='gray')
    axes[1, 1].set_title(f'Both Reduced (25%, 4-bit)\nPSNR: {psnr_both:.2f} dB')

    for ax in axes.flatten():
        ax.axis('off')

    plt.tight_layout()
    plt.savefig('sampling_vs_quantization.png', dpi=150)
    print("Saved: sampling_vs_quantization.png")

    print("\nComparison Results:")
    print(f"Spatial reduction only: PSNR = {psnr_spatial:.2f} dB")
    print(f"Quantization only:      PSNR = {psnr_quant:.2f} dB")
    print(f"Both reductions:        PSNR = {psnr_both:.2f} dB")

# Sử dụng
# compare_sampling_vs_quantization('lena.png')
```

### 7.4. Visualization: False Contour vs Aliasing
```python
def visualize_artifacts(image_path):
    """Hiển thị false contour và aliasing"""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Create gradient image to show false contour clearly
    gradient = np.linspace(0, 255, 512).reshape(1, -1)
    gradient = np.repeat(gradient, 100, axis=0).astype(np.uint8)

    # False contour (severe quantization)
    L = 8  # 3-bit
    false_contour = np.floor(gradient.astype(np.float32) / 256 * L)
    false_contour = (false_contour / (L - 1) * 255).astype(np.uint8)

    # Aliasing (severe downsampling)
    H, W = img.shape
    aliased = cv2.resize(img, (W//8, H//8))
    aliased_back = cv2.resize(aliased, (W, H), cv2.INTER_NEAREST)

    # Display
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))

    axes[0, 0].imshow(gradient, cmap='gray')
    axes[0, 0].set_title('Smooth Gradient (8-bit)')

    axes[0, 1].imshow(false_contour, cmap='gray')
    axes[0, 1].set_title('False Contour (3-bit)\nPosterization effect')

    axes[1, 0].imshow(img, cmap='gray')
    axes[1, 0].set_title('Original Image')

    axes[1, 1].imshow(aliased_back, cmap='gray')
    axes[1, 1].set_title('Aliasing (12.5% resolution)\nBlocky effect')

    for ax in axes.flatten():
        ax.axis('off')

    plt.tight_layout()
    plt.savefig('artifacts_demo.png', dpi=150)
    print("Saved: artifacts_demo.png")

# Sử dụng
# visualize_artifacts('lena.png')
```

## 8. Best Practices

### ✅ Nên làm

1. **Chọn bit-depth phù hợp với ứng dụng**
   ```python
   # Photography/Display
   bit_depth = 8  # 256 levels, đủ cho mắt người

   # Medical imaging
   bit_depth = 12  # 4096 levels, cần dynamic range cao

   # HDR video
   bit_depth = 10  # 1024 levels, tốt hơn 8-bit cho grading
   ```
   **Lý do**: Tránh lãng phí storage nhưng vẫn đảm bảo chất lượng.

2. **Áp dụng định lý Nyquist khi lấy mẫu**
   ```python
   # Anti-aliasing filter trước khi downsample
   def safe_downsample(img, scale_factor):
       # Gaussian blur để loại bỏ high-frequency
       kernel_size = int(2 * scale_factor + 1)
       blurred = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

       # Sau đó mới downsample
       new_size = (img.shape[1] // scale_factor, img.shape[0] // scale_factor)
       downsampled = cv2.resize(blurred, new_size, cv2.INTER_AREA)
       return downsampled
   ```
   **Lý do**: Tránh aliasing artifacts.

3. **Sử dụng histogram để đánh giá quantization**
   ```python
   def check_quantization_quality(img_original, img_quantized):
       """Kiểm tra chất lượng quantization qua histogram"""
       hist_orig = cv2.calcHist([img_original], [0], None, [256], [0, 256])
       hist_quant = cv2.calcHist([img_quantized], [0], None, [256], [0, 256])

       # Plot
       plt.figure(figsize=(12, 4))
       plt.subplot(121)
       plt.plot(hist_orig)
       plt.title('Original Histogram')

       plt.subplot(122)
       plt.plot(hist_quant)
       plt.title('Quantized Histogram')
       plt.show()
   ```
   **Lý do**: Histogram rời rạc = bị posterization.

4. **Test với gradient images**
   ```python
   # Tạo gradient để test quantization
   gradient = np.tile(np.arange(256, dtype=np.uint8), (256, 1))

   # Quantize
   quantized = quantize(gradient, k=4)

   # Kiểm tra banding (false contour)
   cv2.imshow('Gradient Test', np.hstack([gradient, quantized]))
   ```
   **Lý do**: Gradient rất nhạy với quantization, dễ phát hiện artifacts.

### ❌ Không nên làm

1. **Không downsample trực tiếp mà không anti-aliasing**
   ```python
   # ❌ SAI - Gây aliasing
   small = cv2.resize(large, (small_w, small_h))

   # ✅ ĐÚNG
   blurred = cv2.GaussianBlur(large, (5, 5), 0)
   small = cv2.resize(blurred, (small_w, small_h), cv2.INTER_AREA)
   ```

2. **Không giảm bit-depth bằng phép chia thô**
   ```python
   # ❌ SAI - Mất precision
   reduced = img // 16  # 8-bit -> 4-bit

   # ✅ ĐÚNG - Uniform quantization
   L = 16
   reduced = np.floor(img.astype(np.float32) / 256 * L)
   reduced = (reduced / (L - 1) * 255).astype(np.uint8)
   ```

3. **Không lưu ảnh trung gian ở bit-depth thấp khi xử lý**
   ```python
   # ❌ SAI - Mất thông tin qua các bước
   img = load_8bit()
   img = process_step1(img)  # Vẫn 8-bit
   img = process_step2(img)  # Vẫn 8-bit, lỗi tích lũy

   # ✅ ĐÚNG - Xử lý ở precision cao
   img = load_8bit().astype(np.float32)
   img = process_step1(img)
   img = process_step2(img)
   final = np.clip(img, 0, 255).astype(np.uint8)  # Chỉ convert cuối cùng
   ```

4. **Không bỏ qua kích thước file thực tế**
   ```python
   # ❌ SAI - Tính toán lý thuyết
   size_theory = H * W * k / 8  # bytes

   # ✅ ĐÚNG - Xét compression
   # PNG: Lossless, ~50-80% of raw
   # JPEG: Lossy, ~5-20% of raw (quality dependent)
   # WebP: ~30% better than JPEG
   ```

### 💡 Tips

1. **Kiểm tra nhanh chất lượng quantization**
   ```python
   def quick_quality_check(original, processed):
       psnr = cv2.PSNR(original, processed)
       print(f"PSNR: {psnr:.2f} dB")

       if psnr > 40:
           print("✓ Excellent quality")
       elif psnr > 30:
           print("✓ Good quality")
       elif psnr > 20:
           print("⚠ Fair quality")
       else:
           print("✗ Poor quality")
   ```

2. **Rule of thumb cho storage**
   ```
   - 1 Megapixel (1000×1000):
     - RAW 8-bit: ~1 MB
     - PNG: 0.5-0.8 MB
     - JPEG quality=90: 0.1-0.2 MB
     - JPEG quality=50: 0.05-0.1 MB
   ```

3. **Chọn format file phù hợp**
   ```
   - Photography editing: RAW, TIFF (16-bit)
   - Web display: JPEG, WebP (8-bit)
   - Screenshots: PNG (8-bit, lossless)
   - Medical: DICOM (12-16 bit)
   - Scientific: TIFF, HDF5 (16-bit+)
   ```

## 9. Common Pitfalls

### Lỗi 1: Undersampling - Mất chi tiết quan trọng
**Vấn đề**:
```python
# Người dùng muốn resize ảnh 4K xuống 480p
img_4k = cv2.imread('photo_4k.jpg')  # 3840×2160
img_480p = cv2.resize(img_4k, (640, 480))  # Quá nhỏ!
```

**Nguyên nhân**: Giảm quá nhiều một lúc (6× cả chiều dài lẫn chiều rộng), vi phạm Nyquist.

**Giải pháp**:
```python
# Downsample từng bước
def progressive_downsample(img, target_size, steps=3):
    current = img.copy()
    current_size = img.shape[:2][::-1]  # (W, H)

    # Tính intermediate sizes
    sizes = []
    for i in range(steps):
        ratio = ((i + 1) / steps)
        w = int(current_size[0] * (1 - ratio) + target_size[0] * ratio)
        h = int(current_size[1] * (1 - ratio) + target_size[1] * ratio)
        sizes.append((w, h))

    # Downsample từng bước
    for size in sizes:
        current = cv2.GaussianBlur(current, (5, 5), 0)
        current = cv2.resize(current, size, cv2.INTER_AREA)

    return current

# Sử dụng
img_480p = progressive_downsample(img_4k, (640, 480))
```

### Lỗi 2: Quantization Error tích lũy
**Vấn đề**:
```python
# Pipeline xử lý nhiều bước
img = cv2.imread('photo.jpg')  # uint8

# Mỗi operation tích lũy error
img = cv2.add(img, 10)        # Clipping ở 255
img = cv2.multiply(img, 1.1)  # Rounding error
img = cv2.subtract(img, 5)    # Clipping ở 0
# Kết quả: Mất nhiều thông tin!
```

**Nguyên nhân**: uint8 chỉ có 256 levels, mỗi operation làm tròn.

**Giải pháp**:
```python
# Xử lý ở float, convert về uint8 cuối cùng
img = cv2.imread('photo.jpg').astype(np.float32)

img = img + 10
img = img * 1.1
img = img - 5

# Chỉ convert 1 lần
img = np.clip(img, 0, 255).astype(np.uint8)
```

### Lỗi 3: Bỏ qua Gamma correction khi resize
**Vấn đề**:
```python
# Resize ảnh trực tiếp
resized = cv2.resize(img, new_size)  # Kết quả hơi tối/sáng
```

**Nguyên nhân**: Pixel values không linear với brightness (gamma encoding).

**Giải pháp**:
```python
def resize_gamma_correct(img, new_size, gamma=2.2):
    """Resize with proper gamma correction"""
    # Convert to linear space
    img_linear = (img / 255.0) ** gamma

    # Resize in linear space
    resized_linear = cv2.resize(img_linear, new_size, cv2.INTER_LINEAR)

    # Convert back to gamma space
    resized = (resized_linear ** (1/gamma) * 255).astype(np.uint8)

    return resized

# So sánh
img = cv2.imread('photo.jpg', cv2.IMREAD_GRAYSCALE)
resized_wrong = cv2.resize(img, (400, 400))
resized_correct = resize_gamma_correct(img, (400, 400))

# resized_correct sẽ có brightness chính xác hơn
```

### Lỗi 4: Hiểu nhầm bit-depth với dynamic range
**Vấn đề**:
```python
# Người dùng nghĩ 16-bit luôn tốt hơn 8-bit
img_8bit = cv2.imread('photo.jpg')  # Range [0, 255]
img_16bit = img_8bit.astype(np.uint16)  # ❌ Vẫn chỉ 256 unique values!
```

**Nguyên nhân**: Chỉ thay đổi data type không tăng thông tin.

**Giải pháp**:
```python
# Để có 16-bit thực, cần capture từ sensor 16-bit
# Hoặc HDR merging
def create_hdr_16bit(images_8bit):
    """Merge multiple exposures thành 16-bit HDR"""
    # Tone mapping, merge exposure bracket
    hdr = cv2.createCalibrateDebevec().process(images_8bit, times, response)
    # Result có dynamic range cao thật sự
    return hdr

# Không thể tạo 16-bit từ 1 ảnh 8-bit!
```

### Lỗi 5: Dùng nhầm interpolation khi resize
**Vấn đề**:
```python
# Downsample bằng INTER_CUBIC
small = cv2.resize(large, (small_w, small_h), cv2.INTER_CUBIC)  # ❌ Aliasing!

# Upsample bằng INTER_AREA
big = cv2.resize(small, (big_w, big_h), cv2.INTER_AREA)  # ❌ Blur!
```

**Nguyên nhân**: Mỗi method có mục đích riêng.

**Giải pháp**:
```python
# Downsample: Dùng INTER_AREA
small = cv2.resize(large, (small_w, small_h), cv2.INTER_AREA)  # ✓

# Upsample: Dùng INTER_CUBIC hoặc INTER_LANCZOS4
big = cv2.resize(small, (big_w, big_h), cv2.INTER_CUBIC)  # ✓
```

## 10. Bài tập Thực hành

### Bài 1: Phân tích Trade-off
**Đề bài**: Cho ảnh 1920×1080, 8-bit. Bạn cần giảm xuống 50% dung lượng. So sánh 2 cách:
- Cách A: Giảm resolution xuống 1360×765 (50% pixels), giữ 8-bit
- Cách B: Giữ resolution, giảm xuống 4-bit

Hỏi: Cách nào tốt hơn cho ảnh chứa văn bản? Cách nào tốt hơn cho ảnh phong cảnh với gradient?

**Gợi ý**:
```python
# Implement và so sánh PSNR, SSIM
# Test với 2 loại ảnh: text.png và landscape.png
# Quan sát artifacts (blocky vs banding)
```

<details>
<summary>Gợi ý chi tiết</summary>

- Văn bản: Cần spatial resolution cao (biên sắc nét) → Chọn **Cách B**
- Phong cảnh: Cần gradient mượt → Chọn **Cách A**
- Code template:
```python
def compare_methods(img, img_type):
    # Method A: Spatial
    # Method B: Quantization
    # Compute PSNR, SSIM
    # Visualize
    pass
```
</details>

### Bài 2: Implement Uniform Quantization
**Đề bài**: Viết hàm `uniform_quantize(img, k)` thực hiện uniform quantization với k bits.

**Yêu cầu**:
- Input: Ảnh grayscale 8-bit, k ∈ [1, 8]
- Output: Ảnh đã quantize về k bits (nhưng vẫn lưu dạng uint8)
- Tính quantization error: MAE, MSE

**Gợi ý**:
```python
def uniform_quantize(img, k):
    """
    Uniform quantization

    Args:
        img: uint8 grayscale image
        k: number of bits (1-8)

    Returns:
        quantized: uint8 image (k-bit quantized)
        error: MAE
    """
    # TODO: Implement
    pass

# Test
img = cv2.imread('test.jpg', cv2.IMREAD_GRAYSCALE)
for k in range(1, 9):
    quantized, error = uniform_quantize(img, k)
    print(f'{k}-bit: MAE = {error:.2f}')
```

<details>
<summary>Skeleton code</summary>

```python
def uniform_quantize(img, k):
    L = 2 ** k

    # Step 1: Normalize to [0, L-1]
    # ...

    # Step 2: Reconstruct to [0, 255]
    # ...

    # Step 3: Calculate error
    error = np.mean(np.abs(img.astype(np.float32) - quantized.astype(np.float32)))

    return quantized, error
```
</details>

### Bài 3: Anti-Aliasing Filter Design
**Đề bài**: Khi downsample ảnh 4×, cần blur bao nhiêu để tránh aliasing?

**Yêu cầu**:
- Thử các kernel size: 3, 5, 7, 9, 11
- Downsample về 1/4 resolution
- Upsample lại về original size (để so sánh)
- Tính PSNR, plot kết quả

**Gợi ý**:
```python
def test_antialiasing(img, downsample_factor=4):
    kernel_sizes = [3, 5, 7, 9, 11]
    results = {}

    for k_size in kernel_sizes:
        # Blur
        blurred = cv2.GaussianBlur(img, (k_size, k_size), 0)

        # Downsample
        # ...

        # Upsample back
        # ...

        # Calculate PSNR
        # ...

    # Plot
    # ...

# Kỳ vọng: kernel_size ≈ 2 × downsample_factor + 1 cho kết quả tốt
```

## 11. Tóm tắt

| Khái niệm | Định nghĩa | Công thức | Ảnh hưởng |
|-----------|-----------|-----------|-----------|
| Sampling | Rời rạc hóa không gian | M × N | Chi tiết hình học |
| Quantization | Rời rạc hóa mức xám | L = 2^k | Gradient, màu sắc |
| Spatial Resolution | Số pixel | M × N | Càng cao càng chi tiết |
| Gray-level Resolution | Số mức xám | 2^k | Càng cao càng mượt |
| File Size | Dung lượng | M×N×k bits | Tăng theo M, N, k |

**Key Takeaways**:
1. **Sampling** ảnh hưởng chi tiết không gian (edges, shapes)
2. **Quantization** ảnh hưởng độ mượt của gradient (false contour)
3. **Nyquist theorem**: Cần lấy mẫu ít nhất 2× tần số cao nhất
4. **8-bit** thường đủ cho mắt người, nhưng processing nên dùng float
5. **Trade-off**: Chất lượng ↔ Dung lượng - chọn theo ứng dụng

## 12. Tài liệu Tham khảo

1. Gonzalez & Woods - "Digital Image Processing" (Chapter 2)
2. Burger & Burge - "Digital Image Processing: An Algorithmic Introduction"
3. OpenCV Documentation
4. IEEE Standards for Image Coding

---

**Lưu ý**: Tài liệu này phục vụ mục đích học tập cho môn Xử lý Ảnh.
