# Bài 5: Đếm Vật Tròn (Đồng Xu/Bi) - Code Reading Guide

## 1. Tổng Quan

Đếm số lượng đồng xu hoặc bi tròn trong ảnh bằng CLAHE (cân bằng sáng), Canny edge detection và Hough Circle Transform. Phân tích kích thước các vật tròn phát hiện được.

**File code:** `/code-implement/T21-tach-bien/bai-5-coin-counting/count.py`

---

## 2. Input/Output

### Input
- **File:** `../input/sample-images/coins.jpg`
- **Mô tả:** Ảnh bàn có nhiều đồng xu/bi tròn, chụp từ trên xuống, ít chồng lấn
- **Format:** RGB

### Output
- **coins_detected.jpg:** Ảnh với circles được đánh dấu (viền xanh lá, tâm đỏ, đánh số)
- **coins_edges.png:** Canny edges (debug)
- **coins_clahe.png:** Ảnh sau CLAHE (debug)

---

## 3. Thuật Toán Chính

### Bước 1: Cân bằng sáng với CLAHE (dòng 100-103)
- Adaptive histogram equalization cho từng vùng 8×8
- Tăng tương phản cục bộ, xử lý ánh sáng không đều

### Bước 2: Gaussian blur (dòng 105-107)
- Blur nhẹ (σ=1.2) để giảm nhiễu nhưng giữ biên tròn

### Bước 3: Canny edge detection (dòng 109-113)
- Ngưỡng 80-160 để lấy biên của đồng xu

### Bước 4: Hough Circle Transform (dòng 117-126)
- Phát hiện hình tròn với tham số tối ưu
- minRadius=10, maxRadius=80

### Bước 5: Vẽ và phân tích (dòng 129-152)
- Sắp xếp circles theo tọa độ y (từ trên xuống)
- Vẽ circle, tâm, đánh số
- Tính thống kê bán kính

---

## 4. Code Quan Trọng Cần Đọc

### Đoạn 1: CLAHE để cân bằng sáng (dòng 100-103)
```python
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
clahe_img = clahe.apply(gray)
```
**Giải thích:** CLAHE (Contrast Limited Adaptive HE) xử lý từng tile 8×8 riêng biệt, tránh over-amplification (clipLimit=2.0). Quan trọng khi ánh sáng không đều.

### Đoạn 2: HoughCircles với tham số quan trọng (dòng 117-126)
```python
circles = cv2.HoughCircles(
    blur,
    cv2.HOUGH_GRADIENT,
    dp=1.2,              # Độ phân giải accumulator (>1 = thô hơn, nhanh hơn)
    minDist=30,          # Khoảng cách tối thiểu giữa tâm
    param1=120,          # Ngưỡng cao Canny (tự động)
    param2=25,           # Ngưỡng tích lũy (thấp = nhiều circles)
    minRadius=10,
    maxRadius=80
)
```
**Giải thích:**
- `dp=1.2`: Accumulator resolution = image/1.2 → trade-off tốc độ/độ chính xác
- `minDist=30`: Tránh detect 1 đồng xu thành nhiều circles
- `param2=25`: Ngưỡng quan trọng nhất - giảm để phát hiện nhiều hơn, tăng để lọc nhiễu

### Đoạn 3: Sắp xếp circles theo tọa độ (dòng 138-140)
```python
circles_sorted = sorted(circles, key=lambda c: (c[1], c[0]))
# c[1] = y (ưu tiên), c[0] = x (phụ)
```
**Giải thích:** Sắp xếp từ trên xuống (y), trái sang phải (x) để đánh số theo thứ tự đọc tự nhiên.

### Đoạn 4: Visualization chi tiết (dòng 141-152)
```python
for idx, (x, y, r) in enumerate(circles_sorted, 1):
    cv2.circle(out, (x, y), r, (0, 255, 0), 2)      # Viền
    cv2.circle(out, (x, y), 2, (0, 0, 255), 3)      # Tâm
    cv2.putText(out, str(idx), (x - 10, y + 5), ... ) # Số
```
**Giải thích:** 3 lớp visualization: viền circle (xanh lá), tâm (đỏ), số thứ tự (xanh dương).

### Đoạn 5: Phân loại kích thước (dòng 186-193)
```python
avg_radius = np.mean(radii)
std_radius = np.std(radii)

small = sum(1 for r in radii if r < avg_radius - std_radius)
medium = sum(1 for r in radii if avg_radius - std_radius <= r <= avg_radius + std_radius)
large = sum(1 for r in radii if r > avg_radius + std_radius)
```
**Giải thích:** Phân loại dựa trên thống kê (mean ± std). Phát hiện nếu có đồng xu kích thước khác nhau.

---

## 5. Tham Số Quan Trọng

| Tham số | Giá trị | Ý nghĩa | Điều chỉnh |
|---------|---------|---------|-----------|
| CLAHE clipLimit | `2.0` | Giới hạn tăng tương phản | Tăng (3.0-4.0) nếu ảnh tối |
| CLAHE tileGridSize | `(8,8)` | Kích thước tile | Giảm (4,4) cho chi tiết, tăng (16,16) cho tổng thể |
| Gaussian ksize | `(7,7)` | Kích thước kernel | Phải lẻ; tăng nếu nhiễu mạnh |
| Canny threshold | `80, 160` | Low/high threshold | Điều chỉnh nếu edges quá nhiều/ít |
| HoughCircles dp | `1.2` | Độ phân giải | 1.0 = chính xác, 2.0 = nhanh |
| minDist | `30` | Khoảng cách tối thiểu | = 0.8 × đường kính đồng xu nhỏ nhất |
| param2 | `25` | **Ngưỡng quan trọng nhất** | Giảm (15-20) nếu thiếu, tăng (30-40) nếu nhiễu |
| minRadius | `10` | Bán kính nhỏ nhất | Dựa vào đồng xu nhỏ nhất |
| maxRadius | `80` | Bán kính lớn nhất | Dựa vào đồng xu lớn nhất |

