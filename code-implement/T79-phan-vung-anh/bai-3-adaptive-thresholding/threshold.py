"""
=============================================================================
BÀI 3: PHÂN NGƯỠNG THÍCH NGHI (ADAPTIVE THRESHOLDING - MEAN/GAUSSIAN)
=============================================================================
Đề bài: Tách chữ in trên hóa đơn bị bóng/độ sáng không đều.
Mục tiêu: Dùng adaptive threshold (mean/gaussian).
Yêu cầu: Chọn blockSize, C hợp lý; so sánh với Otsu.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T79-99 Phân vùng ảnh (trang 5-6)
=============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def create_sample_receipt():
    """Tạo ảnh mẫu hóa đơn với độ sáng không đều."""
    img = np.ones((500, 600, 3), dtype=np.uint8) * 240

    # Tạo độ sáng không đều (gradient)
    for y in range(500):
        for x in range(600):
            brightness = 240 - int(y * 0.15) + int(np.sin(x/50) * 20)
            brightness = max(180, min(255, brightness))
            img[y, x] = [brightness, brightness, brightness]

    # Vẽ tiêu đề
    cv2.putText(img, "HOA DON BAN HANG", (150, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)

    # Vẽ nội dung hóa đơn
    texts = [
        ("San pham A ......... 100,000 VND", 120),
        ("San pham B ......... 200,000 VND", 170),
        ("San pham C ......... 150,000 VND", 220),
        ("----------------------------", 270),
        ("Tong cong .......... 450,000 VND", 320),
        ("Thue VAT 10% ........ 45,000 VND", 370),
        ("Thanh tien ......... 495,000 VND", 420)
    ]

    for text, y in texts:
        cv2.putText(img, text, (80, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

    return img


def main():
    # Kiểm tra ảnh input
    input_path = "../input/receipt.jpg"

    if os.path.exists(input_path):
        print("Đang đọc ảnh từ:", input_path)
        img = cv2.imread(input_path)
    else:
        print("Không tìm thấy ảnh input, tạo ảnh mẫu...")
        img = create_sample_receipt()
        os.makedirs("../input", exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Chuyển sang ảnh xám
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print("\n" + "="*60)
    print("PHÂN NGƯỠNG THÍCH NGHI - ADAPTIVE THRESHOLDING")
    print("="*60)

    # Tham số
    block_size = 35  # Phải là số lẻ
    C = 7  # Hằng số trừ đi từ mean/gaussian

    print(f"\nTham số:")
    print(f"  - Block size: {block_size}")
    print(f"  - Constant C: {C}")

    # Phân ngưỡng thích nghi MEAN
    bin_mean = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        block_size, C
    )

    # Phân ngưỡng thích nghi GAUSSIAN
    bin_gaus = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        block_size, C
    )

    # Phân ngưỡng Otsu để so sánh
    _, bin_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    print(f"\nThống kê ảnh xám:")
    print(f"  - Độ sáng trung bình: {np.mean(gray):.2f}")
    print(f"  - Độ lệch chuẩn: {np.std(gray):.2f}")
    print(f"  - Min/Max: {np.min(gray)}/{np.max(gray)}")

    # Đếm số pixel văn bản
    text_pixels_mean = np.sum(bin_mean == 0)
    text_pixels_gaus = np.sum(bin_gaus == 0)
    text_pixels_otsu = np.sum(bin_otsu == 0)
    total_pixels = gray.size

    print(f"\nSố pixel văn bản (màu đen):")
    print(f"  - Adaptive MEAN: {text_pixels_mean} ({100*text_pixels_mean/total_pixels:.1f}%)")
    print(f"  - Adaptive GAUSSIAN: {text_pixels_gaus} ({100*text_pixels_gaus/total_pixels:.1f}%)")
    print(f"  - Otsu: {text_pixels_otsu} ({100*text_pixels_otsu/total_pixels:.1f}%)")

    print(f"\nNhận xét:")
    print(f"  - Adaptive threshold thích hợp cho ảnh có độ sáng không đều")
    print(f"  - MEAN: Tính trung bình đơn giản trong block")
    print(f"  - GAUSSIAN: Tính trung bình có trọng số Gaussian, mượt hơn")
    print(f"  - Otsu có thể thất bại với độ sáng không đều")

    # Hiển thị kết quả
    plt.figure(figsize=(12, 10))

    plt.subplot(3, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Ảnh gốc (độ sáng không đều)", fontsize=11, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 2, 2)
    plt.imshow(gray, cmap='gray')
    plt.title("Ảnh xám", fontsize=11, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 2, 3)
    plt.imshow(bin_mean, cmap='gray')
    plt.title(f"Adaptive MEAN\n(blockSize={block_size}, C={C})",
              fontsize=11, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 2, 4)
    plt.imshow(bin_gaus, cmap='gray')
    plt.title(f"Adaptive GAUSSIAN\n(blockSize={block_size}, C={C})",
              fontsize=11, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 2, 5)
    plt.imshow(bin_otsu, cmap='gray')
    plt.title("Otsu (để so sánh)", fontsize=11, fontweight='bold')
    plt.axis('off')

    # Histogram
    plt.subplot(3, 2, 6)
    plt.hist(gray.ravel(), 256, [0, 256], color='steelblue', alpha=0.7)
    plt.title("Histogram ảnh xám", fontsize=11, fontweight='bold')
    plt.xlabel("Mức xám")
    plt.ylabel("Tần suất")
    plt.grid(alpha=0.3)

    plt.tight_layout()

    # Lưu kết quả
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "adaptive_threshold_result.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nĐã lưu kết quả tại: {output_path}")

    plt.show()

    print("\n" + "="*60)
    print("HOÀN THÀNH!")
    print("="*60)


if __name__ == "__main__":
    main()
