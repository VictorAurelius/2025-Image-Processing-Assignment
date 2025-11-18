# Bài 7: Pruning - Xóa Pixel Thừa - How to Read

## Tổng Quan
File `prune.py` (306 dòng) sử dụng Hit-or-Miss Transform với 8 SE để xóa pixel thừa (spurs) ở cạnh.

## Thuật Toán (6 bước)
1. Nhị phân hóa về {0,1} (dòng 84-87)
2. Tạo base SE (dòng 98-105)
3. Xoay tạo 8 SE (dòng 109-117)
4. Lặp Hit-or-Miss (dòng 135-155)
5. Xóa pixels được hit (dòng 146)
6. Hội tụ hoặc max iterations

## Code Quan Trọng

### Base SE (3 Giá Trị)
```python
base = np.array([[0, 0, 0],
                 [-1, 1, -1],
                 [1, 1, 1]], dtype=np.int8)
# 0 = must be 0 (nền)
# 1 = must be 1 (vật thể)
# -1 = don't care
```

### Tạo 8 SE
```python
SEs = []
for k in range(4):
    SEs.append(np.rot90(base, k))
    SEs.append(np.rot90(np.fliplr(base), k))
```

### Hit-or-Miss
```python
hm = cv2.morphologyEx(bw.astype(np.uint8), cv2.MORPH_HITMISS, se)
bw = np.where(hm == 1, 0, bw)  # Xóa pixels được hit
```

## Tham Số
- Max iterations: 10
- SE: 3×3 với 8 hướng xoay

## Kết Quả
- Skeleton gọn gàng, không có gai
- Hội tụ sau 3-5 iterations

**File**: `bai-7-pruning/prune.py`
