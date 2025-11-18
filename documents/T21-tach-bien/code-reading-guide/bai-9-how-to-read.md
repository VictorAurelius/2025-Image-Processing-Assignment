# Bài 9: Đo Kích Thước Vật Thể Bằng Chuẩn Kích Thước - Code Reading Guide

## 1. Tổng Quan

Đo kích thước thực (mm) của vật thể bằng cách sử dụng đồng xu/A4 làm vật chuẩn. Tìm đồng xu bằng HoughCircles, tính tỉ lệ px/mm, sau đó đo vật thể bằng MinAreaRect.

**File code:** `/code-implement/T21-tach-bien/bai-9-object-measurement/measure.py`

---

## 2. Input/Output

### Input
- **File:** `../input/sample-images/measure.jpg`
- **Mô tả:** Ảnh có 1 đồng xu làm chuẩn + vật thể cần đo (ốc, vít, ...)
- **Yêu cầu:** Camera đặt gần vuông góc

### Output
- **measure_out.jpg:** Ảnh với đồng xu chuẩn (xanh dương), vật thể (xanh lá), kích thước (mm)
- **measure_edges.png:** Canny edges (debug)

---

## 3. Thuật Toán Chính

### Bước 1: Tìm đồng xu chuẩn (dòng 119-154)
- Gaussian blur
- **HoughCircles** để phát hiện đồng xu
- Lấy bán kính r (pixels)
- Tính tỉ lệ: `px_per_mm = (2*r) / coin_d_mm`

### Bước 2: Tìm vật thể (dòng 156-194)
- Canny edge detection
- `findContours()` → lọc contours (loại đồng xu, loại nhiễu)
- Chọn contour lớn nhất không phải đồng xu

### Bước 3: Đo kích thước vật thể (dòng 196-219)
- **MinAreaRect:** Tính bounding box xoay (w, h, angle)
- Quy đổi pixels sang mm: `w_mm = w / px_per_mm`

### Bước 4: Visualization (dòng 221-265)
- Vẽ đồng xu chuẩn
- Vẽ vật thể với bbox xoay
- Vẽ các đường đo chiều rộng/dài
- Thêm text kích thước

---

## 4. Code Quan Trọng Cần Đọc

### Đoạn 1: Tìm đồng xu và tính tỉ lệ (dòng 127-154)
```python
cir = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT,
                       dp=1.2, minDist=50, param1=120, param2=25,
                       minRadius=20, maxRadius=120)

x, y, r = np.round(cir[0, 0]).astype(int)
coin_d_mm = 23.6  # Đường kính đồng xu chuẩn (Euro)
px_per_mm = (2 * r) / coin_d_mm
```
**Giải thích:**
- Phát hiện đồng xu = circle
- Đường kính (pixels) = 2r
- **Tỉ lệ:** pixels/mm = (2r pixels) / (23.6 mm)
- Ví dụ: 2r=120px, coin=23.6mm → px_per_mm=5.08

### Đoạn 2: Lọc contours (loại đồng xu) (dòng 166-189)
```python
coin_area = math.pi * r * r
valid_cnts = []

for cnt in cnts:
    area = cv2.contourArea(cnt)
    # Bỏ qua contour quá nhỏ hoặc là đồng xu
    if area > 500 and abs(area - coin_area) > coin_area * 0.3:
        valid_cnts.append(cnt)
```
**Giải thích:**
- Diện tích đồng xu = πr²
- Loại contour có area gần bằng coin_area (±30%)
- Loại contour quá nhỏ (<500 px²)

### Đoạn 3: MinAreaRect (dòng 196-209)
```python
rect = cv2.minAreaRect(cnt)
(cx, cy), (w, h), angle = rect

# Đảm bảo w < h (chiều rộng < chiều dài)
if w > h:
    w, h = h, w
    angle = angle + 90
```
**Giải thích:**
- **MinAreaRect:** Bounding box xoay nhỏ nhất
- Trả về: center, (width, height), angle
- Chuẩn hóa: w luôn là chiều ngắn, h là chiều dài

### Đoạn 4: Quy đổi sang mm (dòng 211-219)
```python
w_mm = w / px_per_mm
h_mm = h / px_per_mm
area_mm2 = (area / (px_per_mm ** 2))
```
**Giải thích:**
- **Chiều dài:** chia cho px_per_mm
- **Diện tích:** chia cho px_per_mm²
- Ví dụ: w=100px, px_per_mm=5 → w_mm=20mm

### Đoạn 5: Vẽ các đường đo (dòng 246-261)
```python
# Chiều rộng: giữa 2 cạnh dài
mid1 = ((box[0][0] + box[1][0]) // 2, (box[0][1] + box[1][1]) // 2)
mid2 = ((box[2][0] + box[3][0]) // 2, (box[2][1] + box[3][1]) // 2)
cv2.line(out, mid1, mid2, (255, 255, 0), 2)

# Chiều dài: giữa 2 cạnh ngắn
mid3 = ((box[1][0] + box[2][0]) // 2, (box[1][1] + box[2][1]) // 2)
mid4 = ((box[3][0] + box[0][0]) // 2, (box[3][1] + box[0][1]) // 2)
cv2.line(out, mid3, mid4, (255, 0, 255), 2)
```
**Giải thích:** Vẽ đường nối giữa 2 cạnh để hiển thị chiều rộng/dài. Màu khác nhau để phân biệt.

---

## 5. Tham Số Quan Trọng

