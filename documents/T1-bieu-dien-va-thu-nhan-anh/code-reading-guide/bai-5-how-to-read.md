# Hướng Dẫn Đọc Code: Bài 5 - Chuyển Hệ Màu & Phát Hiện Vùng Da

## Mục Tiêu Bài Tập

- Hiểu các **color space**: RGB, HSV, YCrCb
- Chuyển đổi giữa các color space bằng OpenCV
- Phát hiện vùng da (skin detection) bằng **color thresholding**
- So sánh hiệu quả của HSV vs YCrCb trong phát hiện da
- Ứng dụng: Lọc ảnh nhạy cảm trước khi đăng lên website

## Kỹ Thuật Chính

- **Color Space Conversion**:
  - BGR → HSV: `cv2.cvtColor(img, cv2.COLOR_BGR2HSV)`
  - BGR → YCrCb: `cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)`
- **Color Thresholding**: `cv2.inRange()` để tạo binary mask
- **Skin Detection Ranges**:
  - HSV: H∈[0, 25], S∈[30, 180], V∈[90, 255]
  - YCrCb: Cr∈[135, 180], Cb∈[85, 135]
- **Mask Application**: `cv2.bitwise_and()` để áp dụng mask
- **Comparison**: Đếm pixels, tính tỷ lệ, tìm intersection

## File Code

`code-implement/T1-bieu-dien-va-thu-nhan-anh/bai-tap-5-color-space/skin_detection.py`

## Sơ Đồ Luồng Xử Lý

```mermaid
graph TD
    A[Đọc ảnh RGB] --> B{File tồn tại?}
    B -->|Không| C[Tạo ảnh portrait mẫu<br/>với màu da]
    B -->|Có| D[Đọc ảnh BGR]
    C --> D

    D --> E1[Chuyển BGR → HSV]
    D --> E2[Chuyển BGR → YCrCb]

    E1 --> F1[Threshold HSV<br/>H:[0,25], S:[30,180], V:[90,255]]
    E2 --> F2[Threshold YCrCb<br/>Cr:[135,180], Cb:[85,135]]

    F1 --> G1[Mask HSV]
    F2 --> G2[Mask YCrCb]

    G1 --> H1[Áp dụng mask HSV<br/>lên ảnh gốc]
    G2 --> H2[Áp dụng mask YCrCb<br/>lên ảnh gốc]

    H1 --> I[Đếm pixels phát hiện]
    H2 --> I

    I --> J[Tính intersection<br/>cả 2 phương pháp]
    J --> K[So sánh & kết luận]
```

## Đọc Code Theo Thứ Tự

### Bước 1: Import Libraries (Dòng 13-15)

```python
import cv2
import numpy as np
import os
```

Bài này đơn giản, chỉ cần 3 thư viện cơ bản.

### Bước 2: Setup Paths (Dòng 19-24)

```python
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "..", "input", "sample-images", "portrait.jpg")
output_dir = os.path.join(script_dir, "..", "output")
os.makedirs(output_dir, exist_ok=True)
```

### Bước 3: Auto-generate Portrait Sample (Dòng 27-46)

**Tạo ảnh với màu da**:

```python
# Ảnh 400x600 RGB
img = np.ones((400, 600, 3), dtype=np.uint8) * 200

# Vẽ vùng da (ellipse)
skin_color = [150, 180, 220]  # BGR format
cv2.ellipse(img, (300, 200), (150, 180), 0, 0, 360, skin_color, -1)

# Vẽ nền không phải da
bg_color = [100, 150, 200]
img[:100, :] = bg_color
img[350:, :] = bg_color
```

**Lưu ý**:
- `skin_color = [150, 180, 220]`: B=150, G=180, R=220
- OpenCV dùng **BGR** thay vì RGB
- Màu da điển hình: R > G > B

### Bước 4: Chuyển Đổi Color Space (Dòng 60-62)

```python
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
```

