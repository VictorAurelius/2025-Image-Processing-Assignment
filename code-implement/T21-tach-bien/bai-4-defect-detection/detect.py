"""
Bài 4 — Kiểm tra lỗi bề mặt (QC) sản phẩm kim loại/nhựa

Mục tiêu:
- Vận dụng toán tử Laplace (đạo hàm bậc 2) để nhấn mạnh điểm đổi cong/biên mảnh
- Chuỗi xử lý: làm trơn → Laplace → |response| → ngưỡng thích nghi → đóng/mở
- Loại bỏ vùng quá nhỏ bằng connected components

Kỹ thuật sử dụng:
- Gaussian blur (σ≈1-2)
- Laplacian filter (đạo hàm bậc 2)
- Otsu thresholding
- Morphology operations (open, close)
- Connected components analysis

Input:
- Ảnh cận cảnh bề mặt sản phẩm (tấm kim loại, vỏ nhựa)
- File: surface.jpg

Output:
- Mask phát hiện lỗi bề mặt (xước/rãnh)
- Overlay hiển thị vị trí lỗi
- Lưu tại: ../output/defect_*.png

Tác giả đề bài: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
import os

if __name__ == "__main__":
    # Thiết lập đường dẫn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "surface.jpg")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")

        # Tạo ảnh bề mặt kim loại với vết xước
        img = np.ones((600, 800), dtype=np.uint8) * 180

        # Thêm texture kim loại (nhiễu nhẹ)
        noise = np.random.normal(0, 8, img.shape).astype(np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        # Vẽ vết xước (đường mảnh, tối hơn)
        cv2.line(img, (100, 150), (700, 200), 120, 2)
        cv2.line(img, (150, 300), (650, 320), 115, 3)
        cv2.line(img, (200, 450), (600, 480), 125, 2)

        # Vẽ vết xước nhỏ
        cv2.line(img, (400, 100), (450, 180), 130, 1)
        cv2.line(img, (300, 500), (280, 560), 135, 1)

        # Vết lõm tròn
        cv2.circle(img, (500, 400), 15, 140, -1)
        cv2.circle(img, (250, 250), 10, 145, -1)

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Đọc ảnh grayscale
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    print("="*80)
    print("BÀI 4: KIỂM TRA LỖI BỀ MẶT (QC) SẢN PHẨM")
    print("="*80)
    print(f"Ảnh gốc: {img.shape}")

    # GaussianBlur (σ≈1.5)
    blur = cv2.GaussianBlur(img, (5, 5), 1.5)
    print(f"\n1. Đã áp dụng Gaussian blur (σ=1.5)")

    # Laplacian (đạo hàm bậc 2)
    lap = cv2.Laplacian(blur, cv2.CV_32F, ksize=3)
    print(f"2. Đã áp dụng Laplacian filter (ksize=3)")

    # Lấy trị tuyệt đối và chuẩn hóa
    resp = np.abs(lap)
    resp = (resp / resp.max() * 255).astype(np.uint8)
    print(f"3. Đã chuẩn hóa response về 0-255")

    # Ngưỡng Otsu
    otsu_thr, mask = cv2.threshold(resp, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(f"4. Đã áp dụng Otsu thresholding (ngưỡng={otsu_thr:.1f})")

    # Morphology: Open để loại nhiễu hạt
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=1)
    print(f"5. Đã áp dụng morphology OPEN (loại nhiễu hạt)")

    # Morphology: Close để nối nét
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8), iterations=1)
    print(f"6. Đã áp dụng morphology CLOSE (nối nét)")

    # Connected components - loại bỏ vùng quá nhỏ
    n, lbl, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    min_area = 30  # pixel tối thiểu

    print(f"\n7. Phân tích connected components:")
    print(f"   - Tìm thấy {n-1} vùng (ngoài background)")
    print(f"   - Diện tích tối thiểu: {min_area} pixels")

    # Tạo mask đã lọc
    keep = np.zeros_like(mask)
    defects = []

    for i in range(1, n):
        area = stats[i, cv2.CC_STAT_AREA]
        if area >= min_area:
            keep[lbl == i] = 255
            x = stats[i, cv2.CC_STAT_LEFT]
            y = stats[i, cv2.CC_STAT_TOP]
            w = stats[i, cv2.CC_STAT_WIDTH]
            h = stats[i, cv2.CC_STAT_HEIGHT]
            defects.append((i, area, x, y, w, h))

    print(f"   - Giữ lại {len(defects)} vùng lỗi hợp lệ:")

    for idx, area, x, y, w, h in defects:
        print(f"     • Lỗi #{idx}: diện tích={area} px², vị trí=({x},{y}), kích thước={w}×{h}")

    # Tạo overlay
    overlay = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Vẽ contours lỗi
    cnts, _ = cv2.findContours(keep, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(overlay, cnts, -1, (0, 0, 255), 2)

    # Vẽ bounding boxes
    for idx, area, x, y, w, h in defects:
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(overlay, f"#{idx}", (x, y - 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Lưu kết quả
    mask_path = os.path.join(output_dir, 'defect_mask.png')
    cv2.imwrite(mask_path, keep)

    overlay_path = os.path.join(output_dir, 'defect_overlay.png')
    cv2.imwrite(overlay_path, overlay)

    # Lưu response (để debug)
    resp_path = os.path.join(output_dir, 'defect_response.png')
    cv2.imwrite(resp_path, resp)

    print("\n" + "="*80)
    print("KẾT QUẢ PHÁT HIỆN LỖI BỀ MẶT")
    print("="*80)

    total_defect_area = sum(area for _, area, _, _, _, _ in defects)
    surface_area = img.shape[0] * img.shape[1]
    defect_ratio = (total_defect_area / surface_area) * 100

    print(f"✓ Tổng số lỗi phát hiện: {len(defects)}")
    print(f"✓ Tổng diện tích lỗi: {total_defect_area} pixels")
    print(f"✓ Tỷ lệ lỗi: {defect_ratio:.4f}% diện tích")

    if len(defects) > 0:
        print(f"\n⚠ CẢNH BÁO: Phát hiện {len(defects)} lỗi bề mặt")
        print(f"  → Sản phẩm KHÔNG ĐẠT chất lượng QC")
    else:
        print(f"\n✓ Không phát hiện lỗi bề mặt")
        print(f"  → Sản phẩm ĐẠT chất lượng QC")

    print(f"\nĐã lưu:")
    print(f"  - Mask lỗi: {mask_path}")
    print(f"  - Overlay: {overlay_path}")
    print(f"  - Response: {resp_path}")
    print("\nHoàn thành!")
