# Bài 6: Đo Đạc Hạt/Lỗ - How to Read

## Tổng Quan
File `measure.py` (329 dòng) phân loại hạt/lỗ theo kích thước (nhỏ/vừa/lớn) bằng Closing+findContours.

## Thuật Toán (7 bước)
1. Nhị phân INV (dòng 87)
2. Closing làm tròn (dòng 96-99)
3. findContours (dòng 106-107)
4. Tính diện tích (dòng 110-113)
5. Phân cụm percentile (dòng 120-132)
6. Vẽ phân loại (dòng 139-169)
7. Thống kê (dòng 255-294)

## Code Quan Trọng

### Phân Cụm Percentile
```python
areas = [cv2.contourArea(c) for c in contours]
t1, t2 = np.percentile(areas, [33, 66])
small = sum(a <= t1 for a in areas)
mid = sum((a > t1) & (a <= t2) for a in areas)
big = sum(a > t2 for a in areas)
```

### Tính Properties
```python
area = cv2.contourArea(cnt)
perimeter = cv2.arcLength(cnt, True)
M = cv2.moments(cnt)
cx = M['m10'] / M['m00']
cy = M['m01'] / M['m00']
circularity = 4 * np.pi * area / (perimeter ** 2)
```

## Tham Số
- Closing kernel: 3×3, iterations=2
- Percentile: 33% và 66%

## Kết Quả
- Phân loại: S (xanh lá), M (cam), L (đỏ)
- Histogram diện tích
- File thống kê `statistics.txt`

**File**: `bai-6-particle-measurement/measure.py`
