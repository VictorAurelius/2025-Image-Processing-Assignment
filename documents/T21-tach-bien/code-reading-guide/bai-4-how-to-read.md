# Bài 4: Kiểm Tra Lỗi Bề Mặt (QC) Sản Phẩm - Code Reading Guide

## 1. Tổng Quan

Phát hiện lỗi bề mặt (vết xước, rãnh, lõm) trên sản phẩm kim loại/nhựa bằng Laplacian filter (đạo hàm bậc 2), sau đó lọc nhiễu bằng morphology và connected components. Ứng dụng cho QC tự động trong sản xuất.

**File code:** `/code-implement/T21-tach-bien/bai-4-defect-detection/detect.py`

---

## 2. Input/Output

### Input
- **File:** `../input/sample-images/surface.jpg`
- **Mô tả:** Ảnh cận cảnh bề mặt sản phẩm (tấm kim loại, vỏ nhựa)
- **Format:** Grayscale

### Output
- **defect_mask.png:** Mask nhị phân các vùng lỗi
- **defect_overlay.png:** Ảnh gốc với lỗi được đánh dấu (contour đỏ, bbox xanh lá)
- **defect_response.png:** Laplacian response (để debug)

---

## 3. Thuật Toán Chính

### Bước 1: Tiền xử lý (dòng 82-84)
- Gaussian blur (σ=1.5) để giảm nhiễu

### Bước 2: Laplacian filter (dòng 86-93)
- Tính đạo hàm bậc 2 → nhấn mạnh điểm đổi cong, biên mảnh
- Lấy trị tuyệt đối và chuẩn hóa về 0-255

### Bước 3: Ngưỡng Otsu (dòng 96-97)
- Tự động tìm ngưỡng tối ưu để phân tách lỗi/nền

### Bước 4: Morphology (dòng 99-105)
- **Open:** Loại nhiễu hạt (kernel 3×3)
- **Close:** Nối nét đứt quãng (kernel 5×5)

### Bước 5: Lọc theo diện tích (dòng 107-132)
- Connected components analysis
- Loại bỏ vùng < 30 pixels (nhiễu)
- Tính x, y, w, h của mỗi lỗi

### Bước 6: Visualization (dòng 135-145)
- Vẽ contours lỗi (đỏ)
- Vẽ bounding boxes (xanh lá)
- Đánh số từng lỗi

---

## 4. Code Quan Trọng Cần Đọc

### Đoạn 1: Laplacian filter (dòng 86-93)
```python
lap = cv2.Laplacian(blur, cv2.CV_32F, ksize=3)
resp = np.abs(lap)
resp = (resp / resp.max() * 255).astype(np.uint8)
```
**Giải thích:** Laplacian = ∂²f/∂x² + ∂²f/∂y² → phát hiện thay đổi đột ngột về độ sáng (vết xước, rãnh). Dùng `CV_32F` để tránh overflow, sau đó chuẩn hóa về uint8.

### Đoạn 2: Otsu thresholding (dòng 96-97)
```python
otsu_thr, mask = cv2.threshold(resp, 0, 255,
                               cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```
**Giải thích:** Otsu tự động tìm ngưỡng tối ưu dựa trên histogram. Phù hợp khi lỗi/nền có phân bố rõ ràng. `otsu_thr` trả về giá trị ngưỡng tính được.

### Đoạn 3: Morphology operations (dòng 99-105)
```python
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,
                        np.ones((3, 3), np.uint8), iterations=1)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,
                        np.ones((5, 5), np.uint8), iterations=1)
```
**Giải thích:**
- **OPEN = Erosion + Dilation:** Xóa nhiễu hạt nhỏ
- **CLOSE = Dilation + Erosion:** Lấp khe hở trong lỗi
- Thứ tự quan trọng: Open trước để loại nhiễu, Close sau để nối nét

### Đoạn 4: Connected components với stats (dòng 108-127)
```python
n, lbl, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
min_area = 30

for i in range(1, n):  # Bỏ qua background (i=0)
    area = stats[i, cv2.CC_STAT_AREA]
    if area >= min_area:
        keep[lbl == i] = 255
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
```
**Giải thích:** `connectedComponentsWithStats` vừa gán nhãn vừa tính stats (diện tích, bbox) cho mỗi vùng. Hiệu quả hơn `findContours` + `contourArea` khi cần cả 2.

### Đoạn 5: Đánh giá QC pass/fail (dòng 158-175)
```python
total_defect_area = sum(area for _, area, _, _, _, _ in defects)
defect_ratio = (total_defect_area / surface_area) * 100

if len(defects) > 0:
    print(f"⚠ CẢNH BÁO: Phát hiện {len(defects)} lỗi bề mặt")
    print(f"  → Sản phẩm KHÔNG ĐẠT chất lượng QC")
```
**Giải thích:** Tính tỷ lệ % diện tích lỗi để đánh giá. Có thể thiết lập ngưỡng (ví dụ: >0.5% là fail).

---

## 5. Tham Số Quan Trọng

