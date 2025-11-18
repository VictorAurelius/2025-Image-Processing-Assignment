# Lý thuyết: Các chỉ số Đánh giá Chất lượng Ảnh (Image Quality Metrics)

## 1. Giới thiệu

Đánh giá chất lượng ảnh cần thiết để:
- So sánh thuật toán xử lý ảnh
- Đánh giá mức độ nén
- Đo lường nhiễu và suy giảm
- Tối ưu hóa parameters

**Phân loại**:
- **Full-reference**: Cần ảnh gốc (reference)
- **Reduced-reference**: Cần một số đặc trưng từ ảnh gốc
- **No-reference**: Không cần ảnh gốc (blind quality assessment)

## 2. MAE (Mean Absolute Error)

### 2.1. Định nghĩa
```
MAE = (1 / MN) × Σᵢ Σⱼ |I(i,j) - K(i,j)|
```

Trong đó:
- I: Ảnh gốc
- K: Ảnh test
- M×N: Kích thước ảnh

### 2.2. Code
```python
def mae(img1, img2):
    return np.mean(np.abs(img1.astype(np.float32) - img2.astype(np.float32)))
```

### 2.3. Đặc điểm

**Ưu điểm**:
- Đơn giản, dễ hiểu
- Đơn vị: giá trị pixel (0-255 cho 8-bit)
- Tuyến tính với sai số

**Nhược điểm**:
- Không nhạy với perceptual quality
- Tất cả pixel có trọng số bằng nhau
- Không xét cấu trúc ảnh

**Giá trị**:
- MAE = 0: Hai ảnh giống hệt
- MAE < 5: Rất tốt
- MAE < 10: Tốt
- MAE > 20: Kém

## 3. MSE (Mean Squared Error)

### 3.1. Định nghĩa
```
MSE = (1 / MN) × Σᵢ Σⱼ (I(i,j) - K(i,j))²
```

### 3.2. Code
```python
def mse(img1, img2):
    return np.mean((img1.astype(np.float32) - img2.astype(np.float32))**2)
```

### 3.3. Đặc điểm

**Ưu điểm**:
- Cơ sở toán học mạnh
- Differentiable (dùng cho optimization)
- Phạt nặng outliers (do bình phương)

**Nhược điểm**:
- Đơn vị: pixel² (khó interpret)
- Rất nhạy với outliers
- Không tương quan tốt với human perception

**So sánh MAE vs MSE**:
- MSE phạt nặng sai số lớn hơn MAE
- MAE robust hơn với noise/outliers
- MSE dễ tính đạo hàm hơn (gradient descent)

## 4. PSNR (Peak Signal-to-Noise Ratio)

### 4.1. Định nghĩa
```
PSNR = 10 × log₁₀(MAX² / MSE)
     = 20 × log₁₀(MAX) - 10 × log₁₀(MSE)
```

Với MAX = 255 cho ảnh 8-bit:
```
PSNR = 20 × log₁₀(255) - 10 × log₁₀(MSE)
     ≈ 48.13 - 10 × log₁₀(MSE)
```

### 4.2. Code
```python
def psnr(img1, img2, max_val=255):
    mse_val = mse(img1, img2)
    if mse_val == 0:
        return float('inf')
    return 20 * np.log10(max_val) - 10 * np.log10(mse_val)
```

### 4.3. Đặc điểm

**Ưu điểm**:
- Đơn vị: dB (decibel) - dễ so sánh
- Phổ biến, tiêu chuẩn trong nghiên cứu
- Logarithmic scale

**Nhược điểm**:
- Dựa trên MSE → không tương quan tốt với human perception
- Không xét cấu trúc
- Có thể misleading với texture/pattern

**Giá trị**:
- PSNR > 40 dB: Xuất sắc (gần như không nhận biết được)
- PSNR 30-40 dB: Tốt
- PSNR 20-30 dB: Chấp nhận được
- PSNR < 20 dB: Kém

### 4.4. Ví dụ
```
MSE = 100 → PSNR = 28.13 dB (tốt)
MSE = 10  → PSNR = 38.13 dB (rất tốt)
MSE = 1   → PSNR = 48.13 dB (xuất sắc)
```

## 5. SSIM (Structural Similarity Index)

### 5.1. Định nghĩa
SSIM đo sự giống nhau về cấu trúc giữa 2 ảnh:

```
SSIM(x, y) = [l(x,y)]^α × [c(x,y)]^β × [s(x,y)]^γ
```

Với α = β = γ = 1:
```
SSIM(x, y) = l(x,y) × c(x,y) × s(x,y)
```

**Ba thành phần**:

