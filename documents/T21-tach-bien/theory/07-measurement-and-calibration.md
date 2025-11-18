# Lý Thuyết 7: Đo Đạc Vật Thể và Calibration

## 📋 Tổng Quan

Đo kích thước vật thể trong ảnh là ứng dụng quan trọng của Computer Vision. Tuy nhiên, **pixel không phải đơn vị thực** - cần **calibration** (hiệu chuẩn) để chuyển từ pixel sang đơn vị thực (mm, cm, inch).

## 🎯 Ứng Dụng

- **Bài 9**: Đo kích thước vật thể với vật chuẩn (đồng xu)

**Ứng dụng thực tế**:
- Quality Control (kiểm tra kích thước sản phẩm)
- Agriculture (đo diện tích lá, quả)
- Medical Imaging (đo khối u, cơ quan)
- Logistics (đo package)
- Archaeology (đo artifact)

## 📐 Nguyên Lý Calibration

### Pixels Per Metric (PPM)

**Công thức cơ bản**:
```
pixels_per_metric = pixels_measured / real_world_size
```

**Ví dụ**:
- Đồng xu đường kính 2.4 cm
- Đồng xu trong ảnh: 100 pixels
- PPM = 100 / 2.4 ≈ 41.67 pixels/cm

**Đo vật thể**:
```
real_size = pixels_measured / pixels_per_metric
```

Ví dụ: Vật thể 200 pixels → 200 / 41.67 ≈ 4.8 cm

### Yêu Cầu Quan Trọng ⚠️

1. **Vật chuẩn và vật đo cùng mặt phẳng**
   - Nếu không cùng độ sâu → sai số lớn
   - Camera phải gần vuông góc

2. **Vật chuẩn kích thước đã biết**
   - Đồng xu (đường kính chuẩn)
   - Thẻ tín dụng (85.6mm × 53.98mm)
   - Thước kẻ
   - Marker in sẵn

3. **Không có lens distortion**
   - Nếu có, cần undistort trước
   - Wide-angle lens → méo hình ảnh

## 🔧 Workflow Đo Đạc

### Bước 1: Tìm Vật Chuẩn

```python
# Đọc ảnh
img = cv2.imread('measurement.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7,7), 1.5)

# Threshold
_, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Morphology để làm sạch
kernel = np.ones((5,5), np.uint8)
binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)

# Tìm contours
cnts, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort theo vị trí (trái → phải)
cnts = sorted(cnts, key=lambda c: cv2.boundingRect(c)[0])
```

### Bước 2: Nhận Diện Vật Chuẩn

#### Phương Pháp 1: Theo Vị Trí (Leftmost)

```python
# Giả sử vật chuẩn ở bên trái nhất
reference = cnts[0]
```

#### Phương Pháp 2: Theo Circularity (Đồng Xu)

```python
def is_coin(cnt):
    area = cv2.contourArea(cnt)
    if area < 1000:  # Quá nhỏ
        return False

    perimeter = cv2.arcLength(cnt, True)
    circularity = 4 * np.pi * area / (perimeter ** 2)

    return circularity > 0.8  # Gần tròn

# Tìm đồng xu đầu tiên
reference = None
for c in cnts:
    if is_coin(c):
        reference = c
        break
```

#### Phương Pháp 3: Theo Màu/Template

```python
# Dùng màu sắc
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# Màu đồng (đỏ cam)
mask_coin = cv2.inRange(hsv, (0, 100, 100), (20, 255, 255))

# Hoặc template matching
template = cv2.imread('coin_template.jpg', 0)
result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
```

### Bước 3: Tính Pixels Per Metric

```python
# Bounding box của vật chuẩn
box = cv2.minAreaRect(reference)
(x, y), (w, h), angle = box

# Chiều rộng vật chuẩn (pixels)
ref_width_pixels = max(w, h)

# Kích thước thực của vật chuẩn
COIN_DIAMETER_CM = 2.4  # Đồng xu 500 VND

# Tính PPM
pixels_per_metric = ref_width_pixels / COIN_DIAMETER_CM

print(f"Pixels per cm: {pixels_per_metric:.2f}")
```

### Bước 4: Đo Các Vật Thể Khác