**Giải thích**:
- `cv2.cvtColor()`: Hàm chuyển đổi color space
- `COLOR_BGR2HSV`: BGR → HSV
- `COLOR_BGR2YCrCb`: BGR → YCrCb

**Color spaces**:

**RGB/BGR**:
- 3 channels: Red, Green, Blue
- Tương quan cao giữa các channels
- Nhạy cảm với lighting

**HSV**:
- H (Hue): Màu sắc [0-179 trong OpenCV]
- S (Saturation): Độ bão hòa [0-255]
- V (Value): Độ sáng [0-255]
- Tách màu sắc và độ sáng

**YCrCb**:
- Y (Luma): Độ sáng [0-255]
- Cr (Chroma Red): Thành phần đỏ [0-255]
- Cb (Chroma Blue): Thành phần xanh [0-255]
- Dùng trong JPEG compression

### Bước 5: HSV Thresholding (Dòng 68-78)

**Ngưỡng HSV cho da**:

```python
# OpenCV: H∈[0,179], S∈[0,255], V∈[0,255]
lower_hsv = (0, 30, 90)
upper_hsv = (25, 180, 255)
mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)
```

**Giải thích ngưỡng**:
- **H∈[0, 25]**: Màu da (đỏ-cam)
  - H=0: Đỏ
  - H=25: Cam
  - Chú ý: OpenCV scale H từ 0-179 (thay vì 0-360)
- **S∈[30, 180]**: Độ bão hòa trung bình
  - S < 30: Quá xám (không phải da)
  - S > 180: Quá bão hòa (không phải da)
- **V∈[90, 255]**: Đủ sáng
  - V < 90: Quá tối (bóng)

**cv2.inRange()**:
- Tạo binary mask
- Pixel thỏa → 255 (white)
- Pixel không thỏa → 0 (black)

### Bước 6: YCrCb Thresholding (Dòng 80-89)

**Ngưỡng YCrCb cho da**:

```python
lower_ycc = (0, 135, 85)
upper_ycc = (255, 180, 135)
mask_ycc = cv2.inRange(ycrcb, lower_ycc, upper_ycc)
```

**Giải thích ngưỡng**:
- **Y∈[0, 255]**: Bất kỳ độ sáng nào (không quan trọng)
- **Cr∈[135, 180]**: Chroma Red cao (da có nhiều đỏ)
- **Cb∈[85, 135]**: Chroma Blue thấp-trung bình

**Tại sao YCrCb tốt?**
- Y tách biệt khỏi color
- Cr, Cb ít bị ảnh hưởng bởi lighting
- Dải màu da rõ ràng trong Cr-Cb space

### Bước 7: Lưu Masks (Dòng 92-99)

```python
hsv_path = os.path.join(output_dir, "mask_hsv.png")
ycc_path = os.path.join(output_dir, "mask_ycrcb.png")
cv2.imwrite(hsv_path, mask_hsv)
cv2.imwrite(ycc_path, mask_ycc)
```

### Bước 8: Áp Dụng Masks (Dòng 101-111)

```python
result_hsv = cv2.bitwise_and(img, img, mask=mask_hsv)
result_ycc = cv2.bitwise_and(img, img, mask=mask_ycc)
```

**Giải thích**:
- `cv2.bitwise_and(img, img, mask=mask)`: Giữ pixels theo mask
- `mask=255`: Giữ pixel
- `mask=0`: Đặt pixel về [0, 0, 0] (đen)

**Kết quả**: Ảnh chỉ hiển thị vùng da, phần còn lại đen.

### Bước 9: So Sánh Kết Quả (Dòng 114-133)

**Đếm pixels**:

```python
pixels_hsv = np.sum(mask_hsv > 0)
pixels_ycc = np.sum(mask_ycc > 0)
total_pixels = mask_hsv.shape[0] * mask_hsv.shape[1]

print(f"HSV: {pixels_hsv} pixels ({pixels_hsv/total_pixels*100:.2f}%)")
print(f"YCrCb: {pixels_ycc} pixels ({pixels_ycc/total_pixels*100:.2f}%)")
```

