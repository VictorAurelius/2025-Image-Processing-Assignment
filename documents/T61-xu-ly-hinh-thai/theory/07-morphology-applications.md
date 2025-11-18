# 07 - Morphology Applications (Ứng Dụng Thực Tế)

## Tổng Quan

Xử lý hình thái được ứng dụng rộng rãi trong nhiều lĩnh vực: OCR (nhận dạng ký tự), kiểm tra chất lượng công nghiệp, phân tích ảnh y tế, robot vision, và document processing. Tài liệu này tổng hợp các ứng dụng thực tế từ 9 bài tập trong chương trình T61.

## Ứng Dụng Theo Lĩnh Vực

### 1. Document Processing & OCR

**Bài 1: Làm Sạch Văn Bản Quét**
- Vấn đề: Tài liệu quét bị nhiễu muối tiêu
- Giải pháp: Opening để khử nhiễu
- Kết quả: Văn bản sạch, dễ OCR

**Bài 5: Phân Đoạn Ký Tự**
- Vấn đề: Tách ký tự từ biển số xe, tem phiếu
- Giải pháp: Opening (khử nhiễu) + Closing (nối nét) + Connected Components
- Kết quả: Từng ký tự riêng biệt

**Bài 9: Khử Nền Không Đồng Đều**
- Vấn đề: Tài liệu có chiếu sáng không đều
- Giải pháp: Top-hat (vật thể sáng) + Black-hat (vật thể tối)
- Kết quả: Nền đồng đều, văn bản rõ ràng

### 2. Industrial Inspection

**Bài 2: Phục Hồi Linh Kiện**
- Vấn đề: Linh kiện có lỗ nhỏ, khe hở
- Giải pháp: Closing để lấp lỗ và nối nét
- Kết quả: Vật thể hoàn chỉnh

**Bài 3: Trích Biên Chi Tiết**
- Vấn đề: Phát hiện biên chi tiết công nghiệp
- Giải pháp: Morphological Gradient (Dilation - Erosion)
- Kết quả: Biên liên tục, ít nhiễu

**Bài 6: Đo Đạc Hạt/Lỗ**
- Vấn đề: Phân loại hạt theo kích thước
- Giải pháp: Closing + findContours + diện tích
- Kết quả: Phân loại nhỏ/vừa/lớn

**Bài 8: Tách Foreground**
- Vấn đề: Phân tích vật thể trên băng chuyền
- Giải pháp: Erosion tạo core, subtract tạo rim
- Kết quả: Tách core và biên

### 3. Counting & Segmentation

**Bài 4: Đếm Đối Tượng Dính Nhau**
- Vấn đề: Đồng xu/viên nén chạm nhau
- Giải pháp: Opening + Distance Transform + Watershed
- Kết quả: Tách và đếm chính xác

### 4. Pattern Recognition

**Bài 7: Pruning (Làm Gọn Biên)**
- Vấn đề: Skeleton có gai (spurs)
- Giải pháp: Hit-or-Miss với 8 SE xoay
- Kết quả: Biên gọn gàng

## Code Examples (Tổng Hợp Từ 9 Bài)

### Example 1: Document OCR Pipeline

```python
import cv2
import numpy as np

def preprocess_for_ocr(img_path):
    # Đọc ảnh
    img = cv2.imread(img_path, 0)

    # 1. Nhị phân hóa Otsu
    _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 2. Khử nhiễu (Bài 1)
    kernel_noise = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    denoised = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_noise)

    # 3. Nối nét (Bài 2)
    kernel_connect = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    connected = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel_connect)

    # 4. Khử nền (Bài 9)
    if img.mean() < 200:  # Nền tối
        kernel_bg = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
        tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel_bg)
        enhanced = cv2.add(img, tophat)
    else:
        enhanced = img

    return enhanced, connected

# Sử dụng
cleaned, binary = preprocess_for_ocr('document.jpg')
cv2.imwrite('ocr_ready.png', cleaned)
```

### Example 2: Industrial Inspection Pipeline

