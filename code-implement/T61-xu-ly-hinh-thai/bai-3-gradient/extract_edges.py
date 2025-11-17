"""
================================================================================
BÀI 3: TRÍCH BIÊN BẰNG ĐỐI NGẪU GIÃN–XÓI (MORPHOLOGICAL GRADIENT)
================================================================================

Đề bài:
    Làm nổi đường biên của chi tiết công nghiệp hoặc tế bào.

Mục tiêu:
    Dùng gradient hình thái = dilation − erosion.
    Liên hệ câu hỏi "phát hiện đường biên? giải pháp" trong slide.

Yêu cầu:
    So với Canny; báo cáo sự khác biệt biên thô/mịn.

Hướng dẫn:
    MORPH_GRADIENT với kernel 3×3.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T61-78 Xử lý hình thái (trang 65-66)
================================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def create_sample_objects():
    """Tạo ảnh các vật thể mẫu"""
    img = np.ones((400, 600), dtype=np.uint8) * 255

    # Vẽ hình chữ nhật
    cv2.rectangle(img, (50, 50), (200, 150), 0, -1)

    # Vẽ vòng tròn
    cv2.circle(img, (400, 100), 60, 0, -1)

    # Vẽ đa giác
    pts = np.array([[100, 250], [200, 250], [150, 350]], np.int32)
    cv2.fillPoly(img, [pts], 0)

    # Vẽ elip
    cv2.ellipse(img, (450, 300), (80, 40), 30, 0, 360, 0, -1)

    return img

def main():
    print("="*80)
    print("BÀI 3: TRÍCH BIÊN BẰNG ĐỐI NGẪU GIÃN–XÓI (MORPHOLOGICAL GRADIENT)")
    print("="*80)

    # Tạo thư mục output
    os.makedirs('../output/bai-3-gradient', exist_ok=True)

    # Kiểm tra ảnh input
    input_path = '../input/objects/sample.png'
    if os.path.exists(input_path):
        print(f"\n[+] Đọc ảnh từ: {input_path}")
        img = cv2.imread(input_path, 0)
    else:
        print(f"\n[!] Không tìm thấy ảnh input. Tạo ảnh mẫu...")
        os.makedirs('../input/objects', exist_ok=True)
        img = create_sample_objects()
        cv2.imwrite(input_path, img)
        print(f"[+] Đã tạo ảnh mẫu: {input_path}")

    print(f"[+] Kích thước ảnh: {img.shape}")

    # Nhị phân hóa Otsu
    print("\n" + "="*80)
    print("BƯỚC 1: NHỊ PHÂN HÓA OTSU")
    print("="*80)
    _, bw = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(f"[+] Đã nhị phân hóa bằng phương pháp Otsu")

    # Morphological Gradient
    print("\n" + "="*80)
    print("BƯỚC 2: MORPHOLOGICAL GRADIENT")
    print("="*80)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    print(f"[+] Tạo structuring element RECT 3x3")

    grad = cv2.morphologyEx(bw, cv2.MORPH_GRADIENT, kernel)
    print(f"[+] Thực hiện MORPH_GRADIENT (Dilation - Erosion)")
    print(f"[+] Số pixel biên: {np.sum(grad > 0)}")

    # Canny Edge Detection để so sánh
    print("\n" + "="*80)
    print("BƯỚC 3: CANNY EDGE DETECTION (SO SÁNH)")
    print("="*80)

    edges = cv2.Canny(img, 50, 150)
    print(f"[+] Thực hiện Canny với threshold (50, 150)")
    print(f"[+] Số pixel biên Canny: {np.sum(edges > 0)}")

    # Tính toán độ dày biên trung bình
    print("\n" + "="*80)
    print("PHÂN TÍCH ĐỘ DÀY BIÊN")
    print("="*80)

    # Đếm contours
    contours_morph, _ = cv2.findContours(grad, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_canny, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(f"[+] Số contour (Morph Gradient): {len(contours_morph)}")
    print(f"[+] Số contour (Canny): {len(contours_canny)}")
    print(f"[+] Tỷ lệ pixel biên (Morph/Canny): {np.sum(grad > 0) / np.sum(edges > 0):.2f}")

    # Hiển thị kết quả
    print("\n" + "="*80)
    print("BƯỚC 4: HIỂN THỊ KẾT QUẢ")
    print("="*80)

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(bw, 'gray')
    plt.title('Nhị phân')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(grad, 'gray')
    plt.title('Morph. gradient')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(edges, 'gray')
    plt.title('Canny')
    plt.axis('off')

    plt.tight_layout()
    output_path = '../output/bai-3-gradient/result.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"[+] Đã lưu kết quả: {output_path}")
    plt.show()

    # Lưu các ảnh
    cv2.imwrite('../output/bai-3-gradient/gradient.png', grad)
    cv2.imwrite('../output/bai-3-gradient/canny.png', edges)

    # So sánh với kernel khác nhau
    print("\n" + "="*80)
    print("BƯỚC 5: SO SÁNH KERNEL KHÁC NHAU")
    print("="*80)

    plt.figure(figsize=(18, 5))

    for idx, k in enumerate([3, 5, 7], 1):
        kernel_test = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
        grad_test = cv2.morphologyEx(bw, cv2.MORPH_GRADIENT, kernel_test)
        edge_pixels = np.sum(grad_test > 0)

        print(f"\nKernel {k}x{k}:")
        print(f"  - Số pixel biên: {edge_pixels}")

        plt.subplot(1, 3, idx)
        plt.imshow(grad_test, 'gray')
        plt.title(f'Gradient {k}x{k}\n({edge_pixels} pixels)')
        plt.axis('off')

    plt.tight_layout()
    plt.savefig('../output/bai-3-gradient/kernel_comparison.png', dpi=150, bbox_inches='tight')
    print(f"\n[+] Đã lưu so sánh: ../output/bai-3-gradient/kernel_comparison.png")
    plt.show()

    print("\n" + "="*80)
    print("PHÂN TÍCH KẾT QUẢ")
    print("="*80)
    print("""
    1. MORPHOLOGICAL GRADIENT:
       - Gradient = Dilation - Erosion
       - Tạo biên dày, đều đặn
       - Không nhạy với nhiễu như Canny

    2. SO SÁNH VỚI CANNY:
       - Morph Gradient: Biên dày hơn, liên tục
       - Canny: Biên mỏng, chính xác hơn
       - Morph: Đơn giản, nhanh, phù hợp ảnh nhị phân
       - Canny: Phức tạp, chậm, tốt cho ảnh xám

    3. KERNEL SIZE:
       - 3x3: Biên mỏng, chi tiết
       - 5x5: Biên vừa phải
       - 7x7: Biên dày, làm nổi vật thể

    4. ỨNG DỤNG:
       - Phát hiện biên vật thể
       - Phân tích hình dạng
       - Đo đạc chi tiết công nghiệp
    """)

    print("\n[✓] Hoàn thành!")

if __name__ == "__main__":
    main()
