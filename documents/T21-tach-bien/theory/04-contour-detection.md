# Lý Thuyết 4: Phát Hiện và Phân Tích Contour

## 📋 Tổng Quan

**Contour** là đường cong liền nối các điểm có cùng màu sắc hoặc cường độ. Trong xử lý ảnh, contour thường là **biên của vật thể**.

**Khác biệt Edges vs Contours**:
- **Edges**: Tập hợp các pixel có gradient cao (có thể rời rạc)
- **Contours**: Đường cong **liền mạch** bao quanh vật thể

## 🎯 Ứng Dụng

- **Bài 6**: Cắt nền sản phẩm (contour → bounding box → crop)
- **Bài 8**: Tính diện tích lá cây (contourArea + moments)

**Ứng dụng khác**:
- Object detection/segmentation
- Shape analysis
- Gesture recognition
- Medical imaging
- Quality control

## 📐 Tìm Contours Trong OpenCV

### cv2.findContours()

```python
contours, hierarchy = cv2.findContours(binary, mode, method)
```

**Input**:
- `binary`: Ảnh nhị phân (0 hoặc 255), thường từ Canny/threshold

**Tham số**:
- `mode`: Chế độ lấy contour (RETR_*)
- `method`: Phương pháp xấp xỉ (CHAIN_APPROX_*)

**Output**:
- `contours`: List các contour, mỗi contour là array `(N, 1, 2)` tọa độ
- `hierarchy`: Thông tin phân cấp (contour cha-con)

### Retrieval Mode (RETR_*)

#### 1. RETR_EXTERNAL ⭐ PHỔ BIẾN NHẤT

```python
cnts, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

- Chỉ lấy contour ngoài cùng
- Bỏ qua holes (lỗ bên trong)
- **Dùng khi**: Tìm vật thể, không quan tâm chi tiết bên trong

#### 2. RETR_LIST

- Lấy TẤT CẢ contours, không phân cấp
- Không có quan hệ cha-con
- **Dùng khi**: Cần tất cả contours, không quan tâm hierarchy

#### 3. RETR_TREE

- Lấy tất cả + phân cấp đầy đủ
- Hierarchy chứa thông tin [next, previous, first_child, parent]
- **Dùng khi**: Cần phân tích cấu trúc lồng nhau

#### 4. RETR_CCOMP

- Phân 2 cấp: bên ngoài và holes
- **Dùng khi**: Cần phân biệt vật thể và lỗ

### Approximation Method (CHAIN_APPROX_*)

#### 1. CHAIN_APPROX_SIMPLE ⭐ KHUYẾN NGHỊ

```python
cnts, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

- Chỉ lưu các điểm góc
- Ví dụ: Hình chữ nhật chỉ lưu 4 điểm
- ✅ Tiết kiệm bộ nhớ
- ✅ Nhanh hơn

#### 2. CHAIN_APPROX_NONE

- Lưu TẤT CẢ điểm biên
- Ví dụ: Hình chữ nhật 100×50 → lưu 300 điểm
- ❌ Tốn bộ nhớ
- **Dùng khi**: Cần contour chính xác tuyệt đối

## 🔧 Xử Lý Contours

### 1. Vẽ Contours

```python
# Vẽ tất cả contours
cv2.drawContours(img, contours, -1, (0,255,0), 2)

# Vẽ contour thứ i
cv2.drawContours(img, contours, i, (0,255,0), 2)

# Vẽ filled
cv2.drawContours(img, contours, -1, (0,255,0), -1)  # thickness=-1
```

### 2. Contour Area (Diện Tích)

```python
area = cv2.contourArea(cnt)
```

- Đơn vị: pixel²
- Dùng để filter contours (loại bỏ nhiễu nhỏ)

**Ví dụ**:
```python
# Chỉ giữ contours lớn (> 1000 pixel²)
large_cnts = [c for c in contours if cv2.contourArea(c) > 1000]
```

### 3. Perimeter (Chu Vi)

```python
perimeter = cv2.arcLength(cnt, closed=True)
```

- `closed=True`: Contour khép kín
- Dùng để tính **circularity**, **compactness**

### 4. Bounding Rectangle

#### Upright Bounding Rectangle
```python
x, y, w, h = cv2.boundingRect(cnt)
cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)
```

- Hình chữ nhật thẳng đứng
- **Dùng khi**: Crop vật thể, OCR

#### Rotated Bounding Rectangle
```python
rect = cv2.minAreaRect(cnt)  # ((cx,cy), (w,h), angle)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(img, [box], 0, (0,255,0), 2)
```

