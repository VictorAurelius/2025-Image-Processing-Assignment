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

## 11. Code Examples Chi Tiết

### 11.1. Connected Components Labeling
```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

def label_connected_components(binary_img, connectivity=8):
    """
    Label connected components trong binary image

    Args:
        binary_img: Binary image (0 or 255)
        connectivity: 4 or 8

    Returns:
        num_labels, labeled_image
    """
    # OpenCV connectedComponents
    num_labels, labels = cv2.connectedComponents(binary_img, connectivity=connectivity)

    # num_labels includes background (label 0)
    # So actual components = num_labels - 1

    return num_labels - 1, labels

def visualize_components(binary_img, connectivity=8):
    """Visualize connected components với màu khác nhau"""
    num_components, labels = label_connected_components(binary_img, connectivity)

    # Create colored label image
    # Random colors for each component
    np.random.seed(42)
    colors = np.random.randint(0, 255, size=(num_components + 1, 3), dtype=np.uint8)
    colors[0] = [0, 0, 0]  # Background = black

    colored_labels = colors[labels]

    # Visualize
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(binary_img, cmap='gray')
    axes[0].set_title('Original Binary Image')
    axes[0].axis('off')

    axes[1].imshow(colored_labels)
    axes[1].set_title(f'{connectivity}-Connected Components\n({num_components} components)')
    axes[1].axis('off')

    # Compare 4 vs 8
    num_comp_4, labels_4 = label_connected_components(binary_img, 4)
    num_comp_8, labels_8 = label_connected_components(binary_img, 8)

    axes[2].text(0.5, 0.7, f'4-connected: {num_comp_4} components',
                ha='center', va='center', fontsize=14, transform=axes[2].transAxes)
    axes[2].text(0.5, 0.3, f'8-connected: {num_comp_8} components',
                ha='center', va='center', fontsize=14, transform=axes[2].transAxes)
    axes[2].axis('off')

    plt.tight_layout()
    plt.savefig('connected_components.png', dpi=150)
    print(f"Found {num_components} components with {connectivity}-connectivity")

# Example
binary = cv2.imread('binary_shapes.png', cv2.IMREAD_GRAYSCALE)
visualize_components(binary, connectivity=8)
```

### 11.2. Pathfinding với Different Connectivity
```python
from collections import deque

def bfs_shortest_path(grid, start, goal, connectivity=4):
    """
    Find shortest path using BFS

    Args:
        grid: 2D binary array (1=walkable, 0=obstacle)
        start: (row, col) starting position
        goal: (row, col) goal position
        connectivity: 4 or 8

    Returns:
        path: List of (row, col) from start to goal, or None
        distance: Path length
    """
    if connectivity == 4:
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    else:  # 8
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0),
                    (1, 1), (1, -1), (-1, 1), (-1, -1)]

    H, W = grid.shape
    visited = set([start])
    queue = deque([(start, [start])])

    while queue:
        (row, col), path = queue.popleft()

        if (row, col) == goal:
            return path, len(path) - 1

        for dr, dc in neighbors:
            nr, nc = row + dr, col + dc

            # Check bounds
            if 0 <= nr < H and 0 <= nc < W:
                # Check walkable and not visited
                if grid[nr, nc] == 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))

    return None, float('inf')  # No path found

# Example: Compare 4 vs 8 connectivity
grid = np.ones((10, 10), dtype=np.uint8)
grid[3:7, 4:6] = 0  # Add obstacle

start = (0, 0)
goal = (9, 9)

path_4, dist_4 = bfs_shortest_path(grid, start, goal, connectivity=4)
path_8, dist_8 = bfs_shortest_path(grid, start, goal, connectivity=8)

print(f"4-connected path length: {dist_4}")
print(f"8-connected path length: {dist_8}")
# 8-connected should be shorter (allows diagonal moves)
```

