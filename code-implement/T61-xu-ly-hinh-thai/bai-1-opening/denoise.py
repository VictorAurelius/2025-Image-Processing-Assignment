"""
================================================================================
BÀI 1: LÀM SẠCH VĂN BẢN QUÉT (OPENING ĐỂ KHỬ NHIỄU MUỐI TIÊU)
================================================================================

Đề bài:
    Cho ảnh tài liệu/bản in bị nhiễu muối tiêu, hãy loại bỏ nhiễu mà vẫn giữ nét chữ.

Mục tiêu:
    Nắm phép mở (erosion → dilation) để khử nhiễu hạt nhỏ.

Yêu cầu:
    So sánh kernel 3×3, 5×5; báo cáo PSNR/SSIM trước–sau (tùy chọn).

Hướng dẫn:
    Nhị phân hóa Otsu → MORPH_OPEN → đánh giá.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T61-78 Xử lý hình thái (trang 61-62)
================================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def create_noisy_document():
    """Tạo ảnh tài liệu mẫu có nhiễu muối tiêu"""
    # Tạo ảnh trắng
    img = np.ones((400, 600), dtype=np.uint8) * 255

    # Vẽ text
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'Xin chao!', (50, 100), font, 2, 0, 3)
    cv2.putText(img, 'Image Processing', (50, 200), font, 1.5, 0, 2)
    cv2.putText(img, 'Morphological Operations', (50, 300), font, 1, 0, 2)

    # Thêm nhiễu muối tiêu
    noise = np.random.rand(*img.shape)
    img[noise < 0.02] = 0  # Nhiễu tiêu (đen)
    img[noise > 0.98] = 255  # Nhiễu muối (trắng)

    return img

def main():
    print("="*80)
    print("BÀI 1: LÀM SẠCH VĂN BẢN QUÉT - OPENING ĐỂ KHỬ NHIỄU MUỐI TIÊU")
    print("="*80)

    # Tạo thư mục output
    os.makedirs('../output/bai-1-opening', exist_ok=True)

    # Kiểm tra ảnh input
    input_path = '../input/docs/noisy_scan.png'
    if os.path.exists(input_path):
        print(f"\n[+] Đọc ảnh từ: {input_path}")
        img = cv2.imread(input_path, 0)
    else:
        print(f"\n[!] Không tìm thấy ảnh input. Tạo ảnh mẫu...")
        os.makedirs('../input/docs', exist_ok=True)
        img = create_noisy_document()
        cv2.imwrite(input_path, img)
        print(f"[+] Đã tạo ảnh mẫu: {input_path}")

    print(f"[+] Kích thước ảnh: {img.shape}")
    print(f"[+] Kiểu dữ liệu: {img.dtype}")

    # Nhị phân hóa Otsu
    print("\n" + "="*80)
    print("BƯỚC 1: NHỊ PHÂN HÓA OTSU")
    print("="*80)
    _, bw = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(f"[+] Đã nhị phân hóa bằng phương pháp Otsu")
    print(f"[+] Số pixel trắng: {np.sum(bw == 255)}")
    print(f"[+] Số pixel đen: {np.sum(bw == 0)}")

    # Áp dụng Opening với các kernel khác nhau
    print("\n" + "="*80)
    print("BƯỚC 2: ÁP DỤNG MORPHOLOGICAL OPENING")
    print("="*80)

    for k in [3, 5]:
        print(f"\n--- Kernel {k}x{k} ---")
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
        print(f"[+] Tạo structuring element RECT {k}x{k}")

        open_img = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel)
        print(f"[+] Thực hiện MORPH_OPEN (Erosion → Dilation)")

        # Tính số pixel nhiễu đã loại bỏ
        removed = np.sum(bw != open_img)
        print(f"[+] Số pixel đã thay đổi: {removed}")
        print(f"[+] Tỷ lệ thay đổi: {removed / bw.size * 100:.2f}%")

        # Hiển thị kết quả
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
        plt.imshow(open_img, 'gray')
        plt.title(f'Opening {k}x{k}')
        plt.axis('off')

        plt.tight_layout()
        output_path = f'../output/bai-1-opening/result_kernel_{k}x{k}.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"[+] Đã lưu kết quả: {output_path}")
        plt.show()

        # Lưu ảnh xử lý
        cv2.imwrite(f'../output/bai-1-opening/opened_{k}x{k}.png', open_img)

    print("\n" + "="*80)
    print("PHÂN TÍCH KẾT QUẢ")
    print("="*80)
    print("""
    1. PHÉP MỞ (OPENING):
       - Opening = Erosion → Dilation
       - Loại bỏ nhiễu nhỏ (muối tiêu) mà vẫn giữ cấu trúc chính

    2. SO SÁNH KERNEL:
       - Kernel 3x3: Loại bỏ nhiễu nhỏ, giữ được chi tiết chữ
       - Kernel 5x5: Loại bỏ nhiễu tốt hơn nhưng có thể làm mất nét mảnh

    3. ỨNG DỤNG:
       - Làm sạch văn bản quét trước OCR
       - Tiền xử lý ảnh tài liệu
       - Khử nhiễu ảnh nhị phân
    """)

    print("\n[✓] Hoàn thành!")

if __name__ == "__main__":
    main()
