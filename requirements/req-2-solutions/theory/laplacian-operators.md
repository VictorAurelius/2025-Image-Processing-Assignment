# Toán Tử Laplacian (Laplacian Operator)

## Định Nghĩa

Laplacian là toán tử đạo hàm bậc hai (second-order derivative) được sử dụng để phát hiện biên (edge detection) và các vùng thay đổi cường độ nhanh trong ảnh.

Công thức toán học:
```
∇²f = ∂²f/∂x² + ∂²f/∂y²
```

## Kernel Laplacian Chuẩn

### Kernel 3×3 phổ biến nhất:
```
 0   1   0
 1  -4   1
 0   1   0
```

### Các biến thể khác:

**Laplacian với 8 láng giềng:**
```
 1   1   1
 1  -8   1
 1   1   1
```

**Laplacian có trọng số:**
```
-1  -1  -1
-1   8  -1
-1  -1  -1
```

## Cách Hoạt Động

1. **Convolution**: Kernel được áp dụng lên từng pixel của ảnh
2. **Tính tổng trọng số**: Nhân từng giá trị pixel với hệ số tương ứng trong kernel
3. **Kết quả**: Giá trị dương/âm cho biết hướng thay đổi cường độ

### Đặc điểm:
- Tổng các hệ số trong kernel = 0
- Giá trị trung tâm âm, xung quanh dương (hoặc ngược lại)
- Nhạy với nhiễu

## Padding Modes

Khi áp dụng Laplacian, cần xử lý biên ảnh bằng các phương pháp padding:

### 1. Zero Padding
- Thêm giá trị 0 xung quanh ảnh
- Đơn giản nhưng có thể tạo biên giả

### 2. Edge Padding (Replicate)
- Sao chép giá trị pixel biên
- Phù hợp cho hầu hết trường hợp
- **Được sử dụng trong đề thi**

### 3. Reflect Padding
- Phản xạ ảnh tại biên
- Tạo sự liên tục tự nhiên

### 4. Wrap Padding
- Lấy giá trị từ phía đối diện
- Phù hợp với ảnh tuần hoàn

## Ví Dụ Tính Toán

### Input Image A (3×3):
```
10  25  30
30  20  15
25  60  30
```

### Kernel:
```
 0   1   0
 1  -4   1
 0   1   0
```

### Với Edge Padding:
Ảnh sau padding (5×5):
```
10  10  25  30  30
10  10  25  30  30
30  30  20  15  15
25  25  60  30  30
25  25  60  30  30
```

### Tính pixel tại (0,0) của kết quả:
- Lấy vùng 3×3 xung quanh pixel (1,1) của padded image
- Áp dụng convolution:
```
Vùng:        Kernel:       Phép tính:
10 10 25      0  1  0      0×10 + 1×10 + 0×25
10 10 25   ×  1 -4  1   =  1×10 + (-4)×10 + 1×25
30 30 20      0  1  0      0×30 + 1×30 + 0×20

= 0 + 10 + 0 + 10 - 40 + 25 + 0 + 30 + 0
= 35
```

## Ứng Dụng

### 1. Edge Detection
- Phát hiện biên mạnh trong ảnh
- Thường kết hợp với threshold

### 2. Image Sharpening
- **Sharpening formula**: `sharpened = original - c × laplacian`
- **Alternative**: `sharpened = original + c × laplacian` (tăng độ sáng)
- c là hệ số điều chỉnh độ mạnh

### 3. Feature Enhancement
- Tăng cường chi tiết trong ảnh
- Làm nổi bật vùng thay đổi nhanh

### 4. Image Analysis
- Phân tích texture
- Phát hiện blob
- Medical imaging

## So Sánh Với Gradient

| Đặc điểm | Gradient (1st derivative) | Laplacian (2nd derivative) |
|----------|---------------------------|----------------------------|
| Độ nhạy với nhiễu | Thấp hơn | Cao hơn |
| Phát hiện biên | Có hướng (magnitude + direction) | Không có hướng |
| Ứng dụng | Edge detection phổ biến | Sharpening, feature detection |
| Ví dụ | Sobel, Prewitt | Laplacian, LoG |

## Laplacian of Gaussian (LoG)

Kết hợp Gaussian smoothing với Laplacian để giảm nhiễu:

1. **Bước 1**: Làm mượt ảnh với Gaussian filter
2. **Bước 2**: Áp dụng Laplacian
3. **Kết quả**: Edge detection tốt hơn, ít nhiễu hơn

Kernel LoG có dạng "Mexican hat" trong không gian 3D.

## Lưu Ý Khi Sử Dụng

1. **Nhiễu**: Laplacian rất nhạy với nhiễu → nên làm mượt trước
2. **Giá trị âm**: Kết quả có thể âm → cần xử lý khi hiển thị
3. **Độ lớn biên**: Sử dụng absolute value để đo độ mạnh biên
4. **Padding**: Chọn padding mode phù hợp với ứng dụng

## Tham Khảo

- Digital Image Processing (Gonzalez & Woods) - Chapter 10
- Computer Vision: Algorithms and Applications (Szeliski) - Chapter 4
- OpenCV Documentation: `cv2.Laplacian()`
