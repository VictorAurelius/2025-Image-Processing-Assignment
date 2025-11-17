"""
Bài 7 — Phát hiện vết nứt bê tông bằng LoG đa tỉ lệ + skeleton

Mục tiêu:
- Kết hợp Laplacian of Gaussian nhiều σ để bắt vết nứt nhiều bề rộng
- Ngưỡng thích nghi
- Skeletonize để còn 1-pixel

Kỹ thuật sử dụng:
- Laplacian of Gaussian (LoG) với nhiều scales
- Adaptive thresholding
- Morphology operations
- Skeletonization (làm mảnh)

Input:
- Ảnh bề mặt bê tông/asphalt có vết nứt mảnh
- File: surface_crack.jpg

Output:
- Mask vết nứt
- Skeleton (mạng nứt 1-pixel)
- Lưu tại: ../output/crack_*.png

Tác giả đề bài: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
import os
from skimage.morphology import skeletonize

def LoG(f, sigma):
    """
    Tính Laplacian of Gaussian với sigma cho trước

    Args:
        f: Ảnh đầu vào (float32, normalized 0-1)
        sigma: Độ lệch chuẩn của Gaussian

    Returns:
        Trị tuyệt đối của LoG response
    """
    # Kích thước kernel phải lẻ
    k = int(6 * sigma + 1) | 1

    # Gaussian blur
    g = cv2.GaussianBlur(f, (k, k), sigma)

    # Laplacian
    lap = cv2.Laplacian(g, cv2.CV_32F, ksize=3)

    return np.abs(lap)

if __name__ == "__main__":
    # Thiết lập đường dẫn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "surface_crack.jpg")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")

        # Tạo ảnh bê tông với vết nứt
        img = np.ones((600, 800), dtype=np.uint8) * 170

        # Texture bê tông (nhiễu)
        noise = np.random.normal(0, 15, img.shape).astype(np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        # Làm mờ nhẹ
        img = cv2.GaussianBlur(img, (3, 3), 0.5)

        # Vẽ vết nứt chính (đường không đều)
        pts_main = []
        for i in range(20):
            x = 50 + i * 35
            y = 200 + int(50 * np.sin(i * 0.5)) + np.random.randint(-20, 20)
            pts_main.append((x, y))

        for i in range(len(pts_main) - 1):
            cv2.line(img, pts_main[i], pts_main[i+1], 100, 3)

        # Vết nứt phụ (rẽ nhánh)
        branch1 = [(300, 200), (280, 280), (260, 350)]
        for i in range(len(branch1) - 1):
            cv2.line(img, branch1[i], branch1[i+1], 110, 2)

        branch2 = [(500, 200), (520, 120), (550, 80)]
        for i in range(len(branch2) - 1):
            cv2.line(img, branch2[i], branch2[i+1], 105, 2)

        # Vết nứt nhỏ
        cv2.line(img, (100, 400), (200, 450), 115, 1)
        cv2.line(img, (600, 350), (700, 380), 120, 1)

        # Làm mờ vết nứt để tự nhiên hơn
        img = cv2.GaussianBlur(img, (3, 3), 0.3)

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Đọc ảnh grayscale
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    print("="*80)
    print("BÀI 7: PHÁT HIỆN VẾT NỨT BÊ TÔNG BẰNG LOG ĐA TỈ LỆ")
    print("="*80)
    print(f"Ảnh gốc: {img.shape}")

    # Chuẩn hóa về float32 [0, 1]
    imgf = img.astype(np.float32) / 255.0
    print(f"\n1. Đã chuẩn hóa ảnh về float32 [0, 1]")

    # Áp dụng LoG với nhiều scales
    sigmas = [0.8, 1.2, 1.8, 2.4]
    print(f"\n2. Áp dụng Laplacian of Gaussian với nhiều scales:")

    responses = []
    for s in sigmas:
        r = LoG(imgf, s)
        responses.append(r)
        print(f"   - σ={s:.1f}: max response = {r.max():.4f}")

    # Tổng hợp response từ tất cả scales
    resp = sum(responses)
    print(f"\n3. Đã tổng hợp {len(sigmas)} scales")
    print(f"   - Tổng max response: {resp.max():.4f}")

    # Chuẩn hóa về 0-255
    resp = (resp / resp.max() * 255).astype(np.uint8)
    print(f"4. Đã chuẩn hóa về 0-255")

    # Adaptive threshold
    thr = cv2.adaptiveThreshold(
        resp,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        35,    # Block size
        -5     # C constant
    )
    print(f"5. Đã áp dụng adaptive threshold (blockSize=35, C=-5)")

    # Morphology: Open để loại nhiễu
    thr = cv2.morphologyEx(thr, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=1)
    print(f"6. Đã áp dụng morphology OPEN (loại nhiễu)")

    # Skeletonize (làm mảnh về 1-pixel)
    skel = skeletonize((thr > 0).astype(np.uint8)).astype(np.uint8) * 255
    print(f"7. Đã skeletonize (làm mảnh về 1-pixel)")

    # Phân tích kết quả
    crack_pixels = np.sum(thr > 0)
    skel_pixels = np.sum(skel > 0)
    total_pixels = thr.shape[0] * thr.shape[1]

    crack_ratio = (crack_pixels / total_pixels) * 100
    skel_ratio = (skel_pixels / total_pixels) * 100

    print(f"\n8. Thống kê:")
    print(f"   - Pixels vết nứt (mask): {crack_pixels} ({crack_ratio:.3f}%)")
    print(f"   - Pixels skeleton: {skel_pixels} ({skel_ratio:.3f}%)")
    print(f"   - Tổng pixels: {total_pixels}")

    # Tạo overlay
    overlay = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Vẽ mask (màu đỏ, semi-transparent)
    mask_colored = np.zeros_like(overlay)
    mask_colored[thr > 0] = [0, 0, 255]
    overlay = cv2.addWeighted(overlay, 0.7, mask_colored, 0.3, 0)

    # Vẽ skeleton (màu xanh lá)
    overlay[skel > 0] = [0, 255, 0]

    # Lưu kết quả
    mask_path = os.path.join(output_dir, 'crack_mask.png')
    cv2.imwrite(mask_path, thr)

    skel_path = os.path.join(output_dir, 'crack_skeleton.png')
    cv2.imwrite(skel_path, skel)

    overlay_path = os.path.join(output_dir, 'crack_overlay.png')
    cv2.imwrite(overlay_path, overlay)

    # Lưu response (để debug)
    resp_path = os.path.join(output_dir, 'crack_response.png')
    cv2.imwrite(resp_path, resp)

    print("\n" + "="*80)
    print("KẾT QUẢ PHÁT HIỆN VẾT NỨT")
    print("="*80)

    if crack_pixels > 0:
        print(f"⚠ CẢNH BÁO: Phát hiện vết nứt trên bề mặt bê tông")
        print(f"  - Tỷ lệ nứt: {crack_ratio:.3f}% diện tích")
        print(f"  - Độ dài ước tính: ~{skel_pixels} pixels")

        # Phân loại mức độ
        if crack_ratio < 0.5:
            severity = "NHẸ"
        elif crack_ratio < 2.0:
            severity = "TRUNG BÌNH"
        else:
            severity = "NGHIÊM TRỌNG"

        print(f"  - Mức độ: {severity}")

        # Phân tích connected components để đếm số vết nứt
        n_labels, labels = cv2.connectedComponents(skel)
        num_cracks = n_labels - 1  # Trừ background

        print(f"  - Số vết nứt riêng biệt: {num_cracks}")

        if severity in ["TRUNG BÌNH", "NGHIÊM TRỌNG"]:
            print(f"\n  → Cần kiểm tra và sửa chữa!")
    else:
        print(f"✓ Không phát hiện vết nứt")
        print(f"  → Bề mặt bê tông trong tình trạng tốt")

    print(f"\nĐã lưu:")
    print(f"  - Mask vết nứt: {mask_path}")
    print(f"  - Skeleton (1-pixel): {skel_path}")
    print(f"  - Overlay: {overlay_path}")
    print(f"  - LoG response: {resp_path}")
    print("\nHoàn thành!")
