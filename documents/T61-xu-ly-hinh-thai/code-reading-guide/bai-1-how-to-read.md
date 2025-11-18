# Bài 1: Làm Sạch Văn Bản Quét - How to Read

## Tổng Quan

File `denoise.py` thực hiện khử nhiễu muối tiêu trên văn bản quét bằng phép Opening (Erosion → Dilation). Opening loại bỏ các hạt nhiễu nhỏ mà vẫn bảo toàn nét chữ chính.

## Input/Output

**Input:**
- `../input/docs/noisy_scan.png`: Ảnh văn bản có nhiễu muối tiêu
- Nếu không có, tự động tạo mẫu bằng `create_noisy_document()`

**Output:**
- `../output/bai-1-opening/result_kernel_3x3.png`: Kết quả với kernel 3×3
- `../output/bai-1-opening/result_kernel_5x5.png`: Kết quả với kernel 5×5
- `../output/bai-1-opening/opened_3x3.png`, `opened_5x5.png`: Ảnh sau Opening

## Thuật Toán Chính

**Quy Trình (6 bước):**

1. **Đọc/Tạo Ảnh** (dòng 54-64)
   - Kiểm tra file input
   - Nếu không có → tạo ảnh mẫu

2. **Nhị Phân Hóa Otsu** (dòng 69-76)
   - Threshold tự động
   - Chuyển ảnh thành nhị phân (0/255)

3. **Opening với Kernel 3×3** (dòng 83-96)
   - Tạo SE RECT 3×3
   - Erosion → Dilation
   - Đếm pixels đã loại bỏ

4. **Opening với Kernel 5×5** (dòng 83-96, lặp k=5)
   - Tạo SE RECT 5×5
   - So sánh với 3×3

5. **Visualize Kết Quả** (dòng 97-118)
   - 3 subplot: Gốc, Nhị phân, Opening
   - Lưu ảnh với dpi=150

6. **Phân Tích** (dòng 123-139)
   - In kết luận về Opening

## Code Quan Trọng

### 1. Tạo Ảnh Mẫu Có Nhiễu (Dòng 28-44)

```python
def create_noisy_document():
    """Tạo ảnh tài liệu mẫu có nhiễu muối tiêu"""
    # Tạo ảnh trắng
    img = np.ones((400, 600), dtype=np.uint8) * 255

    # Vẽ text
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'Xin chao!', (50, 100), font, 2, 0, 3)
    cv2.putText(img, 'Image Processing', (50, 200), font, 1.5, 0, 2)

    # Thêm nhiễu muối tiêu
    noise = np.random.rand(*img.shape)
    img[noise < 0.02] = 0  # Nhiễu tiêu (đen)
    img[noise > 0.98] = 255  # Nhiễu muối (trắng)

    return img
```

**Giải thích:**
- `np.ones((400, 600), dtype=np.uint8) * 255`: Tạo ảnh trắng 400×600
- `cv2.putText()`: Vẽ chữ màu đen (0)
- `noise < 0.02`: 2% pixel thành nhiễu đen
- `noise > 0.98`: 2% pixel thành nhiễu trắng
- Tổng 4% pixel là nhiễu

### 2. Nhị Phân Hóa Otsu (Dòng 73)

```python
_, bw = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

**Giải thích:**
- `cv2.THRESH_OTSU`: Tự động tìm threshold tối ưu
- Threshold = 0 sẽ bị ghi đè bởi Otsu
- `bw`: Ảnh nhị phân (0 = chữ, 255 = nền)

### 3. Tạo Structuring Element (Dòng 85-86)

```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
print(f"[+] Tạo structuring element RECT {k}x{k}")
```

**Giải thích:**
- `cv2.MORPH_RECT`: Hình chữ nhật (tất cả pixel = 1)
- `(k, k)`: Kích thước kernel (3×3 hoặc 5×5)
- Kernel lớn hơn → loại nhiễu tốt hơn nhưng có thể mất nét mảnh

**Các loại SE:**
- `MORPH_RECT`: □ (vuông)
- `MORPH_ELLIPSE`: ○ (tròn)
- `MORPH_CROSS`: + (chữ thập)

### 4. Phép Opening (Dòng 88-94)

```python
open_img = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel)
print(f"[+] Thực hiện MORPH_OPEN (Erosion → Dilation)")

# Tính số pixel nhiễu đã loại bỏ
removed = np.sum(bw != open_img)
print(f"[+] Số pixel đã thay đổi: {removed}")
print(f"[+] Tỷ lệ thay đổi: {removed / bw.size * 100:.2f}%")
```

**Giải thích:**
- `cv2.MORPH_OPEN`: Opening = Erosion tiếp theo Dilation
- `bw != open_img`: Pixels khác nhau = nhiễu đã loại bỏ
- `np.sum()`: Đếm số pixels

**Cách hoạt động:**
1. **Erosion**: Loại bỏ pixels ở biên, các hạt nhiễu nhỏ biến mất
2. **Dilation**: Phồng lại vật thể, nét chữ phục hồi
3. **Kết quả**: Nhiễu nhỏ biến mất, nét chữ được bảo toàn

### 5. Visualize So Sánh (Dòng 97-118)

```python
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(img, 'gray')
plt.title('Gốc')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(bw, 'gray')
plt.title('Nhị phân')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(open_img, 'gray')
plt.title(f'Opening {k}x{k}')
plt.axis('off')

