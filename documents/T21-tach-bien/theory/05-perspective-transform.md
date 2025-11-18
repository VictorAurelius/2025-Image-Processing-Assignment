# Lý Thuyết 5: Perspective Transform và Geometric Correction

## 📋 Tổng Quan

**Perspective Transform** (phép biến đổi phối cảnh) cho phép "sửa" góc nhìn của ảnh - từ góc xiên sang góc vuông. Đây là kỹ thuật quan trọng trong:
- Document scanning
- Image rectification
- Augmented Reality
- Camera calibration

## 🎯 Ứng Dụng

- **Bài 2**: Document scanning (4 điểm góc → A4 thẳng)
- **Bài 10**: Document deskew (xoay về 0°)

## 📐 Toán Học Perspective Transform

### Homography Matrix

Perspective transform được biểu diễn bằng ma trận 3×3 (homography):

```
[x']   [h11 h12 h13]   [x]
[y'] = [h21 h22 h23] × [y]
[w']   [h31 h32 h33]   [1]
```

Sau đó normalize:
```
x_output = x' / w'
y_output = y' / w'
```

### Tìm Ma Trận Homography

Cần **4 cặp điểm tương ứng**:
- `src_pts`: 4 điểm trên ảnh gốc
- `dst_pts`: 4 điểm tương ứng trên ảnh đích

```python
M = cv2.getPerspectiveTransform(src_pts, dst_pts)
```

## 🔧 Sử Dụng Trong OpenCV

### Bước 1: Tìm 4 Điểm Góc

#### Phương Pháp 1: Tự Động (Contours)

```python
# 1. Edges
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 1.0)
edges = cv2.Canny(blur, 50, 150)

# 2. Dilate để nối biên
kernel = np.ones((5,5), np.uint8)
dilated = cv2.dilate(edges, kernel, iterations=1)

# 3. Tìm contours
cnts, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 4. Chọn contour lớn nhất (giấy)
cnt = max(cnts, key=cv2.contourArea)

# 5. Xấp xỉ thành 4 điểm (hình chữ nhật)
epsilon = 0.02 * cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, epsilon, True)

if len(approx) == 4:
    pts = approx.reshape(4, 2)
else:
    print("Không tìm thấy 4 góc!")
```

#### Phương Pháp 2: Thủ Công (Mouse Click)

```python
pts = []

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        pts.append([x, y])
        cv2.circle(img, (x, y), 5, (0,0,255), -1)
        cv2.imshow('Image', img)
        if len(pts) == 4:
            cv2.destroyAllWindows()

cv2.imshow('Image', img)
cv2.setMouseCallback('Image', click_event)
cv2.waitKey(0)

pts = np.array(pts, dtype=np.float32)
```

### Bước 2: Sắp Xếp 4 Điểm

**Thứ tự chuẩn**: Top-Left, Top-Right, Bottom-Right, Bottom-Left

```python
def order_points(pts):
    """
    Sắp xếp 4 điểm theo thứ tự: TL, TR, BR, BL
    """
    rect = np.zeros((4, 2), dtype=np.float32)

    # Tổng: TL có tổng nhỏ nhất, BR có tổng lớn nhất
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # Top-Left
    rect[2] = pts[np.argmax(s)]  # Bottom-Right

    # Hiệu: TR có hiệu nhỏ nhất, BL có hiệu lớn nhất
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # Top-Right
    rect[3] = pts[np.argmax(diff)]  # Bottom-Left

    return rect
```

### Bước 3: Tính Kích Thước Output

```python
def compute_output_size(pts):
    """
    Tính width và height của ảnh output
    """
    (tl, tr, br, bl) = pts

    # Width: Max của cạnh trên và cạnh dưới
    width_top = np.linalg.norm(tr - tl)
    width_bottom = np.linalg.norm(br - bl)
    max_width = int(max(width_top, width_bottom))

    # Height: Max của cạnh trái và cạnh phải
    height_left = np.linalg.norm(bl - tl)
    height_right = np.linalg.norm(br - tr)
    max_height = int(max(height_left, height_right))

    return max_width, max_height
```

**Hoặc cố định kích thước** (ví dụ A4):
```python
# A4 ratio: 210mm × 297mm ≈ 1:1.414
width = 600
height = int(width * 1.414)  # 848
```

### Bước 4: Tạo Destination Points

```python
dst_pts = np.array([
    [0, 0],                    # Top-Left
    [width - 1, 0],            # Top-Right
    [width - 1, height - 1],   # Bottom-Right
    [0, height - 1]            # Bottom-Left
], dtype=np.float32)
```

### Bước 5: Perspective Transform

```python
# Tính ma trận homography
M = cv2.getPerspectiveTransform(src_pts, dst_pts)

# Áp dụng transform
warped = cv2.warpPerspective(img, M, (width, height))
```

## 🧪 Ví Dụ Hoàn Chỉnh: Document Scanning

```python
import cv2
import numpy as np

def order_points(pts):
    rect = np.zeros((4, 2), dtype=np.float32)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(img, pts):
    # Sắp xếp điểm
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # Tính kích thước output
    width_top = np.linalg.norm(tr - tl)
    width_bottom = np.linalg.norm(br - bl)
    max_width = int(max(width_top, width_bottom))

    height_left = np.linalg.norm(bl - tl)
    height_right = np.linalg.norm(br - tr)
    max_height = int(max(height_left, height_right))

    # Destination points
    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype=np.float32)

    # Perspective transform
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(img, M, (max_width, max_height))

    return warped

# Sử dụng
img = cv2.imread('document.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 1.0)
edges = cv2.Canny(blur, 50, 150)

# Morphology
kernel = np.ones((5,5), np.uint8)
dilated = cv2.dilate(edges, kernel)

# Contours
cnts, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnt = max(cnts, key=cv2.contourArea)

# Approximation
epsilon = 0.02 * cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, epsilon, True)

if len(approx) == 4:
    pts = approx.reshape(4, 2).astype(np.float32)
    warped = four_point_transform(img, pts)
    cv2.imwrite('scanned.jpg', warped)
```

