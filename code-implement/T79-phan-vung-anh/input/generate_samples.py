"""
Script tạo tất cả ảnh và video mẫu cho 10 bài tập T79
"""

import cv2
import numpy as np
import sys
import os

# Thêm đường dẫn để import từ các bài tập
sys.path.append('..')


def create_all_samples():
    """Tạo tất cả ảnh và video mẫu."""

    print("="*60)
    print("TẠO TẤT CẢ ẢNH VÀ VIDEO MẪU CHO T79")
    print("="*60)

    samples_created = []

    # Import và tạo ảnh từ mỗi module
    try:
        # Bài 1: Conveyor
        from bai_1_global_thresholding.threshold import create_sample_image as create_conveyor
        img = create_conveyor()
        cv2.imwrite("conveyor.jpg", img)
        samples_created.append("conveyor.jpg")
        print("✓ Đã tạo: conveyor.jpg")
    except Exception as e:
        print(f"✗ Lỗi tạo conveyor.jpg: {e}")

    try:
        # Bài 2: Parts
        from bai_2_otsu.threshold import create_sample_image as create_parts
        img = create_parts()
        cv2.imwrite("parts.jpg", img)
        samples_created.append("parts.jpg")
        print("✓ Đã tạo: parts.jpg")
    except Exception as e:
        print(f"✗ Lỗi tạo parts.jpg: {e}")

    try:
        # Bài 3: Receipt
        from bai_3_adaptive_thresholding.threshold import create_sample_receipt
        img = create_sample_receipt()
        cv2.imwrite("receipt.jpg", img)
        samples_created.append("receipt.jpg")
        print("✓ Đã tạo: receipt.jpg")
    except Exception as e:
        print(f"✗ Lỗi tạo receipt.jpg: {e}")

    try:
        # Bài 4: Steel rust
        from bai_4_bayes_ml.threshold import create_sample_image as create_steel
        img = create_steel()
        cv2.imwrite("steel_rust.jpg", img)
        samples_created.append("steel_rust.jpg")
        print("✓ Đã tạo: steel_rust.jpg")
    except Exception as e:
        print(f"✗ Lỗi tạo steel_rust.jpg: {e}")

    try:
        # Bài 5: Lanes
        from bai_5_edge_hough.detect import create_sample_image as create_lanes
        img = create_lanes()
        cv2.imwrite("lanes.jpg", img)
        samples_created.append("lanes.jpg")
        print("✓ Đã tạo: lanes.jpg")
    except Exception as e:
        print(f"✗ Lỗi tạo lanes.jpg: {e}")

    try:
        # Bài 6: Ultrasound
        from bai_6_region_growing.grow import create_sample_image as create_ultrasound
        img = create_ultrasound()
        cv2.imwrite("ultrasound.png", img)
        samples_created.append("ultrasound.png")
        print("✓ Đã tạo: ultrasound.png")
    except Exception as e:
        print(f"✗ Lỗi tạo ultrasound.png: {e}")

    try:
        # Bài 7: Landscape
        from bai_7_split_merge.segment import create_sample_landscape
        img = create_sample_landscape()
        cv2.imwrite("landscape.jpg", img)
        samples_created.append("landscape.jpg")
        print("✓ Đã tạo: landscape.jpg")
    except Exception as e:
        print(f"✗ Lỗi tạo landscape.jpg: {e}")

    try:
        # Bài 8: Satellite
        from bai_8_kmeans.cluster import create_sample_satellite
        img = create_sample_satellite()
        cv2.imwrite("satellite.jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        samples_created.append("satellite.jpg")
        print("✓ Đã tạo: satellite.jpg")
    except Exception as e:
        print(f"✗ Lỗi tạo satellite.jpg: {e}")

    try:
        # Bài 9: Video
        from bai_9_motion_segmentation.segment import create_sample_video
        create_sample_video("gate.mp4", num_frames=50)
        samples_created.append("gate.mp4")
        print("✓ Đã tạo: gate.mp4")
    except Exception as e:
        print(f"✗ Lỗi tạo gate.mp4: {e}")

    try:
        # Bài 10: Coins
        from bai_10_watershed.segment import create_sample_coins
        img = create_sample_coins()
        cv2.imwrite("coins.png", img)
        samples_created.append("coins.png")
        print("✓ Đã tạo: coins.png")
    except Exception as e:
        print(f"✗ Lỗi tạo coins.png: {e}")

    print("\n" + "="*60)
    print(f"HOÀN THÀNH! Đã tạo {len(samples_created)}/{10} files")
    print("="*60)

    if samples_created:
        print("\nCác file đã tạo:")
        for f in samples_created:
            print(f"  - {f}")


if __name__ == "__main__":
    create_all_samples()
