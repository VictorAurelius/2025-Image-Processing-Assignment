"""
Lab 5 — Đánh giá chất lượng ảnh sau suy giảm & phục hồi
Mục tiêu: Thực nghiệm các chỉ số chất lượng khi ảnh bị nhiễu/nén

Bước làm:
- Nhiễu Gaussian + muối tiêu với mức tăng dần
- Giảm bit-depth và/hoặc dùng JPEG compression
- Tính & ghi bảng các chỉ số, rút ra chỉ số phù hợp với cảm nhận thị giác

Tác giả: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os

def add_gaussian_noise(img, sigma=10):
    """Thêm nhiễu Gaussian"""
    noise = np.random.normal(0, sigma, img.shape).astype(np.float32)
    out = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    return out

def add_salt_pepper_noise(img, amount=0.01):
    """Thêm nhiễu muối tiêu"""
    out = img.copy()
    noise = np.random.rand(*img.shape)
    out[noise < amount/2] = 0      # Muối (đen)
    out[noise > 1 - amount/2] = 255  # Tiêu (trắng)
    return out

def mse(a, b):
    """Mean Squared Error"""
    return np.mean((a.astype(np.float32) - b.astype(np.float32))**2)

def psnr(a, b):
    """Peak Signal-to-Noise Ratio"""
    return 20*np.log10(255.0) - 10*np.log10(mse(a,b)+1e-12)

def mae(a, b):
    """Mean Absolute Error"""
    return np.mean(np.abs(a.astype(np.float32) - b.astype(np.float32)))

def ncc(a, b):
    """Normalized Cross-Correlation"""
    a = a.astype(np.float32); b = b.astype(np.float32)
    a = (a - a.mean()) / (a.std() + 1e-6)
    b = (b - b.mean()) / (b.std() + 1e-6)
    return np.mean(a*b)

def compress_jpeg(img, quality):
    """Nén JPEG với mức quality"""
    _, enc = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    dec = cv2.imdecode(enc, cv2.IMREAD_GRAYSCALE)
    return dec

def quantize(img, bits):
    """Lượng tử hóa xuống số bit"""
    L = 2**bits
    q = np.round(img / 255.0 * (L-1))
    rec = (q / (L-1) * 255.0).astype(np.uint8)
    return rec

def evaluate_quality(img_orig, img_degraded, name):
    """Đánh giá chất lượng và trả về kết quả"""
    _mae = mae(img_orig, img_degraded)
    _mse = mse(img_orig, img_degraded)
    _psnr = psnr(img_orig, img_degraded)
    _ssim = ssim(img_orig, img_degraded, data_range=255)
    _ncc = ncc(img_orig, img_degraded)

    return {
        'name': name,
        'mae': _mae,
        'mse': _mse,
        'psnr': _psnr,
        'ssim': _ssim,
        'ncc': _ncc
    }

if __name__ == "__main__":
    # Đường dẫn file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "scene.jpg")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")

        # Tạo ảnh scene phức tạp
        img = np.ones((480, 640), dtype=np.uint8) * 180

        # Vẽ bầu trời
        for i in range(200):
            img[i, :] = 200 - i//4

        # Vẽ núi
        pts = np.array([[0, 300], [200, 150], [400, 250], [640, 200], [640, 480], [0, 480]])
        cv2.fillPoly(img, [pts], 100)

        # Vẽ mặt trời
        cv2.circle(img, (500, 100), 40, 255, -1)

        # Vẽ cây
        for x in [100, 250, 400]:
            cv2.rectangle(img, (x-5, 280), (x+5, 350), 60, -1)
            cv2.circle(img, (x, 270), 25, 80, -1)

        # Thêm texture
        noise_texture = np.random.randint(-10, 10, img.shape, dtype=np.int16)
        img = np.clip(img.astype(np.int16) + noise_texture, 0, 255).astype(np.uint8)

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Đọc ảnh
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    print("="*80)
    print("LAB 5: ĐÁNH GIÁ CHẤT LƯỢNG ẢNH")
    print("="*80)
    print(f"Ảnh gốc: {img.shape}")

    results = []

    # ========== 1. Nhiễu Gaussian ==========
    print("\n" + "="*80)
    print("1. NHIỄU GAUSSIAN")
    print("="*80)

    for sigma in [5, 10, 20, 30]:
        noisy = add_gaussian_noise(img, sigma)
        result = evaluate_quality(img, noisy, f"Gaussian σ={sigma}")
        results.append(result)

        # Lưu ảnh
        output_path = os.path.join(output_dir, f"gaussian_sigma{sigma}.png")
        cv2.imwrite(output_path, noisy)

    # ========== 2. Nhiễu muối tiêu ==========
    print("\n" + "="*80)
    print("2. NHIỄU MUỐI TIÊU")
    print("="*80)

    for amount in [0.01, 0.05, 0.1, 0.2]:
        noisy = add_salt_pepper_noise(img, amount)
        result = evaluate_quality(img, noisy, f"Salt&Pepper {amount*100:.0f}%")
        results.append(result)

        # Lưu ảnh
        output_path = os.path.join(output_dir, f"salt_pepper_{int(amount*100)}.png")
        cv2.imwrite(output_path, noisy)

    # ========== 3. Nén JPEG ==========
    print("\n" + "="*80)
    print("3. NÉN JPEG")
    print("="*80)

    for quality in [90, 70, 50, 30, 10]:
        jpeg = compress_jpeg(img, quality)
        result = evaluate_quality(img, jpeg, f"JPEG Q={quality}")
        results.append(result)

        # Lưu ảnh
        output_path = os.path.join(output_dir, f"jpeg_q{quality}.jpg")
        cv2.imwrite(output_path, jpeg, [int(cv2.IMWRITE_JPEG_QUALITY), quality])

    # ========== 4. Giảm bit-depth ==========
    print("\n" + "="*80)
    print("4. GIẢM BIT-DEPTH")
    print("="*80)

    for bits in [6, 4, 2]:
        quantized = quantize(img, bits)
        result = evaluate_quality(img, quantized, f"{bits}-bit")
        results.append(result)

        # Lưu ảnh
        output_path = os.path.join(output_dir, f"quantized_{bits}bit.png")
        cv2.imwrite(output_path, quantized)

    # ========== 5. Kết hợp (worst case) ==========
    print("\n" + "="*80)
    print("5. KẾT HỢP NHIỀU SỬU GIẢM")
    print("="*80)

    # Gaussian + JPEG
    noisy = add_gaussian_noise(img, 15)
    jpeg_noisy = compress_jpeg(noisy, 40)
    result = evaluate_quality(img, jpeg_noisy, "Gaussian+JPEG")
    results.append(result)
    cv2.imwrite(os.path.join(output_dir, "combined_gaussian_jpeg.jpg"), jpeg_noisy)

    # Salt&Pepper + quantize
    sp = add_salt_pepper_noise(img, 0.05)
    sp_quant = quantize(sp, 4)
    result = evaluate_quality(img, sp_quant, "S&P+4bit")
    results.append(result)
    cv2.imwrite(os.path.join(output_dir, "combined_sp_quant.png"), sp_quant)

    # ========== In bảng kết quả ==========
    print("\n" + "="*80)
    print("BẢNG KẾT QUẢ TỔNG HỢP")
    print("="*80)

    print(f"\n{'Degradation':<25} {'MAE':<10} {'MSE':<12} {'PSNR':<10} {'SSIM':<10} {'NCC':<10}")
    print("-"*80)

    for r in results:
        print(f"{r['name']:<25} {r['mae']:<10.2f} {r['mse']:<12.2f} "
              f"{r['psnr']:<10.2f} {r['ssim']:<10.4f} {r['ncc']:<10.4f}")

    # ========== Phân tích ==========
    print("\n" + "="*80)
    print("PHÂN TÍCH & SO SÁNH CÁC CHỈ SỐ")
    print("="*80)

    # Sắp xếp theo PSNR
    sorted_by_psnr = sorted(results, key=lambda x: x['psnr'], reverse=True)
    print("\nTop 5 tốt nhất theo PSNR:")
    for i, r in enumerate(sorted_by_psnr[:5], 1):
        print(f"  {i}. {r['name']}: {r['psnr']:.2f} dB")

    # Sắp xếp theo SSIM
    sorted_by_ssim = sorted(results, key=lambda x: x['ssim'], reverse=True)
    print("\nTop 5 tốt nhất theo SSIM:")
    for i, r in enumerate(sorted_by_ssim[:5], 1):
        print(f"  {i}. {r['name']}: {r['ssim']:.4f}")

    print("\n" + "="*80)
    print("KẾT LUẬN")
    print("="*80)
    print("""
