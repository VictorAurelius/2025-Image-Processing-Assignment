# Bài 2: Lấp Lỗ Và Nối Nét - How to Read

## Tổng Quan

File `fill_holes.py` (189 dòng) sử dụng phép Closing (Dilation → Erosion) để lấp lỗ nhỏ và nối các khe hở trong vật thể.

## Input/Output

**Input**: `../input/parts/gapped.png` (linh kiện có lỗ)
**Output**: 
- `result.png`: So sánh trước/sau
- `closed.png`: Ảnh đã Closing
- `kernel_comparison.png`: So sánh RECT/ELLIPSE/CROSS

## Thuật Toán Chính

1. Nhị phân hóa Otsu (dòng 78)
2. Closing với ELLIPSE 7×7 (dòng 90-95)
3. Đếm diện tích đã lấp (dòng 98-102)
4. So sánh 3 loại kernel (dòng 140-163)

## Code Quan Trọng

### 1. Closing Để Lấp Lỗ (Dòng 90-102)

```python
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

# Đếm diện tích
black_pixels_after = np.sum(closed == 0)
filled_pixels = black_pixels_after - black_pixels_before
print(f"[+] Đã lấp thêm: {filled_pixels} pixels")
```

**Giải thích**: Closing = Dilation (lấp lỗ) → Erosion (phục hồi kích thước)

### 2. So Sánh Kernel Types (Dòng 140-163)

```python
kernel_types = [
    (cv2.MORPH_RECT, "RECT"),
    (cv2.MORPH_ELLIPSE, "ELLIPSE"),
    (cv2.MORPH_CROSS, "CROSS")
]

for morph_type, name in kernel_types:
    kernel_test = cv2.getStructuringElement(morph_type, (7, 7))
    closed_test = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel_test)
```

## Tham Số Quan Trọng

| Tham Số | Giá Trị | Ý Nghĩa |
|---------|---------|---------|
| Kernel Size | 7×7 | Lớn hơn lỗ cần lấp |
| Kernel Type | ELLIPSE | Lấp đều mọi hướng |
| Iterations | 1 | Số lần lặp Closing |

## Kết Quả Mong Đợi

- RECT: Lấp tốt theo ngang/dọc
- ELLIPSE: Lấp đều, tự nhiên nhất
- CROSS: Chỉ lấp 4 hướng chính

## Lỗi Thường Gặp

**Lỗi 1: Kernel quá nhỏ** → Không lấp đủ lỗ
**Fix**: Tăng kernel size hoặc iterations

**Lỗi 2: Kernel quá lớn** → Nối nhầm vật thể gần nhau
**Fix**: Giảm kernel hoặc dùng selective closing

## Mở Rộng

1. **Selective Hole Filling**: Chỉ lấp lỗ nhỏ hơn ngưỡng
2. **Directional Closing**: Chỉ nối theo hướng nhất định
3. **Iterative Closing**: Lặp nhiều lần với kernel nhỏ

**File**: `bai-2-closing/fill_holes.py`
