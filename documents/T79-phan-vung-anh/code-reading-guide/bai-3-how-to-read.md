# Hướng Dẫn Đọc Code: Bài 3 - Adaptive Thresholding

## Tổng Quan
Phân ngưỡng thích nghi (MEAN/GAUSSIAN) để tách chữ trên hóa đơn có độ sáng không đều.

## Input/Output
**Input:** `../input/receipt.jpg` | **Output:** Ảnh binary với 2 phương pháp adaptive

## Thuật Toán Chính

### 1. `create_sample_receipt()` (dòng 20-50)
Tạo hóa đơn 500×600 với gradient độ sáng không đều.
- Dòng 24-29: Tạo gradient `brightness = 240 - int(y * 0.15) + int(np.sin(x/50) * 20)`
- Dòng 32-48: Vẽ text hóa đơn bằng `cv2.putText()`

### 2. `main()` Pipeline (dòng 53-178)
1. **Adaptive MEAN** (dòng 83-88):
```python
bin_mean = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, block_size, C)
```

2. **Adaptive GAUSSIAN** (dòng 91-96):
```python
bin_gaus = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, block_size, C)
```

3. **So sánh với Otsu** (dòng 99)

## Code Quan Trọng

### Adaptive Threshold (dòng 83-96)
**Công thức MEAN:** `T(x,y) = mean(neighborhood) - C`
**Công thức GAUSSIAN:** `T(x,y) = gaussian_weighted_mean(neighborhood) - C`

**Tham số:**
- `block_size = 35` (phải lẻ): Kích thước vùng láng giềng
- `C = 7`: Hằng số trừ đi từ mean

## Tham Số Quan Trọng

| Tham số | Giá trị | Ý nghĩa | Điều chỉnh |
|---------|---------|---------|------------|
| `block_size` | 35 | Kích thước vùng | ↑ → mượt hơn, ↓ → chi tiết hơn |
| `C` | 7 | Offset | ↑ → ít text, ↓ → nhiều text |

## Kết Quả Mong Đợi
- MEAN: Text rõ nhưng nhiễu
- GAUSSIAN: Text mượt, ít nhiễu hơn
- Otsu: Thất bại với độ sáng không đều

## Lỗi Thường Gặp

### 1. `block_size` phải là số lẻ
```python
# ERROR
cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 34, 7)
# OpenCV error: block_size must be odd

# FIX
block_size = 35  # hoặc bất kỳ số lẻ nào
```

### 2. Text bị mất hoặc quá nhiều nhiễu
**Fix:** Điều chỉnh C
```python
# Nếu text bị mất → giảm C
bin_mean = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 35, 3)

# Nếu nhiễu quá nhiều → tăng C
bin_mean = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 35, 10)
```

### 3. Chậm với ảnh lớn
**Fix:** Giảm resolution hoặc dùng `cv2.pyrDown()`
```python
gray_small = cv2.pyrDown(gray)
bin_small = cv2.adaptiveThreshold(gray_small, 255, ...)
bin_large = cv2.pyrUp(bin_small)
```

## Mở Rộng

### 1. Niblack/Sauvola thresholding
```python
def niblack_threshold(gray, window_size=15, k=0.2):
    mean = cv2.blur(gray, (window_size, window_size))
    mean_sq = cv2.blur(gray**2, (window_size, window_size))
    std = np.sqrt(mean_sq - mean**2)
    threshold = mean + k * std
    return (gray > threshold).astype(np.uint8) * 255
```

### 2. Morphology post-processing
```python
# Loại bỏ điểm nhiễu
kernel = np.ones((2, 2), np.uint8)
clean = cv2.morphologyEx(bin_mean, cv2.MORPH_OPEN, kernel)
```

### 3. Tự động chọn block_size
```python
# Rule of thumb: block_size = 1/10 * min(width, height)
h, w = gray.shape
block_size = max(11, (min(h, w) // 10) | 1)  # Make odd
```

### 4. Kết hợp với denoise
```python
# Denoise trước khi threshold
denoised = cv2.fastNlMeansDenoising(gray, h=10)
bin_mean = cv2.adaptiveThreshold(denoised, 255, ...)
```

### 5. OCR integration
```python
import pytesseract

# Sau khi adaptive threshold
text = pytesseract.image_to_string(bin_gaus, lang='vie')
print(text)
```

---
**File:** `/code-implement/T79-phan-vung-anh/bai-3-adaptive-thresholding/threshold.py` (179 dòng)
**Lý thuyết:** [01-thresholding-methods.md](../theory/01-thresholding-methods.md)
