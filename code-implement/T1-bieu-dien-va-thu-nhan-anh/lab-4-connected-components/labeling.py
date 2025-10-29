"""
Lab 4 — Lân cận & gán nhãn thành phần liên thông (4 vs 8)
Mục tiêu: Thấy ảnh hưởng của lựa chọn lân cận lên số lượng thành phần liên thông

Bước làm:
- Nhị phân hoá ảnh (Otsu)
- Gán nhãn connectedComponents với connectivity=4 và 8
- So sánh số thành phần, trực quan hoá bằng màu giả

Tác giả: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
import os

if __name__ == "__main__":
    # Đường dẫn file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "pcb.png")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")

        # Tạo ảnh mạch in mẫu
        img = np.ones((400, 600), dtype=np.uint8) * 255

        # Vẽ các đường mạch
        cv2.line(img, (50, 50), (250, 50), 0, 3)
        cv2.line(img, (100, 50), (100, 150), 0, 3)
        cv2.line(img, (200, 50), (200, 150), 0, 3)

        # Vẽ các điểm nối
        for x in [50, 100, 150, 200, 250]:
            cv2.circle(img, (x, 50), 8, 0, -1)

        # Vẽ đường chéo (test connectivity)
        for i in range(20):
            cv2.circle(img, (350 + i*5, 100 + i*5), 2, 0, -1)

        # Vẽ các hình nhỏ rời rạc
        cv2.rectangle(img, (400, 200), (450, 250), 0, -1)
        cv2.circle(img, (500, 225), 25, 0, -1)

        # Vẽ text
        cv2.putText(img, "PCB", (250, 350),
                   cv2.FONT_HERSHEY_SIMPLEX, 2, 0, 3)

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Đọc ảnh
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    print("="*70)
    print("LAB 4: GÁN NHÃN THÀNH PHẦN LIÊN THÔNG")
    print("="*70)
    print(f"Ảnh gốc: {img.shape}")

    # Nhị phân hóa bằng Otsu
    _, bw = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Lưu ảnh nhị phân
    bw_path = os.path.join(output_dir, "binary_otsu.png")
    cv2.imwrite(bw_path, bw)
    print(f"Ảnh nhị phân: {bw_path}")

    # Đếm số pixel trắng và đen
    white_pixels = np.sum(bw == 255)
    black_pixels = np.sum(bw == 0)
    print(f"Pixel trắng: {white_pixels} ({white_pixels/bw.size*100:.1f}%)")
    print(f"Pixel đen: {black_pixels} ({black_pixels/bw.size*100:.1f}%)")

    print("\n" + "="*70)
    print("GÁN NHÃN VỚI CONNECTIVITY 4 và 8")
    print("="*70)

    results = {}

    for conn in [4, 8]:
        print(f"\n--- Connectivity {conn} ---")

        # Gán nhãn
        num, labels = cv2.connectedComponents(bw, connectivity=conn)

        print(f"Số thành phần liên thông: {num} (bao gồm background)")
        print(f"Số đối tượng: {num - 1}")

        # Đếm kích thước mỗi component
        unique, counts = np.unique(labels, return_counts=True)
        print(f"Kích thước các component:")
        for label_id, count in zip(unique[:10], counts[:10]):  # Chỉ in 10 đầu
            if label_id == 0:
                print(f"  Label {label_id} (background): {count} pixels")
            else:
                print(f"  Label {label_id}: {count} pixels")
        if len(unique) > 10:
            print(f"  ... và {len(unique)-10} components khác")

        # Gán màu giả để xem
        lab_norm = (labels / (labels.max() + 1e-6) * 255).astype(np.uint8)
        color = cv2.applyColorMap(lab_norm, cv2.COLORMAP_JET)

        # Làm cho background thành trắng
        color[labels == 0] = [255, 255, 255]

        # Lưu kết quả
        color_path = os.path.join(output_dir, f"labels_conn{conn}.png")
        cv2.imwrite(color_path, color)
        print(f"Đã lưu: {color_path}")

        # Lưu labels map (grayscale)
        labels_path = os.path.join(output_dir, f"labels_conn{conn}_gray.png")
        cv2.imwrite(labels_path, lab_norm)

        results[conn] = {
            'num_components': num,
            'labels': labels,
            'sizes': dict(zip(unique, counts))
        }

    # So sánh
    print("\n" + "="*70)
    print("SO SÁNH KẾT QUẢ")
    print("="*70)

    num_4 = results[4]['num_components']
    num_8 = results[8]['num_components']

    print(f"4-connectivity: {num_4} components")
    print(f"8-connectivity: {num_8} components")
    print(f"Chênh lệch: {abs(num_4 - num_8)} components")

    if num_4 > num_8:
        print(f"\n4-connectivity có NHIỀU HƠN {num_4 - num_8} components")
        print("Lý do: Các pixel chéo không được coi là liên thông")
    elif num_8 > num_4:
        print(f"\n8-connectivity có NHIỀU HƠN {num_8 - num_4} components")
        print("Lưu ý: Trường hợp này hiếm gặp")
    else:
        print("\nSố components BẰNG NHAU")
        print("Lý do: Không có đường chéo ảnh hưởng đến kết quả")

    # Phân tích chi tiết
    print("\nPhân tích chi tiết:")
    labels_4 = results[4]['labels']
    labels_8 = results[8]['labels']

    # Tìm vị trí khác nhau
    diff = (labels_4 != labels_8)
    num_diff_pixels = np.sum(diff)

    print(f"Số pixel có label khác nhau: {num_diff_pixels} ({num_diff_pixels/diff.size*100:.2f}%)")

    # Vẽ ảnh khác biệt
    diff_img = np.zeros_like(img)
    diff_img[diff] = 255

    diff_path = os.path.join(output_dir, "difference_4vs8.png")
    cv2.imwrite(diff_path, diff_img)
    print(f"Ảnh khác biệt: {diff_path}")

    # Statistics
    print("\nThống kê kích thước components:")
    for conn in [4, 8]:
        sizes = list(results[conn]['sizes'].values())[1:]  # Bỏ background
        if sizes:
            print(f"\n{conn}-connectivity:")
            print(f"  Min size: {min(sizes)} pixels")
            print(f"  Max size: {max(sizes)} pixels")
            print(f"  Mean size: {np.mean(sizes):.1f} pixels")
            print(f"  Median size: {np.median(sizes):.1f} pixels")

    print("\n" + "="*70)
    print("KẾT LUẬN")
    print("="*70)
    print("""
1. Ảnh hưởng của connectivity:
   - 4-connectivity: Chỉ xét 4 láng giềng (trên, dưới, trái, phải)
     → Số components thường NHIỀU HƠN
     → Các đường chéo bị tách rời

   - 8-connectivity: Xét cả 8 láng giềng (thêm 4 góc chéo)
     → Số components thường ÍT HƠN
     → Các đường chéo được kết nối

2. Ứng dụng:
   - 4-connectivity: Phù hợp khi đối tượng không có kết nối chéo
     Ví dụ: Text, mạch in có đường thẳng

   - 8-connectivity: Phù hợp cho hầu hết trường hợp
     Ví dụ: Phát hiện đối tượng, phân vùng ảnh

3. Lưu ý:
   - Connectivity càng cao → càng ít components
   - Cần chọn phù hợp với bài toán cụ thể
   - Có thể dùng morphology để xử lý trước (đóng các khe hở)

4. m-connectivity:
   - Hạn chế kết nối chéo khi có khe hở
   - Tránh "xuyên tường" giữa các đối tượng
   - OpenCV không hỗ trợ trực tiếp, cần implement riêng
    """)

    print(f"\nĐã lưu tất cả kết quả tại: {output_dir}")
