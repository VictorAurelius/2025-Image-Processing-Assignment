# Bài 1: So Sánh Các Bộ Dò Biên - Code Reading Guide

## 1. Tổng Quan

So sánh hiệu quả của 4 toán tử dò biên (Roberts, Prewitt, Sobel, Scharr) trên ảnh gốc và ảnh nhiễu, với/không có Gaussian smoothing. Mục tiêu là hiểu vai trò của làm trơn và độ nhạy nhiễu của từng toán tử.

**File code:** `/code-implement/T21-tach-bien/bai-1-edge-detectors/compare.py`

---

## 2. Input/Output

### Input
- **File:** `../input/sample-images/building.jpg`
- **Mô tả:** Ảnh đời thực (tòa nhà, đường phố) hoặc ảnh tự tạo với nhiều cạnh
- **Format:** Grayscale hoặc RGB (sẽ chuyển sang grayscale)

### Output
- **Files:** `edges_[toán_tử]_sigma[None/1.0].png` (16 files tổng cộng)
  - Ví dụ: `edges_sobel_sigmaNone.png`, `edges_roberts_sigma1.0_noisy.png`
- **Mô tả:** Ảnh nhị phân của biên (0 hoặc 255) với các toán tử khác nhau

---

## 3. Thuật Toán Chính

### Bước 1: Đọc và chuẩn bị ảnh (dòng 137-147)
- Đọc ảnh, chuyển sang grayscale float32
- Tạo ảnh nhiễu: thêm Gaussian noise với stddev=10

### Bước 2: Tính gradient với hàm `grad2d()` (dòng 32-75)
- **Nếu có sigma:** Làm trơn Gaussian trước (dòng 48-49)
- **Roberts (2x2):** Tính gradient bằng phép trừ pixel chéo (dòng 52-57)
- **Prewitt/Sobel/Scharr (3x3):** Convolution với kernel (dòng 60-75)
  - Prewitt: kernel [-1,0,1] và trọng số đều
  - Sobel: kernel [-1,0,1] và [-2,0,2] (trọng số tâm x2)
  - Scharr: kernel tối ưu cho độ chính xác góc
- **Output:** Magnitude = √(Gx² + Gy²)

### Bước 3: Nhị phân hóa với `binarize()` (dòng 77-89)
- Ngưỡng = 25% của giá trị max
- Pixel >= ngưỡng → 255, ngược lại → 0

### Bước 4: So sánh kết quả (dòng 159-183)
- Chạy 4 toán tử với 2 giá trị sigma (None và 1.0)
- Xử lý cả ảnh gốc và ảnh nhiễu
- Đếm số pixel biên để so sánh

---

## 4. Code Quan Trọng Cần Đọc

### Đoạn 1: Hàm tính gradient với Roberts (dòng 52-57)
```python
if scheme == 'roberts':
    gx = g[:-1,:-1] - g[1:,1:]      # Chéo chính
    gy = g[1:,:-1] - g[:-1,1:]      # Chéo phụ
    mag = np.zeros_like(g)
    mag[:-1,:-1] = np.hypot(gx, gy)  # Magnitude
    return mag
```
**Giải thích:** Roberts dùng kernel 2x2, tính gradient bằng phép trừ trực tiếp giữa các pixel chéo. Đây là toán tử nhỏ nhất nên nhạy cảm với nhiễu nhất.

### Đoạn 2: Kernel Sobel vs Scharr (dòng 63-68)
```python
elif scheme == 'sobel':
    kx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]], np.float32)
    ky = np.array([[ 1,2,1],[ 0,0,0],[-1,-2,-1]], np.float32)
elif scheme == 'scharr':
    kx = np.array([[3,0,-3],[10,0,-10],[3,0,-3]], np.float32)/32.0
    ky = kx.T
```
**Giải thích:** Sobel dùng trọng số [1,2,1] để nhấn mạnh pixel tâm. Scharr dùng trọng số [3,10,3] (chuẩn hóa /32) cho độ chính xác góc cao hơn.

### Đoạn 3: Tính magnitude bằng convolution (dòng 70-75)
```python
Gx = convolve(g, kx, mode=bc)  # Gradient theo x
Gy = convolve(g, ky, mode=bc)  # Gradient theo y
return np.hypot(Gx, Gy)         # √(Gx² + Gy²)
```
**Giải thích:** Dùng `scipy.ndimage.convolve` để tính gradient. `np.hypot()` tính magnitude hiệu quả hơn `sqrt(Gx**2 + Gy**2)`.

### Đoạn 4: Ngưỡng theo tỉ lệ (dòng 77-89)
```python
def binarize(mag, thr_ratio=0.25):
    mmax = mag.max() if mag.size else 0
    return (mag >= thr_ratio*mmax).astype(np.uint8)*255
```
**Giải thích:** Ngưỡng động (25% max) thay vì ngưỡng cố định. Giúp thích nghi với độ tương phản khác nhau của ảnh.

