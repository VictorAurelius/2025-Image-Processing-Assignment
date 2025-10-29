"""
Bài tập 4 — 4/8/m-kết nối & quãng đường robot dọn lớp học
Bối cảnh: Robot di chuyển trên lưới sàn tránh chướng ngại

Yêu cầu:
- Tính đường đi ngắn nhất từ S đến T với kết nối-4, kết nối-8
- So sánh độ dài quãng đường theo Manhattan và Chessboard

Tác giả: TS. Phan Thanh Toàn
"""

from collections import deque
import numpy as np
import cv2
import os

def neighbors(p, conn='4'):
    """
    Lấy các láng giềng của điểm p

    Args:
        p: Tọa độ (x, y)
        conn: Kiểu kết nối '4' hoặc '8'

    Returns:
        List các điểm láng giềng
    """
    x, y = p
    N4 = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    N8 = N4 + [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
    return N4 if conn=='4' else N8

def shortest_path(grid, s, t, conn='4'):
    """
    Tìm đường đi ngắn nhất bằng BFS

    Args:
        grid: Ma trận lưới (0: trống, 1: vật cản)
        s: Điểm bắt đầu (x, y)
        t: Điểm đích (x, y)
        conn: Kiểu kết nối '4' hoặc '8'

    Returns:
        (path, distance): Đường đi và khoảng cách
    """
    H, W = grid.shape
    INF = 10**9
    dist = np.full((H, W), INF, int)
    prev = np.full((H, W, 2), -1, int)
    dq = deque([s])
    dist[s] = 0

    while dq:
        x, y = dq.popleft()
        if (x, y) == t:
            break
        for nx, ny in neighbors((x, y), conn):
            if 0 <= nx < H and 0 <= ny < W and grid[nx, ny] == 0 and dist[nx, ny] > dist[x, y] + 1:
                dist[nx, ny] = dist[x, y] + 1
                prev[nx, ny] = [x, y]
                dq.append((nx, ny))

    # Truy vết đường đi
    path = []
    if dist[t] < INF:
        cur = t
        while (cur != (-1, -1)) and (cur != tuple(prev[cur][0:0])):
            path.append(cur)
            px, py = prev[cur]
            if px == -1:
                break
            cur = (px, py)
        path.reverse()
    return path, dist[t]

def manhattan_distance(p1, p2):
    """Khoảng cách Manhattan (city-block)"""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def chessboard_distance(p1, p2):
    """Khoảng cách Chessboard"""
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))

def euclidean_distance(p1, p2):
    """Khoảng cách Euclidean"""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def visualize_path(grid, path, s, t, title="Path"):
    """Vẽ đường đi lên ảnh"""
    # Tạo ảnh màu từ grid
    vis = np.zeros((*grid.shape, 3), dtype=np.uint8)
    vis[grid == 0] = [255, 255, 255]  # Trống: trắng
    vis[grid == 1] = [0, 0, 0]         # Vật cản: đen

    # Vẽ đường đi
    for p in path:
        vis[p] = [0, 255, 0]  # Xanh lá

    # Vẽ điểm bắt đầu và kết thúc
    vis[s] = [255, 0, 0]  # Đỏ
    vis[t] = [0, 0, 255]  # Xanh dương

    return vis

if __name__ == "__main__":
    print("="*60)
    print("ROBOT PATHFINDING - KẾT NỐI 4 vs 8")
    print("="*60)

    # Tạo lưới mẫu
    grid = np.zeros((10, 15), int)
    grid[3:7, 8] = 1  # Vật cản dọc

    # Điểm bắt đầu và kết thúc
    s = (0, 0)
    t = (9, 14)

    print(f"\nLưới: {grid.shape}")
    print(f"Điểm bắt đầu (S): {s}")
    print(f"Điểm kết thúc (T): {t}")
    print(f"Số vật cản: {np.sum(grid == 1)}")

    # Khoảng cách lý thuyết
    print(f"\nKhoảng cách lý thuyết:")
    print(f"  Manhattan (city-block): {manhattan_distance(s, t)}")
    print(f"  Chessboard: {chessboard_distance(s, t)}")
    print(f"  Euclidean: {euclidean_distance(s, t):.2f}")

    # Tìm đường đi với các loại kết nối
    results = {}
    for conn in ['4', '8']:
        path, L = shortest_path(grid, s, t, conn)
        results[conn] = (path, L)
        print(f"\n{conn}-connectivity:")
        print(f"  Số bước: {L}")
        print(f"  Độ dài đường đi: {len(path)} điểm")

        # Lưu hình ảnh
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "..", "output")
        os.makedirs(output_dir, exist_ok=True)

        vis = visualize_path(grid, path, s, t, f"{conn}-connectivity")
        # Scale up để dễ nhìn
        vis_scaled = cv2.resize(vis, None, fx=30, fy=30, interpolation=cv2.INTER_NEAREST)
        output_path = os.path.join(output_dir, f"robot_path_{conn}conn.png")
        cv2.imwrite(output_path, vis_scaled)
        print(f"  Đã lưu: {output_path}")

    print("\n" + "="*60)
    print("SO SÁNH & KẾT LUẬN")
    print("="*60)
    print(f"""
4-connectivity:
  - Chỉ di chuyển ngang/dọc (4 hướng)
  - Số bước: {results['4'][1]}
  - Tương ứng với khoảng cách Manhattan

8-connectivity:
  - Di chuyển cả đường chéo (8 hướng)
  - Số bước: {results['8'][1]}
  - Tương ứng với khoảng cách Chessboard
  - Ngắn hơn 4-connectivity vì có thể đi chéo

Trong ứng dụng robot thực tế:
- 4-connectivity: Phù hợp với robot chỉ di chuyển thẳng
- 8-connectivity: Phù hợp với robot có thể xoay tự do
- m-connectivity: Hạn chế đi chéo qua các ô kề nhau (tránh "xuyên tường")
    """)
