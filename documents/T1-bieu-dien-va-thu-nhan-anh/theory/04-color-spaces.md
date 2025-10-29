# Lý thuyết: Không gian Màu (Color Spaces)

## 1. Giới thiệu

Không gian màu là mô hình toán học để biểu diễn màu sắc. Mỗi không gian có ưu nhược điểm riêng cho các ứng dụng khác nhau.

## 2. RGB Color Space

### 2.1. Định nghĩa
**RGB** = Red + Green + Blue (mô hình cộng màu)

**Biểu diễn**:
```
Color = (R, G, B)
R, G, B ∈ [0, 255] (8-bit)
```

### 2.2. Đặc điểm
- **Additive**: Cộng ánh sáng (màn hình)
- **Device-dependent**: Phụ thuộc thiết bị
- **Intuitive**: Dễ hiểu nhưng không perceptually uniform

### 2.3. Chuyển đổi
**RGB → Grayscale**:
```
Gray = 0.299×R + 0.587×G + 0.114×B
```

**Lưu ý**: Hệ số khác nhau vì mắt người nhạy với xanh lá nhất.

## 3. HSV Color Space

### 3.1. Định nghĩa
**HSV** = Hue + Saturation + Value

**Thành phần**:
- **H (Hue)**: Màu sắc [0°, 360°] (OpenCV: [0, 179])
- **S (Saturation)**: Độ bão hòa [0, 1] hoặc [0%, 100%]
- **V (Value)**: Độ sáng [0, 1] hoặc [0%, 100%]

### 3.2. Hình học
**Cone model**:
- Đỉnh: Đen (V=0)
- Trục: Trắng-xám-đen
- Chu vi: Màu thuần khiết

**Hue circle**:
```
0° = Đỏ (Red)
60° = Vàng (Yellow)
120° = Xanh lá (Green)
180° = Cyan
240° = Xanh dương (Blue)
300° = Magenta
```

### 3.3. Chuyển đổi RGB → HSV

**Value**:
```
V = max(R, G, B)
```

**Saturation**:
```
S = 0                    if V = 0
S = (V - min(R,G,B)) / V otherwise
```

**Hue** (phức tạp, xem code OpenCV):
```python
hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
```

### 3.4. Ưu điểm
- **Perceptually meaningful**: H là màu, S là độ đậm, V là độ sáng
- **Robust to lighting**: H ít bị ảnh hưởng bởi shadow/lighting
- **Good for color-based segmentation**

### 3.5. Ứng dụng
- Phát hiện vùng da (skin detection)
- Color-based object tracking
- Image editing (Adobe Photoshop)

## 4. YCrCb Color Space

### 4.1. Định nghĩa
**YCrCb** = Luminance + Chroma Red + Chroma Blue

**Thành phần**:
- **Y**: Luma (độ sáng) [16, 235]
- **Cr**: Chroma Red (độ đỏ) [16, 240]
- **Cb**: Chroma Blue (độ xanh) [16, 240]

### 4.2. Chuyển đổi RGB → YCrCb

**Digital 8-bit** (JPEG standard):
```
Y  = 16  + 0.257×R + 0.504×G + 0.098×B
Cr = 128 + 0.439×R - 0.368×G - 0.071×B
Cb = 128 - 0.148×R - 0.291×G + 0.439×B
```

**OpenCV**:
```python
ycrcb = cv2.cvtColor(rgb, cv2.COLOR_RGB2YCrCb)
```

### 4.3. Đặc điểm
- **Separates luma and chroma**: Y riêng biệt với màu
- **Used in video compression**: JPEG, MPEG, H.264
- **Robust to lighting changes**: Cr, Cb ít bị ảnh hưởng bởi lighting

### 4.4. Ứng dụng
- **Skin detection**: Cr, Cb có range đặc trưng cho da người
- **Video compression**: Lợi dụng mắt người nhạy Y hơn Cr, Cb
- **Face detection**: Dựa trên Cr, Cb thresholds

## 5. So sánh các Color Spaces

| Feature | RGB | HSV | YCrCb |
|---------|-----|-----|-------|
| Intuitive | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Lighting invariance | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Skin detection | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Compression | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Speed | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

## 6. Skin Detection

### 6.1. HSV Thresholds
```python
# Ngưỡng da người trong HSV
lower_hsv = (0, 30, 90)    # (H_min, S_min, V_min)
upper_hsv = (25, 180, 255) # (H_max, S_max, V_max)
```

