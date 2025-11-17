"""
Bài 10 — Tự động "deskew" hoá đơn/biên bản bằng góc biên ưu thế

Mục tiêu:
- Phát hiện biên (Sobel/Canny), dùng Hough Lines để lấy góc chính
- Tính median angle của các line
- Xoay ảnh bù để chuẩn hóa

Kỹ thuật sử dụng:
- Gaussian blur
- Canny edge detection
- Hough Lines Transform
- Angle calculation và median filtering
- Rotation với interpolation

Input:
- Ảnh scan hoá đơn/biên bản bị nghiêng
- File: receipt.jpg

Output:
- Ảnh đã được xoay thẳng (deskewed)
- Góc nghiêng phát hiện được
- Lưu tại: ../output/receipt_deskew.jpg

Tác giả đề bài: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
import math
import os

if __name__ == "__main__":
    # Thiết lập đường dẫn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "receipt.jpg")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")

        # Tạo ảnh hoá đơn thẳng
        img_straight = np.ones((800, 600, 3), dtype=np.uint8) * 255

        # Viền giấy
        cv2.rectangle(img_straight, (50, 50), (550, 750), (200, 200, 200), 2)

        # Header
        cv2.putText(img_straight, "HOA DON BAN HANG", (150, 120),
                   cv2.FONT_HERSHEY_BOLD, 1.2, (0, 0, 0), 2)

        # Đường kẻ ngang
        cv2.line(img_straight, (80, 150), (520, 150), (0, 0, 0), 2)

        # Thông tin cửa hàng
        texts = [
            "Cua hang: ABC Store",
            "Dia chi: 123 Nguyen Trai, Q.1",
            "SDT: 0123-456-789",
            "",
            "--------------------------------",
            "Ten hang       SL    Gia",
            "--------------------------------",
            "Banh mi         2    20,000",
            "Sua tuoi        1    15,000",
            "Nuoc ngot       3    30,000",
            "--------------------------------",
            "Tong cong:           65,000",
            "",
            "Cam on quy khach!",
        ]

        y = 180
        for text in texts:
            if text.startswith("-"):
                cv2.line(img_straight, (80, y), (520, y), (0, 0, 0), 1)
            else:
                cv2.putText(img_straight, text, (100, y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
            y += 35

        # Xoay ảnh để tạo góc nghiêng
        skew_angle = 7.5  # độ
        h, w = img_straight.shape[:2]
        center = (w // 2, h // 2)

        # Ma trận xoay
        M = cv2.getRotationMatrix2D(center, skew_angle, 1.0)

        # Tính kích thước ảnh mới để không bị cắt
        cos = abs(M[0, 0])
        sin = abs(M[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))

        # Điều chỉnh ma trận để căn giữa
        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]

        # Xoay ảnh
        img = cv2.warpAffine(img_straight, M, (new_w, new_h),
                            borderMode=cv2.BORDER_CONSTANT,
                            borderValue=(240, 240, 240))

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu (nghiêng {skew_angle}°) tại: {input_path}")

    # Đọc ảnh
    img = cv2.imread(input_path)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    print("="*80)
    print("BÀI 10: TỰ ĐỘNG DESKEW HOÁ ĐƠN/BIÊN BẢN")
    print("="*80)
    print(f"Ảnh gốc: {img.shape}")

    # Chuyển sang grayscale
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"\n1. Đã chuyển sang grayscale")

    # Gaussian blur
    g = cv2.GaussianBlur(g, (5, 5), 1.2)
    print(f"2. Đã áp dụng Gaussian blur (σ=1.2)")

    # Canny edge detection
    ed = cv2.Canny(g, 60, 180)
    print(f"3. Đã phát hiện biên bằng Canny (ngưỡng: 60, 180)")

    # Lưu edges
    edges_path = os.path.join(output_dir, 'receipt_edges.png')
    cv2.imwrite(edges_path, ed)

    # Hough Lines (dạng (rho, theta))
    print(f"\n4. Đang phát hiện đường thẳng bằng Hough Transform...")
    lines = cv2.HoughLines(ed, 1, np.pi / 180, 150)

    angles = []

    if lines is not None:
        print(f"   ✓ Phát hiện được {len(lines)} đường thẳng")

        for rho, theta in lines[:, 0]:
            # Chuyển theta (radian) về góc độ
            # theta = 0 → đường thẳng đứng (90°)
            # theta = π/2 → đường ngang (0°)
            ang = (theta * 180 / np.pi) - 90  # Chuyển về góc so với trục ngang

            # Chỉ lấy các đường gần ngang (-45° đến +45°)
            if -45 < ang < 45:
                angles.append(ang)

        print(f"   ✓ Lọc được {len(angles)} đường gần ngang")
    else:
        print(f"   ✗ Không phát hiện được đường thẳng")
        angles = [0.0]

    # Tính góc nghiêng (median để robust với outliers)
    skew = np.median(angles) if angles else 0.0

    print(f"\n5. Phân tích góc nghiêng:")
    if len(angles) > 0:
        print(f"   - Số góc phát hiện: {len(angles)}")
        print(f"   - Góc trung bình: {np.mean(angles):.3f}°")
        print(f"   - Góc trung vị (median): {skew:.3f}°")
        print(f"   - Độ lệch chuẩn: {np.std(angles):.3f}°")
        print(f"   - Min: {min(angles):.3f}°, Max: {max(angles):.3f}°")
    else:
        print(f"   - Không có góc hợp lệ")

    print(f"\n6. Góc nghiêng ước tính: {skew:.3f}°")

    if abs(skew) < 0.5:
        print(f"   → Ảnh gần như thẳng, không cần xoay")
    elif abs(skew) < 2.0:
        print(f"   → Nghiêng nhẹ")
    elif abs(skew) < 5.0:
        print(f"   → Nghiêng vừa")
    else:
        print(f"   → Nghiêng mạnh")

    # Xoay ảnh bù
    print(f"\n7. Đang xoay ảnh bù {skew:.3f}°...")

    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)

    # Ma trận xoay
    M = cv2.getRotationMatrix2D(center, skew, 1.0)

    # Warp affine
    deskew = cv2.warpAffine(
        img, M, (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REPLICATE
    )

    print(f"8. ✓ Đã xoay ảnh về đúng phương")

    # Lưu kết quả
    output_path = os.path.join(output_dir, 'receipt_deskew.jpg')
    cv2.imwrite(output_path, deskew)

    # Tạo visualization so sánh
    # Resize nếu ảnh quá lớn
    max_height = 800
    if img.shape[0] > max_height:
        scale = max_height / img.shape[0]
        img_show = cv2.resize(img, None, fx=scale, fy=scale)
        deskew_show = cv2.resize(deskew, None, fx=scale, fy=scale)
    else:
        img_show = img.copy()
        deskew_show = deskew.copy()

    # Thêm text
    cv2.putText(img_show, f"Original (skew: {skew:.2f} deg)", (20, 40),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(deskew_show, "Deskewed", (20, 40),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Ghép nối
    comparison = np.hstack([img_show, deskew_show])
    comparison_path = os.path.join(output_dir, 'receipt_comparison.jpg')
    cv2.imwrite(comparison_path, comparison)

    # Vẽ đường Hough lines lên ảnh gốc
    if lines is not None:
        lines_vis = img.copy()
        for rho, theta in lines[:, 0][:50]:  # Chỉ vẽ 50 đường đầu
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(lines_vis, (x1, y1), (x2, y2), (0, 0, 255), 1)

        lines_path = os.path.join(output_dir, 'receipt_lines.jpg')
        cv2.imwrite(lines_path, lines_vis)
        print(f"9. Đã vẽ visualization các đường Hough")

    print("\n" + "="*80)
    print("KẾT QUẢ DESKEWING")
    print("="*80)
    print(f"\nGóc nghiêng phát hiện: {skew:.3f}°")

    if abs(skew) < 0.5:
        print(f"✓ Ảnh ban đầu đã gần như thẳng")
    else:
        print(f"✓ Đã xoay ảnh {abs(skew):.3f}° để chuẩn hóa")

    print(f"\nChất lượng phát hiện:")
    if len(angles) > 20:
        print(f"  - Rất tốt ({len(angles)} đường thẳng)")
    elif len(angles) > 10:
        print(f"  - Tốt ({len(angles)} đường thẳng)")
    elif len(angles) > 5:
        print(f"  - Chấp nhận được ({len(angles)} đường thẳng)")
    else:
        print(f"  - Cần cải thiện ({len(angles)} đường thẳng)")
        print(f"  → Thử điều chỉnh tham số Canny hoặc HoughLines")

    # Đánh giá độ tin cậy
    if len(angles) > 0:
        std = np.std(angles)
        if std < 1.0:
            reliability = "CAO"
        elif std < 3.0:
            reliability = "TRUNG BÌNH"
        else:
            reliability = "THẤP"

        print(f"\nĐộ tin cậy: {reliability}")
        print(f"  - Độ lệch chuẩn góc: {std:.3f}°")

        if reliability == "THẤP":
            print(f"  ⚠ Cảnh báo: Các đường thẳng có góc phân tán")
            print(f"  → Kết quả deskew có thể không chính xác")

    print(f"\nĐã lưu:")
    print(f"  - Ảnh deskewed: {output_path}")
    print(f"  - So sánh trước/sau: {comparison_path}")
    print(f"  - Ảnh edges: {edges_path}")
    if lines is not None:
        print(f"  - Visualization lines: {lines_path}")
    print("\nHoàn thành!")
