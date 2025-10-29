"""
Lab 3 — Đo góc, cung tròn, diện tích & ước lượng hình tròn qua 3 điểm
Mục tiêu: Đo góc, cung, diện tích và nội suy đường tròn qua 3 điểm

Bước làm:
- Chọn 3 điểm trên biên → tính tâm O(x,y) và bán kính r
- Suy ra độ dài cung giữa 2 điểm theo r và góc θ
- Phân đoạn đối tượng, dùng contourArea để đo diện tích

Tác giả: TS. Phan Thanh Toàn
"""

import numpy as np
import cv2
import os
import math

def circle_from_3pts(p1, p2, p3):
    """
    Tính tâm và bán kính đường tròn đi qua 3 điểm

    Args:
        p1, p2, p3: Ba điểm (x, y)

    Returns:
        ((ox, oy), r): Tâm và bán kính
    """
    (x1, y1), (x2, y2), (x3, y3) = map(lambda p: (float(p[0]), float(p[1])), [p1, p2, p3])

    # Giải hệ phương trình tuyến tính
    A = np.array([[2*(x2-x1), 2*(y2-y1)],
                  [2*(x3-x1), 2*(y3-y1)]], dtype=np.float64)
    b = np.array([x2**2+y2**2 - x1**2 - y1**2,
                  x3**2+y3**2 - x1**2 - y1**2], dtype=np.float64)

    O = np.linalg.solve(A, b)
    ox, oy = O
    r = np.hypot(ox-x1, oy-y1)

    return (ox, oy), r

def angle_between_points(center, p1, p2):
    """Tính góc giữa 2 điểm qua tâm (radians)"""
    v1 = np.array([p1[0] - center[0], p1[1] - center[1]])
    v2 = np.array([p2[0] - center[0], p2[1] - center[1]])

    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    cos_angle = np.clip(cos_angle, -1, 1)  # Tránh lỗi số học
    angle = np.arccos(cos_angle)

    return angle

def arc_length(r, theta):
    """Tính độ dài cung tròn"""
    return r * theta

def circle_area(r):
    """Tính diện tích hình tròn"""
    return np.pi * r**2

