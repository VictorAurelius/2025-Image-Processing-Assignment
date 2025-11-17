"""
================================================================================
BÀI 5: PHÂN ĐOẠN KÝ TỰ BIỂN SỐ/SERI (OPENING/CLOSING + CC)
================================================================================

Đề bài:
    Cho ảnh biển số hoặc tem seri in, hãy tách ký tự để OCR.

Mục tiêu:
    Dùng mở/đóng sạch nền, sau đó Connected Components.

Yêu cầu:
    Loại bỏ "dấu chấm/bavia" bằng opening; nối nét bằng closing.

Hướng dẫn:
    Thử RECT vs ELLIPSE kernels tùy chiều nét.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T61-78 Xử lý hình thái (trang 69-70)
================================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def create_plate_image():
    """Tạo ảnh biển số mẫu"""
    img = np.ones((150, 500), dtype=np.uint8) * 255

    # Vẽ chữ số biển số
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, '29A-12345', (30, 100), font, 2.5, 0, 5)

    # Thêm nhiễu nhỏ (dấu chấm, vết bẩn)
    for _ in range(50):
        x = np.random.randint(0, img.shape[1])
        y = np.random.randint(0, img.shape[0])
        cv2.circle(img, (x, y), np.random.randint(1, 3), 0, -1)

    # Thêm khe hở trong chữ
    cv2.line(img, (100, 70), (100, 80), 255, 2)
    cv2.line(img, (250, 75), (250, 85), 255, 2)

    return img

def main():
    print("="*80)
    print("BÀI 5: PHÂN ĐOẠN KÝ TỰ BIỂN SỐ/SERI - OPENING/CLOSING + CC")
    print("="*80)

    # Tạo thư mục output
    os.makedirs('../output/bai-5-character-segmentation', exist_ok=True)

    # Kiểm tra ảnh input
    input_path = '../input/plates/plate.jpg'
    if os.path.exists(input_path):
        print(f"\n[+] Đọc ảnh từ: {input_path}")
        img = cv2.imread(input_path, 0)
    else:
        print(f"\n[!] Không tìm thấy ảnh input. Tạo ảnh mẫu...")
        os.makedirs('../input/plates', exist_ok=True)
        img = create_plate_image()
        cv2.imwrite(input_path, img)
        print(f"[+] Đã tạo ảnh mẫu: {input_path}")

    print(f"[+] Kích thước ảnh: {img.shape}")

    # Nhị phân hóa Otsu (đảo ngược)
    print("\n" + "="*80)
    print("BƯỚC 1: NHỊ PHÂN HÓA OTSU (ĐẢO NGƯỢC)")
    print("="*80)

    _, bw = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    print(f"[+] Đã nhị phân hóa Otsu (chữ trắng, nền đen)")
    print(f"[+] Số pixel ký tự: {np.sum(bw == 255)}")

    # Opening để loại bỏ nhiễu nhỏ
    print("\n" + "="*80)
    print("BƯỚC 2: OPENING ĐỂ LOẠI BỎ NHIỄU")
    print("="*80)

    kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    print(f"[+] Tạo kernel RECT 3x3 cho Opening")

    bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel_open)
    print(f"[+] Đã loại bỏ nhiễu nhỏ bằng Opening")
    noise_removed = np.sum(bw == 255)
    print(f"[+] Số pixel còn lại: {noise_removed}")

    # Closing để nối nét
    print("\n" + "="*80)
    print("BƯỚC 3: CLOSING ĐỂ NỐI NÉT")
    print("="*80)

    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    print(f"[+] Tạo kernel RECT 5x5 cho Closing")

    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel_close)
    print(f"[+] Đã nối các nét gần nhau bằng Closing")
    after_closing = np.sum(bw == 255)
    print(f"[+] Số pixel sau Closing: {after_closing}")

    # Connected Components
    print("\n" + "="*80)
    print("BƯỚC 4: CONNECTED COMPONENTS ANALYSIS")
    print("="*80)

    n, labels = cv2.connectedComponents(bw)
    print(f"[+] Số thành phần (kể cả nền): {n}")
    print(f"[+] Số ký tự ước lượng: {n - 1}")

    # Phân tích từng thành phần
    print("\n[+] Phân tích chi tiết từng thành phần:")
    components_info = []

    for i in range(1, n):  # Bỏ qua nền (0)
        mask = (labels == i).astype(np.uint8) * 255
        pixels = np.sum(mask == 255)
        y_coords, x_coords = np.where(labels == i)

        if len(x_coords) > 0 and len(y_coords) > 0:
            x_min, x_max = x_coords.min(), x_coords.max()
            y_min, y_max = y_coords.min(), y_coords.max()
            width = x_max - x_min
            height = y_max - y_min
            area = width * height

            components_info.append({
                'id': i,
                'pixels': pixels,
                'bbox': (x_min, y_min, width, height),
                'area': area
            })

            print(f"   Component {i}: {pixels} pixels, bbox ({width}x{height}), area {area}")

    # Lọc các component quá nhỏ (nhiễu) hoặc quá lớn
    min_area = 100
    max_area = img.shape[0] * img.shape[1] * 0.5
    valid_components = [c for c in components_info if min_area < c['area'] < max_area]
    print(f"\n[+] Số ký tự hợp lệ (sau lọc): {len(valid_components)}")

    # Vẽ bounding box
    print("\n" + "="*80)
    print("BƯỚC 5: VẼ BOUNDING BOX")
    print("="*80)

    img_result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    for comp in valid_components:
        x, y, w, h = comp['bbox']
        cv2.rectangle(img_result, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img_result, str(comp['id']), (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    print(f"[+] Đã vẽ {len(valid_components)} bounding boxes")

    # Hiển thị kết quả
    print("\n" + "="*80)
    print("BƯỚC 6: HIỂN THỊ KẾT QUẢ")
    print("="*80)

    plt.figure(figsize=(18, 10))

    plt.subplot(2, 3, 1)
    plt.imshow(img, 'gray')
    plt.title('1. Ảnh gốc')
    plt.axis('off')

    plt.subplot(2, 3, 2)
    _, bw_original = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    plt.imshow(bw_original, 'gray')
    plt.title('2. Nhị phân gốc')
    plt.axis('off')

    plt.subplot(2, 3, 3)
    bw_after_open = cv2.morphologyEx(bw_original, cv2.MORPH_OPEN, kernel_open)
    plt.imshow(bw_after_open, 'gray')
    plt.title('3. Sau Opening')
    plt.axis('off')

    plt.subplot(2, 3, 4)
    plt.imshow(bw, 'gray')
    plt.title('4. Sau Closing')
    plt.axis('off')

    plt.subplot(2, 3, 5)
    labels_colored = np.uint8(255 * labels / labels.max())
    plt.imshow(labels_colored, 'jet')
    plt.title(f'5. Components ({n-1} ký tự)')
    plt.axis('off')

    plt.subplot(2, 3, 6)
    plt.imshow(cv2.cvtColor(img_result, cv2.COLOR_BGR2RGB))
    plt.title(f'6. Kết quả\n({len(valid_components)} ký tự)')
    plt.axis('off')

    plt.tight_layout()
    output_path = '../output/bai-5-character-segmentation/result.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"[+] Đã lưu kết quả: {output_path}")
    plt.show()

    # Lưu từng ký tự
    print("\n" + "="*80)
    print("BƯỚC 7: LƯU TỪNG KÝ TỰ")
    print("="*80)

    os.makedirs('../output/bai-5-character-segmentation/characters', exist_ok=True)

    for idx, comp in enumerate(sorted(valid_components, key=lambda c: c['bbox'][0]), 1):
        x, y, w, h = comp['bbox']
        # Thêm padding
        padding = 5
        y1 = max(0, y - padding)
        y2 = min(img.shape[0], y + h + padding)
        x1 = max(0, x - padding)
        x2 = min(img.shape[1], x + w + padding)

        char_img = img[y1:y2, x1:x2]
        char_path = f'../output/bai-5-character-segmentation/characters/char_{idx:02d}.png'
        cv2.imwrite(char_path, char_img)

    print(f"[+] Đã lưu {len(valid_components)} ký tự vào thư mục characters/")

    # Lưu ảnh kết quả
    cv2.imwrite('../output/bai-5-character-segmentation/segmented.png', img_result)
    cv2.imwrite('../output/bai-5-character-segmentation/cleaned.png', bw)

    print("\n" + "="*80)
    print("PHÂN TÍCH KẾT QUẢ")
    print("="*80)
    print(f"""
    1. QUY TRÌNH PHÂN ĐOẠN KÝ TỰ:
       - Nhị phân hóa Otsu (đảo ngược)
       - Opening: Loại bỏ nhiễu nhỏ (dấu chấm, bavia)
       - Closing: Nối các nét gần nhau (khắc phục nét đứt)
       - Connected Components: Tách từng ký tự
       - Lọc theo kích thước: Loại nhiễu và vùng không hợp lệ

    2. KẾT QUẢ:
       - Tổng components: {n - 1}
       - Ký tự hợp lệ: {len(valid_components)}
       - Đã lưu từng ký tự để chuẩn bị OCR

    3. KERNEL SELECTION:
       - Opening (3x3 RECT): Loại nhiễu nhỏ
       - Closing (5x5 RECT): Nối nét, phù hợp chữ số

    4. ỨNG DỤNG:
       - Nhận dạng biển số xe
       - Đọc mã vạch, QR code
       - OCR tài liệu
       - Phân tích tem phiếu
    """)

    print("\n[✓] Hoàn thành!")

if __name__ == "__main__":
    main()
