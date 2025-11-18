# Lý Thuyết 6: Xử Lý Biên Với Morphological Operations

## 📋 Tổng Quan

**Morphological Operations** (phép toán hình thái học) là các phép biến đổi dựa trên hình dạng. Ban đầu phát triển cho ảnh nhị phân, nhưng cũng áp dụng được cho grayscale.

Trong phát hiện biên, morphology giúp:
- **Làm sạch biên** (loại nhiễu)
- **Nối biên gián đoạn**
- **Tách biên dính nhau**
- **Khuếch đại biên yếu**

## 🎯 Ứng Dụng

- **Bài 4**: Phát hiện vết xước (morphological gradient)
- **Bài 7**: Phát hiện vết nứt (top-hat transform)

## 📐 Phép Toán Cơ Bản

### 1. Erosion (Ăn Mòn)

**Ý tưởng**: Làm **nhỏ** vùng trắng, **lớn** vùng đen

```python
eroded = cv2.erode(img, kernel, iterations=1)
```

**Nguyên lý**:
- Trượt kernel qua ảnh
- Pixel giữ giá trị MIN của vùng kernel phủ

**Ảnh hưởng**:
- ✅ Loại bỏ nhiễu nhỏ (white noise)
- ✅ Tách vật thể dính nhau
- ❌ Làm nhỏ vật thể

### 2. Dilation (Giãn Nở)

**Ý tưởng**: Làm **lớn** vùng trắng, **nhỏ** vùng đen

```python
dilated = cv2.dilate(img, kernel, iterations=1)
```

**Nguyên lý**:
- Trượt kernel qua ảnh
- Pixel giữ giá trị MAX của vùng kernel phủ

**Ảnh hưởng**:
- ✅ Nối các vùng gần nhau
- ✅ Lấp khe hở nhỏ
- ❌ Làm lớn vật thể

### 3. Opening (Mở)

**Công thức**: Erosion → Dilation

```python
opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
# Tương đương:
# opened = cv2.dilate(cv2.erode(img, kernel), kernel)
```

**Tác dụng**:
- ✅ Loại bỏ nhiễu nhỏ
- ✅ Làm mượt biên
- ✅ Giữ kích thước vật thể gần như ban đầu

**Dùng khi**: Ảnh có nhiều white noise (chấm trắng nhỏ)

### 4. Closing (Đóng)

**Công thức**: Dilation → Erosion

```python
closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
# Tương đương:
# closed = cv2.erode(cv2.dilate(img, kernel), kernel)
```

**Tác dụng**:
- ✅ Lấp khe hở nhỏ trong vật thể
- ✅ Nối biên gián đoạn
- ✅ Giữ kích thước vật thể gần như ban đầu

**Dùng khi**: Biên bị đứt quãng, cần nối liền

## 🔧 Morphological Gradient Operations

### 1. Morphological Gradient

**Công thức**: Dilation - Erosion

```python
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
# Tương đương:
# dilated = cv2.dilate(img, kernel)
# eroded = cv2.erode(img, kernel)
# gradient = dilated - eroded
```

**Tác dụng**:
- Lấy **biên** của vật thể
- Biên dày hơn Canny/Sobel
- Ít nhiễu hơn Sobel đơn thuần

**Ưu điểm**:
- ✅ Không cần chọn ngưỡng
- ✅ Robust với nhiễu
- ✅ Cho biên liền mạch

**Ví dụ**: Phát hiện vết xước

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 1.0)

# Morphological gradient
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
gradient = cv2.morphologyEx(blur, cv2.MORPH_GRADIENT, kernel)

