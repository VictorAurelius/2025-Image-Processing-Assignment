# Bài 2: Tách Biên & Tự Động Scan Phẳng Tài Liệu - Code Reading Guide

## 1. Tổng Quan

Tự động phát hiện 4 góc của tờ giấy A4 chụp nghiêng bằng điện thoại, sau đó dùng perspective transform để "scan phẳng" tài liệu về góc nhìn vuông góc. Đây là kỹ thuật cơ bản cho các ứng dụng scan tài liệu như CamScanner.

**File code:** `/code-implement/T21-tach-bien/bai-2-document-scanning/scan.py`

---

## 2. Input/Output

### Input
- **File:** `../input/sample-images/doc.jpg`
- **Mô tả:** Ảnh tờ giấy A4 chụp bằng điện thoại (góc nghiêng bất kỳ)
- **Yêu cầu:** Giấy có viền rõ ràng, tương phản với nền

### Output
- **File chính:** `doc_scanned.jpg` - Tài liệu đã scan phẳng (1240×1754 pixels - tỉ lệ A4)
- **File debug:** `doc_debug.jpg` - Ảnh gốc với 4 góc đã phát hiện được đánh dấu

---

## 3. Thuật Toán Chính

### Bước 1: Tiền xử lý (dòng 122-135)
- Chuyển sang grayscale
- Gaussian blur (σ=1.2) để giảm nhiễu
- Tính ngưỡng Otsu tự động
- Canny edge detection với ngưỡng động

### Bước 2: Tìm contour tài liệu (dòng 137-149)
- `findContours()` tìm tất cả contours
- Chọn contour lớn nhất (giả định là tài liệu)
- Xấp xỉ thành đa giác với `approxPolyDP()` (epsilon = 2% chu vi)

### Bước 3: Sắp xếp 4 đỉnh với `order_pts()` (dòng 32-57)
- **Top-Left:** Tổng (x+y) nhỏ nhất
- **Bottom-Right:** Tổng (x+y) lớn nhất
- **Top-Right:** Hiệu (x-y) nhỏ nhất
- **Bottom-Left:** Hiệu (x-y) lớn nhất

### Bước 4: Perspective transform (dòng 169-179)
- Định nghĩa 4 điểm đích (góc vuông A4: 1240×1754)
- Tính ma trận biến đổi với `getPerspectiveTransform()`
- Warp ảnh với `warpPerspective()`

---

## 4. Code Quan Trọng Cần Đọc

### Đoạn 1: Hàm sắp xếp 4 đỉnh (dòng 32-57)
```python
def order_pts(pts):
    s = pts.sum(axis=1)        # x + y
    diff = np.diff(pts, axis=1) # x - y

    tl = pts[np.argmin(s)]      # Top-left: tổng nhỏ nhất
    br = pts[np.argmax(s)]      # Bottom-right: tổng lớn nhất
    tr = pts[np.argmin(diff)]   # Top-right: hiệu nhỏ nhất
    bl = pts[np.argmax(diff)]   # Bottom-left: hiệu lớn nhất

    return np.array([tl, tr, br, bl], dtype=np.float32)
```
**Giải thích:** Trick thông minh để sắp xếp 4 điểm theo thứ tự cố định mà không cần biết ban đầu chúng ở vị trí nào. Quan trọng để perspective transform đúng.

### Đoạn 2: Canny với ngưỡng tự động (dòng 129-135)
```python
_, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
edges = cv2.Canny(blur, th * 0.5, th * 1.5)
```
**Giải thích:** Dùng Otsu để tính ngưỡng tối ưu, sau đó dùng làm tham chiếu cho Canny (low = 0.5×Otsu, high = 1.5×Otsu). Tự động thích nghi với độ tương phản ảnh.

### Đoạn 3: Xấp xỉ đa giác (dòng 146-149)
```python
peri = cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
pts = approx.reshape(-1, 2).astype(np.float32)
```
**Giải thích:** `approxPolyDP()` đơn giản hóa contour thành đa giác. Epsilon = 2% chu vi là giá trị chuẩn, cho phép sai lệch nhỏ để lọc nhiễu nhưng vẫn giữ được hình dạng.

### Đoạn 4: Xử lý trường hợp không tìm được tứ giác (dòng 153-159)
```python
if len(pts) != 4:
    print(f"WARNING: Không tìm được tứ giác...")
    # Fallback: dùng minAreaRect
    rect = cv2.minAreaRect(cnt)
    pts = cv2.boxPoints(rect).astype(np.float32)
```
**Giải thích:** Xử lý robust: nếu xấp xỉ không cho 4 đỉnh (ví dụ tài liệu bo góc), dùng bounding box xoay làm backup.

### Đoạn 5: Perspective transform (dòng 169-179)
```python
w, h = 1240, 1754  # Tỉ lệ A4 (√2)
dst = np.array([[0, 0], [w-1, 0], [w-1, h-1], [0, h-1]], np.float32)
M = cv2.getPerspectiveTransform(src, dst)
scan = cv2.warpPerspective(img, M, (w, h))
```
**Giải thích:** Biến đổi từ 4 điểm bất kỳ (src) sang 4 góc hình chữ nhật (dst). Ma trận M là phép biến đổi affine 3×3. Kết quả là ảnh vuông góc hoàn hảo.

---

## 5. Tham Số Quan Trọng

