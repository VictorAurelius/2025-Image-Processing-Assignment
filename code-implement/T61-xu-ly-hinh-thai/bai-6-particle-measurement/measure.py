"""
================================================================================
BÀI 6: ĐO ĐƯỜNG KÍNH HẠT/LỖ TRÊN BỀ MẶT (MORPHOLOGY + ĐO ĐẠC)
================================================================================

Đề bài:
    Ảnh bề mặt có lỗ/hạt; hãy phân cụm theo kích thước (nhỏ–vừa–lớn).

Mục tiêu:
    Gắn với bài tập "đếm hình tròn theo 3 nhóm kích thước".

Yêu cầu:
    Tính diện tích contour, chia ngưỡng 3 nhóm, đếm từng nhóm.

Hướng dẫn:
    Closing để làm tròn; findContours → diện tích.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T61-78 Xử lý hình thái (trang 71-72)
================================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def create_holes_image():
    """Tạo ảnh bề mặt có lỗ/hạt nhiều kích thước"""
    img = np.ones((500, 600), dtype=np.uint8) * 255

    # Tạo các lỗ/hạt với kích thước khác nhau
    # Nhóm nhỏ (r = 10-20)
    small_positions = [
        (50, 50, 10), (100, 60, 12), (150, 55, 15),
        (80, 120, 11), (130, 130, 13), (180, 125, 14),
        (60, 190, 12), (110, 200, 10), (160, 195, 11)
    ]

    # Nhóm vừa (r = 25-35)
    medium_positions = [
        (300, 80, 25), (400, 90, 28), (500, 85, 30),
        (320, 200, 27), (420, 210, 32), (520, 205, 29),
        (350, 320, 26), (450, 330, 31), (550, 325, 28)
    ]

    # Nhóm lớn (r = 40-55)
    large_positions = [
        (100, 350, 40), (250, 360, 45), (400, 355, 50),
        (180, 450, 42), (330, 455, 48), (480, 450, 52)
    ]

    # Vẽ các lỗ (màu đen)
    all_positions = small_positions + medium_positions + large_positions
    for x, y, r in all_positions:
        cv2.circle(img, (x, y), r, 0, -1)

    return img

def main():
    print("="*80)
    print("BÀI 6: ĐO ĐƯỜNG KÍNH HẠT/LỖ TRÊN BỀ MẶT")
    print("="*80)

    # Tạo thư mục output
    os.makedirs('../output/bai-6-particle-measurement', exist_ok=True)

    # Kiểm tra ảnh input
    input_path = '../input/surface/holes.png'
    if os.path.exists(input_path):
        print(f"\n[+] Đọc ảnh từ: {input_path}")
        img = cv2.imread(input_path, 0)
    else:
        print(f"\n[!] Không tìm thấy ảnh input. Tạo ảnh mẫu...")
        os.makedirs('../input/surface', exist_ok=True)
        img = create_holes_image()
        cv2.imwrite(input_path, img)
        print(f"[+] Đã tạo ảnh mẫu: {input_path}")

    print(f"[+] Kích thước ảnh: {img.shape}")

    # Nhị phân hóa Otsu (đảo ngược)
    print("\n" + "="*80)
    print("BƯỚC 1: NHỊ PHÂN HÓA OTSU")
    print("="*80)

    _, bw = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    print(f"[+] Đã nhị phân hóa Otsu (lỗ = trắng)")
    print(f"[+] Số pixel lỗ: {np.sum(bw == 255)}")

    # Closing để làm tròn
    print("\n" + "="*80)
    print("BƯỚC 2: CLOSING ĐỂ LÀM TRÒN")
    print("="*80)

    kernel = np.ones((3, 3), np.uint8)
    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel, iterations=2)
    print(f"[+] Thực hiện Closing với 2 iterations")
    print(f"[+] Mục đích: Làm tròn các lỗ, loại bỏ nhiễu")

    # Tìm contours
    print("\n" + "="*80)
    print("BƯỚC 3: TÌM VÀ ĐO ĐẠC CONTOURS")
    print("="*80)

    contours, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"[+] Tìm được {len(contours)} contours")

    # Tính diện tích và sắp xếp
    areas = sorted([cv2.contourArea(c) for c in contours])
    print(f"[+] Diện tích min: {min(areas):.2f}")
    print(f"[+] Diện tích max: {max(areas):.2f}")
    print(f"[+] Diện tích trung bình: {np.mean(areas):.2f}")

    # Phân cụm theo percentile
    print("\n" + "="*80)
    print("BƯỚC 4: PHÂN CỤM THEO KÍCH THƯỚC")
    print("="*80)

    t1, t2 = np.percentile(areas, [33, 66])
    print(f"[+] Ngưỡng phân chia:")
    print(f"    - Nhỏ/Vừa (33%): {t1:.2f}")
    print(f"    - Vừa/Lớn (66%): {t2:.2f}")

    small = sum(a <= t1 for a in areas)
    mid = sum((a > t1) & (a <= t2) for a in areas)
    big = sum(a > t2 for a in areas)

    print(f"\n[+] Kết quả phân loại:")
    print(f"    - Nhỏ: {small} hạt (diện tích ≤ {t1:.2f})")
    print(f"    - Vừa: {mid} hạt ({t1:.2f} < diện tích ≤ {t2:.2f})")
    print(f"    - Lớn: {big} hạt (diện tích > {t2:.2f})")

    # Vẽ kết quả với màu phân loại
    print("\n" + "="*80)
    print("BƯỚC 5: VẼ KẾT QUẢ PHÂN LOẠI")
    print("="*80)

    img_result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    for c in contours:
        area = cv2.contourArea(c)

        # Phân loại và chọn màu
        if area <= t1:
            color = (0, 255, 0)  # Xanh lá - Nhỏ
            label = "S"
        elif area <= t2:
            color = (0, 165, 255)  # Cam - Vừa
            label = "M"
        else:
            color = (0, 0, 255)  # Đỏ - Lớn
            label = "L"

        # Vẽ contour
        cv2.drawContours(img_result, [c], -1, color, 2)

        # Tính tâm và bán kính
        M = cv2.moments(c)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            radius = np.sqrt(area / np.pi)

            # Vẽ label
            cv2.putText(img_result, f"{label}", (cx - 10, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    print(f"[+] Đã vẽ {len(contours)} contours với màu phân loại")

    # Hiển thị kết quả
    print("\n" + "="*80)
    print("BƯỚC 6: HIỂN THỊ KẾT QUẢ")
    print("="*80)

    # Tạo histogram phân bố diện tích
    fig = plt.figure(figsize=(18, 10))

    # Ảnh gốc
    plt.subplot(2, 3, 1)
    plt.imshow(img, 'gray')
    plt.title('1. Ảnh gốc')
    plt.axis('off')

    # Nhị phân
    plt.subplot(2, 3, 2)
    plt.imshow(bw, 'gray')
    plt.title('2. Nhị phân + Closing')
    plt.axis('off')

    # Histogram diện tích
    plt.subplot(2, 3, 3)
    plt.hist(areas, bins=30, edgecolor='black', alpha=0.7)
    plt.axvline(t1, color='g', linestyle='--', label=f'33% ({t1:.0f})')
    plt.axvline(t2, color='orange', linestyle='--', label=f'66% ({t2:.0f})')
    plt.xlabel('Diện tích (pixels)')
    plt.ylabel('Số lượng')
    plt.title('3. Phân bố diện tích')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Kết quả phân loại
    plt.subplot(2, 3, 4)
    plt.imshow(cv2.cvtColor(img_result, cv2.COLOR_BGR2RGB))
    plt.title(f'4. Phân loại\n(S:{small}, M:{mid}, L:{big})')
    plt.axis('off')

    # Biểu đồ cột
    plt.subplot(2, 3, 5)
    categories = ['Nhỏ', 'Vừa', 'Lớn']
    counts = [small, mid, big]
    colors = ['green', 'orange', 'red']
    bars = plt.bar(categories, counts, color=colors, alpha=0.7, edgecolor='black')
    plt.ylabel('Số lượng')
    plt.title('5. Thống kê phân loại')
    plt.grid(True, alpha=0.3, axis='y')

    # Thêm giá trị lên cột
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')

    # Scatter plot diện tích vs chu vi
    plt.subplot(2, 3, 6)
    for c in contours:
        area = cv2.contourArea(c)
        perimeter = cv2.arcLength(c, True)

        if area <= t1:
            color = 'green'
        elif area <= t2:
            color = 'orange'
        else:
            color = 'red'

        plt.scatter(area, perimeter, c=color, s=50, alpha=0.6)

    plt.xlabel('Diện tích (pixels)')
    plt.ylabel('Chu vi (pixels)')
    plt.title('6. Diện tích vs Chu vi')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = '../output/bai-6-particle-measurement/result.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"[+] Đã lưu kết quả: {output_path}")
    plt.show()

    # Lưu ảnh kết quả
    cv2.imwrite('../output/bai-6-particle-measurement/classified.png', img_result)

    # Lưu thống kê chi tiết
    print("\n" + "="*80)
    print("BƯỚC 7: THỐNG KÊ CHI TIẾT")
    print("="*80)

    stats_file = '../output/bai-6-particle-measurement/statistics.txt'
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write("THỐNG KÊ ĐO ĐẠC HẠT/LỖ\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Tổng số lỗ/hạt: {len(contours)}\n\n")

        f.write(f"PHÂN LOẠI:\n")
        f.write(f"  - Nhỏ: {small} hạt ({small/len(contours)*100:.1f}%)\n")
        f.write(f"  - Vừa: {mid} hạt ({mid/len(contours)*100:.1f}%)\n")
        f.write(f"  - Lớn: {big} hạt ({big/len(contours)*100:.1f}%)\n\n")

        f.write(f"DIỆN TÍCH:\n")
        f.write(f"  - Min: {min(areas):.2f} px²\n")
        f.write(f"  - Max: {max(areas):.2f} px²\n")
        f.write(f"  - Trung bình: {np.mean(areas):.2f} px²\n")
        f.write(f"  - Độ lệch chuẩn: {np.std(areas):.2f} px²\n\n")

        f.write(f"CHI TIẾT TỪNG HẠT:\n")
        f.write(f"{'ID':<5} {'Diện tích':<12} {'Chu vi':<12} {'Nhóm':<8}\n")
        f.write("-" * 45 + "\n")

        for idx, c in enumerate(contours, 1):
            area = cv2.contourArea(c)
            perimeter = cv2.arcLength(c, True)

            if area <= t1:
                group = "Nhỏ"
            elif area <= t2:
                group = "Vừa"
            else:
                group = "Lớn"

            f.write(f"{idx:<5} {area:<12.2f} {perimeter:<12.2f} {group:<8}\n")

    print(f"[+] Đã lưu thống kê chi tiết: {stats_file}")

    print("\n" + "="*80)
    print("PHÂN TÍCH KẾT QUẢ")
    print("="*80)
    print(f"""
    1. QUY TRÌNH ĐO ĐẠC:
       - Nhị phân hóa Otsu
       - Closing để làm tròn và loại nhiễu
       - Tìm contours
       - Tính diện tích từng contour
       - Phân cụm theo percentile (33%, 66%)

    2. KẾT QUẢ PHÂN LOẠI:
       - Nhỏ (S): {small} hạt - Màu xanh lá
       - Vừa (M): {mid} hạt - Màu cam
       - Lớn (L): {big} hạt - Màu đỏ
       - Tổng: {len(contours)} hạt

    3. THỐNG KÊ:
       - Diện tích min: {min(areas):.2f} px²
       - Diện tích max: {max(areas):.2f} px²
       - Diện tích TB: {np.mean(areas):.2f} px²

    4. ỨNG DỤNG:
       - Kiểm tra chất lượng bề mặt
       - Phân tích vật liệu
       - Đo đạc hạt trong y sinh
       - Kiểm soát sản xuất
    """)

    print("\n[✓] Hoàn thành!")

if __name__ == "__main__":
    main()
