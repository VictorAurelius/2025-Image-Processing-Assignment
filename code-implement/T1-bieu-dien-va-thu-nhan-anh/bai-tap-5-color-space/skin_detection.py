"""
Bài tập 5 — Chuyển hệ màu & phát hiện vùng da mặt (HSV/YCrCb)
Bối cảnh: Lọc ảnh nhạy cảm trước khi đăng lên website trường

Yêu cầu:
- Đọc ảnh RGB, chuyển HSV và YCrCb
- Dùng ngưỡng để tách vùng da
- So sánh mặt nạ kết quả giữa hai không gian màu

Tác giả: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
import os

if __name__ == "__main__":
    # Đường dẫn file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "portrait.jpg")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu với màu da...")

        # Tạo ảnh mẫu với màu da
        img = np.ones((400, 600, 3), dtype=np.uint8) * 200

        # Vẽ vùng da (màu da trung bình)
        # RGB: ~(220, 180, 150)
        skin_color = [150, 180, 220]  # BGR format
        cv2.ellipse(img, (300, 200), (150, 180), 0, 0, 360, skin_color, -1)

        # Vẽ nền không phải da
        bg_color = [100, 150, 200]
        img[:100, :] = bg_color
        img[350:, :] = bg_color

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Đọc ảnh
    img = cv2.imread(input_path)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    print(f"Đã đọc ảnh: {img.shape}")
    print("="*60)
    print("PHÁT HIỆN VÙNG DA - HSV vs YCrCb")
    print("="*60)

    # Chuyển đổi không gian màu
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

    print("\nĐã chuyển đổi sang:")
    print("  - HSV (Hue, Saturation, Value)")
    print("  - YCrCb (Luma, Chroma Red, Chroma Blue)")

    # HSV thresholds
    # Lưu ý: OpenCV scale H:0-179, S:0-255, V:0-255
    # Ngưỡng da: H∈[0,25], S∈[0.2,0.7]*255, V>0.35*255
    lower_hsv = (0, 30, 90)
    upper_hsv = (25, 180, 255)
    mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

    print("\nNgưỡng HSV:")
    print(f"  H (Hue): {lower_hsv[0]} - {upper_hsv[0]}")
    print(f"  S (Saturation): {lower_hsv[1]} - {upper_hsv[1]}")
    print(f"  V (Value): {lower_hsv[2]} - {upper_hsv[2]}")

    # YCrCb thresholds
    # Cr∈[135,180], Cb∈[85,135]
    lower_ycc = (0, 135, 85)
    upper_ycc = (255, 180, 135)
    mask_ycc = cv2.inRange(ycrcb, lower_ycc, upper_ycc)

    print("\nNgưỡng YCrCb:")
    print(f"  Y (Luma): {lower_ycc[0]} - {upper_ycc[0]}")
    print(f"  Cr (Chroma Red): {lower_ycc[1]} - {upper_ycc[1]}")
    print(f"  Cb (Chroma Blue): {lower_ycc[2]} - {upper_ycc[2]}")

    # Lưu kết quả
    hsv_path = os.path.join(output_dir, "mask_hsv.png")
    ycc_path = os.path.join(output_dir, "mask_ycrcb.png")
    cv2.imwrite(hsv_path, mask_hsv)
    cv2.imwrite(ycc_path, mask_ycc)

    print(f"\nĐã lưu:")
    print(f"  Mask HSV: {hsv_path}")
    print(f"  Mask YCrCb: {ycc_path}")

    # Áp dụng mask lên ảnh gốc
    result_hsv = cv2.bitwise_and(img, img, mask=mask_hsv)
    result_ycc = cv2.bitwise_and(img, img, mask=mask_ycc)

    result_hsv_path = os.path.join(output_dir, "skin_hsv.png")
    result_ycc_path = os.path.join(output_dir, "skin_ycrcb.png")
    cv2.imwrite(result_hsv_path, result_hsv)
    cv2.imwrite(result_ycc_path, result_ycc)

    print(f"  Kết quả HSV: {result_hsv_path}")
    print(f"  Kết quả YCrCb: {result_ycc_path}")

    # So sánh
    pixels_hsv = np.sum(mask_hsv > 0)
    pixels_ycc = np.sum(mask_ycc > 0)
    total_pixels = mask_hsv.shape[0] * mask_hsv.shape[1]

    print("\n" + "="*60)
    print("SO SÁNH KẾT QUẢ")
    print("="*60)
    print(f"HSV:")
    print(f"  Số pixel phát hiện: {pixels_hsv}")
    print(f"  Tỷ lệ: {pixels_hsv/total_pixels*100:.2f}%")
    print(f"\nYCrCb:")
    print(f"  Số pixel phát hiện: {pixels_ycc}")
    print(f"  Tỷ lệ: {pixels_ycc/total_pixels*100:.2f}%")

    # Intersection
    intersection = cv2.bitwise_and(mask_hsv, mask_ycc)
    pixels_common = np.sum(intersection > 0)
    print(f"\nGiao (cả 2 phát hiện):")
    print(f"  Số pixel: {pixels_common}")
    print(f"  Tỷ lệ: {pixels_common/total_pixels*100:.2f}%")

    print("\n" + "="*60)
    print("KẾT LUẬN")
    print("="*60)
    print("""
HSV:
  + Tốt cho các ứng dụng trong điều kiện ánh sáng ổn định
  + H (Hue) ít bị ảnh hưởng bởi độ sáng
  - Nhạy cảm với bóng và sự thay đổi ánh sáng

YCrCb:
  + Tốt hơn trong điều kiện ánh sáng thay đổi
  + Cr và Cb tách biệt rõ ràng màu da
  + Ít bị ảnh hưởng bởi độ sáng (Y)
  - Có thể phát hiện nhầm vật thể có màu tương tự

Khuyến nghị:
- Kết hợp cả hai phương pháp (intersection) để tăng độ chính xác
- Cần post-processing (morphology) để loại bỏ nhiễu
- Điều chỉnh ngưỡng tùy theo bộ ảnh cụ thể
    """)
