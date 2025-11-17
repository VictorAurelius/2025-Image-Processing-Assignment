"""
================================================================================
BÀI 8: TÁCH TIỀN CẢNH TRONG ẢNH CÔNG NGHIỆP (FOREGROUND = OBJ − EROSION)
================================================================================

Đề bài:
    Từ ảnh băng chuyền có vật thể trên nền, tách vùng tiền cảnh ổn định.

Mục tiêu:
    Dùng xói mòn để xấp xỉ "core" của đối tượng, rồi lấy hiệu để ra biên/tiền cảnh
    (liên hệ tách biên A − (A ⊖ B) trong bài tập 7).

Yêu cầu:
    Trả 2 lớp: core và rim.

Hướng dẫn:
    core = erode(A,B); rim = A - core.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T61-78 Xử lý hình thái (trang 75-76)
================================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def create_conveyor_items():
    """Tạo ảnh băng chuyền với các vật thể"""
    img = np.ones((500, 700), dtype=np.uint8) * 200  # Nền xám

    # Vẽ các vật thể khác nhau
    # Hình chữ nhật
    cv2.rectangle(img, (50, 100), (200, 250), 255, -1)
    cv2.rectangle(img, (50, 100), (200, 250), 180, 3)  # Viền

    # Hình tròn
    cv2.circle(img, (350, 175), 80, 255, -1)
    cv2.circle(img, (350, 175), 80, 180, 3)  # Viền

    # Hình elip
    cv2.ellipse(img, (550, 175), (70, 50), 0, 0, 360, 255, -1)
    cv2.ellipse(img, (550, 175), (70, 50), 0, 0, 360, 180, 3)  # Viền

    # Hình tam giác
    pts = np.array([[125, 350], [225, 350], [175, 450]], np.int32)
    cv2.fillPoly(img, [pts], 255)
    cv2.polylines(img, [pts], True, 180, 3)  # Viền

    # Hình ngũ giác
    center = (400, 400)
    radius = 70
    angles = np.linspace(0, 2*np.pi, 6)
    pts = np.array([[center[0] + int(radius * np.cos(a)),
                     center[1] + int(radius * np.sin(a))] for a in angles], np.int32)
    cv2.fillPoly(img, [pts], 255)
    cv2.polylines(img, [pts], True, 180, 3)  # Viền

    # Thêm một số nhiễu nhỏ
    noise = np.random.normal(0, 10, img.shape)
    img = np.clip(img + noise, 0, 255).astype(np.uint8)

    return img

def main():
    print("="*80)
    print("BÀI 8: TÁCH TIỀN CẢNH TRONG ẢNH CÔNG NGHIỆP")
    print("="*80)

    # Tạo thư mục output
    os.makedirs('../output/bai-8-foreground-extraction', exist_ok=True)

    # Kiểm tra ảnh input
    input_path = '../input/conveyor/items.png'
    if os.path.exists(input_path):
        print(f"\n[+] Đọc ảnh từ: {input_path}")
        img = cv2.imread(input_path, 0)
    else:
        print(f"\n[!] Không tìm thấy ảnh input. Tạo ảnh mẫu...")
        os.makedirs('../input/conveyor', exist_ok=True)
        img = create_conveyor_items()
        cv2.imwrite(input_path, img)
        print(f"[+] Đã tạo ảnh mẫu: {input_path}")

    print(f"[+] Kích thước ảnh: {img.shape}")

    # Nhị phân hóa Otsu
    print("\n" + "="*80)
    print("BƯỚC 1: NHỊ PHÂN HÓA OTSU")
    print("="*80)

    _, A = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(f"[+] Đã nhị phân hóa Otsu")
    print(f"[+] Số pixel vật thể: {np.sum(A == 255)}")
    print(f"[+] Tỷ lệ vật thể: {np.sum(A == 255) / A.size * 100:.2f}%")

    # Tạo Structuring Element
    print("\n" + "="*80)
    print("BƯỚC 2: TẠO STRUCTURING ELEMENT")
    print("="*80)

    B = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    print(f"[+] Tạo SE ELLIPSE 5x5")
    print(f"[+] Shape: {B.shape}")
    print("[+] SE:")
    print(B)

    # Erosion để tạo core
    print("\n" + "="*80)
    print("BƯỚC 3: EROSION ĐỂ TẠO CORE")
    print("="*80)

    core = cv2.erode(A, B)
    print(f"[+] Đã thực hiện Erosion")
    print(f"[+] Số pixel core: {np.sum(core == 255)}")
    print(f"[+] Tỷ lệ core/vật thể: {np.sum(core == 255) / np.sum(A == 255) * 100:.2f}%")

    # Tách rim (biên/tiền cảnh)
    print("\n" + "="*80)
    print("BƯỚC 4: TÁCH RIM (BIÊN)")
    print("="*80)

    rim = cv2.subtract(A, core)
    print(f"[+] Đã tính rim = A - core")
    print(f"[+] Số pixel rim: {np.sum(rim == 255)}")
    print(f"[+] Tỷ lệ rim/vật thể: {np.sum(rim == 255) / np.sum(A == 255) * 100:.2f}%")

    # Lưu kết quả
    print("\n" + "="*80)
    print("BƯỚC 5: LƯU KẾT QUẢ")
    print("="*80)

    cv2.imwrite('../output/bai-8-foreground-extraction/core.png', core)
    cv2.imwrite('../output/bai-8-foreground-extraction/rim.png', rim)
    print(f"[+] Đã lưu core và rim")

    # Phân tích với kernel khác nhau
    print("\n" + "="*80)
    print("BƯỚC 6: SO SÁNH KERNEL KHÁC NHAU")
    print("="*80)

    kernel_sizes = [3, 5, 7, 9]
    results = []

    for k in kernel_sizes:
        B_test = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
        core_test = cv2.erode(A, B_test)
        rim_test = cv2.subtract(A, core_test)

        core_pixels = np.sum(core_test == 255)
        rim_pixels = np.sum(rim_test == 255)

        results.append({
            'size': k,
            'core': core_test,
            'rim': rim_test,
            'core_pixels': core_pixels,
            'rim_pixels': rim_pixels
        })

        print(f"\nKernel {k}x{k}:")
        print(f"  - Core pixels: {core_pixels}")
        print(f"  - Rim pixels: {rim_pixels}")
        print(f"  - Tỷ lệ rim/core: {rim_pixels/core_pixels if core_pixels > 0 else 0:.2f}")

    # Hiển thị kết quả
    print("\n" + "="*80)
    print("BƯỚC 7: HIỂN THỊ KẾT QUẢ")
    print("="*80)

    fig = plt.figure(figsize=(18, 12))

    # Hàng 1: Quy trình với kernel 5x5
    plt.subplot(3, 4, 1)
    plt.imshow(img, 'gray')
    plt.title('1. Ảnh gốc')
    plt.axis('off')

    plt.subplot(3, 4, 2)
    plt.imshow(A, 'gray')
    plt.title(f'2. Nhị phân (A)\n{np.sum(A==255)} pixels')
    plt.axis('off')

    plt.subplot(3, 4, 3)
    plt.imshow(core, 'gray')
    plt.title(f'3. Core (A⊖B)\n{np.sum(core==255)} pixels')
    plt.axis('off')

    plt.subplot(3, 4, 4)
    plt.imshow(rim, 'gray')
    plt.title(f'4. Rim (A-core)\n{np.sum(rim==255)} pixels')
    plt.axis('off')

    # Hàng 2: So sánh kernel khác nhau (Core)
    for idx, res in enumerate(results, 5):
        plt.subplot(3, 4, idx)
        plt.imshow(res['core'], 'gray')
        plt.title(f'Core {res["size"]}x{res["size"]}\n{res["core_pixels"]} px')
        plt.axis('off')

    # Hàng 3: So sánh kernel khác nhau (Rim)
    for idx, res in enumerate(results, 9):
        plt.subplot(3, 4, idx)
        plt.imshow(res['rim'], 'gray')
        plt.title(f'Rim {res["size"]}x{res["size"]}\n{res["rim_pixels"]} px')
        plt.axis('off')

    plt.tight_layout()
    output_path = '../output/bai-8-foreground-extraction/result.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"[+] Đã lưu kết quả: {output_path}")
    plt.show()

    # Tạo ảnh overlay màu
    print("\n" + "="*80)
    print("BƯỚC 8: TẠO OVERLAY MÀU SẮC")
    print("="*80)

    overlay = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Tô màu core (xanh lam)
    overlay[core == 255] = [255, 200, 0]

    # Tô màu rim (xanh lá)
    overlay[rim == 255] = [0, 255, 0]

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    axes[0].imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
    axes[0].set_title('Core (xanh lam) + Rim (xanh lá)')
    axes[0].axis('off')

    axes[1].imshow(core, 'Blues')
    axes[1].set_title('Core (xanh lam)')
    axes[1].axis('off')

    axes[2].imshow(rim, 'Greens')
    axes[2].set_title('Rim (xanh lá)')
    axes[2].axis('off')

    plt.tight_layout()
    plt.savefig('../output/bai-8-foreground-extraction/overlay.png', dpi=150, bbox_inches='tight')
    print(f"[+] Đã lưu overlay màu")
    plt.show()

    cv2.imwrite('../output/bai-8-foreground-extraction/overlay_color.png', overlay)

    # Thống kê chi tiết
    print("\n" + "="*80)
    print("BƯỚC 9: THỐNG KÊ CHI TIẾT")
    print("="*80)

    # Tính độ dày trung bình của rim
    rim_thickness = []
    for res in results:
        thickness = res['rim_pixels'] / (np.sum(res['core'] == 255) + res['rim_pixels'])
        rim_thickness.append(thickness)

    # Vẽ biểu đồ
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Biểu đồ pixel count
    axes[0].plot([r['size'] for r in results], [r['core_pixels'] for r in results],
                 'o-', label='Core', linewidth=2, markersize=8)
    axes[0].plot([r['size'] for r in results], [r['rim_pixels'] for r in results],
                 's-', label='Rim', linewidth=2, markersize=8)
    axes[0].set_xlabel('Kernel size')
    axes[0].set_ylabel('Số pixels')
    axes[0].set_title('Ảnh hưởng của kernel size')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Biểu đồ tỷ lệ
    axes[1].plot([r['size'] for r in results], rim_thickness,
                 'D-', color='purple', linewidth=2, markersize=8)
    axes[1].set_xlabel('Kernel size')
    axes[1].set_ylabel('Tỷ lệ rim/(core+rim)')
    axes[1].set_title('Độ dày tương đối của rim')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('../output/bai-8-foreground-extraction/statistics.png', dpi=150, bbox_inches='tight')
    print(f"[+] Đã lưu biểu đồ thống kê")
    plt.show()

    print("\n" + "="*80)
    print("PHÂN TÍCH KẾT QUẢ")
    print("="*80)
    print(f"""
    1. PHƯƠNG PHÁP TÁCH TIỀN CẢNH:
       - Core = Erosion(A, B): Phần trung tâm ổn định
       - Rim = A - Core: Phần biên/tiền cảnh
       - Công thức: Rim = A - (A ⊖ B)

    2. KẾT QUẢ VỚI KERNEL 5x5:
       - Tổng pixels vật thể: {np.sum(A == 255)}
       - Core pixels: {np.sum(core == 255)} ({np.sum(core == 255)/np.sum(A == 255)*100:.1f}%)
       - Rim pixels: {np.sum(rim == 255)} ({np.sum(rim == 255)/np.sum(A == 255)*100:.1f}%)

    3. ẢNH HƯỞNG KERNEL SIZE:
       - Kernel nhỏ (3x3): Rim mỏng, core lớn
       - Kernel vừa (5x5): Cân bằng
       - Kernel lớn (7x7, 9x9): Rim dày, core nhỏ

    4. ỨNG DỤNG:
       - Phân tích vật thể trên băng chuyền
       - Tách biên để kiểm tra chất lượng
       - Phát hiện khuyết tật bề mặt
       - Định vị chính xác vật thể
       - Tách foreground/background
    """)

    print("\n[✓] Hoàn thành!")

if __name__ == "__main__":
    main()
