# Lý thuyết: Không gian Màu (Color Spaces)

## 1. Giới thiệu

Không gian màu là mô hình toán học để biểu diễn màu sắc. Mỗi không gian có ưu nhược điểm riêng cho các ứng dụng khác nhau.

## 2. RGB Color Space

### 2.1. Định nghĩa
**RGB** = Red + Green + Blue (mô hình cộng màu)

**Biểu diễn**:
```
Color = (R, G, B)
R, G, B ∈ [0, 255] (8-bit)
```

### 2.2. Đặc điểm
- **Additive**: Cộng ánh sáng (màn hình)
- **Device-dependent**: Phụ thuộc thiết bị
- **Intuitive**: Dễ hiểu nhưng không perceptually uniform

### 2.3. Chuyển đổi
**RGB → Grayscale**:
```
Gray = 0.299×R + 0.587×G + 0.114×B
```

**Lưu ý**: Hệ số khác nhau vì mắt người nhạy với xanh lá nhất.

## 3. HSV Color Space

### 3.1. Định nghĩa
**HSV** = Hue + Saturation + Value

**Thành phần**:
- **H (Hue)**: Màu sắc [0°, 360°] (OpenCV: [0, 179])
- **S (Saturation)**: Độ bão hòa [0, 1] hoặc [0%, 100%]
- **V (Value)**: Độ sáng [0, 1] hoặc [0%, 100%]

### 3.2. Hình học
**Cone model**:
- Đỉnh: Đen (V=0)
- Trục: Trắng-xám-đen
- Chu vi: Màu thuần khiết

**Hue circle**:
```
0° = Đỏ (Red)
60° = Vàng (Yellow)
120° = Xanh lá (Green)
180° = Cyan
240° = Xanh dương (Blue)
300° = Magenta
```

### 3.3. Chuyển đổi RGB → HSV

**Value**:
```
V = max(R, G, B)
```

**Saturation**:
```
S = 0                    if V = 0
S = (V - min(R,G,B)) / V otherwise
```

**Hue** (phức tạp, xem code OpenCV):
```python
hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
```

### 3.4. Ưu điểm
- **Perceptually meaningful**: H là màu, S là độ đậm, V là độ sáng
- **Robust to lighting**: H ít bị ảnh hưởng bởi shadow/lighting
- **Good for color-based segmentation**

### 3.5. Ứng dụng
- Phát hiện vùng da (skin detection)
- Color-based object tracking
- Image editing (Adobe Photoshop)

## 4. YCrCb Color Space

### 4.1. Định nghĩa
**YCrCb** = Luminance + Chroma Red + Chroma Blue

**Thành phần**:
- **Y**: Luma (độ sáng) [16, 235]
- **Cr**: Chroma Red (độ đỏ) [16, 240]
- **Cb**: Chroma Blue (độ xanh) [16, 240]

### 4.2. Chuyển đổi RGB → YCrCb

**Digital 8-bit** (JPEG standard):
```
Y  = 16  + 0.257×R + 0.504×G + 0.098×B
Cr = 128 + 0.439×R - 0.368×G - 0.071×B
Cb = 128 - 0.148×R - 0.291×G + 0.439×B
```

**OpenCV**:
```python
ycrcb = cv2.cvtColor(rgb, cv2.COLOR_RGB2YCrCb)
```

### 4.3. Đặc điểm
- **Separates luma and chroma**: Y riêng biệt với màu
- **Used in video compression**: JPEG, MPEG, H.264
- **Robust to lighting changes**: Cr, Cb ít bị ảnh hưởng bởi lighting

### 4.4. Ứng dụng
- **Skin detection**: Cr, Cb có range đặc trưng cho da người
- **Video compression**: Lợi dụng mắt người nhạy Y hơn Cr, Cb
- **Face detection**: Dựa trên Cr, Cb thresholds

## 5. So sánh các Color Spaces