**Giải thích**:
- H ∈ [0, 25]: Vùng đỏ-cam (da)
- S ∈ [30, 180]: Không quá nhạt, không quá đậm
- V ∈ [90, 255]: Đủ sáng

### 6.2. YCrCb Thresholds
```python
# Ngưỡng da người trong YCrCb
lower_ycc = (0, 135, 85)   # (Y_min, Cr_min, Cb_min)
upper_ycc = (255, 180, 135) # (Y_max, Cr_max, Cb_max)
```

**Giải thích**:
- Y: Bất kỳ (không quan trọng)
- Cr ∈ [135, 180]: Đỏ vừa phải
- Cb ∈ [85, 135]: Xanh thấp

### 6.3. So sánh
- **HSV**: Tốt trong điều kiện ánh sáng ổn định
- **YCrCb**: Tốt hơn với lighting thay đổi
- **Best**: Kết hợp cả hai (intersection)

## 7. Các Color Spaces khác

### 7.1. HSL (Hue, Saturation, Lightness)
Tương tự HSV nhưng L khác V:
- **HSV**: V = max(R,G,B)
- **HSL**: L = (max(R,G,B) + min(R,G,B)) / 2

### 7.2. LAB (CIE L*a*b*)
- **L**: Lightness [0, 100]
- **a**: Green-Red [-128, 127]
- **b**: Blue-Yellow [-128, 127]

**Ưu điểm**: Perceptually uniform (khoảng cách Euclidean = sự khác biệt màu nhận thức)

### 7.3. CMYK (Cyan, Magenta, Yellow, Key/Black)
- **Subtractive color model**: In ấn
- Không dùng trong xử lý ảnh số thường

## 8. Chuyển đổi Color Space

### 8.1. OpenCV
```python
# RGB → HSV
hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)

# RGB → YCrCb
ycrcb = cv2.cvtColor(rgb, cv2.COLOR_RGB2YCrCb)

# BGR → Grayscale
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
```

**Lưu ý**: OpenCV mặc định dùng BGR, không phải RGB!

### 8.2. Scikit-image
```python
from skimage import color

# RGB → LAB
lab = color.rgb2lab(rgb)

# RGB → HSV
hsv = color.rgb2hsv(rgb)
```

## 9. Ứng dụng theo từng Color Space

### 9.1. RGB
- Display (màn hình)
- Camera capture
- Basic image processing

### 9.2. HSV
- Color-based segmentation
- Color adjustment (Photoshop Hue/Saturation)
- Object tracking by color
- Artistic effects

### 9.3. YCrCb
- Video compression (JPEG, MPEG)
- Skin detection
- Face detection preprocessing
- Chroma keying (green screen)

### 9.4. LAB
- Color correction
- Color matching
- Perceptual color difference
- Professional image editing

## 10. Best Practices

### 10.1. Chọn Color Space
```
Task: Color segmentation → HSV
Task: Skin detection → YCrCb
Task: Compression → YCrCb
Task: Display → RGB
Task: Color difference → LAB
```

### 10.2. Thresholding tips
- **HSV**: Careful với Hue wrapping (0° = 360°)
- **YCrCb**: Ignore Y, focus on Cr/Cb
- **RGB**: Thường không tốt cho thresholding

### 10.3. Lighting robustness
```
Best → Worst:
LAB > YCrCb > HSV > RGB
```

## 11. Code Examples

### 11.1. Skin Detection với HSV
```python
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = (0, 30, 90)
upper = (25, 180, 255)
mask = cv2.inRange(hsv, lower, upper)
```

### 11.2. Skin Detection với YCrCb
```python
ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
lower = (0, 135, 85)
upper = (255, 180, 135)
mask = cv2.inRange(ycrcb, lower, upper)
```

### 11.3. Kết hợp 2 masks
```python
mask_hsv = detect_skin_hsv(img)
mask_ycc = detect_skin_ycrcb(img)
mask_final = cv2.bitwise_and(mask_hsv, mask_ycc)
```

## 12. Tóm tắt

**RGB**: Đơn giản, trực tiếp, nhưng không perceptually uniform
**HSV**: Intuitive, tốt cho color selection, robust to lighting changes
**YCrCb**: Excellent cho skin detection và video compression
**LAB**: Perceptually uniform, tốt nhất cho color matching

**Rule of thumb**:
- Display → RGB
- User interaction → HSV
- Skin/face → YCrCb
- Color science → LAB

---

**References**:
- Gonzalez & Woods - Digital Image Processing (Chapter 6)
- OpenCV Documentation - Color Space Conversions
- "A Review on Skin Color Detection" (various papers)
