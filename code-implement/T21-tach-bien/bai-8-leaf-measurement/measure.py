"""
Bài 8 — Tách biên lá cây và đo chu vi/diện tích + "độ răng cưa"

Mục tiêu:
- Edge → contour → polygon approx
- Tính diện tích, chu vi, và chỉ số "răng cưa" (perimeter²/(4π·area))
- Ứng dụng hình học ảnh

Kỹ thuật sử dụng:
- Gaussian blur
- Canny edge detection
- Contour detection
- Geometric measurements
- Serration index (chỉ số răng cưa)

Input:
- Ảnh một chiếc lá trên nền tương phản
- File: leaf.jpg
- (Tuỳ chọn) DPI hoặc thước chuẩn để đổi sang mm

Output:
- Ảnh với contour lá và các số đo
- Thống kê hình học
- Lưu tại: ../output/leaf_metrics.jpg

Tác giả đề bài: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
import math
import os

if __name__ == "__main__":
    # Thiết lập đường dẫn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "leaf.jpg")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")

        # Tạo ảnh nền
        img = np.ones((600, 800, 3), dtype=np.uint8) * 220

        # Vẽ lá (hình ellipse với răng cưa)
        leaf_mask = np.zeros((600, 800), dtype=np.uint8)

        # Tạo hình lá cơ bản (ellipse)
        center = (400, 300)
        axes = (180, 280)
        cv2.ellipse(leaf_mask, center, axes, 0, 0, 360, 255, -1)

        # Thêm răng cưa ở viền
        contours, _ = cv2.findContours(leaf_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            cnt = contours[0]
            # Tạo răng cưa bằng cách làm gồ ghề contour
            new_cnt = []
            for i, pt in enumerate(cnt):
                new_cnt.append(pt)
                if i % 15 == 0:  # Mỗi 15 điểm thêm một răng
                    # Tính vector pháp tuyến
                    x, y = pt[0]
                    dx = x - center[0]
                    dy = y - center[1]
                    norm = math.sqrt(dx*dx + dy*dy)
                    if norm > 0:
                        # Đẩy ra ngoài
                        nx = int(x + dx/norm * 15)
                        ny = int(y + dy/norm * 15)
                        new_cnt.append(np.array([[nx, ny]]))

            new_cnt = np.array(new_cnt)
            leaf_mask = np.zeros((600, 800), dtype=np.uint8)
            cv2.drawContours(leaf_mask, [new_cnt], -1, 255, -1)

        # Màu lá xanh
        img[leaf_mask > 0] = [60, 180, 80]

        # Vẽ gân lá
        cv2.line(img, (400, 50), (400, 550), (40, 140, 50), 3)

        # Gân phụ
        for i in range(8):
            y = 100 + i * 60
            if i % 2 == 0:
                cv2.line(img, (400, y), (320, y + 40), (40, 140, 50), 1)
                cv2.line(img, (400, y), (480, y + 40), (40, 140, 50), 1)
            else:
                cv2.line(img, (400, y), (330, y + 30), (40, 140, 50), 1)
                cv2.line(img, (400, y), (470, y + 30), (40, 140, 50), 1)

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Đọc ảnh
    img = cv2.imread(input_path)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    print("="*80)
    print("BÀI 8: TÁCH BIÊN LÁ CÂY VÀ ĐO CHU VI/DIỆN TÍCH")
    print("="*80)
    print(f"Ảnh gốc: {img.shape}")

    # Chuyển sang grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"\n1. Đã chuyển sang grayscale")

    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (7, 7), 1.5)
    print(f"2. Đã áp dụng Gaussian blur (σ=1.5)")

    # Canny edge detection
    edges = cv2.Canny(blur, 60, 150)
    print(f"3. Đã phát hiện biên bằng Canny (ngưỡng: 60, 150)")

    # Lưu edges
    edges_path = os.path.join(output_dir, 'leaf_edges.png')
    cv2.imwrite(edges_path, edges)

    # Tìm contours
    cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"4. Tìm thấy {len(cnts)} contours")

    # Lấy contour lớn nhất (lá cây)
    cnt = max(cnts, key=cv2.contourArea)
    print(f"5. Chọn contour lớn nhất (lá cây)")

    # Tính các đại lượng hình học
    area = cv2.contourArea(cnt)
    peri = cv2.arcLength(cnt, True)

    # Chỉ số răng cưa: S = P² / (4π·A)
    # Vòng tròn hoàn hảo: S = 1
    # Càng nhiều răng cưa, S càng lớn
    serration = (peri ** 2) / (4 * math.pi * area + 1e-6)

    print(f"\n6. Các đại lượng hình học:")
    print(f"   - Diện tích (Area): {area:.1f} px²")
    print(f"   - Chu vi (Perimeter): {peri:.1f} px")
    print(f"   - Chỉ số răng cưa (Serration): {serration:.3f}")

    # Giải thích chỉ số răng cưa
    if serration < 1.2:
        shape_desc = "gần tròn/trơn"
    elif serration < 2.0:
        shape_desc = "răng cưa nhẹ"
    elif serration < 3.0:
        shape_desc = "răng cưa trung bình"
    else:
        shape_desc = "răng cưa mạnh"

    print(f"   → Hình dạng: {shape_desc}")

    # Các đại lượng bổ sung
    # Bounding box
    x, y, w, h = cv2.boundingRect(cnt)
    aspect_ratio = float(w) / h
    print(f"   - Bounding box: {w}×{h} px")
    print(f"   - Aspect ratio (W/H): {aspect_ratio:.3f}")

    # Extent (tỷ lệ lấp đầy bounding box)
    rect_area = w * h
    extent = float(area) / rect_area
    print(f"   - Extent (area/rect_area): {extent:.3f}")

    # Solidity (tỷ lệ lấp đầy convex hull)
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    solidity = float(area) / hull_area if hull_area > 0 else 0
    print(f"   - Solidity (area/hull_area): {solidity:.3f}")

    # Convexity defects (độ lõm)
    hull_indices = cv2.convexHull(cnt, returnPoints=False)
    if len(hull_indices) > 3 and len(cnt) > 3:
        try:
            defects = cv2.convexityDefects(cnt, hull_indices)
            if defects is not None:
                num_defects = len(defects)
                print(f"   - Số điểm lõm (convexity defects): {num_defects}")
        except:
            print(f"   - Không tính được convexity defects")

    # Tạo ảnh kết quả
    out = img.copy()

    # Vẽ contour (màu xanh lá)
    cv2.drawContours(out, [cnt], -1, (0, 255, 0), 2)

    # Vẽ convex hull (màu xanh dương)
    cv2.drawContours(out, [hull], -1, (255, 0, 0), 2)

    # Vẽ bounding box (màu đỏ)
    cv2.rectangle(out, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Thêm text thông tin
    info_y = 30
    cv2.putText(out, f"Area={area:.1f} px^2, Peri={peri:.1f} px",
               (20, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    info_y += 30
    cv2.putText(out, f"Serration={serration:.3f} ({shape_desc})",
               (20, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    info_y += 30
    cv2.putText(out, f"Aspect={aspect_ratio:.2f}, Extent={extent:.2f}, Solidity={solidity:.2f}",
               (20, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Lưu kết quả
    output_path = os.path.join(output_dir, 'leaf_metrics.jpg')
    cv2.imwrite(output_path, out)

    # Tạo visualization chi tiết hơn
    vis = np.zeros_like(img)
    cv2.drawContours(vis, [cnt], -1, (0, 255, 0), 1)
    cv2.drawContours(vis, [hull], -1, (255, 0, 0), 1)

    vis_path = os.path.join(output_dir, 'leaf_contours.jpg')
    cv2.imwrite(vis_path, vis)

    print("\n" + "="*80)
    print("PHÂN TÍCH HÌNH DẠNG LÁ")
    print("="*80)

    # Phân tích dựa trên các chỉ số
    print(f"\n1. Hình dạng tổng thể:")
    if aspect_ratio < 0.7:
        print(f"   → Lá hình dài (chiều cao > chiều rộng)")
    elif aspect_ratio > 1.3:
        print(f"   → Lá hình rộng (chiều rộng > chiều cao)")
    else:
        print(f"   → Lá cân đối")

    print(f"\n2. Độ lấp đầy:")
    if extent > 0.7:
        print(f"   → Lá lấp đầy bounding box tốt (hình chữ nhật)")
    else:
        print(f"   → Lá có nhiều phần lõm/lồi")

    print(f"\n3. Độ lồi:")
    if solidity > 0.9:
        print(f"   → Viền lá gần như không có lõm sâu")
    elif solidity > 0.7:
        print(f"   → Viền lá có lõm nhẹ")
    else:
        print(f"   → Viền lá có nhiều lõm sâu")

    print(f"\n4. Độ phức tạp viền:")
    if serration < 1.5:
        print(f"   → Viền lá trơn, ít răng cưa")
    elif serration < 2.5:
        print(f"   → Viền lá có răng cưa vừa phải")
    else:
        print(f"   → Viền lá răng cưa mạnh, phức tạp")

    print(f"\nĐã lưu:")
    print(f"  - Ảnh kết quả: {output_path}")
    print(f"  - Ảnh edges: {edges_path}")
    print(f"  - Ảnh contours: {vis_path}")
    print("\nHoàn thành!")