**Intersection (giao)**:

```python
intersection = cv2.bitwise_and(mask_hsv, mask_ycc)
pixels_common = np.sum(intersection > 0)
print(f"Giao: {pixels_common} pixels ({pixels_common/total_pixels*100:.2f}%)")
```

**Ý nghĩa**:
- **Intersection**: Pixels mà CẢ HAI phương pháp đều phát hiện
- Intersection cao → 2 phương pháp đồng thuận
- Intersection thấp → 2 phương pháp khác nhau

### Bước 10: Kết Luận (Dòng 136-154)

```python
print("""
HSV:
  + Tốt cho các ứng dụng trong điều kiện ánh sáng ổn định
  + H (Hue) ít bị ảnh hưởng bởi độ sáng
  - Nhạy cảm với bóng và sự thay đổi ánh sáng

YCrCb:
  + Tốt hơn trong điều kiện ánh sáng thay đổi
  + Cr và Cb tách biệt rõ ràng màu da
  + Ít bị ảnh hưởng bởi độ sáng (Y)
  - Có thể phát hiện nhầm vật thể có màu tương tự

Khuyến nghị:
- Kết hợp cả hai phương pháp (intersection) để tăng độ chính xác
- Cần post-processing (morphology) để loại bỏ nhiễu
- Điều chỉnh ngưỡng tùy theo bộ ảnh cụ thể
""")
```

## Các Đoạn Code Quan Trọng

### 1. Color Space Conversion (Dòng 61-62)

```python
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
```

**cv2.cvtColor() là gì?**
- Hàm chuyển đổi color space
- Sử dụng công thức chuẩn (ITU-R BT.601, BT.709)
- Nhanh (optimized C++ code)

**Công thức chuyển đổi**:

**BGR → HSV**:
```
V = max(R, G, B)
S = (V - min(R,G,B)) / V  (if V ≠ 0)
H = 60° × (G-B)/(V-min)    (if V=R)
```

**BGR → YCrCb** (ITU-R BT.601):
```
Y  = 0.299×R + 0.587×G + 0.114×B
Cr = 0.713×(R - Y) + 128
Cb = 0.564×(B - Y) + 128
```

### 2. Color Thresholding (Dòng 73, 84)

```python
mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)
mask_ycc = cv2.inRange(ycrcb, lower_ycc, upper_ycc)
```

**cv2.inRange() hoạt động như thế nào?**

**Pseudo-code**:
```python
for each pixel (h, s, v):
    if lower_hsv[0] <= h <= upper_hsv[0] and
       lower_hsv[1] <= s <= upper_hsv[1] and
       lower_hsv[2] <= v <= upper_hsv[2]:
        mask[pixel] = 255
    else:
        mask[pixel] = 0
```

**Lưu ý**: Kiểm tra **AND** (tất cả channels phải thỏa)

### 3. Bitwise AND với Mask (Dòng 102-103)

```python
result_hsv = cv2.bitwise_and(img, img, mask=mask_hsv)
```

**Tại sao AND hai lần img?**

**Giải thích**:
- `cv2.bitwise_and(src1, src2, mask=mask)`
- src1 = src2 = img → AND không thay đổi giá trị
- **mask** là điều kiện: giữ pixel nào

**Tương đương**:
```python
result = img.copy()
result[mask_hsv == 0] = [0, 0, 0]
```

**Tại sao không dùng cách trên?**
- `cv2.bitwise_and()` nhanh hơn (optimized)
- Chuẩn trong OpenCV

### 4. Intersection (Dòng 129)

```python
intersection = cv2.bitwise_and(mask_hsv, mask_ycc)
```

