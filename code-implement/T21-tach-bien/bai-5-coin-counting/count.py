"""
Bài 5 — Đếm vật tròn (đồng xu/bi) bằng biên Canny + HoughCircles

Mục tiêu:
- Tiền xử lý ánh sáng, cân bằng histogram
- Dùng Canny (hoặc Sobel → Canny) và Hough hình tròn
- Lọc theo bán kính, theo độ tròn

Kỹ thuật sử dụng:
- CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Gaussian blur
- Canny edge detection
- Hough Circle Transform
- Circle detection và visualization

Input:
- Ảnh bàn có nhiều đồng xu/bi tròn
- Chụp từ trên xuống, ít chồng lấn
- File: coins.jpg

Output:
- Ảnh với circles được đánh dấu
- Số lượng vật tròn phát hiện được
- Lưu tại: ../output/coins_detected.jpg

Tác giả đề bài: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
import os

if __name__ == "__main__":
    # Thiết lập đường dẫn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "coins.jpg")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")

        # Tạo ảnh bàn với đồng xu
        img = np.ones((700, 900, 3), dtype=np.uint8) * 150

        # Thêm texture cho bàn
        noise = np.random.normal(0, 10, (700, 900)).astype(np.int16)
        for c in range(3):
            img[:, :, c] = np.clip(img[:, :, c].astype(np.int16) + noise, 0, 255)

        # Vẽ đồng xu (circles với màu vàng/bạc)
        coins = [
            (150, 150, 45, (180, 160, 90)),   # Vàng
            (350, 180, 50, (200, 200, 200)),  # Bạc
            (600, 150, 42, (180, 160, 90)),
            (200, 380, 48, (200, 200, 200)),
            (450, 350, 45, (180, 160, 90)),
            (700, 380, 50, (200, 200, 200)),
            (280, 550, 46, (180, 160, 90)),
            (550, 570, 44, (200, 200, 200)),
        ]

        for x, y, r, color in coins:
            # Vẽ đồng xu với gradient
            for i in range(r, 0, -1):
                brightness = int(255 * (i / r))
                coin_color = tuple(int(c * brightness / 255) for c in color)
                cv2.circle(img, (x, y), i, coin_color, -1)

            # Viền đồng xu
            cv2.circle(img, (x, y), r, (100, 100, 100), 2)

            # Highlight để tạo hiệu ứng 3D
            cv2.circle(img, (x - r//3, y - r//3), r//4, (255, 255, 255), -1, cv2.LINE_AA)

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Đọc ảnh
    img = cv2.imread(input_path)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    print("="*80)
    print("BÀI 5: ĐẾM VẬT TRÒN (ĐỒNG XU/BI) BẰNG HOUGH CIRCLES")
    print("="*80)
    print(f"Ảnh gốc: {img.shape}")

    # Chuyển sang grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"\n1. Đã chuyển sang grayscale")

    # CLAHE để cân bằng sáng
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_img = clahe.apply(gray)
    print(f"2. Đã áp dụng CLAHE (clipLimit=2.0, tileGridSize=8x8)")

    # Gaussian blur
    blur = cv2.GaussianBlur(clahe_img, (7, 7), 1.2)
    print(f"3. Đã áp dụng Gaussian blur (σ=1.2)")

    # Canny edge (để debug)
    edges = cv2.Canny(blur, 80, 160)
    edges_path = os.path.join(output_dir, 'coins_edges.png')
    cv2.imwrite(edges_path, edges)
    print(f"4. Đã phát hiện biên bằng Canny (ngưỡng: 80, 160)")

    # Hough Circles
    print(f"\n5. Đang phát hiện circles bằng Hough Transform...")
    circles = cv2.HoughCircles(
        blur,
        cv2.HOUGH_GRADIENT,
        dp=1.2,              # Độ phân giải accumulator
        minDist=30,          # Khoảng cách tối thiểu giữa các tâm
        param1=120,          # Ngưỡng cao cho Canny
        param2=25,           # Ngưỡng tích lũy (càng thấp càng nhiều circles)
        minRadius=10,        # Bán kính tối thiểu
        maxRadius=80         # Bán kính tối đa
    )

    # Vẽ kết quả
    out = img.copy()
    count = 0

    if circles is not None:
        circles = np.round(circles[0]).astype(int)
        count = len(circles)

        print(f"   ✓ Phát hiện được {count} vật tròn:")

        # Sắp xếp theo tọa độ y để đánh số từ trên xuống
        circles_sorted = sorted(circles, key=lambda c: (c[1], c[0]))

        for idx, (x, y, r) in enumerate(circles_sorted, 1):
            # Vẽ vòng tròn bên ngoài
            cv2.circle(out, (x, y), r, (0, 255, 0), 2)

            # Vẽ tâm
            cv2.circle(out, (x, y), 2, (0, 0, 255), 3)

            # Đánh số
            cv2.putText(out, str(idx), (x - 10, y + 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            print(f"     • Vật #{idx}: tâm=({x},{y}), bán kính={r} pixels")
    else:
        print(f"   ✗ Không phát hiện được vật tròn nào")
        print(f"   → Thử điều chỉnh tham số HoughCircles")

    # Thêm text tổng số lên ảnh
    cv2.putText(out, f"So luong: {count}", (20, 40),
               cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    # Lưu kết quả
    output_path = os.path.join(output_dir, 'coins_detected.jpg')
    cv2.imwrite(output_path, out)

    # Lưu ảnh CLAHE (để debug)
    clahe_path = os.path.join(output_dir, 'coins_clahe.png')
    cv2.imwrite(clahe_path, clahe_img)

    print("\n" + "="*80)
    print("KẾT QUẢ ĐẾM")
    print("="*80)
    print(f"✓ Số lượng vật tròn phát hiện: {count}")

    if count > 0:
        radii = [r for _, _, r in circles[0]]
        avg_radius = np.mean(radii)
        std_radius = np.std(radii)

        print(f"\nThống kê bán kính:")
        print(f"  - Trung bình: {avg_radius:.1f} pixels")
        print(f"  - Độ lệch chuẩn: {std_radius:.1f} pixels")
        print(f"  - Min: {min(radii)} pixels")
        print(f"  - Max: {max(radii)} pixels")

        # Phân loại kích thước
        small = sum(1 for r in radii if r < avg_radius - std_radius)
        medium = sum(1 for r in radii if avg_radius - std_radius <= r <= avg_radius + std_radius)
        large = sum(1 for r in radii if r > avg_radius + std_radius)

        print(f"\nPhân loại kích thước:")
        print(f"  - Nhỏ: {small} vật")
        print(f"  - Trung bình: {medium} vật")
        print(f"  - Lớn: {large} vật")

    print(f"\nĐã lưu:")
    print(f"  - Ảnh kết quả: {output_path}")
    print(f"  - Ảnh CLAHE: {clahe_path}")
    print(f"  - Ảnh edges: {edges_path}")
    print("\nHoàn thành!")