if __name__ == "__main__":
    print("="*70)
    print("LAB 3: ĐO ĐƯỜNG TRÒN QUA 3 ĐIỂM")
    print("="*70)

    # ========== Ví dụ 1: Tính toán lý thuyết ==========
    print("\n1. VÍ DỤ LÝ THUYẾT")
    print("-"*70)

    # 3 điểm mẫu
    p1 = (100, 200)
    p2 = (200, 100)
    p3 = (300, 200)

    print(f"Điểm 1: {p1}")
    print(f"Điểm 2: {p2}")
    print(f"Điểm 3: {p3}")

    # Tính tâm và bán kính
    O, r = circle_from_3pts(p1, p2, p3)
    print(f"\nTâm O: ({O[0]:.2f}, {O[1]:.2f})")
    print(f"Bán kính r: {r:.2f} pixels")

    # Tính góc giữa p1 và p2
    theta12 = angle_between_points(O, p1, p2)
    print(f"\nGóc giữa p1 và p2: {theta12:.4f} rad ({np.degrees(theta12):.2f}°)")

    # Độ dài cung
    arc12 = arc_length(r, theta12)
    print(f"Độ dài cung p1→p2: {arc12:.2f} pixels")

    # Diện tích
    area = circle_area(r)
    print(f"Diện tích hình tròn: {area:.2f} pixels²")

    # ========== Ví dụ 2: Vẽ và đo trên ảnh ==========
    print("\n" + "="*70)
    print("2. VẼ VÀ ĐO TRÊN ẢNH")
    print("-"*70)

    # Tạo ảnh trống
    img = np.ones((600, 800, 3), dtype=np.uint8) * 255

    # Vẽ đường tròn
    center_int = (int(O[0]), int(O[1]))
    radius_int = int(r)

    cv2.circle(img, center_int, radius_int, (0, 0, 255), 2)

    # Vẽ 3 điểm
    for i, p in enumerate([p1, p2, p3], 1):
        cv2.circle(img, p, 5, (255, 0, 0), -1)
        cv2.putText(img, f"P{i}", (p[0]+10, p[1]-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # Vẽ tâm
    cv2.circle(img, center_int, 5, (0, 255, 0), -1)
    cv2.putText(img, "O", (center_int[0]+10, center_int[1]-10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Vẽ bán kính đến p1
    cv2.line(img, center_int, p1, (0, 255, 0), 1)
    cv2.putText(img, f"r={r:.1f}", (center_int[0], center_int[1]+30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Vẽ cung p1→p2
    cv2.line(img, center_int, p1, (255, 0, 255), 1)
    cv2.line(img, center_int, p2, (255, 0, 255), 1)

    # Thêm thông tin
    info = [
        f"Center: ({O[0]:.1f}, {O[1]:.1f})",
        f"Radius: {r:.1f} px",
        f"Angle P1-P2: {np.degrees(theta12):.1f} deg",
        f"Arc length: {arc12:.1f} px",
        f"Circle area: {area:.1f} px^2"
    ]

    y_pos = 30
    for text in info:
        cv2.putText(img, text, (20, y_pos),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        y_pos += 30

    # Lưu ảnh
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "..", "output")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "circle_measurement.png")
    cv2.imwrite(output_path, img)
    print(f"Đã lưu: {output_path}")

    # ========== Ví dụ 3: Đo đối tượng tròn thực tế ==========
    print("\n" + "="*70)
    print("3. ĐO ĐỐI TƯỢNG TRÒN THỰC TẾ")
    print("-"*70)

    # Tạo ảnh với hình tròn
    img2 = np.zeros((600, 800), dtype=np.uint8)
    cv2.circle(img2, (400, 300), 150, 255, -1)

    # Tìm contour
    contours, _ = cv2.findContours(img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        cnt = contours[0]

        # Tính diện tích contour
        area_contour = cv2.contourArea(cnt)

        # Fit circle
        (cx, cy), radius = cv2.minEnclosingCircle(cnt)

        print(f"Đo bằng contour:")
        print(f"  Tâm: ({cx:.2f}, {cy:.2f})")
        print(f"  Bán kính: {radius:.2f} pixels")
        print(f"  Diện tích đo được: {area_contour:.2f} pixels²")
        print(f"  Diện tích lý thuyết: {np.pi * radius**2:.2f} pixels²")
        print(f"  Sai số: {abs(area_contour - np.pi * radius**2):.2f} pixels²")

        # Vẽ kết quả
        img2_color = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        cv2.circle(img2_color, (int(cx), int(cy)), int(radius), (0, 255, 0), 2)
        cv2.circle(img2_color, (int(cx), int(cy)), 5, (0, 0, 255), -1)

        output_path2 = os.path.join(output_dir, "circle_detection.png")
        cv2.imwrite(output_path2, img2_color)
        print(f"\nĐã lưu: {output_path2}")

    # ========== Ví dụ 4: Quy đổi sang đơn vị thực ==========
    print("\n" + "="*70)
    print("4. QUY ĐỔI SANG ĐƠN VỊ THỰC")
    print("-"*70)

    # Giả sử có thước tham chiếu 10cm = 100 pixels
    reference_cm = 10.0  # cm
    reference_px = 100.0  # pixels
    scale_factor = reference_cm / reference_px  # cm/pixel

    print(f"Thước tham chiếu: {reference_cm} cm = {reference_px} pixels")
    print(f"Scale factor: {scale_factor} cm/pixel")

    # Quy đổi
    r_cm = r * scale_factor
    area_cm2 = area * (scale_factor ** 2)
    arc12_cm = arc12 * scale_factor

    print(f"\nQuy đổi ra đơn vị thực:")
    print(f"  Bán kính: {r_cm:.2f} cm")
    print(f"  Diện tích: {area_cm2:.2f} cm²")
    print(f"  Độ dài cung: {arc12_cm:.2f} cm")

    print("\n" + "="*70)
    print("KẾT LUẬN")
    print("="*70)
    print("""
1. Tính toán từ 3 điểm:
   - Dùng giải hệ phương trình tuyến tính
   - Chính xác khi 3 điểm không thẳng hàng

2. Đo góc và cung:
   - Góc: arccos(dot product của 2 vectors)
   - Cung: s = r × θ (θ là radian)

3. Đo diện tích:
   - Lý thuyết: A = π × r²
   - Thực tế: cv2.contourArea()
   - Sai số nhỏ do discretization

4. Quy đổi đơn vị:
   - Cần đối tượng tham chiếu có kích thước biết trước
   - Scale factor = kích_thước_thực / kích_thước_pixel
   - Áp dụng cho tất cả phép đo

Ứng dụng:
- Đo kích thước vật thể trong ảnh
- Kiểm tra chất lượng sản phẩm tròn
- Đo khoảng cách trên ảnh y tế
    """)
