# Hướng Dẫn Đọc Code: Bài 2 - Otsu Thresholding

## Tổng Quan
Bài 2 sử dụng **Otsu thresholding** để tự động tìm ngưỡng tối ưu và đếm số linh kiện điện tử trên nền phẳng.

## Input/Output
**Input:** Ảnh `../input/parts.jpg` (hoặc tạo mẫu)
**Output:** Ảnh phân vùng, histogram, số linh kiện phát hiện

## Thuật Toán Chính

### 1. `create_sample_image()` (dòng 20-39)
Tạo ảnh 400×600 với 11 linh kiện màu tối trên nền trắng.

### 2. `count_components()` (dòng 42-51)
```python
contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
```
Đếm linh kiện bằng cách tìm contours và lọc theo diện tích.

### 3. `main()` - Pipeline (dòng 54-165)
1. **Đọc ảnh** (dòng 56-66)
2. **Otsu thresholding** (dòng 76): `cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)`
3. **Đảo màu nếu cần** (dòng 79-80)
4. **Đếm linh kiện** (dòng 85-86)
5. **Vẽ bounding boxes** (dòng 89-92)
6. **So sánh với ngưỡng thủ công** (dòng 103-109)

## Code Quan Trọng

### 1. Otsu Auto-Threshold (dòng 76)
```python
T, binimg = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```
**Giải thích:** `cv2.THRESH_OTSU` tự động tìm T tối ưu bằng cách tối đa hóa between-class variance. Tham số `0` bị ignore khi dùng Otsu.

### 2. Đảo màu nếu cần (dòng 79-80)
```python
if np.mean(binimg) > 127:
    binimg = cv2.bitwise_not(binimg)
```
**Giải thích:** Nếu mean > 127 → hầu hết pixels là trắng → linh kiện bị phân thành trắng → đảo lại.

### 3. Tìm và đếm contours (dòng 85-86, 44-50)
```python
contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
min_area = 100
valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
return len(valid_contours), valid_contours
```
**Giải thích:** 
- `RETR_EXTERNAL`: Chỉ lấy contour ngoài cùng
- `CHAIN_APPROX_SIMPLE`: Nén contour (bỏ điểm thừa)
- Lọc `cv2.contourArea(cnt) > 100` để loại nhiễu

### 4. Vẽ bounding boxes (dòng 89-92)
```python
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(img_result, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

### 5. Histogram với ngưỡng (dòng 125-131)
```python
plt.hist(gray.ravel(), 256, [0, 256], color='steelblue', alpha=0.7)
plt.axvline(x=T, color='red', linestyle='--', linewidth=2, label=f'Otsu T={T:.0f}')
```

## Tham Số Quan Trọng

| Tham số | Vị trí | Giá trị | Ý nghĩa |
|---------|--------|---------|---------|
| `min_area` | Dòng 48 | 100 | Diện tích tối thiểu contour (pixels) |
| `manual_T` | Dòng 103 | 128 | Ngưỡng thủ công để so sánh |

## Kết Quả Mong Đợi
- Ngưỡng Otsu: T ≈ 140-160
- Số linh kiện phát hiện: 11
- So sánh: Otsu tốt hơn manual threshold (128)

## Lỗi Thường Gặp

### 1. Đếm sai số lượng (nhiều hơn hoặc ít hơn)
**Nguyên nhân:** `min_area` không phù hợp
**Fix:** Điều chỉnh `min_area` dựa trên kích thước linh kiện thực tế
```python
# Tính area trung bình của linh kiện mẫu
for cnt in contours:
    area = cv2.contourArea(cnt)
    print(f"Area: {area}")
# Chọn min_area = 30-50% của area nhỏ nhất
```

### 2. Otsu thất bại (ngưỡng không tốt)
**Nguyên nhân:** Histogram không bimodal (không có 2 đỉnh rõ ràng)
**Fix:** Tiền xử lý bằng histogram equalization
```python
gray_eq = cv2.equalizeHist(gray)
T, binimg = cv2.threshold(gray_eq, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

### 3. Linh kiện dính nhau được đếm là 1
**Nguyên nhân:** Contour nối liền
**Fix:** Sử dụng morphology erosion hoặc watershed (Bài 10)

## Mở Rộng

### 1. Multi-Otsu (3 levels)
```python
from skimage.filters import threshold_multiotsu

thresholds = threshold_multiotsu(gray, classes=3)
regions = np.digitize(gray, bins=thresholds)
```

### 2. Adaptive thresholding cho từng vùng
```python
# Nếu ảnh có độ sáng không đều
adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 35, 5)
```

### 3. Phân tích chi tiết mỗi linh kiện
```python
for i, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)
    circularity = 4*np.pi*area / (perimeter**2) if perimeter > 0 else 0
    
    print(f"Linh kiện {i+1}:")
    print(f"  Area: {area:.0f} pixels")
    print(f"  Circularity: {circularity:.2f} (1.0 = perfect circle)")
```

### 4. Vẽ label trên mỗi linh kiện
```python
for i, cnt in enumerate(contours, 1):
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        cv2.putText(img, str(i), (cx-10, cy+5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
```

### 5. Lưu thông tin ra CSV
```python
import pandas as pd

data = []
for i, cnt in enumerate(contours, 1):
    area = cv2.contourArea(cnt)
    x, y, w, h = cv2.boundingRect(cnt)
    data.append({'ID': i, 'Area': area, 'Width': w, 'Height': h, 'X': x, 'Y': y})

df = pd.DataFrame(data)
df.to_csv('output/components.csv', index=False)
print(df)
```

---
**File:** `/code-implement/T79-phan-vung-anh/bai-2-otsu/threshold.py` (166 dòng)
**Lý thuyết:** [01-thresholding-methods.md](../theory/01-thresholding-methods.md)
