# Bài 8: Tách Foreground - Core & Rim - How to Read

## Tổng Quan
File `extract.py` (318 dòng) sử dụng Erosion để tách core (tâm) và rim (biên) của vật thể.

## Thuật Toán (5 bước)
1. Nhị phân Otsu (dòng 93-96)
2. Tạo SE ELLIPSE 5×5 (dòng 103-107)
3. Erosion → Core (dòng 114-117)
4. A - Core = Rim (dòng 124-127)
5. So sánh kernel khác nhau (dòng 143-165)

## Code Quan Trọng

### Core & Rim
```python
B = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
core = cv2.erode(A, B)
rim = cv2.subtract(A, core)
```

### Overlay Màu
```python
overlay[core == 255] = [255, 200, 0]  # Core = xanh lam
overlay[rim == 255] = [0, 255, 0]     # Rim = xanh lá
```

## Tham Số
- Kernel: ELLIPSE 5×5
- So sánh: 3×3, 5×5, 7×7, 9×9

## Kết Quả
- Core: Phần trung tâm ổn định
- Rim: Phần biên
- Kernel lớn → rim dày hơn

**File**: `bai-8-foreground-extraction/extract.py`
