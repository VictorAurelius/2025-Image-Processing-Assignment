# Hướng Dẫn Đọc Code: Bài 4 - Bayes-ML Thresholding

## Tổng Quan
Phân ngưỡng dựa trên lý thuyết Bayes và Maximum Likelihood cho 2 lớp Gaussian.

## Input/Output
**Input:** Ảnh kim loại bị rỉ sét | **Output:** Mask vùng rỉ sét với ngưỡng Bayes-ML

## Thuật Toán Chính

### `calc_threshold()` (dòng 20-44)
```python
numerator = mu0 * s1**2 - mu1 * s0**2 + s0 * s1 * np.sqrt(
    (mu1 - mu0)**2 + 2 * (s1**2 - s0**2) * np.log((s1 * P0) / (s0 * P1)))
denominator = s1**2 - s0**2
T = numerator / denominator
```
**Giải thích:** Tìm ngưỡng tối ưu khi 2 Gaussian có phương sai khác nhau.

### Tham số ước lượng (dòng 110-115)
- `mu0=120, s0=12`: Nền kim loại
- `mu1=165, s1=15`: Rỉ sét  
- `P0=0.7, P1=0.3`: Prior probability

## Code Quan Trọng

### Vẽ Gaussian curves (dòng 149-151)
```python
gaussian0 = P0 * (1/(s0*np.sqrt(2*np.pi))) * np.exp(-0.5*((x-mu0)/s0)**2)
gaussian1 = P1 * (1/(s1*np.sqrt(2*np.pi))) * np.exp(-0.5*((x-mu1)/s1)**2)
```

## Tham Số

| Tham số | Giá trị | Cách ước lượng |
|---------|---------|----------------|
| μ₀, σ₀ | 120, 12 | Sample pixels từ vùng nền |
| μ₁, σ₁ | 165, 15 | Sample pixels từ vùng rỉ |
| P₀, P₁ | 0.7, 0.3 | Tỷ lệ diện tích |

## Mở Rộng

### Ước lượng tham số từ ảnh
```python
# Select ROI cho nền
roi_bg = gray[10:50, 10:50]
mu0, s0 = np.mean(roi_bg), np.std(roi_bg)

# Select ROI cho rỉ sét
roi_rust = gray[200:250, 400:450]
mu1, s1 = np.mean(roi_rust), np.std(roi_rust)
```

---
**File:** `bai-4-bayes-ml/threshold.py` (222 dòng)