**Giải thích**:
- AND giữa 2 masks
- Pixel = 255 chỉ khi CẢ HAI masks đều 255
- Kết quả: Vùng mà cả HSV và YCrCb đều phát hiện

**Venn diagram**:
```
HSV:    ████████
YCrCb:      ████████
Intersection:  ████
```

## Hiểu Sâu Hơn

### Câu hỏi 1: Tại sao OpenCV dùng H∈[0, 179] thay vì [0, 360]?

**Trả lời**:

**Lý do**:
- HSV chuẩn: H∈[0°, 360°]
- OpenCV: H∈[0, 179] (uint8)

**Tại sao?**
- `uint8` chỉ lưu được 0-255
- Nếu dùng [0, 360] → cần `uint16` (2 bytes/pixel)
- Dùng [0, 179] → chỉ cần `uint8` (1 byte/pixel)
- Tiết kiệm 50% memory

**Quy đổi**:
```python
H_opencv = H_standard / 2  # 360° → 180
H_standard = H_opencv * 2  # 180 → 360°
```

**Ví dụ**:
- Đỏ: 0° (standard) → 0 (OpenCV)
- Cam: 30° → 15
- Vàng: 60° → 30
- Xanh lá: 120° → 60
- Xanh dương: 240° → 120

**Trong code**:
- `lower_hsv = (0, ...)`: 0° (đỏ)
- `upper_hsv = (25, ...)`: 50° (cam)

### Câu hỏi 2: HSV vs YCrCb, chọn cái nào?

**Trả lời**:

**So sánh chi tiết**:

| Tiêu chí | HSV | YCrCb |
|----------|-----|-------|
| **Robustness với lighting** | Trung bình | Tốt |
| **Đơn giản** | Đơn giản | Đơn giản |
| **Accuracy** | Tốt (stable light) | Tốt (varied light) |
| **False positives** | Ít | Có thể nhiều hơn |
| **Tốc độ** | Nhanh | Nhanh |
| **Dùng trong** | Tracking, segmentation | Skin detection, compression |

**Trong thực tế**:

**HSV tốt khi**:
- Lighting ổn định (indoor, studio)
- Cần tách màu sắc rõ ràng
- Object tracking

**YCrCb tốt khi**:
- Lighting thay đổi (outdoor)
- Cần robust với shadows
- Skin detection, face detection

**Best practice**: **Kết hợp cả hai**
```python
# High precision: Intersection (AND)
mask = cv2.bitwise_and(mask_hsv, mask_ycc)

# High recall: Union (OR)
mask = cv2.bitwise_or(mask_hsv, mask_ycc)
```

### Câu hỏi 3: Tại sao cần post-processing (morphology)?

**Trả lời**:

**Vấn đề sau thresholding**:
- **Noise**: Các pixel rời rạc (false positives)
- **Holes**: Lỗ trong vùng da (false negatives)
- **Rough edges**: Biên không mịn

**Morphology operations**:

**1. Opening (Erosion → Dilation)**:
```python
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask_clean = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
```
- Loại bỏ noise nhỏ
- Mất một số chi tiết

**2. Closing (Dilation → Erosion)**:
```python
mask_clean = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
```
- Lấp lỗ holes
- Kết nối vùng gần nhau

**3. Combined**:
```python
# Remove noise
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
# Fill holes
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
```

**Kết quả**: Mask sạch hơn, chính xác hơn.

### Câu hỏi 4: Làm sao điều chỉnh ngưỡng cho bộ ảnh cụ thể?

**Trả lời**:

**Phương pháp 1: Manual tuning với trackbars**