**1. Luminance** (độ sáng):
```
l(x, y) = (2μₓμᵧ + C₁) / (μₓ² + μᵧ² + C₁)
```

**2. Contrast** (độ tương phản):
```
c(x, y) = (2σₓσᵧ + C₂) / (σₓ² + σᵧ² + C₂)
```

**3. Structure** (cấu trúc):
```
s(x, y) = (σₓᵧ + C₃) / (σₓσᵧ + C₃)
```

**Form đơn giản**:
```
SSIM(x, y) = [(2μₓμᵧ + C₁)(2σₓᵧ + C₂)] / [(μₓ² + μᵧ² + C₁)(σₓ² + σᵧ² + C₂)]
```

Với:
- μ: mean
- σ: standard deviation
- σₓᵧ: covariance
- C₁, C₂: constants để tránh chia cho 0

### 5.2. Code
```python
from skimage.metrics import structural_similarity as ssim

ssim_value = ssim(img1, img2, data_range=255)
```

Hoặc custom:
```python
def ssim_simple(img1, img2):
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2

    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)

    mu1 = img1.mean()
    mu2 = img2.mean()

    sigma1_sq = np.var(img1)
    sigma2_sq = np.var(img2)
    sigma12 = np.cov(img1.flat, img2.flat)[0,1]

    ssim = ((2*mu1*mu2 + C1) * (2*sigma12 + C2)) / \
           ((mu1**2 + mu2**2 + C1) * (sigma1_sq + sigma2_sq + C2))

    return ssim
```

### 5.3. Đặc điểm

**Ưu điểm**:
- **Perceptually meaningful**: Tương quan tốt với human perception
- Xét cấu trúc, không chỉ pixel-wise error
- Symmetric: SSIM(x,y) = SSIM(y,x)
- Bounded: SSIM ∈ [-1, 1], thường [0, 1]

**Nhược điểm**:
- Phức tạp hơn MSE/PSNR
- Chậm hơn (cần tính covariance)
- Cần chọn window size

**Giá trị**:
- SSIM = 1: Hai ảnh giống hệt
- SSIM > 0.95: Rất tốt (khó nhận biết)
- SSIM > 0.90: Tốt
- SSIM > 0.80: Chấp nhận được
- SSIM < 0.80: Kém

### 5.4. Local SSIM
SSIM thường tính local (sliding window):
```python
# Window size 11×11 là standard
ssim_map = ssim(img1, img2, win_size=11, full=True)
mean_ssim = ssim_map.mean()
```

## 6. NCC (Normalized Cross-Correlation)

### 6.1. Định nghĩa
```
NCC = Σᵢ Σⱼ [I(i,j) - μᵢ][K(i,j) - μₖ] / (σᵢ × σₖ × MN)
```

Hoặc:
```
NCC = cov(I, K) / (σᵢ × σₖ)
```

### 6.2. Code
```python
def ncc(img1, img2):
    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)

    # Normalize
    img1 = (img1 - img1.mean()) / (img1.std() + 1e-6)
    img2 = (img2 - img2.mean()) / (img2.std() + 1e-6)

    return np.mean(img1 * img2)
```

### 6.3. Đặc điểm

**Ưu điểm**:
- Bất biến với linear brightness/contrast changes
- Đo correlation, không phải difference
- Giá trị [-1, 1]

**Nhược điểm**:
- Không phổ biến như SSIM
- Không xét structure explicitly

**Giá trị**:
- NCC = 1: Perfect positive correlation
- NCC = 0: No correlation
- NCC = -1: Perfect negative correlation

## 7. So sánh các Metrics

### 7.1. Bảng so sánh

| Metric | Range | Unit | Perceptual | Complexity | Speed |
|--------|-------|------|------------|------------|-------|
| MAE | [0, 255] | pixel | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| MSE | [0, 65025] | pixel² | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| PSNR | [0, ∞] dB | dB | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| SSIM | [-1, 1] | unitless | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| NCC | [-1, 1] | unitless | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

### 7.2. Correlation với Human Perception

**Từ tốt → kém**:
```
SSIM > MS-SSIM > FSIM > PSNR > MSE > MAE
```

### 7.3. Use Cases

**MAE/MSE**:
- Quick comparison
- Optimization (gradient descent)
- Not for perceptual quality

**PSNR**:
- Academic papers (standard)
- Quick benchmark
- Compression evaluation

**SSIM**:
- Perceptual quality assessment
- Image processing algorithm comparison
- Preferred over PSNR

**NCC**:
- Template matching
- Registration
- When brightness/contrast varies

## 8. Ví dụ So sánh