## 🔄 Rotation Correction (Deskew)

### Phát Hiện Góc Nghiêng

#### Phương Pháp 1: Hough Lines

```python
# Tìm các đường thẳng
edges = cv2.Canny(gray, 50, 150)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

# Tính góc trung bình
angles = []
for x1, y1, x2, y2 in lines[:,0]:
    angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
    angles.append(angle)

median_angle = np.median(angles)
```

#### Phương Pháp 2: MinAreaRect

```python
# Tìm contour của văn bản
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cnts, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnt = max(cnts, key=cv2.contourArea)

# Rotated bounding box
rect = cv2.minAreaRect(cnt)
angle = rect[2]

# Chuẩn hoá góc về [-45, 45]
if angle < -45:
    angle = 90 + angle
```

### Xoay Ảnh

```python
def rotate_image(img, angle):
    h, w = img.shape[:2]
    center = (w // 2, h // 2)

    # Ma trận xoay
    M = cv2.getRotationMatrix2D(center, angle, scale=1.0)

    # Tính kích thước mới để không crop
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    new_w = int(h * sin + w * cos)
    new_h = int(h * cos + w * sin)

    # Điều chỉnh translation
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]

    # Xoay
    rotated = cv2.warpAffine(img, M, (new_w, new_h), flags=cv2.INTER_CUBIC,
                             borderMode=cv2.BORDER_REPLICATE)
    return rotated

# Sử dụng
rotated = rotate_image(img, -median_angle)
```

## 📊 So Sánh Các Loại Transform

| Transform | Ma Trận | Tham Số | Bảo Toàn | Ứng Dụng |
|-----------|---------|---------|----------|----------|
| **Translation** | 2×3 | (tx, ty) | Góc, khoảng cách | Di chuyển |
| **Rotation** | 2×3 | θ | Góc, khoảng cách | Xoay |
| **Affine** | 2×3 | 3 điểm | Đường thẳng song song | Shear, scale |
| **Perspective** | 3×3 | 4 điểm | Đường thẳng | Document scan ⭐ |

## 🔬 Ưu Nhược Điểm

### Perspective Transform - Ưu Điểm
- ✅ Sửa méo phối cảnh hoàn hảo
- ✅ Cho kết quả "vuông góc"
- ✅ Chuẩn công nghiệp cho document scan
- ✅ Linh hoạt với mọi góc chụp

### Perspective Transform - Nhược Điểm
- ❌ Cần 4 điểm chính xác
- ❌ Sai số điểm → méo ảnh
- ❌ Không tự động 100% (cần detect góc)
- ❌ Có thể mất phần ảnh ngoài 4 điểm

## 🚀 Kỹ Thuật Nâng Cao

### 1. Interactive Point Selection

```python
import matplotlib.pyplot as plt

def select_points(img):
    fig, ax = plt.subplots()
    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    pts = plt.ginput(4, timeout=0)  # Click 4 điểm
    plt.close()
    return np.array(pts, dtype=np.float32)

pts = select_points(img)
```

### 2. Auto-Detect với Canny + Dilation

```python
# Tìm cạnh ngoài cùng
edges = cv2.Canny(gray, 50, 150)
dilated = cv2.dilate(edges, np.ones((5,5), np.uint8), iterations=2)

# Tìm contour lớn nhất
cnts, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnt = max(cnts, key=cv2.contourArea)

# Xấp xỉ thành hình chữ nhật
peri = cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

# Tăng epsilon nếu không có 4 điểm
epsilon = 0.02
while len(approx) != 4 and epsilon < 0.1:
    epsilon += 0.01
    approx = cv2.approxPolyDP(cnt, epsilon * peri, True)
```

### 3. Border Removal

Sau transform, cắt bỏ viền trắng:

```python
gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# Tìm vùng không trắng
coords = cv2.findNonZero(thresh)
x, y, w, h = cv2.boundingRect(coords)

# Crop
cropped = warped[y:y+h, x:x+w]
```

## 🧪 Debugging Tips

### 4 Điểm Không Đúng

```python
# Visualize các điểm
for i, pt in enumerate(pts):
    cv2.circle(img, tuple(pt.astype(int)), 10, (0,255,0), -1)
    cv2.putText(img, str(i), tuple(pt.astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
cv2.imshow('Points', img)
cv2.waitKey(0)
```

### Ảnh Output Bị Méo

```python
# Kiểm tra thứ tự điểm
rect = order_points(pts)
print("TL:", rect[0])
print("TR:", rect[1])
print("BR:", rect[2])
print("BL:", rect[3])

# Vẽ dest points để xác nhận
for i, pt in enumerate(dst_pts):
    cv2.circle(warped, tuple(pt.astype(int)), 5, (0,0,255), -1)
```

## 📚 Tài Liệu Tham Khảo

- OpenCV Documentation: Geometric Transformations
- Hartley & Zisserman: Multiple View Geometry
- PyImageSearch: Document Scanner

## 🔗 Liên Kết

**Bài thực hành**:
- **Bài 2**: Document scanning (4-point transform)
- **Bài 10**: Document deskew (rotation correction)

**Lý thuyết liên quan**:
- **02-canny-edge-detection.md**: Tìm biên cho detect góc
- **04-contour-detection.md**: Tìm contour giấy

---

**Tác giả**: Dựa trên PDF T21-40 Tách Biên
**Cập nhật**: 2025
