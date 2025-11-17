"""
Bài 1 — So sánh các bộ dò biên trên ảnh thật & ảnh có nhiễu

Mục tiêu:
- Hiểu vai trò làm trơn trước khi lấy đạo hàm
- So sánh độ nhạy nhiễu và "độ dày" biên giữa các toán tử
- Thực hành chuẩn hoá biên độ gradient và đặt ngưỡng theo phần trăm cực đại

Kỹ thuật sử dụng:
- Roberts, Prewitt, Sobel, Scharr edge detectors
- Gaussian smoothing trước edge detection
- Gradient magnitude normalization
- Thresholding theo tỉ lệ

Input:
- Ảnh đời thực (đường phố, tòa nhà, mặt người, sản phẩm...)
- File: input.jpg

Output:
- Ảnh biên với các toán tử khác nhau
- So sánh trên ảnh gốc và ảnh nhiễu
- Lưu tại: ../output/edges_*.png

Tác giả đề bài: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
from scipy.ndimage import convolve, gaussian_filter
import os

def grad2d(f, scheme='sobel', sigma=None, bc='reflect'):
    """
    Tính gradient 2D với nhiều toán tử khác nhau

    Args:
        f: Ảnh đầu vào (grayscale, float32)
        scheme: Loại toán tử ('roberts', 'prewitt', 'sobel', 'scharr')
        sigma: Tham số Gaussian blur (None = không làm trơn)
        bc: Boundary condition cho convolution

    Returns:
        Biên độ gradient (magnitude)
    """
    g = f.copy()

    # Làm trơn Gaussian nếu có sigma
    if sigma is not None:
        g = gaussian_filter(g, sigma=sigma, mode=bc)

    # Toán tử Roberts (2x2)
    if scheme == 'roberts':
        gx = g[:-1,:-1] - g[1:,1:]
        gy = g[1:,:-1] - g[:-1,1:]
        mag = np.zeros_like(g)
        mag[:-1,:-1] = np.hypot(gx, gy)
        return mag

    # Các toán tử convolution 3x3
    if scheme == 'prewitt':
        kx = np.array([[-1,0,1],[-1,0,1],[-1,0,1]], np.float32)
        ky = np.array([[ 1,1,1],[ 0,0,0],[-1,-1,-1]], np.float32)
    elif scheme == 'sobel':
        kx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]], np.float32)
        ky = np.array([[ 1,2,1],[ 0,0,0],[-1,-2,-1]], np.float32)
    elif scheme == 'scharr':
        kx = np.array([[3,0,-3],[10,0,-10],[3,0,-3]], np.float32)/32.0
        ky = kx.T

    # Tính gradient theo x và y
    Gx = convolve(g, kx, mode=bc)
    Gy = convolve(g, ky, mode=bc)

    # Tính magnitude
    return np.hypot(Gx, Gy)

def binarize(mag, thr_ratio=0.25):
    """
    Nhị phân hóa ảnh magnitude theo ngưỡng tỉ lệ

    Args:
        mag: Ảnh magnitude
        thr_ratio: Tỉ lệ ngưỡng so với giá trị max (0.0-1.0)

    Returns:
        Ảnh nhị phân (0 hoặc 255)
    """
    mmax = mag.max() if mag.size else 0
    return (mag >= thr_ratio*mmax).astype(np.uint8)*255

if __name__ == "__main__":
    # Thiết lập đường dẫn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "building.jpg")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")

        # Tạo ảnh building mẫu với nhiều cạnh
        img = np.ones((600, 800), dtype=np.uint8) * 200

        # Vẽ tòa nhà
        cv2.rectangle(img, (150, 150), (350, 500), 100, -1)
        cv2.rectangle(img, (400, 250), (650, 500), 120, -1)

        # Vẽ cửa sổ
        for i in range(3):
            for j in range(4):
                cv2.rectangle(img, (180 + i*50, 200 + j*70),
                            (220 + i*50, 230 + j*70), 255, -1)

        for i in range(4):
            for j in range(3):
                cv2.rectangle(img, (430 + i*50, 300 + j*60),
                            (470 + i*50, 330 + j*60), 255, -1)

        # Vẽ mái nhà
        pts = np.array([[150,150], [250,100], [350,150]], np.int32)
        cv2.fillPoly(img, [pts], 80)

        pts = np.array([[400,250], [525,180], [650,250]], np.int32)
        cv2.fillPoly(img, [pts], 90)

        # Vẽ đường
        cv2.rectangle(img, (0, 500), (800, 600), 150, -1)

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Đọc ảnh và chuyển sang grayscale float32
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    img = img.astype(np.float32)

    # Tạo ảnh nhiễu (Gaussian noise, stddev=10)
    noisy = (img + np.random.normal(0, 10, img.shape)).clip(0, 255).astype(np.float32)

    print("="*80)
    print("BÀI 1: SO SÁNH CÁC BỘ DÒ BIÊN")
    print("="*80)
    print(f"Ảnh gốc: {img.shape}")
    print(f"\nSo sánh 4 toán tử: Roberts, Prewitt, Sobel, Scharr")
    print(f"Với và không có Gaussian smoothing (sigma=1.0)")
    print(f"Ngưỡng: 25% của magnitude tối đa")
    print("="*80)

    # Test với ảnh gốc và ảnh nhiễu
    for sigma in [None, 1.0]:
        sigma_str = "None" if sigma is None else f"{sigma:.1f}"

        print(f"\n--- Sigma = {sigma_str} ---")

        for scheme in ['roberts', 'prewitt', 'sobel', 'scharr']:
            # Xử lý ảnh gốc
            mag = grad2d(img, scheme=scheme, sigma=sigma)
            mask = binarize(mag, 0.25)

            output_path = os.path.join(output_dir, f'edges_{scheme}_sigma{sigma_str}.png')
            cv2.imwrite(output_path, mask)

            # Xử lý ảnh nhiễu
            magN = grad2d(noisy, scheme=scheme, sigma=sigma)
            maskN = binarize(magN, 0.25)

            output_path_noisy = os.path.join(output_dir, f'edges_{scheme}_sigma{sigma_str}_noisy.png')
            cv2.imwrite(output_path_noisy, maskN)

            # Đếm số pixel biên
            edge_count = np.sum(mask > 0)
            edge_count_noisy = np.sum(maskN > 0)

            print(f"  {scheme:8s}: {edge_count:6d} pixels (gốc), {edge_count_noisy:6d} pixels (nhiễu)")

    print("\n" + "="*80)
    print("PHÂN TÍCH & KẾT LUẬN")
    print("="*80)

    print("""