1. So sánh các metrics:

   MAE (Mean Absolute Error):
   - Đơn giản, dễ hiểu
   - Tuyến tính với sai số
   - Không nhạy với outliers như MSE
   - Đơn vị: pixel values [0-255]

   MSE (Mean Squared Error):
   - Phạt nặng các sai số lớn (do bình phương)
   - Nhạy cảm với outliers
   - Cơ sở toán học tốt cho tối ưu hóa
   - Đơn vị: pixel² values

   PSNR (Peak Signal-to-Noise Ratio):
   - Dựa trên MSE, đơn vị dB
   - Dễ so sánh (càng cao càng tốt)
   - >40 dB: Xuất sắc, >30 dB: Tốt, >20 dB: Chấp nhận được
   - Không tương quan tốt với chất lượng chủ quan

   SSIM (Structural Similarity Index):
   - Xét về cấu trúc, độ sáng, độ tương phản
   - Tương quan TỐT NHẤT với cảm nhận con người
   - Giá trị [0, 1], càng gần 1 càng tốt
   - >0.95: Rất tốt, >0.90: Tốt, >0.80: Chấp nhận được
   - Tính toán phức tạp hơn MSE/PSNR

   NCC (Normalized Cross-Correlation):
   - Đo tương quan giữa 2 ảnh
   - Bất biến với brightness shift
   - Giá trị [-1, 1], lý tưởng là 1
   - Ít phổ biến trong đánh giá chất lượng

