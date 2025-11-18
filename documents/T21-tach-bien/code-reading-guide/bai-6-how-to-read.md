# Bài 6: Cắt Nền (Auto-Crop) Ảnh Sản Phẩm - Code Reading Guide

## 1. Tổng Quan

Tự động cắt nền ảnh sản phẩm chụp trên nền đơn giản, tạo file PNG với alpha channel (nền trong suốt). Ứng dụng cho e-commerce, photography sản phẩm.

**File code:** `/code-implement/T21-tach-bien/bai-6-product-cropping/crop.py`

---

## 2. Input/Output

### Input
- **File:** `../input/sample-images/product.jpg`
- **Mô tả:** Ảnh sản phẩm trên nền đơn giản (trắng/xám nhạt), không có vật thể lớn khác
- **Format:** RGB

### Output
- **product_cropped.png:** Sản phẩm đã cắt gọn với **nền trong suốt (alpha channel)**
- **product_mask.png:** Mask nhị phân
- **product_contour.jpg:** Visualization contour và bbox

---

## 3. Thuật Toán Chính

### Bước 1: Edge detection (dòng 89-98)
- Gaussian blur
- Canny edge (ngưỡng 50-150)

### Bước 2: Morphology (dòng 100-108)
- **Closing (×2):** Lấp khe hở trong contour
- **Dilation (×2):** Mở rộng để chắc chắn bao hết sản phẩm

### Bước 3: Tìm contour lớn nhất (dòng 111-127)
- `findContours()` → chọn max theo diện tích
- Vẽ contour đầy (filled) thành mask

### Bước 4: Crop theo bounding box (dòng 129-136)
- `boundingRect()` để lấy x, y, w, h
- Crop cả ảnh và mask

### Bước 5: Tạo PNG với alpha (dòng 138-144)
- Chuyển BGR → BGRA (thêm kênh alpha)
- Set alpha channel = mask

---

## 4. Code Quan Trọng Cần Đọc

### Đoạn 1: Morphology để liền khối (dòng 100-108)
```python
kernel = np.ones((5,5), np.uint8)

# Closing: Lấp khe hở
mask = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)

# Dilation: Mở rộng contour
mask = cv2.dilate(mask, kernel, iterations=2)
```
**Giải thích:**
- **Closing = Dilation + Erosion:** Nối các đoạn edges gián đoạn
- **Dilation:** Đảm bảo contour bao trọn sản phẩm, không bỏ sót viền
- iterations=2: Áp dụng 2 lần cho hiệu quả mạnh

### Đoạn 2: Vẽ contour đầy thành mask (dòng 125-127)
```python
mask_full = np.zeros(gray.shape, np.uint8)
cv2.drawContours(mask_full, [cnt], -1, 255, thickness=-1)
# thickness=-1 → fill toàn bộ bên trong
```
**Giải thích:** `thickness=-1` là filled mode. Tạo mask binary hoàn chỉnh từ contour.

### Đoạn 3: Bounding rectangle để tight crop (dòng 129-136)
```python
x, y, w, h = cv2.boundingRect(cnt)
crop_img = img[y:y+h, x:x+w]
crop_mask = mask_full[y:y+h, x:x+w]
```
**Giải thích:** `boundingRect()` cho bbox vuông góc nhỏ nhất bao quanh contour. Crop để loại bỏ nền dư thừa.

### Đoạn 4: Tạo PNG với alpha channel (dòng 138-144)
```python
bgra = cv2.cvtColor(crop_img, cv2.COLOR_BGR2BGRA)
bgra[:, :, 3] = crop_mask  # Set kênh alpha
cv2.imwrite(output_path, bgra)
```
**Giải thích:**
- BGRA = Blue, Green, Red, Alpha (4 kênh)
- Alpha = 255 (opaque) ở sản phẩm, 0 (transparent) ở nền
- PNG hỗ trợ alpha, JPG không

### Đoạn 5: Tính hiệu quả crop (dòng 193-195)
```python
saved_ratio = (1 - (w*h)/(img.shape[0]*img.shape[1]))*100
print(f"Tiết kiệm: {saved_ratio:.1f}% diện tích")
```
**Giải thích:** Đo lường hiệu quả crop - bao nhiêu % nền đã bị loại bỏ.

---

## 5. Tham Số Quan Trọng

| Tham Số | Giá trị | Ý nghĩa | Điều chỉnh |
|---------|---------|---------|-----------|
| Canny low | `50` | Ngưỡng thấp | Giảm (30-40) nếu edges yếu |
| Canny high | `150` | Ngưỡng cao | Tỉ lệ 1:2 hoặc 1:3 với low |
| Morphology kernel | `(5,5)` | Kích thước kernel | Tăng (7,7) nếu contour rất gián đoạn |
| Closing iterations | `2` | Số lần closing | Tăng lên 3 nếu vẫn có khe hở |
| Dilation iterations | `2` | Số lần dilation | Giảm xuống 1 nếu mask quá rộng |