| Feature | RGB | HSV | YCrCb |
|---------|-----|-----|-------|
| Intuitive | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Lighting invariance | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Skin detection | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Compression | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Speed | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

## 6. Skin Detection

### 6.1. HSV Thresholds
```python
# Ngưỡng da người trong HSV
lower_hsv = (0, 30, 90)    # (H_min, S_min, V_min)
upper_hsv = (25, 180, 255) # (H_max, S_max, V_max)
```

**Giải thích**:
- H ∈ [0, 25]: Vùng đỏ-cam (da)
- S ∈ [30, 180]: Không quá nhạt, không quá đậm
- V ∈ [90, 255]: Đủ sáng

### 6.2. YCrCb Thresholds
```python
# Ngưỡng da người trong YCrCb
lower_ycc = (0, 135, 85)   # (Y_min, Cr_min, Cb_min)
upper_ycc = (255, 180, 135) # (Y_max, Cr_max, Cb_max)
```

**Giải thích**:
- Y: Bất kỳ (không quan trọng)
- Cr ∈ [135, 180]: Đỏ vừa phải
- Cb ∈ [85, 135]: Xanh thấp

### 6.3. So sánh
- **HSV**: Tốt trong điều kiện ánh sáng ổn định
- **YCrCb**: Tốt hơn với lighting thay đổi
- **Best**: Kết hợp cả hai (intersection)

## 7. Các Color Spaces khác

### 7.1. HSL (Hue, Saturation, Lightness)
Tương tự HSV nhưng L khác V:
- **HSV**: V = max(R,G,B)
- **HSL**: L = (max(R,G,B) + min(R,G,B)) / 2

### 7.2. LAB (CIE L*a*b*)
- **L**: Lightness [0, 100]
- **a**: Green-Red [-128, 127]
- **b**: Blue-Yellow [-128, 127]

**Ưu điểm**: Perceptually uniform (khoảng cách Euclidean = sự khác biệt màu nhận thức)

### 7.3. CMYK (Cyan, Magenta, Yellow, Key/Black)
- **Subtractive color model**: In ấn
- Không dùng trong xử lý ảnh số thường

## 8. Chuyển đổi Color Space

### 8.1. OpenCV
```python
# RGB → HSV
hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)

# RGB → YCrCb
ycrcb = cv2.cvtColor(rgb, cv2.COLOR_RGB2YCrCb)

# BGR → Grayscale
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
```

**Lưu ý**: OpenCV mặc định dùng BGR, không phải RGB!

### 8.2. Scikit-image
```python
from skimage import color

# RGB → LAB
lab = color.rgb2lab(rgb)

# RGB → HSV
hsv = color.rgb2hsv(rgb)
```

## 9. Ứng dụng theo từng Color Space

### 9.1. RGB
- Display (màn hình)
- Camera capture
- Basic image processing

### 9.2. HSV
- Color-based segmentation
- Color adjustment (Photoshop Hue/Saturation)
- Object tracking by color
- Artistic effects

### 9.3. YCrCb
- Video compression (JPEG, MPEG)
- Skin detection
- Face detection preprocessing
- Chroma keying (green screen)

### 9.4. LAB
- Color correction
- Color matching
- Perceptual color difference
- Professional image editing

## 10. Best Practices

### 10.1. Chọn Color Space
```
Task: Color segmentation → HSV
Task: Skin detection → YCrCb
Task: Compression → YCrCb
Task: Display → RGB
Task: Color difference → LAB
```

### 10.2. Thresholding tips
- **HSV**: Careful với Hue wrapping (0° = 360°)
- **YCrCb**: Ignore Y, focus on Cr/Cb
- **RGB**: Thường không tốt cho thresholding

### 10.3. Lighting robustness
```
Best → Worst:
LAB > YCrCb > HSV > RGB
```

## 11. Code Examples Chi Tiết

