"""
=============================================================================
BÀI 6: REGION GROWING (LAN TỎA VÙNG) TỪ HẠT GIỐNG
=============================================================================
Đề bài: Tách tổn thương trên ảnh siêu âm/CT vùng có mức xám tương đồng quanh "hạt giống" do bác sĩ chỉ định.
Mục tiêu: Cài đặt region growing 8-lân cận với ngưỡng sai khác cục bộ |I(p)−I(seed)| < τ.
Yêu cầu: Hỗ trợ nhiều seed; dừng khi không thể lan.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T79-99 Phân vùng ảnh (trang 11-12)
=============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import deque


def region_growing(gray, seeds, tau=5):
    """
    Thuật toán Region Growing với 8-láng giềng.

    Args:
        gray: Ảnh xám đầu vào
        seeds: List các điểm giống [(y1, x1), (y2, x2), ...]
        tau: Ngưỡng sai khác cho phép

    Returns:
        out: Ảnh nhị phân vùng đã lan tỏa
    """
    H, W = gray.shape
    visited = np.zeros_like(gray, np.uint8)
    out = np.zeros_like(gray, np.uint8)

    # 8 hướng láng giềng
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    q = deque()

    # Khởi tạo với các seed
    for sy, sx in seeds:
        if 0 <= sy < H and 0 <= sx < W:
            q.append((sy, sx))
            visited[sy, sx] = 1
            out[sy, sx] = 255

    # BFS lan tỏa
    iterations = 0
    while q:
        y, x = q.popleft()
        iterations += 1

        for dy, dx in dirs:
            ny, nx = y + dy, x + dx

            if 0 <= ny < H and 0 <= nx < W and not visited[ny, nx]:
                # Kiểm tra điều kiện tương đồng
                if abs(int(gray[ny, nx]) - int(gray[y, x])) <= tau:
                    visited[ny, nx] = 1
                    out[ny, nx] = 255
                    q.append((ny, nx))

    return out, iterations


def create_sample_image():
    """Tạo ảnh mẫu siêu âm với tổn thương."""
    img = np.ones((400, 500, 3), dtype=np.uint8) * 100

    # Nền với gradient
    for y in range(400):
        for x in range(500):
            val = 100 + int(np.sin(y/30) * 15 + np.cos(x/40) * 15)
            img[y, x] = [val, val, val]

    # Vùng tổn thương (sáng hơn)
    center_y, center_x = 200, 250
    radius = 60

    for y in range(400):
        for x in range(500):
            dist = np.sqrt((y - center_y)**2 + (x - center_x)**2)
            if dist < radius:
                intensity = 140 + int((radius - dist) / radius * 30)
                img[y, x] = [intensity, intensity, intensity]

    # Thêm tổn thương nhỏ
    cv2.circle(img, (150, 120), 25, (155, 155, 155), -1)
    cv2.circle(img, (380, 300), 30, (150, 150, 150), -1)

    # Thêm nhiễu
    noise = np.random.normal(0, 8, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    return img


def main():
    # Kiểm tra ảnh input
    input_path = "../input/ultrasound.png"

    if os.path.exists(input_path):
        print("Đang đọc ảnh từ:", input_path)
        img = cv2.imread(input_path)
    else:
        print("Không tìm thấy ảnh input, tạo ảnh mẫu...")
        img = create_sample_image()
        os.makedirs("../input", exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Chuyển sang ảnh xám
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print("\n" + "="*60)
    print("REGION GROWING - LAN TỎA VÙNG")
    print("="*60)

    # Tham số
    tau = 6  # Ngưỡng sai khác
    seeds = [(200, 250), (120, 150), (300, 380)]  # Điểm giống (y, x)

    print(f"\nTham số:")
    print(f"  - Ngưỡng tau (τ): {tau}")
    print(f"  - Số điểm giống: {len(seeds)}")
    print(f"  - Tọa độ điểm giống (y, x):")
    for i, (sy, sx) in enumerate(seeds, 1):
        if 0 <= sy < gray.shape[0] and 0 <= sx < gray.shape[1]:
            print(f"    {i}. ({sy}, {sx}) - Intensity: {gray[sy, sx]}")

    # Áp dụng Region Growing
    print("\nBắt đầu lan tỏa vùng...")
    mask, iterations = region_growing(gray, seeds, tau=tau)

    # Thống kê
    region_pixels = np.sum(mask == 255)
    total_pixels = gray.size

    print(f"\nKết quả:")
    print(f"  - Số vòng lặp: {iterations}")
    print(f"  - Diện tích vùng: {region_pixels} pixels ({100*region_pixels/total_pixels:.2f}%)")

    if region_pixels > 0:
        region_mean = np.mean(gray[mask == 255])
        region_std = np.std(gray[mask == 255])
        print(f"  - Độ sáng TB vùng: {region_mean:.2f}")
        print(f"  - Độ lệch chuẩn: {region_std:.2f}")

    # Vẽ seed points và vùng lên ảnh
    img_with_seeds = img.copy()
    for sy, sx in seeds:
        if 0 <= sy < gray.shape[0] and 0 <= sx < gray.shape[1]:
            cv2.circle(img_with_seeds, (sx, sy), 5, (0, 0, 255), -1)
            cv2.circle(img_with_seeds, (sx, sy), 7, (255, 255, 255), 2)

    # Overlay mask
    overlay = img.copy()
    overlay[mask > 0] = [0, 255, 0]
    result = cv2.addWeighted(img, 0.6, overlay, 0.4, 0)

    # Vẽ seed lên result
    for sy, sx in seeds:
        if 0 <= sy < gray.shape[0] and 0 <= sx < gray.shape[1]:
            cv2.circle(result, (sx, sy), 5, (0, 0, 255), -1)
            cv2.circle(result, (sx, sy), 7, (255, 255, 255), 2)

    # Tìm contour của vùng
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = img.copy()
    cv2.drawContours(img_contours, contours, -1, (0, 255, 255), 2)

    # Hiển thị kết quả
    plt.figure(figsize=(14, 10))

    plt.subplot(3, 3, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Ảnh gốc", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 2)
    plt.imshow(gray, cmap='gray')
    plt.title("Ảnh xám", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 3)
    plt.imshow(cv2.cvtColor(img_with_seeds, cv2.COLOR_BGR2RGB))
    plt.title(f"Điểm giống (seeds)\n{len(seeds)} điểm",
              fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 4)
    plt.imshow(mask, cmap='gray')
    plt.title(f"Region Growing\n(τ={tau})",
              fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 5)
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title(f"Overlay vùng\n({region_pixels} pixels)",
              fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 6)
    plt.imshow(cv2.cvtColor(img_contours, cv2.COLOR_BGR2RGB))
    plt.title("Contours vùng", fontsize=12, fontweight='bold')
    plt.axis('off')

    # Histogram ảnh xám
    plt.subplot(3, 3, 7)
    plt.hist(gray.ravel(), 256, [0, 256], color='steelblue', alpha=0.7)
    if region_pixels > 0:
        plt.hist(gray[mask == 255], 50, color='green', alpha=0.7, label='Vùng phát hiện')
    plt.title("Histogram", fontsize=12, fontweight='bold')
    plt.xlabel("Mức xám")
    plt.ylabel("Tần suất")
    plt.legend()
    plt.grid(alpha=0.3)

    # Test với tau khác
    plt.subplot(3, 3, 8)
    mask_small, _ = region_growing(gray, seeds, tau=3)
    plt.imshow(mask_small, cmap='gray')
    plt.title(f"Region Growing (τ=3)\n({np.sum(mask_small==255)} pixels)",
              fontsize=11, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 9)
    mask_large, _ = region_growing(gray, seeds, tau=10)
    plt.imshow(mask_large, cmap='gray')
    plt.title(f"Region Growing (τ=10)\n({np.sum(mask_large==255)} pixels)",
              fontsize=11, fontweight='bold')
    plt.axis('off')

    plt.tight_layout()

    # Lưu kết quả
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "region_growing_result.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nĐã lưu kết quả tại: {output_path}")

    plt.show()

    print("\n" + "="*60)
    print("HOÀN THÀNH!")
    print("="*60)


if __name__ == "__main__":
    main()