| Tham số | Giá trị | Ý nghĩa | Điều chỉnh |
|---------|---------|---------|-----------|
| Gaussian `ksize` | `(5,5)` | Kích thước kernel blur | Tăng lên (7,7) nếu ảnh nhiễu |
| Gaussian `sigma` | `1.2` | Độ mạnh blur | Tăng (1.5-2.0) nếu cần làm trơn hơn |
| Canny multiplier | `0.5`, `1.5` | Hệ số nhân với ngưỡng Otsu | Điều chỉnh nếu edges quá yếu/mạnh |
| `approxPolyDP` epsilon | `0.02 * peri` | Sai số cho phép (2% chu vi) | Giảm (0.01) nếu cần chính xác hơn |
| Output size | `1240×1754` | Kích thước A4 chuẩn | Thay đổi theo nhu cầu (ví dụ: 2480×3508 cho 300 DPI) |

---

## 6. Kết Quả Mong Đợi

### Ảnh output
- `doc_scanned.jpg`: Tài liệu hoàn toàn vuông góc, kích thước chuẩn
- Nội dung text/hình ảnh trên giấy rõ nét, không bị méo
- Tỉ lệ A4 chuẩn (chiều cao/chiều rộng = √2 ≈ 1.414)

### Console output
```
1. Đã áp dụng Gaussian blur (σ=1.2)
2. Ngưỡng Otsu tính được: 127.5
3. Đã phát hiện biên bằng Canny (ngưỡng: 63.8, 191.2)
4. Tìm thấy 15 contours
5. Contour lớn nhất có diện tích: 245680 pixels
6. Xấp xỉ đa giác: 4 đỉnh
7. Đã sắp xếp 4 đỉnh: TL, TR, BR, BL
```

### Debug visualization
- 4 góc được đánh số từ 1-4 (màu đỏ)
- Contour giấy màu xanh lá

---

## 7. Lỗi Thường Gặp

### Lỗi 1: "WARNING: Không tìm được tứ giác tài liệu (tìm được X đỉnh)"
**Nguyên nhân:**
- Tài liệu bo góc tròn
- Epsilon quá lớn hoặc quá nhỏ
- Contour bị gián đoạn do ánh sáng không đều

**Cách fix:**
- Code đã có fallback (minAreaRect) → check xem kết quả có chấp nhận được không
- Điều chỉnh epsilon: thử `0.01 * peri` hoặc `0.03 * peri`
- Thêm morphology closing trước findContours:
```python
edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))
```

### Lỗi 2: Ảnh scan bị méo/nghiêng sai
**Nguyên nhân:** 4 điểm được sắp xếp sai thứ tự

**Cách fix:**
- Kiểm tra output của `order_pts()` bằng cách vẽ debug (code đã có tại dòng 186-194)
- Đảm bảo `src` và `dst` cùng thứ tự: [TL, TR, BR, BL]

### Lỗi 3: Contour tìm được không phải tài liệu (là nền hoặc vật khác)
**Nguyên nhân:** Nền có contour lớn hơn tài liệu

**Cách fix:**
- Lọc contour theo tỉ lệ diện tích với ảnh:
```python
img_area = img.shape[0] * img.shape[1]
valid_cnts = [c for c in cnts if 0.1*img_area < cv2.contourArea(c) < 0.9*img_area]
cnt = max(valid_cnts, key=cv2.contourArea)
```

---

## 8. Mở Rộng

### Cải tiến 1: Tự động cắt viền trắng
```python
# Sau khi scan, cắt bỏ phần viền trắng dư thừa
gray_scan = cv2.cvtColor(scan, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray_scan, 250, 255, cv2.THRESH_BINARY_INV)
cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if cnts:
    x, y, w, h = cv2.boundingRect(max(cnts, key=cv2.contourArea))
    scan = scan[y:y+h, x:x+w]
```

### Cải tiến 2: Chuẩn hóa độ sáng
```python
# Sau scan, cân bằng histogram để text rõ hơn
gray_scan = cv2.cvtColor(scan, cv2.COLOR_BGR2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
enhanced = clahe.apply(gray_scan)
scan = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
```

### Cải tiến 3: Phát hiện nhiều tài liệu
```python
# Sắp xếp contours theo diện tích
cnts_sorted = sorted(cnts, key=cv2.contourArea, reverse=True)
for i, cnt in enumerate(cnts_sorted[:3]):  # Xử lý 3 contour lớn nhất
    if cv2.contourArea(cnt) > min_area:
        # Scan từng tài liệu
```

### Cải tiến 4: Tự động phát hiện hướng (portrait/landscape)
```python
w_doc = np.linalg.norm(src[0] - src[1])
h_doc = np.linalg.norm(src[1] - src[2])
if w_doc > h_doc:  # Landscape
    w, h = 1754, 1240
else:              # Portrait
    w, h = 1240, 1754
```

### Cải tiến 5: Thêm shadow removal
```python
# Loại bỏ bóng trên tài liệu
rgb_planes = cv2.split(scan)
result_planes = []
for plane in rgb_planes:
    dilated = cv2.dilate(plane, np.ones((7,7), np.uint8))
    bg = cv2.medianBlur(dilated, 21)
    diff = 255 - cv2.absdiff(plane, bg)
    result_planes.append(diff)
scan = cv2.merge(result_planes)
```

---

## Tips Đọc Code Nhanh

1. **Bắt đầu từ flow chính** (dòng 110-205): đọc theo trình tự comments để hiểu pipeline
2. **Hàm `order_pts()` là chìa khóa** (dòng 32) - đọc kỹ để hiểu logic sắp xếp
3. **Phần tạo ảnh mẫu** (dòng 68-108) có thể skip nếu đã có ảnh input
4. **Chú ý fallback logic** (dòng 153-159) để xử lý edge cases
5. **Debug visualization** (dòng 186-194) rất hữu ích khi troubleshoot

---

**Tổng số dòng:** 206 dòng
**Độ khó:** Trung bình-Khó
**Thời gian đọc hiểu:** 20-25 phút
**Thời gian chạy:** ~1-2 giây
**Ứng dụng thực tế:** CamScanner, Adobe Scan, Office Lens