### 8.1. Gaussian Noise
```
Original vs Gaussian(σ=15):
MAE  ≈ 12
MSE  ≈ 225
PSNR ≈ 24.6 dB
SSIM ≈ 0.85
```

### 8.2. JPEG Compression
```
Original vs JPEG(quality=30):
MAE  ≈ 8
MSE  ≈ 100
PSNR ≈ 28.1 dB
SSIM ≈ 0.90
```

**Observation**: SSIM cao hơn expected vì JPEG giữ structure tốt dù có artifacts.

### 8.3. Salt & Pepper Noise
```
Original vs Salt&Pepper(5%):
MAE  ≈ 13
MSE  ≈ 650  (outliers!)
PSNR ≈ 20.0 dB (thấp vì MSE cao)
SSIM ≈ 0.92 (cao vì structure còn)
```

**Observation**: PSNR misleading, SSIM phản ánh tốt hơn.

## 9. Best Practices

### 9.1. Chọn metric
```
Task: General quality → SSIM
Task: Optimization → MSE/PSNR
Task: Quick check → PSNR
Task: Academic paper → PSNR + SSIM
Task: Perceptual → SSIM only
```

### 9.2. Reporting
Luôn report cả PSNR và SSIM:
```
Method A: PSNR=30.5 dB, SSIM=0.92
Method B: PSNR=29.8 dB, SSIM=0.94
→ Method B better (SSIM higher, perceptual)
```

### 9.3. Multiple metrics
```python
def evaluate_quality(img_ref, img_test):
    return {
        'mae': mae(img_ref, img_test),
        'mse': mse(img_ref, img_test),
        'psnr': psnr(img_ref, img_test),
        'ssim': ssim(img_ref, img_test, data_range=255),
        'ncc': ncc(img_ref, img_test)
    }
```

## 10. Advanced Metrics

### 10.1. MS-SSIM (Multi-Scale SSIM)
Tính SSIM ở nhiều scales (resolutions):
- Better than SSIM
- More computationally expensive

### 10.2. FSIM (Feature Similarity Index)
Dựa trên phase congruency và gradient magnitude:
- Very good perceptual correlation
- Complex to compute

### 10.3. VIF (Visual Information Fidelity)
Based on natural scene statistics

### 10.4. LPIPS (Learned Perceptual Image Patch Similarity)
Sử dụng deep learning:
- State-of-the-art perceptual metric
- Requires pre-trained network

## 11. Limitations

### 11.1. All metrics có hạn chế
- No single metric perfect
- Context matters
- Human subjective test still gold standard

### 11.2. Misleading cases
```
Case 1: Shift by 1 pixel
  → MSE high, but perceptually similar

Case 2: Brightness change
  → MSE high, but structure same

Case 3: JPEG artifacts
  → PSNR ok, but visible blocking
```

## 12. Code Examples Chi Tiết

### 12.1. Implementation đầy đủ các metrics
```python
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
import matplotlib.pyplot as plt

def mae(img1, img2):
    """Mean Absolute Error"""
    return np.mean(np.abs(img1.astype(np.float32) - img2.astype(np.float32)))

def mse(img1, img2):
    """Mean Squared Error"""
    return np.mean((img1.astype(np.float32) - img2.astype(np.float32))**2)

def psnr_custom(img1, img2, max_val=255):
    """Peak Signal-to-Noise Ratio"""
    mse_val = mse(img1, img2)
    if mse_val == 0:
        return float('inf')
    return 20 * np.log10(max_val) - 10 * np.log10(mse_val)

def ncc(img1, img2):
    """Normalized Cross-Correlation"""
    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)

    # Normalize (zero mean, unit variance)
    img1_norm = (img1 - img1.mean()) / (img1.std() + 1e-6)
    img2_norm = (img2 - img2.mean()) / (img2.std() + 1e-6)

    return np.mean(img1_norm * img2_norm)

def comprehensive_evaluation(img_original, img_degraded):
    """Đánh giá đầy đủ chất lượng ảnh"""

    # Ensure same size and type
    assert img_original.shape == img_degraded.shape, "Images must have same shape"

    # Compute all metrics
    results = {
        'MAE': mae(img_original, img_degraded),
        'MSE': mse(img_original, img_degraded),
        'PSNR': psnr(img_original, img_degraded, data_range=255),
        'SSIM': ssim(img_original, img_degraded, data_range=255),
        'NCC': ncc(img_original, img_degraded)
    }

    # Print results
    print("=" * 50)
    print("Image Quality Metrics:")
    print("=" * 50)
    print(f"  MAE:  {results['MAE']:.2f} (lower is better)")
    print(f"  MSE:  {results['MSE']:.2f} (lower is better)")
    print(f"  PSNR: {results['PSNR']:.2f} dB (higher is better)")
    print(f"  SSIM: {results['SSIM']:.4f} (higher is better, max=1.0)")
    print(f"  NCC:  {results['NCC']:.4f} (higher is better, max=1.0)")

    # Interpret SSIM
    if results['SSIM'] > 0.95:
        quality = "Excellent"
    elif results['SSIM'] > 0.90:
        quality = "Good"
    elif results['SSIM'] > 0.80:
        quality = "Fair"
    else:
        quality = "Poor"

    print(f"\nOverall Quality (SSIM-based): {quality}")
    print("=" * 50)

    return results

# Example usage
if __name__ == "__main__":
    # Load images
    img_orig = cv2.imread('original.png', cv2.IMREAD_GRAYSCALE)
    img_degraded = cv2.imread('degraded.png', cv2.IMREAD_GRAYSCALE)

    # Evaluate
    results = comprehensive_evaluation(img_orig, img_degraded)
```