### 11.3. Distance Transform
```python
def compare_distance_transforms(binary_img):
    """So sánh distance transforms với different metrics"""

    # Distance transforms
    dist_l1 = cv2.distanceTransform(binary_img, cv2.DIST_L1, 3)  # Manhattan
    dist_l2 = cv2.distanceTransform(binary_img, cv2.DIST_L2, 5)  # Euclidean
    dist_c = cv2.distanceTransform(binary_img, cv2.DIST_C, 3)    # Chessboard

    # Normalize for display
    dist_l1_display = cv2.normalize(dist_l1, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    dist_l2_display = cv2.normalize(dist_l2, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    dist_c_display = cv2.normalize(dist_c, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))

    axes[0, 0].imshow(binary_img, cmap='gray')
    axes[0, 0].set_title('Original Binary')

    axes[0, 1].imshow(dist_l1_display, cmap='hot')
    axes[0, 1].set_title('L1 Distance (Manhattan)')

    axes[1, 0].imshow(dist_l2_display, cmap='hot')
    axes[1, 0].set_title('L2 Distance (Euclidean)')

    axes[1, 1].imshow(dist_c_display, cmap='hot')
    axes[1, 1].set_title('Chessboard Distance')

    for ax in axes.flatten():
        ax.axis('off')

    plt.tight_layout()
    plt.savefig('distance_transforms.png', dpi=150)

# compare_distance_transforms(binary_img)
```

## 12. Best Practices

### ✅ Nên làm

1. **Chọn connectivity phù hợp**
   ```python
   # OCR/Text: 8-connected (letters có diagonal strokes)
   num_chars = cv2.connectedComponents(text_binary, connectivity=8)[0] - 1

   # Grid-based games: 4-connected
   path = find_path(grid, start, goal, connectivity=4)
   ```

2. **Jordan Curve rule**
   ```python
   # Foreground 4-connected → Background 8-connected
   num_fg = cv2.connectedComponents(fg, connectivity=4)[0] - 1
   num_bg = cv2.connectedComponents(bg, connectivity=8)[0] - 1
   ```

### ❌ Không nên làm

- Không dùng cả foreground và background cùng connectivity

### 💡 Tips

**Connectivity selection**:
```
Task: Character recognition → 8-connected
Task: Circuit inspection   → 4-connected
Task: Pathfinding          → 8-connected (shorter paths)
Task: Flood fill           → 8-connected (fill complete regions)
```

## 13. Common Pitfalls

### Lỗi 1: Foreground/Background paradox
**Vấn đề**: Dùng cả 2 cùng 4-connected hoặc 8-connected.

**Giải pháp**: FG=4 → BG=8, hoặc FG=8 → BG=4.

### Lỗi 2: Quên diagonal cost
**Vấn đề**: Trong pathfinding, diagonal move có cost √2, không phải 1.

**Giải pháp**: Weighted pathfinding (A*, Dijkstra).

## 14. Bài tập Thực hành

### Bài 1: Implement BFS
Viết BFS với 4-connected và 8-connected, so sánh path length.

### Bài 2: Component Analysis
Đếm số objects trong binary image, lọc theo size.

### Bài 3: Distance Map
Tính distance từ mỗi pixel đến nearest obstacle.

## 15. Tóm tắt

| Connectivity | Láng giềng | Distance | Số bước | Ứng dụng |
|--------------|-----------|----------|---------|----------|
| 4-connected | 4 | Manhattan | Nhiều hơn | Robot đơn giản, Grid |
| 8-connected | 8 | Chessboard | Ít hơn | Pathfinding, OCR |
| m-connected | 4-8 | - | Trung bình | Tránh ambiguity |

**Key Points**:
- 4-connectivity: Chặt chẽ, ít ambiguity
- 8-connectivity: Linh hoạt, đường đi ngắn
- m-connectivity: Cân bằng, tránh paradox

**Key Takeaways**:
1. **4-connected** = 4 neighbors (orthogonal only)
2. **8-connected** = 8 neighbors (include diagonals)
3. **Jordan Curve rule**: FG and BG must use different connectivity
4. **Pathfinding**: 8-connected gives shorter paths
5. **Component counting**: Connectivity affects component count

---

**References**:
- Gonzalez & Woods - Digital Image Processing (Chapter 2.5)
- Rosenfeld & Pfaltz - "Sequential Operations in Digital Picture Processing"
