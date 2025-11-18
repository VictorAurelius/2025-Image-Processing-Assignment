# Hướng Dẫn Đọc Code: Bài 9 - Motion Segmentation

## Tổng Quan
Phát hiện chuyển động trong video bằng Frame Differencing và MOG2 Background Subtraction.

## Input/Output
**Input:** Video `../input/gate.mp4` | **Output:** Motion masks, bounding boxes, statistics

## Thuật Toán Chính

### 1. `create_sample_video()` (dòng 20-61)
Tạo video mẫu 640×480 với 3 vật thể di chuyển:
- Vật 1: Trái → Phải (dòng 38-40)
- Vật 2: Phải → Trái (dòng 43-45)
- Vật 3: Đường chéo (dòng 48-52)

### 2. `process_video_motion_detection()` (dòng 64-161)

**MOG2 Background Subtractor (dòng 73):**
```python
bg = cv2.createBackgroundSubtractorMOG2(
    history=300,        # Số frames build model
    varThreshold=25,    # Threshold Mahalanobis distance
    detectShadows=True  # Phát hiện bóng (127)
)
```

**Frame Differencing (dòng 102-105):**
```python
diff = cv2.absdiff(gray, prev)
_, diffth = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
diffth = cv2.morphologyEx(diffth, cv2.MORPH_OPEN, np.ones((3,3)))
```

## Code Quan Trọng

### MOG2 Apply (dòng 93-95)
```python
fg = bg.apply(frame)
_, fgth = cv2.threshold(fg, 200, 255, cv2.THRESH_BINARY)
fgth = cv2.morphologyEx(fgth, cv2.MORPH_OPEN, np.ones((3,3)), iterations=2)
```
**Giải thích:**
- `bg.apply()` update model và return foreground mask
- Shadow pixels = 127 → threshold(200) loại bỏ
- Morphology opening loại nhiễu

### Tìm và vẽ contours (dòng 108-128)
```python
contours_mog2, _ = cv2.findContours(fgth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours_mog2:
    if cv2.contourArea(cnt) > 500:  # Lọc nhiễu
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame_mog2, (x, y), (x+w, y+h), (0, 255, 0), 2)
        num_objects_mog2 += 1
```

### Thống kê (dòng 131-137)
```python
motion_stats.append({
    'frame': frame_count,
    'mog2_objects': num_objects_mog2,
    'diff_objects': num_objects_diff,
    'mog2_pixels': np.sum(fgth == 255),
    'diff_pixels': np.sum(diffth == 255)
})
```

## Tham Số Quan Trọng

### MOG2
| Tham số | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `history` | 300 | Số frames để build background model |
| `varThreshold` | 25 | Threshold phát hiện foreground (↓ → nhạy hơn) |
| `detectShadows` | True | Phát hiện bóng (127 trong mask) |

### Frame Differencing
| Tham số | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `threshold` | 25 | Ngưỡng sai khác giữa 2 frames |
| `min_area` | 500 | Diện tích tối thiểu contour |

## Kết Quả Mong Đợi
- MOG2: Phát hiện toàn bộ vật thể chuyển động
- Frame Diff: Chỉ phát hiện biên chuyển động
- MOG2 xử lý shadow tốt hơn
- Frame Diff nhanh hơn nhưng nhiễu hơn

## Lỗi Thường Gặp

### 1. Phát hiện quá nhiều false positives
**Nguyên nhân:** `varThreshold` quá nhỏ hoặc có nhiễu
**Fix:**
```python
# Tăng varThreshold
bg = cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=40, detectShadows=True)

# Hoặc tăng morphology iterations
fgth = cv2.morphologyEx(fgth, cv2.MORPH_OPEN, kernel, iterations=3)
```

### 2. Vật thể đứng yên bị phát hiện ban đầu rồi biến mất
**Nguyên nhân:** MOG2 học vật thể vào background
**Fix:** Giảm learning rate
```python
fg = bg.apply(frame, learningRate=0.001)  # Default = -1 (auto)
```

### 3. Ghost (bóng ma) khi vật thể di chuyển
**Nguyên nhân:** Background chưa cập nhật đủ nhanh
**Fix:** Tăng learning rate
```python
fg = bg.apply(frame, learningRate=0.01)
```

## Mở Rộng

### 1. KNN Background Subtractor
```python
bg_knn = cv2.createBackgroundSubtractorKNN(
    history=500,
    dist2Threshold=400.0,
    detectShadows=True
)
fg_knn = bg_knn.apply(frame)
```

### 2. Tracking vật thể
```python
# Sử dụng centroid tracking
from collections import defaultdict

trackers = defaultdict(list)
for i, cnt in enumerate(contours):
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        trackers[i].append((cx, cy))
        
        # Vẽ trajectory
        if len(trackers[i]) > 1:
            cv2.polylines(frame, [np.array(trackers[i])], False, (255, 0, 0), 2)
```

### 3. Đếm vật thể qua line
```python
line_y = 200  # Vị trí line đếm

for cnt in contours:
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cy = int(M["m01"] / M["m00"])
        if abs(cy - line_y) < 5:  # Vật thể gần line
            count += 1
```

### 4. Optical Flow
```python
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
```

### 5. Lưu video output
```python
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out_video = cv2.VideoWriter('output.mp4', fourcc, 10, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
    # ... process frame
    out_video.write(frame_with_boxes)

out_video.release()
```

---
**File:** `bai-9-motion-segmentation/segment.py` (270 dòng)
**Lý thuyết:** [05-motion-segmentation.md](../theory/05-motion-segmentation.md)
