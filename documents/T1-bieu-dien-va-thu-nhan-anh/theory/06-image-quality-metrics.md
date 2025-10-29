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

## 12. Code Template

```python
def comprehensive_evaluation(img_original, img_degraded):
    """Đánh giá đầy đủ chất lượng ảnh"""

    # Ensure same size and type
    assert img_original.shape == img_degraded.shape

    # Convert to float
    img1 = img_original.astype(np.float32)
    img2 = img_degraded.astype(np.float32)

    # Compute metrics
    results = {
        'MAE': mae(img1, img2),
        'MSE': mse(img1, img2),
        'PSNR': psnr(img1, img2),
        'SSIM': ssim(img_original, img_degraded, data_range=255),
        'NCC': ncc(img1, img2)
    }

    # Print results
    print("Image Quality Metrics:")
    print(f"  MAE:  {results['MAE']:.2f}")
    print(f"  MSE:  {results['MSE']:.2f}")
    print(f"  PSNR: {results['PSNR']:.2f} dB")
    print(f"  SSIM: {results['SSIM']:.4f}")
    print(f"  NCC:  {results['NCC']:.4f}")

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

    return results
```

## 13. Tóm tắt

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
