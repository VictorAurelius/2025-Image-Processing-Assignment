# Lý Thuyết 2: Thuật Toán Canny Edge Detection

## 📋 Tổng Quan

**Canny Edge Detector** (1986) là thuật toán phát hiện biên "tối ưu" được phát triển bởi John F. Canny. Đây là thuật toán phổ biến nhất trong Computer Vision nhờ 3 tiêu chí tối ưu:

1. **Good Detection**: Tìm được tất cả biên thực sự, ít false positive
2. **Good Localization**: Biên phát hiện gần với biên thực tế
3. **Single Response**: Mỗi biên chỉ được đánh dấu 1 lần (biên mảnh 1 pixel)

## 🎯 Ứng Dụng

Canny được dùng rộng rãi trong:
- **Document scanning**: Tìm viền giấy
- **Lane detection**: Phát hiện làn đường
- **Object detection**: Tiền xử lý trước khi tìm contour
- **Medical imaging**: Phân đoạn cơ quan
- **OCR**: Tách ký tự

## 📐 5 Bước Của Thuật Toán Canny

### Bước 1: Làm Mờ Gaussian

**Mục đích**: Giảm nhiễu trước khi lấy đạo hàm

```python
blur = cv2.GaussianBlur(img, (5,5), sigma=1.4)
```

**Kernel Gaussian**:
```
G(x,y) = (1/(2πσ²)) * exp(-(x²+y²)/(2σ²))
```

**Tham số**:
- `ksize = (5,5)` hoặc `(7,7)`: Kích thước kernel
- `sigma = 1.4`: Độ mạnh làm mờ (Canny gốc dùng 1.4)

**Lưu ý**:
- Sigma càng lớn → giảm nhiễu tốt nhưng mất chi tiết
- Kernel lớn → chậm hơn

### Bước 2: Tính Gradient (Sobel)

**Gradient theo x và y**:
```python
gx = cv2.Sobel(blur, cv2.CV_32F, 1, 0, ksize=3)
gy = cv2.Sobel(blur, cv2.CV_32F, 0, 1, ksize=3)
```

**Magnitude (cường độ)**:
```python
mag = np.sqrt(gx**2 + gy**2)
```

**Direction (hướng)**:
```python
theta = np.arctan2(gy, gx) * 180 / np.pi
```

**Quantize direction** thành 4 hướng:
- 0°: Ngang (→)
- 45°: Chéo phải-trên (↗)
- 90°: Dọc (↑)
- 135°: Chéo trái-trên (↖)

### Bước 3: Non-Maximum Suppression (NMS) ⭐ QUAN TRỌNG

**Mục đích**: Làm mảnh biên từ vài pixel xuống còn 1 pixel

**Nguyên lý**:
- Với mỗi pixel, xem xét 2 pixel láng giềng **theo hướng gradient**
- Nếu magnitude của pixel hiện tại < 2 láng giềng → loại bỏ
- Ngược lại → giữ lại

**Ví dụ**:
```
Gradient hướng 0° (ngang)
Magnitude:  10  [50]  30
            ↑    ↑    ↑
         trái  tại   phải

50 > 10 và 50 > 30 → Giữ 50
Ngược lại → Loại bỏ (set = 0)
```

**Kết quả**: Biên mảnh, rõ nét, chính xác vị trí

### Bước 4: Double Thresholding (Ngưỡng Kép)

**2 ngưỡng**:
- `T_high` (ngưỡng cao): Pixel chắc chắn là biên → **Strong edge**
- `T_low` (ngưỡng thấp): Pixel có thể là biên → **Weak edge**

```python
strong = (mag >= T_high)
weak = (mag >= T_low) & (mag < T_high)
```

**Tỉ lệ thường dùng**:
```
T_high = 0.3 * mag.max()
T_low = 0.5 * T_high  # hoặc 0.4 * T_high
```

**Phân loại pixel**:
- `mag >= T_high`: **Strong edge** (255)
- `T_low <= mag < T_high`: **Weak edge** (128)
- `mag < T_low`: **Non-edge** (0)

