# REQ-1: Biểu diễn và Thu nhận Ảnh - Implementation Plan

## Context
Thực hiện tất cả bài tập từ "T1-20 Biểu diễn và thu nhận ảnh.pdf" bao gồm 10 bài tập/lab với code mẫu hoàn chỉnh.

## Objectives
1. Tạo cấu trúc thư mục phù hợp
2. Implement tất cả code từ PDF (y nguyên, không chỉnh sửa)
3. Tạo documentation đầy đủ cho từng bài
4. Tạo tài liệu lý thuyết nền tảng
5. Thiết lập môi trường chạy code dễ dàng

---

## Task Breakdown

### Phase 1: Setup Project Structure

#### Task 1.1: Create Folder Structure
```
code-implement/
└── T1-bieu-dien-va-thu-nhan-anh/
    ├── bai-tap-1-camera-storage/
    ├── bai-tap-2-quantization/
    ├── bai-tap-3-bitplane-slicing/
    ├── bai-tap-4-connectivity/
    ├── bai-tap-5-color-space/
    ├── lab-1-quantization-eval/
    ├── lab-2-zooming-shrinking/
    ├── lab-3-measure-circle/
    ├── lab-4-connected-components/
    ├── lab-5-image-quality/
    ├── input/
    │   ├── sample-images/
    │   └── test-images/
    └── output/

documents/
└── T1-bieu-dien-va-thu-nhan-anh/
    ├── theory/
    │   ├── 01-sampling-quantization.md
    │   ├── 02-bit-plane-representation.md
    │   ├── 03-pixel-connectivity.md
    │   ├── 04-color-spaces.md
    │   ├── 05-image-interpolation.md
    │   └── 06-image-quality-metrics.md
    ├── exercises/
    │   ├── bai-tap-1.md
    │   ├── bai-tap-2.md
    │   ├── bai-tap-3.md
    │   ├── bai-tap-4.md
    │   ├── bai-tap-5.md
    │   ├── lab-1.md
    │   ├── lab-2.md
    │   ├── lab-3.md
    │   ├── lab-4.md
    │   └── lab-5.md
    └── README.md
```

---

### Phase 2: Implement Code for All Exercises

#### Task 2.1: Bài tập 1 - Camera Storage Calculator
**File**: `code-implement/T1-bieu-dien-va-thu-nhan-anh/bai-tap-1-camera-storage/calculator.py`

**Description**: Tính toán dung lượng lưu trữ và băng thông cho hệ thống camera giám sát

**Requirements**:
- Không có code Python trong PDF (bài lý thuyết)
- Cần tạo calculator tool để tính toán các kịch bản

**Deliverables**:
- Script tính toán dung lượng và băng thông
- So sánh các kịch bản: 1080p/720p/4K

---

#### Task 2.2: Bài tập 2 - Quantization
**File**: `code-implement/T1-bieu-dien-va-thu-nhan-anh/bai-tap-2-quantization/quantize_scan.py`

**Description**: Mô phỏng lượng tử hóa ảnh scan từ 8-bit → 6,4,2 bit và đánh giá chất lượng

**Code từ PDF** (page 3):
```python
import cv2, numpy as np
from skimage.metrics import structural_similarity as ssim

def quantize_gray(img_gray, k):
    L = 2**k
    img = img_gray.astype(np.float32)
    q = np.round(img / 255.0 * (L-1))
    rec = (q / (L-1) * 255.0).astype(np.uint8)
    return rec

def mse(a, b):
    return np.mean((a.astype(np.float32)-b.astype(np.float32))**2)

def psnr(a, b):
    m = mse(a,b)
    return 20*np.log10(255.0) - 10*np.log10(m+1e-12)

img = cv2.imread("scan_de_thi.png", cv2.IMREAD_GRAYSCALE)
for k in [6,4,2]:
    rec = quantize_gray(img, k)
    _mse = mse(img, rec)
    _psnr = psnr(img, rec)
    _ssim = ssim(img, rec, data_range=255)
    print(f"{k} bit -> MSE={_mse:.2f}, PSNR={_psnr:.2f} dB, SSIM={_ssim:.3f}")
    cv2.imwrite(f"scan_quant_{k}bit.png", rec)
```

**Input needed**: `scan_de_thi.png` (sample scanned document)

---

#### Task 2.3: Bài tập 3 - Bit-plane Slicing
**File**: `code-implement/T1-bieu-dien-va-thu-nhan-anh/bai-tap-3-bitplane-slicing/bitplane.py`

