# Bài 7: Phát Hiện Vết Nứt Bê Tông - Code Reading Guide

## 1. Tổng Quan

Phát hiện vết nứt trên bê tông/asphalt bằng Laplacian of Gaussian (LoG) đa tỉ lệ, adaptive thresholding, và skeletonization. Ứng dụng cho kiểm tra kết cấu công trình, đường bộ.

**File code:** `/code-implement/T21-tach-bien/bai-7-crack-detection/detect.py`

---

## 2. Input/Output

### Input
- **File:** `../input/sample-images/surface_crack.jpg`
- **Mô tả:** Ảnh bề mặt bê tông/asphalt có vết nứt mảnh
- **Format:** Grayscale

### Output
- **crack_mask.png:** Mask nhị phân vết nứt
- **crack_skeleton.png:** Skeleton 1-pixel (mạng nứt)
- **crack_overlay.png:** Overlay mask (đỏ) + skeleton (xanh lá) lên ảnh gốc
- **crack_response.png:** LoG response tổng hợp (debug)

---

## 3. Thuật Toán Chính

### Bước 1: LoG đa tỉ lệ với hàm `LoG()` (dòng 32-52, 124-136)
- Áp dụng LoG với 4 giá trị sigma: [0.8, 1.2, 1.8, 2.4]
- Mỗi sigma bắt vết nứt ở 1 bề rộng khác nhau
- Tổng hợp response từ tất cả scales

### Bước 2: Adaptive threshold (dòng 144-152)
- Dùng `ADAPTIVE_THRESH_MEAN_C` với blockSize=35
- Tự động thích nghi với độ sáng cục bộ

### Bước 3: Morphology Open (dòng 154-156)
- Loại bỏ nhiễu hạt nhỏ

### Bước 4: Skeletonization (dòng 159-160)
- Làm mảnh vết nứt về 1 pixel
- Dùng `skimage.morphology.skeletonize`

### Bước 5: Phân tích (dòng 162-173)
- Đếm pixels, tính tỷ lệ %
- Phân loại mức độ (nhẹ/trung bình/nghiêm trọng)

---

## 4. Code Quan Trọng Cần Đọc

### Đoạn 1: Hàm LoG với scale (dòng 32-52)
```python
def LoG(f, sigma):
    k = int(6 * sigma + 1) | 1  # Kernel size lẻ
    g = cv2.GaussianBlur(f, (k, k), sigma)
    lap = cv2.Laplacian(g, cv2.CV_32F, ksize=3)
    return np.abs(lap)
```
**Giải thích:**
- **LoG = Laplacian(Gaussian(f)):** Làm trơn rồi mới tính đạo hàm bậc 2
- Kernel size = 6σ+1 (rule of thumb) và làm lẻ bằng `| 1`
- Trả về trị tuyệt đối vì chỉ quan tâm cường độ, không quan tâm dấu

### Đoạn 2: Multi-scale LoG (dòng 124-136)
```python
sigmas = [0.8, 1.2, 1.8, 2.4]
responses = []
for s in sigmas:
    r = LoG(imgf, s)
    responses.append(r)

resp = sum(responses)  # Tổng hợp
```
**Giải thích:**
- Sigma nhỏ (0.8) → bắt nứt mảnh
- Sigma lớn (2.4) → bắt nứt rộng
- Tổng hợp bằng `sum()` để có response tổng quát

### Đoạn 3: Adaptive threshold (dòng 144-152)
```python
thr = cv2.adaptiveThreshold(
    resp,
    255,
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY,
    35,    # Block size (phải lẻ)
    -5     # C constant (trừ đi từ mean)
)
```
**Giải thích:**
- **Adaptive:** Ngưỡng khác nhau cho từng vùng cục bộ
- **Mean C:** Ngưỡng = mean của block 35×35 trừ C
- C=-5: Bias để nhạy hơn (ngưỡng thấp hơn)

### Đoạn 4: Skeletonization (dòng 159-160)
```python
from skimage.morphology import skeletonize
skel = skeletonize((thr > 0).astype(np.uint8)).astype(np.uint8) * 255
```
**Giải thích:**
- Làm mảnh vết nứt về **1 pixel** giữa
- Giữ nguyên topology (connectivity)
- Hữu ích cho đo độ dài nứt

### Đoạn 5: Phân loại mức độ (dòng 209-217)
```python
if crack_ratio < 0.5:
    severity = "NHẸ"
elif crack_ratio < 2.0:
    severity = "TRUNG BÌNH"
else:
    severity = "NGHIÊM TRỌNG"
```
**Giải thích:** Dựa vào % diện tích nứt để phân loại. Có thể điều chỉnh ngưỡng theo tiêu chuẩn kỹ thuật.

---

## 5. Tham Số Quan Trọng