### 11.1. Complete Skin Detection Pipeline
```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_skin_hsv(img_bgr):
    """Skin detection using HSV color space"""
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # Define skin color range in HSV
    # Hue: 0-25 (red-orange for skin tone)
    # Saturation: 30-180 (not too pale, not too saturated)
    # Value: 90-255 (bright enough)
    lower_hsv = np.array([0, 30, 90], dtype=np.uint8)
    upper_hsv = np.array([25, 180, 255], dtype=np.uint8)

    # Create mask
    mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

    return mask_hsv

def detect_skin_ycrcb(img_bgr):
    """Skin detection using YCrCb color space"""
    # Convert BGR to YCrCb
    ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)

    # Define skin color range in YCrCb
    # Y: 0-255 (any brightness - not critical)
    # Cr: 135-180 (red chroma)
    # Cb: 85-135 (blue chroma)
    lower_ycc = np.array([0, 135, 85], dtype=np.uint8)
    upper_ycc = np.array([255, 180, 135], dtype=np.uint8)

    # Create mask
    mask_ycc = cv2.inRange(ycrcb, lower_ycc, upper_ycc)

    return mask_ycc

def detect_skin_combined(img_bgr, morph_cleanup=True):
    """
    Robust skin detection combining HSV and YCrCb

    Args:
        img_bgr: Input image in BGR format
        morph_cleanup: Apply morphological operations to clean up mask

    Returns:
        mask_final: Binary mask of skin regions
    """
    # Get masks from both color spaces
    mask_hsv = detect_skin_hsv(img_bgr)
    mask_ycc = detect_skin_ycrcb(img_bgr)

    # Combine masks (intersection - both must agree)
    mask_final = cv2.bitwise_and(mask_hsv, mask_ycc)

    if morph_cleanup:
        # Remove small noise
        kernel_erode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        mask_final = cv2.erode(mask_final, kernel_erode, iterations=1)

        # Fill holes
        kernel_dilate = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask_final = cv2.dilate(mask_final, kernel_dilate, iterations=2)

    return mask_final

# Example usage
def demo_skin_detection(image_path):
    """Demo skin detection pipeline"""
    # Load image
    img = cv2.imread(image_path)

    # Detect skin using different methods
    mask_hsv = detect_skin_hsv(img)
    mask_ycc = detect_skin_ycrcb(img)
    mask_combined = detect_skin_combined(img)

    # Apply masks to original image
    skin_hsv = cv2.bitwise_and(img, img, mask=mask_hsv)
    skin_ycc = cv2.bitwise_and(img, img, mask=mask_ycc)
    skin_combined = cv2.bitwise_and(img, img, mask=mask_combined)

    # Visualize results
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))

    axes[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Original')

    axes[0, 1].imshow(mask_hsv, cmap='gray')
    axes[0, 1].set_title('HSV Mask')

    axes[0, 2].imshow(mask_ycc, cmap='gray')
    axes[0, 2].set_title('YCrCb Mask')

    axes[0, 3].imshow(mask_combined, cmap='gray')
    axes[0, 3].set_title('Combined Mask')

    axes[1, 0].axis('off')

    axes[1, 1].imshow(cv2.cvtColor(skin_hsv, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title('HSV Result')

    axes[1, 2].imshow(cv2.cvtColor(skin_ycc, cv2.COLOR_BGR2RGB))
    axes[1, 2].set_title('YCrCb Result')

    axes[1, 3].imshow(cv2.cvtColor(skin_combined, cv2.COLOR_BGR2RGB))
    axes[1, 3].set_title('Combined Result')

    for ax in axes.flatten():
        ax.axis('off')

    plt.tight_layout()
    plt.savefig('skin_detection_comparison.png', dpi=150)
    print("Saved: skin_detection_comparison.png")

# demo_skin_detection('person.jpg')
```

