# Hướng Dẫn Đọc Code: Bài 6 - Region Growing

## Tổng Quan
Lan tỏa vùng từ seed points với tiêu chí |I(p) - I(neighbor)| ≤ τ.

## Input/Output
**Input:** Ảnh siêu âm, seed points | **Output:** Mask vùng lan tỏa

## Thuật Toán Chính

### `region_growing()` (dòng 21-65)

**BFS Queue (dòng 40-64):**
```python
q = deque()
# Khởi tạo seeds
for sy, sx in seeds:
    q.append((sy, sx))
    visited[sy, sx] = 1
    out[sy, sx] = 255

# Lan tỏa
while q:
    y, x = q.popleft()
    for dy, dx in dirs:  # 8-connected
        ny, nx = y + dy, x + dx
        if 0 <= ny < H and 0 <= nx < W and not visited[ny, nx]:
            if abs(int(gray[ny, nx]) - int(gray[y, x])) <= tau:
                visited[ny, nx] = 1
                out[ny, nx] = 255
                q.append((ny, nx))
```

## Code Quan Trọng

### 8 hướng láng giềng (dòng 37-38)
```python
dirs = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
```

### Tiêu chí tương đồng (dòng 60)
```python
if abs(int(gray[ny, nx]) - int(gray[y, x])) <= tau:
```

### Vẽ seed points (dòng 154-156)
```python
cv2.circle(img_with_seeds, (sx, sy), 5, (0, 0, 255), -1)  # Đỏ
cv2.circle(img_with_seeds, (sx, sy), 7, (255, 255, 255), 2)  # Viền trắng
```

## Tham Số

| Tham số | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `tau` | 6 | Ngưỡng sai khác cho phép |
| `seeds` | [(200,250), ...] | Danh sách seed points (y, x) |

## Lỗi Thường Gặp

### Vùng lan tràn quá mức
**Nguyên nhân:** `tau` quá lớn
**Fix:** Giảm tau
```python
mask, _ = region_growing(gray, seeds, tau=3)
```

### Vùng quá nhỏ
**Nguyên nhân:** `tau` quá nhỏ hoặc seed không tốt
**Fix:** Tăng tau hoặc chọn seed ở vùng đại diện

## Mở Rộng

### Tiêu chí kết hợp (local + global)
```python
def region_growing_dynamic(gray, seeds, tau_local=5, tau_global=10):
    # ... (khởi tạo)
    region_mean = np.mean(region_pixels)
    
    # Tiêu chí kết hợp
    if (abs(pixel - neighbor) <= tau_local and 
        abs(pixel - region_mean) <= tau_global):
        # Add to region
```

---
**File:** `bai-6-region-growing/grow.py` (254 dòng)
