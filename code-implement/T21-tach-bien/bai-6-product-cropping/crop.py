"""
Bài 6 — Cắt nền (auto-crop) ảnh sản phẩm bằng biên + contour

Mục tiêu:
- Dùng Canny/Sobel để lấy biên
- Đóng/mở để liền khối
- Chọn contour lớn nhất, tạo mask, alpha-matte PNG

Kỹ thuật sử dụng:
- Gaussian Blur
- Canny Edge Detection
- Morphological operations (closing, dilation)
- Contour detection
- Bounding rectangle
- Alpha channel (BGRA)

Input:
- Ảnh sản phẩm chụp trên nền đơn giản (trắng/xám nhạt)
- Không có vật thể thứ hai lớn
- File: product.jpg

Output:
- Ảnh sản phẩm đã cắt gọn với nền trong suốt (PNG)
- Lưu tại: ../output/product_cropped.png

Tác giả đề bài: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
import os

if __name__ == "__main__":
    # Thiết lập đường dẫn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "product.jpg")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")

        # Tạo ảnh sản phẩm (chai nước) trên nền trắng
        img = np.ones((600, 800, 3), dtype=np.uint8) * 250  # Nền gần trắng

        # Vẽ chai
        # Thân chai
        cv2.rectangle(img, (350, 250), (450, 500), (100, 150, 200), -1)

        # Cổ chai
        cv2.rectangle(img, (370, 200), (430, 250), (100, 150, 200), -1)

        # Nắp chai
        cv2.rectangle(img, (365, 180), (435, 200), (50, 100, 150), -1)

        # Nhãn chai
        cv2.rectangle(img, (360, 300), (440, 400), (255, 200, 100), -1)
        cv2.putText(img, "WATER", (370, 360),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Thêm bóng mờ
        shadow = img.copy()
        cv2.ellipse(shadow, (400, 510), (100, 20), 0, 0, 360, (200, 200, 200), -1)
        img = cv2.addWeighted(img, 0.9, shadow, 0.1, 0)

        # Thêm highlight
        cv2.rectangle(img, (380, 270), (390, 350), (180, 200, 250), -1)

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Đọc ảnh
    img = cv2.imread(input_path)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    print("="*80)
    print("BÀI 6: CẮT NỀN (AUTO-CROP) ẢNH SẢN PHẨM")
    print("="*80)
    print(f"Ảnh gốc: {img.shape}")

    # Chuyển sang grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Làm mờ Gaussian
    blur = cv2.GaussianBlur(gray, (5,5), 1.0)

    # Canny edge detection
    edges = cv2.Canny(blur, 50, 150)

    print(f"Edge detection: Canny (threshold: 50, 150)")

    # Morphological operations để liền khối
    kernel = np.ones((5,5), np.uint8)

    # Closing: Lấp các khe hở trong contour
    mask = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Dilation: Mở rộng contour để chắc chắn bao hết vật thể
    mask = cv2.dilate(mask, kernel, iterations=2)

    print(f"Morphology: Closing (2 iter) + Dilation (2 iter)")

    # Tìm contours
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not cnts:
        print("ERROR: Không tìm thấy contour!")
        exit(1)

    # Chọn contour lớn nhất
    cnt = max(cnts, key=cv2.contourArea)
    area = cv2.contourArea(cnt)

    print(f"Tìm thấy {len(cnts)} contours")
    print(f"Contour lớn nhất: {area:.0f} pixels")

    # Tạo mask đầy đủ từ contour
    mask_full = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask_full, [cnt], -1, 255, thickness=-1)

    # Lấy bounding rectangle để crop
    x, y, w, h = cv2.boundingRect(cnt)

    print(f"Bounding box: x={x}, y={y}, w={w}, h={h}")

    # Crop ảnh và mask
    crop_img = img[y:y+h, x:x+w]
    crop_mask = mask_full[y:y+h, x:x+w]

    # Xuất PNG với alpha channel
    bgra = cv2.cvtColor(crop_img, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = crop_mask  # Set alpha channel

    # Lưu kết quả
    output_path = os.path.join(output_dir, 'product_cropped.png')
    cv2.imwrite(output_path, bgra)

    # Lưu các ảnh trung gian để debug
    cv2.imwrite(os.path.join(output_dir, 'product_edges.png'), edges)
    cv2.imwrite(os.path.join(output_dir, 'product_mask.png'), mask)
    cv2.imwrite(os.path.join(output_dir, 'product_mask_full.png'), mask_full)

    # Tạo ảnh overlay để visualize
    overlay = img.copy()
    cv2.drawContours(overlay, [cnt], -1, (0, 255, 0), 3)
    cv2.rectangle(overlay, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.imwrite(os.path.join(output_dir, 'product_contour.jpg'), overlay)

    print("\n" + "="*80)
    print("PHÂN TÍCH & KẾT LUẬN")
    print("="*80)

    print(f"""
1. Quy trình xử lý:
   a) Canny edge detection: Tìm biên sắc nét
   b) Morphological closing: Lấp khe hở trong contour
   c) Dilation: Mở rộng để bao trọn vật thể
   d) Tìm contour lớn nhất: Chọn sản phẩm chính
   e) Tight crop: Cắt theo bounding rectangle
   f) Alpha matte: Tạo nền trong suốt

2. Ưu điểm:
   - Tự động, không cần input thủ công
   - Hoạt động tốt với nền đơn giản
   - Kết quả PNG với alpha channel chất lượng cao
   - Tight crop tiết kiệm dung lượng

3. Hạn chế:
   - Yêu cầu nền tương phản với sản phẩm
   - Không xử lý được nhiều sản phẩm
   - Morphology có thể làm mất chi tiết mảnh

4. Cải tiến có thể:
   - Sử dụng GrabCut cho mask chính xác hơn
   - Thêm feathering cho alpha channel mượt hơn
   - Xử lý trường hợp bóng/phản chiếu
   - Refinement với edge-aware filtering

5. Ứng dụng:
   - E-commerce: Tạo ảnh sản phẩm nền trắng
   - Product photography: Batch processing
   - Marketing: Tạo composite ảnh
   - QC: Tự động crop ảnh sản phẩm

Kích thước gốc: {img.shape[1]}x{img.shape[0]}
Kích thước sau crop: {w}x{h}
Tiết kiệm: {(1 - (w*h)/(img.shape[0]*img.shape[1]))*100:.1f}% diện tích
    """)

    print(f"\nĐã lưu kết quả tại:")
    print(f"  - {output_path} (PNG với nền trong suốt)")
    print(f"  - product_edges.png (Canny edges)")
    print(f"  - product_mask.png (Mask sau morphology)")
    print(f"  - product_contour.jpg (Visualization)")
    print("\nHoàn thành!")