### 11.2. Color Space Conversion Visualization
```python
def visualize_color_spaces(img_path):
    """Visualize image in different color spaces"""
    # Load image (BGR)
    img_bgr = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # Convert to different color spaces
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    img_ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
    img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # Create figure
    fig, axes = plt.subplots(3, 4, figsize=(16, 12))

    # RGB channels
    axes[0, 0].imshow(img_rgb)
    axes[0, 0].set_title('RGB Original')

    axes[0, 1].imshow(img_rgb[:,:,0], cmap='Reds')
    axes[0, 1].set_title('R Channel')

    axes[0, 2].imshow(img_rgb[:,:,1], cmap='Greens')
    axes[0, 2].set_title('G Channel')

    axes[0, 3].imshow(img_rgb[:,:,2], cmap='Blues')
    axes[0, 3].set_title('B Channel')

    # HSV channels
    axes[1, 0].imshow(img_rgb)
    axes[1, 0].set_title('HSV Original')

    axes[1, 1].imshow(img_hsv[:,:,0], cmap='hsv')
    axes[1, 1].set_title('H (Hue)')

    axes[1, 2].imshow(img_hsv[:,:,1], cmap='gray')
    axes[1, 2].set_title('S (Saturation)')

    axes[1, 3].imshow(img_hsv[:,:,2], cmap='gray')
    axes[1, 3].set_title('V (Value)')

    # YCrCb channels
    axes[2, 0].imshow(img_rgb)
    axes[2, 0].set_title('YCrCb Original')

    axes[2, 1].imshow(img_ycrcb[:,:,0], cmap='gray')
    axes[2, 1].set_title('Y (Luma)')

    axes[2, 2].imshow(img_ycrcb[:,:,1], cmap='RdBu_r')
    axes[2, 2].set_title('Cr (Red chroma)')

    axes[2, 3].imshow(img_ycrcb[:,:,2], cmap='RdYlBu_r')
    axes[2, 3].set_title('Cb (Blue chroma)')

    for ax in axes.flatten():
        ax.axis('off')

    plt.tight_layout()
    plt.savefig('color_space_channels.png', dpi=150)
    print("Saved: color_space_channels.png")

# visualize_color_spaces('colorful_image.jpg')
```

### 11.3. HSV Color Selection Tool
```python
def create_hsv_color_selector():
    """Interactive HSV color range selector for object detection"""
    import cv2

    def nothing(x):
        pass

    # Create window
    cv2.namedWindow('HSV Selector')

    # Create trackbars
    cv2.createTrackbar('H_min', 'HSV Selector', 0, 179, nothing)
    cv2.createTrackbar('H_max', 'HSV Selector', 179, 179, nothing)
    cv2.createTrackbar('S_min', 'HSV Selector', 0, 255, nothing)
    cv2.createTrackbar('S_max', 'HSV Selector', 255, 255, nothing)
    cv2.createTrackbar('V_min', 'HSV Selector', 0, 255, nothing)
    cv2.createTrackbar('V_max', 'HSV Selector', 255, 255, nothing)

    # Load image
    img = cv2.imread('target.jpg')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    while True:
        # Get trackbar values
        h_min = cv2.getTrackbarPos('H_min', 'HSV Selector')
        h_max = cv2.getTrackbarPos('H_max', 'HSV Selector')
        s_min = cv2.getTrackbarPos('S_min', 'HSV Selector')
        s_max = cv2.getTrackbarPos('S_max', 'HSV Selector')
        v_min = cv2.getTrackbarPos('V_min', 'HSV Selector')
        v_max = cv2.getTrackbarPos('V_max', 'HSV Selector')

        # Create mask
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(hsv, lower, upper)

        # Apply mask
        result = cv2.bitwise_and(img, img, mask=mask)

        # Show images
        combined = np.hstack([img, result])
        cv2.imshow('HSV Selector', combined)

        # Print current range
        print(f"\rRange: H[{h_min}-{h_max}] S[{s_min}-{s_max}] V[{v_min}-{v_max}]", end='')

        # Exit on ESC
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
    print(f"\n\nFinal HSV range:")
    print(f"  lower = ({h_min}, {s_min}, {v_min})")
    print(f"  upper = ({h_max}, {s_max}, {v_max})")

# create_hsv_color_selector()
```

