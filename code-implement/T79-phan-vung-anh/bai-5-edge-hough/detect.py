"""
=============================================================================
BÀI 5: DÒ BIÊN + LIÊN KẾT BIÊN + HOUGH (BIÊN/ĐƯỜNG THẲNG)
=============================================================================
Đề bài: Xác định vạch kẻ đường/lằn cắt trên tấm vật liệu công nghiệp.
Mục tiêu: Dùng Canny → HoughLinesP để trích rìa và đường thẳng; tạo mặt nạ phân vùng.
Yêu cầu: Tối ưu tham số Canny, Hough.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T79-99 Phân vùng ảnh (trang 9-10)
=============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def create_sample_image():
    """Tạo ảnh mẫu với các vạch kẻ đường."""
    img = np.ones((400, 600, 3), dtype=np.uint8) * 100  # Nền tối

    # Vẽ các vạch kẻ đường (trắng)
    lines = [
        ((50, 100), (550, 120)),
        ((80, 200), (520, 210)),
        ((100, 300), (500, 290)),
        ((150, 50), (160, 350)),
        ((300, 80), (310, 320)),
        ((450, 60), (460, 340))
    ]

    for pt1, pt2 in lines:
        cv2.line(img, pt1, pt2, (220, 220, 220), 3)

    # Thêm nhiễu nhẹ
    noise = np.random.normal(0, 10, img.shape).astype(np.uint8)
    img = cv2.add(img, noise)

    return img


def main():
    # Kiểm tra ảnh input
    input_path = "../input/lanes.jpg"

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
    print("DÒ BIÊN VÀ PHÁT HIỆN ĐƯỜNG THẲNG - CANNY + HOUGH")
    print("="*60)

    # Tham số Canny
    canny_low = 80
    canny_high = 160

    print(f"\nTham số Canny Edge Detection:")
    print(f"  - Low threshold: {canny_low}")
    print(f"  - High threshold: {canny_high}")

    # Áp dụng Canny
    edges = cv2.Canny(gray, canny_low, canny_high)

    # Đếm số pixel biên
    edge_pixels = np.sum(edges > 0)
    total_pixels = edges.size
    print(f"\nSố pixel biên phát hiện: {edge_pixels} ({100*edge_pixels/total_pixels:.2f}%)")

    # Tham số Hough Lines
    hough_threshold = 80
    min_line_length = 60
    max_line_gap = 10

    print(f"\nTham số Hough Lines:")
    print(f"  - Threshold: {hough_threshold}")
    print(f"  - Min line length: {min_line_length}")
    print(f"  - Max line gap: {max_line_gap}")

    # Áp dụng HoughLinesP
    lines = cv2.HoughLinesP(edges, 1, np.pi/180,
                            threshold=hough_threshold,
                            minLineLength=min_line_length,
                            maxLineGap=max_line_gap)

    # Vẽ các đường thẳng phát hiện được
    out = img.copy()
    num_lines = 0

    if lines is not None:
        num_lines = len(lines)
        print(f"\nSố đường thẳng phát hiện: {num_lines}")

        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(out, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Tính độ dài và góc
            length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
            angle = np.arctan2(y2-y1, x2-x1) * 180 / np.pi

        # Thống kê đường thẳng
        lengths = []
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
            angle = np.arctan2(y2-y1, x2-x1) * 180 / np.pi
            lengths.append(length)
            angles.append(angle)

        print(f"\nThống kê đường thẳng:")
        print(f"  - Độ dài trung bình: {np.mean(lengths):.1f} pixels")
        print(f"  - Độ dài min/max: {np.min(lengths):.1f}/{np.max(lengths):.1f}")
        print(f"  - Góc trung bình: {np.mean(angles):.1f}°")
    else:
        print("\nKhông phát hiện đường thẳng nào!")

    # Tạo mask từ đường thẳng
    mask = np.zeros_like(gray)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(mask, (x1, y1), (x2, y2), 255, 5)

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
    plt.imshow(edges, cmap='gray')
    plt.title(f"Canny edges\n({canny_low}/{canny_high})",
              fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 4)
    plt.imshow(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
    plt.title(f"Hough lines ({num_lines} đường)",
              fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 3, 5)
    plt.imshow(mask, cmap='gray')
    plt.title("Mask từ đường thẳng", fontsize=12, fontweight='bold')
    plt.axis('off')

    # Overlay mask lên ảnh gốc
    plt.subplot(3, 3, 6)
    overlay = img.copy()
    overlay[mask > 0] = [0, 255, 255]  # Màu cyan
    result = cv2.addWeighted(img, 0.7, overlay, 0.3, 0)
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title("Overlay", fontsize=12, fontweight='bold')
    plt.axis('off')

    # Histogram góc
    if lines is not None and len(angles) > 0:
        plt.subplot(3, 3, 7)
        plt.hist(angles, bins=20, color='steelblue', alpha=0.7, edgecolor='black')
        plt.title("Phân bố góc đường thẳng", fontsize=12, fontweight='bold')
        plt.xlabel("Góc (độ)")
        plt.ylabel("Tần suất")
        plt.grid(alpha=0.3)

    # Histogram độ dài
    if lines is not None and len(lengths) > 0:
        plt.subplot(3, 3, 8)
        plt.hist(lengths, bins=15, color='coral', alpha=0.7, edgecolor='black')
        plt.title("Phân bố độ dài đường thẳng", fontsize=12, fontweight='bold')
        plt.xlabel("Độ dài (pixels)")
        plt.ylabel("Tần suất")
        plt.grid(alpha=0.3)

    # Vùng quan tâm (ROI) - ví dụ
    plt.subplot(3, 3, 9)
    roi = gray.copy()
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(roi, (x1, y1), (x2, y2), 255, 3)
    plt.imshow(roi, cmap='gray')
    plt.title("ROI với đường thẳng", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.tight_layout()

    # Lưu kết quả
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "edge_hough_result.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nĐã lưu kết quả tại: {output_path}")

    plt.show()

    print("\n" + "="*60)
    print("HOÀN THÀNH!")
    print("="*60)


if __name__ == "__main__":
    main()
