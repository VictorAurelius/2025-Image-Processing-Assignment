"""
Script tạo tất cả ảnh mẫu cho bài tập T61
"""

import cv2
import numpy as np
import os

def create_all_samples():
    """Tạo tất cả ảnh mẫu"""
    print("="*80)
    print("TẠO ẢNH MẪU CHO BÀI TẬP T61 - XỬ LÝ HÌNH THÁI")
    print("="*80)

    # 1. Văn bản có nhiễu (Bài 1)
    print("\n[1/9] Tạo ảnh văn bản có nhiễu...")
    os.makedirs('docs', exist_ok=True)
    img = np.ones((400, 600), dtype=np.uint8) * 255
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'Xin chao!', (50, 100), font, 2, 0, 3)
    cv2.putText(img, 'Image Processing', (50, 200), font, 1.5, 0, 2)
    cv2.putText(img, 'Morphological Operations', (50, 300), font, 1, 0, 2)
    noise = np.random.rand(*img.shape)
    img[noise < 0.02] = 0
    img[noise > 0.98] = 255
    cv2.imwrite('docs/noisy_scan.png', img)
    print("    ✓ Đã tạo docs/noisy_scan.png")

    # 2. Linh kiện có khe hở (Bài 2)
    print("[2/9] Tạo ảnh linh kiện có khe hở...")
    os.makedirs('parts', exist_ok=True)
    img = np.ones((400, 600), dtype=np.uint8) * 255
    cv2.rectangle(img, (50, 50), (200, 150), 0, -1)
    cv2.rectangle(img, (90, 90), (120, 110), 255, -1)
    cv2.circle(img, (400, 100), 60, 0, -1)
    cv2.circle(img, (410, 90), 20, 255, -1)
    pts = np.array([[100, 250], [200, 250], [150, 350]], np.int32)
    cv2.fillPoly(img, [pts], 0)
    cv2.circle(img, (150, 280), 15, 255, -1)
    cv2.imwrite('parts/gapped.png', img)
    print("    ✓ Đã tạo parts/gapped.png")

    # 3. Các vật thể mẫu (Bài 3)
    print("[3/9] Tạo ảnh các vật thể...")
    os.makedirs('objects', exist_ok=True)
    img = np.ones((400, 600), dtype=np.uint8) * 255
    cv2.rectangle(img, (50, 50), (200, 150), 0, -1)
    cv2.circle(img, (400, 100), 60, 0, -1)
    pts = np.array([[100, 250], [200, 250], [150, 350]], np.int32)
    cv2.fillPoly(img, [pts], 0)
    cv2.ellipse(img, (450, 300), (80, 40), 30, 0, 360, 0, -1)
    cv2.imwrite('objects/sample.png', img)
    print("    ✓ Đã tạo objects/sample.png")

    # 4. Đồng xu chạm nhau (Bài 4)
    print("[4/9] Tạo ảnh đồng xu chạm nhau...")
    os.makedirs('coins', exist_ok=True)
    img = np.ones((500, 600, 3), dtype=np.uint8) * 255
    coins = [
        ((100, 100), 50), ((180, 110), 50), ((140, 180), 50),
        ((350, 120), 60), ((450, 130), 55), ((400, 230), 58),
        ((200, 350), 52), ((340, 380), 56), ((480, 370), 54),
    ]
    for center, radius in coins:
        cv2.circle(img, center, radius, (100, 100, 100), -1)
    cv2.imwrite('coins/touching.jpg', img)
    print("    ✓ Đã tạo coins/touching.jpg")

    # 5. Biển số xe (Bài 5)
    print("[5/9] Tạo ảnh biển số xe...")
    os.makedirs('plates', exist_ok=True)
    img = np.ones((150, 500), dtype=np.uint8) * 255
    cv2.putText(img, '29A-12345', (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 2.5, 0, 5)
    for _ in range(50):
        x = np.random.randint(0, img.shape[1])
        y = np.random.randint(0, img.shape[0])
        cv2.circle(img, (x, y), np.random.randint(1, 3), 0, -1)
    cv2.imwrite('plates/plate.jpg', img)
    print("    ✓ Đã tạo plates/plate.jpg")

    # 6. Bề mặt có lỗ (Bài 6)
    print("[6/9] Tạo ảnh bề mặt có lỗ...")
    os.makedirs('surface', exist_ok=True)
    img = np.ones((500, 600), dtype=np.uint8) * 255
    small = [(50, 50, 10), (100, 60, 12), (150, 55, 15), (80, 120, 11),
             (130, 130, 13), (180, 125, 14), (60, 190, 12), (110, 200, 10)]
    medium = [(300, 80, 25), (400, 90, 28), (500, 85, 30), (320, 200, 27),
              (420, 210, 32), (520, 205, 29), (350, 320, 26), (450, 330, 31)]
    large = [(100, 350, 40), (250, 360, 45), (400, 355, 50),
             (180, 450, 42), (330, 455, 48), (480, 450, 52)]
    for x, y, r in small + medium + large:
        cv2.circle(img, (x, y), r, 0, -1)
    cv2.imwrite('surface/holes.png', img)
    print("    ✓ Đã tạo surface/holes.png")

    # 7. Biên có gai (Bài 7)
    print("[7/9] Tạo ảnh biên có gai...")
    os.makedirs('edges', exist_ok=True)
    img = np.ones((400, 600), dtype=np.uint8) * 255
    cv2.line(img, (50, 100), (550, 100), 0, 2)
    for x in range(100, 500, 30):
        cv2.line(img, (x, 100), (x + 5, 90), 0, 1)
        cv2.line(img, (x + 15, 100), (x + 18, 110), 0, 1)
    cv2.line(img, (300, 150), (300, 350), 0, 2)
    for y in range(180, 330, 25):
        cv2.line(img, (300, y), (290, y + 3), 0, 1)
        cv2.line(img, (300, y + 12), (310, y + 15), 0, 1)
    cv2.imwrite('edges/jagged.png', img)
    print("    ✓ Đã tạo edges/jagged.png")

    # 8. Băng chuyền (Bài 8)
    print("[8/9] Tạo ảnh băng chuyền...")
    os.makedirs('conveyor', exist_ok=True)
    img = np.ones((500, 700), dtype=np.uint8) * 200
    cv2.rectangle(img, (50, 100), (200, 250), 255, -1)
    cv2.circle(img, (350, 175), 80, 255, -1)
    cv2.ellipse(img, (550, 175), (70, 50), 0, 0, 360, 255, -1)
    pts = np.array([[125, 350], [225, 350], [175, 450]], np.int32)
    cv2.fillPoly(img, [pts], 255)
    cv2.imwrite('conveyor/items.png', img)
    print("    ✓ Đã tạo conveyor/items.png")

    # 9. Chiếu sáng không đều (Bài 9)
    print("[9/9] Tạo ảnh chiếu sáng không đều...")
    img = np.ones((600, 800), dtype=np.uint8) * 128
    y, x = np.ogrid[:600, :800]
    gradient = 255 - ((x / 800.0) * 100 + (y / 600.0) * 80)
    gradient = np.clip(gradient, 100, 255).astype(np.uint8)
    img = cv2.addWeighted(img, 0.5, gradient, 0.5, 0)
    cv2.putText(img, 'Document Text', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, 30, 3)
    cv2.putText(img, 'Image Processing', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, 40, 2)
    cv2.rectangle(img, (500, 100), (650, 200), 50, -1)
    cv2.circle(img, (650, 150), 30, 200, -1)
    cv2.imwrite('docs/uneven.jpg', img)
    print("    ✓ Đã tạo docs/uneven.jpg")

    print("\n" + "="*80)
    print("✓ HOÀN THÀNH! Đã tạo tất cả 9 ảnh mẫu.")
    print("="*80)

if __name__ == "__main__":
    create_all_samples()
