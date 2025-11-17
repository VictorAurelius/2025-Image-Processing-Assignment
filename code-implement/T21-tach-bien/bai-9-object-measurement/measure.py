"""
Bài 9 — Đo kích thước vật thể bằng chuẩn kích thước (coin/A4) + biên

Mục tiêu:
- Tách biên → contour lớn nhất của vật thể cần đo
- Tìm đường kính đồng xu (HoughCircles) hoặc cạnh A4 → suy ra tỉ lệ px/mm
- Đo chiều dài/chiều rộng của vật thể và quy đổi mm

Kỹ thuật sử dụng:
- Hough Circle Transform để tìm đồng xu chuẩn
- Canny edge detection
- Contour detection
- MinAreaRect để tìm kích thước vật thể
- Perspective correction (nếu cần)

Input:
- Ảnh có một đồng xu/A4 làm chuẩn
- Vật thể cần đo (ví dụ: con ốc, vít, ...)
- File: measure.jpg
- Camera đặt gần vuông góc

Output:
- Ảnh với kích thước đã đo (mm)
- Tỉ lệ px/mm
- Lưu tại: ../output/measure_out.jpg

Tác giả đề bài: TS. Phan Thanh Toàn
"""

import cv2
import numpy as np
import math
import os

if __name__ == "__main__":
    # Thiết lập đường dẫn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "input", "sample-images", "measure.jpg")
    output_dir = os.path.join(script_dir, "..", "output")

    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)

    # Kiểm tra và tạo ảnh mẫu nếu cần
    if not os.path.exists(input_path):
        print(f"WARNING: File {input_path} không tồn tại!")
        print("Tạo ảnh mẫu...")

        # Tạo ảnh nền
        img = np.ones((700, 900, 3), dtype=np.uint8) * 200

        # Texture nền
        noise = np.random.normal(0, 8, (700, 900)).astype(np.int16)
        for c in range(3):
            img[:, :, c] = np.clip(img[:, :, c].astype(np.int16) + noise, 0, 255)

        # Vẽ đồng xu chuẩn (đường kính giả sử 23.6mm - Euro coin)
        coin_center = (150, 150)
        coin_radius = 60  # pixels
        # Màu vàng
        for r in range(coin_radius, 0, -1):
            brightness = int(255 * (r / coin_radius))
            color = (brightness * 180 // 255, brightness * 160 // 255, brightness * 90 // 255)
            cv2.circle(img, coin_center, r, color, -1)
        cv2.circle(img, coin_center, coin_radius, (100, 100, 100), 2)
        # Highlight
        cv2.circle(img, (coin_center[0] - 20, coin_center[1] - 20), 15, (255, 255, 255), -1, cv2.LINE_AA)

        # Vẽ vật thể cần đo (con ốc/vít - hình chữ nhật với đầu tròn)
        # Phần thân (chiều dài ~80mm, chiều rộng ~15mm trong thực tế)
        # Giả sử tỉ lệ: 60px = 23.6mm → 1mm ≈ 2.54px
        # 80mm ≈ 203px, 15mm ≈ 38px
        obj_center = (600, 400)
        obj_width = 38
        obj_height = 203

        # Xoay một góc để thú vị hơn
        angle = 25

        # Vẽ thân vít (màu xám kim loại)
        rect = ((obj_center[0], obj_center[1]), (obj_width, obj_height), angle)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img, [box], 0, (140, 140, 140), -1)

        # Viền
        cv2.drawContours(img, [box], 0, (80, 80, 80), 2)

        # Vẽ đầu vít (phần tròn)
        # Tính vị trí đầu
        rad = math.radians(angle)
        head_offset_x = int((obj_height / 2 + 20) * math.sin(rad))
        head_offset_y = int((obj_height / 2 + 20) * math.cos(rad))
        head_center = (obj_center[0] - head_offset_x, obj_center[1] - head_offset_y)

        cv2.circle(img, head_center, 25, (160, 160, 160), -1)
        cv2.circle(img, head_center, 25, (80, 80, 80), 2)

        # Vẽ rãnh chữ thập trên đầu vít
        cv2.line(img, (head_center[0] - 15, head_center[1]), (head_center[0] + 15, head_center[1]), (80, 80, 80), 2)
        cv2.line(img, (head_center[0], head_center[1] - 15), (head_center[0], head_center[1] + 15), (80, 80, 80), 2)

        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        cv2.imwrite(input_path, img)
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    # Đọc ảnh
    img = cv2.imread(input_path)

    if img is None:
        print(f"ERROR: Không thể đọc ảnh từ {input_path}")
        exit(1)

    print("="*80)
    print("BÀI 9: ĐO KÍCH THƯỚC VẬT THỂ BẰNG CHUẨN KÍCH THƯỚC")
    print("="*80)
    print(f"Ảnh gốc: {img.shape}")

    # Chuyển sang grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"\n=== BƯỚC 1: TÌM ĐỒNG XU CHUẨN ===")

    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (7, 7), 1.2)
    print(f"1. Đã áp dụng Gaussian blur (σ=1.2)")

    # Tìm đồng xu làm chuẩn bằng HoughCircles
    cir = cv2.HoughCircles(
        blur,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=50,
        param1=120,
        param2=25,
        minRadius=20,
        maxRadius=120
    )

    if cir is None:
        print("\nERROR: Không thấy đồng xu chuẩn trong ảnh!")
        print("Vui lòng đảm bảo có đồng xu trong ảnh để làm chuẩn đo.")
        exit(1)

    x, y, r = np.round(cir[0, 0]).astype(int)
    print(f"2. ✓ Phát hiện đồng xu: tâm=({x},{y}), bán kính={r} pixels")

    # Kích thước thực của đồng xu (mm)
    # Ví dụ: đồng 1 Euro = 23.6mm, đồng 500 VND = 24mm
    coin_d_mm = 23.6  # Thay đổi theo đồng xu thực tế
    print(f"3. Đường kính đồng xu chuẩn: {coin_d_mm} mm")

    # Tính tỉ lệ px/mm
    px_per_mm = (2 * r) / coin_d_mm
    print(f"4. Tỉ lệ: {px_per_mm:.3f} pixels/mm")

    print(f"\n=== BƯỚC 2: TÌM VÀ ĐO VẬT THỂ ===")

    # Canny edge detection
    edges = cv2.Canny(blur, 80, 160)
    print(f"5. Đã phát hiện biên bằng Canny (ngưỡng: 80, 160)")

    # Tìm contours
    cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"6. Tìm thấy {len(cnts)} contours")

    # Lọc contours theo diện tích (loại bỏ đồng xu và nhiễu)
    valid_cnts = []
    coin_area = math.pi * r * r

    for cnt in cnts:
        area = cv2.contourArea(cnt)
        # Bỏ qua contour quá nhỏ hoặc là đồng xu
        if area > 500 and abs(area - coin_area) > coin_area * 0.3:
            valid_cnts.append(cnt)

    if len(valid_cnts) == 0:
        print("\nWARNING: Không tìm thấy vật thể để đo!")
        print("Sử dụng contour lớn nhất không phải đồng xu...")
        # Lấy contour lớn nhất không phải đồng xu
        cnts_sorted = sorted(cnts, key=cv2.contourArea, reverse=True)
        for cnt in cnts_sorted:
            area = cv2.contourArea(cnt)
            if abs(area - coin_area) > coin_area * 0.3:
                valid_cnts = [cnt]
                break

    if len(valid_cnts) == 0:
        print("ERROR: Không tìm thấy vật thể hợp lệ!")
        exit(1)

    # Lấy contour lớn nhất trong các contour hợp lệ
    cnt = max(valid_cnts, key=cv2.contourArea)
    area = cv2.contourArea(cnt)
    print(f"7. Chọn vật thể có diện tích: {area:.0f} pixels²")

    # Tính minAreaRect (bounding box xoay)
    rect = cv2.minAreaRect(cnt)
    (cx, cy), (w, h), angle = rect

    # w, h luôn là chiều ngắn và chiều dài
    # Đảm bảo w < h
    if w > h:
        w, h = h, w
        angle = angle + 90

    print(f"8. MinAreaRect:")
    print(f"   - Tâm: ({cx:.1f}, {cy:.1f})")
    print(f"   - Kích thước (pixels): {w:.1f} × {h:.1f}")
    print(f"   - Góc xoay: {angle:.1f}°")

    # Quy đổi sang mm
    w_mm = w / px_per_mm
    h_mm = h / px_per_mm
    area_mm2 = (area / (px_per_mm ** 2))

    print(f"\n9. Kích thước thực (mm):")
    print(f"   - Chiều rộng: {w_mm:.2f} mm")
    print(f"   - Chiều dài: {h_mm:.2f} mm")
    print(f"   - Diện tích: {area_mm2:.2f} mm²")

    # Tạo ảnh kết quả
    out = img.copy()

    # Vẽ đồng xu chuẩn (màu xanh dương)
    cv2.circle(out, (x, y), r, (255, 0, 0), 3)
    cv2.circle(out, (x, y), 3, (255, 0, 0), -1)
    cv2.putText(out, f"Standard: {coin_d_mm}mm", (x - 60, y - r - 10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Vẽ vật thể (màu xanh lá)
    box = np.int0(cv2.boxPoints(rect))
    cv2.drawContours(out, [box], 0, (0, 255, 0), 3)

    # Đánh dấu góc
    for i, pt in enumerate(box):
        cv2.circle(out, tuple(pt), 5, (0, 0, 255), -1)

    # Thêm text kích thước
    text_x = int(box[0][0])
    text_y = int(box[0][1]) - 15

    cv2.putText(out, f"{w_mm:.2f} x {h_mm:.2f} mm",
               (text_x, text_y),
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Vẽ các đường đo
    # Chiều rộng
    mid1 = ((box[0][0] + box[1][0]) // 2, (box[0][1] + box[1][1]) // 2)
    mid2 = ((box[2][0] + box[3][0]) // 2, (box[2][1] + box[3][1]) // 2)
    cv2.line(out, mid1, mid2, (255, 255, 0), 2)
    cv2.putText(out, f"W: {w_mm:.1f}mm",
               ((mid1[0] + mid2[0]) // 2, (mid1[1] + mid2[1]) // 2 - 10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    # Chiều dài
    mid3 = ((box[1][0] + box[2][0]) // 2, (box[1][1] + box[2][1]) // 2)
    mid4 = ((box[3][0] + box[0][0]) // 2, (box[3][1] + box[0][1]) // 2)
    cv2.line(out, mid3, mid4, (255, 0, 255), 2)
    cv2.putText(out, f"H: {h_mm:.1f}mm",
               ((mid3[0] + mid4[0]) // 2 + 10, (mid3[1] + mid4[1]) // 2),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

    # Thêm thông tin tỉ lệ
    cv2.putText(out, f"Scale: {px_per_mm:.3f} px/mm",
               (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Lưu kết quả
    output_path = os.path.join(output_dir, 'measure_out.jpg')
    cv2.imwrite(output_path, out)

    # Lưu edges (debug)
    edges_path = os.path.join(output_dir, 'measure_edges.png')
    cv2.imwrite(edges_path, edges)

    print("\n" + "="*80)
    print("KẾT QUẢ ĐO LƯỜNG")
    print("="*80)
    print(f"\nĐồng xu chuẩn:")
    print(f"  - Đường kính: {coin_d_mm} mm = {2*r} pixels")
    print(f"  - Tỉ lệ: {px_per_mm:.3f} pixels/mm")
    print(f"  - Hay: 1 mm = {px_per_mm:.3f} pixels")

    print(f"\nVật thể đo được:")
    print(f"  - Kích thước: {w_mm:.2f} × {h_mm:.2f} mm")
    print(f"  - Diện tích: {area_mm2:.2f} mm²")
    print(f"  - Chu vi: {cv2.arcLength(cnt, True)/px_per_mm:.2f} mm")
    print(f"  - Góc xoay: {angle:.1f}°")

    # Tính thêm một số đặc trưng
    perimeter_mm = cv2.arcLength(cnt, True) / px_per_mm
    compactness = (4 * math.pi * area_mm2) / (perimeter_mm ** 2)

    print(f"\nĐặc trưng hình học:")
    print(f"  - Aspect ratio (H/W): {h_mm/w_mm:.3f}")
    print(f"  - Compactness: {compactness:.3f}")

    if compactness > 0.8:
        print(f"  → Hình dạng gần tròn")
    elif compactness > 0.5:
        print(f"  → Hình dạng compact")
    else:
        print(f"  → Hình dạng dài/elongated")

    print(f"\nĐã lưu:")
    print(f"  - Ảnh kết quả: {output_path}")
    print(f"  - Ảnh edges: {edges_path}")
    print("\nHoàn thành!")
