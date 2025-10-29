"""
Lab 1 — Chuẩn hoá & lượng tử hoá động (8→6→4→2 bit) + đánh giá
Mục tiêu: Thấy rõ ảnh hưởng của lượng tử hoá lên chất lượng

Bước làm:
- Đọc ảnh xám; giảm bit theo các mức; lưu ảnh
- Tính MAE, MSE, PSNR, SSIM, NCC giữa gốc và từng mức
- Vẽ bảng/kết luận mức tối thiểu chấp nhận được

Tác giả: TS. Phan Thanh Toàn
"""

from skimage.metrics import structural_similarity as ssim
import numpy as np
import cv2
import os

def mae(a, b):
    """Mean Absolute Error"""
    return np.mean(np.abs(a.astype(np.float32) - b.astype(np.float32)))

def mse(a, b):
    """Mean Squared Error"""
    return np.mean((a.astype(np.float32) - b.astype(np.float32))**2)

def psnr(a, b):
    """Peak Signal-to-Noise Ratio"""
    m = mse(a, b)
    return 20*np.log10(255.0) - 10*np.log10(m+1e-12)

def ncc(a, b):
    """Normalized Cross-Correlation"""
    a = a.astype(np.float32); b = b.astype(np.float32)
    a = (a - a.mean()) / (a.std() + 1e-6)
    b = (b - b.mean()) / (b.std() + 1e-6)
    return np.mean(a*b)

if __name__ == "__main__":
    # Đường dẫn file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "doc.png")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")

        # Tạo ảnh document mẫu
        img = np.ones((600, 800), dtype=np.uint8) * 255
        cv2.putText(img, "DOCUMENT SAMPLE", (200, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, 0, 3)
        cv2.line(img, (100, 150), (700, 150), 0, 2)

        # Thêm text với các mức xám khác nhau
        for i in range(5):
            gray = int(255 - i * 40)
            cv2.putText(img, f"Line {i+1}: Gray level {gray}", (120, 220 + i*60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, gray, 2)

        # Thêm gradient
        for i in range(100):
            color = int(i * 2.55)
            cv2.rectangle(img, (650, 200 + i), (750, 201 + i), color, -1)

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Đọc ảnh
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    print("="*70)
    print("LAB 1: ĐÁNH GIÁ LƯỢNG TỬ HÓA ĐỘNG")
    print("="*70)
    print(f"Ảnh gốc: {img.shape}, dtype: {img.dtype}")

    # Header bảng
    print(f"\n{'Bits':<6} {'MAE':<10} {'MSE':<12} {'PSNR (dB)':<12} {'SSIM':<10} {'NCC':<10}")
    print("-"*70)

    results = []

    # Lượng tử hóa và đánh giá
    for k in [7, 6, 5, 4, 3, 2]:
        # Lượng tử hóa
        rec = ((np.round(img/255*(2**k-1)))/(2**k-1)*255).astype(np.uint8)

        # Tính các metrics
        _mae = mae(img, rec)
        _mse = mse(img, rec)
        _psnr = psnr(img, rec)
        _ssim = ssim(img, rec, data_range=255)
        _ncc = ncc(img, rec)

        results.append({
            'bits': k,
            'mae': _mae,
            'mse': _mse,
            'psnr': _psnr,
            'ssim': _ssim,
            'ncc': _ncc
        })

        # In kết quả
        print(f"{k:<6} {_mae:<10.2f} {_mse:<12.2f} {_psnr:<12.2f} {_ssim:<10.4f} {_ncc:<10.4f}")

        # Lưu ảnh
        output_path = os.path.join(output_dir, f"quantized_{k}bit.png")
        cv2.imwrite(output_path, rec)

    print("-"*70)

    # Phân tích kết quả
    print("\n" + "="*70)
    print("PHÂN TÍCH & KẾT LUẬN")
    print("="*70)

    print("\n1. Quan sát MAE & MSE:")
    print("   - Tăng khi giảm số bit (chất lượng giảm)")
    print("   - MSE nhạy cảm với outliers hơn MAE")

    print("\n2. Quan sát PSNR:")
    for r in results:
        if r['psnr'] >= 40:
            quality = "Xuất sắc"
        elif r['psnr'] >= 30:
            quality = "Tốt"
        elif r['psnr'] >= 20:
            quality = "Chấp nhận được"
        else:
            quality = "Kém"
        print(f"   {r['bits']}-bit: {r['psnr']:.2f} dB → {quality}")

    print("\n3. Quan sát SSIM:")
    for r in results:
        if r['ssim'] >= 0.95:
            quality = "Rất tốt (không nhận biết được)"
        elif r['ssim'] >= 0.90:
            quality = "Tốt (khó nhận biết)"
        elif r['ssim'] >= 0.80:
            quality = "Chấp nhận được (nhận biết được)"
        else:
            quality = "Kém (rõ ràng bị giảm chất lượng)"
        print(f"   {r['bits']}-bit: {r['ssim']:.4f} → {quality}")

    print("\n4. Quan sát NCC:")
    print("   - Đo tương quan cấu trúc giữa 2 ảnh")
    print("   - Giá trị cao (>0.95) → cấu trúc được bảo toàn tốt")

    print("\n" + "="*70)
    print("KHUYẾN NGHỊ")
    print("="*70)

    # Tìm mức bit tối thiểu chấp nhận được
    for r in results:
        if r['ssim'] >= 0.90 and r['psnr'] >= 30:
            min_acceptable = r['bits']
            break
    else:
        min_acceptable = 8

    print(f"""
Mức bit tối thiểu chấp nhận được: {min_acceptable}-bit

Lý do:
- SSIM >= 0.90: Chất lượng chủ quan tốt
- PSNR >= 30 dB: Chất lượng khách quan tốt
- Tiết kiệm {(8-min_acceptable)/8*100:.0f}% dung lượng so với 8-bit

Ứng dụng thực tế:
- 7-6 bit: Ảnh y tế, ảnh khoa học (cần độ chính xác cao)
- 5-4 bit: Ảnh văn bản, document scanning
- 3-2 bit: Chỉ dùng khi cực kỳ hạn chế dung lượng (chất lượng kém)

Lưu ý: Trong thực tế nên dùng nén (JPEG, PNG) thay vì chỉ giảm bit-depth
    """)

    print(f"\nĐã lưu {len(results)} ảnh kết quả tại: {output_dir}")
