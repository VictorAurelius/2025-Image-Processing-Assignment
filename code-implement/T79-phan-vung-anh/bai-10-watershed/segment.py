"""
=============================================================================
BÀI 10: WATERSHED (THEO MIỀN DỰA TRÊN ĐỊA HÌNH) CHO VẬT THỂ CHẠM NHAU
=============================================================================
Đề bài: Đếm đồng xu/hạt bi dính nhau trên nền tương đối đồng đều.
Mục tiêu: Dùng watershed trên ảnh khoảng cách đã tách "marker" để tách các vật thể chạm.
Yêu cầu: Pipeline: lọc → nhị phân → distanceTransform → tìm peak → watershed.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T79-99 Phân vùng ảnh (trang 19-20)
=============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage.segmentation import watershed


def create_sample_coins():
    """Tạo ảnh mẫu với các đồng xu dính nhau."""
    img = np.ones((400, 600, 3), dtype=np.uint8) * 80  # Nền tối

    # Vẽ các đồng xu (tròn sáng), một số dính nhau
    coins = [
        (100, 100, 40),
        (180, 100, 42),  # Dính với coin trên
        (120, 180, 38),
        (300, 120, 45),
        (380, 130, 40),
        (450, 120, 43),  # Dính với coin bên
        (100, 280, 41),
        (190, 290, 39),  # Dính nhẹ
        (300, 300, 44),
        (400, 280, 42),
        (480, 290, 40),  # Dính với coin bên
        (200, 180, 37)
    ]

    for x, y, r in coins:
        cv2.circle(img, (x, y), r, (200, 200, 200), -1)
        # Thêm hiệu ứng ánh sáng
        cv2.circle(img, (x-10, y-10), int(r*0.3), (230, 230, 230), -1)

    # Thêm nhiễu
    noise = np.random.normal(0, 5, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    return img


def main():
    # Kiểm tra ảnh input
    input_path = "../input/coins.png"

    if os.path.exists(input_path):
        print("Đang đọc ảnh từ:", input_path)
        img = cv2.imread(input_path)
    else:
        print("Không tìm thấy ảnh input, tạo ảnh mẫu...")
        img = create_sample_coins()
        os.makedirs("../input", exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Chuyển sang ảnh xám
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print("\n" + "="*60)
    print("WATERSHED SEGMENTATION - PHÂN ĐOẠN VẬT THỂ CHẠM NHAU")
    print("="*60)

    print(f"\nKích thước ảnh: {gray.shape}")

    # Bước 1: Tiền xử lý - Otsu thresholding
    print("\nBước 1: Phân ngưỡng Otsu...")
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Morphology opening để loại nhiễu
    bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=1)

    # Đếm số pixel vật thể
    obj_pixels = np.sum(bw == 255)
    total_pixels = gray.size
    print(f"  - Pixel vật thể: {obj_pixels} ({100*obj_pixels/total_pixels:.1f}%)")

    # Bước 2: Distance Transform
    print("\nBước 2: Tính Distance Transform...")
    dist = cv2.distanceTransform(bw, cv2.DIST_L2, 5)
    print(f"  - Khoảng cách max: {np.max(dist):.2f}")

    # Bước 3: Tìm peaks (markers)
    print("\nBước 3: Tìm local peaks làm markers...")
    coords = peak_local_max(dist, footprint=np.ones((3, 3)), labels=bw)
    print(f"  - Số peaks tìm được: {len(coords)}")

    mask = np.zeros(dist.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, num_markers = ndi.label(mask)
    print(f"  - Số markers: {num_markers}")

    # Bước 4: Watershed
    print("\nBước 4: Áp dụng Watershed...")
    labels = watershed(-dist, markers, mask=bw.astype(bool))

    num_objects = len(np.unique(labels)) - 1  # Trừ background
    print(f"  - Số vật thể phát hiện: {num_objects}")

    # Thống kê các vật thể
    print(f"\nThống kê vật thể:")
    areas = []
    for i in range(1, num_objects + 1):
        area = np.sum(labels == i)
        areas.append(area)

    if areas:
        print(f"  - Diện tích TB: {np.mean(areas):.0f} pixels")
        print(f"  - Diện tích min/max: {np.min(areas)}/{np.max(areas)}")
        print(f"  - Độ lệch chuẩn: {np.std(areas):.1f}")

    # Vẽ kết quả
    # Tạo ảnh màu cho labels
    label_colored = np.zeros_like(img)
    colors = plt.cm.nipy_spectral(np.linspace(0, 1, num_objects + 1))
    colors = (colors[:, :3] * 255).astype(np.uint8)

    for i in range(1, num_objects + 1):
        label_colored[labels == i] = colors[i]

    # Vẽ biên lên ảnh gốc
    img_with_boundaries = img.copy()
    for i in range(1, num_objects + 1):
        mask = (labels == i).astype(np.uint8)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img_with_boundaries, contours, -1, (0, 255, 0), 2)

        # Đánh số
        if contours:
            M = cv2.moments(contours[0])
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.putText(img_with_boundaries, str(i), (cx-10, cy+5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    # Vẽ markers
    img_markers = img.copy()
    for coord in coords:
        cv2.circle(img_markers, (coord[1], coord[0]), 3, (255, 0, 0), -1)

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
    plt.imshow(bw, cmap='gray')
    plt.title("Otsu threshold", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 4)
    plt.imshow(dist, cmap='jet')
    plt.title("Distance Transform", fontsize=12, fontweight='bold')
    plt.colorbar(fraction=0.046, pad=0.04)
    plt.axis('off')

    plt.subplot(3, 3, 5)
    plt.imshow(cv2.cvtColor(img_markers, cv2.COLOR_BGR2RGB))
    plt.title(f"Markers ({num_markers} peaks)", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 6)
    plt.imshow(labels, cmap='nipy_spectral')
    plt.title(f"Watershed labels\n({num_objects} vật thể)",
              fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 7)
    plt.imshow(cv2.cvtColor(label_colored, cv2.COLOR_BGR2RGB))
    plt.title("Labels (màu)", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 8)
    plt.imshow(cv2.cvtColor(img_with_boundaries, cv2.COLOR_BGR2RGB))
    plt.title("Biên + Đánh số", fontsize=12, fontweight='bold')
    plt.axis('off')

    # Histogram diện tích
    plt.subplot(3, 3, 9)
    if areas:
        plt.hist(areas, bins=15, color='steelblue', alpha=0.7, edgecolor='black')
        plt.axvline(x=np.mean(areas), color='red', linestyle='--',
                   linewidth=2, label=f'TB={np.mean(areas):.0f}')
        plt.title("Phân bố diện tích vật thể", fontsize=12, fontweight='bold')
        plt.xlabel("Diện tích (pixels)")
        plt.ylabel("Tần suất")
        plt.legend()
        plt.grid(alpha=0.3)

    plt.tight_layout()

    # Lưu kết quả
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "watershed_result.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nĐã lưu kết quả tại: {output_path}")

    plt.show()

    # Tạo báo cáo chi tiết
    print("\nBáo cáo chi tiết các vật thể:")
    print("-" * 60)
    print(f"{'ID':<5} {'Diện tích':<12} {'Tọa độ tâm':<20} {'Tỷ lệ %'}")
    print("-" * 60)

    for i in range(1, min(num_objects + 1, 16)):  # Hiển thị tối đa 15 vật thể
        mask = (labels == i).astype(np.uint8)
        area = np.sum(mask)
        percentage = 100 * area / obj_pixels

        # Tìm tâm
        M = cv2.moments(mask)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print(f"{i:<5} {area:<12} ({cx:>3}, {cy:>3}){'':<12} {percentage:>5.1f}%")

    print("-" * 60)

    print("\n" + "="*60)
    print("HOÀN THÀNH!")
    print("="*60)


if __name__ == "__main__":
    main()
