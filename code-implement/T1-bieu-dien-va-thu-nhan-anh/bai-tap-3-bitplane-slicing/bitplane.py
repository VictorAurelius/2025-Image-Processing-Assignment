"""
Bài tập 3 — Bit-plane slicing để phát hiện mờ/đốm in
Bối cảnh: Tờ hoá đơn/phiếu thu bị mờ & lẫn nhiễu muối tiêu

Yêu cầu:
- Tách 8 mặt phẳng bit của ảnh xám 8 bit
- Quan sát bit-plane thấp (0–3) vs cao (4-7)
- Tạo ảnh tái dựng từ bit-plane 4–7

Tác giả: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
import os

def ncc(a, b):
    """Tính Normalized Cross-Correlation"""
    a = a.astype(np.float32); b = b.astype(np.float32)
    a = (a - a.mean())/(a.std()+1e-6)
    b = (b - b.mean())/(b.std()+1e-6)
    return np.mean(a*b)

if __name__ == "__main__":
    # Đường dẫn file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "bill.png")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu với nhiễu muối tiêu...")

        # Tạo ảnh bill mẫu
        img = np.ones((600, 800), dtype=np.uint8) * 240
        cv2.putText(img, "INVOICE / HOA DON", (200, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, 0, 2)
        cv2.line(img, (50, 120), (750, 120), 0, 2)
        cv2.putText(img, "Item 1: Product A ......... 100,000 VND", (80, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, 0, 1)
        cv2.putText(img, "Item 2: Product B ......... 250,000 VND", (80, 230),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, 0, 1)
        cv2.putText(img, "Total: .................... 350,000 VND", (80, 320),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, 0, 2)

        # Thêm nhiễu muối tiêu
        noise = np.random.rand(*img.shape)
        img[noise < 0.01] = 0  # Muối
        img[noise > 0.99] = 255  # Tiêu

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Đọc ảnh
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    print(f"Đã đọc ảnh: {img.shape}")
    print("="*60)
    print("BIT-PLANE SLICING")
    print("="*60)

    # Tách 8 mặt phẳng bit
    planes = [(img >> b) & 1 for b in range(8)]

    print("\nTách 8 mặt phẳng bit...")
    for b, p in enumerate(planes):
        output_path = os.path.join(output_dir, f"bitplane_{b}.png")
        cv2.imwrite(output_path, p*255)
        print(f"  Bit-plane {b}: {output_path}")

    # Tái dựng từ bit 4..7 (chỉ giữ các bit cao)
    print("\nTái dựng từ bit-plane 4-7...")
    rec = np.zeros_like(img, dtype=np.uint8)
    for b in range(4, 8):
        rec |= ((planes[b].astype(np.uint8)) << b)

    # Lưu ảnh tái dựng
    recon_path = os.path.join(output_dir, "bill_recon_4to7.png")
    cv2.imwrite(recon_path, rec)
    print(f"  Ảnh tái dựng: {recon_path}")

    # Đánh giá NCC
    ncc_value = ncc(img, rec)
    print(f"\n{'='*60}")
    print(f"NCC (Normalized Cross-Correlation): {ncc_value:.4f}")
    print(f"{'='*60}")

    print("""
QUAN SÁT:
- Bit-plane 0-3 (LSB): Chứa nhiều nhiễu, biến đổi nhanh
  → Nhiễu muối tiêu tập trung ở các bit thấp
- Bit-plane 4-7 (MSB): Chứa cấu trúc chính của văn bản
  → Chữ và đường nét quan trọng

KẾT LUẬN:
- Loại bỏ bit 0-3 giúp giảm nhiễu đáng kể
- NCC cao (~0.95-0.99) chứng tỏ cấu trúc chính được giữ lại
- Phương pháp này hữu ích cho tiền xử lý ảnh nhiễu
    """)
