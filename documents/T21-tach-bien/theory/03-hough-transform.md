# Lý Thuyết 3: Hough Transform

## 📋 Tổng Quan

**Hough Transform** là kỹ thuật phát hiện hình dạng đơn giản (đường thẳng, đường tròn, ellipse) trong ảnh. Phát minh năm 1962 bởi Paul Hough, được cải tiến bởi Richard Duda và Peter Hart năm 1972.

**Ý tưởng cốt lõi**: Chuyển bài toán từ **image space** sang **parameter space** để dễ phát hiện hình dạng.

## 🎯 Ứng Dụng

- **Bài 3**: Phát hiện làn đường (Hough Lines)
- **Bài 5**: Đếm đồng xu (Hough Circles)

**Ứng dụng khác**:
- Lane detection trong xe tự lái
- Phát hiện vật tròn (bánh xe, lon, đồng xu)
- Architectural analysis (tìm cạnh tòa nhà)
- Medical imaging (phát hiện mạch máu)

## 📐 Hough Lines: Phát Hiện Đường Thẳng

### Biểu Diễn Đường Thẳng

#### Cách 1: y = mx + c (Không Tối Ưu)
- ❌ Không biểu diễn được đường thẳng đứng (m = ∞)
- ❌ m có thể rất lớn → khó xử lý

#### Cách 2: Polar Coordinates ⭐ CHUẨN

```
ρ = x*cos(θ) + y*sin(θ)
```

**Tham số**:
- `ρ` (rho): Khoảng cách từ gốc toạ độ đến đường thẳng
- `θ` (theta): Góc từ trục x đến đường vuông góc với đường thẳng

**Ưu điểm**:
- ✅ Biểu diễn được mọi đường thẳng
- ✅ Tham số bị chặn: `ρ ∈ [0, √(w²+h²)]`, `θ ∈ [0, π]`
- ✅ Dễ discretize thành bins

### Nguyên Lý Hough Transform

**Image Space → Parameter Space**:

1. **Image space**: Mỗi điểm (x, y) là 1 pixel biên
2. **Parameter space**: Mỗi điểm (ρ, θ) là 1 đường thẳng

**Voting (Bỏ phiếu)**:

- Mỗi pixel biên (x, y) → vẽ đường cong trong parameter space
- Đường cong này biểu diễn TẤT CẢ đường thẳng đi qua (x, y)
- Nhiều pixel thẳng hàng → các đường cong giao nhau tại 1 điểm
- Điểm có nhiều vote nhất = đường thẳng thực sự

**Ví dụ**:
```
Image space: 3 điểm (x1,y1), (x2,y2), (x3,y3) thẳng hàng
              ↓
Parameter space: 3 đường cong giao nhau tại (ρ₀, θ₀)
              ↓
Kết quả: Đường thẳng ρ = ρ₀, θ = θ₀
```

### OpenCV: Standard Hough Lines

```python
lines = cv2.HoughLines(edges, rho=1, theta=np.pi/180, threshold=100)
```

**Tham số**:
- `edges`: Ảnh biên nhị phân (từ Canny/Sobel)
- `rho`: Độ phân giải ρ (pixel) - thường dùng `1`
- `theta`: Độ phân giải θ (radian) - thường dùng `π/180` (1 độ)
- `threshold`: Số vote tối thiểu để coi là đường thẳng

**Output**: Array của `(ρ, θ)`

**Vẽ đường thẳng**:
```python
for rho, theta in lines[:,0]:
    a, b = np.cos(theta), np.sin(theta)
    x0, y0 = a*rho, b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 2)
```

### OpenCV: Probabilistic Hough Lines ⭐ PHỔ BIẾN HƠN

```python
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50,
                        minLineLength=50, maxLineGap=10)
```

**Tham số thêm**:
- `minLineLength`: Độ dài tối thiểu của đoạn thẳng
- `maxLineGap`: Khoảng cách tối đa giữa 2 điểm để vẫn coi là 1 đường

**Output**: Array của `(x1, y1, x2, y2)` - tọa độ 2 đầu đoạn thẳng

**Ưu điểm**:
- ✅ Trả về đoạn thẳng, không phải đường thẳng vô hạn
- ✅ Dễ sử dụng hơn
- ✅ Nhanh hơn (probabilistic sampling)
- ✅ Phù hợp hầu hết ứng dụng

**Vẽ đường thẳng**:
```python
for x1, y1, x2, y2 in lines[:,0]:
    cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 2)
```

### Ví Dụ: Lane Detection