### 12.2. Comparing multiple degraded versions
```python
def compare_multiple_versions(original, versions_dict):
    """
    So sánh nhiều phiên bản của ảnh

    Args:
        original: ảnh gốc
        versions_dict: dict {name: degraded_image}

    Returns:
        DataFrame với kết quả
    """
    import pandas as pd

    results = []
    for name, img_deg in versions_dict.items():
        metrics = {
            'Version': name,
            'MAE': mae(original, img_deg),
            'MSE': mse(original, img_deg),
            'PSNR': psnr(original, img_deg, data_range=255),
            'SSIM': ssim(original, img_deg, data_range=255),
            'NCC': ncc(original, img_deg)
        }
        results.append(metrics)

    df = pd.DataFrame(results)

    # Sort by SSIM (best first)
    df = df.sort_values('SSIM', ascending=False)

    print("\nComparison Results:")
    print(df.to_string(index=False))

    return df

# Example
original = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)

versions = {
    'JPEG Q=90': cv2.imread('lena_jpeg90.jpg', cv2.IMREAD_GRAYSCALE),
    'JPEG Q=50': cv2.imread('lena_jpeg50.jpg', cv2.IMREAD_GRAYSCALE),
    'JPEG Q=10': cv2.imread('lena_jpeg10.jpg', cv2.IMREAD_GRAYSCALE),
    'Gaussian Blur': cv2.GaussianBlur(original, (5, 5), 0),
    'Resize 50%': cv2.resize(cv2.resize(original, (256, 256)), (512, 512))
}

df = compare_multiple_versions(original, versions)
```

**Output mẫu**:
```
Comparison Results:
     Version    MAE     MSE   PSNR   SSIM    NCC
  JPEG Q=90   2.34   12.45  37.18  0.985  0.992
Gaussian Blur 3.12   18.23  35.52  0.972  0.988
  Resize 50%  5.67   45.89  31.51  0.945  0.971
  JPEG Q=50   8.91  102.34  28.03  0.912  0.945
  JPEG Q=10  23.45  789.12  19.16  0.687  0.812
```

### 12.3. Visualizing SSIM map
```python
def visualize_ssim_map(img1, img2):
    """Hiển thị SSIM map để thấy vùng nào bị degraded nhiều"""

    # Compute SSIM with full map
    ssim_score, ssim_map = ssim(img1, img2, data_range=255, full=True)

    # Normalize SSIM map to [0, 255] for display
    ssim_map_display = ((ssim_map + 1) / 2 * 255).astype(np.uint8)

    # Create difference map
    diff = cv2.absdiff(img1, img2)

    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))

    axes[0, 0].imshow(img1, cmap='gray')
    axes[0, 0].set_title('Original')
    axes[0, 0].axis('off')

    axes[0, 1].imshow(img2, cmap='gray')
    axes[0, 1].set_title('Degraded')
    axes[0, 1].axis('off')

    axes[1, 0].imshow(ssim_map_display, cmap='jet')
    axes[1, 0].set_title(f'SSIM Map (Overall: {ssim_score:.4f})\nRed = Poor, Blue = Good')
    axes[1, 0].axis('off')

    axes[1, 1].imshow(diff, cmap='hot')
    axes[1, 1].set_title('Absolute Difference\nBright = High error')
    axes[1, 1].axis('off')

    plt.tight_layout()
    plt.savefig('ssim_analysis.png', dpi=150)
    print(f"SSIM Score: {ssim_score:.4f}")
    print("Saved: ssim_analysis.png")

# Example
img_orig = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)
img_jpeg = cv2.imread('lena_compressed.jpg', cv2.IMREAD_GRAYSCALE)
visualize_ssim_map(img_orig, img_jpeg)
```

