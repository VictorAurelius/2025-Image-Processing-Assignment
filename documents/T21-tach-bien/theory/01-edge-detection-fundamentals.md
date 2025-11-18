# Lý Thuyết 1: Cơ Bản Về Phát Hiện Biên

## 📋 Tổng Quan

Phát hiện biên (Edge Detection) là quá trình tìm ra những điểm trong ảnh có sự thay đổi đột ngột về độ sáng. Biên thường tương ứng với:
- **Ranh giới giữa các vật thể**
- **Bề mặt có góc nhọn**
- **Thay đổi vật liệu hoặc màu sắc**
- **Bóng đổ, ánh sáng thay đổi**

## 🎯 Ứng Dụng

- **Bài 1**: So sánh các toán tử gradient cơ bản
- **Bài 4**: Phát hiện vết xước trên bề mặt

## 📐 Nguyên Lý Toán Học

### Gradient và Đạo Hàm

Biên được phát hiện thông qua **gradient** của ảnh - đạo hàm theo không gian:

```
∇f = [∂f/∂x, ∂f/∂y]
```

**Magnitude (độ lớn gradient)**:
```
|∇f| = √(Gx² + Gy²)
```

**Direction (hướng)**:
```
θ = arctan(Gy/Gx)
```

### Tại Sao Dùng Gradient?

- Vùng phẳng (uniform): gradient ≈ 0
- Biên (edge): gradient >> 0
- Gradient lớn = sự thay đổi mạnh = có khả năng là biên

## 🔧 Các Toán Tử Gradient Cơ Bản

### 1. Roberts Operator (1963)

**Kernel 2×2**:
```
Gx = [+1  0]     Gy = [ 0 +1]
     [ 0 -1]          [-1  0]
```

**Đặc điểm**:
- ✅ Đơn giản, nhanh nhất
- ✅ Biên mảnh, sắc nét
- ❌ Rất nhạy với nhiễu
- ❌ Chỉ dùng 4 pixel → thiếu thông tin

**Khi nào dùng**: Ảnh sạch, không nhiễu, cần tốc độ

### 2. Prewitt Operator (1970)

**Kernel 3×3**:
```
Gx = [-1 0 +1]    Gy = [+1 +1 +1]
     [-1 0 +1]         [ 0  0  0]
     [-1 0 +1]         [-1 -1 -1]
```

**Đặc điểm**:
- ✅ Trung bình 3 pixel → giảm nhiễu
- ✅ Cân bằng giữa nhiễu và độ chi tiết
- ❌ Vẫn khá nhạy nhiễu
- ❌ Không tối ưu về rotation invariance

**Khi nào dùng**: Ảnh có ít nhiễu, cần cân bằng

### 3. Sobel Operator (1968) ⭐ PHỔ BIẾN NHẤT

**Kernel 3×3**:
```
Gx = [-1 0 +1]    Gy = [+1 +2 +1]
     [-2 0 +2]         [ 0  0  0]
     [-1 0 +1]         [-1 -2 -1]
```

**Đặc điểm**:
- ✅ Trọng số trung tâm (2) → tốt hơn Prewitt
- ✅ Gaussian smoothing tích hợp
- ✅ Ít nhiễu nhất trong 3 toán tử cơ bản
- ✅ Tốc độ nhanh, hiệu quả
- ❌ Biên hơi dày hơn Roberts

**Khi nào dùng**: Hầu hết trường hợp, đặc biệt ảnh thực tế

**Công thức OpenCV**:
```python
gx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3)
gy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3)
mag = np.sqrt(gx**2 + gy**2)
```

### 4. Scharr Operator (2000) ⭐ CHÍNH XÁC NHẤT

**Kernel 3×3**:
```
Gx = [-3  0 +3]    Gy = [+3 +10 +3]
     [-10 0 +10]        [ 0  0   0]
     [-3  0 +3]         [-3 -10 -3]
```

**Đặc điểm**:
- ✅ Tối ưu rotation invariance
- ✅ Chính xác nhất về góc (direction)
- ✅ Tốt với biên nghiêng
- ❌ Hơi chậm hơn Sobel một chút

**Khi nào dùng**: Cần độ chính xác cao, orientation quan trọng

## 🌊 Gaussian Smoothing Trước Edge Detection

### Tại Sao Cần Smoothing?

Đạo hàm **khuếch đại nhiễu** vì:
- Nhiễu = thay đổi cục bộ ngẫu nhiên
- Đạo hàm phát hiện MỌI thay đổi → nhiễu cũng thành "biên giả"

### Gaussian Kernel

```
G(x,y) = (1/(2πσ²)) * exp(-(x²+y²)/(2σ²))
```

**σ (sigma)**: Tham số quan trọng
- `σ = 1.0`: Làm mờ nhẹ, giữ chi tiết
- `σ = 2.0`: Làm mờ vừa, giảm nhiễu tốt
- `σ > 3.0`: Làm mờ mạnh, mất chi tiết

### Trade-off

| Smoothing | Ưu điểm | Nhược điểm |
|-----------|---------|------------|
| **Không** | Biên sắc nét, chi tiết | Nhiễu lớn |
| **Nhẹ (σ=1)** | Cân bằng | Vừa phải |
| **Mạnh (σ≥2)** | Ít nhiễu | Mất chi tiết, biên mờ |

