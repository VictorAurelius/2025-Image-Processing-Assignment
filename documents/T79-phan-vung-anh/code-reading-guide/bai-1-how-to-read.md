# Hướng Dẫn Đọc Code: Bài 1 - Global Thresholding

## Tổng Quan

Bài 1 cài đặt thuật toán **phân ngưỡng toàn cục lặp** (Heuristic Iterative Thresholding) để tách sản phẩm khỏi nền trên ảnh băng chuyền. Thuật toán hội tụ đến ngưỡng tối ưu bằng cách lặp T = (m₁ + m₂)/2.

## Input/Output

**Input:**
- Ảnh màu BGR từ `../input/conveyor.jpg`
- Nếu không tồn tại: tạo ảnh mẫu băng chuyền

**Output:**
- Ảnh nhị phân (binary mask) phân vùng
- Giá trị ngưỡng T hội tụ
- Hình visualization 3 panels: Original | Grayscale | Binary
- File `output/global_threshold_result.png`

## Thuật Toán Chính

### 1. Hàm `global_threshold()` (dòng 20-46)

**Input:** `gray` (ảnh xám), `eps=1e-3`, `max_iter=100`

**Thuật toán:**

```
Dòng 33: Khởi tạo T = mean(gray)
Dòng 34-43: Vòng lặp hội tụ:
  - Dòng 35: Chia 2 nhóm G1 (≥T), G2 (<T)
  - Dòng 36-37: Kiểm tra nhóm rỗng
  - Dòng 38: Tính mean m1, m2
  - Dòng 39: Tính T_new = (m1 + m2)/2
  - Dòng 40-43: Kiểm tra hội tụ |T_new - T| ≤ eps
Dòng 45: Áp dụng cv2.threshold với T đã tìm được
```

**Output:** `(binimg, T)` - ảnh nhị phân và ngưỡng

### 2. Hàm `create_sample_image()` (dòng 49-64)

Tạo ảnh mẫu 400×600 với băng chuyền và 4 hộp sản phẩm.

### 3. Hàm `main()` (dòng 67-147)

Pipeline chính:
1. **Đọc/Tạo ảnh** (dòng 69-79)
2. **Chuyển grayscale** (dòng 82)
3. **Phân ngưỡng** (dòng 89)
4. **Thống kê** (dòng 92-109)
5. **Visualization** (dòng 112-130)
6. **Lưu kết quả** (dòng 133-137)

## Code Quan Trọng

### 1. Vòng lặp hội tụ (dòng 34-43)

```python
for iteration in range(max_iter):
    G1, G2 = gray[gray >= T], gray[gray < T]  # Chia 2 nhóm
    if len(G1) == 0 or len(G2) == 0:
        break
    m1, m2 = float(np.mean(G1)), float(np.mean(G2))
    newT = 0.5 * (m1 + m2)  # Công thức chính
    if abs(newT - T) <= eps:
        T = newT
        break
    T = newT
```

**Giải thích:** Sử dụng NumPy boolean indexing để chia pixels thành 2 nhóm. Hội tụ khi sai số < epsilon hoặc đạt max_iter.

### 2. Áp dụng ngưỡng (dòng 45)

```python
_, binimg = cv2.threshold(gray, T, 255, cv2.THRESH_BINARY)
```

**Giải thích:** `cv2.threshold()` trả về `(threshold_value, binary_image)`. Pixel ≥ T → 255, < T → 0.

### 3. Thống kê phân vùng (dòng 95-101)

```python
num_foreground = np.sum(binimg == 255)
num_background = np.sum(binimg == 0)
total_pixels = gray.size

print(f"  - Pixel nền (đen): {num_background} ({100*num_background/total_pixels:.1f}%)")
print(f"  - Pixel vật thể (trắng): {num_foreground} ({100*num_foreground/total_pixels:.1f}%)")
```

**Giải thích:** Đếm pixels bằng boolean masking và `np.sum()`.

### 4. Tính độ sáng trung bình mỗi vùng (dòng 103-109)

```python
mean_foreground = np.mean(gray[binimg == 255]) if num_foreground > 0 else 0
mean_background = np.mean(gray[binimg == 0]) if num_background > 0 else 0

print(f"  - Vùng nền: {mean_background:.2f}")
print(f"  - Vùng vật thể: {mean_foreground:.2f}")
print(f"  - Chênh lệch: {abs(mean_foreground - mean_background):.2f}")
```

**Giải thích:** Sử dụng binary mask để index vào ảnh xám gốc và tính mean.

### 5. Visualization 3 panels (dòng 112-130)

```python
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Ảnh gốc", fontsize=12, fontweight='bold')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(gray, cmap='gray')
plt.title("Ảnh xám", fontsize=12, fontweight='bold')

plt.subplot(1, 3, 3)
plt.imshow(binimg, cmap='gray')
plt.title(f"Phân ngưỡng toàn cục\n(T = {round(T, 2)})", fontsize=12)
```

**Giải thích:** `subplot(1, 3, i)` tạo 1 hàng, 3 cột. Chuyển BGR→RGB cho matplotlib. Sử dụng `cmap='gray'` cho ảnh xám.

## Tham Số Quan Trọng

| Tham số | Vị trí | Giá trị mặc định | Ý nghĩa | Cách điều chỉnh |
|---------|--------|------------------|---------|-----------------|
| `eps` | Dòng 20 | 1e-3 | Ngưỡng hội tụ | Giảm → chính xác hơn, chậm hơn |
| `max_iter` | Dòng 20 | 100 | Số lần lặp tối đa | Tăng nếu không hội tụ |
| Initial T | Dòng 33 | `mean(gray)` | Ngưỡng khởi tạo | Có thể dùng median hoặc giá trị cố định |