# Ngưỡng
_, edges = cv2.threshold(gradient, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

### 2. Top-Hat (White Top-Hat)

**Công thức**: Original - Opening

```python
tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
# Tương đương:
# opened = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
# tophat = gray - opened
```

**Tác dụng**:
- Lấy **chi tiết sáng** nhỏ hơn kernel
- Loại bỏ nền, giữ lại vật thể nhỏ sáng

**Ứng dụng**:
- Phát hiện vết xước sáng trên nền tối
- Phát hiện text nhỏ
- Tách foreground/background

**Ví dụ**: Phát hiện vết nứt

```python
# Top-hat với kernel lớn
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,25))
tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)

# Ngưỡng
_, cracks = cv2.threshold(tophat, 20, 255, cv2.THRESH_BINARY)
```

### 3. Black-Hat

**Công thức**: Closing - Original

```python
blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
# Tương đương:
# closed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
# blackhat = closed - gray
```

**Tác dụng**:
- Lấy **chi tiết tối** nhỏ hơn kernel
- Phát hiện vết tối trên nền sáng

**Ứng dụng**:
- Phát hiện vết xước tối
- Phát hiện khuyết điểm tối
- Tách background

## 🔨 Structuring Elements (Kernels)

### Hình Dạng Kernel

```python
# 1. Rectangular (Chữ nhật)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
# [[1 1 1 1 1]
#  [1 1 1 1 1]
#  [1 1 1 1 1]
#  [1 1 1 1 1]
#  [1 1 1 1 1]]

# 2. Ellipse (Hình elip)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
# [[0 0 1 0 0]
#  [1 1 1 1 1]
#  [1 1 1 1 1]
#  [1 1 1 1 1]
#  [0 0 1 0 0]]

# 3. Cross (Hình chữ thập)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))
# [[0 0 1 0 0]
#  [0 0 1 0 0]
#  [1 1 1 1 1]
#  [0 0 1 0 0]
#  [0 0 1 0 0]]

# 4. Custom (Tùy chỉnh)
kernel = np.array([[0,1,0],
                   [1,1,1],
                   [0,1,0]], dtype=np.uint8)
```

### Chọn Kernel

**Kích thước**:
- `(3,3)`: Nhỏ, ít ảnh hưởng, nhanh
- `(5,5)`: Chuẩn, cân bằng
- `(7,7)` - `(11,11)`: Lớn, ảnh hưởng mạnh
- `(15,15)+`: Rất lớn, cho top-hat/black-hat

**Hình dạng**:
- **RECT**: Đa dụng, nhanh nhất
- **ELLIPSE**: Tròn hơn, tự nhiên hơn
- **CROSS**: Chỉ theo 4 hướng
- **Custom**: Cho hướng cụ thể (vertical, horizontal)

## 🧪 Ví Dụ Thực Hành

### Ví Dụ 1: Phát Hiện Vết Xước (Bài 4)

```python
# 1. Đọc và tiền xử lý
img = cv2.imread('surface.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 1.0)

# 2. Morphological gradient
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
gradient = cv2.morphologyEx(blur, cv2.MORPH_GRADIENT, kernel)

# 3. Ngưỡng
_, binary = cv2.threshold(gradient, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 4. Morphology để làm sạch
# Opening: Loại nhiễu
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))

# Closing: Nối biên đứt quãng
closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))

# 5. Tìm contours
cnts, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter theo area
scratches = [c for c in cnts if cv2.contourArea(c) > 100]

# Vẽ
cv2.drawContours(img, scratches, -1, (0,255,0), 2)
```

### Ví Dụ 2: Phát Hiện Vết Nứt (Bài 7)

```python
# 1. Đọc và tiền xử lý
img = cv2.imread('crack.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. Top-hat với kernel lớn
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,25))
tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)

# 3. Tăng cường contrast
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
enhanced = clahe.apply(tophat)

# 4. Ngưỡng thấp để lấy vết mờ
_, cracks = cv2.threshold(enhanced, 10, 255, cv2.THRESH_BINARY)

# 5. Morphology để nối vết nứt
kernel_line = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))  # Dọc
cracks = cv2.morphologyEx(cracks, cv2.MORPH_CLOSE, kernel_line)

# 6. Skeleton để làm mảnh
from skimage.morphology import skeletonize
skeleton = skeletonize(cracks // 255).astype(np.uint8) * 255
```

## 📊 So Sánh Morphology vs Gradient

| Tiêu Chí | Sobel/Canny | Morphological Gradient |
|----------|-------------|------------------------|
| **Tốc độ** | Nhanh ⭐ | Chậm hơn |
| **Nhiễu** | Cao | Thấp ⭐ |
| **Độ dày biên** | Mảnh | Dày hơn |
| **Ngưỡng** | Cần điều chỉnh | Ít cần hơn ⭐ |
| **Biên liền** | Có thể đứt | Liền mạch hơn ⭐ |

## 🎚️ Workflow Tối Ưu

### Cho Vật Thể Sáng Trên Nền Tối

```python
1. Grayscale
2. Gaussian blur
3. Top-hat (kernel lớn)
4. Threshold (Otsu hoặc cố định)
5. Morphology cleanup (opening/closing)
6. Contours
```

### Cho Biên Rõ Nét

```python
1. Grayscale
2. Gaussian blur
3. Morphological gradient (kernel nhỏ)
4. Threshold
5. Contours
```

### Cho Vết Xước/Nứt Mảnh

```python
1. Grayscale
2. Top-hat/Black-hat (kernel lớn)
3. CLAHE (tăng contrast)
4. Threshold thấp
5. Closing với kernel hướng (horizontal/vertical)
6. Skeleton/thinning
```

## 🔬 Ưu Nhược Điểm

### Morphology - Ưu Điểm
- ✅ Rất robust với nhiễu
- ✅ Không cần gradient, đơn giản
- ✅ Top-hat tốt cho vật nhỏ
- ✅ Linh hoạt với kernel shape

### Morphology - Nhược Điểm
- ❌ Chậm (nhiều iterations)
- ❌ Biến đổi kích thước vật thể
- ❌ Cần chọn kernel size phù hợp
- ❌ Kém với biên phức tạp

## 🚀 Kỹ Thuật Nâng Cao

### 1. Directional Morphology

Phát hiện vết xước theo hướng cụ thể:

```python
# Kernel dọc (phát hiện xước dọc)
kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1,15))

# Kernel ngang (phát hiện xước ngang)
kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (15,1))

# Top-hat theo hướng
vertical = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel_v)
horizontal = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel_h)

# Kết hợp
scratches = cv2.add(vertical, horizontal)
```

### 2. Multi-Scale Morphology

```python
# Phát hiện vật thể ở nhiều kích thước
results = []
for size in [5, 11, 21, 31]:
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
    results.append(tophat)

# Kết hợp
combined = np.maximum.reduce(results)
```

### 3. Hit-or-Miss Transform

Tìm pattern cụ thể:

```python
# Tìm điểm cuối đường
kernel1 = np.array([[0, 0, 0],
                    [0, 1, 0],
                    [1, 1, 1]], dtype=np.uint8)

kernel2 = np.array([[1, 1, 1],
                    [1, 0, 1],
                    [1, 0, 0]], dtype=np.uint8)

hitmiss = cv2.morphologyEx(binary, cv2.MORPH_HITMISS, kernel1)
```

## 🧪 Debugging Tips

### Biên Bị Mất

```python
# Giảm kernel size
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))  # Thay vì (5,5)

# Giảm iterations
closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=1)

# Dùng ellipse thay vì rect
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
```

### Quá Nhiều Nhiễu

```python
# Tăng kernel opening
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))

# Hoặc tăng iterations
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
```

## 📚 Tài Liệu Tham Khảo

- **Serra, J.** (1982). Image Analysis and Mathematical Morphology
- OpenCV Documentation: Morphological Transformations
- Gonzalez & Woods: Digital Image Processing, Chapter 9

## 🔗 Liên Kết

**Bài thực hành**:
- **Bài 4**: Scratch detection (morphological gradient)
- **Bài 7**: Crack detection (top-hat transform)

**Lý thuyết liên quan**:
- **01-edge-detection-fundamentals.md**: So sánh với gradient-based
- **04-contour-detection.md**: Sử dụng morphology để cải thiện contours

---

**Tác giả**: Dựa trên PDF T21-40 Tách Biên
**Cập nhật**: 2025
