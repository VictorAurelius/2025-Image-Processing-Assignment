# Lý Thuyết: Phân Vùng Chuyển Động (Motion Segmentation)

## Tổng Quan

Phân vùng chuyển động (motion segmentation) là kỹ thuật tách các vùng chuyển động trong chuỗi video, dựa trên sự khác biệt về thời gian giữa các frame liên tiếp. Phương pháp này đặc biệt quan trọng trong video surveillance, tracking, và các ứng dụng thời gian thực.

Hai phương pháp chính là Frame Differencing (sai khác giữa các frame liên tiếp) và Background Subtraction (trừ background model). Frame Differencing đơn giản và nhanh nhưng chỉ phát hiện biên chuyển động, trong khi Background Subtraction mô hình hóa nền để phát hiện toàn bộ vật thể chuyển động.

Ứng dụng rộng rãi: đếm người/xe, phát hiện xâm nhập, phân tích hành vi, gesture recognition, và video compression.

## Ứng Dụng

- **Bài 9**: Motion Segmentation - Đếm người/xe đi qua cổng bằng MOG2 và Frame Differencing

## Nguyên Lý Toán Học

### 1. Frame Differencing

**Temporal Difference:**

```
D_t(x,y) = |I_t(x,y) - I_{t-1}(x,y)|
```

**Thresholding:**

```
FG_t(x,y) = { 1  nếu D_t(x,y) > τ
            { 0  ngược lại
```

**Three-Frame Differencing (robust hơn):**

```
D_t(x,y) = |I_t(x,y) - I_{t-1}(x,y)| AND |I_{t+1}(x,y) - I_t(x,y)|
```

**Độ phức tạp:** O(n) - rất nhanh

### 2. Background Subtraction

**Model nền đơn giản:**

```
B(x,y) = mean{I_1(x,y), I_2(x,y), ..., I_k(x,y)}
```

**Phát hiện foreground:**

```
FG_t(x,y) = { 1  nếu |I_t(x,y) - B(x,y)| > τ
            { 0  ngược lại
```

**Running Average Update:**

```
B_t(x,y) = α × I_t(x,y) + (1-α) × B_{t-1}(x,y)
```

Với α ∈ [0,1] (thường 0.01-0.05)

### 3. Mixture of Gaussians (MOG/MOG2)

Mỗi pixel được mô hình bằng K phân bố Gaussian:

```
P(I_t(x,y)) = Σᵢ₌₁ᴷ wᵢ,ₜ × N(I_t | μᵢ,ₜ, Σᵢ,ₜ)
```

**Gaussian 2D:**

```
N(x | μ, σ²) = (1/(σ√(2π))) × exp(-(x-μ)²/(2σ²))
```

**Update rules (MOG2):**

```
# Matching criterion
Match nếu: |I_t - μᵢ| < 2.5σᵢ

# Weight update
wᵢ,ₜ = (1-α) × wᵢ,ₜ₋₁ + α × M_i,t

# Mean update (nếu match)
μᵢ,ₜ = (1-ρ) × μᵢ,ₜ₋₁ + ρ × I_t

# Variance update
σ²ᵢ,ₜ = (1-ρ) × σ²ᵢ,ₜ₋₁ + ρ × (I_t - μᵢ,ₜ)²
```

Với:
- α: Learning rate (0.001-0.01)
- ρ = α × N(I_t | μᵢ, σᵢ²)

**Background/Foreground classification:**

```
B = Top-b distributions (largest wᵢ/σᵢ)
FG nếu pixel không match bất kỳ B nào
```

**Độ phức tạp:** O(n × K) với K = 3-5

### 4. KNN Background Subtraction

Dựa trên K-nearest neighbors trong temporal history.

```
Distance: d(x, sample) = |I_t(x) - sample|
FG nếu: d(x, sample) > R cho tất cả K neighbors
```

**Tham số:**
- K: Số neighbors (thường 1-3)
- R: Radius threshold
- N_samples: Số mẫu lưu trữ (thường 20-50)

### 5. Optical Flow