```python
for cnt in cnts:
    # Bỏ qua vật chuẩn
    if np.array_equal(cnt, reference):
        continue

    # Bỏ qua vật quá nhỏ (nhiễu)
    if cv2.contourArea(cnt) < 500:
        continue

    # Bounding box
    box = cv2.minAreaRect(cnt)
    box_points = cv2.boxPoints(box)
    box_points = np.int0(box_points)

    # Chiều rộng và chiều cao (pixels)
    (x, y), (w, h), angle = box
    width_pixels = max(w, h)
    height_pixels = min(w, h)

    # Chuyển sang cm
    width_cm = width_pixels / pixels_per_metric
    height_cm = height_pixels / pixels_per_metric

    # Tính diện tích
    area_pixels = cv2.contourArea(cnt)
    area_cm2 = area_pixels / (pixels_per_metric ** 2)

    # Vẽ
    cv2.drawContours(img, [box_points], 0, (0,255,0), 2)

    # Tính trọng tâm để ghi text
    M = cv2.moments(cnt)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])

    # Ghi kích thước
    cv2.putText(img, f"{width_cm:.1f} x {height_cm:.1f} cm",
                (cx - 50, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
    cv2.putText(img, f"Area: {area_cm2:.1f} cm2",
                (cx - 50, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
```

## 📏 Đo Khoảng Cách Giữa Các Điểm

### Tìm Điểm Cực Trị

```python
def extreme_points(cnt):
    """
    Tìm 4 điểm cực trị: left, right, top, bottom
    """
    leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
    rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
    topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
    bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])

    return leftmost, rightmost, topmost, bottommost
```

### Đo Khoảng Cách

```python
import numpy as np

def distance(pt1, pt2):
    """Khoảng cách Euclidean"""
    return np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

# Tìm điểm cực trị
left, right, top, bottom = extreme_points(cnt)

# Đo chiều rộng
width_pixels = distance(left, right)
width_cm = width_pixels / pixels_per_metric

# Đo chiều cao
height_pixels = distance(top, bottom)
height_cm = height_pixels / pixels_per_metric

# Vẽ đường đo
cv2.line(img, left, right, (0,255,255), 2)
cv2.line(img, top, bottom, (0,255,255), 2)

# Đánh dấu điểm
for pt in [left, right, top, bottom]:
    cv2.circle(img, pt, 5, (0,0,255), -1)
```

## 🎯 Đo Diện Tích

### Diện Tích Từ Contour

```python
# Diện tích pixel
area_pixels = cv2.contourArea(cnt)

# Chuyển sang cm²
area_cm2 = area_pixels / (pixels_per_metric ** 2)

# Chuyển sang mm²
area_mm2 = area_cm2 * 100
```

### Diện Tích Từ Mask

```python
# Tạo mask
mask = np.zeros(gray.shape, np.uint8)
cv2.drawContours(mask, [cnt], -1, 255, thickness=-1)

# Đếm pixel trắng
num_pixels = cv2.countNonZero(mask)

# Chuyển sang cm²
area_cm2 = num_pixels / (pixels_per_metric ** 2)
```

## 🧮 Các Phép Đo Nâng Cao

### 1. Perimeter (Chu Vi)

```python
perimeter_pixels = cv2.arcLength(cnt, closed=True)
perimeter_cm = perimeter_pixels / pixels_per_metric
```

### 2. Aspect Ratio

```python
x, y, w, h = cv2.boundingRect(cnt)
aspect_ratio = float(w) / h

# Phân loại
if aspect_ratio > 1.2:
    shape = "Dài"
elif aspect_ratio < 0.8:
    shape = "Cao"
else:
    shape = "Vuông"
```

### 3. Equivalent Diameter

```python
# Đường kính của hình tròn có cùng diện tích
area = cv2.contourArea(cnt)
equi_diameter_pixels = np.sqrt(4 * area / np.pi)
equi_diameter_cm = equi_diameter_pixels / pixels_per_metric
```

### 4. Orientation (Góc Nghiêng)

```python
# Dùng minAreaRect
(x, y), (w, h), angle = cv2.minAreaRect(cnt)

# Hoặc dùng moments
def get_orientation(cnt):
    M = cv2.moments(cnt)
    if M['mu20'] - M['mu02'] == 0:
        return 0
    angle = 0.5 * np.arctan2(2 * M['mu11'], M['mu20'] - M['mu02'])
    return np.degrees(angle)

orientation = get_orientation(cnt)
```

## 📊 Độ Chính Xác và Sai Số

### Nguồn Sai Số

1. **Lens Distortion**: ±5-10%
   - Giải pháp: Camera calibration

2. **Perspective Error**: ±5-15%
   - Giải pháp: Camera vuông góc, cùng mặt phẳng

3. **Edge Detection Error**: ±1-3 pixels
   - Giải pháp: Blur + threshold tốt

4. **Vật Chuẩn Không Chính Xác**: Tùy thuộc
   - Giải pháp: Dùng vật chuẩn tốt (thước, marker in)

### Cải Thiện Độ Chính Xác