---

## 6. Kết Quả Mong Đợi

### Ảnh output
- Mỗi đồng xu được đánh dấu rõ ràng với số thứ tự
- Không có false positives (phát hiện sai)
- Không bỏ sót đồng xu (false negatives)

### Console output
```
✓ Phát hiện được 8 vật tròn:
  • Vật #1: tâm=(150,150), bán kính=60 pixels
  • Vật #2: tâm=(350,180), bán kính=50 pixels
  ...

Thống kê bán kính:
  - Trung bình: 45.5 pixels
  - Độ lệch chuẩn: 5.2 pixels
  - Min: 42 pixels
  - Max: 50 pixels

Phân loại kích thước:
  - Nhỏ: 2 vật
  - Trung bình: 4 vật
  - Lớn: 2 vật
```

---

## 7. Lỗi Thường Gặp

### Lỗi 1: Không phát hiện được vật tròn nào
**Nguyên nhân:**
- `param2` quá cao
- minRadius/maxRadius không phù hợp
- Ảnh quá tối/mờ

**Cách fix:**
- Giảm `param2` từ 25 xuống 15-20
- Kiểm tra ảnh CLAHE: `cv2.imwrite('debug_clahe.png', clahe_img)`
- Kiểm tra edges: `cv2.imwrite('debug_edges.png', edges)`
- Điều chỉnh minRadius/maxRadius theo kích thước thực

### Lỗi 2: Phát hiện nhiều circles trùng lặp cho 1 đồng xu
**Nguyên nhân:** `minDist` quá nhỏ

**Cách fix:**
- Tăng `minDist` lên (40-50)
- Hoặc lọc circles trùng lặp sau:
```python
filtered = []
for c in circles[0]:
    if all(np.linalg.norm(c[:2] - f[:2]) > 30 for f in filtered):
        filtered.append(c)
```

### Lỗi 3: Bỏ sót đồng xu bị che khuất một phần
**Nguyên nhân:** HoughCircles yêu cầu circle hoàn chỉnh

**Cách fix:**
- Giảm `param2` để nhạy hơn
- Hoặc dùng contour-based approach:
```python
cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for cnt in cnts:
    area = cv2.contourArea(cnt)
    peri = cv2.arcLength(cnt, True)
    circularity = 4 * np.pi * area / (peri * peri)
    if circularity > 0.8:  # Gần tròn
        # Đếm là đồng xu
```

---

## 8. Mở Rộng

### Cải tiến 1: Tính tổng tiền (nếu biết mệnh giá)
```python
# Giả sử: bán kính lớn = 500đ, nhỏ = 200đ
coin_values = []
for r in radii:
    if r > avg_radius:
        coin_values.append(500)
    else:
        coin_values.append(200)

total = sum(coin_values)
print(f"Tổng tiền: {total:,} VND")
```

### Cải tiến 2: Phân loại màu sắc
```python
# Lấy màu trung bình trong vùng circle
for x, y, r in circles[0]:
    mask = np.zeros(img.shape[:2], np.uint8)
    cv2.circle(mask, (x, y), r, 255, -1)
    mean_color = cv2.mean(img, mask=mask)[:3]

    # Phân loại dựa vào màu
    if mean_color[0] < 100:  # Màu vàng (B thấp)
        coin_type = "Vàng"
    else:
        coin_type = "Bạc"
```

### Cải tiến 3: Xử lý đồng xu chồng lấn
```python
# Dùng watershed algorithm
from scipy import ndimage

# Distance transform
dist = ndimage.distance_transform_edt(mask)

# Find peaks (coin centers)
local_max = peak_local_max(dist, min_distance=20)

# Watershed segmentation
markers = ndimage.label(local_max)[0]
labels = watershed(-dist, markers, mask=mask)
```

### Cải tiến 4: Deep learning approach
```python
# Dùng YOLO hoặc Faster R-CNN để detect
# Ưu điểm: xử lý được chồng lấn, góc nghiêng
```

### Cải tiến 5: Tính kích thước thực (mm)
```python
# Nếu biết kích thước thực 1 đồng xu (ví dụ: 23.6mm)
known_diameter_mm = 23.6
known_radius_px = circles[0][0][2]  # Giả sử đồng xu đầu tiên

px_per_mm = known_radius_px / (known_diameter_mm / 2)

for x, y, r in circles[0]:
    diameter_mm = 2 * r / px_per_mm
    print(f"Đường kính: {diameter_mm:.2f} mm")
```

---

## Tips Đọc Code Nhanh

1. **Hiểu pipeline:** CLAHE → Blur → Canny → HoughCircles
2. **Tham số HoughCircles** (dòng 117-126) là then chốt
3. **Phần thống kê** (dòng 174-193) cho thông tin chi tiết
4. **Chú ý sorting** (dòng 138) để hiểu cách đánh số
5. **Skip phần tạo ảnh mẫu** (dòng 42-82)

---

**Tổng số dòng:** 200 dòng
**Độ khó:** Trung bình
**Thời gian đọc hiểu:** 15-20 phút
**Thời gian chạy:** <1 giây
**Ứng dụng thực tế:** Đếm tiền tự động, kiểm kho, QC viên nén, kiểm tra linh kiện tròn
