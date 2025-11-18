# Bài 10: Tự Động Deskew Hoá Đơn/Biên Bản - Code Reading Guide

## 1. Tổng Quan

Tự động phát hiện góc nghiêng của tài liệu (hoá đơn, biên bản) bằng Hough Lines, tính góc nghiêng median, sau đó xoay ảnh về đúng phương. Ứng dụng cho OCR preprocessing.

**File code:** `/code-implement/T21-tach-bien/bai-10-deskewing/deskew.py`

---

## 2. Input/Output

### Input
- **File:** `../input/sample-images/receipt.jpg`
- **Mô tả:** Ảnh scan hoá đơn/biên bản bị nghiêng
- **Format:** RGB

### Output
- **receipt_deskew.jpg:** Ảnh đã xoay thẳng
- **receipt_comparison.jpg:** So sánh trước/sau
- **receipt_edges.png:** Canny edges (debug)
- **receipt_lines.jpg:** Visualization Hough lines (debug)

---

## 3. Thuật Toán Chính

### Bước 1: Edge detection (dòng 126-140)
- Grayscale
- Gaussian blur (σ=1.2)
- Canny (60-180)

### Bước 2: Hough Lines (dòng 143-164)
- `HoughLines()` (dạng rho-theta) để tìm đường thẳng
- Lọc chỉ lấy đường gần ngang (-45° đến +45°)

### Bước 3: Tính góc nghiêng (dòng 166-178)
- Chuyển theta sang góc độ
- **Median** của tất cả góc (robust với outliers)

### Bước 4: Xoay ảnh bù (dòng 190-207)
- `getRotationMatrix2D()` với góc = skew
- `warpAffine()` để xoay

### Bước 5: Visualization (dòng 209-250)
- So sánh trước/sau
- Vẽ Hough lines

---

## 4. Code Quan Trọng Cần Đọc

### Đoạn 1: HoughLines (rho-theta format) (dòng 144-164)
```python
lines = cv2.HoughLines(edges, 1, np.pi/180, 150)

angles = []
for rho, theta in lines[:, 0]:
    # theta ∈ [0, π] trong HoughLines
    # theta=0 → đường thẳng đứng (90°)
    # theta=π/2 → đường ngang (0°)
    ang = (theta * 180 / np.pi) - 90

    # Chỉ lấy đường gần ngang (-45° đến +45°)
    if -45 < ang < 45:
        angles.append(ang)
```
**Giải thích:**
- **HoughLines** trả về (rho, theta) - dạng cực
- **Chuyển đổi:** theta (radian) → góc so với trục ngang
- **Lọc:** Chỉ quan tâm đường ngang (text lines)

### Đoạn 2: Tính góc median (robust) (dòng 167-178)
```python
skew = np.median(angles) if angles else 0.0

print(f"   - Số góc phát hiện: {len(angles)}")
print(f"   - Góc trung bình: {np.mean(angles):.3f}°")
print(f"   - Góc trung vị (median): {skew:.3f}°")
print(f"   - Độ lệch chuẩn: {np.std(angles):.3f}°")
```
**Giải thích:**
- **Median thay vì mean:** Ít bị ảnh hưởng bởi outliers
- Ví dụ: góc = [5.1, 5.2, 5.0, 30.0] → mean=11.3, median=5.1
- **Độ lệch chuẩn thấp (<1°):** Độ tin cậy cao

### Đoạn 3: Rotation matrix (dòng 190-204)
```python
center = (w / 2, h / 2)
M = cv2.getRotationMatrix2D(center, skew, 1.0)
# center: tâm xoay
# skew: góc (độ)
# 1.0: scale (không zoom)

deskew = cv2.warpAffine(img, M, (w, h),
                        flags=cv2.INTER_LINEAR,
                        borderMode=cv2.BORDER_REPLICATE)
```
**Giải thích:**
- **getRotationMatrix2D:** Tạo ma trận affine 2×3
- **warpAffine:** Áp dụng biến đổi
- **BORDER_REPLICATE:** Lấp viền bằng pixel biên (thay vì đen)

### Đoạn 4: Vẽ Hough lines (dòng 235-249)
```python
for rho, theta in lines[:, 0][:50]:  # 50 đường đầu
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    # Kéo dài đường thẳng
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(lines_vis, (x1, y1), (x2, y2), (0, 0, 255), 1)
```
**Giải thích:**
- Chuyển (rho, theta) → (x1,y1)-(x2,y2) để vẽ
- ×1000: Kéo dài đường thẳng qua toàn ảnh

### Đoạn 5: Đánh giá độ tin cậy (dòng 273-288)
```python
std = np.std(angles)
if std < 1.0:
    reliability = "CAO"
elif std < 3.0:
    reliability = "TRUNG BÌNH"
else:
    reliability = "THẤP"
```
**Giải thích:**
- **Độ lệch chuẩn thấp:** Các đường thẳng gần song song → góc nhất quán
- **Độ lệch chuẩn cao:** Các đường phân tán → kết quả không chắc chắn

---

## 5. Tham Số Quan Trọng

| Tham Số | Giá trị | Ý nghĩa | Điều chỉnh |
|---------|---------|---------|-----------|
| Canny low | `60` | Ngưỡng thấp | Tăng (80) nếu quá nhiều edges nhiễu |
| Canny high | `180` | Ngưỡng cao | Tỉ lệ ~1:3 với low |
| HoughLines threshold | `150` | Số vote tối thiểu | Giảm (100) nếu thiếu lines, tăng (200) nếu quá nhiều |
| Angle range | `[-45, 45]` | Chỉ lấy đường gần ngang | Mở rộng nếu nghiêng mạnh |
| borderMode | `BORDER_REPLICATE` | Xử lý viền sau xoay | `BORDER_CONSTANT` nếu muốn nền trắng |