```python
# 1. Tiền xử lý
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 1.2)

# 2. ROI mask
h, w = img.shape[:2]
roi = np.array([[(int(w*0.1), h), (int(w*0.45), int(h*0.6)),
                  (int(w*0.55), int(h*0.6)), (int(w*0.9), h)]])
mask = np.zeros_like(gray)
cv2.fillPoly(mask, roi, 255)

# 3. Edge detection
edges = cv2.Canny(blur, 50, 150)
edges = cv2.bitwise_and(edges, mask)

# 4. Hough Lines
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 60,
                        minLineLength=50, maxLineGap=150)

# 5. Phân loại trái/phải dựa vào slope
left_lines, right_lines = [], []
for x1, y1, x2, y2 in lines[:,0]:
    if x2 == x1:
        continue
    slope = (y2 - y1) / (x2 - x1)
    if slope < -0.5:  # Làn trái
        left_lines.append((x1, y1, x2, y2))
    elif slope > 0.5:  # Làn phải
        right_lines.append((x1, y1, x2, y2))

# 6. Vẽ kết quả
for x1, y1, x2, y2 in left_lines:
    cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 3)
for x1, y1, x2, y2 in right_lines:
    cv2.line(img, (x1,y1), (x2,y2), (255,0,0), 3)
```

### Mẹo Chọn Tham Số Hough Lines

**threshold**:
- Cao (100-150): Chỉ lấy đường thẳng dài, rõ ràng
- Thấp (30-60): Lấy cả đường thẳng ngắn, mờ

**minLineLength**:
- Lớn (100+): Chỉ lấy đường dài → ít nhiễu
- Nhỏ (20-50): Lấy cả đường ngắn → nhiều kết quả

**maxLineGap**:
- Nhỏ (5-20): Đường phải liền khít
- Lớn (50-200): Cho phép gián đoạn (lane marking)

## 🔵 Hough Circles: Phát Hiện Đường Tròn

### Biểu Diễn Đường Tròn

```
(x - a)² + (y - b)² = r²
```

**Parameter space**: 3D `(a, b, r)`
- `(a, b)`: Tâm đường tròn
- `r`: Bán kính

### OpenCV: Hough Circles

```python
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                           param1=50, param2=30, minRadius=10, maxRadius=50)
```

**Tham số**:
- `gray`: Ảnh grayscale (KHÔNG cần edges)
- `cv2.HOUGH_GRADIENT`: Phương pháp (hiện chỉ có 1 loại)
- `dp=1`: Tỉ lệ độ phân giải accumulator (1 = giống ảnh gốc)
- `minDist`: Khoảng cách tối thiểu giữa 2 tâm
- `param1`: Ngưỡng cao cho Canny (thấp = param1/2)
- `param2`: Ngưỡng accumulator (vote tối thiểu)
- `minRadius`, `maxRadius`: Giới hạn bán kính

**Output**: Array của `(x, y, r)`

**Vẽ kết quả**:
```python
if circles is not None:
    circles = np.uint16(np.around(circles))
    for x, y, r in circles[0]:
        cv2.circle(img, (x, y), r, (0, 255, 0), 2)  # Viền
        cv2.circle(img, (x, y), 2, (0, 0, 255), 3)  # Tâm
```

### Ví Dụ: Coin Counting

```python
# 1. Đọc và làm mờ
img = cv2.imread('coins.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (9,9), 2.0)

# 2. Hough Circles
circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=1, minDist=30,
                           param1=50, param2=30, minRadius=15, maxRadius=60)

# 3. Đếm và vẽ
if circles is not None:
    circles = np.uint16(np.around(circles))
    count = len(circles[0])
    print(f"Tìm thấy {count} đồng xu")

    for x, y, r in circles[0]:
        cv2.circle(img, (x, y), r, (0, 255, 0), 2)
        cv2.circle(img, (x, y), 2, (0, 0, 255), 3)
```

### Mẹo Chọn Tham Số Hough Circles

**minDist**:
- Nhỏ (10-20): Cho phép đường tròn gần nhau
- Lớn (50+): Tránh phát hiện nhầm

**param1** (Canny threshold):
- Cao (100+): Chỉ lấy biên rõ → ít false positive
- Thấp (30-50): Lấy cả biên mờ → nhiều kết quả

**param2** (Accumulator threshold):
- Cao (40-50): Chỉ lấy đường tròn hoàn hảo → ít kết quả
- Thấp (20-30): Chấp nhận đường tròn không hoàn hảo → nhiều kết quả

**minRadius, maxRadius**:
- Giới hạn chặt nếu biết kích thước vật thể
- Ví dụ đồng xu: `minRadius=15, maxRadius=60`