1. So sánh các toán tử (không làm trơn):
   - Roberts (2x2): Nhạy cảm nhất với nhiễu, biên mảnh nhất
   - Prewitt (3x3): Trung bình, ít nhiễu hơn Roberts
   - Sobel (3x3): Tốt nhất cho hầu hết ứng dụng, cân bằng nhiễu/độ chi tiết
   - Scharr (3x3): Chính xác nhất về góc, ít nhiễu

2. Vai trò của Gaussian smoothing (sigma=1.0):
   - Giảm nhiễu đáng kể
   - Trade-off: Làm mờ biên sắc nét
   - Roberts cải thiện nhiều nhất khi làm trơn
   - Sobel/Scharr: Ít cần làm trơn hơn

3. Khuyến nghị:
   - Ảnh sạch, cần biên sắc nét: Scharr hoặc Sobel không làm trơn
   - Ảnh nhiễu: Sobel + Gaussian (sigma=1-2)
   - Ứng dụng thời gian thực: Sobel (nhanh, hiệu quả)
   - Cần độ chính xác cao: Scharr + Gaussian
    """)

    print(f"\nĐã lưu {4*2*2} = 16 ảnh kết quả tại: {output_dir}")
    print("  - edges_[toán_tử]_sigma[None/1.0].png")
    print("  - edges_[toán_tử]_sigma[None/1.0]_noisy.png")
    print("\nHoàn thành!")
