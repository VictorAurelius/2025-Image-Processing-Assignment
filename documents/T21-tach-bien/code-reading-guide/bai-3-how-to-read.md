# Bài 3: Dò Làn Đường Cơ Bản - Code Reading Guide

## 1. Tổng Quan

Phát hiện làn đường trái/phải từ ảnh camera hành trình sử dụng ROI masking, Sobel edge detection theo hướng x, và Hough Lines Transform. Đây là nền tảng cho các hệ thống cảnh báo lệch làn (Lane Departure Warning).

**File code:** `/code-implement/T21-tach-bien/bai-3-lane-detection/detect.py`

---

## 2. Input/Output

### Input
- **File:** `../input/sample-images/road.jpg`
- **Mô tả:** Ảnh hoặc frame video từ camera trước xe trên đường cao tốc
- **Điều kiện:** Ban ngày, trời nắng, làn đường rõ ràng

### Output
- **File chính:** `lanes_overlay.jpg` - Ảnh với làn đường được highlight
  - Làn trái: màu xanh lá
  - Làn phải: màu xanh dương
  - ROI: viền màu hồng
- **File debug:** `lanes_edges.jpg` - Ảnh edges sau Sobel

---

## 3. Thuật Toán Chính

### Bước 1: Tiền xử lý và ROI (dòng 101-116)
- Chuyển sang grayscale
- Tạo ROI mask hình thang (vùng phía trước xe)
- Áp dụng mask để loại bỏ bầu trời, biển báo, xe khác

### Bước 2: Edge detection theo hướng x (dòng 118-127)
- Gaussian blur (σ=1.2)
- **Sobel theo x** (chỉ gradient ngang) → nhấn mạnh biên dọc
- Ngưỡng 30% magnitude max để lấy edges

### Bước 3: Hough Lines Transform (dòng 131-139)
- Tìm các đoạn thẳng trong ảnh edges
- Tham số: threshold=60, minLineLength=50, maxLineGap=150

### Bước 4: Phân loại làn trái/phải (dòng 142-157)
- Tính slope (hệ số góc) của mỗi đoạn thẳng
- **Slope < -0.5:** Làn trái (góc nghiêng xuống trái)
- **Slope > 0.5:** Làn phải (góc nghiêng xuống phải)

### Bước 5: Visualization (dòng 164-184)
- Vẽ ROI polygon
- Vẽ làn trái (xanh lá), làn phải (xanh dương)
- Thêm chú thích

---

## 4. Code Quan Trọng Cần Đọc

### Đoạn 1: Tạo ROI mask hình thang (dòng 104-114)
```python
roi = np.array([[
    (int(w*0.1), h),           # Bottom-left
    (int(w*0.45), int(h*0.6)), # Top-left
    (int(w*0.55), int(h*0.6)), # Top-right
    (int(w*0.9), h)            # Bottom-right
]], np.int32)

mask = np.zeros_like(gray)
cv2.fillPoly(mask, roi, 255)
gray = cv2.bitwise_and(gray, mask)
```
**Giải thích:** Hình thang bắt chước phối cảnh đường. 10%-90% chiều rộng ở dưới (gần xe), thu hẹp về 45%-55% ở trên (xa xe). Chỉ xử lý vùng này để tăng tốc và giảm nhiễu.

### Đoạn 2: Sobel theo x để nhấn mạnh biên dọc (dòng 121-127)
```python
gx = cv2.Sobel(blur, cv2.CV_32F, 1, 0, ksize=3)  # dx=1, dy=0
mag = np.abs(gx)
thr = 0.3 * mag.max()
edges = (mag >= thr).astype(np.uint8) * 255
```
**Giải thích:** Làn đường là các đường **dọc** (theo chiều chuyển động). Sobel-x chỉ bắt biên dọc, bỏ qua biên ngang (vết nứt ngang đường, vạch zebra). Hiệu quả hơn Sobel magnitude.