## 📊 So Sánh Hough Lines vs Hough Circles

| Tiêu Chí | Hough Lines | Hough Circles |
|----------|-------------|---------------|
| **Parameter space** | 2D (ρ, θ) | 3D (a, b, r) |
| **Tốc độ** | Nhanh ⭐ | Chậm hơn |
| **Độ phức tạp** | O(N²) | O(N³) |
| **Độ chính xác** | Cao | Vừa phải |
| **Input** | Edges (Canny) ⭐ | Grayscale |
| **False positive** | Ít | Nhiều hơn |

## 🎚️ Workflow Tối Ưu

### Cho Hough Lines

```python
1. Grayscale conversion
2. Gaussian blur (σ=1.0-1.5)
3. Canny edge detection
4. ROI masking (nếu cần)
5. Morphological operations (nếu cần nối biên)
6. HoughLinesP
7. Filter theo slope/length
```

### Cho Hough Circles

```python
1. Grayscale conversion
2. Gaussian blur (σ=2.0-3.0, kernel lớn)
3. Morphological opening (nếu có nhiễu)
4. HoughCircles (KHÔNG cần Canny trước)
5. Filter theo radius/position
```

## 🔬 Ưu Nhược Điểm

### Hough Transform - Ưu Điểm
- ✅ Robust với nhiễu, occlusion (che khuất)
- ✅ Tìm được nhiều hình cùng lúc
- ✅ Không cần biên liền mạch
- ✅ Toán học đơn giản, dễ hiểu

### Hough Transform - Nhược Điểm
- ❌ Chậm (đặc biệt Hough Circles)
- ❌ Cần nhiều bộ nhớ (accumulator array)
- ❌ Nhiều tham số cần điều chỉnh
- ❌ Chỉ tốt với hình đơn giản (thẳng, tròn)

## 🚀 Cải Tiến và Biến Thể

### 1. Progressive Probabilistic Hough Transform
- Dùng random sampling thay vì check mọi pixel
- Nhanh hơn 10-100 lần
- `HoughLinesP` trong OpenCV đã dùng kỹ thuật này

### 2. Gradient-Weighted Hough
- Dùng thêm thông tin gradient direction
- Giảm false positive
- Tăng độ chính xác

### 3. Generalized Hough Transform
- Phát hiện hình bất kỳ (không chỉ thẳng/tròn)
- Cần template của hình cần tìm
- Chậm hơn nhiều

### 4. GPU Acceleration
- OpenCV CUDA module có Hough GPU
- Nhanh hơn 50-100 lần
- Phù hợp video real-time

## 🧪 Debugging Tips

### Lines Không Phát Hiện Được

```python
# 1. Kiểm tra edges
cv2.imshow('Edges', edges)  # Phải thấy đường rõ ràng

# 2. Giảm threshold
lines = cv2.HoughLinesP(..., threshold=30)  # Thay vì 60

# 3. Tăng maxLineGap
lines = cv2.HoughLinesP(..., maxLineGap=200)  # Cho phép gián đoạn

# 4. Giảm minLineLength
lines = cv2.HoughLinesP(..., minLineLength=20)  # Lấy cả đường ngắn
```

### Circles Phát Hiện Sai

```python
# 1. Tăng Gaussian blur
blur = cv2.GaussianBlur(gray, (11,11), 3.0)  # Kernel lớn hơn

# 2. Điều chỉnh param2
circles = cv2.HoughCircles(..., param2=25)  # Giảm để lấy nhiều hơn

# 3. Đặt minDist hợp lý
circles = cv2.HoughCircles(..., minDist=50)  # Tránh overlap

# 4. Kiểm tra radius range
circles = cv2.HoughCircles(..., minRadius=20, maxRadius=80)
```

## 📚 Tài Liệu Tham Khảo

- **Hough, P.** (1962). Method and means for recognizing complex patterns
- **Duda, R. & Hart, P.** (1972). Use of the Hough transformation to detect lines and curves in pictures
- OpenCV Documentation: Hough Transform
- [Tutorial hay](https://docs.opencv.org/4.x/d9/db0/tutorial_hough_lines.html)

## 🔗 Liên Kết

**Bài thực hành**:
- **Bài 3**: Lane detection (HoughLinesP + slope filtering)
- **Bài 5**: Coin counting (HoughCircles)

**Lý thuyết liên quan**:
- **02-canny-edge-detection.md**: Tiền xử lý cho Hough Lines
- **04-contour-detection.md**: Phương pháp thay thế cho hình phức tạp

---

**Tác giả**: Dựa trên PDF T21-40 Tách Biên
**Cập nhật**: 2025