### Bước 5: Edge Tracking by Hysteresis

**Mục đích**: Kết nối các biên, loại bỏ noise

**Nguyên lý**:
1. Giữ lại TẤT CẢ **strong edges**
2. Với mỗi **weak edge**:
   - Nếu liền kề (8-connected) với strong edge → **GIỮ LẠI**
   - Ngược lại → **LOẠI BỎ** (coi là nhiễu)

**Ví dụ**:
```
Trước:
255  128  128   0     (255=strong, 128=weak, 0=non-edge)
  0  128    0   0

Sau hysteresis:
255  255  255   0     (weak liền strong → thành strong)
  0    0    0   0     (weak riêng lẻ → loại bỏ)
```

**Kết quả**: Biên liền mạch, ít nhiễu

## 🔧 Sử Dụng OpenCV

### Cách 1: Hàm Canny Có Sẵn (Đơn Giản)

```python
edges = cv2.Canny(img, threshold1=50, threshold2=150)
```

**Tham số**:
- `threshold1`: T_low (ngưỡng thấp)
- `threshold2`: T_high (ngưỡng cao)
- `apertureSize=3`: Kích thước Sobel kernel (3, 5, 7)
- `L2gradient=False`: Dùng L1 norm (|Gx| + |Gy|) thay vì L2 (sqrt)

**Mẹo chọn ngưỡng**:
```python
# Cách 1: Cố định
T_low, T_high = 50, 150

# Cách 2: Tự động theo median
median = np.median(img)
T_low = int(max(0, 0.7 * median))
T_high = int(min(255, 1.3 * median))

# Cách 3: Theo phần trăm
mag = cv2.Sobel(img, cv2.CV_32F, 1, 0) + cv2.Sobel(img, cv2.CV_32F, 0, 1)
T_high = 0.3 * mag.max()
T_low = 0.5 * T_high
```

### Cách 2: Tự Implement (Học Thuật)

```python
# 1. Gaussian blur
blur = cv2.GaussianBlur(img, (5,5), 1.4)

# 2. Sobel gradient
gx = cv2.Sobel(blur, cv2.CV_32F, 1, 0, ksize=3)
gy = cv2.Sobel(blur, cv2.CV_32F, 0, 1, ksize=3)
mag = np.sqrt(gx**2 + gy**2)
theta = np.arctan2(gy, gx)

# 3. Non-maximum suppression (tự viết hàm)
mag_thin = non_maximum_suppression(mag, theta)

# 4. Double threshold
T_high = 0.3 * mag_thin.max()
T_low = 0.5 * T_high
strong = (mag_thin >= T_high).astype(np.uint8) * 255
weak = ((mag_thin >= T_low) & (mag_thin < T_high)).astype(np.uint8) * 128

# 5. Hysteresis (tự viết hàm)
edges = hysteresis_tracking(strong, weak)
```

## 📊 So Sánh Canny vs Sobel

| Tiêu Chí | Sobel | Canny |
|----------|-------|-------|
| **Biên** | Dày (2-3 pixel) | Mảnh (1 pixel) ⭐ |
| **Nhiễu** | Nhiều | Ít ⭐ |
| **Độ chính xác** | Vừa | Cao ⭐ |
| **Tốc độ** | Nhanh ⭐ | Chậm hơn |
| **Tham số** | 1 (ngưỡng) | 2 (T_low, T_high) |
| **Kết nối biên** | Không | Có (hysteresis) ⭐ |
| **Ứng dụng** | Real-time cơ bản | Chất lượng cao |

## 🎚️ Điều Chỉnh Tham Số

### 1. Gaussian Sigma

```python
# Ảnh sạch, nhiều chi tiết
blur = cv2.GaussianBlur(img, (3,3), 0.8)  # Sigma nhỏ

# Ảnh nhiễu vừa
blur = cv2.GaussianBlur(img, (5,5), 1.4)  # Chuẩn

# Ảnh nhiễu nặng
blur = cv2.GaussianBlur(img, (7,7), 2.0)  # Sigma lớn
```