2. Quan sát từ thực nghiệm:

   Nhiễu Gaussian:
   - PSNR giảm dần khi σ tăng
   - SSIM vẫn cao (>0.9) với σ nhỏ
   - Ảnh hưởng đều khắp ảnh

   Nhiễu Salt & Pepper:
   - PSNR giảm mạnh (outliers lớn)
   - SSIM giảm ít hơn PSNR (cấu trúc còn)
   - Chứng tỏ SSIM tốt hơn PSNR

   Nén JPEG:
   - Q=90: Gần như không nhận biết được
   - Q=50: Bắt đầu thấy artifacts
   - Q=10: Blocky artifacts rõ ràng
   - SSIM phản ánh tốt chất lượng chủ quan

   Giảm bit-depth:
   - 6-bit: SSIM > 0.99 (xuất sắc)
   - 4-bit: SSIM ~ 0.95 (tốt)
   - 2-bit: SSIM < 0.90 (kém)
   - Posterization effect rõ ràng

3. Khuyến nghị sử dụng:

   - Đánh giá chủ quan: Dùng SSIM (tương quan tốt nhất)
   - Tối ưu hóa nhanh: Dùng MSE/PSNR (đơn giản)
   - Báo cáo khoa học: Báo cáo cả PSNR và SSIM
   - Nhiễu salt&pepper: Ưu tiên SSIM hoặc NCC
   - So sánh nén: SSIM hoặc MS-SSIM (multi-scale)

4. Hạn chế:

   - Tất cả đều là full-reference (cần ảnh gốc)
   - Không thể đánh giá nếu không có ground truth
   - Cần nghiên cứu no-reference quality metrics cho thực tế

5. Mở rộng:

   - MS-SSIM: Multi-scale SSIM (tốt hơn SSIM)
   - FSIM: Feature Similarity Index
   - VIF: Visual Information Fidelity
   - LPIPS: Learned Perceptual Image Patch Similarity (dùng deep learning)
    """)

    print(f"\nĐã lưu {len(results)} ảnh kết quả tại: {output_dir}")