---

## 6. Kết Quả Mong Đợi

### Ảnh output
- **receipt_deskew.jpg:** Tài liệu hoàn toàn thẳng
- Text lines nằm ngang
- Không bị méo/mất thông tin

### Console output
```
Đã phát hiện biên bằng Canny (ngưỡng: 60, 180)

Đang phát hiện đường thẳng bằng Hough Transform...
  ✓ Phát hiện được 78 đường thẳng
  ✓ Lọc được 65 đường gần ngang

Phân tích góc nghiêng:
  - Số góc phát hiện: 65
  - Góc trung bình: 7.523°
  - Góc trung vị (median): 7.500°
  - Độ lệch chuẩn: 0.456°
  - Min: 6.8°, Max: 8.2°

Góc nghiêng ước tính: 7.500°
  → Nghiêng mạnh

Đang xoay ảnh bù 7.500°...
✓ Đã xoay ảnh về đúng phương

Độ tin cậy: CAO
  - Độ lệch chuẩn góc: 0.456°
```

---

## 7. Lỗi Thường Gặp

### Lỗi 1: Không phát hiện được đường thẳng
**Nguyên nhân:**
- Ảnh quá mờ/nhiễu
- Threshold quá cao
- Text quá ít

**Cách fix:**
- Kiểm tra edges: có rõ không?
- Giảm threshold từ 150 xuống 80-100
- Tăng độ tương phản trước:
```python
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
gray = clahe.apply(gray)
```

### Lỗi 2: Góc nghiêng không chính xác
**Nguyên nhân:**
- Tài liệu có nhiều đường không ngang (bảng, logo)
- Outliers ảnh hưởng

**Cách fix:**
- **Median đã giúp giảm outliers** (code đã dùng)
- Lọc thêm theo độ dài đường:
```python
lines_P = cv2.HoughLinesP(edges, 1, np.pi/180, 100,
                          minLineLength=100, maxLineGap=10)
# Chỉ lấy đường dài
```
- Kiểm tra `std`: nếu >3° thì cảnh báo không tin cậy

### Lỗi 3: Ảnh sau xoay bị cắt góc
**Nguyên nhân:** Kích thước output không đủ lớn

**Cách fix:**
- Tính kích thước mới để chứa toàn bộ ảnh xoay:
```python
cos = abs(M[0, 0])
sin = abs(M[0, 1])
new_w = int((h * sin) + (w * cos))
new_h = int((h * cos) + (w * sin))
M[0, 2] += (new_w / 2) - center[0]
M[1, 2] += (new_h / 2) - center[1]
deskew = cv2.warpAffine(img, M, (new_w, new_h), ...)
```

---

## 8. Mở Rộng

### Cải tiến 1: Projection profile method
```python
# Phương pháp khác: dùng projection
gray_bin = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

# Thử xoay từ -10° đến +10°
angles = np.linspace(-10, 10, 100)
max_variance = 0
best_angle = 0

for angle in angles:
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(gray_bin, M, (w, h))
    # Projection lên trục y
    proj = np.sum(rotated, axis=1)
    variance = np.var(proj)
    if variance > max_variance:
        max_variance = variance
        best_angle = angle

# Góc tốt nhất = góc có variance projection cao nhất
```

### Cải tiến 2: Deep learning
```python
# Dùng CNN để predict góc trực tiếp
# Input: ảnh nghiêng
# Output: góc (regression)
model = load_model('deskew_model.h5')
skew = model.predict(img)[0]
```

### Cải tiến 3: Automatic crop sau deskew
```python
# Sau khi xoay, cắt bỏ viền đen
gray_deskew = cv2.cvtColor(deskew, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray_deskew, 1, 255, cv2.THRESH_BINARY)
cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
x, y, w, h = cv2.boundingRect(max(cnts, key=cv2.contourArea))
deskew = deskew[y:y+h, x:x+w]
```

### Cải tiến 4: Batch processing
```python
import glob
for img_path in glob.glob('input/*.jpg'):
    img = cv2.imread(img_path)
    # ... deskew ...
    out_path = img_path.replace('input', 'output')
    cv2.imwrite(out_path, deskew)
```

### Cải tiến 5: Kết hợp với OCR
```python
import pytesseract

# Deskew trước khi OCR
skew = detect_skew(img)
deskew = rotate_image(img, skew)

# OCR
text = pytesseract.image_to_string(deskew, lang='vie')
print(text)
```

---

## Tips Đọc Code Nhanh

1. **Hiểu HoughLines (rho-theta)** (dòng 143-164) khác HoughLinesP
2. **Median vs Mean** (dòng 167) - tại sao median tốt hơn
3. **Rotation matrix** (dòng 190-204) - chuẩn trong CV
4. **Đánh giá reliability** (dòng 273-288) - quan trọng
5. **Skip phần tạo ảnh** (dòng 42-112)

---

**Tổng số dòng:** 297 dòng
**Độ khó:** Trung bình
**Thời gian đọc hiểu:** 20-25 phút
**Thời gian chạy:** ~1 giây
**Ứng dụng thực tế:** OCR preprocessing, document scanning, archive digitization