### 2. Ngưỡng Canny

**Ngưỡng cao** (ví dụ: `100, 200`):
- ✅ Ít nhiễu
- ❌ Mất biên yếu

**Ngưỡng thấp** (ví dụ: `30, 80`):
- ✅ Tìm được biên yếu
- ❌ Nhiều nhiễu

**Tỉ lệ T_high : T_low**:
- Chuẩn: `1:2` hoặc `1:3`
- Ví dụ: `50:150`, `60:180`, `100:200`

### 3. Sobel Kernel Size

```python
# Kernel nhỏ = chi tiết nhiều, nhiễu nhiều
edges = cv2.Canny(img, 50, 150, apertureSize=3)

# Kernel lớn = mượt hơn, chậm hơn
edges = cv2.Canny(img, 50, 150, apertureSize=5)
```

## 🧪 Ví Dụ Thực Hành

### Ví Dụ 1: Document Scanning

```python
# Đọc ảnh giấy tờ
img = cv2.imread('document.jpg', cv2.IMREAD_GRAYSCALE)

# Canny với ngưỡng cao (chỉ lấy biên rõ)
edges = cv2.Canny(img, 100, 200)

# Tìm contours để lấy viền giấy
cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

### Ví Dụ 2: Lane Detection

```python
# ROI mask (chỉ xét phần đường phía trước)
mask = np.zeros_like(img)
roi = np.array([[(100, height), (width-100, height),
                  (width//2+50, height//2), (width//2-50, height//2)]])
cv2.fillPoly(mask, roi, 255)

# Canny trên ROI
blur = cv2.GaussianBlur(img, (5,5), 1.0)
edges = cv2.Canny(blur, 50, 150)
edges = cv2.bitwise_and(edges, mask)

# Hough Lines để tìm làn
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=150)
```

## 🔬 Ưu Nhược Điểm

### Ưu Điểm
- ✅ Biên mảnh 1 pixel (tốt nhất)
- ✅ Ít nhiễu nhờ Gaussian + hysteresis
- ✅ Kết nối biên tốt
- ✅ Chuẩn công nghiệp (30+ năm)
- ✅ Có sẵn trong mọi thư viện CV

### Nhược Điểm
- ❌ Chậm hơn Sobel (5 bước)
- ❌ Cần điều chỉnh 2 ngưỡng
- ❌ Không tốt với texture phức tạp
- ❌ Yếu với biên mờ, gradient thấp

## 🚀 Cải Tiến và Biến Thể

### 1. Auto Canny

Tự động chọn ngưỡng theo median:

```python
def auto_canny(img, sigma=0.33):
    median = np.median(img)
    lower = int(max(0, (1.0 - sigma) * median))
    upper = int(min(255, (1.0 + sigma) * median))
    return cv2.Canny(img, lower, upper)
```

### 2. Canny với Bilateral Filter

Thay Gaussian bằng Bilateral để giữ biên sắc nét hơn:

```python
blur = cv2.bilateralFilter(img, 9, 75, 75)
edges = cv2.Canny(blur, 50, 150)
```

### 3. Canny 3D (Video)

Mở rộng sang 3D cho video: xét gradient cả theo thời gian.

## 📚 Tài Liệu Tham Khảo

- **Canny, J.** (1986). A Computational Approach to Edge Detection
- OpenCV Documentation: Canny Edge Detection
- [Paper gốc](https://ieeexplore.ieee.org/document/4767851)

## 🔗 Liên Kết

**Bài thực hành**:
- **Bài 2**: Document scanning (dùng Canny → findContours)
- **Bài 3**: Lane detection (Canny → HoughLinesP)
- **Bài 6**: Product cropping (Canny → contours)

**Lý thuyết liên quan**:
- **01-edge-detection-fundamentals.md**: Sobel, gradient cơ bản
- **03-hough-transform.md**: Hough Lines/Circles

---

**Tác giả**: Dựa trên PDF T21-40 Tách Biên
**Cập nhật**: 2025
