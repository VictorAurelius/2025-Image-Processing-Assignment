"""
================================================================================
BÀI 9: KHỬ NỀN KHÔNG ĐỒNG ĐỀU (GRAYSCALE TOP-HAT / BLACK-HAT)
================================================================================

Đề bài:
    Ảnh tài liệu/PCB có chiếu sáng không đều; hãy loại bỏ nền sáng/tối.

Mục tiêu:
    Áp dụng morphology mức xám: top-hat (χ = Img − opening) và
    black-hat (β = closing − Img).

Yêu cầu:
    So sánh histogram trước–sau; thử kernel 15×15.

Hướng dẫn:
    Dùng MORPH_TOPHAT và MORPH_BLACKHAT.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T61-78 Xử lý hình thái (trang 77-78)
================================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def create_uneven_lighting():
    """Tạo ảnh tài liệu với chiếu sáng không đều"""
    img = np.ones((600, 800), dtype=np.uint8) * 128

    # Tạo gradient chiếu sáng (sáng ở góc trên trái, tối ở góc dưới phải)
    y, x = np.ogrid[:600, :800]
    gradient = 255 - ((x / 800.0) * 100 + (y / 600.0) * 80)
    gradient = np.clip(gradient, 100, 255).astype(np.uint8)

    img = cv2.addWeighted(img, 0.5, gradient, 0.5, 0)

    # Vẽ text (vật thể tối trên nền sáng)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'Document Text', (50, 100), font, 2, 30, 3)
    cv2.putText(img, 'Image Processing', (50, 200), font, 1.5, 40, 2)
    cv2.putText(img, 'Morphological', (50, 300), font, 1.5, 35, 2)
    cv2.putText(img, 'Operations', (50, 400), font, 1.5, 38, 2)

    # Vẽ hình chữ nhật (linh kiện PCB)
    cv2.rectangle(img, (500, 100), (650, 200), 50, -1)
    cv2.rectangle(img, (520, 250), (670, 350), 45, -1)
    cv2.rectangle(img, (540, 400), (690, 500), 55, -1)

    # Thêm các đốm sáng (bavia, phản xạ)
    cv2.circle(img, (650, 150), 30, 200, -1)
    cv2.circle(img, (700, 300), 25, 210, -1)

    # Thêm nhiễu nhỏ
    noise = np.random.normal(0, 5, img.shape)
    img = np.clip(img + noise, 0, 255).astype(np.uint8)

    return img

def main():
    print("="*80)
    print("BÀI 9: KHỬ NỀN KHÔNG ĐỒNG ĐỀU - TOP-HAT / BLACK-HAT")
    print("="*80)

    # Tạo thư mục output
    os.makedirs('../output/bai-9-background-removal', exist_ok=True)

    # Kiểm tra ảnh input
    input_path = '../input/docs/uneven.jpg'
    if os.path.exists(input_path):
        print(f"\n[+] Đọc ảnh từ: {input_path}")
        img = cv2.imread(input_path, 0)
    else:
        print(f"\n[!] Không tìm thấy ảnh input. Tạo ảnh mẫu...")
        os.makedirs('../input/docs', exist_ok=True)
        img = create_uneven_lighting()
        cv2.imwrite(input_path, img)
        print(f"[+] Đã tạo ảnh mẫu: {input_path}")

    print(f"[+] Kích thước ảnh: {img.shape}")
    print(f"[+] Giá trị min: {img.min()}, max: {img.max()}, mean: {img.mean():.2f}")

    # Phân tích histogram gốc
    print("\n" + "="*80)
    print("BƯỚC 1: PHÂN TÍCH HISTOGRAM GỐC")
    print("="*80)

    hist_orig = cv2.calcHist([img], [0], None, [256], [0, 256])
    print(f"[+] Đã tính histogram ảnh gốc")

    # Tạo Structuring Element
    print("\n" + "="*80)
    print("BƯỚC 2: TẠO STRUCTURING ELEMENT")
    print("="*80)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    print(f"[+] Tạo SE RECT 15x15")
    print(f"[+] Kernel lớn để ước lượng nền")

    # Top-hat Transform
    print("\n" + "="*80)
    print("BƯỚC 3: TOP-HAT TRANSFORM")
    print("="*80)

    tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    print(f"[+] Top-hat = Img - Opening(Img)")
    print(f"[+] Mục đích: Trích xuất vật thể sáng hơn nền")
    print(f"[+] Giá trị min: {tophat.min()}, max: {tophat.max()}, mean: {tophat.mean():.2f}")

    # Black-hat Transform
    print("\n" + "="*80)
    print("BƯỚC 4: BLACK-HAT TRANSFORM")
    print("="*80)

    blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
    print(f"[+] Black-hat = Closing(Img) - Img")
    print(f"[+] Mục đích: Trích xuất vật thể tối hơn nền")
    print(f"[+] Giá trị min: {blackhat.min()}, max: {blackhat.max()}, mean: {blackhat.mean():.2f}")

    # Điều chỉnh ảnh
    print("\n" + "="*80)
    print("BƯỚC 5: ĐIỀU CHỈNH ẢNH")
    print("="*80)

    # Cách 1: img + tophat - blackhat
    corrected = cv2.normalize(img + tophat - blackhat, None, 0, 255, cv2.NORM_MINMAX)
    print(f"[+] Corrected = normalize(Img + tophat - blackhat)")
    print(f"[+] Giá trị min: {corrected.min()}, max: {corrected.max()}, mean: {corrected.mean():.2f}")

    # Tính histogram sau điều chỉnh
    hist_corrected = cv2.calcHist([corrected], [0], None, [256], [0, 256])

    # Lưu kết quả
    print("\n" + "="*80)
    print("BƯỚC 6: LƯU KẾT QUẢ")
    print("="*80)

    cv2.imwrite('../output/bai-9-background-removal/tophat.png', tophat)
    cv2.imwrite('../output/bai-9-background-removal/blackhat.png', blackhat)
    cv2.imwrite('../output/bai-9-background-removal/corrected.png', corrected)
    print(f"[+] Đã lưu tophat, blackhat, và corrected")

    # So sánh với kernel khác nhau
    print("\n" + "="*80)
    print("BƯỚC 7: SO SÁNH KERNEL KHÁC NHAU")
    print("="*80)

    kernel_sizes = [7, 11, 15, 21]
    results = []

    for k in kernel_sizes:
        kernel_test = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
        tophat_test = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel_test)
        blackhat_test = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel_test)
        corrected_test = cv2.normalize(img + tophat_test - blackhat_test,
                                        None, 0, 255, cv2.NORM_MINMAX)

        results.append({
            'size': k,
            'tophat': tophat_test,
            'blackhat': blackhat_test,
            'corrected': corrected_test
        })

        print(f"\nKernel {k}x{k}:")
        print(f"  - Tophat mean: {tophat_test.mean():.2f}")
        print(f"  - Blackhat mean: {blackhat_test.mean():.2f}")
        print(f"  - Corrected std: {corrected_test.std():.2f}")

    # Hiển thị kết quả
    print("\n" + "="*80)
    print("BƯỚC 8: HIỂN THỊ KẾT QUẢ")
    print("="*80)

    fig = plt.figure(figsize=(15, 10))

    # Hàng 1: Quy trình chính
    plt.subplot(2, 3, 1)
    plt.imshow(img, 'gray')
    plt.title('1. Ảnh gốc\n(chiếu sáng không đều)')
    plt.axis('off')

    plt.subplot(2, 3, 2)
    plt.imshow(tophat, 'gray')
    plt.title('2. Top-hat\n(vật thể sáng)')
    plt.axis('off')

    plt.subplot(2, 3, 3)
    plt.imshow(corrected, 'gray')
    plt.title('3. Điều chỉnh\n(đồng đều)')
    plt.axis('off')

    plt.subplot(2, 3, 4)
    plt.imshow(blackhat, 'gray')
    plt.title('4. Black-hat\n(vật thể tối)')
    plt.axis('off')

    # Histogram so sánh
    plt.subplot(2, 3, 5)
    plt.plot(hist_orig, color='blue', alpha=0.7, label='Gốc')
    plt.plot(hist_corrected, color='green', alpha=0.7, label='Điều chỉnh')
    plt.xlabel('Giá trị pixel')
    plt.ylabel('Tần suất')
    plt.title('5. So sánh Histogram')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # So sánh trước/sau
    plt.subplot(2, 3, 6)
    comparison = np.hstack([img, corrected])
    plt.imshow(comparison, 'gray')
    plt.title('6. Trước (trái) vs Sau (phải)')
    plt.axis('off')

    plt.tight_layout()
    output_path = '../output/bai-9-background-removal/result.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"[+] Đã lưu kết quả: {output_path}")
    plt.show()

    # So sánh kernel sizes
    print("\n" + "="*80)
    print("BƯỚC 9: SO SÁNH KERNEL SIZES")
    print("="*80)

    fig, axes = plt.subplots(2, 4, figsize=(20, 10))

    for idx, res in enumerate(results):
        # Hàng 1: Top-hat
        axes[0, idx].imshow(res['tophat'], 'gray')
        axes[0, idx].set_title(f'Top-hat {res["size"]}x{res["size"]}')
        axes[0, idx].axis('off')

        # Hàng 2: Corrected
        axes[1, idx].imshow(res['corrected'], 'gray')
        axes[1, idx].set_title(f'Corrected {res["size"]}x{res["size"]}')
        axes[1, idx].axis('off')

    plt.tight_layout()
    plt.savefig('../output/bai-9-background-removal/kernel_comparison.png',
                dpi=150, bbox_inches='tight')
    print(f"[+] Đã lưu so sánh kernel")
    plt.show()

    # Phân tích chất lượng
    print("\n" + "="*80)
    print("BƯỚC 10: PHÂN TÍCH CHẤT LƯỢNG")
    print("="*80)

    # Tính contrast và độ đồng đều
    orig_std = img.std()
    orig_contrast = img.max() - img.min()
    corr_std = corrected.std()
    corr_contrast = corrected.max() - corrected.min()

    print(f"\n[+] Độ lệch chuẩn:")
    print(f"    - Gốc: {orig_std:.2f}")
    print(f"    - Điều chỉnh: {corr_std:.2f}")
    print(f"    - Cải thiện: {(corr_std - orig_std) / orig_std * 100:+.2f}%")

    print(f"\n[+] Contrast:")
    print(f"    - Gốc: {orig_contrast}")
    print(f"    - Điều chỉnh: {corr_contrast}")

    # Tính độ đồng đều của nền
    # Chia ảnh thành các vùng và tính variance
    def calculate_uniformity(image):
        h, w = image.shape
        regions = []
        for i in range(0, h, 100):
            for j in range(0, w, 100):
                region = image[i:min(i+100, h), j:min(j+100, w)]
                regions.append(region.mean())
        return np.std(regions)

    orig_uniformity = calculate_uniformity(img)
    corr_uniformity = calculate_uniformity(corrected)

    print(f"\n[+] Độ đồng đều nền (càng thấp càng tốt):")
    print(f"    - Gốc: {orig_uniformity:.2f}")
    print(f"    - Điều chỉnh: {corr_uniformity:.2f}")
    print(f"    - Cải thiện: {(orig_uniformity - corr_uniformity) / orig_uniformity * 100:.2f}%")

    # Vẽ biểu đồ so sánh
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    metrics = ['Std Dev', 'Uniformity']
    orig_values = [orig_std, orig_uniformity]
    corr_values = [corr_std, corr_uniformity]

    x = np.arange(len(metrics))
    width = 0.35

    axes[0].bar(x - width/2, orig_values, width, label='Gốc', alpha=0.8)
    axes[0].bar(x + width/2, corr_values, width, label='Điều chỉnh', alpha=0.8)
    axes[0].set_ylabel('Giá trị')
    axes[0].set_title('So sánh các chỉ số')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(metrics)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3, axis='y')

    # Profile line qua giữa ảnh
    mid_row = img.shape[0] // 2
    axes[1].plot(img[mid_row, :], label='Gốc', alpha=0.7)
    axes[1].plot(corrected[mid_row, :], label='Điều chỉnh', alpha=0.7)
    axes[1].set_xlabel('Vị trí pixel (ngang)')
    axes[1].set_ylabel('Giá trị pixel')
    axes[1].set_title('Profile line qua giữa ảnh')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('../output/bai-9-background-removal/quality_analysis.png',
                dpi=150, bbox_inches='tight')
    print(f"\n[+] Đã lưu phân tích chất lượng")
    plt.show()

    print("\n" + "="*80)
    print("PHÂN TÍCH KẾT QUẢ")
    print("="*80)
    print(f"""
    1. MORPHOLOGY MỨC XÁM:
       - Top-hat = Img - Opening(Img)
         → Trích xuất vật thể sáng hơn nền cục bộ
       - Black-hat = Closing(Img) - Img
         → Trích xuất vật thể tối hơn nền cục bộ
       - Corrected = Img + Top-hat - Black-hat

    2. KẾT QUẢ:
       - Độ đồng đều nền cải thiện: {(orig_uniformity - corr_uniformity) / orig_uniformity * 100:.1f}%
       - Kernel 15x15 phù hợp với chiếu sáng không đều vừa phải

    3. KERNEL SIZE:
       - Nhỏ (7x7): Giữ chi tiết, khử nền yếu
       - Vừa (15x15): Cân bằng tốt
       - Lớn (21x21): Khử nền mạnh, có thể mất chi tiết

    4. ỨNG DỤNG:
       - Cải thiện ảnh tài liệu quét
       - Khử phản xạ ảnh PCB
       - Chuẩn hóa chiếu sáng trước OCR
       - Tiền xử lý ảnh y tế
       - Tách vật thể trong điều kiện ánh sáng xấu
    """)

    print("\n[✓] Hoàn thành!")

if __name__ == "__main__":
    main()