- Hình chữ nhật xoay, diện tích nhỏ nhất
- **Dùng khi**: Tính góc nghiêng, tight crop

### 5. Minimum Enclosing Circle

```python
(x, y), radius = cv2.minEnclosingCircle(cnt)
center = (int(x), int(y))
radius = int(radius)
cv2.circle(img, center, radius, (0,255,0), 2)
```

- Đường tròn nhỏ nhất bao contour
- **Dùng khi**: Kiểm tra độ tròn, estimate size

### 6. Contour Approximation (Xấp Xỉ)

```python
epsilon = 0.01 * cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, epsilon, True)
```

- **Douglas-Peucker algorithm**
- `epsilon`: Độ chính xác (nhỏ = chính xác hơn)
- Giảm số điểm trong contour

**Ví dụ**:
```python
# Phát hiện hình dạng
num_vertices = len(approx)
if num_vertices == 3:
    shape = "Triangle"
elif num_vertices == 4:
    shape = "Rectangle"
elif num_vertices > 6:
    shape = "Circle"
```

### 7. Convex Hull

```python
hull = cv2.convexHull(cnt)
cv2.drawContours(img, [hull], 0, (0,255,0), 2)
```

- Bao lồi của contour
- **Dùng khi**: Hand gesture recognition, defect detection

### 8. Moments

```python
M = cv2.moments(cnt)
```

- Tính các moment toán học
- **Ứng dụng**: Tìm trọng tâm, tính orientation

**Trọng tâm (Centroid)**:
```python
cx = int(M['m10'] / M['m00'])
cy = int(M['m01'] / M['m00'])
```

**Diện tích**:
```python
area = M['m00']  # Tương đương cv2.contourArea(cnt)
```

## 🎚️ Workflow Thực Tế

### Workflow 1: Object Cropping (Bài 6)

```python
# 1. Edges
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 1.0)
edges = cv2.Canny(blur, 50, 150)

# 2. Morphology để đóng khe hở
kernel = np.ones((5,5), np.uint8)
closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
dilated = cv2.dilate(closed, kernel, iterations=2)

# 3. Tìm contours
cnts, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 4. Chọn contour lớn nhất
cnt = max(cnts, key=cv2.contourArea)

# 5. Bounding rectangle
x, y, w, h = cv2.boundingRect(cnt)

# 6. Crop
cropped = img[y:y+h, x:x+w]

# 7. Tạo mask cho alpha channel
mask = np.zeros(gray.shape, np.uint8)
cv2.drawContours(mask, [cnt], -1, 255, thickness=-1)
mask_crop = mask[y:y+h, x:x+w]

# 8. BGRA
bgra = cv2.cvtColor(cropped, cv2.COLOR_BGR2BGRA)
bgra[:, :, 3] = mask_crop
cv2.imwrite('output.png', bgra)
```

### Workflow 2: Area Measurement (Bài 8)

```python
# 1. Threshold để tách vật thể
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 2. Tìm contours
cnts, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 3. Filter theo diện tích (loại nhiễu)
cnts = [c for c in cnts if cv2.contourArea(c) > 500]

# 4. Tính diện tích từng contour
for cnt in cnts:
    area = cv2.contourArea(cnt)
    M = cv2.moments(cnt)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])

    # Vẽ contour
    cv2.drawContours(img, [cnt], -1, (0,255,0), 2)

    # Ghi diện tích
    cv2.putText(img, f"{area:.0f}px", (cx, cy),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
```

## 📊 Các Đặc Trưng Hình Dạng

### 1. Aspect Ratio

```python
x, y, w, h = cv2.boundingRect(cnt)
aspect_ratio = float(w) / h
```

- Tỉ lệ chiều rộng/chiều cao
- **Ứng dụng**: Phân loại hình (dọc/ngang)

### 2. Extent (Độ Đầy)

```python
area = cv2.contourArea(cnt)
x, y, w, h = cv2.boundingRect(cnt)
rect_area = w * h
extent = float(area) / rect_area
```

- Tỉ lệ diện tích contour / bounding box
- Giá trị: 0-1
- Hình chữ nhật: extent ≈ 1
- Hình phức tạp: extent < 0.7

### 3. Solidity (Độ Đặc)

```python
area = cv2.contourArea(cnt)
hull = cv2.convexHull(cnt)
hull_area = cv2.contourArea(hull)
solidity = float(area) / hull_area
```

- Tỉ lệ diện tích contour / convex hull
- Giá trị: 0-1
- Hình lồi: solidity ≈ 1
- Hình có lõm: solidity < 0.9

### 4. Circularity (Độ Tròn)

