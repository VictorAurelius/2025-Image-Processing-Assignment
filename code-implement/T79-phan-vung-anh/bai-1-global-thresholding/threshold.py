"""
=============================================================================
BÀI 1: PHÂN NGƯỠNG TOÀN CỤC (HEURISTIC ITERATIVE THRESHOLD)
=============================================================================
Đề bài: Tách sản phẩm khỏi nền trên ảnh chụp băng chuyền có ánh sáng tương đối đều.
Mục tiêu: Áp dụng thuật toán ngưỡng toàn cục, hội tụ T = (m₁+m₂)/2.
Yêu cầu: Ảnh xám/hoặc RGB (sẽ chuyển xám); báo cáo giá trị ngưỡng và mask nhị phân.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T79-99 Phân vùng ảnh (trang 1-2)
=============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

def global_threshold(gray, eps=1e-3, max_iter=100):
    """
    Thuật toán phân ngưỡng toàn cục lặp.

    Args:
        gray: Ảnh xám đầu vào
        eps: Ngưỡng hội tụ
        max_iter: Số vòng lặp tối đa

    Returns:
        binimg: Ảnh nhị phân sau phân ngưỡng
        T: Giá trị ngưỡng tìm được
    """
    T = float(np.mean(gray))
    for iteration in range(max_iter):
        G1, G2 = gray[gray >= T], gray[gray < T]
        if len(G1) == 0 or len(G2) == 0:
            break
        m1, m2 = float(np.mean(G1)), float(np.mean(G2))
        newT = 0.5 * (m1 + m2)
        if abs(newT - T) <= eps:
            T = newT
            break
        T = newT

    _, binimg = cv2.threshold(gray, T, 255, cv2.THRESH_BINARY)
    return binimg, T


def create_sample_image():
    """Tạo ảnh mẫu băng chuyền với sản phẩm."""
    img = np.ones((400, 600, 3), dtype=np.uint8) * 180  # Nền xám sáng

    # Vẽ băng chuyền
    cv2.rectangle(img, (0, 100), (600, 300), (140, 140, 140), -1)

    # Vẽ các sản phẩm (hộp) màu tối
    boxes = [(100, 130, 150, 180), (220, 150, 270, 200),
             (360, 140, 410, 190), (480, 160, 530, 210)]

    for x1, y1, x2, y2 in boxes:
        cv2.rectangle(img, (x1, y1), (x2, y2), (60, 60, 60), -1)
        cv2.rectangle(img, (x1, y1), (x2, y2), (40, 40, 40), 2)

    return img


def main():
    # Kiểm tra ảnh input
    input_path = "../input/conveyor.jpg"

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

    # Áp dụng phân ngưỡng toàn cục
    print("\n" + "="*60)
    print("PHÂN NGƯỠNG TOÀN CỤC - GLOBAL THRESHOLDING")
    print("="*60)

    binimg, T = global_threshold(gray)

    # Phân tích kết quả
    print(f"\nGiá trị ngưỡng hội tụ: T = {round(T, 2)}")
    print(f"Kích thước ảnh: {gray.shape}")

    num_foreground = np.sum(binimg == 255)
    num_background = np.sum(binimg == 0)
    total_pixels = gray.size

    print(f"\nThống kê phân vùng:")
    print(f"  - Pixel nền (đen): {num_background} ({100*num_background/total_pixels:.1f}%)")
    print(f"  - Pixel vật thể (trắng): {num_foreground} ({100*num_foreground/total_pixels:.1f}%)")

    mean_foreground = np.mean(gray[binimg == 255]) if num_foreground > 0 else 0
    mean_background = np.mean(gray[binimg == 0]) if num_background > 0 else 0

    print(f"\nĐộ sáng trung bình:")
    print(f"  - Vùng nền: {mean_background:.2f}")
    print(f"  - Vùng vật thể: {mean_foreground:.2f}")
    print(f"  - Chênh lệch: {abs(mean_foreground - mean_background):.2f}")

    # Hiển thị kết quả
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Ảnh gốc", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(gray, cmap='gray')
    plt.title("Ảnh xám", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(binimg, cmap='gray')
    plt.title(f"Phân ngưỡng toàn cục\n(T = {round(T, 2)})",
              fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.tight_layout()

    # Lưu kết quả
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "global_threshold_result.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nĐã lưu kết quả tại: {output_path}")

    plt.show()

    print("\n" + "="*60)
    print("HOÀN THÀNH!")
    print("="*60)


if __name__ == "__main__":
    main()