---

## 6. Kết Quả Mong Đợi

### Ảnh output
- **product_cropped.png:** Sản phẩm với nền hoàn toàn trong suốt
- Khi mở trong Photoshop/GIMP: thấy checkerboard pattern (trong suốt)
- Kích thước: chỉ vừa đủ bao sản phẩm (tight crop)

### Console output
```
Tìm thấy 5 contours
Contour lớn nhất: 45680 pixels
Bounding box: x=350, y=180, w=100, h=320

Kích thước gốc: 800x600
Kích thước sau crop: 100x320
Tiết kiệm: 93.3% diện tích
```

---

## 7. Lỗi Thường Gặp

### Lỗi 1: Contour không phải sản phẩm (là nền)
**Nguyên nhân:** Nền có contour lớn hơn sản phẩm

**Cách fix:**
- Lọc contour theo tỉ lệ diện tích:
```python
img_area = img.shape[0] * img.shape[1]
valid = [c for c in cnts if 0.05*img_area < cv2.contourArea(c) < 0.8*img_area]
cnt = max(valid, key=cv2.contourArea)
```

### Lỗi 2: Mask bị lỗ/gián đoạn (sản phẩm có nhiều màu)
**Nguyên nhân:** Canny phát hiện cả edges bên trong sản phẩm

**Cách fix:**
- Tăng iterations cho Closing: `iterations=3`
- Hoặc dùng flood fill:
```python
h, w = mask.shape
flood_mask = mask.copy()
cv2.floodFill(flood_mask, None, (0,0), 255)
mask = cv2.bitwise_not(flood_mask)
```

### Lỗi 3: Viền sản phẩm bị cắt mất
**Nguyên nhân:** Dilation không đủ

**Cách fix:**
- Tăng iterations cho Dilation
- Hoặc thêm padding:
```python
pad = 5  # pixels
x, y, w, h = max(0, x-pad), max(0, y-pad), w+2*pad, h+2*pad
```

---

## 8. Mở Rộng

### Cải tiến 1: GrabCut cho mask chính xác hơn
```python
# Thay thế Canny + morphology bằng GrabCut
rect = (x, y, w, h)
mask = np.zeros(img.shape[:2], np.uint8)
bgd_model = np.zeros((1,65), np.float64)
fgd_model = np.zeros((1,65), np.float64)

cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
mask = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
```

### Cải tiến 2: Feathering cho alpha mượt
```python
# Làm mềm viền alpha
alpha = crop_mask.astype(np.float32)
alpha = cv2.GaussianBlur(alpha, (5,5), 2.0)
bgra[:, :, 3] = alpha.astype(np.uint8)
```

### Cải tiến 3: Shadow removal
```python
# Loại bỏ bóng trước khi crop
rgb_planes = cv2.split(img)
result_planes = []
for plane in rgb_planes:
    dilated = cv2.dilate(plane, np.ones((7,7), np.uint8))
    bg = cv2.medianBlur(dilated, 21)
    diff = 255 - cv2.absdiff(plane, bg)
    result_planes.append(diff)
img = cv2.merge(result_planes)
```

### Cải tiến 4: Batch processing
```python
import glob

for img_path in glob.glob('input/*.jpg'):
    img = cv2.imread(img_path)
    # ... xử lý ...
    output_name = os.path.basename(img_path).replace('.jpg', '.png')
    cv2.imwrite(f'output/{output_name}', bgra)
```

### Cải tiến 5: Deep learning (U-Net)
```python
# Train model segmentation
# Input: ảnh sản phẩm
# Output: mask chính xác đến từng pixel
# Xử lý được: sản phẩm phức tạp, bóng, phản chiếu
```

---

## Tips Đọc Code Nhanh

1. **Pipeline:** Canny → Morphology → Contour → Crop → Alpha
2. **Morphology** (dòng 100-108) là chìa khóa để mask tốt
3. **Alpha channel** (dòng 138-144) là điểm mới so với các bài khác
4. **Phần phân tích** (dòng 157-196) giải thích rõ ưu/nhược điểm
5. **Skip tạo ảnh mẫu** (dòng 42-75)

---

**Tổng số dòng:** 204 dòng
**Độ khó:** Trung bình
**Thời gian đọc hiểu:** 15-20 phút
**Thời gian chạy:** <1 giây
**Ứng dụng thực tế:** E-commerce (Shopee, Lazada), product photography, catalog tự động