| Tham Số | Giá trị | Ý nghĩa | Điều chỉnh |
|---------|---------|---------|-----------|
| sigmas | `[0.8, 1.2, 1.8, 2.4]` | Các scale cho LoG | Thêm/bớt scale, điều chỉnh range |
| Laplacian ksize | `3` | Kích thước kernel | Có thể thử 5 |
| Adaptive blockSize | `35` | Kích thước block (phải lẻ) | Tăng (51) nếu ảnh lớn |
| Adaptive C | `-5` | Constant trừ đi | Giảm (-10) để nhạy hơn, tăng (0) để lọc nhiễu |
| OPEN kernel | `(3,3)` | Kernel loại nhiễu | Tăng nếu nhiễu mạnh |
| min_area (nếu dùng) | N/A | Không có trong code | Có thể thêm để lọc vùng nhỏ |

---

## 6. Kết Quả Mong Đợi

### Ảnh output
- **crack_mask.png:** Trắng = nứt, đen = nền
- **crack_skeleton.png:** Đường 1-pixel màu trắng
- **crack_overlay.png:** Mask màu đỏ semi-transparent, skeleton xanh lá

### Console output
```
Áp dụng Laplacian of Gaussian với nhiều scales:
  - σ=0.8: max response = 0.1234
  - σ=1.2: max response = 0.0987
  - σ=1.8: max response = 0.0756
  - σ=2.4: max response = 0.0543

Thống kê:
  - Pixels vết nứt (mask): 2450 (0.510%)
  - Pixels skeleton: 1230 (0.256%)

⚠ CẢNH BÁO: Phát hiện vết nứt trên bề mặt bê tông
  - Tỷ lệ nứt: 0.510% diện tích
  - Độ dài ước tính: ~1230 pixels
  - Mức độ: NHẸ
  - Số vết nứt riêng biệt: 3
```

---

## 7. Lỗi Thường Gặp

### Lỗi 1: Phát hiện quá nhiều nhiễu texture
**Nguyên nhân:** Adaptive threshold quá nhạy

**Cách fix:**
- Tăng C từ -5 lên -2 hoặc 0
- Tăng blockSize lên 51
- Tăng kernel OPEN lên (5,5) với iterations=2

### Lỗi 2: Bỏ sót vết nứt mảnh
**Nguyên nhân:** Sigma range không bao phủ

**Cách fix:**
- Thêm sigma nhỏ hơn: `[0.5, 0.8, 1.2, 1.8, 2.4]`
- Giảm C xuống -8 hoặc -10

### Lỗi 3: ImportError: No module named 'skimage'
**Nguyên nhân:** Chưa cài scikit-image

**Cách fix:**
```bash
pip install scikit-image
```

---

## 8. Mở Rộng

### Cải tiến 1: Phân tích hướng nứt
```python
# Tính gradient direction của vết nứt
gx = cv2.Sobel(skel.astype(np.float32), cv2.CV_32F, 1, 0)
gy = cv2.Sobel(skel.astype(np.float32), cv2.CV_32F, 0, 1)
angle = np.arctan2(gy, gx) * 180 / np.pi

# Phân loại
horizontal = np.sum((abs(angle) < 30) | (abs(angle) > 150))
vertical = np.sum((60 < abs(angle) < 120))
print(f"Nứt ngang: {horizontal}, Nứt dọc: {vertical}")
```

### Cải tiến 2: Đo độ rộng trung bình
```python
# Dùng distance transform
dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
avg_width = 2 * dist[skel > 0].mean()  # pixels
print(f"Độ rộng trung bình: {avg_width:.2f} px")
```

### Cải tiến 3: Tracking vết nứt theo thời gian
```python
# So sánh với ảnh trước đó để phát hiện nứt mới
prev_skel = cv2.imread('prev_skeleton.png', 0)
new_cracks = cv2.absdiff(skel, prev_skel)
print(f"Vết nứt mới: {np.sum(new_cracks > 0)} pixels")
```

### Cải tiến 4: Deep learning
```python
# Dùng U-Net hoặc DeepCrack
# Input: ảnh bê tông
# Output: segmentation mask vết nứt
# Ưu điểm: Chính xác hơn, ít tham số
```

### Cải tiến 5: 3D reconstruction (nếu có stereo camera)
```python
# Tính độ sâu vết nứt
# Kết hợp depth map và skeleton
# → Đánh giá mức độ nguy hiểm chính xác hơn
```

---

## Tips Đọc Code Nhanh

1. **Hiểu LoG** (dòng 32-52) - cốt lõi thuật toán
2. **Multi-scale approach** (dòng 124-136) - tại sao cần nhiều sigma
3. **Adaptive threshold** (dòng 144-152) - so với Otsu
4. **Skeletonization** (dòng 159) - ý nghĩa và ứng dụng
5. **Phân tích severity** (dòng 209-226) - cách đánh giá

---

**Tổng số dòng:** 237 dòng
**Độ khó:** Trung bình-Khó
**Thời gian đọc hiểu:** 20-25 phút
**Thời gian chạy:** ~2 giây (do multi-scale)
**Ứng dụng thực tế:** Kiểm tra đường bộ, cầu, tòa nhà, sân bay, đập thủy điện
