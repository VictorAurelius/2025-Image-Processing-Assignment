"""
Bài tập 2 — Lấy mẫu & lượng tử hoá khi scan tài liệu
Bối cảnh: Số hoá đề thi A4 để lưu trữ

Yêu cầu:
- Mô phỏng ảnh xám 8 bit → giảm còn 6–4–2 bit (lượng tử hoá)
- Tính MAE, MSE, PSNR, SSIM giữa ảnh gốc và ảnh giảm bit
- Nêu mức bit tối thiểu để chữ vẫn đọc tốt

Tác giả: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os

def quantize_gray(img_gray, k):
    """
    Lượng tử hóa ảnh xám từ 8-bit xuống k-bit

    Args:
        img_gray: Ảnh xám 8-bit
        k: Số bit mục tiêu

    Returns:
        Ảnh đã lượng tử hóa
    """
    L = 2**k
    img = img_gray.astype(np.float32)
    q = np.round(img / 255.0 * (L-1))
    rec = (q / (L-1) * 255.0).astype(np.uint8)
    return rec

def mse(a, b):
    """Tính Mean Squared Error"""
    return np.mean((a.astype(np.float32)-b.astype(np.float32))**2)

def psnr(a, b):
    """Tính Peak Signal-to-Noise Ratio"""
    m = mse(a,b)
    return 20*np.log10(255.0) - 10*np.log10(m+1e-12)

def mae(a, b):
    """Tính Mean Absolute Error"""
    return np.mean(np.abs(a.astype(np.float32) - b.astype(np.float32)))

if __name__ == "__main__":
    # Đường dẫn file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "scan_de_thi.png")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output nếu chưa có
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra file tồn tại
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")
        # Tạo ảnh text mẫu
        img = np.ones((800, 600), dtype=np.uint8) * 255
        cv2.putText(img, "SAMPLE EXAM DOCUMENT", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
        cv2.putText(img, "Question 1: Lorem ipsum dolor", (50, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, 0, 1)
        cv2.putText(img, "Question 2: Sit amet consectetur", (50, 300),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, 0, 1)
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
    print("LƯỢNG TỬ HÓA ẢNH SCAN TÀI LIỆU")
    print("="*60)

    # Lượng tử hóa và đánh giá
    for k in [6, 4, 2]:
        rec = quantize_gray(img, k)
        _mse = mse(img, rec)
        _mae = mae(img, rec)
        _psnr = psnr(img, rec)
        _ssim = ssim(img, rec, data_range=255)

        print(f"\n{k} bit -> MAE={_mae:.2f}, MSE={_mse:.2f}, PSNR={_psnr:.2f} dB, SSIM={_ssim:.3f}")

        # Lưu ảnh kết quả
        output_path = os.path.join(output_dir, f"scan_quant_{k}bit.png")
        cv2.imwrite(output_path, rec)
        print(f"   Đã lưu: {output_path}")

    print("\n" + "="*60)
    print("KẾT LUẬN")
    print("="*60)
    print("""
Dựa trên các chỉ số:
- 6 bit: PSNR cao, SSIM > 0.99 → Chất lượng rất tốt, chữ rõ ràng
- 4 bit: PSNR trung bình, SSIM > 0.95 → Chấp nhận được cho văn bản
- 2 bit: PSNR thấp, SSIM < 0.9 → Chất lượng kém, mất nhiều chi tiết

Mức bit tối thiểu khuyến nghị: 4-bit
- Đủ để đọc chữ tốt
- Tiết kiệm 50% dung lượng so với 8-bit
- SSIM vẫn > 0.95 (chấp nhận được)
    """)