**Description**: Tách và tái dựng ảnh từ các mặt phẳng bit

**Code từ PDF** (page 5):
```python
import cv2, numpy as np

img = cv2.imread("bill.png", cv2.IMREAD_GRAYSCALE)
planes = [(img >> b) & 1 for b in range(8)]

for b, p in enumerate(planes):
    cv2.imwrite(f"bitplane_{b}.png", p*255)

# tái dựng từ bit 4..7
rec = np.zeros_like(img, dtype=np.uint8)
for b in range(4,8):
    rec |= ((planes[b].astype(np.uint8)) << b)

cv2.imwrite("bill_recon_4to7.png", rec)

def ncc(a, b):
    a = a.astype(np.float32); b = b.astype(np.float32)
    a = (a - a.mean())/(a.std()+1e-6)
    b = (b - b.mean())/(b.std()+1e-6)
    return np.mean(a*b)

print("NCC:", ncc(img, rec))
```

**Input needed**: `bill.png` (noisy bill/receipt image)

---

#### Task 2.4: Bài tập 4 - Connectivity & Pathfinding
**File**: `code-implement/T1-bieu-dien-va-thu-nhan-anh/bai-tap-4-connectivity/robot_path.py`

**Description**: Tính đường đi ngắn nhất trên lưới với kết nối 4/8

**Code từ PDF** (page 7):
```python
from collections import deque
import numpy as np

def neighbors(p, conn='4'):
    x,y = p
    N4 = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    N8 = N4 + [(x+1,y+1),(x+1,y-1),(x-1,y+1),(x-1,y-1)]
    return N4 if conn=='4' else N8

def shortest_path(grid, s, t, conn='4'):
    H,W = grid.shape
    INF = 10**9
    dist = np.full((H,W), INF, int)
    prev = np.full((H,W,2), -1, int)
    dq = deque([s]); dist[s]=0

    while dq:
        x,y = dq.popleft()
        if (x,y)==t: break
        for nx,ny in neighbors((x,y), conn):
            if 0<=nx<H and 0<=ny<W and grid[nx,ny]==0 and dist[nx,ny]>dist[x,y]+1:
                dist[nx,ny]=dist[x,y]+1; prev[nx,ny]=[x,y]; dq.append((nx,ny))

    # truy vết
    path = []
    if dist[t]<INF:
        cur = t
        while (cur!=( -1,-1)) and (cur!=tuple(prev[cur][0:0])):
            path.append(cur)
            px,py = prev[cur]
            if px==-1: break
            cur = (px,py)
        path.reverse()
    return path, dist[t]

grid = np.zeros((10,15), int); grid[3:7,8]=1  # vật cản
s=(0,0); t=(9,14)
for conn in ['4','8']:
    path, L = shortest_path(grid, s, t, conn)
    print(conn, "steps:", L)
```

---

#### Task 2.5: Bài tập 5 - Color Space Conversion
**File**: `code-implement/T1-bieu-dien-va-thu-nhan-anh/bai-tap-5-color-space/skin_detection.py`

**Description**: Phát hiện vùng da bằng HSV và YCrCb

**Code từ PDF** (page 9):
```python
import cv2, numpy as np

img = cv2.imread("portrait.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

# HSV thresholds (scale H:0-179, S,V:0-255 trong OpenCV)
lower_hsv = (0, 30, 90); upper_hsv = (25, 180, 255)
mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

# YCrCb thresholds
lower_ycc = (0, 135, 85); upper_ycc = (255, 180, 135)
mask_ycc = cv2.inRange(ycrcb, lower_ycc, upper_ycc)

cv2.imwrite("mask_hsv.png", mask_hsv)
cv2.imwrite("mask_ycrcb.png", mask_ycc)
```

**Input needed**: `portrait.jpg` (portrait with skin)

---

#### Task 2.6: Lab 1 - Quantization Evaluation
**File**: `code-implement/T1-bieu-dien-va-thu-nhan-anh/lab-1-quantization-eval/evaluate.py`

**Description**: Đánh giá toàn diện các metrics cho lượng tử hóa