### 12.4. Testing different noise types
```python
def test_metrics_with_noise(img, noise_type='gaussian', noise_level=25):
    """
    Test các metrics với different noise types

    noise_type: 'gaussian', 'salt_pepper', 'speckle'
    noise_level: sigma cho gaussian, percentage cho salt&pepper
    """
    H, W = img.shape

    if noise_type == 'gaussian':
        # Gaussian noise
        noise = np.random.normal(0, noise_level, (H, W))
        noisy = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)

    elif noise_type == 'salt_pepper':
        # Salt & Pepper noise
        noisy = img.copy()
        num_salt = int((noise_level / 100) * img.size / 2)
        coords = [np.random.randint(0, i-1, num_salt) for i in img.shape]
        noisy[coords[0], coords[1]] = 255  # Salt
        num_pepper = num_salt
        coords = [np.random.randint(0, i-1, num_pepper) for i in img.shape]
        noisy[coords[0], coords[1]] = 0  # Pepper

    elif noise_type == 'speckle':
        # Speckle noise
        noise = np.random.randn(H, W)
        noisy = img + img * noise * (noise_level / 100)
        noisy = np.clip(noisy, 0, 255).astype(np.uint8)

    # Compute metrics
    results = {
        'Noise Type': noise_type,
        'Noise Level': noise_level,
        'MAE': mae(img, noisy),
        'MSE': mse(img, noisy),
        'PSNR': psnr(img, noisy, data_range=255),
        'SSIM': ssim(img, noisy, data_range=255)
    }

    print(f"\n{noise_type.upper()} Noise (level={noise_level}):")
    for k, v in results.items():
        if isinstance(v, float):
            print(f"  {k}: {v:.2f}")
        else:
            print(f"  {k}: {v}")

    return noisy, results

# Test
img = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)

noisy_gaussian, _ = test_metrics_with_noise(img, 'gaussian', 15)
noisy_sp, _ = test_metrics_with_noise(img, 'salt_pepper', 5)
noisy_speckle, _ = test_metrics_with_noise(img, 'speckle', 10)
```

**Observation**: SSIM cao hơn với salt&pepper vì structure vẫn còn, dù MSE cao.

## 13. Best Practices

### ✅ Nên làm

1. **Luôn report cả PSNR và SSIM**
   ```python
   def report_quality(img_ref, img_test, method_name=""):
       """Report both PSNR and SSIM for complete assessment"""
       psnr_val = psnr(img_ref, img_test, data_range=255)
       ssim_val = ssim(img_ref, img_test, data_range=255)

       print(f"{method_name}:")
       print(f"  PSNR: {psnr_val:.2f} dB")
       print(f"  SSIM: {ssim_val:.4f}")

       return {'psnr': psnr_val, 'ssim': ssim_val}

   # Example
   report_quality(original, compressed, "JPEG Compression Q=80")
   ```
   **Lý do**: PSNR là standard, SSIM phản ánh perceptual quality tốt hơn.

2. **Normalize images trước khi tính metrics**
   ```python
   def safe_compute_metrics(img1, img2):
       """Ensure images are properly normalized"""
       # Convert to same dtype
       img1 = img1.astype(np.float32)
       img2 = img2.astype(np.float32)

       # Check range
       if img1.max() <= 1.0:
           data_range = 1.0
       else:
           data_range = 255.0

       psnr_val = psnr(img1, img2, data_range=data_range)
       ssim_val = ssim(img1, img2, data_range=data_range)

       return psnr_val, ssim_val
   ```
   **Lý do**: Tránh lỗi do khác data range ([0,1] vs [0,255]).

3. **Sử dụng SSIM map để debug**
   ```python
   # Khi SSIM thấp, dùng map để tìm vùng bị degraded
   ssim_score, ssim_map = ssim(img1, img2, full=True, data_range=255)

   # Tìm vùng có SSIM thấp nhất
   min_ssim_regions = ssim_map < 0.7

   # Visualize
   plt.imshow(min_ssim_regions, cmap='hot')
   plt.title('Degraded Regions (SSIM < 0.7)')
   ```
   **Lý do**: Giúp hiểu degradation ở đâu, không chỉ overall score.

4. **Chọn metric phù hợp với task**
   ```python
   # Compression evaluation
   metrics_compression = ['PSNR', 'SSIM', 'file_size']

   # Denoising evaluation
   metrics_denoising = ['PSNR', 'SSIM', 'edge_preservation']

   # Super-resolution evaluation
   metrics_sr = ['PSNR', 'SSIM', 'LPIPS', 'perceptual_loss']
   ```
   **Lý do**: Mỗi task có metrics phù hợp riêng.

