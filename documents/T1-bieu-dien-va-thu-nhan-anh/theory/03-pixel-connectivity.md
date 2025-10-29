# Lý thuyết: Kết nối Pixel (Pixel Connectivity)

## 1. Giới thiệu

Kết nối pixel định nghĩa mối quan hệ "láng giềng" giữa các pixel, quan trọng cho:
- Phân đoạn ảnh (segmentation)
- Phát hiện biên (edge detection)
- Gán nhãn vùng (region labeling)
- Tìm đường đi (pathfinding)

## 2. Các loại kết nối

### 2.1. 4-Connectivity (4-kết nối)

**Định nghĩa**: Pixel p và q là 4-connected nếu q nằm trong tập N₄(p).

**Láng giềng N₄(p)** của pixel p(x, y):
```
N₄(p) = {(x±1, y), (x, y±1)}
```

**4 láng giềng**:
```
       (x, y-1)
          |
(x-1, y)--p--(x+1, y)
          |
       (x, y+1)
```

**Đặc điểm**:
- Chỉ xét 4 hướng: trên, dưới, trái, phải
- Khoảng cách Manhattan: |Δx| + |Δy| = 1

### 2.2. 8-Connectivity (8-kết nối)

**Định nghĩa**: Pixel p và q là 8-connected nếu q nằm trong tập N₈(p).

**Láng giềng N₈(p)**:
```
N₈(p) = N₄(p) ∪ N_D(p)
```

Trong đó N_D(p) là 4 láng giềng chéo:
```
N_D(p) = {(x±1, y±1)}
```

**8 láng giềng**:
```
(x-1,y-1) (x,y-1) (x+1,y-1)
(x-1,y)     p     (x+1,y)
(x-1,y+1) (x,y+1) (x+1,y+1)
```

**Đặc điểm**:
- Xét cả 8 hướng (4 hướng chính + 4 chéo)
- Khoảng cách Chessboard: max(|Δx|, |Δy|) = 1

### 2.3. m-Connectivity (m-kết nối)

**Định nghĩa**: Pixel p và q là m-connected nếu:
1. q ∈ N₄(p), HOẶC
2. q ∈ N_D(p) VÀ N₄(p) ∩ N₄(q) không chứa pixel cùng giá trị

**Mục đích**: Tránh hiện tượng "xuyên tường" khi dùng 8-connectivity

**Ví dụ**:
```
1 0 1
0 1 0
1 0 1
```
- 8-connectivity: 4 pixel góc (1) kết nối qua pixel trung tâm
- m-connectivity: 4 pixel góc KHÔNG kết nối (tránh xuyên qua pixel 0)

## 3. Khoảng cách (Distance Metrics)

### 3.1. Euclidean Distance
```
D_E = √((x₁-x₂)² + (y₁-y₂)²)
```

**Đặc điểm**:
- Khoảng cách thực tế, hình học
- Không phụ thuộc connectivity
- Có thể là số thập phân

### 3.2. Manhattan Distance (City-block)
```
D_4 = |x₁-x₂| + |y₁-y₂|
```

**Đặc điểm**:
- Tương ứng với 4-connectivity
- Số bước tối thiểu khi đi thẳng
- Luôn là số nguyên

**Ví dụ**: Từ (0,0) đến (3,4)
```
D_4 = |3-0| + |4-0| = 7 bước
```

### 3.3. Chessboard Distance
```
D_8 = max(|x₁-x₂|, |y₁-y₂|)
```

**Đặc điểm**:
- Tương ứng với 8-connectivity
- Số bước tối thiểu khi đi cả chéo
- Luôn là số nguyên

**Ví dụ**: Từ (0,0) đến (3,4)
```
D_8 = max(3, 4) = 4 bước
```

### 3.4. So sánh
Với 2 điểm p₁=(0,0) và p₂=(3,4):
- D_E = √(9+16) = 5.0
- D_4 = 7
- D_8 = 4

**Bất đẳng thức**:
```
D_8 ≤ D_E ≤ D_4
```

## 4. Đường đi (Paths)

### 4.1. Định nghĩa
Đường đi từ p đến q là chuỗi pixel riêng biệt:
```
{p = p₀, p₁, p₂, ..., p_n = q}
```
trong đó p_i và p_{i+1} là neighbors.

### 4.2. Độ dài đường đi
- **4-path**: Số bước với 4-connectivity
- **8-path**: Số bước với 8-connectivity

### 4.3. Đường đi ngắn nhất
- **4-connected**: Độ dài = D_4
- **8-connected**: Độ dài = D_8

## 5. Vùng liên thông (Connected Components)