### Đoạn 3: HoughLinesP với tham số tùy chỉnh (dòng 132-139)
```python
lines = cv2.HoughLinesP(
    edges,
    rho=1,              # Độ phân giải rho (pixels)
    theta=np.pi/180,    # Độ phân giải theta (1 độ)
    threshold=60,       # Số vote tối thiểu
    minLineLength=50,   # Độ dài đoạn thẳng tối thiểu
    maxLineGap=150      # Khoảng cách tối đa giữa 2 đoạn
)
```
**Giải thích:** `HoughLinesP` (Probabilistic) nhanh hơn `HoughLines` chuẩn. `maxLineGap=150` cho phép nối các vạch đứt quãng (làn giữa).

### Đoạn 4: Phân loại làn dựa vào slope (dòng 147-157)
```python
for x1, y1, x2, y2 in lines[:,0]:
    if x2 == x1:
        continue  # Bỏ qua đường thẳng đứng

    slope = (y2 - y1) / (x2 - x1 + 1e-6)

    if slope < -0.5:      # Làn trái
        left.append((x1, y1, x2, y2))
    elif slope > 0.5:     # Làn phải
        right.append((x1, y1, x2, y2))
```
**Giải thích:**
- **Làn trái:** Khi đi từ dưới lên (y giảm), x cũng giảm → slope âm
- **Làn phải:** Khi đi từ dưới lên, x tăng → slope dương
- Ngưỡng ±0.5 để lọc đường gần ngang

### Đoạn 5: Vẽ kết quả trên ảnh gốc (dòng 165-176)
```python
out = img.copy()
cv2.polylines(out, roi, True, (255, 0, 255), 2)  # ROI (hồng)

for x1, y1, x2, y2 in left:
    cv2.line(out, (x1, y1), (x2, y2), (0, 255, 0), 3)  # Trái (xanh lá)

for x1, y1, x2, y2 in right:
    cv2.line(out, (x1, y1), (x2, y2), (255, 0, 0), 3)  # Phải (xanh dương)
```
**Giải thích:** Overlay trên ảnh gốc để dễ đánh giá. Màu sắc phân biệt rõ ràng: trái/phải/ROI.

---

## 5. Tham Số Quan Trọng

| Tham số | Giá trị | Ý nghĩa | Điều chỉnh |
|---------|---------|---------|-----------|
| ROI top_y | `h*0.6` | Độ cao phần trên ROI | Giảm (0.5) để nhìn xa hơn, tăng (0.7) để gần hơn |
| ROI width_top | `0.45-0.55` | Độ rộng ROI ở trên | Mở rộng (0.4-0.6) nếu góc camera rộng |
| Gaussian sigma | `1.2` | Độ mạnh blur | Tăng (1.5-2.0) nếu ảnh nhiễu |
| Edge threshold | `0.3` | 30% max magnitude | Giảm (0.2) để nhạy hơn, tăng (0.4) để lọc nhiễu |
| Hough threshold | `60` | Số vote tối thiểu | Tăng nếu quá nhiều đường thẳng, giảm nếu thiếu |
| minLineLength | `50` | Độ dài tối thiểu (px) | Tăng để lọc đoạn ngắn nhiễu |
| maxLineGap | `150` | Khoảng cách nối (px) | Tăng cho làn đứt quãng dài |
| Slope threshold | `±0.5` | Ngưỡng phân loại | Điều chỉnh theo góc camera |

---

## 6. Kết Quả Mong Đợi

### Ảnh output
- Làn trái và phải được highlight rõ ràng
- Các đoạn thẳng liền mạch (hoặc gần liền mạch)
- ROI bao quanh vùng đường phía trước

### Console output
```
Tìm thấy 45 đoạn thẳng từ Hough Transform
  - Làn trái: 22 đoạn thẳng
  - Làn phải: 18 đoạn thẳng
```

### Trường hợp lý tưởng
- Mỗi làn có 15-30 đoạn thẳng
- Các đoạn gần song song với nhau
- Không có outliers (đường lạc)

---

## 7. Lỗi Thường Gặp

### Lỗi 1: Không tìm thấy đường thẳng hoặc quá ít
**Nguyên nhân:**
- ROI không chứa làn đường
- Threshold quá cao
- Làn đường mờ/không rõ

**Cách fix:**
- Điều chỉnh ROI: in ra ROI coordinates và visualize
- Giảm `threshold` từ 60 xuống 30-40
- Giảm `minLineLength` từ 50 xuống 30
- Kiểm tra ảnh edges: `cv2.imwrite('debug_edges.png', edges)`