### ❌ Không nên làm

1. **Không chỉ dựa vào PSNR**
   ```python
   # ❌ SAI - Chỉ xem PSNR
   if psnr(img1, img2) > 30:
       print("Good quality")

   # ✅ ĐÚNG - Xem cả SSIM
   psnr_val = psnr(img1, img2, data_range=255)
   ssim_val = ssim(img1, img2, data_range=255)

   if psnr_val > 30 and ssim_val > 0.9:
       print("Good quality")
   ```
   **Lý do**: PSNR có thể misleading (e.g., blur có PSNR cao nhưng trông xấu).

2. **Không so sánh ảnh khác kích thước**
   ```python
   # ❌ SAI - Không check size
   psnr_val = psnr(img1, img2)  # Error nếu khác size!

   # ✅ ĐÚNG - Check và resize nếu cần
   def safe_psnr(img1, img2):
       if img1.shape != img2.shape:
           print(f"Warning: Resizing img2 from {img2.shape} to {img1.shape}")
           img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

       return psnr(img1, img2, data_range=255)
   ```

3. **Không quên data_range parameter**
   ```python
   # ❌ SAI - Quên data_range
   ssim_val = ssim(img1, img2)  # Mặc định data_range=255, có thể sai nếu ảnh [0,1]

   # ✅ ĐÚNG
   if img1.max() <= 1.0:
       ssim_val = ssim(img1, img2, data_range=1.0)
   else:
       ssim_val = ssim(img1, img2, data_range=255)
   ```

4. **Không dùng MSE/MAE làm perceptual metric**
   ```python
   # ❌ SAI - Dùng MSE để đánh giá user perception
   if mse(img1, img2) < 100:
       print("Looks good to user")  # Không chính xác!

   # ✅ ĐÚNG - Dùng SSIM
   if ssim(img1, img2, data_range=255) > 0.9:
       print("Looks good to user")  # Chính xác hơn
   ```

### 💡 Tips

1. **PSNR threshold rules of thumb**
   ```
   PSNR > 40 dB: Imperceptible (không thấy khác biệt)
   PSNR 30-40 dB: Perceptible but acceptable (thấy nhưng chấp nhận được)
   PSNR 20-30 dB: Noticeable degradation (degradation rõ ràng)
   PSNR < 20 dB: Poor quality (chất lượng kém)
   ```

2. **SSIM interpretation**
   ```
   SSIM > 0.99: Visually identical (hầu như giống hệt)
   SSIM > 0.95: Excellent (xuất sắc)
   SSIM > 0.90: Good (tốt)
   SSIM > 0.80: Acceptable (chấp nhận được)
   SSIM < 0.80: Poor (kém)
   ```

3. **Quick metric selection**
   ```python
   def suggest_metric(task):
       suggestions = {
           'compression': ['PSNR', 'SSIM', 'MS-SSIM'],
           'denoising': ['PSNR', 'SSIM'],
           'super_resolution': ['PSNR', 'SSIM', 'LPIPS'],
           'style_transfer': ['LPIPS', 'perceptual_loss'],
           'deblurring': ['PSNR', 'SSIM', 'sharpness'],
           'inpainting': ['SSIM', 'LPIPS'],
           'enhancement': ['SSIM', 'NIQE', 'BRISQUE']  # No-reference
       }
       return suggestions.get(task, ['PSNR', 'SSIM'])

   print(suggest_metric('compression'))  # ['PSNR', 'SSIM', 'MS-SSIM']
   ```

4. **Batch evaluation**
   ```python
   def batch_evaluate(ref_folder, test_folder):
       """Evaluate all images in folders"""
       ref_images = sorted(glob.glob(f"{ref_folder}/*.png"))
       test_images = sorted(glob.glob(f"{test_folder}/*.png"))

       results = []
       for ref_path, test_path in zip(ref_images, test_images):
           img_ref = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
           img_test = cv2.imread(test_path, cv2.IMREAD_GRAYSCALE)

           psnr_val = psnr(img_ref, img_test, data_range=255)
           ssim_val = ssim(img_ref, img_test, data_range=255)

           results.append({
               'image': os.path.basename(ref_path),
               'psnr': psnr_val,
               'ssim': ssim_val
           })

       df = pd.DataFrame(results)
       print(f"\nAverage PSNR: {df['psnr'].mean():.2f} dB")
       print(f"Average SSIM: {df['ssim'].mean():.4f}")

       return df
   ```