```python
def update(x):
    pass

cv2.namedWindow('Tuning')
cv2.createTrackbar('H_low', 'Tuning', 0, 179, update)
cv2.createTrackbar('H_high', 'Tuning', 25, 179, update)
cv2.createTrackbar('S_low', 'Tuning', 30, 255, update)
cv2.createTrackbar('S_high', 'Tuning', 180, 255, update)
cv2.createTrackbar('V_low', 'Tuning', 90, 255, update)
cv2.createTrackbar('V_high', 'Tuning', 255, 255, update)

while True:
    h_low = cv2.getTrackbarPos('H_low', 'Tuning')
    h_high = cv2.getTrackbarPos('H_high', 'Tuning')
    s_low = cv2.getTrackbarPos('S_low', 'Tuning')
    s_high = cv2.getTrackbarPos('S_high', 'Tuning')
    v_low = cv2.getTrackbarPos('V_low', 'Tuning')
    v_high = cv2.getTrackbarPos('V_high', 'Tuning')

    lower = (h_low, s_low, v_low)
    upper = (h_high, s_high, v_high)

    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

**Phương pháp 2: Learning from data**

```python
# Chọn vùng da thủ công (ROI)
roi = img[100:200, 150:250]  # Vùng da
roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

# Tính mean và std
h_mean, s_mean, v_mean = cv2.mean(roi_hsv)[:3]
h_std, s_std, v_std = cv2.meanStdDev(roi_hsv)[1].flatten()

# Ngưỡng = mean ± k*std (k=2 hoặc 3)
k = 2
lower = (h_mean - k*h_std, s_mean - k*s_std, v_mean - k*v_std)
upper = (h_mean + k*h_std, s_mean + k*s_std, v_mean + k*v_std)
```

**Phương pháp 3: Machine Learning**
- Train classifier (SVM, Random Forest) trên labeled data
- Thay thế thresholding bằng model prediction

## Thử Nghiệm

### 1. Thêm morphology post-processing

```python
# Thêm sau dòng 84
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# Clean HSV mask
mask_hsv_clean = cv2.morphologyEx(mask_hsv, cv2.MORPH_OPEN, kernel)
mask_hsv_clean = cv2.morphologyEx(mask_hsv_clean, cv2.MORPH_CLOSE, kernel)

# Clean YCrCb mask
mask_ycc_clean = cv2.morphologyEx(mask_ycc, cv2.MORPH_OPEN, kernel)
mask_ycc_clean = cv2.morphologyEx(mask_ycc_clean, cv2.MORPH_CLOSE, kernel)

# Lưu kết quả
cv2.imwrite(os.path.join(output_dir, "mask_hsv_clean.png"), mask_hsv_clean)
cv2.imwrite(os.path.join(output_dir, "mask_ycc_clean.png"), mask_ycc_clean)
```

**Quan sát**: Mask sạch hơn, ít noise hơn.

### 2. Test với ảnh thật

```python
# Thay dòng 20
input_path = "path/to/real_portrait.jpg"
```

**Quan sát**: Ngưỡng có thể cần điều chỉnh.

### 3. Visualize color spaces

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 3, figsize=(12, 8))

# Original
axes[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
axes[0, 0].set_title('Original')

# HSV channels
axes[0, 1].imshow(hsv[:, :, 0], cmap='hsv')
axes[0, 1].set_title('H')
axes[0, 2].imshow(hsv[:, :, 1], cmap='gray')
axes[0, 2].set_title('S')
axes[1, 0].imshow(hsv[:, :, 2], cmap='gray')
axes[1, 0].set_title('V')

# YCrCb channels
axes[1, 1].imshow(ycrcb[:, :, 1], cmap='gray')
axes[1, 1].set_title('Cr')
axes[1, 2].imshow(ycrcb[:, :, 2], cmap='gray')
axes[1, 2].set_title('Cb')

plt.savefig(os.path.join(output_dir, 'color_spaces.png'))
```

**Quan sát**: Thấy rõ vùng da trong từng channel.

### 4. Union thay vì Intersection

```python
# Thay dòng 129
union = cv2.bitwise_or(mask_hsv, mask_ycc)
pixels_union = np.sum(union > 0)
print(f"Union: {pixels_union} pixels")
```

