# Bài 8: Tách Biên Lá Cây và Đo Chu Vi/Diện Tích - Code Reading Guide

## 1. Tổng Quan

Phát hiện contour lá cây, tính các đại lượng hình học (diện tích, chu vi, aspect ratio, extent, solidity) và đặc biệt là chỉ số "răng cưa" (serration index) để phân loại hình dạng lá.

**File code:** `/code-implement/T21-tach-bien/bai-8-leaf-measurement/measure.py`

---

## 2. Input/Output

### Input
- **File:** `../input/sample-images/leaf.jpg`
- **Mô tả:** Ảnh một chiếc lá trên nền tương phản
- **Tùy chọn:** DPI hoặc thước chuẩn để đổi sang mm (code chưa implement)

### Output
- **leaf_metrics.jpg:** Ảnh với contour, convex hull, bbox và các số đo
- **leaf_edges.png:** Canny edges (debug)
- **leaf_contours.jpg:** Visualization contour + hull

---

## 3. Thuật Toán Chính

### Bước 1: Edge detection (dòng 115-129)
- Grayscale
- Gaussian blur (σ=1.5)
- Canny (60-150)

### Bước 2: Tìm contour lá (dòng 131-137)
- `findContours()` → chọn contour lớn nhất

### Bước 3: Tính các đại lượng hình học (dòng 139-192)
- **Diện tích (Area):** `contourArea()`
- **Chu vi (Perimeter):** `arcLength()`
- **Chỉ số răng cưa (Serration):** P² / (4π·A)
- **Bounding box:** `boundingRect()`
- **Aspect ratio:** W/H
- **Extent:** Area / Rect_area
- **Solidity:** Area / Hull_area
- **Convexity defects:** Số điểm lõm

### Bước 4: Visualization (dòng 194-229)
- Vẽ contour (xanh lá), hull (xanh dương), bbox (đỏ)
- Thêm text thông tin

---

## 4. Code Quan Trọng Cần Đọc

### Đoạn 1: Chỉ số răng cưa (dòng 139-162)
```python
area = cv2.contourArea(cnt)
peri = cv2.arcLength(cnt, True)

# Chỉ số răng cưa: S = P² / (4π·A)
serration = (peri ** 2) / (4 * math.pi * area + 1e-6)

if serration < 1.2:
    shape_desc = "gần tròn/trơn"
elif serration < 2.0:
    shape_desc = "răng cưa nhẹ"
elif serration < 3.0:
    shape_desc = "răng cưa trung bình"
else:
    shape_desc = "răng cưa mạnh"
```
**Giải thích:**
- **Công thức:** S = P² / (4πA)
- **Vòng tròn hoàn hảo:** S = 1.0 (chu vi = 2πr, diện tích = πr²)
- **Càng nhiều răng cưa, S càng lớn** (chu vi tăng nhưng diện tích giữ nguyên)
- +1e-6 để tránh chia cho 0

### Đoạn 2: Extent (tỷ lệ lấp đầy bbox) (dòng 172-175)
```python
x, y, w, h = cv2.boundingRect(cnt)
rect_area = w * h
extent = float(area) / rect_area
```
**Giải thích:**
- **Extent cao (>0.7):** Lá hình chữ nhật, lấp đầy bbox tốt
- **Extent thấp (<0.5):** Lá nhiều lõm/lồi, hình dạng phức tạp

### Đoạn 3: Solidity (tỷ lệ lấp đầy convex hull) (dòng 177-181)
```python
hull = cv2.convexHull(cnt)
hull_area = cv2.contourArea(hull)
solidity = float(area) / hull_area
```
**Giải thích:**
- **Convex hull:** Đa giác lồi nhỏ nhất bao quanh contour
- **Solidity cao (>0.9):** Viền lá gần như không lõm
- **Solidity thấp (<0.7):** Viền lá nhiều lõm sâu

### Đoạn 4: Convexity defects (dòng 183-192)
```python
hull_indices = cv2.convexHull(cnt, returnPoints=False)
if len(hull_indices) > 3 and len(cnt) > 3:
    defects = cv2.convexityDefects(cnt, hull_indices)
    if defects is not None:
        num_defects = len(defects)
```
**Giải thích:**
- **Convexity defects:** Các điểm lõm (khoảng cách từ contour đến hull)
- Số lượng defects cho biết độ phức tạp viền
- Cần `returnPoints=False` để lấy indices cho `convexityDefects()`

### Đoạn 5: Phân tích hình dạng (dòng 235-264)
```python
if aspect_ratio < 0.7:
    print(f"   → Lá hình dài (chiều cao > chiều rộng)")
elif aspect_ratio > 1.3:
    print(f"   → Lá hình rộng (chiều rộng > chiều cao)")
else:
    print(f"   → Lá cân đối")
```
**Giải thích:** Kết hợp nhiều chỉ số để mô tả hình dạng tổng thể.

---

## 5. Tham Số Quan Trọng

| Tham Số | Giá trị | Ý nghĩa | Điều chỉnh |
|---------|---------|---------|-----------|
| Gaussian sigma | `1.5` | Độ mạnh blur | Tăng (2.0) nếu lá có texture nhiều |
| Canny low | `60` | Ngưỡng thấp | Điều chỉnh nếu edges không rõ |
| Canny high | `150` | Ngưỡng cao | Tỉ lệ ~1:2.5 với low |
| Serration thresholds | `1.2, 2.0, 3.0` | Phân loại răng cưa | Dựa vào dataset thực tế |
| Aspect thresholds | `0.7, 1.3` | Phân loại dài/rộng | Dựa vào loài lá |