## 14. Common Pitfalls

### Lỗi 1: Quên convert color images
**Vấn đề**:
```python
# Load color image
img1 = cv2.imread('photo1.jpg')  # BGR, shape (H, W, 3)
img2 = cv2.imread('photo2.jpg')

# Compute SSIM - LỖI! ssim expects 2D
ssim_val = ssim(img1, img2)  # Error hoặc kết quả sai!
```

**Nguyên nhân**: ssim mặc định cho grayscale (2D). Color cần xử lý riêng.

**Giải pháp**:
```python
# Option 1: Convert to grayscale
img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ssim_val = ssim(img1_gray, img2_gray, data_range=255)

# Option 2: SSIM per channel, then average
ssim_per_channel = []
for i in range(3):
    ssim_c = ssim(img1[:,:,i], img2[:,:,i], data_range=255)
    ssim_per_channel.append(ssim_c)
ssim_val = np.mean(ssim_per_channel)

# Option 3: Use multichannel parameter (scikit-image)
ssim_val = ssim(img1, img2, data_range=255, channel_axis=2)
```

### Lỗi 2: PSNR = inf khi images giống hệt
**Vấn đề**:
```python
img1 = cv2.imread('test.png')
img2 = img1.copy()

psnr_val = psnr(img1, img2)
print(psnr_val)  # inf !
```

**Nguyên nhân**: MSE = 0 → PSNR = log(0) = inf

**Giải pháp**:
```python
def safe_psnr(img1, img2, max_val=255):
    """PSNR with handling for identical images"""
    mse_val = mse(img1, img2)

    if mse_val == 0:
        return float('inf')  # Hoặc return một giá trị lớn như 100

    return 20 * np.log10(max_val) - 10 * np.log10(mse_val)

# Hoặc handle khi report
psnr_val = psnr(img1, img2)
if np.isinf(psnr_val):
    print("PSNR: Perfect (identical images)")
else:
    print(f"PSNR: {psnr_val:.2f} dB")
```

### Lỗi 3: So sánh metrics giữa datasets khác nhau
**Vấn đề**:
```python
# Dataset A: Natural photos
psnr_A = 35.2 dB

# Dataset B: Text/documents
psnr_B = 32.1 dB

# KẾT LUẬN SAI: A tốt hơn B
```

**Nguyên nhân**: Các loại ảnh khác nhau có sensitivity khác nhau với degradation.

**Giải pháp**:
```python
# Chỉ so sánh trong cùng 1 dataset
# Hoặc normalize based on baseline

def normalized_metric(test_psnr, baseline_psnr):
    """Normalize metric relative to baseline"""
    improvement = test_psnr - baseline_psnr
    return improvement

# Dataset A
improvement_A = normalized_metric(35.2, 30.0)  # +5.2 dB

# Dataset B
improvement_B = normalized_metric(32.1, 26.5)  # +5.6 dB

# B actually improved more!
```

### Lỗi 4: Không xem SSIM map khi debug
**Vấn đề**:
```python
ssim_val = ssim(img1, img2, data_range=255)
print(f"SSIM: {ssim_val:.4f}")  # 0.7500

# TẠI SAO thấp? Không biết!
```

**Giải pháp**:
```python
# Always get the map when SSIM is low
ssim_val, ssim_map = ssim(img1, img2, data_range=255, full=True)

print(f"SSIM: {ssim_val:.4f}")

# Visualize map to find problem regions
plt.figure(figsize=(12, 4))

plt.subplot(131)
plt.imshow(img1, cmap='gray')
plt.title('Original')

plt.subplot(132)
plt.imshow(img2, cmap='gray')
plt.title('Degraded')

plt.subplot(133)
plt.imshow(ssim_map, cmap='jet')
plt.title('SSIM Map\n(Red=bad, Blue=good)')
plt.colorbar()

plt.tight_layout()
plt.show()

# Bây giờ thấy vùng nào bị degraded!
```

### Lỗi 5: Sử dụng metrics cho wrong purpose
**Vấn đề**:
```python
# Dùng PSNR để optimize perceptual quality
loss = mse_loss(output, target)  # MSE → PSNR
# Kết quả: Blur nhưng PSNR cao!
```

**Nguyên nhân**: PSNR không tương quan tốt với human perception.

**Giải pháp**:
```python
# Use perceptual loss for perceptual tasks
import lpips

loss_fn = lpips.LPIPS(net='alex')  # Perceptual loss
loss = loss_fn(output, target)

# Hoặc combined loss
loss_total = 0.5 * mse_loss + 0.5 * perceptual_loss
```

