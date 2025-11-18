# Bài 3: Trích Biên Bằng Morphological Gradient - How to Read

## Tổng Quan

File `extract_edges.py` (198 dòng) sử dụng Morphological Gradient (Dilation - Erosion) để phát hiện biên và so sánh với Canny Edge Detection.

## Input/Output

**Input**: `../input/objects/sample.png`
**Output**: 
- `gradient.png`: Biên từ Morph Gradient
- `canny.png`: Biên từ Canny
- `kernel_comparison.png`: Gradient với kernel 3×3, 5×5, 7×7

## Thuật Toán Chính

1. Nhị phân hóa (dòng 74)
2. Morph Gradient với RECT 3×3 (dòng 82-87)
3. Canny Edge Detection để so sánh (dòng 94-96)
4. So sánh số pixel biên (dòng 104-109)
5. Test với nhiều kernel sizes (dòng 150-166)

## Code Quan Trọng

### 1. Morphological Gradient (Dòng 85-87)

```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
grad = cv2.morphologyEx(bw, cv2.MORPH_GRADIENT, kernel)
# grad = dilation(bw) - erosion(bw)
```

### 2. So Sánh với Canny (Dòng 94-109)

```python
edges = cv2.Canny(img, 50, 150)
print(f"[+] Số pixel biên Morph: {np.sum(grad > 0)}")
print(f"[+] Số pixel biên Canny: {np.sum(edges > 0)}")
print(f"[+] Tỷ lệ: {np.sum(grad > 0) / np.sum(edges > 0):.2f}")
```

**Kết quả**: Morph gradient có nhiều pixel hơn (biên dày hơn)

### 3. Multi-scale Gradient (Dòng 150-166)

```python
for k in [3, 5, 7]:
    kernel_test = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
    grad_test = cv2.morphologyEx(bw, cv2.MORPH_GRADIENT, kernel_test)
    edge_pixels = np.sum(grad_test > 0)
```

## Tham Số Quan Trọng

| Tham Số | Giá Trị | Ý Nghĩa |
|---------|---------|---------|
| Kernel Size | 3×3 | Độ dày biên (lớn hơn → dày hơn) |
| Canny Low | 50 | Threshold thấp cho hysteresis |
| Canny High | 150 | Threshold cao cho hysteresis |

## Kết Quả Mong Đợi

**Morph Gradient:**
- Biên dày, liên tục
- Ít nhạy với nhiễu
- Nhanh

**Canny:**
- Biên mỏng, chính xác
- Nhạy hơn
- Chậm hơn

## Lỗi Thường Gặp

**Lỗi 1: Biên quá dày** → Giảm kernel size
**Lỗi 2: Biên đứt đoạn** → Tăng kernel size
**Lỗi 3: Nhiều nhiễu** → Áp dụng Opening trước Gradient

## Mở Rộng

1. **Directional Gradient**: Gradient theo hướng ngang/dọc
2. **Internal/External Gradient**: Chỉ lấy biên trong hoặc ngoài
3. **Weighted Gradient**: Kết hợp nhiều scales

**File**: `bai-3-gradient/extract_edges.py`
**Theory**: [02-advanced-morphology.md](../theory/02-advanced-morphology.md)
