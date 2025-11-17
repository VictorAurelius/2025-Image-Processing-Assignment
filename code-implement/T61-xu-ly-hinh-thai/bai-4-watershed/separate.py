"""
================================================================================
BÀI 4: ĐẾM ĐỒNG XU/VIÊN NÉN DÍNH NHAU (OPENING + DISTANCE TRANSFORM + WATERSHED)
================================================================================

Đề bài:
    Ảnh sản phẩm dạng "viên" chạm nhau; hãy tách và đếm số lượng.

Mục tiêu:
    Giải quyết "đếm số đồng xu khi chạm nhau" nêu trong slide.

Yêu cầu:
    Minh họa mask "sure foreground / sure background".

Hướng dẫn:
    Otsu → Opening → Distance Transform → Watershed.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T61-78 Xử lý hình thái (trang 67-68)
================================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def create_touching_coins():
    """Tạo ảnh các đồng xu chạm nhau"""
    img = np.ones((500, 600, 3), dtype=np.uint8) * 255

    # Vẽ các vòng tròn chạm nhau (màu BGR)
    coins = [
        ((100, 100), 50),
        ((180, 110), 50),
        ((140, 180), 50),
        ((350, 120), 60),
        ((450, 130), 55),
        ((400, 230), 58),
        ((200, 350), 52),
        ((340, 380), 56),
        ((480, 370), 54),
    ]

    for center, radius in coins:
        cv2.circle(img, center, radius, (100, 100, 100), -1)

    return img

def main():
    print("="*80)
    print("BÀI 4: ĐẾM ĐỒNG XU/VIÊN NÉN DÍNH NHAU - WATERSHED")
    print("="*80)

    # Tạo thư mục output
    os.makedirs('../output/bai-4-watershed', exist_ok=True)

    # Kiểm tra ảnh input
    input_path = '../input/coins/touching.jpg'
    if os.path.exists(input_path):
        print(f"\n[+] Đọc ảnh từ: {input_path}")
        img = cv2.imread(input_path)
    else:
        print(f"\n[!] Không tìm thấy ảnh input. Tạo ảnh mẫu...")
        os.makedirs('../input/coins', exist_ok=True)
        img = create_touching_coins()
        cv2.imwrite(input_path, img)
        print(f"[+] Đã tạo ảnh mẫu: {input_path}")

    print(f"[+] Kích thước ảnh: {img.shape}")

    # Chuyển sang grayscale
    print("\n" + "="*80)
    print("BƯỚC 1: CHUYỂN SANG GRAYSCALE VÀ NHỊ PHÂN HÓA")
    print("="*80)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"[+] Đã chuyển sang grayscale")

    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    print(f"[+] Đã nhị phân hóa Otsu (đảo ngược)")
    print(f"[+] Số pixel đối tượng: {np.sum(th == 255)}")

    # Opening để khử nhiễu
    print("\n" + "="*80)
    print("BƯỚC 2: OPENING ĐỂ KHỬ NHIỄU")
    print("="*80)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=2)
    print(f"[+] Thực hiện Opening với 2 iterations")

    # Sure background (dilate)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    print(f"[+] Tạo sure background (dilate 3 iterations)")
    print(f"[+] Pixels sure background: {np.sum(sure_bg == 255)}")

    # Distance Transform
    print("\n" + "="*80)
    print("BƯỚC 3: DISTANCE TRANSFORM")
    print("="*80)

    dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    print(f"[+] Tính Distance Transform (L2, mask size 5)")
    print(f"[+] Khoảng cách max: {dist.max():.2f}")
    print(f"[+] Khoảng cách min: {dist.min():.2f}")

    # Sure foreground
    print("\n" + "="*80)
    print("BƯỚC 4: XÁC ĐỊNH SURE FOREGROUND")
    print("="*80)

    _, sure_fg = cv2.threshold(dist, 0.5 * dist.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    print(f"[+] Threshold tại 50% khoảng cách max: {0.5 * dist.max():.2f}")
    print(f"[+] Pixels sure foreground: {np.sum(sure_fg == 255)}")

    # Unknown region
    unknown = cv2.subtract(sure_bg, sure_fg)
    print(f"[+] Pixels unknown: {np.sum(unknown == 255)}")

    # Connected Components
    print("\n" + "="*80)
    print("BƯỚC 5: CONNECTED COMPONENTS")
    print("="*80)

    _, markers = cv2.connectedComponents(sure_fg)
    print(f"[+] Số components ban đầu: {markers.max()}")

    # Tăng tất cả labels lên 1 (nền = 1)
    markers = markers + 1
    # Đánh dấu unknown = 0
    markers[unknown == 255] = 0
    print(f"[+] Đã chuẩn bị markers cho Watershed")

    # Watershed
    print("\n" + "="*80)
    print("BƯỚC 6: WATERSHED SEGMENTATION")
    print("="*80)

    markers = cv2.watershed(img, markers)
    print(f"[+] Đã thực hiện Watershed")

    # Đếm số đối tượng (trừ nền & biên)
    count = len(np.unique(markers)) - 2  # trừ nền & biên (-1)
    print(f"[+] Số đối tượng phát hiện: {count}")

    # Vẽ kết quả
    print("\n" + "="*80)
    print("BƯỚC 7: HIỂN THỊ KẾT QUẢ")
    print("="*80)

    # Tô màu các vùng
    img_result = img.copy()
    img_result[markers == -1] = [0, 0, 255]  # Biên màu đỏ

    # Hiển thị các bước trung gian
    plt.figure(figsize=(18, 10))

    plt.subplot(2, 4, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('1. Ảnh gốc')
    plt.axis('off')

    plt.subplot(2, 4, 2)
    plt.imshow(th, 'gray')
    plt.title('2. Nhị phân (INV)')
    plt.axis('off')

    plt.subplot(2, 4, 3)
    plt.imshow(opening, 'gray')
    plt.title('3. Opening')
    plt.axis('off')

    plt.subplot(2, 4, 4)
    plt.imshow(sure_bg, 'gray')
    plt.title('4. Sure BG')
    plt.axis('off')

    plt.subplot(2, 4, 5)
    plt.imshow(dist, 'jet')
    plt.title('5. Distance Transform')
    plt.colorbar()
    plt.axis('off')

    plt.subplot(2, 4, 6)
    plt.imshow(sure_fg, 'gray')
    plt.title('6. Sure FG')
    plt.axis('off')

    plt.subplot(2, 4, 7)
    plt.imshow(unknown, 'gray')
    plt.title('7. Unknown')
    plt.axis('off')

    plt.subplot(2, 4, 8)
    plt.imshow(cv2.cvtColor(img_result, cv2.COLOR_BGR2RGB))
    plt.title(f'8. Kết quả\n(Đếm: {count} đối tượng)')
    plt.axis('off')

    plt.tight_layout()
    output_path = '../output/bai-4-watershed/result.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"[+] Đã lưu kết quả: {output_path}")
    plt.show()

    # Lưu ảnh kết quả
    cv2.imwrite('../output/bai-4-watershed/segmented.png', img_result)
    cv2.imwrite('../output/bai-4-watershed/distance_transform.png',
                (dist / dist.max() * 255).astype(np.uint8))

    print("\n" + "="*80)
    print("PHÂN TÍCH KẾT QUẢ")
    print("="*80)
    print(f"""
    1. QUY TRÌNH WATERSHED:
       - Bước 1: Nhị phân hóa ảnh
       - Bước 2: Opening khử nhiễu
       - Bước 3: Distance Transform tìm tâm vật thể
       - Bước 4: Xác định Sure FG (chắc chắn là vật thể)
       - Bước 5: Xác định Sure BG (chắc chắn là nền)
       - Bước 6: Watershed phân đoạn vùng Unknown
       - Bước 7: Đếm số đối tượng

    2. KẾT QUẢ:
       - Tổng số đối tượng: {count}
       - Biên phân cách: Màu đỏ
       - Phương pháp: Watershed segmentation

    3. ƯU ĐIỂM:
       - Tách được các vật thể chạm nhau
       - Không cần biết trước số lượng
       - Hoạt động tốt với vật thể hình tròn

    4. ỨNG DỤNG:
       - Đếm đồng xu, viên nén
       - Phân tích tế bào y học
       - Kiểm tra chất lượng sản phẩm
    """)

    print("\n[✓] Hoàn thành!")

if __name__ == "__main__":
    main()