### Lỗi 2: Phát hiện sai làn (trái/phải bị đảo)
**Nguyên nhân:**
- Slope threshold không phù hợp với góc camera
- Camera bị lệch hoặc xoay

**Cách fix:**
- In ra slope của các đường: `print(f"Slope: {slope:.2f}")`
- Điều chỉnh threshold từ ±0.5 sang ±0.3 hoặc ±0.7
- Nếu camera xoay, cần deskew ảnh trước

### Lỗi 3: Phát hiện quá nhiều đường nhiễu (biển báo, xe khác)
**Nguyên nhân:** ROI quá rộng hoặc threshold quá thấp

**Cách fix:**
- Thu hẹp ROI: chỉ lấy phần dưới (top_y = 0.65-0.7)
- Tăng threshold lên 80-100
- Thêm lọc theo độ dài: `if length < 100: continue`

---

## 8. Mở Rộng

### Cải tiến 1: Ngoại suy thành đường liền
```python
# Fit polynomial qua các điểm của làn trái/phải
def fit_lane(segments):
    points = []
    for x1, y1, x2, y2 in segments:
        points.extend([(x1, y1), (x2, y2)])

    if len(points) < 2:
        return None

    points = np.array(points)
    # Fit bậc 1 (đường thẳng) hoặc bậc 2 (đường cong)
    z = np.polyfit(points[:,1], points[:,0], deg=1)
    return z

# Vẽ đường fit
left_fit = fit_lane(left)
if left_fit is not None:
    y_vals = np.linspace(h*0.6, h, 100)
    x_vals = np.polyval(left_fit, y_vals)
    # Vẽ đường liền
```

### Cải tiến 2: Kalman filter cho video
```python
# Smooth làn đường giữa các frame
from filterpy.kalman import KalmanFilter

kf = KalmanFilter(dim_x=2, dim_z=1)
# ... cấu hình và update mỗi frame
```

### Cải tiến 3: Phát hiện đường cong
```python
# Dùng polynomial bậc 2 thay vì đường thẳng
z = np.polyfit(y_points, x_points, deg=2)
# Vẽ đường cong parabol
```

### Cải tiến 4: Xử lý thiếu làn (1 bên)
```python
if len(left) == 0 and len(right) > 0:
    # Ước lượng làn trái từ làn phải
    # Giả định làn song song, cách nhau ~3.5m
```

### Cải tiến 5: Perspective transform (bird's eye view)
```python
# Biến đổi về góc nhìn từ trên xuống
src_pts = roi.reshape(4, 2).astype(np.float32)
dst_pts = np.array([[0,h], [0,0], [w,0], [w,h]], np.float32)
M = cv2.getPerspectiveTransform(src_pts, dst_pts)
warped = cv2.warpPerspective(edges, M, (w, h))
# → Làn đường thành đường thẳng đứng, dễ xử lý hơn
```

### Cải tiến 6: Tính toán vị trí xe trong làn
```python
# Tìm x_left và x_right ở bottom của ảnh
lane_center = (x_left + x_right) / 2
car_center = w / 2
offset = car_center - lane_center  # pixels
offset_m = offset * (3.7 / lane_width_px)  # quy đổi sang mét
print(f"Xe lệch {offset_m:.2f}m về {'trái' if offset > 0 else 'phải'}")
```

---

## Tips Đọc Code Nhanh

1. **Bắt đầu từ pipeline chính** (dòng 87-231): ROI → Sobel → Hough → Classify
2. **Hiểu ROI mask** (dòng 104) là then chốt để loại nhiễu
3. **So sánh Sobel-x vs Sobel magnitude** để thấy lợi ích
4. **Phần phân tích cuối** (dòng 194-226) giải thích rõ từng bước
5. **Skip phần tạo ảnh mẫu** (dòng 42-85) nếu đã có ảnh input

---

**Tổng số dòng:** 232 dòng
**Độ khó:** Trung bình
**Thời gian đọc hiểu:** 20-25 phút
**Thời gian chạy:** ~1 giây
**Ứng dụng thực tế:** Tesla Autopilot, Lane Keep Assist, ADAS
