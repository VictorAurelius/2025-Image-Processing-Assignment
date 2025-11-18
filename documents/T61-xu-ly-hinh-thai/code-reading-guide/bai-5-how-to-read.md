# Bài 5: Phân Đoạn Ký Tự - How to Read

## Tổng Quan
File `segment.py` (263 dòng) tách từng ký tự từ biển số/tem bằng Opening+Closing+Connected Components.

## Thuật Toán (7 bước)
1. Nhị phân INV (dòng 75)
2. Opening khử nhiễu (dòng 84-90)
3. Closing nối nét (dòng 97-103)
4. Connected Components (dòng 110-112)
5. Phân tích từng component (dòng 118-137)
6. Lọc theo area (dòng 141-143)
7. Vẽ bbox & lưu ký tự (dòng 150-226)

## Code Quan Trọng

### Connected Components với Stats
```python
n, labels, stats, centroids = cv2.connectedComponentsWithStats(bw)
# stats[i] = [x, y, w, h, area]
```

### Lọc Components
```python
min_area = 100
max_area = img.shape[0] * img.shape[1] * 0.5
valid = [c for c in components if min_area < c['area'] < max_area]
```

## Tham Số Quan Trọng
- Opening kernel: 3×3 (khử nhiễu nhỏ)
- Closing kernel: 5×5 (nối nét)
- Min area: 100 px (loại nhiễu)
- Max area: 50% ảnh (loại vùng lớn)

## Kết Quả
- Tách từng ký tự riêng biệt
- Lưu vào `characters/char_01.png`, `char_02.png`, ...
- Chuẩn bị cho OCR

**File**: `bai-5-character-segmentation/segment.py`