### 11.4. Performance Comparison
```python
import time

def benchmark_color_conversions(img_bgr, num_iterations=100):
    """Benchmark different color space conversions"""

    conversions = {
        'BGR to GRAY': cv2.COLOR_BGR2GRAY,
        'BGR to RGB': cv2.COLOR_BGR2RGB,
        'BGR to HSV': cv2.COLOR_BGR2HSV,
        'BGR to YCrCb': cv2.COLOR_BGR2YCrCb,
        'BGR to LAB': cv2.COLOR_BGR2LAB,
    }

    results = {}

    print("Benchmarking color space conversions...")
    print(f"Image size: {img_bgr.shape}")
    print(f"Iterations: {num_iterations}\n")

    for name, code in conversions.items():
        start = time.time()
        for _ in range(num_iterations):
            _ = cv2.cvtColor(img_bgr, code)
        elapsed = time.time() - start

        results[name] = elapsed / num_iterations * 1000  # ms

        print(f"{name:<20}: {results[name]:.3f} ms/frame")

    return results

# Example
img = cv2.imread('test.jpg')
benchmark_color_conversions(img)
```

**Output mẫu**:
```
Benchmarking color space conversions...
Image size: (1080, 1920, 3)
Iterations: 100

BGR to GRAY         : 0.523 ms/frame
BGR to RGB          : 0.612 ms/frame
BGR to HSV          : 1.234 ms/frame
BGR to YCrCb        : 0.987 ms/frame
BGR to LAB          : 1.456 ms/frame
```

### 11.5. Color-based Object Tracking
```python
def track_colored_object(video_path, color_range_hsv):
    """
    Track object by color in video

    Args:
        video_path: Path to video file
        color_range_hsv: Tuple of (lower, upper) HSV ranges
    """
    cap = cv2.VideoCapture(video_path)

    lower_hsv, upper_hsv = color_range_hsv

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create mask
        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

        # Clean up mask
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Get largest contour
            largest = max(contours, key=cv2.contourArea)

            # Get bounding box
            x, y, w, h = cv2.boundingRect(largest)

            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Get center
            cx, cy = x + w//2, y + h//2
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Display info
            cv2.putText(frame, f"Object at ({cx}, {cy})", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Show result
        cv2.imshow('Object Tracking', frame)
        cv2.imshow('Mask', mask)

        if cv2.waitKey(30) & 0xFF == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

# Example: Track red object
# Red wraps around in Hue, so need two ranges
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
# track_colored_object('video.mp4', (lower_red1, upper_red1))
```

## 12. Best Practices

### ✅ Nên làm

1. **Luôn nhớ OpenCV dùng BGR, không phải RGB**
   ```python
   # ✅ ĐÚNG
   img = cv2.imread('photo.jpg')  # BGR format
   img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert cho matplotlib

   # ❌ SAI - Quên convert
   plt.imshow(img)  # Màu sai (B và R đảo ngược)!
   ```
   **Lý do**: OpenCV default là BGR để tương thích với camera drivers cũ.

2. **Dùng đúng color space cho từng task**
   ```python
   # Skin detection → YCrCb
   ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

   # Color-based selection → HSV
   hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

   # Color difference → LAB
   lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
   ```

3. **Kết hợp nhiều color spaces cho robust detection**
   ```python
   mask_hsv = detect_in_hsv(img)
   mask_ycrcb = detect_in_ycrcb(img)
   mask_final = cv2.bitwise_and(mask_hsv, mask_ycrcb)  # Intersection
   ```
   **Lý do**: Mỗi color space có điểm mạnh riêng, kết hợp giảm false positives.

### ❌ Không nên làm