plt.tight_layout()
output_path = f'../output/bai-1-opening/result_kernel_{k}x{k}.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
```

**Giải thích:**
- `figsize=(15, 5)`: Kích thước figure (15 inch × 5 inch)
- `subplot(1, 3, i)`: 1 hàng, 3 cột
- `'gray'`: Colormap grayscale
- `axis('off')`: Tắt trục tọa độ
- `dpi=150`: Độ phân giải lưu ảnh

## Tham Số Quan Trọng

| Tham Số | Giá Trị | Ý Nghĩa | Ảnh Hưởng |
|---------|---------|---------|-----------|
| **Kernel Size** | 3×3, 5×5 | Kích thước structuring element | Lớn hơn → khử nhiễu mạnh hơn, có thể mất nét |
| **Threshold** | Otsu (auto) | Ngưỡng nhị phân hóa | Otsu tối ưu cho ảnh bi-modal |
| **Noise Ratio** | 4% (2% muối + 2% tiêu) | Tỷ lệ nhiễu trong ảnh mẫu | Nhiều hơn → khó khử hơn |
| **Iterations** | 1 (default) | Số lần lặp Opening | Tăng → hiệu ứng mạnh hơn |
| **DPI** | 150 | Độ phân giải lưu ảnh | Cao hơn → file lớn hơn, rõ hơn |

## Kết Quả Mong Đợi

**Với Kernel 3×3:**
- Loại bỏ nhiễu nhỏ (1-2 pixel)
- Giữ được hầu hết chi tiết chữ
- Thích hợp cho chữ có nét mảnh

**Với Kernel 5×5:**
- Loại bỏ nhiễu lớn hơn (3-4 pixel)
- Có thể làm mất một số nét mảnh
- Thích hợp cho chữ to, nét đậm

**Số liệu thực tế (ảnh mẫu):**
- Ảnh gốc: 400×600 = 240,000 pixels
- Nhiễu: ~9,600 pixels (4%)
- Opening 3×3 loại bỏ: ~7,000 pixels (~3%)
- Opening 5×5 loại bỏ: ~10,000 pixels (~4%)

## Lỗi Thường Gặp

### Lỗi 1: Kernel Quá Lớn

**Triệu chứng:**
```
Nét chữ mỏng biến mất, chỉ còn lại chữ to
```

**Nguyên nhân:**
- Kernel 7×7 hoặc lớn hơn
- Erosion làm nét mỏng biến mất hoàn toàn

**Cách fix:**
```python
# BAD: Kernel quá lớn
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))

# GOOD: Kernel phù hợp
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# Hoặc tăng iterations thay vì kernel size
opened = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel, iterations=2)
```

### Lỗi 2: Threshold Không Phù Hợp

**Triệu chứng:**
```
Ảnh nhị phân quá sáng hoặc quá tối, chữ không rõ
```

**Nguyên nhân:**
- Dùng threshold cố định thay vì Otsu
- Ảnh có chiếu sáng không đều

**Cách fix:**
```python
# BAD: Threshold cố định
_, bw = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# GOOD: Otsu adaptive
_, bw = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# BETTER: Adaptive threshold cho ảnh không đều
bw = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            cv2.THRESH_BINARY, 11, 2)
```

### Lỗi 3: Không Tạo Output Folder

**Triệu chứng:**
```
FileNotFoundError: [Errno 2] No such file or directory: '../output/bai-1-opening/...'
```

**Nguyên nhân:**
- Chưa tạo thư mục output

**Cách fix:**
```python
# Dòng 52: Đã có
os.makedirs('../output/bai-1-opening', exist_ok=True)

# exist_ok=True: Không lỗi nếu folder đã tồn tại
```

## Mở Rộng

### 1. So Sánh với Median Filter

```python
# Opening (morphology)
opened = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel)

# Median Filter (statistical)
median = cv2.medianBlur(img, 5)

# So sánh
print(f"Opening time: {time_opening:.4f}s")
print(f"Median time: {time_median:.4f}s")
```

**Khi nào dùng gì:**
- Opening: Ảnh nhị phân, nhiễu muối tiêu, bảo toàn hình dạng
- Median: Ảnh grayscale, nhiễu impulse, bảo toàn biên

### 2. Adaptive Kernel Size

```python
def adaptive_opening(image):
    # Ước lượng kích thước nhiễu
    noise_size = estimate_noise_size(image)

    # Kernel = 1.5 × noise size
    kernel_size = max(3, int(noise_size * 1.5))
    kernel_size = kernel_size if kernel_size % 2 == 1 else kernel_size + 1  # Lẻ

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
```

### 3. Sequential Opening-Closing

```python
# Opening → Closing để vừa khử nhiễu, vừa nối nét
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
opened = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel)
closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
```

### 4. Multi-scale Opening

```python
# Opening ở nhiều scales, lấy kết quả tốt nhất
results = []
for k in [3, 5, 7]:
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
    opened = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel)
    results.append(opened)

# Combine bằng voting hoặc max
combined = np.maximum.reduce(results)
```

### 5. Với Ảnh Màu

```python
# Tách channels, xử lý riêng
b, g, r = cv2.split(img_color)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
b_opened = cv2.morphologyEx(b, cv2.MORPH_OPEN, kernel)
g_opened = cv2.morphologyEx(g, cv2.MORPH_OPEN, kernel)
r_opened = cv2.morphologyEx(r, cv2.MORPH_OPEN, kernel)

result = cv2.merge([b_opened, g_opened, r_opened])
```

---

**Tổng Dòng Code**: 145 dòng
**File Gốc**: `/code-implement/T61-xu-ly-hinh-thai/bai-1-opening/denoise.py`
**Theory Liên Quan**: [01-morphology-fundamentals.md](../theory/01-morphology-fundamentals.md)