**Code từ PDF** (page 11):
```python
from skimage.metrics import structural_similarity as ssim
import numpy as np, cv2

def mae(a,b):
    return np.mean(np.abs(a.astype(np.float32)-b.astype(np.float32)))

def mse(a,b):
    return np.mean((a.astype(np.float32)-b.astype(np.float32))**2)

def psnr(a,b):
    m=mse(a,b); return 20*np.log10(255.0)-10*np.log10(m+1e-12)

def ncc(a,b):
    a=a.astype(np.float32); b=b.astype(np.float32)
    a=(a-a.mean())/(a.std()+1e-6); b=(b-b.mean())/(b.std()+1e-6)
    return np.mean(a*b)

img = cv2.imread("doc.png", cv2.IMREAD_GRAYSCALE)
for k in [7,6,5,4,3,2]:
    rec = ((np.round(img/255*(2**k-1)))/(2**k-1)*255).astype(np.uint8)
    print(k, "bit:", "MAE", mae(img,rec), "MSE", mse(img,rec),
          "PSNR", psnr(img,rec), "SSIM", ssim(img,rec,data_range=255), "NCC", ncc(img,rec))
```

**Input needed**: `doc.png` (document image)

---

#### Task 2.7: Lab 2 - Zooming & Shrinking
**File**: `code-implement/T1-bieu-dien-va-thu-nhan-anh/lab-2-zooming-shrinking/resize.py`

**Description**: So sánh các phương pháp nội suy khi phóng/thu ảnh

**Code từ PDF** (page 13):
```python
import cv2, numpy as np
from skimage.metrics import structural_similarity as ssim

img = cv2.imread("campus.jpg", cv2.IMREAD_GRAYSCALE)

# nearest & bilinear
up_near = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_NEAREST)
up_bili = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)

# pixel replication (k=4)
rep = np.repeat(np.repeat(img, 4, axis=0), 4, axis=1)

# shrink & back
small = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
back = cv2.resize(small, (img.shape[1], img.shape[0]),
                  interpolation=cv2.INTER_NEAREST)

print("PSNR back:", cv2.PSNR(img, back), "SSIM back:", ssim(img, back,
                                                            data_range=255))
```

**Input needed**: `campus.jpg` (campus scene)

---

#### Task 2.8: Lab 3 - Circle Measurement
**File**: `code-implement/T1-bieu-dien-va-thu-nhan-anh/lab-3-measure-circle/measure.py`

**Description**: Đo góc, cung tròn, diện tích từ 3 điểm

**Code từ PDF** (page 15):
```python
import numpy as np

def circle_from_3pts(p1, p2, p3):
    (x1,y1),(x2,y2),(x3,y3)=map(lambda p:(float(p[0]),float(p[1])), [p1,p2,p3])
    A = np.array([[2*(x2-x1), 2*(y2-y1)],
                  [2*(x3-x1), 2*(y3-y1)]], dtype=np.float64)
    b = np.array([x2**2+y2**2 - x1**2 - y1**2,
                  x3**2+y3**2 - x1**2 - y1**2], dtype=np.float64)
    O = np.linalg.solve(A, b)
    ox, oy = O
    r = np.hypot(ox-x1, oy-y1)
    return (ox,oy), r

# ví dụ
O, r = circle_from_3pts((100,200),(200,100),(300,200))
print("O, r:", O, r)
```

---

#### Task 2.9: Lab 4 - Connected Components
**File**: `code-implement/T1-bieu-dien-va-thu-nhan-anh/lab-4-connected-components/labeling.py`

**Description**: So sánh kết nối 4 vs 8 trong gán nhãn

**Code từ PDF** (page 17):
```python
import cv2, numpy as np

img = cv2.imread("pcb.png", cv2.IMREAD_GRAYSCALE)
_, bw = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

for conn in [4,8]:
    num, labels = cv2.connectedComponents(bw, connectivity=conn)
    print(f"Connectivity {conn}: components = {num}")

    # gán màu giả để xem
    lab_norm = (labels/(labels.max()+1e-6)*255).astype(np.uint8)
    color = cv2.applyColorMap(lab_norm, cv2.COLORMAP_JET)
    cv2.imwrite(f"labels_conn{conn}.png", color)
```

**Input needed**: `pcb.png` (PCB or circuit image)

---

#### Task 2.10: Lab 5 - Image Quality Assessment
**File**: `code-implement/T1-bieu-dien-va-thu-nhan-anh/lab-5-image-quality/assess.py`

**Description**: Đánh giá chất lượng với nhiễu và nén JPEG

