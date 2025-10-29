"""
Script tự động tạo ảnh mẫu cho T1: Biểu diễn và Thu nhận Ảnh

Tạo tất cả ảnh cần thiết cho các bài tập và lab.
"""

import cv2
import numpy as np
import os

def create_output_dir():
    """Tạo thư mục output"""
    output_dir = os.path.join(os.path.dirname(__file__), "sample-images")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def generate_scan_de_thi(output_dir):
    """Tạo ảnh scan đề thi mẫu"""
    print("Tạo scan_de_thi.png...")

    img = np.ones((800, 600), dtype=np.uint8) * 255

    # Header
    cv2.putText(img, "EXAM / DE THI", (150, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, 0, 3)
    cv2.line(img, (50, 100), (550, 100), 0, 2)

    # Questions
    questions = [
        "Question 1: What is image processing?",
        "a) Processing images digitally",
        "b) Printing images",
        "c) Taking photos",
        "",
        "Question 2: What is quantization?",
        "a) Reducing bit depth",
        "b) Increasing resolution",
        "c) Color conversion",
        "",
        "Question 3: Define PSNR metric.",
        "_________________________________",
        "_________________________________",
    ]

    y = 150
    for q in questions:
        if q:
            cv2.putText(img, q, (70, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1)
        y += 35

    # Footer
    cv2.putText(img, "Good luck!", (230, 750),
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, 0, 2)

    # Thêm texture nhẹ (giống scan thật)
    noise = np.random.randint(-5, 5, img.shape, dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    output_path = os.path.join(output_dir, "scan_de_thi.png")
    cv2.imwrite(output_path, img)
    print(f"  ✓ Đã tạo: {output_path}")

def generate_bill(output_dir):
    """Tạo ảnh hóa đơn với nhiễu muối tiêu"""
    print("Tạo bill.png...")

    img = np.ones((600, 800), dtype=np.uint8) * 240

    # Header
    cv2.putText(img, "INVOICE / HOA DON", (200, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, 0, 2)
    cv2.line(img, (50, 120), (750, 120), 0, 2)

    # Info
    cv2.putText(img, "Date: 29/10/2025", (80, 160),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, 0, 1)
    cv2.putText(img, "Invoice #: 12345", (80, 190),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, 0, 1)

    # Items
    items = [
        "Item 1: Product A ......... 100,000 VND",
        "Item 2: Product B ......... 250,000 VND",
        "Item 3: Product C ......... 150,000 VND",
    ]

    y = 250
    for item in items:
        cv2.putText(img, item, (80, y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, 0, 1)
        y += 40

    cv2.line(img, (80, y+10), (720, y+10), 0, 1)
    cv2.putText(img, "Total: .................... 500,000 VND", (80, y+50),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, 0, 2)

    # Thêm nhiễu muối tiêu
    noise = np.random.rand(*img.shape)
    img[noise < 0.01] = 0      # Muối (đen)
    img[noise > 0.99] = 255    # Tiêu (trắng)

    output_path = os.path.join(output_dir, "bill.png")
    cv2.imwrite(output_path, img)
    print(f"  ✓ Đã tạo: {output_path}")

def generate_portrait(output_dir):
    """Tạo ảnh portrait mẫu với vùng da"""
    print("Tạo portrait.jpg...")

    img = np.ones((480, 640, 3), dtype=np.uint8) * 200

    # Background gradient
    for i in range(480):
        img[i, :] = [180 - i//8, 190 - i//10, 200 - i//12]

    # Face (ellipse with skin color)
    # Màu da trung bình trong BGR: (150, 180, 220)
    skin_color = (150, 180, 220)
    cv2.ellipse(img, (320, 240), (120, 150), 0, 0, 360, skin_color, -1)

    # Neck
    cv2.rectangle(img, (280, 360), (360, 480), skin_color, -1)

    # Eyes (simple representation)
    cv2.ellipse(img, (280, 220), (15, 10), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(img, (360, 220), (15, 10), 0, 0, 360, (255, 255, 255), -1)
    cv2.circle(img, (280, 220), 5, (0, 0, 0), -1)
    cv2.circle(img, (360, 220), 5, (0, 0, 0), -1)

    # Mouth
    cv2.ellipse(img, (320, 300), (30, 15), 0, 0, 180, (100, 100, 150), 2)

    # Hair
    cv2.ellipse(img, (320, 180), (130, 100), 0, 180, 360, (30, 30, 30), -1)

    # Thêm texture
    noise = np.random.randint(-10, 10, img.shape, dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    output_path = os.path.join(output_dir, "portrait.jpg")
    cv2.imwrite(output_path, img)
    print(f"  ✓ Đã tạo: {output_path}")

def generate_doc(output_dir):
    """Tạo ảnh document với nhiều mức xám"""
    print("Tạo doc.png...")

    img = np.ones((600, 800), dtype=np.uint8) * 255

    # Title
    cv2.putText(img, "DOCUMENT SAMPLE", (200, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, 0, 3)
    cv2.line(img, (100, 150), (700, 150), 0, 2)

    # Text with different gray levels
    gray_levels = [50, 80, 110, 140, 170]
    y = 220
    for i, gray in enumerate(gray_levels):
        text = f"Line {i+1}: Gray level {gray} - Lorem ipsum dolor sit amet"
        cv2.putText(img, text, (120, y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, gray, 1)
        y += 50

    # Gradient bar
    for i in range(100):
        gray = int(i * 2.55)
        cv2.rectangle(img, (650, 200 + i), (750, 201 + i), gray, -1)

    # Border
    cv2.rectangle(img, (640, 190), (760, 310), 0, 2)
    cv2.putText(img, "Gradient", (655, 330),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1)

    output_path = os.path.join(output_dir, "doc.png")
    cv2.imwrite(output_path, img)
    print(f"  ✓ Đã tạo: {output_path}")

def generate_campus(output_dir):
    """Tạo ảnh campus mẫu"""
    print("Tạo campus.jpg...")

    img = np.ones((480, 640), dtype=np.uint8) * 200

    # Sky gradient
    for i in range(200):
        img[i, :] = 220 - i//4

    # Building
    cv2.rectangle(img, (100, 150), (250, 400), 100, -1)
    # Windows
    for i in range(3):
        for j in range(4):
            cv2.rectangle(img, (120 + i*40, 180 + j*50),
                         (150 + i*40, 210 + j*50), 255, -1)

    # Tree
    cv2.circle(img, (450, 250), 80, 50, -1)  # Leaves
    cv2.rectangle(img, (440, 250), (460, 400), 80, -1)  # Trunk

    # Ground
    cv2.rectangle(img, (0, 380), (640, 480), 120, -1)

    # Road line
    cv2.line(img, (0, 430), (640, 430), 255, 2)

    # Text
    cv2.putText(img, "CAMPUS", (280, 100),
               cv2.FONT_HERSHEY_SIMPLEX, 2, 0, 3)

    # Texture
    noise = np.random.randint(-8, 8, img.shape, dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    output_path = os.path.join(output_dir, "campus.jpg")
    cv2.imwrite(output_path, img)
    print(f"  ✓ Đã tạo: {output_path}")

def generate_pcb(output_dir):
    """Tạo ảnh mạch in mẫu"""
    print("Tạo pcb.png...")

    img = np.ones((400, 600), dtype=np.uint8) * 255

    # Horizontal traces
    cv2.line(img, (50, 50), (250, 50), 0, 3)
    cv2.line(img, (100, 50), (100, 150), 0, 3)
    cv2.line(img, (200, 50), (200, 150), 0, 3)

    # Pads
    for x in [50, 100, 150, 200, 250]:
        cv2.circle(img, (x, 50), 8, 0, -1)

    # Diagonal trace (test connectivity)
    for i in range(20):
        cv2.circle(img, (350 + i*5, 100 + i*5), 2, 0, -1)

    # Components
    cv2.rectangle(img, (400, 200), (450, 250), 0, -1)
    cv2.circle(img, (500, 225), 25, 0, -1)

    # Text
    cv2.putText(img, "PCB SAMPLE", (50, 350),
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, 0, 2)

    # More traces
    cv2.line(img, (50, 200), (250, 200), 0, 2)
    cv2.line(img, (150, 150), (150, 250), 0, 2)

    output_path = os.path.join(output_dir, "pcb.png")
    cv2.imwrite(output_path, img)
    print(f"  ✓ Đã tạo: {output_path}")

def generate_scene(output_dir):
    """Tạo ảnh cảnh tự nhiên"""
    print("Tạo scene.jpg...")

    img = np.ones((480, 640), dtype=np.uint8) * 180

    # Sky with gradient
    for i in range(200):
        img[i, :] = 200 - i//4

    # Mountains
    pts = np.array([[0, 300], [200, 150], [400, 250], [640, 200], [640, 480], [0, 480]])
    cv2.fillPoly(img, [pts], 100)

    # Sun
    cv2.circle(img, (500, 100), 40, 255, -1)

    # Trees
    for x in [100, 250, 400]:
        # Trunk
        cv2.rectangle(img, (x-5, 280), (x+5, 350), 60, -1)
        # Leaves
        cv2.circle(img, (x, 270), 25, 80, -1)

    # Ground
    cv2.rectangle(img, (0, 350), (640, 480), 110, -1)

    # Clouds
    cv2.ellipse(img, (150, 80), (40, 20), 0, 0, 360, 255, -1)
    cv2.ellipse(img, (400, 60), (50, 25), 0, 0, 360, 255, -1)

    # Texture
    noise_texture = np.random.randint(-10, 10, img.shape, dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise_texture, 0, 255).astype(np.uint8)

    output_path = os.path.join(output_dir, "scene.jpg")
    cv2.imwrite(output_path, img)
    print(f"  ✓ Đã tạo: {output_path}")

if __name__ == "__main__":
    print("="*60)
    print("TẠO ẢNH MẪU CHO T1: BIỂU DIỄN VÀ THU NHẬN ẢNH")
    print("="*60)
    print()

    output_dir = create_output_dir()
    print(f"Thư mục output: {output_dir}")
    print()

    # Tạo tất cả ảnh
    generate_scan_de_thi(output_dir)
    generate_bill(output_dir)
    generate_portrait(output_dir)
    generate_doc(output_dir)
    generate_campus(output_dir)
    generate_pcb(output_dir)
    generate_scene(output_dir)

    print()
    print("="*60)
    print("HOÀN TẤT!")
    print("="*60)
    print(f"Đã tạo 7 ảnh mẫu tại: {output_dir}")
    print()
    print("Danh sách file:")
    for fname in ["scan_de_thi.png", "bill.png", "portrait.jpg",
                  "doc.png", "campus.jpg", "pcb.png", "scene.jpg"]:
        fpath = os.path.join(output_dir, fname)
        if os.path.exists(fpath):
            size = os.path.getsize(fpath) / 1024
            print(f"  ✓ {fname} ({size:.1f} KB)")

    print()
    print("Bây giờ bạn có thể chạy các bài tập mà không cần chuẩn bị ảnh thủ công!")
