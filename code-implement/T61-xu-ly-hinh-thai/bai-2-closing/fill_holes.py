"""
================================================================================
BÀI 2: LẤP LỖ VÀ NỐI NÉT (CLOSING ĐỂ PHỤC HỒI VẬT THỂ)
================================================================================

Đề bài:
    Ảnh linh kiện/biometric có lỗ nhỏ và khe hở; hãy lấp lỗ và nối nét.

Mục tiêu:
    Dùng đóng (dilation → erosion) để lấp lỗ nhỏ, hàn mép.

Yêu cầu:
    Chọn kernel phù hợp hình học (RECT/ELLIPSE/LINE).

Hướng dẫn:
    Nhị phân hóa → MORPH_CLOSE → so sánh diện tích vật thể.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T61-78 Xử lý hình thái (trang 63-64)
================================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def create_gapped_parts():
    """Tạo ảnh linh kiện có khe hở"""
    img = np.ones((400, 600), dtype=np.uint8) * 255

    # Vẽ hình chữ nhật có khe hở
    cv2.rectangle(img, (50, 50), (200, 150), 0, -1)
    cv2.rectangle(img, (90, 90), (120, 110), 255, -1)  # Lỗ nhỏ

    # Vẽ vòng tròn có khe hở
    cv2.circle(img, (400, 100), 60, 0, -1)
    cv2.circle(img, (410, 90), 20, 255, -1)  # Lỗ nhỏ

    # Vẽ đa giác có khe hở
    pts = np.array([[100, 250], [200, 250], [150, 350]], np.int32)
    cv2.fillPoly(img, [pts], 0)
    cv2.circle(img, (150, 280), 15, 255, -1)  # Lỗ nhỏ

    # Vẽ chữ có nét đứt
    cv2.rectangle(img, (350, 250), (450, 350), 0, -1)
    cv2.line(img, (390, 250), (390, 290), 255, 3)  # Khe hở dọc
    cv2.line(img, (410, 310), (410, 350), 255, 3)  # Khe hở dọc

    return img

def main():
    print("="*80)
    print("BÀI 2: LẤP LỖ VÀ NỐI NÉT - CLOSING ĐỂ PHỤC HỒI VẬT THỂ")
    print("="*80)

    # Tạo thư mục output
    os.makedirs('../output/bai-2-closing', exist_ok=True)

    # Kiểm tra ảnh input
    input_path = '../input/parts/gapped.png'
    if os.path.exists(input_path):
        print(f"\n[+] Đọc ảnh từ: {input_path}")
        img = cv2.imread(input_path, 0)
    else:
        print(f"\n[!] Không tìm thấy ảnh input. Tạo ảnh mẫu...")
        os.makedirs('../input/parts', exist_ok=True)
        img = create_gapped_parts()
        cv2.imwrite(input_path, img)
        print(f"[+] Đã tạo ảnh mẫu: {input_path}")

    print(f"[+] Kích thước ảnh: {img.shape}")

    # Nhị phân hóa Otsu
    print("\n" + "="*80)
    print("BƯỚC 1: NHỊ PHÂN HÓA OTSU")
    print("="*80)
    _, bw = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(f"[+] Đã nhị phân hóa bằng phương pháp Otsu")

    # Đếm diện tích trước khi closing
    black_pixels_before = np.sum(bw == 0)
    print(f"[+] Diện tích vật thể trước: {black_pixels_before} pixels")

    # Áp dụng Closing với kernel ELLIPSE
    print("\n" + "="*80)
    print("BƯỚC 2: ÁP DỤNG MORPHOLOGICAL CLOSING")
    print("="*80)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    print(f"[+] Tạo structuring element ELLIPSE 7x7")
    print(f"[+] Kernel shape: {kernel.shape}")

    closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
    print(f"[+] Thực hiện MORPH_CLOSE (Dilation → Erosion)")

    # Đếm diện tích sau khi closing
    black_pixels_after = np.sum(closed == 0)
    filled_pixels = black_pixels_after - black_pixels_before
    print(f"[+] Diện tích vật thể sau: {black_pixels_after} pixels")
    print(f"[+] Đã lấp thêm: {filled_pixels} pixels")
    print(f"[+] Tỷ lệ lấp: {filled_pixels / black_pixels_before * 100:.2f}%")

    # Hiển thị kết quả
    print("\n" + "="*80)
    print("BƯỚC 3: HIỂN THỊ KẾT QUẢ")
    print("="*80)

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(img, 'gray')
    plt.title('Gốc')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(bw, 'gray')
    plt.title('Nhị phân')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(closed, 'gray')
    plt.title('Closing 7x7')
    plt.axis('off')

    plt.tight_layout()
    output_path = '../output/bai-2-closing/result.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"[+] Đã lưu kết quả: {output_path}")
    plt.show()

    # Lưu ảnh xử lý
    cv2.imwrite('../output/bai-2-closing/closed.png', closed)

    # So sánh các loại kernel
    print("\n" + "="*80)
    print("BƯỚC 4: SO SÁNH CÁC LOẠI KERNEL")
    print("="*80)

    kernel_types = [
        (cv2.MORPH_RECT, "RECT"),
        (cv2.MORPH_ELLIPSE, "ELLIPSE"),
        (cv2.MORPH_CROSS, "CROSS")
    ]

    plt.figure(figsize=(18, 5))
    for idx, (morph_type, name) in enumerate(kernel_types, 1):
        kernel_test = cv2.getStructuringElement(morph_type, (7, 7))
        closed_test = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel_test)
        filled_test = np.sum(closed_test == 0) - black_pixels_before

        print(f"\n[{name}]")
        print(f"  - Pixels lấp thêm: {filled_test}")

        plt.subplot(1, 3, idx)
        plt.imshow(closed_test, 'gray')
        plt.title(f'{name} (lấp: {filled_test}px)')
        plt.axis('off')

    plt.tight_layout()
    plt.savefig('../output/bai-2-closing/kernel_comparison.png', dpi=150, bbox_inches='tight')
    print(f"\n[+] Đã lưu so sánh: ../output/bai-2-closing/kernel_comparison.png")
    plt.show()

    print("\n" + "="*80)
    print("PHÂN TÍCH KẾT QUẢ")
    print("="*80)
    print("""
    1. PHÉP ĐÓNG (CLOSING):
       - Closing = Dilation → Erosion
       - Lấp lỗ nhỏ và khe hở trong vật thể
       - Nối các nét gần nhau

    2. SO SÁNH KERNEL:
       - RECT: Lấp tốt theo hướng ngang/dọc
       - ELLIPSE: Lấp đều mọi hướng, tự nhiên hơn
       - CROSS: Chỉ lấp theo 4 hướng chính

    3. ỨNG DỤNG:
       - Phục hồi vật thể bị khuyết
       - Nối các thành phần gần nhau
       - Làm mịn đường biên
    """)

    print("\n[✓] Hoàn thành!")

if __name__ == "__main__":
    main()