**Code từ PDF** (page 19):
```python
import cv2, numpy as np
from skimage.metrics import structural_similarity as ssim

def add_gaussian_noise(img, sigma=10):
    noise = np.random.normal(0, sigma, img.shape).astype(np.float32)
    out = np.clip(img.astype(np.float32)+noise, 0, 255).astype(np.uint8)
    return out

img = cv2.imread("scene.jpg", cv2.IMREAD_GRAYSCALE)
noisy = add_gaussian_noise(img, sigma=15)

# JPEG nén
_, enc = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 40])
jpeg = cv2.imdecode(enc, cv2.IMREAD_GRAYSCALE)

def mse(a,b): return np.mean((a.astype(np.float32)-b.astype(np.float32))**2)

def psnr(a,b): return 20*np.log10(255.0)-10*np.log10(mse(a,b)+1e-12)

def ncc(a,b):
    a=a.astype(np.float32); b=b.astype(np.float32)
    a=(a-a.mean())/(a.std()+1e-6); b=(b-b.mean())/(b.std()+1e-6)
    return np.mean(a*b)

for name, im in [("noisy", noisy), ("jpeg40", jpeg)]:
    print(name, "MSE", mse(img,im), "PSNR", psnr(img,im),
          "SSIM", ssim(img,im,data_range=255), "NCC", ncc(img,im))
```

**Input needed**: `scene.jpg` (natural scene)

---

### Phase 3: Create Documentation

#### Task 3.1: Theory Documents

**File**: `documents/T1-bieu-dien-va-thu-nhan-anh/theory/01-sampling-quantization.md`
- Lý thuyết về lấy mẫu (sampling)
- Lý thuyết về lượng tử hóa (quantization)
- Công thức: L = 2^k
- Trade-off giữa spatial resolution và gray-level resolution

**File**: `documents/T1-bieu-dien-va-thu-nhan-anh/theory/02-bit-plane-representation.md`
- Biểu diễn ảnh qua các mặt phẳng bit
- Ý nghĩa các bit plane (LSB vs MSB)
- Ứng dụng trong xử lý ảnh

**File**: `documents/T1-bieu-dien-va-thu-nhan-anh/theory/03-pixel-connectivity.md`
- Kết nối 4-láng giềng
- Kết nối 8-láng giềng
- Kết nối m (m-connectivity)
- Distance metrics: Manhattan, Chessboard, Euclidean

**File**: `documents/T1-bieu-dien-va-thu-nhan-anh/theory/04-color-spaces.md`
- RGB color space
- HSV color space
- YCrCb color space
- Color space conversion
- Applications in skin detection

**File**: `documents/T1-bieu-dien-va-thu-nhan-anh/theory/05-image-interpolation.md`
- Nearest neighbor interpolation
- Bilinear interpolation
- Pixel replication
- Applications in zooming/shrinking

**File**: `documents/T1-bieu-dien-va-thu-nhan-anh/theory/06-image-quality-metrics.md`
- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- PSNR (Peak Signal-to-Noise Ratio)
- SSIM (Structural Similarity Index)
- NCC (Normalized Cross-Correlation)

---

#### Task 3.2: Exercise Documentation

For each exercise, create a document with:
1. **Giải thích đề bài**: Mô tả chi tiết yêu cầu
2. **Giải thích hướng xử lý**: Phương pháp và thuật toán
3. **Giải thích code**: Comment từng phần code
4. **Kết quả mong đợi**: Output và cách đánh giá

**Files to create**:
- `documents/T1-bieu-dien-va-thu-nhan-anh/exercises/bai-tap-1.md`
- `documents/T1-bieu-dien-va-thu-nhan-anh/exercises/bai-tap-2.md`
- `documents/T1-bieu-dien-va-thu-nhan-anh/exercises/bai-tap-3.md`
- `documents/T1-bieu-dien-va-thu-nhan-anh/exercises/bai-tap-4.md`
- `documents/T1-bieu-dien-va-thu-nhan-anh/exercises/bai-tap-5.md`
- `documents/T1-bieu-dien-va-thu-nhan-anh/exercises/lab-1.md`
- `documents/T1-bieu-dien-va-thu-nhan-anh/exercises/lab-2.md`
- `documents/T1-bieu-dien-va-thu-nhan-anh/exercises/lab-3.md`
- `documents/T1-bieu-dien-va-thu-nhan-anh/exercises/lab-4.md`
- `documents/T1-bieu-dien-va-thu-nhan-anh/exercises/lab-5.md`

