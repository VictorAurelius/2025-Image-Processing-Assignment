"""
Lab 2 — Zooming & Shrinking: nearest/bilinear & pixel replication
Mục tiêu: So sánh nội suy gần nhất, bilinear, pixel replication khi phóng/thu ảnh

Bước làm:
- Phóng ảnh ×1.5 và ×4 (nearest, bilinear, pixel replication)
- Thu ảnh /2 và /4 (nearest, bilinear)
- So sánh PSNR/SSIM giữa ảnh gốc và ảnh sau thu rồi phóng ngược

Tác giả: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os

if __name__ == "__main__":
    # Đường dẫn file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "campus.jpg")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")

        # Tạo ảnh campus mẫu với nhiều chi tiết
        img = np.ones((480, 640), dtype=np.uint8) * 200

        # Vẽ tòa nhà
        cv2.rectangle(img, (100, 150), (250, 400), 100, -1)
        cv2.rectangle(img, (120, 180), (160, 220), 255, -1)  # Cửa sổ
        cv2.rectangle(img, (190, 180), (230, 220), 255, -1)

        # Vẽ cây
        cv2.circle(img, (450, 250), 80, 50, -1)
        cv2.rectangle(img, (440, 250), (460, 400), 80, -1)

        # Vẽ đường
        cv2.rectangle(img, (0, 380), (640, 480), 120, -1)
        cv2.line(img, (0, 430), (640, 430), 255, 2)

        # Thêm text
        cv2.putText(img, "CAMPUS", (280, 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 2, 0, 3)

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Đọc ảnh
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    print("="*70)
    print("LAB 2: ZOOMING & SHRINKING")
    print("="*70)
    print(f"Ảnh gốc: {img.shape}")

    # ========== ZOOMING (Phóng to) ==========
    print("\n" + "="*70)
    print("1. ZOOMING (Phóng to)")
    print("="*70)

    scales = [1.5, 4.0]
    for scale in scales:
        print(f"\n--- Scale ×{scale} ---")

        # Nearest neighbor
        up_near = cv2.resize(img, None, fx=scale, fy=scale,
                            interpolation=cv2.INTER_NEAREST)
        near_path = os.path.join(output_dir, f"zoom_x{scale}_nearest.png")
        cv2.imwrite(near_path, up_near)
        print(f"Nearest: {up_near.shape} → {near_path}")

        # Bilinear
        up_bili = cv2.resize(img, None, fx=scale, fy=scale,
                            interpolation=cv2.INTER_LINEAR)
        bili_path = os.path.join(output_dir, f"zoom_x{scale}_bilinear.png")
        cv2.imwrite(bili_path, up_bili)
        print(f"Bilinear: {up_bili.shape} → {bili_path}")

    # Pixel replication (k=4)
    print(f"\n--- Pixel Replication ×4 ---")
    rep = np.repeat(np.repeat(img, 4, axis=0), 4, axis=1)
    rep_path = os.path.join(output_dir, "zoom_x4_replication.png")
    cv2.imwrite(rep_path, rep)
    print(f"Replication: {rep.shape} → {rep_path}")

    print("""
Nhận xét Zooming:
- Nearest: Hiệu ứng "blocky", gần nhất với pixel gốc
- Bilinear: Mịn hơn, có interpolation tuyến tính
- Replication: Giống Nearest nhưng đơn giản hơn
    """)

    # ========== SHRINKING (Thu nhỏ) ==========
    print("\n" + "="*70)
    print("2. SHRINKING (Thu nhỏ)")
    print("="*70)

    shrink_factors = [2, 4]
    for factor in shrink_factors:
        print(f"\n--- Shrink /{factor} ---")

        fx = fy = 1.0/factor

        # Nearest
        small_near = cv2.resize(img, None, fx=fx, fy=fy,
                               interpolation=cv2.INTER_NEAREST)
        small_near_path = os.path.join(output_dir, f"shrink_div{factor}_nearest.png")
        cv2.imwrite(small_near_path, small_near)
        print(f"Nearest: {small_near.shape} → {small_near_path}")

        # Bilinear
        small_bili = cv2.resize(img, None, fx=fx, fy=fy,
                               interpolation=cv2.INTER_LINEAR)
        small_bili_path = os.path.join(output_dir, f"shrink_div{factor}_bilinear.png")
        cv2.imwrite(small_bili_path, small_bili)
        print(f"Bilinear: {small_bili.shape} → {small_bili_path}")

        # Area (tốt nhất cho shrinking)
        small_area = cv2.resize(img, None, fx=fx, fy=fy,
                               interpolation=cv2.INTER_AREA)
        small_area_path = os.path.join(output_dir, f"shrink_div{factor}_area.png")
        cv2.imwrite(small_area_path, small_area)
        print(f"Area: {small_area.shape} → {small_area_path}")

    # ========== SHRINK & BACK (Đánh giá) ==========
    print("\n" + "="*70)
    print("3. SHRINK → ZOOM BACK (Đánh giá chất lượng)")
    print("="*70)

    methods = [
        ('NEAREST', cv2.INTER_NEAREST),
        ('LINEAR', cv2.INTER_LINEAR),
        ('AREA', cv2.INTER_AREA),
        ('CUBIC', cv2.INTER_CUBIC)
    ]

    print(f"\n{'Method':<15} {'PSNR (dB)':<12} {'SSIM':<10}")
    print("-"*40)

    for name, method in methods:
        # Thu nhỏ /2
        small = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=method)

        # Phóng to về kích thước ban đầu
        back = cv2.resize(small, (img.shape[1], img.shape[0]), interpolation=method)

        # Tính metrics
        psnr_val = cv2.PSNR(img, back)
        ssim_val = ssim(img, back, data_range=255)

        print(f"{name:<15} {psnr_val:<12.2f} {ssim_val:<10.4f}")

        # Lưu kết quả
        back_path = os.path.join(output_dir, f"shrink_back_{name.lower()}.png")
        cv2.imwrite(back_path, back)

    print("\n" + "="*70)
    print("KẾT LUẬN")
    print("="*70)
    print("""
1. Phóng to (Zooming):
   - Nearest: Nhanh nhất, hiệu ứng blocky
   - Bilinear: Mịn hơn, phù hợp cho hầu hết trường hợp
   - Cubic: Mịn nhất, tốn thời gian nhất
   - Replication: Đơn giản, giống Nearest

2. Thu nhỏ (Shrinking):
   - Area: Tốt nhất cho shrinking, giảm aliasing
   - Bilinear: Chấp nhận được
   - Nearest: Có thể bị mất chi tiết

3. Round-trip quality (shrink → zoom back):
   - CUBIC có PSNR và SSIM cao nhất
   - AREA tốt cho shrinking trước
   - NEAREST kém nhất (mất nhiều thông tin)

Khuyến nghị:
- Zooming: INTER_LINEAR hoặc INTER_CUBIC
- Shrinking: INTER_AREA
- Realtime: INTER_NEAREST (nhanh nhất)
    """)