## 15. Bài tập Thực hành

### Bài 1: Implement và Compare Metrics
**Đề bài**: Implement 4 metrics (MAE, MSE, PSNR, SSIM) từ scratch và so sánh với scikit-image.

**Yêu cầu**:
- Tự implement công thức
- So sánh kết quả với library functions
- Test với 3 loại degradation: Gaussian blur, JPEG compression, Gaussian noise

**Gợi ý**:
```python
class ImageQualityMetrics:
    def __init__(self):
        pass

    def mae(self, img1, img2):
        # TODO: Implement
        pass

    def mse(self, img1, img2):
        # TODO: Implement
        pass

    def psnr(self, img1, img2, max_val=255):
        # TODO: Use self.mse()
        pass

    def ssim_simple(self, img1, img2):
        # TODO: Implement simplified SSIM (without sliding window)
        # Hint: Compute on whole image
        pass

# Test
metrics = ImageQualityMetrics()
img1 = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.GaussianBlur(img1, (5, 5), 0)

print("Custom implementations:")
print(f"MAE:  {metrics.mae(img1, img2):.2f}")
print(f"MSE:  {metrics.mse(img1, img2):.2f}")
print(f"PSNR: {metrics.psnr(img1, img2):.2f} dB")

print("\nLibrary functions:")
from skimage.metrics import mean_squared_error
print(f"MSE:  {mean_squared_error(img1, img2):.2f}")
```

<details>
<summary>Gợi ý implementation MAE</summary>

```python
def mae(self, img1, img2):
    return np.mean(np.abs(img1.astype(np.float32) - img2.astype(np.float32)))
```
</details>

### Bài 2: SSIM vs PSNR Disagreement
**Đề bài**: Tìm trường hợp PSNR cao nhưng SSIM thấp (và ngược lại).

**Yêu cầu**:
- Tạo 2 degraded versions từ 1 ảnh gốc:
  - Version A: PSNR cao, SSIM thấp hơn
  - Version B: SSIM cao, PSNR thấp hơn
- Giải thích tại sao

**Gợi ý**:
```python
img = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)

# Hint:
# - Gaussian blur: High PSNR, moderate SSIM (pixel values similar, structure blurred)
# - Salt&Pepper noise: Low PSNR (outliers), moderate SSIM (structure preserved)

# TODO: Create version_A and version_B
# TODO: Compute and compare metrics
# TODO: Visualize
```

<details>
<summary>Gợi ý chi tiết</summary>

- **High PSNR, Low SSIM**: Blur (pixel values còn gần, nhưng cấu trúc mất)
- **Low PSNR, High SSIM**: Salt & Pepper noise (outliers làm MSE cao, nhưng structure còn)
</details>

### Bài 3: Metric-based Algorithm Selection
**Đề bài**: Cho 3 denoising algorithms, chọn best dựa trên metrics.

**Yêu cầu**:
- Add Gaussian noise (σ=25) vào ảnh
- Denoise bằng 3 methods:
  1. Gaussian blur (5×5)
  2. Median filter (5×5)
  3. Bilateral filter
- Tính PSNR, SSIM cho mỗi method
- Chọn best method
- Visualize kết quả

**Gợi ý**:
```python
import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

# Load và add noise
img_clean = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)
noise = np.random.normal(0, 25, img_clean.shape)
img_noisy = np.clip(img_clean + noise, 0, 255).astype(np.uint8)

# Denoise methods
denoised_gaussian = cv2.GaussianBlur(img_noisy, (5, 5), 0)
denoised_median = cv2.medianBlur(img_noisy, 5)
denoised_bilateral = cv2.bilateralFilter(img_noisy, 9, 75, 75)

# TODO: Compute PSNR, SSIM for each
# TODO: Rank methods
# TODO: Visualize

# Expected: Bilateral should win on SSIM (preserves edges)
```

## 16. Tóm tắt

**Key Takeaways**:
1. **SSIM is king** for perceptual quality
2. **PSNR for standard** comparison (but not perfect)
3. **Use multiple metrics** for comprehensive evaluation
4. **MSE/MAE for optimization**, not final assessment
5. **Context matters**: Choose metric based on application

**Quick Reference**:
```
Best perceptual:     SSIM > PSNR
Fastest:             MAE ≈ MSE ≈ PSNR
Standard in papers:  PSNR + SSIM
For optimization:    MSE
```

---

**References**:
- Wang et al. - "Image Quality Assessment: From Error Visibility to Structural Similarity" (2004)
- Gonzalez & Woods - Digital Image Processing
- Scikit-image Documentation
