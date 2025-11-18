# Bài 9: Khử Nền - Top-hat/Black-hat - How to Read

## Tổng Quan
File `remove.py` (353 dòng) sử dụng Top-hat và Black-hat để khử nền không đồng đều trên ảnh grayscale.

## Thuật Toán (10 bước)
1. Đọc ảnh grayscale (dòng 74-83)
2. Histogram gốc (dòng 90-91)
3. Tạo kernel RECT 15×15 (dòng 98-100)
4. Top-hat (dòng 107-110)
5. Black-hat (dòng 117-120)
6. Điều chỉnh: img + tophat - blackhat (dòng 128-130)
7. Histogram sau điều chỉnh (dòng 133)
8. So sánh kernels (dòng 150-171)
9. Phân tích chất lượng (dòng 249-284)
10. Profile line (dòng 306-313)

## Code Quan Trọng

### Top-hat & Black-hat
```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
corrected = cv2.normalize(img + tophat - blackhat, None, 0, 255, cv2.NORM_MINMAX)
```

### Tính Uniformity
```python
def calculate_uniformity(image):
    h, w = image.shape
    regions = []
    for i in range(0, h, 100):
        for j in range(0, w, 100):
            region = image[i:min(i+100, h), j:min(j+100, w)]
            regions.append(region.mean())
    return np.std(regions)  # Càng thấp càng đồng đều
```

## Tham Số
- Kernel: RECT 15×15 (lớn để ước lượng nền)
- So sánh: 7×7, 11×11, 15×15, 21×21

## Kết Quả
- Nền đồng đều hơn
- Độ đồng đều cải thiện 30-50%
- Histogram rõ ràng hơn

**File**: `bai-9-background-removal/remove.py`