```python
import cv2
import numpy as np

def inspect_parts(img_path):
    img = cv2.imread(img_path, 0)
    _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 1. Phục hồi vật thể (Bài 2)
    kernel_repair = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    repaired = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_repair)

    # 2. Trích biên (Bài 3)
    kernel_edge = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    edges = cv2.morphologyEx(repaired, cv2.MORPH_GRADIENT, kernel_edge)

    # 3. Tìm và đo đạc (Bài 6)
    contours, _ = cv2.findContours(repaired, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    defects = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 100:  # Quá nhỏ = khuyết tật
            defects.append(cnt)

    return repaired, edges, defects

# Sử dụng
repaired, edges, defects = inspect_parts('parts.jpg')
print(f"Phát hiện {len(defects)} khuyết tật")
```

### Example 3: Counting Pipeline

```python
import cv2
import numpy as np

def count_objects(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Opening (khử nhiễu)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=2)

    # Sure background
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # Distance Transform
    dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)

    # Sure foreground
    _, sure_fg = cv2.threshold(dist, 0.5 * dist.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)

    # Unknown
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Markers
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    # Watershed
    markers = cv2.watershed(img, markers)

    # Đếm
    count = len(np.unique(markers)) - 2  # Trừ nền và biên
    return count, markers

# Sử dụng
count, markers = count_objects('coins.jpg')
print(f"Số đối tượng: {count}")
```

### Example 4: Character Segmentation Pipeline

```python
import cv2
import numpy as np

def segment_characters(img_path, output_dir='characters'):
    import os
    os.makedirs(output_dir, exist_ok=True)

    img = cv2.imread(img_path, 0)

    # Nhị phân hóa
    _, bw = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Opening (khử nhiễu)
    kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel_open)

    # Closing (nối nét)
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel_close)

    # Connected Components
    n, labels, stats, centroids = cv2.connectedComponentsWithStats(bw)

    # Lọc và lưu
    chars = []
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        if 100 < area < 5000 and 0.2 < w/h < 1.5:
            char_img = img[y:y+h, x:x+w]
            char_path = f"{output_dir}/char_{i:02d}.png"
            cv2.imwrite(char_path, char_img)
            chars.append((i, x, y, w, h))

    return chars

# Sử dụng
chars = segment_characters('license_plate.jpg')
print(f"Phân đoạn {len(chars)} ký tự")
```

### Example 5: Complete Morphology Toolbox

```python
import cv2
import numpy as np

class MorphologyToolbox:
    """Tổng hợp các phép toán morphology thường dùng"""

    @staticmethod
    def denoise(image, kernel_size=3):
        """Bài 1: Khử nhiễu bằng Opening"""
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    @staticmethod
    def fill_holes(image, kernel_size=7):
        """Bài 2: Lấp lỗ bằng Closing"""
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

    @staticmethod
    def extract_edges(image, kernel_size=3):
        """Bài 3: Trích biên bằng Gradient"""
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        return cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)

    @staticmethod
    def count_objects_watershed(image):
        """Bài 4: Đếm đối tượng bằng Watershed"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=2)

        dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist, 0.5 * dist.max(), 255, 0)

        _, markers = cv2.connectedComponents(sure_fg.astype(np.uint8))
        return len(np.unique(markers)) - 1

    @staticmethod
    def segment_characters(image):
        """Bài 5: Phân đoạn ký tự"""
        _, bw = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel_open)

        kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel_close)

        n, labels = cv2.connectedComponents(bw)
        return n - 1, labels

    @staticmethod
    def classify_particles(image):
        """Bài 6: Phân loại hạt theo kích thước"""
        _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        areas = [cv2.contourArea(c) for c in contours]

        if not areas:
            return {'small': 0, 'medium': 0, 'large': 0}

        t1, t2 = np.percentile(areas, [33, 66])

        return {
            'small': sum(a <= t1 for a in areas),
            'medium': sum((a > t1) & (a <= t2) for a in areas),
            'large': sum(a > t2 for a in areas)
        }

    @staticmethod
    def remove_background(image, kernel_size=15):
        """Bài 9: Khử nền bằng Top-hat"""
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        tophat = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)
        blackhat = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)
        return cv2.normalize(image.astype(np.float32) + tophat - blackhat,
                            None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# Sử dụng
toolbox = MorphologyToolbox()

img = cv2.imread('input.jpg', 0)
denoised = toolbox.denoise(img)
filled = toolbox.fill_holes(img)
edges = toolbox.extract_edges(img)

print("Morphology Toolbox ready!")
```

