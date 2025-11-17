#!/usr/bin/env python3
"""
Generate Sample Images for Edge Detection Assignment
Creates 10 sample images for different edge detection scenarios
"""

import cv2
import numpy as np
import os
from pathlib import Path


def create_output_dir():
    """Create sample-images directory if it doesn't exist"""
    output_dir = Path(__file__).parent / "sample-images"
    output_dir.mkdir(exist_ok=True)
    return output_dir


def generate_building_image(output_path):
    """Generate a building image with geometric edges"""
    print("Creating building.jpg...")
    img = np.ones((600, 800, 3), dtype=np.uint8) * 135  # Sky color

    # Ground
    cv2.rectangle(img, (0, 400), (800, 600), (100, 120, 80), -1)

    # Main building
    cv2.rectangle(img, (200, 150), (600, 500), (180, 180, 190), -1)
    cv2.rectangle(img, (200, 150), (600, 500), (80, 80, 90), 3)

    # Windows (grid pattern)
    for row in range(4):
        for col in range(6):
            x = 230 + col * 60
            y = 200 + row * 70
            cv2.rectangle(img, (x, y), (x + 40, y + 50), (100, 140, 180), -1)
            cv2.rectangle(img, (x, y), (x + 40, y + 50), (60, 60, 70), 2)

    # Roof
    pts = np.array([[180, 150], [400, 50], [620, 150]], np.int32)
    cv2.fillPoly(img, [pts], (150, 100, 90))
    cv2.polylines(img, [pts], True, (80, 50, 40), 3)

    # Side building
    cv2.rectangle(img, (50, 250), (200, 500), (160, 160, 170), -1)
    cv2.rectangle(img, (50, 250), (200, 500), (70, 70, 80), 3)

    cv2.imwrite(str(output_path), img)


def generate_document_image(output_path):
    """Generate a document image for scanning"""
    print("Creating doc.jpg...")
    img = np.ones((800, 600, 3), dtype=np.uint8) * 50  # Dark background

    # Document (slightly rotated)
    center = (300, 400)
    angle = 15
    width, height = 400, 500

    # Create white document rectangle
    rect = cv2.boxPoints(((center[0], center[1]), (width, height), angle))
    rect = np.int0(rect)

    # White document
    cv2.fillPoly(img, [rect], (245, 245, 240))
    cv2.polylines(img, [rect], True, (200, 200, 200), 2)

    # Add text lines on document
    for i in range(10):
        # Calculate rotated line positions
        y_offset = -200 + i * 40
        line_start = rotate_point((150, y_offset), center, angle)
        line_end = rotate_point((450, y_offset), center, angle)
        cv2.line(img, line_start, line_end, (80, 80, 80), 2)

    cv2.imwrite(str(output_path), img)


def rotate_point(point, center, angle_deg):
    """Rotate a point around a center"""
    angle_rad = np.deg2rad(angle_deg)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)

    # Translate to origin
    x = point[0] - center[0]
    y = point[1] - center[1]

    # Rotate
    new_x = x * cos_a - y * sin_a
    new_y = x * sin_a + y * cos_a

    # Translate back
    return (int(new_x + center[0]), int(new_y + center[1]))


def generate_road_image(output_path):
    """Generate a road image with lane markings"""
    print("Creating road.jpg...")
    img = np.ones((600, 800, 3), dtype=np.uint8) * 60  # Dark road

    # Road surface
    cv2.rectangle(img, (0, 200), (800, 600), (70, 70, 70), -1)

    # Lane markings (perspective view)
    # Left lane
    pts_left = np.array([[250, 600], [280, 400], [320, 200], [100, 200], (0, 400), (0, 600)], np.int32)
    cv2.fillPoly(img, [pts_left], (85, 85, 85))

    # Right lane
    pts_right = np.array([[550, 600], [520, 400], [480, 200], [700, 200], (800, 400), (800, 600)], np.int32)
    cv2.fillPoly(img, [pts_right], (85, 85, 85))

    # Yellow center line
    cv2.line(img, (380, 600), (400, 200), (0, 180, 255), 4)
    cv2.line(img, (420, 600), (400, 200), (0, 180, 255), 4)

    # Dashed white lines
    for i in range(8):
        y1 = 600 - i * 70
        y2 = y1 - 40
        if y2 < 200:
            break
        # Left dashed
        x_left = 250 - (600 - y1) * 0.15
        cv2.line(img, (int(x_left), y1), (int(x_left), y2), (255, 255, 255), 3)
        # Right dashed
        x_right = 550 + (600 - y1) * 0.15
        cv2.line(img, (int(x_right), y1), (int(x_right), y2), (255, 255, 255), 3)

    cv2.imwrite(str(output_path), img)