```python
# 1. Undistort ảnh (nếu có camera matrix)
undistorted = cv2.undistort(img, camera_matrix, dist_coeffs)

# 2. Dùng nhiều vật chuẩn, lấy trung bình
ppms = []
for ref_cnt in reference_contours:
    box = cv2.minAreaRect(ref_cnt)
    (x, y), (w, h), angle = box
    ppm = max(w, h) / COIN_DIAMETER_CM
    ppms.append(ppm)

pixels_per_metric = np.median(ppms)  # Robust hơn mean

# 3. Sub-pixel accuracy
corner = cv2.cornerSubPix(gray, corner_points, (5,5), (-1,-1), criteria)
```

## 🔬 Ví Dụ Hoàn Chỉnh

```python
import cv2
import numpy as np

def measure_objects(img_path, ref_width_cm=2.4):
    """
    Đo kích thước vật thể với đồng xu làm vật chuẩn

    Args:
        img_path: Đường dẫn ảnh
        ref_width_cm: Đường kính đồng xu (cm)
    """
    # 1. Đọc và tiền xử lý
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 1.5)

    # 2. Threshold + morphology
    _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)

    # 3. Contours
    cnts, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=lambda c: cv2.boundingRect(c)[0])  # Trái → phải

    # 4. Tìm vật chuẩn (leftmost)
    ref_cnt = cnts[0]
    box = cv2.minAreaRect(ref_cnt)
    ref_width_px = max(box[1])

    # 5. Tính PPM
    ppm = ref_width_px / ref_width_cm
    print(f"Pixels per cm: {ppm:.2f}")

    # 6. Đo các vật thể
    results = []
    for i, cnt in enumerate(cnts):
        if cv2.contourArea(cnt) < 500:
            continue

        # Bounding box xoay
        box = cv2.minAreaRect(cnt)
        box_pts = cv2.boxPoints(box)
        box_pts = np.int0(box_pts)

        # Kích thước
        (x, y), (w, h), angle = box
        width_cm = max(w, h) / ppm
        height_cm = min(w, h) / ppm

        # Diện tích
        area_px = cv2.contourArea(cnt)
        area_cm2 = area_px / (ppm ** 2)

        # Lưu kết quả
        results.append({
            'id': i,
            'width_cm': width_cm,
            'height_cm': height_cm,
            'area_cm2': area_cm2,
            'angle': angle
        })

        # Vẽ
        cv2.drawContours(img, [box_pts], 0, (0,255,0), 2)

        # Text
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        if i == 0:  # Vật chuẩn
            text = f"Ref: {width_cm:.1f} cm"
        else:
            text = f"{width_cm:.1f} x {height_cm:.1f} cm"

        cv2.putText(img, text, (cx-50, cy), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255,0,0), 2)

    # 7. Lưu
    cv2.imwrite('measured.jpg', img)

    return results, ppm

# Sử dụng
results, ppm = measure_objects('input.jpg', ref_width_cm=2.4)
for r in results:
    print(f"Object {r['id']}: {r['width_cm']:.2f} x {r['height_cm']:.2f} cm, "
          f"Area: {r['area_cm2']:.2f} cm²")
```

## 🚀 Kỹ Thuật Nâng Cao

### 1. ArUco Markers

Dùng marker QR-like cho calibration chính xác:

```python
import cv2.aruco as aruco

# Tạo marker
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
marker = aruco.drawMarker(aruco_dict, 0, 200)

# Detect marker
corners, ids, _ = aruco.detectMarkers(gray, aruco_dict)

# Tính PPM từ marker size
if ids is not None:
    marker_width_px = np.linalg.norm(corners[0][0][0] - corners[0][0][1])
    MARKER_SIZE_CM = 5.0
    ppm = marker_width_px / MARKER_SIZE_CM
```

### 2. Camera Calibration

```python
# Undistort với camera matrix
undistorted = cv2.undistort(img, mtx, dist)

# Hoặc dùng remapping (nhanh hơn)
h, w = img.shape[:2]
new_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, new_mtx, (w,h), 5)
undistorted = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
```

### 3. 3D Measurement (Stereo)

Dùng 2 camera → depth → 3D measurement

## 📚 Tài Liệu Tham Khảo

- OpenCV Documentation: Camera Calibration
- Zhang, Z. (2000). A Flexible New Technique for Camera Calibration
- ArUco Markers Documentation

## 🔗 Liên Kết

**Bài thực hành**:
- **Bài 9**: Object measurement (coin reference)

**Lý thuyết liên quan**:
- **04-contour-detection.md**: Tìm contours để đo
- **05-perspective-transform.md**: Sửa perspective error

---

**Tác giả**: Dựa trên PDF T21-40 Tách Biên
**Cập nhật**: 2025
