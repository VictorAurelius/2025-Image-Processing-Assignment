"""
=============================================================================
BÀI 4: BAYES / MAXIMUM LIKELIHOOD THRESHOLDING
=============================================================================
Đề bài: Phân tách vùng rỉ sét (đối tượng) trên bề mặt kim loại (nền) khi histogram chồng lấn nhẹ.
Mục tiêu: Dựa vào giả định phân bố Gauss cho H0/H1 và prior P0/P1 để tìm ngưỡng ML/Bayes.
Yêu cầu: Chọn tham số μ,σ gần đúng theo thống kê mẫu nhỏ; hiển thị T và kết quả.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T79-99 Phân vùng ảnh (trang 7-8)
=============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def calc_threshold(mu0, s0, mu1, s1, P0, P1):
    """
    Tính ngưỡng Bayes-ML cho trường hợp 2 lớp Gaussian khác phương sai.

    Args:
        mu0, s0: Mean và std của lớp 0 (nền)
        mu1, s1: Mean và std của lớp 1 (vật thể)
        P0, P1: Prior probability của lớp 0 và 1

    Returns:
        T: Ngưỡng tối ưu
    """
    # Nghiệm xấp xỉ cho trường hợp Gauss khác phương sai
    numerator = mu0 * s1**2 - mu1 * s0**2 + s0 * s1 * np.sqrt(
        (mu1 - mu0)**2 + 2 * (s1**2 - s0**2) * np.log((s1 * P0) / (s0 * P1))
    )
    denominator = s1**2 - s0**2

    if abs(denominator) < 1e-6:
        # Trường hợp s0 = s1
        T = (mu0 + mu1) / 2
    else:
        T = numerator / denominator

    return T


def create_sample_image():
    """Tạo ảnh mẫu bề mặt kim loại có rỉ sét."""
    img = np.ones((400, 600, 3), dtype=np.uint8)

    # Nền kim loại (xám sáng)
    img[:, :] = [120, 120, 120]

    # Thêm texture cho kim loại
    noise = np.random.normal(0, 12, (400, 600))
    for i in range(3):
        img[:, :, i] = np.clip(img[:, :, i] + noise, 0, 255)

    # Vùng rỉ sét (màu nâu/cam nhạt hơn)
    rust_regions = [
        (50, 80, 180, 200),
        (220, 50, 350, 180),
        (380, 150, 550, 320),
        (100, 250, 250, 380)
    ]

    for x1, y1, x2, y2 in rust_regions:
        # Vùng rỉ sét có độ sáng cao hơn một chút
        cv2.ellipse(img, ((x1+x2)//2, (y1+y2)//2),
                    ((x2-x1)//2, (y2-y1)//2), 0, 0, 360,
                    (165, 165, 165), -1)

        # Thêm nhiễu cho vùng rỉ
        mask = np.zeros((400, 600), dtype=np.uint8)
        cv2.ellipse(mask, ((x1+x2)//2, (y1+y2)//2),
                    ((x2-x1)//2, (y2-y1)//2), 0, 0, 360, 255, -1)

        rust_noise = np.random.normal(0, 15, (400, 600))
        for i in range(3):
            img[:, :, i] = np.where(mask > 0,
                                   np.clip(img[:, :, i] + rust_noise, 0, 255),
                                   img[:, :, i])

    return img


def main():
    # Kiểm tra ảnh input
    input_path = "../input/steel_rust.jpg"

    if os.path.exists(input_path):
        print("Đang đọc ảnh từ:", input_path)
        img = cv2.imread(input_path)
    else:
        print("Không tìm thấy ảnh input, tạo ảnh mẫu...")
        img = create_sample_image()
        os.makedirs("../input", exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Chuyển sang ảnh xám
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print("\n" + "="*60)
    print("PHÂN NGƯỠNG BAYES-ML - BAYES/ML THRESHOLDING")
    print("="*60)

    # Ước lượng tham số (trong thực tế lấy từ mẫu thực tế)
    # Ví dụ: các giá trị ước lượng
    mu0 = 120  # Mean của nền (kim loại)
    s0 = 12    # Std của nền
    mu1 = 165  # Mean của rỉ sét
    s1 = 15    # Std của rỉ sét
    P0 = 0.7   # Prior probability của nền
    P1 = 0.3   # Prior probability của rỉ sét

    print(f"\nTham số ước lượng:")
    print(f"  Lớp 0 (Nền kim loại):")
    print(f"    - Mean (μ₀) = {mu0}")
    print(f"    - Std (σ₀) = {s0}")
    print(f"    - Prior (P₀) = {P0}")
    print(f"  Lớp 1 (Rỉ sét):")
    print(f"    - Mean (μ₁) = {mu1}")
    print(f"    - Std (σ₁) = {s1}")
    print(f"    - Prior (P₁) = {P1}")

    # Tính ngưỡng Bayes-ML
    T = calc_threshold(mu0, s0, mu1, s1, P0, P1)

    print(f"\nNgưỡng Bayes-ML tính được: T = {round(T, 2)}")

    # Áp dụng ngưỡng
    _, binimg = cv2.threshold(gray, T, 255, cv2.THRESH_BINARY)

    # Thống kê
    print(f"\nThống kê ảnh xám:")
    print(f"  - Độ sáng trung bình: {np.mean(gray):.2f}")
    print(f"  - Độ lệch chuẩn: {np.std(gray):.2f}")
    print(f"  - Min/Max: {np.min(gray)}/{np.max(gray)}")

    rust_pixels = np.sum(binimg == 255)
    total_pixels = gray.size

    print(f"\nPhân vùng:")
    print(f"  - Vùng nền: {total_pixels - rust_pixels} pixels ({100*(total_pixels-rust_pixels)/total_pixels:.1f}%)")
    print(f"  - Vùng rỉ sét: {rust_pixels} pixels ({100*rust_pixels/total_pixels:.1f}%)")

    # Vẽ phân bố Gaussian
    x = np.linspace(0, 255, 1000)
    gaussian0 = P0 * (1 / (s0 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu0) / s0)**2)
    gaussian1 = P1 * (1 / (s1 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu1) / s1)**2)

    # Hiển thị kết quả
    plt.figure(figsize=(14, 8))

    plt.subplot(2, 3, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Ảnh gốc", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(2, 3, 2)
    plt.imshow(gray, cmap='gray')
    plt.title("Ảnh xám", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.subplot(2, 3, 3)
    plt.imshow(binimg, cmap='gray')
    plt.title(f"Bayes-ML mask\n(T = {round(T, 2)})",
              fontsize=12, fontweight='bold')
    plt.axis('off')

    # Histogram và phân bố Gaussian
    plt.subplot(2, 3, 4)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist_norm = hist / hist.max()
    plt.plot(hist_norm, color='steelblue', alpha=0.7, label='Histogram')
    plt.axvline(x=T, color='red', linestyle='--', linewidth=2, label=f'T={T:.1f}')
    plt.title("Histogram", fontsize=12, fontweight='bold')
    plt.xlabel("Mức xám")
    plt.ylabel("Tần suất (chuẩn hóa)")
    plt.legend()
    plt.grid(alpha=0.3)

    # Phân bố Gaussian lý thuyết
    plt.subplot(2, 3, 5)
    plt.plot(x, gaussian0, 'b-', linewidth=2, label=f'Nền (μ={mu0}, σ={s0})')
    plt.plot(x, gaussian1, 'r-', linewidth=2, label=f'Rỉ sét (μ={mu1}, σ={s1})')
    plt.axvline(x=T, color='green', linestyle='--', linewidth=2, label=f'T={T:.1f}')
    plt.title("Mô hình Gaussian", fontsize=12, fontweight='bold')
    plt.xlabel("Mức xám")
    plt.ylabel("Xác suất")
    plt.legend()
    plt.grid(alpha=0.3)

    # Overlay mask lên ảnh gốc
    plt.subplot(2, 3, 6)
    overlay = img.copy()
    overlay[binimg == 255] = [0, 255, 0]  # Tô xanh vùng rỉ sét
    result = cv2.addWeighted(img, 0.7, overlay, 0.3, 0)
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title("Vùng rỉ sét (overlay)", fontsize=12, fontweight='bold')
    plt.axis('off')

    plt.tight_layout()

    # Lưu kết quả
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "bayes_ml_result.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nĐã lưu kết quả tại: {output_path}")

    plt.show()

    print("\n" + "="*60)
    print("HOÀN THÀNH!")
    print("="*60)


if __name__ == "__main__":
    main()