**Code**:
```python
blur = cv2.GaussianBlur(img, (5,5), sigma=1.0)
```

## 🎚️ Ngưỡng (Thresholding)

Sau khi có magnitude, cần **nhị phân hóa** để lấy biên thực sự:

### 1. Ngưỡng Tuyệt Đối
```python
edges = (mag > threshold).astype(np.uint8) * 255
```
- Ví dụ: `threshold = 50`
- ❌ Khó chọn ngưỡng phù hợp mọi ảnh

### 2. Ngưỡng Tỉ Lệ ⭐ KHUYẾN NGHỊ
```python
threshold = 0.25 * mag.max()
edges = (mag >= threshold).astype(np.uint8) * 255
```
- Tự động thích nghi với từng ảnh
- `0.25` = 25% magnitude tối đa
- ✅ Hoạt động tốt với đa số ảnh

### 3. Otsu's Method
```python
_, edges = cv2.threshold(mag.astype(np.uint8), 0, 255,
                         cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```
- Tự động tìm ngưỡng tối ưu
- Tốt khi histogram có 2 peak rõ ràng

## 📊 So Sánh Các Toán Tử

| Toán Tử | Kích Thước | Nhiễu | Biên | Tốc Độ | Ứng Dụng |
|---------|-----------|-------|------|--------|----------|
| **Roberts** | 2×2 | Rất cao | Mảnh | Nhanh nhất | Ảnh sạch |
| **Prewitt** | 3×3 | Cao | Vừa | Nhanh | Cân bằng |
| **Sobel** ⭐ | 3×3 | Thấp | Vừa | Nhanh | Đa dụng |
| **Scharr** | 3×3 | Thấp | Vừa | Vừa | Chính xác |

## 🧪 Thực Hành

### Workflow Chuẩn

```python
# 1. Đọc ảnh grayscale
img = cv2.imread('input.jpg', cv2.IMREAD_GRAYSCALE)
img = img.astype(np.float32)

# 2. Làm mờ Gaussian (tuỳ chọn)
blur = cv2.GaussianBlur(img, (5,5), 1.0)

# 3. Tính gradient
gx = cv2.Sobel(blur, cv2.CV_32F, 1, 0, ksize=3)
gy = cv2.Sobel(blur, cv2.CV_32F, 0, 1, ksize=3)

# 4. Tính magnitude
mag = np.sqrt(gx**2 + gy**2)

# 5. Ngưỡng
threshold = 0.25 * mag.max()
edges = (mag >= threshold).astype(np.uint8) * 255

# 6. Lưu kết quả
cv2.imwrite('output.png', edges)
```

### Mẹo Chọn Tham Số

**Sobel ksize**:
- `ksize=3`: Chuẩn, nhanh
- `ksize=5`: Mượt hơn, chậm hơn
- `ksize=7`: Rất mượt, chậm

**Gaussian sigma**:
- Ảnh sạch: không cần hoặc `σ=0.5`
- Ảnh nhiễu nhẹ: `σ=1.0`
- Ảnh nhiễu nặng: `σ=2.0`

**Threshold ratio**:
- Chi tiết nhiều: `0.15 - 0.20`
- Cân bằng: `0.25 - 0.30`
- Chỉ biên rõ: `0.35 - 0.50`

## 🔬 Ưu Nhược Điểm

### Ưu Điểm Gradient-Based Methods
- ✅ Đơn giản, dễ hiểu
- ✅ Tốc độ cực nhanh
- ✅ Phù hợp real-time
- ✅ Không cần training

### Nhược Điểm
- ❌ Nhạy với nhiễu (cần smoothing)
- ❌ Biên dày (vài pixel)
- ❌ Khó chọn ngưỡng
- ❌ Kém với texture phức tạp

## 🚀 Cải Tiến

### 1. Non-Maximum Suppression (NMS)
Làm mảnh biên bằng cách:
- Chỉ giữ pixel có magnitude lớn nhất theo hướng gradient
- Kết quả: Biên mảnh 1 pixel

### 2. Hysteresis Thresholding
Dùng 2 ngưỡng:
- `T_high`: Chắc chắn là biên
- `T_low`: Có thể là biên (nếu liền với biên chắc chắn)

→ **Canny Edge Detector** sử dụng cả 2 kỹ thuật này!

## 📚 Tài Liệu Tham Khảo

- Sobel, I. (1968). An Isotropic 3×3 Image Gradient Operator
- Scharr, H. (2000). Optimal Operators in Digital Image Processing
- OpenCV Documentation: Edge Detection
- Gonzalez & Woods: Digital Image Processing, Chapter 10

## 🔗 Liên Kết

**Bài thực hành**:
- **Bài 1**: So sánh Roberts, Prewitt, Sobel, Scharr
- **Bài 4**: Phát hiện vết xước (morphological gradient)

**Lý thuyết liên quan**:
- **02-canny-edge-detection.md**: Thuật toán Canny nâng cao
- **06-morphological-edge-processing.md**: Xử lý biên với morphology

---

**Tác giả**: Dựa trên PDF T21-40 Tách Biên
**Cập nhật**: 2025