Ước lượng vector chuyển động của mỗi pixel.

**Horn-Schunck Constraint:**

```
I_x × u + I_y × v + I_t = 0
```

Với:
- u, v: Optical flow (x, y components)
- I_x, I_y, I_t: Gradients theo x, y, t

**Farneback Dense Optical Flow:**

Approximates neighborhood với polynomial:

```
I(x) ≈ x^T A x + b^T x + c
```

## Code Examples (OpenCV)

### 1. Frame Differencing

```python
import cv2
import numpy as np

def frame_differencing(video_path, threshold=25):
    """
    Phát hiện chuyển động bằng frame differencing.

    Args:
        video_path: Path to video
        threshold: Ngưỡng sai khác

    Returns:
        Processed frames
    """
    cap = cv2.VideoCapture(video_path)

    _, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.GaussianBlur(prev_gray, (5, 5), 0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale and blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # Frame difference
        diff = cv2.absdiff(gray, prev_gray)

        # Threshold
        _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

        # Morphology để loại nhiễu
        kernel = np.ones((3, 3), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # Tìm contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

        # Vẽ bounding boxes
        for cnt in contours:
            if cv2.contourArea(cnt) > 500:  # Lọc nhiễu
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow('Motion', frame)
        cv2.imshow('Difference', thresh)

        prev_gray = gray

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
```

### 2. MOG2 Background Subtraction

```python
def mog2_background_subtraction(video_path):
    """
    Background subtraction bằng MOG2.

    MOG2: Improved adaptive Gaussian mixture model
    """
    cap = cv2.VideoCapture(video_path)

    # Tạo background subtractor
    bg_subtractor = cv2.createBackgroundSubtractorMOG2(
        history=500,            # Số frames để build model
        varThreshold=16,        # Threshold on Mahalanobis distance
        detectShadows=True      # Phát hiện bóng
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Apply background subtraction
        fg_mask = bg_subtractor.apply(frame)

        # Bóng được đánh dấu là 127 (gray)
        # Chuyển thành 0 nếu không muốn xử lý bóng
        fg_mask[fg_mask == 127] = 0

        # Morphology
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=2)

        # Tìm contours
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

        # Vẽ bounding boxes
        for cnt in contours:
            if cv2.contourArea(cnt) > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow('Frame', frame)
        cv2.imshow('FG Mask', fg_mask)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
```

### 3. KNN Background Subtraction

```python
def knn_background_subtraction(video_path):
    """Background subtraction bằng KNN."""

    cap = cv2.VideoCapture(video_path)

    # KNN background subtractor
    bg_subtractor = cv2.createBackgroundSubtractorKNN(
        history=500,
        dist2Threshold=400.0,
        detectShadows=True
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        fg_mask = bg_subtractor.apply(frame)

        # Xử lý tương tự MOG2
        fg_mask[fg_mask == 127] = 0
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

        cv2.imshow('Frame', frame)
        cv2.imshow('KNN Mask', fg_mask)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
```

### 4. Optical Flow (Farneback)

```python
def dense_optical_flow(video_path):
    """Dense optical flow bằng Farneback."""

    cap = cv2.VideoCapture(video_path)

    ret, first_frame = cap.read()
    prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

    # HSV image để visualize flow
    hsv = np.zeros_like(first_frame)
    hsv[..., 1] = 255

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Farneback optical flow
        flow = cv2.calcOpticalFlowFarneback(
            prev_gray, gray,
            None,
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0
        )

        # Tính magnitude và angle
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        # Encode vào HSV
        hsv[..., 0] = ang * 180 / np.pi / 2  # Hue = direction
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)  # Value = magnitude

        # Convert to BGR
        flow_bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        cv2.imshow('Frame', frame)
        cv2.imshow('Optical Flow', flow_bgr)

        prev_gray = gray

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
```

## So Sánh Các Phương Pháp

