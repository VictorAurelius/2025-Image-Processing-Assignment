"""
=============================================================================
BÀI 9: PHÂN VÙNG CHUYỂN ĐỘNG (VIDEO) - FRAME DIFFERENCING & MOG2
=============================================================================
Đề bài: Đếm người/xe đi qua cổng bằng camera đứng yên.
Mục tiêu: So sánh phân đoạn chuyển động bằng sai khác khung và cv2.createBackgroundSubtractorMOG2.
Yêu cầu: Làm mượt, ngưỡng, mở/đóng hình thái học; vẽ bounding boxes.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T79-99 Phân vùng ảnh (trang 17-18)
=============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def create_sample_video(output_path, num_frames=50):
    """Tạo video mẫu với vật thể di chuyển."""
    width, height = 640, 480
    fps = 10

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for i in range(num_frames):
        # Tạo khung hình nền tĩnh
        frame = np.ones((height, width, 3), dtype=np.uint8) * 200

        # Vẽ nền cổng
        cv2.rectangle(frame, (0, 0), (width, 100), (150, 150, 150), -1)
        cv2.rectangle(frame, (0, 100), (50, height), (140, 140, 140), -1)
        cv2.rectangle(frame, (width-50, 100), (width, height), (140, 140, 140), -1)

        # Vật thể 1: Di chuyển từ trái sang phải
        x1 = int(50 + i * 10)
        if x1 < width - 50:
            cv2.rectangle(frame, (x1, 200), (x1+40, 250), (50, 50, 200), -1)

        # Vật thể 2: Di chuyển từ phải sang trái (chậm hơn)
        x2 = int(width - 100 - i * 7)
        if x2 > 50:
            cv2.circle(frame, (x2, 320), 25, (50, 200, 50), -1)

        # Vật thể 3: Di chuyển theo đường chéo
        if i > 10:
            x3 = int(100 + (i-10) * 8)
            y3 = int(150 + (i-10) * 5)
            if x3 < width - 50 and y3 < height - 50:
                cv2.rectangle(frame, (x3, y3), (x3+35, y3+35), (200, 50, 50), -1)

        # Thêm nhiễu nhẹ
        noise = np.random.randint(-5, 5, frame.shape, dtype=np.int16)
        frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        out.write(frame)

    out.release()
    print(f"Đã tạo video mẫu: {output_path}")


def process_video_motion_detection(video_path, output_frames_dir):
    """Xử lý video và phát hiện chuyển động."""
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Lỗi: Không thể mở video!")
        return

    # Tạo background subtractor MOG2
    bg = cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=25, detectShadows=True)

    prev = None
    frame_count = 0
    motion_stats = []

    os.makedirs(output_frames_dir, exist_ok=True)

    print("\nĐang xử lý video...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # Phương pháp 1: MOG2 Background Subtraction
        fg = bg.apply(frame)
        _, fgth = cv2.threshold(fg, 200, 255, cv2.THRESH_BINARY)
        fgth = cv2.morphologyEx(fgth, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)

        # Phương pháp 2: Frame Differencing
        if prev is None:
            prev = gray
            continue

        diff = cv2.absdiff(gray, prev)
        prev = gray
        _, diffth = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        diffth = cv2.morphologyEx(diffth, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

        # Tìm contours và vẽ bounding boxes
        contours_mog2, _ = cv2.findContours(fgth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_diff, _ = cv2.findContours(diffth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Vẽ bounding boxes trên frame
        frame_mog2 = frame.copy()
        frame_diff = frame.copy()

        num_objects_mog2 = 0
        num_objects_diff = 0

        for cnt in contours_mog2:
            if cv2.contourArea(cnt) > 500:  # Lọc nhiễu
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame_mog2, (x, y), (x+w, y+h), (0, 255, 0), 2)
                num_objects_mog2 += 1

        for cnt in contours_diff:
            if cv2.contourArea(cnt) > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame_diff, (x, y), (x+w, y+h), (0, 0, 255), 2)
                num_objects_diff += 1

        # Thống kê
        motion_stats.append({
            'frame': frame_count,
            'mog2_objects': num_objects_mog2,
            'diff_objects': num_objects_diff,
            'mog2_pixels': np.sum(fgth == 255),
            'diff_pixels': np.sum(diffth == 255)
        })

        # Lưu một số frame mẫu
        if frame_count % 10 == 0 or frame_count <= 5:
            # Tạo composite image
            combined = np.vstack([
                np.hstack([frame, cv2.cvtColor(fgth, cv2.COLOR_GRAY2BGR)]),
                np.hstack([frame_mog2, cv2.cvtColor(diffth, cv2.COLOR_GRAY2BGR)])
            ])

            # Thêm text
            cv2.putText(combined, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(combined, "MOG2 Mask", (frame.shape[1]+10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(combined, f"MOG2 ({num_objects_mog2} obj)", (10, frame.shape[0]+30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(combined, "Diff Mask", (frame.shape[1]+10, frame.shape[0]+30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            output_path = os.path.join(output_frames_dir, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(output_path, combined)

    cap.release()

    print(f"Đã xử lý {frame_count} frames")
    return motion_stats


def main():
    # Kiểm tra video input
    input_path = "../input/gate.mp4"

    if not os.path.exists(input_path):
        print("Không tìm thấy video input, tạo video mẫu...")
        os.makedirs("../input", exist_ok=True)
        create_sample_video(input_path, num_frames=50)

    print("\n" + "="*60)
    print("PHÂN VÙNG CHUYỂN ĐỘNG - MOTION SEGMENTATION")
    print("="*60)

    print(f"\nVideo input: {input_path}")

    # Xử lý video
    output_frames_dir = "output/frames"
    motion_stats = process_video_motion_detection(input_path, output_frames_dir)

    if motion_stats:
        print(f"\nThống kê chuyển động:")
        total_frames = len(motion_stats)

        avg_mog2_objects = np.mean([s['mog2_objects'] for s in motion_stats])
        avg_diff_objects = np.mean([s['diff_objects'] for s in motion_stats])
        avg_mog2_pixels = np.mean([s['mog2_pixels'] for s in motion_stats])
        avg_diff_pixels = np.mean([s['diff_pixels'] for s in motion_stats])

        print(f"  - Tổng số frames: {total_frames}")
        print(f"  - Số vật thể TB (MOG2): {avg_mog2_objects:.1f}")
        print(f"  - Số vật thể TB (Diff): {avg_diff_objects:.1f}")
        print(f"  - Pixels chuyển động TB (MOG2): {avg_mog2_pixels:.0f}")
        print(f"  - Pixels chuyển động TB (Diff): {avg_diff_pixels:.0f}")

        # Vẽ biểu đồ thống kê
        plt.figure(figsize=(14, 8))

        frames = [s['frame'] for s in motion_stats]
        mog2_objs = [s['mog2_objects'] for s in motion_stats]
        diff_objs = [s['diff_objects'] for s in motion_stats]
        mog2_pix = [s['mog2_pixels'] for s in motion_stats]
        diff_pix = [s['diff_pixels'] for s in motion_stats]

        plt.subplot(2, 2, 1)
        plt.plot(frames, mog2_objs, 'g-', linewidth=2, label='MOG2')
        plt.plot(frames, diff_objs, 'r--', linewidth=2, label='Frame Diff')
        plt.title("Số vật thể phát hiện theo frame", fontsize=12, fontweight='bold')
        plt.xlabel("Frame")
        plt.ylabel("Số vật thể")
        plt.legend()
        plt.grid(alpha=0.3)

        plt.subplot(2, 2, 2)
        plt.plot(frames, mog2_pix, 'g-', linewidth=2, label='MOG2')
        plt.plot(frames, diff_pix, 'r--', linewidth=2, label='Frame Diff')
        plt.title("Số pixels chuyển động theo frame", fontsize=12, fontweight='bold')
        plt.xlabel("Frame")
        plt.ylabel("Số pixels")
        plt.legend()
        plt.grid(alpha=0.3)

        plt.subplot(2, 2, 3)
        plt.hist([mog2_objs, diff_objs], bins=10, label=['MOG2', 'Frame Diff'],
                color=['green', 'red'], alpha=0.6)
        plt.title("Phân bố số vật thể", fontsize=12, fontweight='bold')
        plt.xlabel("Số vật thể")
        plt.ylabel("Tần suất")
        plt.legend()
        plt.grid(alpha=0.3)

        plt.subplot(2, 2, 4)
        methods = ['MOG2', 'Frame Diff']
        avg_objects = [avg_mog2_objects, avg_diff_objects]
        colors = ['green', 'red']
        plt.bar(methods, avg_objects, color=colors, alpha=0.7)
        plt.title("So sánh số vật thể TB", fontsize=12, fontweight='bold')
        plt.ylabel("Số vật thể")
        plt.grid(alpha=0.3)

        plt.tight_layout()

        # Lưu biểu đồ
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        stats_path = os.path.join(output_dir, "motion_statistics.png")
        plt.savefig(stats_path, dpi=150, bbox_inches='tight')
        print(f"\nĐã lưu biểu đồ thống kê tại: {stats_path}")

        plt.show()

        # Hiển thị một số frame mẫu
        print(f"\nCác frame mẫu đã lưu tại: {output_frames_dir}/")

        print("\nNhận xét:")
        print("  - MOG2: Phù hợp cho phát hiện chuyển động trong thời gian dài")
        print("  - Frame Diff: Đơn giản, nhanh nhưng nhạy với nhiễu")
        print("  - MOG2 xử lý bóng tốt hơn (detectShadows=True)")
        print("  - Frame Diff phát hiện chuyển động nhanh tốt hơn")

    print("\n" + "="*60)
    print("HOÀN THÀNH!")
    print("="*60)


if __name__ == "__main__":
    main()