1. **Không dùng RGB cho thresholding**
   ```python
   # ❌ SAI - RGB coupling makes thresholding hard
   mask = (img[:,:,0] > 100) & (img[:,:,1] < 50) & (img[:,:,2] < 50)  # Phức tạp!

   # ✅ ĐÚNG - HSV decouples color from brightness
   hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   mask = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))  # Đơn giản hơn
   ```

2. **Không quên Hue wrapping**
   ```python
   # ❌ SAI - Red color spans 0° and 360°
   mask = cv2.inRange(hsv, (170, 50, 50), (10, 255, 255))  # Không work!

   # ✅ ĐÚNG - Handle wrapping
   mask1 = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
   mask2 = cv2.inRange(hsv, (170, 50, 50), (180, 255, 255))
   mask = cv2.bitwise_or(mask1, mask2)
   ```

### 💡 Tips

1. **HSV ranges cho màu common**
   ```
   Red:    H ∈ [0-10] or [170-180]
   Orange: H ∈ [10-25]
   Yellow: H ∈ [25-35]
   Green:  H ∈ [35-85]
   Blue:   H ∈ [85-125]
   Purple: H ∈ [125-155]
   ```

2. **Skin detection thresholds**
   ```python
   # HSV (works in normal lighting)
   lower_hsv = (0, 30, 90)
   upper_hsv = (25, 180, 255)

   # YCrCb (more robust to lighting)
   lower_ycc = (0, 135, 85)
   upper_ycc = (255, 180, 135)
   ```

## 13. Common Pitfalls

### Lỗi 1: BGR vs RGB confusion
**Vấn đề**:
```python
img = cv2.imread('photo.jpg')
plt.imshow(img)  # Colors look wrong!
```

**Giải pháp**:
```python
img_bgr = cv2.imread('photo.jpg')
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)  # Correct colors
```

### Lỗi 2: HSV range confusion (0-179 vs 0-360)
**Vấn đề**:
```python
# OpenCV HSV: H ∈ [0, 179]
# Standard HSV: H ∈ [0, 360]
```

**Giải pháp**: Luôn chia 2 khi convert từ degree sang OpenCV range.

### Lỗi 3: Thresholding trong sai color space
**Vấn đề**: Dùng RGB cho skin detection → khó tune, không robust.

**Giải pháp**: Dùng YCrCb hoặc HSV.

## 14. Bài tập Thực hành

### Bài 1: Implement Skin Detector
**Đề bài**: Viết hàm `detect_faces_by_skin()` phát hiện khuôn mặt bằng skin color.

**Gợi ý**:
- Combine HSV và YCrCb
- Morphological cleanup
- Find contours
- Filter by size/shape

### Bài 2: Color-based Object Counter
**Đề bài**: Đếm số objects có màu cụ thể trong ảnh.

**Gợi ý**:
- Convert to HSV
- Threshold
- Connected components labeling
- Filter và count

### Bài 3: Compare Color Spaces
**Đề bài**: So sánh hiệu quả của RGB, HSV, YCrCb cho skin detection trên 10 ảnh.

**Yêu cầu**: Tính precision, recall cho mỗi color space.

## 15. Tóm tắt

**RGB**: Đơn giản, trực tiếp, nhưng không perceptually uniform
**HSV**: Intuitive, tốt cho color selection, robust to lighting changes
**YCrCb**: Excellent cho skin detection và video compression
**LAB**: Perceptually uniform, tốt nhất cho color matching

**Rule of thumb**:
- Display → RGB
- User interaction → HSV
- Skin/face → YCrCb
- Color science → LAB

**Key Takeaways**:
1. **OpenCV uses BGR**, not RGB - always convert for display
2. **HSV separates color from brightness** - best for color-based segmentation
3. **YCrCb robust to lighting** - best for skin detection
4. **Combine multiple color spaces** for robust detection
5. **Hue wraps around** - handle red color carefully

---

**References**:
- Gonzalez & Woods - Digital Image Processing (Chapter 6)
- OpenCV Documentation - Color Space Conversions
- "A Review on Skin Color Detection" (various papers)