| Tham Số | Giá trị | Ý nghĩa | Điều chỉnh |
|---------|---------|---------|-----------|
| coin_d_mm | `23.6` | Đường kính đồng xu chuẩn (mm) | **QUAN TRỌNG:** Thay đổi theo đồng xu thực (500VND=24mm, 1Euro=23.6mm) |
| HoughCircles param2 | `25` | Ngưỡng circle | Điều chỉnh nếu không phát hiện được đồng xu |
| minRadius/maxRadius | `20/120` | Range bán kính đồng xu | Dựa vào kích thước đồng xu |
| Canny threshold | `80, 160` | Edge detection | Điều chỉnh nếu edges không rõ |
| coin_area tolerance | `0.3` | ±30% diện tích đồng xu | Tăng nếu lọc quá strict |
| min_area | `500` | Contour tối thiểu | Tăng để lọc nhiễu |

---

## 6. Kết Quả Mong Đợi

### Ảnh output
- Đồng xu chuẩn: viền xanh dương, text "Standard: 23.6mm"
- Vật thể: bbox xanh lá, góc đánh dấu đỏ
- Đường đo: chiều rộng (vàng), chiều dài (hồng)
- Text: kích thước mm ở nhiều vị trí

### Console output
```
=== BƯỚC 1: TÌM ĐỒNG XU CHUẨN ===
✓ Phát hiện đồng xu: tâm=(150,150), bán kính=60 pixels
Đường kính đồng xu chuẩn: 23.6 mm
Tỉ lệ: 5.085 pixels/mm

=== BƯỚC 2: TÌM VÀ ĐO VẬT THỂ ===
Chọn vật thể có diện tích: 7854 pixels²
MinAreaRect:
  - Tâm: (600.0, 400.0)
  - Kích thước (pixels): 38.0 × 203.0
  - Góc xoay: 25.0°

Kích thước thực (mm):
  - Chiều rộng: 7.47 mm
  - Chiều dài: 39.92 mm
  - Diện tích: 303.77 mm²

Đặc trưng hình học:
  - Aspect ratio (H/W): 5.342
  - Compactness: 0.758
  → Hình dạng dài/elongated
```

---

## 7. Lỗi Thường Gặp

### Lỗi 1: "ERROR: Không thấy đồng xu chuẩn trong ảnh!"
**Nguyên nhân:**
- Không có đồng xu
- Đồng xu bị che/mờ
- Tham số HoughCircles không phù hợp

**Cách fix:**
- Thêm đồng xu vào ảnh
- Giảm `param2` từ 25 xuống 15-20
- Điều chỉnh minRadius/maxRadius
- Debug: `cv2.imwrite('debug_blur.png', blur)`

### Lỗi 2: Đo sai (kích thước không đúng thực tế)
**Nguyên nhân:**
- **coin_d_mm sai** (quan trọng nhất!)
- Đồng xu bị méo/nghiêng
- Camera không vuông góc

**Cách fix:**
- Kiểm tra lại đường kính đồng xu:
  - 500 VND: 24.0 mm
  - 1 Euro: 23.6 mm
  - 25 cent USD: 24.26 mm
- Chụp lại với camera vuông góc

### Lỗi 3: "WARNING: Không tìm thấy vật thể để đo!"
**Nguyên nhân:**
- Vật thể quá nhỏ (<500 px²)
- Vật thể bị lọc nhầm (area gần coin_area)

**Cách fix:**
- Giảm `min_area` xuống 200-300
- Điều chỉnh tolerance từ 0.3 lên 0.5
- Kiểm tra edges: có phát hiện được vật thể không?

---

## 8. Mở Rộng

### Cải tiến 1: Sử dụng nhiều đồng xu để tăng độ chính xác
```python
# Lấy trung bình từ nhiều đồng xu
if len(circles[0]) > 1:
    avg_radius = np.mean([c[2] for c in circles[0]])
    px_per_mm = (2 * avg_radius) / coin_d_mm
```

### Cải tiến 2: Perspective correction
```python
# Nếu camera nghiêng, tính toán perspective warp trước
# Dùng 4 đồng xu làm reference points
```

### Cải tiến 3: Đo nhiều vật thể
```python
# Lặp qua tất cả valid_cnts
for cnt in valid_cnts:
    rect = cv2.minAreaRect(cnt)
    # Đo từng vật thể
```

### Cải tiến 4: ArUco markers thay vì đồng xu
```python
# Dùng ArUco marker làm chuẩn
# Ưu điểm: Chính xác hơn, phát hiện tốt hơn
import cv2.aruco as aruco

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()
corners, ids, _ = aruco.detectMarkers(img, aruco_dict, parameters=parameters)

# Tính tỉ lệ từ kích thước marker đã biết
```

### Cải tiến 5: GUI để nhập coin_d_mm
```python
import tkinter as tk

def get_coin_diameter():
    root = tk.Tk()
    # GUI để user chọn loại đồng xu
    # Trả về đường kính tương ứng
```

---

## Tips Đọc Code Nhanh

1. **2 bước chính:** Tìm đồng xu → Đo vật thể
2. **Tỉ lệ px/mm** (dòng 153) là cốt lõi
3. **Lọc contours** (dòng 166-189) để tách đồng xu/vật thể
4. **MinAreaRect** (dòng 196-209) cho bbox xoay
5. **Quy đổi đơn vị** (dòng 211-219) rất đơn giản

---

**Tổng số dòng:** 308 dòng
**Độ khó:** Trung bình-Khó
**Thời gian đọc hiểu:** 25-30 phút
**Thời gian chạy:** <1 giây
**Ứng dụng thực tế:** QC sản xuất, đo linh kiện điện tử, kiểm tra kích thước sản phẩm