---

## 6. Kết Quả Mong Đợi

### Ảnh output
- Contour lá (xanh lá), hull (xanh dương), bbox (đỏ)
- Text hiển thị: Area, Perimeter, Serration, Aspect, Extent, Solidity

### Console output
```
Các đại lượng hình học:
  - Diện tích (Area): 125680.0 px²
  - Chu vi (Perimeter): 1548.5 px
  - Chỉ số răng cưa (Serration): 1.456
  → Hình dạng: răng cưa nhẹ

  - Bounding box: 360×560 px
  - Aspect ratio (W/H): 0.643
  - Extent (area/rect_area): 0.623
  - Solidity (area/hull_area): 0.875
  - Số điểm lõm (convexity defects): 48

PHÂN TÍCH HÌNH DẠNG LÁ:
1. Hình dạng tổng thể:
   → Lá hình dài (chiều cao > chiều rộng)

2. Độ lấp đầy:
   → Lá có nhiều phần lõm/lồi

3. Độ lồi:
   → Viền lá có lõm nhẹ

4. Độ phức tạp viền:
   → Viền lá có răng cưa vừa phải
```

---

## 7. Lỗi Thường Gặp

### Lỗi 1: "Không tính được convexity defects"
**Nguyên nhân:**
- Contour quá đơn giản (ít điểm)
- Hull indices không hợp lệ

**Cách fix:**
- Code đã có try-except để bắt lỗi
- Không ảnh hưởng đến các đo lường khác

### Lỗi 2: Serration index quá cao/thấp bất thường
**Nguyên nhân:**
- Contour bị nhiễu (răng cưa giả)
- Epsilon của approxPolyDP không phù hợp

**Cách fix:**
- Làm trơn contour trước:
```python
epsilon = 0.005 * cv2.arcLength(cnt, True)
cnt = cv2.approxPolyDP(cnt, epsilon, True)
```

### Lỗi 3: Phát hiện sai contour (không phải lá)
**Nguyên nhân:** Có vật thể khác lớn hơn lá

**Cách fix:**
- Lọc theo màu trước (nếu lá màu xanh):
```python
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (35, 40, 40), (85, 255, 255))  # Green range
gray = cv2.bitwise_and(gray, gray, mask=mask)
```

---

## 8. Mở Rộng

### Cải tiến 1: Đổi sang đơn vị mm
```python
# Đặt vật chuẩn (ví dụ: thước 10cm) trong ảnh
known_width_mm = 100  # 10cm
known_width_px = ...  # đo từ ảnh
px_per_mm = known_width_px / known_width_mm

area_mm2 = area / (px_per_mm ** 2)
peri_mm = peri / px_per_mm
print(f"Diện tích: {area_mm2:.2f} mm²")
print(f"Chu vi: {peri_mm:.2f} mm")
```

### Cải tiến 2: Phân loại loài lá bằng ML
```python
# Features: [serration, aspect, extent, solidity, defects]
features = np.array([serration, aspect_ratio, extent, solidity, num_defects])

# Train classifier (SVM, Random Forest)
model = joblib.load('leaf_classifier.pkl')
species = model.predict([features])[0]
print(f"Loài lá: {species}")
```

### Cải tiến 3: Phân tích màu sắc
```python
# Tính màu trung bình của lá
mask = np.zeros(img.shape[:2], np.uint8)
cv2.drawContours(mask, [cnt], -1, 255, -1)
mean_color = cv2.mean(img, mask=mask)[:3]

# Phân loại sức khỏe (xanh tươi vs vàng/nâu)
if mean_color[1] > 150:  # G channel
    health = "Khỏe mạnh"
else:
    health = "Yếu/bệnh"
```

### Cải tiến 4: Đo diện tích lá theo phương pháp grid
```python
# Đếm số pixels trong contour
mask = np.zeros(img.shape[:2], np.uint8)
cv2.drawContours(mask, [cnt], -1, 255, -1)
area_pixels = np.sum(mask > 0)
# So sánh với contourArea()
```

### Cải tiến 5: Phát hiện bệnh trên lá
```python
# Tìm vùng màu khác thường (đốm bệnh)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# Mask vùng nâu/vàng
disease_mask = cv2.inRange(hsv, (10, 50, 50), (30, 255, 200))
disease_area = np.sum(disease_mask > 0)
disease_ratio = disease_area / area
if disease_ratio > 0.05:
    print("Cảnh báo: Lá bị bệnh!")
```

---

## Tips Đọc Code Nhanh

1. **Chỉ số Serration** (dòng 139-162) - điểm mới và quan trọng
2. **3 chỉ số: Extent, Solidity, Defects** (dòng 165-192)
3. **Phần phân tích** (dòng 231-264) kết hợp các chỉ số
4. **Visualization** (dòng 194-229) rất chi tiết
5. **Skip tạo ảnh mẫu** (dòng 43-101)

---

**Tổng số dòng:** 271 dòng
**Độ khó:** Trung bình
**Thời gian đọc hiểu:** 20-25 phút
**Thời gian chạy:** <1 giây
**Ứng dụng thực tế:** Nông nghiệp (phân loại lá, phát hiện bệnh), thực vật học, giáo dục
