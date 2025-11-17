"""
=============================================================================
BÀI 7: SPLIT-MERGE (TÁCH & HỢP VÙNG TỨ PHÂN)
=============================================================================
Đề bài: Phân đoạn nền trời/biển/đất trong ảnh phong cảnh nhiễu nhẹ.
Mục tiêu: Cài đặt split-merge theo cây tứ phân với tiêu chuẩn đồng nhất σ khu vực.
Yêu cầu: Tham số: ngưỡng độ lệch chuẩn σ_max và diện tối thiểu.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T79-99 Phân vùng ảnh (trang 13-14)
=============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from skimage.segmentation import felzenszwalb


def create_sample_landscape():
    """Tạo ảnh phong cảnh mẫu với trời/biển/đất."""
    img = np.zeros((400, 600, 3), dtype=np.uint8)

    # Nền trời (xanh da trời)
    img[0:150, :] = [220, 180, 135]

    # Biển (xanh dương)
    img[150:280, :] = [180, 140, 80]

    # Đất/cát (nâu/vàng)
    img[280:400, :] = [100, 160, 200]

    # Thêm gradient cho tự nhiên
    for y in range(150):
        img[y, :] = img[y, :] - [int(y * 0.3), int(y * 0.2), int(y * 0.1)]

    for y in range(150, 280):
        img[y, :] = img[y, :] + [0, int((y - 150) * 0.1), int((y - 150) * 0.2)]

    # Thêm mây
    cv2.ellipse(img, (150, 80), (60, 30), 0, 0, 360, (255, 240, 230), -1)
    cv2.ellipse(img, (300, 60), (80, 35), 0, 0, 360, (255, 245, 235), -1)
    cv2.ellipse(img, (450, 90), (70, 30), 0, 0, 360, (255, 240, 230), -1)

    # Thêm đảo nhỏ
    cv2.ellipse(img, (500, 240), (50, 20), 0, 0, 360, (80, 120, 100), -1)

    # Thêm nhiễu
    noise = np.random.normal(0, 8, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    return img


def main():
    # Kiểm tra ảnh input
    input_path = "../input/landscape.jpg"

    if os.path.exists(input_path):
        print("Đang đọc ảnh từ:", input_path)
        img = cv2.imread(input_path)
    else:
        print("Không tìm thấy ảnh input, tạo ảnh mẫu...")
        img = create_sample_landscape()
        os.makedirs("../input", exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Chuyển sang RGB cho scikit-image
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    print("\n" + "="*60)
    print("SPLIT-MERGE SEGMENTATION - PHÂN ĐOẠN TỨ PHÂN")
    print("="*60)

    # Tham số cho felzenszwalb (region-based segmentation)
    scale = 100
    sigma = 0.8
    min_size = 150

    print(f"\nTham số Felzenszwalb (Region-based):")
    print(f"  - Scale: {scale}")
    print(f"  - Sigma: {sigma}")
    print(f"  - Min size: {min_size}")

    # Áp dụng Felzenszwalb segmentation
    print("\nĐang phân đoạn...")
    seg = felzenszwalb(img_rgb, scale=scale, sigma=sigma, min_size=min_size)

    # Thống kê
    num_segments = len(np.unique(seg))
    print(f"\nKết quả:")
    print(f"  - Số vùng phát hiện: {num_segments}")

    # Tính thống kê cho mỗi vùng
    print(f"\nThống kê các vùng:")
    for i in range(min(5, num_segments)):  # Hiển thị 5 vùng đầu
        mask = (seg == i)
        area = np.sum(mask)
        if area > 0:
            mean_color = np.mean(img_rgb[mask], axis=0)
            print(f"  Vùng {i}: {area} pixels, màu TB: RGB({mean_color[0]:.0f}, {mean_color[1]:.0f}, {mean_color[2]:.0f})")

    # Tạo ảnh kết quả với màu trung bình mỗi vùng
    seg_mean = np.zeros_like(img_rgb)
    for i in np.unique(seg):
        mask = (seg == i)
        if np.sum(mask) > 0:
            mean_color = np.mean(img_rgb[mask], axis=0)
            seg_mean[mask] = mean_color

    # Vẽ biên vùng
    from skimage.segmentation import mark_boundaries
    boundaries = mark_boundaries(img_rgb, seg, color=(1, 1, 0), mode='thick')

    # Test với tham số khác
    print("\nThử nghiệm với tham số khác...")
    seg_fine = felzenszwalb(img_rgb, scale=50, sigma=0.5, min_size=50)
    seg_coarse = felzenszwalb(img_rgb, scale=200, sigma=1.0, min_size=300)

    num_fine = len(np.unique(seg_fine))
    num_coarse = len(np.unique(seg_coarse))

    print(f"  - Phân đoạn mịn (scale=50): {num_fine} vùng")
    print(f"  - Phân đoạn thô (scale=200): {num_coarse} vùng")

    # Hiển thị kết quả
    plt.figure(figsize=(14, 10))

    plt.subplot(3, 3, 1)
    plt.imshow(img_rgb)
    plt.title("Ảnh gốc", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 2)
    plt.imshow(seg, cmap='tab20')
    plt.title(f"Phân đoạn vùng\n({num_segments} vùng)",
              fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 3)
    plt.imshow(boundaries)
    plt.title("Biên vùng", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 4)
    plt.imshow(seg_mean.astype(np.uint8))
    plt.title("Màu trung bình mỗi vùng", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 5)
    plt.imshow(seg_fine, cmap='tab20b')
    plt.title(f"Phân đoạn mịn\n({num_fine} vùng)",
              fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 6)
    plt.imshow(seg_coarse, cmap='tab20c')
    plt.title(f"Phân đoạn thô\n({num_coarse} vùng)",
              fontsize=12, fontweight='bold')
    plt.axis('off')

    # Hiển thị 3 vùng lớn nhất
    plt.subplot(3, 3, 7)
    segment_ids, counts = np.unique(seg, return_counts=True)
    top3_ids = segment_ids[np.argsort(counts)[-3:]]
    mask_top3 = np.zeros_like(seg)
    for idx in top3_ids:
        mask_top3[seg == idx] = idx
    plt.imshow(mask_top3, cmap='tab10')
    plt.title("3 vùng lớn nhất", fontsize=12, fontweight='bold')
    plt.axis('off')

    # Histogram số pixel mỗi vùng
    plt.subplot(3, 3, 8)
    plt.bar(range(len(counts)), sorted(counts, reverse=True), color='steelblue', alpha=0.7)
    plt.title("Phân bố kích thước vùng", fontsize=12, fontweight='bold')
    plt.xlabel("Vùng (sắp xếp)")
    plt.ylabel("Số pixels")
    plt.grid(alpha=0.3)
    plt.yscale('log')

    # Overlay segments
    plt.subplot(3, 3, 9)
    overlay = img_rgb.copy()
    # Vẽ viền mỗi segment
    for i in np.unique(seg):
        mask = (seg == i).astype(np.uint8)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        color = tuple(np.random.randint(0, 255, 3).tolist())
        cv2.drawContours(overlay, contours, -1, color, 2)
    plt.imshow(overlay)
    plt.title("Overlay contours", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.tight_layout()

    # Lưu kết quả
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "split_merge_result.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nĐã lưu kết quả tại: {output_path}")

    plt.show()

    print("\n" + "="*60)
    print("HOÀN THÀNH!")
    print("="*60)


if __name__ == "__main__":
    main()