### 5.1. Định nghĩa
Tập S là **connected** nếu tồn tại đường đi giữa mọi cặp pixel trong S.

### 5.2. Thành phần liên thông
**Connected Component**: Tập con liên thông cực đại của ảnh nhị phân.

**Ứng dụng**:
- Đếm số đối tượng
- Phân tích hình dạng
- OCR (nhận dạng ký tự)

### 5.3. Ảnh hưởng của connectivity

**Ví dụ**:
```
1 0 1
0 1 0
1 0 1
```

- **4-connectivity**: 5 components (4 góc + 1 trung tâm)
- **8-connectivity**: 1 component (tất cả kết nối)

## 6. Thuật toán BFS/DFS với connectivity

### 6.1. BFS (Breadth-First Search)
```python
def bfs_4connected(grid, start):
    queue = deque([start])
    visited = {start}
    neighbors_4 = [(0,1), (0,-1), (1,0), (-1,0)]

    while queue:
        x, y = queue.popleft()
        for dx, dy in neighbors_4:
            nx, ny = x+dx, y+dy
            if valid(nx, ny) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
```

### 6.2. BFS với 8-connectivity
```python
neighbors_8 = [(0,1), (0,-1), (1,0), (-1,0),
               (1,1), (1,-1), (-1,1), (-1,-1)]
```

## 7. Ứng dụng thực tế

### 7.1. OCR (Optical Character Recognition)
- Dùng 8-connectivity để nhóm pixel thành ký tự
- Phân tích connected components
- Tách các ký tự riêng biệt

### 7.2. Robot Navigation
- **4-connectivity**: Robot chỉ đi thẳng (robot đơn giản)
- **8-connectivity**: Robot đi cả chéo (robot linh hoạt)
- **m-connectivity**: Tránh "xuyên" qua góc

### 7.3. Medical Imaging
- Phân đoạn cơ quan
- Dùng 8-connectivity cho vùng liên tục
- Đo kích thước vùng bệnh lý

### 7.4. Circuit Board Inspection
- Kiểm tra mạch in
- 4-connectivity: Phát hiện đứt mạch nghiêm ngặt
- 8-connectivity: Cho phép kết nối chéo

## 8. Paradox trong connectivity

### 8.1. Jordan Curve Theorem Problem
Với ảnh nhị phân:
- Nếu foreground dùng 4-connectivity
- Thì background phải dùng 8-connectivity (và ngược lại)

**Lý do**: Tránh mâu thuẫn topology.

**Ví dụ**:
```
0 1 0
1 0 1
0 1 0
```
Nếu cả foreground (1) và background (0) đều dùng 4-connectivity:
- 4 pixel (1) tạo 4 components riêng
- Nhưng cũng tạo thành 1 vòng kín
- → Mâu thuẫn!

## 9. Lựa chọn connectivity

| Trường hợp | Connectivity | Lý do |
|------------|--------------|-------|
| Văn bản OCR | 8 | Chữ có nét chéo |
| Mạch in | 4 | Tránh ngắn mạch qua góc |
| Biên đường | 8 | Đường có thể chéo |
| Grid game | 4 | Chỉ đi thẳng |
| Pathfinding | 8 | Đường đi ngắn hơn |
| Flood fill | 8 | Tô đầy đủ vùng |

## 10. Code examples

### 10.1. Kiểm tra connectivity
```python
def is_4_connected(p1, p2):
    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1])
    return (dx + dy) == 1

def is_8_connected(p1, p2):
    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1])
    return max(dx, dy) == 1
```

### 10.2. Đếm connected components
```python
def count_components(binary_img, connectivity=8):
    num_labels, labels = cv2.connectedComponents(
        binary_img,
        connectivity=connectivity
    )
    return num_labels - 1  # Trừ background
```

## 11. Tóm tắt

| Connectivity | Láng giềng | Distance | Số bước | Ứng dụng |
|--------------|-----------|----------|---------|----------|
| 4-connected | 4 | Manhattan | Nhiều hơn | Robot đơn giản, Grid |
| 8-connected | 8 | Chessboard | Ít hơn | Pathfinding, OCR |
| m-connected | 4-8 | - | Trung bình | Tránh ambiguity |

**Key Points**:
- 4-connectivity: Chặt chẽ, ít ambiguity
- 8-connectivity: Linh hoạt, đường đi ngắn
- m-connectivity: Cân bằng, tránh paradox

---

**References**:
- Gonzalez & Woods - Digital Image Processing (Chapter 2.5)
- Rosenfeld & Pfaltz - "Sequential Operations in Digital Picture Processing"