## So Sánh Ứng Dụng

| Lĩnh Vực | Bài Tập | Phép Toán Chính | Độ Khó | Tính Thực Tế |
|----------|---------|-----------------|--------|--------------|
| **Document OCR** | Bài 1, 5, 9 | Opening, Closing, Top-hat | Trung bình | Rất cao |
| **Industrial Inspection** | Bài 2, 3, 6, 8 | Closing, Gradient, Erosion | Trung bình | Cao |
| **Counting** | Bài 4 | Watershed | Khó | Cao |
| **Pattern Recognition** | Bài 7 | Hit-or-Miss | Khó | Trung bình |

## Best Practices

### 1. Chọn Kernel Size

```python
# Quy tắc ngón tay:
# - Nhiễu nhỏ: kernel 3x3
# - Khe hở vừa: kernel 5x5, 7x7
# - Nền không đều: kernel 15x15, 21x21

# Adaptive kernel
def choose_kernel_size(image_size, feature_size):
    # Kernel ~ 1/3 đến 1/2 kích thước feature
    return max(3, min(31, int(feature_size * 0.4)))
```

### 2. Thứ Tự Operations

```python
# Pipeline chuẩn cho văn bản:
# 1. Threshold (Otsu)
# 2. Opening (khử nhiễu)
# 3. Closing (nối nét)
# 4. Connected Components (phân đoạn)

# Pipeline cho counting:
# 1. Threshold
# 2. Opening (khử nhiễu)
# 3. Distance Transform
# 4. Watershed (tách)
```

### 3. Parameter Tuning

```python
# Sử dụng trackbar để điều chỉnh real-time
def create_morphology_demo(img_path):
    img = cv2.imread(img_path, 0)

    def update(val):
        kernel_size = cv2.getTrackbarPos('Kernel', 'Morphology') * 2 + 1
        iterations = cv2.getTrackbarPos('Iterations', 'Morphology')
        op_type = cv2.getTrackbarPos('Operation', 'Morphology')

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))

        if op_type == 0:
            result = cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel, iterations=iterations)
        elif op_type == 1:
            result = cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel, iterations=iterations)
        elif op_type == 2:
            result = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=iterations)
        else:
            result = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=iterations)

        cv2.imshow('Morphology', result)

    cv2.namedWindow('Morphology')
    cv2.createTrackbar('Kernel', 'Morphology', 1, 10, update)
    cv2.createTrackbar('Iterations', 'Morphology', 1, 5, update)
    cv2.createTrackbar('Operation', 'Morphology', 0, 3, update)

    update(0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Sử dụng
create_morphology_demo('test.jpg')
```

## Tổng Kết

Morphology là công cụ mạnh mẽ cho xử lý ảnh, đặc biệt:

**Khi Nào Dùng Morphology:**
- Ảnh nhị phân hoặc có cấu trúc rõ ràng
- Cần bảo toàn hình dạng
- Preprocessing cho OCR, counting
- Phân tích hình dạng

**Khi Nào KHÔNG Dùng:**
- Ảnh tự nhiên phức tạp
- Cần edge mỏng chính xác (dùng Canny)
- Segmentation phức tạp (dùng Deep Learning)

## Tài Liệu Tham Khảo

- **9 Bài Tập**: Code tại `/code-implement/T61-xu-ly-hinh-thai/`
- **OpenCV Docs**: https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html

## Liên Kết

- [Bài 1-9 Code Reading Guides](../code-reading-guide/)
- [Theory 01-06](./01-morphology-fundamentals.md)

---

**Nguồn**: T61-78 - Ph.D Phan Thanh Toàn