### Đoạn 5: Loop so sánh toàn diện (dòng 159-183)
```python
for sigma in [None, 1.0]:
    for scheme in ['roberts', 'prewitt', 'sobel', 'scharr']:
        mag = grad2d(img, scheme=scheme, sigma=sigma)
        mask = binarize(mag, 0.25)
        # Xử lý cả ảnh gốc và nhiễu
        magN = grad2d(noisy, scheme=scheme, sigma=sigma)
        maskN = binarize(magN, 0.25)
```
**Giải thích:** 2 loops lồng nhau tạo 16 kết quả (4 toán tử × 2 sigma × 2 loại ảnh). Giúp so sánh trực quan tất cả các trường hợp.

---

## 5. Tham Số Quan Trọng

| Tham số | Giá trị | Ý nghĩa | Điều chỉnh |
|---------|---------|---------|-----------|
| `sigma` | `None` hoặc `1.0` | Độ lệch chuẩn Gaussian blur | Tăng lên (1.5-2.0) nếu ảnh nhiễu mạnh |
| `thr_ratio` | `0.25` | Ngưỡng = 25% max magnitude | Giảm (0.15-0.2) để giữ nhiều biên, tăng (0.3-0.4) để lọc nhiễu |
| `noise_std` | `10` (dòng 147) | Độ lệch chuẩn nhiễu Gaussian | Tăng để test với nhiễu mạnh hơn |
| `bc` (boundary condition) | `'reflect'` | Xử lý biên khi convolution | Có thể dùng `'constant'`, `'nearest'` |

---

## 6. Kết Quả Mong Đợi

### Ảnh output
- 16 ảnh PNG nhị phân (trắng đen)
- Biên sắc nét xuất hiện màu trắng (255)
- Nền đen (0)

### Quan sát điển hình
- **Roberts:** Biên mảnh nhất, nhiễu nhiều nhất (đặc biệt khi sigma=None)
- **Prewitt:** Ít nhiễu hơn Roberts, biên hơi dày
- **Sobel:** Cân bằng tốt, ít nhiễu, biên rõ ràng
- **Scharr:** Tương tự Sobel nhưng chính xác hơn ở góc nghiêng

### Console output
```
Roberts: 12543 pixels (gốc), 18765 pixels (nhiễu)
Sobel: 11234 pixels (gốc), 12456 pixels (nhiễu)
```
→ Sobel ổn định hơn (chênh lệch gốc/nhiễu thấp)

---

## 7. Lỗi Thường Gặp

### Lỗi 1: "ValueError: operands could not be broadcast"
**Nguyên nhân:** Ảnh input không phải grayscale hoặc shape không khớp

**Cách fix:**
```python
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # Đảm bảo grayscale
img = img.astype(np.float32)                  # Đổi sang float32
```

### Lỗi 2: Output toàn đen hoặc toàn trắng
**Nguyên nhân:** `thr_ratio` không phù hợp hoặc ảnh quá đồng nhất

**Cách fix:**
- Giảm `thr_ratio` từ 0.25 xuống 0.1-0.15
- Kiểm tra `mag.max()` có > 0 không
- In ra `print(f"Magnitude range: {mag.min():.2f} - {mag.max():.2f}")`

### Lỗi 3: Biên quá nhiễu (ảnh nhiễu)
**Nguyên nhân:** Chưa làm trơn hoặc sigma quá nhỏ

**Cách fix:**
- Tăng sigma từ 1.0 lên 1.5 hoặc 2.0
- Thử thêm morphology opening: `cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)`

---

## 8. Mở Rộng

### Cải tiến 1: Thêm toán tử Canny
```python
edges_canny = cv2.Canny(img.astype(np.uint8), 50, 150)
```
So sánh với các toán tử gradient đơn giản

### Cải tiến 2: Tính metrics định lượng
```python
# Precision/Recall nếu có ground truth
# Hoặc edge density, edge strength
edge_density = np.sum(mask > 0) / mask.size
avg_strength = mag[mask > 0].mean()
```

### Cải tiến 3: Visualize gradient direction
```python
Gx = convolve(g, kx, mode=bc)
Gy = convolve(g, ky, mode=bc)
angle = np.arctan2(Gy, Gx) * 180 / np.pi
# Hiển thị heatmap của góc gradient
```

### Cải tiến 4: Thử nhiễu khác nhau
```python
# Salt & pepper noise
# Speckle noise
# Motion blur
```

### Cải tiến 5: So sánh thời gian chạy
```python
import time
start = time.time()
mag = grad2d(img, scheme='sobel')
print(f"Sobel: {(time.time()-start)*1000:.2f}ms")
```

---

## Tips Đọc Code Nhanh

1. **Bắt đầu từ `if __name__ == "__main__":`** (dòng 91) để hiểu flow chính
2. **Đọc hàm `grad2d()`** (dòng 32) - đây là trái tim của thuật toán
3. **Chú ý điều kiện `if scheme == ...`** để phân biệt các toán tử
4. **Bỏ qua phần tạo ảnh mẫu** (dòng 100-135) nếu đã có ảnh input
5. **Đọc phần phân tích cuối** (dòng 189-207) để hiểu kết luận

---

**Tổng số dòng:** 213 dòng
**Độ khó:** Trung bình
**Thời gian đọc hiểu:** 15-20 phút
**Thời gian chạy:** ~2-3 giây (16 ảnh output)