def generate_surface_image(output_path):
    """Generate a surface image with defects"""
    print("Creating surface.jpg...")
    img = np.ones((600, 800, 3), dtype=np.uint8) * 200  # Light gray surface

    # Add texture
    noise = np.random.randint(-15, 15, (600, 800, 3), dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Add defects (dark spots)
    cv2.circle(img, (200, 150), 30, (120, 120, 120), -1)
    cv2.ellipse(img, (500, 300), (40, 25), 45, 0, 360, (100, 100, 100), -1)
    cv2.circle(img, (350, 450), 20, (110, 110, 110), -1)

    # Add scratches
    cv2.line(img, (100, 100), (300, 200), (80, 80, 80), 2)
    cv2.line(img, (600, 150), (750, 400), (90, 90, 90), 1)

    cv2.imwrite(str(output_path), img)


def generate_coins_image(output_path):
    """Generate an image with coins"""
    print("Creating coins.jpg...")
    img = np.ones((600, 800, 3), dtype=np.uint8) * 100  # Dark background

    # Define coin positions and sizes
    coins = [
        (150, 150, 60, (180, 160, 120)),  # Large gold coin
        (350, 180, 50, (200, 200, 210)),  # Medium silver coin
        (550, 150, 60, (180, 160, 120)),  # Large gold coin
        (200, 350, 45, (180, 160, 120)),  # Medium gold coin
        (450, 380, 50, (200, 200, 210)),  # Medium silver coin
        (650, 350, 45, (200, 200, 210)),  # Medium silver coin
        (300, 500, 40, (180, 160, 120)),  # Small gold coin
        (550, 480, 40, (180, 160, 120)),  # Small gold coin
    ]

    for x, y, r, color in coins:
        # Coin body
        cv2.circle(img, (x, y), r, color, -1)
        # Edge
        cv2.circle(img, (x, y), r, (max(0, color[0]-40), max(0, color[1]-40), max(0, color[2]-40)), 3)
        # Highlight
        cv2.circle(img, (x-10, y-10), int(r*0.3),
                  (min(255, color[0]+40), min(255, color[1]+40), min(255, color[2]+40)), -1)

    cv2.imwrite(str(output_path), img)


def generate_product_image(output_path):
    """Generate a product image on white background"""
    print("Creating product.jpg...")
    img = np.ones((600, 800, 3), dtype=np.uint8) * 250  # White background

    # Product (a box)
    # Front face
    cv2.rectangle(img, (250, 150), (550, 500), (180, 120, 100), -1)
    cv2.rectangle(img, (250, 150), (550, 500), (120, 80, 60), 3)

    # Top face (parallelogram for 3D effect)
    pts_top = np.array([[250, 150], [550, 150], [600, 100], [300, 100]], np.int32)
    cv2.fillPoly(img, [pts_top], (200, 140, 120))
    cv2.polylines(img, [pts_top], True, (140, 100, 80), 2)

    # Right face
    pts_right = np.array([[550, 150], [600, 100], [600, 450], [550, 500]], np.int32)
    cv2.fillPoly(img, [pts_right], (160, 100, 80))
    cv2.polylines(img, [pts_right], True, (100, 60, 40), 2)

    # Label on front
    cv2.rectangle(img, (300, 250), (500, 350), (220, 220, 230), -1)
    cv2.rectangle(img, (300, 250), (500, 350), (100, 100, 110), 2)
    cv2.putText(img, "PRODUCT", (320, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 50), 2)

    cv2.imwrite(str(output_path), img)


def generate_surface_crack_image(output_path):
    """Generate a concrete surface with cracks"""
    print("Creating surface_crack.jpg...")
    img = np.ones((600, 800, 3), dtype=np.uint8) * 170  # Concrete gray

    # Add concrete texture
    noise = np.random.randint(-20, 20, (600, 800, 3), dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Main crack (zigzag pattern)
    points = [(100, 50), (150, 150), (120, 250), (180, 350), (150, 450), (200, 550)]
    for i in range(len(points) - 1):
        cv2.line(img, points[i], points[i+1], (60, 60, 60), 3)
        # Add branching
        if i % 2 == 0:
            branch_x = points[i][0] + np.random.randint(-30, 30)
            branch_y = points[i][1] + np.random.randint(30, 60)
            cv2.line(img, points[i], (branch_x, branch_y), (70, 70, 70), 2)

    # Secondary crack
    points2 = [(500, 100), (550, 200), (580, 300), (600, 400), (650, 500)]
    for i in range(len(points2) - 1):
        cv2.line(img, points2[i], points2[i+1], (65, 65, 65), 2)

    # Small cracks
    cv2.line(img, (300, 150), (380, 200), (75, 75, 75), 1)
    cv2.line(img, (400, 350), (480, 380), (75, 75, 75), 1)

    cv2.imwrite(str(output_path), img)


def generate_leaf_image(output_path):
    """Generate a leaf image for measurement"""
    print("Creating leaf.jpg...")
    img = np.ones((800, 600, 3), dtype=np.uint8) * 240  # Light background

    # Leaf shape (using ellipse and custom contour)
    # Main leaf body
    cv2.ellipse(img, (300, 400), (120, 200), 0, 0, 360, (80, 150, 60), -1)

    # Leaf edges (serrated)
    pts_left = []
    pts_right = []

    for i in range(15):
        t = i / 14.0
        y = 200 + int(t * 400)
        # Left side (serrated)
        x_left = 180 - int(np.sin(t * np.pi) * 120)
        offset = 10 if i % 2 == 0 else 0
        pts_left.append([x_left + offset, y])
        # Right side (serrated)
        x_right = 420 + int(np.sin(t * np.pi) * 120)
        pts_right.append([x_right - offset, y])

    # Create complete contour
    pts = np.array(pts_left + pts_right[::-1], np.int32)
    cv2.fillPoly(img, [pts], (80, 150, 60))
    cv2.polylines(img, [pts], True, (40, 90, 30), 2)

    # Central vein
    cv2.line(img, (300, 200), (300, 600), (50, 100, 40), 3)

    # Side veins
    for i in range(1, 8):
        y = 220 + i * 50
        length = 80 - abs(i - 4) * 15
        cv2.line(img, (300, y), (300 - length, y + 30), (50, 100, 40), 1)
        cv2.line(img, (300, y), (300 + length, y + 30), (50, 100, 40), 1)

    cv2.imwrite(str(output_path), img)


def generate_measure_image(output_path):
    """Generate objects for measurement"""
    print("Creating measure.jpg...")
    img = np.ones((600, 800, 3), dtype=np.uint8) * 230  # Light gray background

    # Reference ruler at bottom
    cv2.rectangle(img, (50, 550), (750, 580), (200, 200, 150), -1)
    cv2.rectangle(img, (50, 550), (750, 580), (100, 100, 80), 2)

    # Ruler markings (every 50 pixels = 1 cm)
    for i in range(15):
        x = 50 + i * 50
        height = 15 if i % 2 == 0 else 10
        cv2.line(img, (x, 580), (x, 580 - height), (100, 100, 80), 1)
        if i % 2 == 0:
            cv2.putText(img, str(i), (x-8, 575), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (80, 80, 60), 1)

    # Object 1: Rectangle
    cv2.rectangle(img, (100, 200), (300, 400), (100, 120, 180), -1)
    cv2.rectangle(img, (100, 200), (300, 400), (60, 80, 120), 2)

    # Object 2: Circle
    cv2.circle(img, (500, 300), 80, (180, 100, 100), -1)
    cv2.circle(img, (500, 300), 80, (120, 60, 60), 2)

    # Object 3: Triangle
    pts = np.array([[650, 450], [750, 450], [700, 300]], np.int32)
    cv2.fillPoly(img, [pts], (100, 180, 100))
    cv2.polylines(img, [pts], True, (60, 120, 60), 2)

    cv2.imwrite(str(output_path), img)


def generate_receipt_image(output_path):
    """Generate a receipt image for deskewing"""
    print("Creating receipt.jpg...")
    img = np.ones((800, 600, 3), dtype=np.uint8) * 80  # Dark background

    # Receipt paper (rotated)
    center = (300, 400)
    angle = -10
    width, height = 280, 600

    # Create receipt rectangle
    rect = cv2.boxPoints(((center[0], center[1]), (width, height), angle))
    rect = np.int0(rect)

    # White receipt paper
    cv2.fillPoly(img, [rect], (250, 250, 245))
    cv2.polylines(img, [rect], True, (200, 200, 200), 2)

    # Add receipt header
    header_y = -250
    for line_offset in [0, 30, 60]:
        y = header_y + line_offset
        start = rotate_point((200, y), center, angle)
        end = rotate_point((400, y), center, angle)
        cv2.line(img, start, end, (50, 50, 50), 2)

    # Add receipt items (lines)
    for i in range(12):
        y_offset = -150 + i * 40
        line_start = rotate_point((180, y_offset), center, angle)
        line_end = rotate_point((420, y_offset), center, angle)
        cv2.line(img, line_start, line_end, (80, 80, 80), 1)

    # Add total line (thicker)
    total_y = 250
    total_start = rotate_point((180, total_y), center, angle)
    total_end = rotate_point((420, total_y), center, angle)
    cv2.line(img, total_start, total_end, (50, 50, 50), 3)

    cv2.imwrite(str(output_path), img)


def main():
    """Main function to generate all sample images"""
    print("=" * 60)
    print("Generating Sample Images for Edge Detection Assignment")
    print("=" * 60)
    print()

    # Create output directory
    output_dir = create_output_dir()
    print(f"Output directory: {output_dir}")
    print()

    # Generate all images
    generators = [
        ("building.jpg", generate_building_image),
        ("doc.jpg", generate_document_image),
        ("road.jpg", generate_road_image),
        ("surface.jpg", generate_surface_image),
        ("coins.jpg", generate_coins_image),
        ("product.jpg", generate_product_image),
        ("surface_crack.jpg", generate_surface_crack_image),
        ("leaf.jpg", generate_leaf_image),
        ("measure.jpg", generate_measure_image),
        ("receipt.jpg", generate_receipt_image),
    ]

    total = len(generators)
    for idx, (filename, generator_func) in enumerate(generators, 1):
        output_path = output_dir / filename
        print(f"[{idx}/{total}] ", end="")
        generator_func(output_path)

    print()
    print("=" * 60)
    print(f"Successfully generated {total} sample images!")
    print(f"Images saved to: {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