## Kết Quả Mong Đợi

**Với ảnh mẫu:**
- Ngưỡng hội tụ: T ≈ 110-120
- Số vòng lặp: 3-5 iterations
- Pixel nền: ~70-80%
- Pixel vật thể: ~20-30%
- Chênh lệch độ sáng: 60-80

**Console output mẫu:**
```
============================================================
PHÂN NGƯỠNG TOÀN CỤC - GLOBAL THRESHOLDING
============================================================

Giá trị ngưỡng hội tụ: T = 117.82
Kích thước ảnh: (400, 600)

Thống kê phân vùng:
  - Pixel nền (đen): 188234 (78.4%)
  - Pixel vật thể (trắng): 51766 (21.6%)

Độ sáng trung bình:
  - Vùng nền: 155.34
  - Vùng vật thể: 84.27
  - Chênh lệch: 71.07
```

## Lỗi Thường Gặp

### 1. Lỗi: Division by zero trong vòng lặp

**Nguyên nhân:** Một trong hai nhóm G1 hoặc G2 rỗng (len = 0)

**Fix:**
```python
# Dòng 36-37 đã có check
if len(G1) == 0 or len(G2) == 0:
    break
```

**Khi nào xảy ra:** Ảnh đồng nhất (tất cả pixels cùng giá trị) hoặc T khởi tạo quá cực đoan.

### 2. Lỗi: Không hội tụ sau max_iter

**Nguyên nhân:** eps quá nhỏ, ảnh có nhiễu lớn, hoặc histogram không bimodal

**Fix:**
```python
# Tăng eps hoặc max_iter
binimg, T = global_threshold(gray, eps=1e-2, max_iter=200)
```

**Debug:** In ra giá trị T mỗi iteration để quan sát xu hướng:
```python
print(f"Iteration {iteration}: T = {T:.2f}, newT = {newT:.2f}, diff = {abs(newT-T):.4f}")
```

### 3. Lỗi: FileNotFoundError khi đọc ảnh

**Nguyên nhân:** Đường dẫn `../input/conveyor.jpg` không tồn tại

**Fix:** Code đã xử lý bằng cách tạo ảnh mẫu:
```python
if os.path.exists(input_path):
    img = cv2.imread(input_path)
else:
    img = create_sample_image()
```

**Lưu ý:** Đảm bảo thư mục `../input/` tồn tại trước khi chạy.

## Mở Rộng

### 1. Thử nghiệm với ảnh thực tế

```python
# Đọc ảnh thực tế của băng chuyền
img = cv2.imread('real_conveyor.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Tiền xử lý: denoise
gray = cv2.GaussianBlur(gray, (5, 5), 0)

binimg, T = global_threshold(gray, eps=1e-3)
```

### 2. So sánh với Otsu

```python
# Otsu thresholding
T_otsu, binimg_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# So sánh
print(f"Global Iterative: T = {T:.2f}")
print(f"Otsu: T = {T_otsu:.2f}")
print(f"Difference: {abs(T - T_otsu):.2f}")
```

### 3. Tối ưu hóa: Early stopping

```python
def global_threshold_optimized(gray, eps=1e-3, max_iter=100, check_interval=5):
    """Kiểm tra hội tụ mỗi check_interval iterations."""
    T = float(np.mean(gray))
    T_history = []

    for iteration in range(max_iter):
        G1, G2 = gray[gray >= T], gray[gray < T]
        if len(G1) == 0 or len(G2) == 0:
            break

        m1, m2 = float(np.mean(G1)), float(np.mean(G2))
        newT = 0.5 * (m1 + m2)

        T_history.append(newT)

        # Kiểm tra oscillation
        if len(T_history) >= check_interval:
            recent = T_history[-check_interval:]
            if np.std(recent) < eps:  # Đã ổn định
                T = np.mean(recent)
                break

        if abs(newT - T) <= eps:
            T = newT
            break
        T = newT

    return T, iteration + 1
```

### 4. Phân tích histogram

```python
# Vẽ histogram với ngưỡng
import matplotlib.pyplot as plt

hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

plt.figure(figsize=(10, 5))
plt.plot(hist, color='steelblue')
plt.axvline(x=T, color='red', linestyle='--', linewidth=2, label=f'T={T:.0f}')
plt.title('Histogram với ngưỡng hội tụ')
plt.xlabel('Gray level')
plt.ylabel('Frequency')
plt.legend()
plt.grid(alpha=0.3)
plt.show()
```

### 5. Morphological post-processing

```python
# Làm sạch kết quả bằng morphology
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# Opening: loại bỏ nhiễu nhỏ
binimg_clean = cv2.morphologyEx(binimg, cv2.MORPH_OPEN, kernel)

# Closing: lấp lỗ nhỏ
binimg_clean = cv2.morphologyEx(binimg_clean, cv2.MORPH_CLOSE, kernel)

# So sánh
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].imshow(binimg, cmap='gray')
axes[0].set_title('Original')
axes[1].imshow(binimg_clean, cmap='gray')
axes[1].set_title('After Morphology')
plt.show()
```

---

**File code:** `/code-implement/T79-phan-vung-anh/bai-1-global-thresholding/threshold.py`
**Lý thuyết:** [01-thresholding-methods.md](../theory/01-thresholding-methods.md)
**Tổng số dòng code:** 148 dòng
