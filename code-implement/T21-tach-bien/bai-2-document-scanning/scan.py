"""
Bài 2 — Tách biên & tự động "scan phẳng" tài liệu

Mục tiêu:
- Dùng Canny/Sobel để nhấn mạnh cạnh
- Tìm contour lớn nhất, xấp xỉ đa giác, sắp xếp 4 đỉnh
- Sử dụng cv2.getPerspectiveTransform để scan phẳng

Kỹ thuật sử dụng:
- Gaussian blur để giảm nhiễu
- Canny edge detection với ngưỡng tự động (Otsu)
- Morphology operations để liền mảnh cạnh
- Contour detection và polygon approximation
- Perspective transform

Input:
- Ảnh tờ giấy A4 chụp bằng điện thoại (góc nghiêng)
- File: doc.jpg

Output:
- Tài liệu đã được scan phẳng
- Kích thước A4 chuẩn (1240×1754 px)
- Lưu tại: ../output/doc_scanned.jpg

Tác giả đề bài: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
import os

def order_pts(pts):
    """
    Sắp xếp 4 điểm theo thứ tự: Top-Left, Top-Right, Bottom-Right, Bottom-Left

    Args:
        pts: Mảng 4 điểm (4, 2)

    Returns:
        Mảng 4 điểm đã được sắp xếp
    """
    s = pts.sum(axis=1)  # x + y
    diff = np.diff(pts, axis=1)  # x - y

    # Top-left có tổng nhỏ nhất
    tl = pts[np.argmin(s)]

    # Bottom-right có tổng lớn nhất
    br = pts[np.argmax(s)]

    # Top-right có diff nhỏ nhất
    tr = pts[np.argmin(diff)]

    # Bottom-left có diff lớn nhất
    bl = pts[np.argmax(diff)]

    return np.array([tl, tr, br, bl], dtype=np.float32)

if __name__ == "__main__":
    # Thiết lập đường dẫn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "doc.jpg")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")

        # Tạo ảnh giấy A4 nghiêng
        img = np.ones((800, 1000, 3), dtype=np.uint8) * 120

        # Vẽ tờ giấy trắng với góc nghiêng
        pts = np.array([[200, 100], [800, 150], [750, 650], [150, 600]], np.int32)
        cv2.fillPoly(img, [pts], (240, 240, 240))

        # Viền giấy
        cv2.polylines(img, [pts], True, (200, 200, 200), 3)

        # Vẽ text mô phỏng nội dung
        paper_img = np.ones((600, 400, 3), dtype=np.uint8) * 240
        cv2.putText(paper_img, "DOCUMENT", (80, 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (50, 50, 50), 3)
        cv2.rectangle(paper_img, (50, 150), (350, 160), (50, 50, 50), -1)

        for i in range(10):
            y = 200 + i * 30
            cv2.line(paper_img, (50, y), (350, y), (100, 100, 100), 2)

        # Warp text vào vùng giấy
        src_pts = np.array([[0, 0], [400, 0], [400, 600], [0, 600]], np.float32)
        dst_pts = np.array([[200, 100], [800, 150], [750, 650], [150, 600]], np.float32)
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv2.warpPerspective(paper_img, M, (1000, 800))

        # Blend
        mask = cv2.inRange(warped, (230, 230, 230), (255, 255, 255))
        mask_inv = cv2.bitwise_not(mask)
        img_bg = cv2.bitwise_and(img, img, mask=mask)
        warped_fg = cv2.bitwise_and(warped, warped, mask=mask_inv)
        img = cv2.add(img_bg, warped_fg)

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Đọc ảnh
    img = cv2.imread(input_path)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    print("="*80)
    print("BÀI 2: TÁCH BIÊN & TỰ ĐỘNG SCAN PHẲNG TÀI LIỆU")
    print("="*80)
    print(f"Ảnh gốc: {img.shape}")

    # Chuyển sang grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Làm mờ Gaussian nhẹ (σ≈1.2)
    blur = cv2.GaussianBlur(gray, (5, 5), 1.2)
    print(f"\n1. Đã áp dụng Gaussian blur (σ=1.2)")

    # Auto ngưỡng bằng Otsu
    _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(f"2. Ngưỡng Otsu tính được: {_:.1f}")

    # Canny với ngưỡng tự động
    edges = cv2.Canny(blur, th * 0.5, th * 1.5)
    print(f"3. Đã phát hiện biên bằng Canny (ngưỡng: {th*0.5:.1f}, {th*1.5:.1f})")

    # Tìm contours
    cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"4. Tìm thấy {len(cnts)} contours")

    # Lấy contour lớn nhất
    cnt = max(cnts, key=cv2.contourArea)
    area = cv2.contourArea(cnt)
    print(f"5. Contour lớn nhất có diện tích: {area:.0f} pixels")

    # Xấp xỉ đa giác
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
    pts = approx.reshape(-1, 2).astype(np.float32)

    print(f"6. Xấp xỉ đa giác: {len(pts)} đỉnh")

    if len(pts) != 4:
        print(f"\nWARNING: Không tìm được tứ giác tài liệu (tìm được {len(pts)} đỉnh)")
        print("Cố gắng lấy 4 điểm xa nhất...")

        # Fallback: lấy 4 điểm góc từ bounding box xoay
        rect = cv2.minAreaRect(cnt)
        pts = cv2.boxPoints(rect).astype(np.float32)

    # Sắp xếp 4 đỉnh (TL, TR, BR, BL)
    src = order_pts(pts)
    print(f"7. Đã sắp xếp 4 đỉnh:")
    print(f"   Top-Left:     {src[0]}")
    print(f"   Top-Right:    {src[1]}")
    print(f"   Bottom-Right: {src[2]}")
    print(f"   Bottom-Left:  {src[3]}")

    # Kích thước A4 đầu ra (tỉ lệ √2, ví dụ 1240×1754 px)
    w, h = 1240, 1754
    dst = np.array([[0, 0], [w-1, 0], [w-1, h-1], [0, h-1]], np.float32)

    # Tính ma trận perspective transform
    M = cv2.getPerspectiveTransform(src, dst)
    print(f"\n8. Đã tính ma trận perspective transform")

    # Warp perspective
    scan = cv2.warpPerspective(img, M, (w, h))
    print(f"9. Đã warp ảnh về kích thước A4: {w}×{h} pixels")

    # Lưu kết quả
    output_path = os.path.join(output_dir, 'doc_scanned.jpg')
    cv2.imwrite(output_path, scan)

    # Vẽ contour trên ảnh gốc để kiểm tra
    img_debug = img.copy()
    cv2.drawContours(img_debug, [approx], -1, (0, 255, 0), 3)
    for i, pt in enumerate(src.astype(int)):
        cv2.circle(img_debug, tuple(pt), 10, (0, 0, 255), -1)
        cv2.putText(img_debug, str(i+1), tuple(pt + 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    debug_path = os.path.join(output_dir, 'doc_debug.jpg')
    cv2.imwrite(debug_path, img_debug)

    print("\n" + "="*80)
    print("KẾT QUẢ")
    print("="*80)
    print(f"✓ Đã scan phẳng tài liệu thành công")
    print(f"✓ Kích thước đầu ra: {w}×{h} pixels (tỉ lệ A4)")
    print(f"✓ Tài liệu đã được chuẩn hóa về góc nhìn vuông góc")
    print(f"\nĐã lưu:")
    print(f"  - Ảnh scan: {output_path}")
    print(f"  - Ảnh debug: {debug_path}")
    print("\nHoàn thành!")