```python
area = cv2.contourArea(cnt)
perimeter = cv2.arcLength(cnt, True)
circularity = 4 * np.pi * area / (perimeter ** 2)
```

- Giá trị: 0-1
- Hình tròn hoàn hảo: circularity = 1
- Hình dài: circularity < 0.5

## 🔬 Ưu Nhược Điểm

### Contours - Ưu Điểm
- ✅ Cho thông tin hình dạng đầy đủ
- ✅ Nhiều thuộc tính: area, perimeter, moments
- ✅ Dễ filter, phân loại
- ✅ Hỗ trợ hierarchy (cha-con)
- ✅ Hiệu quả với vật thể rõ ràng

### Contours - Nhược Điểm
- ❌ Cần ảnh nhị phân chất lượng
- ❌ Nhạy với nhiễu (cần morphology)
- ❌ Kém với vật thể chồng lấn
- ❌ Kém với texture phức tạp

## 🚀 Kỹ Thuật Nâng Cao

### 1. Contour Filtering

```python
# Filter theo diện tích
MIN_AREA, MAX_AREA = 1000, 50000
filtered = [c for c in contours
            if MIN_AREA < cv2.contourArea(c) < MAX_AREA]

# Filter theo aspect ratio
filtered = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    aspect = float(w) / h
    if 0.8 < aspect < 1.2:  # Gần vuông
        filtered.append(c)

# Filter theo circularity
filtered = []
for c in contours:
    area = cv2.contourArea(c)
    perimeter = cv2.arcLength(c, True)
    circularity = 4 * np.pi * area / (perimeter ** 2)
    if circularity > 0.7:  # Gần tròn
        filtered.append(c)
```

### 2. Contour Sorting

```python
# Sắp xếp theo diện tích (lớn nhất trước)
sorted_cnts = sorted(contours, key=cv2.contourArea, reverse=True)

# Sắp xếp trái → phải
def get_x(c):
    M = cv2.moments(c)
    return int(M['m10'] / M['m00'])
sorted_cnts = sorted(contours, key=get_x)

# Sắp xếp trên → dưới
def get_y(c):
    M = cv2.moments(c)
    return int(M['m01'] / M['m00'])
sorted_cnts = sorted(contours, key=get_y)
```

### 3. Contour Merging

```python
# Merge contours gần nhau
from scipy.spatial import distance

def merge_close_contours(contours, threshold=50):
    # Tính centroid mỗi contour
    centroids = []
    for c in contours:
        M = cv2.moments(c)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        centroids.append((cx, cy))

    # Merge gần nhau
    merged = []
    used = set()
    for i, c1 in enumerate(contours):
        if i in used:
            continue
        group = [c1]
        for j, c2 in enumerate(contours[i+1:], i+1):
            if j in used:
                continue
            dist = distance.euclidean(centroids[i], centroids[j])
            if dist < threshold:
                group.append(c2)
                used.add(j)

        # Merge group
        merged_cnt = np.vstack(group)
        merged.append(merged_cnt)

    return merged
```

## 🧪 Debugging Tips

### Không Tìm Thấy Contour

```python
# 1. Kiểm tra binary image
cv2.imshow('Binary', binary)  # Phải thấy vật thể trắng, nền đen

# 2. Thử invert
binary_inv = cv2.bitwise_not(binary)
cnts, _ = cv2.findContours(binary_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 3. Morphology để đóng khe hở
kernel = np.ones((5,5), np.uint8)
closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
cnts, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 4. Giảm ngưỡng
_, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)  # Thay vì 127
```

### Quá Nhiều Contours Nhỏ (Nhiễu)

```python
# 1. Filter theo area
min_area = 500
cnts = [c for c in contours if cv2.contourArea(c) > min_area]

# 2. Morphology opening
kernel = np.ones((3,3), np.uint8)
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

# 3. Gaussian blur mạnh hơn trước threshold
blur = cv2.GaussianBlur(gray, (9,9), 2.0)
```

## 📚 Tài Liệu Tham Khảo

- OpenCV Documentation: Contours
- Suzuki, S. (1985). Topological structural analysis of digitized binary images (thuật toán findContours)
- OpenCV Tutorials: Contours - Getting Started

## 🔗 Liên Kết

**Bài thực hành**:
- **Bài 6**: Product cropping (contour → crop → alpha)
- **Bài 8**: Leaf area calculation (contourArea + moments)

**Lý thuyết liên quan**:
- **02-canny-edge-detection.md**: Tiền xử lý edges
- **06-morphological-edge-processing.md**: Morphology cho contours tốt hơn

---

**Tác giả**: Dựa trên PDF T21-40 Tách Biên
**Cập nhật**: 2025