---

### Phase 4: Setup Environment

#### Task 4.1: Create requirements.txt
**File**: `code-implement/T1-bieu-dien-va-thu-nhan-anh/requirements.txt`

```
opencv-python>=4.8.0
numpy>=1.24.0
scikit-image>=0.21.0
matplotlib>=3.7.0
```

#### Task 4.2: Create Run Scripts

**File**: `code-implement/T1-bieu-dien-va-thu-nhan-anh/run_all.sh`
```bash
#!/bin/bash
# Run all exercises sequentially

echo "Running Bai tap 2..."
cd bai-tap-2-quantization && python quantize_scan.py && cd ..

echo "Running Bai tap 3..."
cd bai-tap-3-bitplane-slicing && python bitplane.py && cd ..

echo "Running Bai tap 4..."
cd bai-tap-4-connectivity && python robot_path.py && cd ..

echo "Running Bai tap 5..."
cd bai-tap-5-color-space && python skin_detection.py && cd ..

echo "Running Lab 1..."
cd lab-1-quantization-eval && python evaluate.py && cd ..

echo "Running Lab 2..."
cd lab-2-zooming-shrinking && python resize.py && cd ..

echo "Running Lab 3..."
cd lab-3-measure-circle && python measure.py && cd ..

echo "Running Lab 4..."
cd lab-4-connected-components && python labeling.py && cd ..

echo "Running Lab 5..."
cd lab-5-image-quality && python assess.py && cd ..

echo "All exercises completed!"
```

**File**: `code-implement/T1-bieu-dien-va-thu-nhan-anh/README.md`
- Hướng dẫn cài đặt môi trường
- Hướng dẫn chạy từng bài
- Hướng dẫn chuẩn bị input images
- Giải thích cấu trúc thư mục

---

### Phase 5: Prepare Input Data

#### Task 5.1: Create Sample Images Guide
**File**: `code-implement/T1-bieu-dien-va-thu-nhan-anh/input/README.md`

List of required input images:
1. `scan_de_thi.png` - Scanned document/exam paper
2. `bill.png` - Noisy bill/receipt with salt-pepper noise
3. `portrait.jpg` - Portrait photo with visible skin
4. `doc.png` - Document image for quantization testing
5. `campus.jpg` - Campus scene for resizing
6. `pcb.png` - PCB or circuit board image
7. `scene.jpg` - Natural scene for quality assessment

**Provide instructions**:
- How to prepare/download sample images
- Image format requirements
- Alternative datasets if needed

#### Task 5.2: Create Sample Data Generator
**File**: `code-implement/T1-bieu-dien-va-thu-nhan-anh/input/generate_samples.py`

Script to:
- Download sample images from open datasets
- Create synthetic test images
- Generate grid obstacles for pathfinding

---

### Phase 6: Main README

#### Task 6.1: Create Main Documentation
**File**: `documents/T1-bieu-dien-va-thu-nhan-anh/README.md`

Content:
- Tổng quan về chủ đề "Biểu diễn và Thu nhận Ảnh"
- Danh sách tất cả bài tập/lab
- Link đến theory documents
- Link đến exercise explanations
- Quick start guide
- References và tài liệu tham khảo

---

## Summary Checklist

### Code Implementation
- [ ] Bài tập 1: Camera storage calculator
- [ ] Bài tập 2: Quantization with metrics
- [ ] Bài tập 3: Bit-plane slicing
- [ ] Bài tập 4: Connectivity & pathfinding
- [ ] Bài tập 5: Color space & skin detection
- [ ] Lab 1: Quantization evaluation
- [ ] Lab 2: Zooming & shrinking
- [ ] Lab 3: Circle measurement
- [ ] Lab 4: Connected components
- [ ] Lab 5: Image quality assessment

### Documentation
- [ ] 6 theory documents
- [ ] 10 exercise explanation documents
- [ ] Main README
- [ ] Code README with usage guide
- [ ] Input data guide

### Environment Setup
- [ ] requirements.txt
- [ ] run_all.sh script
- [ ] Sample data generator
- [ ] Folder structure created

---

## Notes
- Tất cả code phải giữ nguyên như trong PDF
- Chỉ thêm comments và documentation
- Chuẩn bị sample images hoặc hướng dẫn tải
- Test tất cả code trước khi hoàn thành
- Documentation phải bằng tiếng Việt, có thể thêm thuật ngữ tiếng Anh
