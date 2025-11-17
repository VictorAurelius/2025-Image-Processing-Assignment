"""
Bài 3 — Dò làn đường cơ bản cho ảnh camera hành trình

Mục tiêu:
- Tiền xử lý ROI (vùng nón phía trước)
- Dùng Sobel hướng x/y để khuếch đại biên dọc
- Sử dụng Hough Lines để tìm đường thẳng

Kỹ thuật sử dụng:
- ROI masking (Region of Interest)
- Gaussian Blur để giảm nhiễu
- Sobel edge detection theo hướng x
- Hough Lines Transform (HoughLinesP)
- Phân tách trái/phải theo hệ số góc

Input:
- Ảnh hoặc frame video từ camera trước xe trên đường cao tốc
- Điều kiện: ngày, trời nắng
- File: road.jpg

Output:
- Ảnh với làn đường được highlight
- Lưu tại: ../output/lanes_overlay.jpg

Tác giả đề bài: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
import os

if __name__ == "__main__":
    # Thiết lập đường dẫn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "road.jpg")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")

        # Tạo ảnh đường cao tốc mẫu
        img = np.ones((600, 800, 3), dtype=np.uint8) * 80  # Nền xám đen (asphalt)

        # Vẽ nền đường
        cv2.rectangle(img, (0, 300), (800, 600), (70, 70, 70), -1)

        # Vẽ làn đường trái (vàng)
        pts_left = np.array([
            [100, 600], [200, 360], [220, 360], [120, 600]
        ], np.int32)
        cv2.fillPoly(img, [pts_left], (0, 200, 255))

        # Vẽ làn đường phải (trắng)
        pts_right = np.array([
            [680, 600], [580, 360], [600, 360], [700, 600]
        ], np.int32)
        cv2.fillPoly(img, [pts_right], (255, 255, 255))

        # Vẽ làn giữa (trắng đứt quãng)
        for i in range(6):
            y_start = 600 - i*80
            y_end = y_start - 40
            x_start = 400 - int((600-y_start) * 0.1)
            x_end = 400 - int((600-y_end) * 0.1)
            pts = np.array([
                [x_start-5, y_start], [x_end-5, y_end],
                [x_end+5, y_end], [x_start+5, y_start]
            ], np.int32)
            cv2.fillPoly(img, [pts], (255, 255, 255))

        # Thêm một chút texture
        noise = np.random.randint(-20, 20, img.shape, dtype=np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        # Vẽ bầu trời
        cv2.rectangle(img, (0, 0), (800, 300), (180, 200, 220), -1)

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Đọc ảnh
    img = cv2.imread(input_path)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    h, w, _ = img.shape

    print("="*80)
    print("BÀI 3: DÒ LÀN ĐƯỜNG CƠ BẢN")
    print("="*80)
    print(f"Ảnh gốc: {img.shape}")

    # Chuyển sang grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Tạo ROI mask (vùng hình thang phía trước)
    roi = np.array([[
        (int(w*0.1), h),
        (int(w*0.45), int(h*0.6)),
        (int(w*0.55), int(h*0.6)),
        (int(w*0.9), h)
    ]], np.int32)

    mask = np.zeros_like(gray)
    cv2.fillPoly(mask, roi, 255)
    gray = cv2.bitwise_and(gray, mask)

    print(f"ROI: Vùng hình thang từ y={int(h*0.6)} đến y={h}")

    # Làm mờ Gaussian
    blur = cv2.GaussianBlur(gray, (5,5), 1.2)

    # Sobel theo x để nhấn mạnh biên dọc (làn đường)
    gx = cv2.Sobel(blur, cv2.CV_32F, 1, 0, ksize=3)
    mag = np.abs(gx)

    # Ngưỡng để lấy edges
    thr = 0.3 * mag.max()
    edges = (mag >= thr).astype(np.uint8) * 255

    print(f"Edge detection: Sobel-x với ngưỡng = {thr:.1f}")

    # Hough Lines Transform để tìm đường thẳng
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi/180,
        threshold=60,
        minLineLength=50,
        maxLineGap=150
    )

    # Phân loại đường trái/phải dựa vào slope
    left, right = [], []

    if lines is not None:
        print(f"Tìm thấy {len(lines)} đoạn thẳng từ Hough Transform")

        for x1, y1, x2, y2 in lines[:,0]:
            if x2 == x1:
                continue  # Bỏ qua đường thẳng đứng

            slope = (y2 - y1) / (x2 - x1 + 1e-6)

            # Phân loại dựa vào slope
            if slope < -0.5:  # Slope âm = làn trái
                left.append((x1, y1, x2, y2))
            elif slope > 0.5:  # Slope dương = làn phải
                right.append((x1, y1, x2, y2))

        print(f"  - Làn trái: {len(left)} đoạn thẳng")
        print(f"  - Làn phải: {len(right)} đoạn thẳng")
    else:
        print("Không tìm thấy đường thẳng!")

    # Vẽ kết quả
    out = img.copy()

    # Vẽ ROI
    cv2.polylines(out, roi, True, (255, 0, 255), 2)

    # Vẽ làn trái (xanh lá)
    for x1, y1, x2, y2 in left:
        cv2.line(out, (x1, y1), (x2, y2), (0, 255, 0), 3)

    # Vẽ làn phải (xanh dương)
    for x1, y1, x2, y2 in right:
        cv2.line(out, (x1, y1), (x2, y2), (255, 0, 0), 3)

    # Thêm chú thích
    cv2.putText(out, "Lan trai (xanh la)", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(out, "Lan phai (xanh duong)", (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.putText(out, "ROI (hong)", (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

    # Lưu kết quả
    output_path = os.path.join(output_dir, 'lanes_overlay.jpg')
    cv2.imwrite(output_path, out)

    # Lưu ảnh edges để debug
    edges_path = os.path.join(output_dir, 'lanes_edges.jpg')
    cv2.imwrite(edges_path, edges)

    print("\n" + "="*80)
    print("PHÂN TÍCH & KẾT LUẬN")
    print("="*80)

    print("""
1. ROI (Region of Interest):
   - Giới hạn vùng xử lý ở phần đường phía trước
   - Giảm nhiễu từ bầu trời, biển báo, xe khác
   - Hình thang để phù hợp với phối cảnh

2. Sobel theo hướng x:
   - Khuếch đại biên dọc (làn đường thường dọc)
   - Bỏ qua biên ngang (vệt nứt ngang đường)
   - Hiệu quả hơn magnitude cho bài toán này

3. Hough Lines:
   - Tìm đoạn thẳng trong ảnh edges
   - Parameters quan trọng:
     * threshold: 60 (số vote tối thiểu)
     * minLineLength: 50 (độ dài tối thiểu)
     * maxLineGap: 150 (khoảng cách tối đa giữa 2 đoạn)

4. Phân loại trái/phải:
   - Dựa vào slope (hệ số góc)
   - Slope < -0.5: Làn trái (góc nghiêng xuống trái)
   - Slope > 0.5: Làn phải (góc nghiêng xuống phải)

5. Cải tiến có thể:
   - Ngoại suy các đoạn thẳng thành 1 đường liền
   - Sử dụng Kalman filter để smooth giữa các frame (video)
   - Phát hiện đường cong bằng polynomial fitting
   - Xử lý trường hợp thiếu làn (1 bên)
    """)

    print(f"\nĐã lưu kết quả tại:")
    print(f"  - {output_path}")
    print(f"  - {edges_path}")
    print("\nHoàn thành!")