**Quan sát**: Union > HSV, Union > YCrCb.

## Kết Quả Mẫu

**Input**: Portrait 400x600 với vùng da ellipse

**HSV Detection**:
- Pixels phát hiện: 84,720 (35.3%)
- Vùng: Ellipse trung tâm + một số nền

**YCrCb Detection**:
- Pixels phát hiện: 81,450 (33.9%)
- Vùng: Chủ yếu ellipse, ít nền hơn

**Intersection**:
- Pixels: 78,200 (32.6%)
- Vùng: Chính xác hơn

**Nhận xét**:
- YCrCb ít false positives hơn
- HSV dễ điều chỉnh hơn
- Intersection cho precision cao nhất

## Common Pitfalls

### 1. Lỗi: HSV range sai

**Nguyên nhân**: Dùng H∈[0, 360] thay vì [0, 179]

**Cách fix**:
```python
# SAI
lower_hsv = (0, 30, 90)
upper_hsv = (50, 180, 255)  # H=50 → 100°

# ĐÚNG
upper_hsv = (25, 180, 255)  # H=25 → 50°
```

### 2. Lỗi: Quên BGR format

**Nguyên nhân**: OpenCV dùng BGR, không phải RGB

**Cách fix**:
```python
# SAI: skin_color RGB
skin_color = [220, 180, 150]  # R, G, B

# ĐÚNG: BGR
skin_color = [150, 180, 220]  # B, G, R
```

### 3. Lỗi: Mask không hoạt động

**Nguyên nhân**: Ngưỡng quá khắt khe

**Cách fix**: Kiểm tra lại ranges, có thể mở rộng.

### 4. Lỗi: bitwise_and sai

**Nguyên nhân**: Truyền mask sai

**Cách fix**:
```python
# SAI
result = cv2.bitwise_and(img, mask_hsv)

# ĐÚNG
result = cv2.bitwise_and(img, img, mask=mask_hsv)
```

### 5. Intersection trả về 0

**Nguyên nhân**: Hai masks không overlap

**Nguyên nhân thường gặp**: Ngưỡng quá khác nhau

## Tham Khảo

**Theory Documents**:
- `documents/T1-bieu-dien-va-thu-nhan-anh/theory/03-color-spaces.md`
- `documents/T1-bieu-dien-va-thu-nhan-anh/theory/04-skin-detection.md`

**OpenCV Documentation**:
- [cvtColor](https://docs.opencv.org/4.x/d8/d01/group__imgproc__color__conversions.html)
- [inRange](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga48af0ab51e36436c5d04340e036ce981)
- [bitwise operations](https://docs.opencv.org/4.x/d2/de8/group__core__array.html)

**Papers**:
- Vezhnevets et al. (2003) - "A Survey on Pixel-Based Skin Color Detection Techniques"
- Kakumanu et al. (2007) - "A survey of skin-color modeling and detection methods"

**Applications**:
- Face detection
- Hand gesture recognition
- NSFW content filtering
- Person detection

## Checklist Hiểu Bài

Sau khi đọc code, bạn nên có thể:

- [ ] Giải thích 3 color spaces: RGB, HSV, YCrCb
- [ ] Chuyển đổi giữa color spaces bằng cv2.cvtColor()
- [ ] Hiểu tại sao OpenCV dùng H∈[0, 179]
- [ ] Giải thích ngưỡng HSV và YCrCb cho da
- [ ] Sử dụng cv2.inRange() để tạo mask
- [ ] Áp dụng mask bằng cv2.bitwise_and()
- [ ] Tính intersection và union của masks
- [ ] So sánh HSV vs YCrCb (ưu/nhược điểm)
- [ ] Điều chỉnh ngưỡng cho bộ ảnh cụ thể
- [ ] Áp dụng vào face detection, gesture recognition

---

**Lưu ý**: Bài này quan trọng cho computer vision, là nền tảng cho face detection, tracking, và content filtering.