| Tham số | Giá trị | Ý nghĩa | Điều chỉnh |
|---------|---------|---------|-----------|
| Gaussian sigma | `1.5` | Độ mạnh blur | Tăng (2.0-3.0) nếu nhiễu mạnh |
| Laplacian ksize | `3` | Kích thước kernel | Có thể thử 5, 7 cho lỗi lớn hơn |
| min_area | `30` | Diện tích tối thiểu (pixels) | Tăng lên (50-100) để lọc nhiễu mạnh hơn |
| OPEN kernel | `(3,3)` | Kernel loại nhiễu | Tăng nếu nhiễu hạt lớn |
| CLOSE kernel | `(5,5)` | Kernel nối nét | Tăng nếu lỗi bị đứt quãng nhiều |

---

## 6. Kết Quả Mong Đợi

### Ảnh output
- **defect_mask.png:** Trắng = lỗi, Đen = nền
- **defect_overlay.png:** Lỗi được highlight với contour đỏ và bbox xanh lá
- **defect_response.png:** Ảnh grayscale cho thấy Laplacian response

### Console output
```
Tìm thấy 7 vùng (ngoài background)
Giữ lại 5 vùng lỗi hợp lệ:
  • Lỗi #1: diện tích=245 px², vị trí=(100,150), kích thước=60×8
  • Lỗi #2: diện tích=180 px², vị trí=(200,450), kích thước=50×7
  ...

✓ Tổng số lỗi phát hiện: 5
✓ Tổng diện tích lỗi: 850 pixels
✓ Tỷ lệ lỗi: 0.1771% diện tích
⚠ CẢNH BÁO: Phát hiện 5 lỗi bề mặt
  → Sản phẩm KHÔNG ĐẠT chất lượng QC
```

---

## 7. Lỗi Thường Gặp

### Lỗi 1: Phát hiện quá nhiều nhiễu (false positives)
**Nguyên nhân:**
- Bề mặt có texture nhiều hạt
- min_area quá nhỏ
- Blur chưa đủ mạnh

**Cách fix:**
- Tăng `min_area` lên 50-100
- Tăng Gaussian sigma lên 2.0-3.0
- Thêm iterations cho OPEN: `iterations=2`

### Lỗi 2: Bỏ sót lỗi thực (false negatives)
**Nguyên nhân:**
- Lỗi quá mờ/nhạt
- Otsu threshold không phù hợp

**Cách fix:**
- Giảm min_area xuống 20
- Thử adaptive threshold thay Otsu:
```python
mask = cv2.adaptiveThreshold(resp, 255,
                             cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                             cv2.THRESH_BINARY, 11, 2)
```
- Tăng độ tương phản trước khi xử lý: `clahe = cv2.createCLAHE(...)`

### Lỗi 3: Lỗi bị đứt quãng thành nhiều vùng nhỏ
**Nguyên nhân:** CLOSE kernel quá nhỏ

**Cách fix:**
- Tăng kernel CLOSE lên (7,7) hoặc (9,9)
- Tăng iterations: `iterations=2`

---

## 8. Mở Rộng

### Cải tiến 1: Phân loại loại lỗi
```python
# Dựa vào aspect ratio và diện tích
aspect = w / h
if aspect > 3.0:
    defect_type = "Xước dài"
elif aspect < 0.5:
    defect_type = "Xước dọc"
elif area > 200:
    defect_type = "Lõm/vết tròn"
else:
    defect_type = "Lỗi nhỏ"
```

### Cải tiến 2: Độ nghiêm trọng (severity)
```python
if defect_ratio < 0.1:
    severity = "NHẸ - Chấp nhận được"
elif defect_ratio < 0.5:
    severity = "TRUNG BÌNH - Cần kiểm tra"
else:
    severity = "NGHIÊM TRỌNG - Loại bỏ"
```

### Cải tiến 3: So sánh với template chuẩn
```python
# Tải ảnh sản phẩm chuẩn (không lỗi)
template = cv2.imread('template.jpg', cv2.IMREAD_GRAYSCALE)

# Align ảnh test với template
# Trừ 2 ảnh để tìm khác biệt
diff = cv2.absdiff(img, template)
_, defects = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
```

### Cải tiến 4: Sử dụng deep learning
```python
# Thay thế Laplacian bằng CNN
# Model: UNet, Mask R-CNN cho segmentation
# Training data: ảnh có/không lỗi được label
```

### Cải tiến 5: Multi-scale Laplacian
```python
# Phát hiện lỗi ở nhiều kích thước
scales = [1.0, 1.5, 2.0, 3.0]
responses = []
for sigma in scales:
    blur = cv2.GaussianBlur(img, (0,0), sigma)
    lap = cv2.Laplacian(blur, cv2.CV_32F)
    responses.append(np.abs(lap))

# Tổng hợp (max hoặc mean)
final_resp = np.max(responses, axis=0)
```

---

## Tips Đọc Code Nhanh

1. **Hiểu Laplacian** (dòng 86-93) - cốt lõi của thuật toán
2. **Pipeline morphology** (dòng 99-105) - quan trọng để lọc nhiễu
3. **Connected components** (dòng 108-127) - cách lọc theo diện tích
4. **Phần đánh giá QC** (dòng 158-175) - logic pass/fail
5. **Skip phần tạo ảnh mẫu** (dòng 42-68) nếu có ảnh input

---

**Tổng số dòng:** 182 dòng
**Độ khó:** Trung bình
**Thời gian đọc hiểu:** 15-20 phút
**Thời gian chạy:** <1 giây
**Ứng dụng thực tế:** QC tự động trong sản xuất điện tử, ô tô, nhựa, kim loại
