# Hướng Dẫn Đọc Code: Bài 5 - Edge Detection + Hough Transform

## Tổng Quan
Dò biên bằng Canny và phát hiện đường thẳng bằng Hough Transform.

## Input/Output
**Input:** Ảnh có vạch kẻ đường | **Output:** Edges + đường thẳng phát hiện

## Thuật Toán Chính

### 1. Canny Edge Detection (dòng 74)
```python
edges = cv2.Canny(gray, canny_low=80, canny_high=160)
```
**Tham số:** `low=80, high=160` (tỷ lệ 1:2 hoặc 1:3)

### 2. HoughLinesP (dòng 92-95)
```python
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80,
                        minLineLength=60, maxLineGap=10)
```

## Code Quan Trọng

### Vẽ đường thẳng (dòng 105-107)
```python
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(out, (x1, y1), (x2, y2), (0, 255, 0), 2)
```

### Tính góc và độ dài (dòng 110-111)
```python
length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
angle = np.arctan2(y2-y1, x2-x1) * 180 / np.pi
```

## Tham Số

| Tham số | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `threshold` | 80 | Số votes tối thiểu trong Hough space |
| `minLineLength` | 60 | Độ dài tối thiểu (pixels) |
| `maxLineGap` | 10 | Khoảng cách nối 2 đoạn |

## Lỗi Thường Gặp

### Phát hiện quá nhiều/ít đường
**Fix:** Điều chỉnh threshold
```python
# Nhiều đường → tăng threshold
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=120, ...)

# Ít đường → giảm threshold
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, ...)
```

## Mở Rộng

### Lọc đường thẳng theo góc
```python
vertical_lines = []
horizontal_lines = []
for line in lines:
    x1, y1, x2, y2 = line[0]
    angle = np.arctan2(y2-y1, x2-x1) * 180 / np.pi
    
    if abs(angle) > 80 or abs(angle) < 100:  # Gần vertical
        vertical_lines.append(line)
    elif abs(angle) < 10 or abs(angle) > 170:  # Gần horizontal
        horizontal_lines.append(line)
```

---
**File:** `bai-5-edge-hough/detect.py` (223 dòng)
