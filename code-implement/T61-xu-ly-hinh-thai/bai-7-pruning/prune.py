"""
================================================================================
BÀI 7: XÓA PIXEL THỪA Ở CẠNH (PRUNING BẰNG HIT-OR-MISS)
================================================================================

Đề bài:
    Ảnh biên/skeleton còn gai (spurs), hãy xóa pixel thừa thành mép gọn.

Mục tiêu:
    Thực hiện yêu cầu "xóa các pixel thừa ở cạnh… nêu rõ SE & bước".

Yêu cầu:
    Dùng cv2.MORPH_HITMISS với bộ SE xoay 8 hướng.

Hướng dẫn:
    Chuẩn hóa nhị phân {0,1}; lặp hit-or-miss và trừ khỏi ảnh.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T61-78 Xử lý hình thái (trang 73-74)
================================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def create_jagged_edges():
    """Tạo ảnh biên có gai/spurs"""
    img = np.ones((400, 600), dtype=np.uint8) * 255

    # Vẽ các đường có gai
    # Đường ngang có gai
    cv2.line(img, (50, 100), (550, 100), 0, 2)
    # Thêm gai
    for x in range(100, 500, 30):
        cv2.line(img, (x, 100), (x + 5, 90), 0, 1)
        cv2.line(img, (x + 15, 100), (x + 18, 110), 0, 1)

    # Đường dọc có gai
    cv2.line(img, (300, 150), (300, 350), 0, 2)
    for y in range(180, 330, 25):
        cv2.line(img, (300, y), (290, y + 3), 0, 1)
        cv2.line(img, (300, y + 12), (310, y + 15), 0, 1)

    # Hình vuông có gai ở góc
    pts = np.array([[100, 250], [200, 250], [200, 350], [100, 350]], np.int32)
    cv2.polylines(img, [pts], True, 0, 2)
    # Gai ở các góc
    corners = [(100, 250), (200, 250), (200, 350), (100, 350)]
    for cx, cy in corners:
        cv2.line(img, (cx, cy), (cx + np.random.randint(-10, 10),
                                   cy + np.random.randint(-10, 10)), 0, 1)

    return img

def main():
    print("="*80)
    print("BÀI 7: XÓA PIXEL THỪA Ở CẠNH - PRUNING BẰNG HIT-OR-MISS")
    print("="*80)

    # Tạo thư mục output
    os.makedirs('../output/bai-7-pruning', exist_ok=True)

    # Kiểm tra ảnh input
    input_path = '../input/edges/jagged.png'
    if os.path.exists(input_path):
        print(f"\n[+] Đọc ảnh từ: {input_path}")
        img = cv2.imread(input_path, 0)
    else:
        print(f"\n[!] Không tìm thấy ảnh input. Tạo ảnh mẫu...")
        os.makedirs('../input/edges', exist_ok=True)
        img = create_jagged_edges()
        cv2.imwrite(input_path, img)
        print(f"[+] Đã tạo ảnh mẫu: {input_path}")

    print(f"[+] Kích thước ảnh: {img.shape}")

    # Nhị phân hóa và chuẩn hóa về {0,1}
    print("\n" + "="*80)
    print("BƯỚC 1: NHỊ PHÂN HÓA VÀ CHUẨN HÓA")
    print("="*80)

    _, bw = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(f"[+] Đã nhị phân hóa và chuẩn hóa về {{0,1}}")
    print(f"[+] Giá trị unique: {np.unique(bw)}")
    print(f"[+] Số pixel đối tượng (1): {np.sum(bw == 1)}")

    # Tạo các Structuring Elements cho pruning
    print("\n" + "="*80)
    print("BƯỚC 2: TẠO STRUCTURING ELEMENTS")
    print("="*80)

    SEs = []
    # SE cơ bản để phát hiện pixel đơn lẻ ở cạnh
    # -1 = don't care, 0 = must be 0, 1 = must be 1
    base = np.array([[0, 0, 0],
                     [-1, 1, -1],
                     [1, 1, 1]], dtype=np.int8)

    print("[+] SE cơ bản (phát hiện pixel thừa):")
    print(base)
    print("    0 = phải là 0 (nền)")
    print("    1 = phải là 1 (vật thể)")
    print("   -1 = don't care (không quan tâm)")

    # Xoay SE để tạo 8 hướng
    print("\n[+] Tạo 8 hướng xoay của SE:")
    for k in range(4):
        rotated = np.rot90(base, k)
        SEs.append(rotated)
        print(f"    - Xoay {k*90}°")

        flipped = np.rot90(np.fliplr(base), k)
        SEs.append(flipped)
        print(f"    - Xoay {k*90}° + flip")

    print(f"\n[+] Tổng số SE: {len(SEs)}")

    # Lưu ảnh trước pruning
    bw_before = bw.copy()
    pixels_before = np.sum(bw == 1)

    # Pruning lặp đi lặp lại
    print("\n" + "="*80)
    print("BƯỚC 3: THỰC HIỆN PRUNING")
    print("="*80)

    changed = True
    iteration = 0
    max_iterations = 10

    print("[+] Bắt đầu vòng lặp pruning...")

    while changed and iteration < max_iterations:
        iteration += 1
        before = bw.copy()

        removed_count = 0
        for idx, se in enumerate(SEs):
            hm = cv2.morphologyEx(bw.astype(np.uint8), cv2.MORPH_HITMISS, se)
            removed = np.sum(hm == 1)
            removed_count += removed

            # Xóa các pixel được hit
            bw = np.where(hm == 1, 0, bw)

        changed = np.any(before != bw)
        pixels_current = np.sum(bw == 1)

        print(f"    Iteration {iteration}: Xóa {removed_count} pixels, còn {pixels_current} pixels")

        if not changed:
            print(f"[+] Hội tụ sau {iteration} iterations")
            break

    if iteration >= max_iterations:
        print(f"[!] Đạt giới hạn {max_iterations} iterations")

    pixels_after = np.sum(bw == 1)
    pixels_removed = pixels_before - pixels_after

    print(f"\n[+] KẾT QUẢ PRUNING:")
    print(f"    - Pixels trước: {pixels_before}")
    print(f"    - Pixels sau: {pixels_after}")
    print(f"    - Pixels đã xóa: {pixels_removed}")
    print(f"    - Tỷ lệ xóa: {pixels_removed/pixels_before*100:.2f}%")

    # Lưu ảnh kết quả
    print("\n" + "="*80)
    print("BƯỚC 4: LƯU KẾT QUẢ")
    print("="*80)

    pruned_img = (bw * 255).astype('uint8')
    cv2.imwrite('../output/bai-7-pruning/pruned.png', pruned_img)
    print(f"[+] Đã lưu ảnh pruned")

    # Hiển thị kết quả
    print("\n" + "="*80)
    print("BƯỚC 5: HIỂN THỊ KẾT QUẢ")
    print("="*80)

    fig = plt.figure(figsize=(18, 10))

    # Ảnh gốc
    plt.subplot(2, 3, 1)
    plt.imshow(img, 'gray')
    plt.title('1. Ảnh gốc')
    plt.axis('off')

    # Nhị phân trước pruning
    plt.subplot(2, 3, 2)
    plt.imshow(bw_before * 255, 'gray')
    plt.title(f'2. Trước pruning\n({pixels_before} pixels)')
    plt.axis('off')

    # Sau pruning
    plt.subplot(2, 3, 3)
    plt.imshow(bw * 255, 'gray')
    plt.title(f'3. Sau pruning\n({pixels_after} pixels)')
    plt.axis('off')

    # Pixels bị xóa
    plt.subplot(2, 3, 4)
    diff = bw_before - bw
    plt.imshow(diff * 255, 'hot')
    plt.title(f'4. Pixels đã xóa\n({pixels_removed} pixels)')
    plt.colorbar()
    plt.axis('off')

    # Overlay so sánh
    plt.subplot(2, 3, 5)
    overlay = np.zeros((*bw.shape, 3), dtype=np.uint8)
    overlay[bw_before == 1] = [255, 0, 0]  # Trước: đỏ
    overlay[bw == 1] = [0, 255, 0]  # Sau: xanh
    overlay[(bw_before == 1) & (bw == 1)] = [255, 255, 0]  # Giữ nguyên: vàng
    plt.imshow(overlay)
    plt.title('5. So sánh\n(Đỏ=xóa, Vàng=giữ, Xanh=sau)')
    plt.axis('off')

    # Hiển thị một số SE
    plt.subplot(2, 3, 6)
    plt.text(0.1, 0.9, 'Một số SE được sử dụng:', fontsize=12, weight='bold')

    se_strs = []
    for i in [0, 2, 4]:
        se_str = f"\nSE {i+1} (hướng {i*45}°):\n"
        se = SEs[i]
        for row in se:
            se_str += "  " + " ".join([
                "." if x == -1 else str(x) for x in row
            ]) + "\n"
        se_strs.append(se_str)

    plt.text(0.1, 0.1, "\n".join(se_strs), fontsize=9, family='monospace',
             verticalalignment='bottom')
    plt.axis('off')

    plt.tight_layout()
    output_path = '../output/bai-7-pruning/result.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"[+] Đã lưu kết quả: {output_path}")
    plt.show()

    # Zoom vào một vùng để thấy rõ
    print("\n" + "="*80)
    print("BƯỚC 6: ZOOM CHI TIẾT")
    print("="*80)

    # Chọn vùng có nhiều thay đổi
    y, x = np.where(diff == 1)
    if len(x) > 0 and len(y) > 0:
        cx, cy = int(np.mean(x)), int(np.mean(y))
        size = 50
        x1, x2 = max(0, cx - size), min(bw.shape[1], cx + size)
        y1, y2 = max(0, cy - size), min(bw.shape[0], cy + size)

        fig, axes = plt.subplots(1, 2, figsize=(12, 6))

        axes[0].imshow(bw_before[y1:y2, x1:x2] * 255, 'gray', interpolation='nearest')
        axes[0].set_title('Trước pruning (zoom)')
        axes[0].axis('off')
        axes[0].grid(True, alpha=0.3)

        axes[1].imshow(bw[y1:y2, x1:x2] * 255, 'gray', interpolation='nearest')
        axes[1].set_title('Sau pruning (zoom)')
        axes[1].axis('off')
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('../output/bai-7-pruning/zoom_detail.png', dpi=150, bbox_inches='tight')
        print(f"[+] Đã lưu zoom chi tiết")
        plt.show()

    print("\n" + "="*80)
    print("PHÂN TÍCH KẾT QUẢ")
    print("="*80)
    print(f"""
    1. PHƯƠNG PHÁP PRUNING:
       - Sử dụng Hit-or-Miss Transform
       - SE phát hiện pixel đơn lẻ ở cạnh (spurs)
       - Xoay SE theo 8 hướng để phát hiện đầy đủ
       - Lặp đi lặp lại cho đến khi hội tụ

    2. STRUCTURING ELEMENT:
       - 0: Pixel phải là nền
       - 1: Pixel phải là vật thể
       - -1: Don't care (không quan tâm)

    3. KẾT QUẢ:
       - Iterations: {iteration}
       - Pixels xóa: {pixels_removed}
       - Tỷ lệ: {pixels_removed/pixels_before*100:.2f}%

    4. ỨNG DỤNG:
       - Làm mịn skeleton
       - Xóa nhiễu cạnh
       - Tinh chỉnh biên
       - Chuẩn bị cho nhận dạng
    """)

    print("\n[✓] Hoàn thành!")

if __name__ == "__main__":
    main()