| Phương pháp | Độ phức tạp | Tốc độ | Ưu điểm | Nhược điểm |
|------------|-------------|--------|---------|------------|
| **Frame Diff** | O(n) | Rất nhanh | Đơn giản, realtime | Chỉ phát hiện biên |
| **Running Average** | O(n) | Nhanh | Đơn giản | Không xử lý được illumination changes |
| **MOG/MOG2** | O(n×K) | Nhanh | Robust, xử lý multi-modal | Cần training, tham số |
| **KNN** | O(n×N) | Trung bình | Không giả định phân bố | Chậm hơn MOG2 |
| **Optical Flow** | O(n) | Chậm | Thông tin chuyển động chi tiết | Tính toán nặng |

## Ưu Nhược Điểm

### Frame Differencing

**Ưu điểm:**
- Cực kỳ đơn giản và nhanh
- Không cần training
- Realtime cho mọi hardware

**Nhược điểm:**
- Chỉ phát hiện biên chuyển động (không phải toàn bộ vật thể)
- Nhạy với nhiễu
- Không xử lý được stopped objects

### MOG2

**Ưu điểm:**
- Adaptive, xử lý illumination changes
- Phát hiện shadow
- Robust với multi-modal backgrounds
- Tốc độ tốt

**Nhược điểm:**
- Cần training period
- Nhiều tham số cần điều chỉnh
- Không tốt với dynamic backgrounds

### Optical Flow

**Ưu điểm:**
- Thông tin chuyển động chi tiết (magnitude + direction)
- Không cần background model
- Có thể tracking individual objects

**Nhược điểm:**
- Chậm (computational expensive)
- Nhạy với nhiễu
- Aperture problem

## Kỹ Thuật Nâng Cao

### 1. Adaptive Learning Rate

```python
# Học nhanh khi có thay đổi lớn, chậm khi stable
def adaptive_learning_rate(diff, base_rate=0.01):
    if diff > threshold_high:
        return base_rate * 5  # Học nhanh
    elif diff < threshold_low:
        return base_rate * 0.5  # Học chậm
    else:
        return base_rate
```

### 2. Shadow Removal

```python
def remove_shadows(fg_mask, frame, bg_model):
    """Loại bỏ bóng từ foreground mask."""

    # Bóng: Chromaticity giống nền, Intensity thấp hơn
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_bg = cv2.cvtColor(bg_model, cv2.COLOR_BGR2HSV)

    # Ratio test
    ratio = hsv[..., 2] / (hsv_bg[..., 2] + 1e-5)

    # Shadow nếu: 0.5 < ratio < 0.95 và hue/sat giống
    shadow_mask = ((ratio > 0.5) & (ratio < 0.95) &
                   (abs(hsv[..., 0] - hsv_bg[..., 0]) < 10))

    fg_mask[shadow_mask] = 0

    return fg_mask
```

### 3. Temporal Median Filter

```python
def temporal_median_background(video_path, n_frames=50):
    """Tạo background bằng temporal median."""

    cap = cv2.VideoCapture(video_path)

    frames = []
    for _ in range(n_frames):
        ret, frame = cap.read()
        if ret:
            frames.append(frame)

    # Median theo temporal axis
    background = np.median(frames, axis=0).astype(np.uint8)

    cap.release()
    return background
```

## Tài Liệu Tham Khảo

1. **Stauffer, C., & Grimson, W. E. L.** (1999). "Adaptive background mixture models for real-time tracking." CVPR, 246-252.

2. **Zivkovic, Z.** (2004). "Improved adaptive Gaussian mixture model for background subtraction." ICPR, 2, 28-31.

3. **Farnebäck, G.** (2003). "Two-frame motion estimation based on polynomial expansion." SCIA, 363-370.

4. **Piccardi, M.** (2004). "Background subtraction techniques: a review." IEEE SMC, 4, 3099-3104.

## Liên Kết

- **Code:** [Bài 9: Motion Segmentation](/code-implement/T79-phan-vung-anh/bai-9-motion-segmentation/)
- **Lý thuyết:** [06: Evaluation](06-segmentation-evaluation.md)

---

**Tác giả:** Ph.D Phan Thanh Toàn | **Cập nhật:** 2025-11-17
