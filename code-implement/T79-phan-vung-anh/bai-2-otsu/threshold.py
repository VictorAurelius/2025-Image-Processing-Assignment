"""
=============================================================================
BÀI 2: OTSU TỐI ƯU (BETWEEN-CLASS VARIANCE)
=============================================================================
Đề bài: Đếm số viên linh kiện trên nền phẳng dưới điều kiện sáng ổn định.
Mục tiêu: Dùng Otsu để tự động tìm ngưỡng tối ưu.
Yêu cầu: Hiển thị histogram và mask; so sánh với ngưỡng thủ công.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T79-99 Phân vùng ảnh (trang 3-4)
=============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def create_sample_image():
    """Tạo ảnh mẫu linh kiện điện tử."""
    img = np.ones((400, 600, 3), dtype=np.uint8) * 220  # Nền trắng

    # Tạo các linh kiện (hình chữ nhật) màu tối
    components = [
        (50, 50, 100, 100), (140, 60, 190, 110), (230, 40, 280, 90),
        (340, 70, 390, 120), (450, 50, 500, 100),
        (80, 180, 130, 230), (200, 200, 250, 250), (320, 190, 370, 240),
        (100, 300, 150, 350), (250, 310, 300, 360), (400, 290, 450, 340)
    ]

    for x1, y1, x2, y2 in components:
        # Màu linh kiện
        color = (50, 50, 50)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
        # Viền
        cv2.rectangle(img, (x1, y1), (x2, y2), (30, 30, 30), 1)

    return img


def count_components(binary_img):
    """Đếm số linh kiện trong ảnh nhị phân."""
    # Tìm contours
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Lọc các contour có diện tích đủ lớn
    min_area = 100
    valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    return len(valid_contours), valid_contours


def main():
    # Kiểm tra ảnh input
    input_path = "../input/parts.jpg"

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
    print("PHÂN NGƯỠNG OTSU - OTSU THRESHOLDING")
    print("="*60)

    # Áp dụng Otsu
    T, binimg = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Đảo màu nếu cần (linh kiện màu trắng)
    if np.mean(binimg) > 127:
        binimg = cv2.bitwise_not(binimg)

    print(f"\nNgưỡng Otsu tối ưu: T = {T:.2f}")

    # Đếm số linh kiện
    num_components, contours = count_components(binimg)
    print(f"Số lượng linh kiện phát hiện: {num_components}")

    # Vẽ bounding boxes lên ảnh gốc
    img_result = img.copy()
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img_result, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Thống kê histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

    print(f"\nThống kê ảnh:")
    print(f"  - Độ sáng trung bình: {np.mean(gray):.2f}")
    print(f"  - Độ lệch chuẩn: {np.std(gray):.2f}")
    print(f"  - Min/Max: {np.min(gray)}/{np.max(gray)}")

    # So sánh với ngưỡng thủ công
    manual_T = 128
    _, binimg_manual = cv2.threshold(gray, manual_T, 255, cv2.THRESH_BINARY_INV)
    num_manual, _ = count_components(binimg_manual)

    print(f"\nSo sánh:")
    print(f"  - Otsu (T={T:.0f}): {num_components} linh kiện")
    print(f"  - Thủ công (T={manual_T}): {num_manual} linh kiện")

    # Hiển thị kết quả
    plt.figure(figsize=(14, 8))

    plt.subplot(2, 3, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Ảnh gốc", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(2, 3, 2)
    plt.imshow(gray, cmap='gray')
    plt.title("Ảnh xám", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(2, 3, 3)
    plt.hist(gray.ravel(), 256, [0, 256], color='steelblue', alpha=0.7)
    plt.axvline(x=T, color='red', linestyle='--', linewidth=2, label=f'Otsu T={T:.0f}')
    plt.title("Histogram", fontsize=12, fontweight='bold')
    plt.xlabel("Mức xám")
    plt.ylabel("Tần suất")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.subplot(2, 3, 4)
    plt.imshow(binimg, cmap='gray')
    plt.title(f"Otsu mask (T={T:.0f})", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(2, 3, 5)
    plt.imshow(cv2.cvtColor(img_result, cv2.COLOR_BGR2RGB))
    plt.title(f"Phát hiện {num_components} linh kiện", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(2, 3, 6)
    plt.imshow(binimg_manual, cmap='gray')
    plt.title(f"Ngưỡng thủ công (T={manual_T})", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.tight_layout()

    # Lưu kết quả
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "otsu_threshold_result.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nĐã lưu kết quả tại: {output_path}")

    plt.show()

    print("\n" + "="*60)
    print("HOÀN THÀNH!")
    print("="*60)


if __name__ == "__main__":
    main()
